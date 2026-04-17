# Phase 49: Witness Registry and Centered Scaffold Correctness - Pattern Map

**Mapped:** 2026-04-17
**Files analyzed:** 8
**Analogs found:** 8 / 8

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `src/eml_symbolic_regression/witnesses.py` | utility / config | transform | `src/eml_symbolic_regression/semantics.py` + `src/eml_symbolic_regression/benchmark.py` | role-match |
| `src/eml_symbolic_regression/optimize.py` | service | batch / transform | `src/eml_symbolic_regression/optimize.py` | exact |
| `src/eml_symbolic_regression/benchmark.py` | service / orchestrator | batch / file-I/O | `src/eml_symbolic_regression/benchmark.py` | exact |
| `src/eml_symbolic_regression/master_tree.py` | model / utility | transform | `src/eml_symbolic_regression/master_tree.py` | exact |
| `src/eml_symbolic_regression/__init__.py` | config / public API | static export | `src/eml_symbolic_regression/__init__.py` | exact |
| `tests/test_benchmark_contract.py` | test | request-response / validation | `tests/test_benchmark_contract.py` | exact |
| `tests/test_benchmark_runner.py` | test | file-I/O / artifact | `tests/test_benchmark_runner.py` | exact |
| `tests/test_optimizer_cleanup.py` | test | batch / optimizer manifest | `tests/test_optimizer_cleanup.py` | exact |

## Pattern Assignments

### `src/eml_symbolic_regression/witnesses.py` (utility / config, transform)

**Analog:** `src/eml_symbolic_regression/semantics.py` for frozen metadata and serialization, plus `src/eml_symbolic_regression/benchmark.py` for scaffold validation and exclusion strings.

**Imports pattern** (`src/eml_symbolic_regression/semantics.py` lines 3-6):

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
```

Use only stdlib plus `.semantics.EmlOperator`. Keep `witnesses.py` independent of `benchmark.py`, `optimize.py`, and `master_tree.py` so it can be imported by all three without cycles.

**Frozen metadata pattern** (`src/eml_symbolic_regression/semantics.py` lines 12-24, 49-84):

```python
@dataclass(frozen=True)
class EmlOperator:
    """Operator-family metadata for raw and centered EML nodes."""

    family: str = "raw_eml"
    s: float = 1.0
    t: complex = 1.0 + 0.0j
    terminal: str = "one"

    def __post_init__(self) -> None:
        family = str(self.family)
        if family not in {"raw_eml", "ceml_s_t", "ceml_s", "zeml_s"}:
            raise ValueError(f"unknown EML operator family: {family!r}")

    @property
    def is_raw(self) -> bool:
        return self.family == "raw_eml"

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "family": self.family,
            "label": self.label,
            "s": self.s,
            "terminal": self.terminal,
        }
        return payload
```

Copy this shape for `ScaffoldWitness` and `ScaffoldPlan`: frozen dataclasses, small scalar fields, explicit `as_dict()` for inspection and artifact-safe serialization.

**Registry validation pattern** (`src/eml_symbolic_regression/benchmark.py` lines 288-295):

```python
allowed_scaffolds = {"exp", "log", "scaled_exp"}
unknown_scaffolds = sorted(set(self.scaffold_initializers) - allowed_scaffolds)
if unknown_scaffolds:
    raise BenchmarkValidationError(
        "invalid_budget",
        f"unknown scaffold initializers: {', '.join(unknown_scaffolds)}",
        path=f"{path}.scaffold_initializers",
    )
```

Replace the local literal set at call sites with a registry helper such as `known_scaffold_kinds()`. Keep validation fail-closed for unknown names.

**Exclusion code pattern** (`src/eml_symbolic_regression/benchmark.py` lines 951-972):

```python
def _operator_variant_budget(base: OptimizerBudget, variant: _OperatorVariant) -> OptimizerBudget:
    scaffold_initializers = base.scaffold_initializers
    scaffold_exclusions = base.scaffold_exclusions
    if not variant.operator_family.is_raw:
        removed = tuple(scaffold for scaffold in scaffold_initializers if scaffold == "scaled_exp")
        scaffold_initializers = tuple(scaffold for scaffold in scaffold_initializers if scaffold != "scaled_exp")
        if removed:
            scaffold_exclusions = tuple(
                dict.fromkeys(
                    (
                        *scaffold_exclusions,
                        "scaled_exp:centered_family_incompatible_raw_witness",
                    )
                )
            )
    return replace(
        base,
        scaffold_initializers=scaffold_initializers,
        scaffold_exclusions=scaffold_exclusions,
        operator_family=variant.operator_family,
        operator_schedule=variant.operator_schedule,
    )
```

Move this ad hoc logic into the registry resolver. Preserve ordered de-duplication with `tuple(dict.fromkeys(...))`, but use the canonical reason `centered_family_same_family_witness_missing` for `exp`, `log`, and `scaled_exp` when the active operator family has no same-family witness.

**Core resolver shape to copy into new module:**

```python
CENTERED_FAMILY_SAME_FAMILY_WITNESS_MISSING = "centered_family_same_family_witness_missing"


