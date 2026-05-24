# PR 1 Review — validate command

**Branch:** `feature/validate-command`
**PR:** [pending — open at https://github.com/Abdilamir/handoff-forge/compare/master...feature/validate-command]
**Reviewer:** Greptile

---

## Review Checklist

- [ ] `check_required_files` correctly placed in services/ (not in cli.py)
- [ ] `REQUIRED_FILES` constant correctly placed in cli.py (not in services/)
- [ ] `cmd_validate` delegates to service — no direct filesystem access in cli.py
- [ ] Exit code 0 = all present, exit code 1 = any missing
- [ ] Non-existent directory handled with error message to stderr
- [ ] All 5 new tests passing (check_required_files coverage)
- [ ] No new runtime dependencies introduced
- [ ] No breaking changes to existing commands

---

## Greptile Feedback Log

| Round | Score | Issues Raised | Action Taken |
|-------|-------|---------------|--------------|
| 1     |       |               |              |
| 2     |       |               |              |
| 3     |       |               |              |

**Target: 5/5 before merge.**

---

## Final Sign-off

- [ ] Greptile score: 5/5
- [ ] Human diff review complete
- [ ] All tests passing on branch
- [ ] CHANGELOG.md updated
- [ ] Ready to merge
