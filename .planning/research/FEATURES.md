# Feature Landscape: v1.1 EML Compiler and Warm Starts

**Domain:** Compiler-driven warm starts for EML symbolic regression  
**Project:** EML Symbolic Regression  
**Researched:** 2026-04-15  
**Overall confidence:** HIGH for user-facing behavior; MEDIUM for exact compiler rule coverage until implementation proves the identities and depth costs.

## Scope

This research covers only new v1.1 behavior. v1 already provides exact EML ASTs, deterministic JSON, soft complete master trees, optimizer/snapping, verifier-owned recovery status, cleanup, CLI demo reports, and catalog demos. v1.1 should not re-solve those foundations; it should connect them into a compiler-driven warm-start workflow.

The user-facing promise should be: given a supported ordinary formula, compile it into an exact EML AST, embed that AST into a compatible soft master tree, perturb the logits in a controlled way, train back toward the solution, snap, and let the verifier decide whether the result is a recovered EML formula. This is warm-started recovery from a known compiler scaffold, not blind discovery.

## Expected User Workflow

1. User selects a supported demo or provides a SymPy-compatible expression such as `exp(-0.8*x)` or `2*x/(0.5 + x)`.
2. The compiler normalizes the expression, checks that every node is in the supported subset, and emits an exact EML AST plus a compilation trace.
3. The compiler validates the EML AST against the source expression on safe sample points before it is used for training.
4. The warm-start embedder builds or checks a compatible `SoftEMLTree` depth, variable set, and constant bank, then initializes logits near the compiled AST.
5. The perturbation step applies seeded logit noise or bounded slot perturbations and records how far the initial snap moved from the compiled tree.
6. Training runs from that perturbed warm start, then snaps to an exact AST.
7. Existing cleanup and verification run. A demo is promoted to trained EML recovery only when the verifier emits `recovered`.
8. The report clearly separates `compiled_reference`, `warm_start_attempt`, `snapped_candidate`, `recovered`, `verified_showcase`, and `failed` evidence.

## Table Stakes

Features users will expect for v1.1 to feel coherent. Missing any of these makes compiler-driven warm starts hard to trust.