@dataclass(frozen=True)
class ScaffoldWitness:
    kind: str
    operator_family: str
    attempt_kind: str
    min_depth: int
    strategy: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "operator_family": self.operator_family,
            "attempt_kind": self.attempt_kind,
            "min_depth": self.min_depth,
            "strategy": self.strategy,
        }


@dataclass(frozen=True)
class ScaffoldPlan:
    enabled: tuple[str, ...]
    exclusions: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {"enabled": list(self.enabled), "exclusions": list(self.exclusions)}
```

Initial registry entries should declare `exp`, `log`, and `scaled_exp` for `raw_eml` only. Do not register centered witnesses until same-family witnesses exist and are tested.

---

### `src/eml_symbolic_regression/optimize.py` (service, batch / transform)

**Analog:** `src/eml_symbolic_regression/optimize.py`

**Imports pattern** (lines 5-14):

```python
from dataclasses import dataclass, field, replace
from typing import Any, Callable, Mapping

import numpy as np
import torch

from .expression import format_constant_value
from .master_tree import ActiveSlotAlternatives, SnapDecision, SnapResult, SoftEMLTree, constant_label
from .semantics import AnomalyStats, EmlOperator, TrainingSemanticsConfig, as_complex_tensor, mse_complex_numpy, raw_eml_operator
from .verify import DataSplit, VerificationReport, verify_candidate
```

Add registry imports beside the existing local imports. Use `replace` to pass a filtered `TrainingConfig` into `_training_attempts()` rather than mutating `config`.

**Training config scaffold fields** (lines 17-42):

```python
@dataclass(frozen=True)
class TrainingConfig:
    depth: int = 2
    variables: tuple[str, ...] = ("x",)
    constants: tuple[complex, ...] = (1.0,)
    steps: int = 300
    restarts: int = 3
    seed: int = 0
    scaffold_initializers: tuple[str, ...] = ("exp", "log", "scaled_exp")
    operator_family: EmlOperator = field(default_factory=raw_eml_operator)
    operator_schedule: tuple[EmlOperator, ...] = ()
```

Do not change raw defaults. Resolve availability after config construction, based on the initial training operator.

**Attempt generation entry point** (lines 312-328):

```python
attempts = _training_attempts(config, initializer is not None)

for attempt_index, attempt in enumerate(attempts):
    restart = int(attempt["restart"])
    seed = int(attempt["seed"])
    torch.manual_seed(seed)
    model = SoftEMLTree(
        config.depth,
        config.variables,
        config.constants,
        operator_family=_operator_for_step(config, 0, max(config.steps, 1)),
    )
    model.reset_parameters(seed=seed, scale=0.25)
    if initializer is not None:
        initialization_log = initializer(model, restart, seed)
    elif attempt["kind"].startswith("scaffold_"):
        initialization_log = _apply_scaffold(model, attempt)
```

Compute `initial_operator = _operator_for_step(config, 0, max(config.steps, 1))` once near this block, resolve the scaffold plan, and use the same initial operator for both the model and registry lookup. This closes direct `fit_eml_tree()` callers, not only benchmark suite expansion.

**Training attempts pattern** (lines 486-526):

```python
def _training_attempts(config: TrainingConfig, has_external_initializer: bool) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    if not has_external_initializer:
        for scaffold in config.scaffold_initializers:
            if scaffold not in {"exp", "log", "scaled_exp"}:
                continue
            if scaffold == "log" and config.depth < 3:
                continue
            if scaffold == "scaled_exp" and config.depth < 9:
                continue
            for variable in config.variables:
                if scaffold == "scaled_exp":
                    for coefficient in _scaled_exp_constants(config.constants):
                        attempts.append(
                            {
                                "kind": "scaffold_scaled_exp",
                                "variable": variable,
                                "coefficient": coefficient,
                                "restart": -1,
                                "seed": config.seed,
                            }
                        )
                else:
                    attempts.append(
                        {
                            "kind": f"scaffold_{scaffold}",
                            "variable": variable,
                            "restart": -1,
                            "seed": config.seed,
                        }
                    )
    for restart in range(config.restarts):
        attempts.append(
            {
                "kind": "random",
                "variable": None,
                "restart": restart,
                "seed": config.seed + restart,
            }
        )
    return attempts
```

Keep depth and constant feasibility checks here. Registry availability should filter scaffold names before this loop; depth skips should remain silent skips, not same-family witness exclusions.

**Operator schedule pattern** (lines 529-539):

```python
def _operator_for_step(config: TrainingConfig, step: int, total_steps: int) -> EmlOperator:
    if not config.operator_schedule:
        return config.operator_family
    if total_steps <= 1:
        return config.operator_schedule[-1]
    bucket = int((max(step, 0) * len(config.operator_schedule)) / total_steps)
    return config.operator_schedule[min(bucket, len(config.operator_schedule) - 1)]


