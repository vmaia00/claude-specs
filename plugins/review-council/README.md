# review-council

An **always-on, multi-persona code-review pipeline** for Claude Code. Every review spins up a
full panel of distinct-angle reviewer subagents — no sampling, no tier-skipping, no token
optimization. Depth is the point.

## The flow

```
                 ┌─ Panel R1 (review the diff) ─┐
   diff  ─────►  │  9 isolated persona reviewers │ ─► finding-verifier ─► Code Review
                 └───────────────────────────────┘    (falsify each)      Master ─► solution.md
                                                                                       │
                 ┌─ Panel R2 (review the Solution) ─┐                                  ▼
 solution.md ◄── │  contrarian + adversarial lanes  │ ─► finding-verifier ─► Code Review Master 2
                 └──────────────────────────────────┘    (falsify each)      ─► verdict.md + fix work-list
                                                                                       │
                                                                          (only with --fix) ▼
                                                                              Code Executor & Fixer
                                                                              ─► apply ─► bounded
                                                                                 re-review-after-fix
```

1. **Persona Panel R1** — distinct-angle reviewers run in parallel, each isolated (sees only the
   diff + its own brief). An adversarial **verifier** then tries to falsify every finding.
2. **Code Review Master** — dedupes by root cause, ranks, preserves minority/high-severity
   findings, and synthesizes one coherent **Solution**.
3. **Persona Panel R2** — a *different*, deliberately adversarial set re-reviews the Solution.
4. **Code Review Master 2** — produces the final verdict + a ranked **fix work-list**.
5. **Code Executor & Fixer** — *opt-in* (`--fix`): applies only the work-list items, keeps tests
   green, then re-reviews the patch in a bounded loop. **Never commits or pushes.**

## Usage

```
/review-council:deep-review              # review the local uncommitted diff
/review-council:deep-review --pr 123     # review a GitHub PR
/review-council:deep-review --fix        # also apply the agreed fixes to the working tree
```

Artifacts for each run are written under `.claude/deep-review/<run>/`
(`findings-r1.json` → `solution.md` → `findings-r2.json` → `verdict.md` → `fix-report.md`).

## What's inside

- **1 command** — `deep-review` (the orchestrator).
- **13 agents** — 9 panelist personas + an adversarial verifier + the Code Review Master +
  the contrarian + the Fixer.
- **1 skill** — `deep-review` (`SKILL.md` + `REFERENCE.md`): the pipeline contract, the unified
  finding schema, the persona briefs, and the failure-mode guards.

Every agent is `model: inherit` and least-privilege (reviewers are read-only; only the Fixer
writes). See `THIRD-PARTY-NOTICES.md` for the seven panelists adapted from ECC (MIT).

## Design notes

The pipeline is **independent-fan-out, not debate**: panelists never see each other (research
shows same-model debate conforms to the modal answer and votes out correct minority findings).
The verifier and the recall-biased Master are the precision levers; the always-on panel is the
recall lever. See `skills/deep-review/REFERENCE.md` for the rationale and the per-stage contract.
