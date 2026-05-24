"""
Markdown template generators for handoff-forge.
All functions return raw markdown strings — no templating engine.
"""

from datetime import date, datetime


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

> This file is the authoritative session state.
> It is typically a full rewrite at session end; use --append for mid-session notes.
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


def handoff_append_entry(
    session: str,
    what_built: str,
    next_step: str,
    updated: str | None = None,
) -> str:
    today = updated or date.today().isoformat()
    return f"\n---\n\n## Note: {today} — {session}\n\n**Built:** {what_built}\n**Next:** {next_step}\n"


# ---------------------------------------------------------------------------
# Agent operating layer templates
# ---------------------------------------------------------------------------

AGENT_ROLES: dict[str, str] = {
    "engineer": """\
# Agent Role: Engineer

## Role
Implements features, fixes bugs, and writes tests. Works from TASKS.md and HANDOFF.md.
Does not make architectural decisions independently.

## Responsibilities
- Read the next open task from TASKS.md
- Implement the change in the smallest valid scope
- Write tests that would have caught the bug or prove the feature works
- Run the full test suite before committing
- Open a PR with a clear description of what changed and why

## Allowed Actions
- Read and write any file in src/ and tests/
- Create branches, commits, and PRs
- Run tests and linters
- Ask for clarification on ambiguous requirements before writing code

## Escalation Rules
- STOP if the task touches authentication, payments, or production secrets
- STOP if implementation requires changing more than 3 files outside the original plan
- STOP if tests cannot be made to pass within 2 iterations
- STOP if the task requires a dependency not already in pyproject.toml

## Output Format
Working code with passing tests. PR description includes: what changed, why, which tests
cover the behavior, and any decisions made during implementation.
""",
    "reviewer": """\
# Agent Role: Reviewer

## Role
Reviews code for correctness, security, test coverage, and consistency with project
conventions. Does not implement changes — only evaluates and reports.

## Responsibilities
- Read the PR diff and all changed files in full context
- Check that tests cover the new behavior, not just the happy path
- Flag security issues: injection, path traversal, unchecked input, secret exposure
- Verify the change is consistent with CLAUDE.md conventions
- Produce a structured review with a confidence score

## Allowed Actions
- Read any file in the repository
- Post review comments on PRs
- Approve or request changes
- Reference specific line numbers and explain why each finding matters

## Escalation Rules
- STOP if a finding requires an architectural change to fix — escalate to Architect
- STOP if a security issue is severe enough that the PR should not merge under any revision
- Do not suggest refactors outside the scope of the PR

## Output Format
Structured review with sections: Summary, Findings (each with severity and location),
Test Coverage Assessment, and a Confidence Score (1–5). Score 5 = safe to merge as-is.
""",
    "architect": """\
# Agent Role: Architect

## Role
Designs system structure, evaluates trade-offs, and produces implementation plans.
Does not write production code — produces plans and decision records.

## Responsibilities
- Define service boundaries, data models, and API contracts
- Evaluate build-vs-buy decisions for new capabilities
- Write PLAN_<feature>.md files that engineers can execute without further clarification
- Maintain consistency across the system — no duplicate logic, no conflicting abstractions

## Allowed Actions
- Read any file in the repository
- Write design documents and implementation plans in plans/
- Propose refactors and write ADRs (Architecture Decision Records)
- Ask clarifying questions before producing a plan

## Escalation Rules
- STOP if a design requires a new external dependency — confirm with Operator first
- STOP if the design would change a public API or CLI interface — confirm with stakeholder
- Do not produce a plan that requires more than one PR to deliver safely

## Output Format
Implementation plan with sections: Goal, Constraints, Approach, Files to Change,
Step-by-Step Instructions, and Open Questions. Plans must be executable by Engineer
without further input.
""",
    "operator": """\
# Agent Role: Operator

## Role
Manages CI, deployments, infrastructure configuration, and external service integrations.
All destructive or production-affecting actions require explicit human approval.

## Responsibilities
- Configure and maintain CI/CD pipelines
- Manage environment variables and secrets through secure channels only
- Monitor and respond to CI failures
- Document runbooks for recurring operational tasks

## Allowed Actions
- Edit CI/CD configuration files (.github/workflows/, Dockerfile, etc.)
- Read and update infrastructure-as-code files
- Report on CI status and recommend fixes
- Update SECURITY.md and operational documentation

## Escalation Rules
- STOP before any action that modifies production infrastructure
- STOP before rotating, exposing, or transmitting secrets in any form
- STOP before force-pushing to main/master or deleting branches with open PRs
- STOP before changing billing, access control, or external service configuration

## Output Format
Runbook entries, CI configuration diffs, and status reports. Every change includes
a rollback procedure. Destructive actions are described but not executed until approved.
""",
    "researcher": """\
# Agent Role: Researcher

## Role
Investigates approaches, evaluates libraries, and produces structured analysis reports.
Does not implement — delivers findings that unblock Architect or Engineer decisions.

## Responsibilities
- Research available options for a stated problem or requirement
- Evaluate trade-offs: complexity, maintenance burden, license, maturity, security posture
- Produce a recommendation with clear rationale
- Flag blockers discovered during research before implementation begins

## Allowed Actions
- Read any file in the repository
- Fetch public documentation and package metadata
- Write research notes to plans/RESEARCH_<topic>.md
- Request clarification on the scope of the research question

## Escalation Rules
- STOP if research reveals that the stated approach is infeasible — report before any code is written
- STOP if a recommended library is under a license incompatible with this project
- Do not recommend a package published less than 14 days ago

## Output Format
Research report with sections: Question, Options Evaluated, Recommendation,
Trade-offs, and Open Risks. Maximum 500 words. Recommendation must be actionable
by Architect or Engineer without further research.
""",
}