def _final_operator(config: TrainingConfig) -> EmlOperator:
    return config.operator_schedule[-1] if config.operator_schedule else config.operator_family
```

Use `_operator_for_step(..., 0, ...)`, not `_final_operator()`, for scaffold witness availability. Continuation runs apply scaffolds before final hardening.

**Manifest pattern** (lines 448-472):

```python
manifest = {
    "schema": "eml.run_manifest.v1",
    "config": _training_config_payload(config),
    "operator_trace": _operator_trace(config),
    "best_restart": best_log,
    "restarts": restart_logs,
    "candidates": [candidate.as_dict() for candidate in ranked_candidates],
    "selection": {
        "mode": selection_mode,
        "candidate_count": len(candidates),
        "selected_candidate_id": selected_candidate.candidate_id,
        "fallback_candidate_id": fallback_candidate.candidate_id,
    },
    "selected_candidate": selected_candidate.as_dict(),
    "fallback_candidate": fallback_candidate.as_dict(),
    "snap": selected_candidate.snap.as_dict(),
    "best_loss": selected_candidate.best_fit_loss,
    "legacy_best_loss": legacy_best_loss,
    "post_snap_loss": selected_candidate.post_snap_loss,
    "status": status,
}
```

Add optimizer-level `scaffold_exclusions` to the manifest. Keep the serialized `config` reflecting the effective filtered `scaffold_initializers` so artifacts prove centered runs did not receive raw scaffold attempts.

**Scaffold helper dispatch pattern** (lines 603-629):

```python
def _apply_scaffold(model: SoftEMLTree, attempt: Mapping[str, Any]) -> dict[str, Any]:
    kind = str(attempt["kind"])
    variable = str(attempt["variable"])
    if kind == "scaffold_exp":
        model.force_exp(variable)
    elif kind == "scaffold_log":
        model.force_log(variable)
    elif kind == "scaffold_scaled_exp":
        coefficient = complex(attempt["coefficient"])
        embedding = model.force_scaled_exp(variable, coefficient)
        return {
            "kind": kind,
            "variable": variable,
            "coefficient": format_constant_value(coefficient),
            "constant_label": constant_label(coefficient),
            "seed": attempt["seed"],
            "strategy": "paper_scaled_exponential_family",
            "embedding": embedding.as_dict(),
        }
    else:
        raise ValueError(f"unknown scaffold initializer {kind!r}")
```

Guard dispatch through the registry before invoking raw helper methods. If a non-raw operator reaches this boundary, fail closed with the same canonical reason code.

---

### `src/eml_symbolic_regression/benchmark.py` (service / orchestrator, batch / file-I/O)

**Analog:** `src/eml_symbolic_regression/benchmark.py`

**Imports pattern** (lines 13-17, 22-38):

```python
from copy import deepcopy
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

from .optimize import TrainingConfig, fit_eml_tree
from .semantics import AnomalyStats, EmlOperator, as_complex_tensor, eml_operator_from_spec, mse_complex_numpy, raw_eml_operator
```

Add witness registry imports beside the local imports. Keep benchmark-specific validation errors local to `benchmark.py`; the registry should provide data and reason strings.

**Budget parse and serialize pattern** (lines 177-192, 304-331):

```python
scaffold_initializers = values["scaffold_initializers"]
if not isinstance(scaffold_initializers, (list, tuple)):
    raise BenchmarkValidationError(
        "malformed_budget",
        "scaffold_initializers must be a list",
        path=f"{path}.scaffold_initializers",
    )
values["scaffold_initializers"] = tuple(str(value) for value in scaffold_initializers)
scaffold_exclusions = values["scaffold_exclusions"]
if not isinstance(scaffold_exclusions, (list, tuple)):
    raise BenchmarkValidationError(
        "malformed_budget",
        "scaffold_exclusions must be a list",
        path=f"{path}.scaffold_exclusions",
    )
values["scaffold_exclusions"] = tuple(str(value) for value in scaffold_exclusions)
```

```python
def as_dict(self) -> dict[str, Any]:
    return {
        "scaffold_initializers": list(self.scaffold_initializers),
        "scaffold_exclusions": list(self.scaffold_exclusions),
        "operator_family": self.operator_family.as_dict(),
        "operator_schedule": [operator.as_dict() for operator in self.operator_schedule],
    }
