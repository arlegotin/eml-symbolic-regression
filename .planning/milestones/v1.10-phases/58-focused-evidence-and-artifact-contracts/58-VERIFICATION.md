---
phase: 58-focused-evidence-and-artifact-contracts
status: pass
verified: 2026-04-18
---

# Phase 58 Verification

## Requirement Checks

| Requirement | Verdict | Evidence |
|-------------|---------|----------|
| LOGI-04 | PASS | `v1.10-logistic-evidence` records strict unsupported compile status; no warm-start is attempted because strict support did not exist. |
| LOGI-05 | PASS | Logistic focused artifact records `unsupported`, strict `depth_exceeded`, relaxed depth `15`, and no warm-start promotion. |
| EVID-01 | PASS | Built-in suite `v1.10-logistic-evidence` contains compile-only `logistic-compile` because strict support is unavailable. |
| EVID-02 | PASS | Built-in suite `v1.10-planck-diagnostics` contains compile-only `planck-compile` because strict support is unavailable. |
| EVID-03 | PASS | CLI wrote artifacts to `artifacts/campaigns/v1.10-logistic-evidence/` and `artifacts/campaigns/v1.10-planck-diagnostics/`. |
| EVID-04 | PASS | Run artifacts record status, strict reason, relaxed depth, node count, macro hits, validation status, and aggregate unsupported classification. |
| EVID-05 | PASS | Focused contract, runner, CLI, baseline preservation, motif improvement, and fail-closed coverage pass in the requested test files. |

## Measured Outcomes

| Law | Strict Status | Strict Reason | Relaxed Depth | Node Count | Macro Hits |
|-----|---------------|---------------|---------------|------------|------------|
| logistic | unsupported | depth_exceeded | 15 | 49 | `exponential_saturation_template` |
| Planck | unsupported | depth_exceeded | 14 | 59 | `low_degree_power_template`, `scaled_exp_minus_one_template`, `direct_division_template` |

## Commands

```bash
PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py::test_logistic_v110_compile_benchmark_records_improved_unsupported_diagnostic tests/test_benchmark_runner.py::test_planck_v110_compile_benchmark_records_improved_unsupported_diagnostic tests/test_verifier_demos_cli.py::test_cli_benchmark_writes_v110_focused_campaign_artifacts -q
# 64 passed in 2.95s

PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark v1.10-logistic-evidence
# v1.10-logistic-evidence: 1 runs, 1 unsupported, 0 failed -> artifacts/campaigns/v1.10-logistic-evidence/suite-result.json; aggregate -> artifacts/campaigns/v1.10-logistic-evidence/aggregate.md

PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark v1.10-planck-diagnostics
# v1.10-planck-diagnostics: 1 runs, 1 unsupported, 0 failed -> artifacts/campaigns/v1.10-planck-diagnostics/suite-result.json; aggregate -> artifacts/campaigns/v1.10-planck-diagnostics/aggregate.md

PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py tests/test_benchmark_contract.py tests/test_benchmark_runner.py tests/test_verifier_demos_cli.py -q
# 137 passed, 4 warnings in 240.44s
```

## Residual Risk

Planck is now one depth level above the strict compile gate (`14` versus `13`), but it remains unsupported as required. Logistic is still two levels above the strict compile gate (`15` versus `13`), so warm-start evidence is explicitly absent.
