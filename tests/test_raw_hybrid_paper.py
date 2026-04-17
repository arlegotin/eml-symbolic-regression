import hashlib
import json
from pathlib import Path

import pytest

from eml_symbolic_regression.raw_hybrid_paper import (
    RAW_HYBRID_PAPER_PRESET_ID,
    RawHybridPaperError,
    RawHybridSource,
    default_raw_hybrid_sources,
    write_raw_hybrid_paper_package,
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def test_default_raw_hybrid_sources_cover_required_evidence():
    sources = default_raw_hybrid_sources()
    source_ids = {source.source_id for source in sources}

    assert {source.preset_id for source in sources} == {RAW_HYBRID_PAPER_PRESET_ID}
    assert {
        "proof-shallow-pure-blind-aggregate",
        "proof-shallow-scaffolded-aggregate",
        "proof-perturbed-basin-aggregate",
        "proof-basin-probes-aggregate",
        "proof-depth-curve-aggregate",
        "v1.8-centered-decision-json",
        "v1.8-centered-decision-markdown",
        "v1.8-centered-completeness-boundary",
        "v1.9-arrhenius-aggregate",
        "v1.9-arrhenius-run",
        "v1.9-michaelis-aggregate",
        "v1.9-michaelis-run",
        "v1.9-repair-aggregate",
        "v1.9-repair-summary-json",
        "v1.6-beer-lambert-run",
        "v1.6-shockley-run",
        "v1.6-planck-diagnostic-run",
        "v1.6-logistic-diagnostic-run",
    } <= source_ids
    assert all(source.required for source in sources)
    assert all(source.path.suffix in {".json", ".md"} for source in sources)
    assert all(source.path.is_file() for source in sources)


def test_raw_hybrid_package_fails_closed_on_missing_required_source(tmp_path, monkeypatch):
    missing = tmp_path / "missing" / "aggregate.json"
    monkeypatch.setattr(
        "eml_symbolic_regression.raw_hybrid_paper.default_raw_hybrid_sources",
        lambda: (
            RawHybridSource(
                source_id="missing-required",
                role="proof_aggregate",
                path=missing,
                required=True,
            ),
        ),
    )

    with pytest.raises(RawHybridPaperError) as exc:
        write_raw_hybrid_paper_package(output_dir=tmp_path / "paper", require_existing=True)

    assert "missing-required" in str(exc.value)
    assert str(missing) in str(exc.value)


def test_raw_hybrid_source_locks_hash_specific_files(tmp_path):
    paths = write_raw_hybrid_paper_package(
        output_dir=tmp_path / "paper",
        require_existing=True,
        reproduction_command="PYTHONPATH=src python -m eml_symbolic_regression.cli raw-hybrid-paper --output-dir out",
    )

    locks = json.loads(paths.source_locks_json.read_text(encoding="utf-8"))

    assert locks["schema"] == "eml.raw_hybrid_source_locks.v1"
    assert locks["preset_id"] == RAW_HYBRID_PAPER_PRESET_ID
    assert locks["sources"]
    for row in locks["sources"]:
        path = Path(row["path"])
        assert path.is_file()
        assert row["source_id"]
        assert row["role"]
        assert row["required"] is True
        assert row["sha256"] == _sha256(path)


def test_raw_hybrid_manifest_records_package_contract(tmp_path):
    paths = write_raw_hybrid_paper_package(
        output_dir=tmp_path / "paper",
        require_existing=True,
        reproduction_command="PYTHONPATH=src python -m eml_symbolic_regression.cli raw-hybrid-paper --output-dir out",
    )

    manifest = json.loads(paths.manifest_json.read_text(encoding="utf-8"))

    assert manifest["schema"] == "eml.raw_hybrid_paper.v1"
    assert manifest["preset_id"] == RAW_HYBRID_PAPER_PRESET_ID
    assert manifest["reproducibility"]["command"] == (
        "PYTHONPATH=src python -m eml_symbolic_regression.cli raw-hybrid-paper --output-dir out"
    )
    assert manifest["source_locks"] == str(paths.source_locks_json)
    assert manifest["outputs"]["manifest_json"] == str(paths.manifest_json)
    assert manifest["outputs"]["source_locks_json"] == str(paths.source_locks_json)
