# Phase 49: Witness Registry and Centered Scaffold Correctness - Research

**Researched:** 2026-04-17 [VERIFIED: current_date]
**Domain:** Python package scaffold/witness availability, operator-family routing, benchmark artifact contracts [VERIFIED: .planning/ROADMAP.md]
**Confidence:** HIGH for local code architecture, HIGH for required behavior, MEDIUM for exact public API naming because no prior registry module exists [VERIFIED: src/eml_symbolic_regression][VERIFIED: .planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md]

<user_constraints>
## User Constraints (from CONTEXT.md)

The following block is copied from `.planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md`; it is user/project constraint input for planning. [VERIFIED: .planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md]

### Locked Decisions

#### Registry Contract
- Add an inspectable witness or initializer registry keyed by scaffold kind and operator family.
- Treat existing `exp`, `log`, and `scaled_exp` scaffold helpers as raw EML witnesses until a same-family centered witness is explicitly registered and tested.
- Keep raw EML defaults unchanged so existing shallow scaffolded and raw-hybrid evidence paths do not regress.
- Prefer fail-closed registry lookups over ad hoc conditionals at individual call sites.

#### Centered Exclusion Semantics
- Centered `CEML_s`, `ZEML_s`, and continuation variants must drop raw scaffold attempts unless a same-family registry entry exists.
- Use the canonical reason code `centered_family_same_family_witness_missing` for scaffold exclusions in optimizer and benchmark artifacts.
- Preserve the existing `centered_family_same_family_seed_missing` reason for warm-start and perturbed-tree exact-seed gates.
- Tests should prove centered-family runs cannot directly reach raw scaffold helpers through benchmark budgets or optimizer attempt generation.

#### Artifact and Test Coverage
- Benchmark budgets, run artifacts, aggregate metrics, and optimizer manifests should expose scaffold exclusions with operator-family context.
- Add focused tests near `tests/test_benchmark_contract.py`, `tests/test_benchmark_runner.py`, and optimizer cleanup/manifest coverage rather than broad campaign reruns.
- Existing v1.8 centered-family evidence should remain interpretable as negative diagnostic evidence with a corrected scaffold-confound boundary.
- Keep the implementation reusable for future same-family centered witnesses without enabling unsupported centered recovery by default.

### Claude's Discretion

Use the smallest registry shape that makes current scaffold availability auditable and blocks centered raw-witness contamination. Avoid formula-specific exceptions and avoid changing verifier-owned recovery semantics.

### Deferred Ideas (OUT OF SCOPE)

Constructing actual centered-family witnesses for `exp`, `log`, scaled exponentials, and reciprocal motifs remains deferred to the centered-family theory track.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| WIT-01 | Developer can inspect an explicit witness/initializer registry that declares scaffold availability by operator family. | Add a small registry module with serializable entries for `exp`, `log`, and `scaled_exp`, initially registered only for `raw_eml`. [VERIFIED: .planning/REQUIREMENTS.md][VERIFIED: src/eml_symbolic_regression/optimize.py:486] |
| WIT-02 | Centered families no longer receive raw `exp`, `log`, or `scaled_exp` scaffold attempts unless a tested same-family witness is registered. | Resolve requested scaffolds through the registry for the initial operator in both benchmark variants and optimizer attempts. [VERIFIED: .planning/REQUIREMENTS.md][VERIFIED: src/eml_symbolic_regression/benchmark.py:951][VERIFIED: src/eml_symbolic_regression/optimize.py:486] |
| WIT-03 | Raw-specific scaffold helpers fail closed or are only reachable through raw-family registry entries. | Guard `_apply_scaffold()` and the direct `SoftEMLTree.force_exp`, `force_log`, and `force_scaled_exp` paths with registry checks for non-raw operators. [VERIFIED: .planning/REQUIREMENTS.md][VERIFIED: src/eml_symbolic_regression/optimize.py:603][VERIFIED: src/eml_symbolic_regression/master_tree.py:556] |
| WIT-04 | Benchmark and optimizer artifacts record centered scaffold exclusions with explicit reason codes such as `centered_family_same_family_witness_missing`. | Preserve existing `OptimizerBudget.scaffold_exclusions`, add optimizer-manifest exclusions, and expose metrics through `_extract_run_metrics()`. [VERIFIED: .planning/REQUIREMENTS.md][VERIFIED: src/eml_symbolic_regression/benchmark.py:140][VERIFIED: src/eml_symbolic_regression/benchmark.py:2406] |
</phase_requirements>

## Summary

Phase 49 should be planned as a small internal contract change, not as a new math feature: add an inspectable scaffold witness registry, route scaffold selection through it, and make centered-family missing witnesses visible in budget, optimizer, run, and aggregate artifacts. [VERIFIED: .planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md][VERIFIED: .planning/ROADMAP.md]

