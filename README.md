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
- A fail-closed SymPy subset compiler that emits exact EML ASTs with metadata, rule traces, assumptions, literal-constant provenance, and independent validation against ordinary SymPy evaluation.
- Constant-catalog soft master trees plus exact AST embedding with embed-to-snap round-trip checks.
- Compiler-driven warm-start training reports that perturb, train, snap, and verify through the existing optimizer/verifier boundary.
- Demo specs from `sources/FOR_DEMO.md`.
- CLI commands for paper checks and demo reports.
- Pytest coverage for the MVP pipeline.

The implementation is intentionally honest about scope: exact EML recovery is demonstrated for paper-grounded shallow formulas and for Beer-Lambert via a compiler-generated warm start. Harder showcase demos remain verified catalog candidates or explicit unsupported/depth reports unless a trained exact EML candidate passes the verifier.

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

Compile a supported demo formula into EML and validate it:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli demo beer_lambert --compile-eml --output artifacts/beer-compile-report.json
```

Run the compiler warm-start recovery path:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli demo beer_lambert --warm-start-eml --output artifacts/beer-lambert-warm-report.json
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
- `compiled_seed`: the source formula compiled to an exact EML AST and that AST verified numerically. This is a seed/provenance stage, not a trained recovery claim by itself.
- `warm_start_attempt`: the compiler seed was embedded into a compatible soft tree, optionally perturbed, trained through the existing optimizer, snapped, and classified.
- `trained_exact_recovery`: the post-training snapped exact EML AST passed the verifier. Demo reports promote top-level `claim_status` to `recovered` only at this stage.
- `unsupported`: the compiler or warm-start gate failed closed, usually because an operator, constant policy, depth, node budget, or warm-start depth limit was exceeded.

## Limits

This repo does not promise blind recovery of arbitrary deep formulas. The paper reports that blind recovery degrades sharply with depth and that depth-6 blind recovery was not observed in the reported attempts. Warm-start success is a different claim: it shows return-to-solution from a compiler-provided scaffold, with fixed literal constants when the source formula contains coefficients.

The default compiler/warm-start gates intentionally keep Michaelis-Menten and Planck honest: their catalog formulas verify, but their compiled EML trees currently exceed the default depth budget for warm-start promotion.
