# Technology Stack: v1.1 Compiler-Driven Warm Starts

**Project:** EML Symbolic Regression
**Research dimension:** Stack additions for v1.1 EML Compiler and Warm Starts
**Researched:** 2026-04-15
**Overall confidence:** HIGH for dependency recommendation; MEDIUM for pure-`1` constant compilation depth feasibility

## Recommendation

No new third-party runtime dependencies are needed for v1.1. The existing Python/PyTorch/SymPy/NumPy/mpmath/pytest stack is sufficient for compiler-driven warm starts.

The work should add project-owned modules and integration points, not a new CAS, parser generator, symbolic-regression engine, GPU layer, Rust backend, or theorem prover. SymPy already provides the ordinary expression tree, PyTorch already owns trainable logits and perturbations, and the existing exact AST / verifier stack already defines what counts as recovered.

Recommended v1.1 stack shape:

```text
SymPy ordinary expression
  -> local compiler subset / rule registry
  -> exact EML Expr AST with compiler metadata
  -> warm-start embedding into SoftEMLTree logits
  -> optional deterministic logit perturbation
  -> existing PyTorch optimizer / snap
  -> existing verifier and cleanup reports
```

The main implementation choice is to keep the compiler deterministic, explicit, and verifier-gated. It should compile only the supported subset and return structured unsupported-rule errors for everything else.

## Local Baseline

Observed locally on 2026-04-15:

| Tool | Local / Project Version | Keep for v1.1? | Why |
|------|-------------------------|----------------|-----|
| Python | 3.11.5, `>=3.11,<3.13` in `pyproject.toml` | Yes | Existing package, dataclasses, argparse, JSON artifacts, deterministic compiler metadata. |
| PyTorch | 2.10.0 local, `torch>=2.10` | Yes | Existing `SoftEMLTree`, logits, Adam loop, `complex128` evaluation, perturbation via seeded tensors. |
| SymPy | 1.14.0 local, `sympy>=1.14` | Yes | Existing catalog candidates and cleanup already use SymPy; compiler should walk SymPy `Expr.func` / `Expr.args`. |
| NumPy | 1.26.4 local, `numpy>=1.26` | Yes | Existing deterministic datasets and post-snap numeric checks. |
| mpmath | 1.3.0 local, `mpmath>=1.3` | Yes | Existing high-precision verifier; compiler output must pass this before being called recovered. |
| pytest | 7.4.0 local, dev extra | Yes | Add compiler, embedding, perturbation, and demo regression tests. |

## Stack Additions

These are code-level additions inside the current stack, not package dependencies.

| Addition | Likely Module | Primary Stack | Purpose |
|----------|---------------|---------------|---------|
| SymPy subset compiler | `src/eml_symbolic_regression/compiler.py` | SymPy, existing `expression.py` AST | Compile a defined ordinary-expression subset into exact `Expr` trees. |
| Compiler report schema | `compiler.py` / CLI report payloads | dataclasses, JSON | Record source expression, normalized SymPy form, rules used, unsupported nodes, output depth/node count. |
| Warm-start embedding | `src/eml_symbolic_regression/warm_start.py` or `master_tree.py` helper | PyTorch, existing `SoftEMLTree.set_slot` | Map exact EML AST paths onto compatible soft-tree slot logits. |
| Logit perturbation | `warm_start.py` / `optimize.py` | PyTorch `Generator`, `torch.no_grad` | Test return-to-solution behavior from near-correct trees. |
| Warm-start training config | `optimize.py` | dataclasses | Add optional initialization source, strength, noise, and seed fields without changing the optimizer dependency. |
| Demo promotion metadata | `datasets.py`, `cli.py` | existing DemoSpec, JSON reports | Distinguish `catalog`, `compiled_exact`, `warm_start_recovered`, `warm_start_failed`, and `stretch` claims. |

## Compiler Implementation Choices

### Use SymPy Exprs as the Front End

Use SymPy expressions as the compiler input. The current demo catalog already stores Beer-Lambert, Michaelis-Menten, logistic, Shockley, damped oscillator, and Planck as `SympyCandidate`, so v1.1 can compile those in-process without adding a string parser.

If a CLI string input is added, keep it secondary and trusted. SymPy official docs warn that `parse_expr` uses `eval` and should not be used on unsanitized input. For v1.1, prefer named built-in demo specs or a whitelisted parser wrapper with restricted `local_dict`, restricted `global_dict`, and supported function names only.

Implementation rule:

