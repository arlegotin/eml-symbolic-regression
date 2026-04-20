# Phase 72: Automated Test Suite and CI Hardening - Research

**Researched:** 2026-04-20
**Status:** Complete

## Phase Goal

The public repo has meaningful algorithmic tests and CI, not just packaging/framing checks.

## Requirements

- `TEST-01`: Unit tests cover EML semantics, branch behavior, compiler output, verifier contracts, and artifact manifest validation.
- `TEST-02`: Minimal evidence-regression exercises train -> snap -> verify -> artifact generation.
- `TEST-03`: CI runs unit tests, selected integration/evidence smoke, clean-room reproduction smoke, and public snapshot checks.
- `TEST-04`: CI preserves branch discipline for `dev` and `main`.

## Current Coverage

- `tests/test_semantics_expression.py`: canonical semantics, centered semantics, anomaly counters, faithful/guarded behavior.
- `tests/test_compiler_warm_start.py`: compiler and warm-start contracts.
- `tests/test_verify.py`: verifier evidence levels, symbolic/dense/adversarial/certificate labels, split role isolation.
- `tests/test_optimizer_cleanup.py` and `tests/test_benchmark_contract.py`: optimizer manifests, candidate pools, budget parsing, run IDs.
- `tests/test_publication_rebuild.py`: clean-room publication manifest and placeholder validation.
- Existing CI is limited to `publish-main.yml`; there is no general test workflow.

## Gaps

- No GitHub Actions CI runs unit or integration tests.
- No locally testable branch/public-snapshot validation script.
- `publish-main.yml` currently removes all `.github` content, so generated `main` cannot carry public CI.
- No single minimal regression test writes a complete train/snap/verify artifact and validates its schema.

## Implementation Direction

1. Add `.github/workflows/ci.yml`.
2. Add `scripts/validate-ci-contract.py` with `dev` and `public-snapshot` modes.
3. Adjust `publish-main.yml` to remove only the publishing workflow from `.github`, preserving public CI.
4. Add `tests/test_evidence_regression.py`.
5. Add tests for the CI contract validator.

## Verification Strategy

- Run the new evidence regression and CI contract tests.
- Run focused suites used by CI locally.
- Run `scripts/validate-ci-contract.py --mode dev --root .`.
- Simulate the public snapshot filter in a temporary directory and run `--mode public-snapshot`.
