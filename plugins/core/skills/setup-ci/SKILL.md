---
name: setup-ci
description: Detect a repo's stack and scaffold real GitHub Actions workflows for it — lint, tests, coverage, secret/SAST/CodeQL security scanning, tag-based release automation, and (only if a benchmark suite already exists) performance-regression tracking. Never overwrites existing workflows or fabricates dimensions the repo has no basis for (e.g. benchmarks). Use when setting up CI for a new repo, or auditing an existing repo's CI for gaps against this baseline.
---

# setup-ci

Scaffolds real, working GitHub Actions workflows — not a checklist. Every dimension below is
either wired to something the repo actually has, or explicitly skipped with a stated reason.
Never invent a dimension the repo has no basis for (don't add a benchmark workflow if there are no
benchmarks; don't add a release workflow if the repo isn't versioned/published).

## Step 1 — Detect the stack(s)

Look for marker files. A repo can have more than one (monorepo) — handle each independently and
scope that stack's workflow with `paths:` filters if it lives under a subdirectory.

| Marker | Stack | Package manager tell |
|---|---|---|
| `package.json` | Node/TypeScript | lockfile: `package-lock.json` (npm) / `pnpm-lock.yaml` (pnpm) / `yarn.lock` (yarn) |
| `pyproject.toml`, `requirements*.txt`, `setup.cfg` | Python | `poetry.lock` / `uv.lock` / plain pip |
| `go.mod` | Go | — |
| `Cargo.toml` | Rust | — |
| `pom.xml`, `build.gradle[.kts]` | Java/Kotlin | Maven vs Gradle |
| `*.csproj`, `*.sln` | .NET | — |
| `Gemfile` | Ruby | — |
| `composer.json` | PHP | — |

Read the manifest's `scripts`/`Makefile`/`justfile` for the *actual* lint/test/build commands —
don't assume a default. If a stack has no test script or test files, don't scaffold a test job
for it; report it as a gap instead of faking one.

## Step 2 — Inventory what already exists

`ls .github/workflows/`. For every existing workflow, note which dimension (below) it already
covers by grep'ing for tool names (`eslint`, `pytest`, `codeql`, `gitleaks`, ...). **Never
overwrite or replace an existing workflow silently** — replacing CI can break branch-protection
required-check names. If a dimension looks covered, skip it and say so. If the user wants an
existing workflow replaced, confirm first (a repo-wide CI change is a "confirm before" action per
`PRINCIPLES.md`).

## Step 3 — Decide which dimensions apply

| Dimension | Scaffold when | Skip when |
|---|---|---|
| **Lint** | a linter config or `lint` script exists, or the stack has an obvious default (`go vet`, `cargo clippy`) | no linter and no obvious default — don't invent lint rules |
| **Tests** | a test framework/script/test files exist | zero tests found — report the gap, don't scaffold an empty job |
| **Coverage** | tests exist *and* the runner supports a coverage flag (`--coverage`, `-cover`, `pytest --cov`) | no coverage-capable test runner |
| **Security — secrets** | always (language-agnostic: gitleaks + trufflehog) | never — cheap and universal |
| **Security — SAST/CodeQL** | the stack is CodeQL-supported (JS/TS, Python, Go, Java/Kotlin, Ruby, C/C++, C#, Swift) | unsupported language — note it, don't fake it |
| **Dependency review** | the repo has a lockfile (dependency graph exists) | no dependency manifest |
| **Multi-platform build matrix** | the repo ships/tests binaries per-OS (compiled language *and* either existing per-OS release assets, an install script branching on OS, or the user confirms it matters) | a single-target service/library — ask rather than default to a 3-OS matrix; it multiplies CI cost for no benefit on e.g. a backend API |
| **Release automation** | the repo is versioned for distribution (has a version field in its manifest) *and* has no existing release workflow | internal-only repo not meant to be tagged/published |
| **Performance regression** | a benchmark suite already exists (`bench/`, `*.bench.*`, `#[bench]`/criterion, `pytest-benchmark`, vitest `bench()`) | no benchmarks — this is the one most tempting to fake; don't scaffold it just because the baseline mentions it |

## Step 4 — Confirm scope before writing

Show the user: detected stack(s), the dimension table above filled in for this repo (scaffold /
skip + why for each row), and which existing workflows are being left untouched. This is a
repo-wide, moderately hard-to-reverse change (new required-check names, new repo secrets needed) —
get a go-ahead before writing, per `PRINCIPLES.md` §3.

## Step 5 — Generate workflows

Copy the matching file(s) from `templates/`, substitute the bracketed placeholders
(`<NODE_VERSION>`, `<TEST_CMD>`, `<PATHS_FILTER>`, ...) with values from Step 1, and adapt job
names for a monorepo subdirectory. Match this plugin's own house style (see this repo's
`.github/workflows/*.yml` for a live reference) even though you're writing into a *different*
repo:

- **Least-privilege `permissions:`** at the workflow level; elevate per-job only where needed
  (e.g. `security-events: write` for CodeQL/SARIF upload).
- **`concurrency:` with `cancel-in-progress: true`** on PR/push-triggered workflows, keyed on
  `${{ github.workflow }}-${{ github.ref }}`. Omit on the release workflow — never cancel a
  release mid-flight.
- **Pin actions to a major-version tag** (e.g. `actions/checkout@v7`), not `@main`/unpinned.
- **Comment the *why*, not the *what*** — e.g. why a job is advisory (`|| true`) or scheduled
  instead of gating.
- Gating dimensions (lint, test, security) trigger on `pull_request` + `push: branches: [main]`.
  Advisory/slow dimensions (link rot, full dependency audit, perf trend) trigger on `schedule` +
  `workflow_dispatch`, not every PR.

## Step 6 — Write, verify, report

1. Write the files. **Never `git add`/commit/push** — leave the scaffold for the user to review,
   same as `core:new-project`/`core:init-repo`.
2. If `actionlint` or a YAML linter is available, run it against the new files.
3. Report: the file tree created, the dimension table from Step 3 (so skips are visible, not
   silent), and the manual follow-ups the user still needs to do — add repo secrets
   (`CODECOV_TOKEN`, `CODSPEED_TOKEN`, etc.), enable "Code scanning" / Dependabot in repo settings,
   and add the new job names to branch-protection required checks.

## Templates

| File | Covers |
|---|---|
| `templates/security.yml` | gitleaks + trufflehog (always) + CodeQL (language-conditional) + dependency review |
| `templates/release.yml` | tag-triggered release with native GH release notes + a guard against re-releasing an existing tag |
| `templates/ci-node.yml` | Node/TS lint + test + coverage |
| `templates/ci-python.yml` | Python lint + test + coverage |
| `templates/ci-go.yml` | Go vet/lint + test + coverage, optional OS/arch build matrix |
| `templates/ci-rust.yml` | Rust fmt/clippy + test + coverage, optional OS/arch build matrix |
| `templates/perf-codspeed.yml` | Benchmark regression tracking — only wire in if Step 3 found real benchmarks |

For a stack without a template (Java, .NET, Ruby, PHP, ...), apply the same shape by hand: official
`setup-<lang>` action, the project's own lint/test commands, least-privilege permissions,
concurrency cancel-in-progress, pinned action versions.
