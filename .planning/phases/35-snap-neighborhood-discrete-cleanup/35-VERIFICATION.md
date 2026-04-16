---
phase: 35-snap-neighborhood-discrete-cleanup
verified: 2026-04-16T10:50:51Z
status: passed
score: 4/4 must-haves verified
score_verified: 4
score_total: 4
overrides_applied: 0
requirements:
  - id: DISC-01
    status: satisfied
    evidence: "Active slot alternatives expose bounded top-k choices and `expand_snap_neighborhood()` deduplicates exact AST variants."
  - id: DISC-02
    status: satisfied
    evidence: "`cleanup_failed_candidate()` repairs failed exact candidates without target AST or embedding inputs."
  - id: DISC-03
    status: satisfied
    evidence: "Repair artifacts now include changed slots/subtrees, margins, probability gaps, accepted moves, and repair variant counts."
  - id: DISC-04
    status: satisfied
    evidence: "Blind, warm-start, and perturbed-basin artifacts preserve the original selected/fallback candidate manifest even when cleanup runs."
---

# Phase 35: Snap-Neighborhood Discrete Cleanup Verification Report

**Phase Goal:** Users can recover near-miss snapped candidates through bounded target-free discrete cleanup instead of relying on a single greedy slotwise argmax.
**Verified:** 2026-04-16T10:50:51Z
**Status:** passed

## Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Low-margin active slots can emit replayable top-k alternatives. | VERIFIED | `SoftEMLTree.active_slot_alternatives()` now records ranked choices plus descendant subtree assignments where needed. |
| 2 | Neighborhood expansion deduplicates exact ASTs before verifier work. | VERIFIED | `expand_snap_neighborhood()` replays slot-map variants and keeps only the best provenance for duplicate exact trees. |
| 3 | Failed exact candidates can be cleaned up without target AST access. | VERIFIED | `cleanup_failed_candidate()` uses only the selected candidate snap, serialized alternatives, and verifier splits. |
| 4 | Benchmark artifacts preserve fallback semantics while recording cleanup provenance. | VERIFIED | Blind, warm-start, and perturbed-basin runs expose `repair`, `repair_status`, and repair metrics without mutating the optimizer-selected candidate payload. |

**Score:** 4/4 truths verified

## Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Master-tree slot alternatives and neighborhood dedup | `python -m pytest tests/test_master_tree.py tests/test_repair.py -q` | 17 passed, 2 expected divide-by-zero `log` warnings | PASS |
| Full Phase 35 regression slice | `python -m pytest tests/test_master_tree.py tests/test_repair.py tests/test_benchmark_runner.py tests/test_basin_targets.py tests/test_compiler_warm_start.py -q` | 58 passed, 6 expected numerical warnings | PASS |

## Requirements Coverage

| Requirement | Description | Status | Evidence |
|-------------|-------------|--------|----------|
| DISC-01 | Bounded beam expansion over low-margin active slots with exact AST deduplication | SATISFIED | Active-slot alternatives plus `expand_snap_neighborhood()` |
| DISC-02 | Target-free local repair around failed snapped candidates | SATISFIED | `cleanup_failed_candidate()` in `repair.py` |
| DISC-03 | Cleanup reports show slots/subtrees, margins, and candidate deltas | SATISFIED | Repair move payloads include slot, subtree, slot margin, probability gap, verifier status, and accepted moves |
| DISC-04 | Original snapped candidate remains available as fallback when cleanup does not win | SATISFIED | Repair promotion leaves `trained_eml_candidate.selected_candidate` and `fallback_candidate` untouched |

## Gaps Summary

No Phase 35 gaps remain. Post-snap constant refit and broader numerical/domain controls remain intentionally deferred to Phase 36.

---

_Verified: 2026-04-16T10:50:51Z_
_Verifier: Codex_
