# Phase 51: Reciprocal and Saturation Compiler Motifs - Pattern Map

**Mapped:** 2026-04-17
**Files analyzed:** 9 expected source/test/doc files
**Analogs found:** 9 / 9

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `src/eml_symbolic_regression/compiler.py` | utility / compiler service | transform, fail-closed diagnostics | existing macro layer: `direct_division_template`, `scaled_exp_minus_one_template`, `_macro_diagnostics()` | exact |
| `tests/test_compiler_warm_start.py` | test | transform, request-response, file-I/O | existing Shockley/Arrhenius macro tests, Michaelis unsupported diagnostic test, CLI artifact tests | exact |
| `src/eml_symbolic_regression/cli.py` | CLI controller | request-response, file-I/O | generic `run_demo()` compile/warm-start serialization | exact, likely no production edit |
| `src/eml_symbolic_regression/benchmark.py` | service / config registry | batch, file-I/O | `v1.2-evidence` Michaelis diagnostic row, focused `v1.9-arrhenius-evidence` suite, generic warm-start runner | exact |
| `tests/test_benchmark_contract.py` | test | config validation, batch | built-in suite registry and focused Arrhenius suite contract tests | exact |
| `tests/test_benchmark_runner.py` | test | batch, file-I/O | Shockley and Arrhenius warm-start artifact assertions | exact |
| `docs/IMPLEMENTATION.md` | documentation | reporting | compiler contract, benchmark evidence contract, demo ladder sections | exact |
| `README.md` | documentation | reporting | quick commands, demo statuses, benchmark evidence, limits sections | exact |
| `src/eml_symbolic_regression/datasets.py` | model / dataset registry | batch, transform | existing `michaelis_menten` `DemoSpec` and Arrhenius reciprocal example | reference-only exact |

`src/eml_symbolic_regression/datasets.py` should be treated as a reference unless implementation discovers a real demo-spec bug. The Phase 51 target formula already exists as `michaelis_menten`; motif support belongs in the reusable compiler layer, not in the dataset registry.

## Pattern Assignments

### `src/eml_symbolic_regression/compiler.py` (utility / compiler service, transform)

**Analog:** `src/eml_symbolic_regression/compiler.py`

**Imports and config pattern** (lines 5-11, 25-33):

```python
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

import numpy as np
import sympy as sp

from .expression import Const, Eml, Expr, Var, exp_of, format_constant_value, log_of
```

```python
@dataclass(frozen=True)
class CompilerConfig:
    variables: tuple[str, ...] | None = None
    constant_policy: str = "literal_constants"
    max_depth: int = 13
    max_nodes: int = 256
    max_power: int = 3
    validation_tolerance: float = 1e-8
    enable_macros: bool = True
```

Use the existing SymPy/Python stdlib surface. New motif helpers should not add dependencies or new public config unless the planner has a specific reason.

**Metadata and macro registry pattern** (lines 54-80, 121-124):

```python
@dataclass(frozen=True)
class CompileMetadata:
    source_expression: str
    normalized_expression: str
    variables: tuple[str, ...]
    constants: tuple[complex, ...]
    constant_policy: str
    depth: int
    node_count: int
    assumptions: tuple[str, ...]
    trace: tuple[RuleTrace, ...]
    unsupported_reason: str | None = None
    macro_diagnostics: Mapping[str, Any] | None = None
```

```python
MACRO_RULES = (
    "direct_division_template",
    "scaled_exp_minus_one_template",
)
```

Add `reciprocal_shift_template` and `saturation_ratio_template` to `MACRO_RULES` so hits, misses, depth deltas, and node deltas are reported automatically. Keep names structural; do not name a macro after `michaelis_menten`.

**Arithmetic helper pattern to reuse** (lines 180-194):

```python
def divide_expr(left: Expr, right: Expr) -> Expr:
    """Verified EML identity for left / right."""

    one = Const(1.0)
    return Eml(
        Eml(
            Eml(one, Eml(Eml(one, Eml(one, right)), one)),
            Eml(Eml(one, left), one),
        ),
        one,
    )


def reciprocal_expr(expr: Expr) -> Expr:
    return divide_expr(Const(1.0), expr)
```

Build new motifs from existing exact identities (`add_expr`, `multiply_expr`, `divide_expr`, `reciprocal_expr`) rather than inventing a second arithmetic encoding.

**Macro dispatch pattern** (lines 252-261):

```python
def _compile_special(self, expr: sp.Expr) -> Expr | None:
    if not self.config.enable_macros:
        return None
    if isinstance(expr, sp.Mul):
        macro = self._compile_direct_division(expr)
        if macro is not None:
            return macro
    if isinstance(expr, sp.Add):
        return self._compile_scaled_exp_minus_one(expr)
    return None
```

Extend this dispatch structurally:

- Add a `sp.Pow` branch for reciprocal motifs such as `(x + b)**-1`.
- Add a `sp.Mul` saturation branch for shapes like `a*x*(x+b)**-1`.
- Keep branch order explicit. If `saturation_ratio_template` is more specific than `direct_division_template`, try it before the generic direct-division shortcut.
- Return `None` on non-matches so the ordinary compiler path can either compile generically or fail closed.

**Reusable direct-division macro style** (lines 263-287):

```python
def _compile_direct_division(self, expr: sp.Mul) -> Expr | None:
    numerator_factors: list[sp.Expr] = []
    denominator_factors: list[sp.Expr] = []
    for factor in expr.args:
        if isinstance(factor, sp.Pow) and factor.exp == -1:
            denominator_factors.append(factor.base)
        else:
            numerator_factors.append(factor)
    if not denominator_factors:
        return None
    numerator = sp.Mul(*numerator_factors)
    if sp.simplify(numerator - 1) == 0:
        return None
    denominator = sp.Mul(*denominator_factors)
    try:
        compiled_numerator = self.compile(numerator)
        compiled_denominator = self.compile(denominator)
    except UnsupportedExpression:
        return None
    self.assumptions.append("direct division shortcut lowers numerator/denominator once before exact divide identity")
    return self._record(
        "direct_division_template",
        expr,
        divide_expr(compiled_numerator, compiled_denominator),
    )
```

