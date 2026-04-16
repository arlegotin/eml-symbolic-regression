"""Campaign presets and reproducible output manifests for benchmark evidence."""

from __future__ import annotations

import csv
import json
import math
import platform
import shlex
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

    @property
    def benchmark_suite(self) -> str:
        return self.suite

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
    "proof-shallow": CampaignPreset(
        name="proof-shallow",
        suite="v1.5-shallow-proof",
        tier="proof-contract",
        description="Bounded v1.5 shallow proof campaign for scaffolded training evidence.",
        budget_guardrail="18 runs; declared shallow scaffolded-training proof suite with bounded threshold metadata.",
    ),
    "proof-shallow-pure-blind": CampaignPreset(
        name="proof-shallow-pure-blind",
        suite="v1.5-shallow-pure-blind",
        tier="proof-contract",
        description="Measured v1.5 shallow pure-blind campaign with scaffold initializers disabled.",
        budget_guardrail="18 runs; declared shallow pure-blind suite with measured recovery metadata.",
    ),
    "proof-basin": CampaignPreset(
        name="proof-basin",
        suite="proof-perturbed-basin",
        tier="proof-contract",
        description="Bounded v1.5 perturbed basin proof campaign with Beer-Lambert probe evidence reported separately.",
        budget_guardrail="CI-scale perturbed basin proof suite; high-noise probes are reported separately",
    ),
    "proof-basin-probes": CampaignPreset(
        name="proof-basin-probes",
        suite="proof-perturbed-basin-beer-probes",
        tier="proof-contract",
        description="Visible v1.5 Beer-Lambert perturbed-basin probe campaign outside bounded thresholds.",
        budget_guardrail="4 runs; declared Beer-Lambert high-noise probe rows kept outside the bounded proof denominator.",
    ),
    "proof-depth-curve": CampaignPreset(
        name="proof-depth-curve",
        suite="proof-depth-curve",
        tier="proof-contract",
        description="Measured v1.5 blind-vs-perturbed depth-curve campaign over deterministic exact EML targets.",
        budget_guardrail="20 runs; exact depth-2 through depth-6 blind and perturbed rows with fixed seeds and budgets.",
    ),
    "family-smoke": CampaignPreset(
        name="family-smoke",
        suite="v1.7-family-smoke",
        tier="ci",
        description="CI-scale v1.7 raw-vs-centered operator-family smoke campaign.",
        budget_guardrail="12 runs; raw, fixed centered, and continuation variants over the smoke suite.",
    ),
    "family-shallow-pure-blind": CampaignPreset(
        name="family-shallow-pure-blind",
        suite="v1.7-family-shallow-pure-blind",
        tier="v1.7-family-matrix",
        description="v1.7 shallow pure-blind raw-vs-centered operator-family matrix.",
        budget_guardrail="72 runs; v1.5 shallow pure-blind cases cloned across four operator variants without proof thresholds.",
    ),
    "family-shallow": CampaignPreset(
        name="family-shallow",
        suite="v1.7-family-shallow",
        tier="v1.7-family-matrix",
        description="v1.7 shallow scaffolded raw-vs-centered operator-family matrix.",
        budget_guardrail="72 runs; v1.5 shallow scaffolded cases cloned across four operator variants without proof thresholds.",
    ),
    "family-basin": CampaignPreset(
        name="family-basin",
        suite="v1.7-family-basin",
        tier="v1.7-family-matrix",
        description="v1.7 perturbed-basin raw-vs-centered operator-family matrix.",
        budget_guardrail="Raw basin rows run normally; centered perturbed-tree rows fail closed until same-family seeds exist.",
    ),
    "family-depth-curve": CampaignPreset(
        name="family-depth-curve",
        suite="v1.7-family-depth-curve",
        tier="v1.7-family-matrix",
        description="v1.7 blind-vs-perturbed depth-curve operator-family matrix.",
        budget_guardrail="80 expanded runs; depth-curve cases cloned across four operator variants without proof thresholds.",
    ),
    "family-standard": CampaignPreset(
        name="family-standard",
        suite="v1.7-family-standard",
        tier="v1.7-family-matrix",
        description="v1.7 standard-style raw-vs-centered operator-family comparison campaign.",
        budget_guardrail="Standard-style comparison cloned across four operator variants with isolated v1.7 outputs.",
    ),
    "family-showcase": CampaignPreset(
        name="family-showcase",
        suite="v1.7-family-showcase",
        tier="v1.7-family-matrix",
        description="v1.7 showcase-style raw-vs-centered operator-family comparison campaign.",
        budget_guardrail="Showcase-style comparison cloned across four operator variants with isolated v1.7 outputs.",
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
        "group_evidence_class_csv": output_dir / "group-evidence-class.csv",
        "group_claim_csv": output_dir / "group-claim.csv",
        "group_threshold_policy_csv": output_dir / "group-threshold-policy.csv",
        "depth_curve_csv": output_dir / "depth-curve.csv",
        "operator_family_recovery_csv": output_dir / "operator-family-recovery.csv",
        "operator_family_diagnostics_csv": output_dir / "operator-family-diagnostics.csv",
        "operator_family_comparison_md": output_dir / "operator-family-comparison.md",
        "operator_family_locks_json": output_dir / "operator-family-locks.json",
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
    _write_csv(paths["group_evidence_class_csv"], _group_rows(runs, "evidence_class"), _GROUP_COLUMNS)
    _write_csv(paths["group_claim_csv"], _group_rows(runs, "claim_id"), _GROUP_COLUMNS)
    _write_csv(paths["group_threshold_policy_csv"], _group_rows(runs, lambda run: (run.get("threshold") or {}).get("id")), _GROUP_COLUMNS)
    _write_csv(paths["depth_curve_csv"], _depth_curve_table_rows(aggregate.get("depth_curve", [])), _DEPTH_CURVE_COLUMNS)
    family_recovery_rows = _operator_family_recovery_rows(runs)
    family_diagnostic_rows = _operator_family_diagnostic_rows(runs)
    _write_csv(paths["operator_family_recovery_csv"], family_recovery_rows, _OPERATOR_FAMILY_RECOVERY_COLUMNS)
    _write_csv(paths["operator_family_diagnostics_csv"], family_diagnostic_rows, _OPERATOR_FAMILY_DIAGNOSTIC_COLUMNS)
    paths["operator_family_comparison_md"].write_text(
        _operator_family_comparison_markdown(family_recovery_rows, family_diagnostic_rows),
        encoding="utf-8",
    )
    _write_json(paths["operator_family_locks_json"], _operator_family_lock_payload(runs))

    headline = _headline_metrics(runs)
    _write_json(paths["headline_json"], headline)
    _write_csv(paths["headline_csv"], [headline], list(headline))

    failures = [
        _failure_csv_row(run)
        for run in runs
        if run.get("classification") in {"unsupported", "failed", "snapped_but_failed", "soft_fit_only", "execution_failure", "repaired_candidate"}
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
        "depth_curve_recovery": output_dir / "depth-curve-recovery.svg",
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
    _write_svg(paths["depth_curve_recovery"], _depth_curve_recovery_svg(aggregate.get("depth_curve", [])))
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
        f"| Same-AST exact returns | {headline['same_ast_return']} ({headline['same_ast_return_rate']:.1%}) |",
        f"| Verified-equivalent exact returns | {headline['verified_equivalent_ast']} |",
        f"| Unsupported | {headline['unsupported']} ({headline['unsupported_rate']:.1%}) |",
        f"| Failed | {headline['failed']} ({headline['failure_rate']:.1%}) |",
        f"| Median best soft loss | {_format_optional(headline['median_best_loss'])} |",
        f"| Median post-snap loss | {_format_optional(headline['median_post_snap_loss'])} |",
        f"| Median runtime seconds | {_format_optional(headline['median_runtime_seconds'])} |",
        "",
    ]
    lines.extend(_regime_summary_section(runs))
    lines.extend(_proof_contract_section(runs, aggregate))
    lines.extend(_depth_curve_report_section(aggregate))
    lines.extend(_operator_family_report_section(runs, campaign_dir, table_paths))
    lines.extend(
        [
            "## Figures",
            "",
        ]
    )
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
            _strengths_paragraph(runs, counts),
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
        "thresholds": aggregate.get("thresholds", []),
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
    return shlex.join(parts)


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
    "operator_family",
    "operator_schedule",
    "best_loss",
    "post_snap_loss",
    "snap_min_margin",
    "verifier_status",
    "recovery_class",
    "status",
    "claim_status",
    "claim_id",
    "claim_class",
    "training_mode",
    "evidence_class",
    "return_kind",
    "raw_status",
    "repair_status",
    "repair_verifier_status",
    "repair_accepted_move_count",
    "threshold_policy",
    "dataset_manifest_sha256",
    "provenance_source",
    "provenance_expression",
    "runtime_seconds",
    "active_slot_count",
    "changed_slot_count",
    "warm_start_mechanism",
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

_DEPTH_CURVE_COLUMNS = [
    "depth",
    "start_mode",
    "training_mode",
    "seed_count",
    "recovered",
    "total",
    "recovery_rate",
    "best_loss_median",
    "best_loss_min",
    "best_loss_max",
    "post_snap_loss_median",
    "post_snap_loss_min",
    "post_snap_loss_max",
    "runtime_seconds_median",
    "runtime_seconds_min",
    "runtime_seconds_max",
    "snap_min_margin_median",
    "snap_min_margin_min",
    "snap_min_margin_max",
]

_OPERATOR_FAMILY_RECOVERY_COLUMNS = [
    "operator_family",
    "operator_schedule",
    "formula",
    "start_mode",
    "training_mode",
    "depth",
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
    "post_snap_verifier_pass_rate",
    "median_best_loss",
    "median_post_snap_loss",
    "median_runtime_seconds",
    "median_active_node_count",
    "median_candidate_complexity",
]

_OPERATOR_FAMILY_DIAGNOSTIC_COLUMNS = [
    "operator_family",
    "operator_schedule",
    "start_mode",
    "training_mode",
    "depth",
    "total",
    "verifier_pass_rate",
    "unsupported_rate",
    "repair_attempt_rate",
    "repair_accept_rate",
    "refit_attempt_rate",
    "refit_accept_rate",
    "anomaly_clamp_count_total",
    "anomaly_exp_overflow_count_total",
    "anomaly_expm1_overflow_count_total",
    "anomaly_log_branch_cut_count_total",
    "anomaly_log1p_branch_cut_count_total",
    "anomaly_shifted_singularity_near_count_total",
    "shifted_singularity_min_distance_min",
    "median_active_node_count",
    "median_candidate_complexity",
    "median_post_snap_loss",
]

_FAILURE_COLUMNS = [
    "run_id",
    "formula",
    "start_mode",
    "classification",
    "status",
    "return_kind",
    "raw_status",
    "repair_status",
    "repair_verifier_status",
    "repair_accepted_move_count",
    "reason",
    "artifact_path",
]


def _run_csv_row(run: Mapping[str, Any]) -> dict[str, Any]:
    optimizer = run.get("optimizer", {})
    metrics = run.get("metrics", {})
    threshold = run.get("threshold") if isinstance(run.get("threshold"), Mapping) else {}
    dataset_manifest = run.get("dataset_manifest") if isinstance(run.get("dataset_manifest"), Mapping) else {}
    provenance = run.get("provenance") if isinstance(run.get("provenance"), Mapping) else {}
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
        "operator_family": metrics.get("operator_family"),
        "operator_schedule": metrics.get("operator_schedule"),
        "best_loss": metrics.get("best_loss"),
        "post_snap_loss": metrics.get("post_snap_loss"),
        "snap_min_margin": metrics.get("snap_min_margin"),
        "verifier_status": metrics.get("verifier_status"),
        "recovery_class": run.get("classification"),
        "status": run.get("status"),
        "claim_status": run.get("claim_status"),
        "claim_id": run.get("claim_id"),
        "claim_class": run.get("claim_class"),
        "training_mode": run.get("training_mode"),
        "evidence_class": run.get("evidence_class"),
        "return_kind": run.get("return_kind"),
        "raw_status": run.get("raw_status"),
        "repair_status": run.get("repair_status") or metrics.get("repair_status"),
        "repair_verifier_status": metrics.get("repair_verifier_status"),
        "repair_accepted_move_count": metrics.get("repair_accepted_move_count"),
        "threshold_policy": threshold.get("id"),
        "dataset_manifest_sha256": dataset_manifest.get("manifest_sha256"),
        "provenance_source": provenance.get("source_document"),
        "provenance_expression": provenance.get("symbolic_expression"),
        "runtime_seconds": _runtime_seconds(run),
        "active_slot_count": metrics.get("active_slot_count"),
        "changed_slot_count": metrics.get("changed_slot_count"),
        "warm_start_mechanism": metrics.get("warm_start_mechanism"),
        "reason": run.get("reason"),
        "artifact_path": run.get("artifact_path"),
    }


