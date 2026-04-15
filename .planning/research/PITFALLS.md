# Domain Pitfalls

**Domain:** EML symbolic-regression engine over complete depth-bounded trees  
**Project:** EML Symbolic Regression  
**Researched:** 2026-04-15  
**Overall confidence:** HIGH for EML-specific risks grounded in the paper and north-star document; MEDIUM for tool-version risks verified against current official docs.

## Roadmap Phase Map

Use these phase labels when turning pitfalls into the implementation roadmap.

| Phase | Name | Scope |
|-------|------|-------|
| Phase 0 | Semantics and references | Canonical EML evaluator, complex branch policy, paper examples, high-precision oracle, fixture datasets. |
| Phase 1 | Master tree and shallow recovery | Complete univariate depth-2/depth-3 trees, paper reproduction, deterministic tree serialization, initial tests. |
| Phase 2 | Search and hardening | Restarts, temperature schedules, entropy/size regularization, anomaly logging, snapping margins. |
| Phase 3 | Symbolic export and cleanup | Exact EML AST, JSON export, SymPy translation, targeted rewrites, local discrete cleanup. |
| Phase 4 | Verification and demos | Held-out, extrapolation, high-precision, cross-backend verification, demo suite from `sources/FOR_DEMO.md`. |
| Phase 5 | Scaling | Multivariate support, coefficient fitting, Rust acceleration, GPU profiling, larger benchmarks. |

## Critical Pitfalls

### Pitfall 1: Semantics Drift Between Training and Verification

**What goes wrong:** The training evaluator silently differs from the exact EML semantics. Common causes are hidden epsilons in `log`, training clamps leaking into verification, inconsistent complex branch behavior, or treating a nearly real complex result as real without checking the imaginary residue.

**Why it happens:** EML depends on `eml(x, y) = exp(x) - ln(y)` and requires complex arithmetic internally. The paper explicitly relies on the principal branch when computing values such as `ln(-1)` to generate `i` and `pi`. The north-star document also requires separate training and verification evaluators.

**Consequences:** A formula can pass training loss and still fail as a symbolic expression. Recovered expressions may disagree across PyTorch, mpmath, SymPy, or a future Rust backend.

**Warning signs:**
- The same snapped tree has different outputs in PyTorch and mpmath.
- Verification only passes when the verifier uses the same clamps as training.
- Outputs expected to be real have persistent imaginary parts above tolerance.
- Branch-cut tests near negative real inputs are absent or flaky.

**Prevention:**
- Build a canonical semantics module in Phase 0 before training code.
- Define the exact branch policy for complex `log`, signed zero, infinities, and non-finite values.
- Keep two explicit modes: stabilized training mode and faithful verification mode.
- Ban hidden epsilons and clamps from verification. If a guard is needed, it must be visible in diagnostics.
- Add cross-backend golden tests for `exp(x)`, `ln(x)`, `x - y`, `x * y`, `x / y`, and at least one branch-sensitive identity.

**Detection:** Run every snapped candidate through PyTorch exact mode, mpmath high precision, and SymPy-rendered expression evaluation on random points, extrapolation points, and branch-adjacent points.

**Phase mapping:** Phase 0 blocker; Phase 4 must enforce it for every demo and release artifact.

**Confidence:** HIGH. Sources: paper pp. 5, 10-16; `sources/NORTH_STAR.md`; PyTorch complex docs; mpmath docs.

### Pitfall 2: Calling Soft Fit "Symbolic Recovery"

**What goes wrong:** The model fits data with soft categorical mixtures but never becomes an exact EML tree. The output is a neural surrogate, not a recovered formula.

**Why it happens:** The paper's trainable master tree uses logits or simplex weights as a continuous relaxation of discrete choices. Recovery requires hardening and snapping to exact choices.

**Consequences:** Roadmap and demos overstate the result. A low training MSE can hide non-discrete gates, bloated structures, or unstable extrapolation.

**Warning signs:**
- Reports emphasize training loss but omit gate entropy, snap margins, and post-snap loss.
- Many gates have top-1 probability below 0.95 late in training.
- Snapping causes a large loss jump.
- The CLI prints a formula before exact AST snapping succeeds.

