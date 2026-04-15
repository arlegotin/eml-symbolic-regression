# Hybrid Symbolic Regression over Complete EML Trees
*A 2026 implementation blueprint, grounded in the paper **All elementary functions from a single operator***  

## What this document is

This document explains idea #4 from the earlier list in a self-contained way: **a hybrid symbolic-regression engine that searches over complete EML trees** rather than over a hand-picked heterogeneous menu of operators.

It is “hybrid” because the practical implementation should combine:

1. **continuous optimization** over a differentiable, parameterized EML master tree,
2. **hardening / discretization** of the soft choices into an exact tree,
3. **symbolic cleanup and local discrete search** to simplify and verify the result.

The core conceptual move comes directly from the paper: because `eml(x, y) = exp(x) - ln(y)` together with the constant `1` generates the paper’s scientific-calculator basis, every elementary expression can be represented as a uniform binary tree with grammar

```text
S -> 1 | eml(S, S)
```

That regularity is what makes a “complete” depth-bounded master architecture possible. [Paper, pp. 1-2, 11-15]

---

## Reading guide

Throughout this document:

- **Paper-grounded** means the point is directly supported by the uploaded paper or its repo.
- **Recommended implementation** means it is a practical 2026 design choice that follows from the paper, but is not claimed as a theorem by the paper.

---

## 1. Executive summary

### One-sentence version

Instead of doing symbolic regression by choosing among many operators such as `+`, `-`, `*`, `/`, `sin`, `cos`, `exp`, and `log`, build one **depth-bounded trainable EML tree** that is complete for the paper’s elementary-function class, optimize it on data, then snap and simplify it into an exact symbolic formula. [Paper, pp. 2, 12-15]

### Why this matters

Ordinary symbolic regression has a hidden structural problem: you must decide the operator vocabulary in advance. If the vocabulary is too small, the true law may be unreachable. If it is too large, search becomes brittle and combinatorial. The paper’s main conceptual contribution is that EML turns the search space into **one regular binary-tree family**. That removes the “did I choose the right operator set?” problem for the paper’s target class. [Paper, pp. 2, 12-15]

### The key practical insight

The paper’s experiments show that this is **not yet a black-box universal equation-discovery machine**. Blind recovery from random initialization works very well at depth 2, only about 25% at depths 3-4, below 1% at depth 5, and not at depth 6 in the reported trials. But when the correct tree is perturbed, optimization reliably returns to it, even at depths 5-6. That means the representation is viable and the right basins exist; the hard problem is **finding** those basins from scratch. [Paper, p. 15]

So the strongest 2026 implementation is not “pure gradient descent.” It is a **hybrid engine**:
soft differentiable search -> hardening -> symbolic snapping -> local discrete simplification -> numerical / symbolic verification.

---

## 2. What the paper actually gives you

### 2.1 The mathematical primitive

The paper defines

```text
eml(x, y) = exp(x) - ln(y)
```

and shows constructively that `eml` together with the constant `1` generates the paper’s concrete scientific-calculator basis: arithmetic, exponentials, logarithms, radicals, trigonometric and hyperbolic functions, and constants such as `e`, `pi`, and `i`. [Paper, pp. 1, 5, 8-10]

### 2.2 The representation

Because every compiled formula becomes a binary tree of identical nodes, EML expressions have the trivial grammar

```text
S -> 1 | eml(S, S)
```

For functions, input variables such as `x`, `y`, `z` are added as terminal symbols. The paper emphasizes that this representation is uniform and regular in a way ordinary mixed-operator ASTs are not. [Paper, pp. 2, 11-12]

### 2.3 Why symbolic regression becomes special here

The paper’s central symbolic-regression claim is this:

> Because EML is a single sufficient operator, you can build a “master formula” in EML form that contains **all formulas up to a chosen tree depth**. [Paper, pp. 12-15]

This is the real reason idea #4 is important. A search over complete EML trees is not just another symbolic-regression heuristic. It is a search over a **complete depth-bounded family** for the paper’s elementary basis.

### 2.4 The exact training setup described by the paper

For the univariate case, each input to an `eml` node can be one of three things:

- the constant `1`,
- the input variable `x`,
- the output `f` of a previous subtree.

The paper represents a generic input slot by

```text
alpha_i + beta_i x + gamma_i f
```

so that the three discrete cases are recovered by setting the coefficients to one-hot choices:

