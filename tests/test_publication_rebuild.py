import json

from eml_symbolic_regression.cli import build_parser, publication_rebuild_command
from eml_symbolic_regression.publication import validate_publication_package, write_publication_rebuild


def _json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_publication_rebuild_smoke_writes_manifest_locks_and_validation(tmp_path):
    paths = write_publication_rebuild(
        output_dir=tmp_path / "paper",
        smoke=True,
        overwrite=True,
        allow_dirty=True,
        command="PYTHONPATH=src python -m eml_symbolic_regression.cli publication-rebuild --smoke",
    )

    manifest = _json(paths.manifest_json)
    source_locks = _json(paths.source_locks_json)
    validation = _json(paths.validation_json)

    assert manifest["schema"] == "eml.v113_publication_rebuild.v1"
    assert manifest["mode"] == "smoke"
    assert manifest["git"]["revision"]
    assert manifest["environment"]["python"]
    assert manifest["environment"]["lockfile"]["path"] == "requirements-lock.txt"
    assert source_locks["schema"] == "eml.v113_publication_source_locks.v1"
    assert source_locks["input_count"] >= 3
    assert validation["status"] == "passed"
    assert manifest["validation"]["status"] == "passed"
    assert all(row["sha256"] and row["bytes"] > 0 for row in manifest["inputs"])
    assert all(row["sha256"] and row["bytes"] > 0 for row in manifest["outputs"])


def test_publication_rebuild_cli_writes_package(tmp_path, capsys):
    output_dir = tmp_path / "paper"
    args = build_parser().parse_args(
        [
            "publication-rebuild",
            "--output-dir",
            str(output_dir),
            "--smoke",
            "--overwrite",
            "--allow-dirty",
        ]
    )

    assert args.func is publication_rebuild_command
    assert args.func(args) == 0

    captured = capsys.readouterr().out
    assert "publication rebuild: manifest ->" in captured
    assert "(passed)" in captured
    assert (output_dir / "manifest.json").exists()
    assert (output_dir / "validation.json").exists()


def test_publication_validation_rejects_placeholder_metadata(tmp_path):
    paths = write_publication_rebuild(output_dir=tmp_path / "paper", smoke=True, overwrite=True, allow_dirty=True)
    bad_artifact = paths.output_dir / "bad.json"
    bad_artifact.write_text('{"generated_at": "1970-01-01T00:00:00+00:00", "code_version": "snapshot"}\n', encoding="utf-8")

    validation = validate_publication_package(paths.output_dir)

    assert validation["status"] == "failed"
    checks = {check["id"]: check for check in validation["checks"]}
    violations = checks["placeholder_metadata_rejected"]["details"]["violations"]
    assert {"path": "bad.json", "token": "1970-01-01T00:00:00+00:00"} in violations
    assert {"path": "bad.json", "token": '"snapshot"'} in violations


def test_publication_validation_allows_explicit_deterministic_fixture(tmp_path):
    paths = write_publication_rebuild(output_dir=tmp_path / "paper", smoke=True, overwrite=True, allow_dirty=True)
    fixture = paths.output_dir / "fixtures" / "stable.json"
    fixture.parent.mkdir()
    fixture.write_text('{"generated_at": "1970-01-01T00:00:00+00:00", "code_version": "snapshot"}\n', encoding="utf-8")

    validation = validate_publication_package(paths.output_dir, allowed_placeholder_paths=("fixtures/stable.json",))

    assert validation["status"] == "passed"
