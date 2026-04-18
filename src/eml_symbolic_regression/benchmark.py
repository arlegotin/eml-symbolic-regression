"""Benchmark suite contracts for repeatable EML training evidence."""

from __future__ import annotations

import hashlib
import json
import multiprocessing
import platform
import queue
import statistics
import subprocess
import time
from copy import deepcopy
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

import numpy as np
import torch

from .basin import fit_perturbed_true_tree
from .compiler import CompilerConfig, UnsupportedExpression, compile_and_validate, diagnose_compile_expression
from .datasets import demo_specs, proof_dataset_manifest
from .expression import ConstantOccurrence, Expr, expr_from_document, format_constant_value, parse_constant_value
from .optimize import TrainingConfig, fit_eml_tree
from .proof import (
    EVIDENCE_CLASSES,
    TRAINING_MODES,
    ProofContractError,
    paper_claim,
    threshold_policy,
    validate_claim_reference,
)
from .repair import RepairConfig, cleanup_failed_candidate, repair_perturbed_candidate
from .semantics import AnomalyStats, EmlOperator, as_complex_tensor, eml_operator_from_spec, mse_complex_numpy, raw_eml_operator
from .verify import verify_candidate
from .witnesses import known_scaffold_kinds, resolve_scaffold_plan
from .warm_start import PerturbationConfig, fit_warm_started_eml_tree


START_MODES = ("catalog", "compile", "blind", "warm_start", "perturbed_tree")
BUILTIN_SUITES = (
    "smoke",
    "v1.2-evidence",
    "for-demo-diagnostics",
    "v1.3-standard",
    "v1.3-showcase",
    "v1.5-shallow-pure-blind",
    "v1.5-shallow-proof",
    "proof-perturbed-basin",
    "proof-perturbed-basin-beer-probes",
    "proof-depth-curve",
    "v1.7-family-smoke",
    "v1.7-family-shallow-pure-blind",
    "v1.7-family-shallow",
    "v1.7-family-basin",
    "v1.7-family-depth-curve",
    "v1.7-family-standard",
    "v1.7-family-showcase",
    "v1.8-family-smoke",
    "v1.8-family-calibration",
    "v1.8-family-shallow-pure-blind",
    "v1.8-family-shallow",
    "v1.8-family-basin",
    "v1.8-family-depth-curve",
    "v1.8-family-standard",
    "v1.8-family-showcase",
    "v1.9-arrhenius-evidence",
    "v1.9-michaelis-evidence",
    "v1.9-repair-evidence",
    "v1.10-logistic-evidence",
    "v1.10-planck-diagnostics",
)
DEFAULT_ARTIFACT_ROOT = Path("artifacts") / "benchmarks"
CAMPAIGN_ARTIFACT_ROOT = Path("artifacts") / "campaigns"
STABLE_EVIDENCE_SNAPSHOT_GENERATED_AT = "1970-01-01T00:00:00+00:00"
STABLE_EVIDENCE_SNAPSHOT_CODE_VERSION = "snapshot"
STABLE_EVIDENCE_SNAPSHOT_ELAPSED_SECONDS = 0.0
# Publication bundles must never block on SymPy pretty-printing of failed blind candidates.
SYMBOLIC_INLINE_NODE_BUDGET = 0
SYMBOLIC_RENDER_TIMEOUT_SECONDS = 2.0


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
class BenchmarkRepairConfig:
    preset: str = "default"

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any] | None, *, path: str = "repair") -> "BenchmarkRepairConfig":
        if payload is None:
            payload = {}
        elif not isinstance(payload, Mapping):
            raise BenchmarkValidationError("malformed_repair", "repair must be a mapping", path=path)
        return cls(preset=str(payload.get("preset", "default")))

    def validate(self, path: str) -> None:
        if self.preset not in {"default", "expanded_candidate_pool"}:
            raise BenchmarkValidationError(
                "invalid_repair",
                "repair preset must be one of: default, expanded_candidate_pool",
                path=f"{path}.preset",
            )

    def as_dict(self) -> dict[str, Any]:
        return {"preset": self.preset}

    def to_repair_config(self) -> RepairConfig:
        if self.preset == "expanded_candidate_pool":
            return RepairConfig.expanded_candidate_pool()
        return RepairConfig()


@dataclass(frozen=True)
class OptimizerBudget:
    depth: int = 2
    constants: tuple[complex, ...] = (1.0,)
    steps: int = 20
    restarts: int = 1
    lr: float = 0.05
    hardening_steps: int = 4
    hardening_temperature_end: float = 0.02
    hardening_emit_interval: int = 2
    warm_depth: int = 0
    warm_steps: int = 20
    warm_restarts: int = 1
    max_compile_depth: int = 13
    max_compile_nodes: int = 256
    max_warm_depth: int = 14
    max_power: int = 3
    clamp_exp_real: float = 40.0
    log_domain_epsilon: float = 1e-9
    log_safety_weight: float = 0.0
    log_safety_margin: float = 1e-6
    log_safety_imag_tolerance: float = 1e-6
    refit_steps: int = 80
    refit_lr: float = 0.02
    scaffold_initializers: tuple[str, ...] = ("exp", "log", "scaled_exp")
    scaffold_exclusions: tuple[str, ...] = ()
    operator_family: EmlOperator = field(default_factory=raw_eml_operator)
    operator_schedule: tuple[EmlOperator, ...] = ()

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any] | None, *, path: str = "optimizer") -> "OptimizerBudget":
        payload = payload or {}
        defaults = cls()
        values = {field_name: payload.get(field_name, getattr(defaults, field_name)) for field_name in cls.__dataclass_fields__}
        constants = values["constants"]
        if not isinstance(constants, (list, tuple)):
            raise BenchmarkValidationError("malformed_budget", "constants must be a list", path=f"{path}.constants")
        try:
            values["constants"] = tuple(parse_constant_value(value) for value in constants)
        except (KeyError, TypeError, ValueError) as exc:
            raise BenchmarkValidationError("invalid_budget", "constants must be scalar values", path=f"{path}.constants") from exc
        values["depth"] = int(values["depth"])
        values["steps"] = int(values["steps"])
        values["restarts"] = int(values["restarts"])
        values["hardening_steps"] = int(values["hardening_steps"])
        values["hardening_temperature_end"] = float(values["hardening_temperature_end"])
        values["hardening_emit_interval"] = int(values["hardening_emit_interval"])
        values["warm_depth"] = int(values["warm_depth"])
        values["warm_steps"] = int(values["warm_steps"])
        values["warm_restarts"] = int(values["warm_restarts"])
        values["max_compile_depth"] = int(values["max_compile_depth"])
        values["max_compile_nodes"] = int(values["max_compile_nodes"])
        values["max_warm_depth"] = int(values["max_warm_depth"])
        values["max_power"] = int(values["max_power"])
        values["lr"] = float(values["lr"])
        values["clamp_exp_real"] = float(values["clamp_exp_real"])
        values["log_domain_epsilon"] = float(values["log_domain_epsilon"])
        values["log_safety_weight"] = float(values["log_safety_weight"])
        values["log_safety_margin"] = float(values["log_safety_margin"])
        values["log_safety_imag_tolerance"] = float(values["log_safety_imag_tolerance"])
        values["refit_steps"] = int(values["refit_steps"])
        values["refit_lr"] = float(values["refit_lr"])
        scaffold_initializers = values["scaffold_initializers"]
        if not isinstance(scaffold_initializers, (list, tuple)):
            raise BenchmarkValidationError(
                "malformed_budget",
                "scaffold_initializers must be a list",
                path=f"{path}.scaffold_initializers",
            )
        values["scaffold_initializers"] = tuple(str(value) for value in scaffold_initializers)
        scaffold_exclusions = values["scaffold_exclusions"]
        if not isinstance(scaffold_exclusions, (list, tuple)):
            raise BenchmarkValidationError(
                "malformed_budget",
                "scaffold_exclusions must be a list",
                path=f"{path}.scaffold_exclusions",
            )
        values["scaffold_exclusions"] = tuple(str(value) for value in scaffold_exclusions)
        try:
            values["operator_family"] = eml_operator_from_spec(payload.get("operator_family"))
        except (KeyError, TypeError, ValueError) as exc:
            raise BenchmarkValidationError(
                "invalid_budget",
                "operator_family must identify raw_eml, CEML_s, ZEML_s, or cEML_s_t",
                path=f"{path}.operator_family",
            ) from exc
        operator_schedule = payload.get("operator_schedule", ())
        if operator_schedule in (None, ""):
            values["operator_schedule"] = ()
        elif isinstance(operator_schedule, (list, tuple)):
            parsed_schedule: list[EmlOperator] = []
            for index, item in enumerate(operator_schedule):
                try:
                    parsed_schedule.append(eml_operator_from_spec(item))
                except (KeyError, TypeError, ValueError) as exc:
                    raise BenchmarkValidationError(
                        "invalid_budget",
                        "operator_schedule entries must identify centered-family operators",
                        path=f"{path}.operator_schedule[{index}]",
                    ) from exc
            values["operator_schedule"] = tuple(parsed_schedule)
        else:
            raise BenchmarkValidationError("malformed_budget", "operator_schedule must be a list", path=f"{path}.operator_schedule")
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
        if self.hardening_steps < 0:
            raise BenchmarkValidationError("invalid_budget", "hardening_steps must be 0 or positive", path=f"{path}.hardening_steps")
        if self.hardening_emit_interval <= 0:
            raise BenchmarkValidationError(
                "invalid_budget",
                "hardening_emit_interval must be positive",
                path=f"{path}.hardening_emit_interval",
            )
        if self.warm_depth < 0:
            raise BenchmarkValidationError("invalid_budget", "warm_depth must be 0 or positive", path=f"{path}.warm_depth")
        if self.lr <= 0:
            raise BenchmarkValidationError("invalid_budget", "lr must be positive", path=f"{path}.lr")
        if self.hardening_temperature_end <= 0:
            raise BenchmarkValidationError(
                "invalid_budget",
                "hardening_temperature_end must be positive",
                path=f"{path}.hardening_temperature_end",
            )
        if self.clamp_exp_real <= 0:
            raise BenchmarkValidationError("invalid_budget", "clamp_exp_real must be positive", path=f"{path}.clamp_exp_real")
        if self.log_domain_epsilon <= 0:
            raise BenchmarkValidationError(
                "invalid_budget",
                "log_domain_epsilon must be positive",
                path=f"{path}.log_domain_epsilon",
            )
        if self.log_safety_weight < 0:
            raise BenchmarkValidationError(
                "invalid_budget",
                "log_safety_weight must be 0 or positive",
                path=f"{path}.log_safety_weight",
            )
        if self.log_safety_margin <= 0:
            raise BenchmarkValidationError(
                "invalid_budget",
                "log_safety_margin must be positive",
                path=f"{path}.log_safety_margin",
            )
        if self.log_safety_imag_tolerance <= 0:
            raise BenchmarkValidationError(
                "invalid_budget",
                "log_safety_imag_tolerance must be positive",
                path=f"{path}.log_safety_imag_tolerance",
            )
        if self.refit_steps < 0:
            raise BenchmarkValidationError("invalid_budget", "refit_steps must be 0 or positive", path=f"{path}.refit_steps")
        if self.refit_lr <= 0:
            raise BenchmarkValidationError("invalid_budget", "refit_lr must be positive", path=f"{path}.refit_lr")
        if not self.constants:
            raise BenchmarkValidationError("invalid_budget", "constants must not be empty", path=f"{path}.constants")
        for index, value in enumerate(self.constants):
            if not (np.isfinite(value.real) and np.isfinite(value.imag)):
                raise BenchmarkValidationError("invalid_budget", "constants must be finite", path=f"{path}.constants[{index}]")
        allowed_scaffolds = set(known_scaffold_kinds())
        unknown_scaffolds = sorted(set(self.scaffold_initializers) - allowed_scaffolds)
        if unknown_scaffolds:
            raise BenchmarkValidationError(
                "invalid_budget",
                f"unknown scaffold initializers: {', '.join(unknown_scaffolds)}",
                path=f"{path}.scaffold_initializers",
            )
        for index, operator in enumerate(self.operator_schedule):
            if operator.is_raw:
                raise BenchmarkValidationError(
                    "invalid_budget",
                    "operator_schedule entries must be centered-family operators",
                    path=f"{path}.operator_schedule[{index}]",
                )

    def as_dict(self) -> dict[str, Any]:
        return {
            "depth": self.depth,
            "constants": [format_constant_value(value) for value in self.constants],
            "steps": self.steps,
            "restarts": self.restarts,
            "lr": self.lr,
            "hardening_steps": self.hardening_steps,
            "hardening_temperature_end": self.hardening_temperature_end,
            "hardening_emit_interval": self.hardening_emit_interval,
            "warm_depth": self.warm_depth,
            "warm_steps": self.warm_steps,
            "warm_restarts": self.warm_restarts,
            "max_compile_depth": self.max_compile_depth,
            "max_compile_nodes": self.max_compile_nodes,
            "max_warm_depth": self.max_warm_depth,
            "max_power": self.max_power,
            "clamp_exp_real": self.clamp_exp_real,
            "log_domain_epsilon": self.log_domain_epsilon,
            "log_safety_weight": self.log_safety_weight,
            "log_safety_margin": self.log_safety_margin,
            "log_safety_imag_tolerance": self.log_safety_imag_tolerance,
            "refit_steps": self.refit_steps,
            "refit_lr": self.refit_lr,
            "scaffold_initializers": list(self.scaffold_initializers),
            "scaffold_exclusions": list(self.scaffold_exclusions),
            "operator_family": self.operator_family.as_dict(),
            "operator_schedule": [operator.as_dict() for operator in self.operator_schedule],
        }


