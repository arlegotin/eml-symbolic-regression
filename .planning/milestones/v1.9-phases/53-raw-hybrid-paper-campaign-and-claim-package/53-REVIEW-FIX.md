---
phase: 53-raw-hybrid-paper-campaign-and-claim-package
fixed_at: 2026-04-17T17:06:47Z
review_path: .planning/phases/53-raw-hybrid-paper-campaign-and-claim-package/53-REVIEW.md
iteration: 1
findings_in_scope: 3
fixed: 3
skipped: 0
status: all_fixed
---

# Phase 53: Code Review Fix Report

**Fixed at:** 2026-04-17T17:06:47Z
**Source review:** .planning/phases/53-raw-hybrid-paper-campaign-and-claim-package/53-REVIEW.md
**Iteration:** 1

**Summary:**
- Findings in scope: 3
- Fixed: 3
- Skipped: 0

## Fixed Issues

### CR-01: `--overwrite` can recursively delete arbitrary directories

**Files modified:** `src/eml_symbolic_regression/raw_hybrid_paper.py`, `tests/test_raw_hybrid_paper.py`
**Commit:** f54b50e
**Applied fix:** Replaced recursive `shutil.rmtree()` overwrite behavior with unsafe-target rejection, managed raw-hybrid manifest detection, and cleanup of only known generated top-level package files. Added CLI regression coverage for `--output-dir . --overwrite`, parent/unmanaged non-package directories, and managed package refresh behavior.

### WR-01: File-backed source-lock regression does not verify locked hashes

**Files modified:** `tests/test_raw_hybrid_paper_regression.py`
**Commit:** 3086070
**Applied fix:** Added file-backed SHA-256 recomputation for every source-lock row and asserted each locked source path still exists as a file.

### WR-02: File-backed scientific-law regression omits the historical Michaelis row

**Files modified:** `tests/test_raw_hybrid_paper_regression.py`
**Commit:** bd82e7a
**Applied fix:** Added `Historical Michaelis diagnostic` to the required scientific-law rows and locked its `historical_context` evidence regime plus `unsupported` compile support.

## Skipped Issues

None.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_raw_hybrid_paper.py tests/test_raw_hybrid_paper_regression.py -q` passed with 16 tests.
- `PYTHONPATH=src python -m eml_symbolic_regression.cli raw-hybrid-paper --output-dir artifacts/paper/v1.9/raw-hybrid --require-existing --overwrite` passed.
- The package command changed only `generated_at` values in `artifacts/paper/v1.9/raw-hybrid/manifest.json` and `artifacts/paper/v1.9/raw-hybrid/source-locks.json`; those timestamp-only verification changes were restored to avoid artifact churn.

---

_Fixed: 2026-04-17T17:06:47Z_
_Fixer: Claude (gsd-code-fixer)_
_Iteration: 1_
