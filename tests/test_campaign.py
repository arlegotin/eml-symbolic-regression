import csv
import json
import shlex

import pytest

from eml_symbolic_regression.benchmark import RunFilter, load_suite
from eml_symbolic_regression.campaign import (
    CampaignOutputExistsError,
    _reproduction_command,
    campaign_preset,
    list_campaign_presets,
    run_campaign,
    write_campaign_report,
    write_campaign_tables,
)


def _proof_basin_run(
    *,
    run_id: str = "basin-beer-lambert-bound-seed0-noise5",
    suite_id: str = "proof-perturbed-basin",
    case_id: str = "basin-beer-lambert-bound",
    evidence_class: str = "perturbed_true_tree_recovered",
    classification: str = "same_ast_return",
    status: str = "recovered",
    claim_status: str = "recovered",
    return_kind: str = "same_ast_return",
    raw_status: str = "recovered",
    repair_status: str = "not_attempted",
    perturbation_noise: float = 5.0,
) -> dict:
    return {
        "run_id": run_id,
        "artifact_path": f"artifacts/benchmarks/{suite_id}/{run_id}.json",
        "suite_id": suite_id,
        "case_id": case_id,
        "formula": "beer_lambert",
        "start_mode": "perturbed_tree",
        "seed": 0,
        "perturbation_noise": perturbation_noise,
        "optimizer": {"depth": 9, "steps": 20, "warm_depth": 9, "warm_steps": 40, "restarts": 1, "warm_restarts": 1},
        "dataset": {"points": 12},
        "claim_id": "paper-perturbed-true-tree-basin" if suite_id == "proof-perturbed-basin" else None,
        "claim_class": "bounded_training_proof" if suite_id == "proof-perturbed-basin" else None,
        "training_mode": "perturbed_true_tree_training",
        "threshold_policy_id": "bounded_100_percent" if suite_id == "proof-perturbed-basin" else None,
        "threshold": {"id": "bounded_100_percent"} if suite_id == "proof-perturbed-basin" else None,
        "status": status,
        "claim_status": claim_status,
        "classification": classification,
        "evidence_class": evidence_class,
        "return_kind": return_kind,
        "raw_status": raw_status,
        "repair_status": repair_status,
        "reason": "verified" if claim_status == "recovered" else "verifier_mismatch",
        "metrics": {
            "best_loss": 0.01,
            "post_snap_loss": 0.02,
            "snap_min_margin": 0.7,
            "verifier_status": "recovered" if claim_status == "recovered" else "failed",
            "changed_slot_count": 2,
            "repair_status": repair_status,
            "repair_verifier_status": "recovered" if repair_status == "repaired" else None,
            "repair_accepted_move_count": 1 if repair_status == "repaired" else 0,
        },
        "stage_statuses": {"perturbed_true_tree_attempt": raw_status},
    }


def test_campaign_presets_map_to_budgeted_suites():
    assert list_campaign_presets() == (
        "smoke",
        "standard",
        "showcase",
        "proof-shallow",
        "proof-shallow-pure-blind",
        "proof-basin",
        "proof-basin-probes",
        "proof-depth-curve",
    )

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
    assert any(run.claim_id == "paper-shallow-scaffolded-recovery" for run in load_suite(proof.suite).expanded_runs())

    pure_blind = campaign_preset("proof-shallow-pure-blind")
    assert pure_blind.suite == "v1.5-shallow-pure-blind"
    assert any(run.claim_id == "paper-shallow-blind-recovery" for run in load_suite(pure_blind.suite).expanded_runs())

    proof_basin = campaign_preset("proof-basin")
    assert proof_basin.benchmark_suite == "proof-perturbed-basin"
    assert proof_basin.budget_guardrail == "CI-scale perturbed basin proof suite; high-noise probes are reported separately"
    assert any(run.case_id == "basin-beer-lambert-bound" for run in load_suite(proof_basin.suite).expanded_runs())

    proof_basin_probes = campaign_preset("proof-basin-probes")
    assert proof_basin_probes.suite == "proof-perturbed-basin-beer-probes"
    assert any(run.case_id == "basin-beer-lambert-bound-probes" for run in load_suite(proof_basin_probes.suite).expanded_runs())

    depth_curve = campaign_preset("proof-depth-curve")
    assert depth_curve.suite == "proof-depth-curve"
    assert any(run.case_id == "depth-6-perturbed" for run in load_suite(depth_curve.suite).expanded_runs())


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


