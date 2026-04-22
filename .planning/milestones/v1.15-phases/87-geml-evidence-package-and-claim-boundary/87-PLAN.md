# Phase 87 Plan: GEML Evidence Package and Claim Boundary

## Tasks

1. Add GEML package builder.
   - Gather theory artifacts, suite manifests, campaign paired tables, source locks, and reproduction commands.
   - Support missing campaign results without crashing.

2. Add target-family classification.
   - Classify paired rows by target family.
   - Count i*pi wins, raw wins, both recovered, neither recovered, and loss-only outcomes.
   - Include negative-control family counts.

3. Add claim audit.
   - Block global-superiority language.
   - Block broad blind-recovery language.
   - Block full-universality language.
   - Require restricted theory and matched protocol references.

4. Add package artifacts and tests.
   - Write manifest, source locks, classification tables, claim audit, claim boundary, and reproduction docs.
   - Generate the package under `artifacts/paper/v1.15-geml/`.
   - Test package creation and claim-audit failure modes.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_geml_package.py tests/test_campaign.py tests/test_benchmark_reports.py -q`
- `PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_optimizer_cleanup.py tests/test_verify.py -q`
- `PYTHONPATH=src python -m compileall -q src tests`
- `git diff --check`
