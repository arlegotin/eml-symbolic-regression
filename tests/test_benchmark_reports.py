from eml_symbolic_regression.benchmark import (
    RunFilter,
    aggregate_evidence,
    builtin_suite,
    render_aggregate_markdown,
    run_benchmark_suite,
    write_aggregate_reports,
)


def test_aggregate_evidence_separates_unsupported_and_same_ast(tmp_path):
    base = builtin_suite("smoke")
    suite = type(base)(base.id, base.description, base.cases, tmp_path / "artifacts")

    result = run_benchmark_suite(suite, run_filter=RunFilter(case_ids=("beer-warm", "planck-diagnostic")))
    aggregate = aggregate_evidence(result)

    assert aggregate["schema"] == "eml.benchmark_aggregate.v1"
    assert aggregate["counts"]["total"] == 2
    assert aggregate["counts"]["unsupported"] == 1
    assert aggregate["counts"]["same_ast_return"] == 1
    assert aggregate["counts"]["verifier_recovered"] == 1
    assert {run["classification"] for run in aggregate["runs"]} == {"same_ast_warm_start_return", "unsupported"}


def test_write_aggregate_reports_outputs_json_and_markdown(tmp_path):
    base = builtin_suite("smoke")
    suite = type(base)(base.id, base.description, base.cases, tmp_path / "artifacts")
    result = run_benchmark_suite(suite, run_filter=RunFilter(case_ids=("planck-diagnostic",)))

    paths = write_aggregate_reports(result)

    assert paths["json"].exists()
    assert paths["markdown"].exists()
    markdown = paths["markdown"].read_text()
    assert "# Benchmark Evidence: smoke" in markdown
    assert "| planck |" in markdown


def test_markdown_report_contains_run_artifact_paths(tmp_path):
    base = builtin_suite("smoke")
    suite = type(base)(base.id, base.description, base.cases, tmp_path / "artifacts")
    result = run_benchmark_suite(suite, run_filter=RunFilter(case_ids=("planck-diagnostic",)))

    markdown = render_aggregate_markdown(aggregate_evidence(result))

    assert "planck-diagnostic" in markdown
    assert ".json" in markdown


def test_smoke_benchmark_exercises_required_paths_and_aggregate(tmp_path):
    base = builtin_suite("smoke")
    suite = type(base)(base.id, base.description, base.cases, tmp_path / "artifacts")

    result = run_benchmark_suite(suite)
    paths = write_aggregate_reports(result)
    aggregate = aggregate_evidence(result)

    assert {run.start_mode for run in (item.run for item in result.results)} == {"blind", "warm_start", "compile"}
    assert {"recovered", "snapped_but_failed", "same_ast_return", "unsupported"} >= {item.status for item in result.results}
    assert aggregate["counts"]["total"] == 3
    assert aggregate["counts"]["verifier_recovered"] == 2
    assert aggregate["counts"]["unsupported"] == 1
    assert aggregate["counts"]["same_ast_return"] == 1
    assert aggregate["counts"]["failed"] == 0
    assert paths["json"].exists()
    assert paths["markdown"].exists()
