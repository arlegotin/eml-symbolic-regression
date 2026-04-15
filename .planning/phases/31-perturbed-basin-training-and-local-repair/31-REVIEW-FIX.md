---
phase: 31-perturbed-basin-training-and-local-repair
fixed_at: 2026-04-15T20:14:05Z
review_path: .planning/phases/31-perturbed-basin-training-and-local-repair/31-REVIEW.md
iteration: 2
findings_in_scope: 5
fixed: 5
skipped: 0
status: all_fixed
---

# Phase 31: Code Review Fix Report

**Fixed at:** 2026-04-15T20:14:05Z
**Source review:** `.planning/phases/31-perturbed-basin-training-and-local-repair/31-REVIEW.md`
**Iteration:** 2

**Summary:**
- Findings in scope: 5
- Fixed: 5
- Skipped: 0

## Fixed Issues

### WR-01: Perturbed-Basin Threshold Still Accepts Non-Perturbed Evidence Classes

**Status:** fixed: requires human verification
**Files modified:** `src/eml_symbolic_regression/benchmark.py`, `tests/test_benchmark_reports.py`
**Commit:** b28cbff
**Applied fix:** Restricted `paper-perturbed-true-tree-basin` threshold counting to `perturbed_true_tree_recovered` and `repaired_candidate`, with regression coverage rejecting compiler warm-start, verified-equivalent, same-AST, and scaffolded blind evidence for that claim.

### WR-02: Bound Report Can Support a Noise Level from Incomplete Seed Evidence

**Status:** fixed: requires human verification
**Files modified:** `src/eml_symbolic_regression/diagnostics.py`, `tests/test_basin_bound_report.py`
**Commit:** 5378889
**Applied fix:** Added expected seed/noise inventory handling from aggregate suite metadata, made support-prefix evaluation require complete expected seeds per grid noise, serialized missing/incomplete rows, and added a regression test proving one passing seed out of two does not support the bound.

### WR-03: Locked Evidence References Ephemeral `/tmp` Run Artifacts

**Status:** fixed
**Files modified:** `src/eml_symbolic_regression/diagnostics.py`, `tests/test_basin_bound_report.py`, `artifacts/diagnostics/phase31-basin-bound/basin-bound.json`, `artifacts/diagnostics/phase31-basin-bound/basin-bound.md`, `artifacts/diagnostics/phase31-basin-bound/raw-runs/`
**Commit:** c2d6c89
**Applied fix:** Added durable repo-relative raw run artifacts under the Phase 31 diagnostics directory, regenerated bound JSON/Markdown with repo-relative artifact paths, added artifact checksums to report rows, and added tests rejecting `/tmp` references in committed evidence.

### IN-01: Integration Mark Is Not Registered

**Status:** fixed
**Files modified:** `pyproject.toml`
**Commit:** 4d67749
**Applied fix:** Registered the `integration` pytest marker under `[tool.pytest.ini_options]`.

### WR-01: Bound Support Does Not Require Durable Raw Artifact Checksums

**Status:** fixed: requires human verification
**Files modified:** `src/eml_symbolic_regression/benchmark.py`, `src/eml_symbolic_regression/diagnostics.py`, `tests/test_basin_bound_report.py`, `artifacts/diagnostics/phase31-basin-bound/basin-bound.json`, `artifacts/diagnostics/phase31-basin-bound/basin-bound.md`, `artifacts/diagnostics/phase31-basin-bound/raw-runs/`
**Commit:** 6a78ff5
**Applied fix:** Required bound support rows to have repo-relative artifact paths with recomputed valid SHA-256 checksums, rejected missing/absolute/missing-checksum/mismatched-checksum provenance in regression tests, and normalized committed Phase 31 raw-run snapshots so rerunning the integration evidence test does not churn on `code_version`, `generated_at`, or elapsed timing.

## Skipped Issues

None.

---

_Fixed: 2026-04-15T20:14:05Z_
_Fixer: Claude (gsd-code-fixer)_
_Iteration: 2_
