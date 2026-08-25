# CLAUDE.md — claude-specs marketplace

**Project:** Bool'\''s shared Claude Code plugin marketplace (the `core` foundations, `review-council`, `writing`, `consulting`, and vendored skill packs). See `README.md` for the two-layer model and the release ritual (bump the plugin'\''s `version` in `plugin.json` on every change).

## Document rendering & language

- **PDF deliverables** render from Markdown with the **`writing:latex-doc`** skill from the
  `claude-specs` marketplace (pandoc + XeLaTeX, overflow-safe thesis template). The skill —
  template, method notes, and build script — lives at
  `claude-specs/plugins/writing/skills/latex-doc/`.
- **Portuguese output** uses **European Portuguese (PT-PT)** via the **`writing:pt-pt`** skill
  (vendored from [mfrade/claude-skills](https://github.com/mfrade/claude-skills)); developer
  vocabulary stays in English (guard-rails, cooldown — never translated).
