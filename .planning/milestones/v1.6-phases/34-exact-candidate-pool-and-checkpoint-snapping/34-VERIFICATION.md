---
phase: 34-exact-candidate-pool-and-checkpoint-snapping
verified: 2026-04-16T10:23:15Z
status: passed
score: 4/4 must-haves verified
score_verified: 4
score_total: 4
overrides_applied: 0
requirements:
  - id: HARD-01
    status: satisfied
    evidence: "TrainingConfig and fit_eml_tree add an explicit late hardening window with emitted hardening checkpoint snaps."
  - id: HARD-02
    status: satisfied
    evidence: "Optimizer manifests now retain a `candidates` pool with per-candidate provenance, margins, and exact post-snap loss."
  - id: HARD-03
    status: satisfied
    evidence: "When verification splits are available, candidate selection uses verifier-owned ranking and records the explicit legacy fallback candidate."
  - id: HARD-04
    status: satisfied
    evidence: "CLI and benchmark artifacts expose `selected_candidate`, `fallback_candidate`, and selection provenance/metrics."
---

# Phase 34: Exact Candidate Pool and Checkpoint Snapping Verification Report

**Phase Goal:** Users receive a final exact tree selected from a verifier-gated pool of snapped candidates rather than from the single minimum soft-loss endpoint.
**Verified:** 2026-04-16T10:23:15Z
**Status:** passed

## Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Training now has an explicit late hardening window. | VERIFIED | `TrainingConfig` adds hardening controls and `fit_eml_tree()` emits hardening checkpoint snaps. |
| 2 | The optimizer retains exact candidates instead of only one final snap. | VERIFIED | Optimizer manifests now serialize `candidates`, `selected_candidate`, `fallback_candidate`, and restart-level candidate IDs. |
| 3 | Final exact-candidate selection is verifier-gated when evaluation splits are available. | VERIFIED | Blind, warm-start, and perturbed-basin flows route `verification_splits` into `fit_eml_tree()` and reuse the selected-candidate verification report. |
| 4 | CLI and benchmark artifacts identify both the winner and the old selector fallback. | VERIFIED | CLI demo reports and benchmark runner artifacts expose selection mode, selected/fallback candidate IDs, and source provenance. |

**Score:** 4/4 truths verified

## Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Optimizer candidate-pool contract | `python -m pytest tests/test_optimizer_cleanup.py -q` | 7 passed | PASS |
| CLI trained-report provenance | `python -m pytest tests/test_verifier_demos_cli.py -q` | 6 passed | PASS |
| Blind benchmark artifact provenance | `python -m pytest tests/test_benchmark_runner.py -q` | 17 passed, 2 expected overflow warnings | PASS |
| Warm-start and basin wrappers still honor selected candidate semantics | `python -m pytest tests/test_basin_targets.py tests/test_compiler_warm_start.py -q` | 22 passed, 1 expected overflow warning | PASS |

## Requirements Coverage

| Requirement | Description | Status | Evidence |
|-------------|-------------|--------|----------|
| HARD-01 | Explicit late hardening emits exact snaps at selected checkpoints | SATISFIED | Hardening config and checkpoint emission in `optimize.py` |
| HARD-02 | Candidate pool retains restart/checkpoint provenance and exact-loss metrics | SATISFIED | Serialized `candidates` list with provenance, margins, and post-snap loss |
| HARD-03 | Verifier-owned ranking selects final exact candidate while preserving fallback | SATISFIED | Verifier-gated selection plus explicit `fallback_candidate` manifest entry |
| HARD-04 | CLI/run artifacts expose winner and old-selector provenance | SATISFIED | CLI demo and benchmark metrics now surface selected/fallback candidate metadata |

## Gaps Summary

No Phase 34 gaps remain. Low-margin neighborhood search, target-free repair, and broader report-level exploitation of the new candidate metrics remain intentionally deferred to later v1.6 phases.

---

_Verified: 2026-04-16T10:23:15Z_
_Verifier: Codex_
