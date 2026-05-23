# TASKS.md

> Active task list only. Completed tasks move to CHANGELOG.md.
> Each task must be PR-sized: one feature, one branch, ~200-400 lines max.

---

## Current — In Progress

- [ ] feat: handoff --append flag
      Branch: feat/handoff-append (in progress locally)
      Plan: plans/PLAN_feat-handoff-append.md
      Status: implemented, 48 tests passing — needs push + PR
      Risk: low

## Browser Actions Required

- [ ] Open PR for `feat/handoff-append` once pushed
      Risk: none

- [ ] Open PR for `chore/add-ci` → merge to master
      Branch: chore/add-ci (on origin)
      Contents: .github/workflows/ci.yml
      Risk: low

- [ ] Open PR for `chore/review-prep` → merge to master
      Branch: chore/review-prep (on origin)
      Contents: reviews/PR_1_review_template.md, plans/PROMPT_grep-loop.md
      Risk: low

- [ ] Enable GitHub secret scanning
      URL: https://github.com/Abdilamir/handoff-forge/settings/security_analysis
      Risk: none

## Backlog

- [ ] Update README.md with --append flag documentation
      Files: README.md
      Risk: low

## TASK FORMAT

Each entry:
```
- [ ] Short description — done = specific exit condition
      Files: path/to/file.py (if known)
      Risk: low | medium | high
```
