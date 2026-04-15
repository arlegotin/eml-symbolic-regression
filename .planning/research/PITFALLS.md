# Domain Pitfalls: v1.1 EML Compiler and Warm Starts

**Domain:** Ordinary-expression-to-EML compilation, soft-tree embedding, and warm-start recovery demos  
**Project:** EML Symbolic Regression  
**Researched:** 2026-04-15  
**Overall confidence:** HIGH for risks grounded in the current code, `sources/paper.pdf`, `sources/NORTH_STAR.md`, and `sources/FOR_DEMO.md`; MEDIUM where recommendations infer implementation sequencing for features not yet present.

## Research Basis

The existing MVP already has exact EML AST nodes, deterministic AST JSON, canonical NumPy/mpmath evaluation, stabilized PyTorch training evaluation, complete soft EML master trees, snapping, a verifier-owned `recovered` status, catalog showcase candidates, and CLI demo reports. The current code does **not** yet have a compiler, an AST-to-master-tree embedding layer, warm-start logits, perturbation experiments, or demo promotion rules for compiler-assisted recovery.

The v1.1 risk profile is therefore not "can EML work at all?" The main risk is contract drift while connecting a new compiler and warm-start path to an existing verifier-owned MVP.

## Roadmap Phase Map

Use these phase labels when turning this research into roadmap controls.

| Phase | Name | Scope |
|-------|------|-------|
| Phase 1 | Compiler Contract and Rule Corpus | Define supported SymPy subset, constant policy, domain assumptions, compiler metadata, and rule-level identity tests. |
| Phase 2 | AST Embedding and Warm Starts | Embed compiled exact EML ASTs into compatible `SoftEMLTree` slot paths and initialize logits with explicit margins. |
| Phase 3 | Perturbed Warm-Start Recovery | Add controlled perturbation experiments, seed batches, return-to-solution metrics, and manifests. |
| Phase 4 | Demo Promotion and Reporting | Promote Beer-Lambert and Michaelis-Menten only when compile, train, snap, and verification all pass; keep Planck as stretch. |
| Phase 5 | Regression Tests and Documentation | Lock claim taxonomy, negative tests, reproducibility metadata, and user-facing wording. |

## Critical Pitfalls

### Pitfall 1: Treating Compiler Output as Correct Without Independent Verification

**What goes wrong:** The compiler emits an exact EML AST that is not equivalent to the ordinary source expression, but later training or cleanup hides the mismatch.

**Why it happens:** The paper's EML identities are constructive but branch-sensitive. EML is non-commutative, uses complex logarithms, and some compiler identities may rely on extended-real behavior such as `log(0) = -inf` and `exp(-inf) = 0`. The existing code only has two hand-coded identities, `exp(x)` and `log(x)`, and does not yet have a compiler rule corpus.

**Consequences:** A demo can pass because the target was generated from the same buggy compiled tree, not because the EML identity is valid. Later verification against independent targets will fail, and recovery claims become untrustworthy.

**Warning signs:**
- Compiler tests compare compiled output only to its own SymPy rendering.
- Rule tests use only positive real grids and avoid branch-adjacent points.
- New rules lack source-expression metadata and rule names.
- A broad `simplify()` result is accepted as proof of equivalence.
- The same compiled AST fails against mpmath or NumPy values from the ordinary source expression.

**Prevention:**
- Define a narrow supported subset first: variables, `exp`, `log`, unary negation, subtraction, addition, multiplication, division, and a documented constant subset.
- Every compiler rule must have an identity test against an independent ordinary-expression evaluator, not against EML output.
- Store compiler metadata in AST documents: source expression, normalized source, rule sequence, domain assumptions, constant policy, and compiler version.
- Verify compiled ASTs with NumPy and mpmath before they are allowed into warm-start training.
- Start with identities that do not require infinities or signed-zero tricks unless the semantics layer explicitly supports them.

