# Phase 52: Verifier-Gated Exact Cleanup Expansion - Pattern Map

**Mapped:** 2026-04-17
**Files analyzed:** 14 expected source/test/doc files
**Analogs found:** 13 / 14

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `src/eml_symbolic_regression/repair.py` | service / cleanup engine | request-response, batch transform | current `cleanup_failed_candidate()` and `repair_perturbed_candidate()` | exact |
| `src/eml_symbolic_regression/master_tree.py` | model / neighborhood utility | transform, AST replay/dedup | `ActiveSlotAlternatives`, `expand_snap_neighborhood()` | exact |
| `src/eml_symbolic_regression/optimize.py` | service / candidate-pool model | batch, verifier-gated ranking | `ExactCandidate`, `FitResult`, `_select_exact_candidate()` | exact, preserve API |
| `src/eml_symbolic_regression/benchmark.py` | service / runner / suite registry | batch, file-I/O | blind, warm-start, perturbed cleanup wiring and artifact metrics | exact |
| `src/eml_symbolic_regression/benchmark_suites.py` | config registry | batch | no file exists; suite registry is inside `benchmark.py` | no analog |
| `src/eml_symbolic_regression/campaign.py` | reporting service | batch, file-I/O | repair columns, failure taxonomy, strengths/limits text | role-match, likely reference-only |
| `src/eml_symbolic_regression/diagnostics.py` | reporting service | batch, file-I/O | perturbed basin bound report repair rows | role-match, likely reference-only |
| `tests/test_repair.py` | test | request-response, transform | target-free cleanup, target-aware repair, report serialization tests | exact |
| `tests/test_master_tree.py` | test | transform, AST dedup | slot alternatives and neighborhood dedup tests | exact |
| `tests/test_benchmark_runner.py` | test | batch, file-I/O | monkeypatched repair promotion artifacts | exact |
| `tests/test_benchmark_contract.py` | test | config validation, batch | built-in suite registry and focused evidence suites | role-match |
| `tests/test_benchmark_reports.py` | test | batch aggregation | repair evidence class and threshold taxonomy tests | exact |
| `tests/test_campaign.py` | test | batch reporting, file-I/O | repair columns and report wording tests | role-match |
| `docs/IMPLEMENTATION.md` | documentation | reporting | recovery contract and benchmark evidence contract | exact |

## Pattern Assignments

### `src/eml_symbolic_regression/repair.py` (service / cleanup engine, request-response batch transform)

**Analog:** `src/eml_symbolic_regression/repair.py`

**Imports and config pattern** (lines 5-23):

```python
from dataclasses import dataclass
from typing import Any

from .expression import CenteredEml, Expr
from .master_tree import EmbeddingResult, NeighborhoodMove, SoftEMLTree, expand_snap_neighborhood
from .optimize import FitResult
from .verify import DataSplit, VerificationReport, verify_candidate


@dataclass(frozen=True)
class RepairConfig:
    max_target_reverts: int = 8
    strength: float = 30.0
    allow_target_slot_reverts: bool = True
    allow_catalog_alternatives: bool = False
    cleanup_top_k: int = 2
    cleanup_max_slots: int = 4
    cleanup_beam_width: int = 8
    cleanup_max_moves: int = 2
```

Keep `RepairConfig` as the owner for bounded cleanup defaults. Phase 52 should add larger bounded fields or a named preset here, then thread it into `benchmark.py`. Do not make cleanup unbounded.

**Repair report shape to preserve** (lines 64-93):

```python
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
    variant_count: int = 0

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
            "variant_count": self.variant_count,
        }
```

Add any Phase 52 provenance fields backward-compatibly. Useful additions are `candidate_roots_considered`, `candidate_root_count`, `deduped_variant_count`, and per-move `candidate_id`/`candidate_source`, but keep existing keys stable.

**Current selected-only cleanup entry point to extend** (lines 96-160):

```python
def cleanup_failed_candidate(
    fit: FitResult,
    *,
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
    selected = fit.selected_candidate
    if selected is None or not selected.slot_alternatives:
        return RepairReport(
            status="not_repaired",
            original_status=original_status,
            return_kind=return_kind,
            moves_attempted=(),
            accepted_moves=(),
            repaired_expression=None,
            verification=None,
            reason="missing_slot_alternatives",
        )
```

This is the exact REP-01 change site. Replace `selected = fit.selected_candidate` as the sole root with an ordered candidate-root iterator over:

- `fit.selected_candidate`
- `fit.fallback_candidate` when distinct
- retained `fit.candidates`

Deduplicate roots by exact AST document before expanding neighborhoods so fallback/selected manifests stay intact.

**Bounded alternative slicing pattern** (lines 122-148):

```python
slot_alternatives = tuple(
    item
    for item in selected.slot_alternatives[: config.cleanup_max_slots]
    if item.alternatives[: config.cleanup_top_k]
)
...
bounded = tuple(
    type(group)(
        slot=group.slot,
        current_choice=group.current_choice,
        current_probability=group.current_probability,
        current_margin=group.current_margin,
        alternatives=group.alternatives[: config.cleanup_top_k],
    )
    for group in slot_alternatives
)
```

