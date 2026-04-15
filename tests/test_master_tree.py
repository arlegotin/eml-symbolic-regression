import numpy as np
import pytest

from eml_symbolic_regression.master_tree import EmbeddingError, SoftEMLTree


def test_univariate_parameter_count_matches_paper():
    for depth in (1, 2, 3):
        tree = SoftEMLTree(depth, ("x",))
        assert tree.parameter_count() == tree.expected_univariate_parameter_count()
        assert tree.parameter_count() == 5 * (2**depth) - 6


def test_force_exp_snaps_to_paper_identity():
    tree = SoftEMLTree(1, ("x",))
    tree.force_exp("x")
    snap = tree.snap()
    x = np.linspace(-1.0, 1.0, 10)
    np.testing.assert_allclose(snap.expression.evaluate_numpy({"x": x}), np.exp(x), atol=1e-12)
    assert snap.min_margin > 0.99


def test_force_log_snaps_to_paper_identity():
    tree = SoftEMLTree(3, ("x",))
    tree.force_log("x")
    snap = tree.snap()
    x = np.linspace(0.25, 3.0, 10)
    np.testing.assert_allclose(snap.expression.evaluate_numpy({"x": x}), np.log(x), atol=1e-12)
    assert snap.expression.depth() == 3


def test_slot_catalog_exposes_child_choices():
    tree = SoftEMLTree(2, ("x",))
    catalog = tree.slot_catalog()
    assert catalog["root.left"] == ["const:1", "var:x", "child"]
    assert catalog["root.L.left"] == ["const:1", "var:x"]


def test_force_scaled_exp_snaps_to_exact_depth_nine_shape():
    tree = SoftEMLTree(9, ("x",), constants=(-0.8,))

    embedding = tree.force_scaled_exp("x", -0.8)
    snap = tree.snap()

    x = np.linspace(0.0, 3.0, 12)
    np.testing.assert_allclose(snap.expression.evaluate_numpy({"x": x}), np.exp(-0.8 * x), atol=1e-12)
    assert embedding.success
    assert embedding.round_trip_equal
    assert snap.expression.depth() == 9
    assert snap.active_node_count == 19
    assert snap.min_margin > 0.99
    assert embedding.snap.min_margin > 0.99


def test_force_scaled_exp_requires_coefficient_in_constant_bank():
    tree = SoftEMLTree(9, ("x",), constants=(1.0,))

    with pytest.raises(EmbeddingError, match="missing_constant"):
        tree.force_scaled_exp("x", -0.8)
