# Phase 50: Arrhenius Exact Warm-Start Demo - Pattern Map

**Mapped:** 2026-04-17
**Files analyzed:** 8
**Analogs found:** 8 / 8

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `src/eml_symbolic_regression/datasets.py` | model / dataset registry | batch, transform | `src/eml_symbolic_regression/datasets.py` Beer-Lambert/Shockley `DemoSpec` entries | exact |
| `src/eml_symbolic_regression/benchmark.py` | service / config registry | batch, file-I/O | `src/eml_symbolic_regression/benchmark.py` `_case(...)` warm-start suite rows and runner flow | exact |
| `tests/test_compiler_warm_start.py` | test | request-response, file-I/O, transform | Beer-Lambert/Shockley warm-start tests in `tests/test_compiler_warm_start.py` | exact |
| `tests/test_benchmark_runner.py` | test | batch, file-I/O | smoke/Beer-Lambert benchmark runner tests in `tests/test_benchmark_runner.py` | exact |
| `tests/test_benchmark_contract.py` | test | config validation, batch | built-in suite registry tests in `tests/test_benchmark_contract.py` | role-match |
| `tests/test_proof_dataset_manifest.py` | test | batch, transform | provenance/domain manifest tests in `tests/test_proof_dataset_manifest.py` | exact |
| `docs/IMPLEMENTATION.md` | documentation | reporting | demo ladder, compiler, warm-start, benchmark sections in `docs/IMPLEMENTATION.md` | exact |
| `README.md` | documentation | reporting | Quick Commands, Demo Statuses, Benchmark Evidence sections in `README.md` | exact |

`src/eml_symbolic_regression/cli.py` is an integration analog but is not expected to be modified: existing `demo --warm-start-eml` options already compile, warm-start, verify, promote `claim_status`, and write JSON artifacts.

## Pattern Assignments

### `src/eml_symbolic_regression/datasets.py` (model / dataset registry, batch transform)

**Analog:** `src/eml_symbolic_regression/datasets.py`

**Imports pattern** (lines 5-14):

```python
import hashlib
import json
from dataclasses import dataclass
from typing import Any, Callable

import numpy as np
import sympy as sp

from .expression import Candidate, SympyCandidate, exp_expr, log_expr
from .verify import DataSplit
```

**DemoSpec shape and split generation** (lines 19-50):

```python
@dataclass(frozen=True)
class DemoSpec:
    name: str
    variable: str
    description: str
    target: ArrayFn
    candidate: Candidate
    train_domain: tuple[float, float]
    heldout_domain: tuple[float, float]
    extrap_domain: tuple[float, float]
    source_document: str
    source_linkage: str
    normalized_dimensionless: bool

    def make_splits(self, *, points: int = 80, seed: int = 0) -> list[DataSplit]:
        rng = np.random.default_rng(seed)

        def sample(domain: tuple[float, float], count: int) -> np.ndarray:
            low, high = domain
            values = np.linspace(low, high, count)
            jitter = (high - low) * 0.002 * rng.standard_normal(count)
            return np.sort(values + jitter).astype(np.float64)
```

**Provenance pattern** (lines 52-63):

```python
def formula_provenance(self) -> dict[str, Any]:
    candidate_name = getattr(self.candidate, "name", getattr(self.candidate, "candidate_kind", type(self.candidate).__name__))
    return {
        "formula_id": self.name,
        "variable": self.variable,
        "description": self.description,
        "symbolic_expression": sp.sstr(self.candidate.to_sympy()),
        "candidate_name": str(candidate_name),
        "source_document": self.source_document,
        "source_linkage": self.source_linkage,
        "normalized_dimensionless": self.normalized_dimensionless,
    }
```

**Closest demo entries to copy** (Beer-Lambert lines 142-154, Shockley lines 220-232):

```python
"beer_lambert": DemoSpec(
    name="beer_lambert",
    variable="x",
    description="High-probability exponential-decay showcase.",
    target=lambda a: np.exp(-0.8 * a).astype(np.complex128),
    candidate=_sympy_candidate(sp.exp(-sp.Float("0.8") * x), "x", "beer_lambert_catalog"),
    train_domain=(0.0, 3.0),
    heldout_domain=(0.15, 2.7),
    extrap_domain=(3.1, 4.5),
    source_document="sources/FOR_DEMO.md",
    source_linkage="Beer-Lambert law high-success-probability sanity check",
    normalized_dimensionless=True,
),
```