- `1`  -> `alpha=1, beta=0, gamma=0`
- `x`  -> `alpha=0, beta=1, gamma=0`
- `f`  -> `alpha=0, beta=0, gamma=1`

At the leaves there is no previous subtree output, so there are no `gamma` parameters there. [Paper, pp. 13-14]

The paper gives an explicit level-2 master formula:

```text
F(x) = eml[
  alpha1 + beta1 x + gamma1 eml(alpha3 + beta3 x, alpha4 + beta4 x),
  alpha2 + beta2 x + gamma2 eml(alpha5 + beta5 x, alpha6 + beta6 x)
]
```

and states that the level-`n` univariate master formula has

```text
P(n) = 5 * 2^n - 6
```

parameters. For level 2 that gives 14 parameters, matching the formula above. [Paper, p. 14]

### 2.5 The paper’s proof-of-concept results

The paper reports:

- exact recovery of `ln x` with a complete level-3 tree,
- reduction from 34 to 20 free parameters via simplex reparameterization,
- recovery by a black-box Mathematica optimizer at numerical-precision error,
- snapping of learned weights to exact 0/1 vertices,
- nearly perfect extrapolation beyond the training range in the `ln x` example. [Paper, p. 14]

Then the paper describes a PyTorch implementation for more modern ML-style experiments:

- complex dtype: `torch.complex128`,
- multi-stage optimization with Adam,
- hardening phase toward binary weights,
- final clamping to exact symbolic values,
- success rates that degrade rapidly with depth from random initialization,
- but excellent return-to-solution behavior from perturbed true weights. [Paper, pp. 14-15]

Those results are the empirical basis for the “hybrid, not pure” implementation strategy recommended here.

---

## 3. The core idea, fully described

## 3.1 What problem this engine solves

Input:

- a dataset `(x, y)` or `(x_1, ..., x_d, y)`,
- usually noiseless or moderately noisy scientific data,
- with a prior belief that the hidden law is a relatively small elementary expression.

Output:

- a symbolic formula,
- ideally exact after snapping,
- otherwise a compact approximate symbolic scaffold,
- plus verification diagnostics.

The point is not just prediction. The point is **equation discovery**.

### Best-fit use cases

This approach is most natural when you want one of the following:

- rediscover a known law from data,
- identify a closed-form constitutive relation,
- recover a human-readable correction term inside a scientific model,
- compress a black-box function into an interpretable symbolic expression,
- search for candidate formulas before doing deeper theory work.

### Bad fit use cases

This is a poor first choice when:

- you only care about predictive accuracy,
- the target law is probably non-elementary,
- the data are too noisy or too high-dimensional,
- the target depends on complex control flow or discrete events,
- a standard neural network or tree model is enough.

---

## 3.2 Why EML changes symbolic regression structurally

In a normal symbolic-regression system, the grammar might look roughly like this:

```text
Expr -> constant | variable | Expr + Expr | Expr * Expr | exp(Expr) | log(Expr) | sin(Expr) | ...
```

This creates three major problems:

1. **operator-set choice**: if you omit a needed operator, the target may be unreachable;
2. **heterogeneous search**: different operators have different arities, symmetries, costs, and simplification rules;
3. **irregular architecture**: it is hard to turn the whole search space into one clean trainable object.

EML removes much of that structural mess. The grammar is regular:

```text
S -> 1 | eml(S, S)
```

so a depth-bounded full binary tree is a single architecture family that is complete for the paper’s target basis. [Paper, pp. 2, 11-15]

That is the conceptual shift. The search becomes:

> “Find the right choices inside one universal tree family,”

not

> “Search across many incomparable operator families.”

---

## 3.3 What “complete by design” really means

**Paper-grounded.** The paper states that the EML master formula includes all possible formulas up to the given leaf count / tree depth. [Paper, pp. 12-14]

**Interpretation.** This does **not** mean it includes all mathematics. It means:

- for the paper’s concrete elementary-function basis,
- within a fixed depth budget,
- the master tree is a complete container.

That is a very strong property compared with ordinary symbolic regression.

**Practical consequence.** Your main approximation knob is no longer the operator vocabulary; it is the **depth budget** and the optimization method.

---

## 3.4 Why the implementation should be hybrid

The paper itself gives the reason:

- shallow exact recovery is feasible,
- deeper blind recovery becomes hard,
- but correct solutions have stable basins once you get near them. [Paper, p. 15]

