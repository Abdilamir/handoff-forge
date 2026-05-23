# TASKS.md

> Active task list only. Completed tasks move to CHANGELOG.md.
> Each task must be PR-sized: one feature, one branch, ~200-400 lines max.

---

## Current — In Progress

- [ ] Run Greptile review loop on PR #1 — fix until 5/5
      Branch: feature/validate-command
      See: plans/PROMPT_grep-loop.md, reviews/PR_1_review_template.md
      Status: Greptile has posted review — awaiting feedback paste into session
      Risk: low

## Blocked on Human Action

- [ ] Paste Greptile's PR #1 review feedback into Claude Code session
      Action: copy the Greptile review comment from GitHub PR #1 and paste here
      Why: grep loop cannot execute without the actual review content

## Next (after PR #1 merged)

- [ ] Merge `feature/validate-command` after Greptile 5/5 + human diff review
      Risk: low — requires approval
      Checklist: all tests passing, CHANGELOG updated, HANDOFF updated

- [ ] Enable GitHub secret scanning
      URL: https://github.com/Abdilamir/handoff-forge/settings/security_analysis
      Risk: none — read-only detection

## Queued — Ready (branches already on origin)

- [ ] Open PR for `chore/add-ci` → merge to master
      Branch: chore/add-ci (on origin)
      Contents: .github/workflows/ci.yml — pytest on Python 3.11 + 3.12
      Risk: low

- [ ] Open PR for `chore/review-prep` → merge to master
      Branch: chore/review-prep (on origin)
      Contents: reviews/PR_1_review_template.md, plans/PROMPT_grep-loop.md
      Risk: low

## Backlog

- [ ] Fix tasks insertion position — new tasks should land inside active phase block, not before TASK FORMAT section
      Files: src/handoff_forge/cli.py (cmd_tasks), tests/test_cli.py
      Risk: low

- [ ] Add --append flag to handoff command for accumulating session notes without full rewrite
      Files: cli.py, templates.py, tests/
      Risk: low

## TASK FORMAT

Each entry:
```
- [ ] Short description — done = specific exit condition
      Files: path/to/file.py (if known)
      Risk: low | medium | high
```
