import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import eml_symbolic_regression.benchmark as benchmark_module
from eml_symbolic_regression.basin import BasinTrainingResult
from eml_symbolic_regression.benchmark import (
    BenchmarkCase,
    BenchmarkRun,
    BenchmarkSuite,
    DatasetConfig,
    OptimizerBudget,
    RunFilter,
    builtin_suite,
    evidence_class_for_payload,
    execute_benchmark_run,
    run_benchmark_suite,
)
from eml_symbolic_regression.expression import Const, Eml, Var
from eml_symbolic_regression.master_tree import SoftEMLTree
from eml_symbolic_regression.optimize import FitResult
from eml_symbolic_regression.verify import SplitResult, VerificationReport


ROOT = Path(__file__).resolve().parents[1]
CLI_ENV = {**os.environ, "PYTHONPATH": str(ROOT / "src")}


def _verification_report(status: str) -> VerificationReport:
    return VerificationReport(
        status=status,
        candidate_kind="exact_eml",
        reason="verified" if status == "recovered" else "heldout_failed",
        split_results=[SplitResult("heldout", 0.0 if status == "recovered" else 1.0, 0.0, 0.0, status == "recovered")],
        high_precision_max_error=0.0 if status == "recovered" else 1.0,
        tolerance=1e-8,
    )


def _fit_from_slots(slots: dict[str, str], *, depth: int = 2) -> FitResult:
    tree = SoftEMLTree(depth, ("x",), (1.0,))
    for slot, choice in slots.items():
        node_path, side = slot.rsplit(".", 1)
        tree.set_slot(node_path, side, choice, strength=40.0)
    snap = tree.snap()
    return FitResult(
        status="snapped_candidate",
        best_loss=1.0,
        post_snap_loss=1.0,
        snap=snap,
        manifest={"schema": "eml.run_manifest.v1", "status": "snapped_candidate", "snap": snap.as_dict()},
    )


def test_runner_executes_catalog_compile_blind_and_warm_start(tmp_path):
    suite = type(builtin_suite("smoke"))(
        "smoke",
        "test smoke",
        builtin_suite("smoke").cases,
        tmp_path / "artifacts",
    )

    result = run_benchmark_suite(suite)
    payload = result.as_dict()

    assert payload["counts"]["total"] == 3
    assert all(item.artifact_path.exists() for item in result.results)
    statuses = {item.run.case_id: item.status for item in result.results}
    assert statuses["exp-blind"] in {"recovered", "snapped_but_failed", "failed"}
    assert statuses["beer-warm"] in {"same_ast_return", "verified_equivalent_ast", "snapped_but_failed"}
    assert statuses["planck-diagnostic"] == "unsupported"
    for item in result.results:
        artifact = json.loads(item.artifact_path.read_text(encoding="utf-8"))
        assert artifact["claim_id"] is None
        assert artifact["claim_class"] is None
        assert artifact["threshold"] is None
        assert artifact["training_mode"] == item.run.training_mode
        assert artifact["evidence_class"] == evidence_class_for_payload(artifact)
        assert artifact["dataset"] == item.run.dataset.as_dict()
        assert artifact["dataset_manifest"]["schema"] == "eml.proof_dataset_manifest.v1"
        assert artifact["budget"] == item.run.optimizer.as_dict()
        assert artifact["provenance"]["symbolic_expression"]
        assert artifact["provenance"]["source_document"].startswith("sources/")


def test_runner_filter_executes_subset(tmp_path):
    base = builtin_suite("v1.2-evidence")
    suite = type(base)(base.id, base.description, base.cases, tmp_path / "artifacts")

    result = run_benchmark_suite(suite, run_filter=RunFilter(case_ids=("beer-perturbation-sweep",), seeds=(0,)))

    assert len(result.results) == 3
    assert {item.run.perturbation_noise for item in result.results} == {0.0, 5.0, 35.0}