def _failure_csv_row(run: Mapping[str, Any]) -> dict[str, Any]:
    row = _run_csv_row(run)
    row["classification"] = run.get("classification")
    return row


def _depth_curve_table_rows(rows: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "depth": row.get("depth"),
            "start_mode": row.get("start_mode"),
            "training_mode": row.get("training_mode"),
            "seed_count": row.get("seed_count"),
            "recovered": row.get("recovered"),
            "total": row.get("total"),
            "recovery_rate": row.get("recovery_rate"),
            "best_loss_median": row.get("best_loss_median"),
            "best_loss_min": row.get("best_loss_min"),
            "best_loss_max": row.get("best_loss_max"),
            "post_snap_loss_median": row.get("post_snap_loss_median"),
            "post_snap_loss_min": row.get("post_snap_loss_min"),
            "post_snap_loss_max": row.get("post_snap_loss_max"),
            "runtime_seconds_median": row.get("runtime_seconds_median"),
            "runtime_seconds_min": row.get("runtime_seconds_min"),
            "runtime_seconds_max": row.get("runtime_seconds_max"),
            "snap_min_margin_median": row.get("snap_min_margin_median"),
            "snap_min_margin_min": row.get("snap_min_margin_min"),
            "snap_min_margin_max": row.get("snap_min_margin_max"),
        }
        for row in rows
    ]


