"""Verifier-gated local repair for perturbed true-tree near misses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .expression import Expr
from .verify import VerificationReport


@dataclass(frozen=True)
class RepairConfig:
    max_target_reverts: int = 8
    strength: float = 30.0
    allow_target_slot_reverts: bool = True
    allow_catalog_alternatives: bool = False


@dataclass(frozen=True)
class RepairMove:
    kind: str
    slot: str
    before: str
    after: str
    source: str
    accepted: bool
    verifier_status: str | None = None
    descendant_assignments: tuple[dict[str, str], ...] = ()
    pruned_assignments: tuple[dict[str, str], ...] = ()
    subtree_root: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "slot": self.slot,
            "before": self.before,
            "after": self.after,
            "source": self.source,
            "accepted": self.accepted,
            "verifier_status": self.verifier_status,
            "descendant_assignments": [dict(assignment) for assignment in self.descendant_assignments],
            "pruned_assignments": [dict(assignment) for assignment in self.pruned_assignments],
            "subtree_root": self.subtree_root,
        }


@dataclass(frozen=True)
class RepairReport:
    status: str
    original_status: str
    return_kind: str
    moves_attempted: tuple[RepairMove, ...]
    accepted_moves: tuple[RepairMove, ...]
    repaired_expression: Expr | None
    verification: VerificationReport | None
    reason: str

    def as_dict(self) -> dict[str, Any]:
        verified = self.status == "repaired_candidate" and self.verification is not None and self.verification.status == "recovered"
        repaired_ast = (
            self.repaired_expression.to_document(source="repaired_candidate")
            if verified and self.repaired_expression is not None
            else None
        )
        return {
            "status": self.status,
            "original_status": self.original_status,
            "return_kind": self.return_kind,
            "moves_attempted": [move.as_dict() for move in self.moves_attempted],
            "accepted_moves": [move.as_dict() for move in self.accepted_moves],
            "repaired_ast": repaired_ast,
            "verification": self.verification.as_dict() if self.verification is not None else None,
            "reason": self.reason,
        }