def test_proof_aware_run_artifact_includes_threshold_dataset_and_provenance(tmp_path):
    case = BenchmarkCase.from_mapping(
        {
            "id": "shallow-exp-blind",
            "formula": "exp",
            "start_mode": "blind",
            "seeds": [0],
            "dataset": {"points": 12},
            "optimizer": {"depth": 1, "steps": 6, "restarts": 1},
            "claim_id": "paper-shallow-scaffolded-recovery",
            "threshold_policy_id": "scaffolded_bounded_100_percent",
            "training_mode": "blind_training",
        },
        path="cases[0]",
    )
    suite = BenchmarkSuite("v1.5-shallow-proof", "cheap proof-aware runner smoke", (case,), tmp_path / "artifacts")

    result = run_benchmark_suite(suite)
    artifact = json.loads(result.results[0].artifact_path.read_text(encoding="utf-8"))

    assert artifact["claim_id"] == "paper-shallow-scaffolded-recovery"
    assert artifact["claim_class"] == "scaffolded_training_proof"
    assert artifact["training_mode"] == "blind_training"
    assert artifact["threshold"]["id"] == "scaffolded_bounded_100_percent"
    assert artifact["dataset_manifest"]["schema"] == "eml.proof_dataset_manifest.v1"
    assert artifact["dataset_manifest"]["formula_id"] == "exp"
    assert artifact["dataset_manifest"]["points"] == 12
    assert artifact["budget"]["depth"] == 1
    assert artifact["provenance"]["symbolic_expression"] == "exp(x)"
    assert artifact["provenance"]["source_document"] == "sources/paper.pdf"
    assert artifact["evidence_class"] == evidence_class_for_payload(artifact)


def test_shallow_beer_lambert_blind_run_artifact_exposes_scaled_scaffold_diagnostics(tmp_path):
    base = builtin_suite("v1.5-shallow-proof")
    suite = type(base)(base.id, base.description, base.cases, tmp_path / "artifacts")

    result = run_benchmark_suite(
        suite,
        run_filter=RunFilter(case_ids=("shallow-beer-lambert-blind",), seeds=(0,)),
    )
    artifact = json.loads(result.results[0].artifact_path.read_text(encoding="utf-8"))
    candidate = artifact["trained_eml_candidate"]
    initialization = candidate["best_restart"]["initialization"]
    metrics = artifact["metrics"]

    assert result.results[0].status == "recovered"
    assert artifact["status"] == "recovered"
    assert artifact["budget"]["constants"] == ["-0.8"]
    assert artifact["evidence_class"] == "scaffolded_blind_training_recovered"
    assert initialization["kind"] == "scaffold_scaled_exp"
    assert initialization["strategy"] == "paper_scaled_exponential_family"
    assert initialization["coefficient"] == "-0.8"
    assert initialization["constant_label"] == "const:-0.8"
    assert metrics["scaffold_source"] == "scaffold_scaled_exp"
    assert metrics["scaffold_strategy"] == "paper_scaled_exponential_family"
    assert metrics["scaffold_coefficient"] == "-0.8"
    assert metrics["best_loss"] is not None
    assert metrics["post_snap_loss"] <= 1e-20
    assert metrics["snap_min_margin"] > 0.99
    assert metrics["snap_active_node_count"] == 19
    assert metrics["verifier_status"] == "recovered"


def test_runner_writes_execution_error_if_payload_construction_fails(tmp_path):
    run = BenchmarkRun(
        suite_id="direct",
        case_id="orphan-threshold",
        formula="exp",
        start_mode="blind",
        seed=0,
        perturbation_noise=0.0,
        dataset=DatasetConfig(points=12),
        optimizer=OptimizerBudget(depth=1, steps=1, restarts=1),
        artifact_path=tmp_path / "orphan-threshold.json",
        threshold_policy_id="missing-policy",
        training_mode="blind_training",
    )

    result = execute_benchmark_run(run)
    artifact = json.loads(result.artifact_path.read_text(encoding="utf-8"))

    assert result.status == "execution_error"
    assert artifact["status"] == "execution_error"
    assert artifact["error"]["type"] == "ProofContractError"
    assert artifact["threshold"] is None
    assert artifact["evidence_class"] == "execution_failure"


