import json
import os
import subprocess
import sys
from pathlib import Path

from eml_symbolic_regression.benchmark import RunFilter, builtin_suite, run_benchmark_suite


ROOT = Path(__file__).resolve().parents[1]
CLI_ENV = {**os.environ, "PYTHONPATH": str(ROOT / "src")}


def test_runner_executes_catalog_compile_blind_and_warm_start(tmp_path):
    suite = type(builtin_suite("smoke"))(
        "smoke",
        "test smoke",
        builtin_suite("smoke").cases,
        tmp_path / "artifacts",
    )

    result = run_benchmark_suite(suite)
    payload = result.as_dict()

    assert payload["counts"]["total"] == 3
    assert all(item.artifact_path.exists() for item in result.results)
    statuses = {item.run.case_id: item.status for item in result.results}
    assert statuses["exp-blind"] in {"recovered", "snapped_but_failed", "failed"}
    assert statuses["beer-warm"] in {"same_ast_return", "verified_equivalent_ast", "snapped_but_failed"}
    assert statuses["planck-diagnostic"] == "unsupported"


def test_runner_filter_executes_subset(tmp_path):
    base = builtin_suite("v1.2-evidence")
    suite = type(base)(base.id, base.description, base.cases, tmp_path / "artifacts")

    result = run_benchmark_suite(suite, run_filter=RunFilter(case_ids=("beer-perturbation-sweep",), seeds=(0,)))

    assert len(result.results) == 3
    assert {item.run.perturbation_noise for item in result.results} == {0.0, 5.0, 35.0}


def test_cli_benchmark_writes_suite_result(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "eml_symbolic_regression.cli",
            "benchmark",
            "smoke",
            "--case",
            "planck-diagnostic",
            "--output-dir",
            str(tmp_path),
        ],
        check=True,
        capture_output=True,
        env=CLI_ENV,
        text=True,
    )

    assert "smoke: 1 runs" in result.stdout
    suite_result = tmp_path / "smoke" / "suite-result.json"
    payload = json.loads(suite_result.read_text())
    assert payload["counts"]["total"] == 1
    assert payload["results"][0]["status"] == "unsupported"


def test_for_demo_diagnostic_subset_preserves_unsupported_formula(tmp_path):
    base = builtin_suite("for-demo-diagnostics")
    suite = type(base)(base.id, base.description, base.cases, tmp_path / "artifacts")

    result = run_benchmark_suite(suite, run_filter=RunFilter(case_ids=("damped-oscillator-compile",)))

    assert len(result.results) == 1
    assert result.results[0].status == "unsupported"
    assert result.results[0].payload["compiled_eml"]["reason"] == "unsupported_operator"
