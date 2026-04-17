---
phase: 53-raw-hybrid-paper-campaign-and-claim-package
plan: 03
subsystem: documentation
tags: [raw-hybrid, paper-package, regression-tests, docs, claim-boundaries]

requires:
  - phase: 53-02
    provides: committed raw-hybrid paper package artifacts
provides:
  - file-backed regression locks for the v1.9 raw-hybrid paper package
  - README command and regime-safe package summary
  - implementation documentation for source locks, package outputs, scientific-law columns, and claim boundaries
affects: [phase-53, README, docs, tests, paper-artifacts]

tech-stack:
  added: []
  patterns:
    - generated paper packages are locked by tests that read committed artifact files directly
    - public documentation cites artifact roots only after package generation and validation

key-files:
  created:
    - tests/test_raw_hybrid_paper_regression.py
  modified:
    - README.md
    - docs/IMPLEMENTATION.md
    - artifacts/paper/v1.9/raw-hybrid/manifest.json
    - artifacts/paper/v1.9/raw-hybrid/source-locks.json

key-decisions:
  - "Docs cite the v1.9 package root only after 53-02 artifacts and 53-03 regression locks passed."
  - "README and implementation docs keep Arrhenius and Michaelis-Menten as exact compiler warm-start / same-AST evidence, not blind discovery."
  - "Planck and logistic remain unsupported/stretch diagnostics in the paper package."

patterns-established:
  - "Regression tests should assert package schema, source locks, regime buckets, scientific-law rows, and forbidden claim wording together."
  - "Docs should name evidence regimes explicitly instead of using one merged recovery headline."

requirements-completed: [RHY-02, RHY-03, RHY-04, RHY-05]

duration: 7min
completed: 2026-04-17
---

# Phase 53 Plan 03: Raw-Hybrid Docs and Regression Locks Summary

**Artifact-backed raw-hybrid package regression tests plus README and implementation documentation that preserve evidence boundaries**

## Performance

- **Duration:** 7 min
- **Started:** 2026-04-17T16:52:40Z
- **Completed:** 2026-04-17T16:58:20Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments

- Added `tests/test_raw_hybrid_paper_regression.py` to lock the committed package output inventory, manifest schema, source locks, regime buckets, scientific-law rows, and forbidden claim wording.
- Added the `raw-hybrid-paper` command to README and documented the package root `artifacts/paper/v1.9/raw-hybrid/`.
- Added implementation notes for the package writer contract, source-lock behavior, artifact inventory, scientific-law table columns, claim-boundary policy, centered-family same-family witness caveat, and Planck/logistic unsupported diagnostics.
- Re-ran the package command with `--overwrite` and committed the resulting manifest/source-lock timestamp refresh.

## Task Commits

1. **Task 1:** `14da588` test(53-03): lock raw hybrid paper package artifacts
2. **Task 2:** `e1c8101` docs(53-03): document raw hybrid paper package
3. **Final package refresh:** `28c15e3` docs(53-03): refresh raw hybrid package locks

## Files Created/Modified

- `tests/test_raw_hybrid_paper_regression.py` - File-backed regression tests for package schema, locks, regimes, rows, and wording.
- `README.md` - Added the package command and a regime-safe summary of the v1.9 raw-hybrid paper package.
- `docs/IMPLEMENTATION.md` - Added the raw-hybrid paper package contract and output inventory.
- `artifacts/paper/v1.9/raw-hybrid/manifest.json` - Refreshed after final package generation.
- `artifacts/paper/v1.9/raw-hybrid/source-locks.json` - Refreshed after final package generation.

## Test Results

- `PYTHONPATH=src python -m eml_symbolic_regression.cli raw-hybrid-paper --output-dir artifacts/paper/v1.9/raw-hybrid --require-existing --overwrite` - passed.
- `PYTHONPATH=src python -m pytest tests/test_raw_hybrid_paper.py tests/test_raw_hybrid_paper_regression.py -q` - passed, 15 tests.
- `PYTHONPATH=src python -m pytest tests/test_paper_decision.py tests/test_campaign.py::test_reproduction_command_quotes_shell_sensitive_values -q` - passed, 4 tests.
- `rg "raw-hybrid-paper|artifacts/paper/v1\\.9/raw-hybrid|scientific-law-table|source-locks|not blind discovery|same-family witness" README.md docs/IMPLEMENTATION.md` - passed.
- Documentation forbidden-phrase Python check - passed.

## Decisions Made

- Kept the regression lock public-artifact oriented; it reads committed package files and does not import private writer helpers.
- Documented the raw-hybrid package as a synthesis artifact, not a new evidence denominator or broad campaign run.
- Preserved centered-family wording as negative diagnostic evidence under the same-family witness caveat.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase 53 has all three plans complete and is ready for code review, verification, and phase completion routing.

## Self-Check: PASSED

- Package regression tests exist and pass.
- README and implementation docs cite `artifacts/paper/v1.9/raw-hybrid/`.
- Documentation includes `not blind discovery` and `same-family witness` wording.
- The final package regeneration was committed.

---
*Phase: 53-raw-hybrid-paper-campaign-and-claim-package*
*Completed: 2026-04-17*