```text
Public compiler API accepts sp.Expr first.
CLI string parsing, if present, is a thin trusted convenience layer.
```

### Walk SymPy Trees Directly

Use `expr.func` and `expr.args` rather than parsing printed strings. SymPy documents these as the core way to recurse through expression trees, while also warning that printed form and internal representation may differ.

Practical implications:

- Match `sp.Symbol`, `sp.Integer`, `sp.Rational`, `sp.Float`, `sp.Add`, `sp.Mul`, `sp.Pow`, `sp.exp`, and `sp.log` explicitly.
- Normalize supported syntactic sugar into the subset before compilation: subtraction as `Add`, division as `Mul(..., Pow(denominator, -1))`, unary negation as multiplication by `-1`.
- Treat unsupported functions (`sin`, `cos`, arbitrary `Pow`, special functions, piecewise) as structured compiler failures, not best-effort guesses.
- Keep rule ordering deterministic and record every rule in compiler metadata.

### Constant Handling Is the Key Design Choice

Existing `expression.Const` can serialize and evaluate arbitrary complex constants, but existing `SoftEMLTree` only offers `const:1` as a terminal choice. Beer-Lambert (`exp(-0.8*x)`) and Michaelis-Menten (`2*x/(0.5+x)`) need numeric constants.

Recommended v1.1 choice:

1. Add a constant catalog to `SoftEMLTree`, defaulting to `(1.0,)` to preserve v1 behavior.
2. Let compiler-driven demos pass the exact constants discovered in the source SymPy expression, for example `(1.0, -1.0, 0.5, 0.8, 2.0)`.
3. Encode catalog entries as deterministic labels such as `const:1`, `const:-1`, `const:0.5`.
4. Record `constant_basis` in artifacts as `["1", "literal_catalog"]` when non-`1` constants are used.

This is the practical path for v1.1 demos. It should be reported honestly as constant-catalog warm-start recovery, not blind pure-paper-basis recovery. A pure `1`-only compiler for numeric constants can be researched later, but making every rational/scaled coefficient out of `1` through EML identities is likely to produce deeper, brittle trees and would distract from validating compiler warm starts.

Confidence: HIGH that a literal constant catalog integrates cleanly with current code; MEDIUM that pure-`1` constant compilation is feasible at useful depths for v1.1 demos.

### Compiler Rule Scope

Recommended initial subset:

| Ordinary Form | Compile Policy | Notes |
|---------------|----------------|-------|
| `1`, allowed numeric constants | Direct `Const(value)` | Requires matching master-tree constant catalog for warm start. |
| variables | Direct `Var(name)` | Existing AST already supports named variables. |
| `exp(x)` | Use existing paper identity `Eml(x, Const(1))` | Already present as `exp_expr`. |
| `log(x)` | Use existing paper identity from `log_expr`, generalized to subexpressions | Verify branch behavior on positive/safe domains. |
| `a - b`, `-a` | Compile only through explicit rule templates | Avoid algebraic guessing; record rule names. |
| `a + b` | Compile through explicit EML arithmetic template where implemented | Keep unsupported if the template would exceed depth budget. |
| `a * b` | Compile through explicit EML arithmetic template where implemented | Needed for Beer-Lambert and Michaelis-Menten. |
| `a / b` | Compile as multiplication by reciprocal only if reciprocal template is implemented | Needed for Michaelis-Menten and Planck. |
| `x**n` | Support small nonnegative integer powers by repeated multiplication | Planck needs `x**3`; keep this behind a max-power/depth guard. |

The compiler should expose estimated output depth before training. If the compiled AST exceeds the requested master-tree depth, fail early with `requires_depth=N` rather than producing an unembeddable warm start.

## Warm-Start Integration

### Embedding Into `SoftEMLTree`

Current `SoftEMLTree` already has the important primitive: `set_slot(node_path, side, choice, strength)`. v1.1 should generalize the existing `force_exp` and `force_log` style into a recursive embedder:

```text
embed_expr(model, expr, path="root", strength=30.0)
```

Embedding rules:

- If a slot expression is `Const(value)`, set that slot to the matching constant-catalog label.
- If a slot expression is `Var(name)`, set that slot to `var:name`.
- If a slot expression is `Eml(left, right)`, set that slot to `child` and recurse into `path.L` or `path.R`.
- If the expression depth exceeds the remaining master depth, return a structured error.
- If the compiler emits a leaf as the whole formula, require a wrapper identity or reject it because the current master root is an EML node.

