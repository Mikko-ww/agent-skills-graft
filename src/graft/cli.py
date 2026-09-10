"""graft command line."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from . import __version__, engine, platforms
from .engine import State
from .importer import discover_skill_dirs, import_skill
from .profile import Profile, ProfileError, resolve_profile_path
from .vault import Vault, find_root

app = typer.Typer(
    help="Keep one vault of agent skills; graft them onto Claude Code, Codex, Cursor, pi, ...",
    rich_markup_mode="rich",
)
console = Console()
err = Console(stderr=True)

_STATE_STYLE = {
    State.OK: "green",
    State.LINK: "cyan",
    State.RELINK: "yellow",
    State.ADOPT: "cyan",
    State.CONFLICT: "red",
    State.EXTERNAL_MISSING: "magenta",
    State.ORPHAN: "yellow",
    State.NOT_IN_VAULT: "red",
    State.ERROR: "red",
}

ProfileArg = Annotated[
    str,
    typer.Argument(
        help="'global', a project profile name (profiles/projects/<name>.yaml), or a path"
    ),
]


def _load(profile_name: str) -> tuple[Vault, Profile]:
    vault = Vault(find_root())
    try:
        profile = Profile.load(resolve_profile_path(vault.root, profile_name))
    except (ProfileError, KeyError) as exc:
        err.print(f"[red]error:[/red] {exc}")
        raise typer.Exit(2)
    return vault, profile


def _short(path: Path) -> str:
    home = str(Path.home())
    text = str(path)
    return "~" + text[len(home) :] if text.startswith(home) else text


def _render(report: engine.Report, *, title: str, verbose: bool) -> None:
    table = Table(title=title, show_lines=False, expand=True)
    table.add_column("skill", overflow="fold")
    table.add_column("platform")
    table.add_column("state")
    table.add_column("link", overflow="fold")
    table.add_column("note", overflow="fold")
    for action in sorted(report.actions, key=lambda a: (a.skill, a.platform)):
        if action.state is State.OK and not verbose:
            continue
        style = _STATE_STYLE[action.state]
        table.add_row(
            action.skill,
            action.platform,
            f"[{style}]{action.state.value}[/{style}]",
            _short(action.link),
            action.note or (action.source or ""),
        )
    if table.row_count:
        console.print(table)
    ok = len(report.by_state(State.OK))
    console.print(f"[green]{ok} ok[/green]", end="")
    for state in State:
        if state is State.OK:
            continue
        n = len(report.by_state(state))
        if n:
            console.print(
                f" · [{_STATE_STYLE[state]}]{n} {state.value}[/{_STATE_STYLE[state]}]", end=""
            )
    console.print()


@app.callback(invoke_without_command=True)
def _main(
    ctx: typer.Context,
    version: Annotated[bool, typer.Option("--version", is_eager=True)] = False,
) -> None:
    if version:
        console.print(f"graft {__version__}")
        raise typer.Exit()
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())
        raise typer.Exit()


@app.command()
def status(
    profile: ProfileArg = "global",
    verbose: Annotated[bool, typer.Option("-v", "--verbose", help="also list OK rows")] = False,
) -> None:
    """Compare a profile with what is actually on disk. Changes nothing."""
    vault, prof = _load(profile)
    report = engine.plan(vault, prof)
    _render(report, title=f"graft status · {prof.path.name}", verbose=verbose)
    raise typer.Exit(1 if report.needs_work else 0)


@app.command()
def apply(
    profile: ProfileArg = "global",
    dry_run: Annotated[bool, typer.Option("-n", "--dry-run", help="show, don't touch")] = False,
    force: Annotated[
        bool, typer.Option("--force", help="back up conflicting copies and relink")
    ] = False,
    prune: Annotated[
        bool, typer.Option("--prune", help="remove vault symlinks not in profile")
    ] = False,
    no_external: Annotated[
        bool, typer.Option("--no-external", help="skip `npx skills add`")
    ] = False,
    verbose: Annotated[bool, typer.Option("-v", "--verbose")] = False,
) -> None:
    """Make the filesystem match the profile (idempotent)."""
    vault, prof = _load(profile)
    try:
        report = engine.apply(
            vault, prof, dry_run=dry_run, force=force, prune=prune, skip_external=no_external
        )
    except engine.external.ExternalError as exc:
        err.print(f"[red]external install failed:[/red] {exc}")
        raise typer.Exit(1)
    label = "dry-run" if dry_run else "applied"
    _render(report, title=f"graft apply ({label}) · {prof.path.name}", verbose=verbose)
    for cmd in report.external_commands:
        prefix = "[magenta]would run[/magenta]" if dry_run else "[magenta]ran[/magenta]"
        console.print(f"{prefix}: {' '.join(cmd)}")
    conflicts = report.by_state(State.CONFLICT)
    if conflicts and not force:
        err.print(f"[red]{len(conflicts)} conflict(s)[/red] — inspect, then re-run with --force")
        raise typer.Exit(1)
    if report.by_state(State.NOT_IN_VAULT, State.ERROR):
        raise typer.Exit(1)


@app.command("import")
def import_(
    paths: Annotated[list[Path], typer.Argument(help="skill dir(s) or a dir of skills")],
    profile: Annotated[str, typer.Option("-p", "--profile")] = "global",
    source: Annotated[
        Optional[str], typer.Option("--source", help="treat as external, e.g. openai/skills")
    ] = None,
    to: Annotated[
        Optional[str], typer.Option("--to", help="comma-separated platforms; default: inferred")
    ] = None,
    rename: Annotated[
        Optional[str], typer.Option("--rename", help="store under a new name")
    ] = None,
    dry_run: Annotated[bool, typer.Option("-n", "--dry-run")] = False,
) -> None:
    """Adopt loose skills from ~/.codex/skills, ~/.agents/skills, ... into the vault + profile."""
    vault, prof = _load(profile)
    targets = [t.strip() for t in to.split(",")] if to else None
    skill_dirs = [d for p in paths for d in discover_skill_dirs(p)]
    if not skill_dirs:
        err.print("[red]no SKILL.md found under the given path(s)[/red]")
        raise typer.Exit(1)
    if rename and len(skill_dirs) > 1:
        err.print("[red]--rename only makes sense with a single skill[/red]")
        raise typer.Exit(2)

    table = Table(title=f"graft import{' (dry-run)' if dry_run else ''}")
    table.add_column("path")
    table.add_column("name")
    table.add_column("outcome")
    table.add_column("detail")
    for skill_dir in skill_dirs:
        result = import_skill(
            vault, prof, skill_dir, source=source, to=targets, rename=rename, dry_run=dry_run
        )
        style = {"conflict": "red", "skipped": "yellow"}.get(result.outcome, "green")
        table.add_row(
            _short(result.path), result.name, f"[{style}]{result.outcome}[/{style}]", result.detail
        )
    console.print(table)
    if not dry_run:
        console.print(f"profile updated: {_short(prof.path)} — run [bold]graft apply[/bold] next")


@app.command("platforms")
def platforms_cmd() -> None:
    """List known platforms and where they read global skills from."""
    table = Table(title="platforms")
    table.add_column("id")
    table.add_column("label")
    table.add_column("project dir")
    table.add_column("global dir")
    table.add_column("exists")
    for p in platforms.PLATFORMS.values():
        g = p.global_skills_dir()
        table.add_row(p.id, p.label, p.project_skills_dir, _short(g), "yes" if g.is_dir() else "-")
    console.print(table)


@app.command("skills")
def skills_cmd() -> None:
    """List skills in the vault."""
    vault = Vault(find_root())
    table = Table(title=f"vault skills · {_short(vault.skills_dir)}")
    table.add_column("dir")
    table.add_column("name")
    for dir_name, skill in vault.skills().items():
        table.add_row(dir_name, skill.name if skill.name != dir_name else "")
    console.print(table)


if __name__ == "__main__":
    app()
