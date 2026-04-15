# Phase 20: Tidy CSV Export and Derived Metrics - Plan

status: planned

## Goal

Users can analyze benchmark campaign results through flat CSV tables and headline metric summaries.

## Tasks

- Add reason extraction to aggregate run summaries.
- Add campaign table writers for `runs.csv`, grouped summaries, headline metrics, and failed/unsupported cases.
- Record generated table paths in `campaign-manifest.json`.
- Extend campaign tests to validate CSV schemas, headline counts, and reason-code exports.

## Verification

- `python -m pytest tests/test_campaign.py tests/test_benchmark_reports.py -q`

## Out of Scope

- SVG/PNG plot rendering.
- Markdown report assembly.
