# Feature Landscape

**Domain:** EML symbolic regression MVP
**Project:** EML Symbolic Regression
**Researched:** 2026-04-15
**Overall confidence:** HIGH

This research is based on `.planning/PROJECT.md`, `sources/NORTH_STAR.md`, `sources/FOR_DEMO.md`, `sources/paper.pdf`, and `AGENTS.md`. The MVP should be a research-grade Python package and CLI that proves the complete EML recovery loop on synthetic scientific datasets: build a complete depth-bounded EML tree, optimize soft categorical choices, snap to an exact tree, simplify locally, and verify against held-out and high-precision evaluators.

## Table Stakes

Features users will expect from a credible first implementation. Missing any of these makes the system feel incomplete or undermines the paper-grounded claim.

| Feature | Why Expected | Complexity | Dependencies | Notes |
|---------|--------------|------------|--------------|-------|
| Canonical EML semantics | The whole project rests on `eml(x, y) = exp(x) - ln(y)` plus terminal `1`, evaluated over complex values with a clear branch policy. | High | None | Must separate stabilized training evaluation from faithful verification evaluation. Include behavior for branch cuts, infinities, signed zero, NaN/Inf, and principal complex log. |
| Depth-bounded complete EML master trees | The core paper result is that EML expressions form the regular grammar `S -> 1 | eml(S, S)`, allowing all formulas up to a chosen depth to live inside one tree family. | High | Canonical EML semantics | Start with univariate depths 2-3 for reproduction; make depth an explicit user/config parameter. Use the paper's categorical slot choices: terminal `1`, variables, and previous subtree outputs. |
| Differentiable categorical gates | The MVP needs soft choices during training and exact one-hot choices after hardening. | High | Master tree construction | Use logits and softmax-style probabilities. Do not expose a long-term dependency on unstable helper APIs for categorical hardening; wrap the logic behind the project API. |
| Complex128 PyTorch training path | The paper proof of concept used `torch.complex128`, and symbolic recovery is branch- and precision-sensitive. | Medium | EML semantics, master tree, gates | `complex64` can be a later speed mode, not the default. |
| Stabilized training evaluator | Deep EML compositions can overflow through repeated `exp` and can produce complex NaNs. | High | Complex128 training path | Clamp only in training mode. Track max real input to `exp`, NaN/Inf counts, clamp counts, and per-node anomaly counters. |
| Optimization engine with restarts | Blind recovery drops rapidly with depth; single-run gradient descent is not a serious MVP. | High | Training evaluator, gates | Include Adam or AdamW, multiple restarts, deterministic seeds, temperature annealing, entropy regularization, expected-size penalty, and numerical-stability penalty. |
| Depth curriculum and warm starts | The paper reports weak blind recovery at deeper depths but strong convergence from perturbed correct solutions. | Medium | Optimizer, serialization of intermediate solutions | Support shallow-to-deeper curriculum, subtree reuse, and warm-started runs from snapped or known scaffolds. |
| Hardening and exact snapping | The model must become a discrete symbolic candidate, not remain a soft neural approximation. | High | Gates, optimizer | Choose argmax categories, remove dead branches, round to exact one-hot gates, and produce an exact EML tree. |
| Deterministic tree serialization | Snapped outputs must be reproducible and inspectable. | Medium | Snapping | Export exact EML trees to deterministic JSON. Include depth, gates, terminals, source config, seed, and training metadata. |
| SymPy expression export | Users need human-readable formulas, not only EML ASTs. | Medium | Snapping, tree serialization | Translate snapped trees to SymPy expressions and pretty strings. Use targeted rewrites; do not rely on generic `simplify()` as an oracle. |
| Local discrete cleanup | Gradient search can find valid but bloated structures, and the paper notes compiled EML forms are often not shortest. | High | Snapping, SymPy export, verifier | Prune inert branches, collapse repeated patterns, try small subtree substitutions, and rerun verification after every cleanup candidate. |
| Verification gate for "recovered" status | Training loss alone is not recovery. | High | Snapping, export, cleanup, data generation | Require post-snap agreement on training, held-out, extrapolation, and high-precision mpmath points. Include cross-backend comparison where available. |
| Synthetic dataset and sampling utilities | The first release targets noiseless or modest-noise scientific datasets and demos from `FOR_DEMO.md`. | Medium | EML semantics for target evaluation, verifier | Provide normalized/domain-aware sampling, train/held-out/extrapolation splits, optional low noise, and singularity avoidance. |
| Reproducible CLI | The project goal is a package and CLI before any UI. | Medium | Pipeline components | CLI should run experiments, demos, snapping, cleanup, verification, and report generation from config files. |
| Demo suite from `FOR_DEMO.md` | The first release must showcase the system with examples chosen for feasibility and impact. | Medium | Data generators, optimizer, snapping, verifier, CLI | Include simple sanity laws and at least one flagship law. Use normalized, dimensionless forms wherever possible. |
| Test coverage for the recovery pipeline | A research engine without semantics and verification tests is not trustworthy. | High | All core components | Cover EML semantics, tree construction, categorical gates, snapping, serialization, SymPy export, cleanup invariants, verification, and demo smoke tests. |

