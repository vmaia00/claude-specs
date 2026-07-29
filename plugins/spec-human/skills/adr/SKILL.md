---
name: adr
description: Architecture decision records as the destination for method detail evicted from a spec. Use when recording a technical decision, when asked "why did we choose X", when maintaining a decisions log, when moving implementation detail out of a specification, or when an engineering document turns out to be a bundle of decisions misfiled as a peer of the functional spec.
---

# ADRs

An ADR is where evicted method-HOW goes to keep its reasoning. Removing prescription from a spec is
only safe if the prescription lands somewhere; otherwise the next team re-derives it badly, or the
same argument is had again in six months with nobody remembering the first answer.

Sort first with `constraint-vs-method`. Constraints stay in the spec. Everything else comes here.

## Record shape

```md
# ADR-NNNN: <decision, stated as a choice>

Status: proposed | accepted | superseded by ADR-NNNN
Date: YYYY-MM-DD

## Context
What forced a choice. The alternatives that were real, and why the obvious one was not taken.
Five lines. If it needs more, the decision is two decisions.

## Decision
One or two sentences. Present tense.

## Binding vs recommendation
- **Binding:** what the team may not change without breaking something, and what breaks.
  Usually empty, or one line pointing at a constraint in the spec.
- **Recommendation:** everything else in this record. Advisory. The team may decide otherwise
  without asking, and should record that as a superseding ADR.

## Consequences
What gets easier, what gets harder, what is now hard to reverse.

## What would change this
The concrete inputs that would reopen it: a benchmark, a pending vendor answer, a load threshold.
Real pending inputs only, never hypotheticals.
```

**The `Binding vs recommendation` field is not in the classic template and is required here.** It is
what makes an ADR safe as the destination for evicted prescription. Without it, a team reading an ADR
cannot tell advice from an order, and will treat the whole file as either one — both wrong.

## Rules

- **Numbered sequentially, never renumbered.** The number is the reference.
- **Immutable once accepted.** Correct a decision by writing a new ADR that supersedes it and links
  back; never edit the original. The wrong old decision plus its reasoning is more useful than a
  clean file that hides that the question was ever open.
- **One decision per record.** Two decisions in one file cannot be superseded independently.
- **Short.** Two minutes to read. An ADR longer than a page is a design document wearing a badge.
- **Indexed.** A table at the front of the ADR folder: number, title, status, date. It is the only
  navigation anyone uses.

## Where they live

Beside the spec set, in their own folder, referenced from the spec by number at the point where the
constraint appears — one link, not a discussion.

```
spec/
  01-functional.md          ← what and why; constraints with failure modes
  02-user-stories.md
  03-data-model.md
  decisions/
    README.md               ← index
    0001-....md
```

The spec says *what must hold*; the ADR says *how we would meet it and why*. A reader who trusts the
team reads only the spec. A reader who has to build reads both. Neither has to read the other's part.

## Splitting an over-prescriptive engineering document into ADRs

When a document in the set is mostly method-HOW, do not rewrite it and do not delete it. Split it.

1. Find the decision boundaries: each place the document chooses between real alternatives.
2. One ADR per boundary, carrying that section's context and reasoning as written.
3. For each, fill `Binding vs recommendation`. Most will be pure recommendation. The few binding
   lines get promoted into the spec as constraints, with failure modes, and the ADR points at them.
4. Leave the original as an index of the ADRs it became, or retire it once the index exists.
5. Retire nothing silently: the index records what the document was.

**Worked example.** In one failed document set, an entire engineering document opened by declaring
itself an engineering decision and explicitly handing the WHAT to another document. It was an ADR
bundle misfiled as a peer of the user stories — read as a specification, it was pure overreach; read
as decisions, it was exactly right. Reclassifying it answered a large part of the "too technical"
complaint **without cutting a single line**. Before cutting an over-detailed document, check whether
it is simply in the wrong category.
