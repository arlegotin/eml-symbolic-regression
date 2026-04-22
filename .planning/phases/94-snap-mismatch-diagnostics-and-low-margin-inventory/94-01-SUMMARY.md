---
phase: 94
plan: 01
status: complete
completed: 2026-04-22
requirements-completed: [SNAP-01, SNAP-02, SNAP-03]
key-files:
  created:
    - src/eml_symbolic_regression/paper_v117.py
    - tests/test_paper_v117.py
  modified:
    - src/eml_symbolic_regression/benchmark.py
    - src/eml_symbolic_regression/campaign.py
    - src/eml_symbolic_regression/cli.py
    - tests/test_campaign.py
---

# Phase 94 Plan 01: Snap Mismatch Diagnostics and Inventory Summary

Implemented v1.17 snap diagnostics for campaign rows and package artifacts.

## What Changed

- Benchmark metrics now preserve selected/fallback candidate IDs, selection mode, candidate pool size, snap active node count, low-margin slot counts, lowest-margin slot payloads, low-confidence alternatives, and soft-versus-hard snap deltas.
- GEML paired comparison rows now expose raw/ipi-prefixed snap diagnostics without changing comparison outcome or recovery accounting.
- Added `paper_v117.py` with `write_v117_snap_diagnostics()` for `snap-diagnostics.{json,csv,md}`, `snap-neighborhood-seeds.json`, source locks, and manifest output.
- Added `geml-v117-snap-diagnostics` CLI registration.

## Verification

```bash
python -m pytest tests/test_campaign.py::test_campaign_tables_emit_geml_paired_comparison tests/test_paper_v117.py -q
```

Result: `4 passed`.

## Deviations from Plan

None - plan executed exactly as written.

## Self-Check: PASSED
