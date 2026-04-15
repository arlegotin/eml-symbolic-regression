import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from eml_symbolic_regression.benchmark import (
    BenchmarkCase,
    BenchmarkRun,
    BenchmarkRunResult,
    BenchmarkSuite,
    DatasetConfig,
    OptimizerBudget,
    RunFilter,
    aggregate_evidence,
    builtin_suite,
    render_aggregate_markdown,
    run_benchmark_suite,
    write_aggregate_reports,
)


def _synthetic_result(
    *,
    case_id: str,
    start_mode: str,
    training_mode: str,
    evidence_class: str,
    status: str = "recovered",
    claim_status: str = "recovered",
    perturbation_noise: float = 0.0,
    return_kind: str | None = None,
    raw_status: str | None = None,
    repair_status: str | None = None,
    claim_id: str | None = "paper-shallow-blind-recovery",
    claim_class: str | None = "bounded_training_proof",
    threshold_policy_id: str | None = "bounded_100_percent",
) -> BenchmarkRunResult:
    run = BenchmarkRun(
        suite_id="synthetic-proof",
        case_id=case_id,
        formula="exp",
        start_mode=start_mode,
        seed=0,
        perturbation_noise=perturbation_noise,
        dataset=DatasetConfig(points=12),
        optimizer=OptimizerBudget(depth=1, steps=1, restarts=1),
        artifact_path=Path(f"/tmp/{case_id}.json"),
        claim_id=claim_id,
        threshold_policy_id=threshold_policy_id,
        training_mode=training_mode,
    )
    payload = {
        "run": run.as_dict(),
        "status": status,
        "claim_status": claim_status,
        "claim_id": claim_id,
        "claim_class": claim_class,
        "training_mode": training_mode,
        "evidence_class": evidence_class,
        "return_kind": return_kind,
        "raw_status": raw_status,
        "repair_status": repair_status,
        "threshold": {"id": threshold_policy_id} if threshold_policy_id is not None else None,
        "dataset": run.dataset.as_dict(),
        "dataset_manifest": {"schema": "eml.proof_dataset_manifest.v1"},
        "provenance": {"symbolic_expression": "exp(x)"},
        "metrics": {},
        "stage_statuses": {},
    }
    return BenchmarkRunResult(run, status, run.artifact_path, payload)


def test_aggregate_evidence_separates_unsupported_and_same_ast(tmp_path):
    base = builtin_suite("smoke")
    suite = type(base)(base.id, base.description, base.cases, tmp_path / "artifacts")

    result = run_benchmark_suite(suite, run_filter=RunFilter(case_ids=("beer-warm", "planck-diagnostic")))
    aggregate = aggregate_evidence(result)

    assert aggregate["schema"] == "eml.benchmark_aggregate.v1"
    assert aggregate["counts"]["total"] == 2
    assert aggregate["counts"]["unsupported"] == 1
    assert aggregate["counts"]["same_ast_return"] == 1
    assert aggregate["counts"]["verifier_recovered"] == 1
    assert aggregate["counts"]["evidence_classes"]["same_ast"] == 1
    assert aggregate["counts"]["evidence_classes"]["unsupported"] == 1
    assert {group["key"] for group in aggregate["groups"]["evidence_class"]} == {"same_ast", "unsupported"}
    assert {run["classification"] for run in aggregate["runs"]} == {"same_ast_warm_start_return", "unsupported"}


def test_warm_start_depth_gate_overrides_compiled_seed_claim_status(tmp_path):
    case = BenchmarkCase.from_mapping(
        {
            "id": "beer-warm-depth-gated",
            "formula": "beer_lambert",
            "start_mode": "warm_start",
            "seeds": [0],
            "perturbation_noise": [0.0],
            "dataset": {"points": 12},
            "optimizer": {
                "warm_steps": 1,
                "warm_restarts": 1,
                "max_warm_depth": 1,
            },
        },
        path="cases[0]",
    )
    suite = BenchmarkSuite("warm-depth-gate", "depth-gated warm-start regression", (case,), tmp_path / "artifacts")

    result = run_benchmark_suite(suite)
    aggregate = aggregate_evidence(result)
    artifact = json.loads(result.results[0].artifact_path.read_text(encoding="utf-8"))

    assert result.results[0].status == "unsupported"
    assert artifact["claim_status"] == "unsupported"
    assert artifact["warm_start_eml"]["reason"] == "depth_too_large_for_warm_start"
    assert aggregate["counts"]["verifier_recovered"] == 0
    assert aggregate["counts"]["unsupported"] == 1
    assert aggregate["runs"][0]["claim_status"] == "unsupported"


