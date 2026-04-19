# Phase 67: Bounded Baseline and Logistic Strict-Support Probes - Summary

**Completed:** 2026-04-19  
**Status:** Complete

## Outcome

Added a bounded probe package under `artifacts/paper/v1.11/draft/` for the conventional symbolic-regression baseline status and logistic strict-support diagnostic.

## Delivered

- Added `paper-probes` CLI support.
- Added `bounded-probes-manifest.json`.
- Added `tables/conventional-symbolic-baseline-probe.{json,csv,md}`.
- Added `tables/logistic-strict-support-probe.{json,csv,md}`.
- Added `tables/logistic-strict-support-diagnostic.json`.
- Added focused tests for baseline status, logistic strict-gate behavior, artifact generation, and CLI registration.

## Results

- Conventional symbolic-regression baseline status: `unavailable`.
- Local modules checked: PySR, gplearn, PyOperon, karoo-gp.
- Logistic strict gate: 13.
- Logistic strict result: `unsupported`, `depth_exceeded`.
- Logistic relaxed motif depth: 15.
- Remaining depth gap to strict gate: 2.
- Logistic promotion: `no`.

## Claim Boundary

The baseline row is diagnostic-only and excluded from EML recovery denominators. The logistic relaxed-depth improvement remains a diagnostic compiler result, not a recovery promotion.
