---
name: spec-audience-declaration
description: Declare who executes a specification before writing it, and let that declaration set density, apparatus and prescription depth. Use when starting a spec, PRD or design doc; when asked "who is this for"; when a spec set changes hands or a new build team is onboarded; when deciding how detailed a document should be; or when reviewing a document whose level of detail is being disputed.
---

# Declare the executor

## Principle

**The executor is a requirement, not a preface.** It belongs in the first paragraph of the
document, not in a cover email or a kickoff meeting.

The executor determines four things that nothing else can settle:

- **Density** — how much text per unit of scope.
- **Apparatus** — provenance tags, ID cross-refs, impact matrices, changelogs, status labels.
- **Prescription depth** — where the document stops: at the constraint, or at the method.
- **Ordering** — what leads, what is appendix, what is omitted.

A document whose executor is undeclared **cannot be reviewed**. "Is this too detailed?" has no
answer without knowing who executes. Both "yes" and "no" are defensible, so the review collapses
into taste, and taste loses to whoever is more senior in the room.

## Do this first

Before writing any spec, PRD or design doc, ask for the executor. If the answer is not available,
state the assumed executor explicitly in the header and flag it as unconfirmed. Never proceed
silently.

## The header block

Stamp this on every spec, at the top, before any content:

```
Executor:            human engineering team | coding agent | mixed (state the split)
Assumed knowledge:   what the executor already holds and this document will not re-explain
May decide alone:    the decision space delegated to the executor
Must never decide:   the constraints that are not theirs to move, and who owns each
Doctrine:            spec-human | spec-agentic
```

Rules for the block:

- **Assumed knowledge is a promise.** Anything listed there must not reappear as explanation in the
  body. If it does, you have not decided who the reader is.
- **"Must never decide" is the load-bearing line.** It is what lets you delete method detail without
  losing control: the boundary is stated once, in the header, instead of being enforced by
  prescribing every step. See `constraint-vs-method`.
- **Mixed executors get a split, not an average.** Name which parts each executes. Averaging the
  density produces a document that is too thin for the agent and too thick for the human.

## Routing

| Declared executor | Doctrine | Projection that ships |
|---|---|---|
| Human team (in-house or external build partner) | `spec-human` | Selected what/why prose, hyperlinked, story cards with acceptance criteria. Rigour lives in a back layer the reader may consult but need not read. |
| Coding agent | `spec-agentic` | Exhaustive coverage, per-claim provenance, stable resolvable IDs, impact maps, contract set, changelog in body. |
| Mixed | Both | Two projections generated from one back layer. Never one document trying to serve both. |

## A change of executor is a change of requirements

When a spec set changes hands, **re-declare and re-project. Do not patch.**

Trimming an agent-doctrine document into a human-doctrine one by deleting tags leaves the
structure, ordering and uniform depth intact, which is most of what the human reader objects to.
Re-derive the human projection from the back layer instead.

Treat these as executor-change triggers: a new Tech Lead or build partner; a shift from
agent-generated implementation to a hired team, or the reverse; a spec set being handed to anyone
who was not in the room when it was commissioned.

## The cautionary tale

1. A consulting engagement wrote an MVP spec set optimised for agent execution: roughly 152 000
   words, one traceability marker per line, zero hyperlinks, every cross-reference a bare ID.
2. That density was chosen as a **governance instrument** — the client did not trust the incumbent
   supplier, and exhaustive, cited, unambiguous text was the control that made cutting corners
   visible.
3. The client then hired a senior Tech Lead and handed him the same documents.
4. His verdict: too detailed, obviously machine-produced, sourced for everything, full of
   references that are hard to follow. Every item measurably true.
5. Nothing in the documents was wrong for their original executor, and no word changed. The
   executor changed, and the same density that read as *control over a supplier* now read as
   *distrust of him*.

The failure was not the writing. It was that the document never declared who it was for, so it
could not be re-derived when that changed.

## References

- [references/executor-header.md](references/executor-header.md) — filled header examples, the
  handover re-declaration procedure, and how to audit a document that lacks a header.
- Companion doctrines: the `spec-for-humans` skill in this plugin; the `spec-agentic` plugin for
  the mirror image.