**Prevention:**
- Define "recovered" as post-snap, discrete, verified, and simpler-than-nearby-alternatives where feasible.
- Track fit loss, gate entropy, top-1 margin, expected tree size, post-snap loss, and verification pass/fail separately.
- Refuse to export a recovered formula if any active gate is below a configured confidence margin, unless a top-k snap search resolves it.
- Keep "soft fit" and "recovered formula" as separate result statuses in the API and CLI.

**Detection:** Regression tests should include cases where soft loss is low but snapping fails, and should assert that the result is not labeled recovered.

**Phase mapping:** Phase 2 defines hardening metrics; Phase 3 enforces exact export; Phase 4 validates recovery claims.

**Confidence:** HIGH. Sources: paper pp. 13-15; `sources/NORTH_STAR.md`.

### Pitfall 3: Blind Depth Escalation

**What goes wrong:** The implementation assumes complete depth-bounded search means practical recovery at arbitrary depth from random initialization.

**Why it happens:** "Complete by design" is a representation claim, not an optimization guarantee. The paper reports blind recovery from random initialization at 100% for depth 2, about 25% for depths 3-4, below 1% for depth 5, and 0 successes in 448 attempts at depth 6. Warm starts from perturbed correct trees succeed much more reliably.

**Consequences:** The roadmap burns time on deep blind recovery before proving shallow correctness. Demos become unreliable and seed-sensitive.

**Warning signs:**
- Phase plans promise blind recovery of depth-5 or depth-6 formulas in v1.
- More restarts are added without curriculum, warm starts, or diagnostics.
- CI includes a deep recovery test that passes only for one lucky seed.
- Search cost grows exponentially while exact recovery rate is not measured.

**Prevention:**
- Start with depth 2 and depth 3 paper-like targets.
- Add depth curriculum: solve shallow, embed into deeper scaffolds, then unfreeze new gates.
- Make warm starts and priors first-class features rather than ad hoc demo hacks.
- Report recovery distributions across seeds, not single best runs.
- Put arbitrary blind depth-6 recovery explicitly out of scope for v1.

**Detection:** Maintain benchmark tables by depth, target, seed count, recovery rate, median restarts, and wall time.

**Phase mapping:** Phase 1 must reproduce shallow behavior; Phase 2 adds curriculum and restarts; Phase 5 investigates deeper scaling only after shallow reliability is routine.

**Confidence:** HIGH. Sources: paper p. 15; `sources/PROJECT.md`; `sources/NORTH_STAR.md`.

### Pitfall 4: Numerical Explosion From Nested `exp` and Complex `log`

**What goes wrong:** Training produces NaN, Inf, overflow, unstable gradients, or meaningless finite values after extreme intermediate computations.

**Why it happens:** EML composes exponentials and logarithms deeply. The paper reports overflow from multiply composed exponentials and NaNs from complex arithmetic implementation details. PyTorch's numerical accuracy docs also warn that large intermediate values can overflow even when final mathematical results are representable.

**Consequences:** Optimizer results become seed- and device-dependent. Snapping decisions may be based on corrupted gradients. Recovery statistics become misleading.

**Warning signs:**
- NaN/Inf appears in losses or gate gradients.
- Clamp counts rise sharply before convergence.
- A small input-range change makes the same target unrecoverable.
- CPU and GPU runs diverge before snapping.

**Prevention:**
- Default to `torch.complex128` for training.
- Clamp the real part entering `exp` only in training mode, and log every clamp.
- Track per-node max magnitude, NaN count, Inf count, clamp count, and imaginary residue.
- Normalize and nondimensionalize demo inputs before training.
- Fail fast when anomaly rates exceed thresholds instead of continuing silently.
- Re-run the snapped candidate with unclamped faithful semantics before accepting it.

**Detection:** Add anomaly snapshots to each run artifact and assert zero non-finite values in verification mode.

**Phase mapping:** Phase 0 defines numeric policy; Phase 1 adds instrumentation; Phase 2 uses anomaly logs to steer search; Phase 4 rejects unstable candidates.

**Confidence:** HIGH. Sources: paper p. 15; `sources/NORTH_STAR.md`; PyTorch numerical accuracy docs.

