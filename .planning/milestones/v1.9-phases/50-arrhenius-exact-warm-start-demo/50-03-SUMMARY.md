---
phase: 50-arrhenius-exact-warm-start-demo
plan: 03
subsystem: benchmarks-docs
tags: [arrhenius, benchmark-artifacts, warm-start, same-ast, documentation]
requires:
  - phase: 50-02
    provides: Built-in `v1.9-arrhenius-evidence` suite with `arrhenius-warm` artifact contract tests.
provides:
  - Generated focused Arrhenius suite, aggregate, and per-run evidence artifacts.
  - Documentation for normalized Arrhenius exact compiler warm-start evidence.
  - Regime-honest claim language separating same-AST warm-start evidence from blind discovery.
affects: [raw-hybrid-paper-suite, phase-53, documentation, benchmark-artifacts]
tech-stack:
  added: []
  patterns: [evidence-first documentation, focused benchmark artifacts, same-AST warm-start reporting]
key-files:
  created:
    - artifacts/campaigns/v1.9-arrhenius-evidence/v1.9-arrhenius-evidence/suite-result.json
    - artifacts/campaigns/v1.9-arrhenius-evidence/v1.9-arrhenius-evidence/aggregate.json
    - artifacts/campaigns/v1.9-arrhenius-evidence/v1.9-arrhenius-evidence/aggregate.md
    - artifacts/campaigns/v1.9-arrhenius-evidence/v1.9-arrhenius-evidence/v1-9-arrhenius-evidence-arrhenius-warm-75f6e9c1764d.json
    - .planning/phases/50-arrhenius-exact-warm-start-demo/50-03-SUMMARY.md
  modified:
    - README.md
    - docs/IMPLEMENTATION.md
key-decisions:
  - "Docs cite generated `v1.9-arrhenius-evidence` artifacts only after JSON validation passed."
  - "Arrhenius is documented as exact compiler warm-start / same-AST basin evidence, not blind discovery."
  - "Michaelis-Menten and Planck remain unsupported/stretch under default compile/warm-start gates."
patterns-established:
  - "Evidence-first doc updates: generate and validate focused artifacts before adding claim language."
  - "Focused scientific-law artifacts should preserve exact suite id, case id, domains, macro hits, verifier status, and evidence class."
requirements-completed: [ARR-04]
duration: 4min
completed: 2026-04-17
---

# Phase 50 Plan 03: Arrhenius Evidence Documentation Summary

**Focused Arrhenius same-AST warm-start artifacts with README and implementation docs tied to validated JSON evidence**

## Performance

- **Duration:** 4 min
- **Started:** 2026-04-17T12:59:36Z
- **Completed:** 2026-04-17T13:03:00Z
- **Tasks:** 2
- **Files modified:** 7

## Accomplishments

- Ran the focused benchmark command exactly as planned for suite `v1.9-arrhenius-evidence`, case `arrhenius-warm`, seed `0`, and perturbation noise `0.0`.
- Validated the generated suite JSON and per-run artifact before documentation edits: demo id `arrhenius`, formula `exp(-0.8/x)`, positive domains `[0.5, 3.0]`, `[0.6, 2.7]`, `[3.1, 4.2]`, macro hit `direct_division_template`, status `same_ast_return`, claim status `recovered`, warm-start verifier `recovered`, and evidence class `same_ast`.
- Added README and implementation documentation with the Arrhenius demo command, focused benchmark command, artifact root, concrete field values, and same-AST basin wording.
- Preserved the existing Michaelis-Menten and Planck unsupported/stretch caveats under default gates.

## Task Commits

Each task was committed atomically:

1. **Task 1: Generate and validate focused Arrhenius evidence artifact** - `8eacdda` (feat)
2. **Task 2: Document Arrhenius exact warm-start evidence without blind-discovery overclaim** - `7542581` (docs)

**Plan metadata:** summary/state commit for this file.

## Files Created/Modified

