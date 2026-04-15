---
status: passed
---

# Phase 20: Tidy CSV Export and Derived Metrics - Verification

## Must-Haves

- [x] Run-level CSV includes formula, mode, seed, budget, perturbation, losses, verifier status, recovery class, runtime, changed slots, and artifact path.
- [x] Grouped CSV summaries cover formula, start mode, perturbation, depth, and failure class.
- [x] Headline metrics are exported as JSON and CSV.
- [x] Failed and unsupported cases include reason codes and artifact links.

## Test Evidence

```bash
python -m pytest tests/test_campaign.py tests/test_benchmark_reports.py -q
```

Result: 8 passed.