Copy this structure for Phase 51 helpers:

- Parse SymPy structure into symbolic pieces.
- Reject non-matches with `return None`.
- Compile subexpressions through `self.compile(...)`.
- Catch `UnsupportedExpression` inside the macro and return `None`.
- Add a concise assumption.
- Return `self._record("<motif>_template", expr, exact_expr)`.

Do not inspect demo IDs, candidate names, or exact strings like `"2*x/(x + 0.5)"`. Structural matching should work for `1/(x+b)` and `(a*x)/(b+x)` across variables and finite literal constants.

**Existing macro template with constant extraction** (lines 289-311):

```python
def _compile_scaled_exp_minus_one(self, expr: sp.Add) -> Expr | None:
    terms = list(expr.args)
    numeric_terms = [term for term in terms if term.is_number]
    non_numeric_terms = [term for term in terms if not term.is_number]
    if len(numeric_terms) != 1 or len(non_numeric_terms) != 1:
        return None

    coeff, rest = non_numeric_terms[0].as_coeff_Mul()
    if not coeff.is_number or rest.func != sp.exp or len(rest.args) != 1:
        return None
```

Use `as_coeff_Mul()`, `is_number`, `sp.Add`, `sp.Mul`, and `sp.Pow` checks for motif decomposition. Prefer SymPy structure over string matching.

**Depth/node gate and macro diagnostics pattern** (lines 363-430):

```python
compiled = compiler.compile(source)
constants = tuple(sorted(compiled.constants(), key=lambda value: (value.real, value.imag)))
macro_hits = tuple(dict.fromkeys(entry.rule for entry in compiler.trace if entry.rule in MACRO_RULES))
macro_diagnostics = _macro_diagnostics(source, config, compiled, macro_hits) if config.enable_macros else None

if compiled.depth() > config.max_depth:
    raise UnsupportedExpression(
        CompileReason.DEPTH_EXCEEDED,
        source,
        f"compiled depth {compiled.depth()} exceeds max_depth={config.max_depth}",
    )
```

```python
return {
    "hits": list(macro_hits),
    "misses": [rule for rule in MACRO_RULES if rule not in macro_hits],
    "baseline_depth": baseline_depth,
    "baseline_node_count": baseline_nodes,
    "depth_delta": baseline_depth - compiled.depth() if baseline_depth is not None else 0,
    "node_delta": baseline_nodes - compiled.node_count() if baseline_nodes is not None else 0,
}
```

Keep the strict gate at `max_depth=13` unless a plan explicitly changes it and documents the change. Phase 51 success can be either strict recovery or honest unsupported with improved relaxed depth/node diagnostics.

**Fail-closed validation and diagnostic pattern** (lines 464-522):

```python
result = compile_sympy_expression(expression, config)
validation = validate_compiled_expression(result, inputs, tolerance=(config or CompilerConfig()).validation_tolerance)
if not validation.passed:
    raise UnsupportedExpression(
        CompileReason.VALIDATION_FAILED,
        expression,
        f"max_abs_error={validation.max_abs_error:.3e}",
    )
return CompileResult(result.expression, result.metadata, validation)
```

```python
try:
    strict = compile_and_validate(expression, config, inputs)
    return {
        "schema": "eml.compiler_diagnostic.v1",
        "status": "compiled",
        "strict": {
            "metadata": strict.metadata.as_dict(),
            "validation": strict.validation.as_dict() if strict.validation else None,
        },
    }
except UnsupportedExpression as strict_error:
    diagnostic: dict[str, Any] = {
        "schema": "eml.compiler_diagnostic.v1",
        "status": "unsupported",
        "strict": strict_error.as_dict(),
    }
```

Tests should use `diagnose_compile_expression()` when the expected outcome may remain unsupported; do not bypass validation to claim support from a raw compiled tree.

---

### `src/eml_symbolic_regression/datasets.py` (model / dataset registry, reference-only)

**Analog:** `src/eml_symbolic_regression/datasets.py`

**Michaelis-Menten target already exists** (lines 207-218):

```python
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
```

Use this as the integration target. Do not add a second Michaelis formula, do not change domains to make compilation easier, and do not encode motif support in `DemoSpec`.

**Reciprocal precedent from Arrhenius** (lines 155-167):

```python
"arrhenius": DemoSpec(
    name="arrhenius",
    variable="x",
    description="Normalized reciprocal-temperature Arrhenius law from FOR_DEMO.md.",
    target=lambda a: np.exp(-0.8 / a).astype(np.complex128),
    candidate=_sympy_candidate(sp.exp(-sp.Float("0.8") / x), "x", "arrhenius_catalog"),
    train_domain=(0.5, 3.0),
    heldout_domain=(0.6, 2.7),
    extrap_domain=(3.1, 4.2),
    source_document="sources/FOR_DEMO.md",
    source_linkage="Arrhenius law normalized reciprocal-temperature dimensionless input from FOR_DEMO.md",
    normalized_dimensionless=True,
),
```

Arrhenius proves reciprocal-looking expressions can stay generic: Phase 50 added no compiler special case for `arrhenius`.

---

### `tests/test_compiler_warm_start.py` (test, transform / request-response / file-I/O)

**Analog:** `tests/test_compiler_warm_start.py`

**Imports and CLI environment pattern** (lines 1-27):

```python
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest
import sympy as sp

from eml_symbolic_regression.compiler import (
    CompilerConfig,
    CompileReason,
    UnsupportedExpression,
    compile_and_validate,
    compile_sympy_expression,
    diagnose_compile_expression,
)
```

