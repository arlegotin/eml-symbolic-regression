"""v1.16 paper-strength GEML/i*pi EML decision package."""

from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

from .benchmark import V115_GEML_TARGETS, V115_NEGATIVE_CONTROL_TARGETS, V115_OSCILLATORY_TARGETS, builtin_suite


DEFAULT_V116_PACKAGE_DIR = Path("artifacts") / "paper" / "v1.16-geml"
DEFAULT_V116_CAMPAIGN_DIR = Path("artifacts") / "campaigns" / "v1.16-geml-pilot"


class V116PackageError(RuntimeError):
    """Raised when the v1.16 package cannot be safely written."""


@dataclass(frozen=True)
class V116PackagePaths:
    output_dir: Path
    manifest_json: Path
    gate_config_json: Path
    campaign_contract_json: Path
    gate_evaluation_json: Path
    decision_md: Path
    claim_audit_json: Path
    claim_audit_md: Path
    source_locks_json: Path
    reproduction_md: Path

    def as_dict(self) -> dict[str, str]:
        return {key: str(value) for key, value in self.__dict__.items()}


def v116_package_paths(output_dir: Path = DEFAULT_V116_PACKAGE_DIR) -> V116PackagePaths:
    output_dir = Path(output_dir)
    return V116PackagePaths(
        output_dir=output_dir,
        manifest_json=output_dir / "manifest.json",
        gate_config_json=output_dir / "gate-config.json",
        campaign_contract_json=output_dir / "campaign-contract.json",
        gate_evaluation_json=output_dir / "gate-evaluation.json",
        decision_md=output_dir / "decision.md",
        claim_audit_json=output_dir / "claim-audit.json",
        claim_audit_md=output_dir / "claim-audit.md",
        source_locks_json=output_dir / "source-locks.json",
        reproduction_md=output_dir / "reproduction.md",
    )


def default_v116_gate_config(*, min_unique_seeds: int = 3) -> dict[str, Any]:
    """Return the fail-closed v1.16 paper-strength gate."""

    return {
        "schema": "eml.v116_paper_strength_gate.v1",
        "outcomes": {
            "paper_positive": "Verifier-gated exact i*pi recovery beats raw EML on natural-bias targets under the full matched protocol.",
            "promising_preliminary": "Exact i*pi signal exists but the full paper denominator is incomplete.",
            "negative": "Raw EML wins or no exact i*pi recovery signal appears under the declared protocol.",
            "inconclusive": "Evidence is insufficient or confounded; no positive claim is allowed.",
        },
        "positive_recovery_numerator": "trained_exact_recovery_only",
        "diagnostic_only_classes": [
            "loss_only",
            "same_ast_seed_round_trip",
            "verified_equivalent_warm_start",
            "repaired_candidate",
            "compile_only_verified_support",
            "unsupported",
        ],
        "thresholds": {
            "declared_targets": list(V115_GEML_TARGETS),
            "natural_bias_targets": list(V115_OSCILLATORY_TARGETS),
            "negative_control_targets": list(V115_NEGATIVE_CONTROL_TARGETS),
            "min_unique_seeds_for_paper_positive": int(min_unique_seeds),
            "min_natural_ipi_recovery_wins": 1,
            "min_ipi_minus_raw_recovery_wins": 1,
            "max_negative_control_ipi_recovery_wins": 0,
            "require_complete_matched_denominator": True,
            "require_source_locks": True,
        },
        "fail_closed_rules": [
            "loss-only improvement cannot be promoted to recovery",
            "same-AST or exact-seed returns cannot enter trained recovery denominators",
            "negative-control i*pi wins block paper-positive interpretation",
            "missing source locks or incomplete denominators block paper-positive interpretation",
        ],
    }


