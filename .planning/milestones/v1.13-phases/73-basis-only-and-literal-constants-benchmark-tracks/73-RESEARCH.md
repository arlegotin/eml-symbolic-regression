# Phase 73: Basis-Only and Literal-Constants Benchmark Tracks - Research

**Researched:** 2026-04-20
**Status:** Complete

## Current Benchmark Model

`benchmark.py` has the right centralization point: `BenchmarkCase` expands into `BenchmarkRun`, `execute_benchmark_run()` writes one artifact per run, and `aggregate_evidence()` derives publication-facing summaries from those run artifacts. Adding track metadata here avoids parallel schemas.

## Existing Constants Support

`OptimizerBudget.constants` already supports literal terminal banks and stable JSON serialization. The compiler already supports `CompilerConfig.constant_policy` values `basis_only` and `literal_constants`. The missing connection is that benchmark runs do not carry a constants policy, and `_compile_demo()` always uses `literal_constants`.

## Existing Suite Boundaries

The current v1.11 paper suites mix evidence regimes:

- `v1.11-paper-training`: pure blind, scaffolded blind, warm-start scientific-law rows, and perturbed-basin rows.
- `v1.11-logistic-planck-probes`: compile diagnostics and literal-constant blind probes.

Those are useful historical suites, but v1.13 needs explicit track-denominator suites so paper-faithful and applied literal evidence are not conflated.

## Reporting Surface

Aggregate JSON and Markdown are the right reporting surface for denominator separation. The current report already includes groups by formula/start mode/evidence class, so adding `benchmark_track`, `constants_policy`, and a top-level `tracks` summary fits the existing report style.

## Test Strategy

Focused tests should validate schema and denominator contracts without running a full campaign:

- built-in suite inventory contains v1.13 track suites,
- every declared publication target appears in both `basis_only` and `literal_constants`,
- basis-only track has no non-1 optimizer constants and uses compiler `basis_only`,
- literal track declares literal catalogs and compiler `literal_constants`,
- aggregate output separates totals by track,
- a basis-only compile row fails closed on a literal-coefficient formula rather than silently using literal constants.

## Risks

- Adding fields to dataclasses can perturb run IDs. That is acceptable for new v1.13 track suites, but existing suite run IDs should not change unless track metadata is included for legacy suites. To preserve legacy IDs, track metadata should be excluded from run-ID hashing when it is the default inferred basis-only legacy contract.
- Some literal-constant targets may still be unsupported because of depth or compiler coverage. Track infrastructure must report unsupported status rather than promote loss-only rows.