### Pitfall 5: Incorrect Master-Tree Construction

**What goes wrong:** The tree builder is not actually complete for the intended depth, so true formulas are unreachable even though the system claims a complete EML tree.

**Why it happens:** The univariate construction has a precise slot structure: each non-leaf input can choose among `1`, `x`, and a previous subtree output, while leaf slots choose only `1` or `x`. The paper gives the univariate parameter count `P(n) = 5 * 2^n - 6`. It is easy to get indexing, previous-subtree availability, or depth conventions wrong.

**Consequences:** Early failures are misdiagnosed as optimizer weakness. Paper examples such as `ln(x)` may fail even at the depth where they should be representable.

**Warning signs:**
- Level-2 parameter count is not 14 in the univariate case.
- `exp(x)` and constant `e` are not reachable by direct gate assignment.
- `ln(x)` cannot be constructed from the known paper formula.
- Dead branches are included in active gate counts, or active subtrees are pruned too early.

**Prevention:**
- Implement paper formulas as exact construction fixtures before any optimizer.
- Add structural tests for node counts, slot candidate sets, parameter counts, and depth naming.
- Keep a human-readable exact EML AST alongside the differentiable module graph.
- Start univariate; add multivariate gates only after univariate completeness tests pass.

**Detection:** Property tests should enumerate small-depth hard gate assignments and confirm evaluator consistency with the exact AST.

**Phase mapping:** Phase 1 blocker; Phase 5 must repeat the completeness audit for multivariate extensions.

**Confidence:** HIGH. Sources: paper pp. 12-14; `sources/NORTH_STAR.md`.

### Pitfall 6: Snapping Is Underspecified

**What goes wrong:** The hardening stage converts soft gates to one-hot choices using arbitrary thresholds, tie-breaking, or raw parameter values. A candidate that looks near-discrete becomes a different formula after snapping.

**Why it happens:** The relaxation uses logits or simplex weights, but exact EML trees require categorical choices. Near-ties and inactive branches make naive `argmax` brittle.

**Consequences:** Post-snap loss jumps, exact formulas are nondeterministic, and reproducibility collapses across seeds or hardware.

**Warning signs:**
- Different devices snap the same checkpoint differently.
- A small temperature change changes the exported formula.
- Active gate margins are not reported.
- Snapping ignores whether a branch is semantically dead.

**Prevention:**
- Implement snapping behind one explicit abstraction that consumes normalized categorical probabilities.
- Require a minimum top-1 margin for active gates.
- For ambiguous gates, evaluate top-k discrete alternatives after pruning dead branches.
- Store snap decisions, margins, and before/after losses in the run artifact.
- Do not depend directly on long-term availability of `torch.nn.functional.gumbel_softmax`; wrap any helper behind a project API because current PyTorch docs mark it as legacy.

**Detection:** Golden snapshots should reproduce the same snapped AST across repeated runs from the same checkpoint.

**Phase mapping:** Phase 2 defines snap readiness; Phase 3 owns exact AST export; Phase 4 rejects ambiguous formula claims.

**Confidence:** HIGH for snapping need from paper; MEDIUM for API-stability risk from PyTorch docs.

### Pitfall 7: False Positives From Weak Verification Data

**What goes wrong:** A wrong formula matches the training points and passes a shallow holdout but fails on extrapolation, singular neighborhoods, or high-precision evaluation.

**Why it happens:** Symbolic regression is prone to coincidental agreement on small datasets. The paper's search methodology treats numerical matches as candidates requiring independent verification, not proofs.

**Consequences:** The demo can show a plausible but incorrect law. Future cleanup may optimize toward the wrong expression.

**Warning signs:**
- Training and test points come from the same grid or same backend only.
- Verification does not include extrapolation.
- A simpler baseline fits as well as the discovered formula.
- High-precision residuals grow outside the training range.

**Prevention:**
- Use independent train, held-out, extrapolation, and high-precision point sets.
- Generate some verification points with mpmath, not the training backend.
- Include adversarial points near domain boundaries and singularities for each target.
- Compare against smaller-depth candidates and simple baselines before declaring exact recovery.
- Record verification tolerances per target and per numeric backend.

**Detection:** Every "recovered" result must include a verification report with pass/fail status by split and backend.

