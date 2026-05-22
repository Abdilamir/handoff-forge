"""
Markdown template generators for handoff-forge.
All functions return raw markdown strings — no templating engine.
"""

from datetime import date


def handoff_template(
    session: str,
    what_built: str,
    not_finished: str,
    decisions: str,
    next_step: str,
    risks: str,
    updated: str | None = None,
) -> str:
    today = updated or date.today().isoformat()
    return f"""\
# HANDOFF.md

> This file is always a full rewrite — not an append.
> It represents the current state of the project right now.
> A fresh agent reads this first, before doing anything else.

---

## Session: {today} — {session}

### What Was Built
{what_built}

### What Is Not Finished
{not_finished}

### Decisions Made
{decisions}

### Next Step
{next_step}

### Known Risks
{risks}

---

*Last updated: {today} | Session: {session}*
"""


def project_state_template(
    phase: str,
    status: str,
    stack: str,
    done_items: list[str],
    in_progress: str,
    next_steps: str,
    updated: str | None = None,
) -> str:
    today = updated or date.today().isoformat()
    done_lines = "\n".join(f"- [x] {item}" for item in done_items) if done_items else "- None yet"
    return f"""\
# PROJECT_STATE.md

> This file is updated at the end of every session.
> Keep it short — depth lives in HANDOFF.md and DECISIONS.md.

---

## Current Phase
{phase}

## Status
{status}

## Stack
{stack}

## What Is Done
{done_lines}

## What Is In Progress
{in_progress}

## What Is Next
{next_steps}

## Known Blockers
None

## Last Updated
{today}
"""


def tasks_template(
    phase: str,
    tasks: list[str],
    updated: str | None = None,
) -> str:
    today = updated or date.today().isoformat()
    task_lines = "\n".join(f"- [ ] {task}" for task in tasks) if tasks else "- [ ] [Add your first task here]"
    return f"""\
# TASKS.md

> Active task list only. Completed tasks move to CHANGELOG.md.
> Each task must be PR-sized: one feature, one branch, ~200-400 lines max.
> Format: [ ] Task name — exit condition (done = ...)

---

## {phase}

{task_lines}

---

## TASK FORMAT (for new tasks)

```
- [ ] [Task name] — [exit condition: done = ...]
      Files: [which files will change]
      Depends on: [task name, if any]
      Risk: [low/medium/high] — [reason if medium or high]
```

*Last updated: {today}*
"""


def task_entry(description: str) -> str:
    """Format a single task line for appending to TASKS.md."""
    return f"- [ ] {description}"
