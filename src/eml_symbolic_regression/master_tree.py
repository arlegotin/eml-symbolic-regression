"""Complete depth-bounded differentiable EML master trees."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

import torch

from .expression import Const, Eml, Expr, Var
from .semantics import AnomalyStats, as_complex_tensor, eml_torch


def _canonical_constant(value: complex) -> complex:
    value = complex(value)
    return complex(0.0 if abs(value.real) < 1e-15 else value.real, 0.0 if abs(value.imag) < 1e-15 else value.imag)


def normalize_constants(constants: tuple[complex, ...] = (1.0,)) -> tuple[complex, ...]:
    seen: list[complex] = []
    for value in (1.0, *constants):
        canonical = _canonical_constant(value)
        if not any(abs(canonical - existing) <= 1e-12 for existing in seen):
            seen.append(canonical)
    return tuple(sorted(seen, key=lambda item: (item.real, item.imag)))


def constant_label(value: complex) -> str:
    value = _canonical_constant(value)
    if abs(value.imag) < 1e-15:
        real = float(value.real)
        body = str(int(real)) if real.is_integer() else repr(real)
    else:
        body = repr(complex(value))
    return f"const:{body}"


def parse_constant_label(label: str) -> complex:
    if not label.startswith("const:"):
        raise ValueError(f"Not a constant label: {label}")
    body = label.split(":", 1)[1]
    return _canonical_constant(complex(float(body)) if "j" not in body else complex(body))


def expressions_equal(left: Expr, right: Expr, *, constant_tolerance: float = 1e-12) -> bool:
    if isinstance(left, Const) and isinstance(right, Const):
        return abs(complex(left.value) - complex(right.value)) <= constant_tolerance
    if isinstance(left, Var) and isinstance(right, Var):
        return left.name == right.name
    if isinstance(left, Eml) and isinstance(right, Eml):
        return expressions_equal(left.left, right.left, constant_tolerance=constant_tolerance) and expressions_equal(
            left.right, right.right, constant_tolerance=constant_tolerance
        )
    return False


@dataclass(frozen=True)
class SnapDecision:
    path: str
    side: str
    choice: str
    probability: float
    margin: float


@dataclass(frozen=True)
class SnapResult:
    expression: Expr
    decisions: list[SnapDecision]
    min_margin: float
    active_node_count: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "min_margin": self.min_margin,
            "active_node_count": self.active_node_count,
            "decisions": [decision.__dict__ for decision in self.decisions],
            "ast": self.expression.to_document(),
        }


@dataclass(frozen=True)
class EmbeddingConfig:
    strength: float = 30.0


@dataclass(frozen=True)
class EmbeddingAssignment:
    slot: str
    choice: str

    def as_dict(self) -> dict[str, str]:
        return {"slot": self.slot, "choice": self.choice}


@dataclass(frozen=True)
class EmbeddingResult:
    success: bool
    assignments: tuple[EmbeddingAssignment, ...]
    snap: SnapResult
    round_trip_equal: bool
    diagnostics: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "assignments": [assignment.as_dict() for assignment in self.assignments],
            "snap": self.snap.as_dict(),
            "round_trip_equal": self.round_trip_equal,
            "diagnostics": list(self.diagnostics),
        }


class EmbeddingError(ValueError):
    def __init__(self, reason: str, detail: str) -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason}: {detail}")

    def as_dict(self) -> dict[str, str]:
        return {"reason": self.reason, "detail": self.detail}


class _SoftNode(torch.nn.Module):
    def __init__(
        self,
        depth: int,
        variables: tuple[str, ...],
        constants: tuple[complex, ...],
        path: str = "root",
    ) -> None:
        super().__init__()
        if depth < 1:
            raise ValueError("EML master-node depth must be >= 1")
        self.depth = depth
        self.variables = variables
        self.constants = constants
        self.path = path
        self.left_child = _SoftNode(depth - 1, variables, constants, f"{path}.L") if depth > 1 else None
        self.right_child = _SoftNode(depth - 1, variables, constants, f"{path}.R") if depth > 1 else None
        choices = len(self.base_labels) + (1 if depth > 1 else 0)
        self.left_logits = torch.nn.Parameter(torch.zeros(choices, dtype=torch.float64))
        self.right_logits = torch.nn.Parameter(torch.zeros(choices, dtype=torch.float64))

    @property
    def base_labels(self) -> list[str]:
        return [*[constant_label(value) for value in self.constants], *[f"var:{name}" for name in self.variables]]

    @property
    def labels(self) -> list[str]:
        labels = self.base_labels
        return [*labels, "child"] if self.depth > 1 else labels

    def reset_parameters(self, generator: torch.Generator | None = None, scale: float = 0.05) -> None:
        with torch.no_grad():
            self.left_logits.normal_(0.0, scale, generator=generator)
            self.right_logits.normal_(0.0, scale, generator=generator)
        if self.left_child is not None:
            self.left_child.reset_parameters(generator, scale)
        if self.right_child is not None:
            self.right_child.reset_parameters(generator, scale)

    def slot_catalog(self) -> dict[str, list[str]]:
        catalog = {
            f"{self.path}.left": self.labels,
            f"{self.path}.right": self.labels,
        }
        if self.left_child is not None:
            catalog.update(self.left_child.slot_catalog())
        if self.right_child is not None:
            catalog.update(self.right_child.slot_catalog())
        return catalog

    def _base_tensors(self, context: Mapping[str, torch.Tensor]) -> list[torch.Tensor]:
        first = next(iter(context.values()))
        values = [torch.zeros_like(first, dtype=torch.complex128) + value for value in self.constants]
        values.extend(context[name].to(dtype=torch.complex128) for name in self.variables)
        return values

    def _slot_value(
        self,
        logits: torch.Tensor,
        candidates: list[torch.Tensor],
        temperature: float,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        probs = torch.softmax(logits / temperature, dim=0).to(dtype=torch.complex128)
        value = torch.zeros_like(candidates[0], dtype=torch.complex128)
        for probability, candidate in zip(probs, candidates):
            value = value + probability * candidate
        return value, probs

    def forward(
        self,
        context: Mapping[str, torch.Tensor],
        *,
        temperature: float,
        training_semantics: bool,
        stats: AnomalyStats | None,
    ) -> torch.Tensor:
        left_candidates = self._base_tensors(context)
        right_candidates = self._base_tensors(context)
        if self.left_child is not None:
            left_candidates.append(
                self.left_child(
                    context,
                    temperature=temperature,
                    training_semantics=training_semantics,
                    stats=stats,
                )
            )
        if self.right_child is not None:
            right_candidates.append(
                self.right_child(
                    context,
                    temperature=temperature,
                    training_semantics=training_semantics,
                    stats=stats,
                )
            )
        left, _ = self._slot_value(self.left_logits, left_candidates, temperature)
        right, _ = self._slot_value(self.right_logits, right_candidates, temperature)
        return eml_torch(left, right, training=training_semantics, stats=stats, node=self.path)

    def gate_entropy(self, temperature: float = 1.0) -> torch.Tensor:
        entropy = torch.tensor(0.0, dtype=torch.float64, device=self.left_logits.device)
        for logits in (self.left_logits, self.right_logits):
            probs = torch.softmax(logits / temperature, dim=0)
            entropy = entropy - torch.sum(probs * torch.log(probs + 1e-12))
        if self.left_child is not None:
            entropy = entropy + self.left_child.gate_entropy(temperature)
        if self.right_child is not None:
            entropy = entropy + self.right_child.gate_entropy(temperature)
        return entropy

    def expected_child_use(self, temperature: float = 1.0) -> torch.Tensor:
        if self.depth == 1:
            return torch.tensor(0.0, dtype=torch.float64, device=self.left_logits.device)
        value = torch.tensor(0.0, dtype=torch.float64, device=self.left_logits.device)
        value = value + torch.softmax(self.left_logits / temperature, dim=0)[-1]
        value = value + torch.softmax(self.right_logits / temperature, dim=0)[-1]
        if self.left_child is not None:
            value = value + self.left_child.expected_child_use(temperature)
        if self.right_child is not None:
            value = value + self.right_child.expected_child_use(temperature)
        return value

    def _snap_slot(self, side: str, decisions: list[SnapDecision]) -> Expr:
        logits = self.left_logits if side == "left" else self.right_logits
        probs = torch.softmax(logits.detach(), dim=0)
        order = torch.argsort(probs, descending=True)
        index = int(order[0].item())
        second = float(probs[order[1]].item()) if len(order) > 1 else 0.0
        probability = float(probs[index].item())
        margin = probability - second
        choice = self.labels[index]
        decisions.append(SnapDecision(self.path, side, choice, probability, margin))
        if choice.startswith("const:"):
            return Const(parse_constant_label(choice))
        if choice.startswith("var:"):
            return Var(choice.split(":", 1)[1])
        if choice == "child":
            child = self.left_child if side == "left" else self.right_child
            if child is None:
                raise RuntimeError("Snapped child choice without a child node")
            return child._snap(decisions)
        raise RuntimeError(f"Unknown slot choice: {choice}")

    def _snap(self, decisions: list[SnapDecision]) -> Expr:
        return Eml(self._snap_slot("left", decisions), self._snap_slot("right", decisions))

    def set_slot(self, node_path: str, side: str, choice: str, strength: float = 30.0) -> None:
        if self.path == node_path:
            logits = self.left_logits if side == "left" else self.right_logits
            if choice not in self.labels:
                raise ValueError(f"Choice {choice!r} is not legal at {node_path}.{side}: {self.labels}")
            with torch.no_grad():
                logits.fill_(-strength)
                logits[self.labels.index(choice)] = strength
            return
        for child in (self.left_child, self.right_child):
            if child is not None and node_path.startswith(child.path):
                child.set_slot(node_path, side, choice, strength)
                return
        raise ValueError(f"Unknown node path: {node_path}")


class SoftEMLTree(torch.nn.Module):
    """A complete depth-bounded EML tree with soft categorical gates."""

    def __init__(
        self,
        depth: int,
        variables: tuple[str, ...] = ("x",),
        constants: tuple[complex, ...] = (1.0,),
    ) -> None:
        super().__init__()
        self.depth = depth
        self.variables = tuple(variables)
        self.constants = normalize_constants(constants)
        self.root = _SoftNode(depth, self.variables, self.constants)

    def reset_parameters(self, seed: int | None = None, scale: float = 0.05) -> None:
        generator = torch.Generator()
        if seed is not None:
            generator.manual_seed(seed)
        self.root.reset_parameters(generator, scale)

    def forward(
        self,
        context: Mapping[str, Any],
        *,
        temperature: float = 1.0,
        training_semantics: bool = True,
        stats: AnomalyStats | None = None,
    ) -> torch.Tensor:
        tensor_context = {name: as_complex_tensor(value) for name, value in context.items()}
        return self.root(
            tensor_context,
            temperature=temperature,
            training_semantics=training_semantics,
            stats=stats,
        )

    def slot_catalog(self) -> dict[str, list[str]]:
        return self.root.slot_catalog()

    def parameter_count(self) -> int:
        return sum(parameter.numel() for parameter in self.parameters())

    def expected_univariate_parameter_count(self) -> int:
        if len(self.variables) != 1:
            raise ValueError("The paper's 5 * 2^n - 6 count is for univariate trees")
        if self.constants != (1.0 + 0.0j,):
            raise ValueError("The paper's 5 * 2^n - 6 count assumes the pure const:1 terminal bank")
        return 5 * (2**self.depth) - 6

    def gate_entropy(self, temperature: float = 1.0) -> torch.Tensor:
        return self.root.gate_entropy(temperature)

    def expected_child_use(self, temperature: float = 1.0) -> torch.Tensor:
        return self.root.expected_child_use(temperature)

    def snap(self) -> SnapResult:
        decisions: list[SnapDecision] = []
        expression = self.root._snap(decisions)
        min_margin = min((decision.margin for decision in decisions), default=1.0)
        return SnapResult(
            expression=expression,
            decisions=decisions,
            min_margin=min_margin,
            active_node_count=expression.node_count(),
        )

    def set_slot(self, node_path: str, side: str, choice: str, strength: float = 30.0) -> None:
        self.root.set_slot(node_path, side, choice, strength=strength)

    def force_exp(self, variable: str = "x") -> None:
        self.set_slot("root", "left", f"var:{variable}")
        self.set_slot("root", "right", constant_label(1.0))

    def force_log(self, variable: str = "x") -> None:
        if self.depth < 3:
            raise ValueError("The paper log identity requires depth >= 3 in this scaffold")
        self.set_slot("root", "left", constant_label(1.0))
        self.set_slot("root", "right", "child")
        self.set_slot("root.R", "left", "child")
        self.set_slot("root.R", "right", constant_label(1.0))
        self.set_slot("root.R.L", "left", constant_label(1.0))
        self.set_slot("root.R.L", "right", f"var:{variable}")

    def force_scaled_exp(self, variable: str, coefficient: complex, strength: float = 30.0) -> EmbeddingResult:
        from .compiler import scaled_exponential_expr

        expression = scaled_exponential_expr(variable, coefficient)
        return self.embed_expr(expression, EmbeddingConfig(strength=strength))

    def embed_expr(self, expression: Expr, config: EmbeddingConfig | None = None) -> EmbeddingResult:
        return embed_expr_into_tree(self, expression, config=config)


def _leaf_choice(tree: SoftEMLTree, expression: Expr) -> str:
    if isinstance(expression, Const):
        label = constant_label(expression.value)
        if label not in tree.root.base_labels:
            raise EmbeddingError("missing_constant", f"{label} is not in terminal bank {tree.root.base_labels}")
        return label
    if isinstance(expression, Var):
        label = f"var:{expression.name}"
        if label not in tree.root.base_labels:
            raise EmbeddingError("missing_variable", f"{label} is not in terminal bank {tree.root.base_labels}")
        return label
    raise EmbeddingError("incompatible_tree", f"expected leaf, got {type(expression).__name__}")


def _embed_slot(
    tree: SoftEMLTree,
    node: _SoftNode,
    side: str,
    expression: Expr,
    config: EmbeddingConfig,
    assignments: list[EmbeddingAssignment],
) -> None:
    slot = f"{node.path}.{side}"
    if isinstance(expression, Eml):
        child = node.left_child if side == "left" else node.right_child
        if child is None:
            raise EmbeddingError("depth_too_small", f"{slot} needs a child node for expression depth {expression.depth()}")
        node.set_slot(node.path, side, "child", strength=config.strength)
        assignments.append(EmbeddingAssignment(slot, "child"))
        _embed_node(tree, child, expression, config, assignments)
        return

    choice = _leaf_choice(tree, expression)
    node.set_slot(node.path, side, choice, strength=config.strength)
    assignments.append(EmbeddingAssignment(slot, choice))


def _embed_node(
    tree: SoftEMLTree,
    node: _SoftNode,
    expression: Expr,
    config: EmbeddingConfig,
    assignments: list[EmbeddingAssignment],
) -> None:
    if not isinstance(expression, Eml):
        raise EmbeddingError("incompatible_tree", "SoftEMLTree root and child nodes represent EML nodes, not leaf roots")
    _embed_slot(tree, node, "left", expression.left, config, assignments)
    _embed_slot(tree, node, "right", expression.right, config, assignments)


def embed_expr_into_tree(
    tree: SoftEMLTree,
    expression: Expr,
    *,
    config: EmbeddingConfig | None = None,
) -> EmbeddingResult:
    config = config or EmbeddingConfig()
    if expression.depth() > tree.depth:
        raise EmbeddingError("depth_too_small", f"expression depth {expression.depth()} exceeds tree depth {tree.depth}")
    missing_variables = sorted(expression.variables() - set(tree.variables))
    if missing_variables:
        raise EmbeddingError("missing_variable", f"missing variables: {missing_variables}")
    missing_constants = [
        constant_label(value)
        for value in expression.constants()
        if not any(abs(complex(value) - complex(existing)) <= 1e-12 for existing in tree.constants)
    ]
    if missing_constants:
        raise EmbeddingError("missing_constant", f"missing constants: {missing_constants}")

    assignments: list[EmbeddingAssignment] = []
    _embed_node(tree, tree.root, expression, config, assignments)
    snap = tree.snap()
    round_trip = expressions_equal(expression, snap.expression)
    diagnostics = () if round_trip else ("snap_round_trip_mismatch",)
    return EmbeddingResult(bool(round_trip), tuple(assignments), snap, bool(round_trip), diagnostics)
