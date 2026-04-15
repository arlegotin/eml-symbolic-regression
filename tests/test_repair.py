from eml_symbolic_regression.expression import Const, Eml, Var
from eml_symbolic_regression.repair import RepairConfig, RepairMove, RepairReport
from eml_symbolic_regression.verify import SplitResult, VerificationReport


def _verification_report(status: str = "recovered") -> VerificationReport:
    return VerificationReport(
        status=status,
        candidate_kind="exact_eml",
        reason="verified" if status == "recovered" else "heldout_failed",
        split_results=[SplitResult("heldout", 0.0 if status == "recovered" else 1.0, 0.0, 0.0, status == "recovered")],
        high_precision_max_error=0.0 if status == "recovered" else 1.0,
        tolerance=1e-8,
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
