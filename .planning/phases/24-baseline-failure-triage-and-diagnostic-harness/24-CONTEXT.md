# Phase 24: Baseline Failure Triage and Diagnostic Harness - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase turns the committed v1.3 `standard` and `showcase` campaign artifacts into reusable diagnostics. It adds structured triage, immutable baseline fingerprints, and focused rerun commands for blind failures, Beer-Lambert perturbation failures, and compiler/depth gates. It does not change optimizer, warm-start, compiler, or verifier behavior.

</domain>

<decisions>
## Implementation Decisions

### Diagnostic Scope
- Use only committed campaign artifacts under `artifacts/campaigns/v1.3-standard/` and `artifacts/campaigns/v1.3-showcase/` as the baseline source of truth.
- Keep failure classes aligned with the existing `classification` taxonomy: `snapped_but_failed`, `soft_fit_only`, `failed`, `unsupported`, and `execution_failure`.
- Include raw artifact paths and scalar metrics in the triage output so every summarized failure can be audited.
- Store baseline file fingerprints and counts in a lock artifact instead of mutating v1.3 campaign folders.

### Rerun Harness
- Add focused rerun filters on top of existing benchmark/campaign machinery rather than creating a separate runner.
- Add perturbation-noise filtering because Beer-Lambert diagnostics need exact noise-level subsets.
- Make commands reproducible from a clean checkout with `PYTHONPATH=src python -m eml_symbolic_regression.cli ...`.
- Keep full `standard` and `showcase` campaigns available; focused diagnostics are subsets, not replacements.

### the agent's Discretion
Implementation details, output naming, and report formatting are at the agent's discretion as long as they preserve v1.3 baseline immutability and use existing artifact schemas.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/eml_symbolic_regression/benchmark.py` already expands suites, runs filtered subsets, aggregates evidence, and classifies runs.
- `src/eml_symbolic_regression/campaign.py` already writes manifests, CSV tables, SVG figures, and reports.
- `src/eml_symbolic_regression/cli.py` already exposes benchmark and campaign filters for formula, mode, case, and seed.

### Established Patterns
- Evidence artifacts are JSON-first with deterministic Markdown/CSV projections.
- Recovery claims are verifier-owned and represented through `claim_status`, `status`, `classification`, and metrics fields.
- Campaign outputs are guarded by label/overwrite behavior.

### Integration Points
- Extend `RunFilter` and campaign CLI filtering for perturbation noise.
- Add a diagnostics module consumed by a new CLI subcommand.
- Add tests beside campaign/benchmark report tests.

</code_context>

<specifics>
## Specific Ideas

Use `artifacts/campaigns/v1.3-standard/aggregate.json` and `artifacts/campaigns/v1.3-showcase/aggregate.json` for triage. Link each row back to the raw `runs/<suite>/*.json` path and include metrics such as `best_loss`, `post_snap_loss`, `snap_min_margin`, `changed_slot_count`, and `verifier_status`.

</specifics>

<deferred>
## Deferred Ideas

Optimizer, warm-start, and compiler improvements are intentionally deferred to phases 25-27.

</deferred>
