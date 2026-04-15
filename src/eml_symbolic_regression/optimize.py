"""PyTorch optimization loop for soft EML trees."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

import numpy as np
import torch

from .master_tree import SnapResult, SoftEMLTree
from .expression import format_constant_value
from .semantics import AnomalyStats, as_complex_tensor, mse_complex_numpy


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
    entropy_weight: float = 1e-3
    size_weight: float = 1e-4
    seed: int = 0


@dataclass(frozen=True)
class FitResult:
    status: str
    best_loss: float
    post_snap_loss: float
    snap: SnapResult
    manifest: dict[str, Any]


def _temperature(config: TrainingConfig, step: int) -> float:
    if config.steps <= 1:
        return config.temperature_end
    frac = step / (config.steps - 1)
    return config.temperature_start + frac * (config.temperature_end - config.temperature_start)


def fit_eml_tree(
    inputs: Mapping[str, Any],
    target: Any,
    config: TrainingConfig,
    initializer: Callable[[SoftEMLTree, int, int], dict[str, Any]] | None = None,
) -> FitResult:
    """Fit a soft EML tree and return the best snapped candidate.

    This is a candidate generator. Verification must be run separately.
    """

    target_tensor = as_complex_tensor(target)
    tensor_inputs = {name: as_complex_tensor(value) for name, value in inputs.items()}

    best: tuple[float, SoftEMLTree, dict[str, Any]] | None = None
    restart_logs: list[dict[str, Any]] = []

    for restart in range(config.restarts):
        seed = config.seed + restart
        torch.manual_seed(seed)
        model = SoftEMLTree(config.depth, config.variables, config.constants)
        model.reset_parameters(seed=seed, scale=0.25)
        initialization_log = initializer(model, restart, seed) if initializer is not None else None
        optimizer = torch.optim.Adam(model.parameters(), lr=config.lr)
        losses: list[float] = []
        final_stats = AnomalyStats()

        for step in range(config.steps):
            optimizer.zero_grad()
            stats = AnomalyStats()
            temp = _temperature(config, step)
            pred = model(tensor_inputs, temperature=temp, training_semantics=True, stats=stats)
            fit_loss = torch.mean(torch.abs(pred - target_tensor) ** 2)
            entropy = model.gate_entropy(temp)
            size = model.expected_child_use(temp)
            loss = fit_loss + config.entropy_weight * entropy + config.size_weight * size
            if not torch.isfinite(loss):
                break
            loss.backward()
            optimizer.step()
            losses.append(float(fit_loss.detach().item()))
            final_stats = stats

        best_loss = min(losses) if losses else float("inf")
        log = {
            "restart": restart,
            "seed": seed,
            "steps_completed": len(losses),
            "best_fit_loss": best_loss,
            "final_anomalies": final_stats.as_dict(),
            "initialization": initialization_log,
        }
        restart_logs.append(log)
        if best is None or best_loss < best[0]:
            best = (best_loss, model, log)

    if best is None:
        raise RuntimeError("No optimization restart completed")

    best_loss, model, best_log = best
    snap = model.snap()
    snapped_pred = snap.expression.evaluate_numpy({k: np.asarray(v) for k, v in inputs.items()})
    post_snap_loss = mse_complex_numpy(snapped_pred, target)
    status = "snapped_candidate" if np.isfinite(post_snap_loss) else "failed"
    manifest = {
        "schema": "eml.run_manifest.v1",
        "config": {**config.__dict__, "constants": [format_constant_value(value) for value in config.constants]},
        "best_restart": best_log,
        "restarts": restart_logs,
        "snap": snap.as_dict(),
        "best_loss": best_loss,
        "post_snap_loss": post_snap_loss,
        "status": status,
    }
    return FitResult(status, best_loss, post_snap_loss, snap, manifest)