That implies the best current design is:

1. **continuous search** to move toward a promising basin,
2. **discretization** to collapse soft choices into a concrete tree,
3. **symbolic / discrete postprocessing** to refine, shorten, and verify.

If you stop at step 1, you have a soft network, not a symbolic result.
If you start directly at step 3, the search space is too combinatorial.
The power is in the combination.

---

## 4. A practical 2026 architecture

This section is the implementation blueprint I would use now.

## 4.1 System overview

```text
data
  ->
sampling / normalization
  ->
differentiable EML master tree
  ->
complex-valued forward evaluator
  ->
loss + regularizers
  ->
optimizer / curriculum / restarts
  ->
hardening and snapping
  ->
local discrete simplifier / neighborhood search
  ->
cross-backend verifier
  ->
final formula + diagnostics
```

Each block matters. Omitting the later blocks usually leaves you with a fuzzy model, not a trustworthy formula.

---

## 4.2 Core modules

### Module A. Canonical EML semantics layer

This is the most important low-level module.

Responsibilities:

- define one canonical `eml(x, y)` implementation,
- use complex arithmetic internally,
- document branch behavior for `log`,
- define how infinities, signed zeros, and edge cases are handled,
- provide training mode and exact-evaluation mode.

**Why it is necessary.** Section 4.1 of the paper makes clear that EML compilation and evaluation depend on branch choices, extended reals, and backend behavior. Even though this document is about idea #4, the symbolic-regression engine cannot be reliable without a fixed semantics layer. [Paper, pp. 10-11]

**Recommended implementation.**

- Training evaluator: guarded complex forward pass with controlled clamping for stability.
- Verification evaluator: exact canonical semantics with no “helpful” hidden epsilons that change the math.

Do not blur these two roles.

---

### Module B. Differentiable master tree

This is the actual search model.

For univariate input, each input slot to a node chooses among `{1, x, previous_subtree}`.

A practical 2026 implementation should store **logits** for each choice and map them to probabilities via softmax. The node input becomes a weighted mixture of the available choices during the soft phase, then collapses to a one-hot choice during hardening.

For multivariate data, generalize the candidate set to something like:

```text
{1, x1, x2, ..., xd, previous_subtree_outputs}
```

The paper only writes out the univariate case, but explicitly says the construction extends to arbitrary numbers of inputs. [Paper, p. 12]

**Recommended implementation.** Represent the tree as a static module graph so it is easy to:

- batch over many data points,
- profile hotspots,
- compile later,
- export or serialize after training.

---

### Module C. Optimization engine

The first version should support:

- Adam or AdamW,
- multiple restarts,
- temperature annealing for softmax gates,
- entropy penalties to encourage near-discrete choices,
- optional sparsity penalty on active nodes,
- curriculum over tree depth.

**Why curriculum matters.** The paper shows blind recovery drops sharply with depth. That is a strong argument for depth curriculum and subtree reuse. [Paper, p. 15]

---

### Module D. Hardening and snapping

This module turns the soft model into an exact symbolic candidate.

Typical steps:

1. choose argmax category at each gate,
2. remove dead branches,
3. round surviving categorical weights to exact one-hot values,
4. optionally round small real-valued nuisance parameters if your architecture has them,
5. export the resulting exact EML tree.

The paper’s symbolic-regression examples rely on this snap-to-exact stage. [Paper, pp. 14-15]

---

### Module E. Local discrete cleanup

This is where the “hybrid” design becomes much better than the paper’s proof of concept alone.

Responsibilities:

- prune redundant identity-like subtrees,
- collapse repeated patterns,
- search a small neighborhood of alternative equivalent trees,
- hand off to an EML superoptimizer if available,
- optionally translate to ordinary mathematical notation and simplify there too.

This module is justified by two facts:

1. the paper’s compiled EML expressions are often not shortest, and
2. gradient training may reach a correct but bloated structure. [Paper, p. 13]

---

### Module F. Verifier

A formula-discovery engine without a verifier is not ready.

Responsibilities:

- re-evaluate the final formula on fresh points,
- compare against training backend and high-precision oracle,
- test edge cases near branch cuts and singularities,
- report whether the formula is stable across backends.

This is where idea #4 depends on idea #6 from the earlier list.

---

## 4.3 Loss design

The paper focuses on fitting and exact snapping, not on a full production loss design. The practical 2026 objective should be:

