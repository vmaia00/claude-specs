# Story cards and acceptance criteria

The unit of a human-executor spec. In the failure case this was the only one of four documents
that drew no complaint: ~95% what/why, 38 cards, 168 `Given / When / Then` criteria, and a
conventions line banning jargon from its own text.

## Template

```markdown
### <Number>. <Short title in the reader's vocabulary>

**As a** <role, named as the business names it>
**I want** <capability>
**So that** <outcome that matters to someone>

<One or two sentences of why: what breaks today, or what this unlocks. Not mechanism.>

**Acceptance criteria**

1. **Given** <state> **When** <action> **Then** <observable result>
2. **Given** ... **When** ... **Then** ...

**Out of scope:** <the adjacent thing a reader will assume is included, and is not>
**Open:** <the question still owed to someone, with the owner named by role>
```

## Rules

- **Vocabulary is the business's, not the system's.** Put the ban in the document's own conventions
  line so it is enforceable in review: no internal system names, no table names, no protocol
  jargon, no acronyms the business does not already say out loud.
- **Criteria are observable.** *Then* describes what a person or an external system can see. If it
  describes an internal state that only a developer can inspect, it is method and it does not
  belong. Rewrite it as its visible consequence, or delete it.
- **200–300 words per card.** A card at 600 words is two cards, or it has absorbed method detail.
- **Criteria count is the depth signal.** Cards do not all get the same number. A high-risk card
  earns eight criteria; a routine one earns two. Equal counts across all cards is the
  uniform-depth tell in miniature.
- **Cover the unhappy paths deliberately, not exhaustively.** The failures that change behaviour —
  rejection, timeout, partial data, concurrent edit, permission denied — get criteria. Every
  conceivable error does not.
- **One card, one outcome.** If the *So that* has an "and" joining two unrelated outcomes, split.
- **Out of scope is not optional.** Most scope disputes are about the adjacent thing the reader
  assumed. Naming it costs one line and prevents a rebuild.
- **No status labels, no dates, no IDs in the title.** The title names the capability. Anything
  else goes in the back layer.

## Ordering

Order cards by the sequence in which the team will build them, and say so. Not by entity, not by
screen, not alphabetically. The first cards should be the ones that prove the risky assumptions,
and the document should say which those are and why — that single paragraph is most of the
editorial judgement the document contains.

## What does not go on a card

- Endpoint paths, payload shapes, status codes. Those live in the contract set.
- Schema, indexes, cache policy, retries, TTLs. Those are the team's, or an ADR's.
- Provenance tags. If a criterion is contested or legally binding, link the source once, in prose.
- Impact tables listing which components the card touches. That is the team's analysis, not yours.

## Review test

Hand a card to someone from the business side who did not write it. If they can tell you whether
it is correct without asking what a word means, it is finished. If they can also tell you what the
system will do when it goes wrong, the criteria are complete.
