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

## Explicitly out of scope (from the 20-repo survey)
Apps (NextChat, LobeHub, open-design), agent frameworks (AutoGPT, hermes-agent), the Claude Code tool
itself, config switchers (cc-switch), and unrelated projects (RuView). Not skill/agent/command sources.
