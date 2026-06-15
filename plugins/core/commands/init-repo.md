---
description: Scaffold a minimal starter CLAUDE.md (+ AGENTS.md pointer) for the repo-specific layer
argument-hint: [project-name]
allowed-tools: Bash, Read, Write, Glob
---

Scaffold the **local layer** for this repo: a minimal starter `CLAUDE.md` (and an `AGENTS.md`
pointer) so the repo has a place for its own purpose, build/test command, and domain rules.

The shared `core` foundations (orchestrator agents, principles, secret-scan, and the always-on
session directive) already apply via the plugin — this command only seeds the **repo-specific**
file that those don't provide. This is different from Claude Code's built-in `/init` (which writes a
CLAUDE.md by analysing an existing codebase) and from `core:new-project` (which scaffolds a
sub-project under `projects/`).

Steps:

1. Decide the project name: use `$1` if given, else the current repo's folder name. Call it `NAME`.
2. **If `./CLAUDE.md` already exists, stop and report it — never overwrite.** (Offer to show it.)
3. Write `./CLAUDE.md` with exactly this content, substituting `NAME` for `<PROJECT_NAME>` and
   leaving the other `<...>` placeholders for the user to fill:

   ```markdown
   # CLAUDE.md — <PROJECT_NAME>

   **Project:** <one-line description of what this repo is>
   **Domain knowledge lives in:** <e.g. knowledge/ or docs/ — or "n/a">
   **Build / test:** <e.g. npm test, make check — or "n/a">

   This repo uses the shared **`core`** foundations from the `claude-specs` plugin marketplace
   (orchestrator agents, working principles, a secret-scan hook, and an always-on session directive).
   Those apply automatically. The rules below are this repo's **local layer** and take precedence
   where they differ; same-named local agents/commands/hooks override the plugin's.

   ## How we work here
   - **Orchestrate.** Delegate research and edits to subagents; keep the main thread lean; expect
     concise `file:line` conclusions, not raw file dumps. (See `core` PRINCIPLES.md for the full set.)
   - <add this repo's conventions, stack sharp edges, and domain rules here>

   ## Read order before working
   1. This file. 2. <domain knowledge folder>. 3. Any area/module doc you're touching.
   ```

4. If `./AGENTS.md` does **not** exist, write it with this content (a pointer, to avoid drift):

   ```markdown
   # AGENTS.md

   Agent instructions for this repository live in **[CLAUDE.md](./CLAUDE.md)** — a single source of
   truth. Any `AGENTS.md`-aware or Claude Code-compatible tool should read it.
   ```

5. If `./.gitignore` does **not** exist, offer to create one with a secrets/build/OS ignore block
   (`.env`, `.env.*`, `node_modules/`, `dist/`, OS cruft).
6. Show the created files and remind the user to fill the `<...>` placeholders, and — if `core`
   isn't installed on this machine yet — to run
   `/plugin marketplace add vmaia00/claude-specs` then `/plugin install core@claude-specs`.

Do **not** commit or push — leave the scaffold for the user to review.
