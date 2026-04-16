---
phase: 32-paper-depth-curve-training-evidence
verified: 2026-04-16T06:55:45Z
status: passed
score: 10/10 must-haves verified
score_verified: 10
score_total: 10
overrides_applied: 0
requirements:
  - id: CURV-01
    status: satisfied
    evidence: "Built-in suite `proof-depth-curve` covers depths 2 through 6 for both blind and perturbed training with deterministic seeds, budgets, and target IDs."
  - id: CURV-02
    status: satisfied
    evidence: "Aggregate JSON/Markdown and campaign report plumbing now emit per-depth recovery rates, seed counts, runtime, and fit metrics by training mode."
  - id: CURV-03
    status: satisfied
    evidence: "The measured depth-curve claim keeps deeper blind failures visible and report text explicitly frames them as expected paper-boundary evidence."
  - id: CURV-04
    status: satisfied
    evidence: "Raw artifact generation is reproducible through `benchmark proof-depth-curve`, `campaign proof-depth-curve`, and the Phase 33 proof bundle root."
---

# Phase 32: Paper Depth-Curve Training Evidence Verification Report

**Phase Goal:** Users can reproduce the paper's qualitative depth behavior using this implementation's real training runs, metrics, and artifacts.
**Verified:** 2026-04-16T06:55:45Z
**Status:** passed

## Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | A deterministic exact EML inventory exists for depths 2 through 6. | VERIFIED | `src/eml_symbolic_regression/depth_curve.py` defines `DepthCurveTargetSpec` entries `depth_curve_depth2` through `depth_curve_depth6` with explicit domains and provenance. |
| 2 | The inventory is exposed as first-class dataset/demo specs. | VERIFIED | `datasets.py` registers the depth-curve targets so manifests and benchmarks can resolve them by formula ID. |
| 3 | Users can run a measured blind and perturbed depth curve through a built-in proof suite. | VERIFIED | `benchmark.py` adds `proof-depth-curve` with ten rows: five blind and five perturbed-tree runs across depths 2 through 6. |
| 4 | The proof contract rejects malformed depth-curve metadata. | VERIFIED | `benchmark.py` validation constrains the claim to `measured_depth_curve`, allows only blind or perturbed-tree start modes, and rejects perturbed rows with zero perturbation noise. |
| 5 | Aggregate evidence groups results by depth and training mode. | VERIFIED | `aggregate_evidence()` adds `depth_curve`; `render_aggregate_markdown()` emits a dedicated `## Depth Curve` table. |
| 6 | Campaign output surfaces the depth curve in reproducible user-facing form. | VERIFIED | `campaign.py` adds `proof-depth-curve`, writes `depth_curve_csv`, emits a depth-curve report section, and generates a recovery plot. |
| 7 | Depth-4 runner smoke preserves the expected qualitative split. | VERIFIED | `tests/test_benchmark_runner.py::test_depth_curve_runner_records_blind_failure_and_perturbed_recovery` asserts the blind row fails while the paired perturbed row recovers with explicit perturbed-tree metadata. |
| 8 | The claim contract enumerates every depth-curve row and keeps perturbed rows comparative. | VERIFIED | `proof.py` lists all ten case IDs under `paper-blind-depth-degradation` and notes that perturbed rows are comparative basin evidence, not a bounded 100% claim. |
| 9 | Focused CLI reproduction commands work end-to-end. | VERIFIED | The benchmark and campaign smoke commands for `proof-depth-curve` passed in this session using `/tmp` output roots. |
| 10 | The Phase 32 regression slice passes. | VERIFIED | `python -m pytest tests/test_depth_curve_targets.py tests/test_proof_contract.py tests/test_benchmark_contract.py tests/test_benchmark_reports.py tests/test_benchmark_runner.py tests/test_campaign.py -q` passed as part of the combined v1.5 proof slice. |

**Score:** 10/10 truths verified

## Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Depth inventory tests | `python -m pytest tests/test_depth_curve_targets.py -q` | Passed in combined slice | PASS |
| Depth-curve contract/report slice | `python -m pytest tests/test_proof_contract.py tests/test_benchmark_contract.py tests/test_benchmark_reports.py tests/test_benchmark_runner.py tests/test_campaign.py -q` | Passed in combined slice | PASS |
| CLI benchmark smoke | `PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark proof-depth-curve --case depth-2-blind --case depth-2-perturbed --seed 0 --output-dir /tmp/eml-phase32-smoke` | Wrote suite result and raw run artifacts | PASS |
| CLI campaign smoke | `PYTHONPATH=src python -m eml_symbolic_regression.cli campaign proof-depth-curve --case depth-2-blind --case depth-2-perturbed --seed 0 --output-root /tmp/eml-phase32-campaign --label phase32-depth-curve --overwrite` | Wrote report, manifest, aggregate files, and raw runs | PASS |

## Requirements Coverage

| Requirement | Description | Status | Evidence |
|-------------|-------------|--------|----------|
| CURV-01 | Deterministic depth-curve experiment across blind and perturbed training for depths 2 through 6 | SATISFIED | `proof-depth-curve` suite plus deterministic target inventory |
| CURV-02 | Recovery rates, seed counts, losses, runtime, and snap metrics by depth and mode | SATISFIED | `aggregate_evidence()` depth-curve rows and campaign report/table output |
| CURV-03 | Honest narrative versus paper qualitative claims | SATISFIED | `proof.py`, campaign report text, and Markdown depth-curve section |
| CURV-04 | Preserved or reproducible raw artifacts for future comparisons | SATISFIED | Stable benchmark/campaign commands and Phase 33 proof-bundle integration |

## Gaps Summary

No Phase 32 gaps remain. The phase intentionally reports measured blind degradation instead of promoting a bounded deep-blind success claim, which matches the milestone scope and the source paper.

---

_Verified: 2026-04-16T06:55:45Z_
_Verifier: Codex_
