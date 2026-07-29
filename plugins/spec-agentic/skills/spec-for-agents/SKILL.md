---
name: spec-for-agents
description: Write specifications, PRDs and design documents that a coding agent will implement, using a declared executor contract, exhaustive uniform coverage, per-claim provenance tags, stable grep-resolvable IDs, in-body changelogs and tombstones. Use when authoring a spec that Claude Code or another agent will build from, when planning agentic or multi-session development, when the user says "spec for an agent to implement", "agentic development", "the agent will build this", or when an existing spec must be converted from human-team framing to agent-executable framing.
---

# Specs for agent executors

A specification is not a description of a system. It is an instruction set for a named executor.
Change the executor and the same properties flip sign. Write for the executor you actually have.

## 1. Declare the executor in the first paragraph

The failure this doctrine exists to prevent is **undeclared audience**. Every argument about a spec
being "too detailed" or "too vague" is really an argument about who executes it, held without either
side saying so. Stamp the answer at the top of every document, before the table of contents.

```md
## Execution contract

| | |
|---|---|
| **Executor** | agent · human team · mixed (name the split by area) |
| **Already knows** | what the executor loads or holds before reading: repo access, stack, prior docs, ledger |
| **May decide alone** | the classes of choice the executor owns outright |
| **Must never decide** | choices already made, and the document + ID where each lives |
| **Reading order** | documents to load, in order, before writing any code |
| **Projection** | agentic source · human-facing projection (see the `spec-human` plugin) |
```

Rules for the block:

- **Executor is one word, not a hedge.** "Mixed" is allowed only with a stated split by area
  ("data layer: agent; migration cutover: human ops team").
- **"May decide alone" is a real delegation.** If it is empty, the spec has to be exhaustive; that is
  a cost you are accepting on purpose, not an oversight.
- **"Must never decide" carries pointers.** An agent that cannot find where a decision lives will
  re-open it. Each line ends in a document + section + ID.
- **Never leave `Projection` blank.** It is the flag that stops an agentic source from being mailed
  to a human reader. See §7.

## 2. Same property, opposite sign

| Property | Agent executor | Human executor |
|---|---|---|
| Uniform depth, no prioritisation | correct — the agent supplies no editorial judgement | defect — reads as if no judgement was applied |
| Exhaustive coverage | correct — an agent cannot infer the unwritten | defect — buries what matters |
| Per-claim inline provenance tags | correct — verifiable, blocks drift across sessions | defect — the main "machine-made" tell |
| ID cross-refs (`CT-03`, `HU-04.13`, `O36`) | correct — grep-resolvable, stable under edit | defect — a decoder ring |
| Impact / touchpoint matrices | correct — the agent has no working memory | defect — noise a senior engineer already holds |
| Changelog + status labels in the body | correct — state recovery for a fresh context | defect |
| Tombstones for retired sections | correct — stops an agent re-proposing what was killed | defect |
| Prescriptive method-HOW (routes, TTLs, indexes) | correct — the agent supplies no design judgement | defect — insults competence |
| Hyperlinks | irrelevant | essential |
| Selection with stated rationale | insufficient on its own | essential |

Three properties of the executor drive the whole left-hand column:

1. **No working memory across sessions.** Session N+1 starts blank. Anything held only in a previous
   conversation is gone. Structure that a human would carry in their head has to be on disk.
2. **No editorial judgement.** An agent will not decide that section 6 matters more than section 11.
   Uneven depth is read as uneven requirement, not as emphasis. Uniform depth is the only honest
   signal; priority is expressed explicitly, as a labelled phase or gate, never as page count.
3. **Cannot infer the unwritten.** Silence is not a default — it is undefined behaviour, and the
   agent fills it by improvisation that looks confident and is unreviewable. Exhaustiveness is not
   padding; it is the removal of improvisation surface.

## 3. The document set shape that works

Five artefacts, in this order. Each one is loadable alone and refers to the others by ID.

1. **Functional spec, organised by epic** — product missions, users and profiles, information
   architecture, the central domain object and its state machine, then one section per epic, then
   access matrix, non-functional requirements, phasing and acceptance gates, known unknowns.
2. **User stories with Gherkin acceptance criteria** — `As [role], I want [action], so that [value]`
   plus `Given … when … then …`. The criteria are the executor's definition of done and the test
   plan's source. In the worked example: 38 story cards, 168 acceptance criteria.
3. **Data model with invariants** — entities by group, then hard invariants stated as numbered rules
   (`I-7 idempotency per item`), then sizing, then open items, then the physical annex.
4. **Contract set** — the API/event contracts as machine-checkable files, referenced from both specs
   by contract ID. See the `contract-set` skill.
5. **Intake and engineering design records** — pipeline/ingest specs and the record of engineering
   decisions the agent must not re-litigate.

Full section-by-section outline: [references/document-set.md](references/document-set.md).

## 4. Per-claim provenance

Every non-trivial claim carries exactly one tag, inline, at the end of the sentence or bullet:

- `[Fact: file:line]` — traceable to a source. Cite file and line, verbatim quote where short.
- `[Proposal]` — the author's design, not yet confirmed by whoever owns the decision.
- `[Open: ID]` — a question, registered in the ledger under that ID. Never resolved by guess.

