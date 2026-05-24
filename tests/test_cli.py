"""Tests for cli command functions."""

import argparse
import pytest
from pathlib import Path

from handoff_forge.cli import cmd_handoff, cmd_init, cmd_tasks


def _make_args(task: str, target: str, phase: str = "Current Phase") -> argparse.Namespace:
    return argparse.Namespace(task=task, target=target, phase=phase)


def _make_handoff_args(target: str, *, append: bool = False, overwrite: bool = False) -> argparse.Namespace:
    return argparse.Namespace(
        session="Test session",
        built="Built something",
        next="Do next thing",
        incomplete=None,
        decisions=None,
        risks=None,
        target=target,
        overwrite=overwrite,
        append=append,
    )


def test_cmd_tasks_creates_new_file(tmp_path):
    args = _make_args("My first task", str(tmp_path))
    result = cmd_tasks(args)
    assert result == 0
    tasks_file = tmp_path / "TASKS.md"
    assert tasks_file.exists()
    content = tasks_file.read_text(encoding="utf-8")
    assert "- [ ] My first task" in content


def test_cmd_tasks_appends_to_template_format(tmp_path):
    tasks_file = tmp_path / "TASKS.md"
    tasks_file.write_text(
        "# TASKS.md\n\n## Phase 1\n\n- [ ] existing task\n\n## TASK FORMAT\n\nformat info\n",
        encoding="utf-8",
    )
    args = _make_args("new task", str(tmp_path))
    cmd_tasks(args)
    content = tasks_file.read_text(encoding="utf-8")
    phase_pos = content.index("## Phase 1")
    task_format_pos = content.index("## TASK FORMAT")
    new_task_pos = content.index("- [ ] new task")
    assert phase_pos < new_task_pos < task_format_pos


def test_cmd_tasks_inserts_into_first_section(tmp_path):
    tasks_file = tmp_path / "TASKS.md"
    tasks_file.write_text(
        "# TASKS.md\n\n"
        "## Current\n\n"
        "- [ ] existing task\n\n"
        "## Next\n\n"
        "- [ ] queued task\n\n"
        "## Backlog\n\n"
        "- [ ] backlog task\n\n"
        "## TASK FORMAT\n\nformat info\n",
        encoding="utf-8",
    )
    args = _make_args("urgent new task", str(tmp_path))
    cmd_tasks(args)
    content = tasks_file.read_text(encoding="utf-8")
    current_pos = content.index("## Current")
    next_pos = content.index("## Next")
    new_task_pos = content.index("- [ ] urgent new task")
    # New task must be in the Current section, not after Next/Backlog
    assert current_pos < new_task_pos < next_pos


def test_cmd_tasks_appends_when_no_sections(tmp_path):
    tasks_file = tmp_path / "TASKS.md"
    tasks_file.write_text("# TASKS.md\n\nsome content\n", encoding="utf-8")
    args = _make_args("orphan task", str(tmp_path))
    cmd_tasks(args)
    content = tasks_file.read_text(encoding="utf-8")
    assert content.endswith("- [ ] orphan task\n")


def test_cmd_tasks_with_real_template_separator(tmp_path):
    """tasks_template generates --- as the section delimiter; new tasks must land before it."""
    tasks_file = tmp_path / "TASKS.md"
    tasks_file.write_text(
        "# TASKS.md\n\n"
        "## Phase 1\n\n"
        "- [ ] existing task\n\n"
        "---\n\n"
        "## TASK FORMAT (for new tasks)\n\nformat info\n",
        encoding="utf-8",
    )
    args = _make_args("real template task", str(tmp_path))
    cmd_tasks(args)
    content = tasks_file.read_text(encoding="utf-8")
    phase_pos = content.index("## Phase 1")
    sep_pos = content.index("---")
    new_task_pos = content.index("- [ ] real template task")
    assert phase_pos < new_task_pos < sep_pos


# --- cmd_handoff ---

def test_cmd_handoff_append_adds_note_to_existing_file(tmp_path):
    handoff_file = tmp_path / "HANDOFF.md"
    handoff_file.write_text("# HANDOFF.md\n\n## Session: today — Original\n\nOriginal content.\n", encoding="utf-8")
    args = _make_handoff_args(str(tmp_path), append=True)
    result = cmd_handoff(args)
    assert result == 0
    content = handoff_file.read_text(encoding="utf-8")
    assert "Original content." in content
    assert "Test session" in content
    assert "Built something" in content
    # --append must not create backup files
    backups = [f for f in tmp_path.iterdir() if "bak" in f.name]
    assert len(backups) == 0


def test_cmd_handoff_append_creates_full_file_when_none_exists(tmp_path):
    args = _make_handoff_args(str(tmp_path), append=True)
    result = cmd_handoff(args)
    assert result == 0
    content = (tmp_path / "HANDOFF.md").read_text(encoding="utf-8")
    assert "# HANDOFF.md" in content
    assert "Test session" in content


def test_cmd_handoff_append_and_overwrite_errors(tmp_path):
    args = _make_handoff_args(str(tmp_path), append=True, overwrite=True)
    result = cmd_handoff(args)
    assert result == 1


# --- backup hygiene ---

def test_cmd_tasks_update_creates_no_backup(tmp_path):
    tasks_file = tmp_path / "TASKS.md"
    tasks_file.write_text("# TASKS.md\n\n## Phase 1\n\n- [ ] existing\n", encoding="utf-8")
    args = _make_args("another task", str(tmp_path))
    cmd_tasks(args)
    backups = [f for f in tmp_path.iterdir() if "bak" in f.name]
    assert len(backups) == 0


def _make_init_args(target: str, *, overwrite: bool = False) -> argparse.Namespace:
    return argparse.Namespace(target=target, overwrite=overwrite)


def test_cmd_init_overwrite_creates_exactly_one_backup_per_file(tmp_path):
    (tmp_path / "HANDOFF.md").write_text("old handoff", encoding="utf-8")
    args = _make_init_args(str(tmp_path), overwrite=True)
    cmd_init(args)
    backups = [f for f in tmp_path.iterdir() if "bak" in f.name]
    assert len(backups) == 1
    assert backups[0].read_text(encoding="utf-8") == "old handoff"
