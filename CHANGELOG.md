# CHANGELOG.md

---

## 2026-05-23

### [2026-05-23] — feat: handoff --append flag (PR #3) — MERGED
- **Branch:** `feat/handoff-append`
- **Greptile:** Round 1: 3/5 → Round 2 (after fixes): 5/5
- **What:** Added `--append` flag to `handoff` subcommand. Appends a compact `## Note:` block to an existing HANDOFF.md instead of a full rewrite. Greptile Round 1 flagged: (1) template header contradiction ("always a full rewrite"), (2) backup file accumulation on every append call. Both fixed before Round 2.
- **Files changed:**
  - `src/handoff_forge/services/templates.py` — updated `handoff_template` header; added `handoff_append_entry()`
  - `src/handoff_forge/services/file_ops.py` — added `backup: bool = True` param to `write_file`
  - `src/handoff_forge/cli.py` — `cmd_handoff` --append path; `--append` flag in parser
  - `tests/test_cli.py` — 3 new tests for `cmd_handoff` (append, create-on-missing, mutual-exclusion)
  - `tests/test_file_ops.py` — `test_write_file_no_backup_when_backup_false`
  - `tests/test_templates.py` — `TestHandoffAppendEntry` (3 tests); `test_header_acknowledges_append`
  - `plans/PLAN_feat-handoff-append.md` — implementation plan
- **Tests:** 8 new — 50 total passing
- **Breaking changes:** None
- **Tags:** `restore/post-handoff-append-merge`

---

### [2026-05-23] — fix: tasks insertion position (PR #2) — MERGED
- **Branch:** `fix/tasks-insertion-position`
- **Greptile:** Round 1: 4/5 → Round 2: 5/5
- **What:** Fixed `cmd_tasks` inserting new tasks before `## TASK FORMAT` instead of inside the first active section. Moved insertion algorithm to `file_ops.py` per CLAUDE.md rules 2&3.
- **Files changed:**
  - `src/handoff_forge/services/file_ops.py` — added `insert_task_entry()`
  - `src/handoff_forge/cli.py` — `cmd_tasks` reduced to 3-line orchestration
  - `tests/test_file_ops.py` — 4 new tests for `insert_task_entry`
  - `tests/test_cli.py` — new file, 5 tests for `cmd_tasks` CLI behavior
  - `plans/PLAN_fix-tasks-insertion.md` — implementation plan
- **Tests:** 9 new — 42 total passing
- **Breaking changes:** None
- **Tags:** `restore/post-tasks-fix-merge`

---

## 2026-05-22

### [2026-05-22] — feat: validate command (PR #1) — MERGED
- **Branch:** `feature/validate-command`
- **Greptile:** 5/5
- **What:** Added `handoff-forge validate [target]` — checks for 6 required OS files, prints status per file, exits 0 (all present) or 1 (any missing)
- **Files changed:**
  - `src/handoff_forge/services/file_ops.py` — added `check_required_files()`
  - `src/handoff_forge/cli.py` — added `cmd_validate()`, `REQUIRED_FILES` constant, validate subparser
  - `tests/test_file_ops.py` — 5 tests for `check_required_files`
  - `README.md` — validate command section with example output
- **Tests:** 5 new — 33 total at merge
- **Tags:** `restore/post-validate-merge`

### [2026-05-22] — Phase 2 complete: handoff-forge v0.1.0
- **Commit:** `restore/project-init` tag
- **What:** Full working CLI — 5 commands (init, handoff, state, tasks, validate), stdlib only, 28 tests
- **Files created:** pyproject.toml, src/handoff_forge/, tests/, README.md, full OS scaffold
