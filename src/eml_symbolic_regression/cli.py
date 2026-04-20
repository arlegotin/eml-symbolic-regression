"""Command line interface for EML symbolic regression demos."""

from __future__ import annotations

import argparse
import json
import shlex
from pathlib import Path
from typing import Any

import numpy as np

from .benchmark import (
    START_MODES,
    RunFilter,
    list_builtin_suites,
    load_suite,
    run_benchmark_suite,
    suite_with_semantics_mode,
    write_aggregate_reports,
)
from .campaign import DEFAULT_CAMPAIGN_ROOT, campaign_preset, list_campaign_presets, run_campaign
from .cleanup import cleanup_candidate
from .compiler import CompilerConfig, UnsupportedExpression, compile_and_validate, diagnose_compile_expression
from .datasets import demo_specs, expanded_dataset_manifest, expanded_dataset_specs, get_demo, proof_dataset_manifest
from .diagnostics import (
    DEFAULT_BASELINE_CAMPAIGNS,
    run_diagnostic_subset,
    write_baseline_triage,
    write_campaign_comparison,
    write_perturbed_basin_bound_report,
)
from .family_triage import (
    DEFAULT_EVIDENCE_OUTPUT_DIR,
    DEFAULT_TRIAGE_OUTPUT_DIR,
    write_family_evidence_manifest,
    write_family_triage,
)
from .optimize import TrainingConfig, fit_eml_tree
from .paper_assets import DEFAULT_PAPER_ASSETS_OUTPUT_DIR, write_paper_assets
from .paper_decision import DEFAULT_PAPER_OUTPUT_ROOT, write_paper_decision_package
from .paper_diagnostics import DEFAULT_PAPER_DIAGNOSTICS_OUTPUT_DIR, write_paper_diagnostics
from .paper_package import DEFAULT_V111_PAPER_PACKAGE_DIR, write_v111_paper_package
from .paper_v112 import (
    DEFAULT_V112_DRAFT_DIR,
    DEFAULT_V112_REFRESH_DIR,
    DEFAULT_V112_SUPPLEMENT_DIR,
    DEFAULT_V112_TRAINING_DETAIL_DIR,
    write_v112_draft,
    write_v112_evidence_refresh,
)
from .paper_v112 import (
    write_v112_bounded_probes,
    write_v112_paper_facing_assets,
    write_v112_supplement,
    write_v112_training_detail_assets,
)
from .proof import list_claims
from .proof_campaign import DEFAULT_PROOF_OUTPUT_ROOT, PROOF_CAMPAIGN_PRESETS, run_proof_campaign
from .publication import DEFAULT_V113_PUBLICATION_DIR, write_publication_rebuild
from .raw_hybrid_paper import DEFAULT_RAW_HYBRID_OUTPUT_DIR, raw_hybrid_paper_presets, write_raw_hybrid_paper_package
from .verify import verify_candidate
from .warm_start import PerturbationConfig, fit_warm_started_eml_tree


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def list_demos(args: argparse.Namespace | None = None) -> int:
    for name, spec in sorted(demo_specs().items()):
        print(f"{name}: {spec.description}")
    return 0


def list_datasets(args: argparse.Namespace | None = None) -> int:
    for name, spec in sorted(expanded_dataset_specs().items()):
        print(f"{name}: {spec.description} [{spec.classification}/{spec.category}]")
    return 0


