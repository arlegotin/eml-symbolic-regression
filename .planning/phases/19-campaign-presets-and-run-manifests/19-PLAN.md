# Phase 19: Campaign Presets and Run Manifests - Plan

status: planned

## Goal

Users can run named benchmark campaign presets into reproducible output folders without manually composing benchmark filters and output paths.

## Tasks

- Add built-in v1.3 benchmark suites for `standard` and `showcase` campaign presets.
- Add a `campaign.py` module with preset metadata, output-folder guardrails, campaign execution, and manifest generation.
- Add CLI commands to list campaign presets and run a campaign with optional filters, stable label, and overwrite opt-in.
- Add focused tests for preset expansion, output creation, manifest content, and overwrite protection.

## Verification

- `python -m pytest tests/test_campaign.py tests/test_benchmark_contract.py -q`
- Confirm a filtered smoke campaign writes `campaign-manifest.json`, `suite-result.json`, `aggregate.json`, `aggregate.md`, and raw run artifacts.

## Out of Scope

- CSV exports.
- Static figures.
- Final `report.md` assembly.
