import numpy as np

from eml_symbolic_regression.cleanup import cleanup_candidate
from eml_symbolic_regression.datasets import get_demo
from eml_symbolic_regression.optimize import TrainingConfig, fit_eml_tree
from eml_symbolic_regression.verify import verify_candidate


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


def test_optimizer_scaffold_recovers_exp_with_manifest_provenance():
    spec = get_demo("exp")
    splits = spec.make_splits(points=16)
    result = fit_eml_tree(
        splits[0].inputs,
        splits[0].target,
        TrainingConfig(depth=1, variables=("x",), steps=2, restarts=1, seed=0),
    )
    report = verify_candidate(result.snap.expression, splits)
    kinds = [(attempt.get("initialization") or {}).get("kind") for attempt in result.manifest["restarts"]]

    assert report.status == "recovered"
    assert "scaffold_exp" in kinds


def test_optimizer_custom_initializer_does_not_add_scaffold_provenance():
    spec = get_demo("exp")
    train = spec.make_splits(points=16)[0]

    def initializer(model, restart, seed):
        model.force_exp("x")
        return {"kind": "custom_initializer", "restart": restart, "seed": seed}

    result = fit_eml_tree(
        train.inputs,
        train.target,
        TrainingConfig(depth=1, variables=("x",), steps=2, restarts=1, seed=0),
        initializer=initializer,
    )
    kinds = [(attempt.get("initialization") or {}).get("kind") for attempt in result.manifest["restarts"]]

    assert kinds == ["custom_initializer"]


def test_cleanup_report_verifies_candidate():
    spec = get_demo("log")
    splits = spec.make_splits(points=24)
    report = cleanup_candidate(spec.candidate, splits)
    assert "log" in report.cleaned or "exp" in report.cleaned
    assert report.verification is not None
    assert report.verification.status == "recovered"