Add motif tests in this file; it already owns compile diagnostics, warm-start, and CLI JSON assertions.

**Current Michaelis diagnostic test to evolve** (lines 61-77):

```python
def test_michaelis_relaxed_diagnostic_reports_direct_division_macro():
    spec = get_demo("michaelis_menten")
    splits = spec.make_splits(points=24, seed=0)
    diagnostic = diagnose_compile_expression(
        spec.candidate.to_sympy(),
        CompilerConfig(variables=(spec.variable,), max_depth=13, max_nodes=256),
        {spec.variable: splits[0].inputs[spec.variable]},
    )

    assert diagnostic["status"] == "unsupported"
    assert diagnostic["strict"]["reason"] == CompileReason.DEPTH_EXCEEDED
    relaxed_metadata = diagnostic["relaxed"]["metadata"]
    macro = relaxed_metadata["macro_diagnostics"]
    assert relaxed_metadata["depth"] <= 14
    assert macro["hits"] == ["direct_division_template"]
    assert macro["depth_delta"] > 0
    assert macro["node_delta"] > 0
```

For Phase 51, add separate structural tests before or near this one:

- `sp.Pow(x + sp.Float("0.5"), -1)` or `1 / (x + sp.Float("0.5"))` should hit `reciprocal_shift_template` or fail closed with relaxed metadata showing the macro miss/hit state.
- `sp.Float("2.0") * x / (x + sp.Float("0.5"))` should hit `saturation_ratio_template` when strict support is achieved, or show reduced relaxed depth/node count if the strict gate remains unsupported.
- The integration Michaelis test should assert the actual result honestly: strict recovered only if `diagnostic["status"] == "compiled"` / `compile_and_validate()` passes within depth 13; otherwise preserve `CompileReason.DEPTH_EXCEEDED`.

**Planck and unsupported-operator regression pattern** (lines 119-147):

```python
assert diagnostic["status"] == "unsupported"
assert diagnostic["strict"]["reason"] == CompileReason.DEPTH_EXCEEDED
assert diagnostic["relaxed"]["metadata"]["depth"] > 13
assert diagnostic["relaxed"]["metadata"]["trace"]
macro = diagnostic["relaxed"]["metadata"]["macro_diagnostics"]
assert set(macro["hits"]) == {"scaled_exp_minus_one_template", "direct_division_template"}
assert macro["depth_delta"] > 0
assert macro["node_delta"] > 0
```

```python
assert diagnostic["status"] == "unsupported"
assert diagnostic["strict"]["reason"] == CompileReason.UNSUPPORTED_OPERATOR
assert diagnostic["relaxed_error"]["reason"] == CompileReason.UNSUPPORTED_OPERATOR
```

Keep this style for regression guards: Planck remains stretch unless the phase explicitly proves otherwise; unsupported operators like `cos` remain fail-closed.

**Warm-start same-AST pattern** (lines 178-230):

```python
result = fit_warm_started_eml_tree(
    splits[0].inputs,
    splits[0].target,
    TrainingConfig(depth=compiled.metadata.depth, variables=(spec.variable,), steps=1, restarts=1, seed=0),
    compiled.expression,
    perturbation_config=PerturbationConfig(seed=0, noise_scale=0.0),
    verification_splits=splits,
    compiler_metadata=compiled.metadata.as_dict(),
)

assert result.status == "same_ast_return"
assert result.verification is not None
assert result.verification.status == "recovered"
assert result.manifest["status"] == "same_ast_return"
assert result.manifest["diagnosis"]["mechanism"] == "same_ast_return"
assert result.manifest["diagnosis"]["changed_slot_count"] == 0
```

If Michaelis strict support reaches depth 13, copy this zero-noise pattern with `get_demo("michaelis_menten")`, compiled depth, `warm_steps=1`, and macro hits including the new reusable motif. Label it same-AST evidence, not blind discovery.

**CLI artifact pattern and current Michaelis guard** (lines 334-404):

```python
assert "compiled_seed=recovered" in result.stdout
assert "trained_exact_recovery=recovered" in result.stdout
payload = json.loads(output.read_text())
assert payload["claim_status"] == "recovered"
assert payload["stage_statuses"]["compiled_seed"] == "recovered"
assert payload["stage_statuses"]["warm_start_attempt"] == "same_ast_return"
assert payload["stage_statuses"]["trained_exact_recovery"] == "recovered"
assert payload["compiled_eml"]["metadata"]["macro_diagnostics"]["hits"] == ["direct_division_template"]
```

```python
payload = json.loads(output.read_text())
assert payload["claim_status"] == "verified_showcase"
assert payload["stage_statuses"]["compiled_seed"] == "unsupported"
assert payload["warm_start_eml"]["status"] == "unsupported"
relaxed_macro = payload["compiled_eml"]["diagnostic"]["relaxed"]["metadata"]["macro_diagnostics"]
assert relaxed_macro["hits"] == ["direct_division_template"]
assert relaxed_macro["depth_delta"] > 0
```

Update the Michaelis CLI test according to actual compiler behavior. If strict support succeeds, assert the recovered same-AST shape. If not, keep `verified_showcase` / `unsupported` and assert improved macro hits, relaxed depth, node count, and deltas.

**Planck CLI stretch guard** (lines 406-432):

```python
assert payload["claim_status"] == "verified_showcase"
assert payload["stage_statuses"]["stretch"] == "reported"
assert payload["stretch"]["guaranteed_trained_recovery"] is False
assert payload["warm_start_eml"]["status"] == "unsupported"
relaxed_macro = payload["compiled_eml"]["diagnostic"]["relaxed"]["metadata"]["macro_diagnostics"]
assert set(relaxed_macro["hits"]) == {"scaled_exp_minus_one_template", "direct_division_template"}
assert relaxed_macro["depth_delta"] > 0
```