def default_v116_campaign_contract(*, seeds: Iterable[int] = (0, 1, 2)) -> dict[str, Any]:
    """Return the matched campaign denominator contract for v1.16."""

    seeds = tuple(int(seed) for seed in seeds)
    return {
        "schema": "eml.v116_matched_campaign_contract.v1",
        "suite_ids": {
            "smoke": "v1.16-geml-smoke",
            "pilot": "v1.16-geml-pilot",
            "full": "v1.16-geml-full",
        },
        "targets": {
            "natural_bias": list(V115_OSCILLATORY_TARGETS),
            "negative_controls": list(V115_NEGATIVE_CONTROL_TARGETS),
        },
        "matched_fields": [
            "formula",
            "seed",
            "depth",
            "steps",
            "restarts",
            "hardening_steps",
            "hardening_emit_interval",
            "dataset.points",
            "dataset.tolerance",
            "constants_policy",
            "snap_rule",
            "verifier_gate",
        ],
        "operator_families": ["raw_eml", "ipi_eml"],
        "seeds": list(seeds),
        "verifier_gate": "trained exact candidate selected by verifier across train, held-out, extrapolation, and high-precision checks",
        "claim_denominator_rules": {
            "loss_only": "diagnostic_only",
            "same_ast_seed_round_trip": "excluded_from_trained_exact_recovery",
            "compile_only_verified_support": "excluded_from_trained_exact_recovery",
            "negative_controls": "visible_and_claim_blocking",
        },
        "resource_metadata_required": ["wall_clock_seconds", "attempt_count", "candidate_count", "code_version", "platform"],
    }


def evaluate_v116_gate(
    paired_summary: Mapping[str, Any] | None = None,
    classification: Iterable[Mapping[str, Any]] = (),
    *,
    paired_rows: Iterable[Mapping[str, Any]] = (),
    gate_config: Mapping[str, Any] | None = None,
    source_locks_ok: bool = True,
) -> dict[str, Any]:
    """Classify v1.16 GEML evidence without letting loss-only rows carry claims."""

    paired_summary = paired_summary or {}
    gate_config = gate_config or default_v116_gate_config()
    thresholds = gate_config.get("thresholds") if isinstance(gate_config.get("thresholds"), Mapping) else {}
    rows = [dict(row) for row in paired_rows]
    families = [dict(row) for row in classification]
    by_family = {str(row.get("target_family") or "unknown"): row for row in families}
    natural_families = {family for family in by_family if family != "negative_control"}
    natural_rows = [row for family, row in by_family.items() if family in natural_families]

    paired_row_count = int(paired_summary.get("paired_rows") or sum(int(row.get("paired_rows") or 0) for row in families))
    declared_targets = tuple(thresholds.get("declared_targets") or V115_GEML_TARGETS)
    min_unique_seeds = int(thresholds.get("min_unique_seeds_for_paper_positive") or 1)
    unique_seeds = _unique_seed_count(rows) or _summary_seed_count(paired_summary) or 1
    complete_denominator = paired_row_count >= len(declared_targets) * min_unique_seeds and unique_seeds >= min_unique_seeds

    natural_ipi_wins = sum(int(row.get("ipi_recovery_wins") or 0) for row in natural_rows)
    natural_raw_wins = sum(int(row.get("raw_recovery_wins") or 0) for row in natural_rows)
    negative_control = by_family.get("negative_control", {})
    negative_control_ipi_wins = int(negative_control.get("ipi_recovery_wins") or 0)
    loss_only_outcomes = int(paired_summary.get("loss_only_outcomes") or sum(int(row.get("loss_only_outcomes") or 0) for row in families))
    exact_signal = natural_ipi_wins >= int(thresholds.get("min_natural_ipi_recovery_wins") or 1)
    ipi_delta = natural_ipi_wins - natural_raw_wins
    negative_controls_clean = negative_control_ipi_wins <= int(thresholds.get("max_negative_control_ipi_recovery_wins") or 0)
    paper_positive_ready = (
        exact_signal
        and ipi_delta >= int(thresholds.get("min_ipi_minus_raw_recovery_wins") or 1)
        and negative_controls_clean
        and complete_denominator
        and source_locks_ok
    )

    if paper_positive_ready:
        decision = "paper_positive"
        rationale = "Exact verifier-gated i*pi recovery wins satisfy the full matched denominator and negative-control gate."
    elif exact_signal and ipi_delta > 0 and negative_controls_clean:
        decision = "promising_preliminary"
        rationale = "Exact i*pi recovery signal exists, but the full paper-positive denominator is incomplete."
    elif natural_raw_wins > natural_ipi_wins or (complete_denominator and natural_ipi_wins == 0):
        decision = "negative"
        rationale = "The matched exact-recovery evidence does not support an i*pi advantage."
    else:
        decision = "inconclusive"
        rationale = "The evidence is incomplete, loss-only, or confounded; no positive claim is allowed."

    blockers: list[str] = []
    if not exact_signal:
        blockers.append("no_natural_ipi_exact_recovery_signal")
    if not complete_denominator:
        blockers.append("incomplete_matched_denominator")
    if not negative_controls_clean:
        blockers.append("negative_control_ipi_recovery_win")
    if not source_locks_ok:
        blockers.append("missing_or_failed_source_locks")
    if loss_only_outcomes and not exact_signal:
        blockers.append("loss_only_signal_without_exact_recovery")

    return {
        "schema": "eml.v116_gate_evaluation.v1",
        "decision": decision,
        "rationale": rationale,
        "metrics": {
            "paired_rows": paired_row_count,
            "declared_targets": len(declared_targets),
            "unique_seeds": unique_seeds,
            "min_unique_seeds_for_paper_positive": min_unique_seeds,
            "complete_denominator": complete_denominator,
            "natural_ipi_recovery_wins": natural_ipi_wins,
            "natural_raw_recovery_wins": natural_raw_wins,
            "natural_ipi_minus_raw_recovery_wins": ipi_delta,
            "negative_control_ipi_recovery_wins": negative_control_ipi_wins,
            "loss_only_outcomes": loss_only_outcomes,
            "source_locks_ok": bool(source_locks_ok),
        },
        "blockers": blockers,
        "gate": gate_config,
    }