The embedder should verify round-trip compatibility immediately:

```text
compiled Expr -> embed logits -> snap -> exact Expr
```

The snapped AST should match the compiled AST structurally before any perturbation or training is attempted.

### Strength and Probability

Keep logit initialization project-owned. Do not add a categorical-relaxation package.

Use either:

- existing `strength` convention: active choice `+strength`, inactive choices `-strength`; or
- probability-derived gap: `gap = log(p * (k - 1) / (1 - p))` for a target active probability `p`.

The existing `strength=30.0` is effectively one-hot. For perturbation experiments, use a smaller default such as `strength=8.0` to allow gradients to move while still starting near the compiled tree.

### Perturbation

Use PyTorch only:

```text
with torch.no_grad():
    logits.add_(noise_std * torch.randn_like(logits, generator=generator))
```

Record:

- warm-start source hash / expression string,
- logit strength,
- perturbation distribution and seed,
- initial snap before perturbation,
- snap after perturbation,
- final snap after training,
- distance from compiled path as number of changed slot choices.

This directly supports the v1.1 goal of demonstrating recovery from near-correct EML trees.

## Optimizer Choices

Keep the existing Adam loop. Add initialization hooks, not a new optimizer.

Recommended `TrainingConfig` additions:

| Field | Purpose |
|-------|---------|
| `initial_expr: Expr | None` | Optional exact AST to embed before training. |
| `warm_start_strength: float` | Logit preference for compiled choices. |
| `perturbation_std: float` | Gaussian logit noise after embedding. |
| `warm_start_seed: int | None` | Deterministic perturbation independent of restart seed. |
| `verify_initial_snap: bool` | Fail fast if embed/snap does not round-trip. |

Restarts should support mixed initialization:

- one unperturbed compiled initialization,
- several perturbed compiled initializations,
- optional random restarts as a baseline.

Do not use `torch.nn.functional.gumbel_softmax` as a core dependency. Current PyTorch docs keep it available but say it is present for legacy reasons and may be removed from `nn.functional`; the existing softmax-plus-snap design is enough.

## Demo Integration

### Beer-Lambert

Use as the first v1.1 trained warm-start demo.

Recommended path:

1. Compile `exp(-0.8*x)` from the existing SymPy catalog candidate.
2. Include constants required by the expression in the master-tree constant catalog.
3. Embed the compiled AST into a compatible depth.
4. Perturb logits and train.
5. Snap and verify with existing train/held-out/extrapolation/mpmath checks.

Expected confidence: HIGH for constant-catalog warm-start recovery; lower for pure `1`-basis recovery.

### Michaelis-Menten

Use as the second trained warm-start demo if arithmetic templates and depth budget are acceptable.

Recommended path:

1. Compile `2*x/(0.5+x)` from the existing SymPy catalog candidate.
2. Require compiler support for addition, multiplication, reciprocal/division, and numeric constants.
3. Report compiler output depth and node count before training.
4. Treat failure to fit within a practical depth as an honest v1.1 limitation, not a reason to add PySR or another search engine.

Expected confidence: MEDIUM because rational templates can grow quickly and may require careful depth limits.

### Normalized Planck

Keep as stretch reporting.

Planck requires `x**3`, `exp(x) - 1`, and division. It is an excellent compiler stress test and reporting target, but it should not gate v1.1 success. Use compiler output depth/node count and warm-start recovery status to report exactly where it succeeds or fails.

Expected confidence: LOW to MEDIUM for practical warm-start recovery in v1.1, depending on compiled depth and optimization stability.

## What Not To Add

| Candidate Addition | Recommendation | Why |
|-------------------|----------------|-----|
| Lark / ANTLR parser | Do not add | SymPy expressions are already available; string parsing is not the hard part. |
| Pydantic | Do not add | Existing dataclasses + deterministic JSON are enough for compiler and warm-start reports. |
| PySR / SymbolicRegression.jl | Do not add | Would change the project from EML-tree recovery to heterogeneous symbolic regression. |
| JAX | Do not add | Existing implementation and paper blueprint are PyTorch-centered. |
| Rust / PyO3 | Defer | Useful later for exhaustive local search, but v1.1 needs compiler semantics and logit embedding first. |
| Custom CUDA kernels | Defer | Local CUDA is unavailable and v1.1 does not need kernel work. |
| Mathematica | Optional oracle only | Do not make v1.1 depend on proprietary tooling. |
| Lean / theorem prover | Do not add | Current recovery contract is numeric/high-precision/verifier-gated. |
| Units libraries such as Pint | Do not add | Demo guidance favors normalized dimensionless laws; units would distract from compiler warm starts. |
| `torch.nn.functional.gumbel_softmax` as public API | Do not add | Current PyTorch docs flag it as legacy; local softmax/snap is enough. |

