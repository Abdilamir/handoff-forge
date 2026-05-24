# handoff-forge

CLI tool for generating and updating AI engineering session handoff files.

Solves the context-loss problem between AI coding sessions. Run one command at the end of a session to produce a structured HANDOFF.md, PROJECT_STATE.md, and TASKS.md that a fresh agent can read and immediately continue from.

---

## Install

```bash
# Clone and install locally
git clone https://github.com/Abdilamir/handoff-forge.git
cd handoff-forge
pip install -e .

# Verify
handoff-forge --version
```

**Requirements:** Python 3.11+, no external runtime dependencies.

---

## Commands

### `init` — Scaffold handoff files in a project

Creates HANDOFF.md, PROJECT_STATE.md, and TASKS.md in the target directory with starter templates. Safe by default — skips files that already exist.

```bash
# Initialize in the current directory
handoff-forge init

# Initialize in a specific project folder
handoff-forge init ./my-project

# Replace existing files (creates timestamped backups automatically)
handoff-forge init ./my-project --overwrite
```

---

### `handoff` — Generate or update HANDOFF.md

Writes a complete, structured HANDOFF.md from your session notes. Use at the end of a session for a full rewrite, or with `--append` for a compact mid-session checkpoint.

```bash
handoff-forge handoff \
  --session "Auth feature — JWT implementation" \
  --built "Added /auth/login and /auth/refresh endpoints with JWT signing" \
  --next "Implement token blacklist in Redis — see plans/PLAN_auth.md step 3" \
  --decisions "Chose JWT over sessions: stateless, fits current infra" \
  --incomplete "Token refresh not tested under concurrent load" \
  --risks "JWT secret currently hardcoded in dev config — move to env before prod"

# Target a specific project directory
handoff-forge handoff --session "..." --built "..." --next "..." --target ./my-project

# Overwrite an existing HANDOFF.md (backup created automatically)
handoff-forge handoff --session "..." --built "..." --next "..." --overwrite

# Append a compact mid-session note without overwriting the full file
handoff-forge handoff \
  --session "Auth feature — mid-session checkpoint" \
  --built "Login endpoint done, refresh endpoint 50% complete" \
  --next "Finish refresh endpoint — token signing logic in auth/tokens.py" \
  --append
```

`--append` adds a compact `## Note:` block to the bottom of an existing HANDOFF.md. If no HANDOFF.md exists, it creates a full file. `--append` and `--overwrite` are mutually exclusive.

---

### `state` — Update PROJECT_STATE.md

Rewrites PROJECT_STATE.md with current phase, status, and progress. Use after milestones or phase transitions.

```bash
handoff-forge state \
  --phase "Phase 2" \
  --status "In progress — CLI commands complete" \
  --stack "Python 3.11, stdlib only, pytest" \
  --done "Core services implemented" "28 tests passing" "CLI commands working" \
  --progress "Writing README and final polish" \
  --next "Open first PR, run Greptile review"

# Target a specific project
handoff-forge state --phase "..." --status "..." --target ./my-project --overwrite
```

---

### `tasks` — Append a task to TASKS.md

Adds a single task entry to TASKS.md. Appends to an existing file or creates a new one.

```bash
# Add a task (include exit condition for clarity)
handoff-forge tasks "Implement token blacklist — done = integration test passes"

# Target a specific project
handoff-forge tasks "Write deployment guide" --target ./my-project

# Specify phase name (only used when creating a new TASKS.md)
handoff-forge tasks "First task" --phase "Phase 1"
```

---

### `validate` — Check whether a project has all required OS files

Checks for the presence of the six required agentic engineering OS files. Prints each file's status and exits with code 0 (all present) or 1 (any missing).

```bash
# Validate the current directory
handoff-forge validate

# Validate a specific project
handoff-forge validate ./my-project
```

**Example output — complete project:**
```
Validating: /path/to/my-project

  [OK]      CLAUDE.md
  [OK]      HANDOFF.md
  [OK]      TASKS.md
  [OK]      PROJECT_STATE.md
  [OK]      CHANGELOG.md
  [OK]      SECURITY.md

All required files present.
```

