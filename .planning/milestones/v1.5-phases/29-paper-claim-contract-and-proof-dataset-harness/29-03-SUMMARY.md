---
phase: 29-paper-claim-contract-and-proof-dataset-harness
plan: 03
subsystem: proof-campaign-cli
tags: [python, argparse, pytest, campaign, proof-contract]

# Dependency graph
requires:
  - phase: 29-paper-claim-contract-and-proof-dataset-harness
    provides: Plan 01 claim/dataset contracts and Plan 02 proof-aware benchmark aggregate fields
provides:
  - CLI commands for claim matrix inspection and proof dataset manifest generation
  - Proof metadata columns and grouped tables in campaign artifacts
  - Campaign report proof contract section sourced from claim threshold summaries
affects: [phase-30-shallow-proof, phase-33-proof-report]

# Tech tracking
tech-stack:
  added: []
  patterns: [subprocess CLI smoke tests, proof metadata CSV propagation, aggregate-threshold report section]

key-files:
  created:
    - .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-03-SUMMARY.md
  modified:
    - src/eml_symbolic_regression/cli.py
    - src/eml_symbolic_regression/campaign.py
    - tests/test_benchmark_runner.py
    - tests/test_campaign.py

key-decisions:
  - "Proof dataset CLI writes deterministic manifests only; raw arrays remain omitted from Phase 29 artifacts."
  - "Campaign reports derive proof status from aggregate threshold rows, not per-run CSV rows."
  - "STATE.md, ROADMAP.md, and REQUIREMENTS.md were not updated because the sequential orchestrator owns final phase state updates."

patterns-established:
  - "Claim-aware campaign reports render a Proof Contract table only when aggregate runs include claim IDs."
  - "Campaign CSVs preserve recovery_class as the legacy classification alias while adding claim, threshold, dataset digest, and provenance columns."

requirements-completed: [CLAIM-01, CLAIM-02, CLAIM-03, CLAIM-04]

# Metrics
duration: 7m 39s
completed: 2026-04-15
---

# Phase 29 Plan 03: Proof CLI and Campaign Propagation Summary

**Proof claim inspection, deterministic proof dataset manifests, and campaign-level proof metadata/reporting**

## Performance

- **Duration:** 7m 39s
- **Started:** 2026-04-15T13:44:49Z
- **Completed:** 2026-04-15T13:52:28Z
- **Tasks:** 3 TDD tasks
- **Files modified:** 4 implementation/test files plus this summary

## Accomplishments

- Added `list-claims` and `proof-dataset` CLI commands backed by the Plan 01 claim registry and dataset manifest helper.
- Extended campaign `runs.csv`, grouped CSV tables, and campaign manifests with claim ID/class, training mode, evidence class, threshold policy, dataset manifest digest, and provenance fields.
- Added `proof-shallow` campaign preset for filtered execution of the built-in `v1.5-shallow-proof` suite.
- Added a `## Proof Contract` campaign report section that renders claim-level threshold rows separately from headline showcase recovery metrics.

## Task Commits

Each TDD task was committed atomically:

1. **Task 1 RED: CLI proof inspection tests** - `0698b0e` (test)
2. **Task 1 GREEN: proof CLI commands** - `068559e` (feat)
3. **Task 2 RED: campaign proof metadata tests** - `a72c937` (test)
4. **Task 2 GREEN: campaign proof propagation** - `04ac54a` (feat)
5. **Task 3 RED: proof report contract tests** - `692d60e` (test)
6. **Task 3 GREEN: proof report section** - `fc1f0fe` (feat)

**Plan metadata:** this summary file is committed separately as `docs(29-03): complete proof CLI and campaign propagation plan`.

## Files Created/Modified

- `src/eml_symbolic_regression/cli.py` - Added `list-claims` and `proof-dataset` subcommands.
- `src/eml_symbolic_regression/campaign.py` - Added proof campaign preset, proof metadata CSV/table/manifest propagation, and proof report section.
- `tests/test_benchmark_runner.py` - Added subprocess CLI smoke tests for claim inspection and proof dataset manifest generation.
- `tests/test_campaign.py` - Added proof campaign table, manifest, and report tests while preserving legacy smoke campaign expectations.

## Decisions Made