**Phase mapping:** Phase 4 blocker; Phase 1 and Phase 2 can use lighter checks but must not call results final.

**Confidence:** HIGH. Sources: paper pp. 7, 14-15; `sources/NORTH_STAR.md`; mpmath docs.

### Pitfall 8: Symbolic Simplification Becomes an Unchecked Oracle

**What goes wrong:** The implementation relies on generic `simplify()` or branch-invalid identities to transform formulas, accidentally changing the mathematical function.

**Why it happens:** EML uses complex principal-branch semantics. Identities such as `log(exp(x)) = x` are not globally valid over the complex plane. SymPy's own docs state that simplification is not a well-defined stable algorithmic contract and recommend specific simplification functions for algorithmic use.

**Consequences:** Cleanup may produce a prettier but wrong expression. Verification failures appear after the expression has already been presented to users.

**Warning signs:**
- Cleanup calls broad `simplify()` as the main correctness step.
- Rewrites lack assumptions and domain checks.
- A simplified formula passes on positive real samples but fails on complex or negative-adjacent samples.
- The displayed formula is not linked to the exact EML AST that was verified.

**Prevention:**
- Treat SymPy as a renderer and targeted rewrite engine, not as the source of truth.
- Maintain exact EML AST as the canonical artifact.
- Use explicit passes such as `cancel`, `together`, `powsimp`, or targeted trig rewrites only when assumptions are recorded.
- Verify after each cleanup pass; if a rewrite changes behavior, keep the previous expression.
- Report both the exact EML tree and the simplified human expression.

**Detection:** Cleanup tests should include branch-sensitive counterexamples and assert that every rewrite preserves high-precision sampled behavior.

**Phase mapping:** Phase 3 owns targeted cleanup; Phase 4 verifies cleaned formulas.

**Confidence:** HIGH. Sources: `sources/NORTH_STAR.md`; SymPy simplify docs; paper pp. 10-16.

### Pitfall 9: Demo Overreach and Raw Physical Units

**What goes wrong:** The first public demos choose famous but numerically hostile laws, raw SI constants, high-depth expressions, unconstrained phases, or singular domains.

**Why it happens:** Famous laws are attractive, but the paper's optimization results make depth and initialization major constraints. `sources/FOR_DEMO.md` explicitly recommends normalized, dimensionless, visually distinctive targets and warns against raw full Planck law, special functions, piecewise laws, chaotic systems, and high-depth blind recovery.

**Consequences:** The implementation may be correct but look unreliable. Roadmap pressure shifts toward ad hoc demo tuning instead of engine fundamentals.

**Warning signs:**
- The first demo is normalized Planck or damped oscillator before Beer-Lambert/logistic/Michaelis-Menten works.
- Targets include arbitrary physical constants without a coefficient strategy.
- Demo scripts require hand-picked lucky seeds.
- Plots look good but post-snap verification fails.

**Prevention:**
- Follow the high-success sequence from `sources/FOR_DEMO.md`: Beer-Lambert or radioactive decay, Michaelis-Menten, logistic growth, Shockley diode, damped oscillator, normalized Planck.
- Use dimensionless normalized inputs and outputs.
- Separate "sanity demo", "reliable demo", and "flagship demo" tiers.
- Allow warm starts or priors in difficult demos, but label them honestly.
- Do not include raw SI Planck, chaotic systems, special functions, or piecewise empirical laws in v1.

**Detection:** Each demo must run from a clean config with published seeds and produce a verification report, not just a plot.

**Phase mapping:** Phase 4; demo feasibility should influence Phase 1 and Phase 2 benchmarks.

**Confidence:** HIGH. Sources: `sources/FOR_DEMO.md`; paper p. 15.

### Pitfall 10: Misrepresenting EML Completeness

**What goes wrong:** The product claims to recover arbitrary equations or all mathematical functions because EML generates the paper's elementary basis.

**Why it happens:** The phrase "all elementary functions" is easy to overread. The paper uses a concrete scientific-calculator basis and finite expressions built from it, with complex intermediates and a distinguished constant `1`. It does not cover arbitrary non-elementary, piecewise, stochastic, discrete-event, or high-noise laws.

