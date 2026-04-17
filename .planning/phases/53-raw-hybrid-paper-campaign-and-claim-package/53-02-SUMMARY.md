---
phase: 53-raw-hybrid-paper-campaign-and-claim-package
plan: 02
subsystem: reporting
tags: [raw-hybrid, paper-package, artifacts, source-locks, scientific-law-table]

requires:
  - phase: 53-01
    provides: raw-hybrid paper package writer and CLI command
provides:
  - committed v1.9 raw-hybrid paper package artifacts
  - file-level source locks for proof, campaign, repair, and centered-family evidence
  - regime-separated report, scientific-law tables, claim-boundary docs, and centered diagnostics
affects: [phase-53, README, docs, paper-artifacts]

tech-stack:
  added: []
  patterns:
    - artifact generation through synthesis-only CLI commands
    - generated paper packages validated by structural JSON and wording checks before docs cite them

key-files:
  created:
    - artifacts/paper/v1.9/raw-hybrid/manifest.json
    - artifacts/paper/v1.9/raw-hybrid/source-locks.json
    - artifacts/paper/v1.9/raw-hybrid/regime-summary.json
    - artifacts/paper/v1.9/raw-hybrid/raw-hybrid-report.md
    - artifacts/paper/v1.9/raw-hybrid/scientific-law-table.json
    - artifacts/paper/v1.9/raw-hybrid/scientific-law-table.csv
    - artifacts/paper/v1.9/raw-hybrid/scientific-law-table.md
    - artifacts/paper/v1.9/raw-hybrid/claim-boundaries.md
    - artifacts/paper/v1.9/raw-hybrid/centered-negative-diagnostics.md
  modified:
    - src/eml_symbolic_regression/raw_hybrid_paper.py
    - tests/test_raw_hybrid_paper.py

key-decisions:
  - "The v1.9 package cites existing locked v1.6/v1.8/v1.9 evidence instead of rerunning broad campaigns."
  - "Mixed aggregate rows are assigned to regimes from run-level fields, not by applying a source-level default to every row."
  - "Shockley is labeled as `Shockley` in the paper-facing table to match the Phase 53 table contract."

patterns-established:
  - "Generated package validation should check semantic bucket boundaries, not only file existence."
  - "Manifest contracts can keep backward-compatible `preset_id` while also exposing nested `preset.id` for package-level consumers."

requirements-completed: [RHY-01, RHY-02, RHY-03, RHY-04]

duration: 9min
completed: 2026-04-17
---

# Phase 53 Plan 02: Raw-Hybrid Paper Package Artifacts Summary

**Committed v1.9 raw-hybrid paper package with source locks, regime-separated evidence, scientific-law tables, and claim boundaries**

## Performance

- **Duration:** 9 min
- **Started:** 2026-04-17T16:43:45Z
- **Completed:** 2026-04-17T16:51:30Z
- **Tasks:** 2
- **Files modified:** 11 implementation/test files plus 9 generated artifacts

## Accomplishments

- Generated `artifacts/paper/v1.9/raw-hybrid/` through the synthesis-only `raw-hybrid-paper` CLI.
- Validated the package manifest, file-level source locks, generated output inventory, regime buckets, scientific-law table rows, and forbidden claim wording.
- Corrected the package writer so mixed proof aggregates do not leak perturbed, scaffolded, or repaired rows into the Pure Blind bucket.
- Aligned the generated package contract with Phase 53 locks by adding `manifest["preset"]["id"]`, the exact `not blind discovery` phrase, and the `Shockley` law label.

## Task Commits

1. **Task 1 support fix:** `3f09d78` fix(53-02): keep raw hybrid regime buckets scoped
2. **Task 1 contract fix:** `2fe76b7` fix(53-02): align raw hybrid package contract locks
3. **Task 1 artifact generation:** `f63dd6b` docs(53-02): generate raw hybrid paper package

## Files Created/Modified

