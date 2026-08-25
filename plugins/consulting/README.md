# consulting

A **consulting-grade analysis-framework skill** for Claude Code. Its core deliverable is the
*thinking structure* for a research report: given a research subject, it designs the analytical
framework before any data is touched. Opt-in.

## The flow

```
  research subject ─► Analysis Framework ─► ordinary research ─► Report
                      • chapter skeleton     (WebSearch/         written against
                      • named frameworks      WebFetch, user      the framework
                      • per-chapter data      documents)
                        requirements
                      • visualisation plan
```

1. **Framework design** — from just a research subject + scope, pick 2–4 named frameworks
   (SWOT, Porter's Five Forces, TAM-SAM-SOM, RFM, DCF, JTBD, …), lay out a chapter skeleton, and
   specify exactly what data each chapter needs (with search keywords + P0/P1/P2 priority) and how
   it will be visualised.
2. **Research** — data collection happens via ordinary research: WebSearch/WebFetch driven by the
   framework's search keywords, plus any user-supplied documents.
3. **Report** — written against the framework: comparison tables, `Data → User Psychology →
   Strategy Implication` narrative, and a strict **zero-hallucination** policy — every number
   traces to a collected source. Chart and report rendering is delegated to the built-in
   **artifact-design** and **dataviz** skills.

## Usage

The skill auto-loads when you ask for a market analysis, consumer-insight report, financial
analysis, industry research, competitive intelligence, or any consulting-grade analytical report —
whether you need the framework designed or a report written from collected findings.

## What's inside

- **1 skill** — `consulting-analysis` (`SKILL.md`): the framework-design workflow, the named-framework
  toolkit, the per-chapter data-requirement and visualisation templates, condensed report-writing
  guidance, and the quality checklist.

## Settings

Report language is controlled by `output_locale` (default `en_uk`, British English); reasoning
stays in English.
