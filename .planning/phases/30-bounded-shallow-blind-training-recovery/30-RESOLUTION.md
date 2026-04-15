---
phase: 30-bounded-shallow-blind-training-recovery
resolved: 2026-04-15T21:31:00Z
status: complete
resolution: split pure-blind measurement from bounded scaffolded proof
---

# Phase 30 Resolution: Shallow Claim Split

## Decision

Phase 30 is complete through a claim split rather than by pretending scaffolded recovery is pure random-initialized blind recovery.

The long-term solution is:

- `paper-shallow-blind-recovery` is a measured pure random-initialized blind boundary.
- `paper-shallow-scaffolded-recovery` is the bounded 100% scaffolded shallow recovery proof.

This resolves CR-01 from `30-REVIEW.md` without weakening the verifier or counting scaffolded starts as blind-discovery evidence.

## Implementation

- `src/eml_symbolic_regression/proof.py` defines separate claim classes and threshold policies:
  - `measured_pure_blind_recovery`
  - `scaffolded_bounded_100_percent`
- `src/eml_symbolic_regression/benchmark.py` adds optimizer-level `scaffold_initializers` control.
- `v1.5-shallow-pure-blind` disables scaffold initializers and reports measured pure-blind recovery.
- `v1.5-shallow-proof` remains the 18-run bounded proof suite, but is now explicitly scaffolded.
- Aggregate threshold logic counts only `blind_training_recovered` for the pure-blind claim and only `scaffolded_blind_training_recovered` for the scaffolded claim.
- `src/eml_symbolic_regression/campaign.py` adds `proof-shallow-pure-blind` while keeping `proof-shallow` as the bounded scaffolded campaign.

## Verification

- Focused proof/benchmark/campaign slice: `91 passed, 1 warning in 1128.71s (0:18:48)`.
- Remaining tests excluding the focused slice: `90 passed, 7 warnings in 43.35s`.

The focused slice includes the full 18-run scaffolded shallow proof regression. Existing warnings are numerical `semantics.py:110` overflow/divide-by-zero warnings from EML `exp/log` evaluation paths.

## Planning State

- SHAL-01 through SHAL-04 are complete under the revised shallow claim split.
- Phase 30 is complete.
- Phase 32 is unblocked and should use both Phase 30 outputs:
  - measured pure-blind boundary evidence,
  - bounded scaffolded shallow proof evidence.