| Feature | Why Expected | Complexity | Depends On | Expected Behavior |
|---------|--------------|------------|------------|-------------------|
| Defined compiler subset | Users need to know exactly what ordinary formulas are accepted. | Medium | SymPy catalog candidates, exact EML ASTs | Support constants, variables, `exp`, `log`, unary negation, subtraction, addition, multiplication, and division where implemented by explicit compiler rules. Unsupported nodes fail with `unsupported_operator`, not a silent fallback. |
| Numeric constant policy | Beer-Lambert and Michaelis-Menten require `0.8`, `2.0`, and `0.5`. | Medium | `Const`, AST JSON, master-tree terminal choices | v1.1 should treat numeric literals as fixed constants in the compiled AST and report `constant_policy: fixed_literal`. Do not claim those constants were synthesized from the paper's pure `1` basis. |
| Compilation trace | A compiled EML tree can be much larger than the source formula. | Medium | Compiler rule registry, AST metadata | Reports list normalized source expression, rules applied, constants introduced, variables, node count, depth, source-to-EML validation error, and any assumptions. |
| Round-trip validation before training | A bad compiler output would poison every warm-start result. | Medium | EML evaluators, SymPy candidate evaluation, verifier utilities | Compile-only output must be evaluated against the ordinary source expression on safe train/held-out-like points. Fail before warm-starting if max error exceeds tolerance. |
| Compatible terminal bank for warm starts | Current soft trees expose `const:1` and variables; compiler demos need fixed numeric constants too. | High | `SoftEMLTree`, slot catalog, `Const` | The compiler returns the constants it used, and warm-start tree construction includes the same fixed constants as legal terminal choices. If a constant is not representable in the tree, fail with `incompatible_terminal_bank`. |
| Required depth calculation | Users need actionable feedback when an AST cannot fit in a requested tree. | Medium | Exact AST depth, `SoftEMLTree.depth` | The compiler/embedder reports `compiled_depth` and `required_master_depth`. A too-shallow request fails with `depth_too_small` unless the CLI is explicitly allowed to raise depth. |
| AST-to-logit embedding | This is the core bridge from compiler to trainable model. | High | Exact ASTs, soft tree paths, slot choices | Active compiled paths get high but finite logits for the matching `child`, `var:name`, or `const:value` choices. Inactive slots use a deterministic policy and are included in the manifest. |
| Configurable warm-start strength | Users need to tune how close the model starts to the compiled tree. | Low | Logit embedding | Expose a strength parameter with a documented default. Stronger values should snap immediately to the compiled AST before perturbation; weaker values allow more exploration. |
| Controlled perturbation | The paper-grounded value of warm starts is return-to-solution from nearby states. | Medium | Embedded logits, deterministic seeds, manifests | Support seeded Gaussian logit noise as the default perturbation. Report perturbation scale, seed, pre-perturb snap, post-perturb snap, changed slots, and snap margins. |
| Warm-start training mode | Users should be able to run a normal training attempt from the embedded/perturbed state. | Medium | Optimizer, training config, anomaly stats | Existing optimizer settings still apply, but the manifest must identify the run as `initialization: compiled_warm_start` and include compiler and perturbation metadata. |
| Verifier-owned promotion | A compiler-derived tree is not automatically a recovered trained formula. | Low | Existing verifier | Beer-Lambert and Michaelis-Menten become `recovered` demos only after the post-training snapped exact EML AST passes train, held-out, extrapolation, and mpmath checks. |
| Demo status taxonomy | Users must not confuse catalog verification, compile-only success, and trained recovery. | Medium | CLI reports, verifier status | Reports distinguish `compiled_exact_reference`, `warm_start_recovered`, `verified_showcase`, `warm_start_failed`, and `unsupported`. Existing `recovered` remains verifier-owned. |
| Beer-Lambert trained recovery demo | This is the lowest-risk scientific warm-start target. | Medium | Compiler constants, negation/multiplication/exp, embedding, verifier | `beer_lambert` should compile `exp(-0.8*x)`, perturb, train, snap, verify, and report a trained exact EML recovery when it passes. |
| Michaelis-Menten trained recovery demo | This is the first serious non-exponential scientific target for v1.1. | High | Compiler Add/Mul/Div, constants, positive-domain sampling, embedding, verifier | `michaelis_menten` should compile `2*x/(0.5+x)`, run warm-start recovery on its safe positive domain, and promote only on verifier pass. |
| Honest Planck stretch reporting | Normalized Planck is important but deeper and riskier. | Medium | Compiler exp/sub/div/power where feasible, report taxonomy | Planck may be compile-only or attempted warm-start in v1.1, but should remain stretch/unsupported unless the full trained snapped AST verifies. |
| CLI-visible workflow | The feature should be usable without writing Python glue. | Medium | Current `demo` CLI and JSON reports | The CLI should expose compile-only and warm-start demo paths, either as new subcommands or flags on `demo`. Reports remain JSON and reproducible. |
| Regression tests for behavior | Compiler/warm-start bugs can create false recovery claims. | High | pytest, deterministic seeds | Tests cover accepted subset, unsupported-node failures, constant-bank compatibility, embedding/snap equivalence, perturbation determinism, and demo promotion gates. |

## Differentiators

Features that make v1.1 more than a catalog-demo relabeling exercise.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Compiler-to-trainer bridge | Turns known ordinary formulas into trainable EML initializations, directly exploiting the warm-start behavior emphasized in `sources/NORTH_STAR.md`. | High | This should be the centerpiece of v1.1. |
| Evidence-rich warm-start report | Lets users audit whether the model actually returned to the compiled solution after perturbation. | Medium | Include slot changes, snap margins, losses, anomalies, tree edit distance if available, and verifier results. |
| Fixed-literal constant bank | Makes real demo formulas practical without pretending constant synthesis is solved. | Medium | This is pragmatic and honest; later milestones can explore pure-`1` constant generation or learned coefficients. |
| Compile-time validation gate | Prevents bad compiler rules from being mistaken for optimizer or verifier failures. | Medium | A compile artifact should be trustworthy before training begins. |
| Demo promotion by evidence | Moves Beer-Lambert and Michaelis-Menten from `verified_showcase` to trained EML recovery only when the pipeline earns it. | Medium | Keeps the project's existing honesty about recovery claims. |
| Perturb-and-recover UX | Shows the actual scientific result from the paper: nearby correct basins are recoverable even when blind deep recovery is not reliable. | Medium | This is stronger and more honest than presenting warm starts as blind discovery. |

