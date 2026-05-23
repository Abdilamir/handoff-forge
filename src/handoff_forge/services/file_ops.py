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


def write_file(path: Path, content: str, *, overwrite: bool = False, backup: bool = True) -> Path:
    """
    Write content to path.

    If the file exists and overwrite=False, raises FileExistsError.
    If the file exists and overwrite=True, backs it up before writing unless backup=False.
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
        if backup:
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


def check_required_files(directory: Path, required: list[str]) -> dict[str, bool]:
    """
    Check which required filenames exist directly inside directory.
    Returns a dict mapping each filename to True (present) or False (missing).
    Does not recurse into subdirectories.
    """
    directory = Path(directory)
    return {name: (directory / name).exists() for name in required}


def insert_task_entry(content: str, entry: str) -> str:
    """
    Insert a task entry at the end of the first non-TASK-FORMAT ## section.

    Finds the first ## header that is not '## TASK FORMAT', then locates
    the end of that section (the next ## header, a --- separator, or EOF).
    Inserts entry after the last non-blank line of that section.

    If no eligible ## section exists, appends entry to end of content.
    """
    lines = content.splitlines(keepends=True)
    section_starts = [
        i for i, line in enumerate(lines)
        if line.startswith("## ") and not line.startswith("## TASK FORMAT")
    ]
    if not section_starts:
        return content.rstrip() + f"\n{entry}\n"
    first_end = len(lines)
    for i in range(section_starts[0] + 1, len(lines)):
        if lines[i].startswith("## ") or lines[i].strip() == "---":
            first_end = i
            break
    insert_at = first_end
    while insert_at > section_starts[0] + 1 and not lines[insert_at - 1].strip():
        insert_at -= 1
    new_lines = lines[:insert_at] + [f"{entry}\n"] + lines[insert_at:]
    return "".join(new_lines)
