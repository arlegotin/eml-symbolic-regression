# Architecture Patterns: v1.1 EML Compiler and Warm Starts

**Domain:** Hybrid EML symbolic-regression engine  
**Project:** EML Symbolic Regression  
**Researched:** 2026-04-15  
**Overall confidence:** HIGH for integration with the current v1 code; MEDIUM for exact arithmetic-compiler coverage beyond direct `exp`/`log` and literal-constant demos.

## Executive Summary

v1.1 should extend the existing one-way pipeline instead of creating a parallel recovery path. The current architecture already has the right trust boundary: `optimize.py` generates snapped exact candidates, while `verify.py` is the only component allowed to label a formula as `recovered`. Compiler output, warm-start embedding, perturbation training, and promoted demos should all feed that same `Expr -> verify_candidate()` contract.

The new compiler should produce ordinary `expression.Expr` trees, not a separate formula type. Its primary job is to turn a constrained SymPy subset into exact EML ASTs with rule traces and honest unsupported reasons. The compiler should fail closed: if a rule is not verified over safe domains, do not emit a partial AST that looks authoritative.

Warm starts should be implemented as an initializer for `SoftEMLTree`, not as a second optimizer. A compiled `Expr` should be embedded by biasing existing slot logits toward the AST structure, then optional perturbation noise should test return-to-solution behavior. This directly follows the paper/NORTH_STAR observation that blind deep recovery degrades quickly while perturbed correct trees are much easier to recover.

Beer-Lambert and Michaelis-Menten should be promoted by adding compiler/warm-start recovery modes to the demo harness while preserving their catalog reference candidates. Normalized Planck should remain a stretch report until compiled/warm-start verification passes under fixed budgets and the report states seed sensitivity honestly.

## Existing Boundaries to Preserve

| Existing Module | Current Responsibility | v1.1 Rule |
|-----------------|------------------------|-----------|
| `expression.py` | Exact `Const`, `Var`, `Eml` ASTs, JSON documents, SymPy/catalog candidates | Compiler output must be an `Expr`; do not introduce a competing AST. |
| `master_tree.py` | Complete soft EML tree, slot catalog, logits, snapping, forced paper identities | Add general AST embedding and optional terminal constants here or adjacent to it. Keep default behavior unchanged. |
| `optimize.py` | Candidate generator with random restarts, annealing, snap manifest | Add optional initialization/perturbation. It still must not return `recovered`. |
| `verify.py` | Verifier-owned recovery status over train, held-out, extrapolation, and mpmath checks | Keep verifier API stable. Compiler and warm-start outputs must pass through it. |
| `datasets.py` | Demo specs, split generation, catalog reference candidates | Add recovery plans/compile metadata without removing catalog candidates. |
| `cli.py` | Demo/report orchestration and paper checks | Add explicit compile/warm-start modes; keep existing `demo` behavior compatible. |
| `cleanup.py` | Targeted SymPy readability and verifier-gated cleanup reports | Reuse after verification; do not use cleanup as compiler proof. |

## Recommended New Components

| Component | New or Modified | Responsibility | Primary Integration Point |
|-----------|-----------------|----------------|---------------------------|
| `compiler.py` | New | Compile a defined SymPy subset into `Expr`; emit rule trace, constants policy, source expression, unsupported reasons | Consumes `SympyCandidate.to_sympy()` or demo source expressions; produces `Expr` |
| `CompilerConfig` / `CompileResult` | New | Carry variables, constant policy, max depth, enabled rules, source metadata, warnings | Used by demos, CLI, tests, and run manifests |
| Rule library | New | Implement verified identities for `exp`, `log`, constants, variables, and arithmetic rules as they become proven | Called only by `compiler.py` |
| AST embedding helper | New or in `master_tree.py` | Bias a `SoftEMLTree` toward a compiled `Expr` using slot paths and logits | Uses `SoftEMLTree.set_slot()` semantics |
| `EmbeddingConfig` / `EmbeddingResult` | New | Record strength, depth, constants, mapped slots, unused branches, failures | Stored in optimizer manifests |
| Warm-start initializer | Modified `optimize.py` | Initialize model from compiled AST, optionally perturb logits, then train normally | Optional parameter to `fit_eml_tree()` or wrapper |
| `PerturbationConfig` | New | Configure logit noise, seed, active/inactive slot perturbation, optional freeze schedule | Stored in run manifest |
| Demo recovery plan | Modified `datasets.py` | Declare which demos have catalog-only, compiled, warm-start, or stretch modes | Used by CLI/report writer |

