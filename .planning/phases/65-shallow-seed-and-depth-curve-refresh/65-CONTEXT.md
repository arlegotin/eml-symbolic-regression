# Phase 65: Shallow Seed and Depth-Curve Refresh - Context

**Gathered:** 2026-04-19
**Status:** Ready for planning
**Mode:** Auto-generated smart discuss for autonomous execution

<domain>
## Phase Boundary

Add small current-code evidence refreshes for shallow pure-blind/scaffolded seeds and depth 2-5 degradation, with regime separation and source-table outputs for later paper figures.

</domain>

<decisions>
## Implementation Decisions

### Refresh Scope
- Add five new pure-blind shallow seeds and five new scaffolded shallow seeds for the cheap `exp` shallow case.
- Use seeds 2 through 6 so the refresh extends the v1.11 seed set rather than duplicating seeds 0 and 1.
- Keep pure-blind rows scaffold-free and scaffolded rows under the normal scaffold initializer path.
- Run the depth refresh as the current-code `proof-depth-curve` depth 2-5 blind subset with two seeds per depth.

### Artifact Shape
- Store refresh outputs under `artifacts/campaigns/v1.12-evidence-refresh/`.
- Write suite definitions, suite results, aggregate JSON/Markdown, compact run tables, depth summary tables, and a manifest.
- Preserve the original `proof-depth-curve` suite id for depth rows so existing proof-claim validation remains valid.
- Label the refresh as current-code v1.12 evidence and keep archived v1.6 depth rows as historical context only.

### the agent's Discretion
- Choose helper names and table columns that align with existing benchmark aggregate conventions.
- Keep tests focused on suite construction and table shape so the full training refresh is not run in normal unit tests.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `benchmark.py` provides `BenchmarkSuite`, `BenchmarkCase`, `run_benchmark_suite`, `write_aggregate_reports`, and built-in `proof-depth-curve`.
- Existing `v1.11-paper-training` covers only 8 current-code training rows and uses seeds 0 and 1 for shallow exp pure-blind/scaffolded rows.
- `paper_assets.py` already consumes aggregate tables for paper figures.

### Established Patterns
- Benchmark artifacts write run-level JSON, aggregate JSON/Markdown, and grouped tables.
- Evidence classes are derived from execution payloads, not supplied by suite JSON.
- Source paths and reproduction commands are recorded in manifests.

### Integration Points
- Extend `paper_v112.py` with refresh suite builders and a runner.
- Add a `paper-refresh` CLI command.
- Add tests in `tests/test_paper_v112.py`.

</code_context>

<specifics>
## Specific Ideas

- The acceptance target is at least five new pure-blind and five new scaffolded shallow seeds, plus depth 2, 3, 4, and 5 with two seeds each.
- If a run fails, record it in the aggregate rather than hiding it.

</specifics>

<deferred>
## Deferred Ideas

- Paper-facing figures and captions using these rows are Phase 66.
- Source-locking these rows into the package manifest is Phase 68.

</deferred>
