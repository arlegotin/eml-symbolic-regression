---
phase: 28-before-after-campaign-evaluation
verified: 2026-04-15T16:55:00Z
status: passed
score: 5/5 must-haves verified
---

# Phase 28: Before/After Campaign Evaluation Verification Report

**Phase Goal:** Users can see whether v1.4 improved real end-to-end performance by rerunning the same campaign contracts and comparing against v1.3 baselines.
**Verified:** 2026-04-15T16:55:00Z
**Status:** passed

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | v1.4 standard and showcase campaign folders are generated after v1.4 code changes. | VERIFIED | `artifacts/campaigns/v1.4-standard/` and `artifacts/campaigns/v1.4-showcase/` exist with reports, aggregates, tables, figures, and raw run artifacts. |
| 2 | Comparison reports compute recovery, unsupported, failure, loss, and runtime deltas against v1.3 baselines. | VERIFIED | `artifacts/campaigns/v1.4-comparison/comparison.json` contains metrics and deltas for all categories. |
| 3 | Target categories are classified as improved, regressed, or unchanged. | VERIFIED | `comparison.md` reports `overall` improved, `blind_recovery` improved, `beer_perturbation` unchanged, and `compiler_coverage` improved. |
| 4 | A single documented command reproduces the comparison from existing campaign folders. | VERIFIED | `README.md` and `comparison.md` both include the `diagnostics compare` command. |
| 5 | Tests cover comparison behavior and the integrated campaign/optimizer/compiler paths. | VERIFIED | Full suite passed: 58 tests. |

**Score:** 5/5 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/eml_symbolic_regression/diagnostics.py` | Comparison helpers | EXISTS + SUBSTANTIVE | Adds comparison metrics, verdict logic, and JSON/Markdown writers. |
| `artifacts/campaigns/v1.4-standard/report.md` | Standard evidence | EXISTS + SUBSTANTIVE | Generated standard campaign report. |
| `artifacts/campaigns/v1.4-showcase/report.md` | Showcase evidence | EXISTS + SUBSTANTIVE | Generated showcase campaign report. |
| `artifacts/campaigns/v1.4-comparison/comparison.md` | Before/after report | EXISTS + SUBSTANTIVE | Reports category deltas and reproduction command. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|----|--------|---------|
| v1.3 campaign artifacts | v1.4 campaign artifacts | `diagnostics compare` | WIRED | Baseline/candidate pairs are accepted repeatedly and merged into one report. |
| Comparison JSON | Markdown report | `render_campaign_comparison_markdown` | WIRED | JSON and Markdown are written together from the same comparison payload. |
| README command | Generated comparison | CLI `diagnostics compare` | WIRED | The documented command was executed successfully. |

## Requirements Coverage

| Requirement | Status | Blocking Issue |
|-------------|--------|----------------|
| EVAL-01 | SATISFIED | - |
| EVAL-02 | SATISFIED | - |
| EVAL-03 | SATISFIED | - |
| EVAL-04 | SATISFIED | - |
| EVAL-05 | SATISFIED | - |

**Coverage:** 5/5 requirements satisfied

## Automated Checks

```bash
python -m pytest tests/test_diagnostics.py -q
```

Result: 6 passed.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli campaign standard --output-root artifacts/campaigns --label v1.4-standard --overwrite
```

Result: generated `artifacts/campaigns/v1.4-standard/`.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli campaign showcase --output-root artifacts/campaigns --label v1.4-showcase --overwrite
```

Result: generated `artifacts/campaigns/v1.4-showcase/`.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli diagnostics compare --baseline artifacts/campaigns/v1.3-standard --candidate artifacts/campaigns/v1.4-standard --baseline artifacts/campaigns/v1.3-showcase --candidate artifacts/campaigns/v1.4-showcase --output-dir artifacts/campaigns/v1.4-comparison
```

Result: generated `artifacts/campaigns/v1.4-comparison/`; overall verdict `improved`.

```bash
python -m pytest
```

Result: 58 passed, 2 expected overflow-path warnings.

## Human Verification Required

None - all verifiable items checked programmatically.

## Gaps Summary

**No Phase 28 gaps found.** Beer-Lambert high-perturbation recovery remains unchanged and is recorded as future work, but the phase goal was before/after evaluation and reporting.
