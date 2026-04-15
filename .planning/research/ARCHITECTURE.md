# Architecture Patterns

**Domain:** Hybrid EML symbolic-regression engine  
**Project:** EML Symbolic Regression  
**Researched:** 2026-04-15  
**Overall confidence:** HIGH for paper-grounded component boundaries and build order; MEDIUM for scaling choices beyond shallow demos.

## Recommended Architecture

Build the system as a staged pipeline, not as one monolithic model class:

```text
demo spec / dataset config
  -> sampler and normalization
  -> complete depth-bounded EML master-tree spec
  -> PyTorch differentiable model over categorical gate logits
  -> optimizer with restarts, annealing, entropy/size penalties, anomaly logs
  -> hardening and snapping
  -> exact EML AST
  -> local discrete cleanup and targeted symbolic rewrite
  -> verifier across training, held-out, extrapolation, and high-precision points
  -> formula artifacts, diagnostics, CLI/demo reports
```

The central boundary is this: **training may use stabilized numerical semantics; verification must use canonical EML semantics.** The paper explicitly reports overflow, NaNs, clamping, complex128 training, snapping to exact weights, and rapidly declining blind recovery at depth. The architecture should therefore make the soft differentiable search replaceable without weakening the exact post-snap artifact or verifier.

## Component Boundaries

| Component | Responsibility | Must Not Own | Communicates With |
|-----------|----------------|--------------|-------------------|
| EML semantics kernel | Defines `eml(x, y) = exp(x) - log(y)`, complex principal-branch policy, training-vs-verification evaluation modes, anomaly counters | Optimizer policy, dataset generation, symbolic simplification | Differentiable model, exact evaluator, verifier |
| Dataset and sampler layer | Builds train, held-out, extrapolation, and edge-case points; handles normalization and dimensionless demo transforms | Model parameters, snapping, formula simplification | Demo specs, optimizer, verifier |
| Master-tree spec | Describes a complete depth-bounded binary EML scaffold and legal input choices per slot | PyTorch tensors, optimizer state, learned probabilities | Differentiable model, serializer, tests |
| Differentiable EML model | Owns PyTorch logits, softmax/temperature behavior, batched complex128 forward pass, node-level diagnostics | Exact AST ownership, high-precision proof, CLI formatting | Semantics kernel, optimizer, snapper |
| Optimization engine | Runs restarts, schedules, loss terms, entropy/size regularization, early stopping, checkpointing | EML math definitions, AST rewrites | Differentiable model, dataset layer, run recorder |
| Hardener/snapper | Converts soft gates to deterministic one-hot choices, prunes dead subtrees, emits exact AST | Further optimization, broad symbolic simplification | Differentiable model, AST serializer, cleanup |
| Exact EML AST | Stores snapped formulas as immutable expression trees with constants, variables, and `eml` nodes | Training logits, optimizer schedules | Serializer, exact evaluator, SymPy exporter, cleanup |
| Serialization layer | Writes deterministic JSON artifacts for snapped trees, run manifests, verification results, and optional PyTorch checkpoints | Mathematical interpretation beyond schema validation | CLI, demos, verifier, tests |
| Local cleanup and discrete search | Performs bounded subtree rewrites, redundancy pruning, neighborhood search, size reduction | Declaring recovery without verifier approval | Exact AST, semantics kernel, verifier |
| SymPy/export layer | Converts exact EML AST to ordinary expressions and applies targeted rewrites for readability | Acting as the only equivalence oracle | Cleanup, CLI/demo reports, tests |
| Verifier | Enforces acceptance criteria on train, held-out, extrapolation, edge, and mpmath high-precision points | Training or modifying candidates | Dataset layer, exact evaluator, SymPy/export layer, CLI |
| Demo and CLI orchestration | Provides reproducible commands, configs, plots, reports, and canned examples from `sources/FOR_DEMO.md` | Core math semantics | All public pipeline components |

