# The back layer — where traceability goes

The objection to this doctrine is always the same: *if you strip the citations, you lose the
rigour.* You do not. Rigour is not the tags; the tags are one way of surfacing it, and the wrong
way for a human reader. Move it, keep it, link to it.

Say so explicitly in the reader-facing document, once, in the header, or the reader will assume
the claims are unsourced:

> The reasoning behind these requirements is recorded and traceable. The trail lives in the facts
> registry and the decision log, linked below. This document carries the conclusions.

## The four components

**Facts registry.** One canonical entry per fact about the client's world, each with its source and
a status: confirmed by the client, proposed by us and unconfirmed, or explicitly open. Prose cites
the registry as a whole, not per sentence. The registry is where a challenged claim gets settled,
and it is the thing you re-project from when the executor changes.

**Decision log (ADRs).** One record per decision: context, options, decision, consequences, status.
This absorbs every piece of method detail evicted from the spec body, plus every rejected approach
that would otherwise need a tombstone. It is also where an author's opinion becomes durable rather
than conversational. See the `adr` skill.

**Anchor graph.** The machine-readable relation between requirements, facts, decisions and
contracts. It is what makes coverage questions answerable — *which requirements depend on this
unconfirmed fact*, *what breaks if this decision is reversed* — without printing a matrix in the
document. It is generated and queried, never read.

**Contract set.** Interfaces as OpenAPI, JSON Schema or types, versioned alongside the code.
Authoritative for shape; the prose never restates it, only explains intent and constraints the
schema cannot express.

## Division of labour

| Question | Answered by |
|---|---|
| What must be true, and why does it matter | Reader-facing spec |
| How do I know that is true | Facts registry |
| Why was it done this way rather than another | Decision log |
| What else depends on this | Anchor graph, on demand |
| What exactly does the interface look like | Contract set |

Each question has exactly one home. Duplication across homes is how documents go stale, and it is
a large share of the bulk that budgets are trying to remove.

## Consequences worth stating up front

- **The back layer is the durable asset.** Projections are cheap and disposable once it exists;
  without it, every executor change means rewriting from scratch. Build it first even when only
  one projection is needed today.
- **Both doctrines derive from the same back layer.** `spec-human` and `spec-agentic` are two
  renderings, not two sources. Never let a fact exist only inside a projection.
- **Auditability improves.** A registry with one canonical entry per fact is more auditable than
  the same fact tagged 40 times in prose, where the 40 copies drift.
- **Someone must own it.** A back layer with no owner rots faster than a document, because nobody
  reads it end to end. Name the owner in the handover.

## Migrating an agent-doctrine set

1. Extract the facts registry from the inline provenance tags. Deduplicate ruthlessly: hundreds of
   tags typically collapse to a few dozen distinct facts.
2. Extract decisions from prescriptive method passages and tombstones into ADRs.
3. Extract the anchor graph from the ID cross-references before deleting them — the IDs are the
   graph, written out longhand.
4. Extract or generate the contract set from any prose that describes interfaces.
5. Only then write the human projection, from the back layer. Do not edit the old document.
6. Diff conclusions, not text: every requirement, invariant and acceptance criterion still present
   or deliberately dropped.

Step 5 is the one teams skip. Editing the old document forward keeps its ordering, its symmetry
and its uniform depth, which is most of what the reader was objecting to.
