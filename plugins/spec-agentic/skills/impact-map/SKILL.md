---
name: impact-map
description: Build per-entity impact cards and touchpoint matrices that answer "what breaks if this changes" for an agent with no working memory, generated from the data model and contract set rather than written by hand. Use when doing impact analysis or blast-radius analysis, when building a traceability or cross-reference matrix, when asked what depends on an entity or what to re-check before changing one, or when a multi-session agent build keeps breaking things it could not see from the section it was editing.
---

# Impact maps for agent executors

A human engineer editing an entity carries its blast radius in working memory. An agent does not: it
sees the section it opened and nothing else. The impact map puts that memory on disk, next to the
model, in a form the agent lands on by position.

This apparatus is expensive. In the worked example — a client portal data model — 51 entity cards
(1 337 lines) plus three touchpoint matrices (1 008 lines) made **68% of a 3 649-line file**. Run the
decision test in §4 before building it.

## 1. Per-entity impact cards

One card per entity, same seven fields in the same order every time. Uniformity is the point: the
agent learns the shape once and reads every card by position afterwards.

```md
**`UserCompany`** · writer: service P1 (see A.3)

- **Outbound FKs:**
  - UserId -> User
  - ProfileTemplateId -> ProfileTemplate
- **Referenced by (inbound FKs):**
  - CapabilityGrant.UserCompanyId
- **Logical references (non-FK):**
  - ClientId · CompanyId -> back-office (denormalised tenant pair in every row, invariant I-1)
  - this row is the grain of all access isolation (user x company) [Fact: ledger L05 (facts-ledger.md:32)]
- **Invariants touching it:**
  - I-1(a) tenant pair present in the row itself
  - I-4 authorisation data never in a general read cache
  - I-5 nothing is deleted: an association is deactivated, never removed
- **States · jobs · screens:**
  - EC-09 user management and matrix (EP-06)
  - EC-11 company selector (only for users with more than one company)
  - spec §7.7 association layer: synced from the back-office, snapshot on session
- **Contracts citing it (anchor graph, generated):** `ct-01.yaml` (7) · `platform.yaml` (4) · `ct-03.yaml` (1)
- **If it changes, re-check:**
  - CapabilityGrant FKs to this table: the fine-grained matrix grain is the association, not the user
  - ProfileTemplate must exist for the bootstrap template
  - §7.7 back-office <-> local company-list sync
```

Field rules:

- **`writer`** names the single component allowed to write the entity. The most common multi-service
  agent error is a second writer appearing quietly; naming the writer on the card blocks it.
- **Logical references (non-FK)** are the high-value field. FKs the agent can rediscover from the
  schema; cross-system references, denormalised tenant keys and shared idempotency keys it cannot.
- **`If it changes, re-check`** is the card's payload. Everything above it is context; this is the
  instruction. Include open questions by ID — they are the traps.
- **Contracts citing it** is generated, never hand-written. See §3.

Full field-by-field template and anti-patterns:
[references/card-template.md](references/card-template.md).

## 2. The three matrix types

Cards cover the model's interior. Matrices cover the seams to the rest of the spec, which is where an
agent editing one document breaks another.

1. **State machine → entities.** For each state (`S1 accepted`, `S2 held`, …): which entities exist
   in that state, which are null, which invariants apply, which jobs move it, which screens project
   it. This catches the classic agent error of writing a field on an entity that does not yet exist
   in the state being handled.
2. **Scheduled jobs → entities.** For each job: what it reads, what it writes, what it must not
   touch, idempotency key, failure/redrive path. Jobs are the most common source of writes that no
   screen explains.
3. **Screens → API routes → entities.** Three columns end to end. This is the one that answers "if I
   change this route, which screens break" without loading the front end.

Each matrix reuses the *same field layout as the cards*, so the agent parses one shape throughout.
Detail and worked rows: [references/matrices.md](references/matrices.md).

## 3. Generate, do not hand-write

Hand-maintained cross-references are stale within one editing round, and a stale impact map is worse
than none: the agent trusts it.

