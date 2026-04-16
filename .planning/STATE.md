---
gsd_state_version: 1.0
milestone: v1.8
milestone_name: Centered-Family Viability and Full Evidence Run
current_phase: null
status: defining_requirements
stopped_at: v1.8 milestone started; defining requirements and roadmap
last_updated: "2026-04-16T21:29:00Z"
last_activity: 2026-04-16 -- v1.8 milestone started
progress:
  total_phases: 0
  completed_phases: 0
  total_plans: 0
  completed_plans: 0
  percent: 0
---

# GSD State: EML Symbolic Regression

**Initialized:** 2026-04-15
**Current phase:** Not started
**Mode:** YOLO

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-04-16)

**Core value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.
**Current focus:** v1.8 Centered-Family Viability and Full Evidence Run.

## Current Position

Phase: Not started (defining requirements)
Plan: —
Status: Defining requirements
Last activity: 2026-04-16 -- v1.8 milestone started
Progress: [----------] 0% by completed phases (v1.8 roadmap pending)

## Performance Metrics

**Velocity:**

- Total plans completed: Historical v1 through v1.5 milestones complete, plus 5 plans completed in v1.6.
- Average duration: Not tracked
- Total execution time: Not tracked

**Recent Trend:**

- v1.5 proved that representation and verifier contracts are strong while pure-blind shallow recovery remains weak (`2/18`) and deeper blind recovery degrades after depth 3.
- v1.5 scaffolded shallow proof reached `18/18`, and perturbed basin proof reached `9/9`, showing that basin return is much stronger than blind discovery.
- v1.6 delivered search-quality upgrades that weakly dominate the prior exact-candidate selector on declared paths while keeping archived baselines intact.
- v1.7 built centered/scaled operator-family infrastructure but did not run the full centered-family evidence matrix.
- A quick post-v1.7 `family-smoke` run showed raw EML recovering the smoke `exp` blind and Beer-Lambert warm-start paths, while centered blind `exp` variants failed and centered warm-starts were unsupported. v1.8 therefore starts with triage and blocker fixes before full campaigns.

## Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Project context | `.planning/PROJECT.md` | Complete |
| Workflow config | `.planning/config.json` | Complete |
| Milestone log | `.planning/MILESTONES.md` | Complete |
| v1.4 comparison report | `artifacts/campaigns/v1.4-comparison/comparison.md` | Complete |
| v1.5 proof report | `artifacts/proof/v1.5/proof-report.md` | Complete |
| v1.6 proof report | `artifacts/proof/v1.6/proof-report.md` | Complete |
| v1.6 proof manifest and anchor locks | `artifacts/proof/v1.6/proof-campaign.json`, `artifacts/proof/v1.6/anchor-locks.json` | Complete |
| v1.5 milestone audit | `.planning/v1.5-MILESTONE-AUDIT.md` | Complete |
| v1.5 archived requirements | `.planning/milestones/v1.5-REQUIREMENTS.md` | Complete |
| v1.5 archived roadmap | `.planning/milestones/v1.5-ROADMAP.md` | Complete |
| v1.5 archived phase context | `.planning/milestones/v1.5-phases/` | Complete |
| v1.6 archived requirements | `.planning/milestones/v1.6-REQUIREMENTS.md` | Complete |
| v1.6 archived roadmap | `.planning/milestones/v1.6-ROADMAP.md` | Complete |
| v1.6 milestone audit | `.planning/milestones/v1.6-MILESTONE-AUDIT.md` | Complete |
| v1.6 archived phase artifacts | `.planning/milestones/v1.6-phases/` | Complete |
| v1.7 project context | `.planning/PROJECT.md` | Complete |
| v1.7 archived requirements | `.planning/milestones/v1.7-REQUIREMENTS.md` | Complete |
| v1.7 archived roadmap | `.planning/milestones/v1.7-ROADMAP.md` | Complete |
| v1.7 archived phase artifacts | `.planning/milestones/v1.7-phases/` | Complete |
| v1.7 paper decision package | `artifacts/paper/v1.7/` | Complete |
| v1.7 milestone audit | `.planning/milestones/v1.7-MILESTONE-AUDIT.md` | Complete |
| v1.8 project context | `.planning/PROJECT.md` | In Progress |

