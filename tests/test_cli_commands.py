"""Tests for cmd_init, cmd_state, cmd_validate, and cmd_handoff full-rewrite path."""

import argparse
from pathlib import Path

from handoff_forge.cli import cmd_handoff, cmd_init, cmd_state, cmd_validate


# --- helpers ---

def _init_args(target: str, *, overwrite: bool = False) -> argparse.Namespace:
    return argparse.Namespace(target=target, overwrite=overwrite)


def _state_args(target: str, *, overwrite: bool = False) -> argparse.Namespace:
    return argparse.Namespace(
        target=target,
        phase="Phase 1",
        status="In progress",
        stack="Python 3.11",
        done=["Task A"],
        progress="Writing tests",
        next="Ship it",
        overwrite=overwrite,
    )


def _handoff_args(target: str, *, overwrite: bool = False) -> argparse.Namespace:
    return argparse.Namespace(
        target=target,
        session="Full rewrite session",
        built="Built the thing",
        next="Do the next thing",
        incomplete=None,
        decisions=None,
        risks=None,
        overwrite=overwrite,
        append=False,
    )


def _validate_args(target: str) -> argparse.Namespace:
    return argparse.Namespace(target=target)


# --- cmd_init ---

class TestCmdInit:
    def test_creates_all_three_files(self, tmp_path):
        result = cmd_init(_init_args(str(tmp_path)))
        assert result == 0
        assert (tmp_path / "HANDOFF.md").exists()
        assert (tmp_path / "PROJECT_STATE.md").exists()
        assert (tmp_path / "TASKS.md").exists()

    def test_skips_existing_files_by_default(self, tmp_path):
        original = "original content"
        (tmp_path / "HANDOFF.md").write_text(original, encoding="utf-8")
        cmd_init(_init_args(str(tmp_path)))
        assert (tmp_path / "HANDOFF.md").read_text(encoding="utf-8") == original

    def test_overwrites_and_backs_up_existing_file(self, tmp_path):
        (tmp_path / "HANDOFF.md").write_text("old handoff", encoding="utf-8")
        result = cmd_init(_init_args(str(tmp_path), overwrite=True))
        assert result == 0
        new_content = (tmp_path / "HANDOFF.md").read_text(encoding="utf-8")
        assert "Project initialized" in new_content
        backups = [f for f in tmp_path.iterdir() if "bak" in f.name]
        assert len(backups) == 1
        assert backups[0].read_text(encoding="utf-8") == "old handoff"

    def test_creates_target_directory_if_missing(self, tmp_path):
        new_dir = tmp_path / "new_project"
        result = cmd_init(_init_args(str(new_dir)))
        assert result == 0
        assert new_dir.is_dir()
        assert (new_dir / "HANDOFF.md").exists()

    def test_returns_zero_on_success(self, tmp_path):
        assert cmd_init(_init_args(str(tmp_path))) == 0


# --- cmd_validate ---

class TestCmdValidate:
    def test_returns_zero_when_all_required_files_present(self, tmp_path):
        for name in ["CLAUDE.md", "HANDOFF.md", "TASKS.md", "PROJECT_STATE.md", "CHANGELOG.md", "SECURITY.md"]:
            (tmp_path / name).write_text("x", encoding="utf-8")
        assert cmd_validate(_validate_args(str(tmp_path))) == 0

    def test_returns_one_when_files_missing(self, tmp_path):
        (tmp_path / "CLAUDE.md").write_text("x", encoding="utf-8")
        assert cmd_validate(_validate_args(str(tmp_path))) == 1

    def test_returns_one_for_empty_directory(self, tmp_path):
        assert cmd_validate(_validate_args(str(tmp_path))) == 1

    def test_returns_one_for_nonexistent_directory(self, tmp_path):
        assert cmd_validate(_validate_args(str(tmp_path / "ghost"))) == 1


# --- cmd_state ---

class TestCmdState:
    def test_creates_project_state_file(self, tmp_path):
        result = cmd_state(_state_args(str(tmp_path)))
        assert result == 0
        assert (tmp_path / "PROJECT_STATE.md").exists()

    def test_content_contains_phase_and_status(self, tmp_path):
        cmd_state(_state_args(str(tmp_path)))
        content = (tmp_path / "PROJECT_STATE.md").read_text(encoding="utf-8")
        assert "Phase 1" in content
        assert "In progress" in content

    def test_content_contains_done_items(self, tmp_path):
        cmd_state(_state_args(str(tmp_path)))
        content = (tmp_path / "PROJECT_STATE.md").read_text(encoding="utf-8")
        assert "- [x] Task A" in content

    def test_errors_if_file_exists_and_no_overwrite(self, tmp_path):
        (tmp_path / "PROJECT_STATE.md").write_text("existing", encoding="utf-8")
        result = cmd_state(_state_args(str(tmp_path), overwrite=False))
        assert result == 1

    def test_overwrites_with_flag(self, tmp_path):
        (tmp_path / "PROJECT_STATE.md").write_text("old state", encoding="utf-8")
        result = cmd_state(_state_args(str(tmp_path), overwrite=True))
        assert result == 0
        content = (tmp_path / "PROJECT_STATE.md").read_text(encoding="utf-8")
        assert "Phase 1" in content
        assert "old state" not in content


# --- cmd_handoff full-rewrite path ---

class TestCmdHandoffFullRewrite:
    def test_creates_handoff_file(self, tmp_path):
        result = cmd_handoff(_handoff_args(str(tmp_path)))
        assert result == 0
        assert (tmp_path / "HANDOFF.md").exists()

    def test_content_contains_session_and_built(self, tmp_path):
        cmd_handoff(_handoff_args(str(tmp_path)))
        content = (tmp_path / "HANDOFF.md").read_text(encoding="utf-8")
        assert "Full rewrite session" in content
        assert "Built the thing" in content

    def test_errors_if_file_exists_and_no_overwrite(self, tmp_path):
        (tmp_path / "HANDOFF.md").write_text("existing", encoding="utf-8")
        result = cmd_handoff(_handoff_args(str(tmp_path), overwrite=False))
        assert result == 1

    def test_overwrites_with_flag_and_creates_backup(self, tmp_path):
        (tmp_path / "HANDOFF.md").write_text("old handoff", encoding="utf-8")
        result = cmd_handoff(_handoff_args(str(tmp_path), overwrite=True))
        assert result == 0
        content = (tmp_path / "HANDOFF.md").read_text(encoding="utf-8")
        assert "Full rewrite session" in content
        backups = [f for f in tmp_path.iterdir() if "bak" in f.name]
        assert len(backups) == 1