Copy this shape for each candidate root. The planner should avoid mutating `ExactCandidate.slot_alternatives`; build bounded copies per root.

**Verifier-gated ranking pattern** (lines 173-210):

```python
attempted: list[RepairMove] = []
evaluated: list[tuple[tuple[RepairMove, ...], Expr, VerificationReport]] = []
for variant in variants:
    verification = verify_candidate(variant.expression, verification_splits, tolerance=tolerance)
    moves = tuple(
        _with_verification(_repair_move_from_neighborhood(move), verification.status, accepted=verification.status == "recovered")
        for move in variant.moves
    )
    attempted.extend(moves)
    evaluated.append((moves, variant.expression, verification))

best_moves, best_expression, best_verification = min(
    evaluated,
    key=lambda item: _cleanup_ranking_key(item[2], item[1], item[0]),
)
if best_verification.status == "recovered":
    return RepairReport(
        status="repaired_candidate",
        ...
        reason="verified_slot_neighborhood",
        variant_count=len(variants),
    )
```

For Phase 52, keep the verifier as the acceptance gate. Evaluate deduped variants across all roots, rank globally with `_cleanup_ranking_key()`, and only promote when the winning report has `status == "recovered"`.

**Move conversion and ranking pattern** (lines 464-506):

```python
def _repair_move_from_neighborhood(move: NeighborhoodMove) -> RepairMove:
    return RepairMove(
        kind=_move_kind(move.before, move.after),
        slot=move.slot,
        before=move.before,
        after=move.after,
        source="slot_alternative",
        accepted=False,
        descendant_assignments=tuple(assignment.as_dict() for assignment in move.descendant_assignments),
        pruned_assignments=tuple(assignment.as_dict() for assignment in move.pruned_assignments),
        subtree_root=move.subtree_root,
        slot_margin=move.slot_margin,
        probability_gap=move.probability_gap,
        rank=move.rank,
    )
```

```python
return (
    _verification_status_rank(verification.status),
    extrapolation_error,
    verification.high_precision_max_error,
    heldout_error,
    expression.node_count(),
    len(moves),
    sum(move.probability_gap or 0.0 for move in moves),
)
```

If moves need candidate-root provenance, extend `RepairMove` rather than introducing an unrelated move payload shape.

---

### `src/eml_symbolic_regression/master_tree.py` (model / neighborhood utility, transform)

**Analog:** `src/eml_symbolic_regression/master_tree.py`

**Provenance dataclass pattern** (lines 99-137, 140-181):

```python
@dataclass(frozen=True)
class SlotAlternative:
    choice: str
    probability: float
    probability_gap: float
    rank: int
    descendant_assignments: tuple[ReplayAssignment, ...] = ()
    subtree_root: str | None = None
```

```python
@dataclass(frozen=True)
class NeighborhoodMove:
    slot: str
    before: str
    after: str
    slot_margin: float
    probability_gap: float
    rank: int
    descendant_assignments: tuple[ReplayAssignment, ...] = ()
    pruned_assignments: tuple[ReplayAssignment, ...] = ()
    subtree_root: str | None = None
```

Do not invent a second subtree-provenance schema. REP-03 should reuse `descendant_assignments`, `pruned_assignments`, and `subtree_root`.

**Subtree alternatives source** (lines 501-552):

```python
def active_slot_alternatives(
    self,
    top_k: int = 2,
    *,
    max_slots: int | None = None,
    margin_threshold: float | None = None,
) -> tuple[ActiveSlotAlternatives, ...]:
    ...
    subtree_root = child.path if choice == "child" and child is not None else None
    descendant_assignments = child._subtree_assignments() if choice == "child" and child is not None else ()
```

Phase 52 should first consume this existing provenance from retained candidates. Only modify `master_tree.py` if tests prove the current `top_k=2` emission cannot expose the needed subtree choices.

**AST dedup and beam expansion pattern** (lines 720-773):

```python
base_slot_map = slot_map_from_snap(snap)
groups = sorted(slot_alternatives, key=lambda item: (item.current_margin, item.slot))
...
expression = replay_slot_map_expression(
    _slot_map_with_moves(base_slot_map, new_state),
    depth=depth,
    variables=variables,
    constants=constants,
    operator_family=operator_family,
    strength=strength,
)
key = json.dumps(expression.to_document(source="snap_neighborhood_candidate"), sort_keys=True)
candidate = NeighborhoodVariant(
    expression=expression,
    moves=new_state,
    heuristic_gap=sum(item.probability_gap for item in new_state),
)
existing = variants.get(key)
if existing is None or _variant_rank_key(candidate) < _variant_rank_key(existing):
    variants[key] = candidate
```

This is the REP-02 exact-AST dedup pattern. If dedup is needed across candidate roots, lift the same JSON-key strategy into `repair.py` around returned variants; do not weaken per-root dedup here.

**Subtree replay pattern** (lines 788-820):

```python
def _move_from_alternative(
    slot_map: Mapping[str, str],
    group: ActiveSlotAlternatives,
    alternative: SlotAlternative,
) -> NeighborhoodMove:
    subtree_root = alternative.subtree_root
    if group.current_choice == "child" and subtree_root is None:
        subtree_root = _child_root(group.slot)
    pruned_assignments = (
        _descendant_assignments_from_slot_map(slot_map, subtree_root)
        if group.current_choice == "child" and alternative.choice != "child" and subtree_root is not None
        else ()
    )
```

