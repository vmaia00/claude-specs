# Projecting an agentic source for human readers

The agentic document is **source**, not delivery. When a human has to read it — a tech lead, a
stakeholder, a team taking over the build — produce a projection. Do not degrade the source.

Detailed guidance for the human doctrine lives in the `spec-human` plugin. This page covers only the
mechanics of going from an agentic source to a human projection, and the rules for keeping them in
sync.

## The transform, property by property

| In the source | In the projection |
|---|---|
| Uniform depth across all sections | Ruthless selection: what matters, what is decided, what is at risk. Everything else demoted to annex or dropped |
| Exhaustive coverage | Intent plus constraints; the executor fills the rest |
| `[Fact: file:line]` on every claim | Provenance in an appendix, or a single sourcing note per section; keep the tag only where the claim is contested |
| `CT-03`, `HU-04.13`, `O36` inline | Hyperlinks with human-readable labels; the ID in parentheses only if the reader will grep for it |
| Impact and touchpoint matrices | Cut. A senior engineer holds this. Keep at most the diagram |
| Body changelog | Cut to "what changed since you last read this", or move to git |
| Tombstones | Cut, except where a reader is likely to re-propose the retired thing |
| Prescriptive method-HOW (routes, TTLs, indexes) | Cut to the constraint that motivated it ("reads must not serve stale authorisation data"), leaving the method to the team |
| Status labels in headings | A single status line per document, or a status column in one table |

Selection with stated rationale — *why these things and not the others* — is what a human reader
grades the document on. It is optional in the source and mandatory in the projection.

## Rules

1. **The projection is generated from the source, never forked from it.** Two hand-maintained
   documents diverge within one editing round, and then nobody knows which is current.
2. **Name the relationship in both.** Source header: `Projection: agentic source; human projection at
   <path>`. Projection header: `Human-facing projection of <path>`.
3. **The projection may not introduce content.** If the projection needs a fact the source lacks, add
   it to the source with a provenance tag, then regenerate. Otherwise the projection becomes an
   unverifiable second truth.
4. **Length is a design target, not an outcome.** State the target up front (a tech lead reads
   4 000 words; a board reads 800) and select to fit.
5. **Regenerate on every material source edit.** A stale projection is worse than none: the human
   reader believes it.

## When the human is the *executor*, not just the reader

The projection is then not a summary — it is a different specification, and the human doctrine
applies from the first line rather than as a post-process. Do not attempt to reach it by deletion
from an agentic source; the selection and rationale that a human executor needs were never in there
to begin with. Write it for that executor, and keep the agentic source only if an agent will also
build part of the system.

## Observed failure, for calibration

A four-document set of about 152 000 words, correct for its agent executor, was read by a newly
arrived human tech lead. The verdict: too detailed, clearly produced by an agent, sources for
everything, references hard to follow.

None of those findings were wrong, and none of them were defects in the source. They were the
signature of the left-hand column of the doctrine table being read by a right-hand column reader.
The remedy is the projection, not a rewrite of the source.
