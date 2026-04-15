import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from eml_symbolic_regression.diagnostics import (
    build_perturbed_basin_bound_report,
    write_perturbed_basin_bound_report,
)


def _aggregate(suite_id: str, rows: list[dict]) -> dict:
    return {
        "schema": "eml.benchmark_aggregate.v1",
        "suite": {"id": suite_id},
        "runs": rows,
    }


def _row(
    *,
    noise: float,
    evidence_class: str,
    suite_id: str = "proof-perturbed-basin",
    case_id: str = "basin-beer-lambert-bound",
    formula: str = "beer_lambert",
    seed: int = 0,
    status: str | None = None,
    claim_status: str | None = None,
    return_kind: str = "same_ast_return",
    raw_status: str = "recovered",
    repair_status: str = "not_attempted",
    changed_slot_count: int | None = 0,
    repair_accepted_move_count: int | None = 0,
    reason: str = "verified",
    run_id: str | None = None,
) -> dict:
    status = status or ("repaired_candidate" if evidence_class == "repaired_candidate" else "recovered")
    claim_status = claim_status or ("failed" if evidence_class not in {"perturbed_true_tree_recovered", "repaired_candidate"} else "recovered")
    run_id = run_id or f"{case_id}-seed{seed}-noise{noise:g}"
    return {
        "suite_id": suite_id,
        "case_id": case_id,
        "run_id": run_id,
        "artifact_path": f"artifacts/benchmarks/{suite_id}/{run_id}.json",
        "formula": formula,
        "seed": seed,
        "perturbation_noise": noise,
        "status": status,
        "claim_status": claim_status,
        "evidence_class": evidence_class,
        "return_kind": return_kind,
        "raw_status": raw_status,
        "repair_status": repair_status,
        "reason": reason,
        "metrics": {
            "changed_slot_count": changed_slot_count,
            "repair_accepted_move_count": repair_accepted_move_count,
            "repair_status": repair_status,
            "verifier_status": "recovered" if claim_status == "recovered" else "failed",
        },
        "stage_statuses": {"perturbed_true_tree_attempt": raw_status},
    }


def test_bound_report_keeps_probe_rows_and_computes_continuous_prefixes():
    bounded = _aggregate(
        "proof-perturbed-basin",
        [_row(noise=5.0, evidence_class="perturbed_true_tree_recovered", seed=0)],
    )
    probe = _aggregate(
        "proof-perturbed-basin-beer-probes",
        [
            _row(
                noise=15.0,
                evidence_class="repaired_candidate",
                suite_id="proof-perturbed-basin-beer-probes",
                case_id="basin-beer-lambert-bound-probes",
                status="repaired_candidate",
                return_kind="snapped_but_failed",
                raw_status="snapped_but_failed",
                repair_status="repaired",
                changed_slot_count=2,
                repair_accepted_move_count=1,
            ),
            _row(
                noise=35.0,
                evidence_class="snapped_but_failed",
                suite_id="proof-perturbed-basin-beer-probes",
                case_id="basin-beer-lambert-bound-probes",
                status="snapped_but_failed",
                claim_status="failed",
                return_kind="snapped_but_failed",
                raw_status="snapped_but_failed",
                repair_status="not_repaired",
                changed_slot_count=3,
                reason="verifier_mismatch",
            ),
            _row(noise=15.0, evidence_class="perturbed_true_tree_recovered", formula="exp"),
        ],
    )

    report = build_perturbed_basin_bound_report(bounded, probe)

    assert report["schema"] == "eml.perturbed_basin_bound_report.v1"
    assert report["declared_noise_grid"] == [5.0, 15.0, 35.0]
    assert report["bounded_noise_values"] == [5.0]
    assert report["probe_noise_values"] == [15.0, 35.0]
    assert report["declared_bound_noise_max"] == 5.0
    assert report["raw_supported_noise_max"] == 5.0
    assert report["repaired_supported_noise_max"] == 15.0
    assert report["unsupported_noise_values"] == [35.0]
    assert report["claim_recommendation"] == "probe_supports_15"
    assert [row["perturbation_noise"] for row in report["rows"]] == [5.0, 15.0, 35.0]

    repaired = next(row for row in report["rows"] if row["perturbation_noise"] == 15.0)
    failed = next(row for row in report["rows"] if row["perturbation_noise"] == 35.0)
    assert repaired["evidence_class"] == "repaired_candidate"
    assert repaired["repair_status"] == "repaired"
    assert repaired["return_kind"] == "snapped_but_failed"
    assert repaired["changed_slot_count"] == 2
    assert repaired["repair_accepted_move_count"] == 1
    assert failed["reason"] == "verifier_mismatch"
    assert failed["artifact_path"].endswith("noise35.json")


