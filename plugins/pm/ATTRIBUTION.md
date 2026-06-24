# ATTRIBUTION

The contents of this `pm` plugin are **vendored** (copied) from a single MIT-licensed upstream
project. The upstream `LICENSE` is reproduced in this plugin's `LICENSE` file and retained
unchanged.

| Upstream | URL | Commit | Copyright |
|---|---|---|---|
| pm-skills | https://github.com/phuryn/pm-skills | `a0cd730` | © 2026 Paweł Huryn (Product Compass) |

**Vendored on:** 2026-06-24 — **License:** MIT.

## What was copied — 68 skills + 42 commands

Upstream `pm-skills` is itself a marketplace of **9 domain plugins**. Here they are **flattened
into one `pm` plugin**: every `SKILL.md` is copied unchanged except for an added `origin: pm-skills`
frontmatter field, and every command `.md` is copied verbatim. Skill and command names are globally
unique across the 9 domains, so no renaming was needed.

| Upstream domain plugin | Skills | Commands |
|---|---:|---:|
| pm-product-discovery | 13 | 5 |
| pm-product-strategy | 12 | 5 |
| pm-execution | 16 | 11 |
| pm-market-research | 7 | 3 |
| pm-data-analytics | 3 | 3 |
| pm-go-to-market | 6 | 3 |
| pm-marketing-growth | 5 | 2 |
| pm-toolkit | 4 | 5 |
| pm-ai-shipping | 2 | 5 |
| **Total** | **68** | **42** |

## What was changed

- Nine upstream plugins were merged into one (`plugins/pm/`); their per-plugin `plugin.json`,
  `README.md` and `.claude-plugin/marketplace.json` were **not** copied — this plugin carries its
  own `.claude-plugin/plugin.json` and is registered as a single `vendored` entry in the
  claude-specs marketplace.
- Each `SKILL.md` gained one line — `origin: pm-skills` — at the top of its frontmatter, matching
  the convention used by the other vendored plugins in this repo.
- No skill or command body was modified.

## Updating

To refresh: re-clone `phuryn/pm-skills`, re-flatten `*/skills/*` and `*/commands/*` into
`plugins/pm/skills/` and `plugins/pm/commands/`, re-inject the `origin:` field, bump the
`version` in `plugin.json`, and update the commit hash above.
