# Phase 71: Training and Verification Semantics Alignment - Plan

**Planned:** 2026-04-20
**Status:** Ready for execution

## Objective

Add a first-class faithful training semantics mode and publish alignment diagnostics so optimizer artifacts explain whether training used verifier-faithful arithmetic or guarded surrogate arithmetic.

## Tasks

### 1. Semantics Mode

- Add a validated `mode` field to `TrainingSemanticsConfig`.
- In raw and centered PyTorch semantics, apply exp/expm1 clamping and log-safety penalties only when `mode == "guarded"`.
- Keep anomaly counters active in both modes.
- Add tests proving faithful mode does not clamp or add safety penalty.

### 2. Optimizer Config and Manifest

- Add `semantics_mode` to `TrainingConfig`.
- Pass it into `TrainingSemanticsConfig`.
- Add a `semantics_alignment` manifest payload with guard parameters, objective-faithfulness status, fallback reason, anomaly summary, post-snap mismatch, verifier status, evidence level, and certificate status.
- Add optimizer manifest tests.

### 3. Benchmark Wiring

- Add `semantics_mode` to `OptimizerBudget`.
- Parse, validate, serialize, and include it in benchmark run IDs and artifacts through existing optimizer budget payloads.
- Add helper support so CLI benchmark runs can override semantics mode for an entire suite.
- Add budget/CLI tests.

### 4. Demo CLI Wiring

- Add `demo --semantics-mode {guarded,faithful}`.
- Pass it into both direct blind training and warm-start training configs.
- Add parser coverage.

### 5. Verification and Review Artifacts

- Run focused tests.
- Write `71-SUMMARY.md`, `71-REVIEW.md`, and `71-VERIFICATION.md`.
- Mark `SEM-01`, `SEM-02`, and `SEM-03` complete if tests pass. Mark `SEM-04` complete only if certificate status is surfaced in artifact summaries; otherwise record the remaining table-consumer gap.

## Acceptance Checks

- Faithful mode training output equals verifier arithmetic for finite test inputs even when guarded mode would clamp.
- Guarded mode behavior remains backwards compatible.
- Training manifests include `semantics_alignment`.
- Benchmark budget artifacts include `semantics_mode`.
- `benchmark --semantics-mode faithful` can override a loaded suite without editing suite definitions.
- Focused tests pass.