Preserve this behavior. If new macros also fire for Planck through a generic structural rule, update only the macro-hit assertion and still require stretch/unsupported unless verified recovery is actually proven.

---

### `src/eml_symbolic_regression/cli.py` (CLI controller, request-response / file-I/O)

**Analog:** `src/eml_symbolic_regression/cli.py`

**Generic compile and diagnostic serialization** (lines 108-134):

```python
compiled = None
if args.compile_eml or args.warm_start_eml:
    source_expr = spec.candidate.to_sympy()
    validation_inputs = {
        spec.variable: np.concatenate([split.inputs[spec.variable] for split in splits]),
    }
    compiler_config = CompilerConfig(
        variables=(spec.variable,),
        constant_policy=args.constant_policy,
        max_depth=args.max_compile_depth,
        max_nodes=args.max_compile_nodes,
        max_power=args.max_power,
        validation_tolerance=args.tolerance,
    )
    try:
        compiled = compile_and_validate(source_expr, compiler_config, validation_inputs)
        compiled_verification = verify_candidate(compiled.expression, splits, tolerance=args.tolerance)
        payload["compiled_eml"] = compiled.as_dict()
        payload["compiled_eml_verification"] = compiled_verification.as_dict()
        stage_statuses["compiled_seed"] = compiled_verification.status
    except UnsupportedExpression as exc:
        payload["compiled_eml"] = {
            "status": "unsupported",
            **exc.as_dict(),
            "diagnostic": diagnose_compile_expression(source_expr, compiler_config, validation_inputs),
        }
        stage_statuses["compiled_seed"] = "unsupported"
```

This path already surfaces new macro diagnostics. Do not add a Michaelis-specific CLI branch.

**Warm-start gate and promotion pattern** (lines 136-181):

```python
if args.warm_start_eml:
    if compiled is None:
        payload["warm_start_eml"] = {
            "status": "unsupported",
            "reason": "compile_failed",
            "detail": "warm-start requires a validated compiled EML seed",
        }
        stage_statuses["warm_start_attempt"] = "unsupported"
    elif compiled.metadata.depth > args.max_warm_depth:
        payload["warm_start_eml"] = {
            "status": "unsupported",
            "reason": "depth_too_large_for_warm_start",
            "compiled_depth": compiled.metadata.depth,
            "max_warm_depth": args.max_warm_depth,
        }
        stage_statuses["warm_start_attempt"] = "unsupported"
```

```python
payload["warm_start_eml"] = warm.manifest
stage_statuses["warm_start_attempt"] = warm.status
if warm.verification is not None:
    stage_statuses["trained_exact_recovery"] = warm.verification.status
    if warm.verification.status == "recovered":
        payload["claim_status"] = "recovered"
```

Recovery promotion belongs here only through `warm.verification.status == "recovered"`. Do not promote Michaelis from macro hit, compile depth, or training loss alone.

**Default gates** (lines 443-457):

```python
demo.add_argument("--compile-eml", action="store_true", help="Compile the demo source expression into an exact EML AST.")
demo.add_argument(
    "--warm-start-eml",
    action="store_true",
    help="Compile, embed, perturb, train, snap, and verify a compiler warm start.",
)
demo.add_argument("--constant-policy", choices=("basis_only", "literal_constants"), default="literal_constants")
demo.add_argument("--max-compile-depth", type=int, default=13)
demo.add_argument("--max-compile-nodes", type=int, default=256)
demo.add_argument("--max-power", type=int, default=3)
demo.add_argument("--max-warm-depth", type=int, default=14)
demo.add_argument("--warm-depth", type=int, default=0, help="Warm-start tree depth; 0 means compiled depth.")
demo.add_argument("--warm-steps", type=int, default=1)
demo.add_argument("--warm-restarts", type=int, default=1)
demo.add_argument("--warm-noise", type=float, default=0.0)
```

If any gate changes for evidence generation, document it in tests/docs/artifacts. The locked default is strict compile depth 13 and warm-start depth 14.

**Do not copy the Planck special case** (lines 75-81):

```python
if spec.name == "planck":
    payload["stretch"] = {
        "status": "reported",
        "reason": "normalized_planck_is_stretch_target",
        "guaranteed_trained_recovery": False,
    }
    stage_statuses["stretch"] = "reported"
```

This is an existing stretch-report exception. Phase 51 must not add `if spec.name == "michaelis_menten"` or any equivalent formula-id branch.

---

### `src/eml_symbolic_regression/benchmark.py` (service / config registry, batch / file-I/O)

**Analog:** `src/eml_symbolic_regression/benchmark.py`

**Built-in suite registry pattern** (lines 42-70):

```python
START_MODES = ("catalog", "compile", "blind", "warm_start", "perturbed_tree")
BUILTIN_SUITES = (
    "smoke",
    "v1.2-evidence",
    "for-demo-diagnostics",
    ...
    "v1.9-arrhenius-evidence",
)
```

If Phase 51 needs durable evidence for Phase 53, add one focused suite here rather than broadening default campaign denominators. Existing suites already include Michaelis diagnostics.

**Case helper pattern** (lines 851-899):

```python
def _case(
    id: str,
    formula: str,
    start_mode: str,
    *,
    seeds: Iterable[int] = (0,),
    perturbation_noise: Iterable[float] = (0.0,),
    points: int = 24,
    steps: int = 8,
    warm_steps: int = 8,
    restarts: int = 1,
    depth: int = 2,
    constants: Iterable[complex] = (1.0,),
    warm_restarts: int = 1,
    max_warm_depth: int = 14,
    ...
) -> BenchmarkCase:
```

Use `_case(...)`; do not hand-roll `BenchmarkCase` unless the local pattern requires a custom object.