**Detection:** Add a compiler corpus test that compiles each supported operator form, evaluates the ordinary expression and compiled EML AST on train, held-out, extrapolation, and edge-case points, and fails on any max error above tolerance.

**Phase mapping:** Phase 1 blocker; Phase 4 must rerun this for demo formulas.

**Confidence:** HIGH. Sources: `sources/paper.pdf` pp. 10-15, `sources/NORTH_STAR.md`, current `expression.py`, current `verify.py`.

### Pitfall 2: Smuggling Arbitrary Constants Into an EML-Only AST

**What goes wrong:** The compiler handles formulas such as `exp(-0.8*x)` or `2*x/(0.5+x)` by inserting arbitrary `Const(0.8)`, `Const(2)`, or `Const(0.5)` nodes while still labeling the artifact as an exact EML tree over the paper's `{1, eml}` basis.

**Why it happens:** The current `Const` class can store any complex value, but its AST metadata says the constant basis is `["1"]`. The v1.1 target demos contain numeric coefficients. The paper's EML basis can generate constants from `1`, but compiled forms for arithmetic and rationals may be very deep.

**Consequences:** The exported tree is not honest about its grammar. A warm-start demo may be solving an easier "EML plus arbitrary constants" problem while being reported as pure EML recovery.

**Warning signs:**
- AST documents include `const` values other than `1` but still say `constant_basis: ["1"]`.
- Demo success depends on float constants that are not compiled or marked as externally supplied.
- The compiler accepts all SymPy `Float` values silently.
- `candidate_kind` remains `exact_eml` without a coefficient or constant provenance field.

**Prevention:**
- Choose and document one constant policy before demo work:
  - **Pure EML:** compile supported constants from `1`, accepting depth growth.
  - **Supplied constants:** allow externally supplied constants, but label the artifact as EML with supplied constants, not pure `{1, eml}`.
  - **Rational subset:** support only small exact rationals with verified EML expansions.
- Do not allow arbitrary `Float` constants to enter exact recovery silently.
- Extend artifact metadata to distinguish `constant_basis`, `compiled_constants`, `supplied_constants`, and `approximate_coefficients`.
- For Beer-Lambert and Michaelis-Menten, decide whether `0.8`, `2`, and `0.5` are fixed supplied constants, exact rationals, or part of a later coefficient-fitting layer.

**Detection:** Add a schema test that rejects non-`1` constants unless the document explicitly declares the constant policy and provenance.

**Phase mapping:** Phase 1 blocker; Phase 4 demo promotion blocker.

**Confidence:** HIGH. Sources: `.planning/PROJECT.md`, `sources/FOR_DEMO.md`, current `expression.py`, current `datasets.py`.

### Pitfall 3: Generating Trees Too Deep for Warm-Start Recovery

**What goes wrong:** The compiler produces exact but bloated EML trees that exceed the practical master-tree depth budget, making embedding and training unusable.

**Why it happens:** The paper warns that the prototype compiler is not shortest-form. Table 4 shows very large compiler expressions for ordinary arithmetic: multiplication, division, addition, and average can be much larger than direct search forms. v1.1 target demos use multiplication, division, and numeric constants.

**Consequences:** The roadmap spends time compiling formulas that cannot fit into the configured `SoftEMLTree` or that require depths where blind optimization is known to degrade. Warm-starts become too expensive for tests and demos.

**Warning signs:**
- Compiler output depth is not reported.
- A formula compiles but cannot be embedded into the requested master-tree depth.
- The master tree is enlarged until tests become slow or flaky.
- Michaelis-Menten or Planck compiled trees use most of a full deep tree before any training begins.

**Prevention:**
- Treat compiler output depth as a first-class acceptance criterion.
- Add `compile_depth`, `node_count`, and `required_master_depth` to compiler artifacts.
- Implement shortest known identities for the v1.1 subset rather than naive recursive expansion everywhere.
- Put a depth cap on v1.1 demo promotion. If the compiled AST exceeds the cap, classify the demo as "compiled showcase only" or "unsupported at current depth".
- Prefer Beer-Lambert before Michaelis-Menten, and keep normalized Planck as stretch unless its compiled tree remains within an explicit budget.

