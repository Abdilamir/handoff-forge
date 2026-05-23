# TASKS.md

> Active task list only. Completed tasks move to CHANGELOG.md.
> Each task must be PR-sized: one feature, one branch, ~200-400 lines max.

---

## Current — In Progress

- [ ] fix: tasks insertion position
      Branch: fix/tasks-insertion-position (pushed to origin)
      Plan: plans/PLAN_fix-tasks-insertion.md
      Status: implemented + 37 tests passing — awaiting PR open + Greptile review
      Risk: low

## Queued — Ready (branches on origin, PRs not yet opened)

- [ ] Open PR for `chore/add-ci` → merge to master
      Branch: chore/add-ci
      Contents: .github/workflows/ci.yml — pytest on Python 3.11 + 3.12
      Risk: low

- [ ] Open PR for `chore/review-prep` → merge to master
      Branch: chore/review-prep
      Contents: reviews/PR_1_review_template.md, plans/PROMPT_grep-loop.md
      Risk: low

## Browser Actions Required

- [ ] Open PR for `fix/tasks-insertion-position`
      URL: https://github.com/Abdilamir/handoff-forge/compare/master...fix/tasks-insertion-position
      Risk: none

- [ ] Enable GitHub secret scanning
      URL: https://github.com/Abdilamir/handoff-forge/settings/security_analysis
      Risk: none

## Backlog

- [ ] Add --append flag to handoff command for accumulating session notes without full rewrite
      Files: cli.py, templates.py, tests/test_cli.py
      Risk: low

## TASK FORMAT

Each entry:
```
- [ ] Short description — done = specific exit condition
      Files: path/to/file.py (if known)
      Risk: low | medium | high
```
