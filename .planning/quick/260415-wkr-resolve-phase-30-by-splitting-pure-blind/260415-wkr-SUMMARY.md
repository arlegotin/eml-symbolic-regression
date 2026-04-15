# Quick Summary: Resolve Phase 30 by Splitting Pure Blind and Scaffolded Claims

**Date:** 2026-04-15
**Status:** Complete

## Outcome

Resolved the Phase 30 review blocker by replacing the misleading pure-blind 100% framing with two explicit claims:

- `paper-shallow-blind-recovery` is now a measured pure random-initialized blind boundary. Its suite disables scaffold initializers and counts only `blind_training_recovered`.
- `paper-shallow-scaffolded-recovery` is now the bounded 100% shallow proof claim. Its suite requires scaffold initializers and counts only `scaffolded_blind_training_recovered`.

## Changes

- Added `measured_pure_blind_recovery` and `scaffolded_bounded_100_percent` threshold policies.
- Added `scaffold_initializers` to benchmark optimizer budgets and threaded it into `TrainingConfig`.
- Added `v1.5-shallow-pure-blind` for measured random-only blind recovery.
- Reclassified `v1.5-shallow-proof` as the bounded scaffolded proof suite.
- Added `proof-shallow-pure-blind` campaign preset.
- Updated aggregate threshold tests, campaign tests, CLI claim listing tests, and the full shallow proof regression.
- Updated `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, and `.planning/STATE.md` to mark Phase 30 complete and Phase 32 ready.

## Verification

- `PYTHONPATH=src pytest tests/test_proof_contract.py tests/test_benchmark_contract.py tests/test_benchmark_reports.py tests/test_benchmark_runner.py tests/test_campaign.py tests/test_shallow_blind_proof_regression.py`
  - Result: `91 passed, 1 warning in 1128.71s (0:18:48)`.
- `PYTHONPATH=src pytest tests --ignore=tests/test_proof_contract.py --ignore=tests/test_benchmark_contract.py --ignore=tests/test_benchmark_reports.py --ignore=tests/test_benchmark_runner.py --ignore=tests/test_campaign.py --ignore=tests/test_shallow_blind_proof_regression.py`
  - Result: `90 passed, 7 warnings in 43.35s`.

Warnings are the existing numerical `semantics.py:110` overflow/divide-by-zero paths during EML `exp/log` evaluation.
