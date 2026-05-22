# CHANGELOG.md

---

## 2026-05-22 — Phase 3

### [2026-05-22] — feat: validate command
- **Branch:** `feature/validate-command`
- **PR:** pending Greptile review
- **What:** Added `handoff-forge validate [target]` — checks for required OS files, prints status per file, exits 0 (all present) or 1 (any missing)
- **Files changed:**
  - `src/handoff_forge/services/file_ops.py` — added `check_required_files()`
  - `src/handoff_forge/cli.py` — added `cmd_validate()`, `REQUIRED_FILES` constant, and validate subparser
  - `tests/test_file_ops.py` — added 5 tests for `check_required_files`
  - `README.md` — added validate command section with example output
- **Tests added:** 5 new — 33 total passing
- **Breaking changes:** None — purely additive

---

### [2026-05-22] — Phase 2 complete: handoff-forge v0.1.0
- **Commit:** restore/project-init (initial)
- **What:** Full working CLI with 4 commands and 28 passing tests
- **Files created:**
  - `pyproject.toml` — build config, entry point, dev deps
  - `src/handoff_forge/__init__.py`
  - `src/handoff_forge/cli.py` — init, handoff, state, tasks commands
  - `src/handoff_forge/services/__init__.py`
  - `src/handoff_forge/services/file_ops.py` — safe file I/O service
  - `src/handoff_forge/services/templates.py` — markdown template generators
  - `tests/__init__.py`
  - `tests/test_file_ops.py` — 12 tests
  - `tests/test_templates.py` — 16 tests
  - `README.md`
  - OS scaffold: CLAUDE.md, HANDOFF.md, TASKS.md, PROJECT_STATE.md, CHANGELOG.md, DECISIONS.md, SECURITY.md, plans/, reviews/
- **Tests added:** 28 — all passing
