# TASKS.md

> Active task list only. Completed tasks move to CHANGELOG.md.
> Each task must be PR-sized: one feature, one branch, ~200-400 lines max.

---

## Browser Action Required

- [ ] Enable GitHub secret scanning
      URL: https://github.com/Abdilamir/handoff-forge/settings/security_analysis
      Risk: none

## In Progress

- [ ] PR #10 (test/cli-coverage): awaiting Greptile re-review after rebase onto master
- [ ] PR #13 (chore/pyproject-metadata): awaiting Greptile re-review after classifier/URL fixes

## Queue — Phase 5 Stabilisation

- [ ] fix/backup-microseconds — change backup timestamp from %S to %S-%f to eliminate 1-second collision window
      Files: src/handoff_forge/services/file_ops.py, tests/test_file_ops.py
      Risk: low

- [ ] test/coverage-gaps — backup collision test; cmd_validate output format; cmd_init content correctness; cmd_handoff backup content
      Files: tests/
      Risk: low

## Queue — Phase 6 Developer Experience

- [ ] chore/add-makefile — make test, make install, make lint targets
      Files: Makefile (new)
      Risk: low

- [ ] chore/ruff-config — add [tool.ruff] to pyproject.toml, enforce on CI
      Files: pyproject.toml, .github/workflows/ci.yml
      Risk: low

## Completed This Phase

- [x] PR #1 merged: feat: validate command (Greptile 5/5)
- [x] PR #2 merged: fix: tasks insertion position (Greptile 5/5)
- [x] PR #3 merged: feat: handoff --append flag (Greptile 5/5)
- [x] PR #4 merged: docs: README --append documentation (Greptile 5/5)
- [x] PR #5 merged: chore: GitHub Actions CI workflow (Greptile 5/5)
- [x] PR #6 merged: chore: review loop preparation files (Greptile 5/5*)
- [x] PR #7 merged: fix: suppress spurious backups in cmd_init and cmd_tasks (Greptile 5/5)
- [x] PR #8 merged: chore: add .gitignore with security patterns (Greptile 5/5)
- [x] PR #9 merged: chore: add SECURITY.md and source --version from __version__ (Greptile 5/5)
- [x] PR #11 merged: chore: expand CI to Python 3.13 and all branch patterns (Greptile 5/5)
- [x] PR #12 merged: fix: replace placeholder repo URL in README (Greptile 5/5)

*Round 2 returned stale cache; fix verified in branch before merge.

## TASK FORMAT

Each entry:
```
- [ ] Short description — done = specific exit condition
      Files: path/to/file.py (if known)
      Risk: low | medium | high
```
