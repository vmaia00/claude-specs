---
name: latex-doc
description: >
  Render Markdown deliverables into thesis-style A4 PDFs (full-colour cover, TOC,
  chapter-per-page) via pandoc + XeLaTeX, with a template and pipeline engineered so
  content NEVER overflows the margins. Use when the user asks for a PDF deliverable,
  a "tese"-style document render, a LaTeX export of a Markdown doc, or reports
  overflowing/clipped tables, code, or margins in a generated PDF. Works for PT-PT
  documents by default (babel portuguese) and for English via a flag.
---

# latex-doc — overflow-safe thesis PDFs from Markdown

One pandoc template + one Python driver. The Markdown file is the single source of
truth; the `.tex` is a temporary artifact. Extracted from Bool's Projeto PAA "tese"
pipeline (shape inspired by the ipleiria-thesis template; overflow method ported from
a hard-won Chromium print fix — see `references/overflow-method.md`).

## Prerequisites

- `pandoc` on PATH.
- XeLaTeX — TinyTeX is enough (`%APPDATA%\TinyTeX\bin\windows\xelatex.exe` is probed
  first, then PATH). Needed packages: koma-script, fontspec, geometry, microtype,
  setspace, xcolor, tools (longtable/array/calc), booktabs, etoolbox, fancyvrb,
  footnotehyper, hyperref, babel + Portuguese hyphenation.
- XeLaTeX is **mandatory** (fontspec loads system fonts by name).

## How to render

```
python scripts/build_latex.py DOC.md --logo path/to/logo.png
# options: --template, --subtitle, --eyebrow, --out DIR, --strict,
#          -V accent-color=E7453A -V mainfont="Yu Gothic UI" -V lang-english=1
```

Source-document contract:
- **Title** = the first `# ` heading (goes on the cover only).
- **Cover metadata** = a leading two-column pipe table `| **Key** | Value |` in the
  first 40 lines (e.g. Cliente, Fornecedor, Documento, Audiência, Versão, Data,
  Classificação). The `Documento` row becomes the cover eyebrow.
- **Body** starts at the first `## `; every `##` becomes a chapter on a new page
  (`--top-level-division=chapter --shift-heading-level-by=-1`). LaTeX numbering is
  off — number headings in the Markdown itself.
- **Figures**: reference `.svg` freely; the driver swaps in a sibling `.png`.

## The overflow method — the "three families" rule

Only three families of content can be wider than the text block, and **each gets its
own brake in the template/pipeline — never in the .md** (the source must not be held
hostage by the width of an A4 page):

| family | brake |
|---|---|
| code block | `fancyvrb` verbatim redefined with `breaklines=true`, `\footnotesize` |
| table | post-pandoc `l`→`p{}` proportional-column rewrite + `\LTleft=0pt`/`\LTright=\fill` + `\small` |
| image | `\maxwidth` idiom + `\setkeys{Gin}{width=\maxwidth,keepaspectratio}` |

Plus a preamble tolerance block (`\emergencystretch=3em`, `\tolerance=2000`,
`microtype`, babel hyphenation) that lets TeX loosen lines instead of overflowing,
and an inline-code pass that injects `\allowbreak{}` after `/ . : @ = _ -` inside
every `\texttt{}` so long identifiers/paths break instead of jutting into the margin.
A NEW family of wide content gets a new brake in the template — full rationale and
per-line explanation in `references/overflow-method.md`.

## Non-obvious rules (learned the hard way)

1. **`--wrap=none` on pandoc is required** — the post-pandoc regex passes assume
   unwrapped lines.
2. **Two xelatex passes, always**: the first writes the `.toc`, the second prints it.
3. **Never trust nonstopmode's exit code**: check the PDF ends with `%%EOF` — xelatex
   happily emits a truncated PDF and returns 0.
4. **Windows path hygiene**: copy every asset into the temp dir, cite bare filenames,
   run xelatex with `cwd=tmpdir`. An 8.3 short path contains `~` (an active TeX
   character) and spaces break pandoc's image parser.
5. **Scan the `.log` for `Overfull \hbox` before deleting the temp dir** — the
   template deliberately silences warnings under 2pt (`\hfuzz`), so anything still
   reported is real overflow. `--strict` turns it into a failure.
6. Portuguese: template defaults to `babel[portuguese]` (pt-PT hyphenation — itself
   an overflow fix) with `\contentsname` = "Índice". Pass `-V lang-english=1` for
   English documents.

## Branding

The template is brand-parameterised: `accent-color`, `ink-color`, `muted-color`,
`mainfont`, `logo` are pandoc variables (defaults match Bool's palette; the template
itself contains no company name). For white-label/neutral exports, pass a neutral
logo and colours — nothing in the .md changes.