The current risk is real because optimizer scaffold attempts are generated from raw string names in `_training_attempts()`, and `_apply_scaffold()` calls `force_exp()` or `force_log()` without checking the model's operator family. [VERIFIED: src/eml_symbolic_regression/optimize.py:486][VERIFIED: src/eml_symbolic_regression/optimize.py:603] The current benchmark family variant code only removes `scaled_exp` from centered variants and leaves `exp` and `log` scaffold names available under centered operators. [VERIFIED: src/eml_symbolic_regression/benchmark.py:951][VERIFIED: tests/test_benchmark_contract.py:55]

**Primary recommendation:** Add `src/eml_symbolic_regression/witnesses.py` as the single scaffold availability authority, then use it from `benchmark._operator_variant_budget()`, `benchmark._training_config_from_budget()`, `optimize.fit_eml_tree()`, and raw scaffold helper guards. [VERIFIED: src/eml_symbolic_regression/benchmark.py:951][VERIFIED: src/eml_symbolic_regression/benchmark.py:1999][VERIFIED: src/eml_symbolic_regression/optimize.py:294][VERIFIED: src/eml_symbolic_regression/master_tree.py:556]

## Project Constraints (from AGENTS.md)

- Paper fidelity is a project constraint, so scaffold/witness behavior must not imply centered-family constructive completeness without tested centered witnesses. [VERIFIED: AGENTS.md][VERIFIED: artifacts/paper/v1.8/unsafe-claims.md]
- Training defaults and verification semantics should remain grounded in existing PyTorch complex training and post-snap verification contracts. [VERIFIED: AGENTS.md][VERIFIED: pyproject.toml][VERIFIED: src/eml_symbolic_regression/optimize.py:18]
- Candidates are not considered recovered based on training loss alone; verifier-owned status remains outside this phase's registry work. [VERIFIED: AGENTS.md][VERIFIED: src/eml_symbolic_regression/benchmark.py:1565]
- Demos and claims must avoid overclaiming centered-family completeness or universal blind recovery. [VERIFIED: AGENTS.md][VERIFIED: artifacts/paper/v1.8/unsafe-claims.md]
- GSD workflow requires writing the research artifact through the phase workflow before implementation edits. [VERIFIED: AGENTS.md][VERIFIED: .planning/config.json]
- `CLAUDE.md` is absent in the repository root, and no project-local `.claude/skills` or `.agents/skills` directories are present. [VERIFIED: ls CLAUDE.md][VERIFIED: ls .claude/skills][VERIFIED: ls .agents/skills]
- `.planning/graphs/graph.json` is absent, so no knowledge-graph context was available for this research. [VERIFIED: ls .planning/graphs/graph.json]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|--------------|----------------|-----------|
| Scaffold witness declaration | Core package registry | Semantics metadata | Registry decisions depend on `EmlOperator.family` and should be reusable outside benchmark code. [VERIFIED: src/eml_symbolic_regression/semantics.py:13][VERIFIED: src/eml_symbolic_regression/benchmark.py:951] |
| Benchmark scaffold filtering | Benchmark orchestration | Core registry | Family suite expansion mutates `OptimizerBudget.scaffold_initializers` before runs are materialized. [VERIFIED: src/eml_symbolic_regression/benchmark.py:116][VERIFIED: src/eml_symbolic_regression/benchmark.py:951] |
| Optimizer scaffold attempt generation | Optimizer | Core registry | Direct optimizer callers can bypass benchmark filtering today, so `_training_attempts()` must also fail closed. [VERIFIED: src/eml_symbolic_regression/optimize.py:18][VERIFIED: src/eml_symbolic_regression/optimize.py:486] |
| Raw helper execution guard | Master tree / optimizer helper boundary | Core registry | `force_exp()` and `force_log()` currently encode raw paper identities by slot placement and do not check centered operators. [VERIFIED: src/eml_symbolic_regression/master_tree.py:556][VERIFIED: src/eml_symbolic_regression/expression.py:498] |
| Artifact visibility | Benchmark artifact layer | Campaign tables | Run metrics already expose `operator_family`, `operator_schedule`, and `scaffold_exclusions`, and campaign tables consume these metrics. [VERIFIED: src/eml_symbolic_regression/benchmark.py:2406][VERIFIED: src/eml_symbolic_regression/campaign.py:725] |

## Standard Stack

### Core

