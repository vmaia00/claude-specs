# Machine-tell checklist

Run before shipping any human-executor document. Each item: what to search for, why a human reader
rejects it, and what replaces it. None of these is a defect in an agent-executor document — in
`spec-agentic` most are load-bearing.

Do not remove these items silently at the point of writing prose. Remove them by re-projecting from
the back layer, or the structure they left behind stays.

---

## 1. Uniform section depth

**Find:** word count per section; compute the variance. Near-uniform depth across a dozen sections
is the tell.

**Why it fails:** depth is the author's only unspoken signal of importance. Uniform depth says the
author had no view, or never had to choose — which a reader correctly reads as machine output.

**Replace with:** deliberate asymmetry. The section that decides whether the release works is three
times longer than the routine one, and says so in the first line.

---

## 2. Per-claim provenance tags

**Find:** inline citation markers, source-file references, `[ref: ...]`-shaped tokens, footnote
markers on ordinary statements. Count them **per 1 000 words, never per line** — one table row or
bullet can carry 400+ words, so a per-line ratio understates density by roughly an order of
magnitude. **Above 2 per 1 000 words is a finding; above 5 per 1 000 words is terminal.** A measured
set at 8.6 per 1 000 words (1 161 markers) read as a safe 0.18 per line: same document, opposite
verdict, purely from the denominator. Report lines only as a secondary figure.

**Why it fails:** this is the primary "machine-made" tell — the thing readers name first. Citing an
uncontested statement signals that the author could not tell contested from uncontested, i.e.
applied no judgement.

**Replace with:** cite only what a reader would reasonably challenge, what is legally or
contractually binding, or what contradicts intuition. Everything else is asserted. Put the full
trail in the back layer and link it once from the header.

---

## 3. Bare ID cross-references

**Find:** any `AB-12` / `ABC-04.13`-shaped token in running prose. Also count hyperlinks: zero
across a large document is proof no person was expected to read it.

**Why it fails:** it is a decoder ring. The reader must hold an ID-to-meaning mapping the document
never gave them, often pointing at files they were not sent.

**Replace with:** the meaning, hyperlinked to a resolvable anchor. Keep the ID only where the
reader will type it into a tool, and then still link it. If the target was not shipped, cut the
reference.

---

## 4. Apparatus sections

**Find:** headings containing *impact*, *touchpoint*, *traceability*, *coverage matrix*,
*cross-reference index*; any table whose columns are document IDs. Measure their share of total
**words** — matrix rows and prose paragraphs are not the same size, so a share of lines distorts.

**Why it fails:** these exist because an agent has no working memory. A senior engineer already
holds the model the matrix reconstructs, so reading it is pure overhead — and it is the largest
single source of bulk.

**Replace with:** nothing in the reader-facing document. Generate on demand from the back layer if
someone asks.

---

## 5. Changelog in the body

**Find:** revision history, *versão / version* tables, *what changed in v3* sections, dense date
stamps in running text.

**Why it fails:** it is state recovery for a reader with no memory of previous sessions. A human
opens the current version and wants the current truth. History before content also buries the
first thing they should read.

**Replace with:** version control, or one dated changelog file at the end of the set. Dates attach
to decisions, in ADRs.

---

## 6. Tombstones

**Find:** sections describing removed features, *why we no longer do X*, *deprecated — do not
reintroduce*.

**Why it fails:** a human does not re-propose a rejected approach when the ADR exists; they will
look for the reasoning if they suspect it was a mistake. Agents will re-propose, which is why the
agentic doctrine keeps tombstones.

**Replace with:** an ADR with status *rejected* or *superseded*, linked from the relevant section
in one line.

---

## 7. Absent authorial voice

**Find:** the absence of first-person-plural judgement. Search for *we chose*, *we rejected*,
*the risk here*, *most likely to*, *do not*. If there are no hits, there is no author.

**Why it fails:** a document with no opinion offers the reader nothing they could not have derived
themselves, and gives them no way to disagree with a specific person. Consultation value is
carried almost entirely by opinion.

**Replace with:** at least one stated risk opinion per major section; a *we tried X and rejected it
because Y* for each significant fork; a plain statement of what worries the author most. Mark
opinion as opinion so it is not mistaken for a constraint.

---

## 8. Perfect structural symmetry

**Find:** identical subsection sets under every heading — every entity with the same five
sub-headings, every capability with the same seven, several of them near-empty or containing
*N/A* / *none*.

**Why it fails:** it is a template being filled, visibly. Empty slots prove the structure was
chosen before the content existed.

**Replace with:** subsections that exist only when they have content. Consistency of vocabulary,
not of skeleton.

---

## 9. Explaining assumed knowledge

**Find:** explanations of anything the header listed under *assumed knowledge* — protocol
primers, framework tutorials, definitions of terms the executor uses daily.

**Why it fails:** it directly contradicts the header, and it is the specific form of over-detail
that reads as condescension rather than thoroughness.

**Replace with:** deletion. If it was genuinely needed, the header's assumed-knowledge line was
wrong; fix the header instead.

---

## Two things to check that are not on the list

- **The scapegoat check.** When a reader names one chapter as "too technical", measure that
  chapter's share of the document, in words, before acting. In the failure case the accused chapter
  was ~10% of the set; the real driver was uniform exhaustiveness everywhere, attributed to the nearest
  visible cause. Cutting the named chapter would have changed nothing.
- **The lost-requirement check.** After removing apparatus, diff conclusions against the back layer,
  not against the old prose. Every requirement, invariant and acceptance criterion must still be
  present or deliberately dropped. Paragraphs are expendable; requirements are not.
