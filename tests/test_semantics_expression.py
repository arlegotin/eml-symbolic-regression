import json

import numpy as np

from eml_symbolic_regression.expression import expr_from_document, exp_expr, log_expr
from eml_symbolic_regression.semantics import eml_numpy


def test_eml_numpy_matches_definition():
    x = np.array([0.0, 0.5, 1.0], dtype=np.complex128)
    y = np.array([1.0, 2.0, 3.0], dtype=np.complex128)
    np.testing.assert_allclose(eml_numpy(x, y), np.exp(x) - np.log(y))


def test_paper_exp_identity():
    x = np.linspace(-1.0, 1.0, 20)
    expr = exp_expr("x")
    np.testing.assert_allclose(expr.evaluate_numpy({"x": x}), np.exp(x), atol=1e-12)


def test_paper_log_identity():
    x = np.linspace(0.25, 3.0, 20)
    expr = log_expr("x")
    np.testing.assert_allclose(expr.evaluate_numpy({"x": x}), np.log(x), atol=1e-12)


def test_ast_json_round_trip():
    expr = log_expr("x")
    document = expr.to_document(variables=["x"], source="test")
    encoded = json.dumps(document, sort_keys=True)
    decoded = json.loads(encoded)
    rebuilt = expr_from_document(decoded)
    x = np.linspace(0.5, 2.0, 8)
    np.testing.assert_allclose(rebuilt.evaluate_numpy({"x": x}), expr.evaluate_numpy({"x": x}))
