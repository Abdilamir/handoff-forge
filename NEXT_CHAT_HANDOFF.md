# NEXT_CHAT_HANDOFF.md

> Complete context transfer for a new Claude/ChatGPT session on handoff-forge.
> Written: 2026-05-24. Phase 8 complete.

---

## 1. Overall Mission

Build a personal AI-native engineering operating system — a set of tools, workflows, and conventions that allow autonomous AI agents to execute complete software projects with minimal human intervention.

handoff-forge is the first shipped tool in that system. The next milestone is **Project #1: a real revenue-generating product built autonomously using handoff-forge as the operating layer.** Even $1/month is acceptable. The goal is end-to-end autonomous execution, not scale.

---

## 2. What handoff-forge Actually Is Now

A local Python CLI tool (stdlib only, zero runtime dependencies) that solves two problems:

**Problem 1 — Context loss between sessions:** Every AI coding session ends with the agent losing all working memory. handoff-forge standardizes the session handoff files so a fresh agent can read one command's output and immediately continue.

**Problem 2 — Agent orchestration:** Running multi-session autonomous projects requires role-based task delegation, progress checkpointing, and synthesized next-action prompts. handoff-forge now provides all of this.

**Install:**
```bash
git clone https://github.com/Abdilamir/handoff-forge.git
cd handoff-forge
pip install -e .
```

**Version:** 0.1.1  
**Python:** 3.11+  
**Runtime deps:** None (stdlib only)  
**Dev deps:** pytest>=7.4, ruff>=0.4  
**Tests:** 99 passing  
**CI:** GitHub Actions matrix 3.11/3.12/3.13 + ruff (py3.11 only) + pip-audit audit job  
**Repo:** https://github.com/Abdilamir/handoff-forge

---

## 3. Completed Phases

| Phase | What Was Built | PRs |
|-------|---------------|-----|
| Phase 1 | Initial repo scaffold, pyproject.toml, src layout, 28 tests | — |
| Phase 2 | `init`, `handoff`, `state`, `tasks` commands (v0.1.0) | — |
| Phase 3 | `validate` command, `handoff --append`, README docs | PR #1–4 |
| Phase 4 | GitHub Actions CI (3.11/3.12/3.13), .gitignore, SECURITY.md | PR #5–9 |
| Phase 5 | 18 CLI integration tests, CI expansion to 3.13, pyproject.toml metadata hardening | PR #10–13 |
| Phase 6 | Backup microsecond timestamps + collision detection, coverage gap tests, Makefile, ruff enforcement | PR #14–17 |
| Phase 7 | Version bump to 0.1.1, CHANGELOG release history, pip-audit CI job, SECURITY.md dependency audit | PR #18–19 |
| Phase 8 | Agent operating layer: `agents init`, `agent brief`, `next`, `checkpoint` | PR #20 |

**Total: 20 PRs merged. All Greptile reviews resolved. 99 tests passing.**

---

## 4. Architecture Summary

```
handoff-forge/
├── src/handoff_forge/
│   ├── __init__.py              # __version__ = "0.1.1"
│   ├── cli.py                   # Subcommand orchestration only. No business logic.
│   └── services/
│       ├── file_ops.py          # All filesystem I/O (read, write, backup, ensure_dir)
│       └── templates.py         # All markdown generation + agent role specs
├── tests/
│   ├── test_cli_commands.py     # Integration tests for all CLI commands
│   ├── test_file_ops.py         # Unit tests for file_ops.py
│   ├── test_templates.py        # Unit tests for templates.py
│   └── test_agent_commands.py   # Tests for Phase 8 agent commands (99 total w/ above)
├── .github/workflows/ci.yml     # CI: test matrix + ruff + pip-audit
├── pyproject.toml               # Version, deps, ruff config, entry point
├── Makefile                     # install / test / lint / clean
├── CLAUDE.md                    # Agent operating constitution (rules for coding agents)
├── HANDOFF.md                   # Current session handoff (rewritten each session)
├── PROJECT_STATE.md             # Current phase, status, done/in-progress/next
├── TASKS.md                     # Active task list
├── CHANGELOG.md                 # Full PR history
├── SECURITY.md                  # Security policy + dependency audit section
└── NEXT_CHAT_HANDOFF.md         # This file
```

