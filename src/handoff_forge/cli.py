"""
handoff-forge CLI entry point.

Subcommands:
  init     — create HANDOFF.md, PROJECT_STATE.md, TASKS.md in a target directory
  handoff  — generate or overwrite HANDOFF.md with session notes
  state    — update PROJECT_STATE.md
  tasks    — append a task entry to TASKS.md
  validate — check whether a project contains all required OS files
"""

import argparse
import sys
from pathlib import Path

from handoff_forge.services import file_ops, templates


REQUIRED_FILES = [
    "CLAUDE.md",
    "HANDOFF.md",
    "TASKS.md",
    "PROJECT_STATE.md",
    "CHANGELOG.md",
    "SECURITY.md",
]


def cmd_validate(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()

    if not target.is_dir():
        print(f"Error: {target} is not a directory.", file=sys.stderr)
        return 1

    print(f"Validating: {target}\n")

    results = file_ops.check_required_files(target, REQUIRED_FILES)

    for filename, present in results.items():
        status = "[OK]     " if present else "[MISSING]"
        print(f"  {status} {filename}")

    missing = [f for f, ok in results.items() if not ok]

    print()
    if missing:
        print(f"{len(missing)} file(s) missing.")
        return 1

    print("All required files present.")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    file_ops.ensure_directory(target)

    files = {
        "HANDOFF.md": templates.handoff_template(
            session="Project initialized",
            what_built="Project scaffold created by handoff-forge init",
            not_finished="All features pending",
            decisions="None yet",
            next_step="Define your first task in TASKS.md and begin implementation",
            risks="None",
        ),
        "PROJECT_STATE.md": templates.project_state_template(
            phase="Phase 1",
            status="Starting",
            stack="[Fill in your stack]",
            done_items=[],
            in_progress="Nothing yet",
            next_steps="[Define next steps]",
        ),
        "TASKS.md": templates.tasks_template(
            phase="Phase 1",
            tasks=[],
        ),
    }

    created, skipped, backed_up = [], [], []

    for filename, content in files.items():
        path = target / filename
        if file_ops.file_exists(path):
            if args.overwrite:
                backup = file_ops.backup_file(path)
                file_ops.write_file(path, content, overwrite=True)
                backed_up.append(f"  {filename} (backup: {backup.name})")
            else:
                skipped.append(f"  {filename} — already exists, use --overwrite to replace")
        else:
            file_ops.write_file(path, content)
            created.append(f"  {filename}")

    if created:
        print(f"Created in {target}:")
        print("\n".join(created))
    if backed_up:
        print(f"Replaced (with backup) in {target}:")
        print("\n".join(backed_up))
    if skipped:
        print("Skipped (already exist):")
        print("\n".join(skipped))

    return 0


def cmd_handoff(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    path = target / "HANDOFF.md"

    content = templates.handoff_template(
        session=args.session,
        what_built=args.built,
        not_finished=args.incomplete or "Nothing — session completed fully",
        decisions=args.decisions or "No new architecture decisions",
        next_step=args.next,
        risks=args.risks or "None identified",
    )

    try:
        result = file_ops.write_file(path, content, overwrite=args.overwrite)
        print(f"Written: {result}")
    except FileExistsError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


def cmd_state(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    path = target / "PROJECT_STATE.md"

    done_items = args.done if args.done else []

    content = templates.project_state_template(
        phase=args.phase,
        status=args.status,
        stack=args.stack or "[Stack unchanged — update manually]",
        done_items=done_items,
        in_progress=args.progress or "Nothing currently in progress",
        next_steps=args.next or "[Define next steps]",
    )

    try:
        result = file_ops.write_file(path, content, overwrite=args.overwrite)
        print(f"Written: {result}")
    except FileExistsError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


def cmd_tasks(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    path = target / "TASKS.md"

    entry = templates.task_entry(args.task)

    if file_ops.file_exists(path):
        existing = file_ops.read_file(path) or ""
        lines = existing.splitlines(keepends=True)
        section_starts = [i for i, line in enumerate(lines) if line.startswith("## ")]
        if section_starts:
            # Find end of first section: next ## header, a --- separator, or EOF
            first_end = len(lines)
            for i in range(section_starts[0] + 1, len(lines)):
                if lines[i].startswith("## ") or lines[i].strip() == "---":
                    first_end = i
                    break
            # Insert after last non-blank line in first section
            insert_at = first_end
            while insert_at > section_starts[0] + 1 and not lines[insert_at - 1].strip():
                insert_at -= 1
            new_lines = lines[:insert_at] + [f"{entry}\n"] + lines[insert_at:]
            updated = "".join(new_lines)
        else:
            updated = existing.rstrip() + f"\n{entry}\n"
        file_ops.write_file(path, updated, overwrite=True)
    else:
        # No existing file — create a minimal one with this task
        content = templates.tasks_template(
            phase=args.phase or "Current Phase",
            tasks=[args.task],
        )
        file_ops.write_file(path, content)

    print(f"Task added to {path}:")
    print(f"  {entry}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="handoff-forge",
        description="Generate and update AI engineering session handoff files",
    )
    parser.add_argument("--version", action="version", version="handoff-forge 0.1.0")
    sub = parser.add_subparsers(dest="command", required=True)

    # init
    p_init = sub.add_parser("init", help="Create HANDOFF.md, PROJECT_STATE.md, TASKS.md in target directory")
    p_init.add_argument("target", nargs="?", default=".", help="Target directory (default: current directory)")
    p_init.add_argument("--overwrite", action="store_true", help="Replace existing files (creates backups)")
    p_init.set_defaults(func=cmd_init)

    # handoff
    p_handoff = sub.add_parser("handoff", help="Generate or update HANDOFF.md")
    p_handoff.add_argument("--session", required=True, help="Session name, e.g. 'Auth feature'")
    p_handoff.add_argument("--built", required=True, help="What was built this session")
    p_handoff.add_argument("--next", required=True, help="Exact next step for the next session")
    p_handoff.add_argument("--incomplete", help="What was not finished (optional)")
    p_handoff.add_argument("--decisions", help="Architecture decisions made (optional)")
    p_handoff.add_argument("--risks", help="Known risks (optional)")
    p_handoff.add_argument("--target", default=".", help="Directory containing HANDOFF.md (default: .)")
    p_handoff.add_argument("--overwrite", action="store_true", help="Overwrite existing HANDOFF.md (creates backup)")
    p_handoff.set_defaults(func=cmd_handoff)

    # state
    p_state = sub.add_parser("state", help="Update PROJECT_STATE.md")
    p_state.add_argument("--phase", required=True, help="Current phase name")
    p_state.add_argument("--status", required=True, help="Current status description")
    p_state.add_argument("--stack", help="Tech stack description (optional)")
    p_state.add_argument("--done", nargs="+", metavar="ITEM", help="Completed items (repeatable)")
    p_state.add_argument("--progress", help="What is currently in progress")
    p_state.add_argument("--next", help="What is next")
    p_state.add_argument("--target", default=".", help="Directory containing PROJECT_STATE.md (default: .)")
    p_state.add_argument("--overwrite", action="store_true", help="Overwrite existing file (creates backup)")
    p_state.set_defaults(func=cmd_state)

    # tasks
    p_tasks = sub.add_parser("tasks", help="Append a task to TASKS.md")
    p_tasks.add_argument("task", help="Task description — include exit condition")
    p_tasks.add_argument("--phase", help="Phase name (used only when creating a new TASKS.md)")
    p_tasks.add_argument("--target", default=".", help="Directory containing TASKS.md (default: .)")
    p_tasks.set_defaults(func=cmd_tasks)

    # validate
    p_validate = sub.add_parser("validate", help="Check whether a project contains all required OS files")
    p_validate.add_argument("target", nargs="?", default=".", help="Project directory to validate (default: current directory)")
    p_validate.set_defaults(func=cmd_validate)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