def _operator_family_recovery_rows(runs: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str, str, str, str], list[Mapping[str, Any]]] = {}
    for run in runs:
        key = (
            _operator_family_label(run),
            _operator_schedule_label(run),
            str(run.get("formula") or ""),
            str(run.get("start_mode") or ""),
            str(run.get("training_mode") or ""),
            str((run.get("optimizer") or {}).get("depth") or ""),
        )
        grouped.setdefault(key, []).append(run)

    rows: list[dict[str, Any]] = []
    for (operator_family, operator_schedule, formula, start_mode, training_mode, depth), items in sorted(grouped.items()):
        summary = _count_summary(items)
        rows.append(
            {
                "operator_family": operator_family,
                "operator_schedule": operator_schedule,
                "formula": formula,
                "start_mode": start_mode,
                "training_mode": training_mode,
                "depth": depth,
                **summary,
                "post_snap_verifier_pass_rate": _rate(
                    sum(1 for run in items if _metric_text(run, "verifier_status") == "recovered"),
                    len(items),
                ),
                "median_best_loss": _median(_metric(run, "best_loss") for run in items),
                "median_post_snap_loss": _median(_metric(run, "post_snap_loss") for run in items),
                "median_runtime_seconds": _median(_runtime_seconds(run) for run in items),
                "median_active_node_count": _median(_metric(run, "snap_active_node_count") for run in items),
                "median_candidate_complexity": _median(_metric(run, "candidate_complexity") for run in items),
            }
        )
    return rows


