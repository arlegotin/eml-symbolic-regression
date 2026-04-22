---
phase: 97
status: passed
verified: 2026-04-22
---

# Phase 97 Verification

## Goal

Run the smallest useful matched experiment to see whether the snap-first workflow produces exact recovery signal.

## Must-Have Checks

- Selected v1.16-style natural-bias rows are evaluated through the Phase 96 ranking output: verified by sandbox fixture rows.
- Raw EML and i*pi EML use matched visibility through operator-family summary rows.
- The sandbox records whether at least one verifier-gated exact recovery appears: verified by `exact_signal_found` assertions.
- The gate blocks broader campaigns if exact signal remains absent: verified by `block_broader_campaigns` test.

## Automated Checks

```bash
python -m pytest tests/test_paper_v117.py -q
```

Result: `10 passed`.

## Human Verification

None required.
