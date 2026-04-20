# Phase 71: Training and Verification Semantics Alignment - Research

**Researched:** 2026-04-20
**Status:** Complete

## Phase Goal

The optimizer either searches verified semantics directly or publishes hard evidence about surrogate clamp/log-guard mismatch.

## Requirements

- `SEM-01`: faithful-semantics training mode, or documented fallback.
- `SEM-02`: clamp/log-guard ablation controls that quantify spurious recoveries.
- `SEM-03`: every training artifact reports clamp, guard, NaN/Inf, branch, and post-snap mismatch diagnostics.
- `SEM-04`: scientific-law claims include real-domain and branch-validity certificates or explicit unsupported labels.

## Current Behavior

- `semantics.py` evaluates canonical raw EML as `exp(x) - log(y)` and centered-family EML with `expm1/log1p` coordinates.
- `training=True` currently clamps the real part entering exp/expm1 and can add a log-safety penalty. `training=False` already uses faithful unclamped arithmetic.
- `AnomalyStats` already records NaN, Inf, clamp, exp overflow, log small magnitude, non-positive real log input, branch-cut, non-finite log input, expm1 overflow, log1p branch-cut, shifted singularity, and log-safety penalty data.
- `optimize.py` stores per-step traces, final anomalies, selected/fallback candidates, post-snap loss, and verifier reports in `fit_eml_tree()` manifests.
- `benchmark.py` already threads clamp/log guard numeric settings through `OptimizerBudget` into `TrainingConfig` and extracts anomaly fields into aggregate metrics.
- Phase 70 verifier changes already make symbolic, dense random, adversarial, certificate, evidence-level, and metric-role fields available in verification reports.

## Gaps

- There is no explicit way to request faithful training semantics while still running optimizer loops.
- Artifacts show raw anomaly counters but do not summarize whether the objective was faithful or guarded.
- Benchmark budgets cannot yet run the same suite under a different semantics mode.
- CLI demo runs cannot yet request faithful semantics.
- Scientific-law/table consumers need a stable summary field for certificate status; the verifier has the data, but training manifests should surface it alongside semantics mismatch diagnostics.

## Implementation Direction

1. Add `mode: Literal["guarded", "faithful"]` semantics config state, using a string to avoid introducing a new dependency.
2. In faithful mode, bypass training-only clamp and log-safety penalties while keeping all anomaly counters active.
3. Add `semantics_mode` to optimizer and benchmark configs, validate accepted values, and serialize it.
4. Add `semantics_alignment` to optimizer manifests:
   - `training_semantics_mode`
   - `objective_matches_verifier_semantics`
   - fallback reason for guarded training
   - guard parameter payload
   - anomaly totals and post-snap/verifier mismatch fields
   - certificate/evidence fields from selected verification where available
5. Add CLI support for `demo --semantics-mode` and `benchmark --semantics-mode`.
6. Add focused regression tests for behavior and artifact contracts.

## Verification Strategy

- Unit-test faithful raw and centered training behavior against `torch.exp/log` and `torch.expm1/log1p`.
- Unit-test manifest `semantics_alignment` for guarded and faithful runs.
- Unit-test benchmark budget parsing/serialization and invalid-mode rejection.
- Unit-test CLI parser wiring.
- Run focused suites: semantics, optimizer cleanup, benchmark contract, benchmark runner parser smoke, and Phase 70 verifier regressions.

## Risks

- Faithful mode can produce non-finite losses sooner on difficult runs because it removes stabilizing clamps. This is acceptable if artifacts label it clearly and guarded fallback remains explicit.
- Full ablation quantification requires running publication matrix variants. This phase enables and smoke-tests that path; Phase 76 performs the expensive rebuild.
