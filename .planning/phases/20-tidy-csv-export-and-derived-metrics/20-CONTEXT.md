# Phase 20: Tidy CSV Export and Derived Metrics - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning
**Mode:** Auto-generated in autonomous execution

<domain>
## Phase Boundary

This phase converts campaign aggregate evidence into flat CSV and JSON analysis artifacts. It covers run-level rows, grouped recovery summaries, headline metrics, and failed/unsupported case exports. Static charts and Markdown report narrative remain later phases.

</domain>

<decisions>
## Implementation Decisions

### Export Shape
- Put CSV and metric outputs under `tables/` inside each campaign folder.
- Keep one tidy `runs.csv` with one row per benchmark run.
- Write separate grouped CSVs for formula, start mode, perturbation noise, depth, and recovery/failure class.
- Write both JSON and CSV versions of headline metrics for machine and spreadsheet use.

### Metric Semantics
- Keep verifier-owned recovery separate from same-AST warm-start return.
- Keep unsupported and failed cases in all denominators.
- Export runtime from the source run artifact, not from aggregate inference.
- Include reason codes in failed/unsupported rows.

### the agent's Discretion
- Use the Python standard library CSV writer to avoid adding plotting or dataframe dependencies.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `aggregate_evidence` already normalizes run summaries and classifications.
- Run JSON artifacts already contain timing, training losses, verifier status, and perturbation slot changes.

### Established Patterns
- Existing reports keep explicit schema files and compact artifact directories.
- Tests use filtered smoke campaigns for fast, deterministic coverage.

### Integration Points
- `run_campaign` should call the table writer after aggregate generation and record table paths in the manifest.

</code_context>

<specifics>
## Specific Ideas

The table layer should feed both static plots and the final evidence report without requiring users to parse nested JSON.

</specifics>

<deferred>
## Deferred Ideas

Chart rendering and narrative interpretation are deferred to Phases 21 and 22.

</deferred>
