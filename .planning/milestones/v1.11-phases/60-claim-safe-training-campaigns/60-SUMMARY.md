# Phase 60 Summary: Claim-Safe Training Campaigns

## Completed

- Added built-in benchmark suite `v1.11-paper-training`.
- Added built-in benchmark suite `v1.11-logistic-planck-probes`.
- Added campaign presets `paper-training` and `paper-probes`.
- Ran both campaigns with stable labels under `artifacts/campaigns/`.
- Added regression tests for the new suites, campaign presets, real pure-blind training execution, and logistic/Planck unsupported probe rows.

## Campaign Results

### `artifacts/campaigns/v1.11-paper-training/`

Total runs: 8  
Verifier recovered: 8/8  
Unsupported: 0  
Failed: 0

Evidence classes:

- `blind_training_recovered`: 2
- `scaffolded_blind_training_recovered`: 2
- `same_ast`: 3
- `perturbed_true_tree_recovered`: 1

Regime groups:

- Blind: 4/4 recovered, split into 2 pure-blind and 2 scaffolded recovered rows.
- Warm-start: 3/3 recovered as same-AST rows for Shockley, Arrhenius, and Michaelis-Menten.
- Perturbed tree: 1/1 recovered for depth-2 nested exp basin return.

### `artifacts/campaigns/v1.11-logistic-planck-probes/`

Total runs: 4  
Verifier recovered: 0/4  
Unsupported: 2  
Failed: 2

Evidence classes:

- `unsupported`: 2
- `snapped_but_failed`: 1
- `failed`: 1

Regime groups:

- Compile: logistic and Planck remain unsupported with `depth_exceeded`.
- Blind probes: logistic snapped but failed verification; Planck failed verification.

## Interpretation

The positive v1.11 training evidence is real and current-code, but it is claim-class specific. Pure-blind exp recovery, scaffolded exp recovery, same-AST scientific-law warm starts, and perturbed-basin return are separate evidence rows.

Logistic and Planck did receive real probe artifacts. The results are negative: no verifier recovery and no promotion. Their compile rows remain unsupported diagnostics under the unchanged strict gate.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_campaign.py -q`
- `PYTHONPATH=src python -m eml_symbolic_regression.cli campaign paper-training --label v1.11-paper-training --overwrite`
- `PYTHONPATH=src python -m eml_symbolic_regression.cli campaign paper-probes --label v1.11-logistic-planck-probes --overwrite`
- `PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_campaign.py tests/test_benchmark_runner.py -q`
