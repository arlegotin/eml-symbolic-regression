# Phase 72: Automated Test Suite and CI Hardening - Plan

**Planned:** 2026-04-20
**Status:** Ready for execution

## Objective

Add enforceable CI and branch-discipline checks while keeping runtime bounded for ordinary pushes and pull requests.

## Tasks

### 1. CI Workflow

- Create `.github/workflows/ci.yml`.
- Add jobs for:
  - focused core unit tests,
  - selected integration/evidence smoke tests,
  - clean-room publication smoke,
  - branch/public-snapshot contract validation.

### 2. Branch/Public Snapshot Contract

- Add `scripts/validate-ci-contract.py`.
- Validate full dev tree requirements.
- Validate public snapshot required/forbidden paths.
- Update `publish-main.yml` to keep public CI while removing the publish workflow and private local-only paths.

### 3. Evidence Regression

- Add a tiny train -> snap -> verify -> artifact generation test using the `exp` demo.
- Assert the artifact carries optimizer manifest, verifier report, selection data, and `semantics_alignment`.

### 4. Tests

- Add tests for the CI contract validator.
- Run new tests plus CI-command-equivalent focused suites.

### 5. Closeout

- Write `72-SUMMARY.md`, `72-REVIEW.md`, and `72-VERIFICATION.md`.
- Mark `TEST-01` through `TEST-04` complete if local verification passes.

## Acceptance Checks

- `ci.yml` exists and is parseable as a workflow.
- The CI commands run locally.
- The branch validator passes on the current `dev` tree.
- A simulated public snapshot passes validation and excludes local-only artifacts.
- The evidence-regression test writes and validates a run artifact.
