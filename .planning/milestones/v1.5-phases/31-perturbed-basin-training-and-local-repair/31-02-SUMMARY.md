---
phase: 31-perturbed-basin-training-and-local-repair
plan: 02
subsystem: benchmark-repair
tags: [repair, perturbed-tree, verifier, benchmark, taxonomy]

requires:
  - phase: 31-01
    provides: "Perturbed true-tree runner, basin targets, raw return_kind/raw_status fields"
provides:
  - "Verifier-gated target-neighborhood repair for failed perturbed-tree candidates"
  - "Serializable repair moves with slot, descendant, pruned-subtree, and verifier provenance"
  - "Benchmark artifacts and aggregates that preserve raw status, return kind, repair status, and evidence class separately"
affects: [phase-31, phase-33, benchmark-reports, proof-campaigns]

tech-stack:
  added: []
  patterns: ["Frozen repair dataclasses with as_dict serialization", "Verifier-gated artifact promotion", "Aggregate grouping by independent taxonomy fields"]

key-files:
  created:
    - src/eml_symbolic_regression/repair.py
    - .planning/phases/31-perturbed-basin-training-and-local-repair/31-02-SUMMARY.md
  modified:
    - src/eml_symbolic_regression/benchmark.py
    - tests/test_repair.py
    - tests/test_benchmark_runner.py
    - tests/test_benchmark_reports.py

key-decisions:
  - "Accepted repairs are promoted only as repaired_candidate and never mutate raw perturbed_true_tree status."
  - "Repair attempts are limited to target-neighborhood slot moves and remain verifier-gated."
  - "Aggregate classification uses repair_status, return_kind, and raw_status before evidence class fallback."

patterns-established:
  - "RepairMove records source, before/after choice, descendant assignments, pruned assignments, subtree root, and verifier status."
  - "Perturbed benchmark artifacts store repair and repair_status alongside preserved raw_status and return_kind."
  - "Aggregate Markdown includes By Return Kind, By Raw Status, and By Repair Status sections."

requirements-completed: [BASN-02, BASN-04, BASN-05]

duration: 15m 21s
completed: 2026-04-15
---

# Phase 31 Plan 02: Local Repair Summary

**Verifier-gated local repair for failed perturbed-tree candidates with separate raw and repaired evidence taxonomy**

## Performance

- **Duration:** 15m 21s
- **Started:** 2026-04-15T18:54:57Z
- **Completed:** 2026-04-15T19:10:18Z
- **Tasks:** 3
- **Files modified:** 6

## Accomplishments

- Added `repair.py` with `RepairConfig`, `RepairMove`, `RepairReport`, and `repair_perturbed_candidate()`.
- Implemented target-neighborhood repair from snapped and embedded target slot maps, including terminal-to-child, child-to-terminal, and child-subtree replacement moves.
- Wired repair into `perturbed_tree` benchmark failures without overwriting raw `perturbed_true_tree.status`, `raw_status`, or `return_kind`.
- Extended metrics, run summaries, aggregate JSON, and aggregate Markdown with `repair_status`, move counts, return-kind groups, raw-status groups, and repair-status groups.
- Proved repaired artifacts classify as `repaired_candidate`, while raw same-AST, verified-equivalent, snapped-failed, soft-fit, unsupported, and execution-error rows remain distinct.

## Task Commits

1. **Task 1 RED: Repair contract tests** - `ebe5aad` (test)
2. **Task 1 GREEN: Serializable repair contracts** - `494d66a` (feat)
3. **Task 2 RED: Target repair behavior tests** - `1d3392a` (test)
4. **Task 2 GREEN: Target-neighborhood repair** - `57f2a9f` (feat)
5. **Task 3 RED: Benchmark repair taxonomy tests** - `e4ffc79` (test)
6. **Task 3 GREEN: Benchmark repair integration** - `fb90f45` (feat)

## Files Created/Modified

- `src/eml_symbolic_regression/repair.py` - Repair contracts, slot-map repair move generation, candidate reconstruction, and verifier-gated acceptance.
- `src/eml_symbolic_regression/benchmark.py` - Perturbed-tree repair invocation, repair metrics, classification ordering, aggregate groups, and Markdown sections.
- `tests/test_repair.py` - Serialization, move provenance, subtree-aware repair, and verifier-gating coverage.
- `tests/test_benchmark_runner.py` - Repaired perturbed artifact regression proving raw status remains preserved.
- `tests/test_benchmark_reports.py` - Threshold and aggregate taxonomy guardrails for raw and repaired perturbed rows.

## Decisions Made

- Repair is target-neighborhood only; enabling catalog alternatives returns `catalog_alternatives_disabled` rather than silently using unrecorded alternatives.
- Repaired runs set top-level `status` to `repaired_candidate` and `repair_status` to `repaired`, while preserving raw perturbed evidence under `perturbed_true_tree`.
- Aggregate classification gives precedence to `repair_status == "repaired"`, then raw `return_kind`, then raw unsupported and execution failure statuses.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None. The expected RED failures occurred before implementation, then the required verification passed.

## Known Stubs

None.

## Verification

- `python -m pytest tests/test_repair.py tests/test_benchmark_runner.py tests/test_benchmark_reports.py -q` -> 33 passed, 1 warning.
- `python -m pytest tests/test_repair.py tests/test_basin_targets.py -q` -> 17 passed.
- `PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark proof-perturbed-basin-beer-probes --case basin-beer-lambert-bound-probes --seed 0 --perturbation-noise 35.0 --output-dir /tmp/eml-phase31-plan02-repair-smoke` -> 1 run, 0 unsupported, 0 failed; artifact classified as `repaired_candidate` with raw `snapped_but_failed`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Plan 31-03 can use the new repair payloads and aggregate groups to produce Beer-Lambert bound evidence. Residual risk is limited to repair scope: only target-neighborhood moves are implemented, and broader catalog alternatives remain intentionally disabled.

## Self-Check: PASSED

- Confirmed `src/eml_symbolic_regression/repair.py` exists.
- Confirmed `31-02-SUMMARY.md` exists.
- Confirmed task commits `ebe5aad`, `494d66a`, `1d3392a`, `57f2a9f`, `e4ffc79`, and `fb90f45` are present in git history.

---
*Phase: 31-perturbed-basin-training-and-local-repair*
*Completed: 2026-04-15*
