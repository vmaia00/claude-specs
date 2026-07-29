---
name: constraint-vs-method
description: Separate binding constraints from advisory method when a spec is told "what and why, not how". Use when trimming a spec for a human team, when a team asks for less prescription, when deciding what stays binding and what becomes a recommendation, when protecting a security or scalability baseline while simplifying, or when converting prescriptive instructions into constraints with stated failure modes.
---

# Constraint or method

"What and why, not how" is nearly right, and lethal if taken literally. Applied without a sorting
rule it deletes the API contracts, the data invariants and the security baseline in the same pass as
the cache TTLs, because to a reader skimming for prescription they all look identical.

The rule is not *drop the HOW*. It is: **the HOW is two things, and only one of them is negotiable.**

## 1. Two kinds of HOW

**Constraint-HOW — binding.** Statements that, if the team decides otherwise, break correctness,
safety, interoperability, or a commitment already made to someone outside the team.

- API and event contracts (someone else already codes against them)
- Data invariants: uniqueness, idempotency, ordering, referential rules
- State authority: which component owns which transition, and who may not
- The security and scalability baseline: authentication boundaries, authorisation checks, secret
  handling, rate limiting, ingress controls, tenancy isolation
- Retention, audit and traceability obligations
- Anything a regulator, an auditor or a counterparty relies on

These **stay**. Phrase each as **constraint + rationale + consequence-if-violated**, never as a
step-by-step instruction. A constraint with a named failure mode survives review; an instruction
with only a preference behind it invites negotiation and loses.

**Method-HOW — advisory.** Route tables, cache TTLs, index choices, cron and job inventories, file
and folder layout, library and framework selection, class decomposition, queue topology, naming.

A competent team supplies these better than a spec author can, because they hold the code. These are
**evicted** to ADRs, where they read as a recommendation with reasoning instead of an order.

**Eviction is not deletion.** Every method-HOW removed from the spec lands in an ADR with its
rationale intact. If it is worth removing and not worth recording, it was not worth writing.

## 2. The sorting test

Run it on every prescriptive statement, one at a time.

> **If a competent team does this differently, does something *break*, or does it merely *differ*?**
>
> - **Breaks** → constraint-HOW. Keep it, and state the failure mode in the same sentence.
> - **Differs** → method-HOW. Move it to an ADR as a recommendation.

"Breaks" is not a feeling. It qualifies only if you can name at least one of:

1. a contract another party already implements against, violated;
2. data lost, duplicated or corrupted, or an invariant broken;
3. an attack path opened, or an agreed control removed;
4. an obligation to a regulator, auditor, customer or counterparty made unmeetable;
5. a capacity or availability commitment made unreachable.

**Second-order guard.** If you cannot write the failure mode in one sentence, it is method. Wanting
it is not the same as needing it, and the spec is not the place to spend authority on preference.

**Tie-breaker for the ambiguous middle.** Some choices break only *in combination* with another
choice. Then the constraint belongs to the **pair**, not to either part. Write one constraint that
names both and leave each part free.

> Cursor pagination and at-least-once event delivery are each fine alone. Together, without a stable
> total sort key, consumers silently skip records under concurrent writes. The constraint is: *any
> paginated feed that is also replayed must have a stable total order.* Neither the cursor design nor
> the delivery semantics is dictated.

**Do not paraphrase a contract.** A contract file is itself the constraint. The spec points at it by
identifier and states what depends on it. Prose restatements drift from the file and then two
authorities exist.

## 3. Rewriting prescription as constraint

Four patterns. The binding force is unchanged; the method is returned to the team.

**Upload path**

> Before: "Use a signed URL issued by the BFF with a 5-minute TTL and store the object under the
> intake bucket prefix."
>
> After: "Uploads must never transit the application server, and an upload authorisation must expire
> in minutes, not hours, because a leaked long-lived URL is an unauthenticated write path into the
> intake store."

**State authority**

> Before: "The ingestion worker sets `status = accounted` once the ERP call returns 200 and writes an
> audit row with the returned document number."
>
> After: "Exactly one component may move a document into an accounted state, and no document may
> reach that state without a recorded external reference. If two components can set it, reconciliation
> against the system of record has nothing to appeal to and duplicates become undetectable."

**Rate limiting**

> Before: "Configure the gateway at 100 requests/minute per IP, returning 429 with `Retry-After`."
>
> After: "Every public endpoint must sit behind a limit that an unauthenticated caller cannot bypass,
> enforced before application code runs. Without it, one client exhausts the request budget for every
> tenant, and the first symptom is an outage rather than an alert."

**Idempotency**

> Before: "Add a UNIQUE index on `(tenant_id, external_ref)`."
>
> After: "The same inbound document delivered twice must produce one record, enforced where
> concurrent writers cannot race past it. A retried webhook that creates a second entry costs more to
> detect downstream than to prevent at the write."

More rewrites, by domain: [references/rewrites.md](references/rewrites.md).

## 4. Authority is exercised through constraints

Where an architect holds decision authority over the technical design by agreement, "what and why,
not how" **does not revoke that authority**. It changes its *form*.

- Authority expressed as instruction: "do it this way." Reads as distrust, gets argued, and is
  frequently right for reasons the reader cannot see.
- Authority expressed as constraint: "this must hold, because otherwise X fails." Same binding force,
  legible reason, and the team keeps the design work that is genuinely theirs.

Say this out loud when accepting the feedback. It is the argument that lets a spec author take the
criticism in full without surrendering the baseline: *the prescription goes, the constraints stay,
and here is the failure mode behind each one that stays.* A team that rejects a constraint after
reading its failure mode is making a risk acceptance, and that is a decision to record, not an
editing choice.

## 5. What a careless cut destroys first

**The security baseline evaporates first.** It is the most vulnerable material in the document:

- it looks *exactly* like gratuitous prescription — controls, headers, limits, boundaries;
- its value is counterfactual, so nothing visibly worsens on the day it is cut;
- its cost is paid on day one and its benefit arrives on the bad day;
- and it has **no advocate in the room** — no feature owner loses anything by its removal.

Next in line, for the same reason: state authority (reads as an implementation detail), invariants
(read as database trivia), retention and audit rules (read as bureaucracy).

**Rule: never cut by pattern-match.** Do not delete a block because it "looks like implementation
detail". Run the sorting test on it explicitly and record the outcome. Anything that survives as a
constraint gets its failure mode written; anything that does not moves to an ADR.

Keeping the baseline intact while cutting hard:
[references/security-baseline.md](references/security-baseline.md).

## Checklist

- [ ] Every prescriptive statement classified: constraint or method, none left unsorted
- [ ] Every retained constraint carries a rationale and a named consequence-if-violated
- [ ] No retained constraint dictates a mechanism where an outcome would do
- [ ] Contracts referenced by identifier, never paraphrased into prose
- [ ] Every evicted statement landed in an ADR with its reasoning, not deleted
- [ ] Combination constraints written on the pair, with each part left free
- [ ] Security and scalability baseline re-read after the cut, as its own pass
- [ ] Any constraint the team rejects recorded as an accepted risk, with an owner

## Related

- `adr` — where evicted method-HOW lands, with its `binding vs recommendation` field.
- `sample-chapter-first` — validates the cut with the real reader before the set is generated.
- `tech-lead-reader` agent — flags prescription overreach using this sorting test.
