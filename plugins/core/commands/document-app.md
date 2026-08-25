---
description: Reverse-engineer an AI-built codebase into the system documents reviewers and auditors need — a core set (architecture, flows, permissions, variables) plus conditional docs (emails, cron, SEO, automation) when they apply
argument-hint: "<repo path or area; defaults to the whole repository>"
---

# /document-app -- Make the System Reviewable

Produce the durable documentation an AI-built app is missing: an honest map of what the system is, who can do what, and where the risk lives. These docs are the foundation every later audit compares the code against.

## Invocation

```
/document-app
/document-app supabase/functions
/document-app the backend
```

## Workflow

### Step 1: Scope

Audit **$ARGUMENTS**. If empty, document the whole repository, prioritising backend code, auth, data access, background jobs, and anything that sends, schedules, or exposes data.

### Step 2: Reverse-Engineer the Docs

Apply the **shipping-artifacts** skill. Reading the code as the source of truth, produce the applicable documents in the host project's docs convention (e.g. a project's `02-architecture/` folder), falling back to `documentation/`.

**Core (always):**

- `architecture.md` — system overview, stack, auth flow, trust boundaries
- `flows.md` — the permission-relevant journeys: each protected step's authz check, the trust-boundary crossings, and the side effects each flow causes
- `permissions.md` — roles, scope derivation, resource × operation × role matrix, RLS vs. code-enforced checks
- `variables.md` — config & secrets mapped to risk and rotation

**Conditional (only if the capability exists — otherwise note its absence in one line):**

- `emails.md` — notification path, templates, retry/backoff, failure visibility
- `cron.md` — scheduled-work inventory, idempotency, internal-call auth
- `seo.md` — SPA preview approach, route coverage, metadata sanitisation
- `automation.md` — embedded agents/automations: trigger, tool surface, steering vs. hard guardrails, output contract, app-owned side effects, approval gates

Be brutally honest about the current state without being paranoid. Skip any conditional document that doesn't apply and say so. Add a "Related Documents" reference in `architecture.md` for each doc produced. (The test-coverage map, `tests.md`, is produced separately by `/derive-tests`.)

### Step 3: Report

Summarise what was created or updated, what was skipped and why, and any gaps where the code was too unclear to document confidently (those are the first things to fix).

### Step 4: Offer Next Steps

- "Want me to **derive a test-coverage map** (`/derive-tests`) so each documented rule has a verification plan?"
- "Want me to **run the built-in `/security-review`** now that the intended behaviour is documented?"
- "Should I **check for performance issues** — over-fetching, missing indexes, caching?"
- "Want a **general `/code-review` pass** before hand-off?"

## Notes

- These docs describe *this* system — keep generic theory and finished templates out.
- Write for two readers: a human reviewer and the next AI coding agent.
- Don't include an "updated date" line.
- The agent operating-context file (`CLAUDE.md` / `AGENTS.md`) is a separate hand-off artifact — **instructions derived from these docs, not documentation**. Once the docs exist, distil the rules the next agent must follow into it; don't duplicate the documentation there.
