# Phase 30: Bounded Shallow Blind Training Recovery - Research

**Researched:** 2026-04-15
**Domain:** EML blind-training proof suites, scaffold initializers, exact exponential-family recovery
**Confidence:** MEDIUM

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

Source: `.planning/phases/30-bounded-shallow-blind-training-recovery/30-CONTEXT.md` [VERIFIED: 30-CONTEXT.md]

### Proof Suite Scope
- **D-01:** Count only proof-aware blind runs whose derived `evidence_class` is `blind_training_recovered` toward the bounded 100% target.
- **D-02:** Extend the declared shallow proof inventory beyond `exp`, `log`, `radioactive_decay`, and Beer-Lambert to include signed/scaled exponential variants that are shallow enough for this milestone's bounded claim.
- **D-03:** Keep suite seeds, budgets, tolerances, claim IDs, and threshold policies in the suite/case contract; CLI filters are allowed for debugging but cannot redefine the proof target.
- **D-04:** If any proposed signed/scaled variant cannot be supported without exceeding the paper-realistic shallow bound, narrow the supported variant set only with committed evidence and an explicit contract update.

### Recovery Strategy
- **D-05:** Prefer paper-grounded scaffold initializers and shallow EML identities for exponential, logarithmic, scaled exponential, signed exponential, and exponential decay families before increasing generic random-search budgets.
- **D-06:** Preserve blind-training semantics: an initializer may bias the soft master tree from formula-family priors, but it must still train, snap, and pass the verifier; do not route through compiler warm starts or catalog candidates.
- **D-07:** Treat `radioactive_decay` and Beer-Lambert failures as first-class proof targets rather than diagnostics to hide or defer.
- **D-08:** Keep runtime practical for regression tests. Use the smallest deterministic depths, steps, restarts, constants, and seeds that meet the declared proof suite.

### Diagnostics and Regression Gates
- **D-09:** Every proof run artifact must explain scaffold source, best soft loss, post-snap loss, snap margin, active node count, status, and verifier/evidence class.
- **D-10:** Add regression tests that fail if the declared shallow proof suite drops below 100% bounded threshold status.
- **D-11:** Preserve failure diagnostics for any non-proof exploratory variants so future phases can inspect scaffold choice, loss behavior, and snap decisions.
- **D-12:** Keep the existing Phase 29 claim/threshold/evidence taxonomy intact; Phase 30 should improve training behavior, not loosen the definition of recovery.

### Claude's Discretion
- Choose exact scaffold names, helper functions, and tests consistent with the current `optimize.py`, `master_tree.py`, and `benchmark.py` patterns.
- Choose whether signed/scaled exponential variants live in `datasets.py` as new `DemoSpec` entries or in a proof-suite-only target helper, provided artifacts retain formula provenance.
- Choose the least invasive optimizer extension that reaches the bounded proof target with deterministic tests.

### Deferred Ideas (OUT OF SCOPE)
- Perturbed true-tree basin recovery and local snap/discrete repair belong to Phase 31.
- Depth 2 through 6 recovery curves belong to Phase 32.
- Final proof campaign report and committed raw evidence lockdown belong to Phase 33.
- External noisy datasets and non-shallow arbitrary elementary formulas remain out of scope for v1.5.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| SHAL-01 | Declared shallow blind-training proof suite covers `exp`, `log`, `radioactive_decay`, Beer-Lambert-style scaled exponentials, and signed/scaled exponential variants with fixed seeds and budgets. [VERIFIED: .planning/REQUIREMENTS.md:20] | Extend `datasets.py`, `proof.py` claim case IDs, and `benchmark.py` built-in suite together; current suite has only four cases and 12 runs. [VERIFIED: benchmark.py:716-737] [VERIFIED: proof.py:232-248] |
| SHAL-02 | 100% verifier-owned recovery, excluding catalog, compile-only, and same-AST warm-start evidence. [VERIFIED: .planning/REQUIREMENTS.md:21] | Keep `start_mode="blind"`, `training_mode="blind_training"`, and require derived `evidence_class == "blind_training_recovered"` for every eligible proof run. [VERIFIED: benchmark.py:847-867] [VERIFIED: benchmark.py:1205-1225] |
| SHAL-03 | Optimizer and snap diagnostics expose scaffold source, best loss, post-snap loss, snap margin, active node count, and verifier status. [VERIFIED: .planning/REQUIREMENTS.md:22] | Existing manifests already record restart initialization, `best_loss`, `post_snap_loss`, `snap.min_margin`, and `snap.active_node_count`; benchmark metrics already extract verifier status. [VERIFIED: optimize.py:100-130] [VERIFIED: benchmark.py:986-1023] |
| SHAL-04 | Regression tests fail if `radioactive_decay` or declared signed/scaled exponential suite drops below 100%. [VERIFIED: .planning/REQUIREMENTS.md:23] | Add a proof-suite aggregate test that asserts the bounded threshold row is `passed` and that failing classes are absent for `radioactive_decay`, Beer-Lambert, and new variants. [VERIFIED: benchmark.py:1036-1057] [VERIFIED: tests/test_benchmark_reports.py:132-146] |
</phase_requirements>