| Library / Module | Version | Purpose | Why Standard |
|------------------|---------|---------|--------------|
| Python `dataclasses` | stdlib in Python 3.11.5 | Define immutable registry entries and exclusion records. | Existing configs use frozen dataclasses for `TrainingConfig` and `OptimizerBudget`. [VERIFIED: python --version][VERIFIED: src/eml_symbolic_regression/optimize.py:18][VERIFIED: src/eml_symbolic_regression/benchmark.py:116] |
| `eml_symbolic_regression.semantics.EmlOperator` | local module | Normalize raw, `CEML_s`, `ZEML_s`, and shifted centered operator identity. | Existing operator-family parsing and labels are centralized in `semantics.py`. [VERIFIED: src/eml_symbolic_regression/semantics.py:13][VERIFIED: src/eml_symbolic_regression/semantics.py:131] |
| New `eml_symbolic_regression.witnesses` module | local module to add | Own scaffold witness availability and exclusion reason construction. | No existing registry exists, and current logic is split between benchmark filtering and optimizer attempt generation. [VERIFIED: src/eml_symbolic_regression/benchmark.py:951][VERIFIED: src/eml_symbolic_regression/optimize.py:486] |
| PyTorch | 2.10.0 local, `torch>=2.10` project dependency | Execute existing soft tree optimization after scaffold attempts are resolved. | The project already uses PyTorch in optimizer and master-tree code, and this phase should not alter training math. [VERIFIED: python -c package version probe][VERIFIED: pyproject.toml][VERIFIED: src/eml_symbolic_regression/optimize.py:1] |

### Supporting

| Library / Module | Version | Purpose | When to Use |
|------------------|---------|---------|-------------|
| pytest | 7.4.0 local, `pytest>=7.4` dev dependency | Focused regression tests for registry, benchmark contracts, runner artifacts, and optimizer manifests. | Use for WIT-01 through WIT-04 tests. [VERIFIED: python -c package version probe][VERIFIED: pyproject.toml] |
| NumPy | 1.26.4 local, `numpy>=1.26` dependency | Existing tests and optimizer fixtures use NumPy arrays. | Keep existing optimizer and benchmark tests unchanged except assertions around scaffolds. [VERIFIED: python -c package version probe][VERIFIED: pyproject.toml][VERIFIED: tests/test_optimizer_cleanup.py:39] |
| `EmbeddingError` | local exception | Fail closed for direct incompatible scaffold embedding. | Reuse existing reason/detail exception shape for direct helper guard failures. [VERIFIED: src/eml_symbolic_regression/master_tree.py:215] |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Dedicated registry module | Add conditionals in `_operator_variant_budget()` and `_training_attempts()` | Ad hoc conditionals would satisfy current cases but would violate the locked decision to prefer fail-closed registry lookups. [VERIFIED: .planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md] |
| Immutable tuple registry | Mutable runtime registration API | Runtime registration is more flexible, but the current phase only needs auditable source-controlled entries and should avoid test-order side effects. [VERIFIED: .planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md] |
| Structured exclusion objects only | Existing string `kind:reason` fields only | Existing string fields are already serialized and tested, so keep them for compatibility and optionally add richer records only if needed. [VERIFIED: src/eml_symbolic_regression/benchmark.py:140][VERIFIED: src/eml_symbolic_regression/benchmark.py:328] |

**Installation:**

```bash
# No new dependency is required for Phase 49.
python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py tests/test_optimizer_cleanup.py
```

The package already declares Python `>=3.11,<3.13`, `torch>=2.10`, `numpy>=1.26`, `sympy>=1.14`, and `mpmath>=1.3`; local versions are Python 3.11.5, torch 2.10.0, NumPy 1.26.4, SymPy 1.14.0, mpmath 1.3.0, and pytest 7.4.0. [VERIFIED: pyproject.toml][VERIFIED: python --version][VERIFIED: python -c package version probe]

## Architecture Patterns

### System Architecture Diagram

```text
Benchmark suite / direct optimizer caller
        |
        v
Requested scaffold names: ("exp", "log", "scaled_exp")
        |
        v
Initial operator family selection
  - benchmark: operator_schedule[0] if present, else operator_family
  - optimizer: _operator_for_step(config, 0, max(steps, 1))
        |
        v
witnesses.resolve_scaffold_plan(requested, operator, depth, constants)
        |
        +--> enabled raw witnesses -> optimizer _training_attempts()
        |                             -> _apply_scaffold() guard
        |
        +--> excluded centered witnesses -> budget.scaffold_exclusions
                                      -> training manifest scaffold_exclusions
                                      -> run metrics scaffold_exclusions
                                      -> aggregate/campaign artifacts
```

The diagram matches current data flow because benchmark variants are cloned through `_operator_variant_budget()`, benchmark runs become `TrainingConfig` objects through `_training_config_from_budget()`, optimizer attempts are generated in `_training_attempts()`, and run metrics are extracted in `_extract_run_metrics()`. [VERIFIED: src/eml_symbolic_regression/benchmark.py:951][VERIFIED: src/eml_symbolic_regression/benchmark.py:1999][VERIFIED: src/eml_symbolic_regression/optimize.py:486][VERIFIED: src/eml_symbolic_regression/benchmark.py:2406]

### Recommended Project Structure

