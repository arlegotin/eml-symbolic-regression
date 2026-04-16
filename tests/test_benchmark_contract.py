import json

import pytest

from eml_symbolic_regression.benchmark import (
    BenchmarkCase,
    BenchmarkSuite,
    BenchmarkValidationError,
    OptimizerBudget,
    builtin_suite,
    list_builtin_suites,
    load_suite,
)
from eml_symbolic_regression.cli import build_parser
from eml_symbolic_regression.proof import paper_claim


def test_builtin_suite_registry_expands_stable_run_ids():
    assert {
        "smoke",
        "v1.2-evidence",
        "for-demo-diagnostics",
        "v1.5-shallow-pure-blind",
        "v1.5-shallow-proof",
        "proof-perturbed-basin",
        "proof-perturbed-basin-beer-probes",
        "proof-depth-curve",
    } <= set(list_builtin_suites())
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


@pytest.mark.parametrize("start_mode", ["catalog", "compile", "blind"])
def test_non_perturbable_start_modes_reject_perturbation_noise(start_mode):
    suite = BenchmarkSuite.from_mapping(
        {
            "schema": "eml.benchmark_suite.v1",
            "id": "bad",
            "cases": [
                {
                    "id": "bad-case",
                    "formula": "exp",
                    "start_mode": start_mode,
                    "perturbation_noise": [1.0],
                }
            ],
        }
    )

    with pytest.raises(BenchmarkValidationError) as exc:
        suite.validate()

    assert exc.value.reason == "invalid_perturbation"


def test_perturbed_tree_defaults_to_perturbed_true_tree_training_and_keeps_noise_grid():
    case = BenchmarkCase.from_mapping(
        {
            "id": "basin-depth1-perturbed",
            "formula": "basin_depth1_exp",
            "start_mode": "perturbed_tree",
            "perturbation_noise": [0.05, 0.25],
        },
        path="cases[0]",
    )
    suite = BenchmarkSuite("proof-perturbed-basin", "perturbed tree contract", (case,))

    runs = suite.expanded_runs()

    assert {run.start_mode for run in runs} == {"perturbed_tree"}
    assert {run.training_mode for run in runs} == {"perturbed_true_tree_training"}
    assert [run.perturbation_noise for run in runs] == [0.05, 0.25]


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
            "claim_id": "paper-shallow-scaffolded-recovery",
            "threshold_policy_id": "scaffolded_bounded_100_percent",
            "training_mode": "blind_training",
        },
        path="cases[0]",
    )
    suite = BenchmarkSuite("v1.5-shallow-proof", "proof metadata custom suite", (case,))
    suite.validate()
    runs = suite.expanded_runs()

    assert case.as_dict()["claim_id"] == "paper-shallow-scaffolded-recovery"
    assert runs[0].claim_id == "paper-shallow-scaffolded-recovery"
    assert runs[0].threshold_policy_id == "scaffolded_bounded_100_percent"
    assert runs[0].training_mode == "blind_training"
    assert runs[0].as_dict()["threshold_policy_id"] == "scaffolded_bounded_100_percent"
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