```text
L = fit_loss
  + lambda_entropy * gate_entropy
  + lambda_size * expected_tree_size
  + lambda_stability * numerical_penalty
```

Where:

- `fit_loss` is typically MSE over sampled data,
- `gate_entropy` pushes softmax choices toward one-hot decisions,
- `expected_tree_size` discourages unnecessarily complex trees,
- `numerical_penalty` discourages unstable intermediate values.

### Recommended implementation details

- Use separate logging for data fit and symbolic discreteness.
- Track the max absolute real part entering `exp`.
- Track NaN/Inf incidence per node.
- Add penalties before those pathologies dominate gradients.

Do not wait until the model fully explodes.

---

## 4.4 Numerical stabilization

This is the hardest engineering part.

### Paper-grounded issues

The paper explicitly reports:

- overflow from multiply composed exponentials,
- NaNs from the chosen complex arithmetic implementation,
- the need to clamp arguments and values for `exp(x)`,
- the need for careful handling of real and imaginary parts without breaking autograd. [Paper, p. 15]

### Recommended implementation

1. **Default to complex128.**  
   The paper uses `torch.complex128`, and for this use case that is the correct default because branch-sensitive symbolic recovery is much less forgiving than ordinary deep learning. [Paper, p. 15]

2. **Clamp only in training mode.**  
   Clamp the real part going into `exp` and perhaps the magnitude of selected intermediates during training. Keep verification mode mathematically faithful.

3. **Use anomaly counters.**  
   Log per-node counts for NaN, Inf, overflow clamps, and branch-cut encounters.

4. **Separate optimization from proof.**  
   It is acceptable for the training evaluator to be stabilized, but the post-snap formula must be re-run with canonical semantics.

5. **Build a fallback real/imag representation.**  
   PyTorch’s complex tensors are useful, but the current docs still label complex tensors as beta. Keep a fallback implementation that stores real and imaginary parts explicitly if you hit backend issues. [PyTorch Complex Numbers]

---

## 4.5 Search strategy that is most likely to work now

This is the key practical section.

### Recommended 4-stage search

#### Stage 1. Shallow exact recovery
Start with depths 2-3 and noiseless or low-noise benchmarks.

Goal:
- verify the implementation,
- reproduce the paper’s qualitative behavior,
- validate snapping and verification.

#### Stage 2. Curriculum growth
Grow from a solved shallow tree to a deeper tree by:

- embedding the shallow solution inside a deeper scaffold,
- unfreezing only a few new gates at a time,
- using subtree reuse.

This directly exploits the paper’s observation that solutions are stable when initialized near the correct basin. [Paper, p. 15]

#### Stage 3. Hardening
Anneal temperature or increase entropy penalty until gates become nearly one-hot, then snap.

#### Stage 4. Discrete local search
After snapping, run a local neighborhood search:
- subtree substitutions,
- deletions of inert branches,
- known equivalence rewrites,
- shortest-form search in a bounded neighborhood.

This is where you turn a “correct enough” tree into a good formula.

---

## 4.6 What exact recovery should mean operationally

For this engine, “exact recovery” should not mean “training loss is tiny.”

It should mean all of the following:

1. after snapping, the formula is discrete and human-readable;
2. it matches the target on held-out points;
3. it extrapolates on sensible out-of-range tests;
4. it remains consistent under higher precision;
5. it survives cross-backend checking;
6. it is not replaceable by a strictly simpler equivalent candidate found nearby.

Only then should you call it recovered.

---

## 5. What the paper’s experiments imply for product scope

This section is important because it prevents overselling.

### What is realistic now

Based on the paper, a serious 2026 engine should aim first for:

- exact recovery of shallow formulas,
- strong performance when warm-started,
- multistage search with strong priors,
- interpretable symbolic submodels inside larger pipelines.

### What is not realistic to promise yet

Do **not** promise:

- blind recovery of arbitrary depth-6 formulas,
- robust operation on highly noisy real-world scientific datasets without priors,
- shortest-form symbolic output from gradient descent alone,
- backend-independent semantics without a dedicated verification layer.

That would go beyond the paper.

---

## 6. Who would use this

### Primary users

1. **Symbolic-regression researchers**  
   They would use it as a new complete grammar and as a benchmarkable research platform.

2. **Scientific-ML teams**  
   They would use it to recover interpretable submodels from data or to place symbolic blocks inside larger models.