REP-03 subtree-level alternatives are already encoded for terminal-to-child, child-to-terminal, and child-subtree replacement. Tests should assert these fields survive candidate-pool cleanup.

---

### `src/eml_symbolic_regression/optimize.py` (service / candidate-pool model, batch ranking)

**Analog:** `src/eml_symbolic_regression/optimize.py`

**Exact candidate and fit result API to preserve** (lines 66-120):

```python
@dataclass(frozen=True)
class ExactCandidate:
    candidate_id: str
    attempt_index: int
    random_restart: int | None
    seed: int
    attempt_kind: str
    source: str
    checkpoint_index: int | None
    hardening_step: int | None
    global_step: int
    temperature: float
    best_fit_loss: float
    post_snap_loss: float
    snap: SnapResult
    slot_alternatives: tuple[ActiveSlotAlternatives, ...] = ()
    verification: VerificationReport | None = None
    selection_metrics: dict[str, Any] | None = None
```

```python
@dataclass(frozen=True)
class FitResult:
    status: str
    best_loss: float
    post_snap_loss: float
    snap: SnapResult
    manifest: dict[str, Any]
    verification: VerificationReport | None = None
    selected_candidate: ExactCandidate | None = None
    fallback_candidate: ExactCandidate | None = None
    candidates: tuple[ExactCandidate, ...] = ()
```

Phase 52 should consume these fields, not replace them. If more provenance is needed, prefer adding optional fields to `RepairReport` rather than changing `ExactCandidate` constructor arguments.

**Candidate emission keeps alternatives** (lines 202-222):

```python
snap = model.snap()
slot_alternatives = model.active_slot_alternatives(top_k=2)
snapped_pred = snap.expression.evaluate_numpy({name: np.asarray(value) for name, value in inputs.items()})
post_snap_loss = mse_complex_numpy(snapped_pred, target)
return ExactCandidate(
    ...
    snap=snap,
    slot_alternatives=slot_alternatives,
)
```

If larger cleanup needs more than `top_k=2`, this is the one optimize-side source. Treat changes here as higher risk because it affects manifest size and all candidate artifacts. A lower-risk path is to add a repair-time config that can use existing retained roots first, then separately decide whether candidate emission should increase `top_k`.

**Verifier-gated exact-pool selection** (lines 281-297):

```python
selection_mode = "verifier_gated_exact_candidate_pool" if verification_splits is not None else "train_post_snap_exact_candidate_pool"
ranked: list[ExactCandidate] = []
for candidate in candidates:
    report = (
        verify_candidate(candidate.snap.expression, verification_splits, tolerance=tolerance)
        if verification_splits is not None
        else None
    )
    ranked.append(replace(candidate, verification=report, selection_metrics=_selection_metrics(candidate, report)))
ranked.sort(key=_candidate_ranking_key)
return ranked, selection_mode
```

Use this as the mental model for cleanup ranking: verification first, then extrapolation/high-precision/heldout/error/complexity tie-breaks.

**Selected/fallback manifest preservation** (lines 450-493):

```python
selected_candidate = ranked_candidates[0]
fallback_candidate = next(
    candidate
    for candidate in ranked_candidates
    if candidate.candidate_id == str(best_log["legacy_candidate_id"])
)
...
"selected_candidate": selected_candidate.as_dict(),
"fallback_candidate": fallback_candidate.as_dict(),
...
selected_candidate=selected_candidate,
fallback_candidate=fallback_candidate,
candidates=tuple(ranked_candidates),
```

REP-01 says cleanup may use `selected`, `fallback`, and retained `candidates`, but REP-01/REP-02 do not authorize rewriting this manifest. Keep selected/fallback exactly as optimizer emitted them.

---

### `src/eml_symbolic_regression/benchmark.py` (service / runner / registry, batch file-I/O)

**Analog:** `src/eml_symbolic_regression/benchmark.py`

**Imports pattern** (lines 22-39):

```python
from .basin import fit_perturbed_true_tree
from .compiler import CompilerConfig, UnsupportedExpression, compile_and_validate, diagnose_compile_expression
from .datasets import demo_specs, proof_dataset_manifest
from .optimize import TrainingConfig, fit_eml_tree
from .repair import cleanup_failed_candidate, repair_perturbed_candidate
from .verify import verify_candidate
from .warm_start import PerturbationConfig, fit_warm_started_eml_tree
```

Keep benchmark wiring thin: build/run configs, call cleanup, serialize payloads. Cleanup search logic belongs in `repair.py`.

**Existing optimizer budget parser/as_dict pattern** (lines 147-221, 307-335):

```python
@classmethod
def from_mapping(cls, payload: Mapping[str, Any] | None, *, path: str = "optimizer") -> "OptimizerBudget":
    payload = payload or {}
    defaults = cls()
    values = {field_name: payload.get(field_name, getattr(defaults, field_name)) for field_name in cls.__dataclass_fields__}
    ...
    return cls(**values)
```

