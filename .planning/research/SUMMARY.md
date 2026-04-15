# Project Research Summary

**Project:** EML Symbolic Regression
**Domain:** Hybrid symbolic-regression engine over complete depth-bounded EML trees
**Researched:** 2026-04-15
**Confidence:** HIGH for Python/PyTorch MVP direction; MEDIUM for later scaling and acceleration details

## Executive Summary

EML Symbolic Regression is a research-grade Python package and CLI for recovering human-readable elementary formulas from synthetic scientific data using the paper's single-operator representation: `eml(x, y) = exp(x) - ln(y)`. Experts should build this as a staged hybrid search system, not a generic symbolic-regression operator menu and not a pure neural curve fitter. The core loop is: generate normalized data, build a complete depth-bounded EML master tree, optimize soft categorical choices in PyTorch `complex128`, snap the result to an exact EML AST, clean it locally, export readable expressions, and verify with held-out, extrapolation, and high-precision checks.

The recommended v1 is deliberately narrow: univariate shallow-to-moderate depth recovery, deterministic artifacts, verifier-gated demos, and a reproducible CLI. Python, PyTorch, NumPy, SymPy, mpmath, pytest, standard-library JSON/logging, and `argparse` are enough. Rust, custom CUDA, GUI work, arbitrary coefficients, multivariate physics, and noisy real-world discovery should wait until the reference semantics, snapping, cleanup, and verification contract are stable.

The biggest risks are semantic drift between training and verification, mistaking soft fit for symbolic recovery, blind escalation to deep search, numerical explosion from nested `exp`/complex `log`, and demo overreach. The roadmap should mitigate these by building canonical semantics before training, forcing every claim through exact AST export and verification, reporting seed sensitivity and anomaly counts, using curriculum/warm starts for harder targets, and following the demo ladder from simple laws to normalized Planck only after lower rungs are reliable.

## Key Findings

### Recommended Stack

Use a Python-first implementation with PyTorch `complex128` for differentiable complete EML trees, NumPy for deterministic data/reference arrays, SymPy for exact expression rendering and targeted rewrites, mpmath for high-precision verification, and pytest for regression coverage. Keep the MVP package and CLI simple: `pyproject.toml`, `argparse`, standard `logging`, deterministic JSON/JSONL artifacts, and no new runtime dependencies beyond the existing scientific stack unless implementation evidence demands them.

Do not start with JAX, Julia/PySR, Mathematica, Rust, custom CUDA, theorem proving, or a web UI. Those either conflict with the project source documents or add surface area before the EML semantics and recovery contract are proven.

**Core technologies:**
- Python 3.11: package, CLI, orchestration, and fast research iteration.
- PyTorch 2.10 with `torch.complex128`: trainable complete master tree, categorical logits, Adam/AdamW optimization, restarts, annealing, and diagnostics.
- NumPy 1.26: deterministic synthetic data generation, sampling, and CPU reference checks.
- SymPy 1.14: exact AST export to human-readable formulas and targeted cleanup passes.
- mpmath 1.3: high-precision real/complex verification for snapped formulas.
- pytest 7.4: semantics, tree, snapping, verifier, cleanup, and demo regression tests.
- Standard-library `dataclasses`, `enum`, `json`, `argparse`, and `logging`: exact ASTs, deterministic artifacts, CLI, and reproducible run records.

**Version and stack constraints:**
- Declare `requires-python = ">=3.11,<3.13"` when packaging begins.
- Default to `torch.complex128`; treat `complex64` as a later optional speed mode.
- Use PyTorch eager mode first because anomaly inspection and branch-sensitive debugging matter more than compilation speed.
- Use standard PyTorch CUDA only if available; custom CUDA and Rust/PyO3 belong after profiling and golden corpus stabilization.

### Expected Features

The MVP must prove the complete EML recovery loop, not just produce attractive plots. The credible v1 surface is a package and CLI that can train, snap, export, clean, verify, and report recovery attempts on normalized synthetic demos.

