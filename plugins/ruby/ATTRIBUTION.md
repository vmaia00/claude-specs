# ATTRIBUTION

The contents of this `ruby` plugin are **vendored** (copied, some renamed) from three
MIT-licensed upstream projects. Each upstream `LICENSE` is reproduced in this plugin's `LICENSE`
file and retained unchanged.

| Upstream | URL | Commit | Copyright |
|---|---|---|---|
| superpowers-ruby | https://github.com/lucianghinda/superpowers-ruby | `712d734` | © 2025 Jesse Vincent (maintained by Lucian Ghinda) |
| rails-agent-skills | https://github.com/igmarin/rails-agent-skills | `51f5974` | © 2026 Ismael G Marin C |
| ruby-core-skills | https://github.com/igmarin/ruby-core-skills | `e3d43bf` | © 2026 Ismael Marín |

**Vendored on:** 2026-06-17 — **License:** MIT.

## What was copied — 28 curated skills

A focused **Ruby / Rails / Hotwire / TDD** set was selected (not the full catalogues). Each skill
carries an `origin:` frontmatter field naming its source.

**From superpowers-ruby (16):** `ruby`, `sandi-metz-rules`, `ruby-upgrade`, `ruby-commit-message`,
`rails-guides`, `rails-upgrade`, `37signals-style`, `test-driven-development`, `brakeman`,
`verification-before-completion`, and the six Hotwire skills `hwc-stimulus-fundamentals`,
`hwc-forms-validation`, `hwc-realtime-streaming`, `hwc-navigation-content`, `hwc-media-content`,
`hwc-ux-feedback`.

**From rails-agent-skills (9)** *(renamed for clarity / global uniqueness):*

| Vendored name | Upstream name |
|---|---|
| `rails-background-job` | `implement-background-job` |
| `rails-authorization` | `implement-authorization` |
| `rails-performance` | `optimize-performance` |
| `rails-review-migration` | `review-migration` |
| `rails-seed-database` | `seed-database` |
| `rails-version-api` | `version-api` |
| `rails-code-review` | `code-review` |
| `plan-tests` | `plan-tests` |
| `write-tests` | `write-tests` |

**From ruby-core-skills (3)** *(renamed):*

| Vendored name | Upstream name |
|---|---|
| `ruby-service-object` | `create-service-object` |
| `ruby-api-client` | `integrate-api-client` |
| `ruby-yard-docs` | `write-yard-docs` |

### Agent (1)

`agents/code-reviewer.md` — from superpowers-ruby (`712d734`), a senior code-reviewer agent
(plan-alignment + quality/security review). `model:` is `inherit`; an `origin:` field was added.

## Local modifications

- **Flattened** the upstream category nesting (`skills/<category>/<name>/`) into the flat
  `skills/<name>/` layout Claude Code requires; `references/`/`scripts/` sub-folders copied verbatim.
- **Renamed** the skills listed above (folder + `name:` frontmatter) for clarity and to keep names
  globally unique; added an `origin:` field to every skill's frontmatter.
- No skill *body* content was otherwise altered.

## What was NOT copied (and why)

To keep the plugin focused and avoid duplicating the `core` plugin, the following were left out:
- **Overlap with `core`:** superpowers' `handoff`/`handoff-list`/`handoff-resume` (→ core `handoff`),
  `systematic-debugging` (→ core `diagnose`), `writing-skills` (→ core `write-a-skill`).
- **Generic workflow/meta** (superpowers): `brainstorming`, `writing-plans`, `executing-plans`,
  `subagent-driven-development`, `dispatching-parallel-agents`, `consulting-an-oracle`, `compound`,
  `compound-refresh`, `finishing-a-development-branch`, `using-git-worktrees`,
  `using-sqlite-worktrees`, `using-superpowers`, `requesting-code-review`, `receiving-code-review`.
- **Niche/heavy** (rails-agent-skills): the 9-skill `engines/` suite, `api/` (`implement-graphql`,
  `generate-api-collection`), `code-quality/` (`apply-code-conventions`, `apply-stack-conventions`,
  `refactor-code`, `review-architecture`, `security-check`), `context/` (`load-context`,
  `setup-environment`), `testing/test-service`, and the 9 `personas/`.
- **Overlap/niche** (ruby-core-skills): `ddd/*`, `process/*`, `planning/generate-tdd-tasks`,
  `orchestration/skill-router`, `code-quality/respond-to-review`,
  `patterns/implement-calculator-pattern`, `testing/triage-bug`.

## Commands — intentionally NOT vendored

superpowers-ruby's `brainstorm`, `write-plan` and `execute-plan` commands are **deprecated stubs**
upstream — each is a one-line notice telling the user to use the `brainstorming` / `writing-plans` /
`executing-plans` skills instead. Those skills are not part of this curated set, so the commands
would dangle. If the brainstorm → plan → execute workflow is wanted, vendor those three **skills**
(and their helpers) rather than the deprecated commands.

## Possible follow-up (not yet vendored)

rails-agent-skills' 9 `personas/` and superpowers-ruby's workflow skills
(`brainstorming`, `writing-plans`, `executing-plans`) could be added if wanted.

## Maintenance note

This is a **frozen snapshot**, not a live mirror. To refresh, re-clone the upstreams at a newer
commit, re-copy the selected skills, and bump `version` in `.claude-plugin/plugin.json`. Upstream
improvements do **not** flow in automatically.
