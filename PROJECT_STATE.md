# PROJECT_STATE.md

---

## Current Phase
Phase 7 — PyPI & Release Prep

## Status
18 PRs merged, all Greptile 5/5. 78 tests passing. CI runs on Python 3.11/3.12/3.13 with ruff enforced on 3.11. Version 0.1.1. PR #19 (pip-audit) open.

## Stack
- Language: Python 3.11+
- Runtime dependencies: none (stdlib only)
- Dev dependencies: pytest>=7.4, ruff>=0.4
- Entry point: `handoff-forge` CLI via pyproject.toml scripts
- CI: GitHub Actions — matrix 3.11/3.12/3.13 + ruff lint step (gated to 3.11)
- Make targets: install, test, lint, clean

## What Is Done
- [x] PR #1: feat: add validate command (Greptile 5/5, 33 tests)
- [x] PR #2: fix: tasks insertion position (Greptile 5/5, 42 tests)
- [x] PR #3: feat: handoff --append flag (Greptile 5/5, 50 tests)
- [x] PR #4: docs: README --append documentation (Greptile 5/5)
- [x] PR #5: chore: GitHub Actions CI workflow (Greptile 5/5)
- [x] PR #6: chore: review loop preparation files (Greptile 5/5)
- [x] PR #7: fix: suppress spurious backups in cmd_init/cmd_tasks (Greptile 5/5, 53 tests)
- [x] PR #8: chore: add .gitignore with security patterns (Greptile 5/5)
- [x] PR #9: chore: add SECURITY.md and source --version from __version__ (Greptile 5/5)
- [x] PR #10: test: 18 CLI integration tests (Greptile 5/5, 71 tests)
- [x] PR #11: chore: expand CI to Python 3.13 (Greptile 5/5)
- [x] PR #12: fix: correct README clone URL (Greptile 5/5)
- [x] PR #13: chore: pyproject.toml metadata hardening (Greptile 5/5)
- [x] PR #14: fix: microsecond timestamps and collision detection in backup_file (Greptile 5/5, 72 tests)
- [x] PR #15: test: validate output, init content, handoff backup coverage (Greptile 5/5, 78 tests)
- [x] PR #16: chore: Makefile (install/test/lint/clean) + ruff in dev deps (Greptile 5/5)
- [x] PR #17: chore: [tool.ruff] config + CI ruff enforcement (gated to py3.11) (Greptile 5/5)
- [x] PR #18: chore: version bump to 0.1.1 + release history section in CHANGELOG (Greptile 5/5)
- [x] 12 restore tags created
- [x] .gitignore with security patterns
- [x] SECURITY.md — public disclosure policy
- [x] ruff>=0.4 in dev deps, [tool.ruff] configured with line-length=120, enforced on CI

## What Is In Progress
- PR #19 (chore/pip-audit): pip-audit CI job + SECURITY.md documentation — awaiting Greptile review

## What Is Next
- Merge PR #19 after Greptile 5/5
- Enable GitHub secret scanning (browser action required)
- PyPI publish: `python -m build && twine check dist/* && twine upload dist/*`

## Known Issues
- None

## Last Updated
2026-05-24
