# Insights backlog — patterns worth evaluating (not vendored)

A curated backlog mined from reference repos, to consider adopting later. Ideas/links only — no
code is vendored from these. Keep this short; promote an item by opening a focused change.

## Sources mined
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) — index of
  skills, hooks, slash-commands, agent orchestrators, and plugins for Claude Code.
- awesome-claude-skills (several forks, e.g. ComposioHQ / travisvn) — curated skill directories.
- [x1xhlol/system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)
  — leaked system prompts of many AI coding tools (Cursor, Devin, Windsurf, v0, …).

## Candidate patterns to evaluate
- **Persistent memory** — `claude-mem` (see README "Companion tools"). Evaluate whether to standardize
  a memory plugin across repos vs the per-project `MEMORY.md` convention.
- **Code knowledge-graph** — `graphify` for large-codebase navigation; weigh its Python/Tree-sitter
  deps before recommending broadly.
- **Prompt-structuring patterns** (from system-prompts dump): explicit role + capabilities + hard
  constraints + tool-use rules sections; tight "refuse/redirect" wording. Could sharpen agent
  definitions in `core`.
- **Token economy** — `caveman` is now vendored; consider a lighter always-on "be terse" nudge vs an
  opt-in skill.
- **Skill hygiene** (from ECC `skill-stocktake` / mattpocock `write-a-skill`): periodically audit
  `core`/`ecc` skills for overlap, freshness, and bloat.

## From the 2026-08-25 cleanup (reviewer backlog)
- **review-council**: consider merging near-neighbour R1 lanes (readability+type-design,
  performance+concurrency-contract); make `finding-verifier` opt-in; document when to prefer
  built-in `/code-review ultra` vs `deep-review` so both never run on the same diff; once the
  Rails build starts, feed `ruby:rails-code-review`'s Always-Critical flags into the panel as
  reference input rather than a competing review path.
- **spec-agentic**: kept registered-but-uninstalled for the tutor spec phase; delete if still
  uninstalled once tutor spec-writing is underway.
- **ubbu prd-reviewer salvage**: port strategy-red-team's steelman-attack + cheapest-test +
  kill-criterion-per-assumption trick (from the retired pm plugin) into ubbu's local
  prd-reviewer checklist.
- **pt-pt licensing**: upstream mfrade/claude-skills has no LICENSE file (README claims MIT) —
  ask mfrade to add one before any redistribution beyond internal use.

## Explicitly out of scope (from the 20-repo survey)
Apps (NextChat, LobeHub, open-design), agent frameworks (AutoGPT, hermes-agent), the Claude Code tool
itself, config switchers (cc-switch), and unrelated projects (RuView). Not skill/agent/command sources.