def test_reproduction_command_quotes_shell_sensitive_values(tmp_path):
    output_root = tmp_path / "campaign root"
    command = _reproduction_command(
        "smoke",
        output_root,
        "ok; echo injected",
        True,
        {
            "formulas": ["exp", "log; rm -rf /"],
            "start_modes": ["blind"],
            "case_ids": ["case with space"],
            "seeds": [0],
            "perturbation_noises": [0.0],
        },
    )

    assert command == shlex.join(shlex.split(command))
    assert shlex.split(command) == [
        "PYTHONPATH=src",
        "python",
        "-m",
        "eml_symbolic_regression.cli",
        "campaign",
        "smoke",
        "--output-root",
        str(output_root),
        "--label",
        "ok; echo injected",
        "--overwrite",
        "--formula",
        "exp",
        "--formula",
        "log; rm -rf /",
        "--start-mode",
        "blind",
        "--case",
        "case with space",
        "--seed",
        "0",
        "--perturbation-noise",
        "0.0",
    ]


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


def test_campaign_tables_preserve_perturbed_repair_status_columns(tmp_path):
    aggregate = {
        "runs": [
            _proof_basin_run(),
            _proof_basin_run(
                run_id="basin-beer-lambert-bound-probe-repaired",
                suite_id="proof-perturbed-basin-beer-probes",
                case_id="basin-beer-lambert-bound-probes",
                evidence_class="repaired_candidate",
                classification="repaired_candidate",
                status="repaired_candidate",
                return_kind="snapped_but_failed",
                raw_status="snapped_but_failed",
                repair_status="repaired",
                perturbation_noise=15.0,
            ),
        ],
        "counts": {"total": 2, "verifier_recovered": 1, "evidence_classes": {}},
        "thresholds": [],
    }

    paths = write_campaign_tables(aggregate, tmp_path / "tables")

    run_rows = list(csv.DictReader(paths["runs_csv"].open(encoding="utf-8")))
    assert {
        "return_kind",
        "raw_status",
        "repair_status",
        "repair_verifier_status",
        "repair_accepted_move_count",
    } <= set(run_rows[0])
    repaired = next(row for row in run_rows if row["evidence_class"] == "repaired_candidate")
    assert repaired["return_kind"] == "snapped_but_failed"
    assert repaired["raw_status"] == "snapped_but_failed"
    assert repaired["repair_status"] == "repaired"
    assert repaired["repair_verifier_status"] == "recovered"
    assert repaired["repair_accepted_move_count"] == "1"

    failures = list(csv.DictReader(paths["failures_csv"].open(encoding="utf-8")))
    assert len(failures) == 1
    assert failures[0]["classification"] == "repaired_candidate"
    assert failures[0]["raw_status"] == "snapped_but_failed"
    assert failures[0]["repair_status"] == "repaired"


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
    assert row["claim_id"] == "paper-shallow-scaffolded-recovery"
    assert row["claim_class"] == "scaffolded_training_proof"
    assert row["training_mode"] == "blind_training"
    assert row["evidence_class"]
    assert row["threshold_policy"] == "scaffolded_bounded_100_percent"
    assert row["dataset_manifest_sha256"]
    assert row["provenance_source"] == "sources/paper.pdf"
    assert row["provenance_expression"] == "exp(x)"
    assert "threshold_status" not in row

    claim_groups = list(csv.DictReader(result.table_paths["group_claim_csv"].open(encoding="utf-8")))
    assert claim_groups[0]["group"] == "paper-shallow-scaffolded-recovery"

    manifest = json.loads(result.manifest_path.read_text())
    assert manifest["counts"]["evidence_classes"]
    assert manifest["thresholds"]
    threshold = manifest["thresholds"][0]
    assert threshold["claim_id"] == "paper-shallow-scaffolded-recovery"
    assert threshold["threshold_policy_id"] == "scaffolded_bounded_100_percent"
    assert threshold["status"] in {"passed", "failed"}
    assert {"claim_id", "threshold_policy_id", "status", "passed", "eligible", "rate"} <= set(threshold)
    assert manifest["output"]["tables"]["group_evidence_class_csv"].endswith("group-evidence-class.csv")
    assert manifest["output"]["tables"]["group_claim_csv"].endswith("group-claim.csv")
    assert manifest["output"]["tables"]["group_threshold_policy_csv"].endswith("group-threshold-policy.csv")


