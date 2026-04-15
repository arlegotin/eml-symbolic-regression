# Implementation Notes

## Architecture

The package follows the roadmap in `.planning/ROADMAP.md`:

1. `semantics.py` defines canonical and training-mode EML behavior.
2. `expression.py` defines exact ASTs and non-EML catalog candidates used by showcase demos.
3. `master_tree.py` defines complete depth-bounded soft EML trees.
4. `optimize.py` turns a soft tree into snapped candidates.
5. `verify.py` owns recovery status.
6. `cleanup.py` exports readable SymPy expressions and records cleanup reports.
7. `datasets.py` and `cli.py` expose the demo ladder from `sources/FOR_DEMO.md`.

## Recovery Contract

Training loss is not enough. A candidate is only `recovered` when:

- it is an exact EML AST,
- it is evaluated after snapping,
- train, held-out, extrapolation, and mpmath checks pass,
- the verifier emits `recovered`.

Non-EML catalog formulas can pass as `verified_showcase`; those reports are useful for demos and verifier coverage, but they are not labeled as EML recovery.

## Paper-Grounded Fixtures

The test suite includes the two identities most important for the MVP:

```text
exp(x) = eml(x, 1)
ln(x) = eml(1, eml(eml(1, x), 1))
```

It also checks the paper's univariate parameter count for complete master trees:

```text
P(n) = 5 * 2^n - 6
```

## Demo Ladder

The built-in demos mirror `sources/FOR_DEMO.md`:

- `exp`
- `log`
- `beer_lambert`
- `michaelis_menten`
- `logistic`
- `shockley`
- `damped_oscillator`
- `planck`

`exp` and `log` are exact EML candidates. The remaining demos are catalog showcase formulas with verifier reports, ready for future EML warm-start/curriculum work.