**Must have (table stakes):**
- Canonical EML semantics: explicit `eml(x, y) = exp(x) - log(y)`, complex principal-branch policy, branch/Inf/NaN behavior, and separate training versus verification modes.
- Complete depth-bounded master trees: univariate depth-2 and depth-3 first, with legal categorical slot choices and tests proving paper formulas are reachable by hard assignment.
- Differentiable categorical gates: logits and softmax probabilities during training, exact one-hot choices after hardening.
- Complex128 PyTorch training path: Adam/AdamW, multiple restarts, temperature or entropy scheduling, size/stability penalties, and deterministic seeds.
- Stabilized training evaluator: training-only clamps and anomaly counters for NaN, Inf, overflow, branch issues, clamp counts, magnitude, and imaginary residue.
- Hardening and exact snapping: argmax/top-k snap logic, margin reporting, dead-branch pruning, post-snap loss checks, and exact EML AST output.
- Deterministic serialization: exact EML JSON, run manifests, verification reports, and reproducibility metadata.
- SymPy export: readable ordinary-expression rendering with targeted rewrites, not generic simplification as proof.
- Local cleanup: bounded pruning and subtree rewrites, always verifier-gated.
- Verification contract: no candidate is `recovered` until it passes post-snap train, held-out, extrapolation, and high-precision mpmath checks.
- Synthetic dataset utilities: normalized/domain-aware sampling, train/held-out/extrapolation splits, low-noise options, and singularity avoidance.
- Reproducible CLI and demo suite: canned examples from `sources/FOR_DEMO.md`, report artifacts, and tests.

**Should have (differentiators):**
- Hybrid continuous-to-discrete pipeline with clear status taxonomy: `soft_fit_only`, `snap_failed`, `verification_failed`, `recovered`, `unsupported_target`, `numeric_error`.
- Warm-start and curriculum workflows: embed verified shallow ASTs into deeper trees and unfreeze capacity gradually.
- Recovery diagnostics report: training loss, post-snap loss, gate entropy, snap margins, active tree size, cleanup delta, extrapolation error, anomaly counts, seed sensitivity, and verifier status.
- Formula progression demos: simple exact laws, mechanistic rational laws, exponential device law, oscillator, and normalized Planck as a later flagship.
- Small multivariate support and coefficient-fitting layer only after univariate recovery is routine.

**Defer (v2+):**
- Full blind recovery of arbitrary depth-6 formulas.
- High-noise real-world datasets without priors.
- Raw SI Planck law, singular multivariate laws, chaotic systems, special functions, piecewise laws, and stiff ODE closed forms.
- GUI/web frontend, distributed search, custom CUDA kernels, Rust core, theorem-prover equivalence, and generic operator-menu symbolic regression.
- Ad hoc arbitrary learned coefficients inside the EML grammar.

### Architecture Approach

Build a one-way staged pipeline with explicit boundaries: demo/config -> sampler/normalizer -> master-tree spec -> differentiable PyTorch model -> optimizer/restarts -> hardener/snapper -> exact EML AST -> local cleanup/SymPy export -> verifier -> formula artifacts and CLI reports. The central architectural rule is that training may use stabilized numerical semantics, but verification must use canonical EML semantics with no hidden clamps or epsilons.

**Major components:**
1. EML semantics kernel: canonical and training-mode evaluators, complex branch policy, non-finite handling, and anomaly counters.
2. Exact EML AST: immutable `Const(1)`, `Var(name)`, and `Eml(left, right)` tree representation with deterministic JSON.
3. Dataset and sampler layer: normalized synthetic train, held-out, extrapolation, and edge-case point sets.
4. Master-tree spec: complete depth-bounded scaffold and legal slot choices independent of PyTorch tensors.
5. Differentiable EML model: PyTorch logits, softmax/temperature behavior, batched `complex128` forward pass, and node diagnostics.
6. Optimization engine: restarts, schedules, fit/entropy/size/stability losses, early stopping, checkpoints, and run manifests.
7. Hardener/snapper: normalized categorical probabilities to deterministic exact AST, including dead-branch pruning and margin reporting.
8. Serialization layer: separate schemas for ASTs, checkpoints, run manifests, and verification reports.
9. Local cleanup and symbolic export: bounded AST rewrites, targeted SymPy rendering, and size reduction under verifier control.
10. Verifier: train, held-out, extrapolation, edge, backend, and high-precision checks; only this component can label `recovered`.
11. CLI/demo orchestration: reproducible commands, configs, reports, plots, and demo artifacts.

### Critical Pitfalls

