---
gsd_state_version: 1.0
milestone: v1.9
milestone_name: milestone
current_phase: 52
status: executing
stopped_at: Completed 52-01-PLAN.md
last_updated: "2026-04-17T15:15:56.628Z"
last_activity: 2026-04-17
progress:
  total_phases: 5
  completed_phases: 3
  total_plans: 11
  completed_plans: 9
  percent: 82
---

# GSD State: EML Symbolic Regression

**Initialized:** 2026-04-15
**Current phase:** 52
**Mode:** YOLO

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-04-17)

**Core value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.
**Current focus:** Phase 52 — Verifier-Gated Exact Cleanup Expansion

## Current Position

Phase: 52 (Verifier-Gated Exact Cleanup Expansion) — EXECUTING
Plan: 2 of 3
Status: Ready to execute
Last activity: 2026-04-17
Progress: [██████----] 60% by completed phases (v1.9: 3/5 complete)

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
- v1.8 produced negative centered-family evidence under scoped local campaigns and selected a raw-EML searchability paper path. v1.9 should now convert that decision into stronger raw-hybrid scientific-law results.

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
| v1.8 project context | `.planning/PROJECT.md` | Complete |
| v1.8 archived requirements | `.planning/milestones/v1.8-REQUIREMENTS.md` | Complete |
| v1.8 archived roadmap | `.planning/milestones/v1.8-ROADMAP.md` | Complete |
| v1.8 archived phase artifacts | `.planning/milestones/v1.8-phases/` | Complete |
| v1.8 milestone audit | `.planning/milestones/v1.8-MILESTONE-AUDIT.md` | Complete |
| v1.9 active requirements | `.planning/REQUIREMENTS.md` | Complete |
| v1.9 active roadmap | `.planning/ROADMAP.md` | Complete |
| Phase 49 P01 | 4 min | 2 tasks | 4 files |
| Phase 49 P02 | 13 min | 3 tasks | 6 files |
| Phase 50 P01 | 4min | 3 tasks | 4 files |
| Phase 50 P02 | 7min | 2 tasks | 4 files |
| Phase 50 P03 | 4min | 2 tasks | 7 files |
| Phase 51 P01 | 8min | 3 tasks | 3 files |
| Phase 51 P02 | 4min | 2 tasks | 4 files |
| Phase 51 P03 | 4min | 2 tasks | 7 files |
| Phase 52 P01 | 9min | 2 tasks | 3 files |

## Completed Milestone

**v1.8: Centered-Family Viability and Full Evidence Run**

Goal: Determine whether centered/scaled operator families are actually viable improvements over raw EML after fixing missing integration support, calibrating the family grid, running full evidence campaigns, and regenerating the paper decision artifacts.

Target features:

- Centered-family smoke triage, calibration, and missing-support gates.
- Explicit fail-closed handling for centered warm-start, compiler-seed, scaffold, and perturbed-tree paths.
- Fixed-scale and continuation family matrix calibration.
- Scoped family evidence campaigns and paper decision artifacts.
- Raw-EML searchability note recommendation with centered results reported as negative diagnostics.

## Current Milestone

**v1.9: Raw-EML Hybrid Recovery and Paper Suite**

Goal: Produce a stronger raw-EML hybrid paper package by fixing centered scaffold correctness, adding Arrhenius exact recovery, materially improving Michaelis-Menten support, expanding exact cleanup, and generating a regime-separated paper-facing campaign.

Target work:

- Add a witness registry and prevent raw `exp`/`log` scaffolds under centered semantics.
- Add Arrhenius as a normalized strict-compile and exact warm-start recovery demo.
- Add reciprocal-shift and saturation compiler motifs for Michaelis-Menten support.
- Expand exact post-snap cleanup with verifier-gated deduped neighborhoods.
- Generate a raw-hybrid paper suite with regime-separated tables, reports, and claim language.

## Phase Status

