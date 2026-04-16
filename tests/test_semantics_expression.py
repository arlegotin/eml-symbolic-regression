import json

import numpy as np
import torch

from eml_symbolic_regression.expression import Const, Eml, Var, expr_from_document, exp_expr, log_expr
from eml_symbolic_regression.semantics import AnomalyStats, TrainingSemanticsConfig, eml_numpy, eml_torch


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


def test_constant_occurrences_and_updates_are_path_stable():
    expr = Eml(Const(-0.8), Eml(Var("x"), Const(1.0)))

    occurrences = expr.constant_occurrences()
    assert [(item.path, item.refittable) for item in occurrences] == [("root.L", True), ("root.R.R", False)]

    updated = expr.with_constant_updates({"root.L": -0.5})
    updated_occurrences = updated.constant_occurrences()

    assert [complex(item.value) for item in updated_occurrences] == [complex(-0.5), complex(1.0)]
    assert updated.to_node()["right"] == expr.to_node()["right"]


def test_eml_torch_reports_log_domain_anomalies_and_penalty():
    stats = AnomalyStats()
    semantics = TrainingSemanticsConfig(
        clamp_exp_real=1.0,
        log_domain_epsilon=0.05,
        log_safety_weight=2.0,
        log_safety_margin=0.4,
        log_safety_imag_tolerance=0.1,
    )
    x = torch.tensor([2.0 + 0.0j, 0.0 + 0.0j], dtype=torch.complex128)
    y = torch.tensor([0.01 + 0.0j, -0.2 + 0.0j], dtype=torch.complex128)

    out = eml_torch(x, y, training=True, semantics=semantics, stats=stats, node="root")

    assert out.shape == x.shape
    assert stats.clamp_count == 1
    assert stats.exp_overflow_count == 1
    assert stats.log_small_magnitude_count == 1
    assert stats.log_non_positive_real_count == 1
    assert stats.log_branch_cut_count == 1
    assert stats.log_safety_penalty > 0.0
    assert float(stats.training_penalty().item()) > 0.0
    assert stats.by_node["root"]["log_branch_cut_count"] == 1
