"""Campaign presets and reproducible output manifests for benchmark evidence."""

from __future__ import annotations

import json
import platform
import csv
import statistics
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .benchmark import (
    BenchmarkSuite,
    RunFilter,
    _code_version,
    aggregate_evidence,
    load_suite,
    run_benchmark_suite,
    write_aggregate_reports,
)


DEFAULT_CAMPAIGN_ROOT = Path("artifacts") / "campaigns"


class CampaignOutputExistsError(FileExistsError):
    """Raised when a campaign would overwrite evidence without opt-in."""


@dataclass(frozen=True)
class CampaignPreset:
    name: str
    suite: str
    tier: str
    description: str
    budget_guardrail: str

    def as_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "suite": self.suite,
            "tier": self.tier,
            "description": self.description,
            "budget_guardrail": self.budget_guardrail,
        }


@dataclass(frozen=True)
class CampaignResult:
    preset: CampaignPreset
    campaign_dir: Path
    manifest_path: Path
    suite_result_path: Path
    aggregate_paths: Mapping[str, Path]
    table_paths: Mapping[str, Path] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "preset": self.preset.as_dict(),
            "campaign_dir": str(self.campaign_dir),
            "manifest_path": str(self.manifest_path),
            "suite_result_path": str(self.suite_result_path),
            "aggregate_paths": {key: str(value) for key, value in self.aggregate_paths.items()},
            "table_paths": {key: str(value) for key, value in self.table_paths.items()},
        }


_PRESETS = {
    "smoke": CampaignPreset(
        name="smoke",
        suite="smoke",
        tier="ci",
        description="Fast campaign for CI and development checks.",
        budget_guardrail="3 runs; shallow blind baseline, one warm-start recovery path, one unsupported diagnostic.",
    ),
    "standard": CampaignPreset(
        name="standard",
        suite="v1.3-standard",
        tier="showcase-default",
        description="Default evidence campaign for crisp numbers, tables, plots, and report narrative.",
        budget_guardrail="16 runs; shallow blind baselines, Beer-Lambert perturbations, and selected FOR_DEMO diagnostics.",
    ),
    "showcase": CampaignPreset(
        name="showcase",
        suite="v1.3-showcase",
        tier="expanded",
        description="Expanded campaign for presentation-grade evidence with more seeds and perturbation levels.",
        budget_guardrail="29 runs; larger blind and perturbation matrix plus full FOR_DEMO diagnostics.",
    ),
}


def list_campaign_presets() -> tuple[str, ...]:
    return tuple(_PRESETS)


def campaign_preset(name: str) -> CampaignPreset:
    try:
        return _PRESETS[name]
    except KeyError as exc:
        raise ValueError(f"unknown campaign preset {name!r}") from exc


def run_campaign(
    preset_name: str,
    *,
    output_root: Path = DEFAULT_CAMPAIGN_ROOT,
    label: str | None = None,
    overwrite: bool = False,
    run_filter: RunFilter | None = None,
) -> CampaignResult:
    preset = campaign_preset(preset_name)
    campaign_dir = _campaign_dir(output_root, preset.name, label)
    if campaign_dir.exists() and not overwrite:
        raise CampaignOutputExistsError(
            f"{campaign_dir} already exists; choose a new --label or pass --overwrite to replace campaign-level outputs"
        )
    campaign_dir.mkdir(parents=True, exist_ok=True)

    base_suite = load_suite(preset.suite)
    suite = BenchmarkSuite(
        id=base_suite.id,
        description=base_suite.description,
        cases=base_suite.cases,
        artifact_root=campaign_dir / "runs",
        schema=base_suite.schema,
    )
    result = run_benchmark_suite(suite, run_filter=run_filter)
    suite_result_path = campaign_dir / "suite-result.json"
    _write_json(suite_result_path, result.as_dict())
    aggregate_paths = write_aggregate_reports(result, campaign_dir)
    aggregate = aggregate_evidence(result)
    table_paths = write_campaign_tables(aggregate, campaign_dir / "tables")

    manifest = _manifest_payload(
        preset=preset,
        suite=suite,
        campaign_dir=campaign_dir,
        label=label,
        overwrite=overwrite,
        run_filter=run_filter,
        aggregate=aggregate,
        suite_result_path=suite_result_path,
        aggregate_paths=aggregate_paths,
        table_paths=table_paths,
    )
    manifest_path = campaign_dir / "campaign-manifest.json"
    _write_json(manifest_path, manifest)
    return CampaignResult(
        preset=preset,
        campaign_dir=campaign_dir,
        manifest_path=manifest_path,
        suite_result_path=suite_result_path,
        aggregate_paths=aggregate_paths,
        table_paths=table_paths,
    )


