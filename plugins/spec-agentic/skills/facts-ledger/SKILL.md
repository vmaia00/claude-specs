---
name: facts-ledger
description: Keep one canonical registry of what is confirmed (LOCKED), what is our own proposal (WORKING) and what is explicitly unconfirmed (OPEN), with a resolvable source citation on every row. Use when tracking confirmed vs assumed facts, answering "what do we actually know", recording client or stakeholder statements, preventing hallucinated requirements from entering a spec, or onboarding an agent to a project's ground truth.
---

# Facts Ledger

A spec that agents execute has one dominant failure mode: an assumption written in the same voice
as a fact. A human reader carries the difference in their head. A fresh agent context cannot —
it cannot distinguish "the client told us this" from "we decided this on a Tuesday". The ledger
externalises that distinction into a single file that is loaded **before** any design,
conceptualisation or recommendation.

## The three states

| State | Meaning | Force |
|---|---|---|
| **LOCKED** | Confirmed by the counterparty, traceable to a source you can open | Immutable constraint. Every design must honour it. Not negotiable by any alternative architecture. |
| **WORKING** | Our own proposal or direction, not yet confirmed | The degree of freedom. Where designs are allowed to differ. Never presented as fact. |
| **OPEN** | Explicitly unconfirmed in the source | A question for the counterparty. Never a fact, never a premise. |

Two hard consequences:

- A design may only constrain itself on LOCKED rows. If a comparison of options is constrained on
  a WORKING row, the comparison is rigged by an assumption.
- The ledger's own WORKING and OPEN rows are **not citable as fact**, including by you, later,
  in the same project. Only LOCKED rows carry a source that survives being questioned.

## Row format and ID scheme

One table per state. IDs are `L__` / `W__` / `O__`, allocated monotonically from a single register,
**never reused**. Use `D__` for decisions that belong to you rather than to the counterparty
(see "Decisions are not facts").

```md
## LOCKED
| ID | Fact | Source (file:line) | Verbatim | Confirmed by | Artefacts affected |

## WORKING
| ID | Proposal | Source (file:line) | Verbatim | Status |

## OPEN
| ID | Open item | Source (file:line) | Marker | Owner / due |
```

Rules that keep the register stable:

- **Promotion keeps both rows.** When the counterparty confirms `W04`, add a new `L13` and leave
  `W04` in place rewritten as a tombstone: `→ LOCKED via L13 (row kept to preserve references)`.
  Deleting the row breaks every document that cites `W04`.
- **Resolution keeps the row.** A closed `O01` stays, struck through, pointing at what resolved it.
- **Sub-IDs for clauses.** A multi-clause fact addresses as `L41·c` so a document can cite the
  exact clause it depends on.
- **Every row carries the affected artefacts.** That column is the impact map: when a LOCKED fact
  is corrected, it names what must be re-edited in the same pass.

## No claim without a source

Every non-trivial statement about the counterparty's system carries one of four labels. They are
not decoration — they are what makes the sentence safe or unsafe to build on.

| Label | Means | Requires |
|---|---|---|
| `[Fact: file:line]` | Confirmed in an allowlisted source | The citation **and** a verbatim quote in the original language |
| `[Inference]` | Derived by reasoning from cited facts | Names the base facts, with their citations |
| `[Assumption — confirm]` | In no valid source | Explicit; must be confirmed before anything is built on it |
| `[Open in source: file]` | The source itself marks it unconfirmed | Quote the marker |

Source markers such as `[!missing]`, "to confirm", "under evaluation", an empty checkbox or a
"current state (draft)" callout mean **not confirmed**. Never resolve one with a plausible guess;
carry it into the ledger as an OPEN row citing the marker.

When torn between LOCKED and WORKING, **downgrade** and say why. A wrongly locked fact is far more
expensive than a wrongly working one: it hardens into every downstream document.

## Absence is not evidence

"X is not mentioned in this source, therefore X does not exist" is an **inference**, never a
finding and never a risk on the register. This rule exists because it was violated: a real audit
concluded a client had no oversight of a process because a rules document did not list it — while
that rules document was itself an unconfirmed proposal by the consultant, not a description of the
built system. The omission proved nothing about reality.

