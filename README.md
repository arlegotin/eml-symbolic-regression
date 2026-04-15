# EML Symbolic Regression

This repo implements a practical MVP of the paper-grounded idea in `sources/NORTH_STAR.md`: a hybrid symbolic-regression engine over complete EML trees.

The EML operator is:

```text
eml(x, y) = exp(x) - log(y)
```

The paper shows that EML plus the constant `1` can generate the scientific-calculator elementary-function basis, and that formulas can be represented as regular binary EML trees. This implementation turns that into a Python/PyTorch package with exact ASTs, soft master trees, snapping, verification, cleanup, and demos.

## What Is Implemented

- Canonical and training-mode EML semantics.
- Exact immutable EML AST nodes with deterministic JSON serialization.
- Paper identities for `exp(x)` and `ln(x)`.
- Complete depth-bounded soft EML master trees with PyTorch `complex128` gates.
- Adam-based candidate generation with restarts, annealing, entropy/size penalties, snapping, and manifests.
- Verifier-owned recovery status over train, held-out, extrapolation, and mpmath point checks.
- SymPy export and targeted cleanup/report helpers.
- Demo specs from `sources/FOR_DEMO.md`.
- CLI commands for paper checks and demo reports.
- Pytest coverage for the MVP pipeline.

The implementation is intentionally honest about scope: exact EML recovery is demonstrated for paper-grounded shallow formulas, while harder showcase demos are verified catalog candidates unless a trained EML candidate is explicitly requested.

## Quick Commands

Run the paper identity checks:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli verify-paper
```

List demo targets:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli list-demos
```

Write a demo report:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli demo planck --output artifacts/planck-report.json
```

Try soft EML training on a shallow demo:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli demo exp --train-eml --depth 1 --steps 80 --restarts 2 --output artifacts/exp-trained.json
```

Run tests:

```bash
python -m pytest
```

## Demo Statuses

- `recovered`: an exact EML AST passed verifier checks.
- `verified_showcase`: a non-EML catalog formula from the demo spec passed verifier checks. This is useful for testing data, verification, cleanup, and reports, but it is not presented as EML discovery.
- `failed`: verifier checks failed; the report includes a reason code.

## Limits

This MVP does not promise blind recovery of arbitrary deep formulas. The paper reports that blind recovery degrades sharply with depth and that depth-6 blind recovery was not observed in the reported attempts. Harder demos should use curriculum, warm starts, or explicit priors before being presented as recovered EML formulas.