def build_v116_claim_audit(
    claim_text: str,
    *,
    gate_evaluation: Mapping[str, Any],
    gate_config: Mapping[str, Any] | None = None,
    source_locks: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Audit v1.16 paper claims against the predefined gate."""

    gate_config = gate_config or default_v116_gate_config()
    source_locks = source_locks or {}
    lower_claim = claim_text.lower()
    decision = str(gate_evaluation.get("decision") or "")
    checks = [
        _audit_check(
            "gate_has_all_outcomes",
            {"paper_positive", "promising_preliminary", "negative", "inconclusive"} <= set((gate_config.get("outcomes") or {}).keys()),
            "Gate config defines all allowed v1.16 outcomes.",
        ),
        _audit_check(
            "exact_recovery_only_positive_gate",
            gate_config.get("positive_recovery_numerator") == "trained_exact_recovery_only",
            "Positive recovery numerator is verifier-gated trained exact recovery only.",
        ),
        _audit_check(
            "blocks_loss_only_recovery_claims",
            not _contains_any(lower_claim, ("loss-only recovery", "loss only recovery", "loss-only proves recovery")),
            "Claim text does not promote loss-only improvement to recovery.",
        ),
        _audit_check(
            "blocks_global_superiority_language",
            not _contains_any(lower_claim, ("global superiority", "globally better", "universally better", "dominates raw eml")),
            "Claim text avoids global raw/i*pi superiority claims.",
        ),
        _audit_check(
            "blocks_broad_blind_recovery_language",
            not _contains_any(lower_claim, ("broad blind recovery", "solves blind recovery", "recovers arbitrary formulas")),
            "Claim text avoids broad blind-recovery claims.",
        ),
        _audit_check(
            "blocks_full_universality_language",
            not _contains_any(lower_claim, ("full universality", "scientific-calculator universality", "all elementary functions")),
            "Claim text avoids full i*pi/GEML universality claims.",
        ),
        _audit_check(
            "negative_controls_visible",
            "negative control" in lower_claim or "negative-control" in lower_claim,
            "Claim text keeps negative controls visible.",
        ),
        _audit_check(
            "paper_positive_requires_gate_pass",
            ("paper_positive" not in lower_claim and "paper positive" not in lower_claim) or decision == "paper_positive",
            "Paper-positive language appears only when the gate evaluates paper_positive.",
        ),
        _audit_check(
            "source_locks_present",
            bool(source_locks.get("inputs") or source_locks.get("outputs")),
            "Package includes source-lock tables.",
        ),
    ]
    return {
        "schema": "eml.v116_claim_audit.v1",
        "status": "passed" if all(check["status"] == "passed" for check in checks) else "failed",
        "decision": decision,
        "checks": checks,
    }


def write_v116_paper_package(
    output_dir: Path = DEFAULT_V116_PACKAGE_DIR,
    *,
    campaign_dir: Path = DEFAULT_V116_CAMPAIGN_DIR,
    overwrite: bool = False,
    min_unique_seeds: int = 3,
) -> V116PackagePaths:
    """Write v1.16 contract, gate evaluation, and claim audit artifacts."""

    output_dir = Path(output_dir)
    paths = v116_package_paths(output_dir)
    if paths.manifest_json.exists() and not overwrite:
        raise V116PackageError(f"{paths.manifest_json} already exists; pass overwrite=True to refresh")
    paths.output_dir.mkdir(parents=True, exist_ok=True)

    gate_config = default_v116_gate_config(min_unique_seeds=min_unique_seeds)
    contract = default_v116_campaign_contract(seeds=range(min_unique_seeds))
    paired_rows = _read_paired_rows(Path(campaign_dir))
    paired_summary = _read_json(Path(campaign_dir) / "tables" / "geml-paired-summary.json") if (Path(campaign_dir) / "tables" / "geml-paired-summary.json").is_file() else _summary_from_rows(paired_rows)
    classification = _classification_from_rows(paired_rows)
    locks = _source_locks_payload(
        [
            ("roadmap", Path(".planning/ROADMAP.md"), "input"),
            ("requirements", Path(".planning/REQUIREMENTS.md"), "input"),
            ("campaign_manifest", Path(campaign_dir) / "campaign-manifest.json", "input"),
            ("geml_paired_summary", Path(campaign_dir) / "tables" / "geml-paired-summary.json", "input"),
            ("geml_paired_comparison", Path(campaign_dir) / "tables" / "geml-paired-comparison.csv", "input"),
        ]
    )
    source_locks_ok = all(item["status"] == "locked" for item in locks["inputs"])
    evaluation = evaluate_v116_gate(
        paired_summary,
        classification,
        paired_rows=paired_rows,
        gate_config=gate_config,
        source_locks_ok=source_locks_ok,
    )
    decision_md = _decision_markdown(evaluation, classification, Path(campaign_dir))
    audit = build_v116_claim_audit(decision_md, gate_evaluation=evaluation, gate_config=gate_config, source_locks=locks)

    _write_json(paths.gate_config_json, gate_config)
    _write_json(paths.campaign_contract_json, contract)
    _write_json(paths.gate_evaluation_json, evaluation)
    paths.decision_md.write_text(decision_md, encoding="utf-8")
    _write_json(paths.claim_audit_json, audit)
    paths.claim_audit_md.write_text(_claim_audit_markdown(audit), encoding="utf-8")
    paths.reproduction_md.write_text(_reproduction_markdown(Path(campaign_dir), min_unique_seeds), encoding="utf-8")
    locks["outputs"] = _source_locks(
        [
            ("gate_config", paths.gate_config_json),
            ("campaign_contract", paths.campaign_contract_json),
            ("gate_evaluation", paths.gate_evaluation_json),
            ("decision", paths.decision_md),
            ("claim_audit_json", paths.claim_audit_json),
            ("claim_audit_md", paths.claim_audit_md),
            ("reproduction", paths.reproduction_md),
        ],
        role="output",
    )
    _write_json(paths.source_locks_json, locks)
    manifest = {
        "schema": "eml.v116_paper_decision_package.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "decision": evaluation["decision"],
        "rationale": evaluation["rationale"],
        "campaign_dir": str(campaign_dir),
        "gate_config": str(paths.gate_config_json),
        "campaign_contract": str(paths.campaign_contract_json),
        "gate_evaluation": str(paths.gate_evaluation_json),
        "claim_audit": {"status": audit["status"], "json": str(paths.claim_audit_json), "markdown": str(paths.claim_audit_md)},
        "source_locks": str(paths.source_locks_json),
        "reproduction": str(paths.reproduction_md),
    }
    _write_json(paths.manifest_json, manifest)
    return paths


def _classification_from_rows(rows: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for row in rows:
        family = str(row.get("target_family") or "unknown")
        grouped.setdefault(family, []).append(row)
    families = sorted(set(grouped) | {"negative_control", "periodic", "harmonic", "damped_oscillation", "standing_wave", "log_periodic"})
    result: list[dict[str, Any]] = []
    for family in families:
        items = grouped.get(family, [])
        outcomes = _count_by_key(items, "comparison_outcome")
        loss_only = outcomes.get("ipi_lower_post_snap_mse", 0) + outcomes.get("raw_lower_post_snap_mse", 0)
        result.append(
            {
                "target_family": family,
                "declared_targets": _declared_family_count(family),
                "paired_rows": len(items),
                "ipi_recovery_wins": outcomes.get("ipi_recovery_win", 0),
                "raw_recovery_wins": outcomes.get("raw_recovery_win", 0),
                "both_recovered": outcomes.get("both_recovered", 0),
                "neither_recovered": outcomes.get("neutral_no_recovery", 0) + loss_only,
                "loss_only_outcomes": loss_only,
                "ipi_lower_post_snap_mse": outcomes.get("ipi_lower_post_snap_mse", 0),
                "raw_lower_post_snap_mse": outcomes.get("raw_lower_post_snap_mse", 0),
            }
        )
    return result


def _summary_from_rows(rows: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = [dict(row) for row in rows]
    outcomes = _count_by_key(rows, "comparison_outcome")
    return {
        "schema": "eml.geml_paired_summary.v1",
        "paired_rows": len(rows),
        "ipi_recovery_wins": outcomes.get("ipi_recovery_win", 0),
        "raw_recovery_wins": outcomes.get("raw_recovery_win", 0),
        "both_recovered": outcomes.get("both_recovered", 0),
        "loss_only_outcomes": outcomes.get("ipi_lower_post_snap_mse", 0) + outcomes.get("raw_lower_post_snap_mse", 0),
        "unique_seeds": _unique_seed_count(rows),
    }


def _declared_family_count(family: str) -> int:
    suite = builtin_suite("v1.15-geml-oscillatory")
    formulas = {case.formula for case in suite.cases if _family_for_tags(case.tags) == family}
    return len(formulas)


def _family_for_tags(tags: Iterable[Any]) -> str:
    values = {str(tag) for tag in tags}
    if "negative_control" in values:
        return "negative_control"
    if "log_periodic" in values:
        return "log_periodic"
    if "damped_oscillation" in values:
        return "damped_oscillation"
    if "standing_wave" in values:
        return "standing_wave"
    if "harmonic" in values:
        return "harmonic"
    if "periodic" in values:
        return "periodic"
    return "unknown"


def _read_paired_rows(campaign_dir: Path) -> list[dict[str, Any]]:
    path = campaign_dir / "tables" / "geml-paired-comparison.csv"
    if not path.is_file():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _unique_seed_count(rows: Iterable[Mapping[str, Any]]) -> int:
    seeds = {str(row.get("seed")) for row in rows if row.get("seed") not in {None, ""}}
    return len(seeds)


def _summary_seed_count(summary: Mapping[str, Any]) -> int:
    for key in ("unique_seeds", "seed_count"):
        if summary.get(key) is not None:
            return int(summary[key])
    return 0


def _count_by_key(rows: Iterable[Mapping[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = str(row.get(key) or "")
        counts[value] = counts.get(value, 0) + 1
    return counts


def _decision_markdown(evaluation: Mapping[str, Any], classification: Iterable[Mapping[str, Any]], campaign_dir: Path) -> str:
    metrics = evaluation.get("metrics") if isinstance(evaluation.get("metrics"), Mapping) else {}
    lines = [
        "# v1.16 GEML/i*pi EML Paper Decision",
        "",
        f"**Decision:** `{evaluation.get('decision')}`",
        "",
        str(evaluation.get("rationale") or ""),
        "",
        "The decision is controlled by the predefined paper-strength gate. Loss-only improvements are diagnostics, not recovery. Negative-control rows remain visible and claim-blocking.",
        "",
        f"Campaign directory: `{campaign_dir}`",
        "",
        "## Gate Metrics",
        "",
        f"- Paired rows: {metrics.get('paired_rows')}",
        f"- Declared targets: {metrics.get('declared_targets')}",
        f"- Unique seeds: {metrics.get('unique_seeds')}",
        f"- Complete denominator: {metrics.get('complete_denominator')}",
        f"- Natural i*pi exact recovery wins: {metrics.get('natural_ipi_recovery_wins')}",
        f"- Natural raw exact recovery wins: {metrics.get('natural_raw_recovery_wins')}",
        f"- Negative-control i*pi exact recovery wins: {metrics.get('negative_control_ipi_recovery_wins')}",
        f"- Loss-only outcomes: {metrics.get('loss_only_outcomes')}",
        "",
        "## Target Families",
        "",
        "| Family | Declared | Pairs | i*pi Wins | Raw Wins | Loss-Only |",
        "|--------|----------|-------|-----------|----------|-----------|",
    ]
    for row in classification:
        lines.append(
            f"| {row.get('target_family')} | {row.get('declared_targets')} | {row.get('paired_rows')} | "
            f"{row.get('ipi_recovery_wins')} | {row.get('raw_recovery_wins')} | {row.get('loss_only_outcomes')} |"
        )
    lines.append("")
    return "\n".join(lines)


def _claim_audit_markdown(audit: Mapping[str, Any]) -> str:
    lines = ["# v1.16 Claim Audit", "", f"Status: `{audit.get('status')}`", "", "| Check | Status | Description |", "|-------|--------|-------------|"]
    for check in audit.get("checks", []):
        lines.append(f"| {check['id']} | {check['status']} | {check['description']} |")
    lines.append("")
    return "\n".join(lines)


def _reproduction_markdown(campaign_dir: Path, min_unique_seeds: int) -> str:
    return "\n".join(
        [
            "# Reproducing the v1.16 GEML Decision Package",
            "",
            "Run the v1.16 pilot campaign:",
            "",
            "```bash",
            "PYTHONPATH=src python -m eml_symbolic_regression.cli campaign geml-v116-pilot --label v1.16-geml-pilot --overwrite",
            "```",
            "",
            "Refresh this package:",
            "",
            "```bash",
            f"PYTHONPATH=src python -m eml_symbolic_regression.cli geml-paper-v116 --campaign-dir {campaign_dir} --min-unique-seeds {min_unique_seeds} --overwrite",
            "```",
            "",
        ]
    )


def _audit_check(check_id: str, passed: bool, description: str) -> dict[str, str]:
    return {"id": check_id, "status": "passed" if passed else "failed", "description": description}


def _contains_any(text: str, phrases: Iterable[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def _source_locks_payload(items: Iterable[tuple[str, Path, str]]) -> dict[str, Any]:
    grouped = {"schema": "eml.v116_source_locks.v1", "inputs": [], "outputs": []}
    for source_id, path, role in items:
        grouped["inputs" if role == "input" else "outputs"].extend(_source_locks([(source_id, path)], role=role))
    return grouped


def _source_locks(items: Iterable[tuple[str, Path]], *, role: str) -> list[dict[str, Any]]:
    locks: list[dict[str, Any]] = []
    for source_id, path in items:
        if not path.is_file():
            locks.append({"source_id": source_id, "role": role, "path": str(path), "status": "missing"})
            continue
        locks.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "status": "locked",
                "sha256": _sha256(path),
                "bytes": path.stat().st_size,
            }
        )
    return locks


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
