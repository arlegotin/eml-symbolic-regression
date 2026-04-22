---
phase: 95
plan: 01
status: complete
completed: 2026-04-22
requirements-completed: [NBR-01, NBR-03, NBR-04]
key-files:
  modified:
    - src/eml_symbolic_regression/paper_v117.py
    - src/eml_symbolic_regression/cli.py
    - tests/test_paper_v117.py
---

# Phase 95 Plan 01: Bounded Exact Neighborhood Manifests Summary

Implemented deterministic v1.17 snap-neighborhood candidate generation.

## What Changed

- Added `write_v117_neighborhood_candidates()` with manifest, JSON, CSV, Markdown, and source-lock outputs.
- Preserved original snapped and fallback candidates as explicit provenance rows.
- Generated bounded one-slot and two-slot alternatives from serialized snap decisions and low-confidence slot alternatives.
- Added `geml-v117-neighborhoods` CLI registration and tests for deterministic ordering and target-leakage guard fields.

## Verification

```bash
python -m pytest tests/test_paper_v117.py -q
```

Result: `5 passed`.

## Deviations from Plan

None - plan executed exactly as written.

## Self-Check: PASSED
