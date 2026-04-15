"""Exact EML expression trees and candidate formulas."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol

import mpmath as mp
import numpy as np
import sympy as sp
import torch

from .semantics import eml_numpy, eml_torch

AST_SCHEMA = "eml.ast.v1"


def format_constant_value(value: complex) -> str | dict[str, str]:
    """Return a stable JSON representation for a scalar constant."""

    value = complex(value)
    if abs(value.imag) < 1e-15:
        real = float(value.real)
        return str(int(real)) if real.is_integer() else repr(real)
    return {"real": repr(float(value.real)), "imag": repr(float(value.imag))}


def parse_constant_value(value: str | float | int | Mapping[str, Any]) -> complex:
    if isinstance(value, Mapping):
        return complex(float(value["real"]), float(value["imag"]))
    return complex(float(value))


class Candidate(Protocol):
    candidate_kind: str

    def evaluate_numpy(self, context: Mapping[str, Any]) -> np.ndarray:
        ...

    def evaluate_mpmath(self, context: Mapping[str, Any]) -> mp.mpc:
        ...

    def to_sympy(self) -> sp.Expr:
        ...


class Expr:
    """Base class for exact EML AST nodes."""

    candidate_kind = "exact_eml"

    def evaluate_numpy(self, context: Mapping[str, Any]) -> np.ndarray:
        raise NotImplementedError

    def evaluate_torch(self, context: Mapping[str, torch.Tensor], *, training: bool = False) -> torch.Tensor:
        raise NotImplementedError

    def evaluate_mpmath(self, context: Mapping[str, Any]) -> mp.mpc:
        raise NotImplementedError

    def to_sympy(self) -> sp.Expr:
        raise NotImplementedError

    def to_node(self) -> dict[str, Any]:
        raise NotImplementedError

    def node_count(self) -> int:
        raise NotImplementedError

    def depth(self) -> int:
        raise NotImplementedError

    def to_document(self, variables: list[str] | None = None, **metadata: Any) -> dict[str, Any]:
        constants = sorted(self.constants(), key=lambda value: (value.real, value.imag))
        return {
            "schema": AST_SCHEMA,
            "semantics": {
                "operator": "exp(x)-log(y)",
                "log_branch": "principal",
                "constant_basis": [format_constant_value(value) for value in constants],
                "verification_mode": "canonical",
            },
            "variables": variables or sorted(self.variables()),
            "root": self.to_node(),
            "metadata": {
                "node_count": self.node_count(),
                "depth": self.depth(),
                "source": "exact_ast",
                **metadata,
            },
        }

    def variables(self) -> set[str]:
        raise NotImplementedError

    def constants(self) -> set[complex]:
        raise NotImplementedError


def _constant_like(context: Mapping[str, Any], value: complex) -> np.ndarray:
    if context:
        first = np.asarray(next(iter(context.values())), dtype=np.complex128)
        return np.zeros_like(first, dtype=np.complex128) + np.complex128(value)
    return np.asarray(value, dtype=np.complex128)


def _constant_like_torch(context: Mapping[str, torch.Tensor], value: complex) -> torch.Tensor:
    if context:
        first = next(iter(context.values()))
        return torch.zeros_like(first, dtype=torch.complex128) + complex(value)
    return torch.tensor(value, dtype=torch.complex128)


@dataclass(frozen=True)
class Const(Expr):
    value: complex = 1.0 + 0.0j

    def evaluate_numpy(self, context: Mapping[str, Any]) -> np.ndarray:
        return _constant_like(context, self.value)

    def evaluate_torch(self, context: Mapping[str, torch.Tensor], *, training: bool = False) -> torch.Tensor:
        return _constant_like_torch(context, self.value)

    def evaluate_mpmath(self, context: Mapping[str, Any]) -> mp.mpc:
        return mp.mpc(self.value)

    def to_sympy(self) -> sp.Expr:
        if abs(self.value.imag) < 1e-15:
            return sp.Integer(int(self.value.real)) if self.value.real.is_integer() else sp.Float(self.value.real)
        return sp.Float(self.value.real) + sp.I * sp.Float(self.value.imag)

    def to_node(self) -> dict[str, Any]:
        return {"kind": "const", "value": format_constant_value(self.value)}

    def node_count(self) -> int:
        return 1

    def depth(self) -> int:
        return 0

    def variables(self) -> set[str]:
        return set()

    def constants(self) -> set[complex]:
        return {complex(self.value)}


@dataclass(frozen=True)
class Var(Expr):
    name: str = "x"

    def evaluate_numpy(self, context: Mapping[str, Any]) -> np.ndarray:
        return np.asarray(context[self.name], dtype=np.complex128)

    def evaluate_torch(self, context: Mapping[str, torch.Tensor], *, training: bool = False) -> torch.Tensor:
        return context[self.name].to(dtype=torch.complex128)

    def evaluate_mpmath(self, context: Mapping[str, Any]) -> mp.mpc:
        return mp.mpc(context[self.name])

    def to_sympy(self) -> sp.Expr:
        return sp.Symbol(self.name)

    def to_node(self) -> dict[str, Any]:
        return {"kind": "var", "name": self.name}

    def node_count(self) -> int:
        return 1

    def depth(self) -> int:
        return 0

    def variables(self) -> set[str]:
        return {self.name}

    def constants(self) -> set[complex]:
        return set()


@dataclass(frozen=True)
class Eml(Expr):
    left: Expr
    right: Expr

    def evaluate_numpy(self, context: Mapping[str, Any]) -> np.ndarray:
        return eml_numpy(self.left.evaluate_numpy(context), self.right.evaluate_numpy(context))

    def evaluate_torch(self, context: Mapping[str, torch.Tensor], *, training: bool = False) -> torch.Tensor:
        return eml_torch(
            self.left.evaluate_torch(context, training=training),
            self.right.evaluate_torch(context, training=training),
            training=training,
        )

    def evaluate_mpmath(self, context: Mapping[str, Any]) -> mp.mpc:
        return mp.e ** self.left.evaluate_mpmath(context) - mp.log(self.right.evaluate_mpmath(context))

    def to_sympy(self) -> sp.Expr:
        return sp.exp(self.left.to_sympy()) - sp.log(self.right.to_sympy())

    def to_node(self) -> dict[str, Any]:
        return {"kind": "eml", "left": self.left.to_node(), "right": self.right.to_node()}

    def node_count(self) -> int:
        return 1 + self.left.node_count() + self.right.node_count()

    def depth(self) -> int:
        return 1 + max(self.left.depth(), self.right.depth())

    def variables(self) -> set[str]:
        return self.left.variables() | self.right.variables()

    def constants(self) -> set[complex]:
        return self.left.constants() | self.right.constants()


def expr_from_node(node: Mapping[str, Any]) -> Expr:
    kind = node["kind"]
    if kind == "const":
        value = node.get("value", "1")
        return Const(parse_constant_value(value))
    if kind == "var":
        return Var(str(node["name"]))
    if kind == "eml":
        return Eml(expr_from_node(node["left"]), expr_from_node(node["right"]))
    raise ValueError(f"Unknown AST node kind: {kind}")


def expr_from_document(document: Mapping[str, Any]) -> Expr:
    if document.get("schema") != AST_SCHEMA:
        raise ValueError(f"Unsupported AST schema: {document.get('schema')}")
    return expr_from_node(document["root"])


def exp_expr(variable: str = "x") -> Expr:
    """Paper identity: exp(x) = eml(x, 1)."""

    return Eml(Var(variable), Const(1.0))


def log_expr(variable: str = "x") -> Expr:
    """Paper identity: ln(x) = eml(1, eml(eml(1, x), 1))."""

    return Eml(Const(1.0), Eml(Eml(Const(1.0), Var(variable)), Const(1.0)))


def exp_of(expr: Expr) -> Expr:
    """Generalized paper identity: exp(a) = eml(a, 1)."""

    return Eml(expr, Const(1.0))


def log_of(expr: Expr) -> Expr:
    """Generalized paper identity for principal-branch log(a)."""

    return Eml(Const(1.0), Eml(Eml(Const(1.0), expr), Const(1.0)))


@dataclass(frozen=True)
class SympyCandidate:
    """A non-EML candidate used for honest demo showcase verification."""

    expression: sp.Expr
    variables: tuple[str, ...]
    name: str = "catalog_sympy"
    candidate_kind: str = "catalog_sympy"

    def evaluate_numpy(self, context: Mapping[str, Any]) -> np.ndarray:
        symbols = [sp.Symbol(v) for v in self.variables]
        fn = sp.lambdify(symbols, self.expression, modules="numpy")
        values = [np.asarray(context[v], dtype=np.complex128) for v in self.variables]
        return np.asarray(fn(*values), dtype=np.complex128)

    def evaluate_mpmath(self, context: Mapping[str, Any]) -> mp.mpc:
        symbols = [sp.Symbol(v) for v in self.variables]
        fn = sp.lambdify(symbols, self.expression, modules="mpmath")
        values = [mp.mpc(context[v]) for v in self.variables]
        return mp.mpc(fn(*values))

    def to_sympy(self) -> sp.Expr:
        return self.expression

    def to_document(self) -> dict[str, Any]:
        return {
            "schema": "eml.catalog_candidate.v1",
            "kind": self.candidate_kind,
            "name": self.name,
            "variables": list(self.variables),
            "sympy": str(self.expression),
        }
