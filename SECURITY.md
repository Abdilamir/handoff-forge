# SECURITY.md

---

## Security Profile

**Risk level: Very low.** This tool reads and writes local markdown files only. No network access, no credentials, no external services.

---

## Rules in Force

- No runtime dependencies — zero supply chain attack surface
- Dev dependency (pytest) is well-established (>10 years, millions of weekly downloads)
- Tool never reads `.env` files and has no mechanism to do so
- No API keys, tokens, or secrets of any kind
- No network calls in any command

---

## File Safety Guarantees

- Default behavior never overwrites existing files
- All overwrites create automatic timestamped backups
- Backups are in the same directory as the original file — no data is sent anywhere

---

## Pre-Release Checklist

- [ ] `pip-audit` clean (run before any public release)
- [ ] No hardcoded values in source (`git grep -i "password\|secret\|api_key\|token"`)
- [ ] README does not instruct users to pipe scripts from the internet
- [ ] GitHub secret scanning enabled on repo

---

## Audits Run

| Date | What | Result |
|------|------|--------|
| 2026-05-22 | Initial implementation review | Clean — no deps, no network, no secrets |
