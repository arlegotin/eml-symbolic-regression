# EML Symbolic Regression

This package is a research-grade implementation of a symbolic-regression idea from the paper "All elementary functions from a single binary operator": search inside one complete depth-bounded family of EML trees, optimize the soft choices with PyTorch, snap the result into an exact tree, clean it up symbolically, and let an independent verifier decide whether a formula was actually recovered.

The goal is not to claim that arbitrary scientific laws are solved from scratch. The goal is narrower and more useful: recover compact, human-readable elementary formulas from controlled datasets while keeping blind recovery, warm starts, repairs, compiler evidence, and unsupported diagnostics separate.

## What Is EML?

The single operator is:

```text
eml(x, y) = exp(x) - log(y)
```

Together with the constant `1`, the paper shows that this operator can generate the usual scientific-calculator elementary-function basis. Instead of searching over a mixed grammar of `+`, `*`, `/`, `exp`, `log`, trigonometric functions, and other operators, EML expressions use one uniform binary tree grammar:

```text
S -> 1 | eml(S, S)
```

For regression tasks, variables such as `x` are added as terminals. A complete depth-bounded EML tree is then a single container for every EML expression up to that depth. That regularity is the reason this repository uses EML: the operator vocabulary is fixed, and the main knobs become depth, initialization, optimization, snapping, cleanup, and verification.

## What This Package Does

The implemented pipeline is:

```text
dataset
  -> soft complete EML tree
  -> PyTorch complex128 optimization
  -> hardening and snapping
  -> exact EML AST
  -> SymPy cleanup and report helpers
  -> verifier-owned recovery report
```

The package includes:

- canonical and training-mode EML semantics;
- immutable exact EML AST nodes with deterministic JSON serialization;
- paper identity checks for `exp(x)` and `log(x)`;
- complete depth-bounded soft EML trees with categorical gates;
- Adam-based optimization with restarts, annealing, hardening, snapping, and optimizer manifests;
- compiler support for a guarded SymPy subset, including literal-constant provenance and macro traces;
- compiler warm starts that embed an exact AST into a compatible soft tree, perturb, train, snap, and verify;
- verifier checks across train, held-out, extrapolation, and high-precision `mpmath` points;
- benchmark suites, campaign reports, aggregate evidence files, CSV tables, and SVG figures;
- demo targets from `sources/FOR_DEMO.md`.

Training mode may use stability guards such as clamps. Verification mode is the claim boundary: snapped candidates are evaluated again under the verifier contract rather than promoted from training loss.

## What Counts As Recovered?

A candidate is `recovered` only when the verifier says so. Training loss alone is not recovery.

The verifier-owned contract requires an exact candidate to pass:

- the training split;
- a held-out split;
- an extrapolation split;
- high-precision `mpmath` checks.

Compiler output alone is not trained recovery. A compiled formula can be useful seed or provenance evidence, but public recovery promotion requires the warm-start or training path to produce a snapped exact candidate that passes the verifier.

Repaired candidates are repair evidence only. A `repaired_candidate` status means verifier-gated cleanup found a better candidate after the originally selected exact tree failed; it is not blind discovery, compile-only evidence, same-AST warm-start evidence, or perturbed true-tree recovery.

## Install And Quick Start

Python support is declared as `>=3.11,<3.13`.

Install the package in editable mode with the development extra:

```bash
python -m pip install -e ".[dev]"
```

After installation, use the console script declared in `pyproject.toml`:

```bash
eml-sr verify-paper
eml-sr list-demos
eml-sr demo beer_lambert --compile-eml --output artifacts/beer-compile-report.json
eml-sr demo beer_lambert --warm-start-eml --output artifacts/beer-warm-report.json
eml-sr list-benchmarks
eml-sr benchmark smoke --output-dir artifacts/benchmarks
eml-sr campaign smoke --output-root artifacts/campaigns
python -m pytest
```

