status: passed

# Phase 82 Verification

## Result

Passed. The codebase can represent, evaluate, serialize, and document `GEML_a`, with raw EML and i*pi EML available as named specializations.

## Requirements Checked

- **GEML-01:** `GEML_a(x, y) = exp(a*x) - log(y)/a` is represented by `EmlOperator("geml_a")` and exact `Geml` AST nodes.
- **GEML-02:** raw EML remains the canonical `a = 1` specialization, while i*pi EML is exposed through `ipi_eml_operator()` and `ipi_eml_expr()`.
- **GEML-03:** NumPy, PyTorch, and exact mpmath evaluators agree in focused tests.
- **GEML-04:** exact AST JSON, semantics documents, and SymPy export preserve GEML parameter and named-specialization metadata for GEML nodes while preserving legacy raw/centered artifacts.
- **GEML-05:** tests verify `exp(a*GEML_a(u, v)) = exp(a*exp(a*u))/v` for representative `a = 1`, `a = 2`, and `a = i*pi`.

## Review Fixes

The GSD code-review pass found four issues or gaps:

- canonical `a = 1` representation could split between raw `Eml` and `Geml`;
- named specialization metadata could disagree with numeric `a`;
- i*pi mpmath evaluation used double-precision `np.pi`;
- master-tree GEML snap/embed coverage was missing.

All four were addressed before the implementation commit:

- `geml:1` and `geml_operator(1.0)` now canonicalize to raw EML;
- invalid named specialization/parameter pairs raise `ValueError`;
- i*pi mpmath evaluation uses `mp.j * mp.pi`;
- master-tree tests cover i*pi GEML snap and same-family embedding.

## Tests

Passed:

```bash
PYTHONPATH=src python -m pytest tests/test_semantics_expression.py -q
# 17 passed in 1.48s

PYTHONPATH=src python -m pytest tests/test_master_tree.py tests/test_optimizer_cleanup.py -q
# 22 passed, 3 warnings in 8.09s

PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py::test_optimizer_budget_parses_operator_family_and_schedule tests/test_benchmark_runner.py::test_runner_executes_operator_family_smoke_matrix -q
# 2 passed in 3.34s

PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py tests/test_campaign.py -q
# 124 passed, 3 warnings in 268.03s

PYTHONPATH=src python -m pytest tests/test_semantics_expression.py tests/test_master_tree.py tests/test_benchmark_contract.py::test_arrhenius_evidence_suite_contains_exact_warm_start_case tests/test_benchmark_contract.py::test_michaelis_evidence_suite_contains_exact_warm_start_case -q
# 35 passed, 1 warning in 0.98s

PYTHONPATH=src python -m compileall -q src
# passed

git diff --check
# passed
```

Warnings were pre-existing numerical overflow/divide-by-zero warnings in benchmark stress paths and centered/raw EML tests.
