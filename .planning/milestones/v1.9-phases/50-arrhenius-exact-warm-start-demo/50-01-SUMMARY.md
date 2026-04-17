---
phase: 50-arrhenius-exact-warm-start-demo
plan: 01
subsystem: datasets-testing-cli
tags: [arrhenius, demo-spec, compiler, warm-start, pytest]
requires:
  - phase: 49-witness-registry-and-centered-scaffold-correctness
    provides: raw EML scaffold and centered-family exclusion contracts preserved by this plan
provides:
  - built-in normalized Arrhenius demo id `arrhenius`
  - strict compile regression lock for `direct_division_template`
  - zero-noise same-AST warm-start regression lock
  - CLI JSON evidence regression for Arrhenius same-AST recovery
affects: [datasets, compiler-warm-start-tests, cli-demo-evidence, v1.9-arrhenius]
tech-stack:
  added: []
  patterns: [DemoSpec registry entry, verifier-owned recovery, same-AST warm-start evidence]
key-files:
  created:
    - .planning/phases/50-arrhenius-exact-warm-start-demo/50-01-SUMMARY.md
  modified:
    - src/eml_symbolic_regression/datasets.py
    - tests/test_proof_dataset_manifest.py
    - tests/test_compiler_warm_start.py
key-decisions:
  - "Arrhenius uses normalized dimensionless input `x` with formula `exp(-0.8/x)` and positive domains away from zero."
  - "Strict Arrhenius support is locked through the reusable `direct_division_template`; no Arrhenius-specific compiler branch was added."
  - "Zero-noise Arrhenius warm-start evidence remains `same_ast_return` / `same_ast`, not blind discovery."
patterns-established:
  - "Demo provenance tests inspect generated jittered split values, not only configured domain tuples."
  - "CLI warm-start tests assert both verifier-owned `recovered` and same-AST regime labels."
requirements-completed: [ARR-01, ARR-02, ARR-03]
duration: 4min
completed: 2026-04-17
---

# Phase 50 Plan 01: Arrhenius Exact Warm-Start Demo Summary

**Normalized Arrhenius demo `exp(-0.8/x)` with strict direct-division compile and verified same-AST warm-start evidence**

## Performance

- **Duration:** 4 min
- **Started:** 2026-04-17T12:44:53Z
- **Completed:** 2026-04-17T12:48:57Z
- **Tasks:** 3
- **Files modified:** 4

## Accomplishments

- Added built-in demo id `arrhenius` with variable `x`, formula `exp(-0.8/x)`, source `sources/FOR_DEMO.md`, and normalized dimensionless provenance.
- Locked positive train, held-out, and extrapolation domains at `(0.5, 3.0)`, `(0.6, 2.7)`, and `(3.1, 4.2)`, including checks after seeded jitter.
- Added regression coverage proving strict compile depth `7`, macro hit `direct_division_template`, unsupported reason `None`, zero-noise `same_ast_return`, verifier `recovered`, and `changed_slot_count == 0`.
- Added CLI JSON evidence coverage while preserving existing Michaelis-Menten unsupported and Planck stretch behavior.

## Task Commits

Each task was committed atomically:

1. **Task 1 RED: Arrhenius manifest coverage** - `11dba74` (test)
2. **Task 1 GREEN: Arrhenius DemoSpec** - `aa53d01` (feat)
3. **Task 2: Strict compile and warm-start regression locks** - `08bfd73` (test)
4. **Task 3: CLI same-AST evidence regression** - `0d455f9` (test)

**Plan metadata:** summary/state commit for this file.

_Note: Task 2 and Task 3 were test-only locks because the reusable compiler macro, warm-start return path, and CLI artifact path already supported Arrhenius after the DemoSpec was added._

## Files Created/Modified

- `src/eml_symbolic_regression/datasets.py` - Added the `arrhenius` `DemoSpec` using `np.exp(-0.8 / a)`, SymPy candidate `sp.exp(-sp.Float("0.8") / x)`, locked positive domains, and FOR_DEMO provenance.
- `tests/test_proof_dataset_manifest.py` - Added positive-domain, complex-target, finite-target, manifest-domain, provenance, and no-raw-array checks for Arrhenius.
- `tests/test_compiler_warm_start.py` - Added strict compiler metadata, zero-noise warm-start, and CLI same-AST evidence checks for Arrhenius.
- `.planning/phases/50-arrhenius-exact-warm-start-demo/50-01-SUMMARY.md` - Recorded execution evidence and GSD metadata.

## Decisions Made

- Used the normalized dimensionless input `x`, not raw SI temperature, matching `sources/FOR_DEMO.md` guidance.
- Kept the compiler unchanged. The existing `direct_division_template` handles the reciprocal-temperature exponent and records the required macro hit.
- Preserved evidence taxonomy: Arrhenius warm start can have top-level verifier status `recovered`, but the mechanism is `same_ast_return` and the downstream evidence class expectation is `same_ast`.

## Verification

Focused plan verification passed:

```bash
PYTHONPATH=src python -m pytest \
  tests/test_proof_dataset_manifest.py::test_arrhenius_demo_uses_positive_dimensionless_domains \
  tests/test_compiler_warm_start.py::test_compile_arrhenius_uses_direct_division_template \
  tests/test_compiler_warm_start.py::test_arrhenius_warm_start_returns_same_ast_and_verifies \
  tests/test_compiler_warm_start.py::test_cli_warm_start_promotes_arrhenius_same_ast_evidence \
  tests/test_compiler_warm_start.py::test_cli_reports_michaelis_menten_depth_gate_without_promotion \
  tests/test_compiler_warm_start.py::test_cli_reports_planck_as_stretch_without_promotion \
  -q
```

Result: `6 passed in 5.74s`.

## Deviations from Plan

None - plan executed within the requested files. No Arrhenius-specific compiler branch was added.

## Issues Encountered

- Task 2 and Task 3 regression tests passed immediately after Task 1 because Phase 50 research was correct: the existing reusable compiler macro, warm-start classifier, and CLI path already handled the Arrhenius expression once the demo existed. This was treated as a test-only regression lock, not as a reason to alter production compiler logic.

## Known Stubs

None found. Stub scan over modified source and test files found no TODO/FIXME/placeholder text or hardcoded empty values flowing to UI/output behavior.

## User Setup Required

None - no external service configuration required.

## Threat Flags

None. The plan added a local dataset registry entry and tests only; it introduced no new network endpoints, auth paths, file access patterns, schema changes, or trust-boundary changes beyond the planned DemoSpec registry input.

## Next Phase Readiness

Phase 50 can proceed to Plan 02 with Arrhenius available as a built-in positive-domain demo and with strict compile, warm-start, and CLI evidence contracts locked. Michaelis-Menten and Planck remain unsupported/stretch at the existing gates.

## Self-Check: PASSED

- Found summary file `.planning/phases/50-arrhenius-exact-warm-start-demo/50-01-SUMMARY.md`.
- Found modified source/test files `src/eml_symbolic_regression/datasets.py`, `tests/test_proof_dataset_manifest.py`, and `tests/test_compiler_warm_start.py`.
- Found task commits `11dba74`, `aa53d01`, `08bfd73`, and `0d455f9` in git history.
- No tracked file deletions were introduced by task commits.

---
*Phase: 50-arrhenius-exact-warm-start-demo*
*Completed: 2026-04-17*