```

Keep `scaffold_exclusions` string-compatible for existing artifacts. Operator context already travels beside it through `operator_family` and `operator_schedule`.

**Operator variant filtering pattern** (lines 951-972):

```python
def _operator_variant_budget(base: OptimizerBudget, variant: _OperatorVariant) -> OptimizerBudget:
    scaffold_initializers = base.scaffold_initializers
    scaffold_exclusions = base.scaffold_exclusions
    if not variant.operator_family.is_raw:
        removed = tuple(scaffold for scaffold in scaffold_initializers if scaffold == "scaled_exp")
        scaffold_initializers = tuple(scaffold for scaffold in scaffold_initializers if scaffold != "scaled_exp")
        if removed:
            scaffold_exclusions = tuple(
                dict.fromkeys(
                    (
                        *scaffold_exclusions,
                        "scaled_exp:centered_family_incompatible_raw_witness",
                    )
                )
            )
    return replace(
        base,
        scaffold_initializers=scaffold_initializers,
        scaffold_exclusions=scaffold_exclusions,
        operator_family=variant.operator_family,
        operator_schedule=variant.operator_schedule,
    )
```

Replace with `resolve_scaffold_plan(base.scaffold_initializers, initial_operator)`, where the initial operator is `variant.operator_schedule[0]` when present, otherwise `variant.operator_family`. The new exclusion strings should be:

```text
exp:centered_family_same_family_witness_missing
log:centered_family_same_family_witness_missing
scaled_exp:centered_family_same_family_witness_missing
```

**Budget initial operator helper** (lines 1952-1953):

```python
def _budget_operator_family(budget: OptimizerBudget) -> EmlOperator:
    return budget.operator_schedule[0] if budget.operator_schedule else budget.operator_family
```

Use this helper when resolving benchmark budget scaffold availability, because it already encodes "initial schedule operator wins".

**Training config propagation pattern** (lines 1999-2029):

```python
def _training_config_from_budget(
    run: BenchmarkRun,
    *,
    variable: str,
    depth: int,
    steps: int,
    restarts: int,
    seed: int,
    scaffold_initializers: tuple[str, ...] | None = None,
) -> TrainingConfig:
    return TrainingConfig(
        depth=depth,
        variables=(variable,),
        constants=run.optimizer.constants,
        steps=steps,
        restarts=restarts,
        seed=seed,
        scaffold_initializers=run.optimizer.scaffold_initializers if scaffold_initializers is None else scaffold_initializers,
        operator_family=run.optimizer.operator_schedule[0] if run.optimizer.operator_schedule else run.optimizer.operator_family,
        operator_schedule=run.optimizer.operator_schedule,
    )
```

This should receive already-filtered benchmark budgets. Do not re-enable defaults here.

**Run artifact and metrics pattern** (lines 1540-1553, 2406-2472):

```python
def _base_run_payload(run: BenchmarkRun) -> dict[str, Any]:
    return {
        "schema": "eml.benchmark_run.v1",
        "run": run.as_dict(),
        "dataset": run.dataset.as_dict(),
        "budget": run.optimizer.as_dict(),
        "status": "pending",
    }
```

```python
return {
    "operator_family": candidate_operator.get("label") or budget_operator.get("label"),
    "operator_schedule": candidate_schedule_label or budget_schedule_label,
    "scaffold_exclusions": list(budget.get("scaffold_exclusions", ())) if isinstance(budget, Mapping) else [],
    "unsupported_reason": _run_reason(payload) if payload.get("status") == "unsupported" else None,
}
```

Because `_base_run_payload()` stores `budget` and `_extract_run_metrics()` copies `budget.scaffold_exclusions`, planner should not add a parallel artifact field unless a test proves a gap. Add optimizer-manifest exclusions separately for direct optimizer callers.

**Aggregate survival pattern** (lines 2579-2605, 2805-2832):

```python
def aggregate_evidence(result: BenchmarkSuiteResult) -> dict[str, Any]:
    runs = [_run_summary(item) for item in result.results]
    return {
        "schema": "eml.benchmark_aggregate.v1",
        "suite": result.suite.as_dict(),
        "counts": _aggregate_counts(runs),
        "runs": runs,
    }
```

```python
return {
    "run_id": result.run.run_id,
    "optimizer": result.run.optimizer.as_dict(),
    "reason": _run_reason(payload),
    "metrics": payload.get("metrics", {}),
    "stage_statuses": payload.get("stage_statuses", {}),
}
```

Aggregate tests should inspect `aggregate["runs"][0]["metrics"]["scaffold_exclusions"]` if centered scaffold exclusions need explicit aggregate coverage.

---

### `src/eml_symbolic_regression/master_tree.py` (model / utility, transform)

**Analog:** `src/eml_symbolic_regression/master_tree.py`

**Imports pattern** (lines 5-12):

```python
import json
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

import torch

from .expression import CenteredEml, Const, Eml, Expr, Var
from .semantics import AnomalyStats, EmlOperator, TrainingSemanticsConfig, as_complex_tensor, centered_eml_torch, raw_eml_operator
```

If helper guards live in this file, import only constants/functions from `witnesses.py`. Keep `witnesses.py` dependency-light so this import is acyclic.

**Existing error type pattern** (lines 215-222):

```python
class EmbeddingError(ValueError):
    def __init__(self, reason: str, detail: str) -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason}: {detail}")

    def as_dict(self) -> dict[str, str]:
        return {"reason": self.reason, "detail": self.detail}
