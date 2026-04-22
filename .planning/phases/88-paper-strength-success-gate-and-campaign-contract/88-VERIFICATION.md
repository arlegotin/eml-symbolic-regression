---
phase: 88
status: passed
verified: 2026-04-22
---

# Phase 88 Verification

## Goal

Define the exact evidence gate for a paper-positive i*pi/GEML result and lock matched campaign denominators before optimizer changes.

## Must-Haves

- Machine-readable gate config defines `paper_positive`, `promising_preliminary`, `negative`, and `inconclusive`: verified in `default_v116_gate_config`.
- Claim audit rejects loss-only recovery, global superiority, broad blind recovery, full universality, missing negative controls, and paper-positive language without a gate pass: verified in `build_v116_claim_audit` tests.
- Campaign contract locks target families, seeds, budgets, split/verifier fields, resource metadata, and denominator rules: verified in `default_v116_campaign_contract`.
- Package fails closed when exact-recovery signal, denominator completeness, negative-control discipline, or source locks are missing: verified by `evaluate_v116_gate` tests and package fixture.

## Automated Checks

```bash
python -m pytest tests/test_paper_v116.py tests/test_geml_package.py -q
```

Result: passed, 9 tests.
