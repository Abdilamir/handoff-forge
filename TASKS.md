# TASKS.md

> Active task list only. Completed tasks move to CHANGELOG.md.
> Each task must be PR-sized: one feature, one branch, ~200-400 lines max.

---

## Current — In Progress

- [ ] docs: update README with --append flag documentation
      Branch: docs/readme-append-flag (pushed, awaiting PR + Greptile)
      Files: README.md
      Risk: low

## Browser Actions Required (unblocked)

- [ ] Open PR for `docs/readme-append-flag` → merge to master
      URL: https://github.com/Abdilamir/handoff-forge/compare/master...docs/readme-append-flag
      Risk: low

- [ ] Open PR for `chore/add-ci` → merge to master
      Branch: chore/add-ci (on origin)
      Contents: .github/workflows/ci.yml
      URL: https://github.com/Abdilamir/handoff-forge/compare/master...chore/add-ci
      Risk: low

- [ ] Open PR for `chore/review-prep` → merge to master
      Branch: chore/review-prep (on origin)
      Contents: reviews/PR_1_review_template.md, plans/PROMPT_grep-loop.md
      URL: https://github.com/Abdilamir/handoff-forge/compare/master...chore/review-prep
      Risk: low

- [ ] Enable GitHub secret scanning
      URL: https://github.com/Abdilamir/handoff-forge/settings/security_analysis
      Risk: none

## Completed This Phase

- [x] PR #1 merged: feat: validate command (Greptile 5/5)
- [x] PR #2 merged: fix: tasks insertion position (Greptile 5/5)
- [x] PR #3 merged: feat: handoff --append flag (Greptile 3/5 → 5/5)

## TASK FORMAT

Each entry:
```
- [ ] Short description — done = specific exit condition
      Files: path/to/file.py (if known)
      Risk: low | medium | high
```