def _operator_family_diagnostic_rows(runs: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str, str, str], list[Mapping[str, Any]]] = {}
    for run in runs:
        key = (
            _operator_family_label(run),
            _operator_schedule_label(run),
            str(run.get("start_mode") or ""),
            str(run.get("training_mode") or ""),
            str((run.get("optimizer") or {}).get("depth") or ""),
        )
        grouped.setdefault(key, []).append(run)

    rows: list[dict[str, Any]] = []
    for (operator_family, operator_schedule, start_mode, training_mode, depth), items in sorted(grouped.items()):
        total = len(items)
        unsupported = sum(1 for run in items if _summary_class(run) == "unsupported")
        repair_attempts = sum(1 for run in items if _metric_text(run, "repair_status") not in {"", "None", "none", "not_attempted"})
        repair_accepts = sum(
            1
            for run in items
            if _metric_text(run, "repair_status") == "repaired" or _metric_text(run, "repair_verifier_status") == "recovered"
        )
        refit_attempts = sum(1 for run in items if _metric_text(run, "refit_status") not in {"", "None", "none", "not_attempted"})
        refit_accepts = sum(1 for run in items if _metric_text(run, "refit_accepted") == "True")
        rows.append(
            {
                "operator_family": operator_family,
                "operator_schedule": operator_schedule,
                "start_mode": start_mode,
                "training_mode": training_mode,
                "depth": depth,
                "total": total,
                "verifier_pass_rate": _rate(sum(1 for run in items if _metric_text(run, "verifier_status") == "recovered"), total),
                "unsupported_rate": _rate(unsupported, total),
                "repair_attempt_rate": _rate(repair_attempts, total),
                "repair_accept_rate": _rate(repair_accepts, total),
                "refit_attempt_rate": _rate(refit_attempts, total),
                "refit_accept_rate": _rate(refit_accepts, total),
                "anomaly_clamp_count_total": _metric_sum(items, "anomaly_clamp_count"),
                "anomaly_exp_overflow_count_total": _metric_sum(items, "anomaly_exp_overflow_count"),
                "anomaly_expm1_overflow_count_total": _metric_sum(items, "anomaly_expm1_overflow_count"),
                "anomaly_log_branch_cut_count_total": _metric_sum(items, "anomaly_log_branch_cut_count"),
                "anomaly_log1p_branch_cut_count_total": _metric_sum(items, "anomaly_log1p_branch_cut_count"),
                "anomaly_shifted_singularity_near_count_total": _metric_sum(items, "anomaly_shifted_singularity_near_count"),
                "shifted_singularity_min_distance_min": _metric_min(items, "anomaly_shifted_singularity_min_distance"),
                "median_active_node_count": _median(_metric(run, "snap_active_node_count") for run in items),
                "median_candidate_complexity": _median(_metric(run, "candidate_complexity") for run in items),
                "median_post_snap_loss": _median(_metric(run, "post_snap_loss") for run in items),
            }
        )
    return rows


