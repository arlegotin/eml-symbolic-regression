---
gsd_state_version: 1.0
milestone: v1.15
milestone_name: GEML family and i*pi EML exploration
current_phase: 87
current_phase_name: "GEML Evidence Package and Claim Boundary"
status: Ready to plan Phase 87
stopped_at: phase 86 complete
last_updated: "2026-04-22T00:00:00.000Z"
last_activity: 2026-04-22
progress:
  total_phases: 6
  completed_phases: 5
  total_plans: 5
  completed_plans: 5
  percent: 83
---

# GSD State: EML Symbolic Regression

**Initialized:** 2026-04-15
**Current phase:** Phase 87 - GEML Evidence Package and Claim Boundary
**Mode:** YOLO

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-04-22)

**Core value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.
**Current focus:** v1.15 GEML family theory, i*pi EML implementation, and matched EML versus i*pi EML evidence.

## Current Position

Phase: 87 - GEML Evidence Package and Claim Boundary
Plan: -
Status: Ready to plan
Last activity: 2026-04-22 - Phase 86 complete
Progress: [########--] 83% by completed phases

## Current Milestone

v1.15 GEML family and i*pi EML exploration will generalize EML into `GEML_a(x, y) = exp(a*x) - log(y)/a`, specialize `a = i*pi` as the flagship oscillatory operator, prove restricted-domain identities, add branch diagnostics, and run matched recovery comparisons against raw EML.

## Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Project context | `.planning/PROJECT.md` | Updated for v1.15 |
| Archived v1.12 requirements | `.planning/milestones/v1.12-REQUIREMENTS.md` | Complete |
| Archived v1.13 requirements | `.planning/milestones/v1.13-REQUIREMENTS.md` | Complete |
| Archived v1.14 requirements | `.planning/milestones/v1.14-REQUIREMENTS.md` | Complete |
| Archived v1.14 roadmap | `.planning/milestones/v1.14-ROADMAP.md` | Complete |
| Archived v1.14 phase artifacts | `.planning/milestones/v1.14-phases/` | Complete |
| Requirements | `.planning/REQUIREMENTS.md` | Defined for v1.15 |
| Roadmap | `.planning/ROADMAP.md` | Created for v1.15; next phase starts at 82 |
| Research summary | `.planning/research/SUMMARY.md` | Existing context retained; no new domain research selected during initialization |
| Workflow config | `.planning/config.json` | Complete |
| Milestone log | `.planning/MILESTONES.md` | Complete through v1.14 |
| v1.11 final paper package | `artifacts/paper/v1.11/` | Complete, audit passed |
| v1.12 draft skeleton | `artifacts/paper/v1.11/draft/` | Phase 64 complete |
| v1.12 evidence refresh | `artifacts/campaigns/v1.12-evidence-refresh/` | Phase 65 complete |
| v1.12 paper-facing draft assets | `artifacts/paper/v1.11/draft/` | Phase 66 complete |
| v1.12 bounded probes | `artifacts/paper/v1.11/draft/` | Phase 67 complete |
| v1.12 supplement | `artifacts/paper/v1.11/v1.12-supplement/` | Phase 68 complete, audit passed |
| v1.12 training-detail assets | `artifacts/paper/v1.11/draft/training-detail/` | Quick task complete: 4,472 step rows, 232 candidate rows |
| v1.13 clean-room evidence package | `artifacts/paper/v1.13/` | Complete, audit and release gate passed |
| v1.14 corrected evidence package | `artifacts/paper/v1.14/` | Complete, claim audit and release gate passed |
| Phase 82 artifacts | `.planning/phases/82-geml-family-semantics-and-structural-identity/` | Complete |
| Phase 83 artifacts | `.planning/phases/83-i-pi-eml-restricted-theory-and-branch-contract/` | Complete |
| Phase 84 artifacts | `.planning/phases/84-family-aware-training-and-snapping-integration/` | Complete |
| Phase 85 artifacts | `.planning/phases/85-oscillatory-benchmark-pack-and-negative-controls/` | Complete |
| Phase 86 artifacts | `.planning/phases/86-matched-eml-versus-i-pi-eml-campaign-runner/` | Complete |
| i*pi restricted theory | `artifacts/theory/v1.15/` | Complete |

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
- v1.15 treats i*pi EML as the `a = i*pi` specialization of the broader `GEML_a` family rather than as an isolated new operator.
- v1.15 should prove restricted-domain identities and controlled-composition bounds before making empirical or closure claims.
- EML versus i*pi EML comparisons must be matched by depth, optimizer, initialization budget, snapping rule, verifier gates, and reporting schema.
- i*pi EML branch management is part of the operator contract, not a nuisance hidden in implementation details.
- Phase 82 added fixed-parameter `GEML_a` semantics, canonical raw `a = 1` handling, i*pi EML helpers, exact AST JSON/SymPy export, and structural identity tests while preserving legacy raw/centered benchmark artifact compatibility.
- Phase 83 added principal-log branch diagnostics, verifier branch-failure fields, training-only branch guard metadata, and executable i*pi restricted theory artifacts with explicit non-claims.
- Phase 84 threaded fixed GEML specializations through optimizer, hardening, snapping, exact-candidate selection, semantics-alignment evidence, and manifest metrics without reusing raw-family scaffold witnesses for i*pi EML.
- Phase 85 registered normalized oscillatory, log-periodic, and negative-control targets plus matched raw/i*pi benchmark suites and branch-domain fail-closed validation.
- Phase 86 added paired raw EML versus i*pi EML campaign artifacts, exposed Phase 84 metrics in campaign rows, and preserved v1.14 recovery-accounting fields in paired outputs.

### Pending Todos

- Plan Phase 87 with `$gsd-plan-phase 87`.

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
- i*pi EML branch-cut behavior can invalidate naive real-domain identities; branch convention and domain restrictions must be explicit before benchmark claims.
- Full `GEML_a` universality is not assumed. Restricted theorem statements and empirical evidence should carry the milestone.

## Session Continuity

Last session: 2026-04-22
Stopped at: Phase 86 complete; ready for Phase 87
Resume file: None

---
*Last updated: 2026-04-22 after Phase 86 completion*