```text
src/eml_symbolic_regression/
├── witnesses.py      # new scaffold witness registry and availability resolver
├── optimize.py       # consume resolved scaffold plan and guard raw scaffold application
├── benchmark.py      # filter benchmark budgets and serialize centered scaffold exclusions
├── master_tree.py    # direct raw scaffold helper guards
└── __init__.py       # optional public export for registry inspection

tests/
├── test_benchmark_contract.py  # suite expansion and budget exclusion contract
├── test_benchmark_runner.py    # artifact/aggregate reason-code survival
└── test_optimizer_cleanup.py   # direct optimizer and helper fail-closed coverage
```

The new module keeps witness availability separate from numerical semantics and benchmark suite construction. [VERIFIED: src/eml_symbolic_regression/semantics.py:13][VERIFIED: src/eml_symbolic_regression/benchmark.py:951]

### Pattern 1: Immutable Witness Registry

**What:** Use frozen dataclasses for registry entries, with each entry declaring `kind`, `operator_family`, `attempt_kind`, `min_depth`, and strategy metadata. [VERIFIED: src/eml_symbolic_regression/optimize.py:18][VERIFIED: src/eml_symbolic_regression/benchmark.py:116]

**When to use:** Use for all scaffold availability decisions before appending scaffold attempts or calling scaffold helpers. [VERIFIED: src/eml_symbolic_regression/optimize.py:486][VERIFIED: src/eml_symbolic_regression/optimize.py:603]

**Example:**

```python
# Proposed local pattern, derived from existing frozen config dataclasses.
@dataclass(frozen=True)
class ScaffoldWitness:
    kind: str
    operator_family: str
    attempt_kind: str
    min_depth: int
    strategy: str


SCAFFOLD_WITNESSES = (
    ScaffoldWitness("exp", "raw_eml", "scaffold_exp", 1, "generic_paper_primitive"),
    ScaffoldWitness("log", "raw_eml", "scaffold_log", 3, "generic_paper_primitive"),
    ScaffoldWitness("scaled_exp", "raw_eml", "scaffold_scaled_exp", 9, "paper_scaled_exponential_family"),
)
```

The current raw scaffold strategies already appear as initialization metadata from `_apply_scaffold()`. [VERIFIED: src/eml_symbolic_regression/optimize.py:603][VERIFIED: tests/test_optimizer_cleanup.py:140]

### Pattern 2: Single Scaffold Plan Resolver

**What:** Convert requested scaffold names into enabled names plus `kind:reason` exclusions for the active operator family. [VERIFIED: src/eml_symbolic_regression/benchmark.py:140][VERIFIED: src/eml_symbolic_regression/benchmark.py:328]

**When to use:** Use in benchmark budget cloning and optimizer attempt generation so direct optimizer calls cannot bypass benchmark filtering. [VERIFIED: src/eml_symbolic_regression/benchmark.py:951][VERIFIED: src/eml_symbolic_regression/optimize.py:486]

**Example:**

```python
# Proposed local pattern.
CENTERED_FAMILY_SAME_FAMILY_WITNESS_MISSING = "centered_family_same_family_witness_missing"


def scaffold_exclusion_code(kind: str, reason: str) -> str:
    return f"{kind}:{reason}"


def resolve_scaffold_plan(requested: Iterable[str], operator: EmlOperator) -> ScaffoldPlan:
    enabled: list[str] = []
    exclusions: list[str] = []
    for kind in requested:
        witness = scaffold_witness_for(kind, operator)
        if witness is None and not operator.is_raw:
            exclusions.append(scaffold_exclusion_code(kind, CENTERED_FAMILY_SAME_FAMILY_WITNESS_MISSING))
            continue
        if witness is not None:
            enabled.append(kind)
    return ScaffoldPlan(tuple(enabled), tuple(dict.fromkeys(exclusions)))
```

Depth and constant feasibility should remain separate from same-family witness availability to avoid turning existing depth skips into new denominator exclusions. [VERIFIED: src/eml_symbolic_regression/optimize.py:491][VERIFIED: src/eml_symbolic_regression/optimize.py:591]

### Pattern 3: Initial Operator, Not Final Operator, Owns Scaffold Availability

**What:** Resolve scaffold witnesses against the operator active at initialization time. [VERIFIED: src/eml_symbolic_regression/optimize.py:319][VERIFIED: src/eml_symbolic_regression/optimize.py:529]

**When to use:** Use for continuation schedules because the scaffold is applied before training begins and before hardening switches to the final operator. [VERIFIED: src/eml_symbolic_regression/optimize.py:319][VERIFIED: src/eml_symbolic_regression/optimize.py:397]

**Example:**

```python
# Proposed local pattern.
def initial_training_operator(config: TrainingConfig) -> EmlOperator:
    return _operator_for_step(config, 0, max(config.steps, 1))
```