def test_optimizer_budget_parses_and_serializes_constants():
    budget = OptimizerBudget.from_mapping(
        {"depth": 9, "constants": ["-0.8", {"real": "0.4", "imag": "0"}], "scaffold_initializers": ["scaled_exp"]}
    )

    assert budget.constants == (complex(-0.8), complex(0.4))
    assert budget.scaffold_initializers == ("scaled_exp",)
    assert budget.as_dict()["constants"] == ["-0.8", "0.4"]
    assert budget.as_dict()["scaffold_initializers"] == ["scaled_exp"]

    with pytest.raises(BenchmarkValidationError) as exc:
        OptimizerBudget.from_mapping({"constants": ["nan"]}).validate("optimizer")

    assert exc.value.reason == "invalid_budget"
    assert exc.value.path == "optimizer.constants[0]"

    with pytest.raises(BenchmarkValidationError) as exc:
        OptimizerBudget.from_mapping({"scaffold_initializers": "scaled_exp"}).validate("optimizer")

    assert exc.value.reason == "malformed_budget"
    assert exc.value.path == "optimizer.scaffold_initializers"

    with pytest.raises(BenchmarkValidationError) as exc:
        OptimizerBudget.from_mapping({"scaffold_initializers": ["bad"]}).validate("optimizer")

    assert exc.value.reason == "invalid_budget"
    assert exc.value.path == "optimizer.scaffold_initializers"


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
            "claim_id": "paper-shallow-scaffolded-recovery",
            "threshold_policy_id": "scaffolded_bounded_100_percent",
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
        ({"claim_id": "missing-claim", "threshold_policy_id": "measured_pure_blind_recovery", "training_mode": "blind_training"}, "claim_id"),
        ({"claim_id": "paper-shallow-blind-recovery", "training_mode": "blind_training"}, "threshold_policy_id"),
        ({"claim_id": "paper-shallow-blind-recovery", "threshold_policy_id": "missing-policy", "training_mode": "blind_training"}, "threshold_policy_id"),
        ({"claim_id": "paper-shallow-blind-recovery", "threshold_policy_id": "measured_pure_blind_recovery", "training_mode": "catalog_verification"}, "training_mode"),
        (
            {
                "claim_id": "paper-shallow-blind-recovery",
                "threshold_policy_id": "measured_pure_blind_recovery",
                "training_mode": "perturbed_true_tree_training",
            },
            "training_mode",
        ),
        (
            {
                "claim_id": "paper-shallow-blind-recovery",
                "threshold_policy_id": "measured_pure_blind_recovery",
                "training_mode": "blind_training",
            },
            "optimizer.scaffold_initializers",
        ),
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
        "shallow-exp-pure-blind",
        "shallow-log-pure-blind",
        "shallow-radioactive-decay-pure-blind",
        "shallow-beer-lambert-pure-blind",
        "shallow-scaled-exp-growth-pure-blind",
        "shallow-scaled-exp-fast-decay-pure-blind",
    )


def test_shallow_scaffolded_claim_declares_signed_scaled_case_inventory():
    claim = paper_claim("paper-shallow-scaffolded-recovery")

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
    cases_by_id = {case.id: case for case in suite.cases}

    assert [case.id for case in suite.cases] == [
        "shallow-exp-blind",
        "shallow-log-blind",
        "shallow-radioactive-decay-blind",
        "shallow-beer-lambert-blind",
        "shallow-scaled-exp-growth-blind",
        "shallow-scaled-exp-fast-decay-blind",
    ]
    assert len(runs) == 18
    assert {run.seed for run in runs} == {0, 1, 2}
    assert {run.claim_id for run in runs} == {"paper-shallow-scaffolded-recovery"}
    assert {run.threshold_policy_id for run in runs} == {"scaffolded_bounded_100_percent"}
    assert {run.training_mode for run in runs} == {"blind_training"}
    assert {run.start_mode for run in runs} == {"blind"}
    assert all({"v1.5", "proof", "bounded", "scaffolded_blind"} <= set(run.tags) for run in runs)
    assert all(run.optimizer.steps > 0 and run.optimizer.restarts > 0 for run in runs)
    assert all(run.optimizer.as_dict()["constants"] for run in runs)
    assert all(run.optimizer.scaffold_initializers for run in runs)
    assert all(run.threshold_policy_id == paper_claim(run.claim_id).threshold_policy_id for run in runs)
    assert cases_by_id["shallow-exp-blind"].optimizer.depth == 1
    assert cases_by_id["shallow-log-blind"].optimizer.depth == 3

    coefficient_cases = {
        "shallow-radioactive-decay-blind": -0.4,
        "shallow-beer-lambert-blind": -0.8,
        "shallow-scaled-exp-growth-blind": 0.4,
        "shallow-scaled-exp-fast-decay-blind": -1.2,
    }
    for case_id, coefficient in coefficient_cases.items():
        case = cases_by_id[case_id]
        assert case.optimizer.depth == 9
        assert case.optimizer.constants == (complex(coefficient),)
        assert case.optimizer.as_dict()["constants"] == [repr(float(coefficient))]


