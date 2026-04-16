"""Canonical and training-mode EML semantics."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
import torch


@dataclass(frozen=True)
class EmlOperator:
    """Operator-family metadata for raw and centered EML nodes."""

    family: str = "raw_eml"
    s: float = 1.0
    t: complex = 1.0 + 0.0j
    terminal: str = "one"

    def __post_init__(self) -> None:
        family = str(self.family)
        if family not in {"raw_eml", "ceml_s_t", "ceml_s", "zeml_s"}:
            raise ValueError(f"unknown EML operator family: {family!r}")
        s = float(self.s)
        if not np.isfinite(s) or s <= 0:
            raise ValueError("centered EML scale s must be finite and positive")
        t = complex(self.t)
        if not (np.isfinite(t.real) and np.isfinite(t.imag)):
            raise ValueError("centered EML shift t must be finite")
        terminal = str(self.terminal)
        if family == "raw_eml":
            s = 1.0
            t = 1.0 + 0.0j
            terminal = "one"
        elif family == "ceml_s":
            t = 1.0 + 0.0j
            terminal = "one"
        elif family == "zeml_s":
            t = 0.0 + 0.0j
            terminal = "zero"
        else:
            terminal = terminal or "shifted"
        object.__setattr__(self, "family", family)
        object.__setattr__(self, "s", s)
        object.__setattr__(self, "t", t)
        object.__setattr__(self, "terminal", terminal)

    @property
    def is_raw(self) -> bool:
        return self.family == "raw_eml"

    @property
    def label(self) -> str:
        if self.family == "raw_eml":
            return "raw_eml"
        if self.family == "ceml_s":
            return f"CEML_{_format_number(self.s)}"
        if self.family == "zeml_s":
            return f"ZEML_{_format_number(self.s)}"
        return f"cEML_s{_format_number(self.s)}_t{_format_complex(self.t)}"

    @property
    def singularity(self) -> complex:
        return self.t - self.s

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "family": self.family,
            "label": self.label,
            "s": self.s,
            "terminal": self.terminal,
        }
        if self.t.imag:
            payload["t"] = {"real": repr(float(self.t.real)), "imag": repr(float(self.t.imag))}
        else:
            payload["t"] = float(self.t.real)
        if not self.is_raw:
            payload["singularity"] = (
                {"real": repr(float(self.singularity.real)), "imag": repr(float(self.singularity.imag))}
                if self.singularity.imag
                else float(self.singularity.real)
            )
        return payload

    @classmethod
    def from_mapping(cls, payload: dict[str, Any] | None) -> "EmlOperator":
        if payload is None:
            return raw_eml_operator()
        t_payload = payload.get("t", 1.0)
        if isinstance(t_payload, dict):
            t = complex(float(t_payload["real"]), float(t_payload["imag"]))
        else:
            t = complex(float(t_payload), 0.0)
        return cls(
            family=str(payload.get("family", payload.get("name", "raw_eml"))),
            s=float(payload.get("s", 1.0)),
            t=t,
            terminal=str(payload.get("terminal", "")),
        )


def _format_number(value: float) -> str:
    value = float(value)
    return str(int(value)) if value.is_integer() else repr(value)


def _format_complex(value: complex) -> str:
    value = complex(value)
    if abs(value.imag) < 1e-15:
        return _format_number(value.real)
    return repr(value)


def raw_eml_operator() -> EmlOperator:
    return EmlOperator("raw_eml")


def ceml_operator(s: float, t: complex = 1.0 + 0.0j) -> EmlOperator:
    return EmlOperator("ceml_s_t", s=s, t=t, terminal="shifted")


def ceml_s_operator(s: float) -> EmlOperator:
    return EmlOperator("ceml_s", s=s)


def zeml_s_operator(s: float) -> EmlOperator:
    return EmlOperator("zeml_s", s=s)


@dataclass
class TrainingSemanticsConfig:
    """Training-only numerical controls that leave verification semantics unchanged."""

    clamp_exp_real: float = 40.0
    log_domain_epsilon: float = 1e-9
    log_safety_weight: float = 0.0
    log_safety_margin: float = 1e-6
    log_safety_imag_tolerance: float = 1e-6


@dataclass
class AnomalyStats:
    """Small diagnostic bundle for one or more EML evaluations."""

    nan_count: int = 0
    inf_count: int = 0
    clamp_count: int = 0
    max_abs: float = 0.0
    max_exp_real: float = 0.0
    exp_overflow_count: int = 0
    log_small_magnitude_count: int = 0
    log_non_positive_real_count: int = 0
    log_branch_cut_count: int = 0
    log_non_finite_input_count: int = 0
    expm1_overflow_count: int = 0
    log1p_branch_cut_count: int = 0
    shifted_singularity_near_count: int = 0
    shifted_singularity_min_distance: float | None = None
    log_safety_penalty: float = 0.0
    by_node: dict[str, dict[str, float | int]] = field(default_factory=dict)
    _training_penalty: torch.Tensor | None = field(default=None, init=False, repr=False, compare=False)

    def update_torch(
        self,
        value: torch.Tensor,
        exp_arg: torch.Tensor | None = None,
        log_arg: torch.Tensor | None = None,
        node: str | None = None,
        clamp_count: int = 0,
        exp_overflow_count: int = 0,
        log_small_magnitude_count: int = 0,
        log_non_positive_real_count: int = 0,
        log_branch_cut_count: int = 0,
        log_non_finite_input_count: int = 0,
        expm1_overflow_count: int = 0,
        log1p_branch_cut_count: int = 0,
        shifted_singularity_near_count: int = 0,
        shifted_singularity_min_distance: float | None = None,
        log_safety_penalty: torch.Tensor | None = None,
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
        self.exp_overflow_count += exp_overflow_count
        self.log_small_magnitude_count += log_small_magnitude_count
        self.log_non_positive_real_count += log_non_positive_real_count
        self.log_branch_cut_count += log_branch_cut_count
        self.log_non_finite_input_count += log_non_finite_input_count
        self.expm1_overflow_count += expm1_overflow_count
        self.log1p_branch_cut_count += log1p_branch_cut_count
        self.shifted_singularity_near_count += shifted_singularity_near_count
        if shifted_singularity_min_distance is not None and np.isfinite(shifted_singularity_min_distance):
            if self.shifted_singularity_min_distance is None:
                self.shifted_singularity_min_distance = float(shifted_singularity_min_distance)
            else:
                self.shifted_singularity_min_distance = min(
                    self.shifted_singularity_min_distance,
                    float(shifted_singularity_min_distance),
                )

        penalty_value = 0.0
        if log_safety_penalty is not None:
            penalty_value = float(log_safety_penalty.detach().item())
            self.log_safety_penalty += penalty_value
            if self._training_penalty is None:
                self._training_penalty = log_safety_penalty
            else:
                self._training_penalty = self._training_penalty + log_safety_penalty

        if node:
            self.by_node[node] = {
                "nan_count": nan_count,
                "inf_count": inf_count,
                "clamp_count": clamp_count,
                "max_abs": max_abs,
                "max_exp_real": max_exp_real,
                "exp_overflow_count": exp_overflow_count,
                "log_small_magnitude_count": log_small_magnitude_count,
                "log_non_positive_real_count": log_non_positive_real_count,
                "log_branch_cut_count": log_branch_cut_count,
                "log_non_finite_input_count": log_non_finite_input_count,
                "expm1_overflow_count": expm1_overflow_count,
                "log1p_branch_cut_count": log1p_branch_cut_count,
                "shifted_singularity_near_count": shifted_singularity_near_count,
                "shifted_singularity_min_distance": shifted_singularity_min_distance,
                "log_safety_penalty": penalty_value,
            }

    def as_dict(self) -> dict[str, Any]:
        return {
            "nan_count": self.nan_count,
            "inf_count": self.inf_count,
            "clamp_count": self.clamp_count,
            "max_abs": self.max_abs,
            "max_exp_real": self.max_exp_real,
            "exp_overflow_count": self.exp_overflow_count,
            "log_small_magnitude_count": self.log_small_magnitude_count,
            "log_non_positive_real_count": self.log_non_positive_real_count,
            "log_branch_cut_count": self.log_branch_cut_count,
            "log_non_finite_input_count": self.log_non_finite_input_count,
            "expm1_overflow_count": self.expm1_overflow_count,
            "log1p_branch_cut_count": self.log1p_branch_cut_count,
            "shifted_singularity_near_count": self.shifted_singularity_near_count,
            "shifted_singularity_min_distance": self.shifted_singularity_min_distance,
            "log_safety_penalty": self.log_safety_penalty,
            "by_node": self.by_node,
        }

    def training_penalty(self, *, device: torch.device | None = None) -> torch.Tensor:
        if self._training_penalty is None:
            return torch.zeros((), dtype=torch.float64, device=device)
        return self._training_penalty.to(device=device) if device is not None else self._training_penalty


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
    semantics: TrainingSemanticsConfig | None = None,
    stats: AnomalyStats | None = None,
    node: str | None = None,
) -> torch.Tensor:
    """Evaluate EML in PyTorch.

    Training mode clamps only the real part entering exp. Verification
    should call this with training=False.
    """

    x = as_complex_tensor(x)
    y = as_complex_tensor(y, device=x.device)
    semantics = semantics or TrainingSemanticsConfig(clamp_exp_real=clamp_exp_real)
    exp_arg = x
    clamp_count = 0
    exp_overflow_count = 0

    if training:
        real = torch.clamp(x.real, min=-semantics.clamp_exp_real, max=semantics.clamp_exp_real)
        clamp_count = int((real != x.real).sum().detach().item())
        exp_overflow_count = int((x.detach().real > semantics.clamp_exp_real).sum().item())
        exp_arg = torch.complex(real, x.imag)
    else:
        exp_overflow_threshold = float(np.log(np.finfo(np.float64).max))
        exp_overflow_count = int((x.detach().real > exp_overflow_threshold).sum().item())

    log_arg = y.detach()
    log_abs = torch.nan_to_num(torch.abs(log_arg), nan=float("inf"), posinf=float("inf"), neginf=float("inf"))
    log_small_magnitude_count = int((log_abs < semantics.log_domain_epsilon).sum().item())
    log_non_positive_real_count = int((log_arg.real <= 0).sum().item())
    log_branch_cut_count = int(
        ((torch.abs(log_arg.imag) <= semantics.log_domain_epsilon) & (log_arg.real <= 0)).sum().item()
    )
    log_non_finite_input_count = int(
        torch.isnan(log_arg.real).sum().item()
        + torch.isnan(log_arg.imag).sum().item()
        + torch.isinf(log_arg.real).sum().item()
        + torch.isinf(log_arg.imag).sum().item()
    )

    log_safety_penalty = None
    if training and semantics.log_safety_weight > 0:
        safe_margin = max(float(semantics.log_safety_margin), float(semantics.log_domain_epsilon))
        imag_tolerance = max(float(semantics.log_safety_imag_tolerance), float(semantics.log_domain_epsilon))
        real_pressure = torch.relu(safe_margin - y.real)
        axis_proximity = torch.relu(imag_tolerance - torch.abs(y.imag)) / imag_tolerance
        magnitude_pressure = torch.relu(safe_margin - torch.abs(y))
        log_safety_penalty = semantics.log_safety_weight * torch.mean(real_pressure * axis_proximity + magnitude_pressure)

    out = torch.exp(exp_arg) - torch.log(y)
    if stats is not None:
        stats.update_torch(
            out,
            exp_arg=exp_arg,
            log_arg=log_arg,
            node=node,
            clamp_count=clamp_count,
            exp_overflow_count=exp_overflow_count,
            log_small_magnitude_count=log_small_magnitude_count,
            log_non_positive_real_count=log_non_positive_real_count,
            log_branch_cut_count=log_branch_cut_count,
            log_non_finite_input_count=log_non_finite_input_count,
            log_safety_penalty=log_safety_penalty,
        )
    return out


def centered_eml_torch(
    x: torch.Tensor,
    y: torch.Tensor,
    *,
    operator: EmlOperator,
    training: bool = False,
    clamp_exp_real: float = 40.0,
    semantics: TrainingSemanticsConfig | None = None,
    stats: AnomalyStats | None = None,
    node: str | None = None,
) -> torch.Tensor:
    """Evaluate centered/scaled EML in PyTorch using expm1/log1p coordinates."""

    if operator.is_raw:
        return eml_torch(
            x,
            y,
            training=training,
            clamp_exp_real=clamp_exp_real,
            semantics=semantics,
            stats=stats,
            node=node,
        )

    x = as_complex_tensor(x)
    y = as_complex_tensor(y, device=x.device)
    semantics = semantics or TrainingSemanticsConfig(clamp_exp_real=clamp_exp_real)
    s_real = torch.tensor(operator.s, dtype=torch.float64, device=x.device)
    s = torch.complex(s_real, torch.zeros_like(s_real))
    t = torch.tensor(operator.t, dtype=torch.complex128, device=x.device)

    exp_arg = x / s
    clamp_count = 0
    expm1_overflow_count = 0
    if training:
        real = torch.clamp(exp_arg.real, min=-semantics.clamp_exp_real, max=semantics.clamp_exp_real)
        clamp_count = int((real != exp_arg.real).sum().detach().item())
        expm1_overflow_count = int((exp_arg.detach().real > semantics.clamp_exp_real).sum().item())
        exp_arg = torch.complex(real, exp_arg.imag)
    else:
        exp_overflow_threshold = float(np.log(np.finfo(np.float64).max))
        expm1_overflow_count = int((exp_arg.detach().real > exp_overflow_threshold).sum().item())

    log1p_input = (y - t) / s
    log_arg = 1.0 + log1p_input.detach()
    log_abs = torch.nan_to_num(torch.abs(log_arg), nan=float("inf"), posinf=float("inf"), neginf=float("inf"))
    log_small_magnitude_count = int((log_abs < semantics.log_domain_epsilon).sum().item())
    log_non_positive_real_count = int((log_arg.real <= 0).sum().item())
    log_branch_cut_count = int(
        ((torch.abs(log_arg.imag) <= semantics.log_domain_epsilon) & (log_arg.real <= 0)).sum().item()
    )
    log_non_finite_input_count = int(
        torch.isnan(log_arg.real).sum().item()
        + torch.isnan(log_arg.imag).sum().item()
        + torch.isinf(log_arg.real).sum().item()
        + torch.isinf(log_arg.imag).sum().item()
    )
    singularity = t - s
    shifted_distance = torch.nan_to_num(torch.abs(y.detach() - singularity), nan=float("inf"), posinf=float("inf"), neginf=float("inf"))
    shifted_singularity_near_count = int((shifted_distance < semantics.log_domain_epsilon).sum().item())
    shifted_singularity_min_distance = float(shifted_distance.min().item()) if shifted_distance.numel() else None

    log_safety_penalty = None
    if training and semantics.log_safety_weight > 0:
        safe_margin = max(float(semantics.log_safety_margin), float(semantics.log_domain_epsilon))
        imag_tolerance = max(float(semantics.log_safety_imag_tolerance), float(semantics.log_domain_epsilon))
        real_pressure = torch.relu(safe_margin - log_arg.real)
        axis_proximity = torch.relu(imag_tolerance - torch.abs(log_arg.imag)) / imag_tolerance
        magnitude_pressure = torch.relu(safe_margin - torch.abs(log_arg))
        log_safety_penalty = semantics.log_safety_weight * torch.mean(real_pressure * axis_proximity + magnitude_pressure)

    out = s * torch.expm1(exp_arg) - s * torch.log1p(log1p_input)
    if stats is not None:
        stats.update_torch(
            out,
            exp_arg=exp_arg,
            log_arg=log_arg,
            node=node,
            clamp_count=clamp_count,
            expm1_overflow_count=expm1_overflow_count,
            log_small_magnitude_count=log_small_magnitude_count,
            log_non_positive_real_count=log_non_positive_real_count,
            log_branch_cut_count=log_branch_cut_count,
            log1p_branch_cut_count=log_branch_cut_count,
            log_non_finite_input_count=log_non_finite_input_count,
            shifted_singularity_near_count=shifted_singularity_near_count,
            shifted_singularity_min_distance=shifted_singularity_min_distance,
            log_safety_penalty=log_safety_penalty,
        )
    return out


def eml_numpy(x: Any, y: Any) -> np.ndarray:
    """Evaluate canonical EML with NumPy complex128 arrays."""

    x_arr = np.asarray(x, dtype=np.complex128)
    y_arr = np.asarray(y, dtype=np.complex128)
    return np.exp(x_arr) - np.log(y_arr)


def centered_eml_numpy(x: Any, y: Any, *, operator: EmlOperator) -> np.ndarray:
    """Evaluate centered/scaled EML with NumPy complex128 arrays."""

    if operator.is_raw:
        return eml_numpy(x, y)
    x_arr = np.asarray(x, dtype=np.complex128)
    y_arr = np.asarray(y, dtype=np.complex128)
    s = np.complex128(operator.s)
    t = np.complex128(operator.t)
    return s * np.expm1(x_arr / s) - s * np.log1p((y_arr - t) / s)


def mse_complex_numpy(a: Any, b: Any) -> float:
    """Mean squared complex residual."""

    a_arr = np.asarray(a, dtype=np.complex128)
    b_arr = np.asarray(b, dtype=np.complex128)
    return float(np.mean(np.abs(a_arr - b_arr) ** 2))
