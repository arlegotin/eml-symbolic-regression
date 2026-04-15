import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

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


ROOT = Path(__file__).resolve().parents[1]
CLI_ENV = {**os.environ, "PYTHONPATH": str(ROOT / "src")}


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
            "claim_id": "paper-shallow-blind-recovery",
            "threshold_policy_id": "bounded_100_percent",
            "training_mode": "blind_training",
        },
        path="cases[0]",
    )
    suite = BenchmarkSuite("v1.5-shallow-proof", "cheap proof-aware runner smoke", (case,), tmp_path / "artifacts")

    result = run_benchmark_suite(suite)
    artifact = json.loads(result.results[0].artifact_path.read_text(encoding="utf-8"))

    assert artifact["claim_id"] == "paper-shallow-blind-recovery"
    assert artifact["claim_class"] == "bounded_training_proof"
    assert artifact["training_mode"] == "blind_training"
    assert artifact["threshold"]["id"] == "bounded_100_percent"
    assert artifact["dataset_manifest"]["schema"] == "eml.proof_dataset_manifest.v1"
    assert artifact["dataset_manifest"]["formula_id"] == "exp"
    assert artifact["dataset_manifest"]["points"] == 12
    assert artifact["budget"]["depth"] == 1
    assert artifact["provenance"]["symbolic_expression"] == "exp(x)"
    assert artifact["provenance"]["source_document"] == "sources/paper.pdf"
    assert artifact["evidence_class"] == evidence_class_for_payload(artifact)


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
                "status": "same_ast_return",
                "claim_status": "same_ast_return",
                "training_mode": "compiler_warm_start_training",
                "run": {"start_mode": "warm_start"},
            }
        )
        == "same_ast"
    )


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
        line.startswith("paper-shallow-blind-recovery: bounded_training_proof threshold=bounded_100_percent suites=")
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