```python
def as_dict(self) -> dict[str, Any]:
    return {
        "depth": self.depth,
        "constants": [format_constant_value(value) for value in self.constants],
        "steps": self.steps,
        ...
        "operator_schedule": [operator.as_dict() for operator in self.operator_schedule],
    }
```

If cleanup bounds become benchmark-configurable, add fields to `OptimizerBudget.from_mapping()`, `validate()`, and `as_dict()` in this style. Keep types explicit and positive-bound validated.

**Blind cleanup integration to copy** (lines 1638-1658):

```python
if status != "recovered":
    cleanup = cleanup_failed_candidate(
        fit,
        depth=_fit_depth(fit, run.optimizer.depth),
        variables=_fit_variables(fit, (spec.variable,)),
        constants=_fit_constants(fit, run.optimizer.constants),
        verification_splits=splits,
        tolerance=run.dataset.tolerance,
        original_status=status,
        return_kind=status,
    )
    repair_payload = cleanup.as_dict()
    repair_status = "repaired" if cleanup.status == "repaired_candidate" else cleanup.status
    stage_statuses["local_repair"] = cleanup.status
    if cleanup.status == "repaired_candidate" and cleanup.verification is not None:
        status = "repaired_candidate"
        claim_status = cleanup.verification.status
        current_expression = cleanup.repaired_expression or current_expression
        current_verification = cleanup.verification
        current_source = "repaired_candidate"
```

Warm-start has the same pattern at lines 1761-1780. Perturbed-tree has the same target-free-first pattern plus target-aware fallback at lines 1905-1940. Add new config arguments consistently in all three call sites.

**Target-aware fallback must stay second** (lines 1905-1931):

```python
repair = cleanup_failed_candidate(...)
if repair.status != "repaired_candidate":
    target_repair = repair_perturbed_candidate(...)
    if target_repair.status == "repaired_candidate" or repair.variant_count == 0:
        repair = target_repair
```

Preserve this verifier-owned fallback behavior. Phase 52 expands target-free cleanup roots; it must not weaken or hide target-aware perturbed repair semantics.

**Artifact metrics extraction pattern** (lines 2446-2583):

```python
repair = payload.get("repair")
repair_verification = repair.get("verification") if isinstance(repair, Mapping) else None
repair_attempts = repair.get("moves_attempted") if isinstance(repair, Mapping) else None
repair_accepted = repair.get("accepted_moves") if isinstance(repair, Mapping) else None
repair_variant_count = repair.get("variant_count") if isinstance(repair, Mapping) else None
...
"candidate_pool_size": (
    selection.get("candidate_count")
    if isinstance(selection, Mapping)
    else len(candidate.get("candidates", ()))
    if isinstance(candidate, Mapping) and isinstance(candidate.get("candidates"), list)
    else None
),
"selected_candidate_id": selection.get("selected_candidate_id") if isinstance(selection, Mapping) else None,
"fallback_candidate_id": selection.get("fallback_candidate_id") if isinstance(selection, Mapping) else None,
...
"repair_status": payload.get("repair_status"),
"repair_variant_count": repair_variant_count,
"repair_move_count": len(repair_attempts) if isinstance(repair_attempts, list) else 0,
"repair_accepted_move_count": len(repair_accepted) if isinstance(repair_accepted, list) else 0,
"repair_verifier_status": repair_verification.get("status") if isinstance(repair_verification, Mapping) else None,
```

If Phase 52 adds root-count/dedup-count evidence, surface it here from `repair` into `metrics` so aggregate/campaign tables can use it without parsing nested moves.

**Taxonomy pattern** (lines 2908-2961):

```python
def classify_run(payload: Mapping[str, Any]) -> str:
    status = payload.get("status")
    ...
    repair_status = payload.get("repair_status")
    if repair_status == "repaired":
        return "repaired_candidate"
```

```python
if status == "repaired_candidate" or payload.get("repair_status") == "repaired":
    return EVIDENCE_CLASSES["repaired_candidate"]
```

Do not merge `repaired_candidate` into raw recovered/same-AST/verified-equivalent classes.

**Built-in suite registry location** (lines 42-71, 1045-1503):

```python
BUILTIN_SUITES = (
    "smoke",
    ...
    "v1.9-arrhenius-evidence",
    "v1.9-michaelis-evidence",
)
```

Focused REP-04 evidence can be added here as a small suite if needed. There is no current `benchmark_suites.py`.

---

### `src/eml_symbolic_regression/campaign.py` (reporting service, batch file-I/O)

**Analog:** `src/eml_symbolic_regression/campaign.py`

**Repair columns pattern** (lines 569-611, 699-712):

```python
_RUN_COLUMNS = [
    ...
    "return_kind",
    "raw_status",
    "repair_status",
    "repair_verifier_status",
    "repair_accepted_move_count",
    ...
]
```

```python
_FAILURE_COLUMNS = [
    "run_id",
    "formula",
    "start_mode",
    "classification",
    "status",
    "return_kind",
    "raw_status",
    "repair_status",
    "repair_verifier_status",
    "repair_accepted_move_count",
    "reason",
    "artifact_path",
]
```