**Detection:** Add tests that compile demo source expressions and assert expected depth/node-count ceilings. Failing the ceiling should not be a correctness failure; it should classify the target as not suitable for trained recovery yet.

**Phase mapping:** Phase 1 compiler; Phase 2 embedding; Phase 4 demo selection.

**Confidence:** HIGH. Sources: `sources/paper.pdf` Table 4 and p. 15, `sources/FOR_DEMO.md`, `.planning/PROJECT.md`.

### Pitfall 4: AST-to-Master-Tree Embedding Mismatch

**What goes wrong:** A compiled exact AST is valid, but the warm-start initializer cannot map it into the current `SoftEMLTree` slot structure without changing its meaning.

**Why it happens:** The current soft tree has path-specific left and right child subtrees. A slot can choose `const:1`, a variable, or that side's child. Embedding an arbitrary AST requires exact path assignment, depth compatibility, and dead-branch handling. Existing code only has manual `force_exp` and `force_log` helpers.

**Consequences:** Warm starts initialize a tree that snaps to a different expression than the compiled AST. Training then appears to "recover" from an invalid starting point or fails for the wrong reason.

**Warning signs:**
- Warm-start code compares only post-training loss, not the pre-training snapped AST.
- Embedding a compiled AST and immediately snapping does not round-trip to the same AST.
- Unused branches retain random logits and affect reported entropy/size metrics.
- Active paths are inferred from string prefixes without tests for left/right chirality.

**Prevention:**
- Implement `embed_ast(tree, expr, strength)` as a single tested abstraction.
- Require `tree.depth >= expr.depth()` before embedding.
- After embedding and before perturbation, immediately snap and assert structural/evaluation equivalence to the compiled AST.
- Initialize inactive branches deterministically and mark them as inactive in metadata.
- Store an embedding manifest: requested depth, expression depth, active slot assignments, inactive paths, strength, and pre-perturb snap margin.

**Detection:** Golden tests should compile `exp(x)`, `log(x)`, a subtraction identity, and a small rational expression, embed each into a compatible tree, snap immediately, and compare both AST structure and numeric behavior.

**Phase mapping:** Phase 2 blocker; Phase 3 perturbation depends on it.

**Confidence:** HIGH. Sources: current `master_tree.py`, current `tests/test_master_tree.py`, `sources/NORTH_STAR.md`.

### Pitfall 5: Warm-Start Logits Are Either Frozen or Too Weak

**What goes wrong:** The warm-start initializer sets logits so strongly that training cannot recover from perturbations, or so weakly that the correct tree is lost immediately.

**Why it happens:** Current manual helpers use a fixed `strength` value. v1.1 will need controlled initialization and perturbation around exact structures. The paper's warm-start claim is about perturbed correct solutions converging back, not about arbitrary hand-set logits.

**Consequences:** Perturbation demos become artifacts of one magic strength/noise combination. Results do not generalize across depth, formula, or seed.

**Warning signs:**
- Only one warm-start strength and one perturbation scale are reported.
- Stronger logits always pass without meaningful training movement.
- Weak perturbations preserve the same argmax in every slot, so the task is trivial.
- Larger perturbations flip active gates and never recover, but the report still says warm starts work.

**Prevention:**
- Define a grid of warm-start strengths and perturbation scales.
- Report pre-perturb margin, post-perturb margin, percentage of active gates flipped, and post-training recovered status.
- Include both "return without gate flips" and "return after gate flips" categories.
- Keep optimizer config fixed across comparable perturbation sweeps.
- Make a failed perturbation run a valid outcome, not a reason to hide the seed.

**Detection:** A perturbation benchmark should include multiple seeds per formula and produce recovery-rate tables by strength, noise scale, depth, and active-gate flip count.

**Phase mapping:** Phase 3 primary risk; Phase 4 reporting must expose the parameters.

