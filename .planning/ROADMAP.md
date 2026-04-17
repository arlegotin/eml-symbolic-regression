# Roadmap: EML Symbolic Regression

**Updated:** 2026-04-17
**Current milestone:** v1.9 Raw-EML Hybrid Recovery and Paper Suite
**Phase numbering:** Continues from v1.8; v1.9 starts at Phase 49.

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
- **v1.9 Raw-EML Hybrid Recovery and Paper Suite** - Phases 49-53 planned

## Milestone Goal

Produce a stronger raw-EML hybrid paper package by fixing centered scaffold correctness, adding Arrhenius exact recovery, materially improving Michaelis-Menten support, expanding exact cleanup, and generating a regime-separated paper-facing campaign.

## Planned Phases

| Phase | Name | Goal | Requirements | Status |
|-------|------|------|--------------|--------|
| 49 | Witness Registry and Centered Scaffold Correctness | 2/2 | Complete    | 2026-04-17 |
| 50 | Arrhenius Exact Warm-Start Demo | 2/3 | In Progress|  |
| 51 | Reciprocal and Saturation Compiler Motifs | Add reusable reciprocal-shift and saturation-ratio compiler motifs to reduce Michaelis-Menten depth and support honest recovery diagnostics. | MIC-01, MIC-02, MIC-03, MIC-04 | Not Started |
| 52 | Verifier-Gated Exact Cleanup Expansion | Broaden exact post-snap cleanup over deduplicated candidate neighborhoods while preserving verifier-owned fallback behavior. | REP-01, REP-02, REP-03, REP-04 | Not Started |
| 53 | Raw-Hybrid Paper Campaign and Claim Package | Generate the paper-facing raw-hybrid suite, reports, tables, claim boundaries, and docs after the new evidence exists. | RHY-01, RHY-02, RHY-03, RHY-04, RHY-05 | Not Started |

- [x] **Phase 49: Witness Registry and Centered Scaffold Correctness** - Make scaffold/witness availability explicit by operator family and prevent raw witnesses from contaminating centered-family runs. (requirements: WIT-01, WIT-02, WIT-03, WIT-04) (completed 2026-04-17)
- [ ] **Phase 50: Arrhenius Exact Warm-Start Demo** - Add Arrhenius as a normalized scientific-law demo with strict compile support and exact verified warm-start return. (requirements: ARR-01, ARR-02, ARR-03, ARR-04)
- [ ] **Phase 51: Reciprocal and Saturation Compiler Motifs** - Add reusable reciprocal-shift and saturation-ratio compiler motifs to reduce Michaelis-Menten depth and support honest recovery diagnostics. (requirements: MIC-01, MIC-02, MIC-03, MIC-04)
- [ ] **Phase 52: Verifier-Gated Exact Cleanup Expansion** - Broaden exact post-snap cleanup over deduplicated candidate neighborhoods while preserving verifier-owned fallback behavior. (requirements: REP-01, REP-02, REP-03, REP-04)
- [ ] **Phase 53: Raw-Hybrid Paper Campaign and Claim Package** - Generate the paper-facing raw-hybrid suite, reports, tables, claim boundaries, and docs after the new evidence exists. (requirements: RHY-01, RHY-02, RHY-03, RHY-04, RHY-05)

## Phase Details

### Phase 49: Witness Registry and Centered Scaffold Correctness

**Goal:** Make scaffold/witness availability explicit by operator family and prevent raw witnesses from contaminating centered-family runs.

**Why first:** Centered-family evidence remains partly confounded while raw `exp`/`log` scaffold helpers can be reused under centered semantics. This must be fixed before new centered conclusions and before adding richer raw motifs.

**Success criteria:**
1. A witness registry declares scaffold availability by operator family.
2. Raw `exp`, `log`, and `scaled_exp` scaffolds are available for raw EML only unless a same-family witness is explicitly registered.
3. Raw scaffold helpers fail closed or are no longer directly callable under centered families.
4. Optimizer and benchmark manifests expose centered scaffold exclusions with reason codes.

**Requirements:** WIT-01, WIT-02, WIT-03, WIT-04

**Plans:** 2/2 plans complete

Plans:
- [x] 49-01-PLAN.md — Add the raw-only scaffold witness registry and route benchmark budget filtering through it.
- [x] 49-02-PLAN.md — Close direct optimizer/helper bypasses and prove centered scaffold exclusions survive artifacts.

### Phase 50: Arrhenius Exact Warm-Start Demo

**Goal:** Add Arrhenius as a normalized scientific-law demo with strict compile support and exact verified warm-start return.

**Why now:** Arrhenius is the clearest low-risk new scientific-law win: it is normalized, domain-safe away from zero, strictly compilable under current diagnostics, and already has review-time evidence for same-AST warm-start return.

**Success criteria:**
1. `arrhenius` exists as a built-in demo dataset with positive train, held-out, and extrapolation domains.
2. Strict compiler diagnostics report support within the current depth gate and include `direct_division_template`.
3. Zero-noise compiler warm-start returns the same exact AST and verifier status `recovered`.
4. A reproducible artifact/report path records compile depth, warm-start status, verifier status, and evidence regime.