- **Derive edges from the schema** (FKs) and from the contract set (`x-provenance`-style anchors that
  name the spec section or entity each field serves). A small script walks contracts and documents,
  resolves anchors to targets, and emits the "referenced by" and "contracts citing it" lines. In the
  worked example that graph resolved 241 targets · 509 edges · 2 569 citations, regenerated on every
  contract change. See the `anchor-graph` skill.
- **Hand-write only the judgement fields**: invariants touching the entity, and `if it changes,
  re-check`. Those are the parts a generator cannot infer.
- **State the precedence rule on the map itself**: on any divergence between a card and the model
  section, *the model section wins and the card is corrected*. The map is a derived index, never the
  source. Without that line an agent will "fix" the model to match a stale card.
- **Regenerate in the same edit that changed the source.** A generated artefact left stale is a
  second, contradictory truth with no timestamp visible to the reader.

## 4. Decision test: does the apparatus earn its weight

Score the model before building it:

```
E = entities in the model
A = independent agents or sessions that will edit them (count a fresh context as one)
score = E x A
```

| Score | Build |
|---|---|
| < 30 | Nothing. The model fits in one context; an agent holds it. Cards are pure overhead |
| 30-150 | Cards only, generated fields plus `if it changes, re-check`. No matrices |
| > 150 | Cards + all three matrices, generated, with the precedence rule stated |

Three overrides, in either direction:

- **Multi-session edits force it up one band.** If edits span sessions with no shared memory, the map
  is the memory. This is the dominant factor; a 20-entity model edited over ten sessions needs cards.
- **Multiple writers force it up one band.** Two services writing the same entity make the `writer`
  field alone worth the apparatus.
- **A single-session, single-agent build drops it to nothing** regardless of entity count. Do not
  build a map for work that will be finished before the context ends.

If the score says build it and you cannot generate it, build the cards for the top-referenced
entities only (rank by inbound edges) and say in the map that coverage is partial. Partial and
honest beats complete and stale.

## 5. Micro-example, end to end

Model: `Invoice`, `InvoiceLine`, `Customer`, `Payment`. One agent, one session → score 4 × 1 = 4 →
**build nothing**.

Same model, but `Payment` is written by both the billing service and a reconciliation job, and the
build spans four sessions → override on multiple writers and multi-session edits → **build cards**.
The card that pays for itself:

```md
**`Payment`** · writers: billing service (create) · reconciliation job (settle) — two writers, see I-3

- **Outbound FKs:** InvoiceId -> Invoice
- **Referenced by:** (none)
- **Logical references (non-FK):** ProviderRef -> payment provider (opaque, not an FK; unique per provider)
- **Invariants touching it:** I-3 settle is idempotent on ProviderRef · I-5 payments are never deleted, only reversed
- **States · jobs · screens:** job `reconcile-daily` (settle only) · EC-04 invoice detail (read)
- **If it changes, re-check:**
  - the reconciliation job settles by ProviderRef, not by id: renaming or reusing it breaks idempotency
  - Invoice.Status is derived from payments; changing the sum path changes the invoice state machine
  - a third writer is not permitted (I-3); route new writes through one of the two
```

Nothing in that card is discoverable from the `Payment` schema alone, and all of it is needed by a
session that opens the file cold.

## Checklist

- [ ] Decision test run and the resulting band recorded in the map's header
- [ ] One card per entity, identical field order, no field silently omitted
- [ ] `writer` named on every card; multi-writer entities flagged against an invariant
- [ ] Generated fields actually generated, with the generator named and its last run stated
- [ ] Precedence rule stated: model section wins over card
- [ ] `If it changes, re-check` present on every card, and it carries open-item IDs
- [ ] Matrices built only if the score and overrides call for them
- [ ] Map regenerated in the same edit as the source change

## References

- [references/card-template.md](references/card-template.md) — field-by-field template, what belongs
  in each field, and the anti-patterns that make cards decay.
- [references/matrices.md](references/matrices.md) — the three matrix types with worked rows and
  generation recipes.
