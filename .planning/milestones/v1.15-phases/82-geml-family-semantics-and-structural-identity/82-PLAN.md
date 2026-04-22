# Phase 82 Plan: GEML Family Semantics and Structural Identity

## Tasks

1. Extend operator metadata.
   - Add fixed-parameter GEML support to `EmlOperator`.
   - Preserve raw EML defaults and existing centered-family metadata.
   - Add constructors/parsers for `GEML_a`, raw-as-`a=1`, and i*pi EML.

2. Add canonical backend semantics.
   - Implement NumPy and PyTorch evaluators for `GEML_a(x, y) = exp(a*x) - log(y)/a`.
   - Keep faithful verification semantics unclamped.
   - Reuse existing log branch/anomaly behavior for the second slot.

3. Extend exact AST support.
   - Add a family-aware exact node for GEML specializations.
   - Preserve legacy `Eml` JSON round trips.
   - Ensure JSON and semantics documents preserve family parameter and named specialization metadata.
   - Export accurate SymPy expressions.

4. Document and test the structural identity.
   - Add backend agreement tests for NumPy, PyTorch, and exact mpmath evaluation.
   - Add AST JSON round-trip and SymPy export tests.
   - Verify `exp(a*GEML_a(u, v)) = exp(a*exp(a*u))/v` for representative nonzero complex parameters.
   - Add concise documentation for the GEML family contract.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_semantics_expression.py -q`
- Focused raw/centered regression tests if semantic changes touch shared evaluator code.
- `PYTHONPATH=src python -m pytest tests/test_master_tree.py tests/test_optimizer_cleanup.py -q` if snapping or operator predicates change.
- `git diff --check`