Apply this pattern by adding `arrhenius` to `demo_specs()` with:

```python
target=lambda a: np.exp(-0.8 / a).astype(np.complex128)
candidate=_sympy_candidate(sp.exp(-sp.Float("0.8") / x), "x", "arrhenius_catalog")
train_domain=(0.5, 3.0)
heldout_domain=(0.6, 2.7)
extrap_domain=(3.1, 4.2)
source_document="sources/FOR_DEMO.md"
normalized_dimensionless=True
```

Keep the candidate as `sp.exp(-sp.Float("0.8") / x)` so the compiler sees the reciprocal-temperature division motif.

---

### `src/eml_symbolic_regression/benchmark.py` (service / config registry, batch file-I/O)

**Analog:** `src/eml_symbolic_regression/benchmark.py`

**Imports pattern** (lines 22-39):

```python
from .compiler import CompilerConfig, UnsupportedExpression, compile_and_validate, diagnose_compile_expression
from .datasets import demo_specs, proof_dataset_manifest
from .optimize import TrainingConfig, fit_eml_tree
from .verify import verify_candidate
from .warm_start import PerturbationConfig, fit_warm_started_eml_tree
```

**Built-in suite registry pattern** (lines 42-69):

```python
BUILTIN_SUITES = (
    "smoke",
    "v1.2-evidence",
    "for-demo-diagnostics",
    "v1.3-standard",
    "v1.3-showcase",
    ...
    "v1.8-family-showcase",
)
```

Add a focused suite id here if Phase 50 implements the research decision `v1.9-arrhenius-evidence`.

**Case construction pattern** (lines 873-898):

```python
return BenchmarkCase(
    id=id,
    formula=formula,
    start_mode=start_mode,
    seeds=tuple(seeds),
    perturbation_noise=tuple(perturbation_noise),
    dataset=DatasetConfig(points=points),
    optimizer=OptimizerBudget(
        depth=depth,
        constants=tuple(constants),
        steps=steps,
        restarts=restarts,
        warm_steps=warm_steps,
        warm_restarts=warm_restarts,
        max_warm_depth=max_warm_depth,
        scaffold_initializers=tuple(scaffold_initializers),
        operator_family=operator_family or raw_eml_operator(),
        operator_schedule=tuple(operator_schedule),
    ),
    tags=tuple(tags),
    expect_recovery=expect_recovery,
    claim_id=claim_id,
    threshold_policy_id=threshold_policy_id,
    training_mode=training_mode,
)
```

**Warm-start suite row pattern** (lines 1127-1133 and 1165-1172):

```python
_case(
    "shockley-warm",
    "shockley",
    "warm_start",
    warm_steps=1,
    tags=("warm_start", "for_demo"),
    expect_recovery=True,
),
```

Copy this shape for:

```python
_case(
    "arrhenius-warm",
    "arrhenius",
    "warm_start",
    warm_steps=1,
    tags=("v1.9", "arrhenius", "warm_start", "same_ast"),
    expect_recovery=True,
)
```

**Runner warm-start execution pattern** (lines 1646-1771):

```python
if run.start_mode == "warm_start":
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
    ...
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

**Compile helper pattern** (lines 2355-2385):

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

No new artifact schema is needed. The runner already writes per-run JSON and derives `evidence_class`.

---

### `tests/test_compiler_warm_start.py` (test, request-response and file-I/O)

**Analog:** `tests/test_compiler_warm_start.py`

**Imports and CLI env pattern** (lines 1-27):

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
from eml_symbolic_regression.datasets import get_demo
from eml_symbolic_regression.optimize import TrainingConfig
from eml_symbolic_regression.warm_start import PerturbationConfig, fit_warm_started_eml_tree

ROOT = Path(__file__).resolve().parents[1]
CLI_ENV = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
```

**Strict macro compile test pattern** (Shockley lines 42-58, direct division diagnostic lines 61-77):

```python
spec = get_demo("shockley")
splits = spec.make_splits(points=24, seed=0)
result = compile_and_validate(
    spec.candidate.to_sympy(),
    CompilerConfig(variables=(spec.variable,), max_depth=13, max_nodes=128),
    {spec.variable: splits[0].inputs[spec.variable]},
)

assert result.validation is not None
assert result.validation.passed
assert result.metadata.depth <= 13
assert result.metadata.macro_diagnostics is not None
assert result.metadata.macro_diagnostics["hits"] == ["scaled_exp_minus_one_template"]
```