This preserves current schedule semantics, where `operator_schedule[0]` is used at step 0 and `_final_operator()` is used for hardening. [VERIFIED: src/eml_symbolic_regression/optimize.py:529][VERIFIED: src/eml_symbolic_regression/optimize.py:538]

### Anti-Patterns to Avoid

- **Filtering only in benchmark suites:** Direct `fit_eml_tree()` callers can construct centered configs with raw default scaffold names, so optimizer-level filtering is required. [VERIFIED: src/eml_symbolic_regression/optimize.py:18][VERIFIED: src/eml_symbolic_regression/optimize.py:294]
- **Leaving `exp` and `log` centered scaffolds enabled because only `scaled_exp` was excluded before:** The phase explicitly classifies all three current helpers as raw EML witnesses. [VERIFIED: .planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md][VERIFIED: src/eml_symbolic_regression/benchmark.py:951]
- **Using the old reason code `centered_family_incompatible_raw_witness`:** The phase locks the canonical scaffold exclusion reason to `centered_family_same_family_witness_missing`. [VERIFIED: .planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md][VERIFIED: tests/test_benchmark_contract.py:77]
- **Changing verifier-owned recovery semantics:** This phase is about attempts and artifacts; verification status should remain owned by `verify_candidate()` and benchmark result logic. [VERIFIED: AGENTS.md][VERIFIED: src/eml_symbolic_regression/benchmark.py:1565]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Per-call-site scaffold filtering | Repeated `if not operator.is_raw` checks in benchmark and optimizer | One registry resolver in `witnesses.py` | The locked decision asks for fail-closed registry lookups instead of ad hoc conditionals. [VERIFIED: .planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md] |
| A new formula recognizer | Formula-specific exceptions for `exp`, `log`, or Beer-Lambert | Generic scaffold-kind registry entries | Future centered witnesses must be registered as same-family witnesses, not formula-specific shortcuts. [VERIFIED: .planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md] |
| A new dependency | Pydantic or plugin registry framework | stdlib dataclasses plus tuple registry | The repo already uses dataclasses for configs and does not need schema-heavy runtime machinery for three scaffold kinds. [VERIFIED: src/eml_symbolic_regression/optimize.py:18][VERIFIED: src/eml_symbolic_regression/benchmark.py:116] |
| Artifact-only fix | Only adding metrics without blocking attempts | Registry filtering plus helper guards | WIT-02 and WIT-03 require centered runs to stop receiving raw scaffold attempts, not just to label them after use. [VERIFIED: .planning/REQUIREMENTS.md][VERIFIED: src/eml_symbolic_regression/optimize.py:486] |

**Key insight:** The plan must close both entry points: benchmark expansion and direct optimizer calls. [VERIFIED: src/eml_symbolic_regression/benchmark.py:951][VERIFIED: src/eml_symbolic_regression/optimize.py:294]

## Common Pitfalls

### Pitfall 1: Benchmark-Only Filtering

**What goes wrong:** Centered family suites look clean, but direct `fit_eml_tree()` calls can still use default raw scaffolds. [VERIFIED: src/eml_symbolic_regression/optimize.py:18][VERIFIED: src/eml_symbolic_regression/optimize.py:486]

**Why it happens:** `TrainingConfig.scaffold_initializers` defaults to `("exp", "log", "scaled_exp")` and `_training_attempts()` currently consumes those strings directly. [VERIFIED: src/eml_symbolic_regression/optimize.py:40][VERIFIED: src/eml_symbolic_regression/optimize.py:486]

**How to avoid:** Resolve scaffold availability inside `fit_eml_tree()` or `_training_attempts()` against the initial operator, and include computed exclusions in the optimizer manifest. [VERIFIED: src/eml_symbolic_regression/optimize.py:294][VERIFIED: src/eml_symbolic_regression/optimize.py:529]

**Warning signs:** A centered optimizer manifest has `best_restart.attempt_kind` starting with `scaffold_`. [VERIFIED: src/eml_symbolic_regression/benchmark.py:2960]

### Pitfall 2: Guarding `scaled_exp` But Not `exp` or `log`

**What goes wrong:** `scaled_exp` is excluded under centered variants, but `exp` and `log` still seed centered trees with raw paper identities. [VERIFIED: src/eml_symbolic_regression/benchmark.py:951][VERIFIED: tests/test_benchmark_contract.py:72]

**Why it happens:** `_operator_variant_budget()` currently filters only `scaled_exp`. [VERIFIED: src/eml_symbolic_regression/benchmark.py:951]

**How to avoid:** Treat all registered raw scaffold kinds as unavailable for non-raw operators unless a same-family registry entry exists. [VERIFIED: .planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md]

**Warning signs:** A centered benchmark budget still includes `exp` or `log` in `scaffold_initializers`. [VERIFIED: tests/test_benchmark_contract.py:72]

