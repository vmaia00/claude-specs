# Length budgets — reasoning and enforcement

## Why a budget at all

A budget is not a style preference. It is the only mechanism that forces selection. Without a
ceiling, "add the detail" is always locally justified and the document grows until it stops being
read. The budget converts every addition into a trade: what comes out.

Budgets are **per document, prose only**. Machine-readable artefacts (OpenAPI, JSON Schema, type
definitions, migration files, fixtures) cost zero words, because the reader consults them rather
than reading them. Push detail there whenever the choice exists.

## The budgets

| Document | Budget | Ceiling | Unit of growth |
|---|---|---|---|
| Orientation note | 1 500 – 2 500 | 3 000 | Fixed. Does not grow with scope. |
| Product spec (what/why) | 8 000 – 12 000 | 15 000 | Sub-linear in capabilities. |
| User stories + acceptance criteria | 6 000 – 10 000 | 12 000 | Linear: ~200–300 words per card. |
| Data model | 3 000 – 5 000 | 6 000 | Sub-linear in entities. |
| Stack and operations note | 2 000 – 3 000 | 4 000 | Fixed. |
| ADR (each) | 400 – 800 | 1 200 | One per decision. |
| Interface / contract set | machine-readable | — | Not prose. |

Midpoints for a typical MVP set with six ADRs total roughly **30 000 words**.

## Per-document reasoning

**Orientation note.** Its job is to make the rest legible: the problem, why now, the shape of the
answer, what is out of scope. It is read once, before anyone has context, usually the evening
before a kickoff. It is fixed-size because context does not scale with feature count. If it will
not fit, the problem is not yet understood well enough to specify.

**Product spec.** 25–40 pages. The test is restatement: a senior engineer who read it this morning
can explain the system to a colleague this afternoon without opening it. Beyond ~15 000 words no
one holds the whole thing, the document becomes reference material, and reference material is
consulted selectively — which means the parts you most needed read will be skipped. Growth is
sub-linear because capabilities share invariants, and the second and third capability should
mostly inherit rather than restate.

**User stories.** The one document allowed to grow linearly, because each story is genuinely new
information and cards are independently readable — nobody reads all 38 at once, they read the
three they are building. Budget per card, not per document: a card plus its `Given / When / Then`
criteria in 200–300 words. If a card needs 600, it is two cards, or it contains method detail.

**Data model.** Entities, relationships, invariants, lifecycles, and the intent behind each. The
schema is the source of truth for shape; prose exists only for what a schema cannot express —
why an invariant exists, what a state transition means to the business, which field is a
compatibility scar. Prose that restates column types is pure duplication and goes stale first.

**Stack and operations note.** Boundaries and constraints: what must be true of hosting, identity,
data residency, availability, and the interfaces that are not the team's to move. Not routes, not
TTLs, not index definitions, not library choices. Those are the team's, and prescribing them is
the fastest way to be ignored on the things that actually matter.

**ADR.** One decision. Context, options considered, decision, consequences. Over ~1 200 words it
is either several decisions or an essay; split it or cut it.

## What the five-to-one reduction is made of

Going from ~152 000 words to ~30 000 for identical scope does not come from dropping requirements.
It comes, in rough order of yield, from:

1. **Apparatus removal** — per-entity impact cards and traceability matrices made up around 68% of
   one document in the failure case. This is the single largest line item and it costs nothing in
   content, because the same information is derivable from the back layer on demand.
2. **Changelog and status eviction** — roughly 8 500 words of revision history sat in document
   bodies before any content, plus 475 date stamps in one file.
3. **De-duplication** — the same constraint restated per consumer rather than stated once and
   linked.
4. **Method eviction** — prescriptive HOW moved to ADRs or handed back to the team.
5. **Tombstones and per-claim tags** — small individually, several thousand words together.

Note what is not on the list: requirements, acceptance criteria, invariants, contracts. If your
reduction is taking those out, you are shrinking the wrong layer.

## Enforcement

- **Count before shipping.** Word count per document against the table. Report the number in the
  handover; an unmeasured budget is not a budget.
- **Over budget means re-scope, not compress.** Compression produces dense prose that is worse to
  read than the long version. Ask instead: is this two documents? Is a third of it method detail?
  Is a section apparatus?
- **Under budget is a signal too.** A product spec at 2 000 words has usually pushed the hard parts
  into "the team will decide" without saying what they must not decide. Check the header's
  "must never decide" line.
- **Budget the set, not just the file.** Six documents each comfortably within budget can still be
  an unreadable set. Total prose for an MVP set should sit near 30 000 words.