For Arrhenius, use `max_depth=13`, `max_nodes=256`, and assert:

```python
assert result.metadata.unsupported_reason is None
assert result.metadata.depth <= 13
assert result.metadata.macro_diagnostics["hits"] == ["direct_division_template"]
```

**Zero-noise warm-start same-AST pattern** (Beer-Lambert lines 159-183):

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
assert result.manifest["optimizer"]["status"] == "snapped_candidate"
assert result.manifest["status"] == "same_ast_return"
assert result.manifest["diagnosis"]["mechanism"] == "same_ast_return"
assert result.manifest["diagnosis"]["changed_slot_count"] == 0
```

**CLI artifact test pattern** (Shockley lines 257-284):

```python
output = tmp_path / "shockley-warm.json"
result = subprocess.run(
    [
        sys.executable,
        "-m",
        "eml_symbolic_regression.cli",
        "demo",
        "shockley",
        "--warm-start-eml",
        "--points",
        "24",
        "--output",
        str(output),
    ],
    check=True,
    capture_output=True,
    env=CLI_ENV,
    text=True,
)

assert "compiled_seed=recovered" in result.stdout
payload = json.loads(output.read_text())
assert payload["claim_status"] == "recovered"
assert payload["stage_statuses"]["compiled_seed"] == "recovered"
assert payload["stage_statuses"]["warm_start_attempt"] == "same_ast_return"
assert payload["stage_statuses"]["trained_exact_recovery"] == "recovered"
assert payload["compiled_eml"]["metadata"]["macro_diagnostics"]["hits"] == ["scaled_exp_minus_one_template"]
```

For Arrhenius, assert the same stage statuses and replace the macro hit with `["direct_division_template"]`.

**Unsupported regression guards** (lines 287-343):

```python
assert payload["stage_statuses"]["compiled_seed"] == "unsupported"
assert payload["warm_start_eml"]["status"] == "unsupported"
relaxed_macro = payload["compiled_eml"]["diagnostic"]["relaxed"]["metadata"]["macro_diagnostics"]
assert relaxed_macro["hits"] == ["direct_division_template"]
```

Keep the Michaelis-Menten and Planck tests unchanged to prove Arrhenius did not promote existing stretch cases.

---

### `tests/test_benchmark_runner.py` (test, batch and file-I/O)

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
from eml_symbolic_regression.datasets import get_demo
```

**Runner artifact contract pattern** (lines 115-143):

```python
base = builtin_suite("smoke")
suite = type(base)(
    "smoke",
    "test smoke",
    base.cases,
    tmp_path / "artifacts",
)

result = run_benchmark_suite(suite)
payload = result.as_dict()

assert payload["counts"]["total"] == 3
assert all(item.artifact_path.exists() for item in result.results)
for item in result.results:
    artifact = json.loads(item.artifact_path.read_text(encoding="utf-8"))
    assert artifact["training_mode"] == item.run.training_mode
    assert artifact["evidence_class"] == evidence_class_for_payload(artifact)
    assert artifact["dataset_manifest"]["schema"] == "eml.proof_dataset_manifest.v1"
    assert artifact["budget"] == item.run.optimizer.as_dict()
    assert artifact["provenance"]["symbolic_expression"]
```

**Focused filter pattern** (lines 221-228):

```python
base = builtin_suite("v1.2-evidence")
suite = type(base)(base.id, base.description, base.cases, tmp_path / "artifacts")

result = run_benchmark_suite(suite, run_filter=RunFilter(case_ids=("beer-perturbation-sweep",), seeds=(0,)))

assert len(result.results) == 3
assert {item.run.perturbation_noise for item in result.results} == {0.0, 5.0, 35.0}
```

For Arrhenius, use `builtin_suite("v1.9-arrhenius-evidence")`, filter `case_ids=("arrhenius-warm",)`, and assert a single zero-noise run.

**Artifact assertions to copy from evidence-class tests** (lines 329-368):

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

Arrhenius benchmark test should assert:

```python
assert result.results[0].status == "same_ast_return"
assert artifact["claim_status"] == "recovered"
assert artifact["evidence_class"] == "same_ast"
assert artifact["compiled_eml"]["metadata"]["depth"] <= 13
assert artifact["compiled_eml"]["metadata"]["macro_diagnostics"]["hits"] == ["direct_division_template"]
assert artifact["stage_statuses"]["compiled_seed"] == "recovered"
assert artifact["stage_statuses"]["warm_start_attempt"] == "same_ast_return"
assert artifact["stage_statuses"]["trained_exact_recovery"] == "recovered"
assert artifact["metrics"]["verifier_status"] == "recovered"
assert artifact["metrics"]["warm_start_status"] == "same_ast_return"
```

---

### `tests/test_benchmark_contract.py` (test, config validation and batch)

**Analog:** `tests/test_benchmark_contract.py`

**Built-in registry test pattern** (lines 88-123):

```python
def test_builtin_suite_registry_expands_stable_run_ids():
    assert {
        "smoke",
        "v1.2-evidence",
        "for-demo-diagnostics",
        ...
        "v1.8-family-showcase",
    } <= set(list_builtin_suites())
    suite = builtin_suite("smoke")
    runs = suite.expanded_runs()

    assert [run.case_id for run in runs] == ["exp-blind", "beer-warm", "planck-diagnostic"]
    assert runs[0].run_id == suite.expanded_runs()[0].run_id
    assert str(runs[0].artifact_path).endswith(f"{runs[0].run_id}.json")
    assert runs[0].claim_id is None
    assert runs[0].threshold_policy_id is None
    assert runs[0].training_mode == "blind_training"
```

Add `v1.9-arrhenius-evidence` to the expected built-ins if a new suite is added. Add a focused assertion that its expanded run has:

```python
case_id == "arrhenius-warm"
formula == "arrhenius"
start_mode == "warm_start"
training_mode == "compiler_warm_start_training"
perturbation_noise == 0.0
```

**FOR_DEMO coverage pattern** (lines 213-225):

```python
suite = load_suite("for-demo-diagnostics")
formulas = {run.formula for run in suite.expanded_runs()}

assert {
    "beer_lambert",
    "radioactive_decay",
    "michaelis_menten",
    "logistic",
    "shockley",
    "damped_oscillator",
    "planck",
} <= formulas
```

Only update this test if the implementation intentionally adds Arrhenius to `for-demo-diagnostics`. The research recommendation prefers a focused suite, so this test can remain unchanged.

---

### `tests/test_proof_dataset_manifest.py` (test, batch transform)

**Analog:** `tests/test_proof_dataset_manifest.py`

**Manifest contract pattern** (lines 29-45):

```python
first = proof_dataset_manifest("exp", points=12, seed=7, tolerance=1e-8)
second = proof_dataset_manifest("exp", points=12, seed=7, tolerance=1e-8)

assert first == second
assert first["schema"] == "eml.proof_dataset_manifest.v1"
assert first["formula_id"] == "exp"
assert first["variable"] == "x"
assert first["seed"] == 7
assert first["tolerance"] == 1e-8
assert first["sample_policy"] == "linspace_with_seeded_0.2_percent_jitter"
assert len(first["manifest_sha256"]) == 64
```

**Domain/no-raw-arrays pattern** (lines 63-72):

```python
manifest = proof_dataset_manifest("exp", points=12, seed=7, tolerance=1e-8)

domains = {split["name"]: split["domain"] for split in manifest["splits"]}
assert domains == {
    "train": [-1.0, 1.0],
    "heldout": [-0.8, 0.8],
    "extrapolation": [1.05, 1.5],
}
assert not (FORBIDDEN_RAW_KEYS & set(_walk_keys(manifest)))
```

**Provenance-all-demos pattern** (lines 89-100):

```python
for formula_id, spec in demo_specs().items():
    provenance = spec.formula_provenance()

    assert provenance["formula_id"] == formula_id
    assert provenance["variable"] == spec.variable
    assert provenance["description"] == spec.description
    assert provenance["symbolic_expression"]
    assert provenance["candidate_name"]
    assert provenance["source_document"]
    assert provenance["source_linkage"]
    assert isinstance(provenance["normalized_dimensionless"], bool)
```

Add an Arrhenius-specific test if useful:

