# Third-Party Notices

Most of this plugin (the orchestrating command, the Code Review Master, the finding verifier,
the Fixer, the architecture / concurrency-contract / contrarian lanes, and the skill) is original
first-party work.

Seven of the panelist agents are **adapted** (not verbatim) from the ECC project's reviewer
subagents — trimmed to a single review angle, made stack-neutral and read-only, and rewritten to
emit this plugin's unified JSON finding schema.

- **Upstream:** https://github.com/affaan-m/ECC
- **Version:** 2.0.0 (commit `5b173d2e6c11b976a0f13b2f59125e08956c1d47`)
- **License:** MIT — Copyright (c) 2026 Affaan Mustafa. The full license text is retained
  unchanged at [`../ecc/LICENSE`](../ecc/LICENSE) (the ECC plugin vendored in this same repo).

## Adapted files → ECC source

| This plugin | Adapted from (in `plugins/ecc/agents/`) |
|---|---|
| `agents/correctness-reviewer.md` | `code-reviewer.md` (scoped to logic/correctness) |
| `agents/appsec-reviewer.md` | `security-reviewer.md` |
| `agents/error-handling-reviewer.md` | `silent-failure-hunter.md` |
| `agents/test-reviewer.md` | `pr-test-analyzer.md` |
| `agents/type-design-reviewer.md` | `type-design-analyzer.md` |
| `agents/readability-reviewer.md` | `comment-analyzer.md` + `code-simplifier.md` (merged) |
| `agents/performance-reviewer.md` | `performance-optimizer.md` (made read-only) |

Adaptations: removed web/Node/React-specific tooling and bias, narrowed each agent to one
perspective, set `model: inherit`, restricted tools to read-only, and replaced the prose verdict
with the structured finding schema defined in `skills/deep-review/REFERENCE.md`.