### Pitfall 3: Using Final Continuation Operator For Scaffold Decisions

**What goes wrong:** A continuation run can be judged against the wrong operator if filtering uses `_final_operator()` instead of the operator active when the scaffold is applied. [VERIFIED: src/eml_symbolic_regression/optimize.py:529][VERIFIED: src/eml_symbolic_regression/optimize.py:538]

**Why it happens:** Training uses a schedule for steps and then uses the final operator for hardening. [VERIFIED: src/eml_symbolic_regression/optimize.py:337][VERIFIED: src/eml_symbolic_regression/optimize.py:397]

**How to avoid:** Use `operator_schedule[0]` or `_operator_for_step(config, 0, max(config.steps, 1))` for scaffold availability. [VERIFIED: src/eml_symbolic_regression/benchmark.py:1952][VERIFIED: src/eml_symbolic_regression/optimize.py:529]

**Warning signs:** `ZEML_8 -> ZEML_4` runs receive raw scaffold attempts because filtering checked only `ZEML_4`. [VERIFIED: tests/test_benchmark_runner.py:146]

### Pitfall 4: Breaking Raw Shallow Proof Behavior

**What goes wrong:** Raw EML scaffolded proof suites lose `exp`, `log`, or `scaled_exp` attempts and existing shallow recovery tests fail. [VERIFIED: tests/test_optimizer_cleanup.py:140][VERIFIED: tests/test_benchmark_runner.py:247]

**Why it happens:** Registry filtering can accidentally treat raw EML as needing the same missing-witness exclusion as centered families. [VERIFIED: .planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md]

**How to avoid:** Register the three current witnesses for `raw_eml` first and assert raw budgets/manifests remain unchanged. [VERIFIED: .planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md]

**Warning signs:** `test_optimizer_scaled_exp_scaffold_recovers_radioactive_decay_with_manifest` or `test_shallow_beer_lambert_blind_run_artifact_exposes_scaled_scaffold_diagnostics` fails. [VERIFIED: tests/test_optimizer_cleanup.py:140][VERIFIED: tests/test_benchmark_runner.py:247]

## Code Examples

### Registry Inspection

```python
# Proposed public inspection API.
from eml_symbolic_regression.witnesses import list_scaffold_witnesses

witnesses = list_scaffold_witnesses()
assert {"kind": "exp", "operator_family": "raw_eml"} in witnesses
```

This directly supports WIT-01 by making scaffold availability inspectable rather than implicit in optimizer conditionals. [VERIFIED: .planning/REQUIREMENTS.md][VERIFIED: src/eml_symbolic_regression/optimize.py:486]

### Benchmark Budget Filtering

```python
# Proposed replacement pattern inside _operator_variant_budget().
operator = variant.operator_schedule[0] if variant.operator_schedule else variant.operator_family
plan = resolve_scaffold_plan(base.scaffold_initializers, operator)
return replace(
    base,
    scaffold_initializers=plan.enabled,
    scaffold_exclusions=tuple(dict.fromkeys((*base.scaffold_exclusions, *plan.exclusions))),
    operator_family=variant.operator_family,
    operator_schedule=variant.operator_schedule,
)
```

This keeps family-suite clone behavior in the current location while replacing the current `scaled_exp`-only special case. [VERIFIED: src/eml_symbolic_regression/benchmark.py:951]

### Optimizer Attempt Filtering

```python
# Proposed optimizer-side pattern.
initial_operator = _operator_for_step(config, 0, max(config.steps, 1))
plan = resolve_scaffold_plan(config.scaffold_initializers, initial_operator)
attempts = _training_attempts(replace(config, scaffold_initializers=plan.enabled), initializer is not None)
```

This prevents direct centered `TrainingConfig` calls from generating raw scaffold attempts. [VERIFIED: src/eml_symbolic_regression/optimize.py:294][VERIFIED: src/eml_symbolic_regression/optimize.py:486]

### Raw Helper Guard

```python
# Proposed fail-closed guard before invoking force_exp/force_log/force_scaled_exp.
def _require_scaffold_witness(kind: str, operator: EmlOperator) -> None:
    if scaffold_witness_for(kind, operator) is None:
        raise ValueError(f"{kind}:centered_family_same_family_witness_missing")
```

Direct guards are needed because `_apply_scaffold()` can reach raw helpers after attempt generation, and `SoftEMLTree.force_exp()` and `force_log()` currently do not check `operator_family`. [VERIFIED: src/eml_symbolic_regression/optimize.py:603][VERIFIED: src/eml_symbolic_regression/master_tree.py:556]

## State of the Art

