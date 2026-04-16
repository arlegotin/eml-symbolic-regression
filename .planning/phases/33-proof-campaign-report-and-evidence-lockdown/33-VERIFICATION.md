---
phase: 33-proof-campaign-report-and-evidence-lockdown
verified: 2026-04-16T06:55:45Z
status: passed
score: 8/8 must-haves verified
score_verified: 8
score_total: 8
overrides_applied: 0
requirements:
  - id: EVID-01
    status: satisfied
    evidence: "CLI command `proof-campaign` writes the full v1.5 proof bundle root with campaign subdirectories and diagnostics."
  - id: EVID-02
    status: satisfied
    evidence: "The proof report renders claim status, depth-curve summaries, v1.4 context, and explicit out-of-scope claims."
  - id: EVID-03
    status: satisfied
    evidence: "README and the manifest reproducibility block document a single clean-checkout command."
  - id: EVID-04
    status: satisfied
    evidence: "Regression tests cover proof-campaign API/CLI generation and the combined proof-suite slice."
  - id: EVID-05
    status: satisfied
    evidence: "The proof report keeps v1.5 claim denominators separate from v1.4 standard/showcase baselines."
---

# Phase 33: Proof Campaign Report and Evidence Lockdown Verification Report

**Phase Goal:** Users receive a self-contained v1.5 proof report that shows what training can prove, where it is bounded, and what remains unresolved.
**Verified:** 2026-04-16T06:55:45Z
**Status:** passed

## Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | A one-command proof bundle orchestrator exists. | VERIFIED | `src/eml_symbolic_regression/proof_campaign.py` defines `run_proof_campaign()` and the fixed `PROOF_CAMPAIGN_PRESETS` bundle list. |
| 2 | Users can run the bundle from the CLI. | VERIFIED | `cli.py` adds `proof-campaign` with output-root, overwrite, and filter passthrough. |
| 3 | The proof report links bounded and measured claims back to campaign reports and raw run roots. | VERIFIED | `render_proof_campaign_report()` renders report/report-link columns and raw-run links per claim row. |
| 4 | The report includes measured depth-curve evidence. | VERIFIED | `proof_campaign.py` merges `aggregate["depth_curve"]` rows into a dedicated `## Depth Curve` section. |
| 5 | The Phase 31 perturbed basin bound report is preserved inside the proof root. | VERIFIED | `run_proof_campaign()` calls `write_perturbed_basin_bound_report()` into `output_root / diagnostics / basin-bound`. |
| 6 | v1.4 baseline context remains denominator-separated. | VERIFIED | The report includes fixed text stating the denominators are intentionally separate and renders v1.4 baselines in a dedicated section. |
| 7 | The shipped proof root contains all expected bundle artifacts. | VERIFIED | `artifacts/proof/v1.5/` now contains `proof-campaign.json`, `proof-report.md`, five campaign subdirectories, and `diagnostics/basin-bound/`. |
| 8 | Bundle and CLI regression tests pass, and the wider proof workflow regression slice passes. | VERIFIED | `tests/test_proof_campaign.py` passed after the bundle landed, and the combined proof-suite tests passed with `109 passed, 1 warning in 142.45s`. |

**Score:** 8/8 truths verified

## Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Proof-bundle unit/CLI tests | `python -m pytest tests/test_proof_campaign.py -q` | Passed | PASS |
| Full proof-slice regression | `python -m pytest tests/test_depth_curve_targets.py tests/test_proof_contract.py tests/test_benchmark_contract.py tests/test_benchmark_reports.py tests/test_benchmark_runner.py tests/test_campaign.py tests/test_proof_campaign.py -q` | 109 passed, 1 warning | PASS |
| Proof bundle generation | `PYTHONPATH=src python -m eml_symbolic_regression.cli proof-campaign --output-root artifacts/proof/v1.5 --overwrite` | Wrote `proof-campaign.json`, `proof-report.md`, five campaign roots, and `diagnostics/basin-bound/` | PASS |

## Requirements Coverage

| Requirement | Description | Status | Evidence |
|-------------|-------------|--------|----------|
| EVID-01 | One command writes the v1.5 proof artifacts | SATISFIED | `proof-campaign` CLI and `run_proof_campaign()` |
| EVID-02 | Honest report of passed, bounded, failed, and out-of-scope claims | SATISFIED | `proof-report.md` rendering contract |
| EVID-03 | Clean-checkout reproducibility | SATISFIED | README and manifest reproducibility command |
| EVID-04 | Tests lock the proof workflow | SATISFIED | `tests/test_proof_campaign.py` plus the combined proof slice |
| EVID-05 | v1.5 proof results compared against v1.4 without denominator mixing | SATISFIED | dedicated `## v1.4 Context` section and denominator warning text |

## Gaps Summary

No Phase 33 gaps remain. Remaining deeper blind limitations are explicitly listed as out of scope by the proof report rather than left implicit.

---

_Verified: 2026-04-16T06:55:45Z_
_Verifier: Codex_