If Phase 52 adds aggregate metrics, mirror them as columns only if REP-04 needs CSV/report visibility. Otherwise leave campaign reporting untouched.

**CSV row pattern** (lines 715-763):

```python
"repair_status": run.get("repair_status") or metrics.get("repair_status"),
"repair_verifier_status": metrics.get("repair_verifier_status"),
"repair_accepted_move_count": metrics.get("repair_accepted_move_count"),
```

Follow this `row` first, `metrics` fallback pattern for any new `repair_candidate_root_count` or `repair_deduped_variant_count` fields.

**Operator diagnostic rates** (lines 838-888):

```python
repair_attempts = sum(1 for run in items if _metric_text(run, "repair_status") not in {"", "None", "none", "not_attempted"})
repair_accepts = sum(
    1
    for run in items
    if _metric_text(run, "repair_status") == "repaired" or _metric_text(run, "repair_verifier_status") == "recovered"
)
```

This already supports REP-04 acceptance-rate evidence if benchmark metrics are populated.

---

### `src/eml_symbolic_regression/diagnostics.py` (reporting service, batch file-I/O)

**Analog:** `src/eml_symbolic_regression/diagnostics.py`

**Perturbed basin bound row pattern** (lines 65-152, 562-600):

```python
raw_supported = _supported_noise_prefix(
    rows,
    grid,
    lambda row: _has_durable_artifact(row) and row.get("evidence_class") == "perturbed_true_tree_recovered",
    expected_seeds_by_noise=expected_seeds_by_noise,
)
repaired_supported = _supported_noise_prefix(
    rows,
    grid,
    lambda row: _has_durable_artifact(row)
    and row.get("evidence_class") in {"perturbed_true_tree_recovered", "repaired_candidate"},
    expected_seeds_by_noise=expected_seeds_by_noise,
)
```

```python
"repair_status": repair_status,
"changed_slot_count": _row_or_metric(row, metrics, "changed_slot_count"),
"repair_accepted_move_count": _row_or_metric(row, metrics, "repair_accepted_move_count"),
```

Use this as the analog only if REP-04 chooses a Beer-Lambert near-miss evidence path. It already compares raw-supported and repaired-supported bounds without changing verifier requirements.

---

### `tests/test_repair.py` (test, request-response transform)

**Analog:** `tests/test_repair.py`

**Fixture pattern for building exact candidates** (lines 79-106):

```python
def _fit_with_selected_candidate(tree: SoftEMLTree) -> FitResult:
    snap = tree.snap()
    selected = ExactCandidate(
        candidate_id="selected",
        ...
        snap=snap,
        slot_alternatives=tree.active_slot_alternatives(top_k=2),
    )
    return FitResult(
        ...
        selected_candidate=selected,
        fallback_candidate=selected,
        candidates=(selected,),
    )
```

Extend this helper or add a sibling that creates distinct selected/fallback/retained candidates. The REP-01 unit test should prove selected-only cleanup fails while fallback/retained candidate cleanup succeeds.

**Report serialization invariants** (lines 149-179, 182-209):

```python
assert payload["status"] == "not_repaired"
assert payload["original_status"] == "snapped_but_failed"
assert payload["return_kind"] == "snapped_but_failed"
assert payload["accepted_moves"] == []
assert payload["repaired_ast"] is None
```

```python
assert payload["status"] == "repaired_candidate"
assert payload["accepted_moves"] == [accepted.as_dict()]
assert payload["repaired_ast"]["root"]["kind"] == "eml"
assert payload["repaired_ast"]["metadata"]["source"] == "repaired_candidate"
assert payload["verification"]["status"] == "recovered"
```

New tests should preserve these exact expectations while adding root provenance.

**Target-free cleanup success pattern** (lines 316-353):

```python
fit = _fit_with_selected_candidate(tree)
report = cleanup_failed_candidate(
    fit,
    depth=2,
    variables=("x",),
    constants=(1.0,),
    verification_splits=_verification_splits(target_expr),
    tolerance=1e-8,
    original_status="snapped_but_failed",
    return_kind="snapped_but_failed",
)

assert payload["status"] == "repaired_candidate"
assert payload["reason"] == "verified_slot_neighborhood"
assert payload["verification"]["status"] == "recovered"
assert payload["variant_count"] >= 1
assert accepted["source"] == "slot_alternative"
```

Copy this style for candidate-pool cleanup and subtree alternatives. Avoid target AST knowledge in `cleanup_failed_candidate()` tests.

---

### `tests/test_master_tree.py` (test, transform and AST dedup)

**Analog:** `tests/test_master_tree.py`

**Subtree alternative fixture** (lines 96-117):

```python
alternatives = tree.active_slot_alternatives(top_k=2, max_slots=1)

assert len(alternatives) == 1
assert alternatives[0].slot == "root.left"
assert alternatives[0].current_choice == "var:x"
assert alternatives[0].current_margin < 0.2
assert [item.choice for item in alternatives[0].alternatives] == ["child", "const:1"]
assert alternatives[0].alternatives[0].subtree_root == "root.L"
assert [item.as_dict() for item in alternatives[0].alternatives[0].descendant_assignments] == [
    {"slot": "root.L.left", "choice": "var:x"},
    {"slot": "root.L.right", "choice": "const:1"},
]
```

