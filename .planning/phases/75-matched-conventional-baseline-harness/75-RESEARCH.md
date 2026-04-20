# Phase 75: Matched Conventional Baseline Harness - Research

**Researched:** 2026-04-20
**Status:** Complete

## Existing Baseline State

The repo already has EML benchmark suites and campaign reports. Those suites produce EML recovery evidence and must keep their denominators separate from baseline comparisons. A previous v1.12 paper probe checks whether `pysr`, `gplearn`, `pyoperon`, and `karoo_gp` are importable, but it deliberately does not run matched-budget baselines.

## Local Dependency Check

Current local import check:

- `pysr`: missing,
- `gplearn`: missing,
- `pyoperon`: missing,
- `karoo_gp`: missing,
- `sklearn`: available,
- `scipy`: available.

Phase 75 should not install new dependencies. Optional external SR adapters should write explicit unavailable rows and dependency locks when imports fail.

## Harness Shape

The Phase 74 expanded dataset registry is the right input surface because manifests already include:

- split roles,
- units,
- noise policy,
- source/generator,
- domain constraints,
- synthetic/semi-synthetic/real classification,
- compatibility tags.

The harness should produce row-level artifacts keyed by dataset, adapter, seed, constants policy, and start condition. Each row should carry the same budget fields and dataset manifest hash so comparisons can be filtered or audited later.

## Runnable Conventional Baseline

A deterministic least-squares symbolic polynomial baseline is small enough for Phase 75:

- build a fixed feature library from variables: constant, linear terms, squared terms, and pairwise products,
- fit coefficients on the training split with `numpy.linalg.lstsq`,
- export a SymPy expression through `SympyCandidate`,
- score it with the existing verifier over all splits.

This gives a real conventional symbolic row without claiming parity with full SR packages. It also catches split, unit, manifest, and final-confirmation plumbing issues that unavailable external adapters cannot exercise.

## Test Strategy

- Run the harness on a small dataset subset with `eml_reference`, `polynomial_least_squares`, and one missing external adapter.
- Assert rows share dataset manifest hashes, seeds, constants policy, start condition, and budget fields.
- Assert the polynomial baseline completes under `literal_constants` and records final-confirmation metrics.
- Assert external adapter rows are `unavailable`, dependency-checked, source-locked, and excluded from EML denominators.
- Assert CLI writes the manifest, JSON, CSV, Markdown, and dependency-lock artifacts.
