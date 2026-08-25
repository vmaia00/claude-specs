# -*- coding: utf-8 -*-
"""Overflow-safe thesis-style PDF from Markdown, via pandoc + XeLaTeX.

Portable driver extracted from Bool's «_build-latex.py» motor pipeline
(Projeto PAA). The pipeline:

    pandoc (gfm -> latex, --wrap=none) with references/template.tex
      -> breakable_inline_code(tex)   inject \\allowbreak{} inside \\texttt{}
      -> proportional_tables(tex)     rewrite pandoc's natural-width `l`
                                      longtable columns into sqrt-weighted
                                      proportional p{} columns
      -> xelatex -interaction=nonstopmode  (two passes: 1st writes the .toc,
                                            2nd prints it)
      -> %%EOF trailer check          nonstopmode can emit a truncated PDF
                                      and still exit 0
      -> Overfull \\hbox log scan      report residual overflow before the
                                      temp dir (and its .log) is deleted

Source-document contract (see SKILL.md):
  - title       = first `# ` heading
  - metadata    = a leading two-column pipe table `| **Key** | Value |`
                  (first 40 lines); rendered on the cover
  - body        = everything from the first `## ` on; each `##` becomes a
                  chapter on a new page
  - figures     = `.svg` references are swapped for a sibling `.png`

Usage:
  python build_latex.py DOC.md [MORE.md ...]
         [--template PATH] [--logo PATH] [--subtitle TEXT] [--eyebrow TEXT]
         [--out DIR] [--strict] [-V key=value ...]

Requires pandoc on PATH and XeLaTeX (TinyTeX at %APPDATA%/TinyTeX, or any
xelatex on PATH).
"""
import argparse
import io
import os
import re
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATE = os.path.join(HERE, "..", "references", "template.tex")
LOG = ">>> LATEX-DOC - %s <<<"


def find_xelatex():
    tinytex = os.path.join(os.environ.get("APPDATA", ""),
                           "TinyTeX", "bin", "windows", "xelatex.exe")
    if os.path.exists(tinytex):
        return tinytex
    found = shutil.which("xelatex")
    if found:
        return found
    raise SystemExit(LOG % "xelatex not found (TinyTeX or PATH)")


# ---------------------------------------------------------------- metadata
def _cell(txt):
    txt = re.sub(r"\*\*([^*]*)\*\*", r"\1", txt)
    txt = txt.replace("`", "").replace("*", "")
    return re.sub(r"\s{2,}", " ", txt).strip()


def metadata(src):
    """Ordered (key, value) pairs from the leading `| **Key** | Value |` table."""
    pairs = []
    for line in src.split("\n")[:40]:
        m = re.match(r"^\|\s*\*\*([^|*]+)\*\*\s*\|(.*)\|\s*$", line)
        if m:
            pairs.append((_cell(m.group(1)), _cell(m.group(2))))
    return pairs


def title_of(src):
    m = re.search(r"^#\s+(.+)$", src, re.M)
    return _cell(m.group(1)) if m else "Documento"


def escape_tex(txt):
    for a, b in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("$", r"\$"), ("#", r"\#"), ("_", r"\_"), ("{", r"\{"),
                 ("}", r"\}"), ("~", r"\textasciitilde{}"),
                 ("^", r"\textasciicircum{}")):
        txt = txt.replace(a, b)
    return txt


# ---------------------------------------------------------------- figures
RE_FIG_SVG = re.compile(r"(!\[.*?\])\(\s*([^)\s]+)\.svg\s*\)", re.S)
RE_FIG_RASTER = re.compile(r"(!\[[^\]]*\])\(\s*([^)\s]+\.(?:png|jpe?g))\s*\)", re.S)


