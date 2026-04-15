# Research Summary: v1.3 Benchmark Campaign and Evidence Report

**Project:** EML Symbolic Regression
**Domain:** Benchmark campaign reporting, CSV export, and static visualization for EML recovery evidence
**Recorded:** 2026-04-15
**Research decision:** External research skipped. This milestone is a local evidence/reporting milestone based on the current benchmark harness, existing artifacts, `sources/paper.pdf`, `sources/NORTH_STAR.md`, and `sources/FOR_DEMO.md`.

## Executive Summary

v1.3 should convert the v1.2 benchmark harness from "can measure" into "can showcase." The milestone should run a real campaign, export tidy data, generate static figures, and assemble a report that answers the user's real question: how do the original paper's EML ideas perform in practice?

The report must preserve the existing honesty contract. A polished graph should never merge blind recovery with same-AST warm-start return, and unsupported/depth-gated formulas should remain visible rather than hidden.

## Stack Additions

- Keep JSON and Markdown as first-class report artifacts.
- Add standard-library CSV export for tabular analysis.
- Add a lightweight static plotting dependency during implementation, likely `matplotlib`, unless a no-dependency SVG approach proves sufficient during planning.
- Avoid notebook-only workflows; the CLI should generate reproducible artifacts directly.

## Feature Table Stakes

- Campaign presets for `smoke`, `standard`, and `showcase` budget levels.
- Versioned output folders containing raw run artifacts, aggregate JSON, CSV exports, figures, and `report.md`.
- CSV tables for run-level metrics, grouped recovery rates, loss summaries, perturbation sweeps, runtime/depth, and failure taxonomy.
- Static plots for recovery rate by formula/mode, best loss versus post-snap loss, Beer-Lambert perturbation sensitivity, runtime/depth, and unsupported/failure breakdown.
- A concise narrative report explaining what works, what is promising, what fails, and what should be improved next.

## Watch Out For

- Do not let graph polish obscure weak results.
- Do not count same-AST warm-start returns as blind discovery.
- Do not require a long campaign in ordinary tests; use smoke fixtures and synthetic mini data for CI.
- Do not tune the optimizer inside this milestone; use the campaign to create the scoreboard first.
- Keep output deterministic enough that future optimizer milestones can compare "before vs after" cleanly.

## Recommended Phase Shape

1. Campaign presets and run manifests.
2. CSV export and derived metrics.
3. Plot generation.
4. Report assembly.
5. Campaign smoke/full-run documentation and lockdown.

---
*Research decision recorded: 2026-04-15*