## Completed Milestone

**v1.7: Centered-Family Baseline and Paper Decision**

Goal: Determine whether centered/scaled transport families materially improve exact symbolic recovery relative to raw EML while preserving verifier-owned evidence discipline.

Target features:

- Family-aware semantics and exact AST support for raw EML, `cEML_{s,t}`, `CEML_s`, and `ZEML_s`.
- Family-aware soft master tree, snapping, verification, compiler, and warm-start support.
- Raw-vs-centered proof and campaign matrix with fixed `s` grids and continuation schedules.
- Comparative evidence bundle for recovery rates, depth behavior, anomalies, repair/refit dependence, and formula overhead.
- Decision memo choosing between a publish-now robustness/geometry paper and a later successor-family paper requiring constructive completeness evidence.

## Current Milestone

**v1.8: Centered-Family Viability and Full Evidence Run**

Goal: Determine whether centered/scaled operator families are actually viable improvements over raw EML after fixing missing integration support, calibrating the family grid, running full evidence campaigns, and regenerating the paper decision artifacts.

Target work:

- Smoke triage and missing-support audit for centered-family failures.
- Centered warm-start, compiler-seed, initializer, and schedule fixes or explicit gates.
- Expanded fixed-`s` and continuation experiment matrix.
- Full family campaigns with archived aggregates, tables, figures, and regression locks.
- Refreshed paper decision package grounded in actual centered-family aggregates.

## Phase Status

| Phase | Name | Status | Requirements |
|-------|------|--------|--------------|
| TBD | Requirements and roadmap pending | Pending | TBD |

## Accumulated Context

### Decisions

