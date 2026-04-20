# Phase 72: Automated Test Suite and CI Hardening - Summary

**Completed:** 2026-04-20
**Status:** Complete
**Implementation commit:** `6b34b29`

## What Changed

- Added `.github/workflows/ci.yml` with separate jobs for:
  - focused core unit contracts,
  - selected integration smoke tests,
  - clean-room publication rebuild smoke,
  - branch and public snapshot contract validation.
- Added `scripts/validate-ci-contract.py` with two validation modes:
  - `dev` checks required source, test, CI, publication, lockfile, and private planning/source-document paths.
  - `public-snapshot` checks required public paths and rejects private planning docs, source docs, raw run artifacts, aggregate scratch artifacts, and dev-only publish workflow files.
- Updated `.github/workflows/publish-main.yml` so the public snapshot keeps the public CI workflow while removing the dev-only publish workflow.
- Added `tests/test_ci_contract.py` to lock down CI workflow shape, validator behavior, public snapshot requirements, and forbidden artifact detection.
- Added `tests/test_evidence_regression.py` as a small train -> snap -> verify -> artifact regression test for optimizer manifests, selection data, verifier reports, and `semantics_alignment`.

## Requirement Coverage

- `TEST-01`: Complete. Focused unit CI covers EML semantics, principal-branch behavior, compiler warm starts, verifier contracts, optimizer cleanup, benchmark contracts, publication rebuild contracts, and CI contract validation.
- `TEST-02`: Complete. The evidence regression test runs a minimal training and verification pipeline and validates the generated artifact contract.
- `TEST-03`: Complete. CI runs core tests, selected integration/evidence smoke tests, clean-room publication rebuild smoke, and public snapshot checks on `dev`, `main`, pull requests, and manual dispatch.
- `TEST-04`: Complete. The validator enforces full dev-tree requirements and public snapshot exclusions, and the publish workflow now preserves public CI while removing private/dev-only files.

## Verification

- New CI contract and evidence regression tests passed.
- The CI core test command passed locally.
- The selected integration smoke command passed locally.
- The publication rebuild script passed locally.
- Dev-tree and simulated committed public snapshot validators passed.
- `git diff --check` passed.

## Notes

- The publication rebuild smoke generated `artifacts/paper/v1.13` during verification. Those generated smoke artifacts were removed after the command passed because Phase 72 changes only the CI and validation contract, not the publication artifact payload.
- The simulated public snapshot was rerun after committing the CI workflow because `git archive HEAD` only includes committed files.