If REP-03 needs more tree coverage, add tests in this style with a retained candidate exposing a `child` alternative and descendants.

**Dedup fixture** (lines 119-150):

```python
variants = expand_snap_neighborhood(
    snap,
    tree.active_slot_alternatives(top_k=1, max_slots=2),
    depth=2,
    variables=("x",),
    constants=(1.0,),
    beam_width=8,
    max_moves=2,
)

serialized = [json.dumps(item.expression.to_document(), sort_keys=True) for item in variants]

assert len(serialized) == len(set(serialized))
```

Phase 52 cross-root dedup can use the same assertion shape in `tests/test_repair.py`.

---

### `tests/test_benchmark_runner.py` (test, batch file-I/O)

**Analog:** `tests/test_benchmark_runner.py`

**Repairable fit fixture** (lines 64-112):

```python
def _repairable_fit_for_exp() -> FitResult:
    tree = SoftEMLTree(1, ("x",), (1.0,))
    tree.set_slot("root", "right", "const:1", strength=40.0)
    with torch.no_grad():
        tree.root.left_logits.copy_(torch.tensor([2.0, 1.85], dtype=torch.float64))

    snap = tree.snap()
    selected = ExactCandidate(
        candidate_id="selected",
        ...
        verification=_verification_report("failed"),
        slot_alternatives=tree.active_slot_alternatives(top_k=1),
    )
    manifest = {
        "schema": "eml.run_manifest.v1",
        "status": "snapped_candidate",
        "snap": snap.as_dict(),
        "candidates": [selected.as_dict()],
        "selection": {
            "mode": "verifier_gated_exact_candidate_pool",
            "candidate_count": 1,
            "selected_candidate_id": "selected",
            "fallback_candidate_id": "selected",
        },
        "selected_candidate": selected.as_dict(),
        "fallback_candidate": selected.as_dict(),
    }
```

Create a Phase 52 variant with selected/fallback/retained candidate IDs that differ. Assert artifact selected/fallback IDs remain unchanged after repair.

**Blind/warm-start artifact promotion pattern** (lines 490-542):

```python
@pytest.mark.parametrize("start_mode", ["blind", "warm_start"])
def test_target_free_cleanup_promotes_blind_and_warm_start_artifacts(monkeypatch, tmp_path, start_mode):
    ...
    result = execute_benchmark_run(run)
    artifact = json.loads(result.artifact_path.read_text(encoding="utf-8"))
    candidate = artifact["trained_eml_candidate"] if start_mode == "blind" else artifact["warm_start_eml"]["optimizer"]

    assert result.status == "repaired_candidate"
    assert artifact["status"] == "repaired_candidate"
    assert artifact["claim_status"] == "recovered"
    assert artifact["repair_status"] == "repaired"
    assert artifact["repair"]["status"] == "repaired_candidate"
    assert artifact["repair"]["accepted_moves"][0]["source"] == "slot_alternative"
    assert candidate["selected_candidate"]["candidate_id"] == "selected"
    assert candidate["fallback_candidate"]["candidate_id"] == "selected"
```

Extend this exact test shape for candidate-pool cleanup and larger config. The key invariant is unchanged selected/fallback manifest plus promoted `repair`.

**Perturbed-tree target-free then target-aware pattern** (lines 471-488):

```python
assert result.status == "repaired_candidate"
assert artifact["return_kind"] == "snapped_but_failed"
assert artifact["raw_status"] == "snapped_but_failed"
assert artifact["repair_status"] == "repaired"
assert artifact["evidence_class"] == "repaired_candidate"
assert artifact["stage_statuses"]["local_repair"] == "repaired_candidate"
assert artifact["repair"]["verification"]["status"] == "recovered"
assert artifact["repair"]["accepted_moves"][0]["source"] == "embedded_target_slot"
```

Add a regression ensuring expanded target-free cleanup does not suppress the target-aware fallback when no target-free variants verify.

---

### `tests/test_benchmark_contract.py` (test, config validation batch)

**Analog:** `tests/test_benchmark_contract.py`

**Built-in registry assertion pattern** (lines 89-116):

```python
assert {
    "smoke",
    ...
    "v1.9-arrhenius-evidence",
    "v1.9-michaelis-evidence",
} <= set(list_builtin_suites())
suite = builtin_suite("smoke")
runs = suite.expanded_runs()

assert [run.case_id for run in runs] == ["exp-blind", "beer-warm", "planck-diagnostic"]
assert runs[0].run_id == suite.expanded_runs()[0].run_id
```

Use this only if REP-04 adds a built-in evidence suite. Otherwise prefer direct runner tests and leave suite registry untouched.

---

### `tests/test_benchmark_reports.py` (test, batch aggregation)

**Analog:** `tests/test_benchmark_reports.py`

**Synthetic aggregate fixture** (lines 23-76):

