"""Tests for file_ops service."""

import pytest
from pathlib import Path

from handoff_forge.services.file_ops import (
    backup_file,
    check_required_files,
    ensure_directory,
    file_exists,
    insert_task_entry,
    read_file,
    write_file,
)


def test_read_file_returns_content(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("hello world", encoding="utf-8")
    assert read_file(f) == "hello world"


def test_read_file_returns_none_if_missing(tmp_path):
    assert read_file(tmp_path / "nonexistent.md") is None


def test_write_file_creates_new_file(tmp_path):
    target = tmp_path / "HANDOFF.md"
    write_file(target, "# Handoff")
    assert target.read_text(encoding="utf-8") == "# Handoff"


def test_write_file_creates_parent_directories(tmp_path):
    target = tmp_path / "deep" / "nested" / "file.md"
    write_file(target, "content")
    assert target.exists()


def test_write_file_raises_if_exists_and_no_overwrite(tmp_path):
    target = tmp_path / "file.md"
    target.write_text("original", encoding="utf-8")
    with pytest.raises(FileExistsError):
        write_file(target, "new content", overwrite=False)


def test_write_file_backs_up_existing_when_overwrite(tmp_path):
    target = tmp_path / "file.md"
    target.write_text("original", encoding="utf-8")
    write_file(target, "new content", overwrite=True)
    assert target.read_text(encoding="utf-8") == "new content"
    # A backup file should exist
    backups = [f for f in tmp_path.iterdir() if "bak" in f.name]
    assert len(backups) == 1
    assert backups[0].read_text(encoding="utf-8") == "original"


def test_backup_file_creates_timestamped_copy(tmp_path):
    original = tmp_path / "HANDOFF.md"
    original.write_text("session content", encoding="utf-8")
    backup_path = backup_file(original)
    assert backup_path.exists()
    assert "bak" in backup_path.name
    assert backup_path.read_text(encoding="utf-8") == "session content"
    # Original must still exist
    assert original.exists()


def test_backup_file_raises_if_source_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        backup_file(tmp_path / "ghost.md")


def test_ensure_directory_creates_nested(tmp_path):
    target = tmp_path / "a" / "b" / "c"
    result = ensure_directory(target)
    assert target.is_dir()
    assert result == target


def test_ensure_directory_is_idempotent(tmp_path):
    target = tmp_path / "existing"
    target.mkdir()
    ensure_directory(target)  # Should not raise
    assert target.is_dir()


def test_file_exists_true(tmp_path):
    f = tmp_path / "exists.md"
    f.write_text("x", encoding="utf-8")
    assert file_exists(f) is True


def test_file_exists_false(tmp_path):
    assert file_exists(tmp_path / "nope.md") is False


# --- check_required_files ---

def test_check_required_files_all_present(tmp_path):
    for name in ["CLAUDE.md", "HANDOFF.md", "TASKS.md"]:
        (tmp_path / name).write_text("x", encoding="utf-8")
    result = check_required_files(tmp_path, ["CLAUDE.md", "HANDOFF.md", "TASKS.md"])
    assert result == {"CLAUDE.md": True, "HANDOFF.md": True, "TASKS.md": True}


def test_check_required_files_some_missing(tmp_path):
    (tmp_path / "CLAUDE.md").write_text("x", encoding="utf-8")
    result = check_required_files(tmp_path, ["CLAUDE.md", "HANDOFF.md"])
    assert result["CLAUDE.md"] is True
    assert result["HANDOFF.md"] is False


def test_check_required_files_all_missing(tmp_path):
    result = check_required_files(tmp_path, ["CLAUDE.md", "HANDOFF.md", "SECURITY.md"])
    assert all(not present for present in result.values())


def test_check_required_files_preserves_order(tmp_path):
    files = ["CLAUDE.md", "HANDOFF.md", "TASKS.md"]
    result = check_required_files(tmp_path, files)
    assert list(result.keys()) == files


def test_check_required_files_empty_list(tmp_path):
    result = check_required_files(tmp_path, [])
    assert result == {}


# --- insert_task_entry ---

def test_insert_task_entry_into_first_section():
    content = "# TASKS.md\n\n## Current\n\n- [ ] existing\n\n## Next\n\n- [ ] queued\n"
    result = insert_task_entry(content, "- [ ] new task")
    current_pos = result.index("## Current")
    next_pos = result.index("## Next")
    new_pos = result.index("- [ ] new task")
    assert current_pos < new_pos < next_pos


def test_insert_task_entry_with_separator():
    content = "# TASKS.md\n\n## Phase 1\n\n- [ ] existing\n\n---\n\n## TASK FORMAT\n\nfmt\n"
    result = insert_task_entry(content, "- [ ] new task")
    sep_pos = result.index("---")
    new_pos = result.index("- [ ] new task")
    assert new_pos < sep_pos


def test_insert_task_entry_task_format_first_falls_back_to_append():
    content = "# TASKS.md\n\n## TASK FORMAT\n\nfmt info\n"
    result = insert_task_entry(content, "- [ ] new task")
    assert result.endswith("- [ ] new task\n")
    assert "fmt info" in result


def test_insert_task_entry_no_sections_appends():
    content = "# TASKS.md\n\nsome content\n"
    result = insert_task_entry(content, "- [ ] orphan")
    assert result.endswith("- [ ] orphan\n")