- v1.4 changed measured performance, not the definition of `recovered`.
- v1.4 used committed v1.3 `standard` and `showcase` campaigns as before/after baselines.
- Phase 25 primitive scaffolds are paper-grounded default initializers, not a relaxed recovery contract.
- Phase 26 records high-noise Beer-Lambert failures as active-slot perturbation instead of hiding them.
- Phase 27 compiler expansion remains fail-closed and validates Shockley before accepting it.
- Phase 28 comparison shows overall v1.4 recovery improved from 18/45 to 27/45 across standard and showcase campaigns.
- v1.5 interprets "100% fully functional training" as 100% recovery over explicitly declared bounded proof suites, plus honest measured failure boundaries for deeper blind recovery.
- Phase 29 established the v1.5 proof contract: stable paper claim matrix, deterministic proof dataset manifests, proof-aware benchmark artifacts, derived evidence classes, claim-level threshold summaries, CLI inspection commands, and campaign proof metadata/reporting.
- Phase 30 review CR-01 is resolved by splitting the shallow claim contract: `paper-shallow-blind-recovery` is now a measured pure random-initialized blind boundary with scaffold initializers disabled, and `paper-shallow-scaffolded-recovery` owns the bounded 100% scaffolded proof suite.
- Phase 31 completed and verified perturbed true-tree basin recovery, verifier-gated local repair, and durable Beer-Lambert bound evidence. BASN-01 through BASN-05 are complete.
- Phase 32 completed a deterministic exact depth inventory, a measured `proof-depth-curve` suite, per-depth blind-versus-perturbed summaries, and campaign report hooks that preserve deeper blind failures as expected paper-boundary evidence.
- Phase 33 completed the one-command `proof-campaign` bundle rooted at `artifacts/proof/v1.5/`, keeping v1.5 proof denominators separate from v1.4 showcase baselines and carrying forward the perturbed basin bound report.
- v1.6 begins from the proof-bundle evidence that representation is strong but blind search quality is still the dominant bottleneck.
- v1.6 will prioritize weak-dominance upgrades first: exact-candidate pooling, discrete cleanup, refit, and compiler shortening must preserve the current exact candidate as fallback on declared benchmark paths.
- Phase 34 added explicit late hardening checkpoints, retained exact-candidate pooling, verifier-gated selection, and serialized legacy fallback provenance across blind, warm-start, basin, benchmark, and CLI flows.
- Phase 35 added replayable active-slot alternatives, bounded exact-AST-deduplicated neighborhood expansion, target-free cleanup, and repair artifacts for blind, warm-start, and perturbed-basin flows while preserving the original selected candidate manifest.
- Phase 36 added frozen exact-tree constant refit, pre/post refit benchmark artifacts, richer exp/log anomaly stats, and optional training-only log-safety penalties while keeping verification semantics faithful after snapping.
- Phase 37 added explicit compiler macro diagnostics, a direct-division shortening path for true denominator motifs, CLI parity for unsupported compiler diagnostics, and verified Shockley warm-start coverage in the standard benchmark matrix while Michaelis-Menten and Planck remain fail-closed at the shipped compile gate.
- Phase 38 added explicit regime summaries to campaign/proof reports, generic comparison lock manifests, corrected measured proof verdict labeling, and aggregate-level regression locks for selection/fallback/refit metrics.
- The final v1.6 proof bundle was regenerated from the latest code state after fixing pure-blind report pluralization; manifest counts match campaign aggregates, pure-blind reports `2/18` threshold-eligible pure blind recoveries plus one repaired candidate, proof-basin reports `9/9` same-AST perturbed-tree returns, and anchor locks cover the five current proof campaigns plus v1.5/v1.4 anchors.
- v1.7 pivots from raw-EML optimizer-only tuning to a centered/scaled operator-family comparison because the archived proof evidence points to search geometry as the main unresolved bottleneck.
- `CEML_s` and `ZEML_s` must be kept distinct: `CEML_s` is the unit-terminal/formal successor candidate, while `ZEML_s` is the training-centered variant and must not be overclaimed as a completeness replacement.
- Phase 39 added operator-family metadata, centered `expm1`/`log1p` semantics, exact centered ASTs, mpmath/SymPy export, and shifted-singularity diagnostics while preserving raw EML defaults.
- Phase 40 threaded operator-family selection and scheduled continuation metadata through the soft master tree, optimizer manifests, warm-start/basin probes, repair neighborhoods, benchmark budgets, campaign CSV rows, and public package exports while preserving raw EML defaults.
- Phase 41 added v1.7 family benchmark suites and campaign presets for raw, fixed centered, and scheduled continuation variants across smoke, shallow, basin, depth-curve, standard, and showcase-style matrices without reusing archived proof thresholds.
- Phase 42 added operator-family recovery, diagnostics, comparison Markdown, and regression-lock JSON outputs to campaign tables and reports, including centered anomaly counters and active-node/complexity summaries.
- Phase 43 added a reproducible paper decision package generator and generated `artifacts/paper/v1.7/`, with the current decision set to wait for centered-family campaign evidence while preserving raw-EML searchability as a viable paper note.
- v1.8 should not start by launching every full family campaign. It should first turn the quick `family-smoke` failures into actionable fixes or explicit exclusions so the expensive runs answer centered-family viability rather than known missing integration.

### Pending Todos

None recorded.

### Blockers/Concerns

The milestone must not claim universal blind recovery of arbitrary deep elementary expressions or completeness of the centered/scaled family unless v1.8 produces direct evidence. Centered warm-start support, initializer/schedule behavior, and the fixed-`s` grid must be resolved before full campaigns are used for paper claims.

### Quick Tasks Completed

| # | Description | Date | Commit | Directory |
|---|-------------|------|--------|-----------|
| 260415-wkr | Resolve Phase 30 by splitting pure blind and scaffolded shallow recovery claims | 2026-04-15 | 653979d | [260415-wkr-resolve-phase-30-by-splitting-pure-blind](./quick/260415-wkr-resolve-phase-30-by-splitting-pure-blind/) |

## Session Continuity

Last session: 2026-04-16
Stopped at: v1.8 milestone started; requirements and roadmap pending
Resume file: None

---
*Last updated: 2026-04-16 after starting v1.8*
