# Prescription to constraint: a rewrite catalogue

Use with the sorting test in `../SKILL.md` §2. Each entry: the prescriptive form, the constraint
form, and what was returned to the team.

## API surface

| Before | After | Returned to the team |
|---|---|---|
| "Expose `GET /v1/documents?status=&page=&size=` returning `{items, total, cursor}`." | "The document list must be reachable by an authenticated client filtered by state and paginated with a stable total order; the response shape is fixed by contract `CT-xx` and may not diverge from it." | Path, verb naming, query parameter names, page size defaults |
| "Return 409 on duplicate submission with body `{code: DUPLICATE}`." | "A duplicate submission must be distinguishable by the caller from a rejected one without parsing free text, because clients retry on transport failures and must not retry on duplicates." | Status code choice, error envelope, code vocabulary |
| "Version the API by URL prefix." | "A breaking change must not reach a client that did not opt into it; consumers already in production keep their contract until they migrate." | URL vs header vs media-type versioning |

## Data

| Before | After | Returned to the team |
|---|---|---|
| "Add `UNIQUE (tenant_id, external_ref)`." | "One inbound document delivered twice yields one record, enforced where concurrent writers cannot race past it." | Unique index vs upsert vs dedupe at the queue |
| "Soft-delete with `deleted_at` and filter in every query." | "No record subject to a retention obligation may be physically removed before its retention period ends, and deleted records must never appear in user-facing reads." | Soft delete, archival table, partition rotation |
| "Store money as `DECIMAL(18,4)`." | "Monetary values must round-trip without loss at the precision the system of record uses; a value written and read back must compare equal." | Type and precision choice, currency handling |
| "Denormalise the client name onto the document row." | *(No constraint — pure method.)* | Everything. Evict to an ADR. |

## Identity, authorisation, tenancy

| Before | After | Returned to the team |
|---|---|---|
| "Check `req.user.tenantId === row.tenantId` in each handler." | "No request may read or write data outside its tenant, and the check must be impossible to omit by adding a new endpoint." | Middleware, row-level security, repository layer, policy engine |
| "Sessions expire after 30 minutes idle; refresh tokens rotate." | "A stolen session artefact must stop being useful within the hour, and reuse of a rotated credential must be detectable." | Durations within that bound, token format, storage |
| "Passwords: bcrypt cost 12." | "Stored credentials must be unrecoverable from a database dump using a memory-hard or deliberately slow verifier with a per-record salt." | Algorithm and parameters, migration path |

## Storage and transport

| Before | After | Returned to the team |
|---|---|---|
| "Presigned PUT, 5-minute TTL, key `intake/{tenant}/{uuid}`." | "Uploads must not transit the application server and the authorisation must expire in minutes; a leaked long-lived URL is an unauthenticated write path into the intake store." | Signing scheme, TTL within minutes, key layout |
| "Object storage bucket per environment with lifecycle rule at 90 days." | "Environments must not be able to read each other's objects, and objects in the staging area must not accumulate indefinitely without an owner." | Bucket topology, lifecycle mechanics, retention window if none is mandated |
| "All traffic over TLS 1.3 with HSTS preload." | "No credential or document content may traverse a network in cleartext, including internal hops." | Version floor above the minimum, header policy, certificate management |

## Operations and scale

| Before | After | Returned to the team |
|---|---|---|
| "Cron every 5 minutes reconciling pending documents." | "No document may remain in a pending state indefinitely without either progressing or raising an alert; staleness must be observable without a human going to look." | Polling vs events, interval, worker topology |
| "Redis cache, TTL 300s, key `doc:{id}`." | "Cached reads must never serve data that contradicts an authoritative write already acknowledged to the same user." | Cache technology, TTL, invalidation strategy, or no cache at all |
| "Two app instances behind the load balancer." | "A single instance failure must not take the service down, and a deploy must not require a service window." | Instance count, orchestrator, deploy mechanics |
| "Log to stdout in JSON with `traceId`." | "Any user-reported failure must be reconstructable from logs alone, end to end across components, without reproducing it." | Format, transport, retention beyond the audit floor |

## Signals that a statement is method, no matter how it is phrased

- It names a product or library ("Redis", "Kafka", "Prisma") without a compatibility obligation.
- It carries a number that could move 2x either way with no consequence you can name.
- It describes a file, folder, class or module layout.
- It sequences steps ("first do A, then B") where only the end state matters.
- It would need editing if the team changed language or framework — while the requirement would not.

## Signals that a statement is a constraint even though it looks like method

- Another party's code, a contract file or a schema depends on it verbatim.
- Removing it makes a failure silent instead of loud.
- It is the only thing preventing a duplicate, a lost write or a cross-tenant read.
- It exists because of a rule imposed from outside the project.
- It was the outcome of an incident, an audit finding or a negotiated commitment.
