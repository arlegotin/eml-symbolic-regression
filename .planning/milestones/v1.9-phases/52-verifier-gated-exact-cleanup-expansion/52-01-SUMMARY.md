---
phase: 52-verifier-gated-exact-cleanup-expansion
plan: 01
subsystem: optimizer
tags: [repair, cleanup, verifier, exact-ast, candidate-pool]
requires:
  - phase: 34
    provides: "Verifier-gated exact candidate pooling with selected/fallback provenance"
  - phase: 35
    provides: "Replayable active-slot alternatives and exact-AST-deduplicated snap neighborhoods"
provides:
  - "Opt-in expanded target-free cleanup over selected, fallback, and retained exact-candidate roots"
  - "Global exact-AST root and variant deduplication before verifier evaluation"
  - "Repair report and move provenance for accepted candidate root id, source, role, and subtree moves"
affects: [phase-52, benchmark-artifacts, repair-evidence]
tech-stack:
  added: []
  patterns: ["Verifier-gated candidate-pool cleanup with exact-AST dedup and immutable optimizer manifests"]
key-files:
  created:
    - .planning/phases/52-verifier-gated-exact-cleanup-expansion/52-01-SUMMARY.md
  modified:
    - src/eml_symbolic_regression/repair.py
    - tests/test_repair.py
key-decisions:
  - "Expanded cleanup is opt-in through RepairConfig.expanded_candidate_pool(); RepairConfig() remains selected-only."
  - "Candidate roots and cleanup variants are deduplicated by serialized exact AST before verifier work."
  - "Repair promotion remains verifier-owned: only a recovered verification report can serialize repaired_ast or accepted root metadata."
patterns-established:
  - "Repair reports carry candidate-root counts, per-root variant counts, deduped variant count, and accepted root provenance."
  - "Candidate-pool moves preserve existing NeighborhoodMove subtree provenance while adding candidate id/source/root role."
requirements-completed: [REP-01, REP-02, REP-03]
duration: 9 min
completed: 2026-04-17
---

# Phase 52 Plan 01: Verifier-Gated Exact Cleanup Expansion Summary

**Opt-in candidate-pool repair over selected, fallback, and retained exact roots with verifier-gated AST-deduped promotion**

## Performance

- **Duration:** 9 min
- **Started:** 2026-04-17T15:05:50Z
- **Completed:** 2026-04-17T15:14:23Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments

- Added `RepairConfig.expanded_candidate_pool()` with bounded larger cleanup settings and root sources `selected`, `fallback`, and `retained`, while keeping `RepairConfig()` selected-only.
- Reworked `cleanup_failed_candidate()` to enumerate ordered candidate roots, deduplicate roots and variants by exact AST, verify variants globally, and accept only verifier-`recovered` repairs.
- Extended repair reports and moves with candidate-root provenance, per-root variant counts, deduped variant counts, and preserved subtree move metadata.
- Added focused TDD coverage for default behavior, fallback repair, retained repair, duplicate-root dedup, subtree provenance, and failed-verifier gating.

## Task Commits

Each TDD task was committed atomically:

1. **Task 1 RED: expanded preset and provenance serialization tests** - `6891f40` (test)
2. **Task 1 GREEN: repair config/report/move metadata** - `49d7ba7` (feat)
3. **Task 2 RED: candidate-pool cleanup behavior tests** - `a3e814c` (test)
4. **Task 2 GREEN: expanded verifier-gated candidate-pool cleanup** - `c91a58d` (feat)

## Files Created/Modified

- `src/eml_symbolic_regression/repair.py` - Adds opt-in expanded cleanup config, candidate-root workflow, AST root/variant dedup, verifier-gated global ranking, and provenance serialization.
- `tests/test_repair.py` - Adds regression coverage for selected-only defaults, fallback/retained roots, duplicate-root dedup, subtree provenance, and unrecovered variant rejection.
- `.planning/phases/52-verifier-gated-exact-cleanup-expansion/52-01-SUMMARY.md` - Captures execution results and verification evidence.

## Decisions Made

- Kept candidate-pool cleanup opt-in so existing direct callers and benchmark flows do not silently broaden repair budgets.
- Used serialized exact AST documents for both root and variant deduplication, matching the existing `expand_snap_neighborhood()` dedup pattern.
- Left optimizer-selected and fallback candidates untouched; cleanup only emits repair report metadata and a repaired expression when the verifier recovers it.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- One RED test initially used `Eml(Const(1), Const(1))` as the unrecovered target, but that expression was reachable through a legitimate cleanup variant. The fixture was corrected to a deeper target outside the bounded cleanup neighborhood before the GREEN commit.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_repair.py -q` - 16 passed, 6 warnings from existing NumPy log divide-by-zero semantics.
- `PYTHONPATH=src python -m pytest tests/test_master_tree.py -q` - 12 passed, 1 warning from existing NumPy log divide-by-zero semantics.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Plan 52-02 can wire the expanded repair preset into targeted benchmark/evidence paths. The core repair API now reports root counts, per-root variant counts, deduped variant counts, and accepted candidate provenance without mutating optimizer manifests.

## Self-Check: PASSED

- Found `src/eml_symbolic_regression/repair.py`
- Found `tests/test_repair.py`
- Found `.planning/phases/52-verifier-gated-exact-cleanup-expansion/52-01-SUMMARY.md`
- Found task commits `6891f40`, `49d7ba7`, `a3e814c`, and `c91a58d`

---
*Phase: 52-verifier-gated-exact-cleanup-expansion*
*Completed: 2026-04-17*
