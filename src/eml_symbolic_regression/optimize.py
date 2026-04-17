"""PyTorch optimization loop for soft EML trees."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Callable, Mapping

import numpy as np
import torch

from .expression import format_constant_value
from .master_tree import ActiveSlotAlternatives, SnapDecision, SnapResult, SoftEMLTree, constant_label
from .semantics import AnomalyStats, EmlOperator, TrainingSemanticsConfig, as_complex_tensor, mse_complex_numpy, raw_eml_operator
from .verify import DataSplit, VerificationReport, verify_candidate
from .witnesses import (
    CENTERED_FAMILY_SAME_FAMILY_WITNESS_MISSING,
    known_scaffold_kinds,
    resolve_scaffold_plan,
    scaffold_witness_for,
)


@dataclass(frozen=True)
class TrainingConfig:
    depth: int = 2
    variables: tuple[str, ...] = ("x",)
    constants: tuple[complex, ...] = (1.0,)
    steps: int = 300
    restarts: int = 3
    lr: float = 0.05
    temperature_start: float = 2.0
    temperature_end: float = 0.25
    hardening_steps: int = 4
    hardening_temperature_end: float = 0.02
    hardening_emit_interval: int = 2
    entropy_weight: float = 1e-3
    size_weight: float = 1e-4
    clamp_exp_real: float = 40.0
    log_domain_epsilon: float = 1e-9
    log_safety_weight: float = 0.0
    log_safety_margin: float = 1e-6
    log_safety_imag_tolerance: float = 1e-6
    refit_steps: int = 80
    refit_lr: float = 0.02
    seed: int = 0
    scaffold_initializers: tuple[str, ...] = ("exp", "log", "scaled_exp")
    operator_family: EmlOperator = field(default_factory=raw_eml_operator)
    operator_schedule: tuple[EmlOperator, ...] = ()

    def semantics_config(self) -> TrainingSemanticsConfig:
        return TrainingSemanticsConfig(
            clamp_exp_real=self.clamp_exp_real,
            log_domain_epsilon=self.log_domain_epsilon,
            log_safety_weight=self.log_safety_weight,
            log_safety_margin=self.log_safety_margin,
            log_safety_imag_tolerance=self.log_safety_imag_tolerance,
        )

    def operator_payload(self) -> dict[str, Any]:
        return {
            "operator_family": self.operator_family.as_dict(),
            "operator_schedule": [operator.as_dict() for operator in self.operator_schedule],
        }


@dataclass(frozen=True)
class ExactCandidate:
    candidate_id: str
    attempt_index: int
    random_restart: int | None
    seed: int
    attempt_kind: str
    source: str
    checkpoint_index: int | None
    hardening_step: int | None
    global_step: int
    temperature: float
    best_fit_loss: float
    post_snap_loss: float
    snap: SnapResult
    slot_alternatives: tuple[ActiveSlotAlternatives, ...] = ()
    verification: VerificationReport | None = None
    selection_metrics: dict[str, Any] | None = None

    def as_dict(self) -> dict[str, Any]:
        low_margin = sorted(self.snap.decisions, key=lambda item: item.margin)[:5]
        return {
            "candidate_id": self.candidate_id,
            "attempt_index": self.attempt_index,
            "random_restart": self.random_restart,
            "seed": self.seed,
            "attempt_kind": self.attempt_kind,
            "source": self.source,
            "checkpoint_index": self.checkpoint_index,
            "hardening_step": self.hardening_step,
            "global_step": self.global_step,
            "temperature": self.temperature,
            "best_fit_loss": self.best_fit_loss,
            "post_snap_loss": self.post_snap_loss,
            "active_slot_count": len(self.snap.decisions),
            "low_margin_slot_count": sum(1 for item in self.snap.decisions if item.margin < 0.1),
            "lowest_margin_slots": [_decision_payload(item) for item in low_margin],
            "snap": self.snap.as_dict(),
            "slot_alternatives": [item.as_dict() for item in self.slot_alternatives],
            "verification": self.verification.as_dict() if self.verification is not None else None,
            "selection_metrics": dict(self.selection_metrics or {}),
        }


@dataclass(frozen=True)
class FitResult:
    status: str
    best_loss: float
    post_snap_loss: float
    snap: SnapResult
    manifest: dict[str, Any]
    verification: VerificationReport | None = None
    selected_candidate: ExactCandidate | None = None
    fallback_candidate: ExactCandidate | None = None
    candidates: tuple[ExactCandidate, ...] = ()


def _temperature(config: TrainingConfig, step: int) -> float:
    if config.steps <= 1:
        return config.temperature_end
    frac = step / (config.steps - 1)
    return config.temperature_start + frac * (config.temperature_end - config.temperature_start)


def _hardening_temperature(config: TrainingConfig, step: int) -> float:
    if config.hardening_steps <= 1:
        return config.hardening_temperature_end
    frac = step / (config.hardening_steps - 1)
    return config.temperature_end + frac * (config.hardening_temperature_end - config.temperature_end)


def _should_emit_hardening_candidate(config: TrainingConfig, step: int) -> bool:
    if config.hardening_steps <= 0:
        return False
    if step == config.hardening_steps - 1:
        return True
    interval = max(int(config.hardening_emit_interval), 1)
    return step % interval == 0


def _decision_payload(decision: SnapDecision) -> dict[str, Any]:
    return {
        "slot": f"{decision.path}.{decision.side}",
        "choice": decision.choice,
        "probability": decision.probability,
        "margin": decision.margin,
    }


def _train_step(
    model: SoftEMLTree,
    optimizer: torch.optim.Optimizer,
    tensor_inputs: Mapping[str, torch.Tensor],
    target_tensor: torch.Tensor,
    *,
    temperature: float,
    config: TrainingConfig,
    operator_family: EmlOperator,
) -> tuple[float | None, AnomalyStats]:
    optimizer.zero_grad()
    model.set_operator(operator_family)
    stats = AnomalyStats()
    pred = model(
        tensor_inputs,
        temperature=temperature,
        training_semantics=True,
        stats=stats,
        semantics=config.semantics_config(),
    )
    fit_loss = torch.mean(torch.abs(pred - target_tensor) ** 2)
    entropy = model.gate_entropy(temperature)
    size = model.expected_child_use(temperature)
    loss = fit_loss + config.entropy_weight * entropy + config.size_weight * size + stats.training_penalty(device=fit_loss.device)
    if not torch.isfinite(loss):
        return None, stats
    loss.backward()
    optimizer.step()
    return float(fit_loss.detach().item()), stats


def _emit_candidate(
    model: SoftEMLTree,
    inputs: Mapping[str, Any],
    target: Any,
    *,
    candidate_id: str,
    attempt_index: int,
    random_restart: int | None,
    seed: int,
    attempt_kind: str,
    source: str,
    checkpoint_index: int | None,
    hardening_step: int | None,
    global_step: int,
    temperature: float,
    best_fit_loss: float,
) -> ExactCandidate:
    snap = model.snap()
    slot_alternatives = model.active_slot_alternatives(top_k=2)
    snapped_pred = snap.expression.evaluate_numpy({name: np.asarray(value) for name, value in inputs.items()})
    post_snap_loss = mse_complex_numpy(snapped_pred, target)
    return ExactCandidate(
        candidate_id=candidate_id,
        attempt_index=attempt_index,
        random_restart=random_restart,
        seed=seed,
        attempt_kind=attempt_kind,
        source=source,
        checkpoint_index=checkpoint_index,
        hardening_step=hardening_step,
        global_step=global_step,
        temperature=temperature,
        best_fit_loss=best_fit_loss,
        post_snap_loss=post_snap_loss,
        snap=snap,
        slot_alternatives=slot_alternatives,
    )


def _report_group_error(report: VerificationReport | None, predicate: Callable[[str], bool]) -> float:
    if report is None:
        return float("inf")
    values = [result.max_abs_error for result in report.split_results if predicate(result.name.lower())]
    if not values:
        return 0.0
    return float(max(values))


def _selection_metrics(candidate: ExactCandidate, report: VerificationReport | None) -> dict[str, Any]:
    verifier_status = report.status if report is not None else None
    extrap_error = _report_group_error(report, lambda name: "extra" in name)
    heldout_error = _report_group_error(report, lambda name: "hold" in name or "valid" in name)
    return {
        "verifier_status": verifier_status,
        "status_rank": _status_rank(verifier_status),
        "extrapolation_max_abs_error": extrap_error,
        "high_precision_max_error": report.high_precision_max_error if report is not None else float("inf"),
        "heldout_max_abs_error": heldout_error,
        "post_snap_loss": candidate.post_snap_loss,
        "complexity": candidate.snap.active_node_count,
        "soft_fit_loss": candidate.best_fit_loss,
    }


def _status_rank(status: str | None) -> int:
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


def _candidate_ranking_key(candidate: ExactCandidate) -> tuple[Any, ...]:
    metrics = candidate.selection_metrics or {}
    return (
        int(metrics.get("status_rank", 3)),
        _finite_or_inf(metrics.get("extrapolation_max_abs_error")),
        _finite_or_inf(metrics.get("high_precision_max_error")),
        _finite_or_inf(metrics.get("heldout_max_abs_error")),
        _finite_or_inf(metrics.get("post_snap_loss")),
        int(metrics.get("complexity", candidate.snap.active_node_count)),
        _finite_or_inf(metrics.get("soft_fit_loss")),
        candidate.candidate_id,
    )


def _select_exact_candidate(
    candidates: list[ExactCandidate],
    *,
    verification_splits: list[DataSplit] | None,
    tolerance: float,
) -> tuple[list[ExactCandidate], str]:
    selection_mode = "verifier_gated_exact_candidate_pool" if verification_splits is not None else "train_post_snap_exact_candidate_pool"
    ranked: list[ExactCandidate] = []
    for candidate in candidates:
        report = (
            verify_candidate(candidate.snap.expression, verification_splits, tolerance=tolerance)
            if verification_splits is not None
            else None
        )
        ranked.append(replace(candidate, verification=report, selection_metrics=_selection_metrics(candidate, report)))
    ranked.sort(key=_candidate_ranking_key)
    return ranked, selection_mode


def fit_eml_tree(
    inputs: Mapping[str, Any],
    target: Any,
    config: TrainingConfig,
    initializer: Callable[[SoftEMLTree, int, int], dict[str, Any]] | None = None,
    *,
    verification_splits: list[DataSplit] | None = None,
    tolerance: float = 1e-8,
) -> FitResult:
    """Fit a soft EML tree and retain a verifier-rankable exact-candidate pool."""

    target_tensor = as_complex_tensor(target)
    tensor_inputs = {name: as_complex_tensor(value) for name, value in inputs.items()}

    best: tuple[float, dict[str, Any]] | None = None
    restart_logs: list[dict[str, Any]] = []
    candidates: list[ExactCandidate] = []

    initial_operator = _operator_for_step(config, 0, max(config.steps, 1))
    scaffold_plan = resolve_scaffold_plan(config.scaffold_initializers, initial_operator)
    effective_config = replace(config, scaffold_initializers=scaffold_plan.enabled)
    attempts = _training_attempts(effective_config, initializer is not None)

    for attempt_index, attempt in enumerate(attempts):
        restart = int(attempt["restart"])
        seed = int(attempt["seed"])
        torch.manual_seed(seed)
        model = SoftEMLTree(
            effective_config.depth,
            effective_config.variables,
            effective_config.constants,
            operator_family=_operator_for_step(effective_config, 0, max(effective_config.steps, 1)),
        )
        model.reset_parameters(seed=seed, scale=0.25)
        if initializer is not None:
            initialization_log = initializer(model, restart, seed)
        elif attempt["kind"].startswith("scaffold_"):
            initialization_log = _apply_scaffold(model, attempt)
        else:
            initialization_log = None
        optimizer = torch.optim.Adam(model.parameters(), lr=effective_config.lr)
        losses: list[float] = []
        final_stats = AnomalyStats()

        for step in range(effective_config.steps):
            temp = _temperature(effective_config, step)
            operator_family = _operator_for_step(effective_config, step, max(effective_config.steps, 1))
            fit_loss, stats = _train_step(
                model,
                optimizer,
                tensor_inputs,
                target_tensor,
                temperature=temp,
                config=effective_config,
                operator_family=operator_family,
            )
            if fit_loss is None:
                break
            losses.append(fit_loss)
            final_stats = stats

        attempt_best_loss = min(losses) if losses else float("inf")
        log = {
            "restart": attempt_index,
            "random_restart": restart if attempt["kind"] == "random" else None,
            "seed": seed,
            "attempt_kind": attempt["kind"],
            "steps_completed": len(losses),
            "hardening_steps_completed": 0,
            "best_fit_loss": attempt_best_loss,
            "final_anomalies": final_stats.as_dict(),
            "initialization": initialization_log,
            "candidate_ids": [],
        }

        legacy_candidate = _emit_candidate(
            model,
            inputs,
            target,
            candidate_id=f"attempt-{attempt_index:03d}-legacy-final-snap",
            attempt_index=attempt_index,
            random_restart=log["random_restart"],
            seed=seed,
            attempt_kind=str(attempt["kind"]),
            source="legacy_final_snap",
            checkpoint_index=None,
            hardening_step=None,
            global_step=max(len(losses) - 1, 0),
            temperature=_temperature(effective_config, max(len(losses) - 1, 0)),
            best_fit_loss=attempt_best_loss,
        )
        candidates.append(legacy_candidate)
        log["candidate_ids"].append(legacy_candidate.candidate_id)

        hardening_completed = 0
        checkpoint_index = 0
        model.set_operator(_final_operator(effective_config))
        for hardening_step in range(effective_config.hardening_steps):
            temp = _hardening_temperature(effective_config, hardening_step)
            fit_loss, stats = _train_step(
                model,
                optimizer,
                tensor_inputs,
                target_tensor,
                temperature=temp,
                config=effective_config,
                operator_family=_final_operator(effective_config),
            )
            if fit_loss is None:
                break
            hardening_completed = hardening_step + 1
            final_stats = stats
            if _should_emit_hardening_candidate(effective_config, hardening_step):
                candidate = _emit_candidate(
                    model,
                    inputs,
                    target,
                    candidate_id=f"attempt-{attempt_index:03d}-hardening-{checkpoint_index:02d}",
                    attempt_index=attempt_index,
                    random_restart=log["random_restart"],
                    seed=seed,
                    attempt_kind=str(attempt["kind"]),
                    source="hardening_checkpoint",
                    checkpoint_index=checkpoint_index,
                    hardening_step=hardening_step,
                    global_step=effective_config.steps + hardening_step,
                    temperature=temp,
                    best_fit_loss=attempt_best_loss,
                )
                candidates.append(candidate)
                log["candidate_ids"].append(candidate.candidate_id)
                checkpoint_index += 1

        log["hardening_steps_completed"] = hardening_completed
        log["final_anomalies"] = final_stats.as_dict()
        log["legacy_candidate_id"] = legacy_candidate.candidate_id
        restart_logs.append(log)

        if best is None or attempt_best_loss < best[0]:
            best = (attempt_best_loss, log)

    if best is None or not candidates:
        raise RuntimeError("No optimization restart completed")

    legacy_best_loss, best_log = best
    ranked_candidates, selection_mode = _select_exact_candidate(
        candidates,
        verification_splits=verification_splits,
        tolerance=tolerance,
    )
    selected_candidate = ranked_candidates[0]
    fallback_candidate = next(
        candidate
        for candidate in ranked_candidates
        if candidate.candidate_id == str(best_log["legacy_candidate_id"])
    )
    status = "snapped_candidate" if np.isfinite(selected_candidate.post_snap_loss) else "failed"
    manifest = {
        "schema": "eml.run_manifest.v1",
        "config": _training_config_payload(effective_config),
        "operator_trace": _operator_trace(effective_config),
        "scaffold_exclusions": list(scaffold_plan.exclusions),
        "scaffold_witness_operator": initial_operator.as_dict(),
        "best_restart": best_log,
        "restarts": restart_logs,
        "candidates": [candidate.as_dict() for candidate in ranked_candidates],
        "selection": {
            "mode": selection_mode,
            "candidate_count": len(candidates),
            "selected_candidate_id": selected_candidate.candidate_id,
            "fallback_candidate_id": fallback_candidate.candidate_id,
            "selected_attempt_index": selected_candidate.attempt_index,
            "selected_source": selected_candidate.source,
            "fallback_attempt_index": fallback_candidate.attempt_index,
            "fallback_source": fallback_candidate.source,
        },
        "selected_candidate": selected_candidate.as_dict(),
        "fallback_candidate": fallback_candidate.as_dict(),
        "snap": selected_candidate.snap.as_dict(),
        "best_loss": selected_candidate.best_fit_loss,
        "legacy_best_loss": legacy_best_loss,
        "post_snap_loss": selected_candidate.post_snap_loss,
        "status": status,
    }
    return FitResult(
        status=status,
        best_loss=selected_candidate.best_fit_loss,
        post_snap_loss=selected_candidate.post_snap_loss,
        snap=selected_candidate.snap,
        manifest=manifest,
        verification=selected_candidate.verification,
        selected_candidate=selected_candidate,
        fallback_candidate=fallback_candidate,
        candidates=tuple(ranked_candidates),
    )


def _training_attempts(config: TrainingConfig, has_external_initializer: bool) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    if not has_external_initializer:
        known_scaffolds = set(known_scaffold_kinds())
        for scaffold in config.scaffold_initializers:
            if scaffold not in known_scaffolds:
                continue
            if scaffold == "log" and config.depth < 3:
                continue
            if scaffold == "scaled_exp" and config.depth < 9:
                continue
            for variable in config.variables:
                if scaffold == "scaled_exp":
                    for coefficient in _scaled_exp_constants(config.constants):
                        attempts.append(
                            {
                                "kind": "scaffold_scaled_exp",
                                "variable": variable,
                                "coefficient": coefficient,
                                "restart": -1,
                                "seed": config.seed,
                            }
                        )
                else:
                    attempts.append(
                        {
                            "kind": f"scaffold_{scaffold}",
                            "variable": variable,
                            "restart": -1,
                            "seed": config.seed,
                        }
                    )
    for restart in range(config.restarts):
        attempts.append(
            {
                "kind": "random",
                "variable": None,
                "restart": restart,
                "seed": config.seed + restart,
            }
        )
    return attempts


def _operator_for_step(config: TrainingConfig, step: int, total_steps: int) -> EmlOperator:
    if not config.operator_schedule:
        return config.operator_family
    if total_steps <= 1:
        return config.operator_schedule[-1]
    bucket = int((max(step, 0) * len(config.operator_schedule)) / total_steps)
    return config.operator_schedule[min(bucket, len(config.operator_schedule) - 1)]


def _final_operator(config: TrainingConfig) -> EmlOperator:
    return config.operator_schedule[-1] if config.operator_schedule else config.operator_family


def _training_config_payload(config: TrainingConfig) -> dict[str, Any]:
    payload = {
        key: value
        for key, value in config.__dict__.items()
        if key not in {"operator_family", "operator_schedule", "constants"}
    }
    payload["scaffold_initializers"] = list(config.scaffold_initializers)
    payload["constants"] = [format_constant_value(value) for value in config.constants]
    payload.update(config.operator_payload())
    return payload


def _operator_trace(config: TrainingConfig) -> list[dict[str, Any]]:
    if not config.operator_schedule:
        trace = [
            {
                "phase": "training",
                "start_step": 0,
                "end_step": max(config.steps - 1, 0),
                "operator": config.operator_family.as_dict(),
            }
        ]
    else:
        trace = []
        schedule = list(config.operator_schedule)
        total_steps = max(config.steps, 1)
        for index, operator in enumerate(schedule):
            start = int((index * total_steps) / len(schedule))
            end = int(((index + 1) * total_steps) / len(schedule)) - 1
            trace.append(
                {
                    "phase": "training",
                    "schedule_index": index,
                    "start_step": start,
                    "end_step": max(start, end),
                    "operator": operator.as_dict(),
                }
            )
    if config.hardening_steps > 0:
        trace.append(
            {
                "phase": "hardening",
                "start_step": config.steps,
                "end_step": config.steps + config.hardening_steps - 1,
                "operator": _final_operator(config).as_dict(),
            }
        )
    return trace


def _scaled_exp_constants(constants: tuple[complex, ...]) -> tuple[complex, ...]:
    result: list[complex] = []
    for value in constants:
        coefficient = complex(value)
        if not (np.isfinite(coefficient.real) and np.isfinite(coefficient.imag)):
            continue
        if abs(coefficient - 1.0) <= 1e-12:
            continue
        result.append(coefficient)
    return tuple(result)


def _apply_scaffold(model: SoftEMLTree, attempt: Mapping[str, Any]) -> dict[str, Any]:
    kind = str(attempt["kind"])
    variable = str(attempt["variable"])
    scaffold_kind = kind.removeprefix("scaffold_")
    if scaffold_witness_for(scaffold_kind, model.operator_family) is None:
        raise ValueError(f"{scaffold_kind}:{CENTERED_FAMILY_SAME_FAMILY_WITNESS_MISSING}")
    if kind == "scaffold_exp":
        model.force_exp(variable)
    elif kind == "scaffold_log":
        model.force_log(variable)
    elif kind == "scaffold_scaled_exp":
        coefficient = complex(attempt["coefficient"])
        embedding = model.force_scaled_exp(variable, coefficient)
        return {
            "kind": kind,
            "variable": variable,
            "coefficient": format_constant_value(coefficient),
            "constant_label": constant_label(coefficient),
            "seed": attempt["seed"],
            "strategy": "paper_scaled_exponential_family",
            "embedding": embedding.as_dict(),
        }
    else:
        raise ValueError(f"unknown scaffold initializer {kind!r}")
    return {
        "kind": kind,
        "variable": variable,
        "seed": attempt["seed"],
        "strategy": "generic_paper_primitive",
    }