1. **Semantics drift between training and verification** — build canonical semantics first, make evaluator mode explicit, ban hidden verification clamps, and cross-check snapped ASTs with mpmath and other backends.
2. **Calling soft fit symbolic recovery** — keep soft fit, snap readiness, post-snap loss, and verified recovery as separate statuses; never print a recovered formula before exact AST verification.
3. **Blind depth escalation** — start with depth-2/depth-3 paper-like targets, measure recovery distributions across seeds, and use curriculum/warm starts before deeper searches.
4. **Numerical explosion from nested `exp` and complex `log`** — default to `complex128`, normalize data, clamp only in training mode, log per-node anomalies, and fail fast on non-finite verification.
5. **Incorrect master-tree construction** — validate parameter counts, depth conventions, legal slot choices, and known paper formulas by direct hard gate assignment before optimization.
6. **Underspecified snapping** — centralize hardening, require active-gate margins, handle ties deterministically, store snap decisions, and evaluate top-k alternatives when ambiguous.
7. **Weak verification data and false positives** — use independent train/held-out/extrapolation/high-precision points, include boundary probes, compare against smaller candidates, and require verifier reports for every `recovered` result.
8. **Unchecked symbolic simplification** — keep exact EML AST as source of truth, use targeted SymPy rewrites only, and re-run verification after every cleanup candidate.
9. **Demo overreach** — follow the feasibility ladder and avoid raw physical units, hidden constants, special functions, and high-depth flagship demos before the pipeline is reliable.
10. **Acceleration before correctness** — defer Rust/CUDA until the Python reference and golden corpus are locked down and profiling identifies bottlenecks.

### Demo Strategy

The demo suite is part of the product, not a cosmetic extra. It should be staged to prove increasingly difficult capabilities while making seed sensitivity and failures visible.

**Recommended progression:**
1. Paper-like `exp(x)` and `ln(x)` recoveries: first correctness and snapping proof.
2. Beer-Lambert or radioactive decay: first user-visible sanity demo.
3. Michaelis-Menten: reliable mechanistic scientific law and likely first serious headline.
4. Logistic growth: nonlinear saturating law that exercises rational/exponential structure.
5. Shockley diode: engineering example aligned with EML's exponential-minus-log bias.
6. Damped harmonic oscillator: visually strong stretch demo after trig/phase handling stabilizes.
7. Normalized Planck spectrum `x^3 / (exp(x) - 1)`: flagship only after curriculum, warm starts, cleanup, and verifier reporting are mature.

**Demo rules:**
- Use normalized, dimensionless domains and avoid raw SI constants in v1.
- Store clean configs, seed batches, optimizer budgets, run manifests, snapped ASTs, SymPy exports, plots, and verification reports.
- Report both successes and failed restart counts; do not hide seed sensitivity.
- Treat Michaelis-Menten as the dependable public demo if Planck or oscillator remains too brittle.

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 1: Semantics, AST, and Deterministic Artifacts

**Rationale:** Every later component depends on exact EML meaning. If branch policy, `complex128` behavior, verification mode, or JSON artifacts drift later, optimizer and demo results become untrustworthy.

**Delivers:** canonical EML evaluator, explicit training/canonical modes, high-precision reference checks, exact AST types, deterministic AST JSON, and tests for paper identities such as `exp(x)` and `ln(x)`.

**Addresses:** canonical EML semantics, deterministic tree serialization, basic verification foundations, and test coverage.

**Avoids:** semantics drift, hidden epsilons in verification, real-valued targets hiding complex residue, and nondiffable result artifacts.

### Phase 2: Complete Master Trees and Soft Evaluation

**Rationale:** The complete scaffold must be proven independently before any optimizer failure is interpreted. Hand-set one-hot gates should reproduce known formulas at depth 2/3.

**Delivers:** univariate depth-bounded master-tree specs, legal slot catalogs, PyTorch `complex128` differentiable model, softmax categorical gates, batched forward pass, shape/property tests, and node-level diagnostics.

**Uses:** Python, PyTorch eager mode, NumPy reference fixtures, exact AST conversion hooks.

**Implements:** master-tree spec and differentiable EML model boundaries.

**Avoids:** incorrect master-tree construction, unreachable formulas, depth convention errors, and data-generation/evaluator shared-bug traps.

### Phase 3: Optimizer, Restarts, Hardening, and Recovery Statuses

**Rationale:** Search should become a candidate generator only after semantics and completeness are tested. This phase creates the transition from soft tensors to exact candidates, while refusing to call low loss recovery.

**Delivers:** Adam/AdamW training loop, restarts, deterministic seeds, temperature/entropy scheduling, size/stability penalties, anomaly logging, run manifests, hardening/snapper, snap margins, top-k ambiguity handling, post-snap loss checks, and result statuses.

