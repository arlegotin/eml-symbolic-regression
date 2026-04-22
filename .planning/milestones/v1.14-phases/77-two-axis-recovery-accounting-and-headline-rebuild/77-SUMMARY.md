# Phase 77: Two-Axis Recovery Accounting and Headline Rebuild - Summary

**Completed:** 2026-04-21
**Status:** Complete
**Implementation commit:** `2ab6890`

## What Changed

- Added run-level `verification_outcome`, `evidence_regime`, and `discovery_class` fields to benchmark artifacts and aggregate rows.
- Added aggregate counts for:
  - verification-passed rows,
  - trained exact recoveries,
  - compile-only verified support,
  - unsupported rows,
  - failed rows.
- Updated aggregate Markdown, track summaries, campaign CSVs, headline metrics, regime summary, and campaign report text to separate verifier pass counts from trained recovery claims.
- Updated publication claim audit logic so compile-only verified rows are audited as support rows, not trained recovery rows.
- Added claim-audit checks for compile-only recovery promotion and corrected paper-track headline counts.
- Added regression tests for two-axis aggregate accounting and compile-only audit rejection.

## Requirement Coverage

- `REC-01`: Complete. Run and aggregate outputs now expose `verification_outcome`, `evidence_regime`, and `discovery_class`.
- `REC-02`: Complete. `start_mode=compile` verifier passes are classified as `compile_only_verified_support`.
- `REC-03`: Complete in code/audit logic. The publication-track audit expects 8 trained exact recoveries, 1 compile-only verified support row, 15 unsupported rows, and 0 failed rows.
- `REC-04`: Complete. Tests and claim-audit checks fail if compile-only rows are promoted into trained recovery.

## Verification

- Focused accounting suite passed.
- Broader benchmark/campaign/publication/baseline slice passed after the accounting schema update.
- `git diff --check` passed.

## Notes

- Existing compatibility fields such as `claim_status`, `classification`, `evidence_class`, and `verifier_recovered` are preserved.
- Historical generated artifacts are not rewritten in this phase; Phase 81 performs the corrected evidence rebuild.