def test_evidence_class_for_payload_is_derived_and_covers_reserved_repair():
    assert evidence_class_for_payload({"evidence_class": "blind_training_recovered", "status": "unsupported"}) == "unsupported"
    assert evidence_class_for_payload({"status": "repaired_candidate"}) == "repaired_candidate"
    assert evidence_class_for_payload({"status": "failed", "repair_status": "repaired"}) == "repaired_candidate"
    assert evidence_class_for_payload({"status": "recovered", "claim_status": "recovered", "run": {"start_mode": "catalog"}}) == "catalog_verified"
    assert evidence_class_for_payload({"status": "recovered", "claim_status": "recovered", "run": {"start_mode": "compile"}}) == "compile_only_verified"
    assert (
        evidence_class_for_payload(
            {
                "status": "recovered",
                "claim_status": "recovered",
                "training_mode": "blind_training",
                "run": {"start_mode": "blind"},
            }
        )
        == "blind_training_recovered"
    )
    assert (
        evidence_class_for_payload(
            {
                "status": "recovered",
                "claim_status": "recovered",
                "training_mode": "blind_training",
                "run": {"start_mode": "blind"},
                "trained_eml_candidate": {"best_restart": {"attempt_kind": "scaffold_scaled_exp"}},
            }
        )
        == "scaffolded_blind_training_recovered"
    )
    assert (
        evidence_class_for_payload(
            {
                "status": "same_ast_return",
                "claim_status": "same_ast_return",
                "training_mode": "compiler_warm_start_training",
                "run": {"start_mode": "warm_start"},
            }
        )
        == "same_ast"
    )
    assert (
        evidence_class_for_payload(
            {
                "status": "recovered",
                "claim_status": "recovered",
                "return_kind": "same_ast_return",
                "raw_status": "recovered",
                "training_mode": "perturbed_true_tree_training",
                "run": {"start_mode": "perturbed_tree", "perturbation_noise": 0.05},
            }
        )
        == "perturbed_true_tree_recovered"
    )
    assert (
        evidence_class_for_payload(
            {
                "status": "recovered",
                "claim_status": "recovered",
                "return_kind": "same_ast_return",
                "training_mode": "perturbed_true_tree_training",
                "run": {"start_mode": "warm_start", "perturbation_noise": 0.05},
            }
        )
        != "perturbed_true_tree_recovered"
    )


def test_perturbed_tree_runner_records_return_kind_and_raw_status(tmp_path):
    case = BenchmarkCase.from_mapping(
        {
            "id": "basin-depth1-perturbed",
            "formula": "basin_depth1_exp",
            "start_mode": "perturbed_tree",
            "seeds": [0],
            "perturbation_noise": [0.05],
            "dataset": {"points": 12},
            "optimizer": {"depth": 1, "warm_steps": 1, "warm_restarts": 1},
            "training_mode": "perturbed_true_tree_training",
        },
        path="cases[0]",
    )
    suite = BenchmarkSuite("proof-perturbed-basin", "cheap perturbed-tree smoke", (case,), tmp_path / "artifacts")

    result = run_benchmark_suite(suite)
    artifact = json.loads(result.results[0].artifact_path.read_text(encoding="utf-8"))

    assert result.results[0].status == "recovered"
    assert artifact["status"] == "recovered"
    assert artifact["run"]["start_mode"] == "perturbed_tree"
    assert artifact["training_mode"] == "perturbed_true_tree_training"
    assert artifact["return_kind"] == "same_ast_return"
    assert artifact["raw_status"] == "recovered"
    assert artifact["claim_status"] == "recovered"
    assert artifact["evidence_class"] == "perturbed_true_tree_recovered"
    assert artifact["stage_statuses"]["perturbed_true_tree_attempt"] == "recovered"
    assert artifact["perturbed_true_tree"]["schema"] == "eml.perturbed_true_tree_manifest.v1"
    assert artifact["perturbed_true_tree"]["optimizer"]["best_restart"]["initialization"]["kind"] == "perturbed_true_tree"
    assert artifact["metrics"]["verifier_status"] == "recovered"