def test_v15_shallow_pure_blind_suite_expands_measured_random_only_runs():
    suite = load_suite("v1.5-shallow-pure-blind")
    runs = suite.expanded_runs()
    cases_by_id = {case.id: case for case in suite.cases}

    assert [case.id for case in suite.cases] == [
        "shallow-exp-pure-blind",
        "shallow-log-pure-blind",
        "shallow-radioactive-decay-pure-blind",
        "shallow-beer-lambert-pure-blind",
        "shallow-scaled-exp-growth-pure-blind",
        "shallow-scaled-exp-fast-decay-pure-blind",
    ]
    assert len(runs) == 18
    assert {run.seed for run in runs} == {0, 1, 2}
    assert {run.claim_id for run in runs} == {"paper-shallow-blind-recovery"}
    assert {run.threshold_policy_id for run in runs} == {"measured_pure_blind_recovery"}
    assert {run.training_mode for run in runs} == {"blind_training"}
    assert {run.start_mode for run in runs} == {"blind"}
    assert all({"v1.5", "proof", "measured", "pure_blind"} <= set(run.tags) for run in runs)
    assert all(run.optimizer.scaffold_initializers == () for run in runs)
    assert all(run.threshold_policy_id == paper_claim(run.claim_id).threshold_policy_id for run in runs)
    assert cases_by_id["shallow-exp-pure-blind"].optimizer.depth == 1
    assert cases_by_id["shallow-log-pure-blind"].optimizer.depth == 3

    coefficient_cases = {
        "shallow-radioactive-decay-pure-blind": -0.4,
        "shallow-beer-lambert-pure-blind": -0.8,
        "shallow-scaled-exp-growth-pure-blind": 0.4,
        "shallow-scaled-exp-fast-decay-pure-blind": -1.2,
    }
    for case_id, coefficient in coefficient_cases.items():
        case = cases_by_id[case_id]
        assert case.optimizer.depth == 9
        assert case.optimizer.constants == (complex(coefficient),)
        assert case.optimizer.as_dict()["constants"] == [repr(float(coefficient))]


def test_proof_perturbed_basin_suite_expands_bounded_nonzero_runs():
    suite = load_suite("proof-perturbed-basin")
    runs = suite.expanded_runs()
    cases_by_id = {case.id: case for case in suite.cases}

    assert [case.id for case in suite.cases] == [
        "basin-depth1-perturbed",
        "basin-depth2-perturbed",
        "basin-depth3-perturbed",
        "basin-beer-lambert-bound",
    ]
    assert len(runs) == 9
    assert {run.start_mode for run in runs} == {"perturbed_tree"}
    assert {run.training_mode for run in runs} == {"perturbed_true_tree_training"}
    assert {run.claim_id for run in runs} == {"paper-perturbed-true-tree-basin"}
    assert {run.threshold_policy_id for run in runs} == {"bounded_100_percent"}
    assert all(run.perturbation_noise > 0.0 for run in runs)
    assert all({"v1.5", "proof", "bounded", "perturbed_tree"} <= set(run.tags) for run in runs)
    assert all(run.threshold_policy_id == paper_claim(run.claim_id).threshold_policy_id for run in runs)
    assert cases_by_id["basin-depth1-perturbed"].optimizer.depth == 1
    assert cases_by_id["basin-depth1-perturbed"].optimizer.warm_steps == 12
    assert cases_by_id["basin-depth2-perturbed"].optimizer.depth == 2
    assert cases_by_id["basin-depth2-perturbed"].optimizer.warm_steps == 16
    assert cases_by_id["basin-depth3-perturbed"].optimizer.depth == 3
    assert cases_by_id["basin-depth3-perturbed"].optimizer.warm_steps == 20
    assert cases_by_id["basin-beer-lambert-bound"].optimizer.warm_steps == 40
    assert cases_by_id["basin-beer-lambert-bound"].optimizer.warm_restarts == 1
    assert cases_by_id["basin-beer-lambert-bound"].optimizer.max_warm_depth == 10