def write_campaign_tables(aggregate: Mapping[str, Any], output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    runs = list(aggregate.get("runs", ()))

    paths = {
        "runs_csv": output_dir / "runs.csv",
        "group_formula_csv": output_dir / "group-formula.csv",
        "group_start_mode_csv": output_dir / "group-start-mode.csv",
        "group_perturbation_noise_csv": output_dir / "group-perturbation-noise.csv",
        "group_depth_csv": output_dir / "group-depth.csv",
        "group_failure_class_csv": output_dir / "group-failure-class.csv",
        "headline_json": output_dir / "headline-metrics.json",
        "headline_csv": output_dir / "headline-metrics.csv",
        "failures_csv": output_dir / "failures.csv",
    }

    run_rows = [_run_csv_row(run) for run in runs]
    _write_csv(paths["runs_csv"], run_rows, _RUN_COLUMNS)

    _write_csv(paths["group_formula_csv"], _group_rows(runs, "formula"), _GROUP_COLUMNS)
    _write_csv(paths["group_start_mode_csv"], _group_rows(runs, "start_mode"), _GROUP_COLUMNS)
    _write_csv(paths["group_perturbation_noise_csv"], _group_rows(runs, "perturbation_noise"), _GROUP_COLUMNS)
    _write_csv(paths["group_depth_csv"], _group_rows(runs, lambda run: run.get("optimizer", {}).get("depth")), _GROUP_COLUMNS)
    _write_csv(paths["group_failure_class_csv"], _group_rows(runs, "classification"), _GROUP_COLUMNS)

    headline = _headline_metrics(runs)
    _write_json(paths["headline_json"], headline)
    _write_csv(paths["headline_csv"], [headline], list(headline))

    failures = [
        {
            "run_id": run.get("run_id"),
            "formula": run.get("formula"),
            "start_mode": run.get("start_mode"),
            "classification": run.get("classification"),
            "status": run.get("status"),
            "reason": run.get("reason"),
            "artifact_path": run.get("artifact_path"),
        }
        for run in runs
        if run.get("classification") in {"unsupported", "failed", "snapped_but_failed", "soft_fit_only", "execution_failure"}
    ]
    _write_csv(paths["failures_csv"], failures, _FAILURE_COLUMNS)
    return paths


def _campaign_dir(output_root: Path, preset_name: str, label: str | None) -> Path:
    folder = label or f"{preset_name}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    return output_root / folder


def _manifest_payload(
    *,
    preset: CampaignPreset,
    suite: BenchmarkSuite,
    campaign_dir: Path,
    label: str | None,
    overwrite: bool,
    run_filter: RunFilter | None,
    aggregate: Mapping[str, Any],
    suite_result_path: Path,
    aggregate_paths: Mapping[str, Path],
    table_paths: Mapping[str, Path],
) -> dict[str, Any]:
    filter_payload = _filter_payload(run_filter)
    command = _reproduction_command(preset.name, campaign_dir.parent, label, overwrite, filter_payload)
    return {
        "schema": "eml.campaign_manifest.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "preset": preset.as_dict(),
        "suite": suite.as_dict(),
        "run_filter": filter_payload,
        "counts": aggregate["counts"],
        "output": {
            "campaign_dir": str(campaign_dir),
            "raw_run_root": str(suite.artifact_root / suite.id),
            "suite_result": str(suite_result_path),
            "aggregate_json": str(aggregate_paths["json"]),
            "aggregate_markdown": str(aggregate_paths["markdown"]),
            "tables": {key: str(value) for key, value in table_paths.items()},
        },
        "reproducibility": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "code_version": _code_version(),
            "command": command,
            "overwrite": overwrite,
        },
    }


def _filter_payload(run_filter: RunFilter | None) -> dict[str, list[Any]]:
    run_filter = run_filter or RunFilter()
    return {
        "formulas": list(run_filter.formulas),
        "start_modes": list(run_filter.start_modes),
        "case_ids": list(run_filter.case_ids),
        "seeds": list(run_filter.seeds),
    }


def _reproduction_command(
    preset_name: str,
    output_root: Path,
    label: str | None,
    overwrite: bool,
    run_filter: Mapping[str, list[Any]],
) -> str:
    parts = [
        "PYTHONPATH=src",
        "python",
        "-m",
        "eml_symbolic_regression.cli",
        "campaign",
        preset_name,
        "--output-root",
        str(output_root),
    ]
    if label:
        parts.extend(["--label", label])
    if overwrite:
        parts.append("--overwrite")
    for key, flag in (("formulas", "--formula"), ("start_modes", "--start-mode"), ("case_ids", "--case"), ("seeds", "--seed")):
        for value in run_filter.get(key, []):
            parts.extend([flag, str(value)])
    return " ".join(parts)


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


_RUN_COLUMNS = [
    "run_id",
    "suite_id",
    "case_id",
    "formula",
    "start_mode",
    "seed",
    "depth",
    "steps",
    "warm_depth",
    "warm_steps",
    "restarts",
    "warm_restarts",
    "perturbation_noise",
    "best_loss",
    "post_snap_loss",
    "snap_min_margin",
    "verifier_status",
    "recovery_class",
    "status",
    "claim_status",
    "runtime_seconds",
    "active_slot_count",
    "changed_slot_count",
    "reason",
    "artifact_path",
]

_GROUP_COLUMNS = [
    "group",
    "total",
    "verifier_recovered",
    "same_ast_return",
    "verified_equivalent_ast",
    "unsupported",
    "failed",
    "execution_error",
    "verifier_recovery_rate",
    "unsupported_rate",
    "failure_rate",
]

