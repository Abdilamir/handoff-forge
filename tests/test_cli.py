"""Tests for cli command functions."""

import argparse
import pytest
from pathlib import Path

from handoff_forge.cli import cmd_tasks


def _make_args(task: str, target: str, phase: str = "Current Phase") -> argparse.Namespace:
    return argparse.Namespace(task=task, target=target, phase=phase)


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
