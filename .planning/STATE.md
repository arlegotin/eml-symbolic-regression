---
gsd_state_version: 1.0
milestone: none
milestone_name: None - v1.10 shipped
current_phase: none
status: milestone_complete
stopped_at: v1.10 archived and ready for next milestone
last_updated: "2026-04-18T14:41:51.262Z"
last_activity: 2026-04-18 -- v1.10 archived
progress:
  total_phases: 5
  completed_phases: 5
  total_plans: 5
  completed_plans: 5
  percent: 100
---

# GSD State: EML Symbolic Regression

**Initialized:** 2026-04-15
**Current phase:** None
**Mode:** YOLO

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-04-18)

**Core value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.
**Current focus:** No active milestone. v1.10 is archived.

## Current Position

Phase: None
Plan: None
Status: v1.10 archived
Last activity: 2026-04-18 -- v1.10 archived
Progress: [██████████] 100% by completed phases

## Current Milestone

No active milestone. Start the next milestone with `$gsd-new-milestone`.

## Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Project context | `.planning/PROJECT.md` | Complete |
| Archived v1.10 requirements | `.planning/milestones/v1.10-REQUIREMENTS.md` | Complete |
| Roadmap | `.planning/ROADMAP.md` | Collapsed after v1.10 |
| Workflow config | `.planning/config.json` | Complete |
| Milestone log | `.planning/MILESTONES.md` | Complete through v1.10 |
| v1.9 raw-hybrid paper package | `artifacts/paper/v1.9/raw-hybrid/` | Complete |
| v1.10 focused motif evidence | `artifacts/campaigns/v1.10-logistic-evidence/`, `artifacts/campaigns/v1.10-planck-diagnostics/` | Complete |

## Performance Metrics

**Recent trend:**

- v1.9 shipped raw-only scaffold honesty, Arrhenius same-AST evidence, Michaelis-Menten motif support, expanded cleanup diagnostics, and the raw-hybrid paper package.
- v1.10 starts from strong compiler wins but keeps logistic and Planck unsupported unless structural, validation-gated motifs pass the existing support and verifier contracts.

## Accumulated Context

### Decisions

- v1.10 continues Phase numbering from Phase 54 after v1.9 Phase 53.
- Compiler improvements must be structural, validation-gated, and diagnostic-visible.
- Formula-name recognizers, exact-constant recognizers, and silent gate relaxation remain out of scope.
- Logistic can be warmed only after strict compile support exists under a non-looser gate.
- Planck can improve compile depth while still remaining unsupported/stretch unless the full compile, warm-start, and verifier contract passes.
- [Phase 54]: Archived compiler baselines are now locked in tests: logistic relaxed depth 27 with no macro hits, Planck relaxed depth 20 with the two existing macro hits, and existing supported macros remain intact.
- [Phase 55]: Reciprocal and saturation motif matchers now support validated `g+b` and `c*g/(g+b)` subexpressions, add validation-visible macro diagnostics, and preserve fail-closed non-unit behavior.
- [Phase 56]: Logistic now compiles through structural `exponential_saturation_template` at relaxed depth 15 (down from 27) with baseline deltas recorded; strict depth 13 still fails, so no warm-start promotion is claimed.
- [Phase 56]: Code review warning WR-01 was fixed by normalizing equal-scale ratio forms such as `k*exp(a)/(k*exp(a)+c)` into the same exponential-saturation family.
- [Phase 57]: `low_degree_power_template` now shortens cubes via validated `exp(n*log(g))` only when shorter; `x**3` drops from depth 16 to 9 while `x**2` keeps the existing shorter path.
- [Phase 57]: Planck relaxed compile depth drops from 20 to 14 with `low_degree_power_template`, `scaled_exp_minus_one_template`, and `direct_division_template`; strict depth 13 still fails, so Planck remains stretch/unsupported.
- [Phase 58]: Focused suites `v1.10-logistic-evidence` and `v1.10-planck-diagnostics` now write compile-only campaign artifacts under `artifacts/campaigns/`; both rows remain unsupported because strict depth 13 still fails.
- [Phase 58]: Logistic focused evidence records relaxed depth 15, node count 49, and `exponential_saturation_template`; Planck focused evidence records relaxed depth 14, node count 59, and the low-degree power plus existing denominator/division motifs.

### Pending Todos

None recorded.

### Blockers/Concerns

Preserve Shockley, Arrhenius, and Michaelis-Menten support while changing motif logic. Keep all v1.10 evidence focused; broad paper package refresh is out of scope.

## Session Continuity

Last session: 2026-04-18
Stopped at: v1.10 archived; ready for `$gsd-new-milestone`
Resume file: None

---
*Last updated: 2026-04-18 after archiving v1.10*
