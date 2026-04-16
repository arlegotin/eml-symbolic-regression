import json
import os
import subprocess
import sys
from pathlib import Path

from eml_symbolic_regression.datasets import get_demo
from eml_symbolic_regression.verify import verify_candidate


ROOT = Path(__file__).resolve().parents[1]
CLI_ENV = {**os.environ, "PYTHONPATH": str(ROOT / "src")}


def test_exact_eml_demos_are_recovered():
    for name in ("exp", "log"):
        spec = get_demo(name)
        report = verify_candidate(spec.candidate, spec.make_splits(points=32), tolerance=1e-8)
        assert report.status == "recovered"


def test_catalog_showcase_is_not_labeled_exact_recovery():
    spec = get_demo("planck")
    report = verify_candidate(spec.candidate, spec.make_splits(points=32), tolerance=1e-8)
    assert report.status == "verified_showcase"
    assert report.reason == "verified_non_eml_candidate"


def test_cli_demo_writes_report(tmp_path):
    output = tmp_path / "exp-report.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "eml_symbolic_regression.cli",
            "demo",
            "exp",
            "--points",
            "24",
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        env=CLI_ENV,
        text=True,
    )
    assert "exp: recovered" in result.stdout
    payload = json.loads(output.read_text())
    assert payload["claim_status"] == "recovered"
    assert payload["verification"]["status"] == "recovered"


def test_cli_demo_train_eml_writes_selection_and_fallback_provenance(tmp_path):
    output = tmp_path / "exp-trained-report.json"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "eml_symbolic_regression.cli",
            "demo",
            "exp",
            "--points",
            "24",
            "--train-eml",
            "--depth",
            "1",
            "--steps",
            "2",
            "--restarts",
            "1",
            "--hardening-steps",
            "2",
            "--hardening-emit-interval",
            "1",
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        env=CLI_ENV,
        text=True,
    )
    payload = json.loads(output.read_text())
    selection = payload["trained_eml_candidate"]["selection"]

    assert payload["trained_eml_verification"]["status"] == "recovered"
    assert selection["mode"] == "verifier_gated_exact_candidate_pool"
    assert selection["selected_candidate_id"] == payload["trained_eml_candidate"]["selected_candidate"]["candidate_id"]
    assert selection["fallback_candidate_id"] == payload["trained_eml_candidate"]["fallback_candidate"]["candidate_id"]
    assert payload["trained_eml_candidate"]["fallback_candidate"]["source"] == "legacy_final_snap"


def test_cli_verify_paper():
    result = subprocess.run(
        [sys.executable, "-m", "eml_symbolic_regression.cli", "verify-paper", "--points", "24"],
        check=True,
        capture_output=True,
        env=CLI_ENV,
        text=True,
    )
    assert "exp: recovered" in result.stdout
    assert "log: recovered" in result.stdout


def test_cli_list_demos():
    result = subprocess.run(
        [sys.executable, "-m", "eml_symbolic_regression.cli", "list-demos"],
        check=True,
        capture_output=True,
        env=CLI_ENV,
        text=True,
    )
    assert "planck:" in result.stdout
    assert "michaelis_menten:" in result.stdout
