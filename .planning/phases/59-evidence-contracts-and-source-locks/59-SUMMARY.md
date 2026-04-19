# Phase 59 Summary: Evidence Contracts and Source Locks

## Completed

- Made the raw-hybrid paper package writer version-aware.
- Preserved the default v1.9 package path and regression behavior.
- Added the v1.11 preset `v1.11-paper-evidence-package`.
- Added v1.11 source inventory entries for current v1.10 logistic and Planck focused artifacts.
- Removed stale v1.6 logistic and Planck diagnostics from the v1.11 scientific-law table source set.
- Added `claim-ledger.json` with machine-readable regime/law claim rows and rules forbidding loss-only recovery and mixed-regime blind claims.
- Extended the CLI with `raw-hybrid-paper --preset`.
- Generated the initial v1.11 source-locked package at `artifacts/paper/v1.11/raw-hybrid/`.

## Key Outputs

- `artifacts/paper/v1.11/raw-hybrid/manifest.json`
- `artifacts/paper/v1.11/raw-hybrid/source-locks.json`
- `artifacts/paper/v1.11/raw-hybrid/claim-ledger.json`
- `artifacts/paper/v1.11/raw-hybrid/scientific-law-table.json`

## Result

The v1.11 scientific-law table now records:

- Logistic diagnostic: unsupported, relaxed compile depth 15, `exponential_saturation_template`.
- Planck diagnostic: unsupported, relaxed compile depth 14, `low_degree_power_template`, `scaled_exp_minus_one_template`, and `direct_division_template`.
- Shockley, Arrhenius, and Michaelis-Menten remain supported same-AST/warm-start diagnostics.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_raw_hybrid_paper.py -q`
- `PYTHONPATH=src python -m pytest tests/test_raw_hybrid_paper_regression.py -q`
- `PYTHONPATH=src python -m eml_symbolic_regression.cli raw-hybrid-paper --preset v1.11-paper-evidence-package --output-dir artifacts/paper/v1.11/raw-hybrid --require-existing --overwrite`
