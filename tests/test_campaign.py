import csv
import json

import pytest

from eml_symbolic_regression.benchmark import RunFilter, load_suite
from eml_symbolic_regression.campaign import (
    CampaignOutputExistsError,
    campaign_preset,
    list_campaign_presets,
    run_campaign,
)


def test_campaign_presets_map_to_budgeted_suites():
    assert list_campaign_presets() == ("smoke", "standard", "showcase", "proof-shallow")

    standard = campaign_preset("standard")
    suite = load_suite(standard.suite)
    runs = suite.expanded_runs()

    assert standard.tier == "showcase-default"
    assert {run.start_mode for run in runs} >= {"blind", "warm_start", "compile"}
    assert any(run.case_id == "beer-perturbation-sweep" for run in runs)
    assert any(run.formula == "michaelis_menten" for run in runs)
    assert any(run.formula == "planck" for run in runs)
    assert {"radioactive_decay", "logistic", "shockley"} <= {run.formula for run in runs}

    proof = campaign_preset("proof-shallow")
    assert proof.suite == "v1.5-shallow-proof"
    assert any(run.claim_id == "paper-shallow-blind-recovery" for run in load_suite(proof.suite).expanded_runs())


def test_campaign_writes_manifest_suite_result_and_aggregate(tmp_path):
    result = run_campaign(
        "smoke",
        output_root=tmp_path,
        label="ci-smoke",
        run_filter=RunFilter(case_ids=("planck-diagnostic",)),
    )

    assert result.campaign_dir == tmp_path / "ci-smoke"
    assert result.manifest_path.exists()
    assert result.suite_result_path.exists()
    assert result.aggregate_paths["json"].exists()
    assert result.aggregate_paths["markdown"].exists()

    manifest = json.loads(result.manifest_path.read_text())
    assert manifest["schema"] == "eml.campaign_manifest.v1"
    assert manifest["preset"]["name"] == "smoke"
    assert manifest["suite"]["id"] == "smoke"
    assert manifest["counts"]["total"] == 1
    assert manifest["run_filter"]["case_ids"] == ["planck-diagnostic"]
    assert "campaign smoke" in manifest["reproducibility"]["command"]


def test_campaign_refuses_silent_overwrite(tmp_path):
    run_campaign(
        "smoke",
        output_root=tmp_path,
        label="existing",
        run_filter=RunFilter(case_ids=("planck-diagnostic",)),
    )

    with pytest.raises(CampaignOutputExistsError):
        run_campaign(
            "smoke",
            output_root=tmp_path,
            label="existing",
            run_filter=RunFilter(case_ids=("planck-diagnostic",)),
        )

    replacement = run_campaign(
        "smoke",
        output_root=tmp_path,
        label="existing",
        overwrite=True,
        run_filter=RunFilter(case_ids=("planck-diagnostic",)),
    )

    assert replacement.manifest_path.exists()


def test_campaign_writes_tidy_csvs_and_headline_metrics(tmp_path):
    result = run_campaign(
        "smoke",
        output_root=tmp_path,
        label="csv-smoke",
        run_filter=RunFilter(case_ids=("beer-warm", "planck-diagnostic")),
    )

    assert result.table_paths["runs_csv"].exists()
    assert result.table_paths["group_formula_csv"].exists()
    assert result.table_paths["group_start_mode_csv"].exists()
    assert result.table_paths["group_perturbation_noise_csv"].exists()
    assert result.table_paths["group_depth_csv"].exists()
    assert result.table_paths["group_failure_class_csv"].exists()
    assert result.table_paths["headline_json"].exists()
    assert result.table_paths["headline_csv"].exists()
    assert result.table_paths["failures_csv"].exists()

    run_rows = list(csv.DictReader(result.table_paths["runs_csv"].open(encoding="utf-8")))
    assert len(run_rows) == 2
    assert {
        "formula",
        "start_mode",
        "seed",
        "depth",
        "steps",
        "perturbation_noise",
        "best_loss",
        "post_snap_loss",
        "verifier_status",
        "recovery_class",
        "runtime_seconds",
        "changed_slot_count",
        "warm_start_mechanism",
        "artifact_path",
    } <= set(run_rows[0])
    assert {
        "claim_id",
        "claim_class",
        "training_mode",
        "evidence_class",
        "threshold_policy",
        "dataset_manifest_sha256",
        "provenance_source",
        "provenance_expression",
    } <= set(run_rows[0])
    assert "threshold_status" not in set(run_rows[0])
    assert run_rows[0]["training_mode"]
    assert run_rows[0]["claim_id"] == ""

    headline = json.loads(result.table_paths["headline_json"].read_text())
    assert headline["total_runs"] == 2
    assert headline["verifier_recovered"] == 1
    assert headline["unsupported"] == 1
    assert headline["same_ast_return"] == 1

    failures = list(csv.DictReader(result.table_paths["failures_csv"].open(encoding="utf-8")))
    assert len(failures) == 1
    assert failures[0]["classification"] == "unsupported"
    assert failures[0]["reason"]


