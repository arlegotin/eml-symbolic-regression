"""Verifier-gated local repair for perturbed true-tree near misses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .expression import Expr
from .master_tree import EmbeddingResult, SoftEMLTree
from .optimize import FitResult
from .verify import DataSplit, VerificationReport, verify_candidate


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


def repair_perturbed_candidate(
    fit: FitResult,
    *,
    target_expr: Expr,
    embedding: EmbeddingResult,
    depth: int,
    variables: tuple[str, ...],
    constants: tuple[complex, ...],
    verification_splits: list[DataSplit],
    tolerance: float,
    config: RepairConfig | None = None,
    original_status: str,
    return_kind: str,
) -> RepairReport:
    config = config or RepairConfig()
    if config.allow_catalog_alternatives:
        return RepairReport(
            status="not_repaired",
            original_status=original_status,
            return_kind=return_kind,
            moves_attempted=(),
            accepted_moves=(),
            repaired_expression=None,
            verification=None,
            reason="catalog_alternatives_disabled",
        )
    if not config.allow_target_slot_reverts:
        return RepairReport(
            status="not_repaired",
            original_status=original_status,
            return_kind=return_kind,
            moves_attempted=(),
            accepted_moves=(),
            repaired_expression=None,
            verification=None,
            reason="target_slot_reverts_disabled",
        )

    snapped_slot_map = _snapped_slot_map(fit)
    target_slot_map = _target_slot_map(embedding)
    moves = _target_neighborhood_moves(snapped_slot_map, target_slot_map)
    attempted: list[RepairMove] = []

    for move in moves:
        candidate = _candidate_from_moves(
            snapped_slot_map,
            (move,),
            depth=depth,
            variables=variables,
            constants=constants,
            strength=config.strength,
        )
        verification = verify_candidate(candidate, verification_splits, tolerance=tolerance)
        attempted_move = _with_verification(move, verification.status, accepted=verification.status == "recovered")
        attempted.append(attempted_move)
        if verification.status == "recovered":
            return RepairReport(
                status="repaired_candidate",
                original_status=original_status,
                return_kind=return_kind,
                moves_attempted=tuple(attempted),
                accepted_moves=(attempted_move,),
                repaired_expression=candidate,
                verification=verification,
                reason="verified_local_move",
            )

    if len(moves) > 1 and len(moves) <= config.max_target_reverts:
        candidate = _candidate_from_moves(
            snapped_slot_map,
            moves,
            depth=depth,
            variables=variables,
            constants=constants,
            strength=config.strength,
        )
        verification = verify_candidate(candidate, verification_splits, tolerance=tolerance)
        accepted = verification.status == "recovered"
        combined_moves = tuple(_with_verification(move, verification.status, accepted=accepted) for move in moves)
        attempted.extend(combined_moves)
        if accepted:
            return RepairReport(
                status="repaired_candidate",
                original_status=original_status,
                return_kind=return_kind,
                moves_attempted=tuple(attempted),
                accepted_moves=combined_moves,
                repaired_expression=candidate,
                verification=verification,
                reason="verified_target_neighborhood",
            )

    return RepairReport(
        status="not_repaired",
        original_status=original_status,
        return_kind=return_kind,
        moves_attempted=tuple(attempted),
        accepted_moves=(),
        repaired_expression=None,
        verification=None,
        reason="no_verified_local_move",
    )


def _snapped_slot_map(fit: FitResult) -> dict[str, str]:
    return {f"{decision.path}.{decision.side}": decision.choice for decision in fit.snap.decisions}


def _target_slot_map(embedding: EmbeddingResult) -> dict[str, str]:
    return {assignment.slot: assignment.choice for assignment in embedding.assignments}


def _target_neighborhood_moves(snapped: dict[str, str], target: dict[str, str]) -> tuple[RepairMove, ...]:
    moves: list[RepairMove] = []
    covered_descendants: set[str] = set()

    for slot in _sorted_slots(sorted(set(snapped) | set(target))):
        before = snapped.get(slot)
        after = target.get(slot)
        if before == "child" and after == "child":
            subtree_root = _child_root(slot)
            target_descendants = _descendant_assignments(target, subtree_root)
            snapped_descendants = _descendant_assignments(snapped, subtree_root)
            if target_descendants and target_descendants != snapped_descendants:
                moves.append(
                    RepairMove(
                        kind="child_subtree_replacement",
                        slot=slot,
                        before="child",
                        after="child",
                        source="embedded_target_slot",
                        accepted=False,
                        descendant_assignments=target_descendants,
                        pruned_assignments=_pruned_assignments(snapped, target, subtree_root),
                        subtree_root=subtree_root,
                    )
                )
                covered_descendants.update(assignment["slot"] for assignment in target_descendants)
                covered_descendants.update(assignment["slot"] for assignment in snapped_descendants)

    for slot in _sorted_slots(sorted(set(snapped) | set(target))):
        if slot in covered_descendants:
            continue
        before = snapped.get(slot)
        after = target.get(slot)
        if before == after or after is None:
            continue
        if before is None:
            moves.append(
                RepairMove(
                    kind="slot_revert",
                    slot=slot,
                    before="<unset>",
                    after=after,
                    source="embedded_target_slot",
                    accepted=False,
                )
            )
            continue
        if before != "child" and after == "child":
            subtree_root = _child_root(slot)
            descendant_assignments = _descendant_assignments(target, subtree_root)
            moves.append(
                RepairMove(
                    kind="terminal_to_child",
                    slot=slot,
                    before=before,
                    after=after,
                    source="embedded_target_slot",
                    accepted=False,
                    descendant_assignments=descendant_assignments,
                    subtree_root=subtree_root,
                )
            )
            covered_descendants.update(assignment["slot"] for assignment in descendant_assignments)
            continue
        if before == "child" and after != "child":
            subtree_root = _child_root(slot)
            moves.append(
                RepairMove(
                    kind="child_to_terminal",
                    slot=slot,
                    before=before,
                    after=after,
                    source="embedded_target_slot",
                    accepted=False,
                    pruned_assignments=_descendant_assignments(snapped, subtree_root),
                    subtree_root=subtree_root,
                )
            )
            continue
        moves.append(
            RepairMove(
                kind="slot_revert",
                slot=slot,
                before=before,
                after=after,
                source="embedded_target_slot",
                accepted=False,
            )
        )

    return tuple(moves)


def _candidate_from_moves(
    snapped_slot_map: dict[str, str],
    moves: tuple[RepairMove, ...],
    *,
    depth: int,
    variables: tuple[str, ...],
    constants: tuple[complex, ...],
    strength: float,
) -> Expr:
    slot_map = dict(snapped_slot_map)
    for move in moves:
        slot_map[move.slot] = move.after
        for assignment in move.descendant_assignments:
            slot_map[assignment["slot"]] = assignment["choice"]

    tree = SoftEMLTree(depth, variables, constants)
    for slot, choice in _slot_items_for_replay(slot_map):
        node_path, side = slot.rsplit(".", 1)
        tree.set_slot(node_path, side, choice, strength=strength)
    return tree.snap().expression


def _with_verification(move: RepairMove, verifier_status: str, *, accepted: bool) -> RepairMove:
    return RepairMove(
        kind=move.kind,
        slot=move.slot,
        before=move.before,
        after=move.after,
        source=move.source,
        accepted=accepted,
        verifier_status=verifier_status,
        descendant_assignments=move.descendant_assignments,
        pruned_assignments=move.pruned_assignments,
        subtree_root=move.subtree_root,
    )


def _child_root(slot: str) -> str:
    node_path, side = slot.rsplit(".", 1)
    return f"{node_path}.{'L' if side == 'left' else 'R'}"


def _descendant_assignments(slot_map: dict[str, str], subtree_root: str) -> tuple[dict[str, str], ...]:
    return tuple({"slot": slot, "choice": slot_map[slot]} for slot in _sorted_slots(slot for slot in slot_map if slot.startswith(f"{subtree_root}.")))


def _pruned_assignments(snapped: dict[str, str], target: dict[str, str], subtree_root: str) -> tuple[dict[str, str], ...]:
    pruned = [slot for slot in snapped if slot.startswith(f"{subtree_root}.") and slot not in target]
    return tuple({"slot": slot, "choice": snapped[slot]} for slot in _sorted_slots(pruned))


def _slot_items_for_replay(slot_map: dict[str, str]) -> tuple[tuple[str, str], ...]:
    return tuple((slot, slot_map[slot]) for slot in _sorted_slots(slot_map))


def _sorted_slots(slots: Any) -> list[str]:
    return sorted(slots, key=lambda slot: (slot.count("."), slot))
