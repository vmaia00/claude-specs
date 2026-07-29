---
name: spec-for-humans
description: Write specifications for a human engineering team — what and why, never how. Use when writing a spec, PRD or design doc that a Tech Lead or build team will read; when asked for "what and why not how"; when simplifying or re-projecting an over-detailed spec; when handing specs to an external build team; or when a document has been called too detailed, too technical or obviously machine-generated.
---

# Specs for human executors

Precondition: the executor is declared. Run `spec-audience-declaration` first. This register is
correct **only** for a competent human team, and wrong for a coding agent.

## 1. What and why, before any how

Every section answers, in this order: **what must be true**, **why it matters**, and only then
anything about mechanism. If a paragraph opens with a mechanism, it is in the wrong document or
the wrong order.

Method detail is not deleted, it is relocated. Where a method genuinely is fixed, say so as a
constraint with its reason, and link the ADR. See `constraint-vs-method` for the cut, and `adr`
for where the evicted detail lives.

## 2. Selection over exhaustiveness

A human author **omits, ranks, and says what matters most**. That is the visible evidence of
editorial judgement, and its absence is what makes a document read as machine-made.

- Lead each chapter with what is most likely to be got wrong, not with what is first alphabetically
  or first in the data model.
- State ranking in words: *this is the part that decides whether the release works*; *this is
  routine and needs no discussion*.
- **The uniform-depth test:** if every subsection is roughly the same length, no judgement was
  applied. Fix by cutting, not by padding the short ones.
- Anything you cannot rank, you do not yet understand. Rank it or cut it.

## 3. Length budgets

Budgets are per document, prose only. Machine-readable artefacts do not count against them.

| Document | Budget | Ceiling | Why |
|---|---|---|---|
| Orientation note | 1 500 – 2 500 | 3 000 | Read before the kickoff, in one sitting. If context needs more, the problem is not understood yet. |
| Product spec (what/why) | 8 000 – 12 000 | 15 000 | 25–40 pages. A senior engineer reads it in a morning and can restate it from memory. |
| User stories + acceptance criteria | 6 000 – 10 000 | 12 000 | ~200–300 words per card. The only part allowed to grow linearly with scope. |
| Data model | 3 000 – 5 000 | 6 000 | Entities, invariants, lifecycles. The schema is the source of truth; prose explains intent only. |
| Stack and operations note | 2 000 – 3 000 | 4 000 | Boundaries and constraints, not routes, TTLs or index definitions. |
| ADR (each) | 400 – 800 | 1 200 | One decision, one or two pages: context, options, decision, consequences. |
| Interface / contract set | machine-readable | — | OpenAPI, JSON Schema, types. Never prose. Costs zero words. |

A full MVP set lands near **30 000 words**. The failure this doctrine exists to prevent shipped
**152 000** for the same scope. Five-to-one is the routine reduction, and it comes almost entirely
from apparatus and repetition, not from dropped requirements.

Over budget is a signal to re-scope the document, not to shrink the font. See
[references/length-budgets.md](references/length-budgets.md).

## 4. Links, not codes

**Never make a reader resolve an identifier by hand.** Every cross-reference is a hyperlink to a
target the reader can open.

- Write the meaning, then link it: *the [document-status contract](...)*, not `CT-03`.
- If the target is not in the reader's hands, either ship it with the set or cut the reference.
  A pointer into a document the reader does not have is worse than no pointer.
- Anchor every heading so links land on the passage, not the top of a 200-page file.
- Bare IDs in a human-facing document are a decoder ring. Zero hyperlinks across a large spec set
  is the clearest possible proof that no person was expected to read it.

## 5. Keep the machinery out of the prose

- **Changelog out of the body.** One dated file at the end, or the version-control history. Never
  thousands of words of revision history before the content starts.
- **Status labels out of the prose.** Draft/confirmed/pending state belongs in the back layer or a
  single status table, not inline on every claim.
- **No tombstones.** A human does not re-propose a rejected approach if the ADR exists; agents do,
  which is why the other doctrine keeps them.
- **No scattered date stamps.** Dates go on decisions, in the ADR, not on paragraphs.
- **No audit-finding IDs in headings.** Headings name the subject in the reader's vocabulary.

## 6. Pre-ship checklist: the machine tells

Search for each and remove it. Details and search patterns in
[references/machine-tell-checklist.md](references/machine-tell-checklist.md).

- [ ] **Uniform section depth** — every subsection the same length.
- [ ] **Per-claim provenance tags** — inline citations on sentences that no one disputes.
- [ ] **Bare ID cross-references** — any `AB-12`-shaped token in running prose.
- [ ] **Apparatus sections** — impact cards, touchpoint tables, traceability matrices.
- [ ] **Changelog in the body** — revision history before or between content.
- [ ] **Tombstones** — sections describing what was removed and why it stays removed.
- [ ] **Absent authorial voice** — no stated risk opinion, no *we tried X and rejected it*, no
      *this is the part most likely to hurt us*. A document with no opinion had no author.
- [ ] **Perfect structural symmetry** — identical subsection sets under every heading, regardless
      of whether each has content worth writing.
- [ ] **Explaining what the header promised was assumed knowledge.**

## 7. Traceability moves, it does not disappear

This is the reassurance a team migrating from the agentic doctrine needs, and it must be stated in
the document itself, once, in the header:

> The reasoning behind these requirements is recorded and traceable. The trail lives in the facts
> registry and the decision log, linked below. This document carries the conclusions.

Rigour stays in the **back layer** — facts registry, decision log, anchor graph, contract set. The
reader-facing document carries conclusions plus links for anyone who wants to audit one. Nothing
is lost; the audit trail simply stops being interleaved with the argument. See
[references/back-layer.md](references/back-layer.md).

## 8. The format that already works

In the failed spec set, one of four documents drew **no complaint at all**: the user stories —
roughly 95% what/why, 38 story cards, 168 `Given / When / Then` acceptance criteria, and a
conventions line that explicitly banned jargon from its own text. It was the least apparatus-heavy
document and the only one written in the reader's vocabulary.

Use it as the model. Story card plus Gherkin acceptance criteria, in the reader's own words, is the
default unit of a human-executor spec. Template in
[references/story-cards.md](references/story-cards.md).

## Related

- `constraint-vs-method` — which detail survives the cut and which is method the team owns.
- `sample-chapter-first` — validate this register on one chapter before generating the set.
- `adr` — where evicted method detail and rejected options live.
- `spec-agentic` plugin — the mirror doctrine, for when the executor is a coding agent.
