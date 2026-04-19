# Phase 60 Plan: Claim-Safe Training Campaigns

## Goal

Run real current-code training in bounded regimes that can be reported without overclaiming.

## Scope

- Add v1.11 benchmark suites for:
  - compact paper training evidence,
  - logistic and Planck low-budget probes.
- Add campaign presets that write focused roots under `artifacts/campaigns/v1.11-*`.
- Run the suites and commit the generated artifacts.
- Preserve unsupported Planck/logistic status unless full strict verifier support appears.

## Tasks

1. Add `v1.11-paper-training` benchmark suite with pure blind, scaffolded, same-AST warm-start, and perturbed-basin cases.
2. Add `v1.11-logistic-planck-probes` benchmark suite with current compile diagnostics and low-budget real blind probes.
3. Add `paper-training` and `paper-probes` campaign presets.
4. Run the campaigns with stable labels.
5. Inspect aggregate results and record them in the phase summary.
6. Run targeted benchmark/campaign tests.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py tests/test_campaign.py -q`
- `PYTHONPATH=src python -m eml_symbolic_regression.cli campaign paper-training --label v1.11-paper-training --overwrite`
- `PYTHONPATH=src python -m eml_symbolic_regression.cli campaign paper-probes --label v1.11-logistic-planck-probes --overwrite`

## Constraints

- Real training results are verifier-owned, not loss-owned.
- Scaffolded, warm-start, same-AST, perturbed-basin, compile-only, and unsupported rows remain separate.
- Logistic and Planck probes are negative/stretch diagnostics unless the unchanged strict contract passes.