**Confidence:** HIGH. Sources: `sources/paper.pdf` p. 15, `.planning/PROJECT.md`, current `master_tree.py`.

### Pitfall 6: Measuring Perturbation Success With Training Loss Instead of Exact Return

**What goes wrong:** A perturbed warm-start run is counted as successful because it fits the target, even though it snaps to a different exact tree or fails held-out/high-precision verification.

**Why it happens:** Existing `fit_eml_tree` is explicitly a candidate generator and verification is separate. Warm-start experiments can easily reuse best training loss as their success metric.

**Consequences:** The project overstates the paper's "returns to correct solution" behavior. A run may be a soft fit, an alternative equivalent tree, a wrong tree that interpolates, or a verified recovery, and these are different claims.

**Warning signs:**
- Perturbation reports contain `best_loss` but not post-snap verification.
- The result is not compared to the compiled seed AST.
- Equivalent-but-different trees are not distinguished from exact AST return.
- Failure reason codes are absent.

**Prevention:**
- Track separate statuses:
  - `returned_same_ast`
  - `verified_equivalent_ast`
  - `snapped_candidate_not_verified`
  - `soft_fit_only`
  - `failed`
- Require post-snap train, held-out, extrapolation, and mpmath checks before any recovery label.
- Compare the final AST to the warm-start AST structurally and numerically.
- Report alternative verified trees honestly as verified equivalents, not necessarily return-to-same-tree.

**Detection:** Add a test where a soft fit has low training loss but snaps incorrectly, and assert it is not counted as warm-start recovery.

**Phase mapping:** Phase 3 success metrics; Phase 4 demo claims; Phase 5 docs.

**Confidence:** HIGH. Sources: current `optimize.py`, current `verify.py`, `sources/NORTH_STAR.md`.

### Pitfall 7: Breaking the Verifier-Owned Recovery Contract

**What goes wrong:** The compiler or CLI promotes a catalog formula to `recovered` before an exact compiled EML AST has been trained, snapped, and verified.

**Why it happens:** The current demo harness stores catalog formulas as `SympyCandidate` and verifies them as `verified_showcase`, while exact EML ASTs can be `recovered`. v1.1 wants to promote Beer-Lambert and Michaelis-Menten, so it is tempting to reuse catalog verification as recovery evidence.

**Consequences:** The strongest existing contract in the MVP is weakened. Users cannot tell whether a result was catalog verification, compiler output, warm-start training, or post-snap recovery.

**Warning signs:**
- `claim_status` is copied from catalog verification while a trained candidate is nested elsewhere in the report.
- CLI output says "recovered" for a `candidate_kind` of `catalog_sympy`.
- A demo report lacks separate fields for catalog candidate, compiled seed, trained snapped candidate, and final verification.
- Planck is labeled as recovered after direct catalog verification.

**Prevention:**
- Keep verifier-owned `recovered` restricted to exact EML candidates unless `recovered_requires_exact_eml=False` is intentionally used for internal checks.
- Add explicit demo stages: `catalog_showcase`, `compiled_seed_verified`, `warm_start_attempted`, `trained_exact_recovered`.
- Reports should have separate statuses for the source formula, compiled seed, trained candidate, and public claim.
- Promote Beer-Lambert and Michaelis-Menten only when the final trained snapped AST passes the verifier.
- Keep normalized Planck as `stretch_showcase`, `compiled_only`, or `failed_warm_start` unless it passes the same contract.

**Detection:** Preserve and expand the existing test that ensures Planck is `verified_showcase`, not exact recovery. Add the same guard for every catalog-only demo.

**Phase mapping:** Phase 4 blocker; Phase 5 documentation and CLI tests.

**Confidence:** HIGH. Sources: current `verify.py`, current `datasets.py`, current `cli.py`, current `tests/test_verifier_demos_cli.py`, `.planning/PROJECT.md`.

### Pitfall 8: Domain and Branch Assumptions Are Lost During Compilation