## Summary

Phase 30 should not start by raising random restart budgets. The local baseline recovered 6/12 proof runs; all failures are `radioactive_decay` or Beer-Lambert, and every failing artifact confidently snapped to the `log(variable)` scaffold with margin `1.0` and active node count `7`. [VERIFIED: /tmp/eml-phase30-baseline/v1.5-shallow-proof/aggregate.md] [VERIFIED: /tmp/eml-phase30-baseline/v1.5-shallow-proof/*.json]

The core planning issue is representability. The existing compiler verifies `exp(-0.8*x)` and `exp(-0.4*t)` through `exp_of(multiply_expr(Const(k), Var(v)))`, which produces depth `9`, node count `19`, and literal constants `{k, 1}`. [VERIFIED: compiler.py:149-163] [VERIFIED: compiler.py:200-226] [VERIFIED: manual PYTHONPATH=src compiler probe] The current proof suite budgets Beer-Lambert and `radioactive_decay` at depth `4`, so a planner must either prove and implement a shorter exact EML scaffold or explicitly update the proof contract to the smallest verified bounded depth. [VERIFIED: benchmark.py:731-735] [ASSUMED]

**Primary recommendation:** implement a suite-owned exponential-family scaffold contract around exact `exp(k*x)` shapes, literal constant provenance, and verifier-owned blind artifacts; add an evidence task before widening the suite that proves each signed/scaled variant fits the declared depth and does not rely on compiler or catalog evidence. [VERIFIED: 30-CONTEXT.md:16-32] [ASSUMED]

## Project Constraints (from AGENTS.md)

- The implementation must stay faithful to `sources/paper.pdf` and `sources/NORTH_STAR.md` for EML semantics, complete-tree construction, snapping, and complex arithmetic. [VERIFIED: AGENTS.md]
- Training defaults to PyTorch `complex128`; clamps are training-only, and verification mode must remain faithful. [VERIFIED: AGENTS.md] [CITED: sources/NORTH_STAR.md:430-490]
- A candidate is recovered only after held-out, extrapolation, and high-precision verifier checks pass. [VERIFIED: AGENTS.md] [VERIFIED: verify.py:70-125]
- v1.5 must not oversell universal blind deep recovery because the paper reports blind recovery degrading quickly with depth. [VERIFIED: AGENTS.md] [CITED: sources/paper.pdf via pdftotext lines 723-738]
- Demo/proof formulas should remain normalized and dimensionless where possible. [VERIFIED: AGENTS.md] [CITED: sources/FOR_DEMO.md:270-310]
- GSD docs should be committed because `.planning/config.json` has `"commit_docs": true`. [VERIFIED: .planning/config.json:1-4]
- `CLAUDE.md`, `.claude/skills/`, and `.agents/skills/` do not exist in this repository, so no additional project-local skill rules apply. [VERIFIED: `test -f CLAUDE.md`; `test -d .claude/skills`; `test -d .agents/skills`]

## Standard Stack

### Core

| Library / Module | Version / Contract | Purpose | Why Standard |
|------------------|--------------------|---------|--------------|
| Python package runtime | Python `>=3.11,<3.13`; local Python imports succeed under Python 3.11. [VERIFIED: pyproject.toml:10] [VERIFIED: local version probe] | Run optimizer, benchmark, and tests. | Existing project runtime; no new language/runtime is needed. [VERIFIED: pyproject.toml:1-30] |
| PyTorch | Local `2.10.0`; project dependency `torch>=2.10`. [VERIFIED: pyproject.toml:12] [VERIFIED: local version probe] | Soft EML tree logits, Adam loop, complex128 tensor evaluation. | Existing optimizer and paper-aligned training stack. [VERIFIED: optimize.py:79-95] [CITED: sources/paper.pdf via pdftotext lines 723-730] |
| NumPy | Local `1.26.4`; project dependency `numpy>=1.26`. [VERIFIED: pyproject.toml:13] [VERIFIED: local version probe] | Deterministic dataset splits and NumPy verification. | `DemoSpec.make_splits()` and `verify_candidate()` are NumPy-based. [VERIFIED: datasets.py:33-50] [VERIFIED: verify.py:84-93] |
| SymPy | Local `1.14.0`; project dependency `sympy>=1.14`. [VERIFIED: pyproject.toml:14] [VERIFIED: local version probe] | Formula provenance and optional exact-shape oracle. | Existing `DemoSpec` catalog formulas use SymPy expressions. [VERIFIED: datasets.py:66-118] |
| mpmath | Local `1.3.0`; project dependency `mpmath>=1.3`. [VERIFIED: pyproject.toml:15] [VERIFIED: local version probe] | High-precision verification points. | `verify_candidate()` uses 80-digit mpmath checks before returning `recovered`. [VERIFIED: verify.py:95-113] |
| pytest | Local `7.4.0`; dev dependency `pytest>=7.4`. [VERIFIED: pyproject.toml:18-21] [VERIFIED: local version probe] | Regression gates for suite contracts, scaffolds, and proof aggregates. | Existing tests already cover proof metadata, optimizer scaffolds, and reports. [VERIFIED: tests/test_benchmark_contract.py:243-260] [VERIFIED: tests/test_optimizer_cleanup.py:22-34] |

### Supporting

| Module | Version / Contract | Purpose | When to Use |
|--------|--------------------|---------|-------------|
| `src/eml_symbolic_regression.compiler` | Existing project module. [VERIFIED: compiler.py:1-270] | Exact EML identity oracle for `exp(k*x)` and arithmetic depth measurement. | Use in tests/research to prove shapes; do not route proof evidence through compile mode for SHAL-02. [VERIFIED: 30-CONTEXT.md:23-24] |
| `src/eml_symbolic_regression.master_tree` | Existing project module. [VERIFIED: master_tree.py:287-372] | Soft tree construction, constant catalog, slot forcing, snap results, and AST embedding. | Add scaffold helpers here when they are generic tree operations. [VERIFIED: master_tree.py:357-371] |
| `src/eml_symbolic_regression.optimize` | Existing project module. [VERIFIED: optimize.py:16-178] | Training attempts, scaffold provenance, candidate selection, and optimizer manifest. | Extend `TrainingConfig.scaffold_initializers` and `_apply_scaffold()` for exponential-family attempts. [VERIFIED: optimize.py:135-178] |
| `src/eml_symbolic_regression.benchmark` | Existing project module. [VERIFIED: benchmark.py:716-1225] | Proof suite contract, run artifacts, derived evidence class, aggregate threshold status. | Extend suite cases and assert bounded threshold status. [VERIFIED: benchmark.py:1036-1057] |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Family scaffolds | More random restarts at depth 4 | Baseline failures snap confidently to the wrong `log(variable)` AST, so more random budget does not address the known failure mechanism. [VERIFIED: /tmp/eml-phase30-baseline/v1.5-shallow-proof/*.json] |
| Blind proof artifacts | Compiler or warm-start route | Compile-only and same-AST warm starts are explicitly excluded from SHAL-02 proof success. [VERIFIED: .planning/REQUIREMENTS.md:21] [VERIFIED: 30-CONTEXT.md:23-24] |
| Verified EML identities | New symbolic-regression library | Project scope is EML-tree recovery, and no new dependency is needed for this phase. [VERIFIED: AGENTS.md] [VERIFIED: pyproject.toml:11-21] |
| Phase 30 scaffold repair | Local snap/discrete repair | Local repair is deferred to Phase 31. [VERIFIED: 30-CONTEXT.md:102-108] |

**Installation:**

No new package installation is recommended for Phase 30. [VERIFIED: pyproject.toml:11-21]

## Architecture Patterns

### Recommended Project Structure

```text
src/eml_symbolic_regression/
├── datasets.py       # Add declared signed/scaled proof formula specs or proof-only helpers. [VERIFIED: datasets.py:70-191]
├── proof.py          # Extend shallow claim case IDs when suite inventory changes. [VERIFIED: proof.py:232-248]
├── benchmark.py      # Add suite cases, constants/budgets, artifacts, and threshold regression hooks. [VERIFIED: benchmark.py:716-867]
├── master_tree.py    # Add reusable family scaffold forcing/embedding helpers. [VERIFIED: master_tree.py:354-371]
├── optimize.py       # Add scaffold attempt planning and manifest provenance. [VERIFIED: optimize.py:135-178]
└── verify.py         # Leave verifier semantics unchanged. [VERIFIED: verify.py:70-125]

tests/
├── test_master_tree.py          # Exact scaffold shape and snap-margin tests. [VERIFIED: tests/test_master_tree.py:13-34]
├── test_optimizer_cleanup.py    # Scaffold provenance and recovered candidate tests. [VERIFIED: tests/test_optimizer_cleanup.py:22-53]
├── test_benchmark_contract.py   # Suite inventory and proof metadata tests. [VERIFIED: tests/test_benchmark_contract.py:243-260]
├── test_benchmark_runner.py     # Artifact fields and evidence-class derivation tests. [VERIFIED: tests/test_benchmark_runner.py:68-98]
└── test_benchmark_reports.py    # Bounded threshold pass/fail regression. [VERIFIED: tests/test_benchmark_reports.py:132-146]
```

### Pattern 1: Suite-Owned Exponential-Family Contract

**What:** Put formula IDs, seeds, budgets, tolerances, constants, and threshold metadata in the suite/case contract, not in CLI filters. [VERIFIED: 30-CONTEXT.md:16-20] [VERIFIED: benchmark.py:716-737]

**When to use:** Use this for every proof target counted toward `paper-shallow-blind-recovery`. [VERIFIED: proof.py:232-248]

**Planner action:** Extend `BenchmarkCase` / `OptimizerBudget` or an adjacent proof-case config to carry literal constants and scaffold family parameters; serialize those fields in `run_id`, `budget`, and artifacts so proof runs are reproducible. [VERIFIED: benchmark.py:53-86] [VERIFIED: benchmark.py:274-306] [ASSUMED]

### Pattern 2: Family Scaffold Attempts Before Random Restarts

**What:** Existing `fit_eml_tree()` builds scaffold attempts first, then random restarts, and records the winning attempt in the manifest. [VERIFIED: optimize.py:65-79] [VERIFIED: optimize.py:100-130]

**When to use:** Add `scaffold_scaled_exp` and `scaffold_signed_scaled_exp` attempts using declared family constants and variables before random attempts. [VERIFIED: optimize.py:135-178] [ASSUMED]

**Required provenance:** Each new attempt log should include `kind`, `variable`, `scale`, `constant_policy`, `strategy`, `seed`, and whether the scaffold was exact-shape or family-prior. [VERIFIED: optimize.py:173-178] [ASSUMED]

### Pattern 3: Exact Shape Must Be Proven Before It Becomes a Proof Target

**What:** The paper gives exact identities for `exp(x)` and `ln(x)`, and the code has exact helpers for those identities. [CITED: sources/paper.pdf via pdftotext lines 16-23] [VERIFIED: expression.py:235-256]

**Scaled exponential shape:** Existing verified lowering for `exp(k*x)` is `exp_of(multiply_expr(Const(k), Var(variable)))`, where `multiply_expr` is a verified EML multiplication identity and `exp_of` is `Eml(arg, Const(1))`. [VERIFIED: compiler.py:149-163] [VERIFIED: expression.py:247-250]

**Depth evidence:** Manual compiler probes on 2026-04-15 returned depth `9`, node count `19`, constants `{k, 1}` for both `beer_lambert` and `radioactive_decay`. [VERIFIED: manual PYTHONPATH=src compiler probe] This is incompatible with the current depth `4` budget unless Phase 30 proves a shorter shape. [VERIFIED: benchmark.py:731-735] [ASSUMED]

### Pattern 4: Threshold Aggregation Is the Regression Gate

**What:** `aggregate_evidence()` groups runs and computes threshold rows from derived evidence classes. [VERIFIED: benchmark.py:1036-1057] `bounded_100_percent` requires a `1.0` pass rate over allowed evidence classes. [VERIFIED: proof.py:148-164]

**When to use:** Add a regression test that executes a CI-scale proof suite or synthetic proof results and asserts the threshold row for `paper-shallow-blind-recovery` is `passed`, with all eligible runs classified as `blind_training_recovered`. [VERIFIED: tests/test_benchmark_reports.py:132-146] [ASSUMED]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Recovery decision | A custom proof-success boolean | `verify_candidate()` plus `evidence_class_for_payload()` [VERIFIED: verify.py:70-125] [VERIFIED: benchmark.py:1205-1225] | The verifier already checks train, held-out, extrapolation, and high precision. [VERIFIED: verify.py:84-113] |
| Threshold math | A new percent calculation in tests | `aggregate_evidence()` threshold rows [VERIFIED: benchmark.py:1036-1057] | The policy already separates allowed evidence classes from catalog/compile classes. [VERIFIED: proof.py:148-164] |
| EML arithmetic identities | Ad hoc SymPy string rewrites | Existing `multiply_expr`, `exp_of`, `log_of`, and compiler validation tests [VERIFIED: compiler.py:149-163] [VERIFIED: tests/test_compiler_warm_start.py:30-39] | Branch-sensitive EML identities need independent numeric verification. [CITED: sources/paper.pdf via pdftotext lines 470-510] |
| AST-to-tree mapping | Manual per-path code for every new target | `SoftEMLTree.embed_expr()` or small helpers built on `set_slot()` [VERIFIED: master_tree.py:354-450] | Embedding already validates depth, variables, constants, and round-trip snap equality. [VERIFIED: master_tree.py:425-450] |
| Suite metadata | Test-only hardcoded cases | `BenchmarkCase`, `BenchmarkRun`, and built-in suite registry [VERIFIED: benchmark.py:137-306] [VERIFIED: benchmark.py:716-737] | Run IDs and artifacts already include proof metadata and budgets. [VERIFIED: benchmark.py:274-306] |

**Key insight:** The phase should improve candidate generation while leaving proof ownership with existing verifier and threshold machinery. [VERIFIED: 30-CONTEXT.md:28-32]

## Common Pitfalls

### Pitfall 1: Calling a Depth-9 Shape a Depth-4 Proof

**What goes wrong:** The suite keeps `radioactive_decay` and Beer-Lambert at depth `4` while the implemented exact shape requires depth `9`, causing persistent snapped-but-failed runs or disguised warm starts. [VERIFIED: benchmark.py:731-735] [VERIFIED: manual PYTHONPATH=src compiler probe]

**Why it happens:** Current exact `exp(k*x)` lowering goes through multiplication, and multiplication is deep in EML. [VERIFIED: compiler.py:149-163] [CITED: sources/paper.pdf via pdftotext lines 438-439 and 590-720]

**How to avoid:** Add a Wave 0 evidence task: for each signed/scaled candidate, record exact EML depth, node count, constants, verifier result, and whether a shorter direct-search identity exists. [ASSUMED]

**Warning signs:** `snap.active_node_count` remains `7`, `snap.min_margin` remains `1.0`, and artifacts show the `log(variable)` AST for scaled exponential targets. [VERIFIED: /tmp/eml-phase30-baseline/v1.5-shallow-proof/*.json]

### Pitfall 2: Smuggling Compile/Warm-Start Evidence Into Blind Recovery

**What goes wrong:** A proof run is counted after following `compile_and_validate()` or `fit_warm_started_eml_tree()`, even though SHAL-02 excludes compile-only and same-AST warm-start evidence. [VERIFIED: .planning/REQUIREMENTS.md:21] [VERIFIED: tests/test_compiler_warm_start.py:132-156]

**Why it happens:** The existing warm-start path can return `same_ast_return` and verified recovery for Beer-Lambert with one step. [VERIFIED: tests/test_compiler_warm_start.py:132-156]

**How to avoid:** Keep Phase 30 proof cases in `start_mode="blind"` and `training_mode="blind_training"`; use compiler outputs only as research/golden-shape oracles, not as run execution paths. [VERIFIED: benchmark.py:847-867] [VERIFIED: 30-CONTEXT.md:23-24]

**Warning signs:** Artifacts contain `compiled_eml`, `warm_start_eml`, `same_ast_return`, or `compile_only_verified` for a SHAL-02 run. [VERIFIED: benchmark.py:842-928] [VERIFIED: benchmark.py:1205-1225]

### Pitfall 3: Missing Literal Constants in the Blind Terminal Bank

**What goes wrong:** A scaled exponential scaffold cannot be represented or embedded because the tree has only `const:1` and the variable as terminals. [VERIFIED: master_tree.py:145-152] [VERIFIED: tests/test_compiler_warm_start.py:119-128]

**Why it happens:** `TrainingConfig.constants` defaults to `(1.0,)`, and the benchmark blind path does not pass formula-specific constants into the config. [VERIFIED: optimize.py:16-29] [VERIFIED: benchmark.py:847-856]

**How to avoid:** Add suite-owned literal constants to the blind proof budget and propagate them into `TrainingConfig.constants`, while recording that non-`1` constants were supplied by the proof contract. [VERIFIED: master_tree.py:19-35] [ASSUMED]

**Warning signs:** `EmbeddingError("missing_constant")`, absent `const:-0.4` / `const:-0.8` labels in `slot_catalog()`, or artifact configs that list only `constants=["1"]`. [VERIFIED: master_tree.py:375-443] [VERIFIED: optimize.py:122-130]

### Pitfall 4: Expanding the Signed/Scaled Inventory Past the Bound

**What goes wrong:** The suite adds amplitude-scaled targets such as `A*exp(k*x)` or signed-amplitude targets such as `-exp(k*x)` without a bounded exact shape and then fails the 100% threshold. [ASSUMED]

**Why it happens:** Existing EML multiplication and negation identities are available but deep, and Shockley-style `scale*(exp(a)-1)` is depth `13` in the current compiler path. [VERIFIED: compiler.py:135-163] [VERIFIED: compiler.py:242-264] [VERIFIED: tests/test_benchmark_runner.py:315-325]

**How to avoid:** Interpret Phase 30 signed/scaled variants as exponent-coefficient sign/scale variants, such as `exp(-a*x)` and `exp(+a*x)`, unless a committed evidence task proves amplitude-signed variants fit the declared shallow bound. [ASSUMED]

**Warning signs:** New variants require `multiply_expr` outside the exponent, `negate_expr`, or Shockley's `scaled_exp_minus_one_template` before any training begins. [VERIFIED: compiler.py:135-163] [VERIFIED: compiler.py:242-264]

## Code Examples

Verified patterns from current sources:

### Exact Scaled-Exponent Oracle Shape

```python
from eml_symbolic_regression.compiler import multiply_expr
from eml_symbolic_regression.expression import Const, Var, exp_of


def scaled_exponent_expr(variable: str, scale: float):
    # Source: compiler.py multiply_expr + expression.py exp_of.
    return exp_of(multiply_expr(Const(scale), Var(variable)))
```

This produces the verified current `exp(scale * variable)` EML shape, but manual probes show depth `9` and node count `19` for `scale=-0.4` and `scale=-0.8`. [VERIFIED: compiler.py:149-163] [VERIFIED: expression.py:247-250] [VERIFIED: manual PYTHONPATH=src compiler probe]

### Scaffold Helper Shape

```python
from eml_symbolic_regression.master_tree import EmbeddingConfig


def force_scaled_exp(model, variable: str, scale: float, strength: float = 30.0):
    expr = scaled_exponent_expr(variable, scale)
    return model.embed_expr(expr, EmbeddingConfig(strength=strength))
```

Use this only after the suite declares `depth >= expr.depth()` and includes `scale` in the tree constant catalog. [VERIFIED: master_tree.py:425-450] [ASSUMED]

### Proof Artifact Regression Shape

```python
aggregate = aggregate_evidence(result)
threshold = next(
    row for row in aggregate["thresholds"]
    if row["claim_id"] == "paper-shallow-blind-recovery"
)
assert threshold["status"] == "passed"
assert threshold["rate"] == 1.0
assert threshold["evidence_classes"] == {"blind_training_recovered": threshold["eligible"]}
```

This mirrors the existing bounded-threshold tests while tightening the expected result for Phase 30. [VERIFIED: tests/test_benchmark_reports.py:132-146] [ASSUMED]

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Blind random restarts only | Blind runs include primitive `exp` / `log` scaffolds before random restarts. [VERIFIED: optimize.py:135-178] | Phase 25 / v1.4 verification committed as `6bbc5fe`. [VERIFIED: git log] | `exp` and `log` recover in the v1.5 baseline, while scaled exponentials still fail. [VERIFIED: /tmp/eml-phase30-baseline/v1.5-shallow-proof/aggregate.md] |
| Proof success based on raw verifier status | Proof success derives evidence classes and threshold rows. [VERIFIED: benchmark.py:1036-1057] [VERIFIED: benchmark.py:1205-1225] | Phase 29 verification committed as `1f61253`. [VERIFIED: git log] | Catalog/compile evidence can exist but does not satisfy SHAL-02 when evidence class is not blind training recovery. [VERIFIED: proof.py:148-164] |
| Demo formulas only | Proof datasets include manifests with provenance and split signatures. [VERIFIED: datasets.py:212-230] | Phase 29. [VERIFIED: 29-VERIFICATION.md] | Phase 30 can add variants without raw-array artifacts if `DemoSpec` or proof helpers provide provenance. [VERIFIED: datasets.py:52-63] |

**Deprecated/outdated:** Treating Beer-Lambert warm-start success as blind proof is invalid for Phase 30. [VERIFIED: .planning/REQUIREMENTS.md:21] [VERIFIED: tests/test_compiler_warm_start.py:132-156]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The supported signed/scaled variant set should initially mean sign/scale of the exponent coefficient, not amplitude multiplication outside the exponential. | Common Pitfalls / Architecture Patterns | If the user meant amplitude-signed `A*exp(k*x)`, the phase needs deeper shape evidence or a narrowed contract. |
| A2 | A depth-9 exact `exp(k*x)` scaffold may still be acceptable as a bounded shallow proof target if the contract explicitly declares that bound. | Summary / Architecture Patterns | If "shallow" is fixed to depth <=4, current verified shapes cannot satisfy Beer-Lambert or radioactive decay without finding a shorter identity. |
| A3 | Adding literal constants to blind proof budgets can preserve blind semantics when constants are declared in the suite contract and provenance says they are supplied constants. | Architecture Patterns / Pitfalls | If supplied constants are considered compiler/catalog leakage, Phase 30 needs pure-`1` constant synthesis or a different proof target. |

## Open Questions (RESOLVED)

1. **What is the maximum paper-realistic shallow depth for Phase 30 scaled exponentials?**
   - What we know: current proof suite uses depth `4` for Beer-Lambert and `radioactive_decay`. [VERIFIED: benchmark.py:731-735]
   - What's unclear: existing verified compiler lowering needs depth `9`, and this research did not prove a shorter direct-search identity. [VERIFIED: manual PYTHONPATH=src compiler probe]
   - Recommendation: plan a first task that either proves a shorter exact shape or updates the suite contract to the smallest verified depth with committed evidence. [ASSUMED]
   - RESOLVED: Phase 30 may update the shallow scaled-exponential bound to the smallest verified exact depth, but only after a planned evidence task records the depth, node count, constants, verifier status, and reason the bound remains paper-realistic. If a shorter exact shape is found, prefer the shorter bound.

2. **Are amplitude-signed variants in scope for SHAL-01?**
   - What we know: SHAL-01 says signed/scaled exponential variants, while Beer-Lambert and radioactive decay are coefficient-scaled exponentials inside `exp(k*x)`. [VERIFIED: .planning/REQUIREMENTS.md:20] [VERIFIED: datasets.py:100-124]
   - What's unclear: amplitude variants like `-exp(k*x)` or `2*exp(k*x)` require additional negation/multiplication identities. [VERIFIED: compiler.py:135-163]
   - Recommendation: include exponent-coefficient sign/scale variants first; include amplitude variants only after a shape/depth evidence task. [ASSUMED]
   - RESOLVED: Interpret Phase 30 signed/scaled variants as exponent-coefficient sign/scale variants first, such as `exp(-a*x)` and `exp(+a*x)`. Amplitude-signed variants are deferred unless the evidence task proves they fit the declared shallow bound without weakening the training-proof contract.

3. **Should signed/scaled variants live in `datasets.py` or proof-only helpers?**
   - What we know: Phase context allows either, provided formula provenance is retained. [VERIFIED: 30-CONTEXT.md:34-37]
   - What's unclear: permanent demo catalog entries may imply product/showcase support beyond this proof suite. [ASSUMED]
   - Recommendation: use `DemoSpec` entries only for variants likely to remain user-facing; otherwise add a proof-suite target helper that emits the same provenance fields as `DemoSpec.formula_provenance()`. [VERIFIED: datasets.py:52-63] [ASSUMED]
   - RESOLVED: Any target counted by the declared proof suite should be represented as a permanent importable target with full `DemoSpec`-compatible provenance. It may be named as a proof target rather than a showcase demo, but it must not be an anonymous ad hoc helper.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| Python | Package, benchmark, tests | Yes [VERIFIED: local version probe] | 3.11.x local; project allows `>=3.11,<3.13`. [VERIFIED: pyproject.toml:10] | None needed |
| PyTorch | Optimizer and soft tree | Yes [VERIFIED: local version probe] | 2.10.0 [VERIFIED: local version probe] | None recommended |
| NumPy | Dataset generation and verifier | Yes [VERIFIED: local version probe] | 1.26.4 [VERIFIED: local version probe] | None recommended |
| SymPy | Formula provenance and shape oracle | Yes [VERIFIED: local version probe] | 1.14.0 [VERIFIED: local version probe] | None recommended |
| mpmath | High-precision verifier | Yes [VERIFIED: local version probe] | 1.3.0 [VERIFIED: local version probe] | None recommended |
| pytest | Regression tests | Yes [VERIFIED: local version probe] | 7.4.0 [VERIFIED: local version probe] | None recommended |
| pdftotext | Research citation extraction only | Yes [VERIFIED: command -v pdftotext] | `/opt/homebrew/bin/pdftotext` [VERIFIED: command -v pdftotext] | Not required for implementation |

**Missing dependencies with no fallback:** None found for Phase 30 implementation. [VERIFIED: local version probe]

**Missing dependencies with fallback:** None found for Phase 30 implementation. [VERIFIED: local version probe]

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | No [VERIFIED: phase scope has CLI/local artifacts only] | No authentication surface in Phase 30. [VERIFIED: 30-CONTEXT.md:6-32] |
| V3 Session Management | No [VERIFIED: phase scope has CLI/local artifacts only] | No sessions. [VERIFIED: 30-CONTEXT.md:6-32] |
| V4 Access Control | No [VERIFIED: phase scope has local benchmark artifacts only] | No multi-user authorization. [VERIFIED: benchmark.py:768-784] |
| V5 Input Validation | Yes [VERIFIED: custom benchmark suites and proof contracts validate inputs] | Keep `BenchmarkCase.validate()`, `DatasetConfig.validate()`, and proof-contract validation fail-closed. [VERIFIED: benchmark.py:53-86] [VERIFIED: benchmark.py:173-236] |
| V6 Cryptography | No [VERIFIED: phase scope has no secrets or crypto] | Existing SHA digests are artifact integrity metadata, not security controls. [VERIFIED: datasets.py:203-230] |

### Known Threat Patterns for Local Proof Artifacts

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Evidence-class spoofing in suite config | Tampering | Continue rejecting caller-supplied `evidence_class`; derive it from payload execution. [VERIFIED: benchmark.py:161-168] [VERIFIED: benchmark.py:779-781] |
| Malformed proof case counted under a claim | Tampering | Keep suite/case validation against claim suite IDs and case IDs. [VERIFIED: benchmark.py:221-236] |
| Artifact ambiguity between blind and warm-start runs | Repudiation | Keep `training_mode`, `start_mode`, threshold policy, and scaffold provenance serialized. [VERIFIED: benchmark.py:274-306] [VERIFIED: optimize.py:100-130] |
| Invalid dataset sampling parameters | Tampering | Keep positive `points` and `tolerance` validation. [VERIFIED: datasets.py:212-218] [VERIFIED: benchmark.py:62-70] |

## Sources

### Primary (HIGH confidence)

- `.planning/phases/30-bounded-shallow-blind-training-recovery/30-CONTEXT.md` - locked decisions, baseline, deferred scope, and integration points. [VERIFIED: initial read]
- `.planning/REQUIREMENTS.md` - SHAL-01 through SHAL-04. [VERIFIED: initial read]
- `.planning/ROADMAP.md` and `.planning/STATE.md` - phase goal, dependency, and v1.5 scope. [VERIFIED: initial read]
- `.planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-VERIFICATION.md` - proof contract behavior verified in Phase 29. [VERIFIED: initial read]
- `src/eml_symbolic_regression/proof.py` - threshold and claim taxonomy. [VERIFIED: initial read]
- `src/eml_symbolic_regression/datasets.py` - formula inventory and provenance. [VERIFIED: initial read]
- `src/eml_symbolic_regression/benchmark.py` - proof suite, run artifacts, metrics, evidence classes, thresholds. [VERIFIED: initial read plus chunked reread]
- `src/eml_symbolic_regression/optimize.py` and `src/eml_symbolic_regression/master_tree.py` - scaffold attempts, constants, snapping, embedding. [VERIFIED: initial read]
- `src/eml_symbolic_regression/expression.py`, `verify.py`, `diagnostics.py`, and targeted tests - exact identities, verifier contract, current tests. [VERIFIED: initial read]
- `sources/paper.pdf` via `pdftotext` - EML definition, exp/log identities, master tree, PyTorch recovery behavior. [CITED: sources/paper.pdf via pdftotext]
- `sources/NORTH_STAR.md` and `sources/FOR_DEMO.md` - project blueprint and demo suitability constraints. [CITED: sources/NORTH_STAR.md] [CITED: sources/FOR_DEMO.md]

### Secondary (MEDIUM confidence)

- `.planning/research/STACK.md`, `.planning/research/ARCHITECTURE.md`, `.planning/research/PITFALLS.md` - prior milestone research for constant catalogs, embedding, compiler/warm-start pitfalls. [VERIFIED: local research docs]
- Manual local compiler probes for `beer_lambert`, `radioactive_decay`, and `shockley` using `PYTHONPATH=src`. [VERIFIED: manual command output]
- Baseline artifacts under `/tmp/eml-phase30-baseline/v1.5-shallow-proof/`. [VERIFIED: local artifact read]

### Tertiary (LOW confidence)

- Whether a shorter depth <=4 exact identity exists for `exp(k*x)` with literal constants was not resolved by this research. [ASSUMED]

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - versions and dependencies are local and already used by the repo. [VERIFIED: pyproject.toml] [VERIFIED: local version probe]
- Architecture: MEDIUM - integration points are clear, but the scaled-exponential depth bound needs an evidence task before planning can lock budgets. [VERIFIED: benchmark.py:716-737] [VERIFIED: manual compiler probe]
- Pitfalls: HIGH - baseline artifacts and existing tests directly expose the failure mode and proof-boundary risks. [VERIFIED: /tmp/eml-phase30-baseline/v1.5-shallow-proof/aggregate.md] [VERIFIED: tests/test_compiler_warm_start.py:132-156]

**Research date:** 2026-04-15
**Valid until:** 2026-05-15 for local code patterns; revisit sooner if Phase 30 changes suite depth, literal constant policy, or evidence taxonomy. [ASSUMED]
