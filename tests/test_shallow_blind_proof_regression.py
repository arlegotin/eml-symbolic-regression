import json

import pytest

from eml_symbolic_regression.benchmark import aggregate_evidence, load_suite, run_benchmark_suite


EXPECTED_SHALLOW_CASE_IDS = (
    "shallow-exp-blind",
    "shallow-log-blind",
    "shallow-radioactive-decay-blind",
    "shallow-beer-lambert-blind",
    "shallow-scaled-exp-growth-blind",
    "shallow-scaled-exp-fast-decay-blind",
)

FORBIDDEN_PROOF_EVIDENCE = {
    "catalog_verified",
    "compile_only_verified",
    "same_ast",
}


@pytest.fixture(scope="module")
def shallow_proof_result(tmp_path_factory):
    base = load_suite("v1.5-shallow-proof")
    suite = type(base)(base.id, base.description, base.cases, tmp_path_factory.mktemp("shallow-proof") / "artifacts")
    result = run_benchmark_suite(suite)
    return result, aggregate_evidence(result)


def test_v15_shallow_blind_proof_suite_recovers_only_with_blind_training(shallow_proof_result):
    result, aggregate = shallow_proof_result

    assert [case.id for case in result.suite.cases] == list(EXPECTED_SHALLOW_CASE_IDS)
    assert len(result.results) == 18
    assert {run["case_id"] for run in aggregate["runs"]} == set(EXPECTED_SHALLOW_CASE_IDS)
    assert {"shallow-radioactive-decay-blind", "shallow-beer-lambert-blind"} <= {
        run["case_id"] for run in aggregate["runs"]
    }
    assert {
        "shallow-scaled-exp-growth-blind",
        "shallow-scaled-exp-fast-decay-blind",
    } <= {run["case_id"] for run in aggregate["runs"]}

    for item in result.results:
        artifact = json.loads(item.artifact_path.read_text(encoding="utf-8"))

        assert item.status == "recovered"
        assert artifact["status"] == "recovered"
        assert artifact["claim_status"] == "recovered"
        assert artifact["run"]["start_mode"] == "blind"
        assert artifact["training_mode"] == "blind_training"
        assert artifact["evidence_class"] == "blind_training_recovered"
        assert artifact["evidence_class"] not in FORBIDDEN_PROOF_EVIDENCE
        assert "compiled_eml" not in artifact
        assert "compiled_eml_verification" not in artifact
        assert "warm_start_eml" not in artifact
        assert "verification" not in artifact

