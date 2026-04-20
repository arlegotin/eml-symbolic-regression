# EML Symbolic Regression

One binary operator can express a surprising amount of mathematics:

```text
eml(x, y) = exp(x) - log(y)
```

This project turns that idea into a symbolic-regression engine. Instead of asking a search algorithm to juggle a menu of operators like `+`, `*`, `/`, `exp`, `log`, and `sin`, it searches inside one regular family of EML trees. The system trains a soft tree, snaps it into an exact symbolic expression, cleans up the result, and then makes the verifier decide whether the formula was actually recovered.

The short version: it is a PyTorch-first, verifier-gated equation discovery package for compact elementary formulas.

## Current Release Evidence

The v1.13 release package is source-locked under `artifacts/paper/v1.13/`. The release gate passed, the claim audit passed, and the final paper-track campaign ran 24 configured rows with zero execution failures.

The headline numbers are deliberately split by evidence regime:

| Track | Rows | Verifier recovered | Unsupported | Failed | What it means |
| --- | ---: | ---: | ---: | ---: | --- |
| Basis-only compile track | 12 | 1 | 11 | 0 | Strict `{1, eml, variables}` style support is still narrow. |
| Literal-constant warm-start track | 12 | 8 | 4 | 0 | Exact basins are strong when useful constants and seeds are explicit. |
| Combined | 24 | 9 | 15 | 0 | 37.5% verifier-owned recovery, with unsupported cases kept in the denominator. |

Those 9 recoveries are not all the same kind of claim: 1 is compile-only verified evidence, and 8 are same-AST warm-start returns. The release does not claim broad blind symbolic-regression superiority.

| Recovery by formula | Recovery by start mode |
| --- | --- |
| ![Verifier recovery rate by formula](artifacts/campaigns/v1.13-paper-tracks-final/figures/recovery-by-formula.svg) | ![Verifier recovery rate by start mode](artifacts/campaigns/v1.13-paper-tracks-final/figures/recovery-by-start-mode.svg) |

| Unsupported taxonomy | Training loss before and after snap |
| --- | --- |
| ![Failure and unsupported taxonomy](artifacts/campaigns/v1.13-paper-tracks-final/figures/failure-taxonomy.svg) | ![Training loss before and after snap](artifacts/campaigns/v1.13-paper-tracks-final/figures/loss-before-after-snap.svg) |

Useful release artifacts:

- `artifacts/paper/v1.13/manifest.json`: root publication manifest.
- `artifacts/paper/v1.13/claim-audit.md`: claim audit, status `passed`.
- `artifacts/paper/v1.13/release-gate.md`: release gate, status `passed`.
- `artifacts/paper/v1.13/reproduction.md`: reproduction command and environment notes.
- `artifacts/campaigns/v1.13-paper-tracks-final/tables/`: campaign tables.
- `artifacts/baselines/v1.13/baseline-report.md`: matched baseline harness report.
- `artifacts/datasets/v1.13/`: expanded dataset manifests.

## The Trick

EML expressions are built from one repeated binary node:

```text
S -> 1 | eml(S, S)
```

For regression, variables such as `x` are added as terminals. A complete depth-bounded EML tree can then represent every EML expression up to that depth. That gives the optimizer one uniform search space instead of a mixed forest of operator-specific ASTs.

That does not make symbolic regression easy. It makes the search space regular enough to attack with a hybrid pipeline.

## How It Works

```text
data
  -> complete soft EML tree
  -> PyTorch complex128 optimization
  -> hardening and snapping
  -> exact EML AST
  -> symbolic cleanup
  -> verifier report
```

The engine has a few important moving parts:

- `complex128` training, because EML uses exponentials and principal-branch logarithms.
- Categorical gates over complete depth-bounded trees.
- Adam optimization with restarts, annealing, hardening, and snap manifests.
- Exact immutable EML expression trees with deterministic JSON serialization.
- A guarded compiler for a supported SymPy subset, useful for warm starts and diagnostics.
- Warm-start runs that embed an exact tree, perturb it, train it, snap it, and verify the result.
- SymPy cleanup for readable formulas.
- High-precision `mpmath` checks after training.

Training mode can use numerical safety guards. Verification mode is stricter: snapped formulas are evaluated again under the recovery contract.

## What The Fits Look Like

The grid below shows two good fits and two failed/stretch diagnostics. Good candidates sit directly on the target; diagnostic candidates visibly miss the shape. The legend is outside the panels, and the curves use solid colors so overlap does not turn into dashed-line clutter.

![2x2 grid of EML good fits and failed diagnostics](readme-assets/fit-gallery.svg)

## What Counts As Recovery