```

Use `EmbeddingError` for direct helper fail-closed behavior in `force_exp()`, `force_log()`, and `force_scaled_exp()`. The `reason` should be `centered_family_same_family_witness_missing`.

**Raw helper methods to guard** (lines 556-574):

```python
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
```

Add the witness guard before any slot mutation or expression embedding. This prevents custom initializers from bypassing optimizer and benchmark filtering.

**Operator mismatch guard pattern** (lines 618-623, 662-667):

```python
if expression_operator != tree.operator_family:
    raise EmbeddingError(
        "operator_family_mismatch",
        f"tree operator {tree.operator_family.label} cannot embed {expression_operator.label}",
    )
```

Model guard errors should follow this style: short machine reason plus detail containing both scaffold kind and operator label.

---

### `src/eml_symbolic_regression/__init__.py` (config / public API, static export)

**Analog:** `src/eml_symbolic_regression/__init__.py`

**Import/export pattern** (lines 3-18, 20-52):

```python
from .compiler import CompilerConfig, CompileResult, UnsupportedExpression, compile_and_validate, compile_sympy_expression
from .expression import CenteredEml, Const, Eml, Expr, SympyCandidate, Var, ceml_expr, ceml_s_expr, exp_expr, log_expr, zeml_s_expr
from .master_tree import EmbeddingConfig, SoftEMLTree, embed_expr_into_tree
from .semantics import (
    EmlOperator,
    ceml_operator,
    ceml_s_operator,
    centered_eml_numpy,
    centered_eml_torch,
    eml_numpy,
    eml_operator_from_spec,
    eml_torch,
    raw_eml_operator,
    zeml_s_operator,
)
from .verify import VerificationReport, verify_candidate

__all__ = [
    "Const",
    "CenteredEml",
    "CompilerConfig",
]
```

If WIT-01 is satisfied through top-level inspection, add witness exports here and append them to `__all__`. If planner keeps inspection module-scoped, leave this file untouched and use `from eml_symbolic_regression.witnesses import ...` in tests.

---

### `tests/test_benchmark_contract.py` (test, request-response / validation)

**Analog:** `tests/test_benchmark_contract.py`

**Imports pattern** (lines 1-15):

```python
import json

import pytest

from eml_symbolic_regression.benchmark import (
    BenchmarkCase,
    BenchmarkSuite,
    BenchmarkValidationError,
    OptimizerBudget,
    builtin_suite,
    list_builtin_suites,
    load_suite,
)
```

Add witness registry imports here for WIT-01 inspection tests if the module API is not covered elsewhere.

**Family matrix scaffold exclusion contract** (lines 55-80):

```python
def test_family_matrix_suites_clone_regimes_with_operator_variants():
    suite = load_suite("v1.7-family-shallow-pure-blind")
    runs = suite.expanded_runs()

    assert len(runs) == 72
    assert {"shallow-exp-pure-blind-raw", "shallow-exp-pure-blind-ceml2", "shallow-exp-pure-blind-zeml8-4"} <= {
        run.case_id for run in runs
    }
    assert {"raw_eml", "CEML_2", "ZEML_2", "ZEML_8"} <= {
        run.optimizer.operator_family.label for run in runs
    }
    assert any([operator.label for operator in run.optimizer.operator_schedule] == ["ZEML_8", "ZEML_4"] for run in runs)

    shallow = load_suite("v1.7-family-shallow")
    centered_scaffolded = [
        run for run in shallow.expanded_runs() if run.case_id == "shallow-beer-lambert-blind-ceml2"
    ]
    assert centered_scaffolded
    assert "scaled_exp" not in centered_scaffolded[0].optimizer.scaffold_initializers
    assert centered_scaffolded[0].optimizer.scaffold_exclusions == (
        "scaled_exp:centered_family_incompatible_raw_witness",
    )
```

Update this test to assert all raw scaffold names are excluded for centered variants and that the old reason code is gone. Preserve run-count and regime-shape assertions.

**Budget validation pattern** (lines 293-319):

```python
budget = OptimizerBudget.from_mapping(
    {"depth": 9, "constants": ["-0.8", {"real": "0.4", "imag": "0"}], "scaffold_initializers": ["scaled_exp"]}
)

assert budget.constants == (complex(-0.8), complex(0.4))
assert budget.scaffold_initializers == ("scaled_exp",)
assert budget.as_dict()["constants"] == ["-0.8", "0.4"]
assert budget.as_dict()["scaffold_initializers"] == ["scaled_exp"]

with pytest.raises(BenchmarkValidationError) as exc:
    OptimizerBudget.from_mapping({"scaffold_initializers": ["bad"]}).validate("optimizer")