def _operator_family_lock_payload(runs: list[Mapping[str, Any]]) -> dict[str, Any]:
    rows = _operator_family_diagnostic_rows(runs)
    return {
        "schema": "eml.operator_family_locks.v1",
        "groups": [
            {
                "operator_family": row["operator_family"],
                "operator_schedule": row["operator_schedule"],
                "start_mode": row["start_mode"],
                "training_mode": row["training_mode"],
                "depth": row["depth"],
                "total": row["total"],
                "verifier_pass_rate": row["verifier_pass_rate"],
                "unsupported_rate": row["unsupported_rate"],
                "repair_attempt_rate": row["repair_attempt_rate"],
                "refit_accept_rate": row["refit_accept_rate"],
            }
            for row in rows
        ],
    }


def _operator_family_comparison_markdown(
    recovery_rows: list[Mapping[str, Any]],
    diagnostic_rows: list[Mapping[str, Any]],
) -> str:
    lines = [
        "# Operator-Family Comparison",
        "",
        "## Recovery",
        "",
        "| Operator | Schedule | Formula | Mode | Depth | Recovered | Total | Rate | Unsupported |",
        "|----------|----------|---------|------|-------|-----------|-------|------|-------------|",
    ]
    for row in recovery_rows:
        lines.append(
            "| {operator_family} | {operator_schedule} | {formula} | {start_mode} | {depth} | "
            "{verifier_recovered} | {total} | {rate:.1%} | {unsupported} |".format(
                operator_family=row.get("operator_family", ""),
                operator_schedule=row.get("operator_schedule", ""),
                formula=row.get("formula", ""),
                start_mode=row.get("start_mode", ""),
                depth=row.get("depth", ""),
                verifier_recovered=int(row.get("verifier_recovered") or 0),
                total=int(row.get("total") or 0),
                rate=float(row.get("verifier_recovery_rate") or 0.0),
                unsupported=int(row.get("unsupported") or 0),
            )
        )
    lines.extend(
        [
            "",
            "## Diagnostics",
            "",
            "| Operator | Schedule | Mode | Depth | Verifier Pass | Unsupported | Repair Attempt | Refit Accept | Active Nodes |",
            "|----------|----------|------|-------|---------------|-------------|----------------|--------------|--------------|",
        ]
    )
    for row in diagnostic_rows:
        lines.append(
            "| {operator_family} | {operator_schedule} | {start_mode} | {depth} | {verifier:.1%} | "
            "{unsupported:.1%} | {repair:.1%} | {refit:.1%} | {active} |".format(
                operator_family=row.get("operator_family", ""),
                operator_schedule=row.get("operator_schedule", ""),
                start_mode=row.get("start_mode", ""),
                depth=row.get("depth", ""),
                verifier=float(row.get("verifier_pass_rate") or 0.0),
                unsupported=float(row.get("unsupported_rate") or 0.0),
                repair=float(row.get("repair_attempt_rate") or 0.0),
                refit=float(row.get("refit_accept_rate") or 0.0),
                active=_format_optional(row.get("median_active_node_count")),
            )
        )
    lines.append("")
    return "\n".join(lines)