## Data Flow

1. A `DemoSpec` or user config defines variables, target generator, sampling ranges, normalization, tree depth, optimizer budget, and acceptance thresholds.
2. The sampler produces four point sets: training, held-out interpolation, extrapolation, and targeted edge/branch/singularity probes.
3. The master-tree builder creates a static complete binary EML scaffold for the requested depth. For univariate v1, each slot chooses among `{1, x, previous_subtree}` where legal. For multivariate later phases, slots choose among `{1, x1, ..., xd, previous_subtrees}`.
4. The differentiable model attaches logits to those slot choices and evaluates weighted mixtures through the training semantics kernel.
5. The optimizer updates logits using fit loss plus discreteness, size, and numerical-stability penalties. It records per-node NaN, Inf, clamp, branch, and magnitude diagnostics.
6. The snapper freezes each categorical slot to argmax one-hot choices, removes unreachable branches, and emits an exact EML AST.
7. Cleanup rewrites only the exact AST, never the training model. It can propose smaller neighbors, but each accepted rewrite must be verifier-approved.
8. The verifier evaluates the candidate with canonical semantics and high-precision backends, then writes a pass/fail result with errors, domains, seeds, and artifact hashes.
9. CLI/demo reports present the final formula, exact EML JSON, optional SymPy form, diagnostics, and plots.

Data flow should be one-way through the default pipeline. Feedback loops are allowed only at explicit boundaries:

```text
failed verification -> new restart / lower depth / adjusted sampler
bloated verified AST -> local cleanup -> verifier
solved shallow AST -> warm-start deeper master tree
```

## Build Order

### Phase 0: Semantics and Exact Tree Foundation

Build this first because every other module depends on it.

Deliver:
- `eml` semantics kernel with explicit training and verification modes.
- Exact EML AST types for `Const(1)`, `Var(name)`, and `Eml(left, right)`.
- Batched evaluator tests for known identities from the paper: `exp(x) = eml(x, 1)` and `ln(x) = eml(1, eml(eml(1, x), 1))`.
- Deterministic JSON serialization for exact ASTs.

Verification boundary:
- Unit tests compare PyTorch/NumPy-style evaluation and mpmath for shallow expressions on safe domains.
- Branch behavior and zero/Inf handling are documented in test names and schema metadata.

### Phase 1: Complete Master Trees and Soft Evaluation

Build the differentiable scaffold only after exact semantics exist.

Deliver:
- Complete depth-2 and depth-3 univariate master trees.
- Slot-choice representation matching the paper's `{1, x, f}` construction.
- PyTorch complex128 forward pass with node diagnostics.
- Shape/property tests proving the depth scaffold has the expected slots and legal choices.

Verification boundary:
- Master-tree tests do not require successful optimization. They only prove that hand-set one-hot gates reproduce known formulas.

### Phase 2: Optimizer, Restarts, and Hardening

This phase turns the scaffold into a search system.

Deliver:
- Adam/AdamW optimization loop.
- Temperature or entropy scheduling.
- Size/stability penalties as separately logged loss terms.
- Multi-seed restarts and run manifests.
- Hardening/snapper from soft gates to exact AST.

Verification boundary:
- Recovery is not accepted on training loss. A run is only a candidate until the snapped AST is evaluated by the verifier.

### Phase 3: Verifier and Acceptance Contract

Build this before demo polish because demos must not report false recoveries.

Deliver:
- Held-out, extrapolation, and high-precision mpmath checks.
- Backend differential checks for snapped ASTs.
- Acceptance result schema with pass/fail, tolerances, max errors, and domains.
- CLI-visible reason codes: `fit_failed`, `snap_unstable`, `heldout_failed`, `extrapolation_failed`, `mpmath_failed`, `simpler_neighbor_found`, `verified`.

Verification boundary:
- Only this component can label a formula as recovered.

### Phase 4: Local Cleanup and Symbolic Export

