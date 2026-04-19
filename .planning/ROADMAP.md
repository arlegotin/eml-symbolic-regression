# Roadmap: EML Symbolic Regression

**Updated:** 2026-04-19  
**Current milestone:** v1.12 Paper draft skeleton and refreshed shallow evidence  
**Phase numbering:** Continuing from v1.11 Phase 63.

## Milestones

- **v1.0 MVP** - Phases 1-7 complete (completed 2026-04-15)
- **v1.1 EML Compiler and Warm Starts** - Phases 8-13 complete (completed 2026-04-15; archive: `.planning/milestones/v1.1-ROADMAP.md`)
- **v1.2 Training Benchmark and Recovery Evidence** - Phases 14-18 complete (completed 2026-04-15; archive: `.planning/milestones/v1.2-ROADMAP.md`)
- **v1.3 Benchmark Campaign and Evidence Report** - Phases 19-23 complete (completed 2026-04-15; archive: `.planning/milestones/v1.3-ROADMAP.md`)
- **v1.4 Recovery Performance Improvements** - Phases 24-28 complete (completed 2026-04-15; archive: `.planning/milestones/v1.4-ROADMAP.md`)
- **v1.5 Training Proof and Recovery Guarantees** - Phases 29-33 complete (completed 2026-04-16; archive: `.planning/milestones/v1.5-ROADMAP.md`)
- **v1.6 Hybrid Search Pipeline and Exact Candidate Recovery** - Phases 34-38 complete (completed 2026-04-16; archive: `.planning/milestones/v1.6-ROADMAP.md`)
- **v1.7 Centered-Family Baseline and Paper Decision** - Phases 39-43 complete (completed 2026-04-16; archive: `.planning/milestones/v1.7-ROADMAP.md`)
- **v1.8 Centered-Family Viability and Full Evidence Run** - Phases 44-48 complete (completed 2026-04-17; archive: `.planning/milestones/v1.8-ROADMAP.md`)
- **v1.9 Raw-EML Hybrid Recovery and Paper Suite** - Phases 49-53 complete (completed 2026-04-17; archive: `.planning/milestones/v1.9-ROADMAP.md`)
- **v1.10 Search-backed motif library and compiler shortening for logistic and Planck** - Phases 54-58 complete (completed 2026-04-18; archive: `.planning/milestones/v1.10-ROADMAP.md`)
- **v1.11 Paper-strength evidence and figure package** - Phases 59-63 complete (completed 2026-04-19; archive: `.planning/milestones/v1.11-ROADMAP.md`)
- **v1.12 Paper draft skeleton and refreshed shallow evidence** - Phases 64-68 active

## Current Status

v1.12 is active. The milestone turns `artifacts/paper/v1.11/` into a paper-shaped draft package, refreshes the small but reviewer-visible shallow/depth evidence, adds paper-facing motif/pipeline/negative-result/taxonomy artifacts, and keeps optional baseline and logistic strict-support probes bounded.

## Active v1.12 Phases

### Phase 64: Draft Skeleton and Claim Taxonomy

**Goal:** Convert the v1.11 package into the first paper-shaped draft scaffold with claim boundaries visible from the start.

**Scope:**
- Create `artifacts/paper/v1.11/draft/` and section skeletons for abstract, methods, results, and limitations.
- Use `paper-readiness.md`, `claim-audit.json`, existing figures/tables, and source locks as the draft's evidence base.
- Add a paper-facing claim taxonomy table separating pure blind, scaffolded, warm-start, same-AST, perturbed-basin, repair/refit, compile-only, unsupported, and failed evidence classes.
- Ensure draft language does not promote logistic or Planck from relaxed-depth improvement alone.

**Requirements:** DRAFT-01, DRAFT-03, FIG-04

**Success criteria:**
1. Draft section files exist under `artifacts/paper/v1.11/draft/`.
2. The claim taxonomy table defines denominator eligibility and safe public claim language.
3. Draft text references the v1.11 source package and preserves regime separation.
4. Logistic and Planck remain unsupported unless strict support evidence is actually produced later.

### Phase 65: Shallow Seed and Depth-Curve Refresh

**Goal:** Add small current-code evidence refreshes that strengthen the bounded shallow recovery and depth-limit story.

**Scope:**
- Run additional shallow pure-blind seeds and additional shallow scaffolded seeds, targeting five to ten new seeds per regime while keeping runs cheap.
- Run a current-code depth refresh over depths 2 through 5 with at least two seeds per depth.
- Write aggregate tables with seeds, budgets, depth, start mode, evidence class, verifier outcome, failure/unsupported reason, and artifact paths.
- Preserve archived v1.6 depth evidence as historical context while labeling v1.12 current-code rows separately.

