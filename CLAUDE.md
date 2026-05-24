# CLAUDE.md — Agent Operating Constitution

## PROJECT

**What this project does:**
handoff-forge is a Python CLI tool that generates and updates HANDOFF.md, PROJECT_STATE.md, and TASKS.md files for AI-assisted engineering sessions. It solves the problem of engineers losing session context between AI coding sessions by making handoff file creation fast, structured, and consistent.

**Vision and end state:**
Done = a developer can run `handoff-forge init ./my-project` and get all three files populated with structured templates, then run `handoff-forge handoff --session "Auth feature"` to generate a complete HANDOFF.md from their notes. The tool runs locally with no network access, no accounts, no configuration files.

**Non-obvious structure conventions:**
- Templates are plain f-strings in `src/handoff_forge/services/templates.py` — do not introduce Jinja2 or any templating engine
- All filesystem I/O goes through `src/handoff_forge/services/file_ops.py` — cli.py never touches the filesystem directly
- Backups use the format `<filename>.bak.<YYYYMMDD-HHMMSS-ffffff>` in the same directory as the original
- The default behavior of every write operation is non-destructive: if a file exists, back it up first

---

## SOURCE CODE CONTEXT

No external packages with source code to fetch — this project uses Python stdlib only.
If a future PR adds a dependency, run: `npx open-source https://github.com/<org>/<repo>`

---

## CODE RULES

1. Before writing any new function, search the codebase for existing implementations
2. All reusable logic lives in `src/handoff_forge/services/`
3. `cli.py` orchestrates — it does not contain business logic
4. After every feature, flag any duplicated code introduced

---

## PR AND CHANGE RULES

5. One feature per PR, target 200 lines, hard cap 400
6. Never modify working behavior unless the task explicitly requires it
7. Before any rename or restructure touching >3 files: restore point first

---

## PACKAGE AND DEPENDENCY RULES

8. Runtime: stdlib only. No exceptions without explicit approval.
9. Dev: pytest only. No additional test tooling without explicit approval.
10. Never install a package published less than 14 days ago

---

## TESTING RULES

11. Every function in services/ must have at least one test
12. Every bug fix needs a test that would have caught it
13. Do not mark a task complete if `pytest` is failing

---

## SAFETY RULES

14. Do not push to remote without explicit instruction
15. Do not modify `.env` files or output secrets
16. Before any refactor touching >3 files, create a restore tag
