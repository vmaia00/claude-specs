# The five-artefact document set

The shape below is drawn from a client portal spec set built for agent execution: roughly
152 000 words over four documents plus a contract set. Sizes are given so the cost is visible.

Split by *kind of statement*, not by chapter of a single book. Each artefact answers one class of
question, is loadable alone, and refers to the others by ID rather than by inclusion.

## 1. Functional specification, organised by epic

The largest document. Measured: 62 177 words, 2 108 lines, 2 109 traceability tokens.

Section order that worked:

| § | Content | Why the agent needs it here |
|---|---|---|
| 0 | Document control, execution contract, ID conventions, changelog | State recovery for a blank session |
| 1-2 | Product missions and numbered product principles (`PU-n`) | The tie-breakers for choices the spec did not foresee |
| 3 | Users and profiles | Every later access statement resolves against these names |
| 4 | Information architecture: navigation, landing per profile | Fixes the surface before behaviour is described |
| 5 | The central domain object: lifecycle, state machine, projections | The single most-referenced section; states get IDs (`S1`…`S11`) |
| 6 | **One section per epic** (`EP-01`…), uniform subsections | The build unit |
| 7 | Access matrix: profile × capability × sensitivity tier | Authorisation stated once, referenced everywhere |
| 8 | Contracts consumed and exposed, by contract ID | The integration boundary |
| 9 | Non-functional requirements specific to this system | Performance, telemetry, privacy rules with numbers |
| 10 | Phasing and acceptance gates | Where priority lives — as gates, never as depth |
| 11 | Known unknowns and the plan to close them | Prevents an agent inventing a resolution |
| 12 | Kick-off readiness | What must be true before code starts |
| 13 | Stack and operations | Hosting, CI/CD, TLS, rate limiting, cache, scaling, monitoring, HA/DR |

Uniform subsections inside every epic section, in the same order every time: purpose · user stories
by ID · screens · rules · edge cases and empty states · open items. Positional predictability is
what lets an agent read a fraction of the document and still land correctly.

**Priority belongs in §10, not in section length.** An agent reads a longer section as a bigger
requirement, not as an emphasised one. Express priority as a numbered phase with a gate condition.

## 2. User stories with Gherkin acceptance criteria

Measured: 38 story cards, 168 acceptance criteria, in a companion document that gap-fills the
functional spec rather than restating it.

```md
### HU-02.7 · Capture-quality guidance at photo time (later phase) [Proposal]

As a user photographing a document on a phone, I want guidance at the moment of capture,
so that the document arrives legible the first time.

Acceptance criteria:
- Given I start camera capture in EC-03, when I frame the document, then I get immediate
  guidance on distance, shadows and legibility before the photo is accepted [Proposal].
- Given a photo judged illegible, when I try to continue, then I can retake it without
  leaving the flow, and the retake creates no duplicate item [Proposal].
- Phase: later phase, aligned with HU-02.5 [Open: O62].
```

Rules:

- **Reference by ID, never redefine.** A companion document that restates a story from the main spec
  creates two versions of one truth and the agent will read whichever it loaded.
- **Continue the numbering, never renumber.** New stories in `EP-07` start after the last existing
  one. Renumbering invalidates every reference elsewhere in the set.
- **Each criterion carries its own provenance tag.** Criteria migrate into tests; the tag migrates
  with them and tells a later session whether a failing test encodes a fact or a guess.
- **INVEST still applies.** Independent, negotiable, valuable, estimable, small, testable.

## 3. Data model with invariants

Measured: 55 841 words. Structure: scope and principles · ERD · entities by group · hard invariants ·
sizing · open items · physical annex · impact map annex · touchpoint matrices.

- **Invariants are numbered rules** (`I-1` tenancy key present in the row itself, `I-7` idempotency
  per item), stated once and referenced from every entity they constrain. An agent that finds the
  same rule restated in three places will implement three variants of it.
- **Entities grouped by concern**, with one writer named per group. "Who writes this" is the
  question an agent gets wrong most often in a multi-service build.
- **The physical annex is separate from the logical model.** Logical model is the contract; the
  physical annex is engineering, and it is labelled as such so a later session knows which one it is
  allowed to change.
- **Impact map and touchpoint matrices**: 68% of this file. See the `impact-map` skill for whether
  that is justified in your case.

## 4. Contract set

Machine-checkable interface definitions (OpenAPI/AsyncAPI/JSON Schema), one file per contract,
each with a stable `CT-nn` ID referenced from both the functional spec and the data model.

The contract set is the only artefact in the group that a CI job can verify against the running
system. Everything else is prose the agent must be trusted to have read. Push as much of the spec's
precision into the contract set as the format allows. See the `contract-set` skill.

## 5. Intake and engineering design records

Pipeline/ingest specification (measured: 135 000 characters) plus the record of engineering
decisions taken outside the client's authority: what was decided, when, why, and what would reverse
it. This is the anti-relitigation artefact. Without it, each new session re-derives the same
architecture, differently.

## Cross-document hygiene

- **One ID namespace across the whole set.** `EP-`, `HU-`, `EC-`, `CT-`, `I-`, `S-`, `PU-`, `PA-`,
  plus reserved prefixes for the fact ledger that never name artefacts. State the convention in §0.
- **Never define the same thing twice.** Cross-reference by ID. Where the same table must appear in
  two documents, generate it into both from one source and say so.
- **State the reading order** in each execution contract, and make each document independently
  loadable — an agent will open exactly one of them first.
- **Regenerate derived content in the same edit.** Impact maps, anchor graphs, matrices and rendered
  outputs are downstream of the source; leaving them stale hands the next session two conflicting
  answers with no way to tell which is current.