def test_perturbed_basin_probe_suite_keeps_high_noise_outside_thresholds():
    suite = load_suite("proof-perturbed-basin-beer-probes")
    runs = suite.expanded_runs()

    assert [case.id for case in suite.cases] == ["basin-beer-lambert-bound-probes"]
    assert len(runs) == 4
    assert {run.formula for run in runs} == {"beer_lambert"}
    assert {run.start_mode for run in runs} == {"perturbed_tree"}
    assert {run.training_mode for run in runs} == {"perturbed_true_tree_training"}
    assert {run.perturbation_noise for run in runs} == {15.0, 35.0}
    assert {run.seed for run in runs} == {0, 1}
    assert {run.claim_id for run in runs} == {None}
    assert {run.threshold_policy_id for run in runs} == {None}
    assert all({"bound_probe", "beer_lambert", "high_noise"} <= set(run.tags) for run in runs)


def test_proof_depth_curve_suite_expands_blind_and_perturbed_rows():
    suite = load_suite("proof-depth-curve")
    runs = suite.expanded_runs()
    cases_by_id = {case.id: case for case in suite.cases}

    assert [case.id for case in suite.cases] == [
        "depth-2-blind",
        "depth-3-blind",
        "depth-4-blind",
        "depth-5-blind",
        "depth-6-blind",
        "depth-2-perturbed",
        "depth-3-perturbed",
        "depth-4-perturbed",
        "depth-5-perturbed",
        "depth-6-perturbed",
    ]
    assert len(runs) == 20
    assert {run.seed for run in runs} == {0, 1}
    assert {run.claim_id for run in runs} == {"paper-blind-depth-degradation"}
    assert {run.threshold_policy_id for run in runs} == {"measured_depth_curve"}
    assert {run.start_mode for run in runs} == {"blind", "perturbed_tree"}
    assert {run.training_mode for run in runs} == {"blind_training", "perturbed_true_tree_training"}
    assert all({"v1.5", "proof", "measured", "depth_curve"} <= set(run.tags) for run in runs)
    assert all(run.threshold_policy_id == paper_claim(run.claim_id).threshold_policy_id for run in runs)
    assert {cases_by_id[f"depth-{depth}-blind"].optimizer.depth for depth in range(2, 7)} == {2, 3, 4, 5, 6}
    assert {cases_by_id[f"depth-{depth}-perturbed"].optimizer.depth for depth in range(2, 7)} == {2, 3, 4, 5, 6}
    assert all(run.perturbation_noise == 0.0 for run in runs if run.start_mode == "blind")
    assert all(run.perturbation_noise > 0.0 for run in runs if run.start_mode == "perturbed_tree")
    assert cases_by_id["depth-2-perturbed"].optimizer.warm_steps == 20
    assert cases_by_id["depth-6-perturbed"].optimizer.warm_steps == 30


def test_cli_start_mode_filter_accepts_perturbed_tree():
    args = build_parser().parse_args(["benchmark", "proof-perturbed-basin", "--start-mode", "perturbed_tree"])

    assert args.start_mode == ["perturbed_tree"]


@pytest.mark.parametrize(
    ("override", "path_suffix"),
    [
        ({"start_mode": "warm_start", "training_mode": "compiler_warm_start_training"}, "start_mode"),
        ({"start_mode": "blind", "training_mode": "blind_training"}, "start_mode"),
        ({"start_mode": "compile", "training_mode": "compile_only_verification"}, "start_mode"),
        ({"perturbation_noise": [0.0]}, "perturbation_noise"),
        ({"training_mode": None}, "training_mode"),
        ({"threshold_policy_id": "measured_depth_curve"}, "threshold_policy_id"),
    ],
)
def test_perturbed_basin_proof_cases_reject_invalid_metadata(override, path_suffix):
    payload = {
        "id": "basin-depth1-perturbed",
        "formula": "basin_depth1_exp",
        "start_mode": "perturbed_tree",
        "perturbation_noise": [0.05],
        "claim_id": "paper-perturbed-true-tree-basin",
        "threshold_policy_id": "bounded_100_percent",
        "training_mode": "perturbed_true_tree_training",
        **{key: value for key, value in override.items() if value is not None},
    }
    if "training_mode" in override and override["training_mode"] is None:
        payload.pop("training_mode")
    suite = BenchmarkSuite.from_mapping({"id": "proof-perturbed-basin", "cases": [payload]})

    with pytest.raises(BenchmarkValidationError) as exc:
        suite.validate()

    assert exc.value.reason == "invalid_proof_contract"
    assert exc.value.path == f"cases[0].{path_suffix}"


