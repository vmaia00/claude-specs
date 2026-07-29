# Executor header — examples, handover, audit

## Filled example: human team

```
Executor:            External build partner, 4 engineers, one Tech Lead. They write all code.
Assumed knowledge:   Their own stack, HTTP, relational modelling, auth patterns, CI. This
                     document explains none of it.
May decide alone:    Framework and library choice, module layout, schema shape below the stated
                     invariants, caching strategy, test structure, deployment mechanics.
Must never decide:   The identity boundary (owned by Security), what the regulator-facing archive
                     retains (owned by Compliance), the published API contract (owned by us —
                     change requires an ADR), which data leaves the tenancy (owned by Legal).
Doctrine:            spec-human. What and why. Method detail is deliberately absent, not omitted
                     by accident; where a method was fixed, there is an ADR and it is linked.
```

## Filled example: coding agent

```
Executor:            Coding agents, fresh session per task, no memory across sessions.
Assumed knowledge:   Language and framework syntax only. Assume nothing about this domain, this
                     codebase's history, or any decision not written here.
May decide alone:    Nothing outside an explicit "agent's choice" marker.
Must never decide:   Anything unstated. Stop and ask rather than infer.
Doctrine:            spec-agentic. Exhaustive; every claim carries provenance; IDs are stable and
                     grep-resolvable; retired approaches have tombstones so they are not re-proposed.
```

## Filled example: mixed

```
Executor:            Agents implement the pipeline and the adapters (chapters 5-8). A human team
                     builds and owns the client-facing application (chapters 1-4).
Assumed knowledge:   Split per part; see each chapter's opening line.
Doctrine:            Chapters 1-4 spec-human. Chapters 5-8 spec-agentic.
                     Both projections derive from the same facts registry and contract set.
```

Mixed documents are a last resort. Prefer two files that share a back layer. A single file with
two registers invites each reader to skim the other's half and conclude the whole thing is
badly written.

## Handover procedure

When the executor changes:

1. **Stop patching.** Do not open the existing document to delete tags.
2. **Confirm the new executor** and write the new header block first, alone, before any prose.
3. **Locate the back layer** — the facts registry, decision log, contract set, anchor graph. If
   there is none, extract one from the existing document; that extraction is the real work and it
   is worth doing, because it is what makes every future projection cheap.
4. **Re-project** from the back layer into the new doctrine. Expect the outline itself to change,
   not just the sentences.
5. **Diff the conclusions, not the text.** The check on a re-projection is that no requirement was
   lost, not that paragraphs survived. Requirements are in the back layer; paragraphs are not.
6. **Retire the old projection** or mark it clearly as the other executor's copy. Two live
   projections with no stated executor is the original failure, twice.

## Auditing a document with no header

Given a document whose density is disputed and whose executor is undeclared, do not argue about
detail. Measure, then declare, then re-project. Useful measurements:

- **Words against scope.** Total words divided by number of shipped capabilities. A number an
  order of magnitude above peer documents is the finding, not an opinion.
- **Markers per line.** Count inline provenance tags and ID cross-references. Approaching one per
  line means the apparatus is the document.
- **Apparatus share.** Percentage of lines in impact cards, traceability matrices, changelogs,
  tombstones and status labels. Anything above roughly a fifth is an agent-doctrine document.
- **Link density.** Number of resolvable hyperlinks divided by number of cross-references. Zero is
  the tell that the reader was never expected to be a person.
- **Depth variance across sections.** Near-zero variance means no editorial judgement was applied.

Report the measurements alongside the executor question. The measurements make the executor
question unavoidable; without them, it stays a matter of taste.

## Common failure: blaming the visible cause

Readers attribute an over-detailed document to whatever is most conspicuous in it, usually the
most technical chapter. Verify before acting: measure that chapter's share of the document. If it
is a small fraction, the complaint is about uniform exhaustiveness everywhere, and cutting the
technical chapter will not fix it. Fix the register, not the scapegoat.
