# PLAN — fix: tasks insertion position

**Branch:** `fix/tasks-insertion-position`
**PR size estimate:** ~40 lines diff
**Files touched:** `src/handoff_forge/cli.py`, `tests/test_cli.py` (new file)

---

## Problem

`cmd_tasks` in `cli.py` (line 168) looks for the string `## TASK FORMAT` and inserts
the new task just before it. This works for the bare template TASKS.md (one phase section
+ TASK FORMAT section). It fails for multi-section TASKS.md (Current / Next / Backlog /
TASK FORMAT) because new tasks land after Backlog instead of inside Current.

**Broken behaviour (multi-section file):**
```
## Current — Immediate
- [ ] existing task

## Next
- [ ] queued task

## Backlog
- [ ] backlog task
- [ ] NEW TASK LANDS HERE  ← wrong

## TASK FORMAT
```

**Correct behaviour:**
```
## Current — Immediate
- [ ] existing task
- [ ] NEW TASK LANDS HERE  ← correct

## Next
...
```

---

## Root Cause

`cli.py:168` — the marker is `## TASK FORMAT`, not "the end of the first section".
Any content before `## TASK FORMAT` counts as the insertion zone.

---

## Fix

Replace the `## TASK FORMAT` marker search with:
1. Find all `## ` section header positions
2. Find the first `## ` header that is not a `## TASK FORMAT` header
3. Find where that section ends (start of the next `## ` header, or a `---` line, whichever comes first)
4. Insert the new task entry just before that end point (after stripping trailing blanks)

**Fallback (no `## ` sections found):** append to end of file, same as today.

---

## Step 1 — Write failing test first (tests/test_cli.py)

Create `tests/test_cli.py`. Test `cmd_tasks` directly by building an
`argparse.Namespace` and calling the function with a `tmp_path` target.

Tests to write:
- `test_cmd_tasks_creates_new_file` — no existing TASKS.md, file gets created
- `test_cmd_tasks_appends_to_template_format` — single-section template TASKS.md,
  task lands in that section (not just before TASK FORMAT)
- `test_cmd_tasks_inserts_into_first_section` — multi-section TASKS.md (Current / Next /
  Backlog / TASK FORMAT), task lands in Current section, not after Backlog
- `test_cmd_tasks_appends_when_no_sections` — TASKS.md with no `## ` headers, task
  appends to end

The third test (`test_cmd_tasks_inserts_into_first_section`) MUST FAIL before the fix.

---

## Step 2 — Implement fix in cli.py

Replace lines 167–170 in `cmd_tasks`:

```python
# BEFORE (broken)
marker = "## TASK FORMAT"
if marker in existing:
    insert_at = existing.index(marker)
    updated = existing[:insert_at].rstrip() + f"\n{entry}\n\n" + existing[insert_at:]
else:
    updated = existing.rstrip() + f"\n{entry}\n"
```

```python
# AFTER (correct)
lines = existing.splitlines(keepends=True)
section_starts = [i for i, line in enumerate(lines) if line.startswith("## ")]

if section_starts:
    # Find end of first section: next ## header, a --- separator, or EOF
    first_end = len(lines)
    for i in range(section_starts[0] + 1, len(lines)):
        if lines[i].startswith("## ") or lines[i].strip() == "---":
            first_end = i
            break
    # Insert after last non-blank line in first section
    insert_at = first_end
    while insert_at > section_starts[0] + 1 and not lines[insert_at - 1].strip():
        insert_at -= 1
    new_lines = lines[:insert_at] + [f"{entry}\n"] + lines[insert_at:]
    updated = "".join(new_lines)
else:
    updated = existing.rstrip() + f"\n{entry}\n"
```

---

## Step 3 — Run tests

```
python -m pytest --tb=short -q
```

All tests must pass. `test_cmd_tasks_inserts_into_first_section` flips from fail to pass.
Total count increases from 33 to 37 (4 new tests in test_cli.py).

---

## Step 4 — Post-feature structure scan

Scan `cli.py` for any duplicated logic introduced. This fix is a pure replacement
inside `cmd_tasks` — no new functions, no service-layer candidates.

---

## Done =

`python -m pytest --tb=short -q` shows 37 passing.
`test_cmd_tasks_inserts_into_first_section` passes.
New task added via CLI lands in the first `## ` section of TASKS.md.
