---
phase: 30-bounded-shallow-blind-training-recovery
verified: 2026-04-15T21:31:00Z
status: passed
score: 8/8 must-haves verified
score_verified: 8
score_total: 8
---

# Phase 30 Verification Report

**Phase Goal:** Users get an honest shallow training proof split: pure random-initialized blind recovery is measured with scaffolds disabled, while scaffolded shallow recovery has its own bounded 100% verifier-owned proof suite.

## Verified Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Pure random-initialized blind recovery is separate from scaffolded recovery. | VERIFIED | `paper-shallow-blind-recovery` now uses claim class `measured_training_boundary`, suite `v1.5-shallow-pure-blind`, and threshold `measured_pure_blind_recovery`. |
| 2 | Pure-blind suite disables scaffold initializers. | VERIFIED | `v1.5-shallow-pure-blind` sets `scaffold_initializers=()` and validation rejects nonempty scaffold initializers for the pure-blind claim. |
| 3 | Scaffolded shallow recovery has its own bounded proof claim. | VERIFIED | `paper-shallow-scaffolded-recovery` uses claim class `scaffolded_training_proof`, suite `v1.5-shallow-proof`, and threshold `scaffolded_bounded_100_percent`. |
| 4 | Scaffolded proof rows require scaffold initializers. | VERIFIED | Benchmark validation rejects empty scaffold initializers for `paper-shallow-scaffolded-recovery`. |
| 5 | Threshold aggregation cannot mix the evidence classes. | VERIFIED | Pure-blind thresholds count only `blind_training_recovered`; scaffolded thresholds count only `scaffolded_blind_training_recovered`. |
| 6 | The bounded scaffolded suite covers the declared six shallow targets and 18 runs. | VERIFIED | Regression tests cover `exp`, `log`, `radioactive_decay`, Beer-Lambert, scaled growth, and scaled fast decay across seeds 0/1/2. |
| 7 | The bounded scaffolded suite reaches 100% verifier-owned recovery. | VERIFIED | Full shallow regression threshold passed 18/18 with evidence class `scaffolded_blind_training_recovered`. |
| 8 | Planning state no longer blocks Phase 32 on the old claim ambiguity. | VERIFIED | Requirements, roadmap, and state now mark Phase 30 complete and Phase 32 ready. |

## Test Evidence

```bash
PYTHONPATH=src pytest tests/test_proof_contract.py tests/test_benchmark_contract.py tests/test_benchmark_reports.py tests/test_benchmark_runner.py tests/test_campaign.py tests/test_shallow_blind_proof_regression.py
```

Result: `91 passed, 1 warning in 1128.71s (0:18:48)`.

```bash
PYTHONPATH=src pytest tests --ignore=tests/test_proof_contract.py --ignore=tests/test_benchmark_contract.py --ignore=tests/test_benchmark_reports.py --ignore=tests/test_benchmark_runner.py --ignore=tests/test_campaign.py --ignore=tests/test_shallow_blind_proof_regression.py
```

Result: `90 passed, 7 warnings in 43.35s`.

Warnings are existing EML numerical warnings from `src/eml_symbolic_regression/semantics.py:110`.
