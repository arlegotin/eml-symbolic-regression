import json

import pytest

from eml_symbolic_regression.benchmark import (
    BenchmarkCase,
    BenchmarkSuite,
    BenchmarkValidationError,
    builtin_suite,
    list_builtin_suites,
    load_suite,
)
from eml_symbolic_regression.proof import paper_claim


def test_builtin_suite_registry_expands_stable_run_ids():
    assert {"smoke", "v1.2-evidence", "for-demo-diagnostics", "v1.5-shallow-proof"} <= set(list_builtin_suites())
    suite = builtin_suite("smoke")
    runs = suite.expanded_runs()

    assert [run.case_id for run in runs] == ["exp-blind", "beer-warm", "planck-diagnostic"]
    assert runs[0].run_id == suite.expanded_runs()[0].run_id
    assert str(runs[0].artifact_path).endswith(f"{runs[0].run_id}.json")
    assert runs[0].claim_id is None
    assert runs[0].threshold_policy_id is None
    assert runs[0].training_mode == "blind_training"


def test_v12_evidence_suite_contains_perturbation_matrix():
    suite = load_suite("v1.2-evidence")
    runs = suite.expanded_runs()
    beer_runs = [run for run in runs if run.case_id == "beer-perturbation-sweep"]

    assert len(beer_runs) == 9
    assert {run.perturbation_noise for run in beer_runs} == {0.0, 5.0, 35.0}
    assert {run.seed for run in beer_runs} == {0, 1, 2}
    blind_formulas = {run.formula for run in runs if run.start_mode == "blind"}
    assert {"exp", "log", "radioactive_decay"} <= blind_formulas
    assert any(run.case_id == "michaelis-warm-diagnostic" and run.start_mode == "warm_start" for run in runs)
    assert any(run.formula == "planck" and "stretch" in run.tags for run in runs)


def test_for_demo_diagnostics_cover_selected_showcase_formulas():
    suite = load_suite("for-demo-diagnostics")
    formulas = {run.formula for run in suite.expanded_runs()}

    assert {
        "beer_lambert",
        "radioactive_decay",
        "michaelis_menten",
        "logistic",
        "shockley",
        "damped_oscillator",
        "planck",
    } <= formulas


def test_unknown_formula_fails_closed():
    suite = BenchmarkSuite.from_mapping(
        {
            "schema": "eml.benchmark_suite.v1",
            "id": "bad",
            "cases": [{"id": "bad-case", "formula": "nope", "start_mode": "blind"}],
        }
    )

    with pytest.raises(BenchmarkValidationError) as exc:
        suite.validate()

    assert exc.value.reason == "unknown_formula"
    assert exc.value.path == "cases[0].formula"


def test_non_warm_start_perturbation_fails_closed():
    suite = BenchmarkSuite.from_mapping(
        {
            "schema": "eml.benchmark_suite.v1",
            "id": "bad",
            "cases": [
                {
                    "id": "bad-case",
                    "formula": "exp",
                    "start_mode": "blind",
                    "perturbation_noise": [1.0],
                }
            ],
        }
    )

    with pytest.raises(BenchmarkValidationError) as exc:
        suite.validate()

    assert exc.value.reason == "invalid_perturbation"


