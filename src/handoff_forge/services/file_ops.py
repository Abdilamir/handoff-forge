"""
All filesystem I/O for handoff-forge lives here.
No other module reads or writes files directly.
"""

import shutil
from datetime import datetime
from pathlib import Path


def read_file(path: Path) -> str | None:
    """Return file contents as a string, or None if the file does not exist."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None


def backup_file(path: Path) -> Path:
    """
    Copy an existing file to <stem>.bak.<YYYYMMDD-HHMMSS><suffix>.
    Returns the backup path. Raises FileNotFoundError if source does not exist.
    """
    if not path.exists():
        raise FileNotFoundError(f"Cannot back up non-existent file: {path}")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = path.with_name(f"{path.stem}.bak.{timestamp}{path.suffix}")
    shutil.copy2(path, backup_path)
    return backup_path


def write_file(path: Path, content: str, *, overwrite: bool = False) -> Path:
    """
    Write content to path.

    If the file exists and overwrite=False, raises FileExistsError.
    If the file exists and overwrite=True, backs it up before writing.
    Creates parent directories if they do not exist.

    Returns the path written to.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        if not overwrite:
            raise FileExistsError(
                f"{path} already exists. Use overwrite=True to replace it "
                f"(a backup will be created automatically)."
            )
        backup_file(path)

    path.write_text(content, encoding="utf-8")
    return path


def ensure_directory(path: Path) -> Path:
    """Create directory and all parents if they do not exist. Returns the path."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def file_exists(path: Path) -> bool:
    return Path(path).exists()
