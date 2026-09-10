"""计划与执行：把清单和文件系统做对比，并修正差异。

刻意设计为无状态：一个链接“被 graft 管理”当且仅当它是 symlink 且解析后落在金库的
skills 目录内。因此不需要 lock 文件就能检测漂移和孤儿链接。
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from . import external, fsutil, platforms
from .profile import Profile, SkillSpec
from .vault import Vault


class State(str, Enum):
    OK = "ok"  # already linked to the vault / external already present
    LINK = "link"  # nothing there yet -> create symlink
    RELINK = "relink"  # symlink exists but points elsewhere / is broken
    ADOPT = "adopt"  # real copy identical to vault -> swap for symlink (safe)
    CONFLICT = "conflict"  # real copy differs from vault -> needs --force
    EXTERNAL_MISSING = "external-missing"  # delegate to `npx skills add`
    ORPHAN = "orphan"  # vault symlink no longer declared in profile
    NOT_IN_VAULT = "not-in-vault"  # profile names a vault skill that does not exist
    ERROR = "error"  # filesystem operation failed (permissions, ...)


@dataclass
class Action:
    state: State
    skill: str
    platform: str
    link: Path
    target: Path | None = None
    source: str | None = None
    note: str = ""


@dataclass
class Report:
    actions: list[Action] = field(default_factory=list)
    external_commands: list[list[str]] = field(default_factory=list)

    def by_state(self, *states: State) -> list[Action]:
        return [a for a in self.actions if a.state in states]

    @property
    def needs_work(self) -> bool:
        return any(a.state is not State.OK for a in self.actions)


def _scope_dir(platform_id: str, project: Path | None) -> Path:
    return platforms.get(platform_id).skills_dir(project)


def plan(vault: Vault, profile: Profile) -> Report:
    report = Report()
    vault_skills = vault.skills()
    project = profile.project
    declared: dict[str, set[str]] = defaultdict(set)  # platform -> skill names

    for spec in profile.skills.values():
        for platform_id in spec.to:
            declared[platform_id].add(spec.name)
            link = _scope_dir(platform_id, project) / spec.name
            if spec.is_external:
                report.actions.append(_plan_external(spec, platform_id, link))
            else:
                report.actions.append(_plan_vault(spec, platform_id, link, vault_skills))

    for platform_id in profile.targets:
        base = _scope_dir(platform_id, project)
        if not base.is_dir():
            continue
        for entry in sorted(base.iterdir()):
            if not entry.is_symlink() or not vault.contains(entry):
                continue
            if entry.name in declared[platform_id]:
                continue
            report.actions.append(
                Action(State.ORPHAN, entry.name, platform_id, entry, note="清单中未声明")
            )
    return report


def _plan_vault(spec: SkillSpec, platform_id: str, link: Path, vault_skills) -> Action:
    skill = vault_skills.get(spec.name)
    if skill is None:
        return Action(
            State.NOT_IN_VAULT, spec.name, platform_id, link, note="金库 skills/ 中不存在"
        )
    target = skill.path
    if link.is_symlink():
        if fsutil.points_to(link, target):
            return Action(State.OK, spec.name, platform_id, link, target)
        return Action(State.RELINK, spec.name, platform_id, link, target, note=_describe(link))
    if link.exists():
        if link.is_dir() and fsutil.dirs_equal(link, target):
            return Action(
                State.ADOPT, spec.name, platform_id, link, target, note="内容与金库一致的真实目录"
            )
        return Action(
            State.CONFLICT, spec.name, platform_id, link, target, note="真实目录，内容与金库不同"
        )
    return Action(State.LINK, spec.name, platform_id, link, target)


def _plan_external(spec: SkillSpec, platform_id: str, link: Path) -> Action:
    if link.exists() or link.is_symlink():
        return Action(State.OK, spec.name, platform_id, link, source=spec.source)
    return Action(State.EXTERNAL_MISSING, spec.name, platform_id, link, source=spec.source)


def _describe(link: Path) -> str:
    try:
        return f"当前指向 {link.readlink()}"
    except OSError:
        return "断链"


def _execute(action: Action, *, dry_run: bool, force: bool, prune: bool) -> None:
    if action.state in (State.LINK, State.RELINK, State.ADOPT):
        if dry_run:
            return
        if action.state is State.ADOPT:
            fsutil.backup(action.link, action.platform)
        fsutil.make_symlink(action.link, action.target)  # type: ignore[arg-type]
    elif action.state is State.CONFLICT and force:
        if dry_run:
            action.note = "将备份后重新建链（--force）"
            return
        moved = fsutil.backup(action.link, action.platform)
        action.note = f"已备份到 {moved}"
        fsutil.make_symlink(action.link, action.target)  # type: ignore[arg-type]
    elif action.state is State.ORPHAN and prune:
        if not dry_run:
            action.link.unlink()
        action.note = "已删除"


def apply(
    vault: Vault,
    profile: Profile,
    *,
    dry_run: bool = False,
    force: bool = False,
    prune: bool = False,
    skip_external: bool = False,
) -> Report:
    report = plan(vault, profile)
    project = profile.project

    for action in report.actions:
        try:
            _execute(action, dry_run=dry_run, force=force, prune=prune)
        except OSError as exc:
            action.state = State.ERROR
            action.note = f"{exc.strerror or exc}: {exc.filename or action.link}"

    if not skip_external:
        grouped: dict[tuple[str, str], set[str]] = defaultdict(set)  # (source, skill) -> agents
        for action in report.by_state(State.EXTERNAL_MISSING):
            grouped[(action.source or "", action.skill)].add(action.platform)
        for (source, skill), agents in sorted(grouped.items()):
            cmd = external.run_add(
                source,
                [skill],
                sorted(agents),
                global_scope=project is None,
                cwd=project,
                dry_run=dry_run,
            )
            report.external_commands.append(cmd)
    return report
