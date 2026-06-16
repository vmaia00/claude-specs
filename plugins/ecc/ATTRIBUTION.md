# ATTRIBUTION

The contents of this `ecc` plugin are **vendored** (copied verbatim) from the ECC project:

- **Upstream:** https://github.com/affaan-m/ECC
- **Version:** 2.0.0
- **Commit:** `5b173d2e6c11b976a0f13b2f59125e08956c1d47`
- **Vendored on:** 2026-06-15
- **License:** MIT — the upstream `LICENSE` is included alongside this file and is retained unchanged.

## What was copied
Only the component catalogs were vendored:

- `agents/`   — 64 subagents
- `skills/`   — 262 skills (each a folder with `SKILL.md`)
- `commands/` — 84 slash commands

## What was NOT copied
ECC's `hooks/`, `rules/`, `mcp-configs/`, `contexts/`, `scripts/`, `src/`, installers, and other
infrastructure were intentionally left out — this plugin is the agents/skills/commands catalog only.

## Local modifications
This copy is **not byte-for-byte verbatim**: the `model:` frontmatter field of the 56 agents that
upstream set to `sonnet` was changed to `inherit` (so they follow the session model). The 7 `opus`
and 1 `haiku` agents are unchanged. No other content was modified.

## Maintenance note
This is a **frozen snapshot**, not a live mirror. To refresh, re-clone the upstream repo at a newer
commit and re-copy the three folders, then bump `version` in `.claude-plugin/plugin.json`. Upstream
improvements do **not** flow in automatically.