**Existing Michaelis diagnostic rows** (lines 1055-1083, 1090-1097, 1125-1135, 1164-1175):

```python
_case("michaelis-warm-diagnostic", "michaelis_menten", "warm_start", tags=("diagnostic", "depth_gate")),
_case("planck-diagnostic", "planck", "compile", tags=("stretch", "depth_gate")),
```

```python
_case("michaelis-compile", "michaelis_menten", "compile", tags=("for_demo", "diagnostic")),
```

The current registry already has Michaelis warm-start and compile diagnostics. Prefer updating artifact expectations for those rows unless Phase 51 needs an isolated new suite for a before/after evidence bundle.

**Focused one-case suite pattern** (lines 1466-1483):

```python
if name == "v1.9-arrhenius-evidence":
    return BenchmarkSuite(
        id="v1.9-arrhenius-evidence",
        description="Focused v1.9 Arrhenius exact warm-start evidence for normalized exp(-0.8/x).",
        cases=(
            _case(
                "arrhenius-warm",
                "arrhenius",
                "warm_start",
                seeds=(0,),
                perturbation_noise=(0.0,),
                points=24,
                warm_steps=1,
                tags=("v1.9", "arrhenius", "warm_start", "same_ast"),
                expect_recovery=True,
            ),
        ),
    )
```

If adding a Phase 51 suite, copy this shape with one Michaelis-focused row. Suggested tags should describe evidence mechanics, for example `("v1.10", "michaelis", "motif", "warm_start")` or `("v1.10", "michaelis", "motif", "unsupported")` depending on the verified result. Do not add it to broad v1.3/v1.8 suites unless explicitly planned.

**Runner serialization pattern** (lines 1514-1530):

```python
payload = _base_run_payload(run)
payload.update(_execute_benchmark_run_inner(run))
...
payload.pop("_compiled", None)
payload["evidence_class"] = evidence_class_for_payload(payload)
payload["metrics"] = _extract_run_metrics(payload)
payload["timing"] = {"elapsed_seconds": time.perf_counter() - started}
_write_json(run.artifact_path, payload)
return BenchmarkRunResult(run, str(payload["status"]), run.artifact_path, payload)
```

No new artifact schema is needed. The existing payload already stores `compiled_eml`, diagnostics, `warm_start_eml`, `metrics`, and `evidence_class`.

**Warm-start unsupported and recovered path** (lines 1665-1790):

```python
compiled_payload = _compile_demo(run, splits)
stage_statuses.update(compiled_payload.pop("stage_statuses"))
if stage_statuses["compiled_seed"] == "unsupported":
    return {
        "status": "unsupported",
        "stage_statuses": {**stage_statuses, "warm_start_attempt": "unsupported"},
        **compiled_payload,
        "warm_start_eml": {
            "status": "unsupported",
            "reason": "compile_failed",
            "detail": "warm-start requires a validated compiled EML seed",
        },
    }
```

```python
if compiled.metadata.depth > run.optimizer.max_warm_depth:
    return {
        "status": "unsupported",
        "stage_statuses": {**stage_statuses, "warm_start_attempt": "unsupported"},
        **compiled_payload,
        "claim_status": "unsupported",
        "warm_start_eml": {
            "status": "unsupported",
            "reason": "depth_too_large_for_warm_start",
            "compiled_depth": compiled.metadata.depth,
            "max_warm_depth": run.optimizer.max_warm_depth,
        },
    }
```

```python
warm = fit_warm_started_eml_tree(
    train.inputs,
    train.target,
    config,
    compiled.expression,
    perturbation_config=PerturbationConfig(seed=run.seed, noise_scale=run.perturbation_noise),
    verification_splits=splits,
    tolerance=run.dataset.tolerance,
    compiler_metadata=compiled.metadata.as_dict(),
)
stage_statuses["warm_start_attempt"] = warm.status
if warm.verification is not None:
    stage_statuses["trained_exact_recovery"] = warm.verification.status
```

Keep this generic. Do not add `run.formula == "michaelis_menten"` branching.

**Compile helper pattern** (lines 2374-2404):

```python
compiled = compile_and_validate(spec.candidate.to_sympy(), compiler_config, validation_inputs)
report = verify_candidate(compiled.expression, splits, tolerance=run.dataset.tolerance)
return {
    "stage_statuses": {"compiled_seed": report.status},
    "compiled_eml": compiled.as_dict(),
    "compiled_eml_verification": report.as_dict(),
    "_compiled": compiled,
    "claim_status": report.status,
}
```

```python
return {
    "stage_statuses": {"compiled_seed": "unsupported"},
    "compiled_eml": {
        "status": "unsupported",
        **exc.as_dict(),
        "diagnostic": diagnose_compile_expression(spec.candidate.to_sympy(), compiler_config, validation_inputs),
    },
    "claim_status": "unsupported",
}
```

This is the benchmark equivalent of the CLI compile path. New macro diagnostics appear here automatically through `compiled.as_dict()` or `diagnose_compile_expression()`.

**Metrics and evidence-class pattern** (lines 2427-2555, 2929-2963):

```python
return {
    "unsupported_reason": _run_reason(payload) if payload.get("status") == "unsupported" else None,
    ...
    "verifier_status": verification.get("status") if isinstance(verification, Mapping) else None,
    "high_precision_max_error": verification.get("high_precision_max_error") if isinstance(verification, Mapping) else None,
    "warm_start_mechanism": diagnosis.get("mechanism"),
    "warm_start_status": diagnosis.get("status"),
}
```

```python
if training_mode == TRAINING_MODES["compiler_warm_start_training"]:
    if status == "same_ast_return" or claim_status == "same_ast_return":
        return EVIDENCE_CLASSES["same_ast"]
    if status == "verified_equivalent_ast" or claim_status == "verified_equivalent_ast":
        return EVIDENCE_CLASSES["verified_equivalent"]
    if recovered:
        return EVIDENCE_CLASSES["compiler_warm_start_recovered"]
```