**What goes wrong:** A compiled EML identity is valid only on a restricted domain, but the verifier samples outside that domain or the docs imply global equality.

**Why it happens:** The paper notes complex principal-branch issues and special behavior around negative real axes, zero, and endpoints. The current demos use safe positive domains for `log` and Michaelis-Menten, but a compiler can introduce intermediate `log`, reciprocal, or division behavior not obvious from the source expression.

**Consequences:** Verification becomes flaky near singularities, and a formula that is valid on the demo interval is overstated as globally valid.

**Warning signs:**
- Compiler output has no domain assumptions.
- Division and log rules do not record denominator/nonzero or positive-domain assumptions.
- Extrapolation ranges cross singularities or branch cuts.
- Imaginary residues are ignored for real target laws.

**Prevention:**
- Attach domain assumptions to compiled artifacts and verifier reports.
- Define demo-specific safe domains and edge probes before running warm starts.
- For division and log, include explicit singularity exclusions and boundary tests.
- Keep real-output acceptance tied to imaginary-residue thresholds.
- Avoid compiler identities requiring `log(0)` or signed infinities until those semantics are first-class in all evaluators.

**Detection:** Add edge-case tests for zero, near-zero, negative real values where applicable, and denominator-near-zero points for rational demos.

**Phase mapping:** Phase 1 compiler contract; Phase 4 verification.

**Confidence:** HIGH. Sources: `sources/paper.pdf` pp. 10-16, current `semantics.py`, current `verify.py`.

### Pitfall 9: Using Compiler Seeds as Evidence of Blind Discovery

**What goes wrong:** Warm-start demos are presented as if the system discovered the formula from data without prior structural information.

**Why it happens:** A compiler-assisted warm start begins from an ordinary source formula or near-correct EML tree. That is valuable, but it is not the same claim as random-initialized symbolic discovery.

**Consequences:** Demo messaging overclaims the system. The paper itself warns that blind recovery degrades sharply with depth; v1.1 should exploit warm starts honestly, not erase the distinction.

**Warning signs:**
- Reports omit whether the run used random initialization, compiled initialization, or perturbed compiled initialization.
- Public copy says "recovered from data" without "warm-started from compiled formula" when applicable.
- Blind and warm-start recovery rates are mixed in one table.

**Prevention:**
- Add a `recovery_mode` field to all run manifests: `blind`, `compiled_seed`, `perturbed_compiled_seed`, `catalog_verification`, or `compiled_only`.
- Report blind and warm-start results separately.
- For warm-start demos, state the prior explicitly: the system verified return-to-solution from a compiler-generated EML seed.
- Keep "catalog showcase" separate from "trained recovery" and "warm-start recovery".

**Detection:** CI should inspect demo JSON and fail if public `claim_status` lacks mode/provenance fields.

**Phase mapping:** Phase 3 manifests; Phase 4 demo reporting; Phase 5 documentation.

**Confidence:** HIGH. Sources: `sources/paper.pdf` p. 15, `sources/FOR_DEMO.md`, `.planning/PROJECT.md`.

### Pitfall 10: Expanding Compiler Scope Faster Than Tests

**What goes wrong:** The compiler accepts broad SymPy expressions, nested functions, floats, powers, trig, or special functions before the v1.1 subset is verified.

**Why it happens:** SymPy makes it easy to traverse arbitrary expression trees. `sources/FOR_DEMO.md` includes attractive stretch formulas such as damped oscillator and Planck, which can pressure the compiler beyond the active v1.1 subset.

**Consequences:** Unsupported expressions produce wrong or huge EML trees. Users see crashes or false confidence instead of clear unsupported-target diagnostics.

**Warning signs:**
- `compile_expr` has a generic fallback that tries to stringify or lambdify unsupported nodes.
- `Pow`, trig, piecewise, special functions, or arbitrary floats are accepted without specific rules.
- Unsupported Planck or damped oscillator cases fail deep in training rather than at compile time.

