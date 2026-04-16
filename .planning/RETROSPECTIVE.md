# Project Retrospective

*A living document updated after each milestone. Lessons feed forward into future planning.*

## Milestone: v1.3 — Benchmark Campaign and Evidence Report

**Shipped:** 2026-04-15
**Phases:** 5 | **Plans:** 5 | **Sessions:** 1

### What Was Built

- Campaign presets for smoke, standard, and showcase benchmark runs.
- Campaign folders with raw run artifacts, aggregate JSON/Markdown, tidy CSVs, SVG figures, manifest, and `report.md`.
- A committed smoke evidence bundle at `artifacts/campaigns/v1.3-smoke/`.
- Documentation for command usage, output schema, plot meanings, and honest interpretation.

### What Worked

- Reusing the benchmark aggregate model kept CSV, plot, and report generation consistent.
- Standard-library CSV and SVG output avoided dependency churn while producing useful artifacts.
- The smoke campaign gave an end-to-end proof without committing a large or slow evidence set.

### What Was Inefficient

- GSD summary extraction did not understand the local summary format, so milestone accomplishments needed manual correction.
- Runtime metrics are read back from raw JSON artifacts; a future aggregate schema could carry timing directly.

### Patterns Established

- Evidence artifacts should keep unsupported and failed cases in the denominator.
- Same-AST warm-start return should remain separate from blind recovery in every table, chart, and report.
- Static reports are enough to validate metric choices before building dashboards.

### Key Lessons

1. The next useful technical work is optimizer/compiler improvement, not more reporting infrastructure.
2. Every future algorithm change should rerun the same campaign presets for before/after comparison.
3. Report generation should be treated as part of the benchmark contract, not as a manually edited artifact.

### Cost Observations

- Model mix: local Codex orchestration with no external subagents.
- Sessions: 1
- Notable: Phase-sized commits kept recovery straightforward despite a broad milestone.

---

## Milestone: v1.6 — Hybrid Search Pipeline and Exact Candidate Recovery

**Shipped:** 2026-04-16
**Phases:** 5 | **Plans:** 5 | **Sessions:** 2

### What Was Built

- Verifier-gated exact-candidate pooling across restarts and hardening checkpoints.
- Target-free low-margin snap-neighborhood cleanup with fallback-preserving exact candidate artifacts.
- Post-snap constant refit and richer `exp`/`log` anomaly diagnostics.
- Macro-aware compiler shortening with conservative warm-start coverage expansion.
- Regime-aware proof/campaign reports, immutable anchor locks, and final `artifacts/proof/v1.6` evidence bundle.

### What Worked

- Treating the optimizer as a candidate generator kept final recovery decisions verifier-owned.
- Preserving fallback candidates made hybrid-stage upgrades safer to evaluate.
- Report-level regression tests caught publication-facing truthfulness issues before closeout.
- Checking report mtimes and aggregates prevented mixed-provenance proof artifacts from being mistaken for final evidence.

### What Was Inefficient

- The final proof bundle had to be rerun multiple times because report prose defects were found only during artifact inspection.
- The GSD `audit-open` command failed with `output is not defined`, so open-artifact audit could not be used as intended.
- Large proof/campaign artifacts make closeout slower and should be frozen deliberately before paper work begins.

### Patterns Established

- Every recovery claim must identify its evidence regime: pure blind, scaffolded blind, warm start, compile-only, catalog, or perturbed basin.
- Human-readable reports must be checked against aggregate JSON before they are cited.
- Publication evidence should be generated from a final code state and then locked with hashes.

### Key Lessons

1. The paper should frame EML training as a verified pipeline with separated evidence regimes, not as universal blind symbolic regression.
2. Pure-blind weakness is a useful scientific result and should remain visible in the manuscript.
3. Claims-to-evidence mapping should happen before any further optimizer work.

### Cost Observations

- Model mix: local Codex orchestration with focused terminal verification.
- Sessions: 2
- Notable: The long proof reruns were worth doing before tagging because they caught a final publication-facing typo and locked the authoritative evidence bundle.

---

## Cross-Milestone Trends

### Process Evolution

| Milestone | Sessions | Phases | Key Change |
|-----------|----------|--------|------------|
| v1.1 | 1 | 6 | Compiler warm starts moved claims from catalog verification to trained exact EML recovery. |
| v1.2 | 1 | 5 | Benchmark evidence replaced anecdotal training checks. |
| v1.3 | 1 | 5 | Campaign reports made benchmark evidence presentation-ready. |
| v1.6 | 2 | 5 | Hybrid exact-candidate recovery and regime-aware proof evidence became paper-grade. |

### Cumulative Quality

| Milestone | Tests | Coverage | Zero-Dep Additions |
|-----------|-------|----------|-------------------|
| v1.1 | 24 | Focused regression coverage | Compiler metadata and warm-start manifests |
| v1.2 | 38 | Benchmark contract and runner coverage | Aggregate Markdown evidence |
| v1.3 | 45 | Campaign, CSV, plot, report, and CLI coverage | CSV export, SVG figures, Markdown report |
| v1.6 | 120+ | Candidate pooling, cleanup, refit, compiler, campaign, proof, and report coverage | Hash-locked proof and comparison artifacts |

### Top Lessons

1. Recovery claims stay credible only when the verifier owns the final status.
2. Measurement should precede optimizer changes when the failure modes are not yet clear.
3. Reproducible artifacts are more useful than one-off demo output for this project.
4. Manuscript claims should be written from aggregate-backed evidence rows, not from narrative report prose alone.