**Addresses:** complex128 training, optimization engine, depth curriculum foundation, exact snapping, reproducible CLI internals.

**Avoids:** calling soft fit recovery, underspecified snapping, numerical explosion, restart brute force without diagnostics, and CI tests dependent on lucky seeds.

### Phase 4: Verifier and Acceptance Contract

**Rationale:** Verification must exist before demo polish so public claims cannot be based on training curves or plausible formulas.

**Delivers:** held-out/interpolation checks, extrapolation checks, mpmath high-precision checks, backend differential checks, branch/singularity probes, acceptance schemas, failure reason codes, and CLI-visible verifier reports.

**Uses:** mpmath, NumPy, exact AST evaluator, serialized datasets, run manifests, and deterministic artifact hashes.

**Implements:** verifier as the sole authority for `recovered`.

**Avoids:** weak verification false positives, training-only formulas, hidden clamps, overclaiming, and demos that pass by plotting only the real part.

### Phase 5: Local Cleanup, SymPy Export, and Human-Readable Reports

**Rationale:** Users need readable formulas, but cleanup and simplification must be verifier-gated so presentation never becomes the source of truth.

**Delivers:** dead-branch pruning, duplicate/redundant subtree cleanup, bounded local neighborhood search, targeted SymPy exporter, selected rewrite passes, before/after tree-size metrics, and report artifacts linking exact AST to rendered formula.

**Addresses:** local discrete cleanup, symbolic expression export, formula readability, and diagnostics report.

**Avoids:** SymPy as an unchecked oracle, branch-invalid rewrites, bloated correct formulas, and untracked simplification drift.

### Phase 6: Demo Harness and Public Showcase

**Rationale:** Demos should exercise a verified pipeline rather than drive ad hoc engine behavior. This phase turns the core into repeatable showcase runs.

**Delivers:** demo spec/config format, dataset generators, normalized sampling, canned demos in the recommended sequence, CLI commands, plots, JSON artifacts, snapped formulas, verification reports, seed/runtime summaries, and demo smoke/regression tests.

**Addresses:** synthetic dataset utilities, reproducible CLI, demo suite from `FOR_DEMO.md`, and public report generation.

**Avoids:** flagship demo first, raw unit-heavy laws, hidden constants, lucky seed demos, high-noise real-world overreach, and unsupported-target confusion.

### Phase 7: Multivariate, Coefficients, and Scaling

**Rationale:** Multivariate support, coefficient fitting, Rust, GPU profiling, and larger benchmarks are valuable only after the reference univariate engine has a stable golden corpus.

**Delivers:** multivariate slot catalogs, small multivariate demos, optional semi-parametric coefficient layer, profiling hooks, Rust/PyO3 or standard PyTorch GPU acceleration only for measured bottlenecks, and expanded benchmark dashboards.

**Addresses:** later differentiators, scaling, performance, and broader scientific use cases.

**Avoids:** acceleration before correctness, incompatible second evaluators, arbitrary coefficients smuggled into the grammar, and unrealistic blind deep recovery claims.

### Phase Ordering Rationale

- Semantics and exact artifacts come first because they define what every recovered expression means.
- Master-tree construction comes before optimization because completeness can and should be tested with direct gate assignments.
- Optimization and snapping come before verification only as candidate generation; the roadmap must still treat verifier implementation as a blocker for demos.
- Cleanup follows verification because smaller formulas are useful only if every rewrite preserves accepted behavior.
- Demos follow the recovery contract because plot-first development hides false positives and seed sensitivity.
- Multivariate and acceleration come last because v1 already has hard numerical, branch, depth, and snapping problems in the univariate case.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 3:** Optimization schedules, entropy/size/stability penalties, top-k snapping, and curriculum policies need empirical tuning against paper-like fixtures.
- **Phase 4:** Verification thresholds, branch-sensitive point selection, and cross-backend agreement need careful domain-specific design.
- **Phase 5:** Safe targeted rewrite sets and cleanup neighborhoods need validation against complex principal-branch semantics.
- **Phase 6:** Planck, oscillator, and Shockley demo budgets may need phase-specific research once lower demos produce empirical recovery data.
- **Phase 7:** Multivariate slot scaling, coefficient handling, Rust/PyO3, and GPU acceleration should be researched only with profiles and golden corpus evidence.