**Consequences:** Roadmap chooses impossible benchmarks, users submit invalid tasks, and failure cases look like bugs.

**Warning signs:**
- Requirements include Bessel, Airy, erf, elliptic functions, integrals, ODE solvers, chaotic systems, or arbitrary data mining in v1.
- Dataset loaders accept unsupported targets without scope warnings.
- Documentation says "universal symbolic regression" without qualifiers.

**Prevention:**
- State the supported class as compact elementary expressions in the paper's calculator basis, within a depth budget.
- Add explicit unsupported-target diagnostics.
- Include negative demos or tests that show graceful "not recovered" behavior.
- Keep "fits arbitrary data" separate from "recovers exact elementary law".

**Detection:** Review docs, CLI messages, and result schemas for overclaiming before every release.

**Phase mapping:** Phase 0 docs and result taxonomy; Phase 4 demo copy; Phase 5 benchmark selection.

**Confidence:** HIGH. Sources: paper pp. 1-2, 5, 12-16; `sources/PROJECT.md`; `sources/FOR_DEMO.md`.

## Moderate Pitfalls

### Pitfall 11: Reproducibility Erodes Under Randomness and Hardware Variation

**What goes wrong:** The same config has different recovery outcomes across runs, devices, or PyTorch versions.

**Warning signs:**
- CI intermittently fails recovery tests.
- A checkpoint snaps differently on CPU and GPU.
- Benchmark tables omit seed counts.

**Prevention:**
- Persist seeds, package versions, dtype, device, backend flags, git commit, dataset hash, and snap settings in every run artifact.
- Use deterministic algorithms where practical, but do not promise bitwise reproducibility across all platforms.
- Test recovery rates statistically across seed batches.
- Run final verification on CPU high precision even if training used GPU.

**Phase mapping:** Phase 1 run artifacts; Phase 2 benchmark harness; Phase 4 release verification.

**Confidence:** HIGH. Sources: PyTorch reproducibility docs; PyTorch numerical accuracy docs.

### Pitfall 12: Real-Valued Targets Hide Complex Failure

**What goes wrong:** The loss only monitors real residuals, so the model produces formulas with non-negligible imaginary components that are discarded or rounded away.

**Warning signs:**
- The evaluator calls `.real` before computing loss without tracking imaginary magnitude.
- Demos only plot the real part.
- High-precision verification reports imaginary residue.

**Prevention:**
- Compute and log both real residual and imaginary residue.
- Add an imaginary penalty or acceptance threshold for real-valued target tasks.
- Keep complex-valued internals explicit in result diagnostics.
- Refuse to render a real formula if imaginary residue exceeds tolerance.

**Phase mapping:** Phase 0 evaluator contract; Phase 1 tests; Phase 4 verification reports.

**Confidence:** HIGH. Sources: paper pp. 5, 15-16; `sources/NORTH_STAR.md`.

### Pitfall 13: Coefficients Are Smuggled Into the Grammar

**What goes wrong:** To fit demos with parameters such as `Vmax`, `Km`, `A`, `gamma`, `omega`, or `Is`, the implementation adds arbitrary continuous coefficients without defining how they snap, verify, or relate to the EML-only grammar.

**Warning signs:**
- Demo success depends on learned real constants not present in the exported AST.
- Exact recovery is claimed while fitted coefficients are approximate floats.
- Parameter fitting and structural discovery are mixed in one opaque loss.

**Prevention:**
- For v1, prefer normalized or dimensionless demo forms with small known constants.
- If coefficients are needed, make them a separate optional layer after symbolic scaffold discovery.
- Report coefficient status explicitly: fixed, fitted approximate, snapped exact, or externally supplied.
- Verify formulas with coefficients at higher precision and include coefficient uncertainty.

**Phase mapping:** Phase 4 demo design; Phase 5 semi-parametric extension.

**Confidence:** MEDIUM-HIGH. Sources: `sources/FOR_DEMO.md`; `sources/NORTH_STAR.md`.

### Pitfall 14: Complete Trees Produce Bloated Correct Formulas

**What goes wrong:** The engine recovers a functionally correct but unnecessarily large EML tree, and users see unreadable output.

