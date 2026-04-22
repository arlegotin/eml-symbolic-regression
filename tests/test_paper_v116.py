import csv
import json

from eml_symbolic_regression.cli import build_parser, geml_paper_v116_command
from eml_symbolic_regression.paper_v116 import (
    build_v116_claim_audit,
    default_v116_gate_config,
    evaluate_v116_gate,
    write_v116_paper_package,
)


def _write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_paired_campaign(campaign_dir, rows):
    table_dir = campaign_dir / "tables"
    table_dir.mkdir(parents=True, exist_ok=True)
    fieldnames = ["formula", "target_family", "seed", "comparison_outcome"]
    with (table_dir / "geml-paired-comparison.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    outcomes = {}
    for row in rows:
        outcomes[row["comparison_outcome"]] = outcomes.get(row["comparison_outcome"], 0) + 1
    _write_json(
        table_dir / "geml-paired-summary.json",
        {
            "schema": "eml.geml_paired_summary.v1",
            "paired_rows": len(rows),
            "unique_seeds": len({row["seed"] for row in rows}),
            "ipi_recovery_wins": outcomes.get("ipi_recovery_win", 0),
            "raw_recovery_wins": outcomes.get("raw_recovery_win", 0),
            "both_recovered": outcomes.get("both_recovered", 0),
            "loss_only_outcomes": outcomes.get("ipi_lower_post_snap_mse", 0) + outcomes.get("raw_lower_post_snap_mse", 0),
        },
    )
    _write_json(campaign_dir / "campaign-manifest.json", {"schema": "fixture", "preset": {"name": "geml-v116-fixture"}})


def test_v116_gate_requires_exact_recovery_not_loss_only():
    gate = default_v116_gate_config(min_unique_seeds=1)
    evaluation = evaluate_v116_gate(
        {"paired_rows": 2, "loss_only_outcomes": 1, "unique_seeds": 1},
        [
            {"target_family": "periodic", "declared_targets": 1, "paired_rows": 1, "ipi_recovery_wins": 0, "raw_recovery_wins": 0, "loss_only_outcomes": 1},
            {"target_family": "negative_control", "declared_targets": 1, "paired_rows": 1, "ipi_recovery_wins": 0, "raw_recovery_wins": 0, "loss_only_outcomes": 0},
        ],
        gate_config=gate,
    )

    assert evaluation["decision"] == "inconclusive"
    assert "loss_only_signal_without_exact_recovery" in evaluation["blockers"]


def test_v116_gate_promotes_full_exact_ipi_win_to_paper_positive():
    gate = default_v116_gate_config(min_unique_seeds=1)
    classification = [
        {"target_family": "periodic", "declared_targets": 2, "paired_rows": 2, "ipi_recovery_wins": 2, "raw_recovery_wins": 0, "loss_only_outcomes": 0},
        {"target_family": "harmonic", "declared_targets": 1, "paired_rows": 1, "ipi_recovery_wins": 1, "raw_recovery_wins": 0, "loss_only_outcomes": 0},
        {"target_family": "negative_control", "declared_targets": 4, "paired_rows": 4, "ipi_recovery_wins": 0, "raw_recovery_wins": 1, "loss_only_outcomes": 0},
    ]
    evaluation = evaluate_v116_gate(
        {"paired_rows": 10, "unique_seeds": 1},
        classification,
        gate_config=gate,
        source_locks_ok=True,
    )

    assert evaluation["decision"] == "paper_positive"
    assert evaluation["metrics"]["natural_ipi_minus_raw_recovery_wins"] == 3


def test_v116_gate_blocks_negative_control_ipi_win():
    gate = default_v116_gate_config(min_unique_seeds=1)
    evaluation = evaluate_v116_gate(
        {"paired_rows": 10, "unique_seeds": 1},
        [
            {"target_family": "periodic", "declared_targets": 2, "paired_rows": 2, "ipi_recovery_wins": 2, "raw_recovery_wins": 0, "loss_only_outcomes": 0},
            {"target_family": "negative_control", "declared_targets": 4, "paired_rows": 4, "ipi_recovery_wins": 1, "raw_recovery_wins": 0, "loss_only_outcomes": 0},
        ],
        gate_config=gate,
    )

    assert evaluation["decision"] == "inconclusive"
    assert "negative_control_ipi_recovery_win" in evaluation["blockers"]


def test_v116_claim_audit_blocks_unsafe_language():
    audit = build_v116_claim_audit(
        "This paper_positive result proves loss-only recovery, global superiority, and all elementary functions.",
        gate_evaluation={"decision": "inconclusive"},
        source_locks={"inputs": [{"status": "locked"}]},
    )

    failed = {check["id"] for check in audit["checks"] if check["status"] == "failed"}
    assert audit["status"] == "failed"
    assert {
        "blocks_loss_only_recovery_claims",
        "blocks_global_superiority_language",
        "blocks_full_universality_language",
        "paper_positive_requires_gate_pass",
    } <= failed


def test_write_v116_paper_package_writes_fail_closed_artifacts(tmp_path):
    campaign_dir = tmp_path / "campaign"
    rows = [
        {"formula": "sin_pi", "target_family": "periodic", "seed": "0", "comparison_outcome": "ipi_lower_post_snap_mse"},
        {"formula": "exp", "target_family": "negative_control", "seed": "0", "comparison_outcome": "raw_lower_post_snap_mse"},
    ]
    _write_paired_campaign(campaign_dir, rows)

    paths = write_v116_paper_package(tmp_path / "package", campaign_dir=campaign_dir, min_unique_seeds=1)

    manifest = json.loads(paths.manifest_json.read_text(encoding="utf-8"))
    audit = json.loads(paths.claim_audit_json.read_text(encoding="utf-8"))
    evaluation = json.loads(paths.gate_evaluation_json.read_text(encoding="utf-8"))

    assert manifest["schema"] == "eml.v116_paper_decision_package.v1"
    assert evaluation["decision"] == "inconclusive"
    assert manifest["decision"] == "inconclusive"
    assert audit["status"] == "passed"
    assert "Loss-only improvements are diagnostics" in paths.decision_md.read_text(encoding="utf-8")


def test_cli_registers_geml_paper_v116():
    args = build_parser().parse_args(["geml-paper-v116", "--output-dir", "out", "--campaign-dir", "campaign"])
    assert args.func is geml_paper_v116_command
