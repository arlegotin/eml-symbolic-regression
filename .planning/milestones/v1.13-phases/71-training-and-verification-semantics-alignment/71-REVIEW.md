---
status: clean
reviewed_at: "2026-04-20"
implementation_commit: fea8229
---

# Phase 71: Training and Verification Semantics Alignment - Review

## Findings

No blocking findings.

## Review Notes

- The faithful mode bypasses training-only clamps and log-safety penalties in both raw and centered PyTorch semantics while preserving anomaly counters.
- `guarded` remains the default, and default benchmark run IDs are preserved to avoid invalidating existing artifact references.
- Suite-wide faithful benchmark overrides produce distinct run IDs, which prevents guarded and faithful ablation artifacts from overwriting each other.
- Optimizer manifests now surface verifier certificate/evidence labels in `semantics_alignment`, so downstream publication rows do not need to infer them from nested candidate payloads.
- `SplitResult` now keeps a default role for legacy positional test/helper construction while still serializing explicit role fields.

## Residual Risk

- Full publication-matrix ablations are enabled but not executed in this phase. Phase 76 remains responsible for regenerating and comparing the full evidence package.
- Faithful mode can expose non-finite training behavior on harder runs; that is expected and should be interpreted through the new diagnostics rather than as a regression in guarded defaults.