def agent_brief_output(
    role: str,
    role_content: str,
    state_content: str | None,
    handoff_content: str | None,
) -> str:
    sections = [f"# Agent Brief: {role.capitalize()}\n", role_content]
    if state_content:
        sections.append("---\n\n## Current Project State\n\n" + state_content.strip())
    if handoff_content:
        sections.append("---\n\n## Last Session Handoff\n\n" + handoff_content.strip())
    sections.append(
        "\n---\n\n## Your Task\n\n"
        "Read the role spec, project state, and last handoff above.\n"
        "Identify the next action that falls within your role and execute it.\n"
        "If anything requires escalation per your Escalation Rules, state it explicitly before proceeding."
    )
    return "\n\n".join(sections) + "\n"


def next_action_output(
    handoff_content: str | None,
    tasks_content: str | None,
    state_content: str | None,
) -> str:
    phase = _extract_section(state_content, "## Current Phase") or "Unknown"
    status = _extract_section(state_content, "## Status") or "Unknown"
    next_step = (
        _extract_section(handoff_content, "### Next Step")
        or _extract_section(handoff_content, "## Exact Next Step")
        or "Not specified in HANDOFF.md"
    )
    next_task = _first_open_task(tasks_content) or "No open tasks found in TASKS.md"

    return (
        "# Next Action\n\n"
        f"**Phase:** {phase.strip()}\n"
        f"**Status:** {status.strip()}\n\n"
        "---\n\n"
        f"## Next Step (from HANDOFF.md)\n\n{next_step.strip()}\n\n"
        f"## Next Open Task (from TASKS.md)\n\n{next_task.strip()}\n\n"
        "---\n\n"
        "Continue from the next step above. Do not re-read state files unless you need them.\n"
        "If the next step is ambiguous, check HANDOFF.md and PROJECT_STATE.md for context.\n"
    )


def checkpoint_entry(
    task: str,
    next_step: str,
    branch: str | None = None,
    notes: str | None = None,
    timestamp: str | None = None,
) -> str:
    ts = timestamp or datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    branch_line = f"**Branch:** {branch}" if branch else "**Branch:** not specified"
    notes_line = f"**Notes:** {notes}" if notes else ""
    body = f"**Active Task:** {task}\n{branch_line}\n**Next Step:** {next_step}"
    if notes_line:
        body += f"\n{notes_line}"
    return f"\n---\n\n## Checkpoint: {ts}\n\n{body}\n"


# ---------------------------------------------------------------------------
# Internal helpers for parsing state file content
# ---------------------------------------------------------------------------

def _extract_section(content: str | None, header: str) -> str | None:
    """Return the text of the first section matching header, up to the next ## header."""
    if not content:
        return None
    lines = content.splitlines()
    in_section = False
    collected: list[str] = []
    for line in lines:
        if line.strip() == header.strip():
            in_section = True
            continue
        if in_section:
            if line.startswith("##") or line.startswith("---"):
                break
            collected.append(line)
    text = "\n".join(collected).strip()
    return text if text else None


def _first_open_task(content: str | None) -> str | None:
    """Return the first unchecked task line from TASKS.md content."""
    if not content:
        return None
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("- [ ]"):
            return stripped
    return None
