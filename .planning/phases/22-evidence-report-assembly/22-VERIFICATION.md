---
status: passed
---

# Phase 22: Evidence Report Assembly - Verification

## Must-Haves

- [x] Campaign folder contains `report.md`.
- [x] Report includes headline metrics, tables, figures, commands, and raw artifact links.
- [x] Narrative explains what EML demonstrates well.
- [x] Limitations separate blind recovery, same-AST return, verified-equivalent recovery, unsupported gates, and failed fits.
- [x] Report includes next experiments.
- [x] A single CLI command is documented for reproduction.

## Test Evidence

```bash
python -m pytest tests/test_campaign.py -q
```

Result: 6 passed.