def test_perturbed_tree_repair_promotes_artifact_without_overwriting_raw(monkeypatch, tmp_path):
    target_expr = Eml(Eml(Var("x"), Const(1.0)), Const(1.0))
    raw_fit = _fit_from_slots({"root.left": "var:x", "root.right": "const:1"})
    embedding = SoftEMLTree(2, ("x",), (1.0,)).embed_expr(target_expr)
    raw_verification = _verification_report("failed")

    def fake_fit_perturbed_true_tree(*args, **kwargs):
        return BasinTrainingResult(
            status="snapped_but_failed",
            return_kind="snapped_but_failed",
            fit=raw_fit,
            embedding=embedding,
            verification=raw_verification,
            manifest={
                "schema": "eml.perturbed_true_tree_manifest.v1",
                "status": "snapped_but_failed",
                "raw_status": "snapped_but_failed",
                "return_kind": "snapped_but_failed",
                "optimizer": raw_fit.manifest,
                "verification": raw_verification.as_dict(),
            },
        )

    monkeypatch.setattr(benchmark_module, "fit_perturbed_true_tree", fake_fit_perturbed_true_tree)
    run = BenchmarkRun(
        suite_id="proof-perturbed-basin",
        case_id="basin-depth2-perturbed",
        formula="basin_depth2_exp_exp",
        start_mode="perturbed_tree",
        seed=0,
        perturbation_noise=0.05,
        dataset=DatasetConfig(points=12),
        optimizer=OptimizerBudget(depth=2, warm_steps=1, warm_restarts=1),
        artifact_path=tmp_path / "repaired-perturbed.json",
        claim_id="paper-perturbed-true-tree-basin",
        threshold_policy_id="bounded_100_percent",
        training_mode="perturbed_true_tree_training",
    )

    result = execute_benchmark_run(run)
    artifact = json.loads(result.artifact_path.read_text(encoding="utf-8"))

    assert result.status == "repaired_candidate"
    assert artifact["status"] == "repaired_candidate"
    assert artifact["claim_status"] == "recovered"
    assert artifact["return_kind"] == "snapped_but_failed"
    assert artifact["raw_status"] == "snapped_but_failed"
    assert artifact["repair_status"] == "repaired"
    assert artifact["evidence_class"] == "repaired_candidate"
    assert artifact["perturbed_true_tree"]["status"] == "snapped_but_failed"
    assert artifact["stage_statuses"]["perturbed_true_tree_attempt"] == "snapped_but_failed"
    assert artifact["stage_statuses"]["local_repair"] == "repaired_candidate"
    assert artifact["repair"]["status"] == "repaired_candidate"
    assert artifact["repair"]["verification"]["status"] == "recovered"
    assert artifact["repair"]["accepted_moves"][0]["source"] == "embedded_target_slot"
    assert artifact["metrics"]["repair_status"] == "repaired"
    assert artifact["metrics"]["repair_move_count"] >= 1
    assert artifact["metrics"]["repair_accepted_move_count"] >= 1
    assert artifact["metrics"]["repair_verifier_status"] == "recovered"


def test_cli_benchmark_writes_suite_result(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "eml_symbolic_regression.cli",
            "benchmark",
            "smoke",
            "--case",
            "planck-diagnostic",
            "--output-dir",
            str(tmp_path),
        ],
        check=True,
        capture_output=True,
        env=CLI_ENV,
        text=True,
    )

    assert "smoke: 1 runs" in result.stdout
    suite_result = tmp_path / "smoke" / "suite-result.json"
    payload = json.loads(suite_result.read_text())
    assert payload["counts"]["total"] == 1
    assert payload["results"][0]["status"] == "unsupported"


