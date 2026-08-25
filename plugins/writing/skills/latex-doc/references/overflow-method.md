# The overflow method — why every line of the tolerance block exists

## Origin story

The method was first learned on the Chromium print pipeline (Edge headless → PDF),
where the failure mode is brutal and silent: when any element exceeds the page
width, Chromium does not crop and does not overflow — it **shrinks the whole
document** (shrink-to-fit, capped at factor 2), body text included. One 970-character
JSON line in one code block once shipped a 60-page document at 7.3pt body instead of
11pt; a 90-character formula shipped another at 10.3pt — and nobody noticed, because
the font declaration in the PDF still said the same size (the shrink hides in the
page matrix). The lesson generalises to LaTeX, where the equivalent failure is the
overfull `\hbox`: content jutting past the right margin.

Two rules came out of that incident:

1. **The "three families" rule.** Only three families of content can be wide — code
   blocks, tables, images. Each gets its own brake **in the template/pipeline, never
   in the source Markdown** (the .md must not be held hostage by the width of an A4
   page). A new family of wide content gets a new brake in the template.
2. **Verify the product, not the source.** Measure the rendered artifact (here:
   scan the `.log` for `Overfull \hbox`; on the Chromium path: measure the body size
   out of the PDF's page matrix). And if you build a verifier, mutation-test it —
   deliberately break a brake and confirm the verifier fails.

## The preamble tolerance block, line by line

```latex
\setstretch{1.32}                 % thesis-style leading
\setlength{\parindent}{0pt}       % block paragraphs...
\setlength{\parskip}{0.55\baselineskip}  % ...nothing ragged at the margins
\emergencystretch=3em   % THE fix: a third line-breaking pass with 3em of
                        % extra glue per line — prevents most overfull boxes
\tolerance=2000         % accept looser lines instead of overflowing (default 200)
\hbadness=10000         % silence underfull/badness noise (cosmetic)
\setlength{\hfuzz}{2pt} % silence overfull warnings under 2pt (cosmetic —
                        % real overflow still reports, which the build scans for)
\usepackage{microtype}  % font expansion + protrusion: measurably fewer
                        % overfull lines, for free
\usepackage[portuguese]{babel}  % hyphenation patterns; unhyphenated Portuguese
                                % words are long — hyphenation IS an overflow fix.
                                % babel, not polyglossia, even under XeLaTeX.
```

## Brake 1 — code

- Blocks: `\DefineVerbatimEnvironment{verbatim}{Verbatim}{fontsize=\footnotesize,breaklines=true}`
  (fancyvrb). `breaklines=true` is the LaTeX equivalent of CSS
  `pre { overflow-wrap: anywhere }`; `\footnotesize` buys ~20% more chars per line.
- Inline: `\texttt` is wrapped at `\small`, and the driver injects `\allowbreak{}`
  after `/ . : @ = _ -` inside every `\texttt{...}` so `corpus/fiscal/codes/RITI.pdf`
  or `motor_ledger` can break at natural separators. (This replaces
  `seqsplit`/`url` machinery; the regex deliberately skips `\texttt` containing
  nested braces.)

## Brake 2 — tables

GFM tables carry no widths, so pandoc emits `\begin{longtable}[]{@{}llll@{}}` —
natural-width columns that blow past the text block whenever a cell holds prose.
The driver rewrites them:

1. Measure the longest cell per column, in characters, clamped to 220.
2. Weight by **square root** — a column ten times longer must not be ten times
   wider; short label columns stay readable.
3. Normalise and emit pandoc's own width idiom:
   `>{\raggedright\arraybackslash}p{(\linewidth - 2n\tabcolsep) * \real{f}}`
   (requires the `array` + `calc` packages).
4. `\raggedright` matters on its own: justified narrow `p{}` columns are themselves
   an overfull-hbox generator.

Supporting template lines: `\LTleft=0pt` + `\LTright=\fill` left-align longtables so
a still-too-wide table overflows only rightward, never into the left margin;
`\AtBeginEnvironment{longtable}{\small\setstretch{1.15}}` drops every table one font
step without touching any table source.

## Brake 3 — images

```latex
\makeatletter
\def\maxwidth{\ifdim\Gin@nat@width>\linewidth\linewidth\else\Gin@nat@width\fi}
\makeatother
\setkeys{Gin}{width=\maxwidth,keepaspectratio}
```

No image can exceed `\linewidth`; smaller images keep natural size.

## Verification

- Two xelatex passes (1st writes `.toc`, 2nd prints it), then require the PDF to end
  with `%%EOF` — under `-interaction=nonstopmode` xelatex can abort mid-document,
  leave a truncated PDF, and still exit 0.
- Scan the `.log` for `Overfull \hbox (...pt too wide)` **before** the temp dir is
  deleted. `\hfuzz=2pt` means anything still reported is real. `--strict` fails the
  build on it.

## The CSS equivalents (Chromium/Edge print path)

For reference, the same three brakes on the HTML side:

```css
@page { size: A4; margin: 17mm 16mm 16mm 16mm; }
pre { white-space: pre-wrap; overflow-wrap: anywhere; max-width: 100%; }
img { max-width: 100%; height: auto; }
@media print {
  .table-wrap table { table-layout: fixed; font-size: 8pt; }
  .table-wrap th, .table-wrap td { overflow-wrap: anywhere; word-break: break-word; }
}
```

And the verification rule: read the page CTM scale out of the PDF (pypdf visitor) —
Chromium keeps the `Tf` font size constant and hides the shrink in the page matrix,
so anyone who only checks `Tf` concludes all documents are fine.
