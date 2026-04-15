"""Command line interface for EML symbolic regression demos."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .cleanup import cleanup_candidate
from .datasets import demo_specs, get_demo
from .optimize import TrainingConfig, fit_eml_tree
from .verify import verify_candidate


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
    report = verify_candidate(
        spec.candidate,
        splits,
        tolerance=args.tolerance,
        recovered_requires_exact_eml=True,
    )
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

    _write_json(Path(args.output), payload)
    print(f"{spec.name}: {report.status} ({report.reason}) -> {args.output}")
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