## Compiler Architecture

### Input and Output

The compiler should accept:

```text
SymPy expression
variables tuple
CompilerConfig(
  constant_policy,
  enabled_rules,
  max_depth,
  fail_on_unsupported=True
)
```

It should return:

```text
CompileResult(
  status="compiled" | "unsupported" | "failed",
  expression: Expr | None,
  source_sympy: str,
  variables: tuple[str, ...],
  rule_trace: list[RuleStep],
  constants: tuple[complex, ...],
  depth: int | None,
  node_count: int | None,
  warnings: list[str],
  metadata: dict
)
```

The emitted `Expr.to_document()` metadata should include `source="compiler"`, the source SymPy string, compiler version, enabled rules, constants policy, and rule trace hash. This keeps compiled ASTs auditable without changing the AST schema.

### Rule Strategy

Implement compiler rules incrementally and prove each one with tests before enabling it by default.

| Rule | Initial Recommendation | Confidence |
|------|------------------------|------------|
| `Symbol("x") -> Var("x")` | Build first | HIGH |
| literal constants -> `Const(value)` | Build with explicit metadata | HIGH for implementation, MEDIUM for paper-purity semantics |
| `exp(a) -> Eml(compile(a), Const(1))` | Build first; paper identity already tested for variables | HIGH |
| `log(a)` | Build using the existing generalized paper identity `Eml(1, Eml(Eml(1, a), 1))` | HIGH on safe positive domains |
| negation/subtraction/addition/multiplication/division | Add through a verified identity library, not ad hoc SymPy string rewrites | MEDIUM |
| unsupported SymPy nodes | Return `unsupported` with reason and path | HIGH |

The important architectural choice is not the exact first batch of arithmetic identities. It is that arithmetic rules live in a tested compiler-rule layer and never bypass verification.

### Constants Policy

Beer-Lambert and Michaelis-Menten currently contain numeric literals (`0.8`, `2.0`, `0.5`). The existing `Const` node can represent arbitrary complex constants, but the AST document currently advertises `constant_basis=["1"]`. v1.1 should make this explicit:

| Policy | Use | Report Wording |
|--------|-----|----------------|
| `basis_only` | Paper-pure checks and identities using only `1` | "exact EML basis expression" |
| `literal_constants` | Demo formulas with fixed known constants from `DemoSpec` | "exact EML AST with literal constants" |

Do not add learned coefficients in this milestone. Literal constants should come from source/demo expressions only, be serialized deterministically, and appear in report metadata. If `literal_constants` is used, the verifier can still validate the formula numerically, but public claims should not imply shortest paper-basis compilation.

## Warm-Start Embedding

### Required Soft Tree Change

`SoftEMLTree` currently has terminal labels:

```text
["const:1", "var:x", "child"]
```

To warm-start compiled Beer-Lambert and Michaelis-Menten, the master tree needs a finite constant catalog:

```python
SoftEMLTree(depth, variables=("x",), constants=(1.0, 0.8, 2.0, 0.5))
```

Default must remain `constants=(1.0,)` so existing tests and the paper parameter-count check continue to pass. `expected_univariate_parameter_count()` should either require the default constant catalog or document that the paper formula applies only when the terminal catalog is `{1, x, child}`.

### Embedding Algorithm

Embed a compiled `Expr` by walking it against the complete tree:

1. Validate `expr.depth() <= model.depth`.
2. Validate all variables exist in `model.variables`.
3. Validate every `Const` value appears in `model.constants`.
4. At each EML node, map side expressions to slot choices:
   - `Const(c)` -> `const:<canonical c>`
   - `Var(name)` -> `var:<name>`
   - `Eml(...)` -> `child`, then recurse into that side child
5. Bias each mapped slot with a configurable strength using current `set_slot()` behavior.
6. Leave unused child branches randomized or low-confidence; they are inactive unless their parent slot later moves to `child`.
7. Return an `EmbeddingResult` with every slot assignment and skipped subtree.

Embedding should not call the verifier. Its proof is mechanical: after embedding with high strength and no perturbation, `model.snap().expression` should evaluate the same as the source `Expr` on safe test points.

### Perturbation

Perturbation should operate on logits after embedding:

```text
reset small random logits
embed compiled AST at strength S
add deterministic logit noise from seed P
optionally lower strength or perturb only active slots
train with normal optimizer
snap
verify
```