Before deducing anything from an absence, check whether the silent document is itself a primary
source or your own generated analysis. If it is your own analysis, the absence proves only that
you never wrote it down. Label any absence-derived claim `[Inference — confirm]` and route it to
the counterparty as an OPEN row.

## Declare the source allowlist

The ledger only works if the project states, in writing, which paths count as primary sources and
which do not. Put this at the top of the ledger or in the project instructions file:

```md
## Valid sources (the only paths citable as fact)
- `vault/**` — the counterparty's own system documentation, EXCEPT `vault/analysis/**`
- `discovery/NN-*.md` — statements made by the counterparty in recorded sessions
- `meetings/**` — raw and derived meeting records, dated
- `vendor-api-map/**` — citable ONLY as vendor capability ("what the published API offers"),
  never as a statement about this counterparty's configuration. Label such citations
  `[vendor-capability — not their config]`.

## Never citable as fact
- `vault/analysis/**` and every other artefact we generated ourselves
- the ledger's own WORKING and OPEN rows
- model knowledge, the open web, and assumptions made earlier in a conversation
```

The scoped-capability entry is worth copying. Vendor documentation tells you what a product *can*
do; it says nothing about how this particular instance is configured. Conflating the two is the
most common way a false fact enters a spec.

## New facts are reconciled, not appended

A new fact is never pasted into the table. Run the ritual:

1. **Verify the source.** No allowlisted source, no lock — record it OPEN and say what source is
   needed. Delegate verification to a read-only checker rather than doing it inline.
2. **Load the ledger** and any live designs.
3. **Test compatibility** with every existing LOCKED row and every live design: compatible /
   silent (name the minimal extension) / conflicting (name exactly which components must change).
4. **Promote or reject.** Only now does the row become LOCKED, with citation, verbatim, confirmed-by
   and date. If it confirms a WORKING row, promote and tombstone.
5. **Log the reconciliation** — date, ID, source, compatible designs, designs needing rework,
   outcome. The log is what lets a later reader see why a fact locked, not just that it did.

Full procedure and log format: [references/intake-ritual.md](references/intake-ritual.md).
Copy-paste starting ledger: [references/ledger-template.md](references/ledger-template.md).

## Decisions are not facts

Split authority on two axes and keep them apart:

- **The WHAT** — scope, business rules, policy, risk acceptance — belongs to the counterparty.
  Confirmed, it becomes LOCKED.
- **The HOW** — architecture, stack, infrastructure, contract shape — is yours. Record it as a
  `D__` decision with a date and a rationale. It **never becomes LOCKED**, because nobody external
  confirmed it, and it is never presented as a counterparty fact. It is still binding on the build
  until reopened by new evidence.

An agent reading `D07` knows it may argue with it. An agent reading `L07` knows it may not. That
is the entire value of the separation.

## Worked rows

```md
## LOCKED
| **L07** | The ERP stays; no ERP replacement is in scope. | `meetings/2026-03-11-scope-call.md:43` | "the ERP stays — non-negotiable; there is no ERP change" | Client sponsor, 2026-03-11 | architecture, integration surface, scope statement |

## WORKING
| **W12** | ERP writes go through the published API with a human-in-the-loop draft step; never direct SQL. | `analysis/erp-access-topology.md:69-106` | "Writes: API with HITL draft. Never write via direct SQL." | Our direction. The *principle* promoted to L13 (2026-03-20); only the **mechanism** (which API, auth, SLA) stays WORKING. |

## OPEN
| **O04** | Authentication for the tax-authority channel: client certificate vs. username + password. | `vault/INT - TaxAuthority.md:33-34` | `[!missing]` | Client IT · due 2026-04-30 · as-built leans to the second option (`discovery/08-portal-at.md:9`) |
```

## Checklist before you build on the ledger

- Every LOCKED row has a citation you can open and a verbatim quote.
- No design constrains itself on a WORKING row.
- No claim in any deliverable is unlabelled.
- No absence has been reported as a finding.
- Every promotion left a tombstone; no ID has been reused.