**Architectural invariants (never break these):**
- All filesystem I/O goes through `file_ops.py`. `cli.py` never touches files directly.
- All markdown generation lives in `templates.py`. No Jinja2 or templating engines.
- `cli.py` is orchestration only — it calls services and prints results.
- Runtime: stdlib only. Zero exceptions without explicit user approval.
- Every write is non-destructive by default: `overwrite=False` raises `FileExistsError`.
- `--overwrite` always creates a timestamped `.bak.<YYYYMMDD-HHMMSS-ffffff>` backup.

---

## 5. Complete Command List

### Original 5 commands

```bash
# Scaffold all state files in a project directory
handoff-forge init [target] [--overwrite]

# Generate or update HANDOFF.md
handoff-forge handoff \
  --session "Auth feature" \
  --built "What was implemented" \
  --next "Exact next step" \
  [--incomplete "..."] [--decisions "..."] [--risks "..."] \
  [--target ./project] [--overwrite] [--append]

# Update PROJECT_STATE.md
handoff-forge state \
  --phase "Phase 2" --status "In progress" \
  [--stack "Python 3.11"] [--done "Item 1" "Item 2"] \
  [--progress "..."] [--next "..."] \
  [--target ./project] [--overwrite]

# Append a task to TASKS.md
handoff-forge tasks "Task description — done = exit condition" \
  [--phase "Phase 1"] [--target ./project]

# Validate that all 6 required OS files exist
handoff-forge validate [target]
# Required: CLAUDE.md, HANDOFF.md, TASKS.md, PROJECT_STATE.md, CHANGELOG.md, SECURITY.md
# Exit 0 = all present, Exit 1 = any missing
```

### Phase 8 agent operating layer (4 new commands)

```bash
# Create agents/ directory with 5 role spec markdown files
handoff-forge agents init [target] [--overwrite]
# Creates: agents/engineer.md, reviewer.md, architect.md, operator.md, researcher.md

# Print a ready-to-paste agent brief for Claude
handoff-forge agent brief <role> [--target ./project]
# role must be one of: engineer, reviewer, architect, operator, researcher
# Output: role spec + PROJECT_STATE.md + HANDOFF.md — paste directly to Claude

# Print synthesized next action from all three state files
handoff-forge next [--target ./project]
# Reads: HANDOFF.md (Next Step), TASKS.md (first open task), PROJECT_STATE.md (phase/status)

# Append a timestamped checkpoint to HANDOFF.md (no backup created)
handoff-forge checkpoint \
  --task "Active task description" \
  --next "Exact next step after this checkpoint" \
  [--branch "feat/thing"] [--notes "Any important note"] \
  [--target ./project]
```

---

## 6. Current Operational Workflow

### Standard session loop

```
START OF SESSION:
  handoff-forge next --target ./project
  # OR: handoff-forge agent brief engineer --target ./project
  # Paste output to Claude → agent knows exactly where to continue

MID-SESSION (every 30-60 min or at blockers):
  handoff-forge checkpoint \
    --task "Currently implementing X" \
    --next "After X, do Y" \
    --branch "feat/x"

END OF SESSION (full rewrite):
  handoff-forge handoff \
    --session "Feature X implementation" \
    --built "What was completed" \
    --next "Exact next step" \
    --target ./project --overwrite
```

### Autonomous agent session loop (for Claude Code sessions)

```
1. handoff-forge agent brief engineer --target ./project
   → paste to Claude

2. Claude implements, commits, opens PR

3. Greptile reviews (automatic on PR open)

4. Claude reads findings, fixes, pushes, waits for re-review

5. CI green + Greptile 5/5 → Claude merges:
   git merge --no-ff <branch> -m "Merge <branch>: <description>"
   git push origin master
   git tag restore/after-pr<N>-merge
   git push origin restore/after-pr<N>-merge
   git branch -d <branch>

6. Claude updates state files:
   - CHANGELOG.md (add PR entry at top)
   - TASKS.md (mark task done)
   - PROJECT_STATE.md (update status, move items)
   - HANDOFF.md (full rewrite)

7. git add + commit + push

8. Repeat from step 1
```

---

## 7. GitHub / Greptile / CI Process

### CI configuration

File: `.github/workflows/ci.yml`

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "${{ matrix.python-version }}", cache: "pip" }
      - run: pip install -e ".[dev]"
      - run: python -m pytest  # all 3 versions
      - name: Lint
        if: matrix.python-version == '3.11'  # CRITICAL: gated to run once only
        run: python -m ruff check src/ tests/

  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11", cache: "pip" }
      - run: pip install -e ".[dev]"
      - run: pip install pip-audit==2.10.0  # pinned
      - run: pip-audit
