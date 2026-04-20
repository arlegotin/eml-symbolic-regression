# Phase 73: Basis-Only and Literal-Constants Benchmark Tracks - Plan

**Planned:** 2026-04-20
**Status:** Ready for execution

## Objective

Make paper-faithful basis-only and applied literal-constant benchmark tracks explicit in suite definitions, run artifacts, aggregate reports, campaign presets, tests, and docs.

## Tasks

### 1. Benchmark Track Schema

- Add track constants and validation to `benchmark.py`.
- Thread track metadata through `BenchmarkCase`, `BenchmarkRun`, run artifacts, and summaries.
- Ensure compiler runs use the run's declared constants policy.

### 2. v1.13 Track Suites

- Add publication target inventory.
- Add built-in suites:
  - `v1.13-paper-basis-only`
  - `v1.13-paper-literal-constants`
  - `v1.13-paper-tracks`
- Preserve legacy suite behavior and run IDs where possible.

### 3. Aggregate Separation

- Add aggregate groups for `benchmark_track` and `constants_policy`.
- Add a top-level per-track summary with separate totals, recovered counts, unsupported counts, failed counts, and recovery rates.
- Render track separation in aggregate Markdown.

### 4. Campaign and CLI Surface

- Add a campaign preset for the combined v1.13 track suite.
- Ensure `list-benchmarks` and `list-campaigns` expose the new track suites without new CLI syntax.

### 5. Tests and Docs

- Add/extend tests for suite inventory, track metadata, aggregate denominator separation, and basis-only compile fail-closed behavior.
- Update `docs/IMPLEMENTATION.md` with the v1.13 track contract.

## Acceptance Checks

- Every publication target has a basis-only and literal-constants run configuration.
- Basis-only rows cannot silently use literal constants.
- Literal rows declare constants policy, literal catalog, and warm-start/scaffold status.
- Mixed-track aggregate reports expose separate denominators.
- Focused benchmark and campaign tests pass.
