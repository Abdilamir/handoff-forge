# DECISIONS.md

---

## 2026-05-22

### [2026-05-22] — stdlib only, no external runtime dependencies
**Decision:** Runtime depends on Python stdlib only (argparse, pathlib, datetime, shutil, textwrap).
**Alternatives considered:** `click` for CLI, `rich` for output formatting.
**Reason:** This project's primary purpose is validating the agentic engineering OS loop, not building a feature-rich tool. Zero runtime deps means zero supply chain risk and zero install friction.
**Consequences:** Output formatting is plain text. No colored output, no progress bars. Acceptable for a dev tool.
**Reversible:** Yes — add click as a dep in a future PR if the interface needs to grow. Low migration cost.

### [2026-05-22] — All file I/O through file_ops.py
**Decision:** `cli.py` never reads or writes files directly. All filesystem operations go through `services/file_ops.py`.
**Alternatives considered:** Direct pathlib calls in cli.py.
**Reason:** Testability. Tests can import and test file_ops in isolation without invoking the CLI. It also makes the backup behavior consistent — one function, one place, one behavior.
**Consequences:** An extra function call for every file operation. Worth it for testability and consistency.
**Reversible:** Low cost to reverse — would just inline the calls into cli.py.

### [2026-05-22] — Templates are f-strings, no templating engine
**Decision:** Markdown templates in `services/templates.py` use Python f-strings.
**Alternatives considered:** Jinja2, string.Template.
**Reason:** Adding a templating engine adds a dependency and complexity for minimal gain. The templates are static enough that f-strings are perfectly readable. Jinja2 is overkill for 4 file formats.
**Consequences:** Template changes require editing Python source rather than template files. Acceptable — these templates are not expected to change frequently.
**Reversible:** Easy — Jinja2 can be introduced later if templates become complex enough to warrant it.

### [2026-05-22] — Default behavior is non-destructive
**Decision:** `init` skips existing files. `handoff` and `state` require explicit `--overwrite`. All overwrites create automatic backups.
**Alternatives considered:** Always overwrite, or ask interactively.
**Reason:** An AI agent running this tool should not silently destroy a handoff file that a developer wrote manually. The default must protect existing work. Backups ensure nothing is unrecoverable.
**Consequences:** Users must pass `--overwrite` to update files, which adds one flag but prevents accidental data loss.
**Reversible:** Yes — flip the default in a future version if users find it annoying.
