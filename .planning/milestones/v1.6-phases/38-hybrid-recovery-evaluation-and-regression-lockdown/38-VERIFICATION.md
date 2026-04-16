---
phase: 38-hybrid-recovery-evaluation-and-regression-lockdown
verified: 2026-04-16T12:14:20Z
status: passed
score: 4/4 must-haves verified
score_verified: 4
score_total: 4
overrides_applied: 0
requirements:
  - id: EVAL-01
    status: satisfied
    evidence: "Campaign and proof reports now include explicit regime summary sections for blind, warm-start, compile-only, catalog, and perturbed-basin evidence."
  - id: EVAL-02
    status: satisfied
    evidence: "Comparison outputs and proof bundles now emit immutable lock manifests for archived anchors and use version-agnostic comparison wording."
  - id: EVAL-03
    status: satisfied
    evidence: "Aggregate/report regression tests now fail if selected/fallback candidate IDs or refit metrics disappear from emitted run rows."
  - id: EVAL-04
    status: satisfied
    evidence: "Measured `reported` proof verdicts stay distinct from bounded claims, and docs/reports keep weak-dominance evidence separate from blind-discovery claims."
---

# Phase 38: Hybrid Recovery Evaluation and Regression Lockdown Verification Report

**Phase Goal:** Users can compare the upgraded hybrid pipeline against archived baselines with honest reporting about what improved and what remains unresolved.
**Verified:** 2026-04-16T12:14:20Z
**Status:** passed

## Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Campaign and proof bundles expose regime separation explicitly. | VERIFIED | `campaign.py` and `proof_campaign.py` now render `## Regime Summary` tables before narrative interpretation. |
| 2 | Comparison outputs are generic and preserve immutable anchor locks. | VERIFIED | `write_campaign_comparison()` writes `comparison-lock.json`, generic markdown, and the JSON payload now includes baseline and candidate lock manifests. |
| 3 | Measured proof thresholds remain measured instead of being mislabeled as bounded claims. | VERIFIED | `_claim_verdict("reported")` now returns `reported`, and proof-bundle tests lock that behavior for the depth-curve claim. |
| 4 | Hybrid-stage weak-dominance metadata is locked at the reporting layer. | VERIFIED | Aggregate-report tests now assert that selected/fallback candidate IDs and refit metrics survive into aggregate run rows. |

**Score:** 4/4 truths verified

## Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Proof and campaign report updates | `python -m pytest tests/test_proof_campaign.py tests/test_campaign.py -q` | 14 passed | PASS |
| Comparison tooling and aggregate regression locks | `python -m pytest tests/test_diagnostics.py tests/test_benchmark_reports.py -q` | 23 passed | PASS |
| Consolidated phase 37-38 surface | `python -m pytest tests/test_compiler_warm_start.py tests/test_benchmark_runner.py tests/test_proof_campaign.py tests/test_campaign.py tests/test_diagnostics.py tests/test_benchmark_reports.py tests/test_benchmark_contract.py -q` | 120 passed, 4 expected numerical warnings from existing overflow-heavy paths | PASS |

## Requirements Coverage

| Requirement | Description | Status | Evidence |
|-------------|-------------|--------|----------|
| EVAL-01 | Regimes remain separate in run artifacts and reports | SATISFIED | New regime summary sections in campaign and proof reports |
| EVAL-02 | Archived v1.5/v1.4 anchors can be compared without overwriting outputs | SATISFIED | Generic comparison artifacts plus proof-bundle and comparison lock manifests |
| EVAL-03 | Regression tests fail if hybrid stages regress below fallback auditability | SATISFIED | Aggregate-level tests lock selection/fallback/refit metrics in emitted run rows |
| EVAL-04 | Reports distinguish weak-dominance claims from measured boundaries | SATISFIED | Corrected `reported` verdict, generic comparison wording, and updated README/report text |

## Gaps Summary

No Phase 38 implementation gaps remain. The only remaining milestone close-out step is explicit archive/tagging of v1.6 into `.planning/milestones/`, which was not executed automatically here.

---

_Verified: 2026-04-16T12:14:20Z_
_Verifier: Codex_