```python
manifest = proof_dataset_manifest("arrhenius", points=24, seed=0, tolerance=1e-8)
assert manifest["formula_id"] == "arrhenius"
assert manifest["variable"] == "x"
assert manifest["provenance"]["source_document"] == "sources/FOR_DEMO.md"
assert manifest["provenance"]["normalized_dimensionless"] is True
assert "exp(-0.8/x)" in manifest["provenance"]["symbolic_expression"]
assert {split["name"]: split["domain"] for split in manifest["splits"]} == {
    "train": [0.5, 3.0],
    "heldout": [0.6, 2.7],
    "extrapolation": [3.1, 4.2],
}
```

Also inspect actual generated splits with `get_demo("arrhenius").make_splits(points=24, seed=0)` and assert all sampled `x` values are positive, because `make_splits()` applies seeded jitter.

---

### `docs/IMPLEMENTATION.md` (documentation, reporting)

**Analog:** `docs/IMPLEMENTATION.md`

**Architecture/module list pattern** (lines 7-19):

```markdown
1. `semantics.py` defines canonical and training-mode EML behavior.
...
11. `benchmark.py` defines repeatable benchmark suites, run execution, post-snap constant refit, per-run artifacts, aggregate evidence reports, and recovery/failure taxonomy.
12. `campaign.py` defines campaign presets, guarded output folders, CSV exports, SVG figures, and `report.md` assembly.
13. `datasets.py` and `cli.py` expose the demo ladder from `sources/FOR_DEMO.md`.
```

**Compiler/warm-start honesty pattern** (lines 47-67):

```markdown
Unsupported functions, unknown variables, unsafe constants, excessive powers, and depth/node budget excesses raise `UnsupportedExpression` with a machine-readable reason code. Every compiled result includes source expression, normalized expression, variables, constants, assumptions, rule trace, depth, and node count.

`literal_constants` means fixed coefficients such as `-0.8`, `0.5`, and `2` are inserted as terminal constants and reported as such. It is not a pure `{1, eml}` synthesis claim.

The compiler now routes supported shortcuts through an explicit macro layer. Current macro rules are `scaled_exp_minus_one_template` for Shockley-style `scale * (exp(a) - 1)` shapes and `direct_division_template` for true numerator-over-denominator motifs such as Michaelis-Menten.
```

Update this text to include Arrhenius as another `direct_division_template` example, while preserving the literal-constant warning.

**Demo ladder pattern** (lines 154-177):

````markdown
## Demo Ladder

The built-in demos mirror `sources/FOR_DEMO.md`:

- `exp`
- `log`
- `beer_lambert`
...
- `planck`

Beer-Lambert and Shockley now have compiler-driven warm-start paths:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli demo beer_lambert --warm-start-eml
PYTHONPATH=src python -m eml_symbolic_regression.cli demo shockley --warm-start-eml --points 24
```
````

Add `arrhenius` to the list and add a command only after tests prove the artifact path:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli demo arrhenius --warm-start-eml --points 24
```

Use claim language: "same-AST exact warm-start return with verifier `recovered`", not "blind discovery".

---

### `README.md` (documentation, reporting)

**Analog:** `README.md`

**Implemented feature list pattern** (lines 13-31):

```markdown
- Verifier-owned recovery status over train, held-out, extrapolation, and mpmath point checks.
- A fail-closed SymPy subset compiler that emits exact EML ASTs with metadata, rule traces, assumptions, literal-constant provenance, and independent validation against ordinary SymPy evaluation.
- Compiler-driven warm-start training reports that perturb, train, snap, and verify through the existing optimizer/verifier boundary.
- Demo specs from `sources/FOR_DEMO.md`.
```

Add Arrhenius as a supported normalized exact warm-start demo without implying blind recovery.

**Quick command pattern** (lines 53-63 and 77-81):

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

