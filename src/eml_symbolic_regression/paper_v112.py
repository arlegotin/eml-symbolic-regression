"""v1.12 paper draft and supplement artifacts."""

from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


DEFAULT_V112_DRAFT_DIR = Path("artifacts") / "paper" / "v1.11" / "draft"
DEFAULT_V111_PAPER_ROOT = Path("artifacts") / "paper" / "v1.11"
DEFAULT_V111_RAW_HYBRID_DIR = DEFAULT_V111_PAPER_ROOT / "raw-hybrid"


@dataclass(frozen=True)
class PaperDraftPaths:
    output_dir: Path
    manifest_json: Path
    abstract_md: Path
    methods_md: Path
    results_md: Path
    limitations_md: Path
    claim_taxonomy_json: Path
    claim_taxonomy_csv: Path
    claim_taxonomy_md: Path

    def as_dict(self) -> dict[str, str]:
        return {key: str(value) for key, value in self.__dict__.items()}


def write_v112_draft(
    *,
    output_dir: Path = DEFAULT_V112_DRAFT_DIR,
    paper_root: Path = DEFAULT_V111_PAPER_ROOT,
    raw_hybrid_dir: Path = DEFAULT_V111_RAW_HYBRID_DIR,
) -> PaperDraftPaths:
    """Write the first paper-shaped draft scaffold from the v1.11 package."""

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paper_root = Path(paper_root)
    raw_hybrid_dir = Path(raw_hybrid_dir)
    paths = PaperDraftPaths(
        output_dir=output_dir,
        manifest_json=output_dir / "manifest.json",
        abstract_md=output_dir / "abstract.md",
        methods_md=output_dir / "methods.md",
        results_md=output_dir / "results.md",
        limitations_md=output_dir / "limitations.md",
        claim_taxonomy_json=output_dir / "claim-taxonomy.json",
        claim_taxonomy_csv=output_dir / "claim-taxonomy.csv",
        claim_taxonomy_md=output_dir / "claim-taxonomy.md",
    )

    readiness_path = paper_root / "paper-readiness.md"
    audit_path = paper_root / "claim-audit.json"
    asset_manifest_path = paper_root / "assets" / "manifest.json"
    source_locks_path = paper_root / "source-locks.json"
    claim_ledger_path = raw_hybrid_dir / "claim-ledger.json"
    scientific_table_path = raw_hybrid_dir / "scientific-law-table.json"

    readiness = readiness_path.read_text(encoding="utf-8")
    audit = _read_json(audit_path)
    assets = _read_json(asset_manifest_path)
    claim_ledger = _read_json(claim_ledger_path)
    scientific = _read_json(scientific_table_path)

    taxonomy_rows = claim_taxonomy_rows(claim_ledger)
    _write_json(
        paths.claim_taxonomy_json,
        {"schema": "eml.v112_claim_taxonomy.v1", "generated_at": _now_iso(), "rows": taxonomy_rows},
    )
    _write_csv(paths.claim_taxonomy_csv, taxonomy_rows)
    paths.claim_taxonomy_md.write_text(_claim_taxonomy_markdown(taxonomy_rows), encoding="utf-8")

    paths.abstract_md.write_text(_abstract_markdown(readiness, scientific), encoding="utf-8")
    paths.methods_md.write_text(_methods_markdown(), encoding="utf-8")
    paths.results_md.write_text(_results_markdown(scientific, assets, audit), encoding="utf-8")
    paths.limitations_md.write_text(_limitations_markdown(), encoding="utf-8")

    source_paths = (
        readiness_path,
        audit_path,
        asset_manifest_path,
        source_locks_path,
        claim_ledger_path,
        scientific_table_path,
    )
    manifest = {
        "schema": "eml.v112_paper_draft.v1",
        "generated_at": _now_iso(),
        "output_dir": str(output_dir),
        "outputs": paths.as_dict(),
        "sources": [_source_lock(path.stem.replace("-", "_"), path) for path in source_paths],
        "claim_boundary": "draft scaffold preserves v1.11 regime separation and unsupported logistic/Planck status",
        "reproduction": {
            "command": f"PYTHONPATH=src python -m eml_symbolic_regression.cli paper-draft --output-dir {output_dir}",
        },
    }
    _write_json(paths.manifest_json, manifest)
    return paths


