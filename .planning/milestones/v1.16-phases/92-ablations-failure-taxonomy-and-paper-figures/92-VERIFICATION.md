---
phase: 92
status: verified
verified: 2026-04-22
---

# Phase 92 Verification

## Goal

Explain why the v1.16 GEML/i*pi result is not strong enough for a positive paper claim using ablation tables, failure taxonomy, and reviewer-facing figures generated from locked campaign evidence.

## Result

- `artifacts/paper/v1.16-geml/ablations/manifest.json` exists.
- Manifest decision is `inconclusive` and `paper_claim_allowed` is `false`.
- Ablation table covers initialization, branch guards, constants, depth, budget, and candidate pooling.
- Failure examples include canonical failure classes and representative observed rows.
- Figure metadata lists five deterministic SVG figures.
- `source_locks_ok` is `true`.

## Evidence

- `ablation-table.md` reports 0 exact recoveries, 12 loss-only pilot outcomes, and explicit not-run rows blocked by the pilot gate.
- `failure-examples.md` maps observed `loss_only_signal` rows to representative examples and keeps other failure classes visible as not observed.
- `figure-metadata.json` records claim boundaries for family recovery, loss before/after snap, branch anomalies, runtime, and representative curves.
- `source-locks.json` locks the pilot paired comparison, run table, budget ladder manifest, failure taxonomy, paper package manifest, and gate evaluation.

## Commands

```bash
python -m pytest tests/test_paper_v116.py -q
PYTHONPATH=src python -m eml_symbolic_regression.cli geml-v116-ablations --campaign-dir artifacts/campaigns/v1.16-geml-pilot --budget-ladder-dir artifacts/campaigns/v1.16-geml-budget-ladder --package-dir artifacts/paper/v1.16-geml --output-dir artifacts/paper/v1.16-geml/ablations --overwrite
```

Both commands completed successfully.

## Verdict

Verified. Phase 92 satisfies the phase goal with source-locked ablation analysis, failure examples, and deterministic paper-facing figures while preserving the non-positive v1.16 decision.
