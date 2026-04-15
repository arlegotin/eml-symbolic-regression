"""Command line interface for EML symbolic regression demos."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from .cleanup import cleanup_candidate
from .compiler import CompilerConfig, UnsupportedExpression, compile_and_validate
from .datasets import demo_specs, get_demo
from .optimize import TrainingConfig, fit_eml_tree
from .verify import verify_candidate
from .warm_start import PerturbationConfig, fit_warm_started_eml_tree


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def list_demos(args: argparse.Namespace | None = None) -> int:
    for name, spec in sorted(demo_specs().items()):
        print(f"{name}: {spec.description}")
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

    if args.train_eml:
        train = splits[0]
        config = TrainingConfig(
            depth=args.depth,
            variables=(spec.variable,),
            steps=args.steps,
            restarts=args.restarts,
            seed=args.seed,
        )
        fit = fit_eml_tree(train.inputs, train.target, config)
        payload["trained_eml_candidate"] = fit.manifest
        trained_report = verify_candidate(fit.snap.expression, splits, tolerance=args.tolerance)
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
            payload["compiled_eml"] = {"status": "unsupported", **exc.as_dict()}
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="eml-sr")
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list-demos", help="List built-in demo targets.")
    list_parser.set_defaults(func=list_demos)

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
    demo.add_argument("--compile-eml", action="store_true", help="Compile the demo source expression into an exact EML AST.")
    demo.add_argument(
        "--warm-start-eml",
        action="store_true",
        help="Compile, embed, perturb, train, snap, and verify a compiler warm start.",
    )
    demo.add_argument("--constant-policy", choices=("basis_only", "literal_constants"), default="literal_constants")
    demo.add_argument("--max-compile-depth", type=int, default=12)
    demo.add_argument("--max-compile-nodes", type=int, default=256)
    demo.add_argument("--max-power", type=int, default=3)
    demo.add_argument("--max-warm-depth", type=int, default=10)
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
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
