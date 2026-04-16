---
phase: 29-paper-claim-contract-and-proof-dataset-harness
verified: 2026-04-15T14:29:29Z
status: passed
score: 10/10 must-haves verified
overrides_applied: 0
---

# Phase 29: Paper Claim Contract and Proof Dataset Harness Verification Report

**Phase Goal:** Users can run proof suites whose datasets, training modes, thresholds, and claim labels are explicitly tied to the paper-grounded statements being tested.
**Verified:** 2026-04-15T14:29:29Z
**Status:** passed
**Re-verification:** No - initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Claim matrix maps v1.5 paper claims to statements, source refs, suite/case IDs, claim classes, and policies. | VERIFIED | `claim_matrix()` returns the four stable claim IDs, each with source refs including `sources/paper.pdf`, `.planning/REQUIREMENTS.md`, and `.planning/ROADMAP.md`. |
| 2 | Threshold policies distinguish bounded 100% proof, measured depth curves, and contract context. | VERIFIED | `threshold_policies()` defines `bounded_100_percent` with `required_rate=1.0`, `measured_depth_curve` with `policy_type="measured_rate"`, and `contract_context` with `policy_type="context_only"`. |
| 3 | Dataset generator produces deterministic train, held-out, and extrapolation manifests with provenance and normalization metadata. | VERIFIED | `proof_dataset_manifest()` calls `DemoSpec.make_splits()`, emits split domains/counts/signatures, provenance, normalization flag, and a manifest digest while omitting raw arrays. |
| 4 | Proof-aware benchmark run artifacts expose claim, training mode, evidence class, threshold, dataset, budget, and provenance fields. | VERIFIED | `_base_run_payload()` writes claim/threshold/dataset_manifest/budget/provenance, and `execute_benchmark_run()` derives `evidence_class` after execution before writing JSON. |
| 5 | Proof-suite validation fails closed for unknown claims, missing thresholds, unsupported training modes, and caller-supplied evidence classes. | VERIFIED | `BenchmarkCase.validate()` wraps proof errors as `BenchmarkValidationError(reason="invalid_proof_contract")`; tests cover unknown claims/policies, missing thresholds, invalid training modes, and suite-supplied `evidence_class`. |
| 6 | Artifact schema distinguishes blind, warm-start, perturbed true-tree, compile-only, catalog, unsupported, failed, snapped, soft-fit, repaired, same-AST, and verified-equivalent evidence classes. | VERIFIED | `EVIDENCE_CLASSES` declares the vocabulary, and `evidence_class_for_payload()` maps all observed/reserved outcomes, including `perturbed_true_tree_recovered`. |
| 7 | Aggregates count evidence classes separately and evaluate claim thresholds from allowed evidence classes, not raw verifier status alone. | VERIFIED | `aggregate_evidence()` includes `counts.evidence_classes`, `groups.evidence_class`, and `_threshold_summary()` uses `policy.allowed_evidence_classes` per `(claim_id, threshold_policy_id)`. |
| 8 | CLI can inspect claims and generate proof dataset manifests without running training. | VERIFIED | `list-claims` reads `list_claims()` and `proof-dataset` calls `proof_dataset_manifest()`; CLI smoke tests execute both through subprocess. |
| 9 | Campaign CSVs and manifests propagate claim, training mode, evidence class, threshold policy, dataset signature, budget/provenance context, and threshold rows. | VERIFIED | `campaign.py` writes proof columns in `runs.csv`, grouped proof tables, and `manifest["thresholds"]` plus `output.tables` paths. |
| 10 | Campaign reports keep proof-suite threshold status separate from showcase recovery summaries. | VERIFIED | `write_campaign_report()` conditionally adds `## Proof Contract` from aggregate threshold rows and includes explicit guardrail wording excluding catalog/compile-only proof counting. |

