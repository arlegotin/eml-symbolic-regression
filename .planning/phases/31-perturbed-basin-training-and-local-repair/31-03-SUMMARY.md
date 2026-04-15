---
phase: 31-perturbed-basin-training-and-local-repair
plan: 03
subsystem: diagnostics
tags: [perturbed-basin, beer-lambert, diagnostics, campaign, cli, integration]
requires:
  - phase: 31-01
    provides: "Perturbed true-tree runner, proof-perturbed-basin suites, return_kind/raw_status/repair_status aggregate fields"
  - phase: 31-02
    provides: "Target-neighborhood repair and repaired_candidate benchmark taxonomy"
provides:
  - "Beer-Lambert perturbed-basin bound report builder and writer"
  - "diagnostics basin-bound CLI command"
  - "proof-basin campaign preset and campaign status taxonomy propagation"
  - "Stable basin-bound.json and basin-bound.md evidence"
affects: [phase-31, phase-33, proof-campaign-reporting]
tech-stack:
  added: []
  patterns: ["Synthetic fast guardrails plus explicit integration evidence generation"]
key-files:
  created:
    - tests/test_basin_bound_report.py
    - artifacts/diagnostics/phase31-basin-bound/basin-bound.json
    - artifacts/diagnostics/phase31-basin-bound/basin-bound.md
  modified:
    - src/eml_symbolic_regression/diagnostics.py
    - src/eml_symbolic_regression/campaign.py
    - src/eml_symbolic_regression/cli.py
    - tests/test_campaign.py
    - tests/test_diagnostics.py
key-decisions:
  - "Bound support is computed as a continuous prefix over the declared grid; isolated higher-noise passes do not raise the bound."
  - "Rows with repair_status='repaired' are normalized to repaired_candidate in bound reports, even if an upstream aggregate mislabeled evidence_class."
  - "Stable bound reports omit report-level generation timestamps to avoid evidence churn across reruns."
patterns-established:
  - "High-noise probes remain visible as probe rows and outside proof threshold denominators."
  - "Campaign CSV/Markdown surfaces preserve return_kind, raw_status, repair_status, and repair verifier fields."
requirements-completed: [BASN-02, BASN-03, BASN-05]
duration: 15min
completed: 2026-04-15
---

# Phase 31 Plan 03: Beer-Lambert Bound Evidence Summary

**Beer-Lambert perturbed-basin bound reports with CLI/campaign hooks, high-noise probe visibility, and committed repaired-bound evidence**

## Performance

- **Duration:** 15 min
- **Started:** 2026-04-15T19:16:33Z
- **Completed:** 2026-04-15T19:31:21Z
- **Tasks:** 3
- **Files modified:** 8 implementation/test/artifact files plus this summary

## Accomplishments

- Added `build_perturbed_basin_bound_report()` and `write_perturbed_basin_bound_report()` for Beer-Lambert bounded/probe aggregate evidence.
- Added `eml-sr diagnostics basin-bound` and a `proof-basin` campaign preset mapped to `proof-perturbed-basin`.
- Extended campaign CSV and Markdown reports so `return_kind`, `raw_status`, `repair_status`, repair verifier status, and repair move counts remain visible.
- Generated stable bound evidence at:
  - `artifacts/diagnostics/phase31-basin-bound/basin-bound.json`
  - `artifacts/diagnostics/phase31-basin-bound/basin-bound.md`

## Task Commits

1. **Task 1: Build the Beer-Lambert perturbed-bound report**
   - `c6524b6` test: add failing basin bound report tests
   - `3e6b0b2` feat: implement basin bound diagnostics
2. **Task 2: Add CLI and campaign entry points for bound evidence**
   - `77a477e` test: add failing basin CLI and campaign tests
   - `227af66` feat: add basin bound CLI and campaign hooks
3. **Task 3: Run Beer-Lambert bound/probe evidence and lock guardrails**
   - `0bf5d48` test: add failing basin evidence guardrails
   - `a071398` fix: prevent repaired rows from raw bound inflation
   - `a02ff4b` feat: lock Beer-Lambert basin bound evidence
   - `6cf929f` fix: make basin bound evidence reproducible

## Files Created/Modified

- `src/eml_symbolic_regression/diagnostics.py` - Bound report builder/writer, Markdown renderer, continuous-prefix support calculation, repaired-row evidence normalization.
- `src/eml_symbolic_regression/campaign.py` - `proof-basin` preset, run/failure CSV repair columns, proof-basin probe-suite narrative and status taxonomy.
- `src/eml_symbolic_regression/cli.py` - `diagnostics basin-bound` subcommand.
- `tests/test_basin_bound_report.py` - Synthetic fast report tests, CLI subprocess test, forbidden-evidence guardrails, integration evidence generation.
- `tests/test_campaign.py` - Campaign preset, CSV, and Markdown proof-basin guardrails.
- `tests/test_diagnostics.py` - Diagnostics builder export compatibility test.
- `artifacts/diagnostics/phase31-basin-bound/basin-bound.json` - Stable machine-readable evidence.
- `artifacts/diagnostics/phase31-basin-bound/basin-bound.md` - Stable human-readable evidence.

