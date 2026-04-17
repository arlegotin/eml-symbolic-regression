import numpy as np

from eml_symbolic_regression.cleanup import cleanup_candidate
from eml_symbolic_regression.datasets import get_demo
from eml_symbolic_regression.expression import Const, Var, ceml_s_expr
from eml_symbolic_regression.optimize import TrainingConfig, fit_eml_tree
from eml_symbolic_regression.semantics import ceml_s_operator, zeml_s_operator
from eml_symbolic_regression.verify import verify_candidate


EXPECTED_CENTERED_SCAFFOLD_EXCLUSIONS = [
    "exp:centered_family_same_family_witness_missing",
    "log:centered_family_same_family_witness_missing",
    "scaled_exp:centered_family_same_family_witness_missing",
]


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
    assert result.manifest["config"]["scaffold_initializers"] == ["exp", "log", "scaled_exp"]
    assert "scaffold_exp" in kinds


def test_optimizer_runs_fixed_centered_family_with_manifest_metadata():
    x = np.linspace(-1.0, 1.0, 16)
    target = 2.0 * np.expm1(x / 2.0)
    expected = ceml_s_expr(Var("x"), Const(1.0), s=2.0)
    result = fit_eml_tree(
        {"x": x},
        target,
        TrainingConfig(
            depth=1,
            variables=("x",),
            steps=2,
            restarts=1,
            seed=0,
            operator_family=ceml_s_operator(2.0),
        ),
    )

    assert result.snap.expression.to_node()["operator"]["label"] == "CEML_2"
    np.testing.assert_allclose(result.snap.expression.evaluate_numpy({"x": x}), expected.evaluate_numpy({"x": x}), atol=1e-12)
    assert result.manifest["config"]["operator_family"]["label"] == "CEML_2"
    assert result.manifest["config"]["scaffold_initializers"] == []
    assert result.manifest["scaffold_exclusions"] == EXPECTED_CENTERED_SCAFFOLD_EXCLUSIONS
    assert result.manifest["scaffold_witness_operator"]["label"] == "CEML_2"
    assert all(not item["attempt_kind"].startswith("scaffold_") for item in result.manifest["restarts"])


def test_optimizer_preserves_centered_schedule_metadata():
    x = np.linspace(-1.0, 1.0, 16)
    target = np.expm1(x)
    result = fit_eml_tree(
        {"x": x},
        target,
        TrainingConfig(
            depth=1,
            variables=("x",),
            steps=4,
            restarts=1,
            seed=0,
            operator_schedule=(zeml_s_operator(8.0), zeml_s_operator(4.0)),
        ),
    )

    assert result.manifest["config"]["operator_schedule"][0]["label"] == "ZEML_8"
    assert result.manifest["config"]["operator_schedule"][1]["label"] == "ZEML_4"
    assert result.manifest["config"]["scaffold_initializers"] == []
    assert result.manifest["scaffold_exclusions"] == EXPECTED_CENTERED_SCAFFOLD_EXCLUSIONS
    assert result.manifest["scaffold_witness_operator"]["label"] == "ZEML_8"
    assert all(not item["attempt_kind"].startswith("scaffold_") for item in result.manifest["restarts"])
    assert [item["operator"]["label"] for item in result.manifest["operator_trace"][:2]] == ["ZEML_8", "ZEML_4"]
    assert result.manifest["operator_trace"][-1]["phase"] == "hardening"
    assert result.manifest["operator_trace"][-1]["operator"]["label"] == "ZEML_4"
    assert result.snap.expression.to_node()["operator"]["label"] == "ZEML_4"


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


def test_optimizer_records_candidate_pool_selection_and_legacy_fallback():
    spec = get_demo("exp")
    splits = spec.make_splits(points=16)
    result = fit_eml_tree(
        splits[0].inputs,
        splits[0].target,
        TrainingConfig(
            depth=1,
            variables=("x",),
            steps=2,
            restarts=1,
            seed=0,
            hardening_steps=2,
            hardening_emit_interval=1,
        ),
        verification_splits=splits,
    )

    selection = result.manifest["selection"]
    selected = result.manifest["selected_candidate"]
    fallback = result.manifest["fallback_candidate"]
    candidates = result.manifest["candidates"]

    assert selection["mode"] == "verifier_gated_exact_candidate_pool"
    assert selection["candidate_count"] == len(candidates)
    assert len(candidates) >= 2
    assert selection["selected_candidate_id"] == selected["candidate_id"]
    assert selection["fallback_candidate_id"] == fallback["candidate_id"]
    assert fallback["source"] == "legacy_final_snap"
    assert any(candidate["source"] == "hardening_checkpoint" for candidate in candidates)
    assert selected["verification"]["status"] == "recovered"
    assert result.verification is not None
    assert result.verification.status == "recovered"


def test_optimizer_scaled_exp_scaffold_recovers_radioactive_decay_with_manifest():
    spec = get_demo("radioactive_decay")
    splits = spec.make_splits(points=12, seed=0)

    result = fit_eml_tree(
        splits[0].inputs,
        splits[0].target,
        TrainingConfig(
            depth=9,
            variables=("t",),
            constants=(-0.4,),
            steps=2,
            restarts=1,
            seed=0,
            scaffold_initializers=("scaled_exp",),
        ),
    )
    report = verify_candidate(result.snap.expression, splits)
    best_restart = result.manifest["best_restart"]
    initialization = best_restart["initialization"]

    assert report.status == "recovered"
    assert best_restart["attempt_kind"] == "scaffold_scaled_exp"
    assert initialization["kind"] == "scaffold_scaled_exp"
    assert initialization["variable"] == "t"
    assert initialization["coefficient"] == "-0.4"
    assert initialization["constant_label"] == "const:-0.4"
    assert initialization["strategy"] == "paper_scaled_exponential_family"
    assert initialization["seed"] == 0
    assert initialization["embedding"]["success"] is True
    assert initialization["embedding"]["snap"]["active_node_count"] == 19


def test_optimizer_scaled_exp_scaffold_recovers_beer_lambert_and_positive_growth():
    cases = (
        ("beer_lambert", "x", -0.8),
        ("scaled_exp_growth", "x", 0.4),
    )

    for formula, variable, coefficient in cases:
        spec = get_demo(formula)
        splits = spec.make_splits(points=12, seed=0)
        result = fit_eml_tree(
            splits[0].inputs,
            splits[0].target,
            TrainingConfig(
                depth=9,
                variables=(variable,),
                constants=(coefficient,),
                steps=2,
                restarts=1,
                seed=0,
                scaffold_initializers=("scaled_exp",),
            ),
        )
        report = verify_candidate(result.snap.expression, splits)

        assert report.status == "recovered"
        assert result.manifest["best_restart"]["attempt_kind"] == "scaffold_scaled_exp"


def test_cleanup_report_verifies_candidate():
    spec = get_demo("log")
    splits = spec.make_splits(points=24)
    report = cleanup_candidate(spec.candidate, splits)
    assert "log" in report.cleaned or "exp" in report.cleaned
    assert report.verification is not None
    assert report.verification.status == "recovered"
