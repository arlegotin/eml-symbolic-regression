"""Canonical and training-mode EML semantics."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
import torch


@dataclass
class AnomalyStats:
    """Small diagnostic bundle for one or more EML evaluations."""

    nan_count: int = 0
    inf_count: int = 0
    clamp_count: int = 0
    max_abs: float = 0.0
    max_exp_real: float = 0.0
    by_node: dict[str, dict[str, float | int]] = field(default_factory=dict)

    def update_torch(
        self,
        value: torch.Tensor,
        exp_arg: torch.Tensor | None = None,
        node: str | None = None,
        clamp_count: int = 0,
    ) -> None:
        detached = value.detach()
        finite_abs = torch.nan_to_num(torch.abs(detached), nan=0.0, posinf=0.0, neginf=0.0)
        nan_count = int(torch.isnan(detached.real).sum().item() + torch.isnan(detached.imag).sum().item())
        inf_count = int(torch.isinf(detached.real).sum().item() + torch.isinf(detached.imag).sum().item())
        max_abs = float(finite_abs.max().item()) if finite_abs.numel() else 0.0
        max_exp_real = 0.0
        if exp_arg is not None and exp_arg.numel():
            max_exp_real = float(torch.max(torch.abs(exp_arg.detach().real)).item())

        self.nan_count += nan_count
        self.inf_count += inf_count
        self.clamp_count += clamp_count
        self.max_abs = max(self.max_abs, max_abs)
        self.max_exp_real = max(self.max_exp_real, max_exp_real)

        if node:
            self.by_node[node] = {
                "nan_count": nan_count,
                "inf_count": inf_count,
                "clamp_count": clamp_count,
                "max_abs": max_abs,
                "max_exp_real": max_exp_real,
            }

    def as_dict(self) -> dict[str, Any]:
        return {
            "nan_count": self.nan_count,
            "inf_count": self.inf_count,
            "clamp_count": self.clamp_count,
            "max_abs": self.max_abs,
            "max_exp_real": self.max_exp_real,
            "by_node": self.by_node,
        }


def as_complex_tensor(value: Any, *, device: torch.device | None = None) -> torch.Tensor:
    """Convert input data to torch.complex128."""

    if isinstance(value, torch.Tensor):
        tensor = value.to(dtype=torch.complex128)
        return tensor.to(device=device) if device is not None else tensor
    return torch.as_tensor(value, dtype=torch.complex128, device=device)


def eml_torch(
    x: torch.Tensor,
    y: torch.Tensor,
    *,
    training: bool = False,
    clamp_exp_real: float = 40.0,
    stats: AnomalyStats | None = None,
    node: str | None = None,
) -> torch.Tensor:
    """Evaluate EML in PyTorch.

    Training mode clamps only the real part entering exp. Verification
    should call this with training=False.
    """

    x = as_complex_tensor(x)
    y = as_complex_tensor(y, device=x.device)
    exp_arg = x
    clamp_count = 0

    if training:
        real = torch.clamp(x.real, min=-clamp_exp_real, max=clamp_exp_real)
        clamp_count = int((real != x.real).sum().detach().item())
        exp_arg = torch.complex(real, x.imag)

    out = torch.exp(exp_arg) - torch.log(y)
    if stats is not None:
        stats.update_torch(out, exp_arg=exp_arg, node=node, clamp_count=clamp_count)
    return out


def eml_numpy(x: Any, y: Any) -> np.ndarray:
    """Evaluate canonical EML with NumPy complex128 arrays."""

    x_arr = np.asarray(x, dtype=np.complex128)
    y_arr = np.asarray(y, dtype=np.complex128)
    return np.exp(x_arr) - np.log(y_arr)


def mse_complex_numpy(a: Any, b: Any) -> float:
    """Mean squared complex residual."""

    a_arr = np.asarray(a, dtype=np.complex128)
    b_arr = np.asarray(b, dtype=np.complex128)
    return float(np.mean(np.abs(a_arr - b_arr) ** 2))
