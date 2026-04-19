import json

from eml_symbolic_regression.cli import build_parser, paper_draft_command
from eml_symbolic_regression.paper_v112 import claim_taxonomy_rows, write_v112_draft


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