def run_demo(args: argparse.Namespace) -> int:
    spec = get_demo(args.name)
    splits = spec.make_splits(points=args.points, seed=args.seed)
    stage_statuses: dict[str, str] = {}
    report = verify_candidate(
        spec.candidate,
        splits,
        tolerance=args.tolerance,
        recovered_requires_exact_eml=True,
    )
    stage_statuses["catalog_showcase"] = report.status
    cleanup = cleanup_candidate(spec.candidate, splits, tolerance=args.tolerance)
    payload: dict[str, Any] = {
        "schema": "eml.demo_report.v1",
        "demo": spec.name,
        "description": spec.description,
        "candidate_kind": getattr(spec.candidate, "candidate_kind", "unknown"),
        "claim_status": report.status,
        "candidate": {
            "sympy": str(spec.candidate.to_sympy()),
        },
        "verification": report.as_dict(),
        "cleanup": cleanup.as_dict(),
        "stage_statuses": stage_statuses,
    }
    if spec.name == "planck":
        payload["stretch"] = {
            "status": "reported",
            "reason": "normalized_planck_is_stretch_target",
            "guaranteed_trained_recovery": False,
        }
        stage_statuses["stretch"] = "reported"

    if args.train_eml:
        train = splits[0]
        config = TrainingConfig(
            depth=args.depth,
            variables=(spec.variable,),
            steps=args.steps,
            restarts=args.restarts,
            seed=args.seed,
            lr=args.lr,
            hardening_steps=args.hardening_steps,
            hardening_temperature_end=args.hardening_temperature_end,
            hardening_emit_interval=args.hardening_emit_interval,
            semantics_mode=args.semantics_mode,
        )
        fit = fit_eml_tree(
            train.inputs,
            train.target,
            config,
            verification_splits=splits,
            tolerance=args.tolerance,
        )
        payload["trained_eml_candidate"] = fit.manifest
        trained_report = fit.verification or verify_candidate(fit.snap.expression, splits, tolerance=args.tolerance)
        payload["trained_eml_verification"] = trained_report.as_dict()
        stage_statuses["blind_baseline"] = trained_report.status

    compiled = None
    if args.compile_eml or args.warm_start_eml:
        source_expr = spec.candidate.to_sympy()
        validation_inputs = {
            spec.variable: np.concatenate([split.inputs[spec.variable] for split in splits]),
        }
        compiler_config = CompilerConfig(
            variables=(spec.variable,),
            constant_policy=args.constant_policy,
            max_depth=args.max_compile_depth,
            max_nodes=args.max_compile_nodes,
            max_power=args.max_power,
            validation_tolerance=args.tolerance,
        )
        try:
            compiled = compile_and_validate(source_expr, compiler_config, validation_inputs)
            compiled_verification = verify_candidate(compiled.expression, splits, tolerance=args.tolerance)
            payload["compiled_eml"] = compiled.as_dict()
            payload["compiled_eml_verification"] = compiled_verification.as_dict()
            stage_statuses["compiled_seed"] = compiled_verification.status
        except UnsupportedExpression as exc:
            payload["compiled_eml"] = {
                "status": "unsupported",
                **exc.as_dict(),
                "diagnostic": diagnose_compile_expression(source_expr, compiler_config, validation_inputs),
            }
            stage_statuses["compiled_seed"] = "unsupported"

    if args.warm_start_eml:
        if compiled is None:
            payload["warm_start_eml"] = {
                "status": "unsupported",
                "reason": "compile_failed",
                "detail": "warm-start requires a validated compiled EML seed",
            }
            stage_statuses["warm_start_attempt"] = "unsupported"
        elif compiled.metadata.depth > args.max_warm_depth:
            payload["warm_start_eml"] = {
                "status": "unsupported",
                "reason": "depth_too_large_for_warm_start",
                "compiled_depth": compiled.metadata.depth,
                "max_warm_depth": args.max_warm_depth,
            }
            stage_statuses["warm_start_attempt"] = "unsupported"
        else:
            train = splits[0]
            warm_depth = args.warm_depth or compiled.metadata.depth
            config = TrainingConfig(
                depth=warm_depth,
                variables=(spec.variable,),
                steps=args.warm_steps,
                restarts=args.warm_restarts,
                seed=args.seed,
                lr=args.lr,
                hardening_steps=args.hardening_steps,
                hardening_temperature_end=args.hardening_temperature_end,
                hardening_emit_interval=args.hardening_emit_interval,
                semantics_mode=args.semantics_mode,
            )
            warm = fit_warm_started_eml_tree(
                train.inputs,
                train.target,
                config,
                compiled.expression,
                perturbation_config=PerturbationConfig(seed=args.seed, noise_scale=args.warm_noise),
                verification_splits=splits,
                tolerance=args.tolerance,
                compiler_metadata=compiled.metadata.as_dict(),
            )
            payload["warm_start_eml"] = warm.manifest
            stage_statuses["warm_start_attempt"] = warm.status
            if warm.verification is not None:
                stage_statuses["trained_exact_recovery"] = warm.verification.status
                if warm.verification.status == "recovered":
                    payload["claim_status"] = "recovered"

    _write_json(Path(args.output), payload)
    statuses = ", ".join(f"{name}={status}" for name, status in stage_statuses.items())
    print(f"{spec.name}: {payload['claim_status']} ({statuses}) -> {args.output}")
    return 0


def verify_paper(args: argparse.Namespace) -> int:
    for name in ("exp", "log"):
        spec = get_demo(name)
        splits = spec.make_splits(points=args.points, seed=args.seed)
        report = verify_candidate(spec.candidate, splits, tolerance=args.tolerance)
        print(f"{name}: {report.status} max_hp={report.high_precision_max_error:.3e}")
        if report.status != "recovered":
            return 1
    return 0


def list_benchmarks(args: argparse.Namespace | None = None) -> int:
    for name in list_builtin_suites():
        suite = load_suite(name)
        print(f"{name}: {suite.description}")
    return 0


def list_claims_command(args: argparse.Namespace | None = None) -> int:
    for claim in sorted(list_claims(), key=lambda item: item.id):
        suites = ",".join(claim.suite_ids)
        print(f"{claim.id}: {claim.claim_class} threshold={claim.threshold_policy_id} suites={suites}")
    return 0


def proof_dataset_command(args: argparse.Namespace) -> int:
    output = Path(args.output) if args.output else Path("artifacts") / "proof-datasets" / f"{args.formula}-manifest.json"
    manifest = proof_dataset_manifest(args.formula, points=args.points, seed=args.seed, tolerance=args.tolerance)
    _write_json(output, manifest)
    print(f"{args.formula}: dataset manifest -> {output}")
    return 0


def dataset_manifest_command(args: argparse.Namespace) -> int:
    output = Path(args.output) if args.output else Path("artifacts") / "datasets" / f"{args.dataset_id}-manifest.json"
    manifest = expanded_dataset_manifest(args.dataset_id, points=args.points, seed=args.seed, tolerance=args.tolerance)
    _write_json(output, manifest)
    print(f"{args.dataset_id}: dataset manifest -> {output}")
    return 0


def list_campaigns(args: argparse.Namespace | None = None) -> int:
    for name in list_campaign_presets():
        preset = campaign_preset(name)
        print(f"{name}: {preset.description} ({preset.budget_guardrail})")
    return 0