def test_proof_basin_report_names_probe_suite_and_status_taxonomy(tmp_path):
    campaign_dir = tmp_path / "proof-basin-report"
    (campaign_dir / "tables").mkdir(parents=True)
    aggregate = {
        "runs": [
            _proof_basin_run(),
            _proof_basin_run(
                run_id="basin-beer-lambert-bound-probes-seed0-noise35",
                suite_id="proof-perturbed-basin-beer-probes",
                case_id="basin-beer-lambert-bound-probes",
                evidence_class="snapped_but_failed",
                classification="snapped_but_failed",
                status="snapped_but_failed",
                claim_status="failed",
                return_kind="snapped_but_failed",
                raw_status="snapped_but_failed",
                repair_status="not_repaired",
                perturbation_noise=35.0,
            ),
        ],
        "counts": {"total": 2, "verifier_recovered": 1, "same_ast_return": 1, "verified_equivalent_ast": 0, "evidence_classes": {}},
        "thresholds": [
            {
                "claim_id": "paper-perturbed-true-tree-basin",
                "threshold_policy_id": "bounded_100_percent",
                "status": "passed",
                "passed": 1,
                "eligible": 1,
                "rate": 1.0,
            }
        ],
    }
    manifest = {
        "preset": campaign_preset("proof-basin").as_dict(),
        "suite": {"id": "proof-perturbed-basin"},
        "output": {"raw_run_root": str(campaign_dir / "runs")},
        "reproducibility": {"command": "PYTHONPATH=src python -m eml_symbolic_regression.cli campaign proof-basin"},
    }
    table_paths = {"runs_csv": campaign_dir / "tables" / "runs.csv"}

    report_path = write_campaign_report(campaign_dir, manifest, aggregate, table_paths, {})
    report = report_path.read_text(encoding="utf-8")
    proof_section = report.split("## Proof Contract", 1)[1].split("## Figures", 1)[0]

    assert "proof-perturbed-basin-beer-probes" in report
    assert "| Field | Meaning |" in report
    assert "`return_kind`" in report
    assert "`raw_status`" in report
    assert "`repair_status`" in report
    assert "paper-perturbed-true-tree-basin" in proof_section
    assert "basin-beer-lambert-bound-probes" not in proof_section


def test_depth_curve_campaign_writes_depth_curve_tables_and_report(tmp_path):
    result = run_campaign(
        "proof-depth-curve",
        output_root=tmp_path,
        label="depth-curve",
        run_filter=RunFilter(case_ids=("depth-2-blind", "depth-2-perturbed"), seeds=(0,)),
    )

    assert result.table_paths["depth_curve_csv"].exists()
    rows = list(csv.DictReader(result.table_paths["depth_curve_csv"].open(encoding="utf-8")))
    assert {row["start_mode"] for row in rows} == {"blind", "perturbed_tree"}
    assert {row["depth"] for row in rows} == {"2"}

    report = result.report_path.read_text(encoding="utf-8")
    assert "## Depth Curve" in report
    assert "paper reports that blind recovery falls sharply with depth" in report
    assert "depth-curve-recovery.svg" in report


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
    assert "## Proof Contract" not in report
    assert "universal blind recovery" not in report
    assert "all elementary functions recovered" not in report

    manifest = json.loads(result.manifest_path.read_text())
    assert manifest["output"]["report_markdown"].endswith("report.md")


def test_proof_campaign_report_separates_threshold_status(tmp_path):
    result = run_campaign(
        "proof-shallow",
        output_root=tmp_path,
        label="proof-report",
        run_filter=RunFilter(case_ids=("shallow-exp-blind",), seeds=(0,)),
    )

    report = result.report_path.read_text(encoding="utf-8")
    manifest = json.loads(result.manifest_path.read_text())
    threshold = manifest["thresholds"][0]

    assert "## Proof Contract" in report
    assert "| Claim | Threshold | Status | Passed | Eligible | Rate |" in report
    assert (
        f"| {threshold['claim_id']} | {threshold['threshold_policy_id']} | {threshold['status']} | "
        f"{threshold['passed']} | {threshold['eligible']} | {threshold['rate']:.3f} |"
    ) in report
    assert (
        "Bounded proof thresholds count only allowed verifier-owned training evidence classes; "
        "catalog and compile-only verification remain separate evidence classes."
    ) in report
    assert "universal blind recovery" not in report
    assert "all elementary functions recovered" not in report
