# Phase 75: Matched Conventional Baseline Harness - Summary

**Completed:** 2026-04-20
**Status:** Complete
**Implementation commit:** `b7f32ce`

## What Changed

- Added `src/eml_symbolic_regression/baselines.py` with a row-oriented matched baseline harness.
- Added baseline adapters:
  - `eml_reference`,
  - `polynomial_least_squares`,
  - `pysr`,
  - `gplearn`,
  - `pyoperon`,
  - `karoo_gp`.
- Added a deterministic built-in conventional symbolic baseline:
  - fixed polynomial feature library,
  - least-squares fit on the train split,
  - SymPy candidate export,
  - verifier scoring across all split roles.
- Added fail-closed dependency checks for optional external SR adapters. Missing integrations emit `unavailable` rows instead of installing dependencies or disappearing from reports.
- Added baseline harness artifacts:
  - `manifest.json`,
  - `baseline-runs.json`,
  - `baseline-runs.csv`,
  - `baseline-report.md`,
  - `dependency-locks.json`.
- Added CLI command `baseline-harness`.
- Documented the matched baseline harness in `docs/IMPLEMENTATION.md`.

## Requirement Coverage

- `BASE-01`: Complete. The harness runs EML comparison controls and a conventional symbolic baseline over the same expanded dataset manifests, seeds, budgets, constants policies, and start-condition fields.
- `BASE-02`: Complete. External adapter dependencies are checked and locked, unavailable adapters fail closed, and every baseline row is explicitly excluded from EML recovery denominators.

## Verification

- Baseline harness tests passed.
- Dataset/proof manifest regression tests passed with the harness in place.
- CLI smoke checks passed for a small harness bundle and the default harness matrix.
- Existing CLI parser semantics-mode test still passes.
- `git diff --check` passed.

## Notes

- The built-in polynomial baseline is deliberately modest. It exercises the matched comparison contract without pretending to replace full PySR/gplearn style systems.
- Optional external SR systems remain unavailable locally and are reported as such. Phase 75 does not install or tune external runtimes.
