# Phase 74: Expanded Dataset and Manifest Suite - Context

**Gathered:** 2026-04-20
**Status:** Ready for planning
**Mode:** Autonomous smart-discuss equivalent

<domain>
## Phase Boundary

Phase 74 expands evidence inputs beyond normalized noiseless synthetic demo splits. The goal is a dataset registry and manifest contract that can describe noisy synthetic sweeps, parameter-identifiability stress, multivariable formulas, unit-aware formulations, and at least one real dataset path with independent splits.

</domain>

<decisions>
## Implementation Decisions

### Registry First

Add an expanded dataset registry in `datasets.py` instead of scattering new fixtures across benchmark, paper, and diagnostics modules. The registry should produce `DataSplit` objects and machine-readable manifests.

### Real Data Fixture

Use a small committed Hubble 1929 velocity-distance CSV fixture with source metadata. It is real observational data used only as broader-data evidence, not as a controlled symbolic-recovery claim.

### Compatibility

Expanded datasets should be compatible with verifier and future benchmark/baseline routing. Phase 74 does not need to run the full campaign over every dataset; Phase 76 owns the final evidence rebuild.

</decisions>

<code_context>
## Existing Code Insights

- `src/eml_symbolic_regression/datasets.py` currently defines `DemoSpec`, demo split generation, and `proof_dataset_manifest()`.
- `DataSplit` already supports multiple variables, roles, and domain metadata.
- Benchmark execution currently uses `DatasetConfig(points, tolerance)` and `proof_dataset_manifest()`.
- Phase 73 added explicit benchmark track metadata, so expanded dataset manifests should declare compatibility with benchmark-track denominators rather than duplicating that schema.
- CLI already has `list-demos` and `proof-dataset`; Phase 74 can add list/write commands for expanded dataset manifests.

</code_context>

<specifics>
## Specific Ideas

- Add `ExpandedDatasetSpec` with split generation and manifest methods.
- Add dataset families:
  - noisy Beer-Lambert sweep,
  - Michaelis-Menten parameter-identifiability stress,
  - multivariable Arrhenius surface,
  - unit-aware Ohm law,
  - real Hubble 1929 velocity-distance fixture.
- Add `list-datasets` and `dataset-manifest` CLI commands.
- Add tests for manifest fields, real data path loading, split independence, multivariable verifier compatibility, and CLI output.

</specifics>

<deferred>
## Deferred Ideas

- Full benchmark campaign execution over expanded datasets remains Phase 76.
- Matched external baselines over expanded datasets remain Phase 75.
- New data visualizations or publication tables are deferred until the final evidence package.

</deferred>
