# Impact card: field-by-field

One card per entity. Same fields, same order, every time. An agent that has read one card can then
read any card by position, which is the whole reason the format is rigid.

## Header line

```md
**`EntityName`** · writer: <single component> (source of that claim)
```

- Backticked entity name so it is greppable and typographically distinct from prose.
- **Writer is singular by default.** If there are genuinely two, write both and point at the
  invariant that permits it: `writers: A (create) · B (settle) — two writers, see I-3`. An unexplained
  second writer is the defect this field exists to catch.
- Cite where the writer assignment comes from (a physical annex table, a service map), so a later
  session does not re-decide it.

## Fields, in order

### 1. Outbound FKs

Declared foreign keys leaving this entity, as `Column -> Target`. Write `(none declared)` explicitly
rather than omitting the field — an omitted field reads as "not yet analysed", a stated `(none)`
reads as "analysed, empty".

### 2. Referenced by (inbound FKs)

`Source.Column` for every FK pointing here. **Generated** from the schema. This is the field that
answers "how many things will I break" at a glance; a high count is itself a signal that the entity
needs care.

### 3. Logical references (non-FK)

The highest-value field, and the only one that cannot be recovered from the database. Include:

- **Cross-system references** — ids owned by another system, with no local FK, and the contract that
  validates them (`ClientId -> back-office (validated via CT-01, no local FK)`).
- **Denormalised keys** carried for isolation or partitioning, with the invariant that mandates them.
- **Shared idempotency keys** (`ContentHash + CompanyId is the shared key with CT-02, I-7`).
- **Shared enums** — a value set defined in another document; name the document.
- **Version/generation counters** consumed elsewhere (`SessionVersion is read by Session.VersionSnapshot`).
- **Legacy columns that do not exist in the target** and live only in the migration map. Say so
  explicitly; otherwise an agent implements them.

### 4. Invariants touching it

Reference numbered invariants by ID with a half-line reminder of what each says. Never restate the
rule in full: two statements of one rule produce two implementations.

### 5. States · jobs · screens

Where this entity appears in the rest of the spec: state-machine states, scheduled jobs, screen IDs,
route paths, and the spec sections that govern it. This is the seam to the functional document, and
the reason an agent editing the data model does not silently break a screen.

### 6. Contracts citing it (generated)

`file.yaml (n)` pairs from the anchor graph, ordered by citation count. Never hand-written; label it
as generated and name the generator so a reader knows a stale line is a regeneration problem, not an
authoring one.

### 7. If it changes, re-check

The payload. Everything above is context. Write instructions, not observations:

- Consequences that are not visible from the schema ("the job settles by `ProviderRef`, not by id:
  reusing it breaks idempotency").
- Open questions by ID that would be resolved or invalidated by the change (`[Open: O36]`).
- Migration constraints (`filtered unique index on ExternalSubjectId is what lets existing accounts
  migrate; dropping it blocks the second wave`).
- Contracts and telemetry rules that must move with the change.

Three to six bullets. If it needs more, the entity is doing too much and the card is telling you so.

## Anti-patterns

| Anti-pattern | Why it decays |
|---|---|
| Restating the invariant text on the card | Two sources for one rule; the agent implements the copy it read |
| Hand-maintaining the generated fields | Stale within one editing round, and trusted anyway |
| Omitting a field when it is empty | Indistinguishable from "not analysed yet" |
| Prose paragraphs instead of the fixed field list | Positional reading breaks; the agent must read the whole card |
| Cards for entities nobody references | Pure weight; rank by inbound edges and cover the top of the list |
| No precedence rule on the annex | An agent "fixes" the model to match a stale card |
| Cards that duplicate the entity definition | The card is an index of consequences, not a second schema |

## Maintenance contract

State this at the top of the card annex, verbatim in substance:

```md
Maintenance: generated fields (referenced-by, contracts-citing) are produced by <generator>;
last run <date>. Judgement fields (invariants, if-it-changes) are revised with every material
change to the model, and the "if it changes, re-check" list of each card is the trigger.
On any divergence between a card and the model section, the model section prevails and the
card is corrected. This annex is a derived index, never the source.
```