**Example output — incomplete project:**
```
Validating: /path/to/my-project

  [OK]      CLAUDE.md
  [MISSING] HANDOFF.md
  [OK]      TASKS.md
  [MISSING] PROJECT_STATE.md
  [OK]      CHANGELOG.md
  [OK]      SECURITY.md

2 file(s) missing.
```

**Required files checked:** `CLAUDE.md`, `HANDOFF.md`, `TASKS.md`, `PROJECT_STATE.md`, `CHANGELOG.md`, `SECURITY.md`

---

## File Safety

- **Default behavior:** `init` skips files that already exist. `handoff` and `state` require `--overwrite` to replace existing files.
- **Backups:** When `--overwrite` is used, the existing file is copied to `<filename>.bak.<YYYYMMDD-HHMMSS-ffffff>` in the same directory before being replaced. `--append` and `checkpoint` never create backups — they only extend the file.
- **No network access:** All commands are fully local. No API calls, no accounts, no telemetry.

---

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest

# Run a specific test file
python -m pytest tests/test_file_ops.py -v
```

---

## Agent Operating Layer

handoff-forge includes a set of commands for running projects with autonomous agents. The agent operating layer manages role specs, session continuity, and next-action synthesis so agents can resume work without human re-priming.

### Workflow: start a new project with agents

```bash
# 1. Initialize project state files
handoff-forge init ./my-project

# 2. Initialize agent role specs
handoff-forge agents init ./my-project
# Creates: my-project/agents/{engineer,reviewer,architect,operator,researcher}.md

# 3. Brief an agent at session start — paste the output directly to Claude
handoff-forge agent brief engineer --target ./my-project

# 4. During the session: drop a checkpoint (no backup created)
handoff-forge checkpoint \
  --task "Implementing auth endpoints" \
  --next "Write integration tests for /auth/login" \
  --branch "feat/auth" \
  --target ./my-project

# 5. At session end: write the full handoff
handoff-forge handoff \
  --session "Auth endpoints" \
  --built "POST /auth/login and /auth/refresh implemented" \
  --next "Write integration tests — see plans/PLAN_auth.md step 3" \
  --target ./my-project --overwrite

# 6. Start the next session: get the next action synthesized from all state files
handoff-forge next --target ./my-project
# Paste the output to Claude. Done.
```

### Agent commands

#### `agents init [target] [--overwrite]`

Creates an `agents/` directory with default role specs for: `engineer`, `reviewer`, `architect`, `operator`, `researcher`. Each spec defines the role, responsibilities, allowed actions, escalation rules, and output format.

```bash
handoff-forge agents init ./my-project
handoff-forge agents init ./my-project --overwrite  # replaces existing specs with backups
```

#### `agent brief <role> [--target]`

Prints a ready-to-use agent brief — the role spec from `agents/<role>.md` combined with the current `PROJECT_STATE.md` and `HANDOFF.md`. Paste the output directly to Claude to start a focused agent session.

```bash
handoff-forge agent brief engineer
handoff-forge agent brief reviewer --target ./my-project
```

#### `next [--target]`

Reads `HANDOFF.md`, `TASKS.md`, and `PROJECT_STATE.md` and outputs the synthesized next action. Replaces the manual "Read HANDOFF.md and tell me what's next" prompt.

```bash
handoff-forge next
handoff-forge next --target ./my-project
```

#### `checkpoint --task "..." --next "..." [--branch] [--notes] [--target]`

Appends a timestamped checkpoint entry to `HANDOFF.md`. Use mid-session to record progress without a full rewrite. No backup is created.

```bash
handoff-forge checkpoint \
  --task "Implementing auth endpoints" \
  --next "Write integration tests" \
  --branch "feat/auth" \
  --notes "JWT secret is in .env — do not commit"
```

---

## How It Fits the Agentic Engineering OS

The intended full session loop:

```
START OF SESSION:
  handoff-forge next --target ./my-project
  # paste output to Claude → agent knows exactly what to do

  # OR brief a specific agent role:
  handoff-forge agent brief engineer --target ./my-project

MID-SESSION CHECKPOINT:
  handoff-forge checkpoint --task "..." --next "..." --branch "feat/x"

  # OR append a handoff note:
  handoff-forge handoff --session "..." --built "..." --next "..." --append

END OF SESSION (full rewrite):
  handoff-forge handoff --session "..." --built "..." --next "..." --overwrite
```