def stage_figures(md, src_dir, tmp):
    """Swap .svg for the sibling .png and copy every figure into the temp dir,
    then cite it by bare filename: a URL with spaces breaks pandoc's image
    parser, and a Windows 8.3 short path brings a tilde -- an active TeX
    character -- into the .tex."""
    def swap_svg(m):
        png = os.path.join(src_dir, m.group(2) + ".png")
        if not os.path.exists(png):
            raise SystemExit(LOG % ("missing PNG for figure: " + png))
        name = os.path.basename(png)
        shutil.copyfile(png, os.path.join(tmp, name))
        return "%s(%s)" % (m.group(1), name)
    md = RE_FIG_SVG.sub(swap_svg, md)

    def swap_raster(m):
        if os.path.exists(os.path.join(tmp, m.group(2))):
            return m.group(0)  # already staged by the svg pass
        img = os.path.join(src_dir, m.group(2))
        if not os.path.exists(img):
            raise SystemExit(LOG % ("missing figure: " + img))
        name = os.path.basename(img)
        shutil.copyfile(img, os.path.join(tmp, name))
        return "%s(%s)" % (m.group(1), name)
    return RE_FIG_RASTER.sub(swap_raster, md)


# ------------------------------------------------- post-pandoc .tex rewrites
RE_LONGTABLE = re.compile(
    r"(\\begin\{longtable\}\[\]\{@\{\})(l+)(@\{\}\})(.*?)(\\end\{longtable\})", re.S)


def proportional_tables(tex):
    """Natural-width `l` columns overflow the text block; turn them into
    proportional p{} columns sized to each column's real content, with line
    breaking inside the cell (what pandoc itself does when the source
    declares widths)."""
    def one(m):
        n = len(m.group(2))
        body = m.group(4)
        longest = [4.0] * n
        for line in body.split("\\\\"):
            cells = line.split(" & ")
            if len(cells) != n:
                continue
            for i, c in enumerate(cells):
                longest[i] = max(longest[i], min(len(c.strip()), 220))
        # square root: a column ten times longer does not get ten times
        # wider; short label columns stay readable
        weights = [x ** 0.5 for x in longest]
        total = sum(weights)
        cols = "".join(
            ">{\\raggedright\\arraybackslash}p{(\\linewidth - %d\\tabcolsep) * \\real{%.4f}}"
            % (2 * n, w / total) for w in weights)
        return "\\begin{longtable}[]{@{}" + cols + "@{}}" + body + m.group(5)
    return RE_LONGTABLE.sub(one, tex)


RE_TEXTTT = re.compile(r"\\texttt\{([^{}]*)\}")


def breakable_inline_code(tex):
    """Inline code does not break and blows past the right margin; give it a
    break point after the natural separators (/ . - _ : @ =)."""
    def one(m):
        body = m.group(1)
        body = re.sub(r"([/.:@=])", r"\1\\allowbreak{}", body)
        body = body.replace(r"\_", r"\_\allowbreak{}")
        body = body.replace("-", "-\\allowbreak{}")
        return r"\texttt{" + body + "}"
    return RE_TEXTTT.sub(one, tex)


# ---------------------------------------------------------------- log scan
RE_OVERFULL = re.compile(r"^Overfull \\hbox \(([\d.]+)pt too wide\)", re.M)


def scan_overfull(log_path):
    """The template silences overfull warnings under 2pt (\\hfuzz); anything
    the log still reports is real overflow. Returns [(pt, line), ...]."""
    if not os.path.exists(log_path):
        return []
    log = io.open(log_path, encoding="utf-8", errors="replace").read()
    return [(float(m.group(1)), log.count("\n", 0, m.start()) + 1)
            for m in RE_OVERFULL.finditer(log)]