- `artifacts/campaigns/v1.9-arrhenius-evidence/v1.9-arrhenius-evidence/suite-result.json` - Suite-level focused benchmark result with one `arrhenius-warm` run.
- `artifacts/campaigns/v1.9-arrhenius-evidence/v1.9-arrhenius-evidence/aggregate.json` - Machine-readable aggregate counts with `same_ast` evidence class.
- `artifacts/campaigns/v1.9-arrhenius-evidence/v1.9-arrhenius-evidence/aggregate.md` - Human-readable aggregate evidence preserving `same_ast_warm_start_return`.
- `artifacts/campaigns/v1.9-arrhenius-evidence/v1.9-arrhenius-evidence/v1-9-arrhenius-evidence-arrhenius-warm-75f6e9c1764d.json` - Per-run artifact with compiler, warm-start, verifier, metrics, and dataset manifest evidence.
- `README.md` - Added Arrhenius exact warm-start and focused benchmark commands plus regime-honest evidence wording.
- `docs/IMPLEMENTATION.md` - Added Arrhenius to the demo ladder and benchmark suite list, with artifact-backed field values and preserved unsupported/stretch notes.
- `.planning/phases/50-arrhenius-exact-warm-start-demo/50-03-SUMMARY.md` - Recorded execution evidence and GSD metadata.

## Decisions Made

- Used the generated focused benchmark artifact as the source of documentation truth instead of describing expected evidence ahead of time.
- Kept top-level `recovered` language verifier-owned while explicitly labeling the run as `same_ast_return` and `same_ast`.
- Did not broaden historical benchmark denominators or change Michaelis-Menten/Planck behavior.

## Verification

Executed successfully:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark v1.9-arrhenius-evidence --case arrhenius-warm --seed 0 --perturbation-noise 0.0 --output-dir artifacts/campaigns/v1.9-arrhenius-evidence
```

Result: `1 runs, 0 unsupported, 0 failed`.

Artifact validation command loaded `suite-result.json`, the referenced per-run artifact, and `aggregate.json`; all required assertions passed.

```bash
PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py::test_cli_warm_start_promotes_arrhenius_same_ast_evidence tests/test_benchmark_runner.py::test_arrhenius_warm_benchmark_records_same_ast_evidence -q
```

Result: `2 passed in 5.63s`.

```bash
rg "arrhenius|exp\(-0\.8/x\)|direct_division_template|same_ast_return|recovered|same_ast|v1\.9-arrhenius-evidence|arrhenius-warm" README.md docs/IMPLEMENTATION.md
rg -n "Michaelis-Menten|Planck|unsupported|stretch" README.md docs/IMPLEMENTATION.md
```

Result: required Arrhenius terms and unsupported/stretch caveats are present.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## Known Stubs

None introduced. Stub scan over modified docs and generated artifact files found no TODO, FIXME, placeholder, empty-string assignment, or generated UI placeholder patterns. Artifact `null` and empty collection fields are expected serialized benchmark data, not stubs.

## User Setup Required

None - no external service configuration required.

## Threat Flags

None. The plan generated local benchmark artifacts and updated documentation only; it introduced no new network endpoints, auth paths, file access patterns, or schema trust boundaries outside the plan threat model.

## Next Phase Readiness

Phase 50 now has a reproducible focused Arrhenius evidence path and documentation tied to validated artifacts. Later raw-hybrid paper packaging can cite `v1.9-arrhenius-evidence` as same-AST warm-start evidence without mixing it into blind-discovery denominators.

## Self-Check: PASSED

- Found summary file `.planning/phases/50-arrhenius-exact-warm-start-demo/50-03-SUMMARY.md`.
- Found generated artifact files `suite-result.json`, `aggregate.json`, `aggregate.md`, and `v1-9-arrhenius-evidence-arrhenius-warm-75f6e9c1764d.json`.
- Found task commits `8eacdda` and `7542581` in git history.
- No tracked file deletions were introduced by task commits.

---
*Phase: 50-arrhenius-exact-warm-start-demo*
*Completed: 2026-04-17*