Phases with standard patterns or enough local guidance to skip standalone research:
- **Phase 1:** Exact ASTs, deterministic JSON, mpmath references, and unit tests are well-scoped by source docs.
- **Phase 2:** PyTorch module boundaries, logits/softmax gates, and property tests are straightforward once the master-tree spec is defined.
- **Early Phase 6 smoke demos:** `exp(x)`, `ln(x)`, Beer-Lambert, and radioactive decay are sufficiently documented for direct implementation.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Research aligns with local environment and project docs: Python 3.11, PyTorch 2.10, NumPy, SymPy, mpmath, and pytest are already present and match the paper/NORTH_STAR direction. Later Rust/CUDA timing is MEDIUM because bottlenecks are not measured yet. |
| Features | HIGH | Table stakes are directly grounded in `.planning/PROJECT.md`, `sources/NORTH_STAR.md`, `sources/FOR_DEMO.md`, and the paper: semantics, complete trees, complex128 training, snapping, cleanup, verification, CLI, demos, and tests. |
| Architecture | HIGH | Component boundaries and build order are strongly supported by the paper's master-tree/training behavior and NORTH_STAR's hybrid pipeline. Scaling beyond shallow demos remains MEDIUM. |
| Pitfalls | HIGH | Critical risks are repeatedly supported across paper results, project constraints, NORTH_STAR warnings, demo guidance, and official numerical/symbolic tooling docs. |

**Overall confidence:** HIGH for the v1 roadmap structure; MEDIUM for exact optimizer budgets, deep-demo success rates, and post-v1 acceleration strategy.

### Gaps to Address

- **Optimizer budget and schedules:** Determine restart counts, temperature schedules, entropy/size weights, and early stopping empirically during Phase 3.
- **Verification thresholds:** Define tolerances per demo/domain and how imaginary residue is handled for real-valued targets during Phase 4.
- **Safe cleanup rewrites:** Validate each SymPy/AST rewrite against branch-sensitive high-precision samples before making it part of the default cleanup path.
- **Coefficient strategy:** Keep v1 normalized where possible; if coefficients are needed, design a separate explicit layer with status metadata and verification.
- **Demo feasibility:** Treat damped oscillator and normalized Planck as stretch/flagship demos gated by successful lower-rung recovery metrics.
- **Performance plan:** Do not select Rust/CUDA work until profiling identifies concrete bottlenecks and the reference Python golden corpus is stable.

## Sources

### Primary (HIGH confidence)

- `.planning/PROJECT.md` — project scope, active requirements, constraints, out-of-scope decisions, and demo expectations.
- `.planning/research/STACK.md` — Python/PyTorch-first stack recommendation, version policy, module stack mapping, and deferred acceleration path.
- `.planning/research/FEATURES.md` — v1 table stakes, differentiators, anti-features, demo features, and requirements implications.
- `.planning/research/ARCHITECTURE.md` — pipeline architecture, component boundaries, data flow, serialization formats, verification boundaries, and build order.
- `.planning/research/PITFALLS.md` — critical/moderate/minor pitfalls, phase warnings, gates, and roadmap choices to avoid.
- `sources/paper.pdf` — EML definition, grammar, master-tree construction, PyTorch `complex128` proof of concept, snapping behavior, recovery rates by depth, and Rust verification note.
- `sources/NORTH_STAR.md` — implementation blueprint for hybrid search, hardening, cleanup, verification, risks, and strong MVP definition.
- `sources/FOR_DEMO.md` — demo sequence, recommended flagship examples, normalization guidance, and examples to avoid.
- `AGENTS.md` — repository instruction that implementation is grounded in the paper, NORTH_STAR, and demo sources.

### Official/current references cited by research files

- PyTorch complex numbers docs — complex tensor support and caveats.
- PyTorch reproducibility and numerical accuracy docs — nondeterminism, overflow, and backend differences.
- PyTorch `gumbel_softmax` docs — legacy warning supporting local abstraction around hardening helpers.
- SymPy simplification and rewriting docs — targeted simplification guidance and limits of generic simplification.
- mpmath docs — arbitrary-precision verification backend.
- pytest parametrization docs — regression and matrix test structure.
- Python packaging `pyproject.toml` metadata specs — package metadata and dependency declaration.
- uv docs — optional repeatable dev workflow.
- NVIDIA CUDA C++ Programming Guide — later acceleration context, not an MVP dependency.

---
*Research completed: 2026-04-15*
*Ready for roadmap: yes*