Once verified candidates exist, make them shorter and readable.

Deliver:
- Dead-branch pruning and duplicate subtree cleanup.
- Bounded local neighborhood search over exact EML ASTs.
- SymPy exporter and targeted rewrite passes.
- Size comparison before/after cleanup.

Verification boundary:
- Every cleanup rewrite returns to the verifier. Generic `simplify()` output is presentation only unless numerically and symbolically checked.

### Phase 5: Demo Harness

Only after the recovery contract is reliable, build the public demos.

Deliver:
- Reproducible demo configs from `sources/FOR_DEMO.md`.
- Highest-success sequence: Beer-Lambert/radioactive decay, Michaelis-Menten, logistic growth, Shockley diode, damped oscillator, normalized Planck spectrum.
- Public-facing trio when stable: Michaelis-Menten, damped harmonic oscillator, normalized Planck spectrum.
- Plots, JSON artifacts, snapped formulas, verification reports, and seed/runtime summaries.

Verification boundary:
- Demo snapshots should include both successful and failed restart counts. Do not hide seed sensitivity.

### Phase 6: Multivariate and Semi-Parametric Extensions

Defer until univariate recovery is routine.

Deliver:
- Slot choices over `{1, x1, ..., xd, previous_subtrees}`.
- Small multivariate demos before singular/risky physics cases.
- Optional coefficient-fitting layer around a snapped symbolic scaffold.

Verification boundary:
- Multivariate demos need domain coverage tests, not just random held-out points.

## Serialization Formats

Use separate formats for exact formulas, trainable checkpoints, run manifests, and verification reports. Do not overload PyTorch checkpoints as symbolic artifacts.

### Exact EML AST JSON

Recommended schema shape:

```json
{
  "schema": "eml.ast.v1",
  "semantics": {
    "operator": "exp(x)-log(y)",
    "log_branch": "principal",
    "constant_basis": ["1"],
    "verification_mode": "canonical"
  },
  "variables": ["x"],
  "root": {
    "kind": "eml",
    "left": { "kind": "const", "value": "1" },
    "right": {
      "kind": "eml",
      "left": {
        "kind": "eml",
        "left": { "kind": "const", "value": "1" },
        "right": { "kind": "var", "name": "x" }
      },
      "right": { "kind": "const", "value": "1" }
    }
  },
  "metadata": {
    "depth": 3,
    "node_count": 5,
    "source": "snapper",
    "created_by": "eml-symbolic-regression"
  }
}
```

Rules:
- Children are ordered because `eml` is non-commutative.
- Constants are strings to avoid float drift.
- Schema version is mandatory.
- Semantics metadata is mandatory because branch and verification policy affect meaning.
- The AST artifact is immutable after verification; cleanup emits a new artifact.

### Trainable Checkpoint

Store PyTorch model state separately:

```text
schema: eml.checkpoint.v1
depth
variables
slot_catalog
logits_state_dict
optimizer_state_dict
temperature
seed
training_semantics
run_id
```

This is a resumable search artifact, not a recovered formula.

### Run Manifest

Store reproducibility metadata:

```text
schema: eml.run.v1
demo_or_dataset
sampling_ranges
normalization
depth
optimizer_config
restart_count
seeds
git_commit_if_available
package_versions
hardware_summary
artifact_paths
```

### Verification Report

Store acceptance data:

```text
schema: eml.verify.v1
candidate_ast_hash
status
thresholds
train_error
heldout_error
extrapolation_error
mpmath_error
edge_case_results
backend_results
failure_reason
verified_at
```

## Verification Boundaries

The project should enforce these boundaries in code and tests:

| Boundary | Allowed Before Boundary | Required After Boundary |
|----------|-------------------------|-------------------------|
| Training evaluator -> snapper | Clamps, soft mixtures, entropy penalties, unstable candidates | One-hot slot decisions and exact AST |
| Snapper -> verifier | Low training loss and plausible formula | Held-out, extrapolation, high-precision, and backend checks |
| Cleanup -> verifier | Smaller or prettier AST candidate | Re-verified formula with no worse acceptance result |
| SymPy exporter -> report | Readable ordinary expression | Exact EML AST remains the source of truth |
| Demo harness -> public claim | Pretty plots and fit curves | Verification report must say `verified` |

Operational definition of "recovered":
- The candidate is snapped to a discrete AST.
- The AST passes train and held-out tolerances.
- It extrapolates on domain-appropriate points.
- It passes high-precision mpmath checks.
- It survives branch/singularity probes relevant to the sampled domain.
- Cleanup cannot find a strictly simpler verified neighbor within the configured local budget.

## Demos and Tests Plug-In Points

### Demo Specs

Each demo should be a config plus generator, not hand-coded logic inside the CLI:

```text
name
variables
target_expression_or_generator
domain_train
domain_heldout
domain_extrapolation
normalization
noise_model
depth_budget
optimizer_budget
acceptance_thresholds
plot_spec
```

Initial demos should follow the feasibility ladder from `sources/FOR_DEMO.md`:

1. Beer-Lambert or radioactive decay as smoke tests.
2. Michaelis-Menten as the first real mechanistic law.
3. Logistic growth as a nonlinear saturating law.
4. Shockley diode because exponential-minus-constant structure is EML-friendly.
5. Damped harmonic oscillator after trig/phase handling is stable.
6. Normalized Planck spectrum as the flagship once depth and warm starts are reliable.

Avoid early demos involving special functions, piecewise laws, chaotic systems, raw SI constants, or singular multivariate laws. They are bad architecture validators because failure is ambiguous.

### Test Layers

| Test Layer | What It Proves | Examples |
|------------|----------------|----------|
| Semantics unit tests | EML identities and branch policy are stable | `exp(x)`, `ln(x)`, identity, negation, reciprocal where domains are safe |
| AST serialization tests | Formula artifacts are deterministic and round-trip | JSON hash stability, ordered children, schema migration guards |
| Master-tree property tests | Complete scaffold exposes legal choices and hand-set gates work | Depth-2/3 formulas, slot counts, no illegal previous-subtree reference |
| Optimization smoke tests | Search loop can recover shallow formulas in controlled settings | `exp(x)`, `ln(x)`, Beer-Lambert |
| Snapper tests | Soft categorical gates become exact ASTs | argmax ties handled deterministically, dead branches pruned |
| Verifier tests | False recovery is rejected | train-only fit fails extrapolation or mpmath checks |
| Cleanup tests | Rewrites preserve accepted behavior | redundant subtree removal followed by verifier pass |
| Demo regression tests | Public examples remain reproducible | fixed seed budgets and stored pass/fail expectations |

## Patterns to Follow

### Pattern 1: Semantics Modes Are Explicit

**What:** Every evaluator call takes an explicit mode: `training` or `canonical`.

**When:** Always. The mode should appear in logs and serialized artifacts.

**Example:**

```python
value, stats = evaluator.eval(ast_or_model, points, mode="canonical")
```

This prevents stabilized training clamps from silently becoming part of the claimed formula.

### Pattern 2: AST Is the Contract Between Search and Verification

**What:** The optimizer outputs logits; the snapper outputs an AST; the verifier accepts only ASTs.

**When:** At every recovery boundary.

**Example:**

```text
logits checkpoint -> snap() -> eml.ast.v1 -> verify() -> eml.verify.v1
```

This keeps "low loss" and "symbolically recovered" as separate states.

### Pattern 3: Warm-Start Through AST Embedding

**What:** A verified shallow AST can be embedded into a deeper master tree by fixing or biasing matching gates, then unfreezing new capacity gradually.

**When:** Depth 4+ searches and difficult demos.

**Why:** The paper reports that perturbed correct trees converge reliably even when blind random recovery fails at deeper depths.