3. **Physicists, chemists, and engineers doing equation discovery**  
   They would use it when they suspect the hidden law is compact and elementary.

4. **Math-software/tooling developers**  
   They would use it as part of a compiler, simplifier, or formula-discovery system.

### Secondary users

- educators explaining neuro-symbolic search,
- formal-methods researchers using it as a structured benchmark,
- teams compressing black-box models into symbolic surrogates.

### Users who probably should not start here

- generic tabular-ML teams,
- recommender-system teams,
- pure forecasting teams that do not need symbolic outputs.

---

## 7. Recommended 2026 technology stack

This section focuses on what is most effective **right now**, not on theoretical purity.

## 7.1 The stack I would actually choose

### Primary research and training layer: Python + PyTorch

**Recommendation:** use **Python** as the orchestration language and **PyTorch** as the primary differentiable runtime.

**Why this is the best first choice now**

- The paper’s ML implementation is already in PyTorch and explicitly uses `torch.complex128`. [Paper, p. 15]
- The public EML toolkit repo includes `EmL_training` for PyTorch artifacts, `EmL_compiler`, `EmL_verification`, and CUDA recognizer tools, so the ecosystem around the paper already points in this direction. [EML toolkit repo]
- Current stable PyTorch docs expose native complex tensors, `torch.compile` for speedups, and `torch.export` for full-graph capture and deployment artifacts. [PyTorch Complex Numbers; PyTorch torch.compile; PyTorch torch.export]

**Practical recommendation:**
- use Python 3.12 or 3.13 for the first serious build if you want the safest compatibility path,
- use the current stable PyTorch branch,
- default to `complex128`,
- treat `complex64` only as an optional speed mode.

### Why not start with JAX or pure C++?

- JAX is viable in principle, but the paper and current repo are PyTorch-centered.
- Pure C++/CUDA is too slow for research iteration at the beginning.
- The main bottlenecks early on are representation, stabilization, snapping, and verification - not just kernel speed.

So the fastest path to a working engine is still Python + PyTorch.

---

## 7.2 Performance and verification layer: Rust

**Recommendation:** implement performance-critical symbolic and discrete components in **Rust**.

This includes:

- bounded exhaustive search,
- local discrete cleanup,
- candidate deduplication,
- exact-tree serialization,
- fast numeric verification,
- batch evaluation of many snapped formulas.

**Why Rust is especially justified here**

The paper states that the `VerifyBaseSet` reimplementation in Rust is roughly three orders of magnitude faster than the original Mathematica version, and the toolkit repo includes verification and recognizer components alongside PyTorch training code. [Paper, pp. 7-8; EML toolkit repo]

**Interoperability recommendation:**
- expose Rust kernels to Python with **PyO3**,
- build and distribute them with **maturin**, which the PyO3 docs explicitly recommend as the easiest path for Rust-based Python modules. [PyO3 / maturin]

This gives you the best of both worlds:
- Python for research velocity,
- Rust for correctness-critical speed.

---

## 7.3 GPU acceleration layer: CUDA only where profiling proves it matters

**Recommendation:** use the standard PyTorch GPU stack first; add custom CUDA only after profiling.

Why:

- the author’s reproducibility materials already include CUDA recognizer tools and a March 2026 validation run on CUDA 13.0 with an RTX 5080. [EML toolkit repo]
- NVIDIA’s current official CUDA Programming Guide is Release 13.2, so CUDA remains the right low-level target if you truly need custom kernels for batched candidate evaluation or search. [CUDA Programming Guide]

**What to accelerate first**
- batched EML evaluation of many candidate trees,
- local neighborhood search scoring,
- candidate deduplication via vectorized signatures.

**What not to custom-kernel too early**
- the full training loop,
- symbolic snapping logic,
- cross-backend verification.

Those are easier to get right in higher-level code first.

---

## 7.4 Symbolic and high-precision layer: SymPy + mpmath, optional Mathematica

**Recommendation:**
- use **SymPy** for algebraic rewriting, pretty-printing, and ordinary-expression output,
- use **mpmath** for arbitrary-precision complex verification,
- keep **Mathematica** optional as a high-confidence oracle if you already have access to it.

Why this combination makes sense:

- the paper uses Mathematica for discovery and symbolic verification,
- but an open implementation benefits from Python-native symbolic and precision tools,
- SymPy’s own docs warn that generic `simplify()` is not a stable algorithmic contract, so use targeted rewrite passes instead of relying on `simplify` as your core logic,
- mpmath gives arbitrary-precision real and complex arithmetic for verification. [SymPy Simplify; SymPy Rewriting; mpmath]

