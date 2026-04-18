---
phase: 58-focused-evidence-and-artifact-contracts
plan: 01
status: complete
completed: 2026-04-18
requirements:
  - LOGI-04
  - LOGI-05
  - EVID-01
  - EVID-02
  - EVID-03
  - EVID-04
  - EVID-05
---

# Phase 58 Summary

## Outcome

Added focused v1.10 benchmark suites and committed campaign artifacts for the post-motif logistic and Planck compiler outcomes.

Both focused rows intentionally remain `unsupported` under the strict compile gate:

- Logistic relaxed compile depth is `15` with `exponential_saturation_template`, down from the archived relaxed depth `27`; strict depth `13` still fails, so no warm-start row is present.
- Planck relaxed compile depth is `14` with `low_degree_power_template`, `scaled_exp_minus_one_template`, and `direct_division_template`, down from the archived relaxed depth `20`; strict depth `13` still fails, so no warm-start row is present.

## Code Changes

- Registered `v1.10-logistic-evidence` and `v1.10-planck-diagnostics` in the built-in benchmark suite registry.
- Pointed these focused suites at `artifacts/campaigns` by default so CLI output lands under the milestone campaign paths.
- Clarified CLI `--output-dir` help text to state that suite outputs are written below `<root>/<suite-id>`.
- Added benchmark contract tests for compile-only suite contents, tags, default artifact roots, and no-recovery expectations.
- Added runner tests asserting the unsupported diagnostics, relaxed compile depths, node counts, macro hits, validation status, and aggregate classification.
- Added CLI tests that run both focused suites and assert suite, aggregate, and run artifacts are written with unsupported compile diagnostics.

## Artifacts

- `artifacts/campaigns/v1.10-logistic-evidence/`
  - `suite-result.json`
  - `aggregate.json`
  - `aggregate.md`
  - `v1-10-logistic-evidence-logistic-compile-c2af27a35e81.json`
- `artifacts/campaigns/v1.10-planck-diagnostics/`
  - `suite-result.json`
  - `aggregate.json`
  - `aggregate.md`
  - `v1-10-planck-diagnostics-planck-compile-795067919a97.json`

## Verification

```bash
PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py::test_logistic_v110_compile_benchmark_records_improved_unsupported_diagnostic tests/test_benchmark_runner.py::test_planck_v110_compile_benchmark_records_improved_unsupported_diagnostic tests/test_verifier_demos_cli.py::test_cli_benchmark_writes_v110_focused_campaign_artifacts -q
# 64 passed in 2.95s

PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py tests/test_benchmark_contract.py tests/test_benchmark_runner.py tests/test_verifier_demos_cli.py -q
# 137 passed, 4 warnings in 240.44s
```

The warnings are existing overflow warnings in training/verification paths covered by older tests.