def claim_taxonomy_rows(claim_ledger: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Return paper-facing evidence-regime definitions with denominator rules."""

    ledger_rows = claim_ledger.get("rows") if isinstance(claim_ledger.get("rows"), list) else []
    by_regime: dict[str, list[Mapping[str, Any]]] = {}
    for row in ledger_rows:
        if not isinstance(row, Mapping):
            continue
        claim_id = str(row.get("claim_id") or "")
        if not claim_id.startswith("v111-regime-"):
            continue
        by_regime.setdefault(str(row.get("eligible_denominator") or ""), []).append(row)

    definitions = [
        (
            "pure_blind",
            "Pure blind",
            "Random-initialized blind training with scaffold initializers disabled.",
            "Only verifier-recovered rows in this class may support pure blind recovery rates.",
            True,
        ),
        (
            "scaffolded",
            "Scaffolded blind",
            "Blind training with declared structural scaffold initializers.",
            "Useful optimizer evidence, but not pure blind discovery.",
            False,
        ),
        (
            "warm_start",
            "Compiler warm start",
            "Training initialized from a compiled EML expression.",
            "Basin or compiler-assisted evidence, not random-initialized discovery.",
            False,
        ),
        (
            "same_ast",
            "Same-AST return",
            "Runs that return the exact compiled or known target AST.",
            "Strong representational and basin evidence, not discovery from scratch.",
            False,
        ),
        (
            "perturbed_basin",
            "Perturbed basin",
            "Known true-tree starts perturbed before optimization.",
            "Measures local basin stability, not blind search.",
            False,
        ),
        (
            "repair_refit",
            "Repair/refit",
            "Verifier-gated local repair or frozen-structure constant refit after snapping.",
            "Post-snap improvement evidence, not the original optimizer discovery event.",
            False,
        ),
        (
            "compile_only",
            "Compile-only",
            "Exact compiler diagnostics without training.",
            "Representation support or unsupported diagnostics, not training recovery.",
            False,
        ),
        (
            "unsupported",
            "Unsupported",
            "Rows blocked by support gates, compile depth, missing witnesses, or explicit unsupported status.",
            "Must remain visible in denominators where eligible and never count as recovered.",
            False,
        ),
        (
            "failed",
            "Failed",
            "Rows that ran but failed verifier recovery, snapping, or acceptable numerical criteria.",
            "Must remain visible and never count as recovered.",
            False,
        ),
    ]

    rows: list[dict[str, Any]] = []
    for evidence_class, label, definition, safe_claim, pure_blind in definitions:
        source_rows = _source_rows_for_taxonomy(evidence_class, by_regime)
        total = sum(int(row.get("total") or 0) for row in source_rows)
        verifier_recovered = sum(int(row.get("verifier_recovered") or 0) for row in source_rows)
        unsupported = sum(int(row.get("unsupported") or 0) for row in source_rows)
        failed = sum(int(row.get("failed") or 0) for row in source_rows)
        rows.append(
            {
                "evidence_class": evidence_class,
                "paper_label": label,
                "definition": definition,
                "denominator_rule": _denominator_rule(evidence_class),
                "eligible_for_pure_blind_rate": pure_blind,
                "eligible_for_verifier_recovery_rate": evidence_class not in {"unsupported", "failed"},
                "rate_source": "verifier-owned counts only",
                "safe_public_claim": safe_claim,
                "source_claim_ids": ";".join(str(row.get("claim_id")) for row in source_rows),
                "source_total": total,
                "source_verifier_recovered": verifier_recovered,
                "source_unsupported": unsupported,
                "source_failed": failed,
                "claim_boundary": "do not merge this class into pure blind discovery unless explicitly eligible",
            }
        )
    return rows


def _source_rows_for_taxonomy(evidence_class: str, by_regime: Mapping[str, list[Mapping[str, Any]]]) -> list[Mapping[str, Any]]:
    if evidence_class == "same_ast":
        return by_regime.get("same_ast_return", [])
    if evidence_class == "repair_refit":
        return [*by_regime.get("repaired", []), *by_regime.get("refit", [])]
    return by_regime.get(evidence_class, [])


def _denominator_rule(evidence_class: str) -> str:
    if evidence_class == "pure_blind":
        return "pure-blind suite rows only; scaffolds, warm starts, repairs, and perturbed starts excluded"
    if evidence_class in {"unsupported", "failed"}:
        return "visible negative rows inside their original regime denominator"
    return f"{evidence_class} rows are denominated separately from pure blind rows"


def _abstract_markdown(readiness: str, scientific: Mapping[str, Any]) -> str:
    supported = [
        str(row.get("law"))
        for row in scientific.get("rows", [])
        if isinstance(row, Mapping) and row.get("compile_support") == "supported" and row.get("verifier_status") == "recovered"
    ]
    supported_text = ", ".join(supported) if supported else "none"
    return "\n".join(
        [
            "# Abstract Draft Skeleton",
            "",
            "## Working Title",
            "",
            "Verifier-gated hybrid symbolic regression over complete EML trees",
            "",
            "## Abstract",
            "",
            "We study symbolic regression in the elementary-function basis generated by the single binary EML operator. The method searches a complete depth-bounded soft EML tree, snaps the optimized categorical choices into an exact tree, applies local repair or refit only under verifier ownership, and reports formulas only after held-out, extrapolation, and high-precision checks.",
            "",
            "The current evidence supports a bounded claim: shallow and scaffolded regimes can recover verified formulas, compiler and same-AST warm starts provide useful basin evidence, and blind recovery degrades quickly with depth. The paper should present this as a verifier-gated hybrid EML methods and evidence study, not as broad superiority over symbolic-regression systems.",
            "",
            f"Supported scientific-law rows in the v1.11 source package: {supported_text}. Logistic and Planck remain unsupported diagnostics unless a later strict support and verifier artifact passes.",
            "",
            "## Evidence Hooks",
            "",
            "- Primary evidence package: `artifacts/paper/v1.11/`.",
            "- Claim audit: `artifacts/paper/v1.11/claim-audit.json`.",
            "- Claim taxonomy: `artifacts/paper/v1.11/draft/claim-taxonomy.md`.",
            "- Evidence refresh placeholders: Phase 65 will add current-code shallow and depth-refresh rows.",
            "",
            "## Framing Guardrail",
            "",
            readiness.split("## Paper Framing", 1)[-1].strip() if "## Paper Framing" in readiness else readiness.strip(),
            "",
        ]
    )


def _methods_markdown() -> str:
    return "\n".join(
        [
            "# Methods Draft Skeleton",
            "",
            "## EML Representation",
            "",
            "Define the EML operator and the complete depth-bounded binary tree grammar. State that exact candidate formulas are represented as EML ASTs, with literal constants reported as explicit provenance when used.",
            "",
            "## Differentiable Search",
            "",
            "Describe the PyTorch `complex128` soft master tree, categorical logits, restart budgets, hardening, and training-mode numerical guards. Make clear that soft loss is a candidate-generation signal, not the recovery criterion.",
            "",
            "## Snapping and Candidate Pooling",
            "",
            "Describe argmax snapping, late-hardening candidate pools, fallback preservation, local cleanup, and post-snap refit as verifier-ranked stages.",
            "",
            "## Compiler and Motif Library",
            "",
            "Describe the SymPy-to-EML compiler as a structural, validation-gated source of exact seeds and diagnostics. Motifs are reusable transformations; formula-name recognizers and silent gate relaxation are excluded.",
            "",
            "## Verification Contract",
            "",
            "State the verifier-owned recovery contract: training split, held-out split, extrapolation split, exact candidate checks, and high-precision checks. A row is recovered only when the verifier status passes.",
            "",
            "## Evidence Regimes",
            "",
            "Use `claim-taxonomy.md` as the methods table for regime separation: pure blind, scaffolded, warm-start, same-AST, perturbed-basin, repair/refit, compile-only, unsupported, and failed.",
            "",
        ]
    )


def _results_markdown(scientific: Mapping[str, Any], assets: Mapping[str, Any], audit: Mapping[str, Any]) -> str:
    rows = [row for row in scientific.get("rows", []) if isinstance(row, Mapping)]
    supported = [str(row.get("law")) for row in rows if row.get("compile_support") == "supported" and row.get("verifier_status") == "recovered"]
    unsupported = [str(row.get("law")) for row in rows if row.get("compile_support") == "unsupported" or row.get("verifier_status") == "unsupported"]
    figure_count = assets.get("counts", {}).get("figures") if isinstance(assets.get("counts"), Mapping) else "unknown"
    table_count = assets.get("counts", {}).get("tables") if isinstance(assets.get("counts"), Mapping) else "unknown"
    return "\n".join(
        [
            "# Results Draft Skeleton",
            "",
            "## Representation and Verification",
            "",
            "Report exact EML AST support, source-locked package generation, and the v1.11 claim audit. The current audit status is "
            f"`{audit.get('status')}`.",
            "",
            "## Regime-Separated Recovery",
            "",
            "Use the regime recovery table and taxonomy table to report pure blind, scaffolded, warm-start, same-AST, perturbed-basin, repair/refit, compile-only, unsupported, and failed rows separately.",
            "",
            "## Depth-Limit Story",
            "",
            "Use archived v1.6 depth-degradation evidence as historical boundary evidence, then replace or supplement with Phase 65 current-code depth-refresh rows.",
            "",
            "## Scientific-Law Rows",
            "",
            f"Supported rows: {', '.join(supported) if supported else 'none'}.",
            "",
            f"Unsupported or diagnostic rows: {', '.join(unsupported) if unsupported else 'none'}. Logistic and Planck remain unsupported unless strict support and verifier recovery both pass.",
            "",
            "## Figures and Tables",
            "",
            f"The v1.11 package already contains {figure_count} figures and {table_count} source tables. Phase 66 will add paper-facing captions, motif evolution, pipeline, negative-results, and taxonomy presentation artifacts.",
            "",
        ]
    )


def _limitations_markdown() -> str:
    return "\n".join(
        [
            "# Limitations Draft Skeleton",
            "",
            "## Blind Search Depth",
            "",
            "Blind gradient search degrades sharply as exact EML depth increases. The paper should report this as a central limitation, not as a minor caveat.",
            "",
            "## Evidence Regime Separation",
            "",
            "Scaffolded, warm-start, same-AST, perturbed true-tree, repair/refit, and compile-only evidence are useful but do not establish pure blind discovery.",
            "",
            "## Logistic and Planck",
            "",
            "Logistic and Planck have improved relaxed-depth diagnostics, but remain unsupported under strict support gates unless a later phase produces strict compiler support and verifier-owned recovery.",
            "",
            "## Baselines",
            "",
            "Current prediction-only baselines are diagnostic, not matched-budget symbolic-regression comparators. A conventional SR baseline is useful only if it is locally feasible without changing the paper's recovery denominators.",
            "",
            "## Scope",
            "",
            "The paper should claim a reproducible verifier-gated hybrid EML pipeline with honest boundaries, not universal deep recovery or broad symbolic-regression superiority.",
            "",
        ]
    )


def _claim_taxonomy_markdown(rows: list[Mapping[str, Any]]) -> str:
    columns = [
        "evidence_class",
        "paper_label",
        "denominator_rule",
        "eligible_for_pure_blind_rate",
        "eligible_for_verifier_recovery_rate",
        "safe_public_claim",
    ]
    return "\n".join(["# Claim Taxonomy", "", *_markdown_table_lines(rows, columns)])


def _markdown_table_lines(rows: list[Mapping[str, Any]], columns: list[str]) -> list[str]:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(_format_markdown(row.get(column)) for column in columns) + " |")
    lines.append("")
    return lines


def _format_markdown(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value if value is not None else "").replace("|", "\\|")


def _write_csv(path: Path, rows: list[Mapping[str, Any]]) -> None:
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(str(key))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: _csv_value(row.get(column)) for column in columns})


def _csv_value(value: Any) -> Any:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True)
    if value is None:
        return ""
    return value


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _source_lock(source_id: str, path: Path) -> dict[str, Any]:
    return {"source_id": source_id, "path": str(path), "sha256": _sha256(path)}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