def test_shallow_bounded_threshold_counts_only_blind_training_recovery():
    suite = BenchmarkSuite("synthetic-proof", "synthetic proof aggregate", ())
    result = SimpleNamespace(
        suite=suite,
        results=(
            _synthetic_result(case_id="blind", start_mode="blind", training_mode="blind_training", evidence_class="blind_training_recovered"),
            _synthetic_result(
                case_id="scaffolded-blind",
                start_mode="blind",
                training_mode="blind_training",
                evidence_class="scaffolded_blind_training_recovered",
            ),
            _synthetic_result(case_id="compile", start_mode="compile", training_mode="compile_only_verification", evidence_class="compile_only_verified"),
            _synthetic_result(case_id="catalog", start_mode="catalog", training_mode="catalog_verification", evidence_class="catalog_verified"),
            _synthetic_result(
                case_id="warm",
                start_mode="warm_start",
                training_mode="compiler_warm_start_training",
                evidence_class="compiler_warm_start_recovered",
            ),
            _synthetic_result(
                case_id="repair",
                start_mode="blind",
                training_mode="blind_training",
                evidence_class="repaired_candidate",
                status="repaired_candidate",
                claim_status="failed",
            ),
            _synthetic_result(
                case_id="verified-equivalent",
                start_mode="warm_start",
                training_mode="compiler_warm_start_training",
                evidence_class="verified_equivalent",
                status="verified_equivalent_ast",
                claim_status="verified_equivalent_ast",
            ),
            _synthetic_result(
                case_id="same-ast",
                start_mode="warm_start",
                training_mode="compiler_warm_start_training",
                evidence_class="same_ast",
                status="same_ast_return",
                claim_status="same_ast_return",
            ),
            _synthetic_result(
                case_id="soft-fit",
                start_mode="blind",
                training_mode="blind_training",
                evidence_class="soft_fit_only",
                status="soft_fit_only",
                claim_status="failed",
            ),
        ),
    )

    aggregate = aggregate_evidence(result)
    threshold = aggregate["thresholds"][0]

    assert aggregate["counts"]["evidence_classes"] == {
        "blind_training_recovered": 1,
        "catalog_verified": 1,
        "compile_only_verified": 1,
        "compiler_warm_start_recovered": 1,
        "repaired_candidate": 1,
        "same_ast": 1,
        "scaffolded_blind_training_recovered": 1,
        "soft_fit_only": 1,
        "verified_equivalent": 1,
    }
    assert threshold["claim_id"] == "paper-shallow-blind-recovery"
    assert threshold["threshold_policy_id"] == "bounded_100_percent"
    assert threshold["eligible"] == 9
    assert threshold["passed"] == 1
    assert threshold["failed"] == 8
    assert threshold["rate"] == pytest.approx(1.0 / 9.0)
    assert threshold["required_rate"] == 1.0
    assert threshold["status"] == "failed"
    assert threshold["evidence_classes"] == aggregate["counts"]["evidence_classes"]