_FAILURE_COLUMNS = ["run_id", "formula", "start_mode", "classification", "status", "reason", "artifact_path"]


def _run_csv_row(run: Mapping[str, Any]) -> dict[str, Any]:
    optimizer = run.get("optimizer", {})
    metrics = run.get("metrics", {})
    return {
        "run_id": run.get("run_id"),
        "suite_id": run.get("suite_id"),
        "case_id": run.get("case_id"),
        "formula": run.get("formula"),
        "start_mode": run.get("start_mode"),
        "seed": run.get("seed"),
        "depth": optimizer.get("depth"),
        "steps": optimizer.get("steps"),
        "warm_depth": optimizer.get("warm_depth"),
        "warm_steps": optimizer.get("warm_steps"),
        "restarts": optimizer.get("restarts"),
        "warm_restarts": optimizer.get("warm_restarts"),
        "perturbation_noise": run.get("perturbation_noise"),
        "best_loss": metrics.get("best_loss"),
        "post_snap_loss": metrics.get("post_snap_loss"),
        "snap_min_margin": metrics.get("snap_min_margin"),
        "verifier_status": metrics.get("verifier_status"),
        "recovery_class": run.get("classification"),
        "status": run.get("status"),
        "claim_status": run.get("claim_status"),
        "runtime_seconds": _runtime_seconds(run),
        "active_slot_count": metrics.get("active_slot_count"),
        "changed_slot_count": metrics.get("changed_slot_count"),
        "reason": run.get("reason"),
        "artifact_path": run.get("artifact_path"),
    }


def _group_rows(runs: list[Mapping[str, Any]], key: str | Any) -> list[dict[str, Any]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for run in runs:
        value = key(run) if callable(key) else run.get(key)
        grouped.setdefault(str(value), []).append(run)
    return [{"group": group, **_count_summary(items)} for group, items in sorted(grouped.items())]


def _count_summary(runs: list[Mapping[str, Any]]) -> dict[str, Any]:
    total = len(runs)
    verifier_recovered = sum(1 for run in runs if run.get("claim_status") == "recovered")
    same_ast = sum(1 for run in runs if run.get("classification") == "same_ast_warm_start_return")
    verified_equivalent = sum(1 for run in runs if run.get("classification") == "verified_equivalent_warm_start_recovery")
    unsupported = sum(1 for run in runs if run.get("classification") == "unsupported")
    failed = sum(1 for run in runs if run.get("classification") in {"failed", "snapped_but_failed", "soft_fit_only"})
    execution_error = sum(1 for run in runs if run.get("classification") == "execution_failure")
    return {
        "total": total,
        "verifier_recovered": verifier_recovered,
        "same_ast_return": same_ast,
        "verified_equivalent_ast": verified_equivalent,
        "unsupported": unsupported,
        "failed": failed,
        "execution_error": execution_error,
        "verifier_recovery_rate": _rate(verifier_recovered, total),
        "unsupported_rate": _rate(unsupported, total),
        "failure_rate": _rate(failed + execution_error, total),
    }


def _headline_metrics(runs: list[Mapping[str, Any]]) -> dict[str, Any]:
    counts = _count_summary(runs)
    total = counts["total"]
    same_ast = counts["same_ast_return"]
    best_losses = [_metric(run, "best_loss") for run in runs]
    post_snap_losses = [_metric(run, "post_snap_loss") for run in runs]
    runtimes = [_runtime_seconds(run) for run in runs]
    return {
        "total_runs": total,
        "verifier_recovered": counts["verifier_recovered"],
        "verifier_recovery_rate": counts["verifier_recovery_rate"],
        "unsupported": counts["unsupported"],
        "unsupported_rate": counts["unsupported_rate"],
        "failed": counts["failed"],
        "failure_rate": counts["failure_rate"],
        "same_ast_return": same_ast,
        "same_ast_return_rate": _rate(same_ast, total),
        "verified_equivalent_ast": counts["verified_equivalent_ast"],
        "median_best_loss": _median(value for value in best_losses if value is not None),
        "median_post_snap_loss": _median(value for value in post_snap_losses if value is not None),
        "median_runtime_seconds": _median(value for value in runtimes if value is not None),
    }


def _metric(run: Mapping[str, Any], key: str) -> float | None:
    value = run.get("metrics", {}).get(key)
    return _number_or_none(value)


def _runtime_seconds(run: Mapping[str, Any]) -> float | None:
    artifact_path = run.get("artifact_path")
    if not artifact_path:
        return None
    path = Path(str(artifact_path))
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError:
        return None
    return _number_or_none(payload.get("timing", {}).get("elapsed_seconds"))


def _median(values: Any) -> float | None:
    numeric = [value for value in values if value is not None]
    return float(statistics.median(numeric)) if numeric else None


def _number_or_none(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _rate(count: int, total: int) -> float:
    return count / total if total else 0.0


def _write_csv(path: Path, rows: list[Mapping[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: "" if row.get(key) is None else row.get(key) for key in fieldnames})
