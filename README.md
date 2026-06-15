# claude-specs

A central, maintained-in-one-place set of **Claude Code foundations** that other repos *pull*
from, while each repo keeps its own domain-specific agents/rules locally.

It's a **Claude Code plugin marketplace**. The shared layer ships as the `core` plugin; your
repo's own `.claude/` is the local layer and **overrides** anything in the plugin with the same
name. Update centrally here, then `git pull` lands in every consuming repo with one command.

## What `core` provides
- **Agents** (`explorer`, `planner`, `builder`, `reviewer`) — the orchestrator subagent set.
- **Command** (`new-project`) — generic sub-project scaffolder.
- **Hook** (`secret-scan`) — blocks Write/Edit/MultiEdit that contain real-looking credentials.
- **PRINCIPLES.md** — orchestrator model, Karpathy's 4 coding principles, universal operating rules.
- **settings.json** — a small permission allowlist to cut routine prompts.

## Install in a repo
```
/plugin marketplace add vmaia00/claude-specs
/plugin install core@claude-specs
```

## Pull updates (after this repo changes)
```
/plugin marketplace update claude-specs
```
This `git pull`s the local clone and re-syncs the plugin. Bumping `version` in
`plugins/core/.claude-plugin/plugin.json` is what signals consumers there's a new version.

## Local development / testing
Point Claude Code at this folder directly instead of GitHub:
```
/plugin marketplace add ./claude-specs
/plugin install core@claude-specs
/reload-plugins        # after editing plugin files
```

## Two-layer model
| Layer | Lives in | Example |
|---|---|---|
| **Shared** (pulled) | this repo's `core` plugin | generic `builder`, `secret-scan`, principles |
| **Local** (per repo) | each repo's `.claude/` | domain agents/hooks that override the shared ones |

See `BOOTSTRAP.md` to stand up a brand-new repo on these foundations.
