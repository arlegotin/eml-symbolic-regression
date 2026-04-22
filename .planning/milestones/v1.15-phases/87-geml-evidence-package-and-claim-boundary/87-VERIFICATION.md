status: passed

# Phase 87 Verification

## Result

Passed. The v1.15 GEML package now locks the restricted theory note, benchmark manifests, smoke paired campaign outputs, target-family classification, source hashes, reproduction commands, and claim-boundary audit.

## Requirements Checked

- **EVID-03:** Target-family classification reports declared targets, paired rows, recovery wins, neutral/loss-only outcomes, and negative-control rows.
- **EVID-04:** Claim audit fails on global-superiority, broad blind-recovery, and full-universality phrasing, and requires both matched protocol and restricted-theory context.
- **EVID-05:** Final package includes theory links, benchmark manifests, aggregate tables, source locks, reproduction commands, and a bounded decision.

## Generated Evidence

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli campaign geml-oscillatory-smoke --label v1.15-geml-oscillatory-smoke --overwrite
# campaign -> artifacts/campaigns/v1.15-geml-oscillatory-smoke

PYTHONPATH=src python -m eml_symbolic_regression.cli geml-package --campaign-dir artifacts/campaigns/v1.15-geml-oscillatory-smoke --overwrite
# audit passed; decision -> inconclusive_smoke_only
```

The smoke package has 2 paired rows:

- `periodic`: 1 paired row, i*pi lower post-snap loss only, no verifier-gated exact recovery.
- `negative_control`: 1 paired row, raw lower post-snap loss only, no verifier-gated exact recovery.

## Tests

Passed:

```bash
PYTHONPATH=src python -m pytest tests/test_geml_package.py tests/test_campaign.py tests/test_benchmark_reports.py -q
# 43 passed in 26.91s

PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_optimizer_cleanup.py tests/test_verify.py -q
# 93 passed, 2 warnings in 8.68s

PYTHONPATH=src python -m compileall -q src tests
# passed

git diff --check
# passed
```

Warnings were the existing NumPy divide-by-zero and invalid multiply warnings in `tests/test_optimizer_cleanup.py::test_optimizer_runs_fixed_centered_family_with_manifest_metadata`.
