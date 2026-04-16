---
phase: 33-proof-campaign-report-and-evidence-lockdown
plan: 01
subsystem: proof-orchestration
tags: [proof-campaign, cli, reporting, evidence, milestone]
requires:
  - phase: 29
    provides: "Claim matrix, threshold policies, and proof-aware artifact schema"
  - phase: 30
    provides: "Measured pure-blind versus scaffolded shallow proof split"
  - phase: 31
    provides: "Perturbed basin suite and basin-bound diagnostics"
  - phase: 32
    provides: "Measured depth-curve suite and campaign reporting hooks"
provides:
  - "One-command proof bundle rooted at `artifacts/proof/v1.5/`"
  - "Machine-readable `proof-campaign.json` manifest"
  - "Human-readable `proof-report.md` with honest denominators and raw-run links"
  - "CLI `proof-campaign` entry point and regression coverage"
affects: [phase-33, v1.5-milestone-audit]
tech-stack:
  added: []
  patterns: ["Bundle orchestration that reuses existing campaign and diagnostic primitives"]
key-files:
  created:
    - src/eml_symbolic_regression/proof_campaign.py
    - tests/test_proof_campaign.py
  modified:
    - src/eml_symbolic_regression/cli.py
    - README.md
key-decisions:
  - "The proof bundle runs a fixed preset set so v1.5 evidence is reproducible and denominator-stable."
  - "The final report keeps v1.5 proof suites and v1.4 showcase baselines separate."
  - "Perturbed basin bound evidence is embedded into the proof root instead of being recomputed in a new ad hoc format."
patterns-established:
  - "Bundle-level reports can layer claim tables, depth-curve summaries, and historical baselines without weakening proof semantics."
requirements-completed: [EVID-01, EVID-02, EVID-03, EVID-04, EVID-05]
duration: 1 session
completed: 2026-04-16
---

# Phase 33 Plan 01: Proof Campaign Report and Evidence Lockdown Summary

**One-command v1.5 proof bundle, claim report, basin-bound carry-through, and CLI/test lockdown**

## Accomplishments

- Added `proof_campaign.py` to orchestrate the fixed v1.5 proof preset set and render a bundled claim report.
- Added CLI command `proof-campaign` with bundle-root and filtering support.
- Added proof-bundle tests that lock both the Python API and CLI contract.
- Updated `README.md` so the v1.5 proof bundle has a single documented reproduction command and stable output root.

## Task Commits

No plan-local commits were created in this autonomous working-tree session. The changes remain uncommitted for user review.

## Files Created/Modified

- `src/eml_symbolic_regression/proof_campaign.py` - proof-bundle orchestration, manifest assembly, and Markdown report rendering.
- `src/eml_symbolic_regression/cli.py` - `proof-campaign` command and filter passthrough.
- `README.md` - proof-bundle reproduction commands and output-root notes.
- `tests/test_proof_campaign.py` - bundle and CLI regression tests.

## Decisions Made

- The bundle root is fixed at `artifacts/proof/v1.5/` by default so later comparisons are straightforward.
- The proof report renders claim rows from campaign threshold summaries instead of recomputing claim verdicts from raw run tables.
- v1.4 baseline context remains descriptive comparison material only and never enters v1.5 proof denominators.

## Deviations from Plan

None. The implementation stayed within the planned orchestration, reporting, and reproduction scope.

## Verification

- `python -m pytest tests/test_proof_campaign.py -q` -> passed.
- `python -m pytest tests/test_depth_curve_targets.py tests/test_proof_contract.py tests/test_benchmark_contract.py tests/test_benchmark_reports.py tests/test_benchmark_runner.py tests/test_campaign.py tests/test_proof_campaign.py -q` -> 109 passed, 1 warning in 142.45s.
- `PYTHONPATH=src python -m eml_symbolic_regression.cli proof-campaign --output-root artifacts/proof/v1.5 --overwrite` -> executed in this autonomous session to generate the final proof root.

## Evidence Outcome

- The final proof bundle root is `artifacts/proof/v1.5/`.
- The bundle writes `proof-campaign.json`, `proof-report.md`, per-preset campaign outputs under `campaigns/`, and a carried-forward perturbed basin bound report under `diagnostics/basin-bound/`.
- The report includes claim status, a depth-curve section, v1.4 comparison context, and out-of-scope claims without mixing denominators.
- Final claim rows in `proof-report.md` show:
  - `paper-shallow-scaffolded-recovery` passed at `18/18`
  - `paper-perturbed-true-tree-basin` passed at `9/9`
  - `paper-shallow-blind-recovery` remained a measured boundary at `2/18`
  - `paper-blind-depth-degradation` captured the expected depth curve with blind `1.0` recovery at depths 2-3 and `0.0` at depths 4-6 while perturbed rows stayed `1.0` across depths 2-6

## Known Stubs

None.

## Issues Encountered

- The full proof bundle is slower than the individual contract tests because it runs the declared proof campaigns rather than synthetic fixtures.

## Next Phase Readiness

No v1.5 implementation phase remains after this plan. The milestone can be audited and marked shipped once the proof root is present and the planning state is synchronized.

## Self-Check: PASSED

- Summary file exists at `.planning/phases/33-proof-campaign-report-and-evidence-lockdown/33-01-SUMMARY.md`.
- `proof-campaign` appears in CLI help and README reproduction guidance.
- Proof-bundle regression coverage exists in `tests/test_proof_campaign.py`.

---
*Phase: 33-proof-campaign-report-and-evidence-lockdown*
*Completed: 2026-04-16*