| Old Approach | Current Phase Approach | When Changed | Impact |
|--------------|------------------------|--------------|--------|
| Centered benchmark variants only removed `scaled_exp` and recorded `scaled_exp:centered_family_incompatible_raw_witness`. | Centered variants remove all raw-only scaffold kinds and record `*:centered_family_same_family_witness_missing`. | Phase 49. [VERIFIED: src/eml_symbolic_regression/benchmark.py:951][VERIFIED: .planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md] | Eliminates centered raw-witness contamination for `exp`, `log`, and `scaled_exp`. [VERIFIED: .planning/REQUIREMENTS.md] |
| Warm-start and perturbed-tree centered paths already failed closed with `centered_family_same_family_seed_missing`. | Preserve that seed-specific reason while adding witness-specific scaffold exclusions. | Phase 45 introduced the existing seed gate, and Phase 49 adds scaffold witness gates. [VERIFIED: src/eml_symbolic_regression/benchmark.py:1686][VERIFIED: src/eml_symbolic_regression/benchmark.py:1829][VERIFIED: .planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md] | Avoids conflating missing exact seeds with missing scaffold witnesses. [VERIFIED: .planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md] |
| Scaffold availability was implicit in private optimizer strings and helper functions. | Scaffold availability becomes inspectable through a registry. | Phase 49. [VERIFIED: .planning/REQUIREMENTS.md][VERIFIED: src/eml_symbolic_regression/optimize.py:486] | Future centered witnesses can be added without reopening benchmark and optimizer filtering logic. [VERIFIED: .planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md] |

**Deprecated/outdated:**

- `scaled_exp:centered_family_incompatible_raw_witness` should be replaced for centered scaffold exclusions by the canonical `centered_family_same_family_witness_missing` reason code. [VERIFIED: .planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md][VERIFIED: tests/test_benchmark_contract.py:77]
- Treating centered `CEML_s` or `ZEML_s` results as proof against centered-family viability is unsafe without same-family witnesses; v1.8 artifacts already warn against centered overclaims. [VERIFIED: artifacts/paper/v1.8/unsafe-claims.md][VERIFIED: artifacts/paper/v1.8/completeness-boundary.md]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| None | All implementation-relevant claims in this research were checked against local code, project planning artifacts, or local environment probes. [VERIFIED: rg inspections][VERIFIED: python version probes] | All | Low. |

## Open Questions

1. **Should the registry be exported from package `__init__.py`?** [VERIFIED: src/eml_symbolic_regression/__init__.py]
   - What we know: `__init__.py` exports public package symbols today, including `EmlOperator` and operator constructors. [VERIFIED: src/eml_symbolic_regression/__init__.py]
   - What's unclear: WIT-01 requires developer inspection but does not require top-level package export. [VERIFIED: .planning/REQUIREMENTS.md]
   - Recommendation: Export `list_scaffold_witnesses`, `scaffold_witness_for`, and the canonical reason constant if tests or CLI docs need top-level access; otherwise keep module-level import in `eml_symbolic_regression.witnesses`. [VERIFIED: src/eml_symbolic_regression/__init__.py]

2. **Should benchmark `scaffold_exclusions` stay string-only or gain structured records?** [VERIFIED: src/eml_symbolic_regression/benchmark.py:140]
   - What we know: `OptimizerBudget.as_dict()` serializes `scaffold_exclusions` as a list of strings and metrics copy that list into run metrics. [VERIFIED: src/eml_symbolic_regression/benchmark.py:328][VERIFIED: src/eml_symbolic_regression/benchmark.py:2472]
   - What's unclear: The success criteria require reason codes with operator-family context, but do not require a new artifact schema. [VERIFIED: .planning/ROADMAP.md][VERIFIED: .planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md]
   - Recommendation: Keep the string field for compatibility and rely on adjacent `operator_family` / `operator_schedule` fields for context unless implementation tests reveal an explicit structured-detail gap. [VERIFIED: src/eml_symbolic_regression/benchmark.py:2470][VERIFIED: src/eml_symbolic_regression/benchmark.py:2472]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| Python | Package code and tests | yes | 3.11.5 | None needed. [VERIFIED: python --version] |
| pytest | Focused regression tests | yes | 7.4.0 | None needed. [VERIFIED: python -c package version probe][VERIFIED: pyproject.toml] |
| PyTorch | Existing optimizer tests | yes | 2.10.0 | None needed for Phase 49. [VERIFIED: python -c package version probe][VERIFIED: pyproject.toml] |
| NumPy | Existing benchmark/optimizer fixtures | yes | 1.26.4 | None needed for Phase 49. [VERIFIED: python -c package version probe][VERIFIED: pyproject.toml] |

**Missing dependencies with no fallback:** None found for this phase. [VERIFIED: python -c package version probe]

**Missing dependencies with fallback:** None found for this phase. [VERIFIED: python -c package version probe]

## Security Domain

