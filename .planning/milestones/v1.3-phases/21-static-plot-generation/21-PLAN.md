# Phase 21: Static Plot Generation - Plan

status: planned

## Goal

Users can generate crisp, deterministic figures from campaign CSV/aggregate data.

## Tasks

- Add `write_campaign_plots` to create stable SVG chart files.
- Generate recovery charts by formula and start mode.
- Generate loss, Beer-Lambert perturbation, runtime/depth/budget, and failure taxonomy charts.
- Record figure paths in `campaign-manifest.json`.
- Add focused tests for SVG creation, stable filenames, and manifest linkage.

## Verification

- `python -m pytest tests/test_campaign.py -q`

## Out of Scope

- Human-written report prose.
- Interactive dashboards.