```python
def _synthetic_result(
    *,
    case_id: str,
    start_mode: str,
    training_mode: str,
    evidence_class: str,
    status: str = "recovered",
    claim_status: str = "recovered",
    perturbation_noise: float = 0.0,
    depth: int = 1,
    return_kind: str | None = None,
    raw_status: str | None = None,
    repair_status: str | None = None,
    ...
) -> BenchmarkRunResult:
    ...
    payload = {
        "run": run.as_dict(),
        "status": status,
        "claim_status": claim_status,
        ...
        "repair_status": repair_status,
        ...
        "metrics": {
            "best_loss": 0.01,
            "post_snap_loss": 0.02,
            "snap_min_margin": 0.7,
        },
    }
```

Add new repair metrics to `payload["metrics"]` in synthetic tests rather than requiring real benchmark execution.

**Repair threshold and taxonomy tests** (lines 290-348, 387-496):

```python
assert threshold["evidence_classes"] == {
    "perturbed_true_tree_recovered": 1,
    "repaired_candidate": 1,
    "snapped_but_failed": 1,
}
```

```python
assert classifications == {
    "same-ast": "same_ast_return",
    "verified-equivalent": "verified_equivalent_ast",
    "repair": "repaired_candidate",
    "snapped": "snapped_but_failed",
    "soft-fit": "soft_fit_only",
    "unsupported": "unsupported",
    "execution-error": "execution_failure",
}
```

If expanded cleanup changes repair rates, tests should still assert taxonomy remains distinct.

---

### `tests/test_campaign.py` (test, batch reporting file-I/O)

**Analog:** `tests/test_campaign.py`

**Repair CSV column test** (lines 332-374):

```python
assert {
    "return_kind",
    "raw_status",
    "repair_status",
    "repair_verifier_status",
    "repair_accepted_move_count",
} <= set(run_rows[0])
repaired = next(row for row in run_rows if row["evidence_class"] == "repaired_candidate")
assert repaired["repair_status"] == "repaired"
assert repaired["repair_verifier_status"] == "recovered"
assert repaired["repair_accepted_move_count"] == "1"
```

Add REP-04 evidence columns here only if campaign tables expose new cleanup-root or dedup metrics.

**Narrative separation pattern** (lines 595-684):

```python
assert "including 1 threshold-eligible pure blind recovery" in text
assert "plus 1 repaired candidate" in text
...
assert "perturbed true-tree basin" in text
assert "repaired candidates" in text
assert "Warm-start runs are especially useful evidence" not in text
```

If report text changes, preserve this distinction between pure blind, perturbed basin, and repaired candidate evidence.

---

### `docs/IMPLEMENTATION.md` (documentation, reporting)

**Analog:** `docs/IMPLEMENTATION.md`

**Recovery contract to update** (lines 21-36):

```markdown
Training loss is not enough. The optimizer now emits a retained exact-candidate pool across restarts plus late hardening checkpoints, but a candidate is only `recovered` when:

- it is an exact EML AST,
- it is evaluated after snapping,
- train, held-out, extrapolation, and mpmath checks pass,
- the verifier emits `recovered`.
```

```markdown
If that selected exact candidate still fails, benchmark flows can now run a bounded target-free cleanup stage over serialized low-margin slot alternatives. Cleanup never overwrites the original selected candidate in place; it records attempted edits and only promotes a repaired candidate when verifier-owned ranking improves.
```

Update this to say cleanup can inspect selected, fallback, and retained exact candidates when provenance is available.

**Benchmark artifact contract** (lines 83-94):

```markdown
Each run writes schema `eml.benchmark_run.v1` with:

- run identity and artifact path,
- dataset and optimizer configuration,
- start mode, seed, perturbation noise, and tags,
- stage statuses,
- normalized metrics such as best loss, post-snap loss, snap margin, active slot changes, verifier status, repair status, repair variant count, and high-precision error when available,
- timing and environment provenance,
- structured errors for unsupported or failed execution paths.
```

```markdown
When a blind, warm-start, or perturbed-basin exact candidate fails verification, the run artifact can now include a `repair` section with attempted slot or subtree edits, their margins/probability gaps, accepted moves, and the repaired verifier report if cleanup wins. The original selected and fallback candidates from the optimizer manifest remain intact for weak-dominance comparisons.
```

Add the expanded candidate-root and dedup evidence fields here if implemented.

## Shared Patterns

### Verifier-Owned Acceptance
**Source:** `src/eml_symbolic_regression/verify.py` lines 72-129  
**Apply to:** `repair.py`, `benchmark.py`, all tests

```python
def verify_candidate(
    candidate: Candidate,
    splits: list[DataSplit],
    *,
    tolerance: float = 1e-8,
    high_precision_points: int = 8,
    high_precision_skip_factor: float = 1e6,
    recovered_requires_exact_eml: bool = True,
) -> VerificationReport:
    ...
    if all_passed and (candidate_kind == "exact_eml" or not recovered_requires_exact_eml):
        status = "recovered"
        reason = "verified"
```

Cleanup may search more, but it must not define recovery itself.

### Exact-AST Serialization For Dedup
**Source:** `src/eml_symbolic_regression/expression.py` lines 110-122 and `master_tree.py` lines 759-767  
**Apply to:** candidate-root dedup, variant dedup, tests

