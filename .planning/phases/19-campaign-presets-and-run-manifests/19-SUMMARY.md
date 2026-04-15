# Phase 19: Campaign Presets and Run Manifests - Summary

**Completed:** 2026-04-15
**Status:** Complete

## Delivered

- Added `smoke`, `standard`, and `showcase` campaign presets.
- Added v1.3 standard/showcase benchmark suites with explicit budget tiers and FOR_DEMO coverage.
- Added `eml_symbolic_regression.campaign` for campaign execution, output-folder guardrails, and manifest generation.
- Added `list-campaigns` and `campaign` CLI commands.
- Added tests for preset expansion, output creation, manifest content, and overwrite protection.

## Key Files

- `src/eml_symbolic_regression/campaign.py`
- `src/eml_symbolic_regression/benchmark.py`
- `src/eml_symbolic_regression/cli.py`
- `tests/test_campaign.py`

## Verification

```bash
python -m pytest tests/test_campaign.py tests/test_benchmark_contract.py -q
```

Result: 9 passed.