`PerturbationConfig` should include:

| Field | Purpose |
|-------|---------|
| `seed` | Deterministic perturbation reproducibility |
| `noise_std` | How far from the compiled solution to start |
| `active_slots_only` | Whether to perturb only mapped slots or all slots |
| `inactive_noise_std` | Separate noise for unused branches |
| `warm_start_strength` | Initial logit separation before noise |
| `freeze_mapped_steps` | Optional early phase where mapped slots are frozen or lightly trained |

For v1.1, prefer no freezing unless a demo needs it. Freezing complicates optimizer state and can hide whether the model actually returns to the solution.

## Optimization Integration

Keep `fit_eml_tree()` backward-compatible. The least disruptive design is:

```python
fit_eml_tree(inputs, target, config, initialization: TreeInitialization | None = None)
```

or a wrapper:

```python
fit_warm_started_eml_tree(inputs, target, config, compiled_expr, embedding_config, perturbation_config)
```

The wrapper is safer for v1.1 because it avoids changing existing call sites and makes warm-start behavior explicit. Internally it can still share the same training loop.

The manifest should add optional keys:

```text
initialization_kind: "random" | "compiled_warm_start"
compiler: CompileResult metadata
embedding: EmbeddingResult metadata
perturbation: PerturbationConfig
initial_snap_loss
initial_verifier_status_if_run
post_training_snap_loss
```

`FitResult.status` should remain a candidate-generator status such as `snapped_candidate`, `failed`, or `warm_started_candidate`. Do not add `recovered` to optimizer statuses.

## Demo Integration

### Dataset Model

Keep `DemoSpec.candidate` as the reference candidate used for target generation and catalog verification. Add a separate recovery plan:

```text
DemoRecoveryPlan(
  mode="catalog" | "compiled" | "warm_start" | "stretch",
  source_expression,
  compiler_config,
  depth,
  constants,
  training_config,
  perturbation_config,
  expected_claim
)
```

This preserves the current catalog showcase behavior while making promotion explicit.

### Report Flow

For promoted demos, the CLI report should contain separate sections:

```text
reference_verification        # existing catalog or exact EML candidate
compiled_eml_ast              # compiler output, if requested
compiled_verification         # verifier result for compiled Expr
warm_start_training_manifest  # optimizer result from perturbation training
warm_start_verification       # verifier result for snapped trained Expr
claim_status                  # derived from verifier result and mode
```

This avoids a common ambiguity: a demo can have a verified catalog formula, a verified compiled formula, and a failed perturbed training run. Only the warm-start verifier result should promote the demo to trained EML recovery.

### CLI Modes

Keep existing `demo NAME` behavior compatible. Add explicit options instead of overloading `--train-eml`:

| Mode | Suggested CLI | Meaning |
|------|---------------|---------|
| Catalog report | `demo NAME` | Current behavior |
| Compile only | `demo NAME --compile-eml` | Compile source expression and verify compiled AST |
| Warm start | `demo NAME --warm-start-eml` | Compile, embed, perturb/train, snap, verify |
| Blind baseline | existing `--train-eml` | Current random-init training attempt |

`--train-eml` should remain a blind baseline. That distinction matters because warm-start success is a different claim than blind recovery.

### Promotion Targets

| Demo | v1 Status | v1.1 Target | Notes |
|------|-----------|-------------|-------|
| `exp` | exact EML recovered | Keep as paper smoke test | Also use as embedding/perturbation fixture |
| `log` | exact EML recovered | Keep as compiler/log fixture | Depth >= 3 remains required |
| `beer_lambert` | catalog showcase | Promote to compiled + warm-start recovery if literal constants are enabled | Good first promoted demo |
| `michaelis_menten` | catalog showcase | Promote after Beer-Lambert | Exercises rational structure and division rules |
| `logistic` / `shockley` | catalog showcase | Defer or use as stretch after arithmetic compiler proves stable | More moving parts |
| `damped_oscillator` | catalog showcase | Defer | Trig/phase compiler support is not in v1.1 target subset |
| `planck` | catalog showcase | Stretch only with honest failure/success report | High depth and denominator structure make it a roadmap flag |

## End-to-End Data Flow