Do not create a new evidence class for "macro hit." Macro hits are compiler diagnostics; recovery class remains driven by run status and verifier status.

---

### `tests/test_benchmark_contract.py` (test, config validation / batch)

**Analog:** `tests/test_benchmark_contract.py`

**Built-in registry and focused-suite test pattern** (lines 89-154):

```python
assert {
    "smoke",
    "v1.2-evidence",
    "for-demo-diagnostics",
    ...
    "v1.9-arrhenius-evidence",
} <= set(list_builtin_suites())
```

```python
suite = builtin_suite("v1.9-arrhenius-evidence")
runs = suite.expanded_runs()

assert suite.id == "v1.9-arrhenius-evidence"
assert [case.id for case in suite.cases] == ["arrhenius-warm"]
assert len(runs) == 1
...
assert run.start_mode == "warm_start"
assert run.training_mode == "compiler_warm_start_training"
assert run.seed == 0
assert run.perturbation_noise == 0.0
assert run.dataset.points == 24
assert run.optimizer.warm_steps == 1
assert run.optimizer.max_warm_depth == 14
```

If Phase 51 adds a focused suite, add it to `list_builtin_suites()` expectations and copy this one-case contract style.

**Existing Michaelis suite coverage** (lines 231-242):

```python
suite = load_suite("v1.2-evidence")
runs = suite.expanded_runs()
...
assert any(run.case_id == "michaelis-warm-diagnostic" and run.start_mode == "warm_start" for run in runs)
assert any(run.formula == "planck" and "stretch" in run.tags for run in runs)
```

Keep this assertion unless the plan intentionally changes the v1.2 diagnostic row. If a focused Phase 51 suite is added, do not remove the existing diagnostic coverage.

---

### `tests/test_benchmark_runner.py` (test, batch / file-I/O)

**Analog:** `tests/test_benchmark_runner.py`

**Generic artifact contract pattern** (lines 115-143):

```python
result = run_benchmark_suite(suite)
payload = result.as_dict()

assert payload["counts"]["total"] == 3
assert all(item.artifact_path.exists() for item in result.results)
...
for item in result.results:
    artifact = json.loads(item.artifact_path.read_text(encoding="utf-8"))
    assert artifact["training_mode"] == item.run.training_mode
    assert artifact["evidence_class"] == evidence_class_for_payload(artifact)
    assert artifact["dataset"] == item.run.dataset.as_dict()
    assert artifact["dataset_manifest"]["schema"] == "eml.proof_dataset_manifest.v1"
    assert artifact["budget"] == item.run.optimizer.as_dict()
    assert artifact["provenance"]["symbolic_expression"]
```

All Phase 51 benchmark artifact tests should read the written JSON artifact, not only inspect in-memory result fields.

**Evidence-class same-AST pattern** (lines 329-367):

```python
assert (
    evidence_class_for_payload(
        {
            "status": "same_ast_return",
            "claim_status": "same_ast_return",
            "training_mode": "compiler_warm_start_training",
            "run": {"start_mode": "warm_start"},
        }
    )
    == "same_ast"
)
```

Use this to lock same-AST evidence if Michaelis becomes strict-supported and warm-start recovered.

**Warm-start artifact assertion pattern** (lines 832-895):

```python
result = run_benchmark_suite(suite, run_filter=RunFilter(case_ids=("shockley-warm",)))

assert len(result.results) == 1
assert result.results[0].status == "same_ast_return"
assert result.results[0].payload["claim_status"] == "recovered"
assert result.results[0].payload["evidence_class"] == "same_ast"
compiled = result.results[0].payload["compiled_eml"]
assert compiled["metadata"]["depth"] <= 13
assert compiled["metadata"]["macro_diagnostics"]["hits"] == ["scaled_exp_minus_one_template"]
assert result.results[0].payload["stage_statuses"]["compiled_seed"] == "recovered"
assert result.results[0].payload["stage_statuses"]["warm_start_attempt"] == "same_ast_return"
assert result.results[0].payload["stage_statuses"]["trained_exact_recovery"] == "recovered"
```

```python
artifact = json.loads(result.results[0].artifact_path.read_text(encoding="utf-8"))
...
assert artifact["compiled_eml"]["metadata"]["macro_diagnostics"]["hits"] == ["direct_division_template"]
assert artifact["compiled_eml"]["metadata"]["depth"] == 7
assert artifact["warm_start_eml"]["status"] == "same_ast_return"
assert artifact["warm_start_eml"]["verification"]["status"] == "recovered"
assert artifact["warm_start_eml"]["diagnosis"]["changed_slot_count"] == 0
...
aggregate = benchmark_module.aggregate_evidence(result)
aggregate_run = aggregate["runs"][0]

assert aggregate_run["evidence_class"] == "same_ast"
assert aggregate_run["classification"] == "same_ast_warm_start_return"
```

For Michaelis:

- If strict + warm-start passes, assert the same recovered/same-AST fields and macro hits containing `saturation_ratio_template` and/or `reciprocal_shift_template`.
- If strict remains unsupported, assert `result.results[0].status == "unsupported"`, `artifact["evidence_class"] == "unsupported"`, `artifact["stage_statuses"]["compiled_seed"] == "unsupported"`, and inspect `artifact["compiled_eml"]["diagnostic"]["relaxed"]["metadata"]["macro_diagnostics"]` for measured depth/node reduction.

---

### `docs/IMPLEMENTATION.md` (documentation, reporting)

**Analog:** `docs/IMPLEMENTATION.md`

**Compiler contract pattern** (lines 38-52):