def test_perturbed_basin_proof_cases_reject_caller_supplied_evidence_class():
    with pytest.raises(BenchmarkValidationError) as exc:
        BenchmarkCase.from_mapping(
            {
                "id": "basin-depth1-perturbed",
                "formula": "basin_depth1_exp",
                "start_mode": "perturbed_tree",
                "perturbation_noise": [0.05],
                "claim_id": "paper-perturbed-true-tree-basin",
                "threshold_policy_id": "bounded_100_percent",
                "training_mode": "perturbed_true_tree_training",
                "evidence_class": "perturbed_true_tree_recovered",
            },
            path="cases[0]",
        )

    assert exc.value.reason == "invalid_proof_contract"
    assert exc.value.path == "cases[0].evidence_class"


@pytest.mark.parametrize(
    ("override", "reason", "path_suffix"),
    [
        ({"start_mode": "compile", "training_mode": "compile_only_verification"}, "invalid_perturbation", "perturbation_noise"),
        ({"start_mode": "warm_start", "training_mode": "compiler_warm_start_training"}, "invalid_proof_contract", "start_mode"),
        ({"threshold_policy_id": "bounded_100_percent"}, "invalid_proof_contract", "threshold_policy_id"),
        ({"training_mode": None}, "invalid_proof_contract", "training_mode"),
        ({"perturbation_noise": [0.0]}, "invalid_proof_contract", "perturbation_noise"),
    ],
)
def test_depth_curve_perturbed_rows_reject_invalid_metadata(override, reason, path_suffix):
    payload = {
        "id": "depth-4-perturbed",
        "formula": "depth_curve_depth4",
        "start_mode": "perturbed_tree",
        "perturbation_noise": [0.05],
        "claim_id": "paper-blind-depth-degradation",
        "threshold_policy_id": "measured_depth_curve",
        "training_mode": "perturbed_true_tree_training",
        **{key: value for key, value in override.items() if value is not None},
    }
    if "training_mode" in override and override["training_mode"] is None:
        payload.pop("training_mode")
    suite = BenchmarkSuite.from_mapping({"id": "proof-depth-curve", "cases": [payload]})

    with pytest.raises(BenchmarkValidationError) as exc:
        suite.validate()

    assert exc.value.reason == reason
    assert exc.value.path == f"cases[0].{path_suffix}"


@pytest.mark.parametrize(
    "override",
    [
        {"start_mode": "catalog", "training_mode": "catalog_verification"},
        {"start_mode": "compile", "training_mode": "compile_only_verification"},
        {"start_mode": "warm_start", "training_mode": "compiler_warm_start_training"},
        {"threshold_policy_id": "measured_depth_curve"},
        {"threshold_policy_id": "bounded_100_percent"},
    ],
)
def test_shallow_scaffolded_proof_suite_rejects_non_blind_or_wrong_threshold_metadata(override):
    payload = {
        "id": "shallow-exp-blind",
        "formula": "exp",
        "start_mode": "blind",
        "claim_id": "paper-shallow-scaffolded-recovery",
        "threshold_policy_id": "scaffolded_bounded_100_percent",
        "training_mode": "blind_training",
        **override,
    }
    suite = BenchmarkSuite.from_mapping({"id": "v1.5-shallow-proof", "cases": [payload]})

    with pytest.raises(BenchmarkValidationError) as exc:
        suite.validate()

    assert exc.value.reason == "invalid_proof_contract"
