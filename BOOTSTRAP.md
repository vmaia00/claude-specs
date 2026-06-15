# Bootstrap a new repo on these foundations

Two ways to adopt the shared layer. **Prefer the plugin** — it pulls updates with one command
instead of re-copying files.

## Option A — Plugin (recommended)
1. In the new repo:
   ```
   /plugin marketplace add vmaia00/claude-specs
   /plugin install core@claude-specs
   ```
2. You now have the `explorer`/`planner`/`builder`/`reviewer` agents, the `new-project` command,
   the `secret-scan` hook, and the permission allowlist — all from the plugin.
3. Add the **local layer**: a repo `CLAUDE.md` describing the project (purpose, where domain
   knowledge lives, build/test command), and any domain-specific agents/hooks under `.claude/`.
   Same-named local items override the plugin's.
4. Pull future improvements with `/plugin marketplace update claude-specs`.

## Option B — Copy (no plugin runtime)
For CI, other harnesses, or air-gapped use, copy `plugins/core/` contents into the repo's
`.claude/` (agents → `.claude/agents/`, etc.) and the `PRINCIPLES.md` into the repo. No live link;
re-copy to update.

## The core idea
The **main thread orchestrates**; it delegates research and development to subagents so its own
context stays lean. Subagents return conclusions and diffs with `file:line` citations, not raw
file dumps. This keeps long sessions cheap and focused. See `plugins/core/PRINCIPLES.md`.
