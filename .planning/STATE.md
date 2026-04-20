---
gsd_state_version: 1.0
milestone: v1.13
milestone_name: Publication-grade reproduction and validation
current_phase: 75
current_phase_name: Matched Conventional Baseline Harness
status: Ready to discuss
stopped_at: v1.12 archived
last_updated: "2026-04-20T13:50:35Z"
last_activity: 2026-04-20
progress:
  total_phases: 8
  completed_phases: 6
  total_plans: 6
  completed_plans: 6
  percent: 75
---

# GSD State: EML Symbolic Regression

**Initialized:** 2026-04-15
**Current phase:** 75
**Mode:** YOLO

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-04-20)

**Core value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.
**Current focus:** v1.13 publication-grade reproduction and validation.

## Current Position

Phase: 75 - Matched Conventional Baseline Harness
Plan: Not started
Status: Ready to discuss
Last activity: 2026-04-20 - Completed Phase 74 and advanced to Phase 75
Progress: [########--] 75% by completed phases

## Current Milestone

**v1.13: Publication-grade reproduction and validation**

Goal: Build a clean-room publication path that can regenerate the paper evidence from an empty checkout, strengthen verifier and split discipline, add real CI/test coverage, run dual-track and matched-baseline evidence, and publish the resulting code and artifacts safely to `main`.

## Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Project context | `.planning/PROJECT.md` | Updated for v1.13 |
| Archived v1.12 requirements | `.planning/milestones/v1.12-REQUIREMENTS.md` | Complete |
| Requirements | `.planning/REQUIREMENTS.md` | Defined for v1.13 |
| Roadmap | `.planning/ROADMAP.md` | Active v1.13 phases 69-76 |
| Research summary | `.planning/research/SUMMARY.md` | Reuse existing context; no new domain research selected |
| Workflow config | `.planning/config.json` | Complete |
| Milestone log | `.planning/MILESTONES.md` | Complete through v1.12 |
| v1.11 final paper package | `artifacts/paper/v1.11/` | Complete, audit passed |
| v1.12 draft skeleton | `artifacts/paper/v1.11/draft/` | Phase 64 complete |
| v1.12 evidence refresh | `artifacts/campaigns/v1.12-evidence-refresh/` | Phase 65 complete |
| v1.12 paper-facing draft assets | `artifacts/paper/v1.11/draft/` | Phase 66 complete |
| v1.12 bounded probes | `artifacts/paper/v1.11/draft/` | Phase 67 complete |
| v1.12 supplement | `artifacts/paper/v1.11/v1.12-supplement/` | Phase 68 complete, audit passed |
| v1.12 training-detail assets | `artifacts/paper/v1.11/draft/training-detail/` | Quick task complete: 4,472 step rows, 232 candidate rows |
| v1.13 clean-room evidence package | TBD | Planned |

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

### Pending Todos

- Continue Phase 75 with autonomous discuss, plan, and execute.

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

### Blockers/Concerns

- External SR baselines may require dependencies or network access. If unavailable locally, record that explicitly instead of blocking the milestone.
- Extra training runs should stay shallow and cheap; broad new campaigns are out of scope.

## Session Continuity

Last session: 2026-04-19
Stopped at: v1.12 archived
Resume file: None

---
*Last updated: 2026-04-20 after Phase 74 completion*
