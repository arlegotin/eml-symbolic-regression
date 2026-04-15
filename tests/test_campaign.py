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
    assert list_campaign_presets() == ("smoke", "standard", "showcase")

    standard = campaign_preset("standard")
    suite = load_suite(standard.suite)
    runs = suite.expanded_runs()

    assert standard.tier == "showcase-default"
    assert {run.start_mode for run in runs} >= {"blind", "warm_start", "compile"}
    assert any(run.case_id == "beer-perturbation-sweep" for run in runs)
    assert any(run.formula == "michaelis_menten" for run in runs)
    assert any(run.formula == "planck" for run in runs)
    assert {"radioactive_decay", "logistic", "shockley"} <= {run.formula for run in runs}


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
        "artifact_path",
    } <= set(run_rows[0])

    headline = json.loads(result.table_paths["headline_json"].read_text())
    assert headline["total_runs"] == 2
    assert headline["verifier_recovered"] == 1
    assert headline["unsupported"] == 1
    assert headline["same_ast_return"] == 1

    failures = list(csv.DictReader(result.table_paths["failures_csv"].open(encoding="utf-8")))
    assert len(failures) == 1
    assert failures[0]["classification"] == "unsupported"
    assert failures[0]["reason"]


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
