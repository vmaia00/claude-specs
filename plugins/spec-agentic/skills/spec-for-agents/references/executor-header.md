# The execution contract block

Stamp this at the top of every specification document, above the table of contents and below the
title. It is the first thing a fresh agent session reads and the first thing a reviewer checks.

## Template

```md
## Execution contract

| | |
|---|---|
| **Executor** | agent · human team · mixed (split stated by area) |
| **Already knows** | what the executor holds or loads before this document |
| **May decide alone** | classes of choice the executor owns outright |
| **Must never decide** | choices already made + document/section/ID where each lives |
| **Reading order** | documents to load, in order, before writing code |
| **Projection** | agentic source · human-facing projection of <source doc> |
```

## Filled example — agent executor

```md
## Execution contract

| | |
|---|---|
| **Executor** | Agent (Claude Code), multi-session, no shared memory between sessions |
| **Already knows** | repo read access; the stack (framework + ORM + queue); documents 03, 06, 07 loaded on demand by ID |
| **May decide alone** | file layout inside a module, private helper naming, test fixture shape, log message wording |
| **Must never decide** | tenancy key shape (§6 I-1) · auth model (§7.7) · contract payloads (contract set, CT-01…CT-18) · retention windows (§5.7) · anything tagged `[Fact: …]` |
| **Reading order** | 03 blueprint → this document → 06 data model → contract set → 07 intake |
| **Projection** | agentic source. Human-facing projection: `05-summary-for-review.md` |
```

## Filled example — human executor

```md
## Execution contract

| | |
|---|---|
| **Executor** | Human team (4 engineers, in-house, own the codebase after handover) |
| **Already knows** | the domain, the existing codebase, standard web architecture; does not know our access model or the intake state machine |
| **May decide alone** | all method-HOW: routes, schema details, caching, indexes, libraries, deployment topology |
| **Must never decide** | the access matrix (§7) · retention obligations (§5.7) · the contract surface consumed by third parties (CT-01…CT-18) |
| **Reading order** | this document; annexes only when the linked section calls for them |
| **Projection** | human-facing projection of the agentic source `05-portal-spec.md` |
```

## Filled example — mixed, split by area

```md
## Execution contract

| | |
|---|---|
| **Executor** | Mixed. Application layer + tests: agent. Data migration and cutover: human ops team. Infrastructure: human platform team. |
| **Already knows** | agent: repo, stack, documents 06/07 · ops: the source database and the current runbook · platform: the target cloud account |
| **May decide alone** | agent: nothing outside the module boundary (§6.3) · ops: migration batching, window, rollback drill · platform: everything below the load balancer |
| **Must never decide** | all three: the invariants (§4) and the contract surface (contract set) |
| **Reading order** | agent: 06 → this → contracts · ops: §11 migration annex only · platform: §13 stack & operations only |
| **Projection** | agentic source for §1-§10; §11 and §13 are already written as human projections |
```

Never average the doctrines across a mixed team. Write each area for its own executor and say so in
the block. A document that is 60% agentic and 40% human throughout satisfies neither reader.

## What each blank field costs you

| Field left blank | Failure signature |
|---|---|
| **Executor** | The perennial "too detailed" / "too vague" argument, never resolved because nobody names the reader. Reviewers grade the document against an executor they imagined. |
| **Already knows** | Either the spec re-explains the stack for 3 000 words, or it assumes context the agent does not load and the agent invents it. |
| **May decide alone** | The agent either asks for approval on trivia (and stalls) or silently makes structural decisions (and drifts). |
| **Must never decide** | Settled decisions get re-opened every session, in good faith, with fresh rationale. The most expensive blank of the six. |
| **Reading order** | The agent loads the largest document first, fills context with detail, and runs out of room before reaching the constraints. |
| **Projection** | The agentic source reaches a human stakeholder and the whole document set is judged unusable on presentation grounds. |

## Placement and maintenance

- **Placement:** immediately after the document control table, before any content. Not in an annex.
- **Repeat it per document** in a set. A document loaded alone must carry its own contract; do not
  rely on the reader having read document 01.
- **Update it when the executor changes.** A hand-off from agent build to human maintenance is a
  change of executor, and it obliges a new projection — not an edit to the source.
- **The contract block is itself `[Proposal]` unless someone with authority set it.** Tag it.
