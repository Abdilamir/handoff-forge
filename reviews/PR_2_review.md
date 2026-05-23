# PR 2 Review — fix: tasks insertion position

**Branch:** `fix/tasks-insertion-position`
**PR:** #2 (pending open)
**Reviewer:** Greptile

---

## Greptile Feedback Log

| Round | Score | Issues Raised | Action Taken |
|-------|-------|---------------|--------------|
| 1     | 4/5   | (1) Algorithm in cli.py violates CLAUDE.md rules 2&3; (2) TASK FORMAT-first edge case inserts inside format block; (3) No --- separator test | All three fixed: insert_task_entry() moved to file_ops.py, TASK FORMAT filter added, separator test added. 42 tests passing. |
| 2     | TBD   | Awaiting re-review | — |

**Target: 5/5 before merge.**

---

## Round 1 Fix Summary

**Issue 1 — Architecture (agreed):**
Extracted `insert_task_entry(content, entry) -> str` from `cmd_tasks` into `file_ops.py`.
`cmd_tasks` now delegates in 3 lines. CLAUDE.md rules 2 & 3 satisfied.

**Issue 2 — Edge case (agreed):**
Added `not line.startswith("## TASK FORMAT")` filter to section_starts comprehension.
When TASK FORMAT is the only `## ` header, falls back to append-to-end.

**Issue 3 — Missing test (agreed):**
Added `test_cmd_tasks_with_real_template_separator` to `test_cli.py` — uses `---` delimiter.
Added 4 unit tests for `insert_task_entry` directly in `test_file_ops.py`.

---

## Final Sign-off (fill after loop completes)

- [ ] Greptile score: 5/5
- [ ] Human diff review: `git diff master...fix/tasks-insertion-position`
- [ ] All 42 tests passing on branch
- [ ] CHANGELOG.md updated with merge entry
- [ ] Ready to merge
