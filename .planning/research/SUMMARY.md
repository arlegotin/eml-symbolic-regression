# Project Research Summary

**Project:** EML Symbolic Regression
**Domain:** Compiler-driven warm starts for a hybrid EML symbolic-regression engine
**Researched:** 2026-04-15
**Confidence:** HIGH for stack and architecture direction; MEDIUM for arithmetic compiler depth and Planck recovery feasibility

## Executive Summary

v1.1 should turn the completed v1 verifier, exact AST, soft master tree, optimizer, cleanup, and demo harness into a compiler-driven warm-start workflow. The product is still a research-grade Python package and CLI, but the new value is narrower and more precise: given a supported ordinary SymPy expression, compile it into an exact EML AST, embed that tree into a compatible trainable `SoftEMLTree`, perturb the logits, train back toward a snapped exact tree, and let the existing verifier decide whether the formula is recovered.

The recommended approach is incremental and verifier-gated. Add a project-owned compiler for a small SymPy subset, a finite literal constant catalog for demos that need numeric constants, an AST-to-logit embedding layer, deterministic perturbation metadata, and explicit CLI/report modes for compile-only and warm-start recovery. Do not add a parser generator, PySR, JAX, Rust, CUDA, theorem proving, learned coefficients, or broad SymPy coverage in v1.1.

The main risk is contract drift: compiler output, catalog formulas, or warm-start seeds can look like recovery without proving trained exact return-to-solution. Mitigate that by keeping `expression.Expr` as the only exact tree type, preserving `verify.py` as the sole owner of `recovered`, validating compiled ASTs against independent ordinary-expression evaluations before training, requiring embed->snap round trips, and separating catalog, compiled, warm-start, blind, failed, and stretch claims in reports.

## Key Findings

### Recommended Stack

No new runtime dependencies are needed. The current Python/PyTorch/SymPy/NumPy/mpmath/pytest stack already covers v1.1: SymPy supplies the ordinary-expression front end, the existing `expression.py` AST remains the exact EML target, PyTorch initializes and perturbs logits, and the existing verifier decides acceptance.

The v1.1 additions should be modules and configuration objects, not new platforms: `compiler.py`, compiler report schemas, warm-start embedding helpers, logit perturbation config, optimizer initialization hooks or a wrapper, and demo recovery metadata.

**Core technologies and additions:**
- Python 3.11: package, CLI, dataclasses, deterministic JSON, and report manifests.
- SymPy 1.14: accepted input type for supported ordinary expressions; traverse `Expr.func` and `Expr.args`, not printed strings.
- PyTorch 2.10 with `complex128`: existing `SoftEMLTree`, logits, warm-start biasing, seeded perturbation, and normal training loop.
- NumPy and mpmath: independent compile-time validation and verifier checks against the ordinary source expression.
- pytest: compiler rule tests, negative tests, embedding round trips, perturbation determinism, and demo promotion gates.
- Standard library `argparse`, `logging`, `json`, and dataclasses: CLI modes and layered manifests without extra dependencies.

**Stack additions, not dependencies:**
- `compiler.py`: deterministic SymPy-subset compiler with rule traces and unsupported-node diagnostics.
- `CompileResult` / `CompilerConfig`: source expression, normalized form, enabled rules, depth, node count, constants, domain assumptions, and warnings.
- Constant catalog support in `SoftEMLTree`: default stays `(1.0,)`; warm-start demos can include source literals such as `0.8`, `2.0`, and `0.5`.
- `embed_expr_into_tree()` or equivalent helper: maps exact AST paths to slot logits using `set_slot()` semantics.
- `PerturbationConfig` and embedding metadata: seed, noise scale, strength, active slot changes, snap margins, and pre/post perturbation snaps.
- Demo recovery plans: separate catalog showcase, compile-only, warm-start, blind baseline, and stretch modes.

### Feature Scope

v1.1 should promise warm-started recovery from a compiler-generated scaffold, not blind discovery of arbitrary deep formulas. The user-facing workflow is: select a supported demo or SymPy expression, compile it, validate the compiled AST, embed it, perturb logits, train, snap, clean up, verify, and report the public claim.