def test_perturbed_bounded_threshold_counts_repaired_candidates():
    suite = BenchmarkSuite("synthetic-perturbed-proof", "synthetic perturbed proof aggregate", ())
    result = SimpleNamespace(
        suite=suite,
        results=(
            _synthetic_result(
                case_id="raw",
                start_mode="perturbed_tree",
                training_mode="perturbed_true_tree_training",
                evidence_class="perturbed_true_tree_recovered",
                perturbation_noise=0.05,
                return_kind="same_ast_return",
                raw_status="recovered",
                claim_id="paper-perturbed-true-tree-basin",
                threshold_policy_id="bounded_100_percent",
            ),
            _synthetic_result(
                case_id="repair",
                start_mode="perturbed_tree",
                training_mode="perturbed_true_tree_training",
                evidence_class="repaired_candidate",
                status="repaired_candidate",
                claim_status="recovered",
                perturbation_noise=0.05,
                return_kind="snapped_but_failed",
                raw_status="snapped_but_failed",
                repair_status="repaired",
                claim_id="paper-perturbed-true-tree-basin",
                threshold_policy_id="bounded_100_percent",
            ),
            _synthetic_result(
                case_id="failed",
                start_mode="perturbed_tree",
                training_mode="perturbed_true_tree_training",
                evidence_class="snapped_but_failed",
                status="snapped_but_failed",
                claim_status="failed",
                perturbation_noise=0.05,
                return_kind="snapped_but_failed",
                raw_status="snapped_but_failed",
                repair_status="not_repaired",
                claim_id="paper-perturbed-true-tree-basin",
                threshold_policy_id="bounded_100_percent",
            ),
        ),
    )

    threshold = aggregate_evidence(result)["thresholds"][0]

    assert threshold["claim_id"] == "paper-perturbed-true-tree-basin"
    assert threshold["eligible"] == 3
    assert threshold["passed"] == 2
    assert threshold["failed"] == 1
    assert threshold["status"] == "failed"
    assert threshold["evidence_classes"] == {
        "perturbed_true_tree_recovered": 1,
        "repaired_candidate": 1,
        "snapped_but_failed": 1,
    }


def test_aggregate_evidence_keeps_perturbed_raw_and_repair_taxonomy_distinct():
    suite = BenchmarkSuite("synthetic-perturbed-taxonomy", "synthetic taxonomy aggregate", ())
    common = {
        "start_mode": "perturbed_tree",
        "training_mode": "perturbed_true_tree_training",
        "claim_id": None,
        "claim_class": None,
        "threshold_policy_id": None,
        "perturbation_noise": 0.05,
    }
    result = SimpleNamespace(
        suite=suite,
        results=(
            _synthetic_result(
                case_id="same-ast",
                evidence_class="perturbed_true_tree_recovered",
                return_kind="same_ast_return",
                raw_status="recovered",
                **common,
            ),
            _synthetic_result(
                case_id="verified-equivalent",
                evidence_class="perturbed_true_tree_recovered",
                return_kind="verified_equivalent_ast",
                raw_status="recovered",
                **common,
            ),
            _synthetic_result(
                case_id="repair",
                evidence_class="repaired_candidate",
                status="repaired_candidate",
                claim_status="recovered",
                return_kind="snapped_but_failed",
                raw_status="snapped_but_failed",
                repair_status="repaired",
                **common,
            ),
            _synthetic_result(
                case_id="snapped",
                evidence_class="perturbed_true_tree_recovered",
                status="snapped_but_failed",
                claim_status="failed",
                return_kind="snapped_but_failed",
                raw_status="snapped_but_failed",
                repair_status="not_repaired",
                **common,
            ),
            _synthetic_result(
                case_id="soft-fit",
                evidence_class="perturbed_true_tree_recovered",
                status="soft_fit_only",
                claim_status="failed",
                return_kind="soft_fit_only",
                raw_status="soft_fit_only",
                repair_status="not_repaired",
                **common,
            ),
            _synthetic_result(
                case_id="unsupported",
                evidence_class="unsupported",
                status="unsupported",
                claim_status="unsupported",
                raw_status="unsupported",
                **common,
            ),
            _synthetic_result(
                case_id="execution-error",
                evidence_class="execution_failure",
                status="execution_error",
                claim_status="execution_error",
                raw_status="execution_error",
                **common,
            ),
        ),
    )

    aggregate = aggregate_evidence(result)
    markdown = render_aggregate_markdown(aggregate)
    classifications = {run["case_id"]: run["classification"] for run in aggregate["runs"]}

    assert classifications == {
        "same-ast": "same_ast_return",
        "verified-equivalent": "verified_equivalent_ast",
        "repair": "repaired_candidate",
        "snapped": "snapped_but_failed",
        "soft-fit": "soft_fit_only",
        "unsupported": "unsupported",
        "execution-error": "execution_failure",
    }
    assert aggregate["counts"]["same_ast_return"] == 1
    assert aggregate["counts"]["verified_equivalent_ast"] == 1
    assert aggregate["counts"]["repaired_candidate"] == 1
    assert {group["key"] for group in aggregate["groups"]["return_kind"]} >= {
        "same_ast_return",
        "verified_equivalent_ast",
        "snapped_but_failed",
        "soft_fit_only",
    }
    assert {group["key"] for group in aggregate["groups"]["raw_status"]} >= {
        "recovered",
        "snapped_but_failed",
        "soft_fit_only",
        "unsupported",
        "execution_error",
    }
    assert {group["key"] for group in aggregate["groups"]["repair_status"]} >= {"repaired", "not_repaired", "none"}
    assert "## By Return Kind" in markdown
    assert "## By Raw Status" in markdown
    assert "## By Repair Status" in markdown