```text
DemoSpec
  -> make_splits()
  -> reference candidate verification
  -> source SymPy expression
  -> compiler.py
  -> CompileResult.expression: Expr
  -> verify_candidate(compiled Expr)
  -> SoftEMLTree(depth, variables, constants)
  -> embed Expr into logits
  -> perturb logits
  -> train with optimize.py loop
  -> snap to Expr
  -> cleanup_candidate()
  -> verify_candidate(snapped Expr)
  -> CLI JSON report
```

Allowed feedback loops:

```text
unsupported compiler rule -> mark demo unsupported or reduce target subset
embedding depth failure -> increase configured depth or simplify compiled AST
warm-start verification failure -> rerun with stronger embedding / lower perturbation / more steps
verified but bloated AST -> cleanup -> verifier
```

Do not add a feedback loop where verifier silently changes the formula or where cleanup rewrites are accepted without re-verification.

## Build Order

1. **Compiler result scaffolding and direct rules**
   - Add `compiler.py`, `CompilerConfig`, `CompileResult`, rule traces, unsupported reasons.
   - Implement variables, literal constants, `exp`, and generalized `log`.
   - Tests: compile/evaluate against SymPy for `x`, `1`, `exp(x)`, `log(x)`, nested expressions on safe positive domains.

2. **Constant catalogs and AST embedding**
   - Modify `SoftEMLTree` terminal labels to support `constants=(...)` with default `(1.0,)`.
   - Add general `embed_expr_into_tree()` using `set_slot()` semantics.
   - Tests: existing parameter-count tests still pass; embedding `exp_expr` and `log_expr` snaps back to equivalent ASTs; missing constants/depth fail clearly.

3. **Warm-start perturbation training**
   - Add wrapper or optional initializer around `fit_eml_tree()`.
   - Add perturbation metadata and initial/post-training snap loss to manifests.
   - Tests: warm-start `exp` or compiled Beer-Lambert with small perturbation returns a verified snapped candidate under deterministic settings.

4. **Arithmetic compiler subset**
   - Add verified rules for negation/subtraction/addition/multiplication/division only as tests prove identities.
   - Tests: each rule has NumPy/mpmath equivalence checks and fail-closed unsupported behavior.
   - Michaelis-Menten depends on division and addition; do not promote it before this phase passes.

5. **Demo promotion and CLI reports**
   - Add `DemoRecoveryPlan` metadata to `beer_lambert` and `michaelis_menten`.
   - Add `--compile-eml` and `--warm-start-eml`.
   - Reports must distinguish catalog, compiled, warm-start, blind, and stretch statuses.

6. **Planck stretch reporting**
   - Add a report mode that runs compiler/warm-start if supported but labels failures honestly.
   - Do not block v1.1 on Planck recovery.

## Testing Strategy

| Test Layer | What It Proves | Required Examples |
|------------|----------------|-------------------|
| Compiler unit tests | SymPy subset lowers to `Expr` or fails closed | constants, variables, `exp`, `log`, unsupported functions |
| Compiler rule equivalence | Each enabled identity is numerically valid on safe domains | arithmetic rules before enabling Beer-Lambert/Michaelis-Menten promotion |
| AST document tests | Compiler metadata survives JSON output | source expression, constant policy, rule trace, depth, node count |
| Constant catalog tests | Existing paper tree behavior is unchanged by added constants | default parameter count; labels for `const:1`; explicit labels for `0.8`, `0.5`, `2.0` |
| Embedding tests | Compiled AST maps to legal soft-tree slots | exact snap after high-strength embedding; clear failure for missing depth/constants |
| Perturbation tests | Warm-start recovery is deterministic and not confused with blind recovery | initial snap, perturbed logits, final snap, manifest metadata |
| Verifier integration tests | Compiler/warm-start candidates still use the existing recovery contract | `verify_candidate(compiled_expr)` and `verify_candidate(snapped_expr)` |
| CLI report tests | Public claims are separated correctly | catalog report, compile-only report, warm-start report, failed stretch report |
| Demo promotion tests | Beer-Lambert and Michaelis-Menten are only promoted when verifier passes | report `claim_status` derived from trained EML verification |

Avoid CI tests that require lucky random blind recovery. Warm-start tests should use fixed seeds, small perturbations, and paper/simple demo targets.

## Anti-Patterns to Avoid

### Parallel Candidate Types

Do not introduce a `CompiledExpr` that bypasses `expression.Expr`. It will split evaluator, cleanup, and verifier behavior.

### Optimizer-Owned Recovery

