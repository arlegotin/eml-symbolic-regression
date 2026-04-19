import json

from eml_symbolic_regression.cli import build_parser, paper_draft_command, paper_refresh_command
from eml_symbolic_regression.paper_v112 import (
    claim_taxonomy_rows,
    refresh_run_rows,
    v112_depth_refresh_suite,
    v112_shallow_refresh_suite,
    write_v112_draft,
)


def _json(path):
    return json.loads(open(path, encoding="utf-8").read())


def test_claim_taxonomy_separates_pure_blind_from_assisted_regimes():
    ledger = _json("artifacts/paper/v1.11/raw-hybrid/claim-ledger.json")

    rows = claim_taxonomy_rows(ledger)
    by_class = {row["evidence_class"]: row for row in rows}

    assert {
        "pure_blind",
        "scaffolded",
        "warm_start",
        "same_ast",
        "perturbed_basin",
        "repair_refit",
        "compile_only",
        "unsupported",
        "failed",
    } <= set(by_class)
    assert by_class["pure_blind"]["eligible_for_pure_blind_rate"] is True
    assert by_class["scaffolded"]["eligible_for_pure_blind_rate"] is False
    assert by_class["same_ast"]["eligible_for_pure_blind_rate"] is False
    assert by_class["unsupported"]["eligible_for_verifier_recovery_rate"] is False
    assert by_class["failed"]["eligible_for_verifier_recovery_rate"] is False


def test_write_v112_draft_outputs_sections_and_taxonomy(tmp_path):
    paths = write_v112_draft(output_dir=tmp_path / "draft")

    manifest = json.loads(paths.manifest_json.read_text(encoding="utf-8"))
    taxonomy = json.loads(paths.claim_taxonomy_json.read_text(encoding="utf-8"))
    abstract = paths.abstract_md.read_text(encoding="utf-8")
    results = paths.results_md.read_text(encoding="utf-8")
    limitations = paths.limitations_md.read_text(encoding="utf-8")

    assert manifest["schema"] == "eml.v112_paper_draft.v1"
    assert manifest["claim_boundary"].startswith("draft scaffold preserves")
    assert paths.methods_md.exists()
    assert paths.claim_taxonomy_csv.exists()
    assert any(row["evidence_class"] == "pure_blind" for row in taxonomy["rows"])
    assert "verifier-gated" in abstract
    assert "Logistic and Planck remain unsupported" in results
    assert "do not establish pure blind discovery" in limitations


def test_paper_draft_cli_writes_manifest(tmp_path, capsys):
    output_dir = tmp_path / "draft"
    args = build_parser().parse_args(["paper-draft", "--output-dir", str(output_dir)])

    assert args.func is paper_draft_command
    assert args.func(args) == 0

    captured = capsys.readouterr().out
    assert "paper draft: manifest ->" in captured
    assert (output_dir / "abstract.md").exists()
    assert (output_dir / "claim-taxonomy.md").exists()


def test_v112_shallow_refresh_suite_has_new_separate_seed_denominators(tmp_path):
    suite = v112_shallow_refresh_suite(tmp_path)
    runs = suite.expanded_runs()

    assert suite.id == "v1.12-shallow-refresh"
    assert len(runs) == 10
    assert {run.seed for run in runs} == {2, 3, 4, 5, 6}
    pure = [run for run in runs if run.case_id == "exp-pure-blind-seed-refresh"]
    scaffolded = [run for run in runs if run.case_id == "exp-scaffolded-seed-refresh"]
    assert len(pure) == 5
    assert len(scaffolded) == 5
    assert all(run.optimizer.scaffold_initializers == () for run in pure)
    assert all(run.optimizer.scaffold_initializers for run in scaffolded)


def test_v112_depth_refresh_suite_uses_current_code_depth_2_to_5_subset(tmp_path):
    suite = v112_depth_refresh_suite(tmp_path)
    runs = suite.expanded_runs()

    assert suite.id == "proof-depth-curve"
    assert len(runs) == 8
    assert {run.case_id for run in runs} == {"depth-2-blind", "depth-3-blind", "depth-4-blind", "depth-5-blind"}
    assert {run.optimizer.depth for run in runs} == {2, 3, 4, 5}
    assert {run.seed for run in runs} == {0, 1}
    assert all(run.start_mode == "blind" for run in runs)


def test_refresh_run_rows_exposes_seed_depth_status_and_artifact_path():
    aggregate = {
        "runs": [
            {
                "suite_id": "suite",
                "case_id": "case",
                "formula": "exp",
                "start_mode": "blind",
                "seed": 2,
                "optimizer": {"depth": 1, "steps": 4, "restarts": 1, "scaffold_initializers": []},
                "evidence_class": "blind_training_recovered",
                "classification": "blind_recovery",
                "status": "recovered",
                "claim_status": "recovered",
                "metrics": {"verifier_status": "recovered", "best_loss": 0.0},
                "reason": "recovered",
                "artifact_path": "artifacts/run.json",
            }
        ]
    }

    rows = refresh_run_rows(aggregate, source="unit")

    assert rows == [
        {
            "source": "unit",
            "suite_id": "suite",
            "case_id": "case",
            "formula": "exp",
            "start_mode": "blind",
            "seed": 2,
            "depth": 1,
            "steps": 4,
            "restarts": 1,
            "scaffold_initializers": "",
            "evidence_class": "blind_training_recovered",
            "classification": "blind_recovery",
            "status": "recovered",
            "claim_status": "recovered",
            "verifier_status": "recovered",
            "best_loss": 0.0,
            "post_snap_loss": None,
            "snap_min_margin": None,
            "reason": "recovered",
            "artifact_path": "artifacts/run.json",
            "claim_boundary": "row belongs only to its source suite/start-mode denominator",
        }
    ]


def test_paper_refresh_cli_is_registered():
    args = build_parser().parse_args(["paper-refresh", "--output-dir", "artifacts/tmp-refresh", "--overwrite"])

    assert args.func is paper_refresh_command
    assert args.output_dir == "artifacts/tmp-refresh"
    assert args.overwrite is True