**Warning signs:**
- Post-snap tree size is close to the full master tree size.
- Many subtrees evaluate to constants or identities.
- The simplified expression is much shorter than the verified EML AST, but the transformation path is not recorded.

**Prevention:**
- Track active node count and expected tree size during training.
- Add size regularization after semantics are stable.
- Prune dead branches before top-k snap search.
- Run bounded local cleanup and compare against smaller-depth candidates.
- Report both pre-cleanup and post-cleanup sizes.

**Phase mapping:** Phase 2 size pressure; Phase 3 cleanup; Phase 4 final reporting.

**Confidence:** HIGH. Sources: paper Table 4 and pp. 12-15; `sources/NORTH_STAR.md`.

### Pitfall 15: Acceleration Arrives Before Correctness

**What goes wrong:** Rust or custom CUDA work begins before the Python reference semantics, snapping, and verification are locked down.

**Warning signs:**
- There are two evaluators with no shared golden tests.
- Performance tasks block paper reproduction.
- Optimized kernels implement training clamps but not verification semantics.

**Prevention:**
- Build a slow, clear Python reference first.
- Treat any Rust or CUDA evaluator as a derived backend that must pass the exact same golden corpus.
- Add acceleration only after profiling identifies a specific bottleneck.
- Prioritize Rust for local discrete cleanup and verification before custom CUDA training kernels.

**Phase mapping:** Phase 5 only, except small profiling hooks. Phase 0-4 should not depend on acceleration.

**Confidence:** HIGH. Sources: `sources/PROJECT.md`; `sources/NORTH_STAR.md`.

### Pitfall 16: Data Generation Leaks the Answer

**What goes wrong:** Synthetic targets are generated using the same EML evaluator or same snapped tree representation being tested, so tests validate shared bugs rather than recovery.

**Warning signs:**
- Target data and candidate evaluation call the same code path.
- No closed-form ordinary-expression generator exists for demos.
- Bugs in EML semantics do not break any benchmark.

**Prevention:**
- Generate benchmark targets from independent ordinary formulas where possible.
- For paper-specific EML fixtures, also include independently evaluated mpmath or SymPy expected values.
- Store dataset provenance and generator expression with each fixture.

**Phase mapping:** Phase 1 paper reproduction; Phase 4 demos.

**Confidence:** MEDIUM-HIGH. Sources: paper verification methodology pp. 7, 14-15; `sources/NORTH_STAR.md`.

## Minor Pitfalls

### Pitfall 17: Result Files Are Not Diffable or Deterministic

**What goes wrong:** JSON exports change key ordering, omit dtype/backend metadata, or serialize floats inconsistently.

**Prevention:** Define a deterministic AST schema with stable node IDs, sorted keys, explicit dtype/backend metadata, and separate fields for exact symbols versus approximate numeric diagnostics.

**Phase mapping:** Phase 3.

**Confidence:** MEDIUM. Source: `sources/PROJECT.md` requirement for deterministic JSON.

### Pitfall 18: CLI Exit Codes Do Not Distinguish Failure Modes

**What goes wrong:** Optimization failure, snap ambiguity, verification failure, unsupported target, and internal numeric error all look like generic failure.

**Prevention:** Define result statuses early: `soft_fit_only`, `snap_failed`, `verification_failed`, `recovered`, `unsupported_target`, `numeric_error`.

**Phase mapping:** Phase 1 initial statuses; Phase 4 user-facing stability.

**Confidence:** MEDIUM. Source: roadmap implications from `sources/PROJECT.md` and `sources/NORTH_STAR.md`.

### Pitfall 19: Test Suite Only Checks Happy Paths

**What goes wrong:** The engine passes simple recovery tests but lacks tests for branch cuts, NaNs, snap ties, failed verification, and unsupported targets.

**Prevention:** Add negative tests from the start: invalid domains, high-depth impossible demo, ambiguous gates, numerical explosion, simplifier-invalid rewrite, and "not recovered" reporting.

**Phase mapping:** All phases; especially Phase 0 and Phase 4.

**Confidence:** HIGH. Sources: paper p. 15; `sources/NORTH_STAR.md`.

### Pitfall 20: Benchmark Metrics Optimize the Wrong Thing

