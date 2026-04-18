---
phase: 58-focused-evidence-and-artifact-contracts
status: discussed
mode: autonomous-smart-discuss
created: 2026-04-18
requirements: [LOGI-04, LOGI-05, EVID-01, EVID-02, EVID-03, EVID-04, EVID-05]
---

# Phase 58 Context: Focused Evidence and Artifact Contracts

## Goal

Add focused benchmark suites and deterministic artifacts that report v1.10 logistic and Planck outcomes without pretending either is solved.

## Locked Defaults

- Logistic relaxed depth is now `15` with `exponential_saturation_template`, but strict depth `13` still fails.
- Planck relaxed depth is now `14` with `low_degree_power_template`, `scaled_exp_minus_one_template`, and `direct_division_template`, but strict depth `13` still fails.
- Neither target should get a warm-start case unless strict compile support exists.
- Artifact paths should be focused and deterministic:
  - `artifacts/campaigns/v1.10-logistic-evidence/`
  - `artifacts/campaigns/v1.10-planck-diagnostics/`

## Implementation Decisions

- Add `v1.10-logistic-evidence` with a compile-only `logistic-compile` case.
- Add `v1.10-planck-diagnostics` with a compile-only `planck-compile` case.
- Do not add warm-start cases in v1.10 because strict compile support did not pass for either formula.
- Tests should verify suite contracts, runner artifacts, CLI artifact paths, and macro diagnostics.
- Generate and commit focused artifacts after tests confirm the suite contracts.

## Existing Code Insights

### Reusable Assets

- `benchmark.py` already has focused v1.9 evidence suites.
- `run_benchmark_suite()` writes per-run artifacts and aggregate reports.
- CLI `benchmark` supports `--output-dir` for deterministic artifact roots.

## Deferred Ideas

- Logistic warm-start evidence remains future work until strict support exists.
- Planck warm-start evidence remains future work until strict support exists.

## Threat Model

- **Evidence inflation**: Compile-depth improvement must remain classified as unsupported/compile-only.
- **Artifact ambiguity**: Focused paths must make it clear these are v1.10 diagnostic artifacts, not broad paper package refreshes.
- **Regression**: Existing v1.9 Arrhenius and Michaelis evidence suites must remain unchanged.