## Installation

No installation changes are required for v1.1.

Current `pyproject.toml` already declares the needed runtime stack:

```toml
dependencies = [
  "torch>=2.10",
  "numpy>=1.26",
  "sympy>=1.14",
  "mpmath>=1.3",
]

[project.optional-dependencies]
dev = [
  "pytest>=7.4",
]
```

Do not expand runtime dependencies unless implementation uncovers a concrete blocker.

## Integration Checklist for Roadmap

Recommended phase ordering for v1.1:

1. **Compiler AST subset and reports** - Add deterministic SymPy-to-EML compilation with unsupported-node errors and metadata.
2. **Constant catalog and embedding** - Extend `SoftEMLTree` labels to include compiler constants; implement embed/snap round-trip tests.
3. **Perturbed warm-start training** - Add `TrainingConfig` initialization hooks and logit perturbation reports.
4. **Demo promotion** - Promote Beer-Lambert first, then Michaelis-Menten if compiled depth and verification pass.
5. **Stretch reporting** - Add Planck compiler/warm-start report without requiring recovery.

Phase dependencies:

```text
compiler subset -> constant catalog -> embedding -> perturbation training -> trained demos
```

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| No new dependencies | HIGH | Existing `pyproject.toml`, source modules, and official docs cover the needed compiler/warm-start functions. |
| SymPy as compiler front end | HIGH | SymPy `Expr.func` / `Expr.args` are designed for expression-tree traversal; existing demos already use SymPy candidates. |
| PyTorch for warm-start logits | HIGH | Current `SoftEMLTree` already exposes slot logits and `set_slot`; perturbation is simple tensor initialization. |
| Literal constant catalog | HIGH | Existing `Const(value)` supports arbitrary constants; master-tree labels need a small extension. |
| Pure `1`-basis constant compilation for demos | MEDIUM/LOW | Paper-fidelitous but likely deep and brittle for `0.8`, `0.5`, and `2.0`; defer unless v1.1 explicitly wants that research. |
| Beer-Lambert warm-start recovery | HIGH | Formula is structurally simple once constants are available. |
| Michaelis-Menten warm-start recovery | MEDIUM | Rational arithmetic can inflate EML depth; needs depth/node-count guardrails. |
| Planck warm-start recovery | LOW/MEDIUM | Best treated as stretch due to power + exponential + subtraction + division depth. |

## Sources

Local project sources:

- `.planning/PROJECT.md` - v1.1 goal: ordinary-expression compiler subset, warm-start embedding, perturbation recovery, Beer-Lambert/Michaelis-Menten trained demos, Planck stretch reporting.
- `.planning/STATE.md` - confirms v1 is complete and v1.1 is defining requirements.
- `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` - v1 validated capabilities and verifier-owned recovery contract.
- `src/eml_symbolic_regression/expression.py` - exact `Const`, `Var`, `Eml`, JSON artifacts, SymPy candidate support, paper identities.
- `src/eml_symbolic_regression/master_tree.py` - current soft tree labels, logits, `set_slot`, snap, `force_exp`, `force_log`.
- `src/eml_symbolic_regression/optimize.py` - current Adam training config and manifest shape.
- `src/eml_symbolic_regression/datasets.py` - current demo catalog expressions for Beer-Lambert, Michaelis-Menten, and Planck.
- `src/eml_symbolic_regression/verify.py`, `cleanup.py`, `cli.py` - existing verifier, cleanup, and demo report integration points.
- `sources/NORTH_STAR.md` - warm-start/recovery rationale, hybrid pipeline, complex128 training, hardening/snap, verification.
- `sources/FOR_DEMO.md` - demo ordering and cautions about depth, units, and Planck as a hard showcase.

Official/current external sources checked:

- SymPy parsing docs: https://docs.sympy.org/latest/modules/parsing.html
- SymPy expression manipulation docs: https://docs.sympy.org/latest/tutorials/intro-tutorial/manipulation.html
- PyTorch complex numbers docs: https://docs.pytorch.org/docs/stable/complex_numbers.html
- PyTorch `gumbel_softmax` docs: https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.gumbel_softmax.html
- Python dataclasses docs: https://docs.python.org/3/library/dataclasses.html

