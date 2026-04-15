# Requirements: EML Symbolic Regression Milestone v1.3

**Defined:** 2026-04-15
**Milestone:** v1.3 Benchmark Campaign and Evidence Report
**Core Value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.

## Milestone v1.3 Requirements

Requirements for this milestone only. Completed v1, v1.1, and v1.2 requirements are recorded as validated capabilities in `.planning/PROJECT.md`.

### Campaign Execution

- [ ] **CAMP-01**: User can run named campaign presets (`smoke`, `standard`, `showcase`) that select benchmark suites, budget tiers, seeds, and output folders without hand-writing filters.
- [ ] **CAMP-02**: User can generate a versioned campaign output directory containing raw run artifacts, suite results, aggregate reports, a campaign manifest, and reproducibility metadata.
- [ ] **CAMP-03**: User can run a standard campaign that includes shallow blind baselines, Beer-Lambert perturbation sweeps, Michaelis-Menten diagnostics, Planck diagnostics, and selected FOR_DEMO cases.
- [ ] **CAMP-04**: User can rerun a campaign without silently overwriting prior evidence, either by creating a new timestamped/versioned folder or explicitly allowing overwrite.
- [ ] **CAMP-05**: User receives clear runtime/budget guardrails so smoke tests stay fast while showcase campaigns can be larger and explicit.

### Data Export

- [ ] **DATA-01**: User receives a tidy run-level CSV containing formula, start mode, seed, depth, steps, perturbation noise, best loss, post-snap loss, verifier status, recovery class, runtime, changed slots, and artifact path.
- [ ] **DATA-02**: User receives grouped CSV summaries for recovery rate by formula, start mode, perturbation level, depth, and failure class.
- [ ] **DATA-03**: User receives a headline metrics JSON/CSV table with total runs, verifier recovery rate, unsupported rate, failure rate, same-AST return rate, median losses, and runtime summaries.
- [ ] **DATA-04**: User can export unsupported and failed cases with reason codes and links back to the source run artifacts.

### Plot Generation

- [ ] **PLOT-01**: User can generate a recovery-rate chart by formula and start mode.
- [ ] **PLOT-02**: User can generate a loss comparison chart showing best soft loss versus post-snap loss on a log scale where appropriate.
- [ ] **PLOT-03**: User can generate a Beer-Lambert perturbation chart showing recovery class and changed-slot behavior by perturbation noise.
- [ ] **PLOT-04**: User can generate runtime and depth/budget charts that make practical cost visible.
- [ ] **PLOT-05**: User can generate an unsupported/failure taxonomy chart by formula and recovery class.
- [ ] **PLOT-06**: User receives deterministic figure files with stable names suitable for linking from a Markdown report.

### Evidence Report

- [ ] **REPT-01**: User receives a self-contained `report.md` in the campaign folder with headline metrics, tables, figures, commands, and links to raw artifacts.
- [ ] **REPT-02**: User can read a concise narrative explaining what the paper's EML idea demonstrates well in this implementation.
- [ ] **REPT-03**: User can read limitations that separate blind recovery, same-AST warm-start return, verified-equivalent warm-start recovery, unsupported depth/compiler gates, and failed fits.
- [ ] **REPT-04**: User receives a short "next experiments" section that turns measured failures into optimizer or compiler improvement priorities.
- [ ] **REPT-05**: User can reproduce the report by rerunning one documented CLI command from a clean checkout.

### Tests and Documentation

- [ ] **TEST-11**: User can run focused tests for campaign preset expansion, output folder creation, overwrite protection, CSV export, and headline metrics.
- [ ] **TEST-12**: User can run focused tests for plot file generation and report assembly using CI-scale benchmark fixtures.
- [ ] **TEST-13**: User can read documentation describing campaign commands, output structure, CSV schemas, plot meanings, and how to present results honestly.

## Future Requirements

Deferred to later milestones.

### Optimization and Showcase Expansion

- **FUT-11**: User can improve optimizer robustness for slot-changing perturbations using the v1.3 scoreboard as a before/after baseline.
- **FUT-12**: User can reduce compiled arithmetic tree depth or improve compiler templates to promote Michaelis-Menten beyond diagnostics.
- **FUT-13**: User can add interactive dashboards after static reports prove the right metrics and plots.
- **FUT-14**: User can add external real-world datasets after synthetic/source-document campaign reporting is stable.
- **FUT-15**: User can compare EML recovery against other symbolic-regression baselines.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Optimizer redesign | v1.3 should create the scoreboard before changing the algorithm. |
| Hiding weak results | The milestone exists to show both promise and limitations clearly. |
| Interactive dashboard | Static CSV, PNG/SVG, and Markdown reports are enough for a crisp showcase. |
| External noisy datasets | First showcase the paper-derived demos and current synthetic benchmarks reproducibly. |
| Claiming general real-world symbolic-regression superiority | The report should describe current evidence, not overgeneralize. |
| Manually edited figures | Plots must be generated from campaign artifacts so future runs are comparable. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| CAMP-01 | Phase 19 | Pending |
| CAMP-02 | Phase 19 | Pending |
| CAMP-03 | Phase 19 | Pending |
| CAMP-04 | Phase 19 | Pending |
| CAMP-05 | Phase 19 | Pending |
| DATA-01 | Phase 20 | Pending |
| DATA-02 | Phase 20 | Pending |
| DATA-03 | Phase 20 | Pending |
| DATA-04 | Phase 20 | Pending |
| PLOT-01 | Phase 21 | Pending |
| PLOT-02 | Phase 21 | Pending |
| PLOT-03 | Phase 21 | Pending |
| PLOT-04 | Phase 21 | Pending |
| PLOT-05 | Phase 21 | Pending |
| PLOT-06 | Phase 21 | Pending |
| REPT-01 | Phase 22 | Pending |
| REPT-02 | Phase 22 | Pending |
| REPT-03 | Phase 22 | Pending |
| REPT-04 | Phase 22 | Pending |
| REPT-05 | Phase 22 | Pending |
| TEST-11 | Phase 23 | Pending |
| TEST-12 | Phase 23 | Pending |
| TEST-13 | Phase 23 | Pending |

**Coverage:**
- v1.3 requirements: 23 total
- Mapped to phases: 23
- Unmapped: 0

---
*Requirements defined: 2026-04-15*
*Last updated: 2026-04-15 after milestone v1.3 roadmap creation*
