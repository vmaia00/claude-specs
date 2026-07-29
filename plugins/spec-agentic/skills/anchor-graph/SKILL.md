---
name: anchor-graph
description: Reference across documents by stable named anchors and IDs instead of line numbers, and verify the whole set with a CI gate. Use when cross-references between specs break as documents are edited, when you need "reference by name, not line number", when fighting link rot in a spec set, when building a traceability graph, or when checking that a document set is internally consistent before calling it final.
---

# Anchor Graph

A spec set that agents execute is a graph, not a stack of documents. The edges are cross-references.
If the edges rot silently, the set keeps looking correct and stops being correct — and an agent,
unlike a human reviewer, will follow a rotten edge without noticing anything is wrong.

Two mechanisms keep the graph honest: **anchors that survive editing**, and **verifiers that fail
the build when one does not resolve**.

## Line numbers rot; names do not

A citation of the form `Doc6:289` is dead the moment `Doc6` gains a paragraph above line 289. It
does not fail loudly — it silently points at different content, and verification then *passes*
against the wrong text.

This is not theoretical. In one spec set, three source documents shifted in a single day (+10, +3
and +94 lines). By the third shift there was no intermediate state left from which to reconstruct
the offset, and every numeric citation into those documents had to be re-anchored by hand. What
survived was re-anchoring **by content**: citations that named an entity and a field were
repairable by machine; citations that carried only a number were not.

**Rule: the name is the anchor, the line is a hint.** The hint is convenient for humans and is
auto-repaired by the verifier when it drifts. The name is what resolves.

### Token grammar

Pick one grammar for the whole set and never mix in a second. A working one:

```
Doc6 · Entity.Field (l. 289)       a field of an entity
Doc6 · Entity (l. 280-313)         a whole entity, or prose inside it
Doc6 §3.7 Group G (l. 715-793)     a named group spanning several tables
Doc5 §6.4 (l. 644)                 a prose section
Doc5 · US-04.2 (l. 673)            a user story
Doc5 · «short verbatim text» (l. 123)   no nameable anchor: quote the text
```

Notes that matter in practice:

- The parenthesised line is **never** the anchor. State this in the set's README, or someone will
  "fix" a stale hint by editing the name.
- Use angle quotes (or another delimiter absent from your file format) for verbatim anchors.
  Straight quotes break YAML scalars that are already quoted.
- Prose forms that already name the source ("Doc 3, section 3.3") are fine; teach the verifier to
  confirm that the section exists.

## ID families

One prefix per artefact kind, allocated from a single register:

| Family | Kind | Example |
|---|---|---|
| `CT-` | capability contract (a downstream interface) | `CT-08 match.suggest` |
| `SC-` | screen | `SC-03 Send` |
| `EP-` | epic | `EP-02 Submit a document` |
| `US-` | user story | `US-04.2` |
| `PR-` | design principle | `PR-1 nothing disappears` |
| `L/W/O/D` | ledger rows (see the `facts-ledger` skill) | `L13`, `W22`, `O72` |

Allocation rules:

- **Never reuse a retired number.** A withdrawn item leaves a tombstone: *"additive 8 withdrawn —
  number reserved, do not reuse"*. Reuse turns every historical citation into a false positive,
  which is worse than a dangling one because it resolves.
- **A reserved number stays reserved.** If `CT-11` is reserved but unassigned, the next contract
  takes `CT-19`, not `CT-11`. A reserved number is not occupied in passing; only the register's
  owner assigns it.
- **Sub-IDs are addressable.** `US-04.2`, `L41·c`. Cite the clause you actually depend on so a
  change to a sibling clause does not invalidate your citation.
- **One register file** lists every allocated, reserved and retired ID with its status. If the
  register lives in two places, neither is authoritative.

## The anchor graph

Generate a JSON map of which file cites which target, inverted (target → citing files, with
counts). It is cheap — one regex pass over the set — and it buys three things you cannot get by
reading:

- **Orphan detection.** A declared ID that nothing cites is either dead weight or a missing link.
  A cited ID that nothing declares is a dangling edge.
- **Impact preview.** Before editing a target, list its citers. This is the difference between
  "I changed an entity" and "I changed an entity that 14 contract files depend on".
- **Safe rename.** Rename the target, then re-run the graph and confirm the citer set is identical.

```python
# anchor -> {file: count}, inverted and sorted by traffic
PAT = re.compile(r"Doc(\d)\s*(?:·\s*([\w.\-]+)|§\s*([\d.\w ]+?))\s*\(l\.\s*[\d\-, ]+\)")
edges = defaultdict(lambda: defaultdict(int))
for path in files:
    for m in PAT.finditer(read(path)):
        target = f"Doc{m[1]} · {m[2] or '§' + m[3].strip()}"
        edges[target][path] += 1
```

Commit the generated map, or regenerate it in CI and diff. Either way it must be reproducible.

## The verifiers are a CI gate

Two checks. Neither is optional, and **no document is called final before both pass**.

**Structure check** — does every document still follow the declared shape? Compare the working tree
against a git ref: strip prose fields, serialise the remaining skeleton deterministically, and
require byte equality. Separately, require the multiset of citations to be unchanged — reordering
is allowed, losing or inventing is not. This is what makes an editorial rewrite provably editorial.

**Anchor check** — does every citation resolve by name against the source documents? Fail on: a
name that does not exist, an ambiguous name the hint cannot disambiguate, and any surviving
line-only citation in the old format. Auto-repair a drifted line hint in place and report it as a
warning, not a failure.

Output shape — terse, countable, and actionable:

```
files: 21 · anchors resolved: 1555
line hints repaired: 3
  ~ ct/ct-03.yaml:88 — hint corrected (341 → 347)
FAILURES: 2
  · p1/p1-enviar.yaml:214 — Doc6 has no entity "DocumentoRemetente"
      Doc6 · DocumentoRemetente.Estado (l. 402)
  · README.md:57 — citation with no nameable anchor (old format): Doc5:1195
exit 1
```

Full verifier design, including the skeleton-diff guard and CI wiring:
[references/verifiers.md](references/verifiers.md).

## Warning: IDs are not links

The worked example carried **1 555 ID cross-references and zero hyperlinks** in a single document.
For an agent reader that is not a defect: grep resolves every one of them, and a hyperlink would
add nothing an agent can use.

For a human reader it is a wall. A human projection of the same document must convert every ID
into a real link, collapse the register columns, and drop the provenance tags — that is a different
doctrine with a different toolkit. See the `spec-human` plugin. Do not try to serve both audiences
from one rendering: the properties that make the agentic set reliable are exactly the ones a human
reviewer rejects.

## Checklist

- One token grammar, documented in the set's README, with "the line is a hint" stated explicitly.
- One ID register; nothing reused, reserved numbers left alone, retirements tombstoned.
- Anchor graph regenerated and diffed on every change.
- Structure check and anchor check both green before "final".
- Human projection, if any, generated from the same source — never maintained in parallel.
