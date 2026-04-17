"""Raw-hybrid paper package synthesis from locked evidence artifacts."""

from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


RAW_HYBRID_PAPER_PRESET_ID = "v1.9-raw-hybrid-paper"
DEFAULT_RAW_HYBRID_OUTPUT_DIR = Path("artifacts") / "paper" / "v1.9" / "raw-hybrid"


class RawHybridPaperError(RuntimeError):
    """Raised when the raw-hybrid paper package cannot be generated safely."""


@dataclass(frozen=True, kw_only=True)
class RawHybridSource:
    source_id: str
    role: str
    path: Path
    required: bool = True
    preset_id: str = RAW_HYBRID_PAPER_PRESET_ID
    description: str = ""
    law: str | None = None
    evidence_regime: str | None = None

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "preset_id": self.preset_id,
            "source_id": self.source_id,
            "role": self.role,
            "path": str(self.path),
            "required": self.required,
        }
        if self.description:
            payload["description"] = self.description
        if self.law is not None:
            payload["law"] = self.law
        if self.evidence_regime is not None:
            payload["evidence_regime"] = self.evidence_regime
        return payload


@dataclass(frozen=True)
class RawHybridPaperPaths:
    output_dir: Path
    manifest_json: Path
    source_locks_json: Path
    regime_summary_json: Path
    raw_hybrid_report_md: Path
    scientific_law_table_json: Path
    scientific_law_table_csv: Path
    scientific_law_table_md: Path
    claim_boundaries_md: Path
    centered_negative_diagnostics_md: Path

    def as_dict(self) -> dict[str, str]:
        return {
            "output_dir": str(self.output_dir),
            "manifest_json": str(self.manifest_json),
            "source_locks_json": str(self.source_locks_json),
            "regime_summary_json": str(self.regime_summary_json),
            "raw_hybrid_report_md": str(self.raw_hybrid_report_md),
            "scientific_law_table_json": str(self.scientific_law_table_json),
            "scientific_law_table_csv": str(self.scientific_law_table_csv),
            "scientific_law_table_md": str(self.scientific_law_table_md),
            "claim_boundaries_md": str(self.claim_boundaries_md),
            "centered_negative_diagnostics_md": str(self.centered_negative_diagnostics_md),
        }