def _group_rows(runs: list[Mapping[str, Any]], key: str | Any) -> list[dict[str, Any]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for run in runs:
        value = key(run) if callable(key) else run.get(key)
        grouped.setdefault(str(value), []).append(run)
    return [{"group": group, **_count_summary(items)} for group, items in sorted(grouped.items())]


def _count_summary(runs: list[Mapping[str, Any]]) -> dict[str, Any]:
    total = len(runs)
    verifier_recovered = sum(1 for run in runs if run.get("claim_status") == "recovered")
    classes = [_summary_class(run) for run in runs]
    same_ast = sum(1 for run in runs if _is_same_ast_return(run))
    verified_equivalent = sum(1 for run in runs if _is_verified_equivalent_return(run))
    unsupported = sum(1 for value in classes if value == "unsupported")
    failed = sum(1 for value in classes if value in {"failed", "snapped_but_failed", "soft_fit_only"})
    execution_error = sum(1 for value in classes if value == "execution_failure")
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


def _summary_class(run: Mapping[str, Any]) -> str:
    return str(run.get("evidence_class") or run.get("classification") or "unknown")


def _count_phrase(count: int, singular: str, plural: str | None = None) -> str:
    word = singular if count == 1 else (plural or f"{singular}s")
    return f"{count} {word}"


def _is_same_ast_return(run: Mapping[str, Any]) -> bool:
    values = {str(run.get("classification") or ""), str(run.get("evidence_class") or ""), str(run.get("return_kind") or "")}
    return bool(values & {"same_ast", "same_ast_return", "same_ast_warm_start_return"})


def _is_verified_equivalent_return(run: Mapping[str, Any]) -> bool:
    values = {str(run.get("classification") or ""), str(run.get("evidence_class") or ""), str(run.get("return_kind") or "")}
    return bool(values & {"verified_equivalent", "verified_equivalent_ast", "verified_equivalent_warm_start_recovery"})


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


def _metric_text(run: Mapping[str, Any], key: str) -> str:
    value = run.get("metrics", {}).get(key)
    return "" if value is None else str(value)


def _metric_sum(runs: list[Mapping[str, Any]], key: str) -> float:
    return float(sum(value for value in (_metric(run, key) for run in runs) if value is not None))


def _metric_min(runs: list[Mapping[str, Any]], key: str) -> float | None:
    values = [value for value in (_metric(run, key) for run in runs) if value is not None and math.isfinite(value)]
    return min(values) if values else None


def _operator_family_label(run: Mapping[str, Any]) -> str:
    metrics = run.get("metrics") if isinstance(run.get("metrics"), Mapping) else {}
    value = metrics.get("operator_family")
    if value:
        return str(value)
    optimizer = run.get("optimizer") if isinstance(run.get("optimizer"), Mapping) else {}
    operator = optimizer.get("operator_family") if isinstance(optimizer.get("operator_family"), Mapping) else {}
    return str(operator.get("label") or operator.get("family") or "raw_eml")


def _operator_schedule_label(run: Mapping[str, Any]) -> str:
    metrics = run.get("metrics") if isinstance(run.get("metrics"), Mapping) else {}
    value = metrics.get("operator_schedule")
    if value:
        return str(value)
    optimizer = run.get("optimizer") if isinstance(run.get("optimizer"), Mapping) else {}
    schedule = optimizer.get("operator_schedule")
    if isinstance(schedule, list) and schedule:
        return " -> ".join(str(item.get("label") or item.get("family") or "") for item in schedule if isinstance(item, Mapping))
    return "fixed"


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


def _strengths_paragraph(runs: list[Mapping[str, Any]], counts: Mapping[str, Any]) -> str:
    recovered = int(counts.get("verifier_recovered", 0))
    same_ast = int(counts.get("same_ast_return", 0))
    equivalent = int(counts.get("verified_equivalent_ast", 0))
    total = int(counts.get("total", 0))
    blind_runs = [run for run in runs if run.get("start_mode") == "blind"]
    warm_runs = [run for run in runs if run.get("start_mode") == "warm_start"]
    compile_runs = [run for run in runs if run.get("start_mode") == "compile"]
    catalog_runs = [run for run in runs if run.get("start_mode") == "catalog"]
    perturbed_runs = [run for run in runs if run.get("start_mode") == "perturbed_tree"]
    scaffolded_blind = sum(1 for run in blind_runs if run.get("evidence_class") == "scaffolded_blind_training_recovered")
    pure_blind = sum(1 for run in blind_runs if run.get("evidence_class") == "blind_training_recovered")
    repaired = sum(1 for run in runs if run.get("classification") == "repaired_candidate")
    blind_recovered = sum(1 for run in blind_runs if run.get("claim_status") == "recovered")

    if blind_runs and not (warm_runs or compile_runs or catalog_runs or perturbed_runs):
        if scaffolded_blind:
            return (
                f"This campaign shows the strongest current bounded blind-training behavior in this bundle: "
                f"{recovered}/{total} blind runs passed verifier-owned recovery, and all {scaffolded_blind} recovered rows are "
                "scaffolded blind recoveries. Read these results as bounded scaffolded-training evidence, not as pure random-initialized "
                "blind discovery."
            )
        repaired_note = f", plus {_count_phrase(repaired, 'repaired candidate')}" if repaired else ""
        return (
            f"This campaign measures the current pure random-initialized blind boundary: "
            f"{recovered}/{total} blind runs passed verifier-owned recovery, including "
            f"{_count_phrase(pure_blind, 'threshold-eligible pure blind recovery', 'threshold-eligible pure blind recoveries')}"
            f"{repaired_note}. "
            "These rows are recovery-boundary evidence, not warm-start basin evidence."
        )

    if perturbed_runs and not (blind_runs or warm_runs or compile_runs or catalog_runs):
        return (
            f"This campaign isolates the perturbed true-tree basin: {recovered}/{total} perturbed runs passed verifier-owned recovery, "
            f"with {same_ast} same-AST returns, {equivalent} verified-equivalent returns, and {repaired} repaired candidates. "
            "Those outcomes demonstrate local basin and repair behavior, not blind-discovery performance."
        )

    if warm_runs and not (blind_runs or compile_runs or catalog_runs or perturbed_runs):
        return (
            f"This campaign isolates warm-start recovery behavior: {recovered}/{total} runs passed verifier-owned recovery, "
            f"with {same_ast} returns to the same compiled EML AST and {equivalent} verified-equivalent returns. "
            "Those are recovery and basin checks, not blind-discovery claims."
        )

    return (
        f"This campaign shows the strongest current mixed-regime behavior when the EML representation is verified after snapping: "
        f"{recovered}/{total} runs passed verifier-owned recovery. It includes {blind_recovered}/{len(blind_runs) if blind_runs else 0} "
        f"blind recoveries, {same_ast} same-AST exact returns, and {equivalent} verified-equivalent exact returns. "
        "Those evidence paths remain separated in the tables so blind discovery, warm-start basin behavior, and non-training diagnostics are "
        "not merged into one claim."
    )


def _regime_summary_section(runs: list[Mapping[str, Any]]) -> list[str]:
    lines = [
        "## Regime Summary",
        "",
        "| Regime | Runs | Verifier Recovered | Same AST | Verified Equivalent | Unsupported | Failed |",
        "|--------|------|--------------------|----------|---------------------|-------------|--------|",
    ]
    for regime in ("blind", "warm_start", "compile", "catalog", "perturbed_tree"):
        regime_runs = [run for run in runs if run.get("start_mode") == regime]
        lines.append(
            f"| {regime} | {len(regime_runs)} | "
            f"{sum(1 for run in regime_runs if run.get('claim_status') == 'recovered')} | "
            f"{sum(1 for run in regime_runs if _is_same_ast_return(run))} | "
            f"{sum(1 for run in regime_runs if _is_verified_equivalent_return(run))} | "
            f"{sum(1 for run in regime_runs if run.get('classification') == 'unsupported')} | "
            f"{sum(1 for run in regime_runs if run.get('classification') in {'failed', 'snapped_but_failed', 'soft_fit_only', 'execution_failure'})} |"
        )
    lines.extend(
        [
            "",
            "This table keeps blind, compiler-assisted warm-start, compile-only, catalog, and perturbed-basin evidence visibly separate before any narrative interpretation.",
            "",
        ]
    )
    return lines


def _proof_contract_section(runs: list[Mapping[str, Any]], aggregate: Mapping[str, Any]) -> list[str]:
    if not any(run.get("claim_id") for run in runs):
        return []
    proof_basin = _is_proof_basin_report(runs, aggregate)
    lines = [
        "## Proof Contract",
        "",
        "| Claim | Threshold | Status | Passed | Eligible | Rate |",
        "|-------|-----------|--------|--------|----------|------|",
    ]
    for row in aggregate.get("thresholds", []):
        lines.append(
            f"| {row['claim_id']} | {row['threshold_policy_id']} | {row['status']} | "
            f"{row['passed']} | {row['eligible']} | {row['rate']:.3f} |"
        )
    lines.extend(
        [
            "",
            "Bounded proof thresholds count only allowed verifier-owned training evidence classes; catalog and compile-only verification remain separate evidence classes.",
            "",
        ]
    )
    if proof_basin:
        lines.extend(
            [
                "Beer-Lambert high-noise probe rows are reported by the separate `proof-perturbed-basin-beer-probes` suite; they remain outside the bounded proof threshold table.",
                "",
                "### Perturbed Basin Status Taxonomy",
                "",
                "| Field | Meaning |",
                "|-------|---------|",
                "| `return_kind` | Raw perturbed-tree return path such as `same_ast_return`, `verified_equivalent_ast`, `snapped_but_failed`, or `soft_fit_only`. |",
                "| `raw_status` | Status before local repair, preserved even when a repair succeeds. |",
                "| `repair_status` | Local repair outcome; repaired candidates remain `repaired_candidate` rather than raw perturbed recovery. |",
                "",
            ]
        )
    return lines


def _is_proof_basin_report(runs: list[Mapping[str, Any]], aggregate: Mapping[str, Any]) -> bool:
    if any(run.get("suite_id") == "proof-perturbed-basin" for run in runs):
        return True
    return any(row.get("claim_id") == "paper-perturbed-true-tree-basin" for row in aggregate.get("thresholds", ()))


def _operator_family_report_section(
    runs: list[Mapping[str, Any]],
    campaign_dir: Path,
    table_paths: Mapping[str, Path],
) -> list[str]:
    operators = {_operator_family_label(run) for run in runs}
    if len(operators) <= 1:
        return []
    lines = [
        "## Operator-Family Comparison",
        "",
        "Family rows keep recovery regimes separate by formula, start mode, training mode, depth, fixed operator, and continuation schedule.",
        "",
    ]
    for label, key in (
        ("comparison markdown", "operator_family_comparison_md"),
        ("recovery CSV", "operator_family_recovery_csv"),
        ("diagnostics CSV", "operator_family_diagnostics_csv"),
        ("regression locks JSON", "operator_family_locks_json"),
    ):
        path = table_paths.get(key)
        if path is not None:
            rel = _relative_link(path, campaign_dir)
            lines.append(f"- [{label}]({rel})")
    lines.append("")
    return lines


def _depth_curve_report_section(aggregate: Mapping[str, Any]) -> list[str]:
    rows = list(aggregate.get("depth_curve", ()))
    if not rows:
        return []

    lines = [
        "## Depth Curve",
        "",
        "| Depth | Mode | Seeds | Recovered | Total | Rate | Median Best Loss | Median Post-Snap Loss | Median Runtime | Median Snap Margin |",
        "|-------|------|-------|-----------|-------|------|------------------|-----------------------|----------------|--------------------|",
    ]
    for row in rows:
        lines.append(
            f"| {row['depth']} | {row['start_mode']} | {row['seed_count']} | {row['recovered']} | {row['total']} | "
            f"{row['recovery_rate']:.3f} | {_format_optional(row['best_loss_median'])} | "
            f"{_format_optional(row['post_snap_loss_median'])} | {_format_optional(row['runtime_seconds_median'])} | "
            f"{_format_optional(row['snap_min_margin_median'])} |"
        )

    blind_rows = [row for row in rows if row.get("start_mode") == "blind"]
    perturbed_rows = [row for row in rows if row.get("start_mode") == "perturbed_tree"]
    blind_success_depths = [int(row["depth"]) for row in blind_rows if float(row.get("recovery_rate") or 0.0) > 0.0]
    perturbed_success_depths = [int(row["depth"]) for row in perturbed_rows if float(row.get("recovery_rate") or 0.0) >= 1.0]
    blind_phrase = (
        f"blind recovery only through depth {max(blind_success_depths)} in this inventory"
        if blind_success_depths
        else "no blind recovery in this inventory"
    )
    perturbed_phrase = (
        f"perturbed recovery at every measured depth through {max(perturbed_success_depths)}"
        if perturbed_success_depths
        else "perturbed recovery below the declared target"
    )
    lines.extend(
        [
            "",
            "The paper reports that blind recovery falls sharply with depth while perturbed true-tree starts return much more reliably. "
            f"This campaign shows {blind_phrase}, alongside {perturbed_phrase}. "
            "Those deeper blind failures are measured boundary evidence, not product regressions or failed proof claims.",
            "",
        ]
    )
    return lines


def _limitations_section(runs: list[Mapping[str, Any]]) -> str:
    blind_total = sum(1 for run in runs if run.get("start_mode") == "blind")
    blind_recovered = sum(
        1 for run in runs if run.get("start_mode") == "blind" and run.get("claim_status") == "recovered"
    )
    blind_pure_recovered = sum(
        1 for run in runs if run.get("start_mode") == "blind" and run.get("evidence_class") == "blind_training_recovered"
    )
    blind_scaffolded_recovered = sum(
        1
        for run in runs
        if run.get("start_mode") == "blind" and run.get("evidence_class") == "scaffolded_blind_training_recovered"
    )
    same_ast = sum(1 for run in runs if _is_same_ast_return(run))
    equivalent = sum(1 for run in runs if _is_verified_equivalent_return(run))
    unsupported = sum(1 for run in runs if run.get("classification") == "unsupported")
    failed = sum(1 for run in runs if run.get("classification") in {"failed", "snapped_but_failed", "soft_fit_only", "execution_failure"})
    blind_note = ""
    if blind_total:
        blind_note = (
            f" This campaign records {blind_scaffolded_recovered} scaffolded blind recoveries and "
            f"{blind_pure_recovered} pure random-initialized blind recoveries; compare declared pure-blind proof suites separately."
        )
    return "\n".join(
        [
            f"- Blind training recovery: {blind_recovered}/{blind_total} blind runs recovered.{blind_note}",
            f"- Same-AST exact return: {same_ast} runs snapped back to the compiled seed or exact target; useful basin evidence, not discovery.",
            f"- Verified-equivalent exact return: {equivalent} runs snapped to a different exact AST that verified.",
            f"- Unsupported gates: {unsupported} runs were blocked by compiler/depth/operator limits and remain in the denominator.",
            f"- Failed fits: {failed} runs did not pass verifier-owned recovery after training or execution.",
        ]
    )


def _depth_curve_recovery_svg(rows: list[Mapping[str, Any]]) -> str:
    if not rows:
        return _empty_svg("Depth-Curve Recovery", "No depth-curve rows available.", width=960, height=520)
    bars = [
        {
            "label": f"d{row['depth']} {row['start_mode']}",
            "value": float(row.get("recovery_rate") or 0.0),
            "display": f"{float(row.get('recovery_rate') or 0.0):.0%}",
        }
        for row in rows
    ]
    return _bar_chart_svg(
        "Depth-Curve Recovery by Depth and Mode",
        bars,
        y_label="recovered / total",
        max_value=1.0,
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