When running directly from a source checkout without installation, use the module entry point:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli verify-paper
PYTHONPATH=src python -m eml_symbolic_regression.cli list-demos
PYTHONPATH=src python -m eml_symbolic_regression.cli demo beer_lambert --compile-eml --output artifacts/beer-compile-report.json
PYTHONPATH=src python -m eml_symbolic_regression.cli demo beer_lambert --warm-start-eml --output artifacts/beer-warm-report.json
PYTHONPATH=src python -m eml_symbolic_regression.cli list-benchmarks
PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark smoke --output-dir artifacts/benchmarks
PYTHONPATH=src python -m eml_symbolic_regression.cli campaign smoke --output-root artifacts/campaigns
python -m pytest
```

Use `eml-sr --help`, `eml-sr demo --help`, `eml-sr benchmark --help`, and `eml-sr campaign --help` for the full command surface.

## Demos And Evidence

The demo ladder is drawn from `sources/FOR_DEMO.md`: normalized, dimensionless, visually distinctive laws are preferred because the paper reports rapid degradation for blind random-initialized recovery at higher depths.

Common demo IDs include:

- `exp` and `log`: paper-grounded EML identity smoke tests;
- `beer_lambert` and `radioactive_decay`: exponential-decay baselines;
- `shockley`: electronics demo close to EML's exponential-minus-constant bias;
- `arrhenius`: normalized reciprocal-temperature law, `exp(-0.8/x)`;
- `michaelis_menten`: normalized saturation law, `2*x/(x+0.5)`;
- `logistic` and `planck`: useful stretch diagnostics under the current gates;
- `damped_oscillator`: visually strong but harder because it mixes decay and oscillation.

Evidence regimes are deliberately separate:

| Regime | Meaning |
| --- | --- |
| `blind_recovery` | Random/scaffold-free training produced a snapped exact EML candidate that passed the verifier. |
| `trained_exact_recovery` | A post-training snapped exact EML AST passed the verifier. |
| `same_ast_warm_start_return` / `same_ast` | A compiler warm start returned to the same exact AST and verified. This is basin evidence, not blind discovery. |
| `verified_equivalent_warm_start_recovery` | A warm-started run snapped to a different exact AST that still verified. |
| `compiled_seed` / `compile_only` | The source expression compiled to exact EML and validated as a seed. This is not trained recovery by itself. |
| `repaired_candidate` | Verifier-gated cleanup repaired a failed exact candidate. This is repair evidence only. |
| `refit` | A frozen structure with literal constants was numerically refit and rechecked. It is a separate evidence regime. |
| `perturbed_basin` | A true or compiled tree was perturbed and recovered inside a declared basin. It is not blind discovery. |
| `verified_showcase` | A non-EML catalog formula passed verifier checks for demo/report coverage. It is not EML discovery. |
| `unsupported` | A compile, warm-start, depth, node, operator, or verifier gate failed closed. Unsupported cases stay visible. |

Arrhenius and Michaelis-Menten currently have exact compiler warm-start / same-AST evidence. They should not be described as blind discoveries. Beer-Lambert and Shockley are supported warm-start paths. Planck and logistic remain unsupported or stretch diagnostics unless the strict compiler, warm-start, and verifier contracts pass. Repaired candidates remain repair-only evidence.

Benchmark suites and campaigns write machine-readable run artifacts plus aggregate reports. The smoke path is the fastest end-to-end check:

```bash
eml-sr benchmark smoke --output-dir artifacts/benchmarks
eml-sr campaign smoke --output-root artifacts/campaigns
```

## Limits And Claim Boundaries

The paper reports that blind recovery from random initialization works well for shallow targets, degrades sharply by moderate depth, and was not observed at depth 6 in the reported attempts. This repository keeps that limitation visible.

Do not read the artifacts as a broad superiority claim over conventional symbolic regression or as blind discovery of arbitrary deep formulas. The strongest current story is a verifier-gated hybrid EML system with shallow recovery, exact compiler paths, warm-start basin evidence, repair diagnostics, and honest unsupported cases.

In particular:

- training loss alone is not recovery;
- compiler output alone is not trained recovery;
- warm-start, same-AST, scaffolded, repaired, refit, compile-only, verified_showcase, perturbed-basin, and unsupported results are separate evidence regimes;
- Arrhenius and Michaelis-Menten are exact compiler warm-start / same-AST evidence, not blind discovery;
- Planck and logistic remain unsupported/stretch diagnostics unless strict support and verifier contracts pass;
- repaired candidates are repair evidence only.

## Repository Map

- `sources/paper.pdf`: source paper.
- `sources/NORTH_STAR.md`: implementation blueprint and paper-grounded constraints.
- `sources/FOR_DEMO.md`: demo ranking and feasibility guidance.
- `docs/IMPLEMENTATION.md`: recovery, compiler, warm-start, benchmark, campaign, and claim-boundary contracts.
- `pyproject.toml`: package metadata, Python requirement, dependencies, dev extra, and `eml-sr` console script.
- `src/eml_symbolic_regression/`: package source.
- `tests/`: pytest coverage for semantics, tree construction, snapping, verification, compiler paths, benchmarks, and paper artifacts.
- `artifacts/`: generated and committed evidence packages, campaigns, reports, tables, and figures.

For a new reader, start with this README, then read `docs/IMPLEMENTATION.md` for the current contract and `sources/NORTH_STAR.md` for the broader rationale.
