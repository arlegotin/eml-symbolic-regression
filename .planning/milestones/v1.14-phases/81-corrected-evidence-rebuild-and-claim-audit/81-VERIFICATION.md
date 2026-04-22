# Phase 81 Verification

## Publication Rebuild

Command:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli publication-rebuild --output-dir artifacts/paper/v1.14 --overwrite --allow-dirty
```

Result:

- Passed.
- Manifest written to `artifacts/paper/v1.14/manifest.json`.
- Validation written to `artifacts/paper/v1.14/validation.json`.
- Manifest recorded clean source revision `d2988def50795727706f381d662a14fc0106fe09` before the generated evidence package commit.

## Claim Audit

`artifacts/paper/v1.14/claim-audit.json`:

- `status`: `passed`
- `trained_exact_recovery_rows`: 8
- `compile_only_verified_support_rows`: 1
- `unsupported_rows`: 15
- `failed_rows`: 0
- `verification_passed_rows`: 9

Passed audit checks include:

- `paper_track_corrected_headline_counts`
- `compile_only_excluded_from_trained_recovery`
- `baseline_rows_expose_quarantine_fields`
- `baseline_main_surface_claims_quarantined`

## Release Gate

`artifacts/paper/v1.14/release-gate.json`:

- `status`: `passed`
- `claim_audit_passed`: `passed`
- `dev_contract_valid`: `passed`
- `public_snapshot_contract_valid`: `passed`
- `main_sync.status`: `ready_for_publish_main_workflow`

## Stale Wording Scan

Current README and v1.14 package surfaces were scanned for stale recovered-headline and unsupported baseline language. No matches were found for the stale phrases checked, including `Nine rows`, `9 rows`, `recovered headline`, `baseline reports`, `useful basin`, `warm-start basin`, and `robustness`.

## Tests

Passed:

```bash
PYTHONPATH=src python -m pytest tests/test_publication_rebuild.py tests/test_ci_contract.py -q
# 16 passed

PYTHONPATH=src python -m pytest tests/test_publication_rebuild.py tests/test_ci_contract.py tests/test_baseline_harness.py tests/test_benchmark_reports.py tests/test_campaign.py tests/test_verify.py tests/test_expanded_datasets.py -q
# 77 passed in 32.59s

PYTHONPATH=src python -m pytest tests/test_shallow_blind_proof_regression.py::test_v15_shallow_pure_blind_suite_declares_measured_random_only_boundary tests/test_shallow_scaled_exponential_contract.py tests/test_verifier_demos_cli.py tests/test_verify.py -q
# 24 passed in 9.77s
```

Interrupted long-running checks:

```bash
PYTHONPATH=src python -m pytest -q
# Interrupted after 382 passed, 21 warnings in 979.53s.
# The active test was tests/test_shallow_blind_proof_regression.py::test_v15_shallow_suite_recovers_but_uses_scaffolded_blind_training.

PYTHONPATH=src python -m pytest tests/test_shallow_blind_proof_regression.py::test_v15_shallow_suite_recovers_but_uses_scaffolded_blind_training tests/test_shallow_blind_proof_regression.py::test_v15_shallow_scaffolded_threshold_accepts_scaffolded_recovery -q
# Interrupted after 1255.58s while still CPU-bound in the shared 18-run proof-regression fixture.
```

The interrupted proof-regression fixture predates Phase 81 and runs the historical v1.5 scaffolded training proof suite. It was not completed in this local verification window, so this phase is verified against the corrected publication package, claim audit, release gate, and affected tests rather than a complete all-tests pass.

## Push-Size Guard

After the corrected package was slimmed, the publication-only all-in-one `suite-result.json` snapshot is no longer retained in `artifacts/paper/v1.14/`. The smaller aggregate, report, table, source-lock, claim-audit, release-gate, and raw-run artifacts remain.

Checks:

```bash
find . -path ./.git -prune -o -type f -size +100M -print
# no output
```
