---
phase: 24-baseline-failure-triage-and-diagnostic-harness
verified: 2026-04-15T14:40:00Z
status: passed
score: 4/4 must-haves verified
---

# Phase 24: Baseline Failure Triage and Diagnostic Harness Verification Report

**Phase Goal:** Users can inspect and rerun focused diagnostics for the exact v1.3 failure modes before changing optimizer/compiler behavior.
**Verified:** 2026-04-15T14:40:00Z
**Status:** passed

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Baseline triage compares v1.3 standard and showcase failures by formula, start mode, perturbation noise, and recovery class. | VERIFIED | `artifacts/diagnostics/v1.4-baseline/triage.md` contains Failure Groups for both campaigns. |
| 2 | Triage rows link to representative raw run artifacts and include optimizer/verifier metrics. | VERIFIED | Representative Failure Runs table links raw JSON artifacts and includes best loss, snap loss, margin, changed slots, and verifier status. |
| 3 | Focused diagnostic reruns can target blind failures, Beer-Lambert perturbation failures, and compiler/depth gates without a full campaign. | VERIFIED | `diagnostics rerun` supports the three targets and `RunFilter` supports exact case/seed/noise filters. |
| 4 | v1.3 aggregate and suite-result fingerprints are persisted without modifying v1.3 campaign folders. | VERIFIED | `baseline-lock.json` contains SHA-256 fingerprints for v1.3 campaign files; git status did not show v1.3 artifact modifications. |

**Score:** 4/4 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/eml_symbolic_regression/diagnostics.py` | Diagnostics API | EXISTS + SUBSTANTIVE | Contains triage, selection, lock, and rerun helpers. |
| `tests/test_diagnostics.py` | Test coverage | EXISTS + SUBSTANTIVE | Covers report/lock output and exact perturbation filter selection. |
| `artifacts/diagnostics/v1.4-baseline/triage.md` | Baseline report | EXISTS + SUBSTANTIVE | Generated from committed v1.3 standard/showcase campaigns. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|----|--------|---------|
| CLI | Diagnostics module | `diagnostics triage` / `diagnostics rerun` | WIRED | `src/eml_symbolic_regression/cli.py` imports and calls diagnostics helpers. |
| Diagnostics rerun | Campaign runner | `run_diagnostic_subset` -> `run_campaign` | WIRED | Focused subsets reuse campaign output contracts. |
| Beer perturbation selection | Benchmark runner | `RunFilter.perturbation_noises` | WIRED | Tests assert exact `(35.0,)` filter selection. |

## Requirements Coverage

| Requirement | Status | Blocking Issue |
|-------------|--------|----------------|
| DIAG-01 | SATISFIED | - |
| DIAG-02 | SATISFIED | - |
| DIAG-03 | SATISFIED | - |
| DIAG-04 | SATISFIED | - |

**Coverage:** 4/4 requirements satisfied

## Automated Checks

```bash
python -m pytest tests/test_diagnostics.py tests/test_benchmark_runner.py tests/test_campaign.py -q
```

Result: 14 passed, 1 expected runtime warning from overflow-path benchmark semantics.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli diagnostics triage --baseline artifacts/campaigns/v1.3-standard --baseline artifacts/campaigns/v1.3-showcase --output-dir artifacts/diagnostics/v1.4-baseline
```

Result: report and baseline lock generated.

## Human Verification Required

None - all verifiable items checked programmatically.

## Gaps Summary

**No gaps found.** Phase goal achieved. Ready to proceed.
