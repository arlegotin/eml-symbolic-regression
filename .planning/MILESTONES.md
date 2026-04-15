# Milestones

## v1.2 Training Benchmark and Recovery Evidence (Shipped: 2026-04-15)

**Phases completed:** 5 phases, 5 plans, 0 tasks

**Key accomplishments:**

- Added deterministic benchmark suite contracts, built-in suite registry, fail-closed validation, stable run IDs, and deterministic artifact paths.
- Added benchmark CLI execution for catalog verification, compile diagnostics, blind optimizer training, and compiler warm-start training.
- Expanded formula coverage with `radioactive_decay`, shallow blind baselines, Beer-Lambert perturbation sweeps, Michaelis-Menten warm diagnostics, Planck stretch diagnostics, and selected FOR_DEMO formulas.
- Added normalized per-run metrics plus aggregate JSON/Markdown evidence reports with recovery rates, grouping, taxonomy, and code/environment provenance.
- Added CI-scale benchmark smoke coverage and generated smoke evidence artifacts in `artifacts/benchmarks/smoke/`.
- Updated documentation to explain benchmark commands, report artifacts, same-AST warm-start return, verifier-owned recovery rates, and unsupported/failure interpretation.

---

## v1.1 EML Compiler and Warm Starts (Shipped: 2026-04-15)

**Phases completed:** 6 phases, 6 plans, 0 tasks

**Key accomplishments:**

- Added a fail-closed SymPy-to-EML compiler with structured metadata, rule traces, unsupported reason codes, and independent validation.
- Extended soft master trees with finite literal constant catalogs and exact AST embedding with snap-back verification.
- Added deterministic compiler warm-start training through the existing optimizer while keeping `recovered` verifier-owned.
- Promoted Beer-Lambert to verified trained exact EML recovery through the compiler warm-start path.
- Added honest Michaelis-Menten default-depth diagnostics and explicit normalized Planck stretch reporting.
- Expanded regression coverage to 24 tests and documented literal constants, warm-start provenance, and non-blind scope.

---