Add Arrhenius commands after the tests pass:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli demo arrhenius --warm-start-eml --points 24 --output artifacts/arrhenius-warm-report.json
PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark v1.9-arrhenius-evidence --case arrhenius-warm --seed 0 --output-dir artifacts/benchmarks
```

**Evidence taxonomy pattern** (lines 131-157):

```markdown
- `compiled_seed`: the source formula compiled to an exact EML AST and that AST verified numerically. This is a seed/provenance stage, not a trained recovery claim by itself.
- `warm_start_attempt`: the compiler seed was embedded into a compatible soft tree, optionally perturbed, trained through the existing optimizer, snapped, and classified.
- `trained_exact_recovery`: the post-training snapped exact EML AST passed the verifier. Demo reports promote top-level `claim_status` to `recovered` only at this stage.
...
- `same_ast_return` means a warm-started run snapped back to the compiled seed; this is useful basin-stability evidence, not blind discovery.
```

Preserve this wording when adding Arrhenius. The top-level `claim_status` may be `recovered`, but the regime must remain `same_ast`.

## Shared Patterns

### Strict Compiler Macro Diagnostics

**Source:** `src/eml_symbolic_regression/compiler.py` lines 263-287, 402-430
**Apply to:** dataset candidate shape, compiler tests, CLI artifact assertions, benchmark artifact assertions

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
    ...
    return self._record(
        "direct_division_template",
        expr,
        divide_expr(compiled_numerator, compiled_denominator),
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

### Verifier-Owned Recovery

**Source:** `src/eml_symbolic_regression/verify.py` lines 72-137
**Apply to:** all tests and docs that mention `recovered`

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

Use verifier status for claims; never promote Arrhenius from training loss alone.

### Warm-Start Status and Manifest Diagnosis

**Source:** `src/eml_symbolic_regression/warm_start.py` lines 107-181, 184-231
**Apply to:** compiler warm-start tests, CLI artifact assertions, benchmark metrics

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

manifest = {
    "schema": "eml.warm_start_manifest.v1",
    "status": status,
    "compiler_metadata": compiler_metadata,
    "terminal_bank": {
        "variables": list(config.variables),
        "constants": [format_constant_value(value) for value in config.constants],
    },
    "embedding": embedding.as_dict(),
    "perturbation_config": perturbation_config.__dict__,
    "optimizer": fit.manifest,
    "verification": verification.as_dict() if verification else None,
    "diagnosis": _diagnose_warm_start(status, fit, verification),
}
```

Zero-noise Arrhenius should assert `status == "same_ast_return"` and diagnosis `changed_slot_count == 0`.

### CLI JSON Artifact Shape

**Source:** `src/eml_symbolic_regression/cli.py` lines 108-185
**Apply to:** CLI test and README commands

```python
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
    compiled = compile_and_validate(source_expr, compiler_config, validation_inputs)
    compiled_verification = verify_candidate(compiled.expression, splits, tolerance=args.tolerance)
    payload["compiled_eml"] = compiled.as_dict()
    payload["compiled_eml_verification"] = compiled_verification.as_dict()
    stage_statuses["compiled_seed"] = compiled_verification.status
```

```python
payload["warm_start_eml"] = warm.manifest
stage_statuses["warm_start_attempt"] = warm.status
if warm.verification is not None:
    stage_statuses["trained_exact_recovery"] = warm.verification.status
    if warm.verification.status == "recovered":
        payload["claim_status"] = "recovered"

_write_json(Path(args.output), payload)
```

### Benchmark Evidence Class

**Source:** `src/eml_symbolic_regression/benchmark.py` lines 1495-1511, 2910-2952
**Apply to:** benchmark suite, runner tests, docs

```python
payload.pop("_compiled", None)
payload["evidence_class"] = evidence_class_for_payload(payload)
payload["metrics"] = _extract_run_metrics(payload)
payload["timing"] = {"elapsed_seconds": time.perf_counter() - started}
_write_json(run.artifact_path, payload)
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

For Arrhenius same-AST warm-starts, expected `evidence_class` is `same_ast`, even when `claim_status == "recovered"`.

### FOR_DEMO Arrhenius Source Linkage

**Source:** `sources/FOR_DEMO.md` lines 92-108
**Apply to:** dataset provenance and docs

```markdown
### 5) Arrhenius law

k(T)=A e^{-E_a/(RT)}

**Why it is great**

* classic chemistry/physics
* shows exponential dependence on reciprocal temperature
* strong extrapolation story

**Caution**
Use transformed or nondimensionalized temperature input. Raw SI scaling can make optimization uglier.
```

The Phase 50 dataset should use normalized `x`, not raw SI temperature.

## No Analog Found

No files lack a codebase analog. Planner should not invent new compiler, warm-start, verifier, or artifact schemas for this phase.

## Metadata

**Analog search scope:** `src/eml_symbolic_regression`, `tests`, `docs`, `README.md`, `sources/FOR_DEMO.md`
**Files scanned:** 20 source/test/doc files plus phase artifacts
**Pattern extraction date:** 2026-04-17
