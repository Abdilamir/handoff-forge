# Grep Loop Prompt — Review Loop Protocol

Use this prompt after Greptile posts its review on a PR. Paste Greptile's feedback into the session after the prompt.

---

## Session Start Prompt

```
Read HANDOFF.md. Do not write any code yet.

Tell me:
1. What was the last thing completed?
2. What is the exact next step?
3. Are there any known risks or blockers?
```

---

## Review Loop Prompt

```
Here is Greptile's review of PR [number] — [feature name]:

[PASTE GREPTILE FEEDBACK HERE]

For each issue raised:
1. State whether you agree or disagree and why
2. If you agree: fix it, show the diff, confirm tests still pass
3. If you disagree: state the defensible reason (see HANDOFF.md Decisions Made section)

Do not fix issues we disagree with. Do not introduce new behavior.
Target: resolve until Greptile rates this 5/5.
```

---

## After Each Fix Round

```
Tests still passing? Run: python -m pytest --tb=short -q
Commit the fix: git commit -m "fix: [description of what was addressed]"
Then re-request Greptile review.
```

---

## Merge Checklist (only after 5/5)

```
Before merging:
1. All tests passing on feature branch
2. Greptile score 5/5
3. Human diff review complete (git diff master...feature/validate-command)
4. CHANGELOG.md updated with final merge entry
5. No uncommitted changes

Merge: git checkout master && git merge --no-ff feature/validate-command
Tag: git tag restore/post-validate-merge
```
