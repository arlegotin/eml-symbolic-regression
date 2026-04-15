"""Campaign presets and reproducible output manifests for benchmark evidence."""

from __future__ import annotations

import json
import platform
from dataclasses import dataclass
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

    def as_dict(self) -> dict[str, Any]:
        return {
            "preset": self.preset.as_dict(),
            "campaign_dir": str(self.campaign_dir),
            "manifest_path": str(self.manifest_path),
            "suite_result_path": str(self.suite_result_path),
            "aggregate_paths": {key: str(value) for key, value in self.aggregate_paths.items()},
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
    )
    manifest_path = campaign_dir / "campaign-manifest.json"
    _write_json(manifest_path, manifest)
    return CampaignResult(
        preset=preset,
        campaign_dir=campaign_dir,
        manifest_path=manifest_path,
        suite_result_path=suite_result_path,
        aggregate_paths=aggregate_paths,
    )


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