**Requirements:** EVID-01, EVID-02, EVID-03

**Success criteria:**
1. Shallow refresh artifacts include at least five new pure-blind seeds and five new scaffolded seeds or explicit runtime failure notes.
2. Depth refresh artifacts cover depths 2, 3, 4, and 5 with at least two seeds each.
3. Aggregates keep regimes and denominators separate.
4. Source tables can drive updated depth and shallow-recovery paper figures without hidden recomputation.

### Phase 66: Paper-Facing Figures, Captions, and Negative Results

**Goal:** Make the paper visually and tabularly legible with motif evolution, pipeline, captions, and explicit negative-result framing.

**Scope:**
- Add figure and table captions under the draft package with source references.
- Add a motif library evolution figure or table with before/after examples for logistic, Planck, Shockley, Arrhenius, and Michaelis-Menten where source evidence exists.
- Add one visual EML tree or pipeline figure covering data, soft complete EML tree, snap, candidate pool/repair/refit, and verifier.
- Add a logistic/Planck negative-results table showing compile support, relaxed-depth improvement, blind probe outcome, and promotion status.

**Requirements:** DRAFT-02, FIG-01, FIG-02, FIG-03

**Success criteria:**
1. Caption files cover every paper-facing figure/table produced or reused by the v1.12 package.
2. Motif before/after numbers come from source-locked tables, with Planck depth-convention differences explained if present.
3. The pipeline figure has adjacent metadata or source data and a regeneration command.
4. Logistic and Planck negative rows visibly record no promotion unless strict support and verifier recovery pass.

### Phase 67: Bounded Baseline and Logistic Strict-Support Probes

**Goal:** Attempt the two high-upside but failure-prone upgrades without letting them block the paper skeleton.

**Scope:**
- Check for locally available conventional symbolic-regression tooling, such as PySR or another installed SR comparator.
- If feasible, run one lightweight diagnostic baseline and report it as diagnostic-only.
- If unavailable or installation would become a time sink, record deferred/unavailable status with limitation text.
- Attempt a bounded reusable-motif logistic strict-support push, preserving fail-closed compiler behavior and strict gate honesty.

**Requirements:** BASE-01, COMP-01

**Success criteria:**
1. Baseline status is one of completed, deferred, or unavailable with explicit limitation text.
2. Baseline diagnostics never enter EML recovery denominators.
3. Logistic compiler changes, if any, are structural and validation-gated.
4. Logistic remains unsupported unless strict support and verifier evidence pass.

### Phase 68: Package Assembly, Source Locks, and Claim Audit

**Goal:** Assemble the v1.12 supplement to the v1.11 paper package and verify that all draft claims are source-backed.

**Scope:**
- Update or supplement `artifacts/paper/v1.11/manifest.json`, `source-locks.json`, claim-audit outputs, and reproduction commands for v1.12 additions.
- Source-lock draft skeletons, captions, refreshed evidence, figures, tables, baseline status, and logistic strict-support probe outputs.
- Audit mixed-regime denominator safety, logistic/Planck promotion status, figure/table source coverage, and draft-section presence.
- Update planning docs with actual results and next recommended manuscript work.

**Requirements:** AUDIT-01, AUDIT-02, AUDIT-03

**Success criteria:**
1. All v1.12-added paper artifacts are listed in a manifest or supplement manifest.
2. Claim audit passes or reports actionable blockers without hiding unsupported rows.
3. Reproduction commands distinguish mandatory refreshes from optional/deferred probes.
4. The next phase after v1.12 can focus on manuscript prose rather than evidence organization.

## Execution Order

1. Phase 64
2. Phase 65
3. Phase 66
4. Phase 67
5. Phase 68

## Notes

- Keep `artifacts/paper/v1.11/` as the root requested by the milestone brief, adding `draft/` and v1.12 supplement files rather than mutating source claims invisibly.
- Keep all evidence regimes separate: pure blind, scaffolded, warm-start, same-AST, perturbed-basin, repair/refit, compile-only, unsupported, and failed.
- Prefer small current-code reruns and paper-facing synthesis over broad new campaigns.
- Baseline and logistic strict-support work are high-upside probes, not success preconditions.
- Do not relax strict support gates for logistic or Planck.

---
*Roadmap opened for v1.12 on 2026-04-19*
