import json

import pytest

from eml_symbolic_regression.benchmark import (
    BenchmarkSuite,
    BenchmarkValidationError,
    builtin_suite,
    list_builtin_suites,
    load_suite,
)


def test_builtin_suite_registry_expands_stable_run_ids():
    assert {"smoke", "v1.2-evidence", "for-demo-diagnostics"} <= set(list_builtin_suites())
    suite = builtin_suite("smoke")
    runs = suite.expanded_runs()

    assert [run.case_id for run in runs] == ["exp-blind", "beer-warm", "planck-diagnostic"]
    assert runs[0].run_id == suite.expanded_runs()[0].run_id
    assert str(runs[0].artifact_path).endswith(f"{runs[0].run_id}.json")


def test_v12_evidence_suite_contains_perturbation_matrix():
    suite = load_suite("v1.2-evidence")
    runs = suite.expanded_runs()
    beer_runs = [run for run in runs if run.case_id == "beer-perturbation-sweep"]

    assert len(beer_runs) == 9
    assert {run.perturbation_noise for run in beer_runs} == {0.0, 5.0, 35.0}
    assert {run.seed for run in beer_runs} == {0, 1, 2}


def test_unknown_formula_fails_closed():
    suite = BenchmarkSuite.from_mapping(
        {
            "schema": "eml.benchmark_suite.v1",
            "id": "bad",
            "cases": [{"id": "bad-case", "formula": "nope", "start_mode": "blind"}],
        }
    )

    with pytest.raises(BenchmarkValidationError) as exc:
        suite.validate()

    assert exc.value.reason == "unknown_formula"
    assert exc.value.path == "cases[0].formula"


def test_non_warm_start_perturbation_fails_closed():
    suite = BenchmarkSuite.from_mapping(
        {
            "schema": "eml.benchmark_suite.v1",
            "id": "bad",
            "cases": [
                {
                    "id": "bad-case",
                    "formula": "exp",
                    "start_mode": "blind",
                    "perturbation_noise": [1.0],
                }
            ],
        }
    )

    with pytest.raises(BenchmarkValidationError) as exc:
        suite.validate()

    assert exc.value.reason == "invalid_perturbation"


def test_custom_suite_loads_from_json(tmp_path):
    path = tmp_path / "suite.json"
    path.write_text(
        json.dumps(
            {
                "schema": "eml.benchmark_suite.v1",
                "id": "custom",
                "artifact_root": str(tmp_path / "artifacts"),
                "cases": [{"id": "compile-exp", "formula": "exp", "start_mode": "compile", "dataset": {"points": 12}}],
            }
        ),
        encoding="utf-8",
    )

    suite = load_suite(path)
    runs = suite.expanded_runs()

    assert suite.id == "custom"
    assert len(runs) == 1
    assert runs[0].dataset.points == 12
    assert str(runs[0].artifact_path).startswith(str(tmp_path / "artifacts"))