def run_benchmark(args: argparse.Namespace) -> int:
    suite = load_suite(args.suite)
    if args.semantics_mode:
        suite = suite_with_semantics_mode(suite, args.semantics_mode)
    if args.output_dir:
        suite = type(suite)(suite.id, suite.description, suite.cases, Path(args.output_dir), suite.schema)
    run_filter = RunFilter(
        formulas=tuple(args.formula or ()),
        start_modes=tuple(args.start_mode or ()),
        case_ids=tuple(args.case or ()),
        seeds=tuple(args.seed or ()),
        perturbation_noises=tuple(args.perturbation_noise or ()),
    )
    result = run_benchmark_suite(suite, run_filter=run_filter)
    summary_path = suite.artifact_root / suite.id / "suite-result.json"
    _write_json(summary_path, result.as_dict())
    aggregate_paths = write_aggregate_reports(result, suite.artifact_root / suite.id)
    counts = result.as_dict()["counts"]
    print(
        f"{suite.id}: {counts['total']} runs, {counts['unsupported']} unsupported, "
        f"{counts['failed']} failed -> {summary_path}; aggregate -> {aggregate_paths['markdown']}"
    )
    return 0


def run_campaign_command(args: argparse.Namespace) -> int:
    run_filter = RunFilter(
        formulas=tuple(args.formula or ()),
        start_modes=tuple(args.start_mode or ()),
        case_ids=tuple(args.case or ()),
        seeds=tuple(args.seed or ()),
        perturbation_noises=tuple(args.perturbation_noise or ()),
    )
    result = run_campaign(
        args.preset,
        output_root=Path(args.output_root),
        label=args.label,
        overwrite=args.overwrite,
        run_filter=run_filter,
    )
    print(
        f"{args.preset}: campaign -> {result.campaign_dir}; "
        f"manifest -> {result.manifest_path}; report -> {result.report_path}"
    )
    return 0


def run_proof_campaign_command(args: argparse.Namespace) -> int:
    run_filter = RunFilter(
        formulas=tuple(args.formula or ()),
        start_modes=tuple(args.start_mode or ()),
        case_ids=tuple(args.case or ()),
        seeds=tuple(args.seed or ()),
        perturbation_noises=tuple(args.perturbation_noise or ()),
    )
    has_filter = any(
        (
            run_filter.formulas,
            run_filter.start_modes,
            run_filter.case_ids,
            run_filter.seeds,
            run_filter.perturbation_noises,
        )
    )
    campaign_filters = {preset: run_filter for preset in PROOF_CAMPAIGN_PRESETS} if has_filter else None
    result = run_proof_campaign(
        output_root=Path(args.output_root),
        overwrite=args.overwrite,
        campaign_filters=campaign_filters,
        reproduction_command=_proof_campaign_reproduction_command(args),
    )
    print(
        f"proof campaign: root -> {result.output_root}; "
        f"manifest -> {result.manifest_path}; report -> {result.report_path}"
    )
    return 0


def _proof_campaign_reproduction_command(args: argparse.Namespace) -> str:
    parts = [
        "PYTHONPATH=src",
        "python",
        "-m",
        "eml_symbolic_regression.cli",
        "proof-campaign",
        "--output-root",
        str(args.output_root),
    ]
    if args.overwrite:
        parts.append("--overwrite")
    for key, flag in (
        ("formula", "--formula"),
        ("start_mode", "--start-mode"),
        ("case", "--case"),
        ("seed", "--seed"),
        ("perturbation_noise", "--perturbation-noise"),
    ):
        for value in getattr(args, key, ()) or ():
            parts.extend([flag, str(value)])
    return shlex.join(parts)


def diagnostics_triage_command(args: argparse.Namespace) -> int:
    baselines = tuple(Path(path) for path in (args.baseline or DEFAULT_BASELINE_CAMPAIGNS))
    paths = write_baseline_triage(baselines, Path(args.output_dir))
    print(f"diagnostics triage: report -> {paths['markdown']}; lock -> {paths['lock_json']}")
    return 0


def diagnostics_family_triage_command(args: argparse.Namespace) -> int:
    paths = write_family_triage(
        smoke_aggregate=Path(args.smoke_aggregate),
        calibration_aggregate=Path(args.calibration_aggregate) if args.calibration_aggregate else None,
        output_dir=Path(args.output_dir),
    )
    print(f"family triage: report -> {paths.markdown_path}; gate -> {paths.go_no_go_path}")
    return 0


def diagnostics_family_evidence_command(args: argparse.Namespace) -> int:
    completed = [_campaign_manifest_entry(Path(path)) for path in args.completed_manifest]
    scoped = []
    for value in args.scoped:
        name, reason = value.split(":", 1) if ":" in value else (value, "deliberately scoped by v1.8 gate")
        scoped.append({"name": name, "scope_reason": reason})
    paths = write_family_evidence_manifest(
        completed_campaigns=completed,
        scoped_campaigns=scoped,
        output_dir=Path(args.output_dir),
    )
    print(f"family evidence manifest: markdown -> {paths.markdown_path}; json -> {paths.json_path}")
    return 0


