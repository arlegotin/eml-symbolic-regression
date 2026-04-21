# Phase 77: Two-Axis Recovery Accounting and Headline Rebuild - Plan

**Planned:** 2026-04-21
**Status:** Ready for execution

## Objective

Make recovery accounting two-axis: verifier pass status remains visible, while trained recovery headlines exclude compile-only support.

## Tasks

### 1. Run-Level Accounting Fields

- Add derived `verification_outcome`, `evidence_regime`, and `discovery_class` fields to benchmark run artifacts.
- Preserve existing `status`, `claim_status`, `classification`, and `evidence_class` compatibility fields.

### 2. Aggregate Counts

- Add aggregate/group counts for:
  - verification-passed rows,
  - trained exact recoveries,
  - compile-only verified support,
  - unsupported rows,
  - failed rows.
- Keep existing group tables functional.

### 3. Campaign Headline Rebuild

- Update campaign headline metrics JSON/CSV and report Markdown to foreground the corrected two-axis numbers.
- Add run CSV columns for the new accounting fields.

### 4. Claim Audit Gate

- Update the publication claim audit so trained recovery claims exclude compile-only rows.
- Add checks that fail if compile-only rows enter the trained recovery numerator.
- Add corrected headline-count checks for paper-track aggregates.

### 5. Tests

- Add/update regression tests for synthetic aggregates and claim audit behavior.
- Run focused benchmark/campaign/publication tests.

## Acceptance Checks

- Paper-track aggregate logic reports 8 trained exact recoveries and 1 compile-only verified support row.
- Compile-only verified rows remain verifier-passed support but are not trained recoveries.
- Claim audit fails when compile-only rows are counted as trained recovery.
- Existing smoke campaign and publication rebuild tests still pass.
