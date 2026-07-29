---
name: sample-chapter-first
description: Ship one representative chapter to the real reader before generating a document set. Use before producing a large spec or documentation set, when validating tone, density or format with a stakeholder, when asking "is this the right level of detail", when a new reader is taking over a document set, or when avoiding a rewrite of work already produced.
---

# Sample chapter first

**Rule: before generating a document set, send one representative chapter to the person who will
actually consume it, and wait for an answer.**

In the case this plugin exists to answer, roughly 152 000 words across four documents were produced
without a single chapter being shown to the engineer who would build from them. The verdict, on
delivery of the whole set: too detailed, too technical, obviously machine-produced, references
impossible to follow. The cheapest available check was never run, and the set had to be reworked
wholesale.

The gate is not a review of content. It is a test of **register**: density, tone, format, and whether
the reader can resolve what the document points at. Register cannot be validated from inside the
authoring context, because the author holds everything the reader does not.

## What the sample must contain

A chapter is diagnostic only if it exercises every property that could be wrong. Minimum:

1. **One section at full intended density** — not a summary, not the introduction. The reader must
   see the worst case, not the best.
2. **One cross-reference of each kind used** — to another document in the set, and to a companion
   artefact. This is what surfaces whether references are resolvable by someone holding only what was
   sent.
3. **One acceptance-criteria block** in the exact format the set will use.
4. **One technical constraint**, written in the form the set will use, with its rationale.

Anything less does not surface the mismatch. An introduction plus a table of contents always reads
fine and predicts nothing.

Send it as it will be delivered: same file format, same rendering, same naming. Format complaints are
real complaints and you want them now.

## The three questions

Ask exactly these, in writing, and do not soften them.

| Question | If the answer is bad, this is what it means |
|---|---|
| **Is the level of detail right for how you intend to work?** | "Too much" is rarely about volume; it is prescription the reader expects to own. Sort it with `constraint-vs-method` before writing more. "Not enough" means the executor assumption is wrong in the other direction — re-run the audience declaration. |
| **Can you resolve every reference using only what I sent you?** | Any "no" is a structural defect, not an editing one. It means the set assumes companion material, an ID glossary or project history the reader does not hold. Fix the reference model before generating; it is not fixable later without touching every file. |
| **What would you cut?** | The answer names the reader's noise floor. Cut it everywhere, once, before the set exists. Also read what they *do not* offer to cut: that is what the set is for. |

A fourth, optional but revealing: **who do you think wrote this?** If the reader volunteers "an
agent", the machine tells are above threshold and the whole set will be discounted on arrival,
whatever its quality.

## Where this sits in the pipeline

A typical delivery pipeline checks facts, then quality, then grammar, then brand. Every stage asks
whether the document is correct, well made and on-brand. **None asks whether the intended reader can
use it.** That is the missing gate, and it is the only one whose failure invalidates all the others:
a document that is factually perfect and unusable is worth nothing.

It runs **first**, not last — before generation, not before delivery. Placed at the end it is a
post-mortem.

```
audience declared → SAMPLE CHAPTER → reader answers → generate set → facts → quality → brand → deliver
```

If the reader does not answer, that is itself a finding: escalate, or generate the smallest viable
subset and hold the rest. Do not interpret silence as approval and produce the set anyway.

While waiting, run the `tech-lead-reader` agent on the sample. It simulates the reader from the
folder alone and catches unresolvable references and machine tells cheaply. It is a rehearsal, not a
substitute: it cannot tell you what the real reader intends to own.

## Cost asymmetry

The sample costs hours. The rewrite costs weeks, and is paid alongside the loss of confidence that
comes from a rejected delivery — which no amount of subsequent quality recovers. There is no volume
of work at which skipping this gate is rational, and the larger the set, the more it favours running
it.

## Checklist

- [ ] The reader is a named individual who will build or approve, not a role or a proxy
- [ ] The sample is one full-density section, not an introduction or summary
- [ ] It contains a cross-reference of every kind the set will use
- [ ] It contains one acceptance-criteria block and one constraint, in final form
- [ ] It is delivered in the final format and rendering
- [ ] The three questions were asked verbatim, in writing
- [ ] The answers changed something before the set was generated, or the set was not generated