## Demo Features

The demo set is not optional for the MVP because it is the main way the first implementation proves value. The demos should be staged from highest success probability to strongest public-facing examples.

| Demo Feature | Category | Complexity | MVP Role | Dependencies | Notes |
|--------------|----------|------------|----------|--------------|-------|
| `exp(x)` / `ln(x)` paper-like recovery | Sanity / paper reproduction | Low-Med | First correctness proof | Semantics, depth 2-3 trees, optimizer, snapping, verifier | `ln(x)` is explicitly discussed in the paper as exactly recoverable at shallow depth with snapping. |
| Beer-Lambert or radioactive decay | Sanity demo | Low | First user-visible recovery demo | Data generation, optimizer, snapping, plots/report | Good smoke test for exact recovery and hardening, but not impressive enough as a headline. |
| Michaelis-Menten kinetics | Core public demo | Medium | First serious scientific law | Rational structure, parameterized synthetic data, verification | Recommended in `FOR_DEMO.md` as one of the strongest three public demos. Good biology/biochemistry story. |
| Logistic growth | Progression demo | Medium | Bridge from simple exponentials to richer scientific laws | Exponential/rational structure, warm starts helpful | High success-probability sequence places it before Shockley and harder flagship demos. |
| Shockley diode equation | Engineering demo | Medium | Credible electronics example | Exponential minus constant, scaling/normalization | Structurally close to EML's natural `exp - log` bias and likely more feasible than trig-heavy demos. |
| Damped harmonic oscillator | Headline demo | High | Demonstrate oscillation plus decay | Trig support through EML, depth curriculum, warm starts, strong verifier | Public-facing, visually striking, but harder due to trig + exp + phase. Do after simpler demos are stable. |
| Normalized Planck spectrum `x^3 / (exp(x) - 1)` | Flagship demo | High | Prestige demo | Powers, exp, subtraction, division, normalized sampling, warm starts/curriculum | Use the normalized dimensionless form, not raw SI Planck law. This should be the flagship once the pipeline is reliable. |

## Differentiators

Features that set this project apart from ordinary symbolic-regression demos. These are not all required on day one, but the MVP should include enough of them to make the project distinctive.

| Feature | Value Proposition | Complexity | Dependencies | Notes |
|---------|-------------------|------------|--------------|-------|
| Complete depth-bounded EML search family | Avoids hand-picking heterogeneous operator vocabularies like `+`, `*`, `sin`, `log`, `exp`. | High | EML semantics, master tree | This is the central differentiator from conventional symbolic regression. |
| Exact snap-and-verify recovery contract | Makes "recovered" mean a discrete, human-readable formula that passes out-of-sample and high-precision checks. | High | Snapping, verifier | Prevents the common failure mode of presenting a curve fit as equation discovery. |
| Hybrid continuous-to-discrete pipeline | Uses gradient optimization to approach basins, then discrete cleanup to get cleaner formulas. | High | Optimizer, snapping, cleanup | Directly follows `NORTH_STAR.md`: pure gradient descent is not enough. |
| Warm-start and curriculum-first UX | Aligns the product with the paper's empirical result that deeper correct basins exist but are hard to find randomly. | Medium | Optimizer, serialization, CLI configs | This should be exposed as a normal workflow, not buried as an expert trick. |
| Recovery diagnostics report | Gives users evidence: fit loss, entropy, tree size before/after cleanup, extrapolation error, verification pass rate, anomalies, and seed sensitivity. | Medium | Logging, verifier, cleanup | Strongly supports research credibility and roadmap decisions. |
| Formula progression demos | Shows increasing difficulty: shallow exact law -> rational biochemical law -> exponential device law -> oscillator -> normalized Planck. | Medium | Demo suite, CLI, reporting | Makes the showcase honest about feasibility instead of jumping straight to the hardest law. |
| Small multivariate support | Broadens beyond univariate demos and matches the paper's stated extension to arbitrary input variables. | High | Generalized gate choices, data utilities, verifier | Include only if univariate core is stable. Start with simple two-variable paper-like or low-risk scientific examples; defer risky Van der Waals. |
| Targeted symbolic cleanup, not generic simplification | Produces smaller, more legible formulas without pretending symbolic equivalence is solved. | High | SymPy export, verifier | Use explicit rewrite passes and bounded local search. |

## Anti-Features / Out of Scope

