---
phase: 89
status: passed
verified: 2026-04-22
---

# Phase 89 Verification

## Goal

Improve i*pi/GEML search enough to produce exact candidates on natural targets without exact formula leakage.

## Must-Haves

- Generic phase/log initializers are available for i*pi rows and recorded in manifests: verified by optimizer test.
- Initializer provenance records `generic_ipi_operator_primitive` and `formula_leakage: false`.
- v1.16 suites preserve matched raw/i*pi budgets except for the explicit i*pi initializer field.
- Existing v1.15 raw/i*pi suite budget matching still passes.
- Branch-safe declarations remain required for i*pi rows.

## Automated Checks

```bash
python -m pytest tests/test_optimizer_cleanup.py::test_optimizer_uses_generic_ipi_phase_initializer_without_formula_leakage tests/test_optimizer_cleanup.py::test_optimizer_runs_ipi_eml_with_branch_and_snap_metadata tests/test_benchmark_contract.py::test_v115_geml_oscillatory_suite_pairs_raw_and_ipi_budgets tests/test_benchmark_contract.py::test_v116_geml_suites_use_generic_ipi_initializers_and_match_raw_budgets tests/test_benchmark_contract.py::test_phase_initializers_fail_closed_for_raw_operator tests/test_campaign.py::test_campaign_presets_map_to_budgeted_suites -q
```

Result: passed, 6 tests.
