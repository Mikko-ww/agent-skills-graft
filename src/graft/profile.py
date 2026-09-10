"""Declarative profiles: *what* goes *where*.

    # profiles/global.yaml
    targets: [claude-code, codex, cursor]

    skills:
      searching-github-projects: { to: [codex, cursor] }   # vault skill
      mcp-builder: { to: "*" }                             # "*" = every target
      frontend-design:                                     # external skill
        source: anthropics/skills                          #   -> npx skills add
        to: [cursor, claude-code]
      pdf: [codex]                                         # shorthand for { to: [codex] }

Profiles are edited with ruamel.yaml so comments survive `graft import` write-backs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq

from . import platforms

_yaml = YAML()
_yaml.preserve_quotes = True
_yaml.indent(mapping=2, sequence=4, offset=2)
_yaml.width = 120


class ProfileError(ValueError):
    pass


@dataclass
class SkillSpec:
    name: str
    to: list[str]
    source: str | None = None  # None -> lives in the vault; "owner/repo" -> external

    @property
    def is_external(self) -> bool:
        return self.source is not None


@dataclass
class Profile:
    path: Path
    targets: list[str]
    skills: dict[str, SkillSpec] = field(default_factory=dict)
    project: Path | None = None
    _doc: CommentedMap = field(default_factory=CommentedMap, repr=False)

    # ---- loading -------------------------------------------------------

    @classmethod
    def load(cls, path: Path) -> "Profile":
        if not path.is_file():
            raise ProfileError(f"profile not found: {path}")
        with path.open(encoding="utf-8") as fh:
            doc = _yaml.load(fh) or CommentedMap()
        if not isinstance(doc, dict):
            raise ProfileError(f"{path}: top level must be a mapping")

        targets = list(doc.get("targets") or [])
        if not targets:
            raise ProfileError(f"{path}: 'targets' must list at least one platform")
        for target in targets:
            platforms.get(target)  # raises on unknown

        project = doc.get("path")
        project_path = Path(str(project)).expanduser() if project else None

        skills: dict[str, SkillSpec] = {}
        for name, raw in (doc.get("skills") or {}).items():
            skills[str(name)] = _parse_skill(str(name), raw, targets, path)

        return cls(path=path, targets=targets, skills=skills, project=project_path, _doc=doc)

    # ---- mutation (used by `graft import`) -------------------------------

    def add_skill(self, spec: SkillSpec, *, replace: bool = False) -> bool:
        """Add `spec` to the in-memory document. Returns False if it already existed."""
        skills_node = self._doc.get("skills")
        if skills_node is None:
            skills_node = CommentedMap()
            self._doc["skills"] = skills_node
        if spec.name in skills_node and not replace:
            return False
        entry = CommentedMap()
        if spec.source:
            entry["source"] = spec.source
        to_node = CommentedSeq(spec.to)
        to_node.fa.set_flow_style()
        entry["to"] = to_node
        if not spec.source:
            entry.fa.set_flow_style()  # vault skills render compactly: name: { to: [...] }
        skills_node[spec.name] = entry
        self.skills[spec.name] = spec
        return True

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as fh:
            _yaml.dump(self._doc, fh)


def _parse_skill(name: str, raw: Any, targets: list[str], path: Path) -> SkillSpec:
    source: str | None = None
    if raw is None or raw == "*":
        to_raw: Any = "*"
    elif isinstance(raw, str):
        to_raw = [raw]
    elif isinstance(raw, list):
        to_raw = raw
    elif isinstance(raw, dict):
        to_raw = raw.get("to", "*")
        source = raw.get("source")
        unknown = set(raw) - {"to", "source"}
        if unknown:
            raise ProfileError(f"{path}: skill '{name}' has unknown keys {sorted(unknown)}")
    else:
        raise ProfileError(f"{path}: skill '{name}' has an unsupported value {raw!r}")

    if to_raw == "*":
        to = list(targets)
    elif isinstance(to_raw, str):
        to = [to_raw]
    else:
        to = [str(t) for t in to_raw]

    for target in to:
        platforms.get(target)
        if target not in targets:
            raise ProfileError(
                f"{path}: skill '{name}' targets '{target}' which is not in 'targets'"
            )
    return SkillSpec(name=name, to=to, source=str(source) if source else None)


def resolve_profile_path(vault_root: Path, name: str) -> Path:
    """`global` -> profiles/global.yaml, `foo` -> profiles/projects/foo.yaml, or a literal path."""
    literal = Path(name).expanduser()
    if literal.suffix in {".yaml", ".yml"} and literal.exists():
        return literal
    if name == "global":
        return vault_root / "profiles" / "global.yaml"
    return vault_root / "profiles" / "projects" / f"{name}.yaml"
