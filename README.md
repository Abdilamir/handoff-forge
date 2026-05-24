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
- **Backups:** When `--overwrite` is used, the existing file is copied to `<filename>.bak.<YYYYMMDD-HHMMSS>` in the same directory before being replaced. `--append` never creates backups — it only extends the file.
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

## How It Fits the Agentic Engineering OS

This tool is part of the [agentic-engineering-os](../agentic-engineering-os) workflow. The intended loop:

```
MID-SESSION CHECKPOINT:
  handoff-forge handoff --session "..." --built "..." --next "..." --append

END OF SESSION (full rewrite):
  handoff-forge handoff --session "..." --built "..." --next "..."

START OF NEXT SESSION (Claude Code prompt):
  "Read HANDOFF.md. Do not write any code. Tell me what was last completed and what the exact next step is."
```
