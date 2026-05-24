# CHANGELOG.md

---

## Release History

### [0.1.1] — 2026-05-24

First feature-complete release. All 17 PRs merged, Greptile 5/5 across the board.

**What's included:**
- `init`, `handoff`, `state`, `tasks`, `validate` — 5 CLI commands, stdlib only
- `handoff --append` for mid-session checkpoint notes (no backup created)
- `validate` exit codes: 0 = all required files present, 1 = any missing
- Non-destructive writes: every overwrite creates a `.bak.<YYYYMMDD-HHMMSS-ffffff>` backup with collision detection
- CI: GitHub Actions matrix on Python 3.11/3.12/3.13 + ruff lint enforcement
- Dev tooling: `Makefile` (install/test/lint/clean), `ruff>=0.4`, `[tool.ruff]` config

**Release checklist:**
- [ ] `pip install -e ".[dev]" && make test` — 78 tests passing
- [ ] `make lint` — ruff clean
- [ ] `python -m build && twine check dist/*`
- [ ] `twine upload dist/*`
- [ ] Create GitHub Release tag `v0.1.1`

### [0.1.0] — 2026-05-22

Initial working release: 5 commands, stdlib only, 28 tests.

---

### [2026-05-24] — chore: add ruff linting to dev deps and CI (PR #17) — MERGED
- **Branch:** `chore/ruff-config`
- **Greptile:** Round 1: 3/5 (ruff dep conflict) → Round 2: 4/5 (redundant matrix runs) → Round 3: 5/5
- **What:** Added `[tool.ruff]` config to `pyproject.toml` (line-length=120, target-version=py311, select=E/F/W/I). Added ruff lint step to CI gated on `matrix.python-version == '3.11'` to avoid redundant identical runs across the matrix. Applied mechanical lint fixes: two long `add_argument` calls reformatted, unused import removed, import order corrected, blank-line violations cleaned up across cli.py and test files.
- **Files changed:** `.github/workflows/ci.yml`, `pyproject.toml`, `src/handoff_forge/cli.py`, `tests/test_cli_commands.py`, `tests/test_file_ops.py`
- **Tests:** 78 (unchanged — purely tooling/style changes)
- **Breaking changes:** None
- **Tags:** `restore/after-pr17-merge`

---

### [2026-05-24] — test: coverage gaps — validate output, init content, handoff backup (PR #15) — MERGED
- **Branch:** `test/coverage-gaps`
- **Greptile:** Round 1: 4/5 (missing length guard on backups[0]) → Round 2: 5/5
- **What:** Added 6 tests: cmd_validate [OK]/[MISSING] output labels; cmd_init section header content in each generated file; cmd_handoff --overwrite backup content verification with explicit length guard.
- **Files changed:** `tests/test_cli_commands.py`, `tests/test_cli.py`, `tests/test_file_ops.py`
- **Tests:** 6 new — 78 total passing
- **Breaking changes:** None
- **Tags:** `restore/after-pr15-pr16-merge`

---

### [2026-05-24] — chore: Makefile with install, test, lint, clean targets (PR #16) — MERGED
- **Branch:** `chore/add-makefile`
- **Greptile:** Round 1: 3/5 (ruff missing from dev deps) → Round 2: 5/5
- **What:** Added `Makefile` with `make install/test/lint/clean`. Added `ruff>=0.4` to dev extras so `make lint` works after `make install`.
- **Files changed:** `Makefile` (new), `pyproject.toml`
- **Breaking changes:** None
- **Tags:** `restore/after-pr15-pr16-merge`

---

### [2026-05-24] — fix: microsecond timestamps and collision detection in backup_file (PR #14) — MERGED
- **Branch:** `fix/backup-microseconds`
- **Greptile:** Round 1: 4/5 (CLAUDE.md format string stale) → Round 2: 5/5
- **What:** Extended backup timestamp from `%Y%m%d-%H%M%S` to `%Y%m%d-%H%M%S-%f`. Added collision detection: if backup path already exists, appends `-1`, `-2`, ... until a free name is found (fixes Windows timer resolution issue where two rapid calls can produce identical microsecond timestamps). Replaced flaky timing-based test with deterministic mock-patched collision test. Updated CLAUDE.md format string.
- **Files changed:** `src/handoff_forge/services/file_ops.py`, `tests/test_file_ops.py`, `CLAUDE.md`
- **Tests:** 1 new (collision resolution) — 72 total passing
- **Breaking changes:** None (backup filename format extends, `.gitignore` `*.bak.*.md` pattern still matches)
- **Tags:** `restore/after-pr14-merge`

