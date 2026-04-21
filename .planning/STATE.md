---
gsd_state_version: 1.0
milestone: v1.14
milestone_name: Evidence claim integrity and audit hardening
current_phase: 81
current_phase_name: "Corrected Evidence Rebuild and Claim Audit"
status: v1.14 phases complete
stopped_at: phase 81 complete
last_updated: "2026-04-21T11:45:00.000Z"
last_activity: 2026-04-21
progress:
  total_phases: 5
  completed_phases: 5
  total_plans: 5
  completed_plans: 5
  percent: 100
---

# GSD State: EML Symbolic Regression

**Initialized:** 2026-04-15
**Current phase:** Phase 81 - Corrected Evidence Rebuild and Claim Audit
**Mode:** YOLO

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-04-21)

**Core value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.
**Current focus:** v1.14 claim-accounting repair and evidence-surface hardening.

## Current Position

Phase: 81 - Corrected Evidence Rebuild and Claim Audit
Plan: Complete
Status: Complete
Last activity: 2026-04-21 - Phase 81 complete
Progress: [##########] 100% by completed phases

## Current Milestone

v1.14 Evidence claim integrity and audit hardening phases are complete. Phase 81 regenerated the corrected publication package at `artifacts/paper/v1.14/`, and the claim audit plus release gate passed.

## Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Project context | `.planning/PROJECT.md` | Updated for v1.14 |
| Archived v1.12 requirements | `.planning/milestones/v1.12-REQUIREMENTS.md` | Complete |
| Archived requirements | `.planning/milestones/v1.13-REQUIREMENTS.md` | Complete |
| Requirements | `.planning/REQUIREMENTS.md` | Defined for v1.14 |
| Roadmap | `.planning/ROADMAP.md` | Created for v1.14; next phase starts at 77 |
| Research summary | `.planning/research/SUMMARY.md` | Reuse existing context; no new domain research selected |
| Workflow config | `.planning/config.json` | Complete |
| Milestone log | `.planning/MILESTONES.md` | Complete through v1.13 |
| v1.11 final paper package | `artifacts/paper/v1.11/` | Complete, audit passed |
| v1.12 draft skeleton | `artifacts/paper/v1.11/draft/` | Phase 64 complete |
| v1.12 evidence refresh | `artifacts/campaigns/v1.12-evidence-refresh/` | Phase 65 complete |
| v1.12 paper-facing draft assets | `artifacts/paper/v1.11/draft/` | Phase 66 complete |
| v1.12 bounded probes | `artifacts/paper/v1.11/draft/` | Phase 67 complete |
| v1.12 supplement | `artifacts/paper/v1.11/v1.12-supplement/` | Phase 68 complete, audit passed |
| v1.12 training-detail assets | `artifacts/paper/v1.11/draft/training-detail/` | Quick task complete: 4,472 step rows, 232 candidate rows |
| v1.13 clean-room evidence package | `artifacts/paper/v1.13/` | Complete, audit and release gate passed |
| Phase 77 artifacts | `.planning/phases/77-two-axis-recovery-accounting-and-headline-rebuild/` | Complete |
| Phase 78 artifacts | `.planning/phases/78-warm-start-evidence-relabeling/` | Complete |
| Phase 79 artifacts | `.planning/phases/79-baseline-claim-surface-quarantine/` | Complete |
| Phase 80 artifacts | `.planning/phases/80-multivariate-verifier-target-matching/` | Complete |
| Phase 81 artifacts | `.planning/phases/81-corrected-evidence-rebuild-and-claim-audit/` | Complete |
| v1.14 corrected evidence package | `artifacts/paper/v1.14/` | Complete, claim audit and release gate passed |

## Accumulated Context

### Decisions

- v1.12 continues phase numbering after v1.11 Phase 63.
- The paper should remain framed as a verifier-gated hybrid EML symbolic-regression methods/evidence paper, not broad blind-SR superiority.
- Pure blind, scaffolded, same-AST, warm-start, perturbed-basin, repair/refit, compile-only, unsupported, and failed evidence remain separate denominators.
- Logistic and Planck remain unsupported unless strict support and verifier contracts actually pass.
- Additional shallow/depth seeds are credibility refreshes, not a change in the claim standard.
- Conventional symbolic-regression comparison is useful but must not become a time sink; unavailable dependencies should be reported as deferred.
- A logistic strict-support push is bounded compiler work and may fail; no gate relaxation is allowed.
- v1.13 supersedes the manuscript-prose next step because publication-readiness gaps are now the blocking issue.
- Clean-room reproduction, verifier strength, leakage removal, semantics mismatch quantification, dual benchmark tracks, matched baselines, expanded datasets, and final `main` publication are all in scope.
- Placeholder snapshot metadata may remain only in deterministic-test fixtures, not in final paper/publication manifests.
- Candidate selection and final confirmation data must be separated unless symbolic equivalence is established.
- Training artifacts must label `guarded` versus `faithful` semantics, expose guard/anomaly/post-snap diagnostics, and surface verifier certificate/evidence labels.
- Full guarded-versus-faithful publication-matrix ablations are enabled by Phase 71 and remain part of the Phase 76 evidence rebuild.
- Basis-only and literal-constant benchmark tracks are separate v1.13 denominators. Publication claims should use the new v1.13 track suites when denominator purity matters.
- Expanded dataset manifests now cover noisy synthetic, parameter-identifiability, multivariable, unit-aware, and real observational inputs. The Hubble fixture is real-data plumbing evidence, not an exact recovery target.
- Baseline comparison rows are generated by the Phase 75 harness and are excluded from EML recovery denominators. Optional external SR dependencies fail closed when unavailable.
- v1.14 must repair public claim accounting before manuscript or release work continues: compile-only support, same-AST seed retention, and trained recovery need separate headline surfaces.
- Phase 77 added separate `verification_outcome`, `evidence_regime`, and `discovery_class` accounting fields. Compile-only verified support is no longer counted as trained exact recovery.
- Phase 78 added explicit `warm_start_evidence`, `ast_return_status`, and `total_restarts` fields. Zero-perturbation same-AST warm starts are labeled `exact_seed_round_trip`.
- Phase 79 added baseline launch/quarantine fields and claim-audit checks. Current baseline rows remain diagnostic/future-work context, not public comparator evidence.
- Phase 80 fixed high-precision target lookup for multivariate splits without `target_mpmath` by matching the full input row.
- Phase 81 routed corrected publication output to `artifacts/paper/v1.14/`, preserved historical v1.13 artifacts, regenerated the corrected evidence package, and passed claim-audit/release-gate checks with 8 trained exact recoveries, 1 compile-only verified support row, 15 unsupported rows, and 0 failed rows.

### Pending Todos

- Archive or close the v1.14 milestone with `$gsd-complete-milestone` if desired.

### Deferred Items

Items acknowledged and deferred at milestone close on 2026-04-20:

| Category | Item | Status |
|----------|------|--------|
| quick_task | 260419-ukc-rewrite-readme-to-make-it-clear-engaging | missing |
| quick_task | 260419-uxg-make-readme-clear-and-cool-without-menti | missing |
| quick_task | 260420-b8n-add-readme-plot-section-showing-how-demo | missing |
| quick_task | 260420-bdg-expand-readme-fit-plots-with-four-additi | missing |
| quick_task | 260420-bia-fix-readme-plot-gallery-to-one-conservat | missing |
| quick_task | 260420-g7h-include-useful-public-artifacts-in-sanit | unknown |
| quick_task | 260420-ixp-return-tests-to-generated-main-branch | unknown |

### Completed Quick Tasks

| Date | Task | Status | Artifacts |
|------|------|--------|-----------|
| 2026-04-19 | Paper-ready training detail artifacts | Complete | `artifacts/paper/v1.11/draft/training-detail/` |
| 2026-04-19 | README clarity and usage rewrite | Complete | `.planning/quick/260419-ukc-rewrite-readme-to-make-it-clear-engaging/` |
| 2026-04-19 | Public-facing README polish | Complete | `.planning/quick/260419-uxg-make-readme-clear-and-cool-without-menti/` |
| 2026-04-20 | README approximation plots | Complete | `.planning/quick/260420-b8n-add-readme-plot-section-showing-how-demo/` |
| 2026-04-20 | Expanded conservative README plot gallery | Complete | `.planning/quick/260420-bdg-expand-readme-fit-plots-with-four-additi/` |
| 2026-04-20 | Fixed 2x2 README plot gallery | Complete | `.planning/quick/260420-bia-fix-readme-plot-gallery-to-one-conservat/` |
| 2026-04-20 | Publish sanitized main from dev | Complete | `.planning/quick/260420-fsn-add-github-actions-automation-to-publish/` |
| 2026-04-20 | Include curated public artifacts | Complete | `.planning/quick/260420-g7h-include-useful-public-artifacts-in-sanit/` |
| 2026-04-20 | Return tests to generated main branch | Complete | `.planning/quick/260420-ixp-return-tests-to-generated-main-branch/` |
| 2026-04-20 | README v1.13 release evidence plots | Complete | `.planning/quick/260420-ng7-update-readme-with-v1-13-release-evidenc/` |
| 2026-04-20 | README clearer v1.13 evidence and fit plots | Complete | `.planning/quick/260420-nll-replace-readme-plots-with-clearer-v1-13-/` |
| 2026-04-20 | README narrative and conservative target plots | Complete | `.planning/quick/260420-nuw-simplify-readme-release-narrative-and-re/` |
| 2026-04-20 | README data-split plot gallery | Complete | `.planning/quick/260420-o1v-update-readme-plot-gallery-with-data-spl/` |
| 2026-04-20 | README plot legend-only cleanup | Complete | `.planning/quick/260420-o7r-simplify-readme-plot-gallery-labels-and-/` |
| 2026-04-20 | README current narrative and plot labels | Complete | `.planning/quick/260420-oij-remove-readme-release-framing-and-label-/` |
| 2026-04-20 | README unverified EML trial plot curves | Complete | `.planning/quick/260420-oth-show-unverified-eml-trial-curves-and-fun/` |
| 2026-04-20 | README EML status plot restyle | Complete | `.planning/quick/260420-p1b-restyle-readme-plot-gallery-with-status-/` |
| 2026-04-20 | Hide workflows from main and shorten update commit | Complete | `.planning/quick/260420-p9c-hide-github-workflows-from-generated-mai/` |
| 2026-04-21 | Remove oversized generated publication artifact from history | Complete | `.planning/quick/260421-g4k-remove-oversized-unused-artifacts-from-g/` |

### Blockers/Concerns

- External SR baselines may require dependencies or network access. If unavailable locally, record that explicitly instead of blocking the milestone.
- Extra training runs should stay shallow and cheap; broad new campaigns are out of scope.

## Session Continuity

Last session: 2026-04-21
Stopped at: v1.14 phases complete
Resume file: None

---
*Last updated: 2026-04-21 after oversized artifact cleanup*