def default_raw_hybrid_sources() -> tuple[RawHybridSource, ...]:
    """Return the locked evidence inputs for the v1.9 raw-hybrid paper package."""

    proof_root = Path("artifacts") / "proof" / "v1.6" / "campaigns"
    v18_paper = Path("artifacts") / "paper" / "v1.8"
    arrhenius_root = Path("artifacts") / "campaigns" / "v1.9-arrhenius-evidence" / "v1.9-arrhenius-evidence"
    michaelis_root = Path("artifacts") / "campaigns" / "v1.9-michaelis-evidence" / "v1.9-michaelis-evidence"
    repair_root = Path("artifacts") / "campaigns" / "v1.9-repair-evidence"
    standard_runs = Path("artifacts") / "campaigns" / "v1.6-standard" / "runs" / "v1.3-standard"
    return (
        RawHybridSource(
            source_id="proof-shallow-pure-blind-aggregate",
            role="proof_aggregate",
            path=proof_root / "proof-shallow-pure-blind" / "aggregate.json",
            description="v1.6 shallow pure-blind measured boundary aggregate.",
            evidence_regime="pure_blind",
        ),
        RawHybridSource(
            source_id="proof-shallow-scaffolded-aggregate",
            role="proof_aggregate",
            path=proof_root / "proof-shallow" / "aggregate.json",
            description="v1.6 shallow scaffolded recovery aggregate.",
            evidence_regime="scaffolded",
        ),
        RawHybridSource(
            source_id="proof-perturbed-basin-aggregate",
            role="proof_aggregate",
            path=proof_root / "proof-basin" / "aggregate.json",
            description="v1.6 perturbed true-tree basin aggregate.",
            evidence_regime="perturbed_basin",
        ),
        RawHybridSource(
            source_id="proof-basin-probes-aggregate",
            role="proof_aggregate",
            path=proof_root / "proof-basin-probes" / "aggregate.json",
            description="v1.6 Beer-Lambert basin probe aggregate with repaired candidates separated.",
            evidence_regime="perturbed_basin",
        ),
        RawHybridSource(
            source_id="proof-depth-curve-aggregate",
            role="proof_aggregate",
            path=proof_root / "proof-depth-curve" / "aggregate.json",
            description="v1.6 depth-curve measured boundary aggregate.",
            evidence_regime="pure_blind",
        ),
        RawHybridSource(
            source_id="v1.8-centered-decision-json",
            role="centered_negative_diagnostic",
            path=v18_paper / "decision-memo.json",
            description="v1.8 centered-family decision payload.",
        ),
        RawHybridSource(
            source_id="v1.8-centered-decision-markdown",
            role="centered_negative_diagnostic",
            path=v18_paper / "decision-memo.md",
            description="v1.8 centered-family decision memo.",
        ),
        RawHybridSource(
            source_id="v1.8-centered-completeness-boundary",
            role="centered_negative_diagnostic",
            path=v18_paper / "completeness-boundary.md",
            description="v1.8 centered-family completeness caveat.",
        ),
        RawHybridSource(
            source_id="v1.9-arrhenius-aggregate",
            role="scientific_law_aggregate",
            path=arrhenius_root / "aggregate.json",
            description="v1.9 Arrhenius exact compiler warm-start aggregate.",
            law="arrhenius",
            evidence_regime="same_ast_return",
        ),
        RawHybridSource(
            source_id="v1.9-arrhenius-run",
            role="scientific_law_run",
            path=arrhenius_root / "v1-9-arrhenius-evidence-arrhenius-warm-75f6e9c1764d.json",
            description="v1.9 Arrhenius exact compiler warm-start run artifact.",
            law="arrhenius",
            evidence_regime="same_ast_return",
        ),
        RawHybridSource(
            source_id="v1.9-michaelis-aggregate",
            role="scientific_law_aggregate",
            path=michaelis_root / "aggregate.json",
            description="v1.9 Michaelis-Menten exact compiler warm-start aggregate.",
            law="michaelis_menten",
            evidence_regime="same_ast_return",
        ),
        RawHybridSource(
            source_id="v1.9-michaelis-run",
            role="scientific_law_run",
            path=michaelis_root / "v1-9-michaelis-evidence-michaelis-warm-a67d8ccfb108.json",
            description="v1.9 Michaelis-Menten exact compiler warm-start run artifact.",
            law="michaelis_menten",
            evidence_regime="same_ast_return",
        ),
        RawHybridSource(
            source_id="v1.9-repair-aggregate",
            role="repair_evidence",
            path=repair_root / "v1.9-repair-evidence" / "aggregate.json",
            description="v1.9 expanded cleanup repair evidence aggregate.",
            evidence_regime="repaired",
        ),
        RawHybridSource(
            source_id="v1.9-repair-summary-json",
            role="repair_evidence",
            path=repair_root / "repair-evidence-summary.json",
            description="v1.9 expanded cleanup repair summary payload.",
            evidence_regime="repaired",
        ),
        RawHybridSource(
            source_id="v1.9-repair-summary-markdown",
            role="repair_evidence",
            path=repair_root / "repair-evidence-summary.md",
            description="v1.9 expanded cleanup repair summary report.",
            evidence_regime="repaired",
        ),
        RawHybridSource(
            source_id="v1.6-beer-lambert-run",
            role="scientific_law_run",
            path=standard_runs / "v1-3-standard-beer-perturbation-sweep-c671cedf25f1.json",
            description="v1.6 Beer-Lambert warm-start/same-AST diagnostic run artifact.",
            law="beer_lambert",
            evidence_regime="same_ast_return",
        ),
        RawHybridSource(
            source_id="v1.6-shockley-run",
            role="scientific_law_run",
            path=standard_runs / "v1-3-standard-shockley-warm-316f98a5b1fb.json",
            description="v1.6 Shockley warm-start/same-AST diagnostic run artifact.",
            law="shockley",
            evidence_regime="same_ast_return",
        ),
        RawHybridSource(
            source_id="v1.6-planck-diagnostic-run",
            role="scientific_law_run",
            path=standard_runs / "v1-3-standard-planck-diagnostic-2309e6363fc8.json",
            description="v1.6 Planck unsupported compile diagnostic run artifact.",
            law="planck",
            evidence_regime="compile_only",
        ),
        RawHybridSource(
            source_id="v1.6-logistic-diagnostic-run",
            role="scientific_law_run",
            path=standard_runs / "v1-3-standard-logistic-compile-a99c41f57b97.json",
            description="v1.6 logistic unsupported compile diagnostic run artifact.",
            law="logistic",
            evidence_regime="compile_only",
        ),
        RawHybridSource(
            source_id="v1.6-historical-michaelis-diagnostic-run",
            role="scientific_law_run",
            path=standard_runs / "v1-3-standard-michaelis-warm-diagnostic-9917f8383370.json",
            description="v1.6 historical Michaelis unsupported before/after diagnostic run artifact.",
            law="michaelis_menten_historical",
            evidence_regime="historical_context",
        ),
    )