**Must have (table stakes):**
- Defined compiler subset with fail-closed unsupported reasons for unsupported functions, arbitrary powers, trig, piecewise, and special functions.
- Explicit constant policy for numeric literals used by demos.
- Compilation trace with rule names, constants, variables, domain assumptions, depth, node count, and validation error.
- Compile-time validation against independent ordinary-expression evaluation before warm-start training.
- Compatible terminal bank and depth diagnostics before embedding.
- AST-to-logit embedding with immediate high-strength embed->snap round-trip validation.
- Configurable warm-start strength and deterministic perturbation.
- Warm-start training mode that reuses the existing optimizer but records initialization provenance.
- Verifier-owned promotion: no demo becomes `recovered` from compile-only success or training loss.
- CLI-visible compile-only and warm-start modes with JSON reports.
- Regression tests for accepted rules, negative cases, depth failures, constant-bank failures, embedding, perturbation, and claim taxonomy.

**Differentiators:**
- Compiler-to-trainer bridge that demonstrates return-to-solution from near-correct EML trees.
- Evidence-rich warm-start reports with slot changes, margins, anomalies, losses, cleanup, and verifier results.
- Fixed-literal constant bank that makes Beer-Lambert and Michaelis-Menten practical while staying honest about provenance.
- Demo promotion by evidence rather than catalog verification.

**Defer:**
- Full SymPy-to-EML compiler.
- Pure `{1}` synthesis of arbitrary numeric constants.
- Learned coefficients or parameter fitting.
- General multivariate compiler UX.
- Trig/oscillator trained recovery.
- Guaranteed normalized Planck recovery.
- Shortest EML superoptimization, Rust, CUDA, GUI work, theorem proving, and generic symbolic-regression engines.

### Constant Policy

v1.1 should use a fixed literal constant policy for promoted scientific demos. Beer-Lambert needs `0.8`; Michaelis-Menten needs `2.0` and `0.5`. The exact AST already supports arbitrary `Const(value)`, but the soft master tree currently exposes only `const:1`, so warm-start compatibility requires a finite constant catalog.

Recommended policy:
- Keep default master-tree constants as `(1.0,)` so v1 behavior and paper parameter-count checks remain stable.
- Let compiler-driven demo runs include a deterministic literal catalog derived from the source expression, for example `(1.0, -1.0, 0.5, 0.8, 2.0)`.
- Serialize constant provenance explicitly, with fields such as `constant_policy: "literal_constants"`, `constant_basis: ["1", "literal_catalog"]`, `compiled_constants`, and `supplied_constants`.
- Do not claim literal-constant demos are pure `{1, eml}` basis recovery.
- Do not add learned coefficients in v1.1.
- Defer pure `1`-basis constant synthesis or rational-expansion research until a later milestone.

### Demo Promotion Criteria

Catalog verification, compiler success, and warm-start recovery are different claims. Reports must make that distinction visible.

A demo may be promoted to trained warm-start EML recovery only when all of these pass:
1. Source expression belongs to the supported compiler subset.
2. Compiler emits an exact `Expr` with trace metadata and acceptable depth/node count.
3. Compiled AST validates numerically against the independent ordinary source expression.
4. The soft tree has compatible variables, depth, and constant catalog.
5. High-strength embedding snaps immediately back to the compiled AST before perturbation.
6. Seeded perturbation and training run through the normal optimizer.
7. Final snap produces an exact AST.
8. Final exact AST passes train, held-out, extrapolation, and mpmath verification.
9. The public report derives `claim_status` from the final trained exact verification, not from the catalog or compiled seed.

Promotion targets:
- `exp` and `log`: keep as paper smoke tests and embedding fixtures.
- `beer_lambert`: first v1.1 promotion target; expected HIGH confidence with literal constants plus negation/multiplication/exp rules.
- `michaelis_menten`: second promotion target; expected MEDIUM confidence because addition, multiplication, division, positive-domain handling, and depth gates are required.
- `planck`: stretch reporting only; compile/attempt/failure evidence is useful, but do not gate v1.1 on trained recovery.
- `damped_oscillator`, trig-heavy, and special-function demos: defer.

### Architecture Approach

Extend the existing one-way pipeline rather than creating a parallel recovery path. The new compiler should produce ordinary `expression.Expr` trees, and warm-start training should feed the same optimizer, snapper, cleanup, and verifier contracts already established in v1.

**Major components:**
1. `compiler.py` - compiles a whitelisted SymPy subset into exact `Expr` trees and emits structured `CompileResult` metadata.
2. Compiler rule library - verified identities for constants, variables, `exp`, `log`, and arithmetic rules as they are proven.
3. Constant catalog extension - lets `SoftEMLTree` expose finite source literals while preserving the default `const:1` behavior.
4. AST embedding helper - maps compiled AST structure to `SoftEMLTree` slot paths and validates embed->snap equivalence.
5. Warm-start wrapper or initializer - initializes logits from compiled ASTs, applies deterministic perturbation, and runs existing training.
6. Demo recovery plan - declares catalog, compile, warm-start, blind baseline, and stretch modes per demo.
7. CLI/report integration - separates reference verification, compiled seed verification, warm-start training manifest, final verification, and public claim.
8. Test suite expansion - locks compiler rules, negative cases, constants, depth gates, embedding, perturbation, and demo promotion semantics.

