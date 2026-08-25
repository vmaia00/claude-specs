---
name: consulting-analysis
description: Use this skill when the user requests a consulting-grade analytical report or research framework — market analysis, consumer insights, brand analysis, financial analysis, industry research, competitive intelligence, or investment due diligence. Its core deliverable is a rigorous analysis framework — chapter skeleton, named frameworks (SWOT, Porter's Five Forces, TAM-SAM-SOM, …), per-chapter data requirements, and a visualisation plan. Data is then gathered through ordinary research (WebSearch/WebFetch, user-supplied documents) and the report is written against that framework.
---

# Consulting Analysis Framework Skill

## Overview

This skill designs **consulting-grade analysis frameworks** for research reports — market analysis, consumer insights, brand strategy, financial analysis, industry research, competitive intelligence, investment research, macroeconomics. Given a research subject, it produces a rigorous analysis framework: chapter skeleton, named analytical frameworks, per-chapter data requirements, and a visualisation plan. Data collection then happens via ordinary research (WebSearch/WebFetch, user-supplied documents), and the final report is written against the framework.

Output follows McKinsey/BCG consulting voice standards. Report language follows the `output_locale` setting (default: `en_uk`, British English).

## Data Authenticity Protocol

**Strict adherence rule**: all data presented in the report and visualised in charts MUST come from collected research findings or user-supplied documents.
- **No hallucinations**: do not invent, estimate, or simulate data. If data is missing, state "Data not available" rather than fabricating numbers.
- **Traceable sources**: every major claim and chart must be traceable back to a specific source.

## When to Use This Skill

- User asks for a market analysis, consumer-insight report, financial analysis, industry research, or any consulting-grade analytical report
- User provides a research subject and needs a structured analysis framework before research begins
- User provides research findings or documents to be synthesised into a consulting-style report

# Designing the Analysis Framework

## Purpose

Given a **research subject** (e.g., "Gen-Z Skincare Market Analysis", "NEV Industry Competitive Landscape", "Brand X Consumer Profiling"), produce a complete **analysis framework** that serves as the blueprint for research and report writing.

## Inputs

| Input | Description | Required |
|-------|-------------|----------|
| **Research Subject** | The topic or question to be analysed | Yes |
| **Scope / Constraints** | Geographic scope, time range, industry segment, target audience, etc. | Optional |
| **Specific Angles** | Any particular angles or hypotheses the user wants explored | Optional |
| **Domain** | The analytical domain: market, finance, industry, brand, consumer, investment, etc. | Inferred |

## Step 1: Understand the Research Subject

- Parse the research subject to identify the **core entity** (market, brand, product, industry, consumer segment, financial instrument, etc.)
- Identify the **analytical domain** and its **natural analytical dimensions**:

| Domain | Typical Dimensions |
|--------|--------------------|
| Market Analysis | Market size, growth trends, market segmentation, growth drivers, competitive landscape, consumer profiling |
| Brand Analysis | Brand positioning, market share, consumer perception, marketing strategy, competitor comparison |
| Consumer Insights | Demographic profiling, purchase behaviour, decision journey, pain points, scenario analysis |
| Financial Analysis | Macro environment, industry trends, company fundamentals, financial metrics, valuation, risk assessment |
| Industry Research | Value chain analysis, market size, competitive landscape, policy environment, technology trends, entry barriers |
| Investment Due Diligence | Business model, financial health, management assessment, market opportunity, risk factors, exit pathways |
| Competitive Intelligence | Competitor identification, strategic comparison, SWOT analysis, differentiated positioning, market dynamics |

## Step 2: Select Analysis Frameworks & Models

Based on the identified domain and research subject, select **one or more** professional analysis frameworks to structure the reasoning in each chapter. The chosen frameworks guide the **Analysis Logic** in the chapter skeleton (Step 3).

### Strategic & Environmental Analysis

| Framework | Description | Best For |
|-----------|-------------|----------|
| **SWOT Analysis** | Strengths, Weaknesses, Opportunities, Threats | Brand assessment, competitive positioning, strategic planning |
| **PEST / PESTEL Analysis** | Political, Economic, Social, Technological (+ Environmental, Legal) | Macro-environment scanning, market entry assessment, policy impact analysis |
| **Porter's Five Forces** | Supplier bargaining power, buyer bargaining power, threat of new entrants, threat of substitutes, industry rivalry | Industry competitive landscape, entry barrier assessment, profit margin analysis |
| **Porter's Diamond Model** | Factor conditions, demand conditions, related industries, firm strategy & structure | National/regional competitive advantage analysis |
| **VRIO Analysis** | Value, Rarity, Imitability, Organisation | Core competency assessment, resource advantage analysis |

### Market & Growth Analysis

| Framework | Description | Best For |
|-----------|-------------|----------|
| **STP Analysis** | Segmentation, Targeting, Positioning | Market segmentation, target market selection, brand positioning |
| **BCG Matrix (Growth-Share Matrix)** | Stars, Cash Cows, Question Marks, Dogs | Product portfolio management, resource allocation decisions |
| **Ansoff Matrix** | Market penetration, market development, product development, diversification | Growth strategy selection |
| **Product Life Cycle (PLC)** | Introduction, growth, maturity, decline | Product strategy formulation, market timing decisions |
| **TAM-SAM-SOM** | Total / Serviceable / Obtainable Market | Market sizing, opportunity quantification |
| **Technology Adoption Lifecycle** | Innovators → Early Adopters → Early Majority → Late Majority → Laggards | Emerging technology/category penetration analysis |

### Consumer & Behavioural Analysis

| Framework | Description | Best For |
|-----------|-------------|----------|
| **Consumer Decision Journey** | Awareness → Consideration → Evaluation → Purchase → Loyalty | Consumer behaviour path mapping, touchpoint optimisation |
| **AARRR Funnel (Pirate Metrics)** | Acquisition, Activation, Retention, Revenue, Referral | User growth analysis, conversion rate optimisation |
| **RFM Model** | Recency, Frequency, Monetary | Customer value segmentation, precision marketing |
| **Maslow's Hierarchy of Needs** | Physiological → Safety → Social → Esteem → Self-actualisation | Consumer psychology analysis, product value proposition |
| **Jobs-to-be-Done (JTBD)** | The "job" a user needs to accomplish in a specific context | Demand insight, product innovation direction |

### Financial & Valuation Analysis

| Framework | Description | Best For |
|-----------|-------------|----------|
| **DuPont Analysis** | ROE = Net Profit Margin × Asset Turnover × Equity Multiplier | Profitability decomposition, financial health diagnosis |
| **DCF (Discounted Cash Flow)** | Free cash flow discounting | Enterprise/project valuation |
| **Comparable Company Analysis** | PE, PB, PS, EV/EBITDA multiples comparison | Relative valuation, peer benchmarking |
| **EVA (Economic Value Added)** | After-tax operating profit - Cost of capital | Value creation capability assessment |

### Competitive & Strategic Positioning

| Framework | Description | Best For |
|-----------|-------------|----------|
| **Benchmarking** | Key performance indicator item-by-item comparison | Competitor gap analysis, best practice identification |
| **Strategic Group Mapping** | Cluster competitors along two key dimensions | Competitive landscape visualisation, white-space identification |
| **Value Chain Analysis** | Primary activities + support activities value decomposition | Cost advantage sources, differentiation opportunity identification |
| **Blue Ocean Strategy** | Value curve, four-action framework (Eliminate-Reduce-Raise-Create) | Differentiated innovation, new market space creation |
| **Perceptual Mapping** | Plot brand positions along two consumer-perceived dimensions | Brand positioning analysis, market gap discovery |

### Industry & Supply Chain Analysis

| Framework | Description | Best For |
|-----------|-------------|----------|
| **Industry Value Chain** | Upstream → Midstream → Downstream decomposition | Industry structure understanding, profit distribution analysis |
| **Gartner Hype Cycle** | Technology Trigger → Peak of Inflated Expectations → Trough of Disillusionment → Slope of Enlightenment → Plateau of Productivity | Emerging technology maturity assessment |
| **GE-McKinsey Matrix** | Industry Attractiveness × Competitive Strength | Business portfolio prioritisation, investment decisions |

### Selection Principles

1. **Domain-first**: based on the domain identified in Step 1, select **2-4** most relevant frameworks from the toolkit above
2. **Complementary**: choose complementary rather than overlapping frameworks (e.g., macro-level with PESTEL + micro-level with Porter's Five Forces)
3. **Depth over breadth**: better to deeply apply 2 frameworks than superficially stack 6
4. **Data-feasible**: selected frameworks must be supportable by data obtainable through ordinary research — if the data a framework requires cannot reasonably be found, downgrade or substitute
5. **Explicit mapping**: in the chapter skeleton, explicitly annotate which framework each chapter uses and how it is applied

### Framework Selection Output Format

```markdown
| Chapter | Selected Framework(s) | Application |
|---------|----------------------|-------------|
| Market Size & Growth Trends | TAM-SAM-SOM + Product Life Cycle | TAM-SAM-SOM to quantify market space, PLC to determine market stage |
```

## Step 3: Design Chapter Skeleton

Produce a hierarchical chapter structure. Each chapter must include:

1. **Chapter Title** — professional, concise, subject-based (follow the titling constraints below)
2. **Analysis Objective** — what this chapter aims to reveal
3. **Analysis Logic** — the reasoning chain or framework (must reference the frameworks selected in Step 2)
4. **Core Hypothesis** — preliminary hypotheses to be validated or refuted by data
5. **Data Requirements** — see Step 4
6. **Visualisation Plan** — see Step 5

## Step 4: Define Data Requirements Per Chapter

For each chapter, specify **exactly what data needs to be collected**. This is the research checklist that drives the subsequent WebSearch/WebFetch work.

| Field | Description |
|-------|-------------|
| **Data Metric** | The specific metric or data point needed (e.g., "China skincare market size 2020-2025 (in billion CNY)") |
| **Data Type** | Quantitative, Qualitative, or Mixed |
| **Suggested Sources** | Industry reports, financial statements, government statistics, social media, e-commerce platforms, survey data, news |
| **Search Keywords** | Suggested search queries |
| **Priority** | P0 (Required) / P1 (Important) / P2 (Supplementary) |
| **Time Range** | The time period the data should cover |

Output as a per-chapter Markdown table with one row per data requirement, e.g. `| 1 | Market size (billion CNY) | Quantitative | Industry reports | "China skincare market size 2024" | P0 | 2020-2025 |`.

## Step 5: Define Visualisation & Content Plan Per Chapter

For each chapter, specify the **planned visualisation** and **argument structure** for the final report:

- **Visualisation Type & Title** — chart type (line, bar, pie, scatter, radar, heatmap, comparison table, …) and a descriptive title
- **Data Mapping** — which data indicators map to axes or segments, referencing Data Requirement numbers
- **Comparison Table Design** — column headers and comparison dimensions
- **Argument Structure** — the planned "What → Why → So What" narrative outline

This plan specifies *what* each chart shows, not *how* to render it — rendering is delegated to the built-in **artifact-design** and **dataviz** skills at report-writing time.

## Step 6: Output the Complete Analysis Framework

Assemble all outputs into a single, structured **Analysis Framework Document**:

```markdown
# [Research Subject] Analysis Framework

## Research Overview
- **Research Subject**: [...]
- **Scope**: [Geography, time range, industry segment]
- **Analysis Domain**: [Market / Finance / Industry / Brand / Consumer / ...]
- **Core Research Questions**: [1-3 key questions]

## Framework Selection
[Chapter → Framework(s) → Application table]

## Chapter Skeleton

### 1. [Chapter Title]
- **Analysis Objective / Analysis Logic / Core Hypothesis**
#### Data Requirements
[Table per Step 4]
#### Visualisation & Content Plan
[Chart plan + comparison table design + argument structure]

### 2...N. [Chapter Title]
...

## Research Task List
[Consolidate all P0/P1 data requirements across chapters into a deduplicated research checklist]
```

## Framework Quality Checklist

- [ ] Framework covers all natural analytical dimensions for the identified domain
- [ ] 2-4 named frameworks are selected, complementary, data-feasible, and explicitly mapped to chapters
- [ ] Each chapter has a clear Analysis Objective, Analysis Logic (referencing the chosen framework), and Core Hypothesis
- [ ] Data requirements are specific, measurable, and include actionable search keywords
- [ ] Every chapter has at least one visualisation plan with chart type and data mapping
- [ ] Data priorities (P0/P1/P2) are assigned realistically — P0 items are essential for core arguments
- [ ] The Research Task List is comprehensive and deduplicated

# From Framework to Report

Data collection happens via **ordinary research**: run the framework's search keywords through WebSearch/WebFetch, read user-supplied documents, and record findings per chapter — noting each source's title, URL, and access date. The report is then written against the phase-1 framework: chapters follow the skeleton, charts follow the visualisation plan, and every number traces to a collected source. If P0 data cannot be found, flag it explicitly in the report rather than filling the gap.

## Report Writing Guidance

**Structure**: Abstract → 1. Introduction → 2...N. Body chapters (from the skeleton) → N+1. Conclusion → N+2. References. Begin directly with `# Report Title`; no preamble, no horizontal rules (`---`).

**Per sub-chapter**, follow the **"Visual Anchor → Data Contrast → Integrated Analysis"** flow:
1. **Visual anchor**: the planned chart (or a comparison table where no chart applies)
2. **Data contrast table**: key metrics side by side — every number from collected data
3. **Integrated narrative**: "What → Why → So What", ending with a robust analytical paragraph (min. 200 words) that synthesises the findings into a strategic judgement; optionally close with a punchy one-liner in a blockquote (`>`)

**Insight depth**: every insight connects **Data → User Psychology → Strategy Implication** — not "Females are 60%, so target females", but what the number *implies* about motivation and what the business should therefore *do*.

**Rendering**: delegate chart and report rendering to the built-in **artifact-design** and **dataviz** skills — this skill specifies content and data mapping, not rendering mechanics.

**Consulting voice**: McKinsey/BCG tone — authoritative, objective, professional. **Bold** key viewpoints and numbers; English thousands separators (`1,000`). Headings use plain numbering (`1.`, `1.1`) with no "Chapter/Part/Section" prefixes; allowed tone words are Analysis, Profiling, Overview, Insights, Assessment — avoid "Decoding", "DNA", "Secrets", "Unlocking". The Conclusion is flowing prose (no bullets) with no new recommendations — those belong in the body chapters.

**Citations**: cite sources inline with title + URL + access date. If the client or target publication specifies a citation standard, follow that standard for the References section; otherwise a plain title/URL/access-date list is sufficient.

## Settings

```
output_locale = en_uk  # British English by default; configurable per user request
reasoning_locale = en
```
