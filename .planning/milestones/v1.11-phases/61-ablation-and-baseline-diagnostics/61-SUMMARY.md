# Phase 61 Summary: Ablation and Baseline Diagnostics

## Completed

- Added `paper_diagnostics.py` for source-derived paper diagnostics.
- Added CLI command `diagnostics paper-ablations`.
- Generated `artifacts/diagnostics/v1.11-paper-ablations/`.
- Added tests for motif deltas, regime separation, prediction-only baselines, and CLI output.

## Outputs

- `manifest.json`
- `motif-depth-deltas.json/.csv/.md`
- `regime-comparison.json/.csv/.md`
- `repair-refit-diagnostics.json/.csv/.md`
- `baseline-diagnostics.json/.csv/.md`

## Results

Motif depth rows: 6

- Logistic: baseline depth 27 -> motif depth 15, `exponential_saturation_template`, unsupported.
- Planck: baseline depth 24 -> motif depth 14, `low_degree_power_template`, `scaled_exp_minus_one_template`, `direct_division_template`, unsupported.
- Shockley, Arrhenius, and Michaelis-Menten remain supported motif-backed rows.
- Historical Michaelis remains unsupported context.

Regime comparison rows: 12

- v1.11 paper training remains separated by start mode and evidence class.
- v1.11 logistic/Planck probes remain split between unsupported compile rows and failed blind probes.

Repair/refit rows: 12

- v1.9 candidate-pool expansion still records no repair improvements and no final-status regressions.
- v1.11 probe rows expose post-snap refit/repair status without counting it as discovery.

Baseline rows: 20

- Prediction-only mean, linear, cubic, and log-linear-positive diagnostics for exp, logistic, Planck, Michaelis-Menten, and Arrhenius.
- Baseline rows are explicitly labeled as prediction-only diagnostics and excluded from EML recovery denominators.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_paper_diagnostics.py tests/test_verifier_demos_cli.py -q`
- `PYTHONPATH=src python -m eml_symbolic_regression.cli diagnostics paper-ablations --output-dir artifacts/diagnostics/v1.11-paper-ablations`