def test_custom_suite_loads_from_json(tmp_path):
    path = tmp_path / "suite.json"
    path.write_text(
        json.dumps(
            {
                "schema": "eml.benchmark_suite.v1",
                "id": "custom",
                "artifact_root": str(tmp_path / "artifacts"),
                "cases": [{"id": "compile-exp", "formula": "exp", "start_mode": "compile", "dataset": {"points": 12}}],
            }
        ),
        encoding="utf-8",
    )

    suite = load_suite(path)
    runs = suite.expanded_runs()

    assert suite.id == "custom"
    assert len(runs) == 1
    assert runs[0].dataset.points == 12
    assert runs[0].claim_id is None
    assert runs[0].threshold_policy_id is None
    assert runs[0].training_mode == "compile_only_verification"
    assert str(runs[0].artifact_path).startswith(str(tmp_path / "artifacts"))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("seeds", "10"),
        ("perturbation_noise", "0.0"),
        ("tags", "smoke"),
    ],
)
def test_custom_suite_rejects_string_sequence_fields(tmp_path, field, value):
    path = tmp_path / "suite.json"
    path.write_text(
        json.dumps(
            {
                "schema": "eml.benchmark_suite.v1",
                "id": "custom",
                "cases": [{"id": "compile-exp", "formula": "exp", "start_mode": "compile", field: value}],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(BenchmarkValidationError) as exc:
        load_suite(path)

    assert exc.value.reason == "malformed_case"
    assert exc.value.path == f"cases[0].{field}"


def test_case_accepts_and_serializes_proof_metadata():
    case = BenchmarkCase.from_mapping(
        {
            "id": "shallow-exp-blind",
            "formula": "exp",
            "start_mode": "blind",
            "claim_id": "paper-shallow-blind-recovery",
            "threshold_policy_id": "bounded_100_percent",
            "training_mode": "blind_training",
        },
        path="cases[0]",
    )
    suite = BenchmarkSuite("v1.5-shallow-proof", "proof metadata custom suite", (case,))
    suite.validate()
    runs = suite.expanded_runs()

    assert case.as_dict()["claim_id"] == "paper-shallow-blind-recovery"
    assert runs[0].claim_id == "paper-shallow-blind-recovery"
    assert runs[0].threshold_policy_id == "bounded_100_percent"
    assert runs[0].training_mode == "blind_training"
    assert runs[0].as_dict()["threshold_policy_id"] == "bounded_100_percent"
    assert runs[0].run_id != type(runs[0])(
        suite_id=runs[0].suite_id,
        case_id=runs[0].case_id,
        formula=runs[0].formula,
        start_mode=runs[0].start_mode,
        seed=runs[0].seed,
        perturbation_noise=runs[0].perturbation_noise,
        dataset=runs[0].dataset,
        optimizer=runs[0].optimizer,
        artifact_path=runs[0].artifact_path,
        tags=runs[0].tags,
        expect_recovery=runs[0].expect_recovery,
        claim_id="paper-perturbed-true-tree-basin",
        threshold_policy_id="bounded_100_percent",
        training_mode="blind_training",
    ).run_id


@pytest.mark.parametrize(
    ("suite_id", "case_id", "path_suffix"),
    [
        ("proof-custom", "shallow-exp-blind", "claim_id"),
        ("v1.5-shallow-proof", "proof-exp", "id"),
    ],
)
def test_proof_contract_validation_enforces_claim_suite_and_case_scope(suite_id, case_id, path_suffix):
    case = BenchmarkCase.from_mapping(
        {
            "id": case_id,
            "formula": "exp",
            "start_mode": "blind",
            "claim_id": "paper-shallow-blind-recovery",
            "threshold_policy_id": "bounded_100_percent",
            "training_mode": "blind_training",
        },
        path="cases[0]",
    )
    suite = BenchmarkSuite(suite_id, "bad proof metadata scope", (case,))

    with pytest.raises(BenchmarkValidationError) as exc:
        suite.validate()

    assert exc.value.reason == "invalid_proof_contract"
    assert exc.value.path == f"cases[0].{path_suffix}"


@pytest.mark.parametrize(
    ("override", "path_suffix"),
    [
        ({"threshold_policy_id": "missing-policy"}, "threshold_policy_id"),
        ({"claim_id": "missing-claim", "threshold_policy_id": "bounded_100_percent", "training_mode": "blind_training"}, "claim_id"),
        ({"claim_id": "paper-shallow-blind-recovery", "training_mode": "blind_training"}, "threshold_policy_id"),
        ({"claim_id": "paper-shallow-blind-recovery", "threshold_policy_id": "missing-policy", "training_mode": "blind_training"}, "threshold_policy_id"),
        ({"claim_id": "paper-shallow-blind-recovery", "threshold_policy_id": "bounded_100_percent", "training_mode": "catalog_verification"}, "training_mode"),
        ({"claim_id": "paper-shallow-blind-recovery", "threshold_policy_id": "bounded_100_percent", "training_mode": "perturbed_true_tree_training"}, "training_mode"),
    ],
)
def test_proof_contract_validation_fails_closed(override, path_suffix):
    payload = {
        "id": "bad-proof-case",
        "formula": "exp",
        "start_mode": "blind",
        **override,
    }
    suite = BenchmarkSuite.from_mapping({"id": "bad-proof-suite", "cases": [payload]})

    with pytest.raises(BenchmarkValidationError) as exc:
        suite.validate()

    assert exc.value.reason == "invalid_proof_contract"
    assert exc.value.path == f"cases[0].{path_suffix}"


def test_shallow_blind_claim_declares_signed_scaled_case_inventory():
    claim = paper_claim("paper-shallow-blind-recovery")

    assert claim.case_ids == (
        "shallow-exp-blind",
        "shallow-log-blind",
        "shallow-radioactive-decay-blind",
        "shallow-beer-lambert-blind",
        "shallow-scaled-exp-growth-blind",
        "shallow-scaled-exp-fast-decay-blind",
    )


def test_v15_shallow_proof_suite_expands_fixed_proof_contract_runs():
    suite = load_suite("v1.5-shallow-proof")
    runs = suite.expanded_runs()

    assert [case.id for case in suite.cases] == [
        "shallow-exp-blind",
        "shallow-log-blind",
        "shallow-radioactive-decay-blind",
        "shallow-beer-lambert-blind",
    ]
    assert len(runs) == 12
    assert {run.seed for run in runs} == {0, 1, 2}
    assert {run.claim_id for run in runs} == {"paper-shallow-blind-recovery"}
    assert {run.threshold_policy_id for run in runs} == {"bounded_100_percent"}
    assert {run.training_mode for run in runs} == {"blind_training"}
    assert {run.start_mode for run in runs} == {"blind"}
    assert all({"v1.5", "proof", "bounded", "blind"} <= set(run.tags) for run in runs)
    assert all(run.optimizer.steps > 0 and run.optimizer.restarts > 0 for run in runs)