assert exc.value.reason == "invalid_budget"
assert exc.value.path == "optimizer.scaffold_initializers"
```

If registry replaces the hardcoded allowed set, add a contract assertion that known registry names are accepted and unknown names still fail with the same `BenchmarkValidationError`.

**Operator schedule validation pattern** (lines 322-351):

```python
budget = OptimizerBudget.from_mapping(
    {
        "operator_family": {"family": "ceml_s", "s": 2},
        "operator_schedule": ["zeml_s:8", "zeml_s:4"],
    }
)

assert budget.operator_family.label == "CEML_2"
assert [operator.label for operator in budget.operator_schedule] == ["ZEML_8", "ZEML_4"]
assert budget.as_dict()["operator_family"]["label"] == "CEML_2"
assert [item["label"] for item in budget.as_dict()["operator_schedule"]] == ["ZEML_8", "ZEML_4"]
```

Add continuation-specific centered scaffold exclusion assertions here: schedule `["ZEML_8", "ZEML_4"]` should use `ZEML_8` as the scaffold availability operator.

---

### `tests/test_benchmark_runner.py` (test, file-I/O / artifact)

**Analog:** `tests/test_benchmark_runner.py`

**Imports pattern** (lines 1-31):

```python
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import sympy as sp
import torch

import eml_symbolic_regression.benchmark as benchmark_module
from eml_symbolic_regression.benchmark import (
    BenchmarkCase,
    BenchmarkRun,
    BenchmarkSuite,
    DatasetConfig,
    OptimizerBudget,
    RunFilter,
    builtin_suite,
    evidence_class_for_payload,
    execute_benchmark_run,
    run_benchmark_suite,
)
```

Keep runner tests at artifact level: read JSON files, assert serialized budget/config/metrics, and inspect aggregate summaries.

**Artifact equality pattern** (lines 146-163):

```python
def test_runner_executes_operator_family_smoke_matrix(tmp_path):
    base = builtin_suite("v1.7-family-smoke")
    suite = type(base)(base.id, base.description, base.cases, tmp_path / "artifacts")

    result = run_benchmark_suite(
        suite,
        run_filter=RunFilter(case_ids=("exp-blind-ceml2", "exp-blind-zeml8-4"), seeds=(0,)),
    )

    assert len(result.results) == 2
    for item in result.results:
        artifact = json.loads(item.artifact_path.read_text(encoding="utf-8"))
        assert artifact["budget"] == item.run.optimizer.as_dict()
        assert artifact["budget"]["operator_family"]["label"] in {"CEML_2", "ZEML_8"}
        assert artifact["trained_eml_candidate"]["config"]["operator_family"]["label"] in {"CEML_2", "ZEML_8"}
        assert artifact["metrics"]["operator_family"] in {"CEML_2", "ZEML_8"}
```

Extend this pattern to assert centered blind runs have no `scaffold_*` attempt kinds and that `artifact["metrics"]["scaffold_exclusions"]` equals the budget exclusions.

**Unsupported reason aggregate pattern** (lines 185-201):

```python
def test_centered_perturbed_tree_unsupported_reason_survives_aggregate(tmp_path):
    base = builtin_suite("v1.8-family-basin")
    suite = type(base)(base.id, base.description, base.cases, tmp_path / "artifacts")

    result = run_benchmark_suite(
        suite,
        run_filter=RunFilter(case_ids=("basin-depth1-perturbed-ceml2",), seeds=(0,)),
    )
    artifact = json.loads(result.results[0].artifact_path.read_text(encoding="utf-8"))
    aggregate = benchmark_module.aggregate_evidence(result)

    assert result.results[0].status == "unsupported"
    assert artifact["perturbed_true_tree"]["reason"] == "centered_family_same_family_seed_missing"
    assert artifact["metrics"]["unsupported_reason"] == "centered_family_same_family_seed_missing"
    assert aggregate["runs"][0]["reason"] == "centered_family_same_family_seed_missing"
```

Use the same aggregate pattern for scaffold exclusions if planner adds aggregate-specific assertions. Preserve the existing seed-missing reason; do not replace it with witness-missing.

**Raw scaffold diagnostic preservation pattern** (lines 247-270):

```python
def test_shallow_beer_lambert_blind_run_artifact_exposes_scaled_scaffold_diagnostics(tmp_path):
    base = builtin_suite("v1.5-shallow-proof")
    suite = type(base)(base.id, base.description, base.cases, tmp_path / "artifacts")

    result = run_benchmark_suite(
        suite,
        run_filter=RunFilter(case_ids=("shallow-beer-lambert-blind",), seeds=(0,)),
    )
    artifact = json.loads(result.results[0].artifact_path.read_text(encoding="utf-8"))
    candidate = artifact["trained_eml_candidate"]
    initialization = candidate["best_restart"]["initialization"]
    metrics = artifact["metrics"]

    assert result.results[0].status == "recovered"
    assert initialization["kind"] == "scaffold_scaled_exp"
    assert initialization["strategy"] == "paper_scaled_exponential_family"
    assert metrics["scaffold_source"] == "scaffold_scaled_exp"
    assert metrics["scaffold_strategy"] == "paper_scaled_exponential_family"
    assert metrics["scaffold_coefficient"] == "-0.8"