**Recommended build order:**
1. Compiler scaffolding, direct rules, metadata, and compile-time validation.
2. Constant catalog and AST embedding with snap round-trip tests.
3. Arithmetic compiler subset and depth/node-count gates.
4. Perturbed warm-start training wrapper and manifests.
5. Demo promotion/reporting for Beer-Lambert, then Michaelis-Menten.
6. Planck stretch report and documentation of unsupported/failure modes.

### Critical Pitfalls

1. **Treating compiler output as correct without independent verification** - validate compiled ASTs against ordinary SymPy/NumPy/mpmath evaluation before warm starts.
2. **Smuggling arbitrary constants into a pure EML claim** - use explicit `literal_constants` metadata and avoid saying `{1, eml}` recovery when source literals are supplied.
3. **Generating trees too deep for warm-start recovery** - make depth and node count first-class gates before embedding or training.
4. **AST-to-master-tree embedding mismatch** - require immediate embed->snap equivalence and store mapped slots, inactive branches, margins, constants, and depth.
5. **Warm-start logits that are either trivial or unrecoverable** - sweep/report strength, noise, seed, gate flips, and margins instead of relying on one magic setting.
6. **Measuring perturbation success with training loss** - require post-snap exact verification and classify same-AST return, verified equivalent, soft fit only, and failure separately.
7. **Breaking verifier-owned recovery** - keep `recovered` restricted to exact trained/snapped candidates that pass `verify.py`.
8. **Losing domain and branch assumptions** - attach assumptions to compiler artifacts and keep verification ranges away from singularities unless explicitly tested.
9. **Using compiler seeds as evidence of blind discovery** - every artifact needs a `recovery_mode` or equivalent provenance field.
10. **Expanding compiler scope faster than tests** - implement a whitelist compiler with negative tests and stable reason codes.

## Requirements Implications

Downstream requirements should be phrased as observable behavior and acceptance gates, not implementation hopes.

- Given `exp(-0.8*x)`, the CLI can compile the formula to exact EML with literal constant metadata, validate the compiled tree, embed it, perturb logits with a seed, train, snap, verify, and report whether Beer-Lambert was recovered.
- Given `2*x/(0.5+x)`, the CLI can run the same workflow on a safe positive domain and promote Michaelis-Menten only if the final trained exact AST passes the verifier.
- Given an unsupported expression, the compiler returns a machine-readable unsupported reason and does not silently fall back to a catalog formula.
- Given a too-shallow tree, missing constant, unknown variable, or excessive compiled depth, embedding fails before training with actionable diagnostics.
- Every warm-start report includes source expression, normalized expression, compiler trace, constant policy, domain assumptions, compiled depth/node count, terminal bank, embedding assignments, warm-start strength, perturbation config, optimizer config, snap decisions, cleanup output, final verifier result, and public claim status.
- `--train-eml` or equivalent blind-training mode should remain distinct from a new compile/warm-start mode; blind and warm-start success rates must not be merged.
- Public documentation must state that v1.1 demonstrates verifier-gated return-to-solution from compiled warm starts, not unrestricted blind symbolic discovery.

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 1: Compiler Contract and Direct Rules

**Rationale:** The compiler becomes a trust boundary. It must fail closed, record metadata, and validate its output before any warm-start path can depend on it.

**Delivers:** `compiler.py`, `CompilerConfig`, `CompileResult`, rule trace schema, unsupported reason codes, domain assumptions, source-expression metadata, direct rules for variables, literal constants, `exp`, and `log`, and compile-time numeric validation.

**Addresses:** defined compiler subset, traceability, compile-only artifacts, unsupported-expression behavior, and source-to-EML validation.

**Avoids:** wrong compiler identities, shared-oracle bugs, broad SymPy overreach, and cleanup masking compiler errors.

### Phase 2: Constant Catalog and AST Embedding

**Rationale:** Warm-start demos cannot represent Beer-Lambert or Michaelis-Menten constants until the soft tree terminal bank can match compiler literals. Embedding must be mechanically correct before perturbation.

**Delivers:** finite constant catalogs in `SoftEMLTree` with default `(1.0,)`, canonical constant labels, missing-terminal diagnostics, `embed_expr_into_tree()`, `EmbeddingConfig`, `EmbeddingResult`, active slot manifests, inactive branch handling, and high-strength embed->snap tests.