def _campaign_manifest_entry(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    output = payload.get("output") if isinstance(payload.get("output"), dict) else {}
    table_paths = output.get("tables") if isinstance(output.get("tables"), dict) else {}
    return {
        "name": (payload.get("preset") or {}).get("name") if isinstance(payload.get("preset"), dict) else path.parent.name,
        "aggregate_json": output.get("aggregate_json"),
        "report_markdown": output.get("report_markdown"),
        "operator_family_locks_json": table_paths.get("operator_family_locks_json"),
        "reproduction_command": (payload.get("reproducibility") or {}).get("command")
        if isinstance(payload.get("reproducibility"), dict)
        else None,
    }


def diagnostics_rerun_command(args: argparse.Namespace) -> int:
    baselines = tuple(Path(path) for path in (args.baseline or DEFAULT_BASELINE_CAMPAIGNS))
    result = run_diagnostic_subset(
        args.target,
        baselines,
        preset_name=args.preset,
        output_root=Path(args.output_root),
        label=args.label,
        overwrite=args.overwrite,
    )
    print(
        f"diagnostics rerun {args.target}: campaign -> {result.campaign_dir}; "
        f"manifest -> {result.manifest_path}; report -> {result.report_path}"
    )
    return 0


def diagnostics_compare_command(args: argparse.Namespace) -> int:
    paths = write_campaign_comparison(
        tuple(Path(path) for path in args.baseline),
        tuple(Path(path) for path in args.candidate),
        Path(args.output_dir),
    )
    print(f"diagnostics compare: report -> {paths['markdown']}; json -> {paths['json']}")
    return 0


def diagnostics_basin_bound_command(args: argparse.Namespace) -> int:
    paths = write_perturbed_basin_bound_report(
        Path(args.bounded_aggregate),
        Path(args.probe_aggregate) if args.probe_aggregate else None,
        Path(args.output_dir),
    )
    print(f"diagnostics basin-bound: json -> {paths['json']}; markdown -> {paths['markdown']}")
    return 0


def diagnostics_paper_ablations_command(args: argparse.Namespace) -> int:
    paths = write_paper_diagnostics(output_dir=Path(args.output_dir))
    print(
        f"paper diagnostics: manifest -> {paths.manifest_json}; "
        f"motifs -> {paths.motif_depth_deltas_json}; "
        f"baselines -> {paths.baseline_diagnostics_json}"
    )
    return 0


def paper_assets_command(args: argparse.Namespace) -> int:
    paths = write_paper_assets(output_dir=Path(args.output_dir))
    print(
        f"paper assets: manifest -> {paths.manifest_json}; "
        f"figures -> {paths.output_dir / 'figures'}; "
        f"tables -> {paths.output_dir / 'tables'}"
    )
    return 0


def paper_package_command(args: argparse.Namespace) -> int:
    paths = write_v111_paper_package(output_dir=Path(args.output_dir), overwrite=args.overwrite)
    audit = json.loads(paths.claim_audit_json.read_text(encoding="utf-8"))
    print(
        f"paper package: manifest -> {paths.manifest_json}; "
        f"source locks -> {paths.source_locks_json}; "
        f"audit -> {paths.claim_audit_json} ({audit['status']})"
    )
    return 0 if audit["status"] == "passed" else 1


def paper_draft_command(args: argparse.Namespace) -> int:
    paths = write_v112_draft(output_dir=Path(args.output_dir))
    print(
        f"paper draft: manifest -> {paths.manifest_json}; "
        f"sections -> {paths.output_dir}; "
        f"taxonomy -> {paths.claim_taxonomy_json}"
    )
    return 0


def paper_refresh_command(args: argparse.Namespace) -> int:
    paths = write_v112_evidence_refresh(output_dir=Path(args.output_dir), overwrite=args.overwrite)
    manifest = json.loads(paths.manifest_json.read_text(encoding="utf-8"))
    counts = manifest["counts"]
    print(
        f"paper refresh: manifest -> {paths.manifest_json}; "
        f"shallow runs -> {counts['shallow_runs']}; "
        f"depth runs -> {counts['depth_runs']}"
    )
    return 0


def paper_figures_command(args: argparse.Namespace) -> int:
    paths = write_v112_paper_facing_assets(output_dir=Path(args.output_dir))
    print(
        f"paper figures: manifest -> {paths.manifest_json}; "
        f"pipeline -> {paths.pipeline_svg}; "
        f"captions -> {paths.figure_captions_md}"
    )
    return 0


def paper_probes_command(args: argparse.Namespace) -> int:
    paths = write_v112_bounded_probes(output_dir=Path(args.output_dir))
    manifest = json.loads(paths.manifest_json.read_text(encoding="utf-8"))
    statuses = manifest["statuses"]
    print(
        f"paper probes: manifest -> {paths.manifest_json}; "
        f"baseline -> {statuses['baseline']}; "
        f"logistic promotion -> {statuses['logistic_promotion']}"
    )
    return 0


def paper_supplement_command(args: argparse.Namespace) -> int:
    paths = write_v112_supplement(output_dir=Path(args.output_dir), overwrite=args.overwrite)
    manifest = json.loads(paths.manifest_json.read_text(encoding="utf-8"))
    print(
        f"paper supplement: manifest -> {paths.manifest_json}; "
        f"audit -> {manifest['audit_status']}; "
        f"source locks -> {manifest['source_lock_count']}"
    )
    return 0


def paper_training_detail_command(args: argparse.Namespace) -> int:
    paths = write_v112_training_detail_assets(output_dir=Path(args.output_dir), refresh_dir=Path(args.refresh_dir))
    manifest = json.loads(paths.manifest_json.read_text(encoding="utf-8"))
    counts = manifest["counts"]
    print(
        f"paper training detail: manifest -> {paths.manifest_json}; "
        f"step rows -> {counts['step_trace_rows']}; "
        f"candidate rows -> {counts['candidate_lifecycle_rows']}"
    )
    return 0


def publication_rebuild_command(args: argparse.Namespace) -> int:
    paths = write_publication_rebuild(
        output_dir=Path(args.output_dir),
        smoke=args.smoke,
        overwrite=args.overwrite,
        allow_dirty=args.allow_dirty,
        command=_publication_rebuild_command_string(args),
    )
    validation = json.loads(paths.validation_json.read_text(encoding="utf-8"))
    print(
        f"publication rebuild: manifest -> {paths.manifest_json}; "
        f"validation -> {paths.validation_json} ({validation['status']})"
    )
    return 0 if validation["status"] == "passed" else 1


def _publication_rebuild_command_string(args: argparse.Namespace) -> str:
    parts = [
        "PYTHONPATH=src",
        "python",
        "-m",
        "eml_symbolic_regression.cli",
        "publication-rebuild",
        "--output-dir",
        str(args.output_dir),
    ]
    if args.smoke:
        parts.append("--smoke")
    if args.overwrite:
        parts.append("--overwrite")
    if args.allow_dirty:
        parts.append("--allow-dirty")
    return shlex.join(parts)


def paper_decision_command(args: argparse.Namespace) -> int:
    paths = write_paper_decision_package(
        tuple(Path(path) for path in args.aggregate or ()),
        output_dir=Path(args.output_dir),
    )
    print(f"paper decision: memo -> {paths.decision_markdown}; json -> {paths.decision_json}")
    return 0


def raw_hybrid_paper_command(args: argparse.Namespace) -> int:
    paths = write_raw_hybrid_paper_package(
        output_dir=Path(args.output_dir),
        preset=args.preset,
        require_existing=args.require_existing,
        overwrite=args.overwrite,
        reproduction_command=_raw_hybrid_paper_reproduction_command(args),
    )
    print(
        f"raw hybrid paper: manifest -> {paths.manifest_json}; "
        f"report -> {paths.raw_hybrid_report_md}; "
        f"scientific laws -> {paths.scientific_law_table_json}; "
        f"claim boundaries -> {paths.claim_boundaries_md}; "
        f"source locks -> {paths.source_locks_json}"
    )
    return 0


def _raw_hybrid_paper_reproduction_command(args: argparse.Namespace) -> str:
    parts = [
        "PYTHONPATH=src",
        "python",
        "-m",
        "eml_symbolic_regression.cli",
        "raw-hybrid-paper",
        "--output-dir",
        str(args.output_dir),
    ]
    if args.preset != "v1.9-raw-hybrid-paper":
        parts[5:5] = ["--preset", str(args.preset)]
    if args.require_existing:
        parts.append("--require-existing")
    else:
        parts.append("--allow-missing")
    if args.overwrite:
        parts.append("--overwrite")
    return shlex.join(parts)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="eml-sr")
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list-demos", help="List built-in demo targets.")
    list_parser.set_defaults(func=list_demos)

    list_dataset_parser = sub.add_parser("list-datasets", help="List expanded dataset families.")
    list_dataset_parser.set_defaults(func=list_datasets)

    demo = sub.add_parser("demo", help="Run a demo verification/report pipeline.")
    demo.add_argument("name", help="Demo name. Use list-demos to inspect options.")
    demo.add_argument("--output", default="artifacts/demo-report.json")
    demo.add_argument("--points", type=int, default=80)
    demo.add_argument("--seed", type=int, default=0)
    demo.add_argument("--tolerance", type=float, default=1e-8)
    demo.add_argument("--train-eml", action="store_true", help="Also try soft EML training on the train split.")
    demo.add_argument("--depth", type=int, default=2)
    demo.add_argument("--steps", type=int, default=80)
    demo.add_argument("--restarts", type=int, default=2)
    demo.add_argument("--lr", type=float, default=0.05)
    demo.add_argument("--hardening-steps", type=int, default=4)
    demo.add_argument("--hardening-temperature-end", type=float, default=0.02)
    demo.add_argument("--hardening-emit-interval", type=int, default=2)
    demo.add_argument(
        "--semantics-mode",
        choices=("guarded", "faithful"),
        default="guarded",
        help="Training semantics for soft EML optimization.",
    )
    demo.add_argument("--compile-eml", action="store_true", help="Compile the demo source expression into an exact EML AST.")
    demo.add_argument(
        "--warm-start-eml",
        action="store_true",
        help="Compile, embed, perturb, train, snap, and verify a compiler warm start.",
    )
    demo.add_argument("--constant-policy", choices=("basis_only", "literal_constants"), default="literal_constants")
    demo.add_argument("--max-compile-depth", type=int, default=13)
    demo.add_argument("--max-compile-nodes", type=int, default=256)
    demo.add_argument("--max-power", type=int, default=3)
    demo.add_argument("--max-warm-depth", type=int, default=14)
    demo.add_argument("--warm-depth", type=int, default=0, help="Warm-start tree depth; 0 means compiled depth.")
    demo.add_argument("--warm-steps", type=int, default=1)
    demo.add_argument("--warm-restarts", type=int, default=1)
    demo.add_argument("--warm-noise", type=float, default=0.0)
    demo.set_defaults(func=run_demo)

    paper = sub.add_parser("verify-paper", help="Verify paper-grounded exp/log EML identities.")
    paper.add_argument("--points", type=int, default=80)
    paper.add_argument("--seed", type=int, default=0)
    paper.add_argument("--tolerance", type=float, default=1e-8)
    paper.set_defaults(func=verify_paper)

    list_bench = sub.add_parser("list-benchmarks", help="List built-in benchmark suites.")
    list_bench.set_defaults(func=list_benchmarks)

    claims = sub.add_parser("list-claims", help="List paper claim IDs and proof threshold policies.")
    claims.set_defaults(func=list_claims_command)

    proof_dataset = sub.add_parser("proof-dataset", help="Write a deterministic proof dataset manifest.")
    proof_dataset.add_argument("formula", help="Formula ID. Use list-demos to inspect options.")
    proof_dataset.add_argument("--output", help="Output manifest path. Defaults to artifacts/proof-datasets/<formula>-manifest.json.")
    proof_dataset.add_argument("--points", type=int, default=80)
    proof_dataset.add_argument("--seed", type=int, default=0)
    proof_dataset.add_argument("--tolerance", type=float, default=1e-8)
    proof_dataset.set_defaults(func=proof_dataset_command)

    dataset_manifest = sub.add_parser("dataset-manifest", help="Write an expanded dataset manifest.")
    dataset_manifest.add_argument("dataset_id", help="Dataset ID. Use list-datasets to inspect options.")
    dataset_manifest.add_argument("--output", help="Output manifest path. Defaults to artifacts/datasets/<dataset-id>-manifest.json.")
    dataset_manifest.add_argument("--points", type=int, default=80)
    dataset_manifest.add_argument("--seed", type=int, default=0)
    dataset_manifest.add_argument("--tolerance", type=float, default=1e-8)
    dataset_manifest.set_defaults(func=dataset_manifest_command)

    bench = sub.add_parser("benchmark", help="Run a benchmark suite or filtered subset.")
    bench.add_argument("suite", help="Built-in suite name or path to a suite JSON file.")
    bench.add_argument("--output-dir", help="Override artifact root; suite outputs are written under <root>/<suite-id>.")
    bench.add_argument("--formula", action="append", help="Only run this formula ID. Repeatable.")
    bench.add_argument("--start-mode", choices=START_MODES, action="append")
    bench.add_argument("--case", action="append", help="Only run this benchmark case ID. Repeatable.")
    bench.add_argument("--seed", type=int, action="append", help="Only run this seed. Repeatable.")
    bench.add_argument("--perturbation-noise", type=float, action="append", help="Only run this perturbation noise. Repeatable.")
    bench.add_argument(
        "--semantics-mode",
        choices=("guarded", "faithful"),
        help="Override optimizer semantics mode for every case in the suite.",
    )
    bench.set_defaults(func=run_benchmark)

    list_campaign = sub.add_parser("list-campaigns", help="List named benchmark campaign presets.")
    list_campaign.set_defaults(func=list_campaigns)

    campaign = sub.add_parser("campaign", help="Run a named benchmark campaign preset.")
    campaign.add_argument("preset", choices=list_campaign_presets(), help="Named campaign preset.")
    campaign.add_argument("--output-root", default=str(DEFAULT_CAMPAIGN_ROOT), help="Directory that receives campaign folders.")
    campaign.add_argument("--label", help="Stable campaign folder name. Defaults to <preset>-<UTC timestamp>.")
    campaign.add_argument("--overwrite", action="store_true", help="Allow writing into an existing campaign folder.")
    campaign.add_argument("--formula", action="append", help="Only run this formula ID. Repeatable.")
    campaign.add_argument("--start-mode", choices=START_MODES, action="append")
    campaign.add_argument("--case", action="append", help="Only run this benchmark case ID. Repeatable.")
    campaign.add_argument("--seed", type=int, action="append", help="Only run this seed. Repeatable.")
    campaign.add_argument("--perturbation-noise", type=float, action="append", help="Only run this perturbation noise. Repeatable.")
    campaign.set_defaults(func=run_campaign_command)

    proof_campaign = sub.add_parser("proof-campaign", help="Run the current proof bundle and write a claim report.")
    proof_campaign.add_argument("--output-root", default=str(DEFAULT_PROOF_OUTPUT_ROOT), help="Directory that receives proof bundle outputs.")
    proof_campaign.add_argument("--overwrite", action="store_true", help="Allow writing into an existing proof bundle root.")
    proof_campaign.add_argument("--formula", action="append", help="Only run this formula ID across every proof preset. Repeatable.")
    proof_campaign.add_argument("--start-mode", choices=START_MODES, action="append")
    proof_campaign.add_argument("--case", action="append", help="Only run this benchmark case ID across every proof preset. Repeatable.")
    proof_campaign.add_argument("--seed", type=int, action="append", help="Only run this seed across every proof preset. Repeatable.")
    proof_campaign.add_argument(
        "--perturbation-noise",
        type=float,
        action="append",
        help="Only run this perturbation noise across every proof preset. Repeatable.",
    )
    proof_campaign.set_defaults(func=run_proof_campaign_command)

    paper_decision = sub.add_parser("paper-decision", help="Write the paper decision memo package.")
    paper_decision.add_argument("--aggregate", action="append", help="Benchmark aggregate JSON to summarize. Repeatable.")
    paper_decision.add_argument("--output-dir", default=str(DEFAULT_PAPER_OUTPUT_ROOT), help="Directory for decision memo outputs.")
    paper_decision.set_defaults(func=paper_decision_command)

    raw_hybrid_paper = sub.add_parser("raw-hybrid-paper", help="Write a raw-hybrid paper package from locked sources.")
    raw_hybrid_paper.add_argument(
        "--preset",
        choices=raw_hybrid_paper_presets(),
        default="v1.9-raw-hybrid-paper",
        help="Paper package preset to generate.",
    )
    raw_hybrid_paper.add_argument(
        "--output-dir",
        default=str(DEFAULT_RAW_HYBRID_OUTPUT_DIR),
        help="Directory for raw-hybrid paper package outputs.",
    )
    source_group = raw_hybrid_paper.add_mutually_exclusive_group()
    source_group.add_argument(
        "--require-existing",
        dest="require_existing",
        action="store_true",
        default=True,
        help="Fail if any required source artifact is missing. This is the default.",
    )
    source_group.add_argument(
        "--allow-missing",
        dest="require_existing",
        action="store_false",
        help="Allow missing source artifacts for fixture/debug package generation.",
    )
    raw_hybrid_paper.add_argument("--overwrite", action="store_true", help="Allow replacing an existing non-empty package directory.")
    raw_hybrid_paper.set_defaults(func=raw_hybrid_paper_command)

    paper_assets = sub.add_parser("paper-assets", help="Write deterministic v1.11 paper figure and source-table assets.")
    paper_assets.add_argument(
        "--output-dir",
        default=str(DEFAULT_PAPER_ASSETS_OUTPUT_DIR),
        help="Directory for paper asset manifest, tables, figures, and metadata.",
    )
    paper_assets.set_defaults(func=paper_assets_command)

    paper_package = sub.add_parser("paper-package", help="Assemble and audit the final v1.11 paper evidence package.")
    paper_package.add_argument(
        "--output-dir",
        default=str(DEFAULT_V111_PAPER_PACKAGE_DIR),
        help="Directory for final v1.11 manifest, source locks, claim audit, tables, and figures.",
    )
    paper_package.add_argument("--overwrite", action="store_true", help="Allow refreshing an existing package manifest.")
    paper_package.set_defaults(func=paper_package_command)

    paper_draft = sub.add_parser("paper-draft", help="Write the v1.12 paper draft skeleton and claim taxonomy.")
    paper_draft.add_argument(
        "--output-dir",
        default=str(DEFAULT_V112_DRAFT_DIR),
        help="Directory for v1.12 draft skeleton artifacts.",
    )
    paper_draft.set_defaults(func=paper_draft_command)

    paper_refresh = sub.add_parser("paper-refresh", help="Run the v1.12 shallow seed and depth-curve evidence refresh.")
    paper_refresh.add_argument(
        "--output-dir",
        default=str(DEFAULT_V112_REFRESH_DIR),
        help="Directory for v1.12 evidence-refresh artifacts.",
    )
    paper_refresh.add_argument("--overwrite", action="store_true", help="Allow refreshing an existing output directory.")
    paper_refresh.set_defaults(func=paper_refresh_command)

    paper_figures = sub.add_parser("paper-figures", help="Write v1.12 paper-facing captions, motif table, negative table, and pipeline figure.")
    paper_figures.add_argument(
        "--output-dir",
        default=str(DEFAULT_V112_DRAFT_DIR),
        help="Directory for v1.12 draft and paper-facing artifacts.",
    )
    paper_figures.set_defaults(func=paper_figures_command)

    paper_probes = sub.add_parser("paper-probes", help="Write v1.12 bounded baseline and logistic strict-support probe artifacts.")
    paper_probes.add_argument(
        "--output-dir",
        default=str(DEFAULT_V112_DRAFT_DIR),
        help="Directory for v1.12 draft and bounded-probe artifacts.",
    )
    paper_probes.set_defaults(func=paper_probes_command)

    paper_supplement = sub.add_parser("paper-supplement", help="Assemble and audit the v1.12 supplement to the v1.11 paper package.")
    paper_supplement.add_argument(
        "--output-dir",
        default=str(DEFAULT_V112_SUPPLEMENT_DIR),
        help="Directory for v1.12 supplement manifest, source locks, audit, and reproduction commands.",
    )
    paper_supplement.add_argument("--overwrite", action="store_true", help="Allow refreshing an existing supplement directory.")
    paper_supplement.set_defaults(func=paper_supplement_command)

    paper_training_detail = sub.add_parser("paper-training-detail", help="Write v1.12 per-step training traces, lifecycle tables, and loss-curve figures.")
    paper_training_detail.add_argument(
        "--output-dir",
        default=str(DEFAULT_V112_TRAINING_DETAIL_DIR),
        help="Directory for v1.12 training-detail paper artifacts.",
    )
    paper_training_detail.add_argument(
        "--refresh-dir",
        default=str(DEFAULT_V112_REFRESH_DIR),
        help="v1.12 evidence-refresh directory containing traced run artifacts.",
    )
    paper_training_detail.set_defaults(func=paper_training_detail_command)

    publication_rebuild = sub.add_parser(
        "publication-rebuild",
        help="Rebuild the v1.13 publication package and validate provenance.",
    )
    publication_rebuild.add_argument(
        "--output-dir",
        default=str(DEFAULT_V113_PUBLICATION_DIR),
        help="Directory for v1.13 publication manifest, source locks, reproduction docs, and validation.",
    )
    publication_rebuild.add_argument("--smoke", action="store_true", help="Run the fast smoke rebuild contract.")
    publication_rebuild.add_argument("--overwrite", action="store_true", help="Allow refreshing an existing publication package.")
    publication_rebuild.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Record dirty git state instead of failing before publication validation.",
    )
    publication_rebuild.set_defaults(func=publication_rebuild_command)

    diagnostics = sub.add_parser("diagnostics", help="Inspect baseline evidence, rerun focused subsets, and compare campaign outputs.")
    diagnostics_sub = diagnostics.add_subparsers(dest="diagnostics_command", required=True)

    triage = diagnostics_sub.add_parser("triage", help="Write baseline failure triage reports.")
    triage.add_argument("--baseline", action="append", help="Campaign folder to include. Repeatable.")
    triage.add_argument("--output-dir", default="artifacts/diagnostics/v1.4-baseline", help="Directory for triage outputs.")
    triage.set_defaults(func=diagnostics_triage_command)

    family_triage = diagnostics_sub.add_parser("family-triage", help="Write v1.8 centered-family triage and go/no-go artifacts.")
    family_triage.add_argument("--smoke-aggregate", required=True, help="Aggregate JSON from the family-smoke campaign.")
    family_triage.add_argument("--calibration-aggregate", help="Optional aggregate JSON from the family-calibration campaign.")
    family_triage.add_argument("--output-dir", default=str(DEFAULT_TRIAGE_OUTPUT_DIR), help="Directory for family triage outputs.")
    family_triage.set_defaults(func=diagnostics_family_triage_command)

    family_evidence = diagnostics_sub.add_parser("family-evidence", help="Write v1.8 family evidence manifest.")
    family_evidence.add_argument(
        "--completed-manifest",
        action="append",
        default=[],
        help="Campaign manifest JSON for a completed campaign. Repeatable.",
    )
    family_evidence.add_argument(
        "--scoped",
        action="append",
        default=[],
        help="Scoped campaign in NAME:reason form. Repeatable.",
    )
    family_evidence.add_argument("--output-dir", default=str(DEFAULT_EVIDENCE_OUTPUT_DIR), help="Directory for evidence manifest outputs.")
    family_evidence.set_defaults(func=diagnostics_family_evidence_command)

    rerun = diagnostics_sub.add_parser("rerun", help="Run a focused diagnostic subset selected from baselines.")
    rerun.add_argument(
        "target",
        choices=("blind-failures", "beer-perturbation-failures", "compiler-depth-gates"),
        help="Diagnostic target class.",
    )
    rerun.add_argument("--baseline", action="append", help="Campaign folder to inspect. Repeatable.")
    rerun.add_argument("--preset", choices=list_campaign_presets(), default="standard", help="Campaign preset to rerun with filters.")
    rerun.add_argument("--output-root", default=str(DEFAULT_CAMPAIGN_ROOT), help="Directory that receives campaign folders.")
    rerun.add_argument("--label", help="Stable campaign folder name.")
    rerun.add_argument("--overwrite", action="store_true", help="Allow writing into an existing diagnostic campaign folder.")
    rerun.set_defaults(func=diagnostics_rerun_command)

    compare = diagnostics_sub.add_parser("compare", help="Compare candidate campaign folders against baselines.")
    compare.add_argument("--baseline", action="append", required=True, help="Baseline campaign folder. Repeat with matching --candidate.")
    compare.add_argument("--candidate", action="append", required=True, help="Candidate campaign folder. Repeat with matching --baseline.")
    compare.add_argument("--output-dir", default="artifacts/campaigns/comparison", help="Directory for comparison outputs.")
    compare.set_defaults(func=diagnostics_compare_command)

    basin_bound = diagnostics_sub.add_parser("basin-bound", help="Write Beer-Lambert perturbed-basin bound evidence reports.")
    basin_bound.add_argument("--bounded-aggregate", required=True, help="Aggregate JSON from the bounded proof-perturbed-basin suite.")
    basin_bound.add_argument("--probe-aggregate", help="Optional aggregate JSON from the proof-perturbed-basin-beer-probes suite.")
    basin_bound.add_argument(
        "--output-dir",
        default="artifacts/diagnostics/phase31-basin-bound",
        help="Directory for basin-bound.json and basin-bound.md.",
    )
    basin_bound.set_defaults(func=diagnostics_basin_bound_command)

    paper_ablations = diagnostics_sub.add_parser(
        "paper-ablations",
        help="Write v1.11 paper ablation and baseline diagnostics from locked artifacts.",
    )
    paper_ablations.add_argument(
        "--output-dir",
        default=str(DEFAULT_PAPER_DIAGNOSTICS_OUTPUT_DIR),
        help="Directory for paper ablation/baseline diagnostic outputs.",
    )
    paper_ablations.set_defaults(func=diagnostics_paper_ablations_command)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