```python
def to_document(self, variables: list[str] | None = None, **metadata: Any) -> dict[str, Any]:
    return {
        "schema": AST_SCHEMA,
        "semantics": self.semantics_document(),
        "variables": variables or sorted(self.variables()),
        "root": self.to_node(),
        "metadata": {
            "node_count": self.node_count(),
            "depth": self.depth(),
            "source": "exact_ast",
            **metadata,
        },
    }
```

Use `json.dumps(..., sort_keys=True)` and normalize/remap `metadata["source"]` when comparing logical AST equality across sources.

### Fallback Preservation
**Source:** `src/eml_symbolic_regression/optimize.py` lines 450-493 and `benchmark.py` lines 1638-1658  
**Apply to:** `repair.py`, `benchmark.py`, runner tests

Selected and fallback candidates are already serialized separately in the optimizer manifest. Cleanup should append a `repair` report and promote only the top-level current expression/status when verifier-recovered; it should not edit `trained_eml_candidate.selected_candidate` or `fallback_candidate`.

### Repair Taxonomy
**Source:** `src/eml_symbolic_regression/proof.py` lines 27-42 and `benchmark.py` lines 2908-2961  
**Apply to:** benchmark/campaign/report tests

`repaired_candidate` is a first-class evidence class. Do not count it as `blind_training_recovered`, `same_ast`, or `perturbed_true_tree_recovered`.

## Existing APIs To Preserve

- `cleanup_failed_candidate(fit, *, depth, variables, constants, verification_splits, tolerance, config, original_status, return_kind) -> RepairReport`
- `RepairReport.as_dict()` keys: `status`, `original_status`, `return_kind`, `moves_attempted`, `accepted_moves`, `repaired_ast`, `verification`, `reason`, `variant_count`
- `RepairMove.as_dict()` keys: `kind`, `slot`, `before`, `after`, `source`, `accepted`, `verifier_status`, `descendant_assignments`, `pruned_assignments`, `subtree_root`, optional `slot_margin`, `probability_gap`, `rank`
- `FitResult.selected_candidate`, `FitResult.fallback_candidate`, `FitResult.candidates`
- `ExactCandidate.as_dict()` key `slot_alternatives`
- Benchmark artifact top-level keys: `repair`, `repair_status`, `stage_statuses.local_repair`, `trained_eml_candidate`, `trained_eml_verification`, `claim_status`, `evidence_class`, `metrics`

## Artifact Shapes To Preserve Or Extend

Current not-repaired artifact shape:

```json
{
  "repair": {
    "accepted_moves": [],
    "moves_attempted": [{"source": "slot_alternative", "verifier_status": "failed"}],
    "original_status": "snapped_but_failed",
    "reason": "no_verified_slot_neighborhood",
    "repaired_ast": null,
    "return_kind": "snapped_but_failed",
    "status": "not_repaired",
    "variant_count": 24,
    "verification": null
  },
  "repair_status": "not_repaired"
}
```

Current repaired artifact shape:

```json
{
  "repair": {
    "accepted_moves": [{"source": "slot_alternative", "verifier_status": "recovered"}],
    "original_status": "snapped_but_failed",
    "reason": "verified_slot_neighborhood",
    "repaired_ast": {"schema": "eml.ast.v1", "metadata": {"source": "repaired_candidate"}},
    "return_kind": "snapped_but_failed",
    "status": "repaired_candidate",
    "verification": {"status": "recovered"}
  },
  "repair_status": "repaired",
  "status": "repaired_candidate",
  "evidence_class": "repaired_candidate"
}
```

Phase 52 extension should be additive, for example:

```json
{
  "repair": {
    "candidate_roots_considered": [
      {"candidate_id": "selected", "source": "hardening_checkpoint", "role": "selected"},
      {"candidate_id": "attempt-000-legacy-final-snap", "source": "legacy_final_snap", "role": "fallback"}
    ],
    "candidate_root_count": 2,
    "deduped_variant_count": 48
  }
}
```

## Likely File Ownership

- `repair.py` owns candidate-root enumeration, cross-root AST dedup, verifier-gated global ranking, provenance fields, and larger cleanup preset/config.
- `master_tree.py` owns only missing primitive neighborhood provenance. Use existing APIs first.
- `optimize.py` owns candidate-pool emission. Avoid changing it unless `top_k=2` provenance is demonstrably insufficient.
- `benchmark.py` owns config threading and artifact promotion for blind, warm-start, and perturbed-tree flows.
- `campaign.py` and `diagnostics.py` own evidence presentation only. Touch them only if new metrics need public tables/reports.
- Tests should start in `test_repair.py` and `test_benchmark_runner.py`; aggregate/report tests are only needed if artifact metrics/taxonomy change.

## No Analog Found

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|
| `src/eml_symbolic_regression/benchmark_suites.py` | config registry | batch | This module does not exist. Built-in suite registration, case construction, validation, and loading live in `src/eml_symbolic_regression/benchmark.py`. Prefer extending `benchmark.py` unless a broader refactor is explicitly planned. |

## Metadata

**Analog search scope:** `src/eml_symbolic_regression/*.py`, `tests/test_*.py`, `docs/IMPLEMENTATION.md`, `README.md`, representative committed benchmark/proof artifacts  
**Files scanned:** 26 code/doc files plus targeted artifact examples  
**Pattern extraction date:** 2026-04-17