## Decisions Made

- Bound support uses all rows at each declared noise value; every row in the prefix must pass the relevant evidence-class predicate.
- `raw_supported_noise_max` accepts only `perturbed_true_tree_recovered`; `repaired_supported_noise_max` accepts `perturbed_true_tree_recovered` and `repaired_candidate`.
- Probe evidence can recommend `probe_supports_<noise>`, but campaign proof thresholds still come only from `proof-perturbed-basin`.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Repaired rows could inflate raw support if mislabeled upstream**
- **Found during:** Task 3
- **Issue:** A row with `repair_status='repaired'` and an incorrect raw `evidence_class='perturbed_true_tree_recovered'` would have counted toward raw bound support.
- **Fix:** Bound reports now normalize repaired rows to `repaired_candidate` while preserving `raw_status` and `return_kind`.
- **Files modified:** `src/eml_symbolic_regression/diagnostics.py`, `tests/test_basin_bound_report.py`
- **Verification:** `python -m pytest tests/test_basin_bound_report.py tests/test_campaign.py tests/test_diagnostics.py -q -m "not integration"`
- **Committed in:** `a071398`

**2. [Rule 2 - Missing Critical] Stable evidence churned on rerun**
- **Found during:** Task 3 evidence generation
- **Issue:** Report-level generation timestamps made committed evidence change on every integration rerun.
- **Fix:** Removed the report timestamp and used deterministic `/tmp/eml-phase31-basin-bound` integration artifact roots.
- **Files modified:** `src/eml_symbolic_regression/diagnostics.py`, `tests/test_basin_bound_report.py`, `artifacts/diagnostics/phase31-basin-bound/basin-bound.json`
- **Verification:** Re-ran fast and integration verification after the change; `git status --short` remained clean.
- **Committed in:** `6cf929f`

**Total deviations:** 2 auto-fixed (1 bug, 1 missing critical)
**Impact on plan:** Both fixes strengthen the planned evidence contract without broadening scope.

## Verification

- `python -m pytest tests/test_basin_bound_report.py tests/test_campaign.py tests/test_diagnostics.py -q -m "not integration"` -> 28 passed, 1 deselected, 1 warning.
- `python -m pytest tests/test_basin_bound_report.py -q -m integration` -> 1 passed, 10 deselected, 2 warnings.
- `test -f artifacts/diagnostics/phase31-basin-bound/basin-bound.json` -> passed.
- `test -f artifacts/diagnostics/phase31-basin-bound/basin-bound.md` -> passed.

Warnings:
- `PytestUnknownMarkWarning` for `integration` because marker registration lives outside this plan's owned file list.
- Existing `semantics.py:110` overflow warning appears during high-noise Beer-Lambert integration.

## Evidence Outcome

- Bounded Beer-Lambert rows at noise `5.0`: 2/2 raw `perturbed_true_tree_recovered`.
- Probe rows at noise `15.0`: one raw recovery and one `repaired_candidate`.
- Probe rows at noise `35.0`: two `repaired_candidate` rows.
- Report result: `raw_supported_noise_max = 5.0`, `repaired_supported_noise_max = 35.0`, `claim_recommendation = probe_supports_35`.
- High-noise probes remain `row_source = probe` and are not added to the bounded proof threshold denominator.

## Known Stubs

None.

## Issues Encountered

- No blockers. The only residual test warnings are documented above.

## User Setup Required

None.

## Next Phase Readiness

Phase 31 now has committed Beer-Lambert perturbed-basin bound evidence and reporting hooks that Phase 33 can cite. Phase 30 remains separately review-blocked on pure blind/scaffolded semantics and was not altered by this plan.

## Self-Check: PASSED

- Summary file exists at `.planning/phases/31-perturbed-basin-training-and-local-repair/31-03-SUMMARY.md`.
- Task commits exist in git history: `c6524b6`, `3e6b0b2`, `77a477e`, `227af66`, `0bf5d48`, `a071398`, `a02ff4b`, `6cf929f`.
- Stable evidence files exist at `artifacts/diagnostics/phase31-basin-bound/basin-bound.json` and `artifacts/diagnostics/phase31-basin-bound/basin-bound.md`.

---
*Phase: 31-perturbed-basin-training-and-local-repair*
*Completed: 2026-04-15*
