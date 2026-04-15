# Phase 19: Campaign Presets and Run Manifests - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning
**Mode:** Auto-generated in autonomous execution

<domain>
## Phase Boundary

This phase turns existing benchmark suites into named campaigns. It covers preset selection, budget-tier descriptions, versioned output folders, overwrite protection, run artifacts, aggregate reports, and a reproducibility manifest. CSV exports, plots, and final report assembly remain later phases.

</domain>

<decisions>
## Implementation Decisions

### Campaign Interface
- Add a `campaign` CLI command rather than expanding the lower-level `benchmark` command.
- Keep campaign presets small and explicit: `smoke`, `standard`, and `showcase`.
- Reuse benchmark suites and run filters so campaign execution does not fork benchmark semantics.
- Print the manifest and aggregate report paths at the end of a campaign run.

### Evidence Layout
- Write campaign outputs under `artifacts/campaigns/<label-or-timestamp>/`.
- Put raw per-run JSON artifacts below `runs/<suite-id>/`.
- Keep `suite-result.json`, `aggregate.json`, `aggregate.md`, and `campaign-manifest.json` at campaign root.
- Treat timestamped folders as the default safe rerun path and require `--overwrite` for stable labels.

### Runtime Guardrails
- `smoke` remains CI-scale and exercises one blind, one warm-start, and one unsupported diagnostic path.
- `standard` is the default showcase matrix and includes shallow blind baselines, Beer-Lambert perturbations, Michaelis-Menten, Planck, and selected FOR_DEMO formulas.
- `showcase` expands seeds and perturbations for presentation evidence while staying explicit about cost.

### the agent's Discretion
- The agent may add new built-in benchmark suites if that keeps presets declarative.
- The agent may include focused tests in this phase even though broader report tests land in Phase 23.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `benchmark.py` already has suite contracts, run filters, runner execution, aggregate JSON/Markdown generation, and code-version metadata.
- `cli.py` already exposes benchmark and demo commands with repeatable filter flags.
- Existing benchmark tests use temporary artifact roots and filtered smoke runs for fast coverage.

### Established Patterns
- Artifacts are JSON with stable schema strings and sorted, indented output.
- Built-in suite selection fails closed via `BenchmarkValidationError`.
- CLI commands return concise path-oriented summaries.

### Integration Points
- Campaigns should call `load_suite`, clone the suite with a campaign artifact root, then call `run_benchmark_suite` and `write_aggregate_reports`.
- Preset filters should reuse the existing `RunFilter` structure.

</code_context>

<specifics>
## Specific Ideas

Use `sources/FOR_DEMO.md` coverage by including selected FOR_DEMO cases in the standard preset without running an expensive external data campaign.

</specifics>

<deferred>
## Deferred Ideas

CSV exports, plots, and report narrative are deferred to Phases 20-22.

</deferred>
