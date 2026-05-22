# HANDOFF.md

> This file is always a full rewrite — not an append.
> It represents the current state of the project right now.
> A fresh agent reads this first, before doing anything else.

---

## Session: 2026-05-22 — Phase 3: validate command

### What Was Built
`handoff-forge validate [target-dir]` command.

Checks for the six required agentic engineering OS files in any project directory:
- CLAUDE.md, HANDOFF.md, TASKS.md, PROJECT_STATE.md, CHANGELOG.md, SECURITY.md

Behavior:
- Prints `[OK]` or `[MISSING]` per file
- Exit code 0 = all present
- Exit code 1 = any missing
- Errors on non-existent directory

Files changed:
- `src/handoff_forge/services/file_ops.py` — `check_required_files()` added at end
- `src/handoff_forge/cli.py` — `REQUIRED_FILES` constant, `cmd_validate()`, validate subparser entry
- `tests/test_file_ops.py` — 5 new tests for `check_required_files`
- `README.md` — validate section with full example output added
- `CHANGELOG.md` — Phase 3 entry added

Tests: 33/33 passing. Smoke tested on handoff-forge itself (exit 0) and empty dir (exit 1).
Branch: `feature/validate-command` — NOT yet merged.

### What Is Not Finished
- PR not yet opened on GitHub
- Greptile review not yet run — waiting for GitHub push
- Branch has not been merged to master

### Decisions Made
- `REQUIRED_FILES` constant lives in `cli.py`, not `file_ops.py` — it is configuration for the command, not a service responsibility
- `check_required_files` takes `required: list[str]` as a parameter rather than hardcoding — keeps the service testable and flexible
- No `--fix` flag in this PR — that is a follow-up feature; keeping this PR small is the point

### Next Step
1. Push branch to GitHub:
   ```
   git push -u origin feature/validate-command
   ```
2. Open PR on GitHub — use the PR description below
3. Connect Greptile → wait for automated review
4. Run review loop against Greptile feedback
5. Merge when 5/5

### Known Risks
- None in the implementation
- Greptile may flag `REQUIRED_FILES` living in cli.py as a concern — defensible (see Decisions Made)

---

*Last updated: 2026-05-22 | Session: Phase 3 — validate command*
