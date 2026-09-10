"""The vault: this repository, the single source of truth for our own assets."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

SKILL_FILE = "SKILL.md"
_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
_NAME_RE = re.compile(r"^name:\s*[\"']?([^\"'\n]+?)[\"']?\s*$", re.MULTILINE)


def find_root(start: Path | None = None) -> Path:
    """Locate the vault root.

    Order: $GRAFT_HOME, then walk up from `start` (cwd) looking for `profiles/`
    next to `skills/`, then fall back to the repository this package lives in.
    """
    env = os.environ.get("GRAFT_HOME")
    if env:
        return Path(env).expanduser().resolve()
    here = (start or Path.cwd()).resolve()
    for candidate in (here, *here.parents):
        if (candidate / "profiles").is_dir() and (candidate / "skills").is_dir():
            return candidate
    return Path(__file__).resolve().parents[2]


def skill_name_from_frontmatter(skill_md: Path) -> str | None:
    try:
        text = skill_md.read_text(encoding="utf-8")
    except OSError:
        return None
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return None
    name = _NAME_RE.search(match.group(1))
    return name.group(1).strip() if name else None


@dataclass(frozen=True)
class Skill:
    name: str
    path: Path

    @property
    def skill_md(self) -> Path:
        return self.path / SKILL_FILE


class Vault:
    def __init__(self, root: Path):
        self.root = root

    @property
    def skills_dir(self) -> Path:
        return self.root / "skills"

    @property
    def profiles_dir(self) -> Path:
        return self.root / "profiles"

    def skills(self) -> dict[str, Skill]:
        found: dict[str, Skill] = {}
        if not self.skills_dir.is_dir():
            return found
        for entry in sorted(self.skills_dir.iterdir()):
            if not entry.is_dir() or entry.name.startswith("."):
                continue
            skill_md = entry / SKILL_FILE
            if not skill_md.is_file():
                continue
            name = skill_name_from_frontmatter(skill_md) or entry.name
            found[entry.name] = Skill(name=name, path=entry)
        return found

    def skill(self, dir_name: str) -> Skill | None:
        return self.skills().get(dir_name)

    def contains(self, path: Path) -> bool:
        """True if `path` (after resolving symlinks) lives under the vault's skills dir."""
        try:
            path.resolve().relative_to(self.skills_dir.resolve())
            return True
        except (ValueError, OSError):
            return False