```

**Triggers:** push to `master`, `feature/**`, `feat/**`, `fix/**`, `chore/**`, `test/**`, `docs/**` + PRs targeting master.

### Greptile review process

1. Open PR — Greptile auto-posts inline review comments (usually within 3-5 minutes)
2. Check comment count on the PR to detect new reviews:
   ```powershell
   gh api "repos/Abdilamir/handoff-forge/pulls/<N>/comments" --jq 'length'
   ```
3. Read findings — always look at the last comment's full body
4. Fix findings → push commit → Greptile re-reviews (usually within 3-5 minutes)
5. Repeat until 5/5 (no new P1/P2 findings)

**11-minute merge policy:** If CI is green, PR is MERGEABLE, the identified finding is fixed, and Greptile has not posted a re-review within ~11 minutes → merge without waiting. This prevents indefinite blocking on slow Greptile re-reviews.

**Score interpretation:**
- P1 = critical, must fix
- P2 = high priority, fix before merge
- P3/P4 = lower priority, judgment call
- No findings on a re-review = consider it 5/5

### GH CLI setup

```powershell
# GH_TOKEN is stored in Windows user environment — load it in every PowerShell session:
$env:GH_TOKEN = [System.Environment]::GetEnvironmentVariable("GH_TOKEN", "User")

# gh CLI path:
C:\Program Files\GitHub CLI\gh.exe

# PR body with special characters — MUST use --body-file to avoid arg parsing failures:
$body | Set-Content .pr_body.md -Encoding utf8
gh pr create --title "..." --body-file .pr_body.md
Remove-Item .pr_body.md
```

---

## 8. Restore / Recovery Process

### Restore tags

Every PR merge creates a restore tag on master:

```
restore/after-pr20-merge     ← current (Phase 8 complete)
restore/after-pr19-merge
restore/after-pr18-merge
restore/after-pr17-merge
restore/after-pr15-pr16-merge
...
```

### Recovery commands

```bash
# See all restore tags
git tag | grep restore/

# Reset to a specific restore point (DESTRUCTIVE — confirm with user first)
git checkout restore/after-pr20-merge

# Or create a new branch from a restore tag
git checkout -b recovery/investigate restore/after-pr19-merge

# Before any refactor touching >3 files, create a restore tag first:
git tag restore/<feature-slug>-pre
git push origin restore/<feature-slug>-pre
```

### Standard pre-feature restore tag pattern

```bash
# Before starting a feature:
git tag restore/<feature-slug>-pre
git push origin restore/<feature-slug>-pre

# After merging:
git tag restore/after-pr<N>-merge
git push origin restore/after-pr<N>-merge
```

---

## 9. Agent Operating Layer Details

### Agent role specs

Located at `agents/<role>.md` in any project initialized with `handoff-forge agents init`.

**Five roles:**

| Role | Purpose | Key Constraint |
|------|---------|----------------|
| engineer | Implements features, fixes bugs, writes tests | STOP if task touches auth/payments/secrets |
| reviewer | Reviews PRs for correctness, security, test coverage | Does not implement — only evaluates |
| architect | Designs systems, writes PLAN_<feature>.md files | Does not write production code |
| operator | CI/CD, deployments, secrets management | All production actions require human approval |
| researcher | Investigates options, produces RESEARCH_<topic>.md | Does not implement — delivers findings |

Each role spec contains:
- `## Role` — one-paragraph definition
- `## Responsibilities` — bullet list of what this role does
- `## Allowed Actions` — what the agent may do autonomously
- `## Escalation Rules` — explicit STOP conditions
- `## Output Format` — expected deliverable shape

### `_extract_section` internals

The `next` command's section parser (`templates._extract_section`) is level-aware:
- Determines the markdown heading level of the target header (count `#` chars)
- Stops collecting when it hits any header at the same or higher level (≤ number of `#`)
- Also stops at `---` horizontal rules
- A line must have `# ` (hash + space) to count as a header (prevents `#hashtag` false positives)

This matters because `### Next Step` and `### Known Risks` are both level-3 headers — without level awareness, the parser bleeds through into Known Risks content.

---

## 10. Current Repo Status (2026-05-24)

```
Branch:           master (clean)
Working tree:     clean
Last commit:      chore: update state files after PR #20 merge (Phase 8 complete)
Last restore tag: restore/after-pr20-merge
Version:          0.1.1
Tests:            99 passing
CI:               All green (test 3.11/3.12/3.13 + ruff + audit)
Open PRs:         0
Open issues:      0
```

**Required files status (validate output):**
- CLAUDE.md ✓
- HANDOFF.md ✓
- TASKS.md ✓
- PROJECT_STATE.md ✓
- CHANGELOG.md ✓
- SECURITY.md ✓

---

## 11. What Was Learned

### Greptile behavior
- Greptile posts inline review comments on PRs, not just a summary score
- The overall score is inferred from P1/P2 findings count, not an explicit number
- Re-reviews happen within 3-5 minutes on small fix pushes
- Greptile can get stuck (no re-review) — the 11-minute merge policy prevents indefinite blocking
- `gh api repos/.../pulls/<N>/comments` is the reliable way to read Greptile findings; `gh pr view --comments` requires `read:org` scope

### Windows/PowerShell specifics
- `GH_TOKEN` must be loaded from Windows user env each PowerShell session
- `git commit -m` with here-strings (`@'...'@`) fails with multiline content containing special chars — use a simple single-line `$msg` variable instead
- `gh pr create --body "..."` fails on backticks and special characters — always use `--body-file`
- PowerShell `&&` operator doesn't exist in PS 5.1 — use `;` or `if ($?) { ... }`
- `head` command doesn't exist — use `| Select-Object -First N`

### CI patterns
- The ruff lint step MUST be gated to one Python version: `if: matrix.python-version == '3.11'`
- pip-audit runs as a separate `audit` job, not inside the test matrix (version-agnostic, runs once)
- pip-audit must be pinned (`pip-audit==2.10.0`) for reproducible CI

### Architecture lessons
- Service-layer separation (`file_ops.py` / `templates.py` / `cli.py`) paid off immediately — every Greptile finding was localized to one file
- Stdlib-only constraint is a competitive advantage for distribution, not a burden
- Non-destructive write semantics with automatic backups eliminated an entire class of "oops" scenarios

---

## 12. What NOT to Over-Engineer

- **No config files.** Every option is a CLI flag. Global state would break the "read this file and continue" mental model.
- **No plugin system.** The tool does 9 things and does them well. Extensibility is not a goal.
- **No external templating engines.** f-strings in `templates.py` are readable, testable, and dependency-free.
- **No database.** HANDOFF.md, TASKS.md, PROJECT_STATE.md are the database. Plain text is always correct.
- **No PyPI publish pressure.** The 30-60 day hold-for-real-usage recommendation stands. The external maintenance burden of a public package is real.
- **No test coverage metrics or coverage tools.** The test suite is small enough to reason about directly.
- **No type stub generation or complex CI additions.** The current CI is correct and complete.

---

## 13. Pre-PyPI Blockers (when the time comes)

Three things must happen before PyPI publish:

1. **Add LICENSE file** — MIT license. Without it, the package is technically "all rights reserved."
   ```bash
   # Create LICENSE file with MIT text, commit, push
   ```

2. **Add `pip install handoff-forge` install path to README** — Currently README only shows `git clone` install. PyPI users need `pip install handoff-forge` as the primary install path.

3. **Enable GitHub secret scanning** (browser action — cannot be automated):
   URL: https://github.com/Abdilamir/handoff-forge/settings/security_analysis

**PyPI publish commands (when all blockers resolved):**
```bash
pip install build twine
python -m build
twine check dist/*
twine upload dist/*
# Then: create GitHub Release v0.1.1 via gh release create v0.1.1
```

---

## 14. Project #1 Objective

**Goal:** Build a real, revenue-generating project autonomously using handoff-forge as the operating layer.

**Constraints:**
- Must be autonomous — agents execute the work with minimal human intervention
- Must generate real revenue — even $1/month is a valid success signal
- Must use handoff-forge's agent operating layer in a real project context
- The project itself should be selected for speed-to-revenue, not scope

**Why this matters:**
- Validates handoff-forge as an actual agent operating layer, not just a note-taking CLI
- Produces feedback on what the `next`, `checkpoint`, and `agent brief` commands actually need
- Demonstrates the core thesis: AI agents + structured handoffs = autonomous revenue

**Candidate project types** (fast-to-revenue, low ops burden):
- A single-purpose API (SaaS micro-tool) — one endpoint, one use case, Stripe checkout
- A simple AI wrapper (prompt-to-output, charge per use) — no infra beyond API
- A content automation tool (generates something people pay for)
- A developer utility (CLI tool, paid license model)

**How to start Project #1 with handoff-forge:**
```bash
# In the new project directory:
handoff-forge init ./project-1
handoff-forge agents init ./project-1

# At the start of every agent session:
handoff-forge agent brief engineer --target ./project-1
# Paste the output to Claude. Claude reads it and starts executing.

# Mid-session checkpoints:
handoff-forge checkpoint --task "..." --next "..." --target ./project-1

# End of session:
handoff-forge handoff --session "..." --built "..." --next "..." \
  --target ./project-1 --overwrite

# Next session:
handoff-forge next --target ./project-1
```

---

## 15. Future Phase 9 Ideas

These are collected from Greptile findings, user feedback, and real-usage gaps. Do not implement until Project #1 surface-tests them:

1. **`handoff-forge review` command** — reads last PR diff + HANDOFF.md, generates a structured review prompt for Claude reviewer agent
2. **`handoff-forge status` command** — prints a one-line project health dashboard (phase, open tasks count, last checkpoint age)
3. **Role validation in argparse** — add `choices=AGENT_ROLES` to the `agent brief` role argument so the parser rejects invalid roles before reaching the command function
4. **`handoff-forge changelog add` command** — structured PR entry appender so CHANGELOG updates don't require manual editing
5. **`handoff-forge plan` command** — creates `plans/PLAN_<feature>.md` with a standard template for architect role
6. **Multi-project support** — `handoff-forge projects list` / `set-default` for users with many projects
7. **`handoff-forge brief --role all`** — print all role specs concatenated for a meta-agent session

---

## 16. Exact Commands for Starting the Next Project with Agents

```bash
# Step 1: Create the new project directory
mkdir my-new-project
cd my-new-project

# Step 2: Initialize all handoff-forge state files
handoff-forge init .
# Creates: HANDOFF.md, PROJECT_STATE.md, TASKS.md

# Step 3: Create required OS files (do manually or template)
# CLAUDE.md — operating constitution for agents (what they can/cannot do)
# CHANGELOG.md — PR history log
# SECURITY.md — security policy

# Step 4: Initialize agent role specs
handoff-forge agents init .
# Creates: agents/engineer.md, reviewer.md, architect.md, operator.md, researcher.md

# Step 5: Validate all required files are present
handoff-forge validate .

# Step 6: Update PROJECT_STATE.md with the actual project
handoff-forge state \
  --phase "Phase 1" \
  --status "Starting — defining scope" \
  --stack "Python 3.11, FastAPI, Stripe" \
  --next "Define MVP scope and first task" \
  --overwrite

# Step 7: Add your first task
handoff-forge tasks "Define MVP scope — done = TASKS.md has 3-5 concrete tasks" \
  --phase "Phase 1"

# Step 8: Write the initial handoff
handoff-forge handoff \
  --session "Project initialization" \
  --built "Scaffolded all OS files, defined Phase 1 scope" \
  --next "Implement first task from TASKS.md" \
  --overwrite

# Step 9: Start the first agent session
handoff-forge agent brief engineer .
# Paste output to Claude → agent reads it and starts executing

# Step 10: Mid-session checkpoint
handoff-forge checkpoint \
  --task "Implementing user auth endpoint" \
  --next "Add Stripe checkout after auth is done" \
  --branch "feat/auth"

# Step 11: End of session
handoff-forge handoff \
  --session "Auth endpoint implementation" \
  --built "POST /auth/login and /auth/register complete, tests passing" \
  --next "Implement Stripe checkout — see plans/PLAN_stripe.md" \
  --overwrite

# Step 12: Start next session
handoff-forge next .
# Paste output to Claude → zero re-priming needed
```

---

## 17. Recovery / What To Do If You're Lost

**If you don't know what to do next:**
```bash
handoff-forge next --target ./handoff-forge
```

**If you need to re-prime an agent from scratch:**
```bash
handoff-forge agent brief engineer --target ./handoff-forge
```

**If master is broken:**
```bash
git log --oneline --tags
git checkout restore/after-pr20-merge  # or latest restore tag
```

**If CI is failing:**
```bash
python -m pytest                    # run tests locally first
python -m ruff check src/ tests/    # run ruff locally
pip-audit                           # run audit locally
```

**If Greptile is stuck (no re-review after 11 min):**
- Check: is CI green? Is PR MERGEABLE? Was the finding fixed?
- If all yes → merge with no-ff, create restore tag, continue

---

*Last updated: 2026-05-24 | Phase 8 complete | 20 PRs merged | 99 tests passing*
