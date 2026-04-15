---
status: passed
---

# Phase 19: Campaign Presets and Run Manifests - Verification

## Must-Haves

- [x] `smoke`, `standard`, and `showcase` campaign presets exist.
- [x] Campaigns write a versioned or labeled output directory.
- [x] Campaign output includes raw run artifacts, `suite-result.json`, `aggregate.json`, `aggregate.md`, and `campaign-manifest.json`.
- [x] Standard preset includes shallow blind baselines, Beer-Lambert perturbations, Michaelis-Menten diagnostics, Planck diagnostics, and selected FOR_DEMO cases.
- [x] Existing campaign folders are not silently overwritten.
- [x] Presets document runtime and budget guardrails.

## Test Evidence

```bash
python -m pytest tests/test_campaign.py tests/test_benchmark_contract.py -q
```

Result: 9 passed.