Training loss alone is not recovery.

A formula is `recovered` only when an exact candidate passes the verifier across:

- training data;
- held-out data;
- extrapolation data;
- high-precision checks.

Compiler output alone is not trained recovery. A compiler seed can prove that a formula is representable and can initialize a run, but it is not a discovery claim by itself.

Warm starts, same-AST returns, scaffolded runs, refits, repaired candidates, compile-only checks, and unsupported cases are all separate evidence regimes. That separation is deliberate. It keeps a successful scaffolded or repaired result from being mistaken for blind discovery.

## Install

Python `>=3.11,<3.13` is supported.

```bash
python -m pip install -e ".[dev]"
```

The package installs a CLI:

```bash
eml-sr --help
```

## Quick Start

Verify the paper-grounded EML identities for `exp` and `log`:

```bash
eml-sr verify-paper
```

List built-in demos:

```bash
eml-sr list-demos
```

Compile a supported scientific-law demo into exact EML:

```bash
eml-sr demo beer_lambert --compile-eml --output beer-compile-report.json
```

Run a compiler warm-start path:

```bash
eml-sr demo beer_lambert --warm-start-eml --output beer-warm-report.json
```

Try a shallow blind EML training baseline:

```bash
eml-sr demo exp --train-eml --depth 1 --steps 80 --restarts 2 --output exp-trained.json
```

List benchmark suites:

```bash
eml-sr list-benchmarks
```

Run the small smoke benchmark:

```bash
eml-sr benchmark smoke
```

Run the v1.13 paper-track campaign:

```bash
eml-sr campaign paper-tracks --output-root artifacts/campaigns --label v1.13-paper-tracks-final --overwrite
```

Rebuild the publication package:

```bash
eml-sr publication-rebuild --output-dir artifacts/paper/v1.13 --overwrite --allow-dirty
```

List expanded datasets:

```bash
eml-sr list-datasets
```

Run the matched baseline harness:

```bash
eml-sr baseline-harness --output-dir artifacts/baselines/v1.13 --overwrite
```

Run tests:

```bash
python -m pytest
```

## Demo Ladder

The demos favor normalized, dimensionless formulas with a useful mix of recognizability and feasibility:

- `exp` and `log`: identity checks for the core EML semantics.
- `beer_lambert`: exponential decay and a high-probability warm-start path.
- `radioactive_decay`: a simple scientific baseline.
- `shockley`: an electronics law close to EML's exponential-minus-constant bias.
- `arrhenius`: normalized reciprocal-temperature behavior, `exp(-0.8/x)`.
- `michaelis_menten`: saturation behavior, `2*x/(x+0.5)`.
- `logistic`: nonlinear growth, currently treated carefully as a harder diagnostic.
- `planck`: iconic normalized spectrum, currently a stretch diagnostic rather than a solved blind recovery.
- `damped_oscillator`: visually strong, but harder because it mixes decay and oscillation.

Arrhenius and Michaelis-Menten currently count as exact compiler warm-start / same-AST evidence, not blind discovery. Planck and logistic stay in the stretch/unsupported bucket unless the strict compiler, warm-start, and verifier contracts pass.

## Evidence Labels

| Label | Meaning |
| --- | --- |
| `recovered` | An exact EML candidate passed verifier checks. |
| `blind_recovery` | Random or scaffold-free training snapped to an exact EML candidate that verified. |
| `trained_exact_recovery` | A post-training snapped exact EML AST verified. |
| `same_ast_warm_start_return` | A warm start returned to the same exact AST and verified. Useful basin evidence, not blind discovery. |
| `verified_equivalent_warm_start_recovery` | A warm start snapped to a different exact AST that still verified. |
| `compiled_seed` | The source formula compiled into exact EML and validated as a seed. |
| `verified_showcase` | A non-EML catalog formula verified for demo coverage; it is not EML discovery. |
| `repaired_candidate` | Cleanup repaired a failed exact candidate; this is repair evidence only. |
| `unsupported` | A depth, node, operator, compiler, warm-start, or verifier gate failed closed. |

## Boundaries

This is not a claim that arbitrary deep formulas can be discovered blindly. The reported behavior is much more specific:

- shallow blind recovery is plausible and testable;
- deeper random-initialized recovery gets hard quickly;
- warm starts can show that useful basins exist;
- compiler paths can prove representability and provide seeds;
- repairs can rescue some failed exact candidates, but they are still repair evidence;
- basis-only and literal-constant runs have separate denominators;
- every recovery claim belongs to the verifier, not the optimizer.

That is the point of the package: make symbolic-regression experiments over EML trees concrete, reproducible, and hard to overstate.
