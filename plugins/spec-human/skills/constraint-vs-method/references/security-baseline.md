# Keeping the baseline through the cut

The security and scalability baseline is the material most likely to be lost when a spec is trimmed,
and the least likely to be missed on the day it is lost. Treat its survival as a separate pass, run
after the general cut, not as a by-product of it.

## Why it goes first

1. **It looks like the thing being removed.** Controls, limits, headers, boundaries: prescriptive in
   form, indistinguishable at a skim from route tables and TTLs.
2. **Its value is counterfactual.** Nothing gets slower, later or uglier when it is deleted. The
   document simply gets shorter and the reader feels better.
3. **Costs are immediate, benefits are deferred and invisible.** Every control is work in week one
   against an incident that may be in year two, or never, or already happening undetected.
4. **It has no advocate.** Feature owners lose nothing. The only person who loses is the author, and
   the author is the one being asked to cut.

## The baseline in constraint form

State each item as an outcome with a failure mode. This is what makes it defensible; a control
listed as a product name is a shopping list and gets cut as one.

| Area | Constraint (outcome) | Consequence if violated |
|---|---|---|
| Ingress | All public traffic enters through one controlled boundary that can refuse a request before application code runs | Every endpoint becomes its own security perimeter, and the weakest one defines the system |
| Rate limiting | No unauthenticated caller can consume the request budget of others, and the limit cannot be bypassed by choosing another route | One client, hostile or merely buggy, causes an outage; first symptom is downtime, not an alert |
| Authentication boundary | No route serves data without establishing identity, and adding a route must not be a way to forget | Silent unauthenticated data exposure that no test will find |
| Authorisation | Identity established is not sufficient; every access is checked against what that identity may see | Authenticated users read each other's data; classic and reliably present |
| Tenancy isolation | No request may cross a tenant boundary, enforced somewhere a new endpoint cannot skip | Cross-tenant leak, the single most damaging class in a multi-client product |
| Credentials at rest | Stored credentials are unrecoverable from a database dump | One dump ends the product's credibility |
| Secrets | No secret in source control, in an image, or in a client-side artefact; rotation possible without a redeploy of everything | A leaked non-rotatable secret is a permanent breach |
| Transport | No credential or document content traverses any network in cleartext | Interception on internal hops, which nobody monitors |
| Availability | A single instance failure does not take the service down; deploys need no service window | Planned downtime becomes normal; unplanned downtime becomes long |
| Observability | Any reported failure is reconstructable from logs alone, end to end | Incidents are diagnosed by guesswork and reproduce in production |
| Audit | Actions with legal or financial effect are attributable to an actor and a time, and the record cannot be edited by the actor | Nothing to show an auditor, and no way to answer "who did this" |

None of these names a product, a version, a threshold or a vendor. All of those are method, and all
of them belong in ADRs.

## Handling the pushback

A team asking for less prescription is usually not asking for less security. Separate the two
explicitly:

- Lead with the failure mode, not the control. "An unauthenticated write path into the intake store"
  is arguable on merits; "use presigned URLs" is arguable on taste.
- Offer the method back. "The constraint stays; how you meet it is yours, and the ADR records what I
  would have done and why, as input, not instruction."
- Where a team declines a baseline item anyway, that is a legitimate outcome of a decision that is
  theirs to make, and it is recorded as an **accepted risk** with a named owner and a date. Not as a
  quiet deletion. A baseline item that disappears from a document with no record is the only failure
  mode here that cannot be recovered later.

## Placement in a human-facing set

- One section, near the end, self-contained, headed as a baseline and marked non-negotiable where it
  genuinely is.
- Outcome per line, failure mode per line, no product names.
- Every method detail behind it in ADRs, linked once from the section head.
- Short. A baseline that runs to many pages is being read as method again and will be cut again.
