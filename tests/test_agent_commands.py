"""Tests for agent operating layer commands: agents init, agent brief, next, checkpoint."""

import argparse

from handoff_forge.cli import (
    cmd_agent_brief,
    cmd_agents_init,
    cmd_checkpoint,
    cmd_next,
)
from handoff_forge.services import templates

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _agents_init_args(target: str, overwrite: bool = False) -> argparse.Namespace:
    return argparse.Namespace(target=target, overwrite=overwrite)


def _agent_brief_args(role: str, target: str) -> argparse.Namespace:
    return argparse.Namespace(role=role, target=target)


def _next_args(target: str) -> argparse.Namespace:
    return argparse.Namespace(target=target)


def _checkpoint_args(
    target: str, task: str, next_step: str, branch: str | None = None, notes: str | None = None
) -> argparse.Namespace:
    return argparse.Namespace(target=target, task=task, next=next_step, branch=branch, notes=notes)


# ---------------------------------------------------------------------------
# agents init
# ---------------------------------------------------------------------------

class TestAgentsInit:
    def test_creates_agents_directory_and_all_role_files(self, tmp_path):
        result = cmd_agents_init(_agents_init_args(str(tmp_path)))
        assert result == 0
        agents_dir = tmp_path / "agents"
        assert agents_dir.is_dir()
        for role in templates.AGENT_ROLES:
            assert (agents_dir / f"{role}.md").exists()

    def test_role_files_contain_required_sections(self, tmp_path):
        cmd_agents_init(_agents_init_args(str(tmp_path)))
        for role in templates.AGENT_ROLES:
            content = (tmp_path / "agents" / f"{role}.md").read_text(encoding="utf-8")
            assert "## Role" in content
            assert "## Responsibilities" in content
            assert "## Allowed Actions" in content
            assert "## Escalation Rules" in content
            assert "## Output Format" in content

    def test_skips_existing_files_without_overwrite(self, tmp_path):
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "engineer.md").write_text("custom content", encoding="utf-8")
        cmd_agents_init(_agents_init_args(str(tmp_path)))
        assert (agents_dir / "engineer.md").read_text(encoding="utf-8") == "custom content"

    def test_overwrites_and_backs_up_existing_files(self, tmp_path):
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "engineer.md").write_text("old content", encoding="utf-8")
        result = cmd_agents_init(_agents_init_args(str(tmp_path), overwrite=True))
        assert result == 0
        backups = [f for f in agents_dir.iterdir() if "bak" in f.name]
        assert len(backups) == 1
        assert backups[0].read_text(encoding="utf-8") == "old content"
        new_content = (agents_dir / "engineer.md").read_text(encoding="utf-8")
        assert "## Role" in new_content


# ---------------------------------------------------------------------------
# agent brief
# ---------------------------------------------------------------------------

class TestAgentBrief:
    def test_prints_brief_for_valid_role(self, tmp_path, capsys):
        cmd_agents_init(_agents_init_args(str(tmp_path)))
        result = cmd_agent_brief(_agent_brief_args("engineer", str(tmp_path)))
        assert result == 0
        out = capsys.readouterr().out
        assert "Agent Brief: Engineer" in out
        assert "## Role" in out
        assert "Your Task" in out

    def test_includes_project_state_and_handoff_when_present(self, tmp_path, capsys):
        cmd_agents_init(_agents_init_args(str(tmp_path)))
        (tmp_path / "PROJECT_STATE.md").write_text("## Current Phase\nPhase 42", encoding="utf-8")
        (tmp_path / "HANDOFF.md").write_text("### Next Step\nFix the thing", encoding="utf-8")
        cmd_agent_brief(_agent_brief_args("engineer", str(tmp_path)))
        out = capsys.readouterr().out
        assert "Current Project State" in out
        assert "Last Session Handoff" in out

    def test_returns_error_for_missing_role_file(self, tmp_path, capsys):
        result = cmd_agent_brief(_agent_brief_args("engineer", str(tmp_path)))
        assert result == 1
        err = capsys.readouterr().err
        assert "not found" in err
        assert "agents init" in err


# ---------------------------------------------------------------------------
# next
# ---------------------------------------------------------------------------

