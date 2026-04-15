import numpy as np

from eml_symbolic_regression.expression import Const, Eml, Var
from eml_symbolic_regression.master_tree import EmbeddingResult, SoftEMLTree
from eml_symbolic_regression.optimize import FitResult
from eml_symbolic_regression.repair import RepairConfig, RepairMove, RepairReport, repair_perturbed_candidate
from eml_symbolic_regression.verify import DataSplit, SplitResult, VerificationReport


def _verification_report(status: str = "recovered") -> VerificationReport:
    return VerificationReport(
        status=status,
        candidate_kind="exact_eml",
        reason="verified" if status == "recovered" else "heldout_failed",
        split_results=[SplitResult("heldout", 0.0 if status == "recovered" else 1.0, 0.0, 0.0, status == "recovered")],
        high_precision_max_error=0.0 if status == "recovered" else 1.0,
        tolerance=1e-8,
    )


def _fit_from_slots(
    slots: dict[str, str],
    *,
    depth: int = 2,
    variables: tuple[str, ...] = ("x",),
    constants: tuple[complex, ...] = (1.0,),
) -> FitResult:
    tree = SoftEMLTree(depth, variables, constants)
    for slot, choice in slots.items():
        node_path, side = slot.rsplit(".", 1)
        tree.set_slot(node_path, side, choice, strength=40.0)
    snap = tree.snap()
    return FitResult(
        status="snapped_candidate",
        best_loss=1.0,
        post_snap_loss=1.0,
        snap=snap,
        manifest={"snap": snap.as_dict(), "status": "snapped_candidate"},
    )


def _embedding_for_target(target_expr: Eml, *, depth: int = 2) -> EmbeddingResult:
    tree = SoftEMLTree(depth, ("x",), (1.0,))
    return tree.embed_expr(target_expr)


def _verification_splits(target_expr: Eml) -> list[DataSplit]:
    x_values = np.linspace(-0.4, 0.4, 9).astype(np.complex128)
    inputs = {"x": x_values}
    target = target_expr.evaluate_numpy(inputs)
    return [
        DataSplit("heldout", inputs, target),
        DataSplit("extrap", {"x": (x_values + 0.8).astype(np.complex128)}, target_expr.evaluate_numpy({"x": x_values + 0.8})),
    ]


def _run_repair(fit: FitResult, target_expr: Eml, embedding: EmbeddingResult) -> RepairReport:
    return repair_perturbed_candidate(
        fit,
        target_expr=target_expr,
        embedding=embedding,
        depth=2,
        variables=("x",),
        constants=(1.0,),
        verification_splits=_verification_splits(target_expr),
        tolerance=1e-8,
        original_status="snapped_but_failed",
        return_kind="snapped_but_failed",
    )


def test_repair_config_defaults_to_bounded_target_neighborhood() -> None:
    config = RepairConfig()

    assert config.max_target_reverts == 8
    assert config.strength == 30.0
    assert config.allow_target_slot_reverts is True
    assert config.allow_catalog_alternatives is False


def test_repair_move_serializes_slot_and_subtree_provenance() -> None:
    move = RepairMove(
        kind="terminal_to_child",
        slot="root.left",
        before="var:x",
        after="child",
        source="embedded_target_slot",
        accepted=False,
        verifier_status="failed",
        descendant_assignments=({"slot": "root.L.left", "choice": "var:x"}, {"slot": "root.L.right", "choice": "const:1"}),
        pruned_assignments=({"slot": "root.L.right", "choice": "const:1"},),
        subtree_root="root.L",
    )

    payload = move.as_dict()

    assert payload["kind"] == "terminal_to_child"
    assert payload["slot"] == "root.left"
    assert payload["before"] == "var:x"
    assert payload["after"] == "child"
    assert payload["source"] == "embedded_target_slot"
    assert payload["accepted"] is False
    assert payload["verifier_status"] == "failed"
    assert payload["descendant_assignments"] == [
        {"slot": "root.L.left", "choice": "var:x"},
        {"slot": "root.L.right", "choice": "const:1"},
    ]
    assert payload["pruned_assignments"] == [{"slot": "root.L.right", "choice": "const:1"}]
    assert payload["subtree_root"] == "root.L"


def test_unverified_repair_report_preserves_raw_status_without_repaired_ast() -> None:
    attempted = RepairMove(
        kind="slot_revert",
        slot="root.right",
        before="var:x",
        after="const:1",
        source="embedded_target_slot",
        accepted=False,
        verifier_status="failed",
    )
    report = RepairReport(
        status="not_repaired",
        original_status="snapped_but_failed",
        return_kind="snapped_but_failed",
        moves_attempted=(attempted,),
        accepted_moves=(),
        repaired_expression=Eml(Var("x"), Const(1.0)),
        verification=_verification_report("failed"),
        reason="no_verified_local_move",
    )

    payload = report.as_dict()

    assert payload["status"] == "not_repaired"
    assert payload["original_status"] == "snapped_but_failed"
    assert payload["return_kind"] == "snapped_but_failed"
    assert payload["moves_attempted"] == [attempted.as_dict()]
    assert payload["accepted_moves"] == []
    assert payload["repaired_ast"] is None
    assert payload["verification"]["status"] == "failed"
    assert payload["reason"] == "no_verified_local_move"