## Anti-Features

Features to explicitly not build or not claim in v1.1.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Full SymPy-to-EML compiler | Too broad; SymPy expressions include functions and assumptions outside the v1.1 target. | Define and test a narrow subset, then fail loudly on unsupported nodes. |
| Pure-`1` synthesis of arbitrary numeric constants | The paper basis is important, but generating compact constants like `0.8` and `0.5` from `1` is a separate hard problem. | Use fixed literal constants with explicit metadata and defer constant synthesis. |
| Trainable coefficient fitting | It changes the problem from discrete EML recovery to semi-parametric fitting. | Keep v1.1 constants fixed from the source expression; defer coefficient learning to a scaling milestone. |
| Calling compile-only success "recovered" | Compilation proves representability, not trained recovery from data. | Use `compiled_exact_reference`; reserve `recovered` for verifier-passed snapped training outputs. |
| Calling warm-start recovery "blind discovery" | Warm starts encode the target structure. Mislabeling would undermine credibility. | Report initialization provenance and perturbation strength in every artifact. |
| Auto-promoting demos on training loss | The project already established that training loss is not recovery. | Promotion requires the existing verifier's post-snap checks. |
| Guaranteeing Planck recovery in v1.1 | Normalized Planck is deeper and structurally harder than Beer-Lambert or Michaelis-Menten. | Keep Planck as stretch with compile/attempt/failure evidence. |
| Adding trig compiler support for oscillator demos | Damped oscillator is valuable but not required for the v1.1 target. | Defer trig identities and oscillator trained recovery until compiler basics are stable. |
| General multivariate compiler | v1.1 targets univariate demos. | Keep multivariate support limited to existing tree capability; defer formula compiler UX for multiple variables. |
| Shortest EML superoptimization | Compiled EML trees may be bloated, and shortest form is a separate search problem. | Report depth/node count and use existing cleanup; defer shortest-form search. |
| Silent fallback to catalog formula | Users must know whether an EML AST was compiled and trained. | If compilation or embedding fails, mark the demo `verified_showcase` or `unsupported` with reason codes. |

## Feature Dependencies

```text
Existing SymPy catalog candidate
  -> compiler normalization
  -> supported-subset check
  -> exact EML AST + compilation trace
  -> compile-time numeric validation
  -> constant/variable terminal bank
  -> compatible SoftEMLTree construction
  -> AST-to-logit embedding
  -> seeded perturbation
  -> warm-start training
  -> snapping
  -> cleanup
  -> verifier-owned recovery status
  -> demo promotion report
```

```text
Beer-Lambert promotion
  -> fixed numeric constants
  -> negation / multiplication / exp compiler rules
  -> warm-start embedding
  -> perturb-and-recover run
  -> verifier pass
```

```text
Michaelis-Menten promotion
  -> fixed numeric constants
  -> addition / multiplication / division compiler rules
  -> positive-domain sampling that avoids singularities
  -> warm-start embedding
  -> perturb-and-recover run
  -> verifier pass
```

```text
Planck stretch
  -> exp / subtraction / division rules
  -> power support for small positive integer powers
  -> larger depth budget
  -> honest unsupported-or-failed status if verification does not pass
```

## Complexity Notes

| Area | Complexity | Why |
|------|------------|-----|
| Compiler subset | Medium-High | The hard part is not parsing SymPy; it is making every rule produce semantically faithful EML ASTs with branch-aware validation. |
| Literal constants | Medium | AST support exists, but soft master-tree terminal catalogs currently need to grow beyond `const:1`. |
| Embedding | High | The embedder must map exact AST structure to the master tree's child/terminal slot grammar deterministically and validate snap equivalence. |
| Perturbation | Medium | Logit noise is straightforward, but reports must prove the perturbation meaningfully moved the initialization without destroying compatibility. |
| Beer-Lambert | Medium | The formula is simple, but constants and negated products must work. |
| Michaelis-Menten | High | Rational structure, division, constants, and singularity-safe domains all need to be correct. |
| Planck | High | Deeper expression with power, exp, subtraction, and division; good stretch, poor guarantee. |

