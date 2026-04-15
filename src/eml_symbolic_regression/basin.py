"""Deterministic exact EML targets for perturbed-basin proof runs."""

from __future__ import annotations

from dataclasses import dataclass

from .expression import Const, Eml, Expr, Var


@dataclass(frozen=True)
class BasinTargetSpec:
    id: str
    expression: Expr
    variable: str
    train_domain: tuple[float, float]
    heldout_domain: tuple[float, float]
    extrap_domain: tuple[float, float]
    source_document: str
    source_linkage: str


_X = Var("x")
_ONE = Const(1.0)

_BASIN_TARGETS: tuple[BasinTargetSpec, ...] = (
    BasinTargetSpec(
        id="basin_depth1_exp",
        expression=Eml(_X, _ONE),
        variable="x",
        train_domain=(-1.0, 1.0),
        heldout_domain=(-0.8, 0.8),
        extrap_domain=(1.1, 1.5),
        source_document="sources/NORTH_STAR.md",
        source_linkage="Phase 31 deterministic exact EML basin inventory: depth-1 exp identity",
    ),
    BasinTargetSpec(
        id="basin_depth2_exp_exp",
        expression=Eml(Eml(_X, _ONE), _ONE),
        variable="x",
        train_domain=(-0.8, 0.2),
        heldout_domain=(-0.7, 0.1),
        extrap_domain=(0.3, 0.5),
        source_document="sources/NORTH_STAR.md",
        source_linkage="Phase 31 deterministic exact EML basin inventory: depth-2 nested exp identity",
    ),
    BasinTargetSpec(
        id="basin_depth3_exp_exp_exp",
        expression=Eml(Eml(Eml(_X, _ONE), _ONE), _ONE),
        variable="x",
        train_domain=(-1.0, -0.2),
        heldout_domain=(-0.9, -0.35),
        extrap_domain=(-1.4, -1.1),
        source_document="sources/NORTH_STAR.md",
        source_linkage="Phase 31 deterministic exact EML basin inventory: depth-3 nested exp identity",
    ),
)


def basin_target_specs() -> tuple[BasinTargetSpec, ...]:
    return _BASIN_TARGETS


def basin_target_spec(target_id: str) -> BasinTargetSpec:
    for spec in _BASIN_TARGETS:
        if spec.id == target_id:
            return spec
    available = ", ".join(spec.id for spec in _BASIN_TARGETS)
    raise KeyError(f"Unknown basin target {target_id!r}. Available: {available}")