- `artifacts/paper/v1.9/raw-hybrid/manifest.json` - package manifest with reproduction command, outputs, source list, regime counts, and preset id.
- `artifacts/paper/v1.9/raw-hybrid/source-locks.json` - SHA-256 locks for every declared evidence input file.
- `artifacts/paper/v1.9/raw-hybrid/regime-summary.json` - structured buckets for pure blind, scaffolded, compile-only, warm-start, same-AST, repaired, refit, and perturbed-basin evidence.
- `artifacts/paper/v1.9/raw-hybrid/raw-hybrid-report.md` - human-readable report with separate regime sections.
- `artifacts/paper/v1.9/raw-hybrid/scientific-law-table.json` - machine-readable scientific-law diagnostics.
- `artifacts/paper/v1.9/raw-hybrid/scientific-law-table.csv` - CSV scientific-law diagnostics.
- `artifacts/paper/v1.9/raw-hybrid/scientific-law-table.md` - Markdown scientific-law diagnostics.
- `artifacts/paper/v1.9/raw-hybrid/claim-boundaries.md` - explicit non-blind-discovery claim boundaries.
- `artifacts/paper/v1.9/raw-hybrid/centered-negative-diagnostics.md` - centered-family negative diagnostics with same-family witness caveat.
- `src/eml_symbolic_regression/raw_hybrid_paper.py` - fixed regime bucket classification and package contract details.
- `tests/test_raw_hybrid_paper.py` - added regression coverage for run-level bucket separation and manifest preset contract.

## Verification

- `PYTHONPATH=src python -m eml_symbolic_regression.cli raw-hybrid-paper --output-dir artifacts/paper/v1.9/raw-hybrid --require-existing --overwrite` - passed.
- Manifest/source-lock structural validation snippet from 53-02 - passed.
- Regime/scientific-law/claim-boundary validation snippet from 53-02 - passed.
- `PYTHONPATH=src python -m pytest tests/test_raw_hybrid_paper.py -q` - passed, 10 tests.

## Decisions Made

- Treated the initial mixed Pure Blind report as a correctness defect because it made the report contradict its own regime boundary language.
- Kept the package source inventory unchanged; the fix was row-level classification, not source removal.
- Preserved both `preset_id` and nested `preset.id` in the manifest for compatibility with existing tests and the Phase 53 package lock.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Mixed aggregate rows leaked across regime buckets**
- **Found during:** Task 2 (Validate regime separation, scientific-law rows, and claim boundaries)
- **Issue:** `proof-depth-curve` carried a source-level `pure_blind` default, so perturbed-tree and scaffolded rows appeared in the Pure Blind report section.
- **Fix:** Classified mixed aggregate rows from each run's `start_mode`, `evidence_class`, and repair metadata; added tests for Pure Blind, Scaffolded, and Perturbed Basin boundaries.
- **Files modified:** `src/eml_symbolic_regression/raw_hybrid_paper.py`, `tests/test_raw_hybrid_paper.py`
- **Verification:** `PYTHONPATH=src python -m pytest tests/test_raw_hybrid_paper.py -q`
- **Committed in:** `3f09d78`

**2. [Rule 2 - Missing Critical] Generated package missed exact 53-02 lock contract**
- **Found during:** Task 1 verification
- **Issue:** The manifest exposed only `preset_id`, claim-boundary text lacked the exact phrase `not blind discovery`, and the scientific-law row used `Shockley diode` while the plan contract expected `Shockley`.
- **Fix:** Added nested `preset.id`, an exact non-blind-discovery boundary sentence, and the `Shockley` law label with test updates.
- **Files modified:** `src/eml_symbolic_regression/raw_hybrid_paper.py`, `tests/test_raw_hybrid_paper.py`
- **Verification:** `PYTHONPATH=src python -m pytest tests/test_raw_hybrid_paper.py -q`
- **Committed in:** `2fe76b7`

---

**Total deviations:** 2 auto-fixed missing-critical issues.
**Impact on plan:** The fixes narrowed report semantics to the Phase 53 claim boundary; no broad campaigns or unrelated refactors were introduced.

## Issues Encountered

The first generated package validated file existence but did not pass stronger contract checks. The writer was corrected and the package was regenerated before artifacts were committed.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Plan 53-03 can update README and implementation docs against the committed package root and add file-backed regression tests over the generated artifacts.

## Self-Check: PASSED

- Generated package root exists: `artifacts/paper/v1.9/raw-hybrid/`.
- All nine declared package outputs exist and were committed.
- Source locks contain file-level SHA-256 values.
- Scientific-law table includes Beer-Lambert, Shockley, Arrhenius, Michaelis-Menten, Planck diagnostic, logistic diagnostic, and historical Michaelis diagnostic rows.
- Claim wording preserves warm-start, same-AST, scaffolded, repaired, refit, compile-only, perturbed-basin, and centered-family boundaries.

---
*Phase: 53-raw-hybrid-paper-campaign-and-claim-package*
*Completed: 2026-04-17*
