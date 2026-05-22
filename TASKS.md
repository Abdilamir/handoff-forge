# TASKS.md

> Active task list only. Completed tasks move to CHANGELOG.md.
> Each task must be PR-sized: one feature, one branch, ~200-400 lines max.

---

## Current — Immediate (external blockers, require browser)

- [ ] Open PR on GitHub for `feature/validate-command`
      URL: https://github.com/Abdilamir/handoff-forge/compare/master...feature/validate-command
      Risk: none — branch already pushed

- [ ] Connect Greptile to handoff-forge repo (Phase 3 review loop)
      URL: https://greptile.com → authorize GitHub → select handoff-forge
      Risk: none — read-only GitHub access

- [ ] Enable GitHub secret scanning
      URL: https://github.com/Abdilamir/handoff-forge/settings/security_analysis
      Risk: none — read-only detection

## Queued — Ready to Push (branches already committed locally)

- [ ] Push `chore/add-ci` branch and open PR
      Branch: chore/add-ci (committed locally)
      Contents: .github/workflows/ci.yml — pytest on Python 3.11 + 3.12
      Risk: low

- [ ] Push `chore/review-prep` branch and merge
      Branch: chore/review-prep (committed locally)
      Contents: reviews/PR_1_review_template.md, plans/PROMPT_grep-loop.md
      Risk: low

## After Review Loop (blocked on Greptile)

- [ ] Run Greptile review loop on PR 1 — fix until 5/5
      See: plans/PROMPT_grep-loop.md, reviews/PR_1_review_template.md
      Risk: low

- [ ] Merge `feature/validate-command` after Greptile 5/5 + human diff review
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
