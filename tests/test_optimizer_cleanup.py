import numpy as np

from eml_symbolic_regression.cleanup import cleanup_candidate
from eml_symbolic_regression.datasets import get_demo
from eml_symbolic_regression.optimize import TrainingConfig, fit_eml_tree


def test_optimizer_returns_snapped_candidate_manifest():
    spec = get_demo("exp")
    train = spec.make_splits(points=16)[0]
    result = fit_eml_tree(
        train.inputs,
        train.target,
        TrainingConfig(depth=1, variables=("x",), steps=2, restarts=1, seed=123),
    )
    assert result.status in {"snapped_candidate", "failed"}
    assert "restarts" in result.manifest
    assert result.snap.expression.node_count() >= 3


def test_cleanup_report_verifies_candidate():
    spec = get_demo("log")
    splits = spec.make_splits(points=24)
    report = cleanup_candidate(spec.candidate, splits)
    assert "log" in report.cleaned or "exp" in report.cleaned
    assert report.verification is not None
    assert report.verification.status == "recovered"