---

## 2026-05-24

### [2026-05-24] — chore: expand CI matrix and fix branch trigger patterns (PR #11) — MERGED
- **Branch:** `chore/ci-expand`
- **Greptile:** 5/5
- **What:** Expanded CI Python matrix to include 3.13; added `docs/**` and `test/**` branch triggers to match all naming conventions in use.
- **Files changed:** `.github/workflows/ci.yml`
- **Breaking changes:** None
- **Tags:** `restore/after-pr11-pr12-merge`

---

### [2026-05-24] — fix: replace placeholder repo URL in README (PR #12) — MERGED
- **Branch:** `fix/readme-repo-url`
- **Greptile:** 5/5
- **What:** Replaced `<your-username>` placeholder in README clone URL with the actual `Abdilamir/handoff-forge` URL.
- **Files changed:** `README.md`
- **Breaking changes:** None
- **Tags:** `restore/after-pr11-pr12-merge`

---

### [2026-05-24] — fix: suppress spurious backups in cmd_init and cmd_tasks (PR #7) — MERGED
- **Branch:** `fix/backup-call-sites`
- **Greptile:** Round 1: 4/5 → Round 2: 5/5
- **What:** `cmd_init --overwrite` was double-backing-up each file (explicit `backup_file()` call + `write_file` default `backup=True`). `cmd_tasks` created a backup on every task addition despite the operation being purely additive. Fixed by passing `backup=False` to affected `write_file` calls. Added 3 backup-hygiene tests including all-three-files overwrite coverage.
- **Files changed:** `src/handoff_forge/cli.py`, `tests/test_cli.py`
- **Tests:** 3 new — 53 total passing
- **Breaking changes:** None
- **Tags:** `restore/after-pr7-pr8-pr9-merge`

---

### [2026-05-24] — chore: add .gitignore with security patterns (PR #8) — MERGED
- **Branch:** `chore/add-gitignore`
- **Greptile:** Round 1: 3/5 → Round 2: 5/5
- **What:** Added `.gitignore` with Python, virtual environment, test, distribution, and editor patterns. Crucially added `.env`, `.env.*`, `*.pem`, `*.key` (security regression from initial draft), `open-source/` exclusion, and `*.bak.*.md` pattern matching `backup_file()` output format. Rewrote without UTF-8 BOM.
- **Files changed:** `.gitignore`
- **Breaking changes:** None
- **Tags:** `restore/after-pr7-pr8-pr9-merge`

---

### [2026-05-24] — chore: add SECURITY.md and source --version from __version__ (PR #9) — MERGED
- **Branch:** `chore/project-hygiene`
- **Greptile:** Round 1: 4/5 → Round 2: 5/5
- **What:** Replaced internal-checklist SECURITY.md with a standard public security policy (supported versions table, disclosure channel, security properties). Sourced `--version` from `handoff_forge.__version__` to keep version DRY. Fixed UTF-8 BOM in SECURITY.md.
- **Files changed:** `SECURITY.md`, `src/handoff_forge/cli.py`
- **Breaking changes:** None
- **Tags:** `restore/after-pr7-pr8-pr9-merge`

---

## 2026-05-23

