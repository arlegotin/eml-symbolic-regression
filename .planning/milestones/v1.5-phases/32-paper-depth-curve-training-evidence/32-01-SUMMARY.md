---
phase: 32-paper-depth-curve-training-evidence
plan: 01
subsystem: proof-benchmarking
tags: [depth-curve, proof, benchmark, campaign, reporting]
requires:
  - phase: 29
    provides: "Claim matrix, measured_depth_curve threshold, proof dataset manifests, and proof-aware artifact schema"
  - phase: 30
    provides: "Measured pure-blind semantics that keep scaffolded evidence out of blind training claims"
  - phase: 31
    provides: "First-class perturbed_tree training path and perturbed_true_tree evidence semantics"
provides:
  - "Deterministic exact depth-curve target inventory at depths 2 through 6"
  - "Measured proof-depth-curve benchmark suite with blind and perturbed rows"
  - "Aggregate depth-curve summaries grouped by depth and training mode"
  - "Campaign preset, report section, and plot hook for proof depth curves"
affects: [phase-32, phase-33, v1.5-proof-reporting]
tech-stack:
  added: []
  patterns: ["Measured paper-boundary reporting with deterministic exact targets"]
key-files:
  created:
    - src/eml_symbolic_regression/depth_curve.py
    - tests/test_depth_curve_targets.py
  modified:
    - src/eml_symbolic_regression/datasets.py
    - src/eml_symbolic_regression/benchmark.py
    - src/eml_symbolic_regression/proof.py
    - src/eml_symbolic_regression/campaign.py
    - README.md
    - tests/test_benchmark_contract.py
    - tests/test_benchmark_runner.py
    - tests/test_benchmark_reports.py
    - tests/test_campaign.py
    - tests/test_proof_contract.py
key-decisions:
  - "The depth curve is measured evidence under `measured_depth_curve`, not a bounded 100% threshold."
  - "Depth-curve perturbed rows require explicit `perturbed_tree` metadata and nonzero perturbation noise."
  - "Deeper blind failures remain visible as expected boundary evidence instead of being treated as regressions."
patterns-established:
  - "Exact synthetic proof inventories can be added as first-class dataset specs without weakening verifier ownership."
  - "Campaign-level proof reporting can summarize measured boundaries by depth while keeping claim denominators honest."
requirements-completed: [CURV-01, CURV-02, CURV-03, CURV-04]
duration: 1 session
completed: 2026-04-16
---

# Phase 32 Plan 01: Paper Depth-Curve Training Evidence Summary

**Deterministic exact depth inventory, measured blind-versus-perturbed suite, and reportable depth-curve evidence**

## Accomplishments

- Added `depth_curve.py` with deterministic exact EML targets at depths 2 through 6 and shared verifier-safe domains.
- Registered the new targets in `datasets.py` so proof dataset manifests, benchmarks, and campaigns can address them by formula ID.
- Added built-in suite `proof-depth-curve` with blind and perturbed rows bound to `paper-blind-depth-degradation` and `measured_depth_curve`.
- Extended aggregate JSON and Markdown to emit per-depth blind and perturbed recovery summaries, seed counts, runtime, and fit metrics.
- Added `proof-depth-curve` campaign preset, report section, and plot output so Phase 33 can consume the depth curve directly.

## Task Commits

No plan-local commits were created in this autonomous working-tree session. The changes remain uncommitted for user review.

## Files Created/Modified

- `src/eml_symbolic_regression/depth_curve.py` - exact target inventory for depths 2 through 6.
- `src/eml_symbolic_regression/datasets.py` - demo-spec registration for the depth-curve targets.
- `src/eml_symbolic_regression/benchmark.py` - built-in suite, proof-contract validation, aggregate depth-curve summaries, and Markdown rendering.
- `src/eml_symbolic_regression/proof.py` - expanded `paper-blind-depth-degradation` case inventory and measured-boundary note.
- `src/eml_symbolic_regression/campaign.py` - `proof-depth-curve` preset, depth-curve table output, and recovery plot hook.
- `README.md` - proof-depth-curve and proof-campaign reproduction commands.
- `tests/test_depth_curve_targets.py` - deterministic inventory, manifest, and verifier checks.
- `tests/test_benchmark_contract.py` - suite expansion and metadata guardrails.
- `tests/test_benchmark_runner.py` - blind failure versus perturbed recovery runner smoke.
- `tests/test_benchmark_reports.py` - per-depth aggregate summary tests.
- `tests/test_campaign.py` - campaign preset/report depth-curve checks.
- `tests/test_proof_contract.py` - claim contract expectations for all depth rows.

## Decisions Made

- The inventory favors exact EML expressions that stay finite on the declared real-axis splits, even at depths 5 and 6.
- Blind rows use fixed small budgets and multiple restarts to remain honest measured evidence rather than exhaustively tuned optimizer showcases.
- Aggregate reporting uses seed counts rather than fabricated confidence intervals because the declared proof suite uses small deterministic seed sets.

## Deviations from Plan

None. The implementation stayed within the planned depth-inventory, measured-threshold, and report-hook scope.

## Verification

- `python -m pytest tests/test_depth_curve_targets.py tests/test_proof_contract.py tests/test_benchmark_contract.py tests/test_benchmark_reports.py tests/test_benchmark_runner.py tests/test_campaign.py -q` -> passed as part of the combined v1.5 proof slice.
- `PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark proof-depth-curve --case depth-2-blind --case depth-2-perturbed --seed 0 --output-dir /tmp/eml-phase32-smoke` -> passed.
- `PYTHONPATH=src python -m eml_symbolic_regression.cli campaign proof-depth-curve --case depth-2-blind --case depth-2-perturbed --seed 0 --output-root /tmp/eml-phase32-campaign --label phase32-depth-curve --overwrite` -> passed.

## Evidence Outcome

- The deterministic inventory exposes one exact target at each depth 2 through 6.
- Live probes and runner tests showed the intended qualitative boundary: shallow blind recovery remains possible while deeper blind rows fail and the paired perturbed rows recover.
- The raw artifact contract is now stable and reproducible through `proof-depth-curve`; Phase 33 consumes that contract to write the final v1.5 proof bundle under `artifacts/proof/v1.5/`.

## Known Stubs

None.

## Issues Encountered

- Depth-curve proof execution is intentionally slower than the surrounding contract tests because it runs real training at depths up to 6.

## Next Phase Readiness

Phase 33 can now assemble the one-command proof bundle because the depth curve already has:

- a deterministic target inventory,
- measured blind and perturbed suite rows,
- campaign/report plumbing,
- and regression tests that lock the measured-boundary semantics.

## Self-Check: PASSED

- Summary file exists at `.planning/phases/32-paper-depth-curve-training-evidence/32-01-SUMMARY.md`.
- Required implementation and test files exist in the worktree.
- `proof-depth-curve` appears in benchmark and campaign discovery.

---
*Phase: 32-paper-depth-curve-training-evidence*
*Completed: 2026-04-16*
