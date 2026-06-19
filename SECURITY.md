# Security & quality checks

This repo is a Claude Code plugin marketplace. The code that actually executes on a user's
machine is the hook layer (`.mjs`, `.py`, `.sh`) plus the manifests that drive installation, so
the checks below focus there.

## Automated checks

Layered so that nothing depends on a single local tool:

| Layer | Tool | Where | Gating? |
| --- | --- | --- | --- |
| Secrets (write-time) | `core` plugin `secret-scan.mjs` | Claude Code `PreToolUse` on Write/Edit | blocks the write |
| Secrets (push-time) | gitleaks | local `PreToolUse` hook on `git push` (`~/.claude/settings.json`) | blocks the push |
| Secrets (server-side) | gitleaks-action | `security` workflow, every PR + push to `main` | yes |
| SAST | semgrep | `security` workflow | advisory (see below) |
| Shell lint | shellcheck | `security` workflow | errors only |
| Workflow lint | actionlint | `quality` workflow | yes |
| Manifests + frontmatter | `scripts/validate-plugins.mjs` | `quality` workflow | yes |
| Markdown style | markdownlint-cli2 | `quality` workflow, changed files only | yes |
| Link rot | lychee | `quality` workflow, weekly + on demand | reports |

semgrep is **advisory** at first so legacy findings don't block the PR that introduces it.
Findings still appear under **Security → Code scanning**. To promote it to a gate, edit
`.github/workflows/security.yml`: remove `|| true` and add `--error` to the `semgrep scan` step
once the baseline is triaged.

## Manual one-time setup (repo admin)

GitHub provides server-side secret scanning that cannot be bypassed by skipping a local hook.
It is **free for public repositories** and is not configured from a file — enable it in the UI:

1. **Settings → Code security and analysis**
2. Enable **Secret scanning**
3. Enable **Push protection** (rejects pushes containing detected secrets)
4. Optionally enable **Dependabot** alerts/updates if dependencies are added later

## Local developer setup

```sh
pipx install pre-commit
pre-commit install            # run the same checks on every commit
pre-commit run --all-files    # check the whole tree once
```

## Reporting a vulnerability

Email <vasco.a.maia@outlook.com> with details and reproduction steps. Please do not open a
public issue for undisclosed vulnerabilities.