```markdown
The compiler accepts a deliberately narrow SymPy subset:

- variables from an explicit allow-list,
- finite constants under either `basis_only` or `literal_constants`,
- `exp` and principal-branch `log`,
- addition, subtraction, multiplication, division/reciprocal, and small integer powers through tested EML templates.
```

```markdown
The compiler now routes supported shortcuts through an explicit macro layer. Current macro rules are `scaled_exp_minus_one_template` for Shockley-style `scale * (exp(a) - 1)` shapes and `direct_division_template` for true numerator-over-denominator motifs such as Michaelis-Menten and Arrhenius reciprocal-temperature exponents. Compiler metadata records macro hits, misses, and the depth/node delta against a no-macro baseline so a shortcut can be audited instead of hidden behind an ad hoc branch.
```

Update this section with `reciprocal_shift_template` and `saturation_ratio_template` only after tests prove the names and behavior. Preserve the literal-constant warning immediately above this text.

**Benchmark evidence contract pattern** (lines 69-118):

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
The taxonomy intentionally separates:

- `blind_recovery`
- `same_ast_warm_start_return`
- `verified_equivalent_warm_start_recovery`
- `snapped_but_failed`
- `soft_fit_only`
- `unsupported`
- `execution_failure`
```

Use this language for Michaelis. A reduced compiler depth is not a recovery claim. A strict-supported zero-noise warm start is same-AST compiler evidence unless a blind path is separately demonstrated.

**Demo ladder and honest unsupported pattern** (lines 157-188):

````markdown
Beer-Lambert, Shockley, and normalized Arrhenius now have compiler-driven warm-start paths:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli demo beer_lambert --warm-start-eml
PYTHONPATH=src python -m eml_symbolic_regression.cli demo shockley --warm-start-eml --points 24
PYTHONPATH=src python -m eml_symbolic_regression.cli demo arrhenius --warm-start-eml --points 24 --output artifacts/arrhenius-warm-report.json
```
````

```markdown
At the default gates, Michaelis-Menten and Planck remain honest stretch reports: their catalog formulas verify, the relaxed compiler diagnostics show the macro-shortened exact trees, but the shipped compile/warm-start stages still report unsupported depth instead of promotion.
```

Update this final sentence according to actual Phase 51 results. If Michaelis remains unsupported, document the measured strict/relaxed depth and macro hits. If it recovers, document it as compiler warm-start / same-AST evidence and keep Planck stretch wording intact.

---

### `README.md` (documentation, reporting)

**Analog:** `README.md`

**Implemented scope and honesty pattern** (lines 13-31):

```markdown
- A fail-closed SymPy subset compiler that emits exact EML ASTs with metadata, rule traces, assumptions, literal-constant provenance, and independent validation against ordinary SymPy evaluation.
- Constant-catalog soft master trees plus exact AST embedding with embed-to-snap round-trip checks.
- Compiler-driven warm-start training reports that perturb, train, snap, and verify through the existing optimizer/verifier boundary.
- Repeatable benchmark suites with per-run artifacts, aggregate JSON/Markdown reports, recovery-rate grouping, and explicit failure/unsupported taxonomy.
```

```markdown
The implementation is intentionally honest about scope: exact EML recovery is demonstrated for paper-grounded shallow formulas, for Beer-Lambert via a compiler-generated warm start, and for normalized Arrhenius as exact compiler warm-start / same-AST basin evidence. Harder showcase demos remain verified catalog candidates or explicit unsupported/depth reports unless a trained exact EML candidate passes the verifier.
```

Add Michaelis here only after the verifier-owned outcome is known. If the phase only reduces depth, mention it as improved compiler diagnostics, not exact recovery.

**Quick command and focused evidence pattern** (lines 53-92):

````markdown
Compile a supported demo formula into EML and validate it:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli demo beer_lambert --compile-eml --output artifacts/beer-compile-report.json
```

Run the compiler warm-start recovery path:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli demo beer_lambert --warm-start-eml --output artifacts/beer-lambert-warm-report.json
```
````

If adding a Michaelis command, use the existing CLI shape:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli demo michaelis_menten --warm-start-eml --points 24 --output artifacts/michaelis-menten-warm-report.json
```

If adding a focused benchmark suite, copy the Arrhenius benchmark command style and use the actual suite/case id selected by the plan.

**Demo status and evidence taxonomy pattern** (lines 143-171):

```markdown
- `compiled_seed`: the source formula compiled to an exact EML AST and that AST verified numerically. This is a seed/provenance stage, not a trained recovery claim by itself.
- `warm_start_attempt`: the compiler seed was embedded into a compatible soft tree, optionally perturbed, trained through the existing optimizer, snapped, and classified.
- `trained_exact_recovery`: the post-training snapped exact EML AST passed the verifier. Demo reports promote top-level `claim_status` to `recovered` only at this stage.
- `unsupported`: the compiler or warm-start gate failed closed, usually because an operator, constant policy, depth, node budget, or warm-start depth limit was exceeded.
```

```markdown
- `same_ast_return` means a warm-started run snapped back to the compiled seed; this is useful basin-stability evidence, not blind discovery.
- `unsupported` and failed cases are kept in the denominator; they are part of the evidence.
- `verifier_recovery_rate` is computed from verifier-owned recovery, not from training loss.
```

Preserve this wording. It is the guardrail against treating motif support as blind discovery.

**Current Michaelis limit statement** (lines 199-203):

```markdown
This repo does not promise blind recovery of arbitrary deep formulas. The paper reports that blind recovery degrades sharply with depth and that depth-6 blind recovery was not observed in the reported attempts. Warm-start success is a different claim: it shows return-to-solution from a compiler-provided scaffold, with fixed literal constants when the source formula contains coefficients.

