# Phase 43 Verification

**Status:** passed
**Date:** 2026-04-16

## Commands

```bash
python -m pytest tests/test_paper_decision.py tests/test_verifier_demos_cli.py::test_cli_paper_decision_writes_package
```

Result: `3 passed`.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli paper-decision --aggregate artifacts/proof/v1.6/campaigns/proof-shallow-pure-blind/aggregate.json --aggregate artifacts/proof/v1.6/campaigns/proof-shallow/aggregate.json --aggregate artifacts/proof/v1.6/campaigns/proof-basin/aggregate.json --aggregate artifacts/proof/v1.6/campaigns/proof-depth-curve/aggregate.json --output-dir artifacts/paper/v1.7
```

Result: generated `artifacts/paper/v1.7/decision-memo.md` and sibling claim/boundary files.

## Success Criteria Check

- Decision memo selects a paper posture from available evidence and names missing centered evidence: passed.
- Safe claim language covers centering, local Jacobian normalization, curvature control, shifted singularity, and subtraction-limit behavior: passed.
- Unsafe claim warnings cover unproved completeness, `ZEML_s` zero-terminal limitations, universal recovery, and pocket-calculator replacement claims: passed.
- Figure/table inventory names exact recovery versus depth and supporting anomaly, verifier, repair/refit, and overhead evidence: passed.
- Completeness boundary labels `CEML_s` constructive completeness as incomplete: passed.
