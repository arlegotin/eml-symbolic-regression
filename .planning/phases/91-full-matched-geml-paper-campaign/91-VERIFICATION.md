---
phase: 91
status: verified
verified: 2026-04-22
---

# Phase 91 Verification

## Goal

Produce the full matched GEML paper-campaign package only if the Phase 90 budget ladder permits it, otherwise produce a fail-closed locked package that prevents positive paper claims.

## Result

- Full campaign route: blocked by `artifacts/campaigns/v1.16-geml-budget-ladder/manifest.json`.
- Package produced at `artifacts/paper/v1.16-geml/`.
- Package decision: `inconclusive`.
- Claim audit status: `passed`.
- Budget ladder decision embedded in the package manifest: `stop_full_campaign_fail_closed`.

## Evidence

- `artifacts/paper/v1.16-geml/manifest.json` source-locks the pilot campaign, budget ladder, gate configuration, claim audit, and reproduction notes.
- `artifacts/paper/v1.16-geml/gate-evaluation.json` reports blockers:
  - `no_natural_ipi_exact_recovery_signal`
  - `incomplete_matched_denominator`
  - `loss_only_signal_without_exact_recovery`
- `artifacts/paper/v1.16-geml/decision.md` reports 12 pilot paired rows, 0 raw exact recoveries, 0 i*pi exact recoveries, and 12 loss-only outcomes.

## Commands

```bash
python -m pytest tests/test_paper_v116.py -q
PYTHONPATH=src python -m eml_symbolic_regression.cli geml-paper-v116 --campaign-dir artifacts/campaigns/v1.16-geml-pilot --budget-ladder-dir artifacts/campaigns/v1.16-geml-budget-ladder --output-dir artifacts/paper/v1.16-geml --min-unique-seeds 3 --overwrite
```

Both commands completed successfully.

## Verdict

Verified. Phase 91 satisfies the phase goal by preserving the fail-closed budget-ladder decision and producing a locked, auditable, non-positive v1.16 paper package.