The default compiler/warm-start gates intentionally keep Michaelis-Menten and Planck honest: their catalog formulas verify, but their compiled EML trees currently exceed the default depth budget for warm-start promotion.
```

Update this after implementation with the measured Phase 51 result. Keep the distinction between blind recovery, compiler warm-start recovery, and unsupported diagnostics.

## Shared Patterns

### Reusable Compiler Macros

**Source:** `src/eml_symbolic_regression/compiler.py` lines 252-311
**Apply to:** `src/eml_symbolic_regression/compiler.py`, compiler unit tests, CLI/benchmark artifact assertions

```python
if isinstance(expr, sp.Mul):
    macro = self._compile_direct_division(expr)
    if macro is not None:
        return macro
...
return self._record(
    "direct_division_template",
    expr,
    divide_expr(compiled_numerator, compiled_denominator),
)
```

New Phase 51 motifs should be reusable structural macros. They must not inspect formula IDs, dataset names, candidate names, or exact expression strings.

### Fail-Closed Diagnostics

**Source:** `src/eml_symbolic_regression/compiler.py` lines 480-522; `src/eml_symbolic_regression/cli.py` lines 122-134; `src/eml_symbolic_regression/benchmark.py` lines 2395-2404
**Apply to:** all compiler, CLI, and benchmark changes

```python
except UnsupportedExpression as exc:
    payload["compiled_eml"] = {
        "status": "unsupported",
        **exc.as_dict(),
        "diagnostic": diagnose_compile_expression(source_expr, compiler_config, validation_inputs),
    }
    stage_statuses["compiled_seed"] = "unsupported"
```

Unsupported is a valid outcome when strict gates are not met. Preserve relaxed diagnostics so depth/node reductions are auditable.

### Verifier-Owned Recovery

**Source:** `src/eml_symbolic_regression/verify.py` lines 115-127
**Apply to:** CLI promotion, warm-start tests, benchmark artifact tests, docs

```python
if all_passed and (candidate_kind == "exact_eml" or not recovered_requires_exact_eml):
    status = "recovered"
    reason = "verified"
elif all_passed:
    status = "verified_showcase"
    reason = "verified_non_eml_candidate"
else:
    status = "failed"
```

Use verifier status for claims. A macro hit or lower depth is not enough to mark Michaelis recovered.

### Warm-Start Regime Classification

**Source:** `src/eml_symbolic_regression/warm_start.py` lines 156-181, 184-231
**Apply to:** warm-start tests, CLI JSON assertions, benchmark artifacts, docs

```python
if expressions_equal(fit.snap.expression, compiled_expr):
    status = "same_ast_return"
elif verification is not None and verification.status == "recovered":
    status = "verified_equivalent_ast"
elif fit.status == "snapped_candidate":
    status = "snapped_but_failed"
elif np.isfinite(fit.best_loss):
    status = "soft_fit_only"
else:
    status = "failed"
```

```python
return {
    "status": status,
    "mechanism": mechanism,
    "active_slot_count": active_slot_count,
    "changed_slot_count": changed_slot_count,
    "snap_min_margin": fit.snap.min_margin,
    "best_loss": fit.best_loss,
    "post_snap_loss": fit.post_snap_loss,
    "verifier_status": verifier_status,
}
```

If Phase 51 enables Michaelis warm-start recovery, expected zero-noise evidence is likely `same_ast_return` with `changed_slot_count == 0`, unless tests prove a different exact verified AST.

### Benchmark Evidence Class

**Source:** `src/eml_symbolic_regression/benchmark.py` lines 2929-2963
**Apply to:** benchmark runner tests and README/docs wording

```python
if training_mode == TRAINING_MODES["compiler_warm_start_training"]:
    if status == "same_ast_return" or claim_status == "same_ast_return":
        return EVIDENCE_CLASSES["same_ast"]
    if status == "verified_equivalent_ast" or claim_status == "verified_equivalent_ast":
        return EVIDENCE_CLASSES["verified_equivalent"]
    if recovered:
        return EVIDENCE_CLASSES["compiler_warm_start_recovered"]
```

Same-AST warm-start recovery should remain `same_ast`, even when top-level `claim_status == "recovered"`.

## Where Not To Add Formula-Specific Logic

| File | Do Not Add | Use Instead |
|------|------------|-------------|
| `src/eml_symbolic_regression/compiler.py` | `if expression == "2*x/(x + 0.5)"`, `if candidate_name == "michaelis_menten_catalog"`, or a `michaelis_menten_template` | Structural SymPy motif helpers: `reciprocal_shift_template`, `saturation_ratio_template` |
| `src/eml_symbolic_regression/datasets.py` | Alternate Michaelis demo or changed domains to make support look better | Existing `michaelis_menten` `DemoSpec` |
| `src/eml_symbolic_regression/cli.py` | `if spec.name == "michaelis_menten"` promotion or custom status | Existing generic compile/warm-start/verification flow |
| `src/eml_symbolic_regression/benchmark.py` | `if run.formula == "michaelis_menten"` runner behavior | Existing `_compile_demo()` and warm-start runner paths |
| docs / README | "Michaelis recovered" based on compile depth or macro hit | State strict unsupported with measured depth reduction, or same-AST/compiler-warm-start evidence if verifier recovered |

## No Analog Found

No new source pattern lacks a close analog. Planner should not invent:

- a new compiler result schema,
- a new benchmark artifact schema,
- a new evidence class for macro hits,
- a Michaelis-specific CLI or benchmark runner path,
- a second Michaelis dataset entry.

## Metadata

**Analog search scope:** `src/eml_symbolic_regression`, `tests`, `docs/IMPLEMENTATION.md`, `README.md`, `.planning/phases/50-arrhenius-exact-warm-start-demo`
**Files scanned:** 27 source/test/doc/planning files via `rg`; 15 files read with line numbers
**Pattern extraction date:** 2026-04-17
