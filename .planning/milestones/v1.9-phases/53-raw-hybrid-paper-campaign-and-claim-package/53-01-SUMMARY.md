---
phase: 53-raw-hybrid-paper-campaign-and-claim-package
plan: 01
subsystem: reporting
tags: [raw-hybrid, paper-package, cli, source-locks, evidence-regimes]

requires:
  - phase: 49-witness-registry-and-centered-scaffold-correctness
    provides: raw-only scaffold witness caveats for centered-family diagnostics
  - phase: 50-arrhenius-exact-warm-start-demo
    provides: v1.9 Arrhenius same-AST warm-start evidence
  - phase: 51-reciprocal-and-saturation-compiler-motifs
    provides: v1.9 Michaelis-Menten same-AST warm-start evidence
  - phase: 52-verifier-gated-exact-cleanup-expansion
    provides: v1.9 repair-only evidence and fallback preservation summary
provides:
  - raw-hybrid paper package writer for preset v1.9-raw-hybrid-paper
  - raw-hybrid-paper CLI command that validates locked evidence sources
  - regime-separated report, scientific-law table, claim-boundary, and centered diagnostic renderers
affects: [phase-53, paper-artifacts, cli, reporting]

tech-stack:
  added: []
  patterns:
    - typed source inventory with file-level SHA-256 locks
    - synthesis-only CLI command with shlex-quoted reproduction command

key-files:
  created:
    - src/eml_symbolic_regression/raw_hybrid_paper.py
    - tests/test_raw_hybrid_paper.py
  modified:
    - src/eml_symbolic_regression/cli.py

key-decisions:
  - "The raw-hybrid paper package is synthesis-only: it reads declared evidence artifacts and never runs benchmark, campaign, proof-campaign, or paper-decision workflows."
  - "Source locks hash declared files only, not evidence directories."
  - "Scientific-law rows keep Arrhenius and Michaelis as same-AST warm-start evidence, while Planck/logistic remain compile-only unsupported diagnostics."
  - "Centered-family material is rendered as negative diagnostic evidence under the missing same-family witness caveat."

patterns-established:
  - "Paper packages should expose typed source definitions and fail closed on missing required evidence."
  - "Report generators should keep pure blind, scaffolded, compile-only, warm-start, same-AST, repaired, refit, and perturbed-basin evidence in separate buckets."

requirements-completed: [RHY-01, RHY-02, RHY-03, RHY-04]

duration: 11min
completed: 2026-04-17
---

# Phase 53 Plan 01: Raw-Hybrid Paper Package Writer Summary

**Synthesis-only raw-hybrid paper package writer with file-level source locks, regime-separated reports, scientific-law tables, centered caveats, and a CLI entry point**

## Performance

- **Duration:** 11 min
- **Started:** 2026-04-17T16:32:26Z
- **Completed:** 2026-04-17T16:43:34Z
- **Tasks:** 3
- **Files modified:** 3

## Accomplishments

- Added `write_raw_hybrid_paper_package()` with explicit v1.9 source contracts, required-source validation, non-empty output directory protection, and `manifest.json` / `source-locks.json` generation.
- Added regime-separated JSON and Markdown renderers for pure blind, scaffolded, compile-only, warm-start, same-AST return, repaired, refit, and perturbed-basin evidence.
- Added scientific-law JSON/CSV/Markdown table extraction for Beer-Lambert, Shockley, Arrhenius, Michaelis-Menten, Planck, logistic, and historical Michaelis diagnostics.
- Added `raw-hybrid-paper` CLI wiring with `--output-dir`, `--require-existing`, `--allow-missing`, `--overwrite`, and shell-safe reproduction command persistence.

## Task Commits

Each TDD task was committed atomically:

1. **Task 1 RED:** `30adda4` test(53-01): add raw hybrid source package contracts
2. **Task 1 GREEN:** `0594435` feat(53-01): add raw hybrid source package writer
3. **Task 2 RED:** `f946abb` test(53-01): add raw hybrid report contracts
4. **Task 2 GREEN:** `fe8ccc7` feat(53-01): render raw hybrid paper reports
5. **Task 3 RED:** `d4f5377` test(53-01): add raw hybrid CLI contracts
6. **Task 3 GREEN:** `5a432e6` feat(53-01): wire raw hybrid paper CLI

## Files Created/Modified

- `src/eml_symbolic_regression/raw_hybrid_paper.py` - New package writer, source inventory, locks, regime summaries, scientific-law extractors, claim boundaries, and centered diagnostics.
- `src/eml_symbolic_regression/cli.py` - Added the `raw-hybrid-paper` command and shell-safe reproduction command builder.
- `tests/test_raw_hybrid_paper.py` - Added source validation, lock, manifest, report, table, centered caveat, and CLI contract tests.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_raw_hybrid_paper.py -q` - passed, 10 tests.
- `PYTHONPATH=src python -m pytest tests/test_paper_decision.py tests/test_campaign.py::test_reproduction_command_quotes_shell_sensitive_values -q` - passed, 4 tests.
- `PYTHONPATH=src python -m eml_symbolic_regression.cli raw-hybrid-paper --output-dir /tmp/eml-raw-hybrid-paper-test --require-existing --overwrite` - passed, wrote the smoke package to `/tmp/eml-raw-hybrid-paper-test`.
- Confirmed `artifacts/paper/v1.9/raw-hybrid` was not created.

## Decisions Made

- Kept the writer synthesis-only to satisfy the Phase 53 scope boundary and Denial-of-Service mitigation.
- Used declared file paths as the source-lock unit so package provenance is stable and auditable.
- Used source-regime metadata plus aggregate/run fields to populate buckets without reclassifying historical outcomes.
- Rendered centered-family evidence only from v1.8 decision inputs and avoided intrinsic impossibility language.

## Deviations from Plan

None - plan executed as written.

## Known Stubs

None. Stub scan found only normal optional dataclass defaults and local empty container initialization; no placeholder output or unwired UI/data path was introduced.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Plan 53-02 can run the CLI into `artifacts/paper/v1.9/raw-hybrid` and validate the generated paper package without needing broad campaign reruns.

## Self-Check: PASSED

- Created files exist: `src/eml_symbolic_regression/raw_hybrid_paper.py`, `tests/test_raw_hybrid_paper.py`, and this summary.
- Task commits found: `30adda4`, `0594435`, `f946abb`, `fe8ccc7`, `d4f5377`, `5a432e6`.
- No tracked file deletions were introduced by task commits.

---
*Phase: 53-raw-hybrid-paper-campaign-and-claim-package*
*Completed: 2026-04-17*
