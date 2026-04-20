# Phase 73: Basis-Only and Literal-Constants Benchmark Tracks - Summary

**Completed:** 2026-04-20
**Status:** Complete
**Implementation commit:** `994dbaf`

## What Changed

- Added explicit benchmark track metadata:
  - `basis_only`
  - `literal_constants`
- Threaded track metadata through:
  - `BenchmarkCase`
  - `BenchmarkRun`
  - run artifacts
  - suite serialization
  - aggregate run summaries
  - aggregate Markdown reports.
- Made compile benchmark rows use the run's declared constants policy instead of always using `literal_constants`.
- Added publication target inventory and v1.13 built-in suites:
  - `v1.13-paper-basis-only`
  - `v1.13-paper-literal-constants`
  - `v1.13-paper-tracks`
- Added a `paper-tracks` campaign preset for the combined v1.13 suite.
- Added aggregate track-denominator summaries and groups for `benchmark_track` and `constants_policy`.
- Documented the v1.13 benchmark track contract in `docs/IMPLEMENTATION.md`.

## Requirement Coverage

- `TRACK-01`: Complete. Every declared publication benchmark target has a `basis_only` run configuration using compiler `basis_only` policy and no non-1 literal terminal constants.
- `TRACK-02`: Complete. Every declared publication benchmark target has a `literal_constants` run configuration with literal catalog, constants policy, start mode, warm-start status, and scaffold status exposed in artifacts.
- `TRACK-03`: Complete. Aggregate JSON and Markdown now report separate track denominators, plus groups by benchmark track and constants policy.

## Verification

- Benchmark contract, aggregate report, and campaign preset tests passed.
- Focused runner tests passed for:
  - basis-only fail-closed compile behavior,
  - existing logistic compile diagnostics,
  - existing Planck compile diagnostics.
- The broader touched benchmark/campaign/CLI test set passed before the final additive `warm_start_status` payload field; focused serialization and report tests were rerun after that addition.
- Filtered CLI smoke runs passed for both:
  - literal-constant `exp` warm-start row,
  - basis-only Beer-Lambert compile row failing closed as unsupported.
- `git diff --check` passed.

## Notes

- Existing legacy suites keep their historical literal-capable compiler behavior by default. The new v1.13 suites are the strict track-denominator contract.
- Phase 73 does not regenerate the full v1.13 evidence package. Phase 76 remains responsible for running the publication campaign and claim audit over the new track suites.