def test_cli_list_claims_prints_claim_matrix():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "eml_symbolic_regression.cli",
            "list-claims",
        ],
        check=True,
        capture_output=True,
        env=CLI_ENV,
        text=True,
    )

    lines = result.stdout.strip().splitlines()
    assert lines == sorted(lines)
    assert any(
        line.startswith("paper-shallow-blind-recovery: measured_training_boundary threshold=measured_pure_blind_recovery suites=")
        for line in lines
    )
    assert any(
        line.startswith(
            "paper-shallow-scaffolded-recovery: scaffolded_training_proof threshold=scaffolded_bounded_100_percent suites="
        )
        for line in lines
    )
    assert any(line.endswith("suites=proof-depth-curve") for line in lines)


def test_cli_proof_dataset_writes_manifest_without_raw_arrays(tmp_path):
    output = tmp_path / "exp-proof-manifest.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "eml_symbolic_regression.cli",
            "proof-dataset",
            "exp",
            "--points",
            "12",
            "--seed",
            "7",
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        env=CLI_ENV,
        text=True,
    )

    assert f"exp: dataset manifest -> {output}" in result.stdout
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["schema"] == "eml.proof_dataset_manifest.v1"
    assert payload["formula_id"] == "exp"
    assert payload["seed"] == 7
    assert payload["splits"][0]["name"] == "train"
    assert payload["splits"][0]["count"] == 12
    assert payload["provenance"]["symbolic_expression"] == "exp(x)"
    assert payload["manifest_sha256"]
    encoded = json.dumps(payload)
    assert '"inputs"' not in encoded
    assert '"target"' not in encoded
    assert '"values"' not in encoded


@pytest.mark.parametrize(
    ("extra_args", "message"),
    [
        (["--points", "0"], "points must be positive"),
        (["--tolerance=-1e-8"], "tolerance must be positive"),
    ],
)
def test_cli_proof_dataset_rejects_invalid_sampling_contracts(tmp_path, extra_args, message):
    output = tmp_path / "bad-proof-manifest.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "eml_symbolic_regression.cli",
            "proof-dataset",
            "exp",
            "--output",
            str(output),
            *extra_args,
        ],
        check=False,
        capture_output=True,
        env=CLI_ENV,
        text=True,
    )

    assert result.returncode != 0
    assert message in result.stderr
    assert not output.exists()


def test_cli_campaign_writes_report(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "eml_symbolic_regression.cli",
            "campaign",
            "smoke",
            "--case",
            "planck-diagnostic",
            "--output-root",
            str(tmp_path),
            "--label",
            "cli-smoke",
        ],
        check=True,
        capture_output=True,
        env=CLI_ENV,
        text=True,
    )

    assert "report ->" in result.stdout
    report = tmp_path / "cli-smoke" / "report.md"
    manifest = tmp_path / "cli-smoke" / "campaign-manifest.json"
    assert report.exists()
    assert manifest.exists()
    assert "## Headline Metrics" in report.read_text(encoding="utf-8")


def test_for_demo_diagnostic_subset_preserves_unsupported_formula(tmp_path):
    base = builtin_suite("for-demo-diagnostics")
    suite = type(base)(base.id, base.description, base.cases, tmp_path / "artifacts")

    result = run_benchmark_suite(suite, run_filter=RunFilter(case_ids=("damped-oscillator-compile",)))

    assert len(result.results) == 1
    assert result.results[0].status == "unsupported"
    assert result.results[0].payload["compiled_eml"]["reason"] == "unsupported_operator"
    assert result.results[0].payload["compiled_eml"]["diagnostic"]["strict"]["reason"] == "unsupported_operator"


def test_shockley_compile_moves_to_verified_compiled_ast(tmp_path):
    base = builtin_suite("v1.3-standard")
    suite = type(base)(base.id, base.description, base.cases, tmp_path / "artifacts")

    result = run_benchmark_suite(suite, run_filter=RunFilter(case_ids=("shockley-compile",)))

    assert len(result.results) == 1
    assert result.results[0].status == "recovered"
    assert result.results[0].payload["evidence_class"] == "compile_only_verified"
    compiled = result.results[0].payload["compiled_eml"]
    assert compiled["metadata"]["depth"] <= 13
    assert any(entry["rule"] == "scaled_exp_minus_one_template" for entry in compiled["metadata"]["trace"])