**Requirements:** ARR-01, ARR-02, ARR-03, ARR-04

**Plans:** 2/3 plans executed

Plans:
- [x] 50-01-PLAN.md - Add normalized Arrhenius demo and strict same-AST warm-start/CLI tests.
- [x] 50-02-PLAN.md - Add focused Arrhenius benchmark suite and artifact regression tests.
- [ ] 50-03-PLAN.md - Generate focused evidence artifact and document regime-safe commands.

### Phase 51: Reciprocal and Saturation Compiler Motifs

**Goal:** Add reusable reciprocal-shift and saturation-ratio compiler motifs to reduce Michaelis-Menten depth and support honest recovery diagnostics.

**Why now:** Michaelis-Menten is the highest-value medium-difficulty target because it is scientifically recognizable and currently close to the support gate. A reciprocal-shift macro is the most concrete compiler opportunity identified by the review.

**Success criteria:**
1. Reciprocal-shift motifs such as `1/(x+b)` are supported or fail closed with improved diagnostics.
2. Saturation-ratio motifs such as `(a*x)/(b+x)` use reusable compiler logic rather than formula-specific hardcoding.
3. Before/after diagnostics record depth, node count, rule trace, and macro hits for reciprocal shift and Michaelis targets.
4. Michaelis-Menten is exact-recovered if strict support reaches the gate; otherwise the milestone records a material depth reduction and honest unsupported status.

**Requirements:** MIC-01, MIC-02, MIC-03, MIC-04

### Phase 52: Verifier-Gated Exact Cleanup Expansion

**Goal:** Broaden exact post-snap cleanup over deduplicated candidate neighborhoods while preserving verifier-owned fallback behavior.

**Why now:** Existing evidence shows soft fits often snap to stable but wrong exact corners. A larger, verifier-gated exact cleanup neighborhood is directly targeted at those symbolic selection failures.

**Success criteria:**
1. Cleanup can consider selected, fallback, and retained exact candidates where candidate pool provenance is available.
2. Cleanup defaults or presets allow a larger deduplicated neighborhood than the v1.6/v1.8 configuration while remaining bounded.
3. Subtree-level alternatives are used when provenance exposes them.
4. Targeted before/after artifacts show whether repair improves near-miss subsets without weakening fallback behavior.

**Requirements:** REP-01, REP-02, REP-03, REP-04

### Phase 53: Raw-Hybrid Paper Campaign and Claim Package

**Goal:** Generate the paper-facing raw-hybrid suite, reports, tables, claim boundaries, and docs after the new evidence exists.

**Why last:** Paper artifacts should follow real code and campaign evidence. This phase packages the results without blurring evidence regimes or overselling warm-start recovery as blind discovery.

**Success criteria:**
1. A raw-hybrid paper suite includes shallow blind boundaries, perturbed basin evidence, Beer-Lambert, Shockley, Arrhenius, and Michaelis diagnostics.
2. Reports keep pure blind, scaffolded, compile-only, warm-start, same-AST return, repaired, refit, and perturbed-basin regimes separate.
3. Scientific-law tables include formula, compile support, depth, macro hits, warm-start status, verifier status, and artifact paths.
4. Centered-family material is framed as negative diagnostic evidence with same-family witness caveats.
5. README/docs updates cite successful artifacts and avoid blind-discovery overclaims.

**Requirements:** RHY-01, RHY-02, RHY-03, RHY-04, RHY-05

## Coverage

| Requirement | Phase | Status |
|-------------|-------|--------|
| WIT-01 | Phase 49 | Complete |
| WIT-02 | Phase 49 | Complete |
| WIT-03 | Phase 49 | Complete |
| WIT-04 | Phase 49 | Complete |
| ARR-01 | Phase 50 | Pending |
| ARR-02 | Phase 50 | Pending |
| ARR-03 | Phase 50 | Pending |
| ARR-04 | Phase 50 | Pending |
| MIC-01 | Phase 51 | Pending |
| MIC-02 | Phase 51 | Pending |
| MIC-03 | Phase 51 | Pending |
| MIC-04 | Phase 51 | Pending |
| REP-01 | Phase 52 | Pending |
| REP-02 | Phase 52 | Pending |
| REP-03 | Phase 52 | Pending |
| REP-04 | Phase 52 | Pending |
| RHY-01 | Phase 53 | Pending |
| RHY-02 | Phase 53 | Pending |
| RHY-03 | Phase 53 | Pending |
| RHY-04 | Phase 53 | Pending |
| RHY-05 | Phase 53 | Pending |

**Coverage summary:**
- v1.9 requirements: 21 total
- Mapped to phases: 21
- Unmapped: 0

## Next Step

Start with Phase 49 to fix witness/scaffold correctness before adding raw motifs or paper-facing evidence.

`$gsd-plan-phase 49`

---
*Roadmap created: 2026-04-17 for milestone v1.9*
*Last updated: 2026-04-17 after roadmap creation*
