# PLAN: Phase 3 — validate command

**Branch:** `feature/validate-command`
**Goal:** Add `handoff-forge validate <target-dir>` that checks whether a project contains all required OS files.
**Exit condition:** Done = command runs, prints present/missing files, returns correct exit code, tests pass, README updated.

---

## Scope (exactly this, nothing more)

Required files to check:
- CLAUDE.md
- HANDOFF.md
- TASKS.md
- PROJECT_STATE.md
- CHANGELOG.md
- SECURITY.md

**Exit codes:**
- 0 = all files present
- 1 = one or more missing

**Output format:**
```
Validating: /path/to/project

  [OK]      CLAUDE.md
  [OK]      HANDOFF.md
  [MISSING] TASKS.md
  [OK]      PROJECT_STATE.md
  [MISSING] CHANGELOG.md
  [OK]      SECURITY.md

2 file(s) missing.
```

---

## Files to change

| File | Change | Lines (est.) |
|------|--------|--------------|
| `src/handoff_forge/services/file_ops.py` | Add `check_required_files()` | +15 |
| `src/handoff_forge/cli.py` | Add `cmd_validate()` + subparser entry | +30 |
| `tests/test_file_ops.py` | Add 4 tests for `check_required_files` | +25 |
| `README.md` | Add validate section | +20 |
| `CHANGELOG.md` | Add entry | +8 |
| `HANDOFF.md` | Full rewrite | ~50 |

**Estimated diff: ~100 lines. Well within the 200-line target.**

---

## What is explicitly out of scope

- No --fix flag (auto-creating missing files) — that is a follow-up feature
- No JSON output flag
- No recursive directory scanning
- No custom required-file lists via flags
- No changes to existing commands

---

## Risk: Low
All changes are additive. Existing 28 tests are not touched. New function in file_ops.py is pure (no side effects beyond reading the filesystem).
