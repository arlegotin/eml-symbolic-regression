"""Campaign presets and reproducible output manifests for benchmark evidence."""

from __future__ import annotations

import csv
import json
import math
import platform
import statistics
from dataclasses import dataclass, field
from datetime import datetime, timezone
from html import escape
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
    figure_paths: Mapping[str, Path] = field(default_factory=dict)
    report_path: Path | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "preset": self.preset.as_dict(),
            "campaign_dir": str(self.campaign_dir),
            "manifest_path": str(self.manifest_path),
            "suite_result_path": str(self.suite_result_path),
            "aggregate_paths": {key: str(value) for key, value in self.aggregate_paths.items()},
            "table_paths": {key: str(value) for key, value in self.table_paths.items()},
            "figure_paths": {key: str(value) for key, value in self.figure_paths.items()},
            "report_path": str(self.report_path) if self.report_path is not None else None,
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
    figure_paths = write_campaign_plots(aggregate, campaign_dir / "figures")

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
        figure_paths=figure_paths,
    )
    report_path = write_campaign_report(campaign_dir, manifest, aggregate, table_paths, figure_paths)
    manifest["output"]["report_markdown"] = str(report_path)
    manifest_path = campaign_dir / "campaign-manifest.json"
    _write_json(manifest_path, manifest)
    return CampaignResult(
        preset=preset,
        campaign_dir=campaign_dir,
        manifest_path=manifest_path,
        suite_result_path=suite_result_path,
        aggregate_paths=aggregate_paths,
        table_paths=table_paths,
        figure_paths=figure_paths,
        report_path=report_path,
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


def write_campaign_plots(aggregate: Mapping[str, Any], output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    runs = list(aggregate.get("runs", ()))
    paths = {
        "recovery_by_formula": output_dir / "recovery-by-formula.svg",
        "recovery_by_start_mode": output_dir / "recovery-by-start-mode.svg",
        "loss_before_after_snap": output_dir / "loss-before-after-snap.svg",
        "beer_perturbation": output_dir / "beer-perturbation.svg",
        "runtime_depth_budget": output_dir / "runtime-depth-budget.svg",
        "failure_taxonomy": output_dir / "failure-taxonomy.svg",
    }

    _write_svg(
        paths["recovery_by_formula"],
        _bar_chart_svg(
            "Verifier Recovery Rate by Formula",
            _rate_bars(_group_rows(runs, "formula"), "group", "verifier_recovery_rate", percent=True),
            y_label="recovered / total",
            max_value=1.0,
        ),
    )
    _write_svg(
        paths["recovery_by_start_mode"],
        _bar_chart_svg(
            "Verifier Recovery Rate by Start Mode",
            _rate_bars(_group_rows(runs, "start_mode"), "group", "verifier_recovery_rate", percent=True),
            y_label="recovered / total",
            max_value=1.0,
        ),
    )
    _write_svg(paths["loss_before_after_snap"], _loss_chart_svg(runs))
    _write_svg(paths["beer_perturbation"], _beer_perturbation_svg(runs))
    _write_svg(paths["runtime_depth_budget"], _runtime_depth_svg(runs))
    _write_svg(paths["failure_taxonomy"], _failure_taxonomy_svg(runs))
    return paths


def write_campaign_report(
    campaign_dir: Path,
    manifest: Mapping[str, Any],
    aggregate: Mapping[str, Any],
    table_paths: Mapping[str, Path],
    figure_paths: Mapping[str, Path],
) -> Path:
    report_path = campaign_dir / "report.md"
    runs = list(aggregate.get("runs", ()))
    headline = _headline_metrics(runs)
    counts = aggregate.get("counts", {})
    preset = manifest.get("preset", {})
    suite = manifest.get("suite", {})
    command = manifest.get("reproducibility", {}).get("command", "")

    lines = [
        f"# EML Benchmark Campaign Report: {preset.get('name', 'campaign')}",
        "",
        str(preset.get("description", "")),
        "",
        "## Reproduce",
        "",
        "Run this command from a clean checkout:",
        "",
        "```bash",
        str(command),
        "```",
        "",
        f"- Suite: `{suite.get('id', '')}`",
        f"- Budget tier: `{preset.get('tier', '')}`",
        f"- Guardrail: {preset.get('budget_guardrail', '')}",
        f"- Raw run artifacts: [{_relative_link(manifest['output']['raw_run_root'], campaign_dir)}]({_relative_link(manifest['output']['raw_run_root'], campaign_dir)})",
        "",
        "## Headline Metrics",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total runs | {headline['total_runs']} |",
        f"| Verifier recovered | {headline['verifier_recovered']} ({headline['verifier_recovery_rate']:.1%}) |",
        f"| Same-AST warm-start returns | {headline['same_ast_return']} ({headline['same_ast_return_rate']:.1%}) |",
        f"| Verified equivalent warm-start recoveries | {headline['verified_equivalent_ast']} |",
        f"| Unsupported | {headline['unsupported']} ({headline['unsupported_rate']:.1%}) |",
        f"| Failed | {headline['failed']} ({headline['failure_rate']:.1%}) |",
        f"| Median best soft loss | {_format_optional(headline['median_best_loss'])} |",
        f"| Median post-snap loss | {_format_optional(headline['median_post_snap_loss'])} |",
        f"| Median runtime seconds | {_format_optional(headline['median_runtime_seconds'])} |",
        "",
        "## Figures",
        "",
    ]
    for key, path in figure_paths.items():
        rel = _relative_link(path, campaign_dir)
        lines.append(f"- [{key.replace('_', ' ')}]({rel})")

    lines.extend(
        [
            "",
            "## Tables",
            "",
        ]
    )
    for key, path in table_paths.items():
        rel = _relative_link(path, campaign_dir)
        lines.append(f"- [{key.replace('_', ' ')}]({rel})")

    lines.extend(
        [
            "",
            "## What EML Demonstrates Well",
            "",
            _strengths_paragraph(counts),
            "",
            "## Limitations",
            "",
            _limitations_section(runs),
            "",
            "## Failed and Unsupported Cases",
            "",
            _failure_table(runs, campaign_dir),
            "",
            "## Next Experiments",
            "",
            "- Improve blind optimizer robustness and compare against this campaign's `snapped_but_failed` cases.",
            "- Reduce compiled arithmetic tree depth for formulas gated as unsupported, especially Michaelis-Menten and Planck-style expressions.",
            "- Expand perturbation sweeps after optimizer changes so same-AST returns and verified-equivalent recoveries can be compared over time.",
            "- Add external noisy datasets only after the synthetic/source-document campaign remains reproducible and interpretable.",
            "",
        ]
    )

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


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
    figure_paths: Mapping[str, Path],
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
            "figures": {key: str(value) for key, value in figure_paths.items()},
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
        "perturbation_noises": list(run_filter.perturbation_noises),
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
    for key, flag in (
        ("formulas", "--formula"),
        ("start_modes", "--start-mode"),
        ("case_ids", "--case"),
        ("seeds", "--seed"),
        ("perturbation_noises", "--perturbation-noise"),
    ):
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


def _strengths_paragraph(counts: Mapping[str, Any]) -> str:
    recovered = int(counts.get("verifier_recovered", 0))
    same_ast = int(counts.get("same_ast_return", 0))
    equivalent = int(counts.get("verified_equivalent_ast", 0))
    total = int(counts.get("total", 0))
    return (
        f"This campaign shows the strongest current behavior when the EML representation is verified after snapping: "
        f"{recovered}/{total} runs passed verifier-owned recovery. Warm-start runs are especially useful evidence: "
        f"{same_ast} returned to the same compiled EML AST and {equivalent} produced a different verified-equivalent AST. "
        "Those are not blind-discovery claims, but they are practical evidence that the paper's uniform EML tree can be "
        "compiled, embedded, perturbed, optimized, snapped, and independently verified."
    )


def _limitations_section(runs: list[Mapping[str, Any]]) -> str:
    blind_total = sum(1 for run in runs if run.get("start_mode") == "blind")
    blind_recovered = sum(1 for run in runs if run.get("classification") == "blind_recovery")
    same_ast = sum(1 for run in runs if run.get("classification") == "same_ast_warm_start_return")
    equivalent = sum(1 for run in runs if run.get("classification") == "verified_equivalent_warm_start_recovery")
    unsupported = sum(1 for run in runs if run.get("classification") == "unsupported")
    failed = sum(1 for run in runs if run.get("classification") in {"failed", "snapped_but_failed", "soft_fit_only", "execution_failure"})
    return "\n".join(
        [
            f"- Blind recovery: {blind_recovered}/{blind_total} blind runs recovered. Treat this separately from compiler-assisted paths.",
            f"- Same-AST warm-start return: {same_ast} runs snapped back to the compiled seed; useful basin evidence, not discovery.",
            f"- Verified-equivalent warm-start recovery: {equivalent} runs snapped to a different exact AST that verified.",
            f"- Unsupported gates: {unsupported} runs were blocked by compiler/depth/operator limits and remain in the denominator.",
            f"- Failed fits: {failed} runs did not pass verifier-owned recovery after training or execution.",
        ]
    )


def _failure_table(runs: list[Mapping[str, Any]], campaign_dir: Path) -> str:
    failures = [
        run
        for run in runs
        if run.get("classification") in {"unsupported", "failed", "snapped_but_failed", "soft_fit_only", "execution_failure"}
    ]
    if not failures:
        return "No failed or unsupported cases in this campaign."
    lines = [
        "| Formula | Mode | Class | Reason | Artifact |",
        "|---------|------|-------|--------|----------|",
    ]
    for run in failures:
        artifact = _relative_link(run.get("artifact_path", ""), campaign_dir)
        lines.append(
            f"| {run.get('formula')} | {run.get('start_mode')} | {run.get('classification')} | "
            f"{run.get('reason')} | [{run.get('run_id')}]({artifact}) |"
        )
    return "\n".join(lines)


def _relative_link(path: str | Path, base: Path) -> str:
    path_obj = Path(str(path))
    try:
        return path_obj.relative_to(base).as_posix()
    except ValueError:
        return path_obj.as_posix()


def _format_optional(value: Any) -> str:
    number = _number_or_none(value)
    return "n/a" if number is None else f"{number:.4g}"


def _write_svg(path: Path, svg: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")


def _rate_bars(rows: list[Mapping[str, Any]], label_key: str, value_key: str, *, percent: bool) -> list[dict[str, Any]]:
    bars = []
    for row in rows:
        value = float(row.get(value_key) or 0.0)
        bars.append(
            {
                "label": str(row.get(label_key)),
                "value": value,
                "display": f"{value:.0%}" if percent else f"{value:.3g}",
            }
        )
    return bars


def _bar_chart_svg(
    title: str,
    bars: list[Mapping[str, Any]],
    *,
    y_label: str,
    max_value: float | None = None,
    width: int = 960,
    height: int = 520,
) -> str:
    if not bars:
        return _empty_svg(title, "No data available.", width=width, height=height)

    left = 86
    right = 36
    top = 76
    bottom = 130
    plot_width = width - left - right
    plot_height = height - top - bottom
    baseline = top + plot_height
    max_seen = max(float(bar.get("value") or 0.0) for bar in bars)
    scale_max = max(max_value or max_seen, max_seen, 1e-12)
    slot = plot_width / len(bars)
    bar_width = max(12, min(64, slot * 0.58))
    palette = ["#2f6f8f", "#d1495b", "#4f8a3a", "#7a5195", "#a5673f", "#1f8a70"]

    parts = [_svg_header(width, height), f'<text x="{left}" y="38" class="title">{escape(title)}</text>']
    parts.append(f'<text x="{left}" y="60" class="subtitle">{escape(y_label)}</text>')
    parts.append(f'<line x1="{left}" y1="{baseline}" x2="{width - right}" y2="{baseline}" class="axis" />')
    parts.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{baseline}" class="axis" />')
    for tick in range(5):
        value = scale_max * tick / 4
        y = baseline - (value / scale_max * plot_height)
        parts.append(f'<line x1="{left - 5}" y1="{y:.2f}" x2="{width - right}" y2="{y:.2f}" class="grid" />')
        parts.append(f'<text x="{left - 12}" y="{y + 4:.2f}" class="tick" text-anchor="end">{value:.2g}</text>')

    for index, bar in enumerate(bars):
        value = float(bar.get("value") or 0.0)
        h = value / scale_max * plot_height if scale_max else 0.0
        x = left + index * slot + (slot - bar_width) / 2
        y = baseline - h
        color = palette[index % len(palette)]
        label = escape(str(bar.get("label", "")))
        display = escape(str(bar.get("display", f"{value:.3g}")))
        parts.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_width:.2f}" height="{h:.2f}" fill="{color}" rx="3" />')
        parts.append(f'<text x="{x + bar_width / 2:.2f}" y="{max(y - 8, top - 8):.2f}" class="value" text-anchor="middle">{display}</text>')
        parts.append(
            f'<text x="{x + bar_width / 2:.2f}" y="{baseline + 22}" class="label" text-anchor="end" '
            f'transform="rotate(-35 {x + bar_width / 2:.2f} {baseline + 22})">{label}</text>'
        )
    parts.append("</svg>")
    return "\n".join(parts)


def _loss_chart_svg(runs: list[Mapping[str, Any]]) -> str:
    bars: list[dict[str, Any]] = []
    for run in runs:
        best = _metric(run, "best_loss")
        snapped = _metric(run, "post_snap_loss")
        if best is None and snapped is None:
            continue
        label = f"{run.get('formula')} s{run.get('seed')}"
        if best is not None:
            bars.append({"label": f"{label} best", "value": _loss_score(best), "display": _sci(best)})
        if snapped is not None:
            bars.append({"label": f"{label} snap", "value": _loss_score(snapped), "display": _sci(snapped)})
    return _bar_chart_svg(
        "Training Loss Before and After Snap",
        bars,
        y_label="-log10(loss), higher is lower loss",
        max_value=max((float(bar["value"]) for bar in bars), default=1.0),
    )


def _beer_perturbation_svg(runs: list[Mapping[str, Any]]) -> str:
    beer_runs = [run for run in runs if run.get("formula") == "beer_lambert"]
    groups = _group_rows(beer_runs, "perturbation_noise")
    bars = []
    for group in groups:
        noise_runs = [run for run in beer_runs if str(run.get("perturbation_noise")) == group["group"]]
        changed = [_number_or_none(run.get("metrics", {}).get("changed_slot_count")) for run in noise_runs]
        changed = [value for value in changed if value is not None]
        changed_label = f", slots {statistics.median(changed):.1f}" if changed else ""
        bars.append(
            {
                "label": f"noise {group['group']}",
                "value": group["verifier_recovery_rate"],
                "display": f"{group['verifier_recovery_rate']:.0%}{changed_label}",
            }
        )
    return _bar_chart_svg("Beer-Lambert Perturbation Recovery", bars, y_label="recovered / total", max_value=1.0)


def _runtime_depth_svg(runs: list[Mapping[str, Any]]) -> str:
    grouped: dict[str, list[float]] = {}
    for run in runs:
        runtime = _runtime_seconds(run)
        if runtime is None:
            continue
        optimizer = run.get("optimizer", {})
        label = f"d{optimizer.get('depth')} / ws{optimizer.get('warm_steps')}"
        grouped.setdefault(label, []).append(runtime)
    bars = [
        {"label": label, "value": statistics.mean(values), "display": f"{statistics.mean(values):.2f}s"}
        for label, values in sorted(grouped.items())
    ]
    return _bar_chart_svg("Runtime by Depth and Warm Budget", bars, y_label="mean elapsed seconds")


def _failure_taxonomy_svg(runs: list[Mapping[str, Any]]) -> str:
    rows = [
        row
        for row in _group_rows(runs, "classification")
        if row["group"] in {"unsupported", "failed", "snapped_but_failed", "soft_fit_only", "execution_failure"}
    ]
    bars = [{"label": row["group"], "value": row["total"], "display": str(row["total"])} for row in rows]
    return _bar_chart_svg("Unsupported and Failure Taxonomy", bars, y_label="run count")


def _loss_score(loss: float) -> float:
    return max(0.0, -math.log10(max(float(loss), 1e-16)))


def _sci(value: float) -> str:
    return f"{float(value):.1e}"


def _empty_svg(title: str, message: str, *, width: int, height: int) -> str:
    return "\n".join(
        [
            _svg_header(width, height),
            f'<text x="64" y="48" class="title">{escape(title)}</text>',
            f'<text x="64" y="92" class="subtitle">{escape(message)}</text>',
            "</svg>",
        ]
    )


def _svg_header(width: int, height: int) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
<style>
  .title {{ font: 700 24px sans-serif; fill: #1d252c; }}
  .subtitle {{ font: 400 14px sans-serif; fill: #4b5563; }}
  .axis {{ stroke: #28343d; stroke-width: 1.3; }}
  .grid {{ stroke: #d7dde3; stroke-width: 1; }}
  .tick {{ font: 12px sans-serif; fill: #51606d; }}
  .label {{ font: 12px sans-serif; fill: #1d252c; }}
  .value {{ font: 700 11px sans-serif; fill: #1d252c; }}
</style>'''