Warm-start training can report `snapped_candidate` or `warm_started_candidate`, but never `recovered`. Only `verify.py` owns recovery.

### Hidden Literal Constants

If the compiler uses `Const(0.8)` or `Const(2.0)`, the report must say so. Do not present literal-constant recovery as pure `{1, eml}` basis recovery.

### CLI Flag Ambiguity

Blind training and warm-start training should not share the same public claim. Keep `--train-eml` as random-init/blind and add a separate warm-start mode.

### Compiler Overreach

Unsupported arithmetic or functions should be reported as unsupported. A failed compile is better than a silently wrong AST that later appears in a demo report.

## Roadmap Implications

The phase plan should follow dependencies:

1. **Compiler Core** before demos because promoted demos need auditable compiled ASTs.
2. **Constant Catalog + Embedding** before perturbation because warm starts cannot represent demo constants otherwise.
3. **Perturbation Training** before demo promotion because the milestone is about return-to-solution behavior, not just compiling references.
4. **Arithmetic Rule Expansion** before Michaelis-Menten because rational structure depends on addition/division.
5. **Demo Reporting** after the engine path is stable because claims must distinguish catalog, compiled, warm-start, and stretch outcomes.

Likely deeper research flags:

- Arithmetic EML identities for `+`, `-`, `*`, `/` under literal-constant and basis-only policies.
- Minimum tree depths for Beer-Lambert and Michaelis-Menten compiled forms.
- Perturbation budgets that are strong enough to demonstrate recovery but not so strong that CI becomes flaky.
- Whether Planck can compile within practical depth after denominator and power rules are implemented.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Existing boundary preservation | HIGH | Directly grounded in current `expression.py`, `master_tree.py`, `optimize.py`, `verify.py`, `datasets.py`, and `cli.py`. |
| Compiler-as-`Expr` design | HIGH | Reuses exact AST, serializers, cleanup, and verifier without new candidate plumbing. |
| Warm-start embedding design | HIGH | Current slot paths and `set_slot()` already support the needed traversal pattern for `{1, variables, child}` trees. |
| Constant catalog requirement | HIGH | Existing `SoftEMLTree` cannot choose `Const(0.8)` or `Const(2.0)` without extending terminal labels. |
| Arithmetic compiler feasibility | MEDIUM | Required by the milestone, but exact identities and depth blow-up need rule-by-rule validation. |
| Demo promotion path | HIGH for Beer-Lambert, MEDIUM for Michaelis-Menten | Beer-Lambert is structurally simpler; Michaelis-Menten depends on reliable division/addition compilation. |
| Planck stretch | LOW to MEDIUM | Source guidance and v1 research both flag Planck as high-value but likely depth-sensitive. |

## Sources

- `.planning/PROJECT.md` - v1.1 milestone goal, active requirements, constraints, and out-of-scope boundaries.
- `.planning/STATE.md` - current completed v1 phases and existing artifact status.
- `.planning/research/SUMMARY.md` - v1 architecture and pitfall synthesis.
- `src/eml_symbolic_regression/expression.py` - exact ASTs, candidate protocol, SymPy catalog candidates, JSON schema, paper identities.
- `src/eml_symbolic_regression/master_tree.py` - soft tree slot structure, logits, `set_slot()`, snapping, paper identity forcing.
- `src/eml_symbolic_regression/optimize.py` - training config, random restarts, annealing, snap manifest, candidate-generator boundary.
- `src/eml_symbolic_regression/verify.py` - verifier-owned `recovered` status and split/high-precision checks.
- `src/eml_symbolic_regression/datasets.py` - existing demo specs, catalog candidates, split generation.
- `src/eml_symbolic_regression/cli.py` - current demo, blind training, and report flow.
- `src/eml_symbolic_regression/semantics.py` - canonical/training EML semantics and anomaly stats.
- `src/eml_symbolic_regression/cleanup.py` - targeted cleanup and verifier-gated reports.
- `tests/test_master_tree.py`, `tests/test_optimizer_cleanup.py`, `tests/test_semantics_expression.py`, `tests/test_verifier_demos_cli.py` - existing regression expectations.
- `docs/IMPLEMENTATION.md` and `README.md` - public recovery contract and demo status wording.
- `sources/NORTH_STAR.md` - hybrid pipeline, warm-start rationale, numerical risks, and verification boundaries.
- `sources/FOR_DEMO.md` - demo promotion sequence, high-probability demos, and Planck caution.