**Practical rule:**  
Use SymPy for representation and targeted rewrites, not as a magical equivalence oracle.

---

## 7.5 Model compilation and deployment: torch.compile for speed, torch.export for frozen artifacts

**Recommendation:**

- use **`torch.compile`** to speed up stable training/evaluation code once the model structure is settled,
- use **`torch.export`** only after the model is frozen enough to require full graph capture.

Why this split matters:

- `torch.compile` is flexible and can graph-break instead of failing hard,
- `torch.export` requires a fully traceable graph but produces a portable full-graph representation that can be saved and run outside normal Python runtime assumptions. [PyTorch torch.compile; PyTorch torch.export]

For this project, that means:

- during research: prefer `torch.compile`,
- during packaging / serving / reproducible artifacts: prefer `torch.export`.

---

## 7.6 A note on categorical hardening

The paper discusses using logits with softmax to model the discrete choices in the master tree, and cites Gumbel-Softmax. [Paper, p. 14]

**Recommended implementation:** do not build the system around a long-term dependency on `torch.nn.functional.gumbel_softmax`.

Why:
- the PyTorch docs say that function remains available but also note it is present for legacy reasons and may be removed from `nn.functional` in the future. [PyTorch gumbel_softmax]

A safer choice is:

- implement your own straight-through categorical hardening logic,
- or wrap the current helper behind your own abstraction.

That way your engine does not depend on one unstable API.

---

## 8. Recommended implementation plan

## 8.1 Phase 0 - Reproduce the paper qualitatively

Deliverables:

- canonical EML evaluator,
- level-2 and level-3 univariate master trees,
- exact recovery of a few paper-like targets such as `ln x`, `exp(x)`, and simple composed two-variable examples,
- snap-to-discrete stage,
- cross-checks against a high-precision oracle.

Success criterion:
- your system behaves like the paper at shallow depth.

---

## 8.2 Phase 1 - Make it reliable

Deliverables:

- restart strategy,
- entropy / sparsity regularizers,
- anomaly logging,
- held-out and extrapolation tests,
- backend verifier,
- JSON or protobuf AST format for snapped trees.

Success criterion:
- shallow recovery becomes routine rather than lucky.

---

## 8.3 Phase 2 - Make it hybrid for real

Deliverables:

- local discrete cleanup,
- bounded neighborhood search,
- translation from EML tree to ordinary expression,
- symbolic simplification passes,
- optional handoff to an EML shortest-form searcher.

Success criterion:
- formulas become shorter, cleaner, and more trustworthy after training.

---

## 8.4 Phase 3 - Scale to multivariate and semi-parametric models

Deliverables:

- multivariate gates over `{1, x1, ..., xd, previous_subtrees}`,
- optional coefficient-fitting layer after symbolic scaffold discovery,
- support for noise robustness and repeated measurements.

Success criterion:
- the engine handles realistic scientific datasets with modest dimensionality.

---

## 9. Risks and failure modes

## 9.1 Optimization failure from random initialization

This is the main one, and the paper already demonstrates it. [Paper, p. 15]

**Mitigations**
- curriculum over depth,
- subtree reuse,
- many restarts,
- warm starts from heuristic or discrete search,
- train shallow parts first.

---

## 9.2 Numerical explosion

Because `eml` contains `exp`, deep compositions explode easily. [Paper, p. 15]

**Mitigations**
- clamped training evaluator,
- complex128 default,
- magnitude logging,
- early stopping on anomaly spikes.

---

## 9.3 False symbolic confidence

A snapped formula can fit well but still be semantically wrong near singularities or branch cuts.

**Mitigations**
- high-precision verification,
- edge-case sweeps,
- backend differential testing,
- explicit branch-policy reporting.

---

## 9.4 Bloated but correct formulas

Gradient search may return a valid but needlessly large tree.

**Mitigations**
- size penalties,
- post-snap local search,
- handoff to an EML superoptimizer.

---

## 9.5 Overfitting to synthetic benchmarks

An engine can do well on EML-generated tasks yet fail on messy real data.

**Mitigations**
- noisy benchmarks,
- extrapolation tests,
- real scientific case studies,
- ablation against non-EML baselines.

---

## 10. Evaluation metrics that actually matter