**What goes wrong:** The project optimizes only MSE or wall time and loses sight of exact symbolic recovery.

**Prevention:** Track exact recovery rate, post-snap verification pass rate, tree size, cleanup delta, seed sensitivity, anomaly counts, extrapolation error, and search cost.

**Phase mapping:** Phase 2 benchmark harness; Phase 4 demo reports; Phase 5 scaling.

**Confidence:** HIGH. Sources: `sources/NORTH_STAR.md`; paper pp. 14-15.

## Phase-Specific Warnings

| Phase | Likely pitfall | Mitigation |
|-------|----------------|------------|
| Phase 0 | Semantics drift gets baked into every later component. | Build canonical exact and training evaluators first; add branch and high-precision tests before optimizer work. |
| Phase 1 | Master tree is incomplete or depth conventions are wrong. | Reproduce paper formulas and parameter counts with direct hard gate assignments before training. |
| Phase 2 | Search work becomes restart brute force. | Require recovery-rate dashboards, curriculum, warm starts, anomaly logs, and snap-readiness metrics. |
| Phase 3 | Cleanup changes formula semantics. | Keep exact EML AST canonical; use targeted rewrites only; verify after every cleanup pass. |
| Phase 4 | Demos overclaim exact recovery. | Use normalized demo sequence; require post-snap, held-out, extrapolation, and mpmath verification reports. |
| Phase 5 | Scaling creates a second incompatible engine. | Treat Rust/GPU/multivariate paths as derived implementations validated against Phase 0-4 golden corpora. |

## Implementation Gates

The roadmap should not advance past these gates without explicit evidence.

| Gate | Required evidence | Blocks |
|------|-------------------|--------|
| Semantics gate | Exact EML evaluator matches mpmath/SymPy fixtures on branch-sensitive tests. | Any training milestone. |
| Completeness gate | Depth-2 and depth-3 univariate master trees reach known paper formulas by direct assignment. | Optimization claims. |
| Recovery gate | A result can be labeled `recovered` only after snapping, exact AST export, and verification pass. | Demos and release notes. |
| Demo gate | Demo has clean config, published seed batch, verification report, and no hidden manual constants. | Public showcase. |
| Scaling gate | Accelerated or multivariate backend passes the golden corpus from the reference implementation. | Rust/CUDA/multivariate roadmap. |

## Highest-Risk Roadmap Choices to Avoid

| Bad choice | Why it is dangerous | Better choice |
|------------|---------------------|---------------|
| Start with deep blind recovery. | Paper reports rapid collapse beyond shallow depths from random initialization. | Start with shallow paper reproduction and curriculum. |
| Merge training and verification evaluators. | Stabilizers can change the mathematical function. | Keep training clamps visible and absent from exact verification. |
| Use generic simplification as proof. | Complex branch identities are not globally safe, and SymPy warns generic simplification is heuristic. | Use targeted rewrites plus high-precision verification. |
| Ship demos before snap/export/verify. | Low MSE is not symbolic recovery. | Require exact AST and verification report for every showcase result. |
| Add arbitrary coefficients ad hoc. | It changes the grammar and weakens exact-recovery claims. | Normalize demos first; add a documented coefficient layer later. |

## Sources

- Local: `sources/paper.pdf`, Andrzej Odrzywolek, "All elementary functions from a single operator", arXiv:2603.21852v2, 2026.
- Local: `sources/NORTH_STAR.md`, "Hybrid Symbolic Regression over Complete EML Trees".
- Local: `sources/FOR_DEMO.md`, demo selection and sequencing guidance.
- Local: `.planning/PROJECT.md`, project scope and constraints.
- PyTorch complex numbers docs: https://docs.pytorch.org/docs/stable/complex_numbers.html
- PyTorch reproducibility docs: https://docs.pytorch.org/docs/stable/notes/randomness.html
- PyTorch numerical accuracy docs: https://docs.pytorch.org/docs/stable/notes/numerical_accuracy.html
- PyTorch `gumbel_softmax` docs: https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.gumbel_softmax.html
- SymPy simplify docs: https://docs.sympy.org/latest/modules/simplify/simplify.html
- mpmath docs: https://mpmath.org/doc/current/