### Pattern 4: Cleanup Is Bounded and Verifier-Gated

**What:** Local discrete search proposes candidate ASTs within a fixed edit/size budget.

**When:** After snapping and before final report.

**Why:** EML compiler forms can be correct but bloated; gradient search can also recover non-minimal structures.

## Anti-Patterns to Avoid

### Anti-Pattern 1: Pure Gradient Engine

**What:** Stop at soft weights or report the best training loss.

**Why bad:** The project value is exact, human-readable formula recovery, not just curve fitting.

**Instead:** Always snap to an exact AST and verify.

### Anti-Pattern 2: Hidden Epsilons in Verification

**What:** Reuse training clamps, epsilons, or branch fixes in the final verifier without declaring them.

**Why bad:** The formula may only be true under the stabilizer, not under EML semantics.

**Instead:** Keep training and canonical evaluators separate, and serialize the semantics policy.

### Anti-Pattern 3: SymPy as an Equivalence Oracle

**What:** Treat a successful generic simplification as proof.

**Why bad:** Generic simplification is heuristic and branch-sensitive.

**Instead:** Use targeted rewrites for presentation and verifier-backed acceptance for claims.

### Anti-Pattern 4: Flagship Demo First

**What:** Start with normalized Planck or damped oscillator before shallow recovery is reliable.

**Why bad:** Failure will not identify whether the problem is semantics, search, snapping, or verification.

**Instead:** Build the feasibility ladder and promote demos only after lower rungs pass.

## Scalability Considerations

| Concern | At MVP / 100 runs | At 10K runs | At 1M candidate evaluations |
|---------|-------------------|-------------|-----------------------------|
| Training search | Python + PyTorch complex128, few depths, local run manifests | Batched restarts, torch.compile where stable, checkpoint pruning | Distributed restart scheduler, hardware-aware budgets |
| Exact AST verification | Python evaluator plus mpmath on selected points | Rust/PyO3 evaluator for batches, mpmath only for finalists | Rust/CUDA candidate scoring, sampled high-precision finalist verification |
| Cleanup search | Small bounded neighborhood in Python | Rust-backed deduplication and scoring | Dedicated candidate index, structural hashes, batched signatures |
| Demo reproducibility | Fixed seeds and stored configs | Artifact registry and result comparison | Database-backed experiment tracking |
| Numerical stability | Per-node counters and early stopping | Aggregate anomaly analytics across runs | Automated curriculum/restart policies from failure modes |

## Roadmap Implications

The roadmap should order phases by verification dependency, not by demo appeal:

1. **Semantics and serialization first** because all downstream artifacts depend on exact EML meaning.
2. **Master-tree construction second** because it can be tested with hand-set gates before optimization exists.
3. **Optimization and snapping third** because recovery candidates must cross from soft tensors into exact ASTs.
4. **Verifier fourth and before public demos** because "recovered" is a verifier status, not an optimizer status.
5. **Cleanup and symbolic export fifth** because readability should improve verified formulas without becoming the source of truth.
6. **Demos sixth** because they should exercise a proven pipeline and expose seed sensitivity honestly.
7. **Multivariate/scaling later** because depth, branch behavior, and numerical instability are already hard in univariate v1.

## Sources

- `.planning/PROJECT.md` - project scope, active requirements, constraints, and out-of-scope boundaries.
- `sources/NORTH_STAR.md` - hybrid pipeline, module recommendations, build phases, risks, and MVP guidance.
- `sources/FOR_DEMO.md` - demo sequence, high-probability examples, flagship examples, and anti-demo guidance.
- `sources/paper.pdf` - EML definition, grammar, master-tree construction, complex arithmetic requirements, proof-of-concept recovery, PyTorch complex128 experiments, and reported depth-scaling limits.
- `AGENTS.md` - repository instruction that this implementation is grounded in the paper, north-star blueprint, and demo list.
