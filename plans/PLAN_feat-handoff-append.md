# PLAN — feat: handoff --append flag

**Branch:** `feat/handoff-append`
**PR size estimate:** ~50 lines diff
**Files touched:** `src/handoff_forge/services/templates.py`, `src/handoff_forge/cli.py`, `tests/test_templates.py`, `tests/test_cli.py`

---

## Feature

Add `--append` flag to the `handoff` command. When set, a compact dated note entry
is appended to the bottom of an existing HANDOFF.md instead of rewriting the whole
file. Useful for accumulating mid-session notes without losing the current session state.

```bash
# Full rewrite (existing behaviour)
handoff-forge handoff --session "Auth" --built "JWT endpoints" --next "Add refresh"

# Append a note to existing file (new behaviour)
handoff-forge handoff --session "Mid-session" --built "Fixed login bug" --next "Continue tests" --append
```

---

## Appended Entry Format

```markdown
---

## Note: 2026-05-23 — Mid-session

**Built:** Fixed login bug
**Next:** Continue tests
```

---

## Behaviour Rules

- `--append` + file exists → read file, append entry, write back (backup created by write_file)
- `--append` + file does not exist → create full HANDOFF.md (same as normal, no --overwrite needed)
- `--append` is mutually exclusive with `--overwrite` (guard in cmd_handoff; print error if both set)
- `--incomplete`, `--decisions`, `--risks` are ignored in append mode (compact format only)

---

## Step 1 — templates.py

Add `handoff_append_entry(session, what_built, next_step, updated=None) -> str`.
Returns the compact note block including the leading `\n---\n`.

---

## Step 2 — cli.py

1. Add `--append` flag to `p_handoff` parser (store_true)
2. In `cmd_handoff`:
   - If both `--append` and `--overwrite` are set: print error to stderr, return 1
   - If `--append` and file exists: read + append entry + write back
   - If `--append` and file does not exist: fall through to full template (create new)
   - Otherwise: existing full-rewrite logic (unchanged)

---

## Step 3 — Tests

In `tests/test_templates.py`:
- `test_handoff_append_entry_contains_session`
- `test_handoff_append_entry_contains_built_and_next`
- `test_handoff_append_entry_starts_with_separator`

In `tests/test_cli.py`:
- `test_cmd_handoff_append_adds_note_to_existing_file`
- `test_cmd_handoff_append_creates_full_file_when_none_exists`
- `test_cmd_handoff_append_and_overwrite_errors`

---

## Done =

`python -m pytest --tb=short -q` shows 48+ passing.
Running `handoff-forge handoff --session "Note" --built "X" --next "Y" --append`
adds a compact block to the bottom of HANDOFF.md without replacing the existing content.
