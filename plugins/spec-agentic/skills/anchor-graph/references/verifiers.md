# Verifier design

Three small scripts, run in this order, owned by the spec set and wired into CI. They are the
reason a spec set can be called final by a machine rather than by a feeling.

```
1. structure check   does the change touch only what it claims to touch?
2. anchor check      does every citation resolve by name?
3. publish           regenerate the reference copy from the source
```

Adapt the sketches below; do not treat them as a library. The conventions matter, the code does not.

---

## 1. The index: name → lines

Everything else depends on being able to resolve a name inside a source document. Build an index
per source document, from its own structure:

- **Headings** give sections (`§3.7`), with their line ranges and nesting.
- **Entity headings** in a data model give entities; the table rows beneath give their fields.
- **Story headings** give `US-nn.n`.
- **Named groups** ("Group G") give multi-entity ranges.
- Anything else falls back to **verbatim text**: normalise the line (strip markup, quotes and
  repeated whitespace) on both sides — when generating the anchor and when resolving it — so the
  two normalisations cannot drift apart.

The index is also what lets you *convert* an existing set: line → name for every legacy citation,
in a one-off pass, with the survivors listed for manual conversion.

```python
class Index:
    def __init__(self, path):
        self.lines = read(path).split("\n")
        self.sections = []   # [{num, title, level, start, end}]
        self.stories  = {}   # "US-04.2" -> (start, end)
        self.entities = {}   # "Documento" -> {start, end, fields: {name: [lines]}}
        self._build()

    def resolve(self, token):
        """-> (start, end) or raise Ambiguous / NotFound"""
```

**Ambiguity is a failure, not a coin flip.** If a field name occurs in two entities and the token
does not qualify it, fail and tell the author to qualify. Silently picking the nearest match is how
a citation ends up pointing at the wrong entity for six months.

---

## 2. Anchor check

Walk the **raw text** of every file in the set, not the parsed tree. Raw text catches citations
inside YAML comments, inside prose blocks, and inside the README — a parse would not see them.

For each token found:

| Outcome | Action |
|---|---|
| Name resolves, hint matches | count it, move on |
| Name resolves, hint drifted | rewrite the hint **in place**, report as a warning |
| Name does not exist | FAIL, print `file:line`, the message and the offending token |
| Name is ambiguous | FAIL, list the candidate locations |
| Old numeric-only format | FAIL — the citation is not verifiable |

Also verify prose references that name a section in words ("Doc 3, section 3.3"): confirm that the
document exists in the set and that the section number exists in it.

In-place hint repair is the feature that keeps the convention alive. Without it, authors stop
updating hints, hints become noise, and the set drifts back to unverifiable citations.

```python
def check(path, failures, warnings):
    text = read(path)
    def handle(m):
        state, hint, msg = resolve_token(m)
        if state == "fail":
            failures.append(f"{path}:{line_of(m)} — {msg}\n      {m.group(0)}")
        elif state == "repair":
            warnings.append(f"{path}:{line_of(m)} — hint corrected ({msg})")
            return m.group(0).replace(f"(l. {m['hint']})", f"(l. {hint})")
        return m.group(0)
    new = TOKEN.sub(handle, text)
    if new != text:
        write(path, new)
```

---

## 3. Structure check (the editorial guard)

The problem it solves: someone reorganises a document set "for readability" and, somewhere in
2 000 lines of diff, an enum value or a `required` list changes too. Nobody catches it by reading.

Compare the working tree against a git ref and require three things per file:

1. **Skeleton identical.** Strip the prose fields (`description`, `summary`, free-text decision
   notes, titles), serialise the rest with sorted keys, and require byte equality. Normalise line
   hints to a placeholder first, so a legitimate hint repair inside a structural field does not
   register as a structural change.
2. **Citation multiset identical.** Collect every citation token, keyed **without** the line hint,
   and compare the bags. Reordering is fine. Losing one or inventing one is not — report exactly
   which were lost and which are new.
3. **Still parses, and every `$ref` still resolves.**

```python
PROSE = {"description", "summary", "rationale", "title", "note"}

def skeleton(node):
    if isinstance(node, dict):
        return {k: skeleton(v) for k, v in sorted(node.items())
                if k not in PROSE and not is_pure_provenance(k)}
    if isinstance(node, list):
        return [skeleton(v) for v in node]
    if isinstance(node, str):
        return HINT.sub("(l. _)", node)
    return node
```

Print the first divergence with its top-level keys. Forcing the author to hunt for it guarantees
the check gets disabled.

---

## 4. Publish

The source carries the full provenance chain: anchors, decision records, provenance tags. That is
audit material, not documentation. A reader of the published reference sees noise, and every route
title starts with a bracketed marker.

**The source keeps everything; the render cleans.** Never strip the source. Write a cleaned copy to
a separate output directory, and have the publisher *validate* that no provenance trace survived.

What goes:

- pure-provenance extensions (the anchor list);
- inside a decision record, the origin and source fields — the *choice* itself stays, because the
  "why" is the most useful content in the set;
- inline citations, both formats;
- provenance markers in square brackets, including the leading marker that made titles start with
  `[...]`.

What stays: design content. Gating markers, authorisation and idempotency notes, status, open
points, out-of-scope declarations, prose references to sections and to the set's own filenames.

Removal is where publishing breaks. Deleting a token mid-sentence leaves orphaned punctuation
("marked.", stray separators, an unclosed parenthesis whose opener was inside the removed span).
Remove the **whole formula**, not just the token, and finish with a pass that collapses orphaned
separators and double spaces.

---

## 5. CI wiring

```yaml
- run: python _verify_structure.py "$BASE_SHA"   # editorial guard, needs a ref
- run: python _verify_anchors.py                 # must exit 0
- run: git diff --exit-code                      # hint repairs must be committed
- run: python _graph.py . graph-anchors.json
- run: python _publish.py                        # regenerates + validates the render
```

The `git diff --exit-code` step is deliberate: the anchor checker repairs hints in place, and an
unrepaired working tree in CI means someone bypassed the local run.

Gate merges on all of it. A spec set whose verifiers are advisory is a spec set with rotten edges
and a green badge.
