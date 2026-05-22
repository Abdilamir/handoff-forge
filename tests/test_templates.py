"""Tests for template generators."""

from handoff_forge.services.templates import (
    handoff_template,
    project_state_template,
    task_entry,
    tasks_template,
)


class TestHandoffTemplate:
    def test_contains_session_name(self):
        result = handoff_template(
            session="Auth feature",
            what_built="Login endpoint",
            not_finished="Token refresh",
            decisions="Used JWT over sessions",
            next_step="Implement refresh endpoint",
            risks="None",
            updated="2026-05-22",
        )
        assert "Auth feature" in result

    def test_contains_what_built(self):
        result = handoff_template(
            session="S1",
            what_built="Added CSV export",
            not_finished="None",
            decisions="None",
            next_step="Add tests",
            risks="None",
            updated="2026-05-22",
        )
        assert "Added CSV export" in result

    def test_contains_next_step(self):
        result = handoff_template(
            session="S1",
            what_built="x",
            not_finished="x",
            decisions="x",
            next_step="Run pytest",
            risks="x",
            updated="2026-05-22",
        )
        assert "Run pytest" in result

    def test_uses_provided_date(self):
        result = handoff_template(
            session="S1",
            what_built="x",
            not_finished="x",
            decisions="x",
            next_step="x",
            risks="x",
            updated="2099-01-01",
        )
        assert "2099-01-01" in result

    def test_starts_with_heading(self):
        result = handoff_template(
            session="S1",
            what_built="x",
            not_finished="x",
            decisions="x",
            next_step="x",
            risks="x",
        )
        assert result.startswith("# HANDOFF.md")

    def test_contains_last_updated_line(self):
        result = handoff_template(
            session="Deploy step",
            what_built="x",
            not_finished="x",
            decisions="x",
            next_step="x",
            risks="x",
            updated="2026-05-22",
        )
        assert "*Last updated: 2026-05-22 | Session: Deploy step*" in result


class TestProjectStateTemplate:
    def test_contains_phase(self):
        result = project_state_template(
            phase="Phase 2",
            status="In progress",
            stack="Python 3.11, stdlib",
            done_items=["Init done"],
            in_progress="CLI commands",
            next_steps="Write tests",
            updated="2026-05-22",
        )
        assert "Phase 2" in result

    def test_done_items_formatted_as_checkboxes(self):
        result = project_state_template(
            phase="P1",
            status="done",
            stack="Python",
            done_items=["Task A", "Task B"],
            in_progress="nothing",
            next_steps="ship it",
            updated="2026-05-22",
        )
        assert "- [x] Task A" in result
        assert "- [x] Task B" in result

    def test_empty_done_items_shows_none_yet(self):
        result = project_state_template(
            phase="P1",
            status="starting",
            stack="Python",
            done_items=[],
            in_progress="nothing",
            next_steps="begin",
            updated="2026-05-22",
        )
        assert "None yet" in result

    def test_starts_with_heading(self):
        result = project_state_template(
            phase="P1",
            status="x",
            stack="x",
            done_items=[],
            in_progress="x",
            next_steps="x",
        )
        assert result.startswith("# PROJECT_STATE.md")


class TestTasksTemplate:
    def test_contains_phase(self):
        result = tasks_template(phase="Phase 2", tasks=["Build CLI"])
        assert "Phase 2" in result

    def test_tasks_formatted_as_checkboxes(self):
        result = tasks_template(
            phase="Phase 2",
            tasks=["Implement init command", "Write tests"],
        )
        assert "- [ ] Implement init command" in result
        assert "- [ ] Write tests" in result

    def test_empty_tasks_shows_placeholder(self):
        result = tasks_template(phase="Phase 1", tasks=[])
        assert "Add your first task here" in result

    def test_starts_with_heading(self):
        result = tasks_template(phase="P1", tasks=[])
        assert result.startswith("# TASKS.md")


class TestTaskEntry:
    def test_formats_correctly(self):
        assert task_entry("Build the thing") == "- [ ] Build the thing"

    def test_empty_description(self):
        assert task_entry("") == "- [ ] "