# ---------------------------------------------------------------- build
def build(md_path, opts):
    src_dir = os.path.dirname(os.path.abspath(md_path)) or "."
    stem = os.path.splitext(os.path.basename(md_path))[0]
    src = io.open(md_path, encoding="utf-8").read()
    pairs = metadata(src)
    meta = dict(pairs)

    # H1 and metadata live on the cover; the LaTeX body starts at the first
    # chapter.
    m = re.search(r"^## ", src, re.M)
    body = src[m.start():] if m else src

    tmp = tempfile.mkdtemp(prefix="latex-doc-")
    try:
        body = stage_figures(body, src_dir, tmp)
        md_tmp = os.path.join(tmp, stem + ".md")
        io.open(md_tmp, "w", encoding="utf-8").write(body)
        tex_tmp = os.path.join(tmp, stem + ".tex")

        args = ["pandoc", "-f", "gfm", "-t", "latex", "--wrap=none",
                "--top-level-division=chapter", "--shift-heading-level-by=-1",
                "--template", os.path.abspath(opts.template),
                "-V", "title=" + escape_tex(title_of(src)),
                "-V", "eyebrow=" + escape_tex(opts.eyebrow or meta.get("Documento", "")),
                "-o", tex_tmp, md_tmp]
        subtitle = opts.subtitle or meta.get("Subtítulo", "") or meta.get("Subtitle", "")
        if subtitle:
            args += ["-V", "subtitle=" + escape_tex(subtitle)]
        if opts.logo:
            args += ["-V", "logo=" + os.path.abspath(opts.logo).replace("\\", "/")]
        rows = ["      \\textbf{%s} & %s \\\\" % (escape_tex(k), escape_tex(v))
                for k, v in pairs
                if k not in ("Documento", "Subtítulo", "Subtitle")]
        args += ["-V", "metatable=" + "\n".join(rows)]
        for kv in opts.variables:
            args += ["-V", kv]
        r = subprocess.run(args, capture_output=True, encoding="utf-8")
        if r.returncode != 0:
            raise SystemExit(LOG % ("pandoc failed: " + (r.stderr or "").strip()[:800]))

        tex = io.open(tex_tmp, encoding="utf-8").read()
        tex = breakable_inline_code(tex)
        tex = proportional_tables(tex)
        io.open(tex_tmp, "w", encoding="utf-8").write(tex)

        # Two passes: the first writes the .toc, the second prints it. Run
        # INSIDE the temp dir with bare filenames: its path carries a tilde
        # from the 8.3 short name, an active TeX character.
        xelatex = find_xelatex()
        pdf_tmp = os.path.join(tmp, stem + ".pdf")
        for _ in (1, 2):
            subprocess.run([xelatex, "-interaction=nonstopmode", stem + ".tex"],
                           capture_output=True, cwd=tmp)
        log_path = os.path.join(tmp, stem + ".log")

        # A truncated PDF (xelatex aborting mid-run) must not ship: the file
        # has to close with the %%EOF trailer.
        if not os.path.exists(pdf_tmp) or \
                b"%%EOF" not in io.open(pdf_tmp, "rb").read()[-64:]:
            tail = io.open(log_path, encoding="utf-8", errors="replace").read()[-1500:] \
                if os.path.exists(log_path) else ""
            raise SystemExit(LOG % ("truncated/missing PDF for " + stem + ":\n" + tail))

        # Residual overflow: everything \hfuzz did not silence is real.
        overfull = scan_overfull(log_path)
        if overfull:
            worst = sorted(overfull, reverse=True)[:5]
            msg = "%d Overfull hbox in %s (worst: %s)" % (
                len(overfull), stem,
                ", ".join("%.1fpt@log:%d" % w for w in worst))
            if opts.strict:
                raise SystemExit(LOG % msg)
            print(LOG % ("WARNING " + msg))

        out_dir = opts.out or src_dir
        dest = os.path.join(out_dir, stem + ".pdf")
        shutil.copyfile(pdf_tmp, dest)
        print(LOG % ("PDF %s (%d bytes, %d overfull)" %
                     (dest, os.path.getsize(dest), len(overfull))))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    p = argparse.ArgumentParser(description="Overflow-safe PDF from Markdown")
    p.add_argument("docs", nargs="+", help="markdown source file(s)")
    p.add_argument("--template", default=DEFAULT_TEMPLATE)
    p.add_argument("--logo", default=None, help="cover logo image (png/jpg/pdf)")
    p.add_argument("--subtitle", default=None)
    p.add_argument("--eyebrow", default=None)
    p.add_argument("--out", default=None, help="output dir (default: beside the .md)")
    p.add_argument("--strict", action="store_true",
                   help="fail on any residual Overfull hbox")
    p.add_argument("-V", dest="variables", action="append", default=[],
                   metavar="key=value",
                   help="extra pandoc variable (accent-color, mainfont, lang-english...)")
    opts = p.parse_args()
    if not shutil.which("pandoc"):
        raise SystemExit(LOG % "pandoc not found on PATH")
    for doc in opts.docs:
        build(doc, opts)


if __name__ == "__main__":
    main()
