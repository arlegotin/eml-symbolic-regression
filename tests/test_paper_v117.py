import csv
import json

from eml_symbolic_regression.cli import build_parser, geml_v117_neighborhoods_command, geml_v117_snap_diagnostics_command
from eml_symbolic_regression.master_tree import SoftEMLTree
from eml_symbolic_regression.paper_v117 import write_v117_neighborhood_candidates, write_v117_snap_diagnostics


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


def test_write_v117_neighborhood_candidates_generates_bounded_deterministic_variants(tmp_path):
    snap_dir = tmp_path / "snap"
    artifact = tmp_path / "candidate.json"
    tree = SoftEMLTree(2, ("x",))
    tree.set_slot("root", "left", "child", strength=40.0)
    tree.set_slot("root", "right", "const:1", strength=40.0)
    tree.set_slot("root.L", "left", "var:x", strength=40.0)
    tree.set_slot("root.L", "right", "const:1", strength=40.0)
    tree.root.right_logits.data.copy_(tree.root.right_logits.data.new_tensor([2.0, 1.9, 0.0]))
    tree.root.left_child.left_logits.data.copy_(tree.root.left_child.left_logits.data.new_tensor([1.8, 2.0]))
    snap = tree.snap()
    candidate = {
        "candidate_id": "raw-selected",
        "snap": snap.as_dict(),
        "slot_alternatives": [item.as_dict() for item in tree.active_slot_alternatives(top_k=1, max_slots=2)],
    }
    _write_json(
        artifact,
        {
            "trained_eml_candidate": {
                "config": {
                    "variables": ["x"],
                    "constants": ["1"],
                    "operator_family": tree.operator_family.as_dict(),
                },
                "candidates": [candidate],
                "selected_candidate": candidate,
            }
        },
    )
    _write_json(
        snap_dir / "snap-neighborhood-seeds.json",
        {
            "schema": "fixture",
            "rows": [
                {
                    "seed_id": "sin_pi:seed0:raw:selected",
                    "pair_id": "sin_pi:seed0:depth2",
                    "formula": "sin_pi",
                    "target_family": "periodic",
                    "seed": "0",
                    "operator_family": "raw_eml",
                    "candidate_id": "raw-selected",
                    "fallback_candidate_id": "raw-fallback",
                    "comparison_outcome": "raw_lower_post_snap_mse",
                    "artifact_path": str(artifact),
                    "target_formula_leakage": False,
                }
            ],
        },
    )

    first = write_v117_neighborhood_candidates(tmp_path / "neighborhoods-a", snap_diagnostics_dir=snap_dir, candidate_budget=6)
    second = write_v117_neighborhood_candidates(tmp_path / "neighborhoods-b", snap_diagnostics_dir=snap_dir, candidate_budget=6)

    first_rows = json.loads(first.neighborhood_candidates_json.read_text(encoding="utf-8"))["rows"]
    second_rows = json.loads(second.neighborhood_candidates_json.read_text(encoding="utf-8"))["rows"]
    assert first_rows == second_rows
    assert [row["provenance"] for row in first_rows[:2]] == ["original_snap", "fallback_snap"]
    assert any(row["move_count"] == 1 for row in first_rows)
    assert any(row["move_count"] == 2 for row in first_rows)
    assert {row["target_formula_leakage"] for row in first_rows} == {False}
    assert all("target_tree" not in row for row in first_rows)


def test_cli_registers_geml_v117_neighborhoods():
    args = build_parser().parse_args(["geml-v117-neighborhoods", "--output-dir", "out", "--snap-diagnostics-dir", "snap"])
    assert args.func is geml_v117_neighborhoods_command
    assert args.snap_diagnostics_dir == "snap"