def test_verified_repair_report_serializes_repaired_ast_and_verification() -> None:
    accepted = RepairMove(
        kind="slot_revert",
        slot="root.right",
        before="var:x",
        after="const:1",
        source="embedded_target_slot",
        accepted=True,
        verifier_status="recovered",
    )
    report = RepairReport(
        status="repaired_candidate",
        original_status="snapped_but_failed",
        return_kind="snapped_but_failed",
        moves_attempted=(accepted,),
        accepted_moves=(accepted,),
        repaired_expression=Eml(Var("x"), Const(1.0)),
        verification=_verification_report("recovered"),
        reason="verified_local_move",
    )

    payload = report.as_dict()

    assert payload["status"] == "repaired_candidate"
    assert payload["accepted_moves"] == [accepted.as_dict()]
    assert payload["repaired_ast"]["root"]["kind"] == "eml"
    assert payload["repaired_ast"]["metadata"]["source"] == "repaired_candidate"
    assert payload["verification"]["status"] == "recovered"


def test_terminal_to_child_repair_applies_new_descendant_assignments() -> None:
    target_expr = Eml(Eml(Var("x"), Const(1.0)), Const(1.0))
    fit = _fit_from_slots({"root.left": "var:x", "root.right": "const:1"})
    report = _run_repair(fit, target_expr, _embedding_for_target(target_expr))

    payload = report.as_dict()
    accepted = payload["accepted_moves"][0]

    assert payload["status"] == "repaired_candidate"
    assert payload["original_status"] == "snapped_but_failed"
    assert payload["return_kind"] == "snapped_but_failed"
    assert payload["verification"]["status"] == "recovered"
    assert accepted["kind"] == "terminal_to_child"
    assert accepted["slot"] == "root.left"
    assert accepted["before"] == "var:x"
    assert accepted["after"] == "child"
    assert accepted["source"] == "embedded_target_slot"
    assert accepted["verifier_status"] == "recovered"
    assert accepted["descendant_assignments"] == [
        {"slot": "root.L.left", "choice": "var:x"},
        {"slot": "root.L.right", "choice": "const:1"},
    ]
    assert accepted["subtree_root"] == "root.L"


def test_child_to_terminal_repair_records_pruned_descendants() -> None:
    target_expr = Eml(Var("x"), Const(1.0))
    fit = _fit_from_slots(
        {
            "root.left": "child",
            "root.L.left": "var:x",
            "root.L.right": "const:1",
            "root.right": "const:1",
        }
    )
    report = _run_repair(fit, target_expr, _embedding_for_target(target_expr))

    accepted = report.as_dict()["accepted_moves"][0]

    assert report.status == "repaired_candidate"
    assert accepted["kind"] == "child_to_terminal"
    assert accepted["slot"] == "root.left"
    assert accepted["before"] == "child"
    assert accepted["after"] == "var:x"
    assert accepted["pruned_assignments"] == [
        {"slot": "root.L.left", "choice": "var:x"},
        {"slot": "root.L.right", "choice": "const:1"},
    ]
    assert accepted["subtree_root"] == "root.L"


def test_child_subtree_replacement_replays_descendant_target_slots() -> None:
    target_expr = Eml(Eml(Var("x"), Const(1.0)), Const(1.0))
    fit = _fit_from_slots(
        {
            "root.left": "child",
            "root.L.left": "const:1",
            "root.L.right": "var:x",
            "root.right": "const:1",
        }
    )
    report = _run_repair(fit, target_expr, _embedding_for_target(target_expr))

    accepted = report.as_dict()["accepted_moves"][0]

    assert report.status == "repaired_candidate"
    assert accepted["kind"] == "child_subtree_replacement"
    assert accepted["slot"] == "root.left"
    assert accepted["before"] == "child"
    assert accepted["after"] == "child"
    assert accepted["descendant_assignments"] == [
        {"slot": "root.L.left", "choice": "var:x"},
        {"slot": "root.L.right", "choice": "const:1"},
    ]
    assert accepted["subtree_root"] == "root.L"


def test_repair_does_not_accept_without_verifier_recovery() -> None:
    target_expr = Eml(Eml(Var("x"), Const(1.0)), Const(1.0))
    wrong_verifier_target = Eml(Const(1.0), Const(1.0))
    fit = _fit_from_slots({"root.left": "var:x", "root.right": "const:1"})

    report = repair_perturbed_candidate(
        fit,
        target_expr=target_expr,
        embedding=_embedding_for_target(target_expr),
        depth=2,
        variables=("x",),
        constants=(1.0,),
        verification_splits=_verification_splits(wrong_verifier_target),
        tolerance=1e-8,
        original_status="snapped_but_failed",
        return_kind="snapped_but_failed",
    )

    payload = report.as_dict()

    assert payload["status"] == "not_repaired"
    assert payload["reason"] == "no_verified_local_move"
    assert payload["accepted_moves"] == []
    assert payload["repaired_ast"] is None
    assert {move["verifier_status"] for move in payload["moves_attempted"]} == {"failed"}
