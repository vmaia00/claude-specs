---
name: contract-set
description: Build an OpenAPI-first contract set as the spine of a spec set — a shared conventions library, one internal contract per downstream capability, and front-facing surface contracts per functional area, each versioned, owned and verifier-gated. Use for API contract design, "define the interface before the implementation", OpenAPI spec sets, BFF surface design, and contract-first development.
---

# Contract Set

In a spec set that agents execute, the contracts are the spine. Prose describes intent; contracts
are the only part a builder can be held to. Everything else in the set exists to justify a field.

## Three layers

```
contract-set/
  common/      shared conventions library — no routes, sole owner of reused components
  capability/  internal contracts, one per downstream capability the product consumes
  surface/     the product's own front-facing contracts, one per functional area
```

**`common/`** owns, exactly once: the error model (RFC 7807 with a registered code list), the
pagination envelope, common parameters and headers, security schemes, and domain enums. Every other
file reaches it by relative `$ref` and **never redefines** a component. One owner per shared shape
is the whole point; the day two files define `Problem`, they diverge.

**`capability/`** is one contract per downstream capability — the interface you consume from a
system that is not yours (or not yours yet). Named by capability, not by system: `docs.intake`,
`archive.read`, `erp.write`. The name outlives the vendor behind it.

**`surface/`** is the tier your own front end calls — the BFF. One file per functional area, not
one per screen. Surface routes are largely **projections** of capability contracts: same shape,
narrowed to what a session-scoped caller may see. Keeping them separate lets the front end evolve
its ergonomics without renegotiating a downstream interface.

Why the split, in one line: the shared library prevents divergence, the capability layer is what
you must agree with someone else, the surface layer is what you may change alone.

## Version and status per file

Every file declares its own version and its own status.

- **SemVer per contract**, independently. Minor releases are **additive only** — nothing removed,
  renamed or retyped. A major needs an N-1 window where the previous version stays served.
- **`1.0` means "ready to specify"**. It never means "agreed with the counterparty". Say this in
  the set's README, in those words. It is the single most common misreading, and it converts your
  own design into a commitment nobody made.
- **Status vocabulary**, per file and per route:

| Status | Meaning |
|---|---|
| **field-level** | Routes and payloads complete to the field. Buildable. |
| **stub gated** | Shape registered, content absent, blocked on a named external gate. |
| **mixed** | Both, route by route. |

Gating rules that stop invention dead:

- A gated **surface** returns `501` with a stable error code (`gate-closed`). It never pretends to
  be available.
- A gated **field** is typed but travels null or absent. Never with a fabricated value.
- The **shape does not change when the gate closes**. That is what makes it safe to build against
  a gated route today.
- Whatever has no source is declared open **inside the contract itself**, tagged, never invented.

## Contracts are the boundary between the WHAT and the HOW

State this explicitly in the set, because it is the property that buys the schedule:

- The **product spec defines and consumes** contracts. It says what the product does, which
  capability it needs, and what shape it needs it in.
- The **engine behind a contract implements the pipeline**. How it classifies, matches, retries or
  writes is entirely its own business, invisible through the interface.

The two halves are therefore buildable **independently and in parallel**, by different teams, on
different timelines. Neither can silently break the other, because the only coupling is a versioned
file with an additive-only minor policy. Lose the discipline and you lose the parallelism — that is
the actual cost of a contract edited casually.

A corollary worth enforcing: when the prose spec and the published contract set disagree, **the
contract set wins**. Write that rule down; otherwise every disagreement becomes a negotiation.

## Verify, then publish

Never call a contract closed before the verifiers pass. The loop:

1. **Structure check** — prove that an editorial change touched only prose: skeleton unchanged,
   citation multiset unchanged, file still parses, `$ref`s still resolve.
2. **Anchor check** — every provenance citation resolves by name against its source document.
3. **Publish** — regenerate a clean reference copy into a separate directory, stripping the audit
   trail and keeping the design content. The source keeps everything; the render cleans.

All three are described in the `anchor-graph` skill and its verifier reference. Wire them as a CI
gate over the contract folder.

Consumer-driven contract tests belong in the same gate once code exists: each consumer publishes
the expectations it actually exercises, and the producer runs them before publishing a version.

## Every contract needs a named owner

An owner is not the implementer. The owner is whoever answers for the contract, approves changes,
and decides whether a change is additive or breaking.

**An unowned contract is an open question wearing a spec's clothes.** It reads as a decision, it
gets built against, and when it turns out to be wrong there is nobody who was wrong. Make owner
assignment an exit criterion of the first increment: a published contract with no owner degrades to
documentation within a sprint.

Track it plainly:

| Contract | Owner | Status | Gate |
|---|---|---|---|
| `capability/docs.intake` | — **unassigned** | field-level | — |
| `capability/erp.write` | — **unassigned** | not specified | instance licensing, module availability |

An honest table of unassigned owners is worth more than a plausible one.

## File skeleton and route conventions

Every file follows the same skeleton, carries its provenance in `x-` extensions, and obeys the
set-wide route conventions (tenant from the session and never from the payload, cursor pagination,
`Idempotency-Key` on creation, `If-Match` on updates, binaries only via short-lived signed URLs).

Full skeleton, extension vocabulary and conventions:
[references/file-skeleton.md](references/file-skeleton.md).

## Checklist

- `common/` is the sole owner of every reused component; no file redefines one.
- Every file declares version and status; every gated route and field says what gate blocks it.
- No payload field exists without a source; unsourced items are declared open in the file.
- Prose-vs-contract precedence written down.
- Structure check, anchor check and publish all green before "closed".
- Owner named per contract, or listed as unassigned in public.