**Addresses:** numeric constant policy, compatible terminal banks, required depth checks, AST-to-logit embedding, and round-trip safety.

**Avoids:** silent literal constants, parameter-count regressions, embedding chirality bugs, and warm starts that snap to the wrong AST.

### Phase 3: Arithmetic Rule Corpus and Depth Gates

**Rationale:** Beer-Lambert requires negation/multiplication/exp, and Michaelis-Menten requires addition, multiplication, division, constants, and domain handling. These identities are the highest-uncertainty part of v1.1.

**Delivers:** tested compiler rules for unary negation, subtraction, addition, multiplication, reciprocal/division, and optionally small integer powers behind depth caps; independent NumPy/mpmath equivalence tests; rule-level assumptions; depth/node-count budgets for demo formulas.

**Addresses:** practical demo coverage, compiler correctness, branch/domain assumptions, and promotion feasibility.

**Avoids:** bloated unembeddable EML trees, Planck scope pull, arithmetic identities accepted without proof, and arbitrary SymPy fallback.

### Phase 4: Perturbed Warm-Start Training

**Rationale:** The milestone is not just compile-only representability; it must show return-to-solution behavior from perturbed compiled trees using the normal optimizer and verifier.

**Delivers:** warm-start training wrapper or initializer, deterministic perturbation config, independent perturbation seed, active/inactive noise controls, pre/post perturb snaps, changed-slot metrics, initial/post-training losses, anomaly stats, and candidate-generation manifests.

**Addresses:** warm-start strength, perturbation, optimizer integration, reproducibility, and recovery metrics.

**Avoids:** magic logit settings, training-loss-only success, optimizer-owned recovery labels, and irreproducible demo runs.

### Phase 5: Demo Promotion and Claim Reporting

**Rationale:** Public claims need a stage-aware report so users can distinguish catalog showcase, compiled seed, warm-start attempt, trained exact recovery, blind baseline, and stretch status.

**Delivers:** `DemoRecoveryPlan`, CLI compile-only and warm-start modes, stage-separated JSON reports, concise stdout summaries, Beer-Lambert promotion gate, Michaelis-Menten promotion gate, Planck stretch reporting, and public documentation wording.

**Addresses:** demo taxonomy, verifier-owned promotion, CLI-visible workflow, and honest showcase criteria.

**Avoids:** catalog formulas being labeled recovered, Planck overpromising, hidden warm-start provenance, and blind/warm-start claim mixing.

### Phase 6: Regression Tests and Documentation Lockdown

**Rationale:** v1.1 touches claim semantics and numerical correctness. Negative tests and docs should be added alongside features, with a final phase to lock the public contract.

**Delivers:** negative compiler tests, constant-policy schema tests, depth and terminal-bank failures, embedding round-trip golden tests, perturbation determinism, verifier-owned claim tests, CLI report tests, and documentation explaining constants, recovery modes, and demo statuses.

**Addresses:** long-term maintainability and user-facing trust.

**Avoids:** untested unsupported cases, schema drift, accidental claim regression, and future contributors broadening compiler scope silently.

### Phase Ordering Rationale

- Compiler contract comes first because every later phase depends on an auditable exact AST and rule trace.
- Constant catalogs and embedding come before perturbation because warm starts must be representable and snap-correct before noise is meaningful.
- Arithmetic rule expansion gets its own phase because it has medium confidence and controls whether Michaelis-Menten is promotable.
- Perturbation training follows embedding and arithmetic because it should test a correct scaffold, not debug compiler structure.
- Demo reporting comes after the engine path because claim taxonomy must reflect real artifacts from compile, embed, train, snap, and verify.
- Planck remains a stretch report because it combines power, exponential, subtraction, division, depth growth, and optimizer sensitivity.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 3:** Exact EML identities for addition, subtraction, multiplication, division, reciprocal, and small powers; depth blow-up and branch assumptions need rule-level proof.
- **Phase 4:** Perturbation budgets, strength/noise grids, gate-flip thresholds, and deterministic recovery-rate reporting need empirical tuning.
- **Phase 5:** Planck feasibility, practical depth limits, and public status wording need careful validation if attempted.

