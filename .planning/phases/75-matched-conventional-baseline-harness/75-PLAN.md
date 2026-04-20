# Phase 75: Matched Conventional Baseline Harness - Plan

**Planned:** 2026-04-20
**Status:** Ready for execution

## Objective

Add a matched baseline harness that runs EML comparison controls and conventional symbolic baselines through one dataset/budget/seed/constants/start-condition contract, while fail-closing unavailable external integrations and preserving EML denominator separation.

## Tasks

### 1. Baseline Harness Module

- Add `src/eml_symbolic_regression/baselines.py`.
- Define adapter IDs, budget fields, output paths, and row serialization.
- Load expanded dataset splits and manifests from Phase 74.
- Emit manifest, JSON, CSV, Markdown, and dependency-lock artifacts.

### 2. Adapter Execution

- Add `eml_reference` adapter:
  - verifies clean dataset candidates where present,
  - respects constants policy by failing closed when a non-basis literal expression is requested under `basis_only`,
  - marks blind reference rows unsupported because reference candidates are not blind search evidence.
- Add `polynomial_least_squares` adapter:
  - runs only in `blind` + `literal_constants`,
  - fits a fixed polynomial symbolic feature library on the train split,
  - verifies the fitted candidate on all splits.
- Add optional external adapters:
  - `pysr`,
  - `gplearn`,
  - `pyoperon`,
  - `karoo_gp`;
  - missing dependencies must produce `unavailable` rows.

### 3. CLI

- Add `baseline-harness` command.
- Support dataset, adapter, seed, constants policy, start condition, points, tolerance, budget, output directory, and overwrite options.

### 4. Tests and Docs

- Add tests for direct harness execution and CLI output.
- Verify denominator separation and dependency-lock artifacts.
- Update implementation docs with the baseline harness contract.

## Acceptance Checks

- Harness can produce EML and conventional baseline rows from the same dataset manifests.
- Runnable conventional polynomial baseline completes and records final-confirmation metrics.
- Optional external SR adapters fail closed when dependencies are missing.
- Outputs include dependency/source locks and denominator policy.
- CLI can write the baseline harness artifact bundle.