def _tuple_field(payload: Mapping[str, Any], key: str, default: tuple[Any, ...], path: str) -> tuple[Any, ...]:
    value = payload.get(key, default)
    if not isinstance(value, (list, tuple)):
        raise BenchmarkValidationError("malformed_case", f"{key} must be a list", path=f"{path}.{key}")
    return tuple(value)


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
    claim_id: str | None = None
    threshold_policy_id: str | None = None
    training_mode: str | None = None
    repair: BenchmarkRepairConfig | None = None

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any], *, path: str) -> "BenchmarkCase":
        required = ("id", "formula", "start_mode")
        for key in required:
            if key not in payload:
                raise BenchmarkValidationError("malformed_case", f"missing required field {key!r}", path=path)
        seeds = tuple(int(seed) for seed in _tuple_field(payload, "seeds", (0,), path))
        noises = tuple(float(value) for value in _tuple_field(payload, "perturbation_noise", (0.0,), path))
        tags = tuple(str(tag) for tag in _tuple_field(payload, "tags", (), path))
        if "evidence_class" in payload:
            raise BenchmarkValidationError(
                "invalid_proof_contract",
                "evidence_class is derived from execution results and cannot be supplied by suite JSON",
                path=f"{path}.evidence_class",
            )
        return cls(
            id=str(payload["id"]),
            formula=str(payload["formula"]),
            start_mode=str(payload["start_mode"]),
            seeds=seeds,
            perturbation_noise=noises,
            dataset=DatasetConfig.from_mapping(payload.get("dataset")),
            optimizer=OptimizerBudget.from_mapping(payload.get("optimizer"), path=f"{path}.optimizer"),
            tags=tags,
            expect_recovery=bool(payload.get("expect_recovery", False)),
            claim_id=_optional_str(payload.get("claim_id")),
            threshold_policy_id=_optional_str(payload.get("threshold_policy_id")),
            training_mode=_optional_str(payload.get("training_mode")),
            repair=(
                BenchmarkRepairConfig.from_mapping(payload.get("repair"), path=f"{path}.repair")
                if "repair" in payload and payload.get("repair") is not None
                else None
            ),
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
        proof_contract_validated = False
        if self.claim_id == "paper-perturbed-true-tree-basin":
            self._validate_proof_contract(path)
            proof_contract_validated = True
        if self.start_mode not in {"warm_start", "perturbed_tree"} and any(noise != 0.0 for noise in self.perturbation_noise):
            raise BenchmarkValidationError(
                "invalid_perturbation",
                "only warm_start and perturbed_tree cases may use nonzero perturbation noise",
                path=f"{path}.perturbation_noise",
            )
        if not proof_contract_validated:
            self._validate_proof_contract(path)
        self.dataset.validate(f"{path}.dataset")
        self.optimizer.validate(f"{path}.optimizer")
        if self.repair is not None:
            self.repair.validate(f"{path}.repair")

    def _validate_proof_contract(self, path: str) -> None:
        training_mode = self.training_mode or _default_training_mode(self.start_mode)
        _validate_training_mode_for_start_mode(training_mode, self.start_mode, f"{path}.training_mode")
        if self.claim_id is None:
            if self.threshold_policy_id is not None:
                raise BenchmarkValidationError(
                    "invalid_proof_contract",
                    "threshold_policy_id requires claim_id",
                    path=f"{path}.threshold_policy_id",
                )
            return
        if self.threshold_policy_id is None:
            raise BenchmarkValidationError(
                "invalid_proof_contract",
                "claim_id requires threshold_policy_id",
                path=f"{path}.threshold_policy_id",
            )
        if self.training_mode is None:
            raise BenchmarkValidationError(
                "invalid_proof_contract",
                "claim_id requires training_mode",
                path=f"{path}.training_mode",
            )
        try:
            claim = validate_claim_reference(self.claim_id, self.threshold_policy_id, path=path)
        except ProofContractError as exc:
            raise _benchmark_proof_error(exc, path) from exc

        if claim.id == "paper-shallow-blind-recovery":
            if self.start_mode != "blind":
                raise BenchmarkValidationError(
                    "invalid_proof_contract",
                    "paper-shallow-blind-recovery cases must use blind start_mode",
                    path=f"{path}.start_mode",
                )
            if self.training_mode != TRAINING_MODES["blind_training"]:
                raise BenchmarkValidationError(
                    "invalid_proof_contract",
                    "paper-shallow-blind-recovery cases must use blind_training mode",
                    path=f"{path}.training_mode",
                )
            if self.threshold_policy_id != "measured_pure_blind_recovery":
                raise BenchmarkValidationError(
                    "invalid_proof_contract",
                    "paper-shallow-blind-recovery cases must use measured_pure_blind_recovery threshold",
                    path=f"{path}.threshold_policy_id",
                )
            if self.optimizer.scaffold_initializers:
                raise BenchmarkValidationError(
                    "invalid_proof_contract",
                    "paper-shallow-blind-recovery cases must disable scaffold_initializers",
                    path=f"{path}.optimizer.scaffold_initializers",
                )
        if claim.id == "paper-shallow-scaffolded-recovery":
            if self.start_mode != "blind":
                raise BenchmarkValidationError(
                    "invalid_proof_contract",
                    "paper-shallow-scaffolded-recovery cases must use blind start_mode",
                    path=f"{path}.start_mode",
                )
            if self.training_mode != TRAINING_MODES["blind_training"]:
                raise BenchmarkValidationError(
                    "invalid_proof_contract",
                    "paper-shallow-scaffolded-recovery cases must use blind_training mode",
                    path=f"{path}.training_mode",
                )
            if self.threshold_policy_id != "scaffolded_bounded_100_percent":
                raise BenchmarkValidationError(
                    "invalid_proof_contract",
                    "paper-shallow-scaffolded-recovery cases must use scaffolded_bounded_100_percent threshold",
                    path=f"{path}.threshold_policy_id",
                )
            if not self.optimizer.scaffold_initializers:
                raise BenchmarkValidationError(
                    "invalid_proof_contract",
                    "paper-shallow-scaffolded-recovery cases require scaffold_initializers",
                    path=f"{path}.optimizer.scaffold_initializers",
                )
        if claim.id == "paper-perturbed-true-tree-basin":
            if self.start_mode != "perturbed_tree":
                raise BenchmarkValidationError(
                    "invalid_proof_contract",
                    "paper-perturbed-true-tree-basin cases must use perturbed_tree start_mode",
                    path=f"{path}.start_mode",
                )
            if self.training_mode != TRAINING_MODES["perturbed_true_tree_training"]:
                raise BenchmarkValidationError(
                    "invalid_proof_contract",
                    "paper-perturbed-true-tree-basin cases must use perturbed_true_tree_training mode",
                    path=f"{path}.training_mode",
                )
            if self.threshold_policy_id != "bounded_100_percent":
                raise BenchmarkValidationError(
                    "invalid_proof_contract",
                    "paper-perturbed-true-tree-basin cases must use bounded_100_percent threshold",
                    path=f"{path}.threshold_policy_id",
                )
            if any(noise == 0.0 for noise in self.perturbation_noise):
                raise BenchmarkValidationError(
                    "invalid_proof_contract",
                    "paper-perturbed-true-tree-basin cases require declared nonzero perturbation noise",
                    path=f"{path}.perturbation_noise",
                )
        if claim.id == "paper-blind-depth-degradation":
            if self.start_mode not in {"blind", "perturbed_tree"}:
                raise BenchmarkValidationError(
                    "invalid_proof_contract",
                    "paper-blind-depth-degradation cases must use blind or perturbed_tree start_mode",
                    path=f"{path}.start_mode",
                )
            if self.threshold_policy_id != "measured_depth_curve":
                raise BenchmarkValidationError(
                    "invalid_proof_contract",
                    "paper-blind-depth-degradation cases must use measured_depth_curve threshold",
                    path=f"{path}.threshold_policy_id",
                )
            if self.start_mode == "perturbed_tree" and any(noise == 0.0 for noise in self.perturbation_noise):
                raise BenchmarkValidationError(
                    "invalid_proof_contract",
                    "paper-blind-depth-degradation perturbed rows require declared nonzero perturbation noise",
                    path=f"{path}.perturbation_noise",
                )

    def as_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.id,
            "formula": self.formula,
            "start_mode": self.start_mode,
            "seeds": list(self.seeds),
            "perturbation_noise": list(self.perturbation_noise),
            "dataset": self.dataset.as_dict(),
            "optimizer": self.optimizer.as_dict(),
            "tags": list(self.tags),
            "expect_recovery": self.expect_recovery,
            "claim_id": self.claim_id,
            "threshold_policy_id": self.threshold_policy_id,
            "training_mode": self.training_mode,
        }
        if self.repair is not None:
            payload["repair"] = self.repair.as_dict()
        return payload


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
    claim_id: str | None = None
    threshold_policy_id: str | None = None
    training_mode: str | None = None
    repair: BenchmarkRepairConfig | None = None

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
        if self.claim_id is not None or self.threshold_policy_id is not None:
            parts["proof"] = {
                "claim_id": self.claim_id,
                "threshold_policy_id": self.threshold_policy_id,
                "training_mode": self.training_mode,
            }
        if self.repair is not None:
            parts["repair"] = self.repair.as_dict()
        digest = hashlib.sha1(json.dumps(parts, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()[:12]
        return f"{_slug(self.suite_id)}-{_slug(self.case_id)}-{digest}"

    def as_dict(self) -> dict[str, Any]:
        payload = {
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
            "claim_id": self.claim_id,
            "threshold_policy_id": self.threshold_policy_id,
            "training_mode": self.training_mode,
        }
        if self.repair is not None:
            payload["repair"] = self.repair.as_dict()
        return payload


@dataclass(frozen=True)
class RunFilter:
    formulas: tuple[str, ...] = ()
    start_modes: tuple[str, ...] = ()
    case_ids: tuple[str, ...] = ()
    seeds: tuple[int, ...] = ()
    perturbation_noises: tuple[float, ...] = ()

    def includes(self, run: BenchmarkRun) -> bool:
        return (
            (not self.formulas or run.formula in self.formulas)
            and (not self.start_modes or run.start_mode in self.start_modes)
            and (not self.case_ids or run.case_id in self.case_ids)
            and (not self.seeds or run.seed in self.seeds)
            and (not self.perturbation_noises or run.perturbation_noise in self.perturbation_noises)
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
            if case.claim_id is not None:
                claim = paper_claim(case.claim_id)
                if self.id not in claim.suite_ids:
                    raise BenchmarkValidationError(
                        "invalid_proof_contract",
                        "claim does not declare this suite",
                        path=f"cases[{index}].claim_id",
                    )
                if claim.case_ids and case.id not in claim.case_ids:
                    raise BenchmarkValidationError(
                        "invalid_proof_contract",
                        "claim does not declare this case",
                        path=f"cases[{index}].id",
                    )

    def expanded_runs(self) -> tuple[BenchmarkRun, ...]:
        self.validate()
        runs: list[BenchmarkRun] = []
        for case in self.cases:
            noises = case.perturbation_noise if case.start_mode in {"warm_start", "perturbed_tree"} else (0.0,)
            training_mode = case.training_mode or _default_training_mode(case.start_mode)
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
                        claim_id=case.claim_id,
                        threshold_policy_id=case.threshold_policy_id,
                        training_mode=training_mode,
                        repair=case.repair,
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
                            claim_id=placeholder.claim_id,
                            threshold_policy_id=placeholder.threshold_policy_id,
                            training_mode=placeholder.training_mode,
                            repair=placeholder.repair,
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


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _default_training_mode(start_mode: str) -> str:
    modes = {
        "catalog": TRAINING_MODES["catalog_verification"],
        "compile": TRAINING_MODES["compile_only_verification"],
        "blind": TRAINING_MODES["blind_training"],
        "warm_start": TRAINING_MODES["compiler_warm_start_training"],
        "perturbed_tree": TRAINING_MODES["perturbed_true_tree_training"],
    }
    try:
        return modes[start_mode]
    except KeyError as exc:
        raise BenchmarkValidationError(
            "invalid_start_mode",
            f"{start_mode!r} is not one of: {', '.join(START_MODES)}",
            path="start_mode",
        ) from exc


def _validate_training_mode_for_start_mode(training_mode: str, start_mode: str, path: str) -> None:
    if training_mode not in TRAINING_MODES.values():
        raise BenchmarkValidationError(
            "invalid_proof_contract",
            f"{training_mode!r} is not one of: {', '.join(TRAINING_MODES.values())}",
            path=path,
        )
    expected = _default_training_mode(start_mode)
    if training_mode != expected:
        raise BenchmarkValidationError(
            "invalid_proof_contract",
            f"{start_mode!r} cases require training_mode {expected!r}, got {training_mode!r}",
            path=path,
        )


def _benchmark_proof_error(exc: ProofContractError, path: str) -> BenchmarkValidationError:
    exc_path = exc.path or "claim_id"
    if exc_path.startswith(f"{path}."):
        final_path = exc_path
    else:
        leaf = "threshold_policy_id" if "threshold_policy_id" in exc_path else "claim_id" if "claim_id" in exc_path else exc_path.rsplit(".", 1)[-1]
        final_path = f"{path}.{leaf}"
    return BenchmarkValidationError("invalid_proof_contract", exc.detail, path=final_path)


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
    constants: Iterable[complex] = (1.0,),
    warm_restarts: int = 1,
    max_warm_depth: int = 14,
    scaffold_initializers: Iterable[str] = ("exp", "log", "scaled_exp"),
    tags: Iterable[str] = (),
    expect_recovery: bool = False,
    claim_id: str | None = None,
    threshold_policy_id: str | None = None,
    training_mode: str | None = None,
    operator_family: EmlOperator | None = None,
    operator_schedule: Iterable[EmlOperator] = (),
    repair: BenchmarkRepairConfig | None = None,
) -> BenchmarkCase:
    return BenchmarkCase(
        id=id,
        formula=formula,
        start_mode=start_mode,
        seeds=tuple(seeds),
        perturbation_noise=tuple(perturbation_noise),
        dataset=DatasetConfig(points=points),
        optimizer=OptimizerBudget(
            depth=depth,
            constants=tuple(constants),
            steps=steps,
            restarts=restarts,
            warm_steps=warm_steps,
            warm_restarts=warm_restarts,
            max_warm_depth=max_warm_depth,
            scaffold_initializers=tuple(scaffold_initializers),
            operator_family=operator_family or raw_eml_operator(),
            operator_schedule=tuple(operator_schedule),
        ),
        tags=tuple(tags),
        expect_recovery=expect_recovery,
        claim_id=claim_id,
        threshold_policy_id=threshold_policy_id,
        training_mode=training_mode,
        repair=repair,
    )


@dataclass(frozen=True)
class _OperatorVariant:
    id: str
    operator_family: EmlOperator
    operator_schedule: tuple[EmlOperator, ...] = ()

    @property
    def label(self) -> str:
        if self.operator_schedule:
            return " -> ".join(operator.label for operator in self.operator_schedule)
        return self.operator_family.label

    @property
    def tags(self) -> tuple[str, ...]:
        return ("operator_family", f"operator:{self.id}")


def _family_variants(
    *,
    scales: Iterable[int] = (2,),
    include_continuation: bool = True,
    include_long_continuation: bool = False,
) -> tuple[_OperatorVariant, ...]:
    variants = [_OperatorVariant("raw", raw_eml_operator())]
    for scale in scales:
        variants.append(_OperatorVariant(f"ceml{scale}", eml_operator_from_spec(f"ceml_s:{scale}")))
        variants.append(_OperatorVariant(f"zeml{scale}", eml_operator_from_spec(f"zeml_s:{scale}")))
    if include_continuation:
        variants.append(
            _OperatorVariant(
                "zeml8-4",
                eml_operator_from_spec("zeml_s:8"),
                (eml_operator_from_spec("zeml_s:8"), eml_operator_from_spec("zeml_s:4")),
            )
        )
    if include_long_continuation:
        variants.append(
            _OperatorVariant(
                "zeml8-4-2-1",
                eml_operator_from_spec("zeml_s:8"),
                (
                    eml_operator_from_spec("zeml_s:8"),
                    eml_operator_from_spec("zeml_s:4"),
                    eml_operator_from_spec("zeml_s:2"),
                    eml_operator_from_spec("zeml_s:1"),
                ),
            )
        )
    return tuple(variants)


def _operator_variant_budget(base: OptimizerBudget, variant: _OperatorVariant) -> OptimizerBudget:
    initial_operator = variant.operator_schedule[0] if variant.operator_schedule else variant.operator_family
    scaffold_plan = resolve_scaffold_plan(base.scaffold_initializers, initial_operator)
    return replace(
        base,
        scaffold_initializers=scaffold_plan.enabled,
        scaffold_exclusions=tuple(dict.fromkeys((*base.scaffold_exclusions, *scaffold_plan.exclusions))),
        operator_family=variant.operator_family,
        operator_schedule=variant.operator_schedule,
    )


def _family_case(base: BenchmarkCase, variant: _OperatorVariant, *, suite_tag: str) -> BenchmarkCase:
    return replace(
        base,
        id=f"{base.id}-{variant.id}",
        optimizer=_operator_variant_budget(base.optimizer, variant),
        tags=tuple(dict.fromkeys((*base.tags, suite_tag, "family_matrix", *variant.tags))),
        claim_id=None,
        threshold_policy_id=None,
        expect_recovery=False if not variant.operator_family.is_raw else base.expect_recovery,
    )


def _family_suite(
    *,
    id: str,
    description: str,
    base_name: str,
    include_continuation: bool = True,
    scales: Iterable[int] = (2,),
    include_long_continuation: bool = False,
    suite_tag: str = "v1.7",
) -> BenchmarkSuite:
    base = builtin_suite(base_name)
    variants = _family_variants(
        scales=scales,
        include_continuation=include_continuation,
        include_long_continuation=include_long_continuation,
    )
    cases = tuple(_family_case(case, variant, suite_tag=suite_tag) for case in base.cases for variant in variants)
    return BenchmarkSuite(id=id, description=description, cases=cases)


def _v18_family_suite(*, id: str, description: str, base_name: str) -> BenchmarkSuite:
    return _family_suite(
        id=id,
        description=description,
        base_name=base_name,
        scales=(1, 2, 4, 8),
        include_continuation=True,
        include_long_continuation=True,
        suite_tag="v1.8",
    )


def _family_calibration_suite() -> BenchmarkSuite:
    cases = (
        _case(
            "cal-exp-blind",
            "exp",
            "blind",
            points=16,
            depth=1,
            steps=12,
            restarts=1,
            tags=("v1.8", "family_calibration", "exp_probe"),
        ),
        _case(
            "cal-log-blind",
            "log",
            "blind",
            points=16,
            depth=3,
            steps=18,
            restarts=1,
            tags=("v1.8", "family_calibration", "log_probe"),
        ),
    )
    variants = _family_variants(
        scales=(1, 2, 4, 8),
        include_continuation=True,
        include_long_continuation=True,
    )
    return BenchmarkSuite(
        id="v1.8-family-calibration",
        description="Focused v1.8 family calibration probes for shallow exp/log behavior across fixed scales and schedules.",
        cases=tuple(_family_case(case, variant, suite_tag="v1.8") for case in cases for variant in variants),
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
    if name == "v1.3-standard":
        return BenchmarkSuite(
            id="v1.3-standard",
            description="Standard v1.3 campaign matrix with shallow blind baselines, perturbation sweeps, and FOR_DEMO diagnostics.",
            cases=(
                _case("exp-blind", "exp", "blind", seeds=(0, 1), depth=1, steps=80, tags=("blind", "shallow")),
                _case("log-blind", "log", "blind", seeds=(0, 1), depth=3, steps=80, tags=("blind", "shallow")),
                _case(
                    "radioactive-decay-blind",
                    "radioactive_decay",
                    "blind",
                    seeds=(0, 1),
                    depth=4,
                    steps=80,
                    tags=("blind", "shallow", "for_demo"),
                ),
                _case(
                    "beer-perturbation-sweep",
                    "beer_lambert",
                    "warm_start",
                    seeds=(0, 1),
                    perturbation_noise=(0.0, 5.0, 35.0),
                    warm_steps=60,
                    tags=("warm_start", "perturbation", "for_demo"),
                    expect_recovery=True,
                ),
                _case("michaelis-warm-diagnostic", "michaelis_menten", "warm_start", tags=("diagnostic", "depth_gate", "for_demo")),
                _case("logistic-compile", "logistic", "compile", tags=("diagnostic", "for_demo")),
                _case(
                    "shockley-warm",
                    "shockley",
                    "warm_start",
                    warm_steps=1,
                    tags=("warm_start", "for_demo"),
                    expect_recovery=True,
                ),
                _case("planck-diagnostic", "planck", "compile", tags=("stretch", "depth_gate", "for_demo")),
            ),
        )
    if name == "v1.3-showcase":
        return BenchmarkSuite(
            id="v1.3-showcase",
            description="Showcase v1.3 campaign matrix with expanded seeds, perturbations, and full FOR_DEMO diagnostics.",
            cases=(
                _case("exp-blind", "exp", "blind", seeds=(0, 1, 2), depth=1, steps=120, tags=("blind", "shallow")),
                _case("log-blind", "log", "blind", seeds=(0, 1, 2), depth=3, steps=120, tags=("blind", "shallow")),
                _case(
                    "radioactive-decay-blind",
                    "radioactive_decay",
                    "blind",
                    seeds=(0, 1, 2),
                    depth=4,
                    steps=120,
                    tags=("blind", "shallow", "for_demo"),
                ),
                _case(
                    "beer-perturbation-sweep",
                    "beer_lambert",
                    "warm_start",
                    seeds=(0, 1, 2),
                    perturbation_noise=(0.0, 2.5, 5.0, 15.0, 35.0),
                    warm_steps=90,
                    tags=("warm_start", "perturbation", "for_demo"),
                    expect_recovery=True,
                ),
                _case("michaelis-warm-diagnostic", "michaelis_menten", "warm_start", warm_steps=90, tags=("diagnostic", "depth_gate", "for_demo")),
                _case("logistic-compile", "logistic", "compile", tags=("diagnostic", "for_demo")),
                _case(
                    "shockley-warm",
                    "shockley",
                    "warm_start",
                    warm_steps=1,
                    tags=("warm_start", "for_demo"),
                    expect_recovery=True,
                ),
                _case("damped-oscillator-compile", "damped_oscillator", "compile", tags=("stretch", "for_demo")),
                _case("planck-diagnostic", "planck", "compile", tags=("stretch", "depth_gate", "for_demo")),
            ),
        )
    if name == "v1.5-shallow-pure-blind":
        proof_kwargs = {
            "seeds": (0, 1, 2),
            "steps": 120,
            "restarts": 2,
            "points": 32,
            "tags": ("v1.5", "proof", "measured", "pure_blind"),
            "expect_recovery": False,
            "claim_id": "paper-shallow-blind-recovery",
            "threshold_policy_id": "measured_pure_blind_recovery",
            "training_mode": "blind_training",
            "scaffold_initializers": (),
        }
        return BenchmarkSuite(
            id="v1.5-shallow-pure-blind",
            description="Measured v1.5 pure random-initialized shallow blind suite with scaffold initializers disabled.",
            cases=(
                _case("shallow-exp-pure-blind", "exp", "blind", depth=1, **proof_kwargs),
                _case("shallow-log-pure-blind", "log", "blind", depth=3, **proof_kwargs),
                _case("shallow-radioactive-decay-pure-blind", "radioactive_decay", "blind", depth=9, constants=(-0.4,), **proof_kwargs),
                _case("shallow-beer-lambert-pure-blind", "beer_lambert", "blind", depth=9, constants=(-0.8,), **proof_kwargs),
                _case("shallow-scaled-exp-growth-pure-blind", "scaled_exp_growth", "blind", depth=9, constants=(0.4,), **proof_kwargs),
                _case("shallow-scaled-exp-fast-decay-pure-blind", "scaled_exp_fast_decay", "blind", depth=9, constants=(-1.2,), **proof_kwargs),
            ),
        )
    if name == "v1.5-shallow-proof":
        proof_kwargs = {
            "seeds": (0, 1, 2),
            "steps": 120,
            "restarts": 2,
            "points": 32,
            "tags": ("v1.5", "proof", "bounded", "scaffolded_blind"),
            "expect_recovery": True,
            "claim_id": "paper-shallow-scaffolded-recovery",
            "threshold_policy_id": "scaffolded_bounded_100_percent",
            "training_mode": "blind_training",
        }
        return BenchmarkSuite(
            id="v1.5-shallow-proof",
            description="Bounded v1.5 shallow scaffolded-training proof suite with fixed proof constants and evidenced scaled-exponential depth.",
            cases=(
                _case("shallow-exp-blind", "exp", "blind", depth=1, **proof_kwargs),
                _case("shallow-log-blind", "log", "blind", depth=3, **proof_kwargs),
                _case("shallow-radioactive-decay-blind", "radioactive_decay", "blind", depth=9, constants=(-0.4,), **proof_kwargs),
                _case("shallow-beer-lambert-blind", "beer_lambert", "blind", depth=9, constants=(-0.8,), **proof_kwargs),
                _case("shallow-scaled-exp-growth-blind", "scaled_exp_growth", "blind", depth=9, constants=(0.4,), **proof_kwargs),
                _case("shallow-scaled-exp-fast-decay-blind", "scaled_exp_fast_decay", "blind", depth=9, constants=(-1.2,), **proof_kwargs),
            ),
        )
    if name == "proof-perturbed-basin":
        proof_kwargs = {
            "points": 12,
            "tags": ("v1.5", "proof", "bounded", "perturbed_tree"),
            "expect_recovery": True,
            "claim_id": "paper-perturbed-true-tree-basin",
            "threshold_policy_id": "bounded_100_percent",
            "training_mode": "perturbed_true_tree_training",
        }
        return BenchmarkSuite(
            id="proof-perturbed-basin",
            description="Bounded v1.5 perturbed true-tree basin proof suite with declared nonzero perturbation envelopes.",
            cases=(
                _case(
                    "basin-depth1-perturbed",
                    "basin_depth1_exp",
                    "perturbed_tree",
                    seeds=(0, 1),
                    perturbation_noise=(0.05, 0.25),
                    depth=1,
                    warm_steps=12,
                    **proof_kwargs,
                ),
                _case(
                    "basin-depth2-perturbed",
                    "basin_depth2_exp_exp",
                    "perturbed_tree",
                    seeds=(0,),
                    perturbation_noise=(0.05, 0.10),
                    depth=2,
                    warm_steps=16,
                    **proof_kwargs,
                ),
                _case(
                    "basin-depth3-perturbed",
                    "basin_depth3_exp_exp_exp",
                    "perturbed_tree",
                    seeds=(0,),
                    perturbation_noise=(0.05,),
                    depth=3,
                    warm_steps=20,
                    **proof_kwargs,
                ),
                _case(
                    "basin-beer-lambert-bound",
                    "beer_lambert",
                    "perturbed_tree",
                    seeds=(0, 1),
                    perturbation_noise=(5.0,),
                    warm_steps=40,
                    warm_restarts=1,
                    max_warm_depth=10,
                    **proof_kwargs,
                ),
            ),
        )
    if name == "proof-perturbed-basin-beer-probes":
        return BenchmarkSuite(
            id="proof-perturbed-basin-beer-probes",
            description="Visible Beer-Lambert high-noise perturbed true-tree probe rows outside the bounded proof denominator.",
            cases=(
                _case(
                    "basin-beer-lambert-bound-probes",
                    "beer_lambert",
                    "perturbed_tree",
                    seeds=(0, 1),
                    perturbation_noise=(15.0, 35.0),
                    points=12,
                    warm_steps=40,
                    warm_restarts=1,
                    max_warm_depth=10,
                    tags=("bound_probe", "beer_lambert", "high_noise"),
                ),
            ),
        )
    if name == "proof-depth-curve":
        blind_kwargs = {
            "seeds": (0, 1),
            "points": 24,
            "steps": 80,
            "restarts": 3,
            "tags": ("v1.5", "proof", "measured", "depth_curve", "blind"),
            "expect_recovery": False,
            "claim_id": "paper-blind-depth-degradation",
            "threshold_policy_id": "measured_depth_curve",
            "training_mode": "blind_training",
        }
        perturbed_kwargs = {
            "seeds": (0, 1),
            "points": 24,
            "warm_restarts": 1,
            "tags": ("v1.5", "proof", "measured", "depth_curve", "perturbed_tree"),
            "expect_recovery": True,
            "claim_id": "paper-blind-depth-degradation",
            "threshold_policy_id": "measured_depth_curve",
            "training_mode": "perturbed_true_tree_training",
        }
        return BenchmarkSuite(
            id="proof-depth-curve",
            description="Measured v1.5 blind-vs-perturbed depth curve over deterministic exact EML targets at depths 2 through 6.",
            cases=(
                _case("depth-2-blind", "depth_curve_depth2", "blind", depth=2, **blind_kwargs),
                _case("depth-3-blind", "depth_curve_depth3", "blind", depth=3, **blind_kwargs),
                _case("depth-4-blind", "depth_curve_depth4", "blind", depth=4, **blind_kwargs),
                _case("depth-5-blind", "depth_curve_depth5", "blind", depth=5, **blind_kwargs),
                _case("depth-6-blind", "depth_curve_depth6", "blind", depth=6, **blind_kwargs),
                _case(
                    "depth-2-perturbed",
                    "depth_curve_depth2",
                    "perturbed_tree",
                    depth=2,
                    warm_steps=20,
                    perturbation_noise=(0.05,),
                    **perturbed_kwargs,
                ),
                _case(
                    "depth-3-perturbed",
                    "depth_curve_depth3",
                    "perturbed_tree",
                    depth=3,
                    warm_steps=20,
                    perturbation_noise=(0.05,),
                    **perturbed_kwargs,
                ),
                _case(
                    "depth-4-perturbed",
                    "depth_curve_depth4",
                    "perturbed_tree",
                    depth=4,
                    warm_steps=30,
                    perturbation_noise=(0.05,),
                    **perturbed_kwargs,
                ),
                _case(
                    "depth-5-perturbed",
                    "depth_curve_depth5",
                    "perturbed_tree",
                    depth=5,
                    warm_steps=30,
                    perturbation_noise=(0.05,),
                    **perturbed_kwargs,
                ),
                _case(
                    "depth-6-perturbed",
                    "depth_curve_depth6",
                    "perturbed_tree",
                    depth=6,
                    warm_steps=30,
                    perturbation_noise=(0.02,),
                    **perturbed_kwargs,
                ),
            ),
        )
    if name == "v1.7-family-smoke":
        return _family_suite(
            id="v1.7-family-smoke",
            description="CI-scale v1.7 raw-vs-centered operator-family smoke matrix.",
            base_name="smoke",
        )
    if name == "v1.7-family-shallow-pure-blind":
        return _family_suite(
            id="v1.7-family-shallow-pure-blind",
            description="v1.7 family matrix cloned from the shallow pure-blind proof denominator without proof thresholds.",
            base_name="v1.5-shallow-pure-blind",
        )
    if name == "v1.7-family-shallow":
        return _family_suite(
            id="v1.7-family-shallow",
            description="v1.7 family matrix cloned from the shallow scaffolded proof denominator without proof thresholds.",
            base_name="v1.5-shallow-proof",
        )
    if name == "v1.7-family-basin":
        return _family_suite(
            id="v1.7-family-basin",
            description="v1.7 family matrix cloned from the perturbed-basin proof denominator without proof thresholds.",
            base_name="proof-perturbed-basin",
        )
    if name == "v1.7-family-depth-curve":
        return _family_suite(
            id="v1.7-family-depth-curve",
            description="v1.7 family matrix cloned from the blind-vs-perturbed depth curve without proof thresholds.",
            base_name="proof-depth-curve",
        )
    if name == "v1.7-family-standard":
        return _family_suite(
            id="v1.7-family-standard",
            description="v1.7 standard-style raw-vs-centered operator-family comparison matrix.",
            base_name="v1.3-standard",
        )
    if name == "v1.7-family-showcase":
        return _family_suite(
            id="v1.7-family-showcase",
            description="v1.7 showcase-style raw-vs-centered operator-family comparison matrix.",
            base_name="v1.3-showcase",
        )
    if name == "v1.8-family-smoke":
        return _v18_family_suite(
            id="v1.8-family-smoke",
            description="CI-scale v1.8 raw-vs-centered operator-family smoke matrix with expanded fixed scales and schedules.",
            base_name="smoke",
        )
    if name == "v1.8-family-calibration":
        return _family_calibration_suite()
    if name == "v1.8-family-shallow-pure-blind":
        return _v18_family_suite(
            id="v1.8-family-shallow-pure-blind",
            description="v1.8 family matrix cloned from the shallow pure-blind proof denominator without proof thresholds.",
            base_name="v1.5-shallow-pure-blind",
        )
    if name == "v1.8-family-shallow":
        return _v18_family_suite(
            id="v1.8-family-shallow",
            description="v1.8 family matrix cloned from the shallow scaffolded proof denominator without proof thresholds.",
            base_name="v1.5-shallow-proof",
        )
    if name == "v1.8-family-basin":
        return _v18_family_suite(
            id="v1.8-family-basin",
            description="v1.8 family matrix cloned from the perturbed-basin proof denominator without proof thresholds.",
            base_name="proof-perturbed-basin",
        )
    if name == "v1.8-family-depth-curve":
        return _v18_family_suite(
            id="v1.8-family-depth-curve",
            description="v1.8 family matrix cloned from the blind-vs-perturbed depth curve without proof thresholds.",
            base_name="proof-depth-curve",
        )
    if name == "v1.8-family-standard":
        return _v18_family_suite(
            id="v1.8-family-standard",
            description="v1.8 standard-style raw-vs-centered operator-family comparison matrix.",
            base_name="v1.3-standard",
        )
    if name == "v1.8-family-showcase":
        return _v18_family_suite(
            id="v1.8-family-showcase",
            description="v1.8 showcase-style raw-vs-centered operator-family comparison matrix.",
            base_name="v1.3-showcase",
        )
    if name == "v1.9-arrhenius-evidence":
        return BenchmarkSuite(
            id="v1.9-arrhenius-evidence",
            description="Focused v1.9 Arrhenius exact warm-start evidence for normalized exp(-0.8/x).",
            cases=(
                _case(
                    "arrhenius-warm",
                    "arrhenius",
                    "warm_start",
                    seeds=(0,),
                    perturbation_noise=(0.0,),
                    points=24,
                    warm_steps=1,
                    tags=("v1.9", "arrhenius", "warm_start", "same_ast"),
                    expect_recovery=True,
                ),
            ),
        )
    if name == "v1.9-michaelis-evidence":
        return BenchmarkSuite(
            id="v1.9-michaelis-evidence",
            description="Focused v1.9 Michaelis-Menten exact warm-start evidence for normalized 2*x/(x+0.5).",
            cases=(
                _case(
                    "michaelis-warm",
                    "michaelis_menten",
                    "warm_start",
                    seeds=(0,),
                    perturbation_noise=(0.0,),
                    points=24,
                    warm_steps=1,
                    tags=("v1.9", "michaelis", "warm_start", "same_ast"),
                    expect_recovery=True,
                ),
            ),
        )
    if name == "v1.9-repair-evidence":
        expanded_repair = BenchmarkRepairConfig(preset="expanded_candidate_pool")
        return BenchmarkSuite(
            id="v1.9-repair-evidence",
            description="Focused v1.9 near-miss before/after suite for default versus expanded verifier-gated cleanup.",
            cases=(
                _case(
                    "repair-radioactive-blind-default",
                    "radioactive_decay",
                    "blind",
                    seeds=(1,),
                    points=24,
                    depth=4,
                    steps=80,
                    restarts=1,
                    tags=("v1.9", "repair", "near_miss", "default_cleanup"),
                    expect_recovery=False,
                ),
                _case(
                    "repair-radioactive-blind-expanded",
                    "radioactive_decay",
                    "blind",
                    seeds=(1,),
                    points=24,
                    depth=4,
                    steps=80,
                    restarts=1,
                    tags=("v1.9", "repair", "near_miss", "expanded_cleanup"),
                    expect_recovery=False,
                    repair=expanded_repair,
                ),
                _case(
                    "repair-beer-warm-default",
                    "beer_lambert",
                    "warm_start",
                    seeds=(1,),
                    perturbation_noise=(35.0,),
                    points=24,
                    depth=2,
                    warm_steps=60,
                    warm_restarts=1,
                    tags=("v1.9", "repair", "near_miss", "default_cleanup"),
                    expect_recovery=False,
                ),
                _case(
                    "repair-beer-warm-expanded",
                    "beer_lambert",
                    "warm_start",
                    seeds=(1,),
                    perturbation_noise=(35.0,),
                    points=24,
                    depth=2,
                    warm_steps=60,
                    warm_restarts=1,
                    tags=("v1.9", "repair", "near_miss", "expanded_cleanup"),
                    expect_recovery=False,
                    repair=expanded_repair,
                ),
            ),
        )
    if name == "v1.10-logistic-evidence":
        return BenchmarkSuite(
            id="v1.10-logistic-evidence",
            description="Focused v1.10 logistic compile evidence after exponential-saturation motif work.",
            cases=(
                _case(
                    "logistic-compile",
                    "logistic",
                    "compile",
                    seeds=(0,),
                    points=24,
                    tags=("v1.10", "logistic", "compile", "diagnostic", "unsupported"),
                    expect_recovery=False,
                ),
            ),
            artifact_root=CAMPAIGN_ARTIFACT_ROOT,
        )
    if name == "v1.10-planck-diagnostics":
        return BenchmarkSuite(
            id="v1.10-planck-diagnostics",
            description="Focused v1.10 Planck compile diagnostics after low-degree power motif work.",
            cases=(
                _case(
                    "planck-compile",
                    "planck",
                    "compile",
                    seeds=(0,),
                    points=24,
                    tags=("v1.10", "planck", "compile", "diagnostic", "stretch", "unsupported"),
                    expect_recovery=False,
                ),
            ),
            artifact_root=CAMPAIGN_ARTIFACT_ROOT,
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
    payload: dict[str, Any] | None = None
    try:
        payload = _base_run_payload(run)
        payload.update(_execute_benchmark_run_inner(run))
    except Exception as exc:  # noqa: BLE001 - benchmark suites must preserve unexpected run failures.
        if payload is None:
            payload = _minimal_run_payload(run)
        payload["status"] = "execution_error"
        payload["error"] = {"type": type(exc).__name__, "message": str(exc)}
    payload.pop("_compiled", None)
    payload["evidence_class"] = evidence_class_for_payload(payload)
    payload["metrics"] = _extract_run_metrics(payload)
    payload["timing"] = {"elapsed_seconds": time.perf_counter() - started}
    _write_json(run.artifact_path, payload)
    return BenchmarkRunResult(run, str(payload["status"]), run.artifact_path, payload)


def _minimal_run_payload(run: BenchmarkRun) -> dict[str, Any]:
    return {
        "schema": "eml.benchmark_run.v1",
        "run": run.as_dict(),
        "claim_id": run.claim_id,
        "claim_class": None,
        "training_mode": run.training_mode,
        "threshold": None,
        "dataset": run.dataset.as_dict(),
        "dataset_manifest": None,
        "budget": run.optimizer.as_dict(),
        "provenance": None,
    }


def _base_run_payload(run: BenchmarkRun) -> dict[str, Any]:
    manifest = proof_dataset_manifest(run.formula, points=run.dataset.points, seed=run.seed, tolerance=run.dataset.tolerance)
    claim = paper_claim(run.claim_id) if run.claim_id is not None else None
    threshold = threshold_policy(run.threshold_policy_id).as_dict() if run.threshold_policy_id is not None else None
    return {
        "schema": "eml.benchmark_run.v1",
        "run": run.as_dict(),
        "claim_id": run.claim_id,
        "claim_class": claim.claim_class if claim is not None else None,
        "training_mode": run.training_mode,
        "threshold": threshold,
        "dataset": run.dataset.as_dict(),
        "dataset_manifest": manifest,
        "budget": run.optimizer.as_dict(),
        "provenance": manifest["provenance"],
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
        config = _training_config_from_budget(
            run,
            variable=spec.variable,
            depth=run.optimizer.depth,
            steps=run.optimizer.steps,
            restarts=run.optimizer.restarts,
            seed=run.seed,
        )
        fit = fit_eml_tree(
            train.inputs,
            train.target,
            config,
            verification_splits=splits,
            tolerance=run.dataset.tolerance,
        )
        report = fit.verification or verify_candidate(fit.snap.expression, splits, tolerance=run.dataset.tolerance)
        stage_statuses["blind_baseline"] = report.status
        status = report.status if report.status == "recovered" else ("snapped_but_failed" if fit.status == "snapped_candidate" else fit.status)
        claim_status = report.status
        current_expression = fit.snap.expression
        current_verification = report
        current_source = "selected_exact_candidate"
        repair_payload = None
        repair_status = "not_attempted"
        if status != "recovered":
            cleanup = cleanup_failed_candidate(
                fit,
                depth=_fit_depth(fit, run.optimizer.depth),
                variables=_fit_variables(fit, (spec.variable,)),
                constants=_fit_constants(fit, run.optimizer.constants),
                verification_splits=splits,
                tolerance=run.dataset.tolerance,
                config=_repair_config_for_run(run),
                original_status=status,
                return_kind=status,
            )
            repair_payload = cleanup.as_dict()
            repair_status = "repaired" if cleanup.status == "repaired_candidate" else cleanup.status
            stage_statuses["local_repair"] = cleanup.status
            if cleanup.status == "repaired_candidate" and cleanup.verification is not None:
                status = "repaired_candidate"
                claim_status = cleanup.verification.status
                current_expression = cleanup.repaired_expression or current_expression
                current_verification = cleanup.verification
                current_source = "repaired_candidate"

        refit = _run_post_snap_refit(
            current_expression,
            verification=current_verification,
            source=current_source,
            training_split=train,
            verification_splits=splits,
            config=config,
            tolerance=run.dataset.tolerance,
        )
        stage_statuses["post_snap_refit"] = refit.status
        if refit.accepted and refit.verification is not None:
            claim_status = refit.verification.status
            if repair_status != "repaired" and refit.verification.status == "recovered":
                status = "recovered"
        return {
            "status": status,
            "stage_statuses": stage_statuses,
            "trained_eml_candidate": _manifest_with_budget_scaffold_exclusions(fit.manifest, run.optimizer),
            "trained_eml_verification": report.as_dict(),
            "repair": repair_payload,
            "repair_status": repair_status,
            "refit": refit.payload,
            "claim_status": claim_status,
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
                "claim_status": "unsupported",
                "warm_start_eml": {
                    "status": "unsupported",
                    "reason": "depth_too_large_for_warm_start",
                    "compiled_depth": compiled.metadata.depth,
                    "max_warm_depth": run.optimizer.max_warm_depth,
                },
            }
        if not _budget_operator_family(run.optimizer).is_raw:
            return {
                "status": "unsupported",
                "stage_statuses": {**stage_statuses, "warm_start_attempt": "unsupported"},
                **compiled_payload,
                "claim_status": "unsupported",
                "warm_start_eml": {
                    "status": "unsupported",
                    "reason": "centered_family_same_family_seed_missing",
                    **_centered_seed_unsupported_context(
                        run,
                        mode="warm_start",
                        seed_source="compiler_warm_start",
                    ),
                },
            }

        train = splits[0]
        warm_depth = run.optimizer.warm_depth or compiled.metadata.depth
        config = _training_config_from_budget(
            run,
            variable=spec.variable,
            depth=warm_depth,
            steps=run.optimizer.warm_steps,
            restarts=run.optimizer.warm_restarts,
            seed=run.seed,
            scaffold_initializers=(),
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
        status = warm.status
        claim_status = warm.verification.status if warm.verification else warm.status
        current_expression = warm.fit.snap.expression
        current_verification = warm.verification
        current_source = "warm_start_candidate"
        repair_payload = None
        repair_status = "not_attempted"
        if status not in {"same_ast_return", "verified_equivalent_ast", "recovered"}:
            cleanup = cleanup_failed_candidate(
                warm.fit,
                depth=_fit_depth(warm.fit, warm_depth),
                variables=_fit_variables(warm.fit, (spec.variable,)),
                constants=_fit_constants(warm.fit, run.optimizer.constants),
                verification_splits=splits,
                tolerance=run.dataset.tolerance,
                config=_repair_config_for_run(run),
                original_status=status,
                return_kind=status,
            )
            repair_payload = cleanup.as_dict()
            repair_status = "repaired" if cleanup.status == "repaired_candidate" else cleanup.status
            stage_statuses["local_repair"] = cleanup.status
            if cleanup.status == "repaired_candidate" and cleanup.verification is not None:
                status = "repaired_candidate"
                claim_status = cleanup.verification.status
                current_expression = cleanup.repaired_expression or current_expression
                current_verification = cleanup.verification
                current_source = "repaired_candidate"

        refit = _run_post_snap_refit(
            current_expression,
            verification=current_verification,
            source=current_source,
            training_split=train,
            verification_splits=splits,
            config=config,
            tolerance=run.dataset.tolerance,
        )
        stage_statuses["post_snap_refit"] = refit.status
        if refit.accepted and refit.verification is not None:
            claim_status = refit.verification.status
            if (
                repair_status != "repaired"
                and refit.verification.status == "recovered"
                and status not in {"same_ast_return", "verified_equivalent_ast", "recovered"}
            ):
                status = "verified_equivalent_ast"
        return {
            "status": status,
            "stage_statuses": stage_statuses,
            **compiled_payload,
            "warm_start_eml": warm.manifest,
            "repair": repair_payload,
            "repair_status": repair_status,
            "refit": refit.payload,
            "claim_status": claim_status,
        }

    if run.start_mode == "perturbed_tree":
        target_payload: dict[str, Any]
        target_metadata: dict[str, Any]
        candidate = spec.candidate
        if isinstance(candidate, Expr):
            target_expr = candidate
            target_payload = {"target_eml": target_expr.to_document(variables=[spec.variable], source="demo_spec_exact_eml")}
            target_metadata = {"formula_id": run.formula, "source": "demo_spec_exact_eml"}
        else:
            compiled_payload = _compile_demo(run, splits)
            stage_statuses.update(compiled_payload.pop("stage_statuses"))
            if stage_statuses["compiled_seed"] == "unsupported":
                return {
                    "status": "unsupported",
                    "stage_statuses": {**stage_statuses, "perturbed_true_tree_attempt": "unsupported"},
                    **compiled_payload,
                    "perturbed_true_tree": {
                        "status": "unsupported",
                        "reason": "compile_failed",
                        "detail": "perturbed-tree training requires an exact EML target seed",
                    },
                    "claim_status": "unsupported",
                }
            compiled = compiled_payload.pop("_compiled")
            target_expr = compiled.expression
            target_payload = compiled_payload
            target_metadata = {
                "formula_id": run.formula,
                "source": "compiled_demo_candidate",
                "compiled_metadata": compiled.metadata.as_dict(),
            }

        if target_expr.depth() > run.optimizer.max_warm_depth:
            return {
                "status": "unsupported",
                "stage_statuses": {**stage_statuses, "perturbed_true_tree_attempt": "unsupported"},
                **target_payload,
                "perturbed_true_tree": {
                    "status": "unsupported",
                    "reason": "depth_too_large_for_perturbed_tree",
                    "target_depth": target_expr.depth(),
                    "max_warm_depth": run.optimizer.max_warm_depth,
                },
                "claim_status": "unsupported",
            }
        if not _budget_operator_family(run.optimizer).is_raw:
            return {
                "status": "unsupported",
                "stage_statuses": {**stage_statuses, "perturbed_true_tree_attempt": "unsupported"},
                **target_payload,
                "perturbed_true_tree": {
                    "status": "unsupported",
                    "reason": "centered_family_same_family_seed_missing",
                    **_centered_seed_unsupported_context(
                        run,
                        mode="perturbed_tree",
                        seed_source=str(target_metadata.get("source", "target_exact_tree")),
                    ),
                },
                "claim_status": "unsupported",
            }

        train = splits[0]
        training_depth = run.optimizer.warm_depth or max(run.optimizer.depth, target_expr.depth())
        config = _training_config_from_budget(
            run,
            variable=spec.variable,
            depth=training_depth,
            steps=run.optimizer.warm_steps,
            restarts=run.optimizer.warm_restarts,
            seed=run.seed,
            scaffold_initializers=(),
        )
        basin = fit_perturbed_true_tree(
            train.inputs,
            train.target,
            config,
            target_expr,
            perturbation_config=PerturbationConfig(seed=run.seed, noise_scale=run.perturbation_noise),
            verification_splits=splits,
            tolerance=run.dataset.tolerance,
            target_metadata=target_metadata,
        )
        stage_statuses["perturbed_true_tree_attempt"] = basin.status
        if basin.verification is not None:
            stage_statuses["trained_exact_recovery"] = basin.verification.status
        raw_status = str(basin.manifest.get("raw_status") or basin.status)
        status = basin.status
        claim_status = basin.verification.status if basin.verification else basin.status
        current_expression = basin.fit.snap.expression
        current_verification = basin.verification
        current_source = "perturbed_true_tree_candidate"
        repair_payload = None
        repair_status = "not_attempted"
        if basin.status != "recovered":
            repair_constants = tuple(sorted(target_expr.constants(), key=lambda value: (value.real, value.imag)))
            repair = cleanup_failed_candidate(
                basin.fit,
                depth=_fit_depth(basin.fit, training_depth),
                variables=_fit_variables(basin.fit, tuple(sorted(target_expr.variables()))),
                constants=_fit_constants(basin.fit, repair_constants),
                verification_splits=splits,
                tolerance=run.dataset.tolerance,
                config=_repair_config_for_run(run),
                original_status=raw_status,
                return_kind=basin.return_kind,
            )
            if repair.status != "repaired_candidate":
                target_repair = repair_perturbed_candidate(
                    basin.fit,
                    target_expr=target_expr,
                    embedding=basin.embedding,
                    depth=training_depth,
                    variables=tuple(sorted(target_expr.variables())),
                    constants=repair_constants,
                    verification_splits=splits,
                    tolerance=run.dataset.tolerance,
                    original_status=raw_status,
                    return_kind=basin.return_kind,
                )
                if target_repair.status == "repaired_candidate" or repair.variant_count == 0:
                    repair = target_repair
            repair_payload = repair.as_dict()
            repair_status = "repaired" if repair.status == "repaired_candidate" else repair.status
            stage_statuses["local_repair"] = repair.status
            if repair.status == "repaired_candidate" and repair.verification is not None:
                status = "repaired_candidate"
                claim_status = repair.verification.status
                current_expression = repair.repaired_expression or current_expression
                current_verification = repair.verification
                current_source = "repaired_candidate"

        refit = _run_post_snap_refit(
            current_expression,
            verification=current_verification,
            source=current_source,
            training_split=train,
            verification_splits=splits,
            config=config,
            tolerance=run.dataset.tolerance,
        )
        stage_statuses["post_snap_refit"] = refit.status
        if refit.accepted and refit.verification is not None:
            claim_status = refit.verification.status
            if repair_status != "repaired" and refit.verification.status == "recovered" and status != "recovered":
                status = "recovered"
        return {
            "status": status,
            "stage_statuses": stage_statuses,
            **target_payload,
            "perturbed_true_tree": basin.manifest,
            "trained_eml_candidate": _manifest_with_budget_scaffold_exclusions(basin.fit.manifest, run.optimizer),
            "trained_eml_verification": basin.verification.as_dict() if basin.verification else None,
            "return_kind": basin.return_kind,
            "raw_status": raw_status,
            "repair": repair_payload,
            "repair_status": repair_status,
            "refit": refit.payload,
            "claim_status": claim_status,
        }

    raise BenchmarkValidationError("invalid_start_mode", f"unsupported start mode {run.start_mode!r}")


def _fit_depth(fit: FitResult, default_depth: int) -> int:
    config = fit.manifest.get("config") if isinstance(fit.manifest, Mapping) else None
    return int(config.get("depth", default_depth)) if isinstance(config, Mapping) else int(default_depth)


def _manifest_with_budget_scaffold_exclusions(manifest: Mapping[str, Any], budget: OptimizerBudget) -> dict[str, Any]:
    payload = deepcopy(dict(manifest))
    payload["scaffold_exclusions"] = list(
        dict.fromkeys(
            (
                *payload.get("scaffold_exclusions", ()),
                *budget.scaffold_exclusions,
            )
        )
    )
    return payload


def _repair_config_for_run(run: BenchmarkRun) -> RepairConfig | None:
    return run.repair.to_repair_config() if run.repair is not None else None


def _budget_operator_family(budget: OptimizerBudget) -> EmlOperator:
    return budget.operator_schedule[0] if budget.operator_schedule else budget.operator_family


def _budget_operator_schedule_label(budget: OptimizerBudget) -> str:
    return " -> ".join(operator.label for operator in budget.operator_schedule)


def _centered_seed_unsupported_context(run: BenchmarkRun, *, mode: str, seed_source: str) -> dict[str, Any]:
    operator = _budget_operator_family(run.optimizer)
    return {
        "operator_family": operator.as_dict(),
        "operator_schedule": [item.as_dict() for item in run.optimizer.operator_schedule],
        "unsupported_class": "missing_same_family_exact_seed",
        "counts_in_denominator": True,
        "mode": mode,
        "seed_source": seed_source,
        "detail": (
            f"{mode} requires an exact target tree from {operator.label}; "
            "raw EML compiler seeds are not embedded into centered-family trees as exact returns"
        ),
    }


def _fit_variables(fit: FitResult, default_variables: tuple[str, ...]) -> tuple[str, ...]:
    config = fit.manifest.get("config") if isinstance(fit.manifest, Mapping) else None
    variables = config.get("variables") if isinstance(config, Mapping) else None
    return tuple(str(value) for value in variables) if isinstance(variables, list) else tuple(default_variables)


def _fit_constants(fit: FitResult, default_constants: tuple[complex, ...]) -> tuple[complex, ...]:
    config = fit.manifest.get("config") if isinstance(fit.manifest, Mapping) else None
    constants = config.get("constants") if isinstance(config, Mapping) else None
    if not isinstance(constants, list):
        return tuple(default_constants)
    return tuple(parse_constant_value(value) for value in constants)


@dataclass(frozen=True)
class RefitResult:
    status: str
    accepted: bool
    expression: Expr | None
    verification: VerificationReport | None
    payload: dict[str, Any]


def _training_config_from_budget(
    run: BenchmarkRun,
    *,
    variable: str,
    depth: int,
    steps: int,
    restarts: int,
    seed: int,
    scaffold_initializers: tuple[str, ...] | None = None,
) -> TrainingConfig:
    return TrainingConfig(
        depth=depth,
        variables=(variable,),
        constants=run.optimizer.constants,
        steps=steps,
        restarts=restarts,
        seed=seed,
        lr=run.optimizer.lr,
        hardening_steps=run.optimizer.hardening_steps,
        hardening_temperature_end=run.optimizer.hardening_temperature_end,
        hardening_emit_interval=run.optimizer.hardening_emit_interval,
        clamp_exp_real=run.optimizer.clamp_exp_real,
        log_domain_epsilon=run.optimizer.log_domain_epsilon,
        log_safety_weight=run.optimizer.log_safety_weight,
        log_safety_margin=run.optimizer.log_safety_margin,
        log_safety_imag_tolerance=run.optimizer.log_safety_imag_tolerance,
        refit_steps=run.optimizer.refit_steps,
        refit_lr=run.optimizer.refit_lr,
        scaffold_initializers=run.optimizer.scaffold_initializers if scaffold_initializers is None else scaffold_initializers,
        operator_family=run.optimizer.operator_schedule[0] if run.optimizer.operator_schedule else run.optimizer.operator_family,
        operator_schedule=run.optimizer.operator_schedule,
    )


def _exact_candidate_metrics(
    expression: Expr,
    verification: VerificationReport | None,
    *,
    post_snap_loss: float,
) -> dict[str, Any]:
    verifier_status = verification.status if verification is not None else None
    return {
        "verifier_status": verifier_status,
        "status_rank": _refit_status_rank(verifier_status),
        "extrapolation_max_abs_error": _report_group_error(verification, lambda name: "extra" in name),
        "high_precision_max_error": verification.high_precision_max_error if verification is not None else float("inf"),
        "heldout_max_abs_error": _report_group_error(verification, lambda name: "hold" in name or "valid" in name),
        "post_snap_loss": post_snap_loss,
        "complexity": expression.node_count(),
    }


def _report_group_error(report: VerificationReport | None, predicate: Any) -> float:
    if report is None:
        return float("inf")
    values = [result.max_abs_error for result in report.split_results if predicate(result.name.lower())]
    if not values:
        return 0.0
    return float(max(values))


def _exact_candidate_ranking_key(metrics: Mapping[str, Any]) -> tuple[Any, ...]:
    return (
        int(metrics.get("status_rank", 3)),
        _finite_or_inf(metrics.get("extrapolation_max_abs_error")),
        _finite_or_inf(metrics.get("high_precision_max_error")),
        _finite_or_inf(metrics.get("heldout_max_abs_error")),
        _finite_or_inf(metrics.get("post_snap_loss")),
        int(metrics.get("complexity", 0)),
    )


def _refit_status_rank(status: str | None) -> int:
    return {
        "recovered": 0,
        "verified_showcase": 1,
        "failed": 2,
        None: 3,
    }.get(status, 3)


def _finite_or_inf(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return float("inf")
    return number if np.isfinite(number) else float("inf")


def _constant_rows(
    occurrences: tuple[ConstantOccurrence, ...],
    updated_values: Mapping[str, complex] | None = None,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in occurrences:
        after = complex(updated_values[item.path]) if updated_values is not None and item.path in updated_values else complex(item.value)
        rows.append(
            {
                "path": item.path,
                "before": format_constant_value(item.value),
                "after": format_constant_value(after),
                "changed": abs(after - complex(item.value)) > 1e-12,
                "refittable": item.refittable,
            }
        )
    return rows


def _symbolic_expression_worker(document: Mapping[str, Any], result_queue: Any) -> None:
    try:
        expression = expr_from_document(document)
        result_queue.put({"status": "rendered", "value": str(expression.to_sympy())})
    except Exception as exc:  # noqa: BLE001 - child process must marshal failures back to parent.
        result_queue.put({"status": "omitted_error", "detail": f"{type(exc).__name__}: {exc}"})


def _render_symbolic_expression_subprocess(document: Mapping[str, Any], *, timeout_seconds: float) -> dict[str, Any]:
    context = multiprocessing.get_context("spawn")
    result_queue = context.Queue(maxsize=1)
    process = context.Process(target=_symbolic_expression_worker, args=(document, result_queue))
    process.start()
    process.join(timeout_seconds)
    if process.is_alive():
        process.terminate()
        process.join(1.0)
        return {
            "status": "omitted_timeout",
            "mode": "subprocess",
            "timeout_seconds": timeout_seconds,
            "detail": "symbolic SymPy rendering exceeded the publication artifact time budget",
        }
    try:
        result = result_queue.get_nowait()
    except queue.Empty:
        return {
            "status": "omitted_error",
            "mode": "subprocess",
            "timeout_seconds": timeout_seconds,
            "detail": f"symbolic renderer exited with code {process.exitcode}",
        }
    return {
        "mode": "subprocess",
        "timeout_seconds": timeout_seconds,
        **dict(result),
    }


def _safe_symbolic_expression_payload(expression: Expr) -> dict[str, Any]:
    node_count = expression.node_count()
    depth = expression.depth()
    if node_count <= SYMBOLIC_INLINE_NODE_BUDGET:
        try:
            return {
                "status": "rendered",
                "mode": "inline",
                "node_count": node_count,
                "depth": depth,
                "value": str(expression.to_sympy()),
            }
        except Exception as exc:  # noqa: BLE001 - artifact export must fail soft on presentation-only rendering.
            return {
                "status": "omitted_error",
                "mode": "inline",
                "node_count": node_count,
                "depth": depth,
                "detail": f"{type(exc).__name__}: {exc}",
            }

    payload = _render_symbolic_expression_subprocess(
        expression.to_document(variables=sorted(expression.variables()), source="symbolic_render"),
        timeout_seconds=SYMBOLIC_RENDER_TIMEOUT_SECONDS,
    )
    payload["node_count"] = node_count
    payload["depth"] = depth
    return payload


def _exact_candidate_payload(
    expression: Expr,
    verification: VerificationReport | None,
    *,
    source: str,
    post_snap_loss: float,
    anomalies: dict[str, Any] | None = None,
    constant_rows: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    metrics = _exact_candidate_metrics(expression, verification, post_snap_loss=post_snap_loss)
    symbolic_payload = _safe_symbolic_expression_payload(expression)
    symbolic_expression = symbolic_payload.pop("value", None)
    payload: dict[str, Any] = {
        "source": source,
        "ast": expression.to_document(variables=sorted(expression.variables()), source=source),
        "symbolic_expression": symbolic_expression,
        "symbolic_expression_render": symbolic_payload,
        "post_snap_loss": post_snap_loss,
        "metrics": metrics,
        "verification": verification.as_dict() if verification is not None else None,
    }
    if anomalies is not None:
        payload["final_anomalies"] = anomalies
    if constant_rows is not None:
        payload["constants"] = constant_rows
    return payload


def _run_post_snap_refit(
    expression: Expr,
    *,
    verification: VerificationReport | None,
    source: str,
    training_split: DataSplit,
    verification_splits: list[DataSplit],
    config: TrainingConfig,
    tolerance: float,
) -> RefitResult:
    occurrences = expression.constant_occurrences()
    pre_loss = mse_complex_numpy(expression.evaluate_numpy(training_split.inputs), training_split.target)
    pre_payload = _exact_candidate_payload(
        expression,
        verification,
        source=source,
        post_snap_loss=pre_loss,
        constant_rows=_constant_rows(occurrences),
    )
    refittable = tuple(item for item in occurrences if item.refittable)
    fixed = tuple(item for item in occurrences if not item.refittable)

    if config.refit_steps <= 0:
        return RefitResult(
            status="not_attempted",
            accepted=False,
            expression=None,
            verification=None,
            payload={
                "status": "not_attempted",
                "accepted": False,
                "reason": "refit_disabled",
                "refittable_constants": _constant_rows(refittable),
                "fixed_constants": _constant_rows(fixed),
                "pre_refit_candidate": pre_payload,
                "post_refit_candidate": None,
                "selected_candidate": "pre_refit",
            },
        )

    if not refittable:
        return RefitResult(
            status="not_attempted",
            accepted=False,
            expression=None,
            verification=None,
            payload={
                "status": "not_attempted",
                "accepted": False,
                "reason": "no_refittable_constants",
                "refittable_constants": [],
                "fixed_constants": _constant_rows(fixed),
                "pre_refit_candidate": pre_payload,
                "post_refit_candidate": None,
                "selected_candidate": "pre_refit",
            },
        )

    parameter_map: dict[str, torch.nn.Parameter] = {}
    real_only_paths: set[str] = set()
    for item in refittable:
        value = complex(item.value)
        if abs(value.imag) <= 1e-12:
            parameter_map[item.path] = torch.nn.Parameter(torch.tensor(float(value.real), dtype=torch.float64))
            real_only_paths.add(item.path)
        else:
            parameter_map[item.path] = torch.nn.Parameter(torch.tensor(value, dtype=torch.complex128))
    optimizer = torch.optim.Adam(list(parameter_map.values()), lr=config.refit_lr)
    tensor_inputs = {name: as_complex_tensor(value) for name, value in training_split.inputs.items()}
    target_tensor = as_complex_tensor(training_split.target)
    best_loss = pre_loss
    best_values = {
        path: complex(float(parameter.detach().item()), 0.0) if path in real_only_paths else complex(parameter.detach().cpu().item())
        for path, parameter in parameter_map.items()
    }
    final_stats = AnomalyStats()
    steps_completed = 0

    for step in range(config.refit_steps):
        optimizer.zero_grad()
        stats = AnomalyStats()
        override_map = {
            path: torch.complex(parameter, torch.zeros_like(parameter))
            if path in real_only_paths
            else parameter.to(dtype=torch.complex128)
            for path, parameter in parameter_map.items()
        }
        prediction = expression.evaluate_torch(
            tensor_inputs,
            training=True,
            stats=stats,
            semantics=config.semantics_config(),
            constant_overrides=override_map,
        )
        fit_loss = torch.mean(torch.abs(prediction - target_tensor) ** 2)
        loss = fit_loss + stats.training_penalty(device=fit_loss.device)
        if not torch.isfinite(loss):
            final_stats = stats
            break
        loss.backward()
        optimizer.step()
        steps_completed = step + 1
        final_stats = stats
        fit_loss_value = float(fit_loss.detach().item())
        if np.isfinite(fit_loss_value) and fit_loss_value <= best_loss:
            best_loss = fit_loss_value
            best_values = {
                path: complex(float(parameter.detach().item()), 0.0)
                if path in real_only_paths
                else complex(parameter.detach().cpu().item())
                for path, parameter in parameter_map.items()
            }

    post_expression = expression.with_constant_updates(best_values)
    post_verification = verify_candidate(post_expression, verification_splits, tolerance=tolerance)
    post_payload = _exact_candidate_payload(
        post_expression,
        post_verification,
        source="post_snap_refit",
        post_snap_loss=best_loss,
        anomalies=final_stats.as_dict(),
        constant_rows=_constant_rows(refittable, best_values),
    )

    pre_metrics = pre_payload["metrics"] if isinstance(pre_payload.get("metrics"), Mapping) else {}
    post_metrics = post_payload["metrics"] if isinstance(post_payload.get("metrics"), Mapping) else {}
    accepted = _exact_candidate_ranking_key(post_metrics) <= _exact_candidate_ranking_key(pre_metrics)
    reason = "verifier_rank_improved_or_matched" if accepted else "fallback_rank_stronger"

    return RefitResult(
        status="accepted" if accepted else "rejected",
        accepted=accepted,
        expression=post_expression if accepted else None,
        verification=post_verification if accepted else None,
        payload={
            "status": "accepted" if accepted else "rejected",
            "accepted": accepted,
            "reason": reason,
            "optimizer": {"steps": config.refit_steps, "lr": config.refit_lr},
            "steps_completed": steps_completed,
            "refittable_constants": _constant_rows(refittable, best_values),
            "fixed_constants": _constant_rows(fixed),
            "pre_refit_candidate": pre_payload,
            "post_refit_candidate": post_payload,
            "selected_candidate": "post_refit" if accepted else "pre_refit",
        },
    )


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
            "compiled_eml": {
                "status": "unsupported",
                **exc.as_dict(),
                "diagnostic": diagnose_compile_expression(spec.candidate.to_sympy(), compiler_config, validation_inputs),
            },
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
    selected = candidate.get("selected_candidate") if isinstance(candidate, Mapping) else None
    fallback = candidate.get("fallback_candidate") if isinstance(candidate, Mapping) else None
    selection = candidate.get("selection") if isinstance(candidate, Mapping) else None

    verification = payload.get("trained_eml_verification")
    if not verification and isinstance(payload.get("warm_start_eml"), Mapping):
        verification = payload["warm_start_eml"].get("verification")
    if not verification:
        verification = payload.get("compiled_eml_verification") or payload.get("verification")
    if not verification and isinstance(selected, Mapping):
        verification = selected.get("verification")

    repair = payload.get("repair")
    repair_verification = repair.get("verification") if isinstance(repair, Mapping) else None
    repair_attempts = repair.get("moves_attempted") if isinstance(repair, Mapping) else None
    repair_accepted = repair.get("accepted_moves") if isinstance(repair, Mapping) else None
    repair_variant_count = repair.get("variant_count") if isinstance(repair, Mapping) else None
    repair_root_summaries = repair.get("variants_by_candidate_root") if isinstance(repair, Mapping) else None

    diagnosis = {}
    warm_start = payload.get("warm_start_eml")
    if isinstance(warm_start, Mapping):
        diagnosis = warm_start.get("diagnosis") or {}

    budget = payload.get("budget") if isinstance(payload.get("budget"), Mapping) else {}
    budget_operator = budget.get("operator_family") if isinstance(budget.get("operator_family"), Mapping) else {}
    budget_schedule = budget.get("operator_schedule")
    budget_schedule_label = (
        " -> ".join(str(item.get("label", "")) for item in budget_schedule if isinstance(item, Mapping))
        if isinstance(budget_schedule, list)
        else None
    )
    candidate_config = candidate.get("config") if isinstance(candidate, Mapping) and isinstance(candidate.get("config"), Mapping) else {}
    candidate_operator = candidate_config.get("operator_family") if isinstance(candidate_config.get("operator_family"), Mapping) else {}
    candidate_schedule = candidate_config.get("operator_schedule")
    candidate_schedule_label = (
        " -> ".join(str(item.get("label", "")) for item in candidate_schedule if isinstance(item, Mapping))
        if isinstance(candidate_schedule, list)
        else None
    )

    active_slot_changes = None
    changed_slots = None
    initialization: Mapping[str, Any] = {}
    if isinstance(candidate, Mapping):
        initialization = candidate.get("best_restart", {}).get("initialization") or {}
        anomalies = candidate.get("best_restart", {}).get("final_anomalies") or {}
        perturbation = initialization.get("perturbation") or {}
        changes = perturbation.get("active_slot_changes")
        if isinstance(changes, list):
            active_slot_changes = len(changes)
            changed_slots = sum(1 for item in changes if item.get("changed"))
    else:
        anomalies = {}

    refit = payload.get("refit") if isinstance(payload.get("refit"), Mapping) else {}
    post_refit = refit.get("post_refit_candidate") if isinstance(refit.get("post_refit_candidate"), Mapping) else {}
    post_refit_verification = post_refit.get("verification") if isinstance(post_refit.get("verification"), Mapping) else {}
    refit_constants = refit.get("refittable_constants")

    return {
        "operator_family": candidate_operator.get("label") or budget_operator.get("label"),
        "operator_schedule": candidate_schedule_label or budget_schedule_label,
        "scaffold_exclusions": list(budget.get("scaffold_exclusions", ())) if isinstance(budget, Mapping) else [],
        "unsupported_reason": _run_reason(payload) if payload.get("status") == "unsupported" else None,
        "best_loss": (
            selected.get("best_fit_loss")
            if isinstance(selected, Mapping)
            else candidate.get("best_loss")
            if isinstance(candidate, Mapping)
            else None
        ),
        "legacy_best_loss": candidate.get("legacy_best_loss") if isinstance(candidate, Mapping) else None,
        "post_snap_loss": (
            selected.get("post_snap_loss")
            if isinstance(selected, Mapping)
            else candidate.get("post_snap_loss")
            if isinstance(candidate, Mapping)
            else None
        ),
        "fallback_post_snap_loss": fallback.get("post_snap_loss") if isinstance(fallback, Mapping) else None,
        "snap_min_margin": (
            selected.get("snap", {}).get("min_margin")
            if isinstance(selected, Mapping)
            else candidate.get("snap", {}).get("min_margin")
            if isinstance(candidate, Mapping)
            else None
        ),
        "snap_active_node_count": (
            selected.get("snap", {}).get("active_node_count")
            if isinstance(selected, Mapping)
            else candidate.get("snap", {}).get("active_node_count")
            if isinstance(candidate, Mapping)
            else None
        ),
        "candidate_complexity": (
            selected.get("metrics", {}).get("complexity")
            if isinstance(selected, Mapping) and isinstance(selected.get("metrics"), Mapping)
            else None
        ),
        "candidate_pool_size": (
            selection.get("candidate_count")
            if isinstance(selection, Mapping)
            else len(candidate.get("candidates", ()))
            if isinstance(candidate, Mapping) and isinstance(candidate.get("candidates"), list)
            else None
        ),
        "selected_candidate_id": selection.get("selected_candidate_id") if isinstance(selection, Mapping) else None,
        "selected_candidate_source": selected.get("source") if isinstance(selected, Mapping) else None,
        "selected_candidate_attempt_index": selected.get("attempt_index") if isinstance(selected, Mapping) else None,
        "selected_candidate_checkpoint_index": selected.get("checkpoint_index") if isinstance(selected, Mapping) else None,
        "fallback_candidate_id": selection.get("fallback_candidate_id") if isinstance(selection, Mapping) else None,
        "fallback_candidate_source": fallback.get("source") if isinstance(fallback, Mapping) else None,
        "fallback_candidate_attempt_index": fallback.get("attempt_index") if isinstance(fallback, Mapping) else None,
        "fallback_candidate_checkpoint_index": fallback.get("checkpoint_index") if isinstance(fallback, Mapping) else None,
        "selection_mode": selection.get("mode") if isinstance(selection, Mapping) else None,
        "scaffold_source": initialization.get("kind") if isinstance(initialization, Mapping) else None,
        "scaffold_strategy": initialization.get("strategy") if isinstance(initialization, Mapping) else None,
        "scaffold_coefficient": initialization.get("coefficient") if isinstance(initialization, Mapping) else None,
        "active_slot_count": active_slot_changes,
        "changed_slot_count": changed_slots,
        "verifier_status": verification.get("status") if isinstance(verification, Mapping) else None,
        "high_precision_max_error": verification.get("high_precision_max_error") if isinstance(verification, Mapping) else None,
        "warm_start_mechanism": diagnosis.get("mechanism"),
        "warm_start_status": diagnosis.get("status"),
        "repair_status": payload.get("repair_status"),
        "repair_variant_count": repair_variant_count,
        "repair_candidate_root_count": repair.get("candidate_root_count") if isinstance(repair, Mapping) else None,
        "repair_candidate_root_summary_count": len(repair_root_summaries) if isinstance(repair_root_summaries, list) else 0,
        "repair_deduped_variant_count": repair.get("deduped_variant_count") if isinstance(repair, Mapping) else None,
        "repair_accepted_candidate_id": repair.get("accepted_candidate_id") if isinstance(repair, Mapping) else None,
        "repair_accepted_candidate_source": repair.get("accepted_candidate_source") if isinstance(repair, Mapping) else None,
        "repair_accepted_candidate_root_source": repair.get("accepted_candidate_root_source") if isinstance(repair, Mapping) else None,
        "repair_move_count": len(repair_attempts) if isinstance(repair_attempts, list) else 0,
        "repair_accepted_move_count": len(repair_accepted) if isinstance(repair_accepted, list) else 0,
        "repair_verifier_status": repair_verification.get("status") if isinstance(repair_verification, Mapping) else None,
        "refit_status": refit.get("status") if isinstance(refit, Mapping) else None,
        "refit_accepted": refit.get("accepted") if isinstance(refit, Mapping) else None,
        "refit_post_snap_loss": post_refit.get("post_snap_loss") if isinstance(post_refit, Mapping) else None,
        "refit_verifier_status": post_refit_verification.get("status") if isinstance(post_refit_verification, Mapping) else None,
        "refit_constant_count": len(refit_constants) if isinstance(refit_constants, list) else 0,
        "anomaly_clamp_count": anomalies.get("clamp_count") if isinstance(anomalies, Mapping) else None,
        "anomaly_exp_overflow_count": anomalies.get("exp_overflow_count") if isinstance(anomalies, Mapping) else None,
        "anomaly_log_small_magnitude_count": anomalies.get("log_small_magnitude_count") if isinstance(anomalies, Mapping) else None,
        "anomaly_log_non_positive_real_count": anomalies.get("log_non_positive_real_count") if isinstance(anomalies, Mapping) else None,
        "anomaly_log_branch_cut_count": anomalies.get("log_branch_cut_count") if isinstance(anomalies, Mapping) else None,
        "anomaly_log_non_finite_input_count": anomalies.get("log_non_finite_input_count") if isinstance(anomalies, Mapping) else None,
        "anomaly_log_safety_penalty": anomalies.get("log_safety_penalty") if isinstance(anomalies, Mapping) else None,
        "anomaly_expm1_overflow_count": anomalies.get("expm1_overflow_count") if isinstance(anomalies, Mapping) else None,
        "anomaly_log1p_branch_cut_count": anomalies.get("log1p_branch_cut_count") if isinstance(anomalies, Mapping) else None,
        "anomaly_shifted_singularity_near_count": anomalies.get("shifted_singularity_near_count") if isinstance(anomalies, Mapping) else None,
        "anomaly_shifted_singularity_min_distance": (
            anomalies.get("shifted_singularity_min_distance") if isinstance(anomalies, Mapping) else None
        ),
    }


def write_aggregate_reports(
    result: BenchmarkSuiteResult,
    output_dir: Path | None = None,
    *,
    stable_snapshot: bool = False,
) -> dict[str, Path]:
    output_dir = output_dir or (result.suite.artifact_root / result.suite.id)
    aggregate = aggregate_evidence(result)
    if stable_snapshot:
        aggregate = _stable_evidence_snapshot(aggregate)
        for item in result.results:
            _write_json(item.artifact_path, _stable_evidence_snapshot(item.payload))
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
            "evidence_class": _group_counts(runs, lambda item: item["evidence_class"]),
            "return_kind": _group_counts(runs, lambda item: item.get("return_kind") or "none"),
            "raw_status": _group_counts(runs, lambda item: item.get("raw_status") or "none"),
            "repair_status": _group_counts(runs, lambda item: item.get("repair_status") or "none"),
            "perturbation_noise": _group_counts(runs, lambda item: str(item["perturbation_noise"])),
            "depth": _group_counts(runs, lambda item: str(item["optimizer"]["depth"])),
            "seed_group": _group_counts(runs, lambda item: "all" if item["seed"] is not None else "unknown"),
        },
        "depth_curve": _depth_curve_summary(runs),
        "thresholds": _threshold_summary(runs),
        "runs": runs,
    }


def _stable_evidence_snapshot(payload: Mapping[str, Any]) -> dict[str, Any]:
    snapshot = deepcopy(dict(payload))
    if "generated_at" in snapshot:
        snapshot["generated_at"] = STABLE_EVIDENCE_SNAPSHOT_GENERATED_AT
    environment = snapshot.get("environment")
    if isinstance(environment, dict):
        environment["code_version"] = STABLE_EVIDENCE_SNAPSHOT_CODE_VERSION
    timing = snapshot.get("timing")
    if isinstance(timing, dict):
        timing["elapsed_seconds"] = STABLE_EVIDENCE_SNAPSHOT_ELAPSED_SECONDS
    return snapshot


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
    for key in (
        "total",
        "verifier_recovered",
        "same_ast_return",
        "verified_equivalent_ast",
        "repaired_candidate",
        "unsupported",
        "failed",
        "execution_error",
    ):
        lines.append(f"| {key} | {counts[key]} |")
    lines.append(f"| verifier_recovery_rate | {counts['verifier_recovery_rate']:.3f} |")
    lines.extend(["", "## By Formula", "", _markdown_group_table(aggregate["groups"]["formula"])])
    lines.extend(["", "## By Start Mode", "", _markdown_group_table(aggregate["groups"]["start_mode"])])
    lines.extend(["", "## By Evidence Class", "", _markdown_group_table(aggregate["groups"]["evidence_class"])])
    lines.extend(["", "## By Return Kind", "", _markdown_group_table(aggregate["groups"]["return_kind"])])
    lines.extend(["", "## By Raw Status", "", _markdown_group_table(aggregate["groups"]["raw_status"])])
    lines.extend(["", "## By Repair Status", "", _markdown_group_table(aggregate["groups"]["repair_status"])])
    if aggregate.get("depth_curve"):
        lines.extend(["", "## Depth Curve", "", _markdown_depth_curve_table(aggregate["depth_curve"])])
    lines.extend(["", "## Thresholds", "", _markdown_threshold_table(aggregate.get("thresholds", []))])
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


def _markdown_depth_curve_table(rows: list[Mapping[str, Any]]) -> str:
    lines = [
        "| Depth | Mode | Seeds | Recovered | Total | Rate | Median Best Loss | Median Post-Snap Loss | Median Runtime | Median Snap Margin |",
        "|-------|------|-------|-----------|-------|------|------------------|-----------------------|----------------|--------------------|",
    ]
    for row in rows:
        lines.append(
            f"| {row['depth']} | {row['start_mode']} | {row['seed_count']} | {row['recovered']} | {row['total']} | "
            f"{row['recovery_rate']:.3f} | {_format_optional_number(row['best_loss_median'])} | "
            f"{_format_optional_number(row['post_snap_loss_median'])} | {_format_optional_number(row['runtime_seconds_median'])} | "
            f"{_format_optional_number(row['snap_min_margin_median'])} |"
        )
    return "\n".join(lines)


def _markdown_threshold_table(thresholds: list[Mapping[str, Any]]) -> str:
    if not thresholds:
        return "No proof threshold metadata."
    lines = [
        "| Claim | Policy | Eligible | Passed | Failed | Rate | Required | Status |",
        "|-------|--------|----------|--------|--------|------|----------|--------|",
    ]
    for row in thresholds:
        required = row["required_rate"]
        required_value = "" if required is None else f"{required:.3f}"
        lines.append(
            f"| {row['claim_id']} | {row['threshold_policy_id']} | {row['eligible']} | {row['passed']} | "
            f"{row['failed']} | {row['rate']:.3f} | {required_value} | {row['status']} |"
        )
    return "\n".join(lines)


def _depth_curve_summary(runs: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    depth_curve_runs = [run for run in runs if run.get("claim_id") == "paper-blind-depth-degradation"]
    if not depth_curve_runs:
        return []

    grouped: dict[tuple[int, str, str], list[Mapping[str, Any]]] = {}
    for run in depth_curve_runs:
        depth = int(run.get("optimizer", {}).get("depth") or 0)
        start_mode = str(run.get("start_mode") or "unknown")
        training_mode = str(run.get("training_mode") or "unknown")
        grouped.setdefault((depth, start_mode, training_mode), []).append(run)

    rows: list[dict[str, Any]] = []
    for (depth, start_mode, training_mode), items in sorted(grouped.items()):
        best_losses = [_run_metric_number(run, "best_loss") for run in items]
        post_snap_losses = [_run_metric_number(run, "post_snap_loss") for run in items]
        runtimes = [_run_timing_seconds(run) for run in items]
        snap_margins = [_run_metric_number(run, "snap_min_margin") for run in items]
        recovered = sum(1 for run in items if run.get("claim_status") == "recovered")
        rows.append(
            {
                "depth": depth,
                "start_mode": start_mode,
                "training_mode": training_mode,
                "seed_count": len({int(run["seed"]) for run in items if run.get("seed") is not None}),
                "total": len(items),
                "recovered": recovered,
                "recovery_rate": recovered / len(items) if items else 0.0,
                "best_loss_values": [value for value in best_losses if value is not None],
                "best_loss_median": _median_or_none(value for value in best_losses if value is not None),
                "best_loss_min": min((value for value in best_losses if value is not None), default=None),
                "best_loss_max": max((value for value in best_losses if value is not None), default=None),
                "post_snap_loss_values": [value for value in post_snap_losses if value is not None],
                "post_snap_loss_median": _median_or_none(value for value in post_snap_losses if value is not None),
                "post_snap_loss_min": min((value for value in post_snap_losses if value is not None), default=None),
                "post_snap_loss_max": max((value for value in post_snap_losses if value is not None), default=None),
                "runtime_seconds_values": [value for value in runtimes if value is not None],
                "runtime_seconds_median": _median_or_none(value for value in runtimes if value is not None),
                "runtime_seconds_min": min((value for value in runtimes if value is not None), default=None),
                "runtime_seconds_max": max((value for value in runtimes if value is not None), default=None),
                "snap_min_margin_values": [value for value in snap_margins if value is not None],
                "snap_min_margin_median": _median_or_none(value for value in snap_margins if value is not None),
                "snap_min_margin_min": min((value for value in snap_margins if value is not None), default=None),
                "snap_min_margin_max": max((value for value in snap_margins if value is not None), default=None),
                "evidence_classes": _count_by_key(items, "evidence_class"),
            }
        )
    return rows


def _run_metric_number(run: Mapping[str, Any], key: str) -> float | None:
    metrics = run.get("metrics") if isinstance(run.get("metrics"), Mapping) else {}
    try:
        value = metrics.get(key)
        if value is None or value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _run_timing_seconds(run: Mapping[str, Any]) -> float | None:
    artifact_path = run.get("artifact_path")
    if not artifact_path:
        return None
    path = Path(str(artifact_path))
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError:
        return None
    timing = payload.get("timing") if isinstance(payload.get("timing"), Mapping) else {}
    try:
        value = timing.get("elapsed_seconds")
        if value is None or value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _median_or_none(values: Any) -> float | None:
    numeric = [value for value in values if value is not None]
    return float(statistics.median(numeric)) if numeric else None


def _format_optional_number(value: Any) -> str:
    try:
        if value is None or value == "":
            return "n/a"
        return f"{float(value):.4g}"
    except (TypeError, ValueError):
        return "n/a"


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
        "claim_id": payload.get("claim_id"),
        "claim_class": payload.get("claim_class"),
        "training_mode": payload.get("training_mode") or result.run.training_mode,
        "threshold_policy_id": result.run.threshold_policy_id,
        "threshold": payload.get("threshold"),
        "dataset_manifest": payload.get("dataset_manifest"),
        "provenance": payload.get("provenance"),
        "status": result.status,
        "return_kind": payload.get("return_kind"),
        "raw_status": payload.get("raw_status"),
        "repair_status": payload.get("repair_status"),
        "claim_status": payload.get("claim_status"),
        "classification": classify_run(payload),
        "evidence_class": payload.get("evidence_class") or evidence_class_for_payload(payload),
        "reason": _run_reason(payload),
        "metrics": payload.get("metrics", {}),
        "stage_statuses": payload.get("stage_statuses", {}),
    }


def _run_reason(payload: Mapping[str, Any]) -> str:
    error = payload.get("error")
    if isinstance(error, Mapping):
        error_type = error.get("type", "execution_error")
        message = error.get("message")
        return f"{error_type}: {message}" if message else str(error_type)

    compiled = payload.get("compiled_eml")
    if isinstance(compiled, Mapping) and compiled.get("status") == "unsupported":
        return str(compiled.get("reason") or "unsupported")

    warm = payload.get("warm_start_eml")
    if isinstance(warm, Mapping) and warm.get("status") == "unsupported":
        return str(warm.get("reason") or "unsupported")

    perturbed = payload.get("perturbed_true_tree")
    if isinstance(perturbed, Mapping) and perturbed.get("status") == "unsupported":
        return str(perturbed.get("reason") or "unsupported")

    for key in ("trained_eml_verification", "compiled_eml_verification", "verification"):
        verification = payload.get(key)
        if isinstance(verification, Mapping) and verification.get("reason"):
            return str(verification["reason"])

    if isinstance(warm, Mapping):
        verification = warm.get("verification")
        if isinstance(verification, Mapping) and verification.get("reason"):
            return str(verification["reason"])

    return str(payload.get("status") or "unknown")


def classify_run(payload: Mapping[str, Any]) -> str:
    status = payload.get("status")
    claim_status = payload.get("claim_status")
    return_kind = payload.get("return_kind")
    raw_status = payload.get("raw_status")
    repair_status = payload.get("repair_status")
    start_mode = payload.get("run", {}).get("start_mode") if isinstance(payload.get("run"), Mapping) else None
    if repair_status == "repaired":
        return "repaired_candidate"
    if return_kind in {"same_ast_return", "verified_equivalent_ast", "snapped_but_failed", "soft_fit_only"}:
        return str(return_kind)
    if raw_status == "unsupported":
        return "unsupported"
    if status == "unsupported":
        return "unsupported"
    if status == "execution_error":
        return "execution_failure"
    if start_mode == "blind" and claim_status == "recovered":
        if _blind_payload_used_scaffold(payload):
            return "scaffolded_blind_recovery"
        return "blind_recovery"
    if start_mode == "perturbed_tree" and status == "recovered":
        return f"perturbed_true_tree_{payload.get('return_kind') or 'recovered'}"
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


def evidence_class_for_payload(payload: Mapping[str, Any]) -> str:
    status = payload.get("status")
    claim_status = payload.get("claim_status")
    run = payload.get("run") if isinstance(payload.get("run"), Mapping) else {}
    start_mode = run.get("start_mode")
    training_mode = payload.get("training_mode") or run.get("training_mode")
    recovered = status in {"recovered", "verified_showcase"} or claim_status in {"recovered", "verified_showcase"}

    if status == "unsupported":
        return EVIDENCE_CLASSES["unsupported"]
    if status == "execution_error":
        return EVIDENCE_CLASSES["execution_failure"]
    if status == "repaired_candidate" or payload.get("repair_status") == "repaired":
        return EVIDENCE_CLASSES["repaired_candidate"]
    if status == "snapped_but_failed":
        return EVIDENCE_CLASSES["snapped_but_failed"]
    if status == "soft_fit_only":
        return EVIDENCE_CLASSES["soft_fit_only"]
    if status == "failed":
        return EVIDENCE_CLASSES["failed"]
    if start_mode == "catalog" and recovered:
        return EVIDENCE_CLASSES["catalog_verified"]
    if start_mode == "compile" and recovered:
        return EVIDENCE_CLASSES["compile_only_verified"]
    if training_mode == TRAINING_MODES["blind_training"] and recovered:
        if _blind_payload_used_scaffold(payload):
            return EVIDENCE_CLASSES["scaffolded_blind_training_recovered"]
        return EVIDENCE_CLASSES["blind_training_recovered"]
    if training_mode == TRAINING_MODES["compiler_warm_start_training"]:
        if status == "same_ast_return" or claim_status == "same_ast_return":
            return EVIDENCE_CLASSES["same_ast"]
        if status == "verified_equivalent_ast" or claim_status == "verified_equivalent_ast":
            return EVIDENCE_CLASSES["verified_equivalent"]
        if recovered:
            return EVIDENCE_CLASSES["compiler_warm_start_recovered"]
    if (
        start_mode == "perturbed_tree"
        and training_mode == TRAINING_MODES["perturbed_true_tree_training"]
        and recovered
        and _declares_nonzero_perturbation(run)
    ):
        return EVIDENCE_CLASSES["perturbed_true_tree_recovered"]
    return str(status or "unknown")


def _declares_nonzero_perturbation(run: Mapping[str, Any]) -> bool:
    try:
        return float(run.get("perturbation_noise", 0.0)) != 0.0
    except (TypeError, ValueError):
        return False


def _blind_payload_used_scaffold(payload: Mapping[str, Any]) -> bool:
    candidate = payload.get("trained_eml_candidate")
    if not isinstance(candidate, Mapping):
        return False
    best_restart = candidate.get("best_restart")
    if not isinstance(best_restart, Mapping):
        return False
    attempt_kind = best_restart.get("attempt_kind")
    return isinstance(attempt_kind, str) and attempt_kind.startswith("scaffold_")


def _aggregate_counts(runs: list[Mapping[str, Any]]) -> dict[str, Any]:
    total = len(runs)
    verifier_recovered = sum(1 for run in runs if run.get("claim_status") == "recovered")
    evidence_classes: dict[str, int] = {}
    for run in runs:
        evidence_class = str(run.get("evidence_class") or "unknown")
        evidence_classes[evidence_class] = evidence_classes.get(evidence_class, 0) + 1
    return {
        "total": total,
        "verifier_recovered": verifier_recovered,
        "same_ast_return": sum(1 for run in runs if run["classification"] in {"same_ast_warm_start_return", "same_ast_return"}),
        "verified_equivalent_ast": sum(
            1 for run in runs if run["classification"] in {"verified_equivalent_warm_start_recovery", "verified_equivalent_ast"}
        ),
        "repaired_candidate": sum(1 for run in runs if run["classification"] == "repaired_candidate"),
        "unsupported": sum(1 for run in runs if run["classification"] == "unsupported"),
        "failed": sum(1 for run in runs if run["classification"] in {"failed", "snapped_but_failed", "soft_fit_only"}),
        "execution_error": sum(1 for run in runs if run["classification"] == "execution_failure"),
        "verifier_recovery_rate": verifier_recovered / total if total else 0.0,
        "evidence_classes": dict(sorted(evidence_classes.items())),
    }


def _threshold_summary(runs: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[Mapping[str, Any]]] = {}
    for run in runs:
        claim_id = run.get("claim_id")
        threshold = run.get("threshold")
        threshold_policy_id = run.get("threshold_policy_id")
        if threshold_policy_id is None and isinstance(threshold, Mapping):
            threshold_policy_id = threshold.get("id")
        if claim_id is None and threshold_policy_id is None:
            continue
        if claim_id is None or threshold_policy_id is None:
            continue
        grouped.setdefault((str(claim_id), str(threshold_policy_id)), []).append(run)

    rows: list[dict[str, Any]] = []
    for (claim_id, threshold_policy_id), items in sorted(grouped.items()):
        claim = paper_claim(claim_id)
        policy = threshold_policy(threshold_policy_id)
        allowed_evidence_classes = _counted_evidence_classes_for_claim(claim_id, policy.allowed_evidence_classes)
        evidence_counts: dict[str, int] = {}
        passed = 0
        for item in items:
            evidence_class = str(item.get("evidence_class") or "unknown")
            evidence_counts[evidence_class] = evidence_counts.get(evidence_class, 0) + 1
            if evidence_class in allowed_evidence_classes:
                passed += 1

        eligible = len(items)
        rate = passed / eligible if eligible else 0.0
        failed = eligible - passed
        if policy.policy_type == "bounded_rate":
            required = policy.required_rate if policy.required_rate is not None else 1.0
            status = "passed" if eligible > 0 and rate >= required else "failed"
        elif policy.policy_type == "measured_rate":
            status = "reported"
        else:
            status = "context"
            failed = 0

        rows.append(
            {
                "claim_id": claim_id,
                "claim_class": claim.claim_class,
                "threshold_policy_id": threshold_policy_id,
                "threshold": policy.as_dict(),
                "eligible": eligible,
                "passed": passed,
                "failed": failed,
                "rate": rate,
                "required_rate": policy.required_rate,
                "status": status,
                "evidence_classes": dict(sorted(evidence_counts.items())),
            }
        )
    return rows


def _counted_evidence_classes_for_claim(claim_id: str, policy_classes: tuple[str, ...]) -> tuple[str, ...]:
    if claim_id == "paper-shallow-blind-recovery":
        return (EVIDENCE_CLASSES["blind_training_recovered"],)
    if claim_id == "paper-shallow-scaffolded-recovery":
        return (EVIDENCE_CLASSES["scaffolded_blind_training_recovered"],)
    if claim_id == "paper-perturbed-true-tree-basin":
        return (
            EVIDENCE_CLASSES["perturbed_true_tree_recovered"],
            EVIDENCE_CLASSES["repaired_candidate"],
        )
    return policy_classes


def _count_by_key(runs: list[Mapping[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for run in runs:
        value = str(run.get(key) or "unknown")
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def _group_counts(runs: list[Mapping[str, Any]], key_fn: Any) -> list[dict[str, Any]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for run in runs:
        grouped.setdefault(str(key_fn(run)), []).append(run)
    return [{"key": key, **_aggregate_counts(items)} for key, items in sorted(grouped.items())]