### [2026-05-23] — chore: review loop preparation files (PR #6) — MERGED
- **Branch:** `chore/review-prep`
- **Greptile:** Round 1: 4/5 → Round 2: stale cache (same review returned); fix verified in branch, merged
- **What:** Added `plans/PROMPT_grep-loop.md` (reusable Greptile review-loop session prompt) and `reviews/PR_1_review_template.md` (PR #1 review checklist). Greptile finding: hardcoded PR-1-specific branch/tag names in merge checklist — replaced with `<branch-name>` and `<feature-slug>` placeholders.
- **Files changed:** `plans/PROMPT_grep-loop.md`, `reviews/PR_1_review_template.md`
- **Breaking changes:** None
- **Tags:** `restore/post-review-prep-merge`

---

### [2026-05-23] — chore: GitHub Actions CI workflow (PR #5) — MERGED
- **Branch:** `chore/add-ci`
- **Greptile:** Round 1: 4/5 → Round 2: 5/5 (Round 2 note: missing job timeout — added before merge)
- **What:** Added `.github/workflows/ci.yml` — pytest matrix on Python 3.11 and 3.12, triggered on push to master/feature/**/fix/**/chore/** and PRs targeting master. Round 1 fixes: `permissions: contents: read`, `fail-fast: false`, `cache: "pip"`. Pre-merge: `timeout-minutes: 10`.
- **Files changed:** `.github/workflows/ci.yml` (new)
- **Breaking changes:** None
- **Tags:** `restore/post-ci-merge`

---

### [2026-05-23] — docs: README --append documentation (PR #4) — MERGED
- **Branch:** `docs/readme-append-flag`
- **Greptile:** 5/5 (one finding: stale "end of every session" description — fixed before merge)
- **What:** Updated README `handoff` section with `--append` example, mutual-exclusion note, corrected section description, File Safety clarification (--append never creates backups), and MID-SESSION CHECKPOINT block in workflow loop.
- **Files changed:** `README.md`
- **Breaking changes:** None
- **Tags:** `restore/post-readme-docs-merge`

---

### [2026-05-23] — feat: handoff --append flag (PR #3) — MERGED
- **Branch:** `feat/handoff-append`
- **Greptile:** Round 1: 3/5 → Round 2 (after fixes): 5/5
- **What:** Added `--append` flag to `handoff` subcommand. Appends a compact `## Note:` block to an existing HANDOFF.md instead of a full rewrite. Greptile Round 1 flagged: (1) template header contradiction ("always a full rewrite"), (2) backup file accumulation on every append call. Both fixed before Round 2.
- **Files changed:**
  - `src/handoff_forge/services/templates.py` — updated `handoff_template` header; added `handoff_append_entry()`
  - `src/handoff_forge/services/file_ops.py` — added `backup: bool = True` param to `write_file`
  - `src/handoff_forge/cli.py` — `cmd_handoff` --append path; `--append` flag in parser
  - `tests/test_cli.py` — 3 new tests for `cmd_handoff` (append, create-on-missing, mutual-exclusion)
  - `tests/test_file_ops.py` — `test_write_file_no_backup_when_backup_false`
  - `tests/test_templates.py` — `TestHandoffAppendEntry` (3 tests); `test_header_acknowledges_append`
  - `plans/PLAN_feat-handoff-append.md` — implementation plan
- **Tests:** 8 new — 50 total passing
- **Breaking changes:** None
- **Tags:** `restore/post-handoff-append-merge`

---

### [2026-05-23] — fix: tasks insertion position (PR #2) — MERGED
- **Branch:** `fix/tasks-insertion-position`
- **Greptile:** Round 1: 4/5 → Round 2: 5/5
- **What:** Fixed `cmd_tasks` inserting new tasks before `## TASK FORMAT` instead of inside the first active section. Moved insertion algorithm to `file_ops.py` per CLAUDE.md rules 2&3.
- **Files changed:**
  - `src/handoff_forge/services/file_ops.py` — added `insert_task_entry()`
  - `src/handoff_forge/cli.py` — `cmd_tasks` reduced to 3-line orchestration
  - `tests/test_file_ops.py` — 4 new tests for `insert_task_entry`
  - `tests/test_cli.py` — new file, 5 tests for `cmd_tasks` CLI behavior
  - `plans/PLAN_fix-tasks-insertion.md` — implementation plan
- **Tests:** 9 new — 42 total passing
- **Breaking changes:** None
- **Tags:** `restore/post-tasks-fix-merge`

---

## 2026-05-22

### [2026-05-22] — feat: validate command (PR #1) — MERGED
- **Branch:** `feature/validate-command`
- **Greptile:** 5/5
- **What:** Added `handoff-forge validate [target]` — checks for 6 required OS files, prints status per file, exits 0 (all present) or 1 (any missing)
- **Files changed:**
  - `src/handoff_forge/services/file_ops.py` — added `check_required_files()`
  - `src/handoff_forge/cli.py` — added `cmd_validate()`, `REQUIRED_FILES` constant, validate subparser
  - `tests/test_file_ops.py` — 5 tests for `check_required_files`
  - `README.md` — validate command section with example output
- **Tests:** 5 new — 33 total at merge
- **Tags:** `restore/post-validate-merge`

### [2026-05-22] — Phase 2 complete: handoff-forge v0.1.0
- **Commit:** `restore/project-init` tag
- **What:** Full working CLI — 5 commands (init, handoff, state, tasks, validate), stdlib only, 28 tests
- **Files created:** pyproject.toml, src/handoff_forge/, tests/, README.md, full OS scaffold
