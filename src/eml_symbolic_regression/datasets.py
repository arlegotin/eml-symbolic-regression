"""Demo datasets based on sources/FOR_DEMO.md."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Callable

import numpy as np
import sympy as sp

from .expression import Candidate, SympyCandidate, exp_expr, log_expr
from .verify import DataSplit

ArrayFn = Callable[[np.ndarray], np.ndarray]


@dataclass(frozen=True)
class DemoSpec:
    name: str
    variable: str
    description: str
    target: ArrayFn
    candidate: Candidate
    train_domain: tuple[float, float]
    heldout_domain: tuple[float, float]
    extrap_domain: tuple[float, float]
    source_document: str
    source_linkage: str
    normalized_dimensionless: bool

    def make_splits(self, *, points: int = 80, seed: int = 0) -> list[DataSplit]:
        rng = np.random.default_rng(seed)

        def sample(domain: tuple[float, float], count: int) -> np.ndarray:
            low, high = domain
            values = np.linspace(low, high, count)
            jitter = (high - low) * 0.002 * rng.standard_normal(count)
            return np.sort(values + jitter).astype(np.float64)

        train_x = sample(self.train_domain, points)
        heldout_x = sample(self.heldout_domain, max(16, points // 2))
        extrap_x = sample(self.extrap_domain, max(16, points // 2))
        target_hp = lambda context: self.candidate.evaluate_mpmath(context)
        return [
            DataSplit("train", {self.variable: train_x}, self.target(train_x), target_hp),
            DataSplit("heldout", {self.variable: heldout_x}, self.target(heldout_x), target_hp),
            DataSplit("extrapolation", {self.variable: extrap_x}, self.target(extrap_x), target_hp),
        ]

    def formula_provenance(self) -> dict[str, Any]:
        candidate_name = getattr(self.candidate, "name", getattr(self.candidate, "candidate_kind", type(self.candidate).__name__))
        return {
            "formula_id": self.name,
            "variable": self.variable,
            "description": self.description,
            "symbolic_expression": sp.sstr(self.candidate.to_sympy()),
            "candidate_name": str(candidate_name),
            "source_document": self.source_document,
            "source_linkage": self.source_linkage,
            "normalized_dimensionless": self.normalized_dimensionless,
        }


def _sympy_candidate(expr: sp.Expr, variable: str, name: str) -> SympyCandidate:
    return SympyCandidate(expr, (variable,), name=name)


def demo_specs() -> dict[str, DemoSpec]:
    x = sp.Symbol("x")
    t = sp.Symbol("t")
    return {
        "exp": DemoSpec(
            name="exp",
            variable="x",
            description="Paper smoke test: exp(x) = eml(x, 1).",
            target=lambda a: np.exp(a).astype(np.complex128),
            candidate=exp_expr("x"),
            train_domain=(-1.0, 1.0),
            heldout_domain=(-0.8, 0.8),
            extrap_domain=(1.05, 1.5),
            source_document="sources/paper.pdf",
            source_linkage="sources/NORTH_STAR.md paper EML identity smoke test for exp(x)",
            normalized_dimensionless=True,
        ),
        "log": DemoSpec(
            name="log",
            variable="x",
            description="Paper smoke test: ln(x) EML identity on the positive real axis.",
            target=lambda a: np.log(a).astype(np.complex128),
            candidate=log_expr("x"),
            train_domain=(0.25, 3.0),
            heldout_domain=(0.35, 2.75),
            extrap_domain=(3.1, 4.2),
            source_document="sources/paper.pdf",
            source_linkage="sources/NORTH_STAR.md paper EML identity smoke test for ln(x)",
            normalized_dimensionless=True,
        ),
        "beer_lambert": DemoSpec(
            name="beer_lambert",
            variable="x",
            description="High-probability exponential-decay showcase.",
            target=lambda a: np.exp(-0.8 * a).astype(np.complex128),
            candidate=_sympy_candidate(sp.exp(-sp.Float("0.8") * x), "x", "beer_lambert_catalog"),
            train_domain=(0.0, 3.0),
            heldout_domain=(0.15, 2.7),
            extrap_domain=(3.1, 4.5),
            source_document="sources/FOR_DEMO.md",
            source_linkage="Beer-Lambert law high-success-probability sanity check",
            normalized_dimensionless=True,
        ),
        "radioactive_decay": DemoSpec(
            name="radioactive_decay",
            variable="t",
            description="FOR_DEMO-style one-term exponential decay baseline.",
            target=lambda a: np.exp(-0.4 * a).astype(np.complex128),
            candidate=_sympy_candidate(sp.exp(-sp.Float("0.4") * t), "t", "radioactive_decay_catalog"),
            train_domain=(0.0, 5.0),
            heldout_domain=(0.15, 4.7),
            extrap_domain=(5.1, 7.0),
            source_document="sources/FOR_DEMO.md",
            source_linkage="Radioactive decay / Newton cooling smoke-test family",
            normalized_dimensionless=True,
        ),
        "michaelis_menten": DemoSpec(
            name="michaelis_menten",
            variable="x",
            description="Mechanistic biochemistry law from FOR_DEMO.md.",
            target=lambda a: (2.0 * a / (0.5 + a)).astype(np.complex128),
            candidate=_sympy_candidate(2 * x / (sp.Float("0.5") + x), "x", "michaelis_menten_catalog"),
            train_domain=(0.05, 5.0),
            heldout_domain=(0.08, 4.5),
            extrap_domain=(5.1, 7.0),
            source_document="sources/FOR_DEMO.md",
            source_linkage="Michaelis-Menten best showcase set mechanistic biochemistry law",
            normalized_dimensionless=True,
        ),
        "logistic": DemoSpec(
            name="logistic",
            variable="x",
            description="Nonlinear growth progression demo.",
            target=lambda a: (1.0 / (1.0 + 2.0 * np.exp(-1.3 * a))).astype(np.complex128),
            candidate=_sympy_candidate(1 / (1 + 2 * sp.exp(-sp.Float("1.3") * x)), "x", "logistic_catalog"),
            train_domain=(0.0, 5.0),
            heldout_domain=(0.1, 4.8),
            extrap_domain=(5.1, 7.0),
            source_document="sources/FOR_DEMO.md",
            source_linkage="Logistic growth first serious demo after simpler warm-ups",
            normalized_dimensionless=True,
        ),
        "shockley": DemoSpec(
            name="shockley",
            variable="x",
            description="Electronics demo structurally close to exponential-minus-constant behavior.",
            target=lambda a: (0.2 * (np.exp(1.4 * a) - 1.0)).astype(np.complex128),
            candidate=_sympy_candidate(sp.Float("0.2") * (sp.exp(sp.Float("1.4") * x) - 1), "x", "shockley_catalog"),
            train_domain=(0.0, 2.0),
            heldout_domain=(0.05, 1.8),
            extrap_domain=(2.05, 2.5),
            source_document="sources/FOR_DEMO.md",
            source_linkage="Shockley diode equation electronics demo structurally close to exponential-minus-constant behavior",
            normalized_dimensionless=True,
        ),
        "damped_oscillator": DemoSpec(
            name="damped_oscillator",
            variable="t",
            description="Stretch demo: oscillation plus decay.",
            target=lambda a: (np.exp(-0.15 * a) * np.cos(2.5 * a + 0.2)).astype(np.complex128),
            candidate=_sympy_candidate(sp.exp(-sp.Float("0.15") * t) * sp.cos(sp.Float("2.5") * t + sp.Float("0.2")), "t", "damped_oscillator_catalog"),
            train_domain=(0.0, 6.0),
            heldout_domain=(0.05, 5.8),
            extrap_domain=(6.1, 8.0),
            source_document="sources/FOR_DEMO.md",
            source_linkage="Damped harmonic oscillator headline time-series symbolic-recovery demo",
            normalized_dimensionless=True,
        ),
        "planck": DemoSpec(
            name="planck",
            variable="x",
            description="Flagship normalized Planck spectrum from FOR_DEMO.md.",
            target=lambda a: (a**3 / (np.exp(a) - 1.0)).astype(np.complex128),
            candidate=_sympy_candidate(x**3 / (sp.exp(x) - 1), "x", "planck_catalog"),
            train_domain=(0.2, 8.0),
            heldout_domain=(0.25, 7.5),
            extrap_domain=(8.1, 10.0),
            source_document="sources/FOR_DEMO.md",
            source_linkage="Normalized Planck spectrum flagship dimensionless physics demo",
            normalized_dimensionless=True,
        ),
    }


def get_demo(name: str) -> DemoSpec:
    specs = demo_specs()
    try:
        return specs[name]
    except KeyError as exc:
        available = ", ".join(sorted(specs))
        raise KeyError(f"Unknown demo {name!r}. Available: {available}") from exc


def _array_sha256(values: np.ndarray) -> str:
    array = np.ascontiguousarray(values)
    digest = hashlib.sha256()
    digest.update(str(array.dtype).encode("utf-8"))
    digest.update(json.dumps(array.shape, separators=(",", ":")).encode("utf-8"))
    digest.update(array.tobytes())
    return digest.hexdigest()


def proof_dataset_manifest(formula_id: str, *, points: int = 80, seed: int = 0, tolerance: float = 1e-8) -> dict[str, Any]:
    points = int(points)
    tolerance = float(tolerance)
    if points <= 0:
        raise ValueError("points must be positive")
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")

    spec = get_demo(formula_id)
    splits = spec.make_splits(points=points, seed=seed)
    domains = {
        "train": spec.train_domain,
        "heldout": spec.heldout_domain,
        "extrapolation": spec.extrap_domain,
    }
    split_metadata: list[dict[str, Any]] = []
    for split in splits:
        inputs = split.inputs[spec.variable]
        split_metadata.append(
            {
                "name": split.name,
                "domain": [float(value) for value in domains[split.name]],
                "count": int(len(inputs)),
                "input_sha256": _array_sha256(inputs),
                "target_sha256": _array_sha256(split.target),
            }
        )

    manifest: dict[str, Any] = {
        "schema": "eml.proof_dataset_manifest.v1",
        "formula_id": spec.name,
        "variable": spec.variable,
        "seed": int(seed),
        "points": points,
        "tolerance": tolerance,
        "sample_policy": "linspace_with_seeded_0.2_percent_jitter",
        "splits": split_metadata,
        "provenance": spec.formula_provenance(),
    }
    encoded = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {**manifest, "manifest_sha256": hashlib.sha256(encoded).hexdigest()}
