# Phase 59 Plan: Evidence Contracts and Source Locks

## Goal

Define and enforce the v1.11 evidence contract before new training and figure generation.

## Scope

- Make the raw-hybrid paper package version-aware while preserving v1.9 compatibility.
- Add v1.11 source inventory entries for current logistic and Planck diagnostics.
- Add claim-ledger fields and package contract tests that prevent stale scientific-law rows.
- Keep package generation synthesis-only: no training, no campaigns, no implicit baselines.

## Tasks

1. Refactor paper package constants and source inventory so v1.9 remains stable and v1.11 can use a separate preset/output root.
2. Add v1.11 source inventory using v1.10 focused logistic and Planck artifacts.
3. Add claim-ledger output and metadata fields needed by later figure/package phases.
4. Extend CLI to accept a package preset while retaining default v1.9 behavior.
5. Add tests for v1.11 source locks, logistic/Planck current rows, and claim boundaries.
6. Run targeted raw-hybrid paper tests.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_raw_hybrid_paper.py tests/test_raw_hybrid_paper_regression.py -q`

## Constraints

- No silent gate relaxation.
- No formula-name recognizers.
- No training runs inside the paper package writer.
- v1.9 regression package remains backward compatible.