class TestNext:
    def test_outputs_next_action_from_state_files(self, tmp_path, capsys):
        (tmp_path / "HANDOFF.md").write_text(
            "### Next Step\nImplement the widget\n", encoding="utf-8"
        )
        (tmp_path / "TASKS.md").write_text(
            "## Phase 1\n- [ ] Build widget\n- [x] Plan widget\n", encoding="utf-8"
        )
        (tmp_path / "PROJECT_STATE.md").write_text(
            "## Current Phase\nPhase 1\n## Status\nIn progress\n", encoding="utf-8"
        )
        result = cmd_next(_next_args(str(tmp_path)))
        assert result == 0
        out = capsys.readouterr().out
        assert "Next Action" in out
        assert "Implement the widget" in out
        assert "- [ ] Build widget" in out
        assert "Phase 1" in out

    def test_returns_error_when_no_state_files_present(self, tmp_path, capsys):
        result = cmd_next(_next_args(str(tmp_path)))
        assert result == 1
        err = capsys.readouterr().err
        assert "no state files" in err


# ---------------------------------------------------------------------------
# checkpoint
# ---------------------------------------------------------------------------

class TestCheckpoint:
    def test_appends_checkpoint_to_existing_handoff(self, tmp_path):
        handoff = tmp_path / "HANDOFF.md"
        handoff.write_text("# HANDOFF.md\n\nExisting content.", encoding="utf-8")
        result = cmd_checkpoint(_checkpoint_args(
            str(tmp_path), task="Implement auth", next_step="Write tests"
        ))
        assert result == 0
        content = handoff.read_text(encoding="utf-8")
        assert "Existing content." in content
        assert "Checkpoint:" in content
        assert "Implement auth" in content
        assert "Write tests" in content

    def test_creates_handoff_when_missing(self, tmp_path):
        result = cmd_checkpoint(_checkpoint_args(
            str(tmp_path), task="First task", next_step="Second task"
        ))
        assert result == 0
        assert (tmp_path / "HANDOFF.md").exists()

    def test_includes_optional_branch_and_notes(self, tmp_path):
        (tmp_path / "HANDOFF.md").write_text("# H\n", encoding="utf-8")
        cmd_checkpoint(_checkpoint_args(
            str(tmp_path), task="Task", next_step="Next",
            branch="feat/thing", notes="Remember to clean up"
        ))
        content = (tmp_path / "HANDOFF.md").read_text(encoding="utf-8")
        assert "feat/thing" in content
        assert "Remember to clean up" in content

    def test_checkpoint_does_not_create_backup(self, tmp_path):
        (tmp_path / "HANDOFF.md").write_text("# H\n", encoding="utf-8")
        cmd_checkpoint(_checkpoint_args(str(tmp_path), task="T", next_step="N"))
        backups = [f for f in tmp_path.iterdir() if "bak" in f.name]
        assert len(backups) == 0


# ---------------------------------------------------------------------------
# Template unit tests
# ---------------------------------------------------------------------------

class TestTemplateHelpers:
    def test_extract_section_returns_content_under_header(self):
        content = "## Current Phase\nPhase 7\n\n## Status\nGreen\n"
        result = templates._extract_section(content, "## Current Phase")
        assert result == "Phase 7"

    def test_extract_section_returns_none_for_missing_header(self):
        assert templates._extract_section("## Other\nstuff\n", "## Missing") is None

    def test_extract_section_handles_none_content(self):
        assert templates._extract_section(None, "## Any") is None

    def test_first_open_task_returns_first_unchecked(self):
        content = "- [x] Done\n- [ ] Next task\n- [ ] Other\n"
        assert templates._first_open_task(content) == "- [ ] Next task"

    def test_first_open_task_returns_none_when_all_done(self):
        assert templates._first_open_task("- [x] Done\n- [x] Also done\n") is None

    def test_checkpoint_entry_includes_all_fields(self):
        entry = templates.checkpoint_entry(
            task="Build widget", next_step="Test widget",
            branch="feat/widget", notes="Check edge cases",
            timestamp="2026-05-24T12:00:00",
        )
        assert "2026-05-24T12:00:00" in entry
        assert "Build widget" in entry
        assert "feat/widget" in entry
        assert "Check edge cases" in entry
