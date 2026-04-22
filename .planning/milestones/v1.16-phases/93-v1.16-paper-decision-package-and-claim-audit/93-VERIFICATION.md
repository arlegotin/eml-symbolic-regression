---
phase: 93
status: verified
verified: 2026-04-22
---

# Phase 93 Verification

## Goal

Assemble the final v1.16 paper-strength evidence package and decide whether i*pi/GEML deserves a positive paper section under the predefined gate.

## Result

- Final decision package exists at `artifacts/paper/v1.16-geml/final-decision/`.
- Final decision is `inconclusive`.
- `paper_claim_allowed` is `false`.
- Final claim audit status is `passed`.
- Package README exists at `artifacts/paper/v1.16-geml/README.md` and states the inconclusive decision.

## Evidence

- `final-decision/manifest.json` reports decision `inconclusive`, audit `passed`, and `source_locks_ok: true`.
- `final-decision/final-decision.md` includes gate metrics, blockers, package contents, figures, and reproduction commands.
- `final-decision/final-claim-audit.json` passes checks for gate outcome, claim boundaries, ablation assets, figure metadata, reproduction commands, and negative-control visibility.
- `final-decision/source-locks.json` locks campaign, ladder, package, ablation, figure, reproduction, and audit inputs.
- `README.md` guides readers to final decision, gate evaluation, ablations, failure examples, figures, and claim audits.

## Commands

```bash
python -m pytest tests/test_paper_v116.py -q
PYTHONPATH=src python -m eml_symbolic_regression.cli geml-v116-final --campaign-dir artifacts/campaigns/v1.16-geml-pilot --budget-ladder-dir artifacts/campaigns/v1.16-geml-budget-ladder --package-dir artifacts/paper/v1.16-geml --ablation-dir artifacts/paper/v1.16-geml/ablations --output-dir artifacts/paper/v1.16-geml/final-decision --overwrite
```

Both commands completed successfully.

## Verdict

Verified. Phase 93 satisfies the phase goal with a source-locked, claim-audited final package whose README and decision match the Phase 88 gate outcome.