**Score:** 10/10 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/eml_symbolic_regression/proof.py` | Paper claim matrix, threshold policies, evidence/training vocabularies, validation helpers | VERIFIED | 313 lines; exports `PaperClaim`, `ThresholdPolicy`, `claim_matrix`, `threshold_policies`, `threshold_policy`, `validate_claim_reference`, `list_claims`. |
| `src/eml_symbolic_regression/datasets.py` | Formula provenance and deterministic proof dataset manifests | VERIFIED | 252 lines; `DemoSpec` has provenance fields; `proof_dataset_manifest()` signs split metadata from `make_splits()`. |
| `src/eml_symbolic_regression/benchmark.py` | Proof-aware suite/run schema, evidence classes, threshold aggregation | VERIFIED | 1323 lines; proof metadata is validated, serialized, classified, and aggregated. |
| `src/eml_symbolic_regression/cli.py` | Claim inspection and proof dataset CLI commands | VERIFIED | 392 lines; subcommands `list-claims` and `proof-dataset` are registered and tested. |
| `src/eml_symbolic_regression/campaign.py` | Campaign table, manifest, and report proof metadata propagation | VERIFIED | 923 lines; adds `proof-shallow`, proof CSV columns/tables, manifest thresholds, and report section. |
| `tests/test_proof_contract.py` | Claim matrix and threshold policy tests | VERIFIED | Stable IDs, evidence-class policy boundaries, depth-curve reporting, and fail-closed proof errors are tested. |
| `tests/test_proof_dataset_manifest.py` | Dataset manifest determinism and provenance tests | VERIFIED | Same-seed determinism, seed-sensitive signatures, split domains/counts, provenance, no raw arrays, and invalid sampling are tested. |
| `tests/test_benchmark_contract.py` | Benchmark proof metadata and validation tests | VERIFIED | Legacy compatibility, proof metadata serialization, suite/case scope, fail-closed errors, and `v1.5-shallow-proof` expansion are tested. |
| `tests/test_benchmark_runner.py` | Run artifact and CLI smoke tests | VERIFIED | Artifact proof fields, derived evidence classes, CLI `list-claims`, CLI `proof-dataset`, execution-error fallback, and compile evidence are tested. |
| `tests/test_benchmark_reports.py` | Aggregate evidence-class and threshold tests | VERIFIED | Evidence counts, bounded threshold policy, measured depth curve reporting, warm-start depth gate, and aggregate markdown are tested. |
| `tests/test_campaign.py` | Campaign proof metadata tests | VERIFIED | Proof campaign preset, CSV columns, manifest thresholds/tables, proof report section, and legacy smoke behavior are tested. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `proof.py` | `.planning/REQUIREMENTS.md` | Stable claim IDs and policies implement CLAIM-01/CLAIM-04 | WIRED | GSD key-link check found the required claim/policy patterns. |
| `datasets.py` | `DemoSpec.make_splits` | Manifest helper computes metadata from deterministic split generator | WIRED | Manual trace: `proof_dataset_manifest()` calls `spec.make_splits(points=points, seed=seed)` before hashing split inputs/targets. |
| `benchmark.py` | `proof.py` | Claim and threshold validation imports | WIRED | Imports `paper_claim`, `threshold_policy`, `validate_claim_reference`, `TRAINING_MODES`, and `EVIDENCE_CLASSES`; validation and aggregation use them. |
| `benchmark.py` | `datasets.py` | Run payload dataset manifest | WIRED | `_base_run_payload()` calls `proof_dataset_manifest()` and embeds `dataset_manifest` plus `provenance`. |
| `aggregate_evidence` | `ThresholdPolicy.allowed_evidence_classes` | Claim threshold summaries use evidence-class counts | WIRED | Manual trace: `_threshold_summary()` loads `threshold_policy()` and increments `passed` only when `evidence_class in policy.allowed_evidence_classes`. |
| `cli.py` | `proof.py` | `list-claims` command | WIRED | `list_claims_command()` calls `list_claims()` and prints claim class, threshold, and suites. |
| `cli.py` | `datasets.py` | `proof-dataset` command | WIRED | `proof_dataset_command()` calls `proof_dataset_manifest()` and writes JSON through `_write_json()`. |
| `campaign.py` | `aggregate_evidence` | CSV/report rows consume aggregate proof fields | WIRED | `run_campaign()` computes aggregate evidence; table/report writers consume `runs`, `counts.evidence_classes`, and `thresholds`. |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `datasets.py` | `splits`, `provenance`, `manifest_sha256` | `DemoSpec.make_splits()` plus `formula_provenance()` | Yes - generated arrays are hashed and excluded from output; source metadata comes from each `DemoSpec`. | FLOWING |
| `benchmark.py` | `dataset_manifest`, `threshold`, `evidence_class` | `_base_run_payload()`, `_execute_benchmark_run_inner()`, `evidence_class_for_payload()` | Yes - run artifacts include generated manifests, claim policy dictionaries, and derived evidence classes. | FLOWING |
| `benchmark.py` | `aggregate["thresholds"]` | `_run_summary()` and `_threshold_summary()` | Yes - thresholds are grouped from actual run summaries and policy registries. | FLOWING |
| `cli.py` | CLI output JSON/claim lines | `list_claims()` and `proof_dataset_manifest()` | Yes - commands call registry/helper functions directly; no training path invoked. | FLOWING |
| `campaign.py` | CSV rows, manifest thresholds, report proof table | `aggregate_evidence(result)` | Yes - campaign tables and reports are populated from aggregate run/threshold rows. | FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Phase-specific proof/benchmark/campaign tests pass | `python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_reports.py tests/test_benchmark_runner.py tests/test_campaign.py tests/test_proof_contract.py tests/test_proof_dataset_manifest.py -q` | 62 passed, 1 existing `semantics.py` overflow warning | PASS |
| Full test suite passes | `python -m pytest -q` | 98 passed, 2 existing `semantics.py` overflow warnings | PASS |
| Claim matrix and thresholds load | `PYTHONPATH=src python -c "... claim_matrix(); threshold_policy(...)"` | Four stable claim IDs printed; bounded rate is `1.0`; measured policy type is `measured_rate` | PASS |
| Dataset manifest is deterministic and seed-sensitive | `PYTHONPATH=src python -c "... proof_dataset_manifest('exp', points=12, seed=7) ..."` | Same seed matched, schema was `eml.proof_dataset_manifest.v1`, train split count was 12, changed seed changed digest | PASS |
| Built-in proof suite expands proof-aware runs | `PYTHONPATH=src python -c "... load_suite('v1.5-shallow-proof').expanded_runs() ..."` | 12 runs, all claim `paper-shallow-blind-recovery`, threshold `bounded_100_percent`, training mode `blind_training` | PASS |
| CLI claim inspection works | `PYTHONPATH=src python -m eml_symbolic_regression.cli list-claims` | Printed all four claim IDs with class, threshold, and suite labels | PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| CLAIM-01 | 29-01, 29-02, 29-03 | User can inspect a paper-claim matrix mapping v1.5 experiments to paper-grounded statements. | SATISFIED | `claim_matrix()`, `paper_claim()`, `list_claims()`, CLI `list-claims`, and tests lock all four claim IDs/classes/source refs. |
| CLAIM-02 | 29-01, 29-02, 29-03 | User can generate deterministic proof datasets with seeds, splits, normalization metadata, target formulas, and provenance. | SATISFIED | `proof_dataset_manifest()` emits schema, seed, split metadata, signatures, provenance, normalization flag, digest; CLI and tests verify it. |
| CLAIM-03 | 29-02, 29-03 | User can distinguish training/evidence modes and failure classes in every proof artifact. | SATISFIED | `TRAINING_MODES`, `EVIDENCE_CLASSES`, `evidence_class_for_payload()`, run artifacts, aggregate rows, CSV columns, and tests cover the taxonomy. |
| CLAIM-04 | 29-01, 29-02, 29-03 | User receives explicit pass/fail thresholds for bounded proof suites and measured depth-curve suites. | SATISFIED | `ThresholdPolicy`, claim threshold IDs, `_threshold_summary()`, aggregate markdown, campaign manifest/report, and tests cover bounded, measured, and context policies. |

No Phase 29 requirements are orphaned in `.planning/REQUIREMENTS.md`: CLAIM-01 through CLAIM-04 are mapped to Phase 29, and all four appear in plan frontmatter across the phase.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `src/eml_symbolic_regression/benchmark.py` | 461 | Local variable named `placeholder` | Info | This is not a stub. It is a temporary `BenchmarkRun` used to compute stable run IDs before constructing the final artifact path. |
| `src/eml_symbolic_regression/campaign.py` | 683 | `return []` | Info | This is intentional empty-section behavior when a campaign has no claim IDs; legacy smoke campaigns should omit the proof section. |

No blocking TODO/FIXME/placeholder prose, hardcoded empty user-visible payloads, or console-only implementations were found in the phase files.

### Human Verification Required

None. The phase delivers local Python contracts, CLI commands, JSON/CSV/Markdown artifacts, and tests that can be verified programmatically. No visual UI, real-time behavior, external service, or subjective flow is required for goal acceptance.

### Gaps Summary

No gaps found. The exact Phase 30 shallow inventory expansion, Phase 31 perturbed true-tree execution path, Phase 32 depth-curve experiments, and Phase 33 one-command proof report are explicitly assigned to later roadmap phases, so they are not Phase 29 blockers.

---

_Verified: 2026-04-15T14:29:29Z_
_Verifier: Claude (gsd-verifier)_
