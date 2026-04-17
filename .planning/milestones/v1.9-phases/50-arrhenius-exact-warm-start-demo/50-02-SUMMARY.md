---
phase: 50-arrhenius-exact-warm-start-demo
plan: 02
subsystem: benchmarks
tags: [arrhenius, benchmark-suite, same-ast, warm-start, pytest]
requires:
  - phase: 50-01
    provides: Built-in `arrhenius` demo with strict compile and same-AST warm-start evidence.
provides:
  - Built-in suite `v1.9-arrhenius-evidence` with exactly one `arrhenius-warm` run.
  - Contract coverage for stable Arrhenius suite expansion.
  - Runner artifact regression proving `direct_division_template`, `same_ast_return`, verifier `recovered`, and evidence class `same_ast`.
affects: [benchmark-registry, benchmark-artifacts, raw-hybrid-paper-suite, phase-53]
tech-stack:
  added: []
  patterns: [focused evidence suites, same-AST artifact regression]
key-files:
  created:
    - .planning/phases/50-arrhenius-exact-warm-start-demo/50-02-SUMMARY.md
  modified:
    - src/eml_symbolic_regression/benchmark.py
    - tests/test_benchmark_contract.py
    - tests/test_benchmark_runner.py
key-decisions:
  - "Arrhenius benchmark evidence is isolated in `v1.9-arrhenius-evidence` instead of broadening existing campaign denominators."
  - "The `arrhenius-warm` benchmark path is classified as `same_ast`, not blind discovery."
patterns-established:
  - "Use one-case focused benchmark suites for reproducible scientific-law evidence before paper-facing packaging."
requirements-completed: [ARR-04]
duration: 7min
completed: 2026-04-17
---

# Phase 50 Plan 02: Arrhenius Benchmark Evidence Summary

**Focused Arrhenius benchmark suite with same-AST warm-start artifact evidence for normalized `exp(-0.8/x)`**

## Performance

- **Duration:** 7 min
- **Started:** 2026-04-17T12:52:34Z
- **Completed:** 2026-04-17T12:59:00Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments

- Added built-in suite `v1.9-arrhenius-evidence` with exactly one case, `arrhenius-warm`.
- Locked suite expansion to demo id `arrhenius`, start mode `warm_start`, seed `0`, perturbation noise `0.0`, `24` points, `warm_steps=1`, and tags `v1.9`, `arrhenius`, `warm_start`, `same_ast`.
- Added runner coverage proving the artifact records compile depth `7`, macro hit `direct_division_template`, status `same_ast_return`, verifier `recovered`, and evidence class `same_ast`.
- Kept the evidence out of broad v1.3/v1.8 suites and did not reclassify Michaelis-Menten or Planck.

## Task Commits

Each task was committed atomically:

1. **Task 1 RED: Arrhenius benchmark suite contract** - `0a41de2` (test)
2. **Task 1 GREEN: Focused Arrhenius evidence suite** - `d2bc599` (feat)
3. **Task 2: Same-AST benchmark artifact regression** - `521f813` (test)

**Plan metadata:** summary/state commit for this file.

_Note: Task 2 was a test-only lock because Task 1's suite registration connected to existing benchmark artifact serialization._

## Files Created/Modified

- `src/eml_symbolic_regression/benchmark.py` - Added `v1.9-arrhenius-evidence` to the built-in registry and returned one focused `arrhenius-warm` case.
- `tests/test_benchmark_contract.py` - Added registry and stable expansion assertions for the focused Arrhenius suite and positive domains.
- `tests/test_benchmark_runner.py` - Added artifact assertions for same-AST warm-start evidence and aggregate classification.
- `.planning/phases/50-arrhenius-exact-warm-start-demo/50-02-SUMMARY.md` - Recorded execution evidence and GSD metadata.

## Decisions Made

- Used a focused one-case benchmark suite rather than adding Arrhenius to standard/showcase family suites.
- Kept `max_warm_depth` at the default `14`; the strict compile depth remains `7`.
- Treated the result as same-AST warm-start evidence: top-level verifier status is `recovered`, but the evidence class is `same_ast` and aggregate classification is `same_ast_warm_start_return`.

## Verification

Focused plan verification passed:

```bash
PYTHONPATH=src python -m pytest \
  tests/test_benchmark_contract.py::test_builtin_suite_registry_expands_stable_run_ids \
  tests/test_benchmark_contract.py::test_arrhenius_evidence_suite_contains_exact_warm_start_case \
  tests/test_benchmark_runner.py::test_arrhenius_warm_benchmark_records_same_ast_evidence \
  -q
```

Result: `3 passed in 3.94s`.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- Task 2 passed immediately after Task 1 because the existing benchmark runner already serialized compiled EML metadata, warm-start diagnostics, verifier status, evidence class, dataset manifest domains, and aggregate classification. No production runner change was required.

## Known Stubs

None introduced. Stub scan over modified source and test files found only pre-existing optional `None` fields, empty collection assertions, and the existing internal `placeholder` variable used for stable run-id construction.

## User Setup Required

None - no external service configuration required.

## Threat Flags

None. The plan touched the declared built-in suite registry and benchmark artifact/reporting boundary only; it introduced no new network endpoints, auth paths, file access patterns, or schema trust boundary outside the plan threat model.

## Next Phase Readiness

Phase 50 can proceed to Plan 03 with a reproducible focused benchmark path. The suite-level artifact evidence is same-AST warm-start evidence and is ready to be generated/documented without broadening campaign denominators.

## Self-Check: PASSED

- Found summary file `.planning/phases/50-arrhenius-exact-warm-start-demo/50-02-SUMMARY.md`.
- Found modified source/test files `src/eml_symbolic_regression/benchmark.py`, `tests/test_benchmark_contract.py`, and `tests/test_benchmark_runner.py`.
- Found task commits `0a41de2`, `d2bc599`, and `521f813` in git history.
- No tracked file deletions were introduced by task commits.

---
*Phase: 50-arrhenius-exact-warm-start-demo*
*Completed: 2026-04-17*