```

Keep this as a raw-regression guard: raw EML budgets should still use the existing scaffold helpers.

---

### `tests/test_optimizer_cleanup.py` (test, batch / optimizer manifest)

**Analog:** `tests/test_optimizer_cleanup.py`

**Imports pattern** (lines 1-8):

```python
import numpy as np

from eml_symbolic_regression.cleanup import cleanup_candidate
from eml_symbolic_regression.datasets import get_demo
from eml_symbolic_regression.expression import Const, Var, ceml_s_expr
from eml_symbolic_regression.optimize import TrainingConfig, fit_eml_tree
from eml_symbolic_regression.semantics import ceml_s_operator, zeml_s_operator
from eml_symbolic_regression.verify import verify_candidate
```

Add `pytest` only if asserting fail-closed exceptions. For direct helper guard tests, prefer importing `EmbeddingError` / `SoftEMLTree` or place helper-specific coverage in `tests/test_master_tree.py` using the analog below.

**Raw exp scaffold manifest pattern** (lines 24-37):

```python
def test_optimizer_scaffold_recovers_exp_with_manifest_provenance():
    spec = get_demo("exp")
    splits = spec.make_splits(points=16)
    result = fit_eml_tree(
        splits[0].inputs,
        splits[0].target,
        TrainingConfig(depth=1, variables=("x",), steps=2, restarts=1, seed=0),
    )
    report = verify_candidate(result.snap.expression, splits)
    kinds = [(attempt.get("initialization") or {}).get("kind") for attempt in result.manifest["restarts"]]

    assert report.status == "recovered"
    assert "scaffold_exp" in kinds
```

Keep this raw-default behavior unchanged. Add separate centered tests rather than weakening this assertion.

**Centered optimizer manifest pattern** (lines 39-59):

```python
def test_optimizer_runs_fixed_centered_family_with_manifest_metadata():
    x = np.linspace(-1.0, 1.0, 16)
    target = 2.0 * np.expm1(x / 2.0)
    expected = ceml_s_expr(Var("x"), Const(1.0), s=2.0)
    result = fit_eml_tree(
        {"x": x},
        target,
        TrainingConfig(
            depth=1,
            variables=("x",),
            steps=2,
            restarts=1,
            seed=0,
            operator_family=ceml_s_operator(2.0),
        ),
    )

    assert result.snap.expression.to_node()["operator"]["label"] == "CEML_2"
    assert result.manifest["config"]["operator_family"]["label"] == "CEML_2"
```

Extend this test to assert the centered optimizer manifest records witness exclusions and that no restart has an `attempt_kind` beginning with `scaffold_`.

**Schedule metadata pattern** (lines 61-83):

```python
def test_optimizer_preserves_centered_schedule_metadata():
    x = np.linspace(-1.0, 1.0, 16)
    target = np.expm1(x)
    result = fit_eml_tree(
        {"x": x},
        target,
        TrainingConfig(
            depth=1,
            variables=("x",),
            steps=4,
            restarts=1,
            seed=0,
            operator_schedule=(zeml_s_operator(8.0), zeml_s_operator(4.0)),
            scaffold_initializers=(),
        ),
    )

    assert result.manifest["config"]["operator_schedule"][0]["label"] == "ZEML_8"
    assert result.manifest["config"]["operator_schedule"][1]["label"] == "ZEML_4"
    assert [item["operator"]["label"] for item in result.manifest["operator_trace"][:2]] == ["ZEML_8", "ZEML_4"]
```

Add a variant with default scaffold initializers if planner wants optimizer-level schedule coverage. It should prove witness exclusions are based on `ZEML_8`, the initial schedule operator.

**Scaled raw scaffold preservation pattern** (lines 140-170):

```python
def test_optimizer_scaled_exp_scaffold_recovers_radioactive_decay_with_manifest():
    spec = get_demo("radioactive_decay")
    splits = spec.make_splits(points=12, seed=0)

    result = fit_eml_tree(
        splits[0].inputs,
        splits[0].target,
        TrainingConfig(
            depth=9,
            variables=("t",),
            constants=(-0.4,),
            steps=2,
            restarts=1,
            seed=0,
            scaffold_initializers=("scaled_exp",),
        ),
    )
    report = verify_candidate(result.snap.expression, splits)
    best_restart = result.manifest["best_restart"]
    initialization = best_restart["initialization"]

    assert report.status == "recovered"
    assert best_restart["attempt_kind"] == "scaffold_scaled_exp"
    assert initialization["kind"] == "scaffold_scaled_exp"
    assert initialization["strategy"] == "paper_scaled_exponential_family"
    assert initialization["embedding"]["success"] is True
