---
status: passed
---

# Phase 21: Static Plot Generation - Verification

## Must-Haves

- [x] Recovery-rate charts compare formulas and start modes.
- [x] Loss chart compares best soft loss and post-snap loss on a log-derived scale.
- [x] Beer-Lambert perturbation chart reports recovery and changed-slot behavior by perturbation noise.
- [x] Runtime/depth/budget chart makes cost visible.
- [x] Failure taxonomy chart includes unsupported and failed cases.
- [x] Figure filenames are stable and Markdown-linkable.

## Test Evidence

```bash
python -m pytest tests/test_campaign.py -q
```

Result: 5 passed.
