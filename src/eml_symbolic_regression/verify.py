"""Verifier-owned recovery status and numeric checks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

import mpmath as mp
import numpy as np

from .expression import Candidate


@dataclass(frozen=True)
class DataSplit:
    name: str
    inputs: dict[str, np.ndarray]
    target: np.ndarray
    target_mpmath: Callable[[Mapping[str, Any]], mp.mpc] | None = None

    def sample_mpmath_contexts(self, limit: int = 8) -> list[dict[str, Any]]:
        count = min(limit, len(next(iter(self.inputs.values()))))
        indices = np.linspace(0, len(next(iter(self.inputs.values()))) - 1, count, dtype=int)
        contexts: list[dict[str, Any]] = []
        for index in indices:
            contexts.append({name: values[index] for name, values in self.inputs.items()})
        return contexts


@dataclass(frozen=True)
class SplitResult:
    name: str
    max_abs_error: float
    mse: float
    max_imag_residue: float
    passed: bool


@dataclass(frozen=True)
class VerificationReport:
    status: str
    candidate_kind: str
    reason: str
    split_results: list[SplitResult]
    high_precision_max_error: float
    tolerance: float
    high_precision_status: str = "performed"

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "candidate_kind": self.candidate_kind,
            "reason": self.reason,
            "tolerance": self.tolerance,
            "high_precision_max_error": self.high_precision_max_error,
            "high_precision_status": self.high_precision_status,
            "split_results": [result.__dict__ for result in self.split_results],
        }


def _target_scalar_from_split(split: DataSplit, context: Mapping[str, Any]) -> complex | mp.mpc:
    if split.target_mpmath is not None:
        return split.target_mpmath(context)
    first_key = next(iter(split.inputs))
    values = split.inputs[first_key]
    matches = np.where(values == context[first_key])[0]
    if len(matches) == 0:
        raise ValueError("Could not find context in split")
    return complex(split.target[int(matches[0])])


def verify_candidate(
    candidate: Candidate,
    splits: list[DataSplit],
    *,
    tolerance: float = 1e-8,
    high_precision_points: int = 8,
    high_precision_skip_factor: float = 1e6,
    recovered_requires_exact_eml: bool = True,
) -> VerificationReport:
    """Verify a candidate over numeric splits and mpmath point checks."""

    split_results: list[SplitResult] = []
    all_passed = True
    hp_max = 0.0
    high_precision_status = "performed"

    for split in splits:
        pred = candidate.evaluate_numpy(split.inputs)
        target = np.asarray(split.target, dtype=np.complex128)
        residual = pred - target
        max_abs = float(np.max(np.abs(residual)))
        mse = float(np.mean(np.abs(residual) ** 2))
        max_imag = float(np.max(np.abs(np.imag(pred)))) if pred.size else 0.0
        passed = bool(max_abs <= tolerance)
        all_passed = all_passed and passed
        split_results.append(SplitResult(split.name, max_abs, mse, max_imag, passed))
        numeric_failure_is_nonfinite = not np.isfinite(max_abs)
        numeric_failure_is_decisive = (not passed) and (numeric_failure_is_nonfinite or max_abs > tolerance * high_precision_skip_factor)
        if numeric_failure_is_decisive:
            high_precision_status = "skipped_numeric_failure"
            hp_max = float("inf") if numeric_failure_is_nonfinite else max(hp_max, max_abs)
            continue

        for context in split.sample_mpmath_contexts(high_precision_points):
            mp.mp.dps = 80
            pred_hp = candidate.evaluate_mpmath(context)
            target_hp = mp.mpc(_target_scalar_from_split(split, context))
            hp_max = max(hp_max, float(abs(pred_hp - target_hp)))

    hp_passed = hp_max <= tolerance
    all_passed = all_passed and hp_passed
    candidate_kind = getattr(candidate, "candidate_kind", "unknown")

    if all_passed and (candidate_kind == "exact_eml" or not recovered_requires_exact_eml):
        status = "recovered"
        reason = "verified"
    elif all_passed:
        status = "verified_showcase"
        reason = "verified_non_eml_candidate"
    elif not hp_passed and high_precision_status != "skipped_numeric_failure":
        status = "failed"
        reason = "mpmath_failed"
    else:
        failed = next((result.name for result in split_results if not result.passed), "unknown")
        status = "failed"
        reason = f"{failed}_failed"

    return VerificationReport(
        status=status,
        candidate_kind=candidate_kind,
        reason=reason,
        split_results=split_results,
        high_precision_max_error=hp_max,
        tolerance=tolerance,
        high_precision_status=high_precision_status,
    )
