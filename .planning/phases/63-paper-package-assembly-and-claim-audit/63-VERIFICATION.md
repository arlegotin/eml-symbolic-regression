# Phase 63 Verification

## Commands

```bash
PYTHONPATH=src python -m pytest tests/test_paper_package.py tests/test_raw_hybrid_paper.py tests/test_paper_assets.py -q
PYTHONPATH=src python -m eml_symbolic_regression.cli paper-package --output-dir artifacts/paper/v1.11 --overwrite
PYTHONPATH=src python -m pytest tests/test_paper_package.py tests/test_raw_hybrid_paper.py tests/test_paper_assets.py tests/test_paper_diagnostics.py tests/test_benchmark_contract.py tests/test_campaign.py tests/test_benchmark_runner.py tests/test_verifier_demos_cli.py -q
```

## Results

- Package, raw-hybrid, and asset tests: 25 passed.
- Final package command completed successfully.
- Claim audit status: passed.
- Impacted regression set: 156 passed, 3 expected overflow warnings.
- Full `PYTHONPATH=src python -m pytest -q` was attempted and reached 85% with no failures before stalling in a slow tail; it was stopped and replaced by the impacted regression set above.

## Artifact Checks

`artifacts/paper/v1.11/claim-audit.json` reports:

- 7 passed checks,
- 0 failed checks,
- 67 source-lock rows.

`artifacts/paper/v1.11/paper-readiness.md` records:

- v1.11 paper-training: 8/8 verifier-recovered.
- Logistic/Planck probes: 0/4 recovered, 2 unsupported, 2 failed.
- Logistic motif depth: 27 -> 15, still unsupported.
- Planck motif depth: 24 -> 14, still unsupported.
- 7 figures and 7 source tables.

## Claim Checks

- Logistic and Planck remain unsupported in the final audit.
- No recovery claim is derived from loss-only fields.
- Regime denominators remain suite/start-mode-local.
- Baseline diagnostics remain prediction-only.
