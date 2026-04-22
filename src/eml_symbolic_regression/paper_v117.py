"""v1.17 snap-first exact-recovery diagnostics and package helpers."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping


DEFAULT_V117_PACKAGE_DIR = Path("artifacts") / "paper" / "v1.17-geml"
DEFAULT_V117_SNAP_DIAGNOSTICS_DIR = DEFAULT_V117_PACKAGE_DIR / "snap-diagnostics"
DEFAULT_V116_CAMPAIGN_DIR = Path("artifacts") / "campaigns" / "v1.16-geml-pilot"


class V117PackageError(RuntimeError):
    """Raised when a v1.17 package artifact cannot be safely written."""


@dataclass(frozen=True)
class V117SnapDiagnosticPaths:
    output_dir: Path
    manifest_json: Path
    snap_diagnostics_json: Path
    snap_diagnostics_csv: Path
    snap_diagnostics_md: Path
    snap_neighborhood_seeds_json: Path
    source_locks_json: Path

    def as_dict(self) -> dict[str, str]:
        return {key: str(value) for key, value in self.__dict__.items()}


def v117_snap_diagnostic_paths(output_dir: Path = DEFAULT_V117_SNAP_DIAGNOSTICS_DIR) -> V117SnapDiagnosticPaths:
    output_dir = Path(output_dir)
    return V117SnapDiagnosticPaths(
        output_dir=output_dir,
        manifest_json=output_dir / "manifest.json",
        snap_diagnostics_json=output_dir / "snap-diagnostics.json",
        snap_diagnostics_csv=output_dir / "snap-diagnostics.csv",
        snap_diagnostics_md=output_dir / "snap-diagnostics.md",
        snap_neighborhood_seeds_json=output_dir / "snap-neighborhood-seeds.json",
        source_locks_json=output_dir / "source-locks.json",
    )


SNAP_DIAGNOSTIC_COLUMNS = [
    "diagnostic_id",
    "pair_id",
    "formula",
    "target_family",
    "seed",
    "operator_family",
    "candidate_role",
    "candidate_id",
    "fallback_candidate_id",
    "comparison_outcome",
    "trained_exact_recovery",
    "verification_outcome",
    "status",
    "snap_min_margin",
    "snap_active_node_count",
    "low_margin_slot_count",
    "lowest_margin_slots_json",
    "low_confidence_alternatives_json",
    "pre_snap_mse",
    "post_snap_mse",
    "post_snap_minus_soft_best",
    "post_snap_minus_pre_snap",
    "branch_cut_crossing_count",
    "branch_cut_proximity_count",
    "branch_input_count",
    "artifact_path",
    "snap_mismatch_class",
    "neighborhood_seed",
]


def write_v117_snap_diagnostics(
    output_dir: Path = DEFAULT_V117_SNAP_DIAGNOSTICS_DIR,
    *,
    campaign_dir: Path = DEFAULT_V116_CAMPAIGN_DIR,
    overwrite: bool = False,
    low_margin_threshold: float = 0.1,
) -> V117SnapDiagnosticPaths:
    """Write v1.17 snap diagnostics and deterministic neighborhood seed manifest."""

    output_dir = Path(output_dir)
    campaign_dir = Path(campaign_dir)
    paths = v117_snap_diagnostic_paths(output_dir)
    if paths.manifest_json.exists() and not overwrite:
        raise V117PackageError(f"{paths.manifest_json} already exists; pass overwrite=True to refresh")
    paths.output_dir.mkdir(parents=True, exist_ok=True)

    paired_rows = _read_csv(campaign_dir / "tables" / "geml-paired-comparison.csv")
    diagnostics = _snap_diagnostic_rows(paired_rows, low_margin_threshold=low_margin_threshold)
    seeds = _snap_neighborhood_seed_rows(diagnostics, low_margin_threshold=low_margin_threshold)
    locks = _source_locks_payload(
        [
            ("campaign_manifest", campaign_dir / "campaign-manifest.json", "input"),
            ("geml_paired_summary", campaign_dir / "tables" / "geml-paired-summary.json", "input"),
            ("geml_paired_comparison", campaign_dir / "tables" / "geml-paired-comparison.csv", "input"),
            ("runs_table", campaign_dir / "tables" / "runs.csv", "input"),
        ]
    )

    _write_json(paths.snap_diagnostics_json, {"schema": "eml.v117_snap_diagnostics.v1", "rows": diagnostics})
    _write_csv(paths.snap_diagnostics_csv, diagnostics, SNAP_DIAGNOSTIC_COLUMNS)
    paths.snap_diagnostics_md.write_text(_snap_diagnostics_markdown(diagnostics), encoding="utf-8")
    _write_json(
        paths.snap_neighborhood_seeds_json,
        {
            "schema": "eml.v117_snap_neighborhood_seeds.v1",
            "source": str(paths.snap_diagnostics_json),
            "low_margin_threshold": low_margin_threshold,
            "rows": seeds,
        },
    )
    locks["outputs"] = _source_locks(
        [
            ("snap_diagnostics_json", paths.snap_diagnostics_json, "output"),
            ("snap_diagnostics_csv", paths.snap_diagnostics_csv, "output"),
            ("snap_diagnostics_md", paths.snap_diagnostics_md, "output"),
            ("snap_neighborhood_seeds", paths.snap_neighborhood_seeds_json, "output"),
        ]
    )
    _write_json(paths.source_locks_json, locks)

    manifest = {
        "schema": "eml.v117_snap_diagnostics_manifest.v1",
        "generated_at": _now_iso(),
        "campaign_dir": str(campaign_dir),
        "outputs": paths.as_dict(),
        "counts": {
            "paired_rows": len(paired_rows),
            "diagnostic_rows": len(diagnostics),
            "neighborhood_seed_rows": len(seeds),
            "low_margin_rows": sum(1 for row in diagnostics if _as_float(row.get("snap_min_margin")) <= low_margin_threshold),
            "loss_only_rows": sum(1 for row in diagnostics if str(row.get("comparison_outcome") or "").endswith("lower_post_snap_mse")),
        },
        "source_locks": str(paths.source_locks_json),
        "source_locks_ok": all(row["status"] == "locked" for row in locks["inputs"]),
        "claim_boundary": "Snap diagnostics seed target-agnostic neighborhood search; they do not change verifier recovery definitions.",
    }
    _write_json(paths.manifest_json, manifest)
    return paths


def _snap_diagnostic_rows(
    paired_rows: Iterable[Mapping[str, Any]],
    *,
    low_margin_threshold: float,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for pair in paired_rows:
        for prefix, operator_family in (("raw", "raw_eml"), ("ipi", "ipi_eml")):
            candidate_id = str(pair.get(f"{prefix}_selected_candidate_id") or "")
            role = "selected" if candidate_id else "selected_unavailable"
            outcome = str(pair.get("comparison_outcome") or "")
            row = {
                "diagnostic_id": f"{pair.get('pair_id', '')}:{operator_family}:{role}",
                "pair_id": str(pair.get("pair_id") or ""),
                "formula": str(pair.get("formula") or ""),
                "target_family": str(pair.get("target_family") or ""),
                "seed": str(pair.get("seed") or ""),
                "operator_family": operator_family,
                "candidate_role": role,
                "candidate_id": candidate_id,
                "fallback_candidate_id": str(pair.get(f"{prefix}_fallback_candidate_id") or ""),
                "comparison_outcome": outcome,
                "trained_exact_recovery": _bool_text(pair.get(f"{prefix}_trained_exact_recovery")),
                "verification_outcome": str(pair.get(f"{prefix}_verification_outcome") or ""),
                "status": str(pair.get(f"{prefix}_status") or ""),
                "snap_min_margin": pair.get(f"{prefix}_snap_min_margin"),
                "snap_active_node_count": pair.get(f"{prefix}_snap_active_node_count"),
                "low_margin_slot_count": pair.get(f"{prefix}_low_margin_slot_count"),
                "lowest_margin_slots_json": _canonical_json_cell(pair.get(f"{prefix}_lowest_margin_slots_json")),
                "low_confidence_alternatives_json": _canonical_json_cell(pair.get(f"{prefix}_low_confidence_alternatives_json")),
                "pre_snap_mse": pair.get(f"{prefix}_pre_snap_mse"),
                "post_snap_mse": pair.get(f"{prefix}_post_snap_mse"),
                "post_snap_minus_soft_best": pair.get(f"{prefix}_post_snap_minus_soft_best"),
                "post_snap_minus_pre_snap": pair.get(f"{prefix}_post_snap_minus_pre_snap"),
                "branch_cut_crossing_count": pair.get(f"{prefix}_branch_cut_crossing_count"),
                "branch_cut_proximity_count": pair.get(f"{prefix}_branch_cut_proximity_count"),
                "branch_input_count": pair.get(f"{prefix}_branch_input_count"),
                "artifact_path": str(pair.get(f"{prefix}_artifact_path") or ""),
            }
            row["snap_mismatch_class"] = _snap_mismatch_class(row, outcome, low_margin_threshold=low_margin_threshold)
            row["neighborhood_seed"] = _is_neighborhood_seed(row, low_margin_threshold=low_margin_threshold)
            rows.append(row)
    return sorted(rows, key=_diagnostic_sort_key)


def _snap_neighborhood_seed_rows(
    diagnostics: Iterable[Mapping[str, Any]],
    *,
    low_margin_threshold: float,
) -> list[dict[str, Any]]:
    seeds: list[dict[str, Any]] = []
    for row in diagnostics:
        if not _is_neighborhood_seed(row, low_margin_threshold=low_margin_threshold):
            continue
        seeds.append(
            {
                "seed_id": f"{row.get('pair_id')}:{row.get('operator_family')}:{row.get('candidate_role')}",
                "pair_id": row.get("pair_id"),
                "formula": row.get("formula"),
                "target_family": row.get("target_family"),
                "seed": row.get("seed"),
                "operator_family": row.get("operator_family"),
                "candidate_id": row.get("candidate_id"),
                "fallback_candidate_id": row.get("fallback_candidate_id"),
                "comparison_outcome": row.get("comparison_outcome"),
                "snap_min_margin": row.get("snap_min_margin"),
                "low_margin_slot_count": row.get("low_margin_slot_count"),
                "lowest_margin_slots_json": row.get("lowest_margin_slots_json"),
                "low_confidence_alternatives_json": row.get("low_confidence_alternatives_json"),
                "artifact_path": row.get("artifact_path"),
                "source": "v1.17_snap_diagnostics",
                "target_formula_leakage": False,
            }
        )
    return sorted(seeds, key=_seed_sort_key)


def _is_neighborhood_seed(row: Mapping[str, Any], *, low_margin_threshold: float) -> bool:
    outcome = str(row.get("comparison_outcome") or "")
    if outcome in {"ipi_recovery_win", "raw_recovery_win", "both_recovered"}:
        return False
    if outcome.endswith("lower_post_snap_mse") or outcome == "neutral_no_recovery":
        return True
    return _as_float(row.get("snap_min_margin"), default=math.inf) <= low_margin_threshold


def _snap_mismatch_class(row: Mapping[str, Any], outcome: str, *, low_margin_threshold: float) -> str:
    if outcome in {"ipi_recovery_win", "raw_recovery_win", "both_recovered"}:
        return "exact_recovery_signal"
    if _as_float(row.get("branch_cut_crossing_count")) > 0:
        return "branch_pathology"
    if _as_float(row.get("snap_min_margin"), default=math.inf) <= low_margin_threshold or _as_float(row.get("low_margin_slot_count")) > 0:
        return "low_margin_snap_mismatch"
    if _as_float(row.get("post_snap_minus_soft_best")) > 0 or _as_float(row.get("post_snap_minus_pre_snap")) > 0:
        return "hard_snap_degradation"
    if outcome.endswith("lower_post_snap_mse"):
        return "loss_only_snap_candidate"
    return "verifier_or_optimization_miss"


def _diagnostic_sort_key(row: Mapping[str, Any]) -> tuple[Any, ...]:
    return (
        0 if bool(row.get("neighborhood_seed")) else 1,
        _as_float(row.get("snap_min_margin"), default=math.inf),
        str(row.get("formula") or ""),
        str(row.get("seed") or ""),
        str(row.get("operator_family") or ""),
        str(row.get("candidate_id") or ""),
    )


def _seed_sort_key(row: Mapping[str, Any]) -> tuple[Any, ...]:
    outcome = str(row.get("comparison_outcome") or "")
    priority = 0 if outcome.endswith("lower_post_snap_mse") else 1
    return (
        priority,
        _as_float(row.get("snap_min_margin"), default=math.inf),
        str(row.get("formula") or ""),
        str(row.get("seed") or ""),
        str(row.get("operator_family") or ""),
        str(row.get("candidate_id") or ""),
    )


def _snap_diagnostics_markdown(rows: Iterable[Mapping[str, Any]]) -> str:
    lines = [
        "# v1.17 Snap Diagnostics",
        "",
        "Snap diagnostics are explanatory only. Exact recovery remains verifier-owned.",
        "",
        "| Pair | Operator | Outcome | Margin | Low Slots | Class | Seed |",
        "|------|----------|---------|--------|-----------|-------|------|",
    ]
    for row in rows:
        lines.append(
            f"| {row.get('pair_id')} | {row.get('operator_family')} | {row.get('comparison_outcome')} | "
            f"{row.get('snap_min_margin')} | {row.get('low_margin_slot_count')} | "
            f"{row.get('snap_mismatch_class')} | {row.get('neighborhood_seed')} |"
        )
    lines.append("")
    return "\n".join(lines)


def _canonical_json_cell(value: Any) -> str:
    if value in (None, ""):
        return ""
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return value
        return json.dumps(parsed, sort_keys=True, separators=(",", ":"))
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _bool_text(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).lower() in {"true", "1", "yes", "recovered"}


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: "" if row.get(key) is None else row.get(key) for key in fieldnames})


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _source_locks_payload(items: Iterable[tuple[str, Path, str]]) -> dict[str, Any]:
    locks = _source_locks(items)
    return {
        "schema": "eml.v117_source_locks.v1",
        "generated_at": _now_iso(),
        "inputs": [row for row in locks if row["role"] == "input"],
        "outputs": [row for row in locks if row["role"] == "output"],
    }


def _source_locks(items: Iterable[tuple[str, Path, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, role in items:
        path = Path(path)
        if path.is_file():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            status = "locked"
            size = path.stat().st_size
        else:
            digest = None
            status = "missing"
            size = 0
        rows.append({"source_id": source_id, "path": str(path), "role": role, "status": status, "sha256": digest, "bytes": size})
    return rows


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