**Prevention:**
- Implement a whitelist compiler: unsupported SymPy node types must fail early with actionable reason codes.
- Add explicit `unsupported_operator`, `unsupported_constant`, `domain_required`, and `depth_limit_exceeded` statuses.
- Use normalized Planck as a stretch target only after the required subrules are present and depth-bounded.
- Do not add trig or arbitrary powers opportunistically to satisfy one demo.

**Detection:** Negative compiler tests should feed unsupported expressions and assert stable failure messages.

**Phase mapping:** Phase 1 compiler; Phase 4 demo classification; Phase 5 docs.

**Confidence:** HIGH. Sources: `.planning/PROJECT.md`, `sources/FOR_DEMO.md`, current `datasets.py`.

## Moderate Pitfalls

### Pitfall 11: Cleanup Masks Compiler Bugs

**What goes wrong:** A compiled EML AST is simplified into a readable expression that matches the source, but the original exact tree was wrong or was never independently verified.

**Warning signs:**
- Reports show only the cleaned SymPy expression.
- Cleanup runs before compiler identity verification.
- A cleanup pass changes behavior but the original compiled tree is discarded.

**Prevention:** Keep the exact compiled AST canonical. Verify the compiled AST before cleanup, verify after cleanup, and record both tree sizes and both verification reports.

**Phase mapping:** Phase 1 and Phase 4.

**Confidence:** HIGH. Sources: current `cleanup.py`, `sources/NORTH_STAR.md`.

### Pitfall 12: Source Traceability Is Too Thin for Debugging

**What goes wrong:** When a compiled warm-start fails, the artifact lacks enough metadata to tell whether the problem is parsing, a compiler rule, embedding, perturbation, optimization, snapping, or verification.

**Warning signs:**
- Run JSON contains only final formula and loss.
- Compiler rule sequence and embedding slot assignments are absent.
- Seed, dtype, depth, perturbation scale, and warm-start strength are not recorded.

**Prevention:** Use layered manifests: compiler manifest, embedding manifest, perturbation manifest, training manifest, snap manifest, verification report, and public claim summary.

**Phase mapping:** Phase 1 through Phase 4; Phase 5 tests schema completeness.

**Confidence:** HIGH. Sources: current `optimize.py` manifest pattern, `.planning/PROJECT.md`.

### Pitfall 13: Demo Data Reuses the Candidate as the High-Precision Target

**What goes wrong:** A demo target and verifier oracle come from the same candidate object, so compiler errors can pass if both sides share the same bug.

**Warning signs:**
- `target_mpmath` is derived from the compiled candidate being evaluated.
- The ordinary source formula is not evaluated independently after compilation.
- Dataset generation changes when the candidate changes.

**Prevention:** For compiler demos, keep the ordinary source expression as the independent oracle and compare compiled/trained exact EML candidates against it. Do not replace the target oracle with the compiled tree.

**Phase mapping:** Phase 1 compiler tests; Phase 4 demo reports.

**Confidence:** HIGH. Sources: current `datasets.py`, current `verify.py`.

### Pitfall 14: Reproducibility Regresses Under Warm Starts

**What goes wrong:** Warm-start runs look deterministic in demos but cannot be reproduced because the perturbation source, seed, or embedding parameters are omitted.

**Warning signs:**
- Perturbation noise uses global RNG state.
- Seed fields cover optimizer restarts but not perturbation.
- The same JSON config cannot reproduce the same pre-training snap.

**Prevention:** Separate seeds for dataset sampling, embedding perturbation, optimizer restarts, and any top-k snap search. Store package versions, dtype, device, tree depth, compiler version, and source expression.

**Phase mapping:** Phase 3 and Phase 4.

**Confidence:** HIGH. Sources: current `optimize.py`, current CLI seed handling.

### Pitfall 15: CLI Output Hides the Trained Candidate Status

**What goes wrong:** The CLI prints the catalog candidate status while the trained EML candidate is nested in JSON, causing users to misread the result.

