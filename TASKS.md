# TASKS.md

> Active task list only. Completed tasks move to CHANGELOG.md.
> Each task must be PR-sized: one feature, one branch, ~200-400 lines max.

---

## Browser Action Required

- [ ] Enable GitHub secret scanning
      URL: https://github.com/Abdilamir/handoff-forge/settings/security_analysis
      Risk: none

## Completed This Phase

- [x] PR #1 merged: feat: validate command (Greptile 5/5)
- [x] PR #2 merged: fix: tasks insertion position (Greptile 5/5)
- [x] PR #3 merged: feat: handoff --append flag (Greptile 5/5)
- [x] PR #4 merged: docs: README --append documentation (Greptile 5/5)
- [x] PR #5 merged: chore: GitHub Actions CI workflow (Greptile 5/5)
- [x] PR #6 merged: chore: review loop preparation files (Greptile 5/5)
- [x] PR #7 merged: fix: suppress spurious backups in cmd_init and cmd_tasks (Greptile 5/5)
- [x] PR #8 merged: chore: add .gitignore with security patterns (Greptile 5/5)
- [x] PR #9 merged: chore: add SECURITY.md and source --version from __version__ (Greptile 5/5)
- [x] PR #10 merged: test: 18 CLI integration tests (Greptile 5/5)
- [x] PR #11 merged: chore: expand CI to Python 3.13 (Greptile 5/5)
- [x] PR #12 merged: fix: correct README clone URL (Greptile 5/5)
- [x] PR #13 merged: chore: pyproject.toml metadata hardening (Greptile 5/5)
- [x] PR #14 merged: fix: microsecond timestamps and collision detection (Greptile 5/5)
- [x] PR #15 merged: test: coverage gaps (validate output, init content, handoff backup) (Greptile 5/5)
- [x] PR #16 merged: chore: Makefile + ruff in dev deps (Greptile 5/5)
- [x] PR #17 merged: chore: ruff config + CI enforcement (Greptile 5/5)
- [x] PR #18 merged: chore: version bump to 0.1.1 + release history in CHANGELOG (Greptile 5/5)
- [x] PR #19 merged: chore: pip-audit CI job + SECURITY.md dependency audit section (Greptile 5/5)

## TASK FORMAT

Each entry:
```
- [ ] Short description — done = specific exit condition
      Files: path/to/file.py (if known)
      Risk: low | medium | high
```