def write_raw_hybrid_paper_package(
    *,
    output_dir: Path = DEFAULT_RAW_HYBRID_OUTPUT_DIR,
    require_existing: bool = True,
    overwrite: bool = False,
    reproduction_command: str | None = None,
) -> RawHybridPaperPaths:
    """Write the raw-hybrid paper package from existing evidence artifacts."""

    output_dir = Path(output_dir)
    sources = default_raw_hybrid_sources()
    source_payloads = _load_sources(sources, require_existing=require_existing)
    _prepare_output_dir(output_dir, overwrite=overwrite)

    paths = _package_paths(output_dir)
    locks = {
        "schema": "eml.raw_hybrid_source_locks.v1",
        "preset_id": RAW_HYBRID_PAPER_PRESET_ID,
        "generated_at": _now_iso(),
        "sources": [_source_lock(source) for source in sources if source.path.exists()],
    }
    manifest = _manifest_payload(
        paths,
        sources=sources,
        source_payloads=source_payloads,
        reproduction_command=reproduction_command
        or f"PYTHONPATH=src python -m eml_symbolic_regression.cli raw-hybrid-paper --output-dir {output_dir}",
    )

    _write_json(paths.source_locks_json, locks)
    _write_json(paths.manifest_json, manifest)
    return paths


def _package_paths(output_dir: Path) -> RawHybridPaperPaths:
    return RawHybridPaperPaths(
        output_dir=output_dir,
        manifest_json=output_dir / "manifest.json",
        source_locks_json=output_dir / "source-locks.json",
        regime_summary_json=output_dir / "regime-summary.json",
        raw_hybrid_report_md=output_dir / "raw-hybrid-report.md",
        scientific_law_table_json=output_dir / "scientific-law-table.json",
        scientific_law_table_csv=output_dir / "scientific-law-table.csv",
        scientific_law_table_md=output_dir / "scientific-law-table.md",
        claim_boundaries_md=output_dir / "claim-boundaries.md",
        centered_negative_diagnostics_md=output_dir / "centered-negative-diagnostics.md",
    )


def _prepare_output_dir(output_dir: Path, *, overwrite: bool) -> None:
    if output_dir.exists() and any(output_dir.iterdir()):
        if not overwrite:
            raise RawHybridPaperError(f"output directory is not empty: {output_dir}")
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)


def _load_sources(sources: tuple[RawHybridSource, ...], *, require_existing: bool) -> dict[str, Any]:
    payloads: dict[str, Any] = {}
    for source in sources:
        if not source.path.exists():
            if require_existing and source.required:
                raise RawHybridPaperError(f"missing required source {source.source_id}: {source.path}")
            continue
        if not source.path.is_file():
            raise RawHybridPaperError(f"source must be a file, not a directory, for {source.source_id}: {source.path}")
        if source.path.suffix == ".json":
            try:
                payloads[source.source_id] = json.loads(source.path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                raise RawHybridPaperError(f"invalid JSON in source {source.source_id}: {source.path}") from exc
    return payloads


def _manifest_payload(
    paths: RawHybridPaperPaths,
    *,
    sources: tuple[RawHybridSource, ...],
    source_payloads: Mapping[str, Any],
    reproduction_command: str,
) -> dict[str, Any]:
    return {
        "schema": "eml.raw_hybrid_paper.v1",
        "preset_id": RAW_HYBRID_PAPER_PRESET_ID,
        "generated_at": _now_iso(),
        "output_dir": str(paths.output_dir),
        "reproducibility": {"command": reproduction_command},
        "source_locks": str(paths.source_locks_json),
        "outputs": paths.as_dict(),
        "sources": [source.as_dict() for source in sources],
        "loaded_json_sources": sorted(source_payloads),
    }


def _source_lock(source: RawHybridSource) -> dict[str, Any]:
    if not source.path.is_file():
        raise RawHybridPaperError(f"cannot hash non-file source {source.source_id}: {source.path}")
    row = source.as_dict()
    row["sha256"] = _sha256(source.path)
    return row


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