Phases with standard patterns or enough local guidance to skip standalone research:
- **Phase 1:** Compiler scaffolding, direct `exp`/`log` rules, metadata schemas, and fail-closed traversal are well documented by local code and SymPy patterns.
- **Phase 2:** Constant catalogs and AST embedding are straightforward extensions of current `Const`, `Var`, `Eml`, `SoftEMLTree`, and `set_slot()` behavior.
- **Phase 6:** Test and documentation mechanics follow existing pytest, CLI report, and artifact patterns.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All research agrees no new dependencies are needed; current `pyproject.toml` stack and v1 modules support the workflow. |
| Features | HIGH/MEDIUM | Workflow, reporting, constants, and promotion gates are clear. Exact breadth of arithmetic compiler coverage remains MEDIUM until rules and depth budgets are proven. |
| Architecture | HIGH | Reusing `expression.Expr`, `SoftEMLTree`, optimizer, cleanup, and verifier preserves v1 boundaries. Arithmetic rule corpus and Planck stretch stay MEDIUM/LOW. |
| Pitfalls | HIGH | Risks are strongly grounded in current code, project constraints, paper limitations, NORTH_STAR, and FOR_DEMO guidance. |

**Overall confidence:** HIGH for v1.1 structure and Beer-Lambert path; MEDIUM for Michaelis-Menten promotion timing; LOW/MEDIUM for Planck trained recovery.

### Gaps to Address

- **Arithmetic identities:** Prove each EML arithmetic rule independently and keep unsupported forms fail-closed until tests pass.
- **Depth ceilings:** Establish practical depth/node-count budgets for Beer-Lambert, Michaelis-Menten, and any Planck attempt.
- **Constant representation:** Decide exact serialization/canonicalization for floats, rationals, and complex literals before demo promotion.
- **Domain assumptions:** Attach positive-domain, nonzero-denominator, branch-cut, and singularity exclusions to compiled artifacts and verifier reports.
- **Perturbation metrics:** Define what counts as meaningful movement from the compiled seed: unchanged snap, active gate flips, verified equivalent AST, or same-AST return.
- **Public wording:** Keep warm-start recovery clearly separate from blind symbolic discovery in CLI output, JSON reports, README text, and release notes.

## Sources

### Primary (HIGH confidence)

- `.planning/PROJECT.md` - v1.1 goal, active requirements, constraints, target demos, and out-of-scope boundaries.
- `.planning/STATE.md` - confirms v1 is complete and v1.1 is defining requirements.
- `.planning/research/STACK.md` - no-new-dependencies recommendation, stack additions, constant catalog guidance, optimizer and demo integration.
- `.planning/research/FEATURES.md` - table stakes, differentiators, anti-features, workflow, requirements implications, and demo promotion expectations.
- `.planning/research/ARCHITECTURE.md` - module boundaries, compiler architecture, warm-start embedding, CLI modes, build order, and testing strategy.
- `.planning/research/PITFALLS.md` - critical pitfalls, phase warnings, gates, and high-risk roadmap choices to avoid.
- `sources/NORTH_STAR.md` - hybrid pipeline, complex128 training, warm-start rationale, hardening/snap, cleanup, and verifier discipline.
- `sources/FOR_DEMO.md` - demo ranking, Beer-Lambert and Michaelis-Menten guidance, normalization cautions, and Planck stretch positioning.
- `sources/paper.pdf` - EML semantics, complete-tree grammar, compiler caveats, depth limits, warm-start behavior, and complex arithmetic concerns.

### Local implementation sources cited by research

- `src/eml_symbolic_regression/expression.py` - exact `Const`, `Var`, `Eml`, JSON artifacts, SymPy candidate support, and paper identities.
- `src/eml_symbolic_regression/master_tree.py` - soft tree labels, logits, `set_slot`, snapping, `force_exp`, `force_log`, and current `const:1` limitation.
- `src/eml_symbolic_regression/optimize.py` - current Adam training config, restarts, annealing, manifests, and candidate-generator boundary.
- `src/eml_symbolic_regression/verify.py` - verifier-owned recovery status and train/held-out/extrapolation/mpmath checks.
- `src/eml_symbolic_regression/datasets.py` and `src/eml_symbolic_regression/cli.py` - current demo specs, catalog reports, CLI flow, and promotion integration points.
- `tests/*.py` - existing semantics, master-tree, optimizer, cleanup, verifier, demo, and Planck guard coverage.

### Official/current references cited by research

- SymPy parsing and expression manipulation docs - input safety, tree traversal, and avoiding printed-form parsing.
- PyTorch complex numbers and `gumbel_softmax` docs - complex tensor support and avoiding legacy functional Gumbel-softmax as a core API.
- Python dataclasses docs - structured config/report objects.
- mpmath and pytest docs - high-precision verification and parametrized regression testing.

---
*Research completed: 2026-04-15*
*Ready for roadmap: yes*
