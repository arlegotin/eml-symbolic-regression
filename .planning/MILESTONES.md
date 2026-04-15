# Milestones

## v1.4 Recovery Performance Improvements (Shipped: 2026-04-15)

**Phases completed:** 5 phases, 5 plans, 0 tasks

**Key accomplishments:**

- Added v1.3 baseline triage, representative failure rows, immutable baseline locks, and focused diagnostic reruns.
- Improved shallow blind recovery with conservative `exp` and `log` scaffold initializers while preserving verifier-owned recovery semantics.
- Added warm-start perturbation diagnosis fields and campaign metrics that identify active-slot perturbation as the dominant Beer-Lambert high-noise failure mechanism.
- Added compiler diagnostics and a validated Shockley `c*exp(a)-c` template, moving Shockley into verified compiled coverage.
- Generated v1.4 standard/showcase campaign evidence and a before/after comparison report showing overall recovery improved from 18/45 to 27/45 against v1.3 baselines.

---

## v1.3 Benchmark Campaign and Evidence Report (Shipped: 2026-04-15)

**Phases completed:** 5 phases, 5 plans, 0 tasks

**Key accomplishments:**

- Added `smoke`, `standard`, and `showcase` campaign presets with guarded output folders and reproducibility manifests.
- Added tidy CSV exports for run-level metrics, grouped recovery summaries, headline metrics, and failed/unsupported reason tables.
- Generated deterministic SVG figures for recovery rates, losses, Beer-Lambert perturbations, runtime/budget, and failure taxonomy.
- Assembled campaign-root `report.md` files with headline metrics, figure/table links, raw artifact links, exact commands, limitations, and next experiments.
- Committed the v1.3 smoke campaign evidence bundle in `artifacts/campaigns/v1.3-smoke/` and verified the workflow with 45 passing tests.

---

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
