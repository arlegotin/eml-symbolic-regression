"""Benchmark suite contracts for repeatable EML training evidence."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

import numpy as np

from .compiler import CompilerConfig, UnsupportedExpression, compile_and_validate
from .datasets import demo_specs
from .optimize import TrainingConfig, fit_eml_tree
from .verify import verify_candidate
from .warm_start import PerturbationConfig, fit_warm_started_eml_tree


START_MODES = ("catalog", "compile", "blind", "warm_start")
BUILTIN_SUITES = ("smoke", "v1.2-evidence", "for-demo-diagnostics")
DEFAULT_ARTIFACT_ROOT = Path("artifacts") / "benchmarks"


class BenchmarkValidationError(ValueError):
    """Raised when a benchmark suite cannot be safely expanded."""

    def __init__(self, reason: str, detail: str, *, path: str | None = None) -> None:
        self.reason = reason
        self.detail = detail
        self.path = path
        location = f" at {path}" if path else ""
        super().__init__(f"{reason}{location}: {detail}")

    def as_dict(self) -> dict[str, str]:
        payload = {"reason": self.reason, "detail": self.detail}
        if self.path is not None:
            payload["path"] = self.path
        return payload


@dataclass(frozen=True)
class DatasetConfig:
    points: int = 32
    tolerance: float = 1e-8

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any] | None) -> "DatasetConfig":
        payload = payload or {}
        return cls(points=int(payload.get("points", cls.points)), tolerance=float(payload.get("tolerance", cls.tolerance)))

    def validate(self, path: str) -> None:
        if self.points <= 0:
            raise BenchmarkValidationError("invalid_dataset", "points must be positive", path=f"{path}.points")
        if self.tolerance <= 0:
            raise BenchmarkValidationError("invalid_dataset", "tolerance must be positive", path=f"{path}.tolerance")

    def as_dict(self) -> dict[str, Any]:
        return {"points": self.points, "tolerance": self.tolerance}


@dataclass(frozen=True)
class OptimizerBudget:
    depth: int = 2
    steps: int = 20
    restarts: int = 1
    lr: float = 0.05
    warm_depth: int = 0
    warm_steps: int = 20
    warm_restarts: int = 1
    max_compile_depth: int = 12
    max_compile_nodes: int = 256
    max_warm_depth: int = 10
    max_power: int = 3

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any] | None) -> "OptimizerBudget":
        payload = payload or {}
        values = {field_name: payload.get(field_name, getattr(cls, field_name)) for field_name in cls.__dataclass_fields__}
        values["depth"] = int(values["depth"])
        values["steps"] = int(values["steps"])
        values["restarts"] = int(values["restarts"])
        values["warm_depth"] = int(values["warm_depth"])
        values["warm_steps"] = int(values["warm_steps"])
        values["warm_restarts"] = int(values["warm_restarts"])
        values["max_compile_depth"] = int(values["max_compile_depth"])
        values["max_compile_nodes"] = int(values["max_compile_nodes"])
        values["max_warm_depth"] = int(values["max_warm_depth"])
        values["max_power"] = int(values["max_power"])
        values["lr"] = float(values["lr"])
        return cls(**values)

    def validate(self, path: str) -> None:
        positive = (
            "depth",
            "steps",
            "restarts",
            "warm_steps",
            "warm_restarts",
            "max_compile_depth",
            "max_compile_nodes",
            "max_warm_depth",
            "max_power",
        )
        for name in positive:
            if int(getattr(self, name)) <= 0:
                raise BenchmarkValidationError("invalid_budget", f"{name} must be positive", path=f"{path}.{name}")
        if self.warm_depth < 0:
            raise BenchmarkValidationError("invalid_budget", "warm_depth must be 0 or positive", path=f"{path}.warm_depth")
        if self.lr <= 0:
            raise BenchmarkValidationError("invalid_budget", "lr must be positive", path=f"{path}.lr")

    def as_dict(self) -> dict[str, Any]:
        return {
            "depth": self.depth,
            "steps": self.steps,
            "restarts": self.restarts,
            "lr": self.lr,
            "warm_depth": self.warm_depth,
            "warm_steps": self.warm_steps,
            "warm_restarts": self.warm_restarts,
            "max_compile_depth": self.max_compile_depth,
            "max_compile_nodes": self.max_compile_nodes,
            "max_warm_depth": self.max_warm_depth,
            "max_power": self.max_power,
        }


@dataclass(frozen=True)
class BenchmarkCase:
    id: str
    formula: str
    start_mode: str
    seeds: tuple[int, ...] = (0,)
    perturbation_noise: tuple[float, ...] = (0.0,)
    dataset: DatasetConfig = field(default_factory=DatasetConfig)
    optimizer: OptimizerBudget = field(default_factory=OptimizerBudget)
    tags: tuple[str, ...] = ()
    expect_recovery: bool = False

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any], *, path: str) -> "BenchmarkCase":
        required = ("id", "formula", "start_mode")
        for key in required:
            if key not in payload:
                raise BenchmarkValidationError("malformed_case", f"missing required field {key!r}", path=path)
        seeds = tuple(int(seed) for seed in payload.get("seeds", (0,)))
        noises = tuple(float(value) for value in payload.get("perturbation_noise", (0.0,)))
        return cls(
            id=str(payload["id"]),
            formula=str(payload["formula"]),
            start_mode=str(payload["start_mode"]),
            seeds=seeds,
            perturbation_noise=noises,
            dataset=DatasetConfig.from_mapping(payload.get("dataset")),
            optimizer=OptimizerBudget.from_mapping(payload.get("optimizer")),
            tags=tuple(str(tag) for tag in payload.get("tags", ())),
            expect_recovery=bool(payload.get("expect_recovery", False)),
        )

    def validate(self, path: str) -> None:
        if not self.id:
            raise BenchmarkValidationError("malformed_case", "case id must not be empty", path=f"{path}.id")
        if self.formula not in demo_specs():
            available = ", ".join(sorted(demo_specs()))
            raise BenchmarkValidationError("unknown_formula", f"{self.formula!r} is not one of: {available}", path=f"{path}.formula")
        if self.start_mode not in START_MODES:
            raise BenchmarkValidationError(
                "invalid_start_mode",
                f"{self.start_mode!r} is not one of: {', '.join(START_MODES)}",
                path=f"{path}.start_mode",
            )
        if not self.seeds:
            raise BenchmarkValidationError("invalid_seeds", "at least one seed is required", path=f"{path}.seeds")
        if any(seed < 0 for seed in self.seeds):
            raise BenchmarkValidationError("invalid_seeds", "seeds must be non-negative", path=f"{path}.seeds")
        if not self.perturbation_noise:
            raise BenchmarkValidationError(
                "invalid_perturbation", "at least one perturbation noise value is required", path=f"{path}.perturbation_noise"
            )
        if any(noise < 0 for noise in self.perturbation_noise):
            raise BenchmarkValidationError(
                "invalid_perturbation", "perturbation noise values must be non-negative", path=f"{path}.perturbation_noise"
            )
        if self.start_mode != "warm_start" and any(noise != 0.0 for noise in self.perturbation_noise):
            raise BenchmarkValidationError(
                "invalid_perturbation",
                "non-warm-start cases must use perturbation noise 0.0",
                path=f"{path}.perturbation_noise",
            )
        self.dataset.validate(f"{path}.dataset")
        self.optimizer.validate(f"{path}.optimizer")

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "formula": self.formula,
            "start_mode": self.start_mode,
            "seeds": list(self.seeds),
            "perturbation_noise": list(self.perturbation_noise),
            "dataset": self.dataset.as_dict(),
            "optimizer": self.optimizer.as_dict(),
            "tags": list(self.tags),
            "expect_recovery": self.expect_recovery,
        }


@dataclass(frozen=True)
class BenchmarkRun:
    suite_id: str
    case_id: str
    formula: str
    start_mode: str
    seed: int
    perturbation_noise: float
    dataset: DatasetConfig
    optimizer: OptimizerBudget
    artifact_path: Path
    tags: tuple[str, ...] = ()
    expect_recovery: bool = False

    @property
    def run_id(self) -> str:
        parts = {
            "suite": self.suite_id,
            "case": self.case_id,
            "formula": self.formula,
            "start_mode": self.start_mode,
            "seed": self.seed,
            "perturbation_noise": self.perturbation_noise,
            "dataset": self.dataset.as_dict(),
            "optimizer": self.optimizer.as_dict(),
        }
        digest = hashlib.sha1(json.dumps(parts, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()[:12]
        return f"{_slug(self.suite_id)}-{_slug(self.case_id)}-{digest}"

    def as_dict(self) -> dict[str, Any]:
        return {
            "suite_id": self.suite_id,
            "case_id": self.case_id,
            "run_id": self.run_id,
            "formula": self.formula,
            "start_mode": self.start_mode,
            "seed": self.seed,
            "perturbation_noise": self.perturbation_noise,
            "dataset": self.dataset.as_dict(),
            "optimizer": self.optimizer.as_dict(),
            "artifact_path": str(self.artifact_path),
            "tags": list(self.tags),
            "expect_recovery": self.expect_recovery,
        }


@dataclass(frozen=True)
class RunFilter:
    formulas: tuple[str, ...] = ()
    start_modes: tuple[str, ...] = ()
    case_ids: tuple[str, ...] = ()
    seeds: tuple[int, ...] = ()

    def includes(self, run: BenchmarkRun) -> bool:
        return (
            (not self.formulas or run.formula in self.formulas)
            and (not self.start_modes or run.start_mode in self.start_modes)
            and (not self.case_ids or run.case_id in self.case_ids)
            and (not self.seeds or run.seed in self.seeds)
        )


@dataclass(frozen=True)
class BenchmarkRunResult:
    run: BenchmarkRun
    status: str
    artifact_path: Path
    payload: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {
            "run": self.run.as_dict(),
            "status": self.status,
            "artifact_path": str(self.artifact_path),
            "payload": self.payload,
        }


@dataclass(frozen=True)
class BenchmarkSuiteResult:
    suite: BenchmarkSuite
    results: tuple[BenchmarkRunResult, ...]

    @property
    def completed(self) -> int:
        return sum(result.status not in {"execution_error"} for result in self.results)

    @property
    def failed(self) -> int:
        return sum(result.status in {"failed", "snapped_but_failed", "soft_fit_only", "execution_error"} for result in self.results)

    @property
    def unsupported(self) -> int:
        return sum(result.status == "unsupported" for result in self.results)

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": "eml.benchmark_suite_result.v1",
            "suite": self.suite.as_dict(),
            "counts": {
                "total": len(self.results),
                "completed": self.completed,
                "failed": self.failed,
                "unsupported": self.unsupported,
            },
            "results": [result.as_dict() for result in self.results],
        }


@dataclass(frozen=True)
class BenchmarkSuite:
    id: str
    description: str
    cases: tuple[BenchmarkCase, ...]
    artifact_root: Path = DEFAULT_ARTIFACT_ROOT
    schema: str = "eml.benchmark_suite.v1"

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "BenchmarkSuite":
        if payload.get("schema", "eml.benchmark_suite.v1") != "eml.benchmark_suite.v1":
            raise BenchmarkValidationError("unsupported_schema", f"unsupported schema {payload.get('schema')!r}", path="schema")
        if "id" not in payload:
            raise BenchmarkValidationError("malformed_suite", "missing required field 'id'", path="id")
        cases_payload = payload.get("cases")
        if not isinstance(cases_payload, list):
            raise BenchmarkValidationError("malformed_suite", "cases must be a list", path="cases")
        cases = tuple(BenchmarkCase.from_mapping(item, path=f"cases[{index}]") for index, item in enumerate(cases_payload))
        return cls(
            id=str(payload["id"]),
            description=str(payload.get("description", "")),
            cases=cases,
            artifact_root=Path(str(payload.get("artifact_root", DEFAULT_ARTIFACT_ROOT))),
        )

    def validate(self) -> None:
        if not self.id:
            raise BenchmarkValidationError("malformed_suite", "suite id must not be empty", path="id")
        if not self.cases:
            raise BenchmarkValidationError("malformed_suite", "suite must contain at least one case", path="cases")
        seen_ids: set[str] = set()
        for index, case in enumerate(self.cases):
            if case.id in seen_ids:
                raise BenchmarkValidationError("duplicate_case", f"duplicate case id {case.id!r}", path=f"cases[{index}].id")
            seen_ids.add(case.id)
            case.validate(f"cases[{index}]")

    def expanded_runs(self) -> tuple[BenchmarkRun, ...]:
        self.validate()
        runs: list[BenchmarkRun] = []
        for case in self.cases:
            noises = case.perturbation_noise if case.start_mode == "warm_start" else (0.0,)
            for seed in case.seeds:
                for noise in noises:
                    placeholder = BenchmarkRun(
                        suite_id=self.id,
                        case_id=case.id,
                        formula=case.formula,
                        start_mode=case.start_mode,
                        seed=seed,
                        perturbation_noise=noise,
                        dataset=case.dataset,
                        optimizer=case.optimizer,
                        artifact_path=Path(),
                        tags=case.tags,
                        expect_recovery=case.expect_recovery,
                    )
                    runs.append(
                        BenchmarkRun(
                            suite_id=placeholder.suite_id,
                            case_id=placeholder.case_id,
                            formula=placeholder.formula,
                            start_mode=placeholder.start_mode,
                            seed=placeholder.seed,
                            perturbation_noise=placeholder.perturbation_noise,
                            dataset=placeholder.dataset,
                            optimizer=placeholder.optimizer,
                            artifact_path=self.artifact_root / self.id / f"{placeholder.run_id}.json",
                            tags=placeholder.tags,
                            expect_recovery=placeholder.expect_recovery,
                        )
                    )
        return tuple(runs)

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "id": self.id,
            "description": self.description,
            "artifact_root": str(self.artifact_root),
            "cases": [case.as_dict() for case in self.cases],
        }


def _slug(value: str) -> str:
    slug = "".join(character.lower() if character.isalnum() else "-" for character in value)
    return "-".join(part for part in slug.split("-") if part)


def _case(
    id: str,
    formula: str,
    start_mode: str,
    *,
    seeds: Iterable[int] = (0,),
    perturbation_noise: Iterable[float] = (0.0,),
    points: int = 24,
    steps: int = 8,
    warm_steps: int = 8,
    restarts: int = 1,
    depth: int = 2,
    warm_restarts: int = 1,
    tags: Iterable[str] = (),
    expect_recovery: bool = False,
) -> BenchmarkCase:
    return BenchmarkCase(
        id=id,
        formula=formula,
        start_mode=start_mode,
        seeds=tuple(seeds),
        perturbation_noise=tuple(perturbation_noise),
        dataset=DatasetConfig(points=points),
        optimizer=OptimizerBudget(depth=depth, steps=steps, restarts=restarts, warm_steps=warm_steps, warm_restarts=warm_restarts),
        tags=tuple(tags),
        expect_recovery=expect_recovery,
    )


def builtin_suite(name: str) -> BenchmarkSuite:
    if name == "smoke":
        return BenchmarkSuite(
            id="smoke",
            description="Fast CI-scale benchmark contract smoke suite.",
            cases=(
                _case("exp-blind", "exp", "blind", depth=1, steps=6, expect_recovery=False, tags=("smoke", "blind")),
                _case("beer-warm", "beer_lambert", "warm_start", warm_steps=1, tags=("smoke", "warm_start"), expect_recovery=True),
                _case("planck-diagnostic", "planck", "compile", tags=("smoke", "stretch")),
            ),
        )
    if name == "v1.2-evidence":
        return BenchmarkSuite(
            id="v1.2-evidence",
            description="Default v1.2 evidence matrix for training recovery claims.",
            cases=(
                _case("exp-blind", "exp", "blind", seeds=(0, 1, 2), depth=1, steps=80, tags=("blind", "shallow")),
                _case("log-blind", "log", "blind", seeds=(0, 1, 2), depth=3, steps=80, tags=("blind", "shallow")),
                _case(
                    "radioactive-decay-blind",
                    "radioactive_decay",
                    "blind",
                    seeds=(0, 1, 2),
                    depth=4,
                    steps=80,
                    tags=("blind", "shallow", "for_demo"),
                ),
                _case(
                    "beer-perturbation-sweep",
                    "beer_lambert",
                    "warm_start",
                    seeds=(0, 1, 2),
                    perturbation_noise=(0.0, 5.0, 35.0),
                    warm_steps=60,
                    tags=("warm_start", "perturbation"),
                    expect_recovery=True,
                ),
                _case("michaelis-warm-diagnostic", "michaelis_menten", "warm_start", tags=("diagnostic", "depth_gate")),
                _case("planck-diagnostic", "planck", "compile", tags=("stretch", "depth_gate")),
            ),
        )
    if name == "for-demo-diagnostics":
        return BenchmarkSuite(
            id="for-demo-diagnostics",
            description="FOR_DEMO formula diagnostics without recovery guarantees.",
            cases=(
                _case("beer-warm", "beer_lambert", "warm_start", perturbation_noise=(0.0, 5.0), warm_steps=40, tags=("for_demo",)),
                _case("radioactive-decay-blind", "radioactive_decay", "blind", depth=4, steps=60, tags=("for_demo", "blind")),
                _case("michaelis-compile", "michaelis_menten", "compile", tags=("for_demo", "diagnostic")),
                _case("logistic-compile", "logistic", "compile", tags=("for_demo", "diagnostic")),
                _case("shockley-compile", "shockley", "compile", tags=("for_demo", "diagnostic")),
                _case("damped-oscillator-compile", "damped_oscillator", "compile", tags=("for_demo", "stretch")),
                _case("planck-compile", "planck", "compile", tags=("for_demo", "stretch")),
            ),
        )
    raise BenchmarkValidationError("unknown_suite", f"{name!r} is not one of: {', '.join(BUILTIN_SUITES)}")


def list_builtin_suites() -> tuple[str, ...]:
    return BUILTIN_SUITES


def load_suite(path_or_name: str | Path) -> BenchmarkSuite:
    value = str(path_or_name)
    if value in BUILTIN_SUITES:
        suite = builtin_suite(value)
    else:
        path = Path(value)
        if not path.exists():
            raise BenchmarkValidationError("suite_not_found", f"{value!r} is not a built-in suite or existing path")
        suite = BenchmarkSuite.from_mapping(json.loads(path.read_text(encoding="utf-8")))
    suite.validate()
    return suite


def filter_runs(runs: Iterable[BenchmarkRun], run_filter: RunFilter | None = None) -> tuple[BenchmarkRun, ...]:
    run_filter = run_filter or RunFilter()
    return tuple(run for run in runs if run_filter.includes(run))


def run_benchmark_suite(suite: BenchmarkSuite, *, run_filter: RunFilter | None = None) -> BenchmarkSuiteResult:
    results = tuple(execute_benchmark_run(run) for run in filter_runs(suite.expanded_runs(), run_filter))
    return BenchmarkSuiteResult(suite, results)


def execute_benchmark_run(run: BenchmarkRun) -> BenchmarkRunResult:
    started = time.perf_counter()
    payload = _base_run_payload(run)
    try:
        payload.update(_execute_benchmark_run_inner(run))
    except Exception as exc:  # noqa: BLE001 - benchmark suites must preserve unexpected run failures.
        payload["status"] = "execution_error"
        payload["error"] = {"type": type(exc).__name__, "message": str(exc)}
    payload.pop("_compiled", None)
    payload["metrics"] = _extract_run_metrics(payload)
    payload["timing"] = {"elapsed_seconds": time.perf_counter() - started}
    _write_json(run.artifact_path, payload)
    return BenchmarkRunResult(run, str(payload["status"]), run.artifact_path, payload)


def _base_run_payload(run: BenchmarkRun) -> dict[str, Any]:
    return {
        "schema": "eml.benchmark_run.v1",
        "run": run.as_dict(),
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "code_version": _code_version(),
        },
        "status": "pending",
        "stage_statuses": {},
    }


def _execute_benchmark_run_inner(run: BenchmarkRun) -> dict[str, Any]:
    spec = demo_specs()[run.formula]
    splits = spec.make_splits(points=run.dataset.points, seed=run.seed)
    stage_statuses: dict[str, str] = {}

    if run.start_mode == "catalog":
        report = verify_candidate(spec.candidate, splits, tolerance=run.dataset.tolerance, recovered_requires_exact_eml=True)
        stage_statuses["catalog_showcase"] = report.status
        return {
            "status": report.status,
            "stage_statuses": stage_statuses,
            "verification": report.as_dict(),
            "claim_status": report.status,
        }

    if run.start_mode == "compile":
        compiled_payload = _compile_demo(run, splits)
        stage_statuses.update(compiled_payload.pop("stage_statuses"))
        return {"status": stage_statuses["compiled_seed"], "stage_statuses": stage_statuses, **compiled_payload}

    if run.start_mode == "blind":
        train = splits[0]
        config = TrainingConfig(
            depth=run.optimizer.depth,
            variables=(spec.variable,),
            steps=run.optimizer.steps,
            restarts=run.optimizer.restarts,
            seed=run.seed,
            lr=run.optimizer.lr,
        )
        fit = fit_eml_tree(train.inputs, train.target, config)
        report = verify_candidate(fit.snap.expression, splits, tolerance=run.dataset.tolerance)
        stage_statuses["blind_baseline"] = report.status
        status = report.status if report.status == "recovered" else ("snapped_but_failed" if fit.status == "snapped_candidate" else fit.status)
        return {
            "status": status,
            "stage_statuses": stage_statuses,
            "trained_eml_candidate": fit.manifest,
            "trained_eml_verification": report.as_dict(),
            "claim_status": report.status,
        }

    if run.start_mode == "warm_start":
        compiled_payload = _compile_demo(run, splits)
        stage_statuses.update(compiled_payload.pop("stage_statuses"))
        if stage_statuses["compiled_seed"] == "unsupported":
            return {
                "status": "unsupported",
                "stage_statuses": {**stage_statuses, "warm_start_attempt": "unsupported"},
                **compiled_payload,
                "warm_start_eml": {
                    "status": "unsupported",
                    "reason": "compile_failed",
                    "detail": "warm-start requires a validated compiled EML seed",
                },
            }

        compiled = compiled_payload.pop("_compiled")
        if compiled.metadata.depth > run.optimizer.max_warm_depth:
            return {
                "status": "unsupported",
                "stage_statuses": {**stage_statuses, "warm_start_attempt": "unsupported"},
                **compiled_payload,
                "warm_start_eml": {
                    "status": "unsupported",
                    "reason": "depth_too_large_for_warm_start",
                    "compiled_depth": compiled.metadata.depth,
                    "max_warm_depth": run.optimizer.max_warm_depth,
                },
            }

        train = splits[0]
        warm_depth = run.optimizer.warm_depth or compiled.metadata.depth
        config = TrainingConfig(
            depth=warm_depth,
            variables=(spec.variable,),
            steps=run.optimizer.warm_steps,
            restarts=run.optimizer.warm_restarts,
            seed=run.seed,
            lr=run.optimizer.lr,
        )
        warm = fit_warm_started_eml_tree(
            train.inputs,
            train.target,
            config,
            compiled.expression,
            perturbation_config=PerturbationConfig(seed=run.seed, noise_scale=run.perturbation_noise),
            verification_splits=splits,
            tolerance=run.dataset.tolerance,
            compiler_metadata=compiled.metadata.as_dict(),
        )
        stage_statuses["warm_start_attempt"] = warm.status
        if warm.verification is not None:
            stage_statuses["trained_exact_recovery"] = warm.verification.status
        return {
            "status": warm.status,
            "stage_statuses": stage_statuses,
            **compiled_payload,
            "warm_start_eml": warm.manifest,
            "claim_status": warm.verification.status if warm.verification else warm.status,
        }

    raise BenchmarkValidationError("invalid_start_mode", f"unsupported start mode {run.start_mode!r}")


def _compile_demo(run: BenchmarkRun, splits: Any) -> dict[str, Any]:
    spec = demo_specs()[run.formula]
    validation_inputs = {spec.variable: np.concatenate([split.inputs[spec.variable] for split in splits])}
    compiler_config = CompilerConfig(
        variables=(spec.variable,),
        constant_policy="literal_constants",
        max_depth=run.optimizer.max_compile_depth,
        max_nodes=run.optimizer.max_compile_nodes,
        max_power=run.optimizer.max_power,
        validation_tolerance=run.dataset.tolerance,
    )
    try:
        compiled = compile_and_validate(spec.candidate.to_sympy(), compiler_config, validation_inputs)
        report = verify_candidate(compiled.expression, splits, tolerance=run.dataset.tolerance)
        return {
            "stage_statuses": {"compiled_seed": report.status},
            "compiled_eml": compiled.as_dict(),
            "compiled_eml_verification": report.as_dict(),
            "_compiled": compiled,
            "claim_status": report.status,
        }
    except UnsupportedExpression as exc:
        return {
            "stage_statuses": {"compiled_seed": "unsupported"},
            "compiled_eml": {"status": "unsupported", **exc.as_dict()},
            "claim_status": "unsupported",
        }


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    serializable = {key: value for key, value in payload.items() if key != "_compiled"}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(serializable, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _code_version() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=2,
        )
        return result.stdout.strip()
    except Exception:  # noqa: BLE001 - provenance should not make benchmark execution fail.
        return "unknown"


def _extract_run_metrics(payload: Mapping[str, Any]) -> dict[str, Any]:
    candidate = payload.get("trained_eml_candidate")
    if not candidate and isinstance(payload.get("warm_start_eml"), Mapping):
        candidate = payload["warm_start_eml"].get("optimizer")

    verification = payload.get("trained_eml_verification")
    if not verification and isinstance(payload.get("warm_start_eml"), Mapping):
        verification = payload["warm_start_eml"].get("verification")
    if not verification:
        verification = payload.get("compiled_eml_verification") or payload.get("verification")

    active_slot_changes = None
    changed_slots = None
    if isinstance(candidate, Mapping):
        initialization = candidate.get("best_restart", {}).get("initialization") or {}
        perturbation = initialization.get("perturbation") or {}
        changes = perturbation.get("active_slot_changes")
        if isinstance(changes, list):
            active_slot_changes = len(changes)
            changed_slots = sum(1 for item in changes if item.get("changed"))

    return {
        "best_loss": candidate.get("best_loss") if isinstance(candidate, Mapping) else None,
        "post_snap_loss": candidate.get("post_snap_loss") if isinstance(candidate, Mapping) else None,
        "snap_min_margin": candidate.get("snap", {}).get("min_margin") if isinstance(candidate, Mapping) else None,
        "snap_active_node_count": candidate.get("snap", {}).get("active_node_count") if isinstance(candidate, Mapping) else None,
        "active_slot_count": active_slot_changes,
        "changed_slot_count": changed_slots,
        "verifier_status": verification.get("status") if isinstance(verification, Mapping) else None,
        "high_precision_max_error": verification.get("high_precision_max_error") if isinstance(verification, Mapping) else None,
    }


def write_aggregate_reports(result: BenchmarkSuiteResult, output_dir: Path | None = None) -> dict[str, Path]:
    output_dir = output_dir or (result.suite.artifact_root / result.suite.id)
    aggregate = aggregate_evidence(result)
    json_path = output_dir / "aggregate.json"
    markdown_path = output_dir / "aggregate.md"
    _write_json(json_path, aggregate)
    markdown_path.write_text(render_aggregate_markdown(aggregate), encoding="utf-8")
    return {"json": json_path, "markdown": markdown_path}


def aggregate_evidence(result: BenchmarkSuiteResult) -> dict[str, Any]:
    runs = [_run_summary(item) for item in result.results]
    return {
        "schema": "eml.benchmark_aggregate.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "suite": result.suite.as_dict(),
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "code_version": _code_version(),
        },
        "counts": _aggregate_counts(runs),
        "groups": {
            "formula": _group_counts(runs, lambda item: item["formula"]),
            "start_mode": _group_counts(runs, lambda item: item["start_mode"]),
            "perturbation_noise": _group_counts(runs, lambda item: str(item["perturbation_noise"])),
            "depth": _group_counts(runs, lambda item: str(item["optimizer"]["depth"])),
            "seed_group": _group_counts(runs, lambda item: "all" if item["seed"] is not None else "unknown"),
        },
        "runs": runs,
    }


def render_aggregate_markdown(aggregate: Mapping[str, Any]) -> str:
    lines = [
        f"# Benchmark Evidence: {aggregate['suite']['id']}",
        "",
        aggregate["suite"].get("description", ""),
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
    ]
    counts = aggregate["counts"]
    for key in ("total", "verifier_recovered", "same_ast_return", "verified_equivalent_ast", "unsupported", "failed", "execution_error"):
        lines.append(f"| {key} | {counts[key]} |")
    lines.append(f"| verifier_recovery_rate | {counts['verifier_recovery_rate']:.3f} |")
    lines.extend(["", "## By Formula", "", _markdown_group_table(aggregate["groups"]["formula"])])
    lines.extend(["", "## By Start Mode", "", _markdown_group_table(aggregate["groups"]["start_mode"])])
    lines.extend(["", "## Runs", "", "| Run ID | Formula | Mode | Status | Classification | Artifact |", "|--------|---------|------|--------|----------------|----------|"])
    for run in aggregate["runs"]:
        lines.append(
            f"| {run['run_id']} | {run['formula']} | {run['start_mode']} | {run['status']} | "
            f"{run['classification']} | {run['artifact_path']} |"
        )
    lines.append("")
    return "\n".join(lines)


def _markdown_group_table(groups: list[Mapping[str, Any]]) -> str:
    lines = [
        "| Group | Total | Verifier Recovered | Same AST | Unsupported | Failed | Recovery Rate |",
        "|-------|-------|--------------------|----------|-------------|--------|---------------|",
    ]
    for group in groups:
        lines.append(
            f"| {group['key']} | {group['total']} | {group['verifier_recovered']} | {group['same_ast_return']} | "
            f"{group['unsupported']} | {group['failed']} | {group['verifier_recovery_rate']:.3f} |"
        )
    return "\n".join(lines)


def _run_summary(result: BenchmarkRunResult) -> dict[str, Any]:
    payload = result.payload
    return {
        "run_id": result.run.run_id,
        "artifact_path": str(result.artifact_path),
        "suite_id": result.run.suite_id,
        "case_id": result.run.case_id,
        "formula": result.run.formula,
        "start_mode": result.run.start_mode,
        "seed": result.run.seed,
        "perturbation_noise": result.run.perturbation_noise,
        "optimizer": result.run.optimizer.as_dict(),
        "dataset": result.run.dataset.as_dict(),
        "status": result.status,
        "claim_status": payload.get("claim_status"),
        "classification": classify_run(payload),
        "metrics": payload.get("metrics", {}),
        "stage_statuses": payload.get("stage_statuses", {}),
    }


def classify_run(payload: Mapping[str, Any]) -> str:
    status = payload.get("status")
    claim_status = payload.get("claim_status")
    start_mode = payload.get("run", {}).get("start_mode") if isinstance(payload.get("run"), Mapping) else None
    if status == "unsupported":
        return "unsupported"
    if status == "execution_error":
        return "execution_failure"
    if start_mode == "blind" and claim_status == "recovered":
        return "blind_recovery"
    if status == "same_ast_return":
        return "same_ast_warm_start_return"
    if status == "verified_equivalent_ast":
        return "verified_equivalent_warm_start_recovery"
    if status == "snapped_but_failed":
        return "snapped_but_failed"
    if status == "soft_fit_only":
        return "soft_fit_only"
    if claim_status == "verified_showcase":
        return "verified_showcase"
    if status == "failed":
        return "failed"
    if claim_status == "recovered":
        return "verifier_recovered"
    return str(status or "unknown")


def _aggregate_counts(runs: list[Mapping[str, Any]]) -> dict[str, Any]:
    total = len(runs)
    verifier_recovered = sum(1 for run in runs if run.get("claim_status") == "recovered")
    return {
        "total": total,
        "verifier_recovered": verifier_recovered,
        "same_ast_return": sum(1 for run in runs if run["classification"] == "same_ast_warm_start_return"),
        "verified_equivalent_ast": sum(1 for run in runs if run["classification"] == "verified_equivalent_warm_start_recovery"),
        "unsupported": sum(1 for run in runs if run["classification"] == "unsupported"),
        "failed": sum(1 for run in runs if run["classification"] in {"failed", "snapped_but_failed", "soft_fit_only"}),
        "execution_error": sum(1 for run in runs if run["classification"] == "execution_failure"),
        "verifier_recovery_rate": verifier_recovered / total if total else 0.0,
    }


def _group_counts(runs: list[Mapping[str, Any]], key_fn: Any) -> list[dict[str, Any]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for run in runs:
        grouped.setdefault(str(key_fn(run)), []).append(run)
    return [{"key": key, **_aggregate_counts(items)} for key, items in sorted(grouped.items())]
