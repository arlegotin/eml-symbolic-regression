import numpy as np
import pytest

from eml_symbolic_regression.compiler import scaled_exponential_expr
from eml_symbolic_regression.datasets import get_demo
from eml_symbolic_regression.verify import verify_candidate


@pytest.mark.parametrize(
    ("formula_id", "variable", "coefficient"),
    [
        ("beer_lambert", "x", -0.8),
        ("radioactive_decay", "t", -0.4),
    ],
)
def test_scaled_exponential_expr_is_exact_shape_evidence(formula_id: str, variable: str, coefficient: float) -> None:
    expr = scaled_exponential_expr(variable, coefficient)
    points = np.linspace(0.0, 2.0, 9)

    np.testing.assert_allclose(
        expr.evaluate_numpy({variable: points}),
        np.exp(coefficient * points).astype(np.complex128),
        atol=1e-10,
        rtol=1e-10,
    )
    assert expr.depth() == 9
    assert expr.node_count() == 19
    assert expr.constants() == {complex(1.0), complex(coefficient)}

    demo = get_demo(formula_id)
    report = verify_candidate(expr, demo.make_splits(points=32, seed=0), tolerance=1e-8)
    assert report.status == "recovered"