| Phase | Name | Status | Requirements |
|-------|------|--------|--------------|
| 49 | Witness Registry and Centered Scaffold Correctness | Complete (2/2 plans) | WIT-01, WIT-02, WIT-03, WIT-04 |
| 50 | Arrhenius Exact Warm-Start Demo | Complete (3/3 plans) | ARR-01, ARR-02, ARR-03, ARR-04 |
| 51 | Reciprocal and Saturation Compiler Motifs | Complete (3/3 plans) | MIC-01, MIC-02, MIC-03, MIC-04 |
| 52 | Verifier-Gated Exact Cleanup Expansion | Ready to plan | REP-01, REP-02, REP-03, REP-04 |
| 53 | Raw-Hybrid Paper Campaign and Claim Package | Not Started | RHY-01, RHY-02, RHY-03, RHY-04, RHY-05 |

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
- Phase 44 reproduced expanded v1.8 family smoke evidence, classified centered blind failures and same-family seed gates, and wrote a `conditional_go_scoped` full-run gate.
- Phase 45 made centered warm-start and perturbed-tree unsupported paths explicit via `centered_family_same_family_seed_missing`, scaffold exclusion metadata, and optimizer schedule traces.
- Phase 46 expanded v1.8 family suites to fixed `s in {1,2,4,8}` plus declared ZEML continuation schedules and added focused `family-calibration`.
- Phase 47 ran scoped v1.8 standard evidence after calibration and recorded deliberate scope decisions for larger shallow, basin, depth-curve, and showcase campaigns.
- Phase 48 generated `artifacts/paper/v1.8/` and chose `publish_raw_eml_searchability_note` because raw EML recovered 80.0% across supplied v1.8 aggregates while the best centered recovery rate was 0.0%.
- [Phase 49]: Current exp, log, and scaled_exp scaffold witnesses are registered only for raw_eml.
- [Phase 49]: Centered benchmark variants serialize exp/log/scaled_exp exclusions with centered_family_same_family_witness_missing.
- [Phase 49]: Continuation benchmark variants resolve scaffold availability against the first scheduled operator.
- [Phase 49]: Direct optimizer calls use the initial training operator, not the final hardening operator, to resolve scaffold witness availability.
- [Phase 49]: Centered raw scaffold helper calls fail with EmbeddingError reason centered_family_same_family_witness_missing before slot mutation or embedding.
- [Phase 49]: Benchmark artifacts copy budget scaffold exclusions into trained optimizer manifests when benchmark filtering has already removed the raw scaffold requests.
- [Phase 50]: Arrhenius uses normalized dimensionless input x with formula exp(-0.8/x) and positive domains away from zero.
- [Phase 50]: Strict Arrhenius support is locked through direct_division_template; no Arrhenius-specific compiler branch was added.
- [Phase 50]: Zero-noise Arrhenius warm-start evidence remains same_ast_return / same_ast, not blind discovery.
- [Phase 50]: Arrhenius benchmark evidence is isolated in v1.9-arrhenius-evidence instead of broadening existing campaign denominators.
- [Phase 50]: The arrhenius-warm benchmark path is classified as same_ast, not blind discovery.
- [Phase 50]: Docs cite generated v1.9-arrhenius-evidence artifacts only after JSON validation passed.
- [Phase 50]: Arrhenius is documented as exact compiler warm-start / same-AST basin evidence, not blind discovery.
- [Phase 50]: Michaelis-Menten and Planck remain unsupported/stretch under default compile/warm-start gates.
- [Phase 51]: Reciprocal and saturation motifs match direct SymPy structure only; no demo-name or string hardcoding was added.
- [Phase 51]: Michaelis-Menten is promoted only as compiled same-AST warm-start evidence, not blind discovery.
- [Phase 51]: Arrhenius remains on direct_division_template and Planck remains stretch/unsupported under warm-start promotion.
- [Phase 51]: Michaelis-Menten evidence is isolated in v1.9-michaelis-evidence; broad v1.2/v1.3/v1.8 and paper-facing suites were not expanded.
- [Phase 51]: michaelis-warm is classified as same-AST warm-start evidence, not blind discovery.
- [Phase 51]: Default compile and warm-start gates remain unchanged for Michaelis evidence: max compile depth 13, max compile nodes 256, and max warm depth 14.
- [Phase 51]: Docs cite v1.9-michaelis-evidence only after strict JSON validation of the generated same-AST artifact.
- [Phase 51]: Michaelis-Menten is documented as exact compiler warm-start / same-AST basin evidence, not blind discovery.
- [Phase 51]: Arrhenius same-AST wording is preserved and Planck remains stretch/unsupported under the shipped warm-start gate.
- [Phase 52]: Expanded cleanup is opt-in through RepairConfig.expanded_candidate_pool(); RepairConfig() remains selected-only.
- [Phase 52]: Candidate roots and cleanup variants are deduplicated by serialized exact AST before verifier work.
- [Phase 52]: Repair promotion remains verifier-owned: only a recovered verification report can serialize repaired_ast or accepted root metadata.

### Pending Todos

None recorded.

### Blockers/Concerns

The milestone must not claim universal blind recovery of arbitrary deep elementary expressions or completeness of the centered/scaled family. v1.9 warm-start, scaffolded, perturbed-basin, repair, refit, and pure-blind results must remain separated in every report. Centered empirical scaling remains paused until same-family witnesses exist.

### Quick Tasks Completed

| # | Description | Date | Commit | Directory |
|---|-------------|------|--------|-----------|
| 260415-wkr | Resolve Phase 30 by splitting pure blind and scaffolded shallow recovery claims | 2026-04-15 | 653979d | [260415-wkr-resolve-phase-30-by-splitting-pure-blind](./quick/260415-wkr-resolve-phase-30-by-splitting-pure-blind/) |

## Session Continuity

Last session: 2026-04-17T15:15:56.624Z
Stopped at: Completed 52-01-PLAN.md
Resume file: None

---
*Last updated: 2026-04-17 after completing Phase 51*
