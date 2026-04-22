# Phase 92: Ablations, Failure Taxonomy, and Paper Figures - Context

**Gathered:** 2026-04-22
**Status:** Ready for planning

<domain>
## Phase Boundary

Produce reviewer-facing v1.16 ablation and figure assets from the source-locked pilot campaign and budget ladder. Do not rerun training or relax the Phase 88 exact-recovery gate.

</domain>

<decisions>
## Implementation Decisions

### Evidence Source
- Use `artifacts/campaigns/v1.16-geml-pilot/` as the measured campaign source.
- Use `artifacts/campaigns/v1.16-geml-budget-ladder/` for fail-closed routing and failure-taxonomy source rows.
- Write Phase 92 artifacts under `artifacts/paper/v1.16-geml/ablations/` so Phase 93 can bundle them into the final package.

### Ablation Interpretation
- Rows must distinguish measured variants from not-run controls.
- Initialization, branch behavior, constants, depth, budget, and candidate pooling should be represented explicitly.
- Loss-only rows remain diagnostic and must not be counted as exact recovery.

### Figures
- Figures should be deterministic SVGs generated from campaign tables.
- Include family recovery, loss before/after snap, branch anomalies, runtime, and representative failure/fit panels.
- Because the pilot found no verified exact recoveries, representative curves should label failures honestly rather than implying fitted recovery.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `paper_v116.py` already provides v1.16 paths, source-lock helpers, campaign row readers, taxonomy generation, and deterministic JSON/CSV/Markdown writers.
- `cli.py` already exposes v1.16 package and ladder commands.
- `tests/test_paper_v116.py` is the active focused v1.16 test module.

### Inputs Available
- `tables/geml-paired-comparison.csv` includes paired raw/i*pi outcomes, MSEs, branch counts, and runtime.
- `tables/runs.csv` and run JSON artifacts include candidate-pool counts, branch diagnostics, optimizer timing, and verification failure classes.
- `failure-taxonomy.json` from Phase 90 already maps paired rows to failure classes and actionable next steps.

</code_context>

<specifics>
## Specific Ideas

Add `write_v116_ablation_assets` plus a `geml-v116-ablations` CLI command. The writer should produce JSON/CSV/Markdown tables, deterministic SVGs, figure metadata, source locks, and a manifest.

</specifics>

<deferred>
## Deferred Ideas

Do not run expensive ablation campaigns after the pilot gate blocked full execution. Not-run ablation variants should remain visible as blocked/unmeasured controls.

</deferred>
