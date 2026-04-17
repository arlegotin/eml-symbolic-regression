---
phase: 53-raw-hybrid-paper-campaign-and-claim-package
reviewed: 2026-04-17T17:01:19Z
depth: standard
files_reviewed: 4
files_reviewed_list:
  - src/eml_symbolic_regression/raw_hybrid_paper.py
  - src/eml_symbolic_regression/cli.py
  - tests/test_raw_hybrid_paper.py
  - tests/test_raw_hybrid_paper_regression.py
findings:
  critical: 1
  warning: 2
  info: 0
  total: 3
status: findings
---

# Phase 53: Code Review Report

**Reviewed:** 2026-04-17T17:01:19Z
**Depth:** standard
**Files Reviewed:** 4
**Status:** findings

## Summary

Reviewed the raw-hybrid paper package writer, CLI wiring, unit tests, and file-backed regression tests for correctness, claim-boundary preservation, path safety, overwrite behavior, source-lock stability, and CLI contract coverage.

The generated evidence buckets and scientific-law rows broadly preserve the intended claim boundaries in the current artifacts, and the focused test suite passes. The main blocker is overwrite path safety: the CLI can recursively delete any non-empty directory supplied as `--output-dir` when `--overwrite` is present. The regression tests also leave important source-lock and historical-row drift undetected.

Verification run:

```bash
PYTHONPATH=src python -m pytest tests/test_raw_hybrid_paper.py tests/test_raw_hybrid_paper_regression.py -q
```

Result: `15 passed in 1.37s`

## Critical Issues

### CR-01: `--overwrite` can recursively delete arbitrary directories

**File:** `/Volumes/git/legotin/eml-symbolic-regression/src/eml_symbolic_regression/raw_hybrid_paper.py:762`

**Issue:** `_prepare_output_dir()` calls `shutil.rmtree(output_dir)` for any existing non-empty path when `overwrite=True`. The CLI exposes `--output-dir` directly, so a typo or malicious value such as `.`, `artifacts`, a parent directory, or another non-package directory can delete unrelated project data before the package is recreated. This is a data-loss risk in the Phase 53 path-safety and overwrite contract.

**Fix:**

Refuse unsafe targets and only overwrite directories that are known raw-hybrid package directories, or remove only the exact generated output files. Also handle existing files explicitly.

```python
EXPECTED_RAW_HYBRID_OUTPUTS = {
    "manifest.json",
    "source-locks.json",
    "regime-summary.json",
    "raw-hybrid-report.md",
    "scientific-law-table.json",
    "scientific-law-table.csv",
    "scientific-law-table.md",
    "claim-boundaries.md",
    "centered-negative-diagnostics.md",
}


def _prepare_output_dir(output_dir: Path, *, overwrite: bool) -> None:
    resolved = output_dir.resolve()
    cwd = Path.cwd().resolve()
    forbidden = {cwd, Path.home().resolve(), Path(resolved.anchor).resolve()}
    if resolved in forbidden:
        raise RawHybridPaperError(f"refusing to use unsafe output directory: {output_dir}")
    if output_dir.exists() and not output_dir.is_dir():
        raise RawHybridPaperError(f"output path is not a directory: {output_dir}")
    if output_dir.exists() and any(output_dir.iterdir()):
        if not overwrite:
            raise RawHybridPaperError(f"output directory is not empty: {output_dir}")
        manifest = output_dir / "manifest.json"
        if not _is_raw_hybrid_manifest(manifest):
            raise RawHybridPaperError(f"refusing to overwrite unmanaged directory: {output_dir}")
        for name in EXPECTED_RAW_HYBRID_OUTPUTS:
            path = output_dir / name
            if path.exists():
                path.unlink()
    output_dir.mkdir(parents=True, exist_ok=True)
```

Add tests that `--output-dir . --overwrite`, a parent directory, and an existing non-package directory are refused, while the known package directory can still be refreshed.

## Warnings

### WR-01: File-backed source-lock regression does not verify locked hashes

**File:** `/Volumes/git/legotin/eml-symbolic-regression/tests/test_raw_hybrid_paper_regression.py:110`

**Issue:** `test_raw_hybrid_manifest_and_source_locks_are_stable()` checks that each committed lock value is a 64-character hex string, but it does not recompute the SHA-256 of `row["path"]`. A stale or manually edited `source-locks.json` with any valid-looking hash would pass, even when the committed package no longer matches the evidence files it claims to lock.

**Fix:**

Recompute every required source hash in the file-backed regression test, and consider exact source-id equality if the inventory is meant to be fixed.

```python
def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


for row in locks["sources"]:
    path = Path(row["path"])
    assert path.is_file(), row["source_id"]
    assert row["sha256"] == _sha256(path), row["source_id"]
```

### WR-02: File-backed scientific-law regression omits the historical Michaelis row

**File:** `/Volumes/git/legotin/eml-symbolic-regression/tests/test_raw_hybrid_paper_regression.py:66`

**Issue:** The implementation and unit test include `"Historical Michaelis diagnostic"`, and Phase 53 treats it as part of the paper package context. The file-backed regression lock only requires Beer-Lambert, Shockley, Arrhenius, Michaelis-Menten, Planck, and Logistic. If the committed `scientific-law-table.json` loses the historical Michaelis diagnostic row, the regression test still passes, weakening the claim-boundary lock around old unsupported Michaelis evidence.

**Fix:** Add `"Historical Michaelis diagnostic"` to `REQUIRED_LAWS` and assert its boundary fields explicitly.

```python
assert by_law["Historical Michaelis diagnostic"]["evidence_regime"] == "historical_context"
assert by_law["Historical Michaelis diagnostic"]["compile_support"] == "unsupported"
```

---

_Reviewed: 2026-04-17T17:01:19Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
