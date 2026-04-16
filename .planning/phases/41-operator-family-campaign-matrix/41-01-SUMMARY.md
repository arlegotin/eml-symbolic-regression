# Phase 41 Summary: Operator-Family Campaign Matrix

**Status:** Complete
**Completed:** 2026-04-16
**Requirements:** EVD-01, EVD-02

## Delivered

- Added v1.7 operator-family benchmark suites for:
  - `v1.7-family-smoke`
  - `v1.7-family-shallow-pure-blind`
  - `v1.7-family-shallow`
  - `v1.7-family-basin`
  - `v1.7-family-depth-curve`
  - `v1.7-family-standard`
  - `v1.7-family-showcase`
- Added reusable family variants: raw EML, fixed `CEML_2`, fixed `ZEML_2`, and scheduled `ZEML_8 -> ZEML_4`.
- Cloned proof-style suites into v1.7 family matrices without reusing v1.5 proof thresholds or claim IDs.
- Added v1.7 family campaign presets for smoke, shallow, basin, depth-curve, standard, and showcase comparisons.
- Preserved raw variants as baseline rows while centered warm-start and perturbed-tree rows remain explicit fail-closed diagnostics until same-family seeds exist.

## Verification

```bash
python -m pytest tests/test_benchmark_contract.py tests/test_campaign.py tests/test_benchmark_runner.py::test_runner_executes_operator_family_smoke_matrix
```

Result: `72 passed`.

## Notes

- Family matrix suites use new v1.7 suite IDs and campaign preset names, so running them does not overwrite archived v1.5/v1.6 proof or campaign artifacts.
- Centered scaffolded clones drop the raw `scaled_exp` scaffold initializer because that initializer embeds raw EML witness trees.
