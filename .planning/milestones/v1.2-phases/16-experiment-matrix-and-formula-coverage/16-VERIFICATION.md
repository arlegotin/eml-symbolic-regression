status: passed

# Phase 16 Verification

The v1.2 experiment matrix now covers shallow blind baselines, Beer-Lambert perturbation robustness, Michaelis-Menten/Planck diagnostics, and selected FOR_DEMO formulas.

| Requirement | Status | Evidence |
|-------------|--------|----------|
| MATR-01 | passed | `v1.2-evidence` includes blind-start baselines for `exp`, `log`, and `radioactive_decay`. |
| MATR-02 | passed | `beer-perturbation-sweep` expands 3 seeds across perturbation noise values `0.0`, `5.0`, and `35.0`. |
| MATR-03 | passed | `michaelis-warm-diagnostic` runs through warm-start routing and records unsupported/depth outcomes when gates block training. |
| MATR-04 | passed | `for-demo-diagnostics` covers Beer-Lambert, radioactive decay, Michaelis-Menten, logistic, Shockley, damped oscillator, and Planck as recovery/diagnostic/stretch cases. |

## Verification Commands

- `python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py -q` passed with 10 tests.
- `PYTHONPATH=src python -m eml_symbolic_regression.cli list-demos | sort` listed the new `radioactive_decay` target.
