# TASKS.md

> Active task list only. Completed tasks move to CHANGELOG.md.
> Each task must be PR-sized: one feature, one branch, ~200-400 lines max.

---

## Current — Immediate

- [ ] Initialize git, push to GitHub, create restore/project-init tag
      Risk: low

## Next

- [ ] Connect Greptile to validate review loop (Phase 3)
      Risk: low — read-only GitHub access

## Backlog

- [ ] Fix tasks insertion position — new tasks should land inside active phase block, not before TASK FORMAT section
      Files: src/handoff_forge/cli.py (cmd_tasks), tests/test_cli.py
      Risk: low

- [ ] Add --append flag to handoff command for accumulating session notes without full rewrite
      Files: cli.py, templates.py, tests/
      Risk: low

- [ ] Add `handoff-forge validate <dir>` command to check if all three files exist and have required sections
      Files: cli.py, services/file_ops.py, tests/
      Risk: low
