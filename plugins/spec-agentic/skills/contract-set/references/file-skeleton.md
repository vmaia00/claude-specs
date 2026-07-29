# Contract file skeleton and set-wide conventions

Every file in the set is OpenAPI 3.1 and follows the same skeleton. Uniformity is not tidiness: it
is what lets a verifier check the set mechanically and an agent read any file without re-learning
the layout.

## Skeleton

```yaml
openapi: 3.1.0
info:
  title: docs.intake — document intake and drain
  version: 0.9.0-working          # SemVer per contract; -working until it is ready to specify
  x-status: WORKING               # our design; not agreed with the counterparty
  x-provenance:                   # pure audit; stripped at publish time
    - Doc6 · Document.SenderState (l. 341)
    - Doc5 §6.4 (l. 646-747)
  x-decision:                     # a decision taken where the source left room
    - id: D-INTAKE-2
      choice: One drain endpoint per channel, not one polymorphic endpoint.
      origin: engineering         # stripped at publish
      source: Doc5 §6.4 (l. 646)  # stripped at publish
  x-open:
    - "[Open: O61] the three-group sender model is unconfirmed source material"
paths: {}
components: {}
```

`x-decision.choice` survives publication. It is the "why" behind a shape and the most useful content
in the set for whoever builds against it. Only the decision's *provenance* is audit trail.

## Extension vocabulary

| Extension | Carries | Published? |
|---|---|---|
| `x-provenance` | the anchor list for every claim in the file | no — pure audit |
| `x-decision` | engineering decisions where the source left room | yes (choice only) |
| `x-status` | file-level status of the contract | yes |
| `x-gated` / `x-gate` | what blocks a route or field, quoted verbatim | yes |
| `x-open` | open points declared in the file itself, tagged | yes |
| `x-out-of-scope` | declared-but-not-specified siblings, so nobody assumes they were forgotten | yes |
| `x-authorization`, `x-idempotency`, `x-concurrency`, `x-telemetry`, `x-step-up` | per-route behavioural notes | yes |

Tag every open point with its class: `[Open: Oxx]` (waiting on the counterparty),
`[Proposal — engineering]` (ours, decided), `[Inference — confirm]` (derived, unverified). The class
tells a reader whether they may argue with it.

## Gating

```yaml
  /clients/{clientId}/indicators:
    get:
      summary: "[GATED SP-1] Financial indicators"
      x-gate: "gated on SP-1/O51 — the data path for indicators is undecided"
      responses:
        "200":
          description: >
            Envelope is field-level. While the gate is closed, gate.available=false and
            values travel null. The shape does not change when the gate opens.
```

Rules:

- A whole gated surface answers `501` with a stable code (`gate-closed`), defined once in `common/`.
- A gated field is typed but null or absent — never a placeholder value, never a sample that looks
  real.
- Prefer `gate.available=false` with null values over `501` when the *envelope* is settled and only
  the content is blocked. Changing the status code when a gate opens is a breaking change; changing
  a null to a value is not.
- Quote the gate **verbatim** from its source. A paraphrased gate drifts into a different gate.

## Set-wide route conventions

Declare these once, in the set README, and enforce them in review:

- **Tenant always from the session, never from the payload.** A tenant id in a request body is a
  privilege-escalation bug waiting for a careless handler.
- **Authorisation per object, in the repository layer** — not in the route handler, where it is
  forgotten on the second route that touches the same object.
- **Cursor pagination, mandatory.** No unbounded collection reads. Append-only logs with unbounded
  retention additionally require a mandatory bounded `from`/`to` window, so no single read equals a
  full scan.
- **`Idempotency-Key` on every creating POST.**
- **`If-Match` carrying the resource version on every updating write.**
- **Binaries only via signed URL**, minted by a dedicated `POST …-url` route, short TTL, bound to
  session and tenant, excluded from telemetry.
- **One language convention for field names**, chosen from the implementation language, applied to
  the whole set. Verbatim source names in another casing get converted — but error *code values*
  stay verbatim, because they are strings, not identifiers, and renaming them costs compatibility
  for no gain.

## `additionalProperties`

Use `additionalProperties: false` on **request** schemas only. On responses it contradicts an
additive-only minor policy and breaks consumer-driven contract tests the first time the producer
adds a field. This is a real, repeatedly made mistake; check for it explicitly in review.

## Numbering and retirement

- Contract numbers come from the set's single register. A **reserved** number stays reserved: the
  next contract takes the next free number, not the reserved one.
- A withdrawn addition keeps its number as a tombstone — *"additive 8 withdrawn, number reserved,
  do not reuse"* — with a one-line reason, so nobody reopens the discussion by accident.
- Naming a contract after a capability (`archive.read`) rather than a system keeps the name valid
  when the system behind it is replaced.

## Contracts that are declared but not specified

List them, with their gate quoted, in the README. A contract that exists in the architecture but is
not specified in the set must be visible as *deliberately absent*, otherwise the build team assumes
it was overlooked and either invents it or blocks on it.

| Contract | Status | Gate (verbatim) |
|---|---|---|
| `capability/archive.custody` | not specified | "v1, two legs (see 3.6)" |
| `capability/vault.broker` | not specified | "v1. Exposed components have no access" |
| `capability/payroll.*` | reserved namespace | "v0 · phase 2, on top of the payroll as-is already surveyed" |

Re-check this table at every increment boundary. The first not-specified contract that the build
actually needs is a schedule risk, and it is visible here weeks before it bites.