- Kept `proof-dataset --output` local and additive, using the existing `_write_json` parent creation behavior and no shell/path expansion.
- Added `proof-shallow` as the campaign entry point for `v1.5-shallow-proof` so downstream proof campaigns can be run through the existing campaign CLI.
- Kept threshold status at claim/policy aggregate level in `manifest["thresholds"]` and the report table, not in per-run CSV rows.
- Left final phase state, roadmap, and requirement updates to the orchestrator, per the sequential executor prompt.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Added proof campaign preset for the v1.5 shallow proof suite**
- **Found during:** Task 2 (campaign table and manifest propagation)
- **Issue:** The plan required a filtered campaign against `v1.5-shallow-proof`, but campaign execution only accepts named presets.
- **Fix:** Added a `proof-shallow` campaign preset that maps to the existing `v1.5-shallow-proof` benchmark suite.
- **Files modified:** `src/eml_symbolic_regression/campaign.py`, `tests/test_campaign.py`
- **Verification:** `python -m pytest tests/test_campaign.py -q`
- **Committed in:** `04ac54a`

**2. [Rule 1 - Bug] Kept threshold-policy grouping safe for legacy runs**
- **Found during:** Task 2 (new grouped threshold policy table)
- **Issue:** Legacy smoke/campaign runs have `threshold=None`, so the new threshold-policy grouping needed to avoid assuming a mapping.
- **Fix:** Grouped threshold policy rows via `(run.get("threshold") or {}).get("id")`, preserving legacy smoke behavior.
- **Files modified:** `src/eml_symbolic_regression/campaign.py`
- **Verification:** `python -m pytest tests/test_campaign.py -q`
- **Committed in:** `04ac54a`

---

**Total deviations:** 2 auto-fixed (1 missing critical, 1 bug)
**Impact on plan:** Both changes were required to satisfy the plan without breaking legacy campaign behavior. No deferred scope was implemented.

## Issues Encountered

- TDD RED phases failed as expected for missing CLI commands, missing campaign proof metadata propagation, and missing proof report section.
- The verification suite still emits the existing `semantics.py` overflow warning in `test_runner_filter_executes_subset`; no new warning source was introduced.

## User Setup Required

None - no external service configuration required.

## Verification

- `python -m pytest tests/test_benchmark_runner.py -q` - passed, 10 tests, 1 existing overflow warning.
- `python -m pytest tests/test_campaign.py -q` - passed, 8 tests.
- `python -m pytest tests/test_benchmark_runner.py tests/test_campaign.py -q` - passed, 18 tests, 1 existing overflow warning.
- `python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_reports.py tests/test_benchmark_runner.py tests/test_campaign.py tests/test_proof_contract.py tests/test_proof_dataset_manifest.py -q` - passed, 47 tests, 1 existing overflow warning.
- Acceptance `rg` checks for CLI commands, proof campaign metadata columns/tables, and proof report wording all returned matches.

## Known Stubs

None. Stub scan found no TODO, FIXME, placeholder, coming soon, not available, or hardcoded empty UI/data payload patterns in created/modified files; the only text match was the normal file-write mode string `open("w", ...)`.

## Threat Flags

None. The planned local CLI filesystem output, campaign CSV/manifest propagation, and report wording trust boundaries were implemented without adding new network endpoints, auth paths, or additional trust boundaries.

## Next Phase Readiness

Phase 30 can use `list-claims`, `proof-dataset`, and the `proof-shallow` campaign preset to run bounded shallow proof work while retaining claim, threshold, dataset digest, and provenance context in campaign artifacts. Phase 33 can consume manifest threshold rows and the report proof section directly.

## Self-Check: PASSED

- Summary file exists at `.planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-03-SUMMARY.md`.
- Modified files exist: `src/eml_symbolic_regression/cli.py`, `src/eml_symbolic_regression/campaign.py`, `tests/test_benchmark_runner.py`, and `tests/test_campaign.py`.
- Task commits found in git history: `0698b0e`, `068559e`, `a72c937`, `04ac54a`, `692d60e`, `fc1f0fe`.
- Stub scan found no actionable stubs in created/modified files.

---
*Phase: 29-paper-claim-contract-and-proof-dataset-harness*
*Completed: 2026-04-15*