```

Leave raw scaled-exponential behavior intact.

**Direct helper guard analog** (`tests/test_master_tree.py` lines 19-82):

```python
def test_force_exp_snaps_to_paper_identity():
    tree = SoftEMLTree(1, ("x",))
    tree.force_exp("x")
    snap = tree.snap()
    x = np.linspace(-1.0, 1.0, 10)
    np.testing.assert_allclose(snap.expression.evaluate_numpy({"x": x}), np.exp(x), atol=1e-12)
    assert snap.min_margin > 0.99

def test_centered_embedding_requires_matching_operator_family():
    tree = SoftEMLTree(1, ("x",), operator_family=zeml_s_operator(2.0))

    with pytest.raises(EmbeddingError, match="operator_family_mismatch"):
        tree.embed_expr(ceml_s_expr(tree.snap().expression.left, tree.snap().expression.right, s=2.0))
```

If direct `SoftEMLTree.force_*` guard coverage is added outside optimizer tests, copy this `pytest.raises(EmbeddingError, match=...)` style and assert the new reason code.

## Shared Patterns

### Operator Family Metadata

**Source:** `src/eml_symbolic_regression/semantics.py` lines 12-84
**Apply to:** `witnesses.py`, `benchmark.py`, `optimize.py`, `master_tree.py`

```python
@dataclass(frozen=True)
class EmlOperator:
    family: str = "raw_eml"

    @property
    def is_raw(self) -> bool:
        return self.family == "raw_eml"

    @property
    def label(self) -> str:
        if self.family == "raw_eml":
            return "raw_eml"
        if self.family == "ceml_s":
            return f"CEML_{_format_number(self.s)}"
        if self.family == "zeml_s":
            return f"ZEML_{_format_number(self.s)}"
        return f"cEML_s{_format_number(self.s)}_t{_format_complex(self.t)}"
```

Registry decisions should be keyed by `operator.family`, while artifacts should carry `operator.as_dict()` / `operator.label`.

### Exclusion String Format

**Source:** `src/eml_symbolic_regression/benchmark.py` lines 958-965
**Apply to:** `witnesses.py`, `benchmark.py`, `optimize.py`, runner tests

```python
scaffold_exclusions = tuple(
    dict.fromkeys(
        (
            *scaffold_exclusions,
            "scaled_exp:centered_family_incompatible_raw_witness",
        )
    )
)
```

Keep the `kind:reason` string format, but replace the reason with `centered_family_same_family_witness_missing` for centered scaffold witness exclusions.

### Initial Operator For Schedules

**Source:** `src/eml_symbolic_regression/benchmark.py` lines 1952-1953 and `src/eml_symbolic_regression/optimize.py` lines 529-535
**Apply to:** benchmark budget filtering and optimizer attempt filtering

```python
def _budget_operator_family(budget: OptimizerBudget) -> EmlOperator:
    return budget.operator_schedule[0] if budget.operator_schedule else budget.operator_family
```

```python
def _operator_for_step(config: TrainingConfig, step: int, total_steps: int) -> EmlOperator:
    if not config.operator_schedule:
        return config.operator_family
    if total_steps <= 1:
        return config.operator_schedule[-1]
    bucket = int((max(step, 0) * len(config.operator_schedule)) / total_steps)
    return config.operator_schedule[min(bucket, len(config.operator_schedule) - 1)]
```

Use the operator at step 0 for scaffold availability. Use final operator only for hardening and final exact node semantics.

### Artifact Visibility

**Source:** `src/eml_symbolic_regression/benchmark.py` lines 1540-1553 and 2469-2472
**Apply to:** `benchmark.py`, `tests/test_benchmark_runner.py`

```python
"budget": run.optimizer.as_dict(),
```

```python
"scaffold_exclusions": list(budget.get("scaffold_exclusions", ())) if isinstance(budget, Mapping) else [],
```

Benchmark budget exclusions already survive into run artifacts and metrics. Tests should assert the exact serialized payloads.

### Fail-Closed Exceptions

**Source:** `src/eml_symbolic_regression/master_tree.py` lines 215-222 and 618-623
**Apply to:** direct helper guards in `master_tree.py`, optimizer dispatch guard in `optimize.py`

```python
class EmbeddingError(ValueError):
    def __init__(self, reason: str, detail: str) -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason}: {detail}")
```

```python
raise EmbeddingError(
    "operator_family_mismatch",
    f"tree operator {tree.operator_family.label} cannot embed {expression_operator.label}",
)
```

Use structured reasons, not silent skips, when an incompatible direct helper is invoked.

## No Analog Found

No file lacks a close implementation or test analog. There is no existing witness registry module, but `semantics.py` and `benchmark.py` together provide the frozen metadata, validation, and artifact serialization patterns needed for `witnesses.py`.

## Metadata

**Analog search scope:** `src/eml_symbolic_regression/`, `tests/`, phase `CONTEXT.md`, phase `RESEARCH.md`
**Files scanned:** 43 source/test files
**Pattern extraction date:** 2026-04-17

