"""Platform registry: where each agent platform reads skills from.

IDs deliberately match the `--agent` names used by the vercel `skills` CLI so the
same identifier can be passed straight through when we delegate external installs.
Paths follow https://github.com/vercel-labs/skills (src/agents.ts).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Platform:
    id: str
    label: str
    project_skills_dir: str  # relative to a project root
    _global_skills_dir: str  # may contain ${VAR:-default} style tokens, expanded at runtime

    def global_skills_dir(self) -> Path:
        return _expand(self._global_skills_dir)

    def skills_dir(self, project: Path | None = None) -> Path:
        if project is None:
            return self.global_skills_dir()
        return project / self.project_skills_dir


def _expand(template: str) -> Path:
    home = Path.home()
    xdg_config = Path(os.environ.get("XDG_CONFIG_HOME") or home / ".config")
    claude_home = Path(os.environ.get("CLAUDE_CONFIG_DIR") or home / ".claude")
    codex_home = Path(os.environ.get("CODEX_HOME") or home / ".codex")
    value = (
        template.replace("$HOME", str(home))
        .replace("$XDG_CONFIG_HOME", str(xdg_config))
        .replace("$CLAUDE_HOME", str(claude_home))
        .replace("$CODEX_HOME", str(codex_home))
    )
    return Path(value)


_PLATFORMS: tuple[Platform, ...] = (
    Platform("claude-code", "Claude Code", ".claude/skills", "$CLAUDE_HOME/skills"),
    Platform("codex", "Codex", ".agents/skills", "$CODEX_HOME/skills"),
    Platform("cursor", "Cursor", ".agents/skills", "$HOME/.cursor/skills"),
    Platform("opencode", "OpenCode", ".agents/skills", "$XDG_CONFIG_HOME/opencode/skills"),
    Platform("pi", "pi", ".pi/skills", "$HOME/.pi/agent/skills"),
    Platform("gemini-cli", "Gemini CLI", ".agents/skills", "$HOME/.gemini/skills"),
    Platform("antigravity", "Antigravity", ".agents/skills", "$HOME/.gemini/antigravity/skills"),
    Platform("github-copilot", "GitHub Copilot", ".agents/skills", "$HOME/.copilot/skills"),
    # Canonical dir used by the vercel `skills` CLI and read by amp/cline/zed/...
    Platform("universal", "Universal (.agents)", ".agents/skills", "$HOME/.agents/skills"),
)

PLATFORMS: dict[str, Platform] = {p.id: p for p in _PLATFORMS}


def get(platform_id: str) -> Platform:
    try:
        return PLATFORMS[platform_id]
    except KeyError:
        known = ", ".join(PLATFORMS)
        raise KeyError(f"unknown platform '{platform_id}' (known: {known})") from None


def detect_from_path(path: Path) -> Platform | None:
    """Return the platform whose *global* skills dir contains `path`, if any."""
    resolved = path.expanduser().absolute()
    for platform in _PLATFORMS:
        base = platform.global_skills_dir().absolute()
        try:
            resolved.relative_to(base)
        except ValueError:
            continue
        return platform
    return None
