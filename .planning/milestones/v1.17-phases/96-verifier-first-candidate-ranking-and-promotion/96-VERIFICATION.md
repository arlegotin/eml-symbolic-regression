---
phase: 96
status: passed
verified: 2026-04-22
---

# Phase 96 Verification

## Goal

Make exact verifier status the first-class promotion rule for all candidate pools.

## Must-Have Checks

- Every candidate is routed through a verifier-status-first ranking field before promotion: verified by `write_v117_candidate_ranking()`.
- Ranking explains why the winner was selected and why lower-loss candidates failed: verified by rejection reason assertions in `tests/test_paper_v117.py`.
- Tables separate exact recovery, verified equivalence, repair-only, loss-only, compile-only, same-AST, fallback, and original-snap outcomes: verified by evidence-class counts.
- Existing recovery-accounting behavior remains compatible because new v1.17 ranking artifacts are additive and do not alter campaign comparison outcomes.

## Automated Checks

```bash
python -m pytest tests/test_paper_v117.py -q
```

Result: `7 passed`.

## Human Verification

None required.