Features to deliberately avoid in the first implementation.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Promise blind recovery of arbitrary depth-6 formulas | The paper reports no blind recovery at depth 6 in 448 attempts. | State depth and initialization assumptions clearly. Use curriculum, priors, warm starts, and shallow-first demos. |
| High-noise real-world scientific datasets without priors | The project is not ready to be a generic black-box discovery tool for messy data. | Use noiseless and modest-noise synthetic datasets with known laws and explicit sampling domains. |
| Web GUI or polished frontend | The first target is reproducibility, verification, and demos. | Build a package, CLI, config files, and report artifacts. |
| Pure gradient-only symbolic regression | A soft model without snapping, cleanup, and verification is not the paper-grounded product. | Ship the hybrid pipeline: optimize -> harden -> snap -> cleanup -> verify. |
| Benchmark-only system with no symbolic output | Fit metrics alone miss the point of equation discovery. | Always export exact EML JSON and human-readable SymPy expressions for recovered candidates. |
| Generic operator-menu symbolic regression | It weakens the central EML claim and adds a conventional search space problem. | Keep EML as the primary grammar; ordinary expressions are export/output format, not the search grammar. |
| Raw full Planck law in SI units as an early flagship | Physical constants and unit scaling make optimization uglier and obscure the core idea. | Use normalized Planck spectrum `x^3 / (exp(x) - 1)`. |
| Early demos with special functions, integrals, piecewise laws, chaotic systems, or stiff ODE closed forms | These are outside the paper's compact elementary-function sweet spot or too numerically brittle. | Use compact, normalized elementary laws from `FOR_DEMO.md`. |
| Claim shortest-form symbolic output | Gradient search may produce bloated but correct trees, and exact shortest-form search is a separate hard problem. | Provide local cleanup and report tree size before/after cleanup. |
| Custom CUDA kernels in v1 | The early bottleneck is correctness, semantics, snapping, and verification, not hand-tuned kernels. | Use standard PyTorch CUDA if available; profile before adding kernels. |
| Formal theorem-prover equivalence | Too heavy for v1 and listed as out of scope in project context. | Use numeric, high-precision, edge-case, cross-backend, and targeted symbolic checks. |
| Relying on generic SymPy `simplify()` as proof | SymPy simplification is useful but not a stable equivalence contract. | Use targeted rewrites plus verification after every rewrite. |

## Feature Dependencies

```text
Canonical EML semantics
  -> training evaluator
  -> depth-bounded master trees
  -> differentiable categorical gates
  -> optimizer with restarts / annealing / regularizers
  -> hardening and exact snapping
  -> deterministic EML JSON export
  -> SymPy expression export
  -> local discrete cleanup
  -> high-precision and held-out verifier
  -> recovered formula report
  -> reproducible CLI demos
```

```text
Synthetic data utilities
  -> train / held-out / extrapolation splits
  -> domain normalization and singularity avoidance
  -> demo generators
  -> verifier
  -> recovery diagnostics report
```

```text
Simple demos
  -> pipeline confidence
  -> Michaelis-Menten / Logistic / Shockley
  -> Damped oscillator
  -> Normalized Planck spectrum
```

```text
Univariate support
  -> small multivariate support
  -> later realistic scientific datasets
```

## MVP Recommendation

Prioritize:

1. Canonical EML semantics, univariate depth-bounded trees, complex128 training, and exact snapping.
2. Verification-first recovery contract: held-out, extrapolation, and high-precision mpmath checks before calling a candidate recovered.
3. Reproducible CLI demos in this order: `ln(x)` / `exp(x)`, Beer-Lambert or radioactive decay, Michaelis-Menten, Logistic or Shockley.
4. Local cleanup and SymPy export once snapping works reliably.
5. One flagship public demo after the pipeline is stable: normalized Planck spectrum if the engine handles it; otherwise damped oscillator as the stretch demo and Michaelis-Menten as the reliable headline.

Defer:

- Small multivariate demos until the univariate recovery pipeline is stable.
- Van der Waals until singularity handling and multivariate verification are strong.
- Hill equation with non-integer exponents until constant/coefficient constraints are designed.
- Custom CUDA, distributed search, theorem-prover integration, and GUI work until core recovery and verification are credible.

## Requirements Implications

The downstream `REQUIREMENTS.md` should avoid vague goals like "discover formulas from data." The MVP requirements should be phrased as verifiable capabilities:

- Given a configured shallow univariate target such as `ln(x)` or `exp(x)`, the CLI can train a complete EML tree, snap it to an exact tree, export JSON and SymPy, and pass high-precision verification.
- Given a demo target from `FOR_DEMO.md`, the CLI can generate normalized synthetic data, run repeated seeded attempts, and report success/failure with diagnostics.
- A candidate is marked `recovered` only if it passes post-snap held-out, extrapolation, and high-precision checks.
- The system records enough metadata to reproduce a run: config, depth, seeds, restart count, training mode clamps, anomalies, snapped tree, cleanup changes, and verification results.

## Sources

- `.planning/PROJECT.md` - project scope, active requirements, out-of-scope constraints, and demo expectations.
- `sources/NORTH_STAR.md` - recommended hybrid pipeline, module boundaries, risks, strong MVP definition, and phase implications.
- `sources/FOR_DEMO.md` - demo ranking, highest-success demo sequence, flagship trio, and demos to avoid.
- `sources/paper.pdf` - EML definition, grammar, master-tree construction, PyTorch proof of concept, recovery behavior by depth, and snapping evidence.
- `AGENTS.md` - repository source-of-truth pointers for paper, implementation details, and demo examples.
