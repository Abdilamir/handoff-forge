# SECURITY.md

## Supported Versions

handoff-forge is a local CLI tool with no network access, no accounts, and no
server-side components. There is no production deployment to patch.

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |

## Reporting a Vulnerability

If you discover a security issue (e.g. path traversal in file writes, unsafe
template rendering, dependency vulnerability):

1. Do **not** open a public GitHub issue.
2. Email the maintainer directly or open a GitHub Security Advisory:
   https://github.com/Abdilamir/handoff-forge/security/advisories/new
3. Include: affected version, reproduction steps, and proposed fix if known.

You will receive a response within 72 hours. If the issue is confirmed, a
patched release will be published and the advisory will be made public after
a reasonable disclosure window.

## Security Properties of This Tool

- **No network access:** all commands are fully local
- **No credentials or secrets handled:** no API keys, tokens, or auth flows
- **Non-destructive writes:** existing files are backed up before overwrite
- **No subprocess calls or shell execution:** pure Python stdlib only
- **No eval or exec:** templates are plain f-strings
