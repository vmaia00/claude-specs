# The three touchpoint matrices

Entity cards map the model's interior. The matrices map the seams between the data model and the
functional spec, which is where an agent editing one document breaks the other. Measured cost in the
worked example: 1 008 lines for the three, on top of 1 337 lines of cards.

Build them only if the decision test in the skill body puts you in the top band. Reuse the **same
field layout as the cards** — the agent should parse one shape across the whole annex.

## Matrix 1 — state machine → entities

One block per state of the central domain object. Answers: in this state, what exists, what is still
null, what may write, what the user sees.

```md
**`S2 held-for-sender-approval`** · writer: receivers (P2) + write-back CT-15 via worker

- **Outbound FKs:** (none: in S2 only the waiting-room item exists, and its DocumentId is null)
- **Referenced by:** the held waiting-room projection read by EC-09
- **Logical references (non-FK):**
  - Item.SenderState enum approved · pending · revoked · blocked (defined in the intake spec §5.3)
  - ClientId required; CompanyId nullable (sender not yet resolved to a company)
- **Invariants touching it:** I-9 single clock on the hold (ExpiresAt, stops on decision) · I-1 tenant key at entry
- **States · jobs · screens:** job `sender-approval-escalation` · EC-09 management · projection "pending your approval"
- **If it changes, re-check:**
  - CT-15 write-back and the terminal rejected-at-source state
  - the reconciler TTL and the degraded path
  - open items O98 (TTL) · O101 (blocked senders) still unresolved
  - the S2 -> expired edge is not yet formalised in the state matrix
```

Why an agent needs it: the most frequent state-machine defect is writing a field on an entity that
does not exist yet in the state being handled. The "outbound FKs: none, because in this state X does
not exist" line prevents exactly that, and it is invisible from both the schema and the state
diagram.

**Generation:** the state list comes from the functional spec's state-machine section; entity
membership per state comes from the physical model plus the nullability rules. Hand-write only the
`if it changes` bullets.

## Matrix 2 — scheduled jobs → entities

One block per job. Jobs write rows that no screen explains, so they are the least discoverable
writers in the system.

| Field | Content |
|---|---|
| Job id and trigger | name, schedule or event, concurrency limit |
| Reads | entities and the filter that selects rows |
| Writes | entities and columns, plus the state transition it performs |
| Must not touch | entities it may read but never write |
| Idempotency key | what makes a re-run safe |
| Failure path | retries, backoff, dead-letter, redrive procedure |
| If it changes | contracts, states and screens that observe its output |

State the **must not touch** line even when it feels obvious. An agent extending a job to "also
update the summary" is the single most common way a second writer appears.

## Matrix 3 — screens → API routes → entities

Three columns, end to end, one row per screen action.

| Screen | Action | Route | Entities read | Entities written | Authorisation | Contract |
|---|---|---|---|---|---|---|
| EC-09 management | list pending senders | `GET /api/management/pending-senders` | WaitingRoomItem | — | capability `approve-sender` | CT-15 |
| EC-09 management | approve sender | `POST /api/management/senders/{id}/approve` | WaitingRoomItem, CapabilityGrant | WaitingRoomItem, AccessChangeLog | capability `approve-sender` | CT-15 |
| EC-04 send receipt | fetch receipt | `GET /api/submissions/{id}` | Submission, SubmissionItem, Document | — | owner or capability `view-submissions` | CT-02 |

Answers, without loading the front end: which screens break if a route changes; which routes touch an
entity; whether any route writes an entity outside its declared writer.

**Generation:** rows derive from the contract set (routes, payload anchors) joined to the screen
inventory in the functional spec. The authorisation column derives from the access matrix. Only the
join is manual, and it is worth automating first — it is the matrix that goes stale fastest.

## Aggregate view

Precede the matrices with three or four lines of aggregate counts from the anchor graph — the
most-cited entities and the most-cited spec sections, with counts. In the worked example this
immediately showed the coupling concentrated in the authorisation section and the primary API
surface, which is exactly the information an agent needs before proposing a change there.

```md
Most-cited targets: Document.Version (16) · Document.DeclaredType (15) · CapabilityGrant (15).
Most-cited spec sections: §8.1 (394) · §7.7 (193) · §9.5 (114) · §5.8 (97).
```

## Keeping them honest

- **Generated from source, regenerated in the same edit** that changed the source.
- **Precedence rule stated once for the whole annex**: on divergence, the model section and the
  contract set prevail; the matrix is corrected.
- **Coverage stated when partial.** "Matrix 3 covers the 18 screens of phase 1; phase 2 screens are
  not yet mapped" is usable. Silent partial coverage is not.
- **Cut a matrix that nothing references.** If no `if it changes, re-check` bullet and no session
  ever pointed at matrix 2, it is 300 lines of weight. Delete it and note the removal.