def test_proof_campaign_tables_and_manifest_preserve_claim_metadata(tmp_path):
    result = run_campaign(
        "proof-shallow",
        output_root=tmp_path,
        label="proof-exp",
        run_filter=RunFilter(case_ids=("shallow-exp-blind",), seeds=(0,)),
    )

    assert result.table_paths["group_evidence_class_csv"].exists()
    assert result.table_paths["group_claim_csv"].exists()
    assert result.table_paths["group_threshold_policy_csv"].exists()

    run_rows = list(csv.DictReader(result.table_paths["runs_csv"].open(encoding="utf-8")))
    assert len(run_rows) == 1
    row = run_rows[0]
    assert row["claim_id"] == "paper-shallow-blind-recovery"
    assert row["claim_class"] == "bounded_training_proof"
    assert row["training_mode"] == "blind_training"
    assert row["evidence_class"]
    assert row["threshold_policy"] == "bounded_100_percent"
    assert row["dataset_manifest_sha256"]
    assert row["provenance_source"] == "sources/paper.pdf"
    assert row["provenance_expression"] == "exp(x)"
    assert "threshold_status" not in row

    claim_groups = list(csv.DictReader(result.table_paths["group_claim_csv"].open(encoding="utf-8")))
    assert claim_groups[0]["group"] == "paper-shallow-blind-recovery"

    manifest = json.loads(result.manifest_path.read_text())
    assert manifest["counts"]["evidence_classes"]
    assert manifest["thresholds"]
    threshold = manifest["thresholds"][0]
    assert threshold["claim_id"] == "paper-shallow-blind-recovery"
    assert threshold["threshold_policy_id"] == "bounded_100_percent"
    assert threshold["status"] in {"passed", "failed"}
    assert {"claim_id", "threshold_policy_id", "status", "passed", "eligible", "rate"} <= set(threshold)
    assert manifest["output"]["tables"]["group_evidence_class_csv"].endswith("group-evidence-class.csv")
    assert manifest["output"]["tables"]["group_claim_csv"].endswith("group-claim.csv")
    assert manifest["output"]["tables"]["group_threshold_policy_csv"].endswith("group-threshold-policy.csv")


def test_campaign_writes_stable_svg_figures(tmp_path):
    result = run_campaign("smoke", output_root=tmp_path, label="figures-smoke")

    assert {
        "recovery_by_formula",
        "recovery_by_start_mode",
        "loss_before_after_snap",
        "beer_perturbation",
        "runtime_depth_budget",
        "failure_taxonomy",
    } <= set(result.figure_paths)

    for path in result.figure_paths.values():
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert text.startswith("<svg ")
        assert "</svg>" in text

    assert result.figure_paths["recovery_by_formula"].name == "recovery-by-formula.svg"
    assert "-log10(loss)" in result.figure_paths["loss_before_after_snap"].read_text(encoding="utf-8")

    manifest = json.loads(result.manifest_path.read_text())
    assert "figures" in manifest["output"]
    assert manifest["output"]["figures"]["failure_taxonomy"].endswith("failure-taxonomy.svg")


def test_campaign_writes_self_contained_report(tmp_path):
    result = run_campaign(
        "smoke",
        output_root=tmp_path,
        label="report-smoke",
        run_filter=RunFilter(case_ids=("beer-warm", "planck-diagnostic")),
    )

    assert result.report_path is not None
    assert result.report_path.exists()
    report = result.report_path.read_text(encoding="utf-8")

    assert "# EML Benchmark Campaign Report: smoke" in report
    assert "## Headline Metrics" in report
    assert "## What EML Demonstrates Well" in report
    assert "## Limitations" in report
    assert "## Next Experiments" in report
    assert "campaign smoke --output-root" in report
    assert "figures/recovery-by-formula.svg" in report
    assert "tables/runs.csv" in report
    assert "unsupported" in report

    manifest = json.loads(result.manifest_path.read_text())
    assert manifest["output"]["report_markdown"].endswith("report.md")