def test_supported_max_uses_continuous_prefix_not_isolated_higher_pass():
    bounded = _aggregate(
        "proof-perturbed-basin",
        [_row(noise=5.0, evidence_class="perturbed_true_tree_recovered")],
    )
    probe = _aggregate(
        "proof-perturbed-basin-beer-probes",
        [
            _row(
                noise=15.0,
                evidence_class="snapped_but_failed",
                suite_id="proof-perturbed-basin-beer-probes",
                case_id="basin-beer-lambert-bound-probes",
                status="snapped_but_failed",
                claim_status="failed",
                return_kind="snapped_but_failed",
                raw_status="snapped_but_failed",
                repair_status="not_repaired",
            ),
            _row(
                noise=35.0,
                evidence_class="perturbed_true_tree_recovered",
                suite_id="proof-perturbed-basin-beer-probes",
                case_id="basin-beer-lambert-bound-probes",
            ),
        ],
    )

    report = build_perturbed_basin_bound_report(bounded, probe)

    assert report["raw_supported_noise_max"] == 5.0
    assert report["repaired_supported_noise_max"] == 5.0
    assert report["unsupported_noise_values"] == [15.0]
    assert report["claim_recommendation"] == "support_declared_bound"


def test_failed_declared_bound_recommends_narrowing():
    bounded = _aggregate(
        "proof-perturbed-basin",
        [
            _row(
                noise=5.0,
                evidence_class="snapped_but_failed",
                status="snapped_but_failed",
                claim_status="failed",
                return_kind="snapped_but_failed",
                raw_status="snapped_but_failed",
                repair_status="not_repaired",
            )
        ],
    )

    report = build_perturbed_basin_bound_report(bounded)

    assert report["raw_supported_noise_max"] is None
    assert report["repaired_supported_noise_max"] is None
    assert report["unsupported_noise_values"] == [5.0]
    assert report["claim_recommendation"] == "narrow_to_none"


def test_write_bound_report_outputs_json_and_markdown(tmp_path):
    bounded_path = tmp_path / "bounded" / "aggregate.json"
    probe_path = tmp_path / "probe" / "aggregate.json"
    bounded_path.parent.mkdir()
    probe_path.parent.mkdir()
    bounded_path.write_text(
        json.dumps(_aggregate("proof-perturbed-basin", [_row(noise=5.0, evidence_class="perturbed_true_tree_recovered")])),
        encoding="utf-8",
    )
    probe_path.write_text(
        json.dumps(
            _aggregate(
                "proof-perturbed-basin-beer-probes",
                [
                    _row(
                        noise=15.0,
                        evidence_class="repaired_candidate",
                        suite_id="proof-perturbed-basin-beer-probes",
                        case_id="basin-beer-lambert-bound-probes",
                        status="repaired_candidate",
                        return_kind="snapped_but_failed",
                        raw_status="snapped_but_failed",
                        repair_status="repaired",
                    )
                ],
            )
        ),
        encoding="utf-8",
    )

    paths = write_perturbed_basin_bound_report(bounded_path, probe_path, tmp_path / "evidence")

    payload = json.loads(paths["json"].read_text(encoding="utf-8"))
    markdown = paths["markdown"].read_text(encoding="utf-8")
    assert paths["json"].name == "basin-bound.json"
    assert paths["markdown"].name == "basin-bound.md"
    assert payload["schema"] == "eml.perturbed_basin_bound_report.v1"
    assert payload["probe_noise_values"] == [15.0]
    assert "proof-perturbed-basin-beer-probes" in markdown
    assert "repaired_candidate" in markdown


def test_cli_diagnostics_basin_bound_writes_reports(tmp_path):
    bounded_path = tmp_path / "bounded.json"
    probe_path = tmp_path / "probe.json"
    output_dir = tmp_path / "diagnostics"
    bounded_path.write_text(
        json.dumps(_aggregate("proof-perturbed-basin", [_row(noise=5.0, evidence_class="perturbed_true_tree_recovered")])),
        encoding="utf-8",
    )
    probe_path.write_text(
        json.dumps(
            _aggregate(
                "proof-perturbed-basin-beer-probes",
                [
                    _row(
                        noise=35.0,
                        evidence_class="snapped_but_failed",
                        suite_id="proof-perturbed-basin-beer-probes",
                        case_id="basin-beer-lambert-bound-probes",
                        status="snapped_but_failed",
                        claim_status="failed",
                        return_kind="snapped_but_failed",
                        raw_status="snapped_but_failed",
                        repair_status="not_repaired",
                    )
                ],
            )
        ),
        encoding="utf-8",
    )
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "eml_symbolic_regression.cli",
            "diagnostics",
            "basin-bound",
            "--bounded-aggregate",
            str(bounded_path),
            "--probe-aggregate",
            str(probe_path),
            "--output-dir",
            str(output_dir),
        ],
        cwd=Path(__file__).parents[1],
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "basin-bound.json" in result.stdout
    assert "basin-bound.md" in result.stdout
    assert json.loads((output_dir / "basin-bound.json").read_text(encoding="utf-8"))["unsupported_noise_values"] == [35.0]
    assert "proof-perturbed-basin-beer-probes" in (output_dir / "basin-bound.md").read_text(encoding="utf-8")