## MVP Recommendation

Prioritize:

1. Compile-only artifacts for supported formulas, with rule traces and numeric validation.
2. Fixed-literal constants in both exact EML ASTs and warm-start-compatible soft tree terminal banks.
3. AST-to-logit embedding that snaps back to the compiled AST before perturbation.
4. Seeded perturbation plus warm-start training reports.
5. Beer-Lambert and Michaelis-Menten promotion only after verifier-passed trained snapped EML outputs.

Defer:

- Pure-`1` constant synthesis.
- Learned coefficients or parameter fitting.
- Full SymPy coverage, trig identities, and oscillator trained recovery.
- Guaranteed normalized Planck recovery.
- Multivariate compiler UX.
- Shortest EML search or Rust/CUDA acceleration for compiler outputs.

## Requirements Implications

Downstream requirements should be phrased as observable behavior:

- Given `exp(-0.8*x)`, the CLI can compile the expression to exact EML, validate it numerically, embed it into a compatible soft tree, perturb logits with a seed, train, snap, verify, and write a report that states whether Beer-Lambert was recovered.
- Given `2*x/(0.5+x)`, the CLI can perform the same workflow on the Michaelis-Menten safe domain and promote the demo only if the verifier passes.
- Given an unsupported expression, the compiler fails with a machine-readable reason and does not silently run the catalog candidate as if it were EML recovery.
- Given a too-shallow tree or missing constant terminal, warm-start embedding fails before training with required depth or terminal-bank diagnostics.
- Every warm-start report includes source expression, compiler trace, compiled AST metadata, terminal bank, warm-start strength, perturbation config, optimizer config, snap decisions, cleanup output, and verifier result.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Warm-start workflow shape | HIGH | Directly follows project v1.1 goals and `sources/NORTH_STAR.md` guidance that perturbed correct initializations are reliable compared with blind deep recovery. |
| Need for fixed literal constants | HIGH | Current demos and code use constants beyond `1`, while current soft tree slot labels expose only `const:1`; v1.1 needs an explicit policy. |
| Beer-Lambert as first promotion target | HIGH | `sources/FOR_DEMO.md` identifies it as easy and useful for exact recovery early. |
| Michaelis-Menten as serious v1.1 target | HIGH | It is already a catalog demo and one of the recommended public examples, but compiler/division coverage makes it higher complexity. |
| Exact compiler identities for full subset | MEDIUM | The subset is required by project goals, but each arithmetic rule must be proven in implementation and validated numerically. |
| Planck recovery in v1.1 | LOW-MEDIUM | Good stretch target, but too risky to promise as trained recovery. |

## Sources

- `.planning/PROJECT.md` - v1.1 goal, active requirements, out-of-scope limits, and demo promotion target.
- `.planning/STATE.md` - current milestone status and completed v1 capabilities.
- `README.md` - implemented recovery contract, CLI shape, demo status meanings, and current limits.
- `docs/IMPLEMENTATION.md` - module boundaries and current demo ladder.
- `src/eml_symbolic_regression/expression.py` - exact ASTs, arbitrary `Const`, SymPy catalog candidate behavior, paper identities.
- `src/eml_symbolic_regression/master_tree.py` - current soft slot catalog, hand-set gates, snapping behavior, and `const:1` limitation.
- `src/eml_symbolic_regression/optimize.py` - current training config, restarts, annealing, entropy/size penalties, and manifests.
- `src/eml_symbolic_regression/verify.py` - verifier-owned `recovered` versus `verified_showcase` status contract.
- `src/eml_symbolic_regression/datasets.py` - current Beer-Lambert, Michaelis-Menten, and Planck demo specs and safe domains.
- `sources/NORTH_STAR.md` - hybrid pipeline, warm-start rationale, verification discipline, and anti-overselling guidance.
- `sources/FOR_DEMO.md` - demo ranking, Beer-Lambert as easy early recovery, Michaelis-Menten as strong public demo, and Planck as flagship/stretch.
