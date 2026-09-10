"""Small filesystem helpers: symlinks, backups, directory equality."""

from __future__ import annotations

import filecmp
import os
import shutil
from datetime import datetime
from pathlib import Path

IGNORED_NAMES = {".DS_Store", "__pycache__", ".git"}


def backup_root() -> Path:
    base = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local" / "share")
    return base / "graft" / "backup"


_session_stamp: str | None = None


def backup(path: Path, label: str) -> Path:
    """Move `path` into a timestamped backup folder and return the new location."""
    global _session_stamp
    if _session_stamp is None:
        _session_stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest_dir = backup_root() / _session_stamp / label
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / path.name
    if dest.exists() or dest.is_symlink():
        dest = dest_dir / f"{path.name}.{datetime.now().strftime('%f')}"
    shutil.move(str(path), str(dest))
    return dest


def dirs_equal(a: Path, b: Path) -> bool:
    """Recursive content comparison ignoring IGNORED_NAMES."""
    cmp = filecmp.dircmp(a, b, ignore=list(IGNORED_NAMES))
    if cmp.left_only or cmp.right_only or cmp.diff_files or cmp.funny_files:
        return False
    return all(dirs_equal(a / sub, b / sub) for sub in cmp.common_dirs)


def points_to(link: Path, target: Path) -> bool:
    if not link.is_symlink():
        return False
    try:
        return link.resolve() == target.resolve()
    except OSError:
        return False


def make_symlink(link: Path, target: Path) -> None:
    link.parent.mkdir(parents=True, exist_ok=True)
    if link.is_symlink():
        link.unlink()
    os.symlink(str(target.resolve()), str(link))


def remove_link_or_backup(path: Path, label: str) -> Path | None:
    """Symlinks are simply unlinked; real files/dirs are moved to the backup area."""
    if path.is_symlink():
        path.unlink()
        return None
    if path.exists():
        return backup(path, label)
    return None
