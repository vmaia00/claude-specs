# Plan: Curate the best non-duplicate skills into `core` + companion installs

> **Status:** proposed roadmap — not yet implemented. Captures the merge strategy for the
> "best skills/agents/commands across N repos" request so it can be executed later.

## Context

A 20-repo ranking was reviewed with the ask to "merge all the best skills/agents/commands."
Triage reality: most of the 20 are **not** mergeable skill sources — apps (NextChat, LobeHub,
open-design), agent frameworks (AutoGPT, hermes-agent), the Claude Code tool itself, reference
dumps (system-prompts, prompts.chat), or unrelated (RuView). Already incorporated: ECC (vendored
`ecc` plugin), karpathy (PRINCIPLES.md), gstack (ETHOS.md). And **ECC already provides 262 skills**,
so the real value is the handful of *non-overlapping* gems.

**Decisions (confirmed):**
- **Scope → curated gems** from the 3 genuine skill repos, deduped against ECC.
- **Packaging → promote into `core`** (lightweight, on-invoke skills; low always-on cost).
- **Memory + refs → install claude-mem as its own plugin; mine system-prompts + awesome-lists into notes** (not vendored).

**Sources & licenses (all MIT):** [mattpocock/skills](https://github.com/mattpocock/skills) (pure
markdown), [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) (JS/Python + hooks),
[safishamsi/graphify](https://github.com/safishamsi/graphify) (Tree-sitter/NetworkX/Python),
[thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) (npm/plugin).

**Judgment applied (ethos: complete-within-scope, don't bloat):** graphify and caveman's full
machinery carry real dependencies → they do **not** go inside lean `core`. Only self-contained
**markdown** skills are promoted; heavy tools become documented companion installs.

---

## Part A — Promote curated markdown skills into `core`

Vendor these self-contained, pure-markdown skills from `mattpocock/skills` (MIT) into
`plugins/core/skills/<name>/SKILL.md`. They fill gaps ECC doesn't cover well and pair with the
session directive's "prefer existing skills" rule:

| Skill | Source path (mattpocock/skills) | Why |
|---|---|---|
| `diagnose` | `skills/engineering/diagnose/` | disciplined reproduce→minimize→hypothesize→fix→test debugging loop |
| `write-a-skill` | `skills/productivity/write-a-skill/` | meta-skill — authoring new skills (useful for maintaining `claude-specs` itself) |
| `handoff` | `skills/productivity/handoff/` | compact a session for agent-to-agent handoff (complements orchestration) |
| `zoom-out` | `skills/engineering/zoom-out/` | pull broader system context for unfamiliar code |
| `caveman` | `skills/productivity/caveman/` | invokable ~65% output-token reduction (markdown only; credits JuliusBrussee) |
| `teach` *(optional)* | `skills/productivity/teach/` | multi-session skill instruction — include only if wanted |

**Skip** (ECC-overlapping or needs mattpocock's scaffolding/ecosystem): `tdd`, `triage`,
`grill-with-docs`, `to-issues`, `to-prd`, `setup-matt-pocock-skills`, `migrate-to-shoehorn`,
`scaffold-exercises`, `improve-codebase-architecture`. **Caveman's** full repo (auto-activation hook
+ `/caveman-commit|review|stats` sub-skills + JS/Python) is **not** vendored — only the markdown skill.

**Attribution (MIT requires it):** add `plugins/core/THIRD-PARTY-NOTICES.md` listing each vendored
skill, its upstream repo + commit, and the retained MIT copyright/license text; note caveman's
upstream is JuliusBrussee. Each vendored `SKILL.md` keeps an `origin:` line in frontmatter.

## Part B — Companion installs (documented, NOT vendored)

These are valuable but dependency-heavy / better consumed as their own plugins. Document in
`README.md` (new "Companion tools" section) + `BOOTSTRAP.md`:
- **claude-mem** (memory across sessions) — `npx claude-mem install` or its plugin marketplace.
- **graphify** (code→knowledge-graph) — its own skill install; note Python/Tree-sitter deps and that
  it sends only semantic content, not raw source.

## Part C — Mine reference repos into notes (not vendored)

Create `research/insights.md` capturing patterns worth adopting later, harvested from
[hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) /
awesome-claude-skills and [system-prompts-and-models](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)
(e.g. notable skills to evaluate, prompt-structuring patterns). Short, curated, links — a backlog,
not a vendor dump.

## Part D — Release
Bump `plugins/core/.claude-plugin/plugin.json` `0.4.0 → 0.5.0`; update README "What core provides"
(skills + companion tools); commit, push, tag `core--v0.5.0` via `claude plugin tag`.

## Critical files
- New: `plugins/core/skills/{diagnose,write-a-skill,handoff,zoom-out,caveman}/SKILL.md` (+ optional `teach`),
  `plugins/core/THIRD-PARTY-NOTICES.md`, `research/insights.md`.
- Edit: `plugins/core/.claude-plugin/plugin.json` (version), `README.md` (skills + companion tools),
  `BOOTSTRAP.md` (companion installs).
- Reuse as model: existing `plugins/ecc/ATTRIBUTION.md` pattern for the notices; the session
  directive already nudges "prefer existing skills" so the new skills get discovered.

## Verification
1. Each vendored `SKILL.md` has valid frontmatter (`name`, `description`); fetched verbatim from
   upstream `main` (record the commit SHA in the notices).
2. `claude plugin validate ./plugins/core --strict` passes.
3. Local install from path → `claude plugin details core@claude-specs` lists the new skills under
   "Skills"; clean up after.
4. Token-cost check: confirm always-on bump is small (skills are on-invoke); note the delta.
5. Links in README/BOOTSTRAP/insights resolve.

## Out of scope (deliberately)
The ~12 non-skill repos (apps, frameworks, the CC tool, reference dumps, RuView); ECC-overlapping
skills; graphify/caveman heavy machinery; bulk vendoring. These can be revisited per-item later —
adding a skill to `core` is cheap and propagates via `/plugin marketplace update`.