Track at least these metrics:

1. **Exact recovery rate** after snapping and cleanup.
2. **Held-out numerical error**.
3. **Extrapolation error** outside the training range.
4. **Tree size** before and after cleanup.
5. **Search cost**: wall time, restarts, GPU hours.
6. **Stability metrics**: NaN/Inf counts, clamp counts.
7. **Verification pass rate** across backends / precisions.
8. **Seed sensitivity**.

If you only report fit loss, you are not measuring the main point of the system.

---

## 11. What a strong MVP should look like

A strong first release in 2026 would have these properties:

- univariate and small multivariate support,
- deterministic tree serialization,
- complex128 PyTorch evaluator,
- snap-to-discrete stage,
- SymPy translation and targeted rewriting,
- mpmath verification,
- Rust-accelerated local search / verification backend,
- optional GPU acceleration through standard PyTorch CUDA,
- reproducible experiment configs.

It does **not** need:
- a fancy web app,
- a huge GUI,
- support for every possible operator,
- full theorem-prover integration.

Those can come later.

---

## 12. Bottom-line recommendation

If you want to build idea #4 now, use this stack:

### Build now
- **Python** for orchestration and research iteration
- **PyTorch** for differentiable complex-valued training
- **complex128** as the default numeric mode
- **Rust** for fast discrete search and verification
- **PyO3 + maturin** to bind Rust into Python
- **SymPy + mpmath** for symbolic cleanup and high-precision checks
- **CUDA via normal PyTorch first**, custom kernels only after profiling

### Build later, if the MVP works
- custom CUDA kernels for massive batched candidate scoring
- distributed search
- coefficient-learning extensions
- more advanced discrete optimizers
- operator mining beyond EML

### Do not do first
- a pure C++ implementation,
- a pure gradient-only engine,
- a no-verification prototype,
- a benchmark-only system with no snapping or cleanup.

The best interpretation of the paper in 2026 is not “EML makes symbolic regression easy.”  
It is:

> **EML gives you a uniquely regular and complete symbolic search architecture, but turning that into a practical discovery system requires a hybrid pipeline that combines differentiable search, discrete snapping, simplification, and verification.**

That is the real implementation idea behind #4.

---

## 13. References and implementation pointers

### Paper and repo
- Andrzej Odrzywolek, **All elementary functions from a single operator** (2026).  
  Page references in this document refer to the uploaded PDF.
- EML toolkit repo: <https://github.com/VA00/SymbolicRegressionPackage/tree/master/EML_toolkit>

### PyTorch
- Complex numbers: <https://docs.pytorch.org/docs/stable/complex_numbers.html>
- `torch.compile`: <https://docs.pytorch.org/tutorials/intermediate/torch_compile_tutorial.html>
- `torch.export`: <https://docs.pytorch.org/docs/stable/user_guide/torch_compiler/export.html>
- `gumbel_softmax`: <https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.gumbel_softmax.html>

### Rust <-> Python
- PyO3 + maturin: <https://pyo3.rs/>

### GPU
- NVIDIA CUDA Programming Guide (Release 13.2): <https://docs.nvidia.com/cuda/cuda-programming-guide/>

### Symbolic / precision tools
- SymPy simplify docs: <https://docs.sympy.org/latest/modules/simplify/simplify.html>
- SymPy term rewriting docs: <https://docs.sympy.org/latest/modules/rewriting.html>
- mpmath docs: <https://mpmath.org/doc/current/>

---

## 14. Appendix: paper facts most worth remembering while implementing

1. EML plus `1` generates the paper’s scientific-calculator basis. [Paper, pp. 1, 5, 8-10]
2. EML expressions form a trivial binary grammar. [Paper, pp. 2, 11-12]
3. The master tree is complete up to the chosen depth. [Paper, pp. 12-14]
4. The univariate parameter count is `5 * 2^n - 6`. [Paper, p. 14]
5. `ln x` is exactly recoverable at shallow depth with snapping. [Paper, p. 14]
6. The PyTorch proof of concept uses `torch.complex128`. [Paper, p. 15]
7. Blind recovery gets hard quickly with depth. [Paper, p. 15]
8. Warm starts / perturbed-correct initializations converge much more reliably. [Paper, p. 15]
9. Numerical stability and branch semantics are first-class issues, not details. [Paper, pp. 10-11, 15]
10. A practical engine therefore has to be hybrid, verified, and semantics-aware.