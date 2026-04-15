---
phase: 17
subsystem: evidence-reporting
status: complete
wave: 1
---

# Phase 17 Plan: Evidence Aggregation and Report Contracts

<objective>
Aggregate benchmark run artifacts into JSON and Markdown evidence reports with recovery rates, failure classes, and provenance.
</objective>

## Tasks

- Add normalized metrics extraction for per-run artifacts.
- Add aggregate evidence JSON with grouped recovery statistics.
- Add Markdown evidence report generation.
- Add code/environment provenance to run and aggregate reports.
- Update CLI benchmark command to write aggregate reports.
- Add tests for aggregation math and report output.

## Verification

- `python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py tests/test_benchmark_reports.py`