**Warning signs:**
- `eml-sr demo michaelis_menten --train-eml` prints only the catalog `claim_status`.
- A trained verification failure is present in JSON but absent from stdout.
- The output path report does not summarize recovery mode.

**Prevention:** For v1.1 demo commands, print a compact stage summary: catalog status, compiled seed status, warm-start training status, final verifier status, and public claim.

**Phase mapping:** Phase 4; Phase 5 CLI tests.

**Confidence:** HIGH. Sources: current `cli.py`.

### Pitfall 16: Performance Problems Are Misdiagnosed as Optimization Failure

**What goes wrong:** Deep compiled warm starts are slow or memory-heavy, and the result is interpreted as a learning failure rather than a tree-size problem.

**Warning signs:**
- Runtime scales sharply with compiled depth.
- Most time is spent evaluating inactive or bloated branches.
- A smaller equivalent identity would fit within the same training budget.

**Prevention:** Report compile depth and node count before training; reject or defer oversized trees; profile only after correctness gates pass; do not add Rust/CUDA just to support an unbounded compiler expansion.

**Phase mapping:** Phase 1 depth gate; Phase 2 embedding; later scaling only if needed.

**Confidence:** MEDIUM-HIGH. Sources: `sources/paper.pdf` Table 4, `sources/NORTH_STAR.md`.

## Minor Pitfalls

### Pitfall 17: AST Schema Versioning Does Not Distinguish Compiled Trees

**What goes wrong:** Hand-authored exact ASTs, compiler outputs, and trained snapped ASTs all serialize identically, losing provenance.

**Prevention:** Keep one AST node schema if desired, but add provenance metadata: `source: hand_identity | compiler | trained_snap`, compiler version, source expression, rule sequence, and recovery mode.

**Phase mapping:** Phase 1 and Phase 4.

**Confidence:** MEDIUM. Sources: current `expression.py`.

### Pitfall 18: Equality Checks Depend on String Forms

**What goes wrong:** Tests compare `str(sympy_expr)` or JSON text rather than structural ASTs and numeric equivalence.

**Prevention:** Use structural AST comparison for embedding round-trips and numeric verification for mathematical equivalence. Reserve string checks for display smoke tests only.

**Phase mapping:** Phase 2 and Phase 5.

**Confidence:** MEDIUM-HIGH. Sources: current tests and `cleanup.py`.

### Pitfall 19: Planck Stretch Work Pulls Scope Away From Beer-Lambert and Michaelis-Menten

**What goes wrong:** Normalized Planck becomes the focus before simpler promoted demos are reliable.

**Prevention:** Phase 4 should require Beer-Lambert and Michaelis-Menten promotion gates first. Planck can report `compiled_depth_exceeded`, `warm_start_failed`, or `verified_showcase` honestly.

**Phase mapping:** Phase 4.

**Confidence:** HIGH. Sources: `.planning/PROJECT.md`, `sources/FOR_DEMO.md`.

### Pitfall 20: Tests Only Cover Successful Compilation

**What goes wrong:** Unsupported expressions, branch-sensitive failures, depth overflow, snap ambiguity, and demo overclaiming are untested.

**Prevention:** Add negative tests for unsupported SymPy nodes, arbitrary floats under pure-EML policy, depth-limit exceeded, invalid embedding depth, perturbed snap failure, and catalog-only demos.

**Phase mapping:** Phase 5, but negative tests should appear alongside each feature.

**Confidence:** HIGH. Sources: current test suite shape and v1.1 requirements.

## Phase-Specific Warnings