Why inline and per-claim rather than a bibliography: the agent reads a paragraph, not a document.
A tag at the point of use is the only form that survives partial reads, and it is what makes a later
session able to tell *this is fixed* from *this is my predecessor's guess* — the single most common
cause of silent drift across a multi-session build.

Cost, measured: one spec document carried 554 provenance tags and 1 555 ID cross-references over
2 108 lines — **2 109 traceability tokens, about one per line**. That is the price. It bought the
ability to re-verify any claim in the document without re-running the discovery that produced it.

The registry of facts behind the tags belongs in a ledger, not in prose. See the `facts-ledger`
skill.

## 5. Uniform structure and stable IDs

- **Uniform section structure** so the agent can locate by position: every epic section has the same
  subsections in the same order, every entity card the same fields. Positional predictability is
  what lets an agent read 8% of a document and still land on the right paragraph.
- **Stable IDs, never renumbered.** IDs name artefacts (`EP-06` epic, `HU-04.13` story, `EC-09`
  screen, `CT-03` contract, `I-7` invariant, `O36` open item). Retire an ID, never reuse it;
  renumbering silently invalidates every reference elsewhere. Reserve distinct prefixes per
  namespace and state the convention in the header block.
- **ID collisions are a build-stopping defect.** Two artefacts sharing one ID means an agent
  resolves the reference to the wrong thing with full confidence. Check for collisions on every
  edit; the worked example hit one and had to renumber a whole batch of stories to repair it.
- **Prefer greppable IDs over hyperlinks.** Links rot on file moves and are invisible to an agent
  reading raw text; `CT-03` resolves by search from any working directory.

Graph maintenance, collision checking and anchor generation: see the `anchor-graph` skill.

## 6. Changelog, status labels and tombstones — in the body

All three are state-recovery mechanisms for an executor that starts every session blank.

- **Changelog in the body, not in git.** Git history answers "what changed"; the body changelog
  answers "why this now says X when you may have been told Y", which is the question a fresh agent
  actually has. Version rows carry the reasoning, not the diff.
- **Status labels on sections** (`draft`, `closed`, `to deepen`, `blocked on O36`) so an agent knows
  whether a section is buildable or is still a question.
- **Tombstones for retired sections.** When a screen or epic is dropped, leave the ID with a one-line
  headstone: what it was, when it was retired, why, and what replaced it. Delete it instead and the
  next session re-proposes it, in good faith, from first principles — repeatedly.

Honest cost: in the worked example the two body changelogs ran to 4 728 and 3 833 words —
**about 8 500 words of pure history** in a set of roughly 152 000. Roughly 6%. Accept it or
consciously cap it (keep the last N versions in the body, archive the rest to a sibling file); do
not silently drop it.

## 7. Failure mode: never ship the agentic source to a human

A spec written this way, handed to a human team, is rejected on sight. The observed verdict on the
worked example, from a newly-arrived human tech lead: *too detailed, clearly produced by an agent,
sources for everything, references hard to follow.* Every one of those is a property from the
left-hand column of §2, read by the wrong executor.

The documentation was not wrong. It was right for the executor it was built for.

**Rule: the agentic document is source, not delivery.** For a human reader, produce a *projection* —
same content, different selection and shape: prioritised, links instead of ID codes, provenance
demoted to an appendix, method-HOW replaced by intent plus constraints. Use the `spec-human` plugin.
Never let a human reader receive the source, and never degrade the source to make it palatable —
that destroys the executor's structure to please a reader who was not going to execute it anyway.

If the audience is genuinely mixed, split by area in the execution contract and project each area
separately. Do not average the two doctrines; the average serves neither.

## 8. When NOT to use this

- **Small scope, one session, one agent.** If the whole job fits in a single context window, the
  apparatus costs more than it returns. Write the plan, build, move on.
- **A human team builds it.** Use `spec-human`.
- **Exploratory or throwaway work**, spikes, prototypes where the output is a finding, not a system.
- **The decisions are not yet made.** This doctrine records decisions with high fidelity; it does not
  make them. Run the decision process first, then specify.
- **No source of truth exists to cite.** Provenance tags over invented facts are worse than no tags:
  they launder guesses into apparent evidence. Get sources, or mark everything `[Proposal]` honestly.

## Checklist before handing a spec to an agent

- [ ] Execution contract block present, executor named in one word, projection stated
- [ ] Every non-trivial claim carries `[Fact: file:line]`, `[Proposal]` or `[Open: ID]`
- [ ] No ID collisions; no renumbered IDs; retired IDs tombstoned, not deleted
- [ ] Uniform subsection structure within each repeated section type
- [ ] Acceptance criteria in Given/When/Then for every story
- [ ] Invariants numbered and referenced from the entities they constrain
- [ ] Body changelog current; status label on every section that is not closed
- [ ] Open items resolvable to a ledger ID; none resolved by guess
- [ ] Contract IDs referenced from both the functional spec and the data model
- [ ] Reading order stated, and each document loadable on its own

## References

- [references/executor-header.md](references/executor-header.md) — the header block, filled examples
  for agent / human / mixed, and the failure signatures of each field left blank.
- [references/document-set.md](references/document-set.md) — the five-artefact set, section by
  section, with the measured shape of the worked example.
- [references/projection-to-humans.md](references/projection-to-humans.md) — what to strip, keep and
  transform when producing the human-facing projection.
