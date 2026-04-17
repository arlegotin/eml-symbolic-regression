---
phase: 51-reciprocal-and-saturation-compiler-motifs
plan: 03
subsystem: benchmarks-docs
tags: [michaelis-menten, evidence-artifacts, warm-start, same-ast, documentation]

requires:
  - phase: 51-01
    provides: Saturation macro compiler support for strict Michaelis-Menten exact EML warm starts.
  - phase: 51-02
    provides: Built-in `v1.9-michaelis-evidence` benchmark suite and runner artifact locks.
provides:
  - Focused `v1.9-michaelis-evidence` artifacts for `michaelis-warm`.
  - Artifact-gated documentation for Michaelis-Menten exact compiler warm-start / same-AST evidence.
  - Documentation of `reciprocal_shift_template` and `saturation_ratio_template` compiler motifs.
affects: [phase-53, raw-hybrid-paper-suite, michaelis_menten, documentation]

tech-stack:
  added: []
  patterns:
    - artifact-gated evidence documentation for focused benchmark suites
    - regime-safe wording that separates same-AST warm-start evidence from blind discovery

key-files:
  created:
    - artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/suite-result.json
    - artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/aggregate.json
    - artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/aggregate.md
    - artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/v1-9-michaelis-evidence-michaelis-warm-a67d8ccfb108.json
    - .planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-03-SUMMARY.md
  modified:
    - README.md
    - docs/IMPLEMENTATION.md

key-decisions:
  - "Docs cite `v1.9-michaelis-evidence` only after strict JSON validation of the generated same-AST artifact."
  - "Michaelis-Menten is documented as exact compiler warm-start / same-AST basin evidence, not blind discovery."
  - "Arrhenius same-AST wording is preserved and Planck remains stretch/unsupported under the shipped warm-start gate."

patterns-established:
  - "Focused evidence docs should list concrete artifact fields: suite, case, formula, macro, depth, node count, status, verifier result, and evidence class."
  - "Scientific-law docs must name the evidence regime before claim language, especially for warm-start and same-AST returns."

requirements-completed: [MIC-03, MIC-04]

duration: 4min
completed: 2026-04-17
---

# Phase 51 Plan 03: Michaelis Evidence Documentation Summary

**Validated Michaelis-Menten same-AST warm-start artifacts with regime-safe README and implementation documentation**

## Performance

- **Duration:** 4 min
- **Started:** 2026-04-17T14:04:28Z
- **Completed:** 2026-04-17T14:08:22Z
- **Tasks:** 2
- **Files modified:** 7

## Accomplishments

- Generated focused benchmark artifacts under `artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/`.
- Validated suite `v1.9-michaelis-evidence`, case `michaelis-warm`, demo id `michaelis_menten`, expression `2*x/(x + 0.5)`, train/heldout/extrapolation domains, macro hit `saturation_ratio_template`, compile depth `12`, node count `41`, status `same_ast_return`, verifier status `recovered`, and evidence class `same_ast`.
- Updated README and implementation docs with Michaelis warm-start commands, focused benchmark reproduction commands, concrete artifact fields, and exact compiler warm-start / same-AST wording.
- Added implementation documentation for `reciprocal_shift_template` and `saturation_ratio_template` while preserving Arrhenius same-AST evidence and Planck stretch/unsupported wording.

## Task Commits

Each task was committed atomically:

1. **Task 1: Generate and validate focused Michaelis evidence artifact** - `5789fe1` (feat)
2. **Task 2: Document Michaelis motif support without blind-discovery overclaim** - `0a3131d` (docs)

**Plan metadata:** summary/state commit for this file.

## Files Created/Modified

- `artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/suite-result.json` - Focused suite result with the one `michaelis-warm` run payload.
- `artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/aggregate.json` - Machine-readable aggregate showing one same-AST recovery and no unsupported/failed runs.
- `artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/aggregate.md` - Human-readable aggregate report with `same_ast_warm_start_return`.
- `artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/v1-9-michaelis-evidence-michaelis-warm-a67d8ccfb108.json` - Per-run artifact for the validated Michaelis warm-start case.
- `README.md` - Added Michaelis warm-start and focused benchmark commands plus regime-safe evidence wording.
- `docs/IMPLEMENTATION.md` - Added reciprocal/saturation macro documentation, suite listing, artifact root, commands, and updated Planck/Michaelis boundaries.
- `.planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-03-SUMMARY.md` - Captures execution results and GSD metadata.

## Verification

- Focused benchmark command: `PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark v1.9-michaelis-evidence --case michaelis-warm --seed 0 --perturbation-noise 0.0 --output-dir artifacts/campaigns/v1.9-michaelis-evidence` -> `1 runs, 0 unsupported, 0 failed`.
- Strict JSON validation: generated suite, aggregate, and per-run artifact matched the required suite/case/demo/expression/domain/macro/depth/node/status/verifier/evidence fields.
- Documentation regression tests: `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py::test_cli_warm_start_promotes_michaelis_same_ast_evidence tests/test_benchmark_runner.py::test_michaelis_warm_benchmark_records_same_ast_evidence tests/test_compiler_warm_start.py::test_cli_reports_planck_as_stretch_without_promotion -q` -> `3 passed`.
- Documentation grep check: `rg "michaelis|2\\*x/\\(x\\+0\\.5\\)|saturation_ratio_template|same_ast_return|recovered|same_ast|v1\\.9-michaelis-evidence|michaelis-warm" README.md docs/IMPLEMENTATION.md` -> matched required Michaelis fields.
- Boundary grep check: `rg "arrhenius|Planck|planck|stretch|unsupported" README.md docs/IMPLEMENTATION.md` -> matched preserved Arrhenius and Planck wording.

## Decisions Made

- Followed the artifact-first evidence gate: documentation changed only after generated JSON passed strict validation.
- Treated Michaelis-Menten as exact compiler warm-start / same-AST basin evidence, not blind discovery or from-scratch recovery.
- Preserved the existing Arrhenius same-AST evidence paragraph and kept Planck documented as stretch/unsupported under the shipped warm-start promotion budget.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None. The focused benchmark produced the expected same-AST artifact on the first run, so no implementation fixes were required.

## Known Stubs

None introduced. Stub scan found no marker text in the files created or modified by this plan. Generated JSON schema fields with `null` or empty arrays are expected artifact data, not UI/data-source stubs.

## User Setup Required

None - no external service configuration required.

## Threat Flags

None. The plan generated local benchmark artifacts and documentation only; it introduced no new network endpoints, auth paths, file access patterns, or schema trust boundaries outside the plan threat model.

## Next Phase Readiness

Phase 53 can consume `v1.9-michaelis-evidence` as focused same-AST warm-start source material for the raw-hybrid paper package. Residual risk remains explicit: the evidence is a single zero-noise compiler warm-start basin result, not blind discovery.

## Self-Check: PASSED

- Verified files exist: `suite-result.json`, `aggregate.json`, `aggregate.md`, the `michaelis-warm` per-run artifact, `README.md`, `docs/IMPLEMENTATION.md`, and this summary.
- Verified task commits exist in git history: `5789fe1`, `0a3131d`.
- Verified task commits introduced no tracked file deletions.
- Stub scan found no marker text in the created or modified files; generated JSON `null` and empty-array values are expected artifact schema data.

---
*Phase: 51-reciprocal-and-saturation-compiler-motifs*
*Completed: 2026-04-17*