def test_measured_depth_curve_threshold_is_reported_not_failed():
    suite = BenchmarkSuite("synthetic-depth", "synthetic depth aggregate", ())
    result = SimpleNamespace(
        suite=suite,
        results=(
            _synthetic_result(
                case_id="depth-6-blind",
                start_mode="blind",
                training_mode="blind_training",
                evidence_class="failed",
                status="failed",
                claim_status="failed",
                claim_id="paper-blind-depth-degradation",
                claim_class="measured_depth_curve",
                threshold_policy_id="measured_depth_curve",
            ),
        ),
    )

    aggregate = aggregate_evidence(result)
    threshold = aggregate["thresholds"][0]

    assert threshold["claim_id"] == "paper-blind-depth-degradation"
    assert threshold["threshold_policy_id"] == "measured_depth_curve"
    assert threshold["eligible"] == 1
    assert threshold["passed"] == 1
    assert threshold["rate"] == 1.0
    assert threshold["required_rate"] is None
    assert threshold["status"] == "reported"


def test_write_aggregate_reports_outputs_json_and_markdown(tmp_path):
    base = builtin_suite("smoke")
    suite = type(base)(base.id, base.description, base.cases, tmp_path / "artifacts")
    result = run_benchmark_suite(suite, run_filter=RunFilter(case_ids=("planck-diagnostic",)))

    paths = write_aggregate_reports(result)

    assert paths["json"].exists()
    assert paths["markdown"].exists()
    markdown = paths["markdown"].read_text()
    assert "# Benchmark Evidence: smoke" in markdown
    assert "## By Evidence Class" in markdown
    assert "## Thresholds" in markdown
    assert "| planck |" in markdown


def test_markdown_report_contains_run_artifact_paths(tmp_path):
    base = builtin_suite("smoke")
    suite = type(base)(base.id, base.description, base.cases, tmp_path / "artifacts")
    result = run_benchmark_suite(suite, run_filter=RunFilter(case_ids=("planck-diagnostic",)))

    markdown = render_aggregate_markdown(aggregate_evidence(result))

    assert "planck-diagnostic" in markdown
    assert ".json" in markdown


def test_smoke_benchmark_exercises_required_paths_and_aggregate(tmp_path):
    base = builtin_suite("smoke")
    suite = type(base)(base.id, base.description, base.cases, tmp_path / "artifacts")

    result = run_benchmark_suite(suite)
    paths = write_aggregate_reports(result)
    aggregate = aggregate_evidence(result)

    assert {run.start_mode for run in (item.run for item in result.results)} == {"blind", "warm_start", "compile"}
    assert {"recovered", "snapped_but_failed", "same_ast_return", "unsupported"} >= {item.status for item in result.results}
    assert aggregate["counts"]["total"] == 3
    assert aggregate["counts"]["verifier_recovered"] == 2
    assert aggregate["counts"]["unsupported"] == 1
    assert aggregate["counts"]["same_ast_return"] == 1
    assert aggregate["counts"]["failed"] == 0
    assert paths["json"].exists()
    assert paths["markdown"].exists()
