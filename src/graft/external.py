"""Delegate *external* skills (owner/repo sources) to the vercel `skills` CLI.

We do not vendor third-party skills into the vault; the profile records the source
and `npx skills add` performs the install, keeping its own `.skill-lock.json`.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


class ExternalError(RuntimeError):
    pass


def skills_cli_available() -> bool:
    return shutil.which("npx") is not None


def build_add_command(
    source: str, skill_names: list[str], agents: list[str], *, global_scope: bool
) -> list[str]:
    cmd = ["npx", "-y", "skills@latest", "add", source]
    for name in skill_names:
        cmd += ["--skill", name]
    for agent in agents:
        cmd += ["--agent", agent]
    if global_scope:
        cmd.append("--global")
    cmd.append("--yes")
    return cmd


def run_add(
    source: str,
    skill_names: list[str],
    agents: list[str],
    *,
    global_scope: bool,
    cwd: Path | None,
    dry_run: bool,
) -> list[str]:
    cmd = build_add_command(source, skill_names, agents, global_scope=global_scope)
    if dry_run:
        return cmd
    if not skills_cli_available():
        raise ExternalError("`npx` not found; install Node.js to manage external skills")
    result = subprocess.run(cmd, cwd=cwd, check=False)
    if result.returncode != 0:
        raise ExternalError(f"`{' '.join(cmd)}` exited with {result.returncode}")
    return cmd