`.planning/config.json` does not define `security_enforcement: false`, so the security-domain section is included. [VERIFIED: .planning/config.json]

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | no | No authentication surface is touched by this phase. [VERIFIED: src/eml_symbolic_regression] |
| V3 Session Management | no | No session surface is touched by this phase. [VERIFIED: src/eml_symbolic_regression] |
| V4 Access Control | no | No user/role access-control surface exists in the inspected code. [VERIFIED: src/eml_symbolic_regression] |
| V5 Input Validation | yes | Validate scaffold kind names through the registry and existing `BenchmarkValidationError` paths. [VERIFIED: src/eml_symbolic_regression/benchmark.py:288][VERIFIED: .planning/REQUIREMENTS.md] |
| V6 Cryptography | no | No cryptographic operation is touched by this phase. [VERIFIED: src/eml_symbolic_regression] |

### Known Threat Patterns for This Stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Artifact integrity drift from implicit raw scaffold use under centered operators | Tampering | Fail closed in registry lookup and serialize exclusions with reason codes. [VERIFIED: .planning/REQUIREMENTS.md][VERIFIED: src/eml_symbolic_regression/benchmark.py:2406] |
| Evidence repudiation from missing denominator-visible exclusions | Repudiation | Preserve exclusions in benchmark budgets, optimizer manifests, run metrics, and aggregate runs. [VERIFIED: .planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md][VERIFIED: src/eml_symbolic_regression/benchmark.py:2579] |
| Invalid scaffold names silently ignored | Tampering | Keep or strengthen `OptimizerBudget.validate()` using registry-known scaffold kinds. [VERIFIED: src/eml_symbolic_regression/benchmark.py:288] |

## Sources

### Primary (HIGH confidence)

- `.planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md` - locked Phase 49 decisions, centered exclusion semantics, artifact/test scope. [VERIFIED: cat]
- `.planning/REQUIREMENTS.md` - WIT-01 through WIT-04 requirement definitions. [VERIFIED: cat]
- `.planning/ROADMAP.md` - Phase 49 goal, success criteria, and milestone sequencing. [VERIFIED: cat]
- `.planning/STATE.md` - v1.8 history and centered-family claim boundary. [VERIFIED: cat]
- `AGENTS.md` - project constraints and GSD workflow rule. [VERIFIED: cat]
- `src/eml_symbolic_regression/optimize.py` - current training config, scaffold attempt generation, operator schedule, and `_apply_scaffold()` behavior. [VERIFIED: rg][VERIFIED: sed]
- `src/eml_symbolic_regression/benchmark.py` - optimizer budget fields, centered budget filtering, artifact metrics, aggregate evidence. [VERIFIED: rg][VERIFIED: sed]
- `src/eml_symbolic_regression/master_tree.py` - direct scaffold helper and embedding mismatch behavior. [VERIFIED: rg][VERIFIED: sed]
- `src/eml_symbolic_regression/semantics.py` - `EmlOperator` family parsing and labels. [VERIFIED: rg][VERIFIED: sed]
- `tests/test_benchmark_contract.py`, `tests/test_benchmark_runner.py`, `tests/test_optimizer_cleanup.py`, `tests/test_campaign.py` - current regression surfaces for this phase. [VERIFIED: rg][VERIFIED: sed]

### Secondary (MEDIUM confidence)

- `artifacts/paper/v1.8/unsafe-claims.md` and `artifacts/paper/v1.8/completeness-boundary.md` - current claim boundary around centered-family witnesses. [VERIFIED: rg]
- `.planning/milestones/v1.8-phases/45-centered-integration-fixes/*` - prior centered same-family seed gate and scaffold-exclusion history. [VERIFIED: rg]

### Tertiary (LOW confidence)

- None. [VERIFIED: source review]

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH - no new dependency is needed, and local package versions were probed. [VERIFIED: pyproject.toml][VERIFIED: python -c package version probe]
- Architecture: HIGH - current scaffold, benchmark, optimizer, and artifact paths were inspected directly. [VERIFIED: src/eml_symbolic_regression/benchmark.py:951][VERIFIED: src/eml_symbolic_regression/optimize.py:486][VERIFIED: src/eml_symbolic_regression/benchmark.py:2406]
- Pitfalls: HIGH - each pitfall maps to an existing hardcoded path or locked Phase 49 decision. [VERIFIED: .planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-CONTEXT.md][VERIFIED: src/eml_symbolic_regression/benchmark.py:951][VERIFIED: src/eml_symbolic_regression/optimize.py:486]
- Public API naming: MEDIUM - a new registry module is recommended, but WIT-01 does not require top-level package export. [VERIFIED: .planning/REQUIREMENTS.md][VERIFIED: src/eml_symbolic_regression/__init__.py]

**Research date:** 2026-04-17 [VERIFIED: current_date]
**Valid until:** 2026-05-17, unless scaffold, benchmark, or optimizer architecture changes first. [VERIFIED: current repository state]
