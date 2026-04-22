import csv
import json

from eml_symbolic_regression.cli import build_parser, geml_v117_snap_diagnostics_command
from eml_symbolic_regression.paper_v117 import write_v117_snap_diagnostics


def _write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_v117_fixture_campaign(campaign_dir):
    table_dir = campaign_dir / "tables"
    table_dir.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "pair_id": "sin_pi:seed0:depth3",
            "formula": "sin_pi",
            "target_family": "periodic",
            "seed": "0",
            "comparison_outcome": "ipi_lower_post_snap_mse",
            "raw_status": "snapped_but_failed",
            "ipi_status": "snapped_but_failed",
            "raw_verification_outcome": "failed",
            "ipi_verification_outcome": "failed",
            "raw_trained_exact_recovery": "False",
            "ipi_trained_exact_recovery": "False",
            "raw_selected_candidate_id": "raw-selected",
            "ipi_selected_candidate_id": "ipi-selected",
            "raw_fallback_candidate_id": "raw-fallback",
            "ipi_fallback_candidate_id": "ipi-fallback",
            "raw_snap_min_margin": "0.42",
            "ipi_snap_min_margin": "0.03",
            "raw_snap_active_node_count": "7",
            "ipi_snap_active_node_count": "9",
            "raw_low_margin_slot_count": "0",
            "ipi_low_margin_slot_count": "2",
            "raw_lowest_margin_slots_json": "[]",
            "ipi_lowest_margin_slots_json": json.dumps(
                [{"slot": "root.left", "choice": "child", "probability": 0.51, "margin": 0.03}]
            ),
            "raw_low_confidence_alternatives_json": "[]",
            "ipi_low_confidence_alternatives_json": json.dumps(
                [{"slot": "root.left", "alternatives": [{"choice": "var:x", "probability_gap": 0.03}]}]
            ),
            "raw_pre_snap_mse": "0.2",
            "ipi_pre_snap_mse": "0.2",
            "raw_post_snap_mse": "0.3",
            "ipi_post_snap_mse": "0.1",
            "raw_post_snap_minus_soft_best": "0.28",
            "ipi_post_snap_minus_soft_best": "0.08",
            "raw_post_snap_minus_pre_snap": "0.1",
            "ipi_post_snap_minus_pre_snap": "-0.1",
            "raw_branch_cut_crossing_count": "0",
            "ipi_branch_cut_crossing_count": "0",
            "raw_branch_cut_proximity_count": "0",
            "ipi_branch_cut_proximity_count": "4",
            "raw_branch_input_count": "0",
            "ipi_branch_input_count": "8",
            "raw_artifact_path": "artifacts/raw.json",
            "ipi_artifact_path": "artifacts/ipi.json",
        },
        {
            "pair_id": "exp:seed0:depth3",
            "formula": "exp",
            "target_family": "negative_control",
            "seed": "0",
            "comparison_outcome": "raw_recovery_win",
            "raw_status": "recovered",
            "ipi_status": "snapped_but_failed",
            "raw_verification_outcome": "recovered",
            "ipi_verification_outcome": "failed",
            "raw_trained_exact_recovery": "True",
            "ipi_trained_exact_recovery": "False",
            "raw_selected_candidate_id": "raw-exact",
            "ipi_selected_candidate_id": "ipi-failed",
            "raw_snap_min_margin": "0.9",
            "ipi_snap_min_margin": "0.9",
        },
    ]
    fieldnames = sorted({key for row in rows for key in row})
    with (table_dir / "geml-paired-comparison.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    _write_json(table_dir / "geml-paired-summary.json", {"schema": "fixture", "paired_rows": 2})
    _write_json(campaign_dir / "campaign-manifest.json", {"schema": "fixture"})


def test_write_v117_snap_diagnostics_emits_low_margin_raw_and_ipi_rows(tmp_path):
    campaign_dir = tmp_path / "campaign"
    _write_v117_fixture_campaign(campaign_dir)

    paths = write_v117_snap_diagnostics(tmp_path / "snap", campaign_dir=campaign_dir)

    manifest = json.loads(paths.manifest_json.read_text(encoding="utf-8"))
    diagnostics = json.loads(paths.snap_diagnostics_json.read_text(encoding="utf-8"))["rows"]
    seeds = json.loads(paths.snap_neighborhood_seeds_json.read_text(encoding="utf-8"))["rows"]
    csv_text = paths.snap_diagnostics_csv.read_text(encoding="utf-8")

    assert manifest["schema"] == "eml.v117_snap_diagnostics_manifest.v1"
    assert manifest["counts"]["diagnostic_rows"] == 4
    assert manifest["counts"]["neighborhood_seed_rows"] == 2
    assert any(row["operator_family"] == "raw_eml" for row in diagnostics)
    ipi = next(row for row in diagnostics if row["candidate_id"] == "ipi-selected")
    assert ipi["snap_mismatch_class"] == "low_margin_snap_mismatch"
    assert ipi["neighborhood_seed"] is True
    assert "root.left" in ipi["lowest_margin_slots_json"]
    assert "raw-selected" in csv_text
    assert {row["target_formula_leakage"] for row in seeds} == {False}


def test_v117_snap_diagnostics_do_not_seed_exact_recovery_rows(tmp_path):
    campaign_dir = tmp_path / "campaign"
    _write_v117_fixture_campaign(campaign_dir)

    paths = write_v117_snap_diagnostics(tmp_path / "snap", campaign_dir=campaign_dir)
    seeds = json.loads(paths.snap_neighborhood_seeds_json.read_text(encoding="utf-8"))["rows"]

    assert all(row["pair_id"] == "sin_pi:seed0:depth3" for row in seeds)
    assert [row["operator_family"] for row in seeds] == ["ipi_eml", "raw_eml"]


def test_cli_registers_geml_v117_snap_diagnostics():
    args = build_parser().parse_args(["geml-v117-snap-diagnostics", "--output-dir", "out", "--campaign-dir", "campaign"])
    assert args.func is geml_v117_snap_diagnostics_command
    assert args.campaign_dir == "campaign"
