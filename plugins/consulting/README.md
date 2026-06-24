# consulting

A **two-phase, consulting-grade research-report skill** for Claude Code. It separates *thinking
structure* from *data collection*: Phase 1 designs the analytical framework, other skills gather
the data, and Phase 2 writes the final McKinsey/BCG-voice report. Opt-in.

## The flow

```
  research subject ─► Phase 1: Framework ─► (handoff) ─► Phase 2: Report
                      • chapter skeleton      data         • charts + tables
                      • named frameworks      collection   • What→Why→So-What
                      • per-chapter data      by other     • zero-hallucination
                        requirements          skills         narrative
                      • visualization plan   (deep-research,
                                              data-analysis…)
```

1. **Phase 1 — Analysis Framework** — from just a research subject + scope, pick 2–4 named
   frameworks (SWOT, Porter's Five Forces, TAM-SAM-SOM, RFM, DCF, JTBD, …), lay out a chapter
   skeleton, and specify exactly what data each chapter needs (with search keywords + P0/P1/P2
   priority) and how it will be visualized.
2. **Handoff** — the framework's search keywords drive other data-collection skills; this skill
   does **not** collect data itself.
3. **Phase 2 — Report** — synthesize the framework + collected Data Package into a polished
   report: embedded charts, comparison tables, and `Data → User Psychology → Strategy Implication`
   narrative. Strict **zero-hallucination** policy — every number traces back to the Data Summary.

## Usage

The skill auto-loads when you ask for a market analysis, consumer-insight report, financial
analysis, industry research, competitive intelligence, or any consulting-grade analytical report —
either to design the framework (Phase 1) or to write the report from collected data (Phase 2).

## What's inside

- **1 skill** — `consulting-analysis` (`SKILL.md`): the two-phase contract, the framework toolkit,
  the per-chapter data-requirement and visualization templates, the report structure template, and
  the quality checklists.

## Settings

Report language is controlled by `output_locale` (default `en_uk`, British English); reasoning
stays in English.