| Phase topic | Likely pitfall | Mitigation |
|-------------|----------------|------------|
| Compiler subset | Accepting more SymPy than the project can verify. | Whitelist nodes; fail unsupported forms early with reason codes. |
| Constants | Treating arbitrary floats as exact EML constants. | Choose pure, supplied, or rational constant policy and encode it in artifacts. |
| Rule corpus | Verifying rules against shared implementation bugs. | Compare compiled ASTs to independent ordinary-expression NumPy/mpmath evaluation. |
| Depth budget | Producing exact but unusable trees. | Report depth/node count and gate demo promotion on explicit ceilings. |
| Embedding | Warm-start path changes the compiled AST. | Immediate embed->snap round-trip tests before perturbation or training. |
| Perturbation | Calling low loss a return-to-solution. | Require post-snap verifier pass and same/equivalent AST classification. |
| Demo reporting | Catalog verification gets promoted to recovery. | Separate catalog, compiled seed, warm-start, trained snap, and public claim statuses. |
| Documentation | Warm starts look like blind discovery. | Add `recovery_mode` to manifests and public wording. |

## Implementation Gates

| Gate | Required evidence | Blocks |
|------|-------------------|--------|
| Compiler identity gate | Supported subset rules pass independent NumPy/mpmath checks with recorded assumptions. | Warm-start embedding. |
| Constant policy gate | Non-`1` constants are either compiled, supplied, or rejected with explicit metadata. | Beer-Lambert and Michaelis-Menten promotion. |
| Depth gate | Compiled demo trees fit configured depth and node-count ceilings. | Training demos. |
| Embedding gate | Compiled AST embeds into `SoftEMLTree` and immediate snap returns the same/equivalent AST. | Perturbation experiments. |
| Perturbation gate | Recovery rates are reported across seed batches, strengths, and noise scales using post-snap verification. | Warm-start claims. |
| Demo claim gate | Public report distinguishes catalog showcase, compiled seed, warm-start recovery, trained exact recovery, and failure. | Release notes and public demos. |

## Highest-Risk Roadmap Choices to Avoid

| Bad choice | Why it is dangerous | Better choice |
|------------|---------------------|---------------|
| Compile arbitrary SymPy expressions immediately. | Unsupported nodes and branch assumptions will fail late and ambiguously. | Start with a narrow whitelist and negative tests. |
| Insert float constants into exact EML ASTs silently. | It misrepresents the grammar and weakens recovery claims. | Declare pure/supplied/rational constant policy. |
| Promote catalog demos based on direct verification. | It bypasses the existing verifier-owned exact recovery contract. | Promote only after compile, embed/warm-start, train, snap, and verify. |
| Treat perturbation success as low training loss. | It does not prove exact return-to-solution. | Require post-snap verification and AST/equivalence classification. |
| Chase Planck before simpler demos pass. | The stretch target can consume roadmap time without validating the core v1.1 pipeline. | Gate Planck behind Beer-Lambert and Michaelis-Menten success. |

## Sources

- Local: `.planning/PROJECT.md` - v1.1 goal, active requirements, scope constraints, demo promotion targets.
- Local: `.planning/STATE.md` - current milestone state and completed v1 contract.
- Local: `src/eml_symbolic_regression/expression.py` - exact AST, `Const`, `Eml`, `SympyCandidate`, JSON metadata, candidate kinds.
- Local: `src/eml_symbolic_regression/master_tree.py` - current complete soft tree, slot choices, manual `force_exp` / `force_log`, snapping decisions.
- Local: `src/eml_symbolic_regression/optimize.py` - candidate generator, training manifest, post-snap loss but verifier separation.
- Local: `src/eml_symbolic_regression/verify.py` - verifier-owned statuses and exact-EML recovery contract.
- Local: `src/eml_symbolic_regression/datasets.py` and `src/eml_symbolic_regression/cli.py` - current catalog demos and CLI report shape.
- Local: `tests/*.py` - current tests for semantics, master tree, optimizer, cleanup, verifier, demos, and Planck showcase guard.
- Local: `sources/paper.pdf` - EML semantics, compiler caveats, depth/complexity table, warm-start behavior, depth limits.
- Local: `sources/NORTH_STAR.md` - hybrid pipeline, exact recovery definition, verifier requirement, numerical and symbolic pitfalls.
- Local: `sources/FOR_DEMO.md` - demo sequencing, normalized/dimensionless target guidance, Planck caution.
