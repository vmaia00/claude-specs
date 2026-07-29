# Intake ritual — reconciling a new fact

The ledger is append-*reconciled*, never append-only. A fact arriving from a meeting, a document or
a call is an event that must be tested against everything already locked before it is allowed in.

## Procedure

### 1. Verify the source

A fact locks only if it traces to an allowlisted source: a dated meeting record, a discovery note,
a counterparty document, or a vault statement explicitly grounded in one of those.

Run the verification with a **read-only** checker (the `spec-auditor` agent, or a dedicated
fact-checker), passing it the claim plus the stated source. Do not verify inline in the same
context that wants the fact to be true.

If no valid source is produced: **stop**. Record the item as OPEN, state exactly what source would
close it, and tell the requester. Do not lock on the strength of someone remembering the meeting.

Common near-misses that are *not* sources:

- A decision document of your own marked "confirmed" — check *whose* decision it records. Your own
  approval of your own proposal is not counterparty confirmation.
- A screenshot or as-built artefact from a system built by a third party. It is evidence of what
  exists, not of what was decided or required. Label it as as-built, keep it OPEN.
- Vendor documentation. Capability, not configuration.

### 2. Load context

Read the whole ledger. Load every live design or option set that could be affected. A fact cannot
be reconciled against documents you have not opened.

### 3. Compatibility check, per design

For each live design, classify:

| Verdict | Meaning | Action |
|---|---|---|
| **Compatible** | The design already assumes or permits the fact | Tag it as honouring the fact; cite the ID |
| **Silent** | The design does not address it | Note the minimal extension needed; do not rewrite |
| **Conflicting** | The design contradicts the fact | Flag for targeted rework, naming exactly which components or choices must change |

A single new LOCKED fact can invalidate an entire design. That is the expected cost of having
options, not an accident. Say so plainly rather than softening the finding.

### 4. Promote

Add the row to the LOCKED table with:

- statement, in the project's working language;
- `file:line` **and** a verbatim quote in the original language — never a translation;
- confirmed-by and date;
- affected artefacts (this column is the impact map for the correction pass).

If the new fact confirms a WORKING row, move it and leave a tombstone in the WORKING table:

```md
| **W04** | Context reads via read-only SQL. | `analysis/erp-access-topology.md:66` | "context reads … read-only SQL" | → **LOCKED via L13** (2026-03-20). *(row kept to preserve references)* |
```

If the fact only confirms **part** of a WORKING row, promote the part and say which part stays
working. Partial promotions are the normal case and the most frequently botched one.

### 5. Log the reconciliation

Append to a log table at the foot of the ledger:

```md
| Date (tag) | What changed | Source | Compatible | Needs rework | Outcome |
|---|---|---|---|---|---|
| 2026-03-20 (#erp-access) | **+L13** — writes via API only, reads read-only; W03/W04 partially promoted | `meetings/2026-03-20-erp-access.md:27` | designs A, C | design B (direct-write path) | +L13 · W03 reduced to mechanism · W04 tombstoned |
```

The log answers "why is this locked?" months later, when the meeting is forgotten and only the row
survives.

## Corrections to an existing row

Facts get corrected. Two kinds, and they are not the same:

- **The fact was wrong.** Rare. Strike the statement, add the correction inline with its own date
  and source, and re-run the compatibility check — a correction is a new fact.
- **An annotation on the fact was wrong.** Common. The fact stands; a note you attached to it
  (a design implication, a scope reading) was mistaken. Correct the annotation, preserve the
  original in the record, and state explicitly that the fact's state did not change. Never let an
  annotation correction masquerade as a state change.

Both cases must list the deliverables to fix in the same pass. A corrected row with no fix list is
a silent inconsistency waiting to be built.

## Anti-patterns

- **Intake for your own proposals.** The ritual is for facts confirmed by the counterparty. Your
  own ideas stay WORKING; running them through intake launders them into facts.
- **Locking from conversation.** "We agreed on the call" with no dated record is OPEN, not LOCKED.
  Ask for the note; lock when it exists.
- **Silent deletion.** A row removed rather than tombstoned breaks every citation to it and hides
  the history that justified the removal.
- **Backfilling a citation.** If you cannot find the line, the claim is not a fact yet. Do not
  point the citation at the nearest plausible paragraph — a citation that resolves to the wrong
  content is worse than no citation, because verification passes.
