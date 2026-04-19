# Phase 60 Verification

## Commands

```bash
PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_campaign.py -q
PYTHONPATH=src python -m eml_symbolic_regression.cli campaign paper-training --label v1.11-paper-training --overwrite
PYTHONPATH=src python -m eml_symbolic_regression.cli campaign paper-probes --label v1.11-logistic-planck-probes --overwrite
PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_campaign.py tests/test_benchmark_runner.py -q
```

## Results

- Benchmark/campaign contract tests: 82 passed.
- `paper-training` campaign generated successfully.
- `paper-probes` campaign generated successfully.
- Runner regression suite: 118 passed, 3 warnings.

## Warning Notes

The runner suite and Planck probe emitted expected overflow warnings from exponentials in failed/unsupported probe paths:

- `semantics.py`: overflow encountered in `exp`.
- `verify.py`: overflow encountered in `square`.

These warnings correspond to failed or unsupported diagnostic rows and were not counted as recovery.

## Artifact Checks

- `artifacts/campaigns/v1.11-paper-training/aggregate.json`: 8 total, 8 verifier recovered.
- `artifacts/campaigns/v1.11-logistic-planck-probes/aggregate.json`: 4 total, 0 verifier recovered, 2 unsupported, 2 failed.
- Logistic and Planck remained unsupported/stretch diagnostics.
