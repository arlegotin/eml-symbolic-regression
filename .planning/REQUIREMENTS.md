# Requirements: v1.12 Paper draft skeleton and refreshed shallow evidence

**Milestone:** v1.12  
**Status:** Active  
**Created:** 2026-04-19  
**Goal:** Turn the v1.11 evidence package into a paper-shaped draft while refreshing the most reviewer-visible shallow/depth evidence and making claim boundaries explicit.

## v1.12 Requirements

### Draft Package

- [x] **DRAFT-01**: The repository provides `artifacts/paper/v1.11/draft/` with paper-section skeletons for abstract, methods, results, and limitations.
- [ ] **DRAFT-02**: The draft package includes figure-caption and table-caption files that reference the relevant v1.11 or v1.12 source artifacts.
- [x] **DRAFT-03**: The draft skeleton converts the v1.11 evidence package into a paper-shaped argument without promoting unsupported logistic or Planck claims.

Acceptance:
- `abstract.md`, `methods.md`, `results.md`, and `limitations.md` exist under `artifacts/paper/v1.11/draft/`.
- Caption artifacts exist under the same draft root, either as `figure-captions.md` and `table-captions.md` or clearly named equivalents.
- Draft text names the evidence regimes it relies on and avoids treating scaffolded, same-AST, warm-start, repair/refit, or perturbed-basin evidence as pure blind discovery.

### Evidence Refresh

- [x] **EVID-01**: Additional shallow current-code runs strengthen the bounded shallow recovery claim with new pure-blind and scaffolded seeds.
- [x] **EVID-02**: A current-code depth-curve refresh measures depths 2 through 5 with at least two seeds per depth.
- [x] **EVID-03**: Refreshed shallow and depth evidence is summarized in source-locked tables that keep regimes, seeds, budgets, and verifier outcomes separate.

Acceptance:
- New shallow-refresh artifacts include at least five additional pure-blind seeds and at least five additional scaffolded seeds unless runtime failure is explicitly recorded.
- Depth-refresh artifacts include depth 2, 3, 4, and 5 rows with at least two seeds each.
- Aggregates record seed, depth where applicable, start mode, evidence class, verifier result, failure/unsupported reason, and artifact path.
- Any figure or table using archived v1.6 depth evidence labels it as archived; any refreshed depth row labels the current code version and command source.

### Paper-Facing Figures and Tables

- [ ] **FIG-01**: The paper package includes a motif library evolution figure or table with before/after examples for logistic, Planck, Shockley, Arrhenius, and Michaelis-Menten where source evidence exists.
- [ ] **FIG-02**: The paper package includes one visual EML tree or pipeline figure showing data -> soft complete EML tree -> snap -> candidate pool/repair/refit -> verifier.
- [ ] **FIG-03**: The paper package includes an explicit logistic/Planck negative-results table covering compile support, relaxed-depth improvement, blind probe outcome, and promotion status.
- [x] **FIG-04**: The paper package includes a claim taxonomy table that separates pure blind, scaffolded, warm-start, same-AST, perturbed-basin, repair/refit, compile-only, unsupported, and failed evidence.

Acceptance:
- Motif before/after values are pulled from source-locked evidence. If Planck depth conventions differ across v1.10/v1.11 tables, the caption explains the convention instead of silently choosing a favorable number.
- The pipeline figure has adjacent source data or metadata and is reproducible by a recorded command.
- The logistic/Planck negative-results table visibly records "promotion: no" unless strict support and verifier recovery pass.
- The claim taxonomy table defines denominator eligibility and paper-safe claim language for each evidence class.

### Bounded Probes

- [ ] **BASE-01**: The milestone attempts one lightweight conventional symbolic-regression baseline if it is already locally available or cheap to install, and otherwise records a deferred/unavailable diagnostic row.
- [ ] **COMP-01**: The milestone attempts one bounded strict-support logistic compiler push using reusable structural motifs only, and records the result without relaxing gates.

Acceptance:
- Conventional baseline output is labeled diagnostic-only and never enters EML recovery denominators.
- If a symbolic baseline dependency is unavailable or installation would become a time sink, the paper package records that fact with limitation text.
- Logistic strict-support work does not introduce formula-name recognizers, exact-constant special cases, or silent strict-gate relaxation.
- Logistic remains unsupported unless the strict compiler support and verifier contract both pass.

### Package Audit

- [ ] **AUDIT-01**: The v1.12 package update source-locks all new draft, table, figure, and evidence-refresh artifacts.
- [ ] **AUDIT-02**: The final audit verifies draft claims, refreshed evidence, negative-result rows, and taxonomy denominators against source artifacts.
- [ ] **AUDIT-03**: Reproduction commands explain how to regenerate or inspect the draft skeleton, refreshed evidence, and added paper-facing assets.

Acceptance:
- `artifacts/paper/v1.11/manifest.json`, `source-locks.json`, or a v1.12 supplement manifest references all new paper-facing artifacts.
- Claim audit output includes checks for mixed-regime denominators, logistic/Planck promotion status, figure/table source coverage, and draft-section presence.
- Reproduction commands distinguish mandatory refresh commands from optional/deferred baseline or strict-support probes.

## Future Requirements

### Manuscript Polish

- **MANU-01**: Expand the draft skeleton into a complete submission-ready manuscript.
- **MANU-02**: Add final narrative prose, related work, bibliography wiring, and venue-specific formatting.

### Broader Comparisons

- **BASE-02**: Run a matched-budget external symbolic-regression comparison after dependencies and benchmark scope are stable.
- **SEARCH-01**: Improve true blind search depth beyond shallow regimes through algorithmic work rather than paper packaging.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Full submission-ready manuscript | v1.12 creates the draft skeleton and paper-facing argument; full prose polish is a later manuscript milestone. |
| Broad matched-budget PySR or external SR competition | Valuable but likely to become a time sink; v1.12 only attempts a lightweight local diagnostic. |
| Relaxing logistic or Planck strict gates | The paper's credibility depends on keeping strict and relaxed support separate. |
| Formula-name compiler recognizers | Compiler improvements must be structural and reusable, not one-off branches for paper rows. |
| Deep blind recovery campaign beyond depth 5 | The requested refresh is small and credibility-focused; broad deep recovery is separate algorithm work. |
| Rewriting archived v1.6/v1.9/v1.10/v1.11 artifacts | Historical artifacts remain source anchors; v1.12 can add current-code supplements but not mutate archives. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| DRAFT-01 | Phase 64 | Complete |
| DRAFT-02 | Phase 66 | Pending |
| DRAFT-03 | Phase 64 | Complete |
| EVID-01 | Phase 65 | Complete |
| EVID-02 | Phase 65 | Complete |
| EVID-03 | Phase 65 | Complete |
| FIG-01 | Phase 66 | Pending |
| FIG-02 | Phase 66 | Pending |
| FIG-03 | Phase 66 | Pending |
| FIG-04 | Phase 64 | Complete |
| BASE-01 | Phase 67 | Pending |
| COMP-01 | Phase 67 | Pending |
| AUDIT-01 | Phase 68 | Pending |
| AUDIT-02 | Phase 68 | Pending |
| AUDIT-03 | Phase 68 | Pending |

**Coverage:**
- v1.12 requirements: 15 total
- Mapped to phases: 15
- Unmapped: 0

---
*Requirements defined: 2026-04-19*
*Last updated: 2026-04-19 after creating v1.12 roadmap*
