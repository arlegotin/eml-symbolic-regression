"""Diagnostics over committed benchmark campaign evidence."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

from .benchmark import RunFilter
from .campaign import CampaignResult, run_campaign


DEFAULT_BASELINE_CAMPAIGNS = (
    Path("artifacts") / "campaigns" / "v1.3-standard",
    Path("artifacts") / "campaigns" / "v1.3-showcase",
)

FAILURE_CLASSES = frozenset({"failed", "snapped_but_failed", "soft_fit_only", "unsupported", "execution_failure"})
DIAGNOSTIC_TARGETS = frozenset({"blind-failures", "beer-perturbation-failures", "compiler-depth-gates"})


def write_baseline_triage(campaign_dirs: Iterable[Path], output_dir: Path) -> dict[str, Path]:
    """Write JSON, Markdown, and lock artifacts for baseline campaign triage."""

    output_dir.mkdir(parents=True, exist_ok=True)
    triage = build_baseline_triage(tuple(campaign_dirs))
    json_path = output_dir / "triage.json"
    markdown_path = output_dir / "triage.md"
    lock_path = output_dir / "baseline-lock.json"
    _write_json(json_path, triage)
    markdown_path.write_text(render_baseline_triage_markdown(triage), encoding="utf-8")
    _write_json(lock_path, {"schema": "eml.baseline_lock.v1", "baselines": triage["baseline_locks"]})
    return {"json": json_path, "markdown": markdown_path, "lock_json": lock_path}


def build_baseline_triage(campaign_dirs: tuple[Path, ...]) -> dict[str, Any]:
    campaigns = [_load_campaign_dir(path) for path in campaign_dirs]
    failure_rows = [row for campaign in campaigns for row in _failure_rows(campaign)]
    group_counts = _group_failure_rows(failure_rows)
    diagnostic_subsets = {
        target: {
            "target": target,
            "run_count": len(rows),
            "run_filter": _filter_payload(filter_for_runs(rows)),
            "runs": rows,
        }
        for target in sorted(DIAGNOSTIC_TARGETS)
        for rows in (select_diagnostic_runs_from_rows(failure_rows, target),)
    }
    return {
        "schema": "eml.baseline_diagnostics.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "baselines": [_baseline_summary(campaign) for campaign in campaigns],
        "baseline_locks": [_baseline_lock(campaign) for campaign in campaigns],
        "failure_group_counts": group_counts,
        "failure_runs": failure_rows,
        "diagnostic_subsets": diagnostic_subsets,
    }


def select_diagnostic_runs(campaign_dirs: Iterable[Path], target: str) -> list[dict[str, Any]]:
    if target not in DIAGNOSTIC_TARGETS:
        raise ValueError(f"unknown diagnostic target {target!r}")
    campaigns = [_load_campaign_dir(path) for path in campaign_dirs]
    failure_rows = [row for campaign in campaigns for row in _failure_rows(campaign)]
    return select_diagnostic_runs_from_rows(failure_rows, target)


def select_diagnostic_runs_from_rows(rows: Iterable[Mapping[str, Any]], target: str) -> list[dict[str, Any]]:
    if target not in DIAGNOSTIC_TARGETS:
        raise ValueError(f"unknown diagnostic target {target!r}")
    selected: list[dict[str, Any]] = []
    for row in rows:
        if target == "blind-failures" and row.get("start_mode") == "blind":
            selected.append(dict(row))
        elif (
            target == "beer-perturbation-failures"
            and row.get("formula") == "beer_lambert"
            and row.get("start_mode") == "warm_start"
            and float(row.get("perturbation_noise") or 0.0) > 0.0
        ):
            selected.append(dict(row))
        elif target == "compiler-depth-gates" and row.get("classification") == "unsupported":
            selected.append(dict(row))
    return selected


def filter_for_runs(rows: Iterable[Mapping[str, Any]]) -> RunFilter:
    row_list = list(rows)
    return RunFilter(
        formulas=_sorted_str(row.get("formula") for row in row_list),
        start_modes=_sorted_str(row.get("start_mode") for row in row_list),
        case_ids=_sorted_str(row.get("case_id") for row in row_list),
        seeds=tuple(sorted({int(row["seed"]) for row in row_list if row.get("seed") is not None})),
        perturbation_noises=tuple(
            sorted({float(row["perturbation_noise"]) for row in row_list if row.get("perturbation_noise") is not None})
        ),
    )


def run_diagnostic_subset(
    target: str,
    campaign_dirs: Iterable[Path],
    *,
    preset_name: str,
    output_root: Path,
    label: str | None = None,
    overwrite: bool = False,
) -> CampaignResult:
    rows = select_diagnostic_runs(campaign_dirs, target)
    if not rows:
        raise ValueError(f"no baseline rows matched diagnostic target {target!r}")
    run_filter = filter_for_runs(rows)
    return run_campaign(preset_name, output_root=output_root, label=label, overwrite=overwrite, run_filter=run_filter)


def render_baseline_triage_markdown(triage: Mapping[str, Any]) -> str:
    lines = [
        "# Baseline Failure Triage",
        "",
        "Committed v1.3 campaign failures grouped for v1.4 improvement work.",
        "",
        "## Baselines",
        "",
        "| Campaign | Runs | Verifier recovered | Unsupported | Failed |",
        "|----------|------|--------------------|-------------|--------|",
    ]
    for baseline in triage["baselines"]:
        counts = baseline.get("counts", {})
        lines.append(
            f"| {baseline['label']} | {counts.get('total', 0)} | {counts.get('verifier_recovered', 0)} | "
            f"{counts.get('unsupported', 0)} | {counts.get('failed', 0)} |"
        )

    lines.extend(
        [
            "",
            "## Failure Groups",
            "",
            "| Formula | Mode | Perturbation | Class | Count |",
            "|---------|------|--------------|-------|-------|",
        ]
    )
    for row in triage["failure_group_counts"]:
        lines.append(
            f"| {row['formula']} | {row['start_mode']} | {row['perturbation_noise']} | "
            f"{row['classification']} | {row['count']} |"
        )

    lines.extend(
        [
            "",
            "## Focused Diagnostic Subsets",
            "",
            "| Target | Runs | Formula filter | Mode filter | Noise filter |",
            "|--------|------|----------------|-------------|--------------|",
        ]
    )
    for target, subset in triage["diagnostic_subsets"].items():
        run_filter = subset["run_filter"]
        lines.append(
            f"| {target} | {subset['run_count']} | {', '.join(run_filter['formulas'])} | "
            f"{', '.join(run_filter['start_modes'])} | {', '.join(str(value) for value in run_filter['perturbation_noises'])} |"
        )

    lines.extend(
        [
            "",
            "## Representative Failure Runs",
            "",
            "| Campaign | Formula | Mode | Seed | Noise | Class | Reason | Metrics | Artifact |",
            "|----------|---------|------|------|-------|-------|--------|---------|----------|",
        ]
    )
    for row in triage["failure_runs"]:
        metrics = row.get("metrics", {})
        metric_text = (
            f"best={_fmt(metrics.get('best_loss'))}; snap={_fmt(metrics.get('post_snap_loss'))}; "
            f"margin={_fmt(metrics.get('snap_min_margin'))}; changed={_fmt(metrics.get('changed_slot_count'))}; "
            f"verifier={metrics.get('verifier_status')}"
        )
        lines.append(
            f"| {row['campaign']} | {row['formula']} | {row['start_mode']} | {row['seed']} | "
            f"{row['perturbation_noise']} | {row['classification']} | {row['reason']} | "
            f"{metric_text} | [{row['run_id']}]({row['artifact_path']}) |"
        )

    lines.extend(
        [
            "",
            "## Baseline Locks",
            "",
            "| Campaign | File | SHA-256 |",
            "|----------|------|---------|",
        ]
    )
    for baseline in triage["baseline_locks"]:
        for file_info in baseline["files"]:
            lines.append(f"| {baseline['label']} | {file_info['path']} | `{file_info['sha256']}` |")
    lines.append("")
    return "\n".join(lines)


def _load_campaign_dir(path: Path) -> dict[str, Any]:
    aggregate_path = path / "aggregate.json"
    if not aggregate_path.exists():
        raise FileNotFoundError(f"missing aggregate.json in {path}")
    aggregate = json.loads(aggregate_path.read_text(encoding="utf-8"))
    manifest_path = path / "campaign-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    return {"path": path, "label": path.name, "aggregate": aggregate, "manifest": manifest}


def _baseline_summary(campaign: Mapping[str, Any]) -> dict[str, Any]:
    aggregate = campaign["aggregate"]
    manifest = campaign.get("manifest") or {}
    return {
        "label": campaign["label"],
        "path": str(campaign["path"]),
        "suite_id": aggregate.get("suite", {}).get("id"),
        "preset": manifest.get("preset", {}).get("name"),
        "counts": aggregate.get("counts", {}),
    }


def _baseline_lock(campaign: Mapping[str, Any]) -> dict[str, Any]:
    path = Path(campaign["path"])
    files = []
    for relative in ("aggregate.json", "suite-result.json", "campaign-manifest.json", "tables/runs.csv", "tables/failures.csv"):
        file_path = path / relative
        if file_path.exists():
            files.append({"path": str(file_path), "sha256": _sha256(file_path)})
    return {"label": campaign["label"], "path": str(path), "files": files}


def _failure_rows(campaign: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for run in campaign["aggregate"].get("runs", ()):
        if run.get("classification") not in FAILURE_CLASSES:
            continue
        rows.append(
            {
                "campaign": campaign["label"],
                "run_id": run.get("run_id"),
                "suite_id": run.get("suite_id"),
                "case_id": run.get("case_id"),
                "formula": run.get("formula"),
                "start_mode": run.get("start_mode"),
                "seed": run.get("seed"),
                "perturbation_noise": run.get("perturbation_noise"),
                "classification": run.get("classification"),
                "status": run.get("status"),
                "claim_status": run.get("claim_status"),
                "reason": run.get("reason"),
                "artifact_path": run.get("artifact_path"),
                "metrics": run.get("metrics", {}),
                "stage_statuses": run.get("stage_statuses", {}),
            }
        )
    return rows


def _group_failure_rows(rows: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    counts: Counter[tuple[str, str, str, str]] = Counter()
    for row in rows:
        key = (
            str(row.get("formula")),
            str(row.get("start_mode")),
            str(row.get("perturbation_noise")),
            str(row.get("classification")),
        )
        counts[key] += 1
    return [
        {
            "formula": formula,
            "start_mode": start_mode,
            "perturbation_noise": perturbation_noise,
            "classification": classification,
            "count": count,
        }
        for (formula, start_mode, perturbation_noise, classification), count in sorted(counts.items())
    ]


def _filter_payload(run_filter: RunFilter) -> dict[str, list[Any]]:
    return {
        "formulas": list(run_filter.formulas),
        "start_modes": list(run_filter.start_modes),
        "case_ids": list(run_filter.case_ids),
        "seeds": list(run_filter.seeds),
        "perturbation_noises": list(run_filter.perturbation_noises),
    }


def _sorted_str(values: Iterable[Any]) -> tuple[str, ...]:
    return tuple(sorted({str(value) for value in values if value is not None}))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _fmt(value: Any) -> str:
    if value is None:
        return "n/a"
    try:
        return f"{float(value):.4g}"
    except (TypeError, ValueError):
        return str(value)
