---
phase: 31-perturbed-basin-training-and-local-repair
verified: 2026-04-15T20:39:00Z
status: passed
score: 19/19 must-haves verified
score_verified: 19
score_total: 19
overrides_applied: 0
requirements:
  - id: BASN-01
    status: satisfied
    evidence: "Deterministic exact basin target specs and dataset manifests are implemented in basin.py and datasets.py; tests cover declared depths/domains."
  - id: BASN-02
    status: satisfied
    evidence: "proof-perturbed-basin executed 9/9 recovered with bounded_100_percent threshold passed."
  - id: BASN-03
    status: satisfied
    evidence: "Committed basin-bound.json has 6 complete Beer-Lambert rows, raw_supported_noise_max=5.0, repaired_supported_noise_max=35.0, bad_hashes=0."
  - id: BASN-04
    status: satisfied
    evidence: "repair.py provides verifier-gated target-neighborhood repair with serialized moves and benchmark integration."
  - id: BASN-05
    status: satisfied
    evidence: "Evidence classes, return_kind, raw_status, repair_status, aggregate groups, and campaign tables remain separate."
---

# Phase 31: Perturbed Basin Training and Local Repair Verification Report

**Phase Goal:** Users can prove the implementation returns to perturbed true EML solutions inside declared bounds and can inspect/repair near-miss snaps.
**Verified:** 2026-04-15T20:39:00Z
**Status:** passed
**Re-verification:** No - initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Exact EML target-tree generator creates deterministic perturbed proof cases across declared depths and noise envelopes. | VERIFIED | `BasinTargetSpec` inventory defines `basin_depth1_exp`, `basin_depth2_exp_exp`, and `basin_depth3_exp_exp_exp` with exact depths 1/2/3 and explicit split domains in `src/eml_symbolic_regression/basin.py`; `proof-perturbed-basin` declares nonzero noise grids for those targets and Beer-Lambert. |
| 2 | Perturbed basin suite reaches 100% verifier-owned recovery inside the declared bounds. | VERIFIED | Ran `PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark proof-perturbed-basin --output-dir /tmp/eml-phase31-verify-proof-basin`: 9 runs, 0 unsupported, 0 failed. Aggregate threshold: eligible=9, passed=9, rate=1.0, status=passed. |
| 3 | Beer-Lambert high-noise cases are recovered or the supported bound is narrowed with committed evidence. | VERIFIED | `artifacts/diagnostics/phase31-basin-bound/basin-bound.json` has 6 expected rows, 0 missing rows, 0 invalid artifact rows, raw_supported_noise_max=5.0, repaired_supported_noise_max=35.0, claim_recommendation=`probe_supports_35`. |
| 4 | Local snap/discrete repair can inspect and modify failed trained candidates without hiding provenance. | VERIFIED | `repair.py` serializes `RepairMove` and `RepairReport`; benchmark preserves `raw_status` and `return_kind`, writes `repair_status`, and promotes only verifier-recovered repairs to `repaired_candidate`. |
| 5 | Same-AST, verified-equivalent, repaired, snapped-but-failed, soft-fit-only, and unsupported outcomes remain separately reported. | VERIFIED | `proof.py` keeps separate evidence classes; `benchmark.py` groups by evidence_class/return_kind/raw_status/repair_status and restricts perturbed-basin threshold counting to `perturbed_true_tree_recovered` and `repaired_candidate`. |
| 6 | User can generate deterministic exact EML basin targets at declared depths before perturbed training. | VERIFIED | `basin_target_specs()` is deterministic; spot-check printed depths/nodes/domains: depth1=1/3 nodes, depth2=2/5 nodes, depth3=3/7 nodes. |
| 7 | User can run `proof-perturbed-basin` through first-class `perturbed_tree` with `perturbed_true_tree_training`. | VERIFIED | `START_MODES` includes `perturbed_tree`; suite expansion spot-check showed 9 runs, only `perturbed_tree`, only `perturbed_true_tree_training`, noises `[0.05, 0.1, 0.25, 5.0]`. |
| 8 | Same-AST return after nonzero perturbation counts only on the perturbed-tree path, with `return_kind` and `raw_status` recorded. | VERIFIED | `evidence_class_for_payload()` requires start_mode `perturbed_tree`, training_mode `perturbed_true_tree_training`, recovered status, and nonzero perturbation; test coverage asserts warm-start same-AST does not become perturbed evidence. |
| 9 | Compiler warm-start, scaffolded blind, warm-start same-AST, and perturbed true-tree recovery remain distinct. | VERIFIED | `proof.py` defines separate classes for `compiler_warm_start_recovered`, `scaffolded_blind_training_recovered`, `same_ast`, and `perturbed_true_tree_recovered`; threshold override in `benchmark.py` rejects non-perturbed classes for the perturbed-basin claim. |
| 10 | User can apply local repair to failed perturbed-tree candidates and inspect every attempted slot move. | VERIFIED | `repair_perturbed_candidate()` builds snapped and target slot maps, attempts target-neighborhood moves, and records attempted/accepted moves with slot, source, descendants, pruned assignments, and verifier status. |
| 11 | A repaired candidate is classified as `repaired_candidate`, never raw `perturbed_true_tree_recovered`. | VERIFIED | `evidence_class_for_payload()` returns `repaired_candidate` when top-level status is `repaired_candidate` or `repair_status == "repaired"` before raw perturbed recovery classification. |
| 12 | Raw return kind, raw status, repair status, accepted moves, verifier status, and evidence class remain visible. | VERIFIED | Benchmark payload includes `return_kind`, `raw_status`, `repair`, `repair_status`, `trained_eml_verification`, and derived `evidence_class`; metrics include repair move counts and repair verifier status. |
| 13 | Benchmark summaries, aggregate groups, and Markdown distinguish raw status, return kind, repair status, and evidence class. | VERIFIED | `aggregate_evidence()` groups by `evidence_class`, `return_kind`, `raw_status`, and `repair_status`; aggregate Markdown includes "By Return Kind", "By Raw Status", and "By Repair Status". |
| 14 | Repair is verifier-gated with held-out, extrapolation, and high-precision checks. | VERIFIED | `repair_perturbed_candidate()` accepts a repair only when `verify_candidate(...).status == "recovered"` over supplied verification splits; `RepairReport.as_dict()` emits `repaired_ast` only for verified repaired candidates. |
| 15 | Beer-Lambert bound evidence includes bounded rows and high-noise probe rows. | VERIFIED | Committed bound report rows include 2 bounded noise-5 rows and 4 probe rows at noise 15 and 35. |
| 16 | High-noise probe rows remain visible with artifact paths, reasons, return kinds, repair status, and changed-slot metrics. | VERIFIED | Bound report rows include `artifact_path`, `artifact_sha256`, `reason`, `return_kind`, `raw_status`, `repair_status`, `changed_slot_count`, and `repair_accepted_move_count`. |
| 17 | Supported perturbation bounds are machine-readable continuous prefixes, not isolated passing maxima. | VERIFIED | `_supported_noise_prefix()` requires expected seeds at each grid noise and breaks on missing/incomplete/failing lower noise. Tests include non-contiguous higher-pass fixtures. |
| 18 | Campaign and CLI outputs keep proof success rates separate from Beer-Lambert probes. | VERIFIED | `proof-basin` preset maps to `proof-perturbed-basin`; report text names `proof-perturbed-basin-beer-probes` as separate, outside bounded threshold tables. CLI has explicit `diagnostics basin-bound`. |
| 19 | Stable `basin-bound.json` and `basin-bound.md` evidence files exist under the phase diagnostics directory. | VERIFIED | Both committed files exist; checksum scan over all 6 linked raw artifacts returned `bad_hashes=0`; `git status --short` remained clean after rerunning the full test slice. |

**Score:** 19/19 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/eml_symbolic_regression/basin.py` | Exact target inventory and perturbed true-tree training wrapper | VERIFIED | Exists, substantive; exports `BasinTargetSpec`, `BasinTrainingResult`, target lookup, and `fit_perturbed_true_tree()`. |
| `src/eml_symbolic_regression/datasets.py` | Basin targets exposed as demos and manifests | VERIFIED | `_basin_demo_specs()` wraps basin specs into `DemoSpec`; `proof_dataset_manifest()` hashes deterministic splits. |
| `src/eml_symbolic_regression/benchmark.py` | Perturbed runner, repair integration, aggregate evidence | VERIFIED | Contains `perturbed_tree` mode, bounded/probe suites, runner dispatch, repair invocation, evidence mapping, and threshold summary. |
| `src/eml_symbolic_regression/proof.py` | Claim/evidence class contract | VERIFIED | Declares `perturbed_true_tree_training`, `perturbed_true_tree_recovered`, `repaired_candidate`, and concrete perturbed-basin case IDs. |
| `src/eml_symbolic_regression/repair.py` | Local repair engine | VERIFIED | Implements serializable repair dataclasses and verifier-gated target-neighborhood repair. |
| `src/eml_symbolic_regression/diagnostics.py` | Beer-Lambert bound report builder/writer | VERIFIED | Builds continuous-prefix bound report, expected seed/noise coverage, durable artifact checksum validation, JSON/Markdown writer. |
| `src/eml_symbolic_regression/campaign.py` | Proof-basin campaign hooks and taxonomy propagation | VERIFIED | Adds `proof-basin`, return/raw/repair CSV columns, and proof-basin report taxonomy text. |
| `src/eml_symbolic_regression/cli.py` | User-facing bound report command | VERIFIED | Adds `diagnostics basin-bound` and accepts `perturbed_tree` via shared start-mode choices. |
| `tests/test_basin_targets.py` | Target and wrapper tests | VERIFIED | Covers deterministic IDs, depths, domains, manifest determinism, verifier recovery, and perturbed wrapper manifest. |
| `tests/test_benchmark_contract.py` | Suite/start-mode validation tests | VERIFIED | Covers perturbed proof suite expansion, nonzero perturbation, probe metadata, CLI filter, invalid metadata rejection. |
| `tests/test_benchmark_runner.py` | Runner artifact/evidence tests | VERIFIED | Covers perturbed-tree recovery artifacts and repaired artifact promotion. |
| `tests/test_benchmark_reports.py` | Aggregate threshold/taxonomy tests | VERIFIED | Covers shallow vs perturbed threshold restrictions and distinct outcome taxonomy. |
| `tests/test_repair.py` | Repair serialization and verifier-gating tests | VERIFIED | Covers move serialization, terminal/child/subtree repair, and non-recovered rejection. |
| `tests/test_basin_bound_report.py` | Bound report and evidence tests | VERIFIED | Covers continuous-prefix support, missing seed rows, durable checksums, CLI, committed evidence, integration generation. |
| `tests/test_campaign.py` | Campaign preset/table/report tests | VERIFIED | Covers `proof-basin`, CSV columns, report taxonomy, and probe separation. |
| `tests/test_diagnostics.py` | Diagnostics compatibility tests | VERIFIED | Confirms bound builder export and existing diagnostics behavior. |
| `tests/test_proof_contract.py` | Claim/evidence policy tests | VERIFIED | Covers perturbed claim inventory and evidence class separation. |
| `artifacts/diagnostics/phase31-basin-bound/basin-bound.json` | Machine-readable Beer-Lambert evidence | VERIFIED | Schema `eml.perturbed_basin_bound_report.v1`; 6 rows; no missing/invalid artifact evidence. |
| `artifacts/diagnostics/phase31-basin-bound/basin-bound.md` | Human-readable Beer-Lambert evidence | VERIFIED | Lists bounded and probe rows, row provenance, evidence classes, return/raw/repair statuses, and checksums. |
| `pyproject.toml` | Test marker registration | VERIFIED | Registers the `integration` marker under pytest options. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `benchmark.py` | `basin.py` | `start_mode == "perturbed_tree"` dispatches to `fit_perturbed_true_tree()` | VERIFIED | GSD key-link verification passed; source import and dispatch exist. |
| `benchmark.py` | `proof.py` | `paper-perturbed-true-tree-basin` rows use `perturbed_true_tree_training` | VERIFIED | Suite metadata and validation enforce the training mode. |
| `benchmark.py` | `datasets.py` | Basin formula IDs resolve through `demo_specs()` and `proof_dataset_manifest()` | VERIFIED | Synthetic basin IDs are available as demos and manifested deterministically. |
| `benchmark.py` | `repair.py` | Perturbed-tree failures call `repair_perturbed_candidate()` | VERIFIED | Repair is invoked only after raw basin failure and preserves raw status. |
| `repair.py` | `master_tree.py` | Repair replays snapped slot decisions with `SoftEMLTree.set_slot()` | VERIFIED | Candidate reconstruction uses slot maps and `set_slot()` replay. |
| `repair.py` | `verify.py` | Accepted repair requires `verify_candidate(...).status == "recovered"` | VERIFIED | Code path gates acceptance on verifier recovery. |
| `diagnostics.py` | Benchmark aggregates/artifacts | Bound report reads aggregate rows and linked run artifacts | VERIFIED | Rows include artifact paths and recomputed SHA-256 checksums. |
| `campaign.py` | `diagnostics.py` semantics | Campaign reports name the probe suite separately | VERIFIED | Report text prevents probe rows from entering proof threshold interpretation. |
| `cli.py` | `diagnostics.py` | `diagnostics basin-bound` calls `write_perturbed_basin_bound_report()` | VERIFIED | CLI parser and command function are wired. |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `datasets.py` | `DemoSpec` basin entries | `basin_target_specs()` | Yes: three exact EML expressions with explicit domains and provenance | VERIFIED |
| `benchmark.py` | `BenchmarkRun` and payload fields | `load_suite("proof-perturbed-basin").expanded_runs()` and `fit_perturbed_true_tree()` | Yes: real training/verification payloads written as run JSON | VERIFIED |
| `repair.py` | `RepairReport` | Raw failed `FitResult`, `EmbeddingResult`, and verification splits | Yes: accepted only after `verify_candidate()` recovery | VERIFIED |
| `benchmark.py` aggregates | `runs`, `thresholds`, `groups` | `aggregate_evidence()` over actual run payloads | Yes: full proof suite rerun yielded 9 run summaries and a passed threshold | VERIFIED |
| `diagnostics.py` bound report | `rows`, supported maxima | Bounded/probe aggregate JSON and linked raw artifacts | Yes: committed report recomputes expected rows and artifact checksums | VERIFIED |
| `campaign.py` / `cli.py` | User-facing reports/commands | Benchmark aggregates and diagnostics writer | Yes: CLI and campaign preset spot-checks list Phase 31 suites and commands | VERIFIED |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Phase 31 test slice | `python -m pytest tests/test_basin_targets.py tests/test_benchmark_contract.py tests/test_benchmark_runner.py tests/test_proof_contract.py tests/test_repair.py tests/test_benchmark_reports.py tests/test_basin_bound_report.py tests/test_campaign.py tests/test_diagnostics.py -q` | 124 passed, 2 warnings (`semantics.py:110` overflow warning in high-noise paths) | PASS |
| Complete bounded perturbed suite | `PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark proof-perturbed-basin --output-dir /tmp/eml-phase31-verify-proof-basin` | 9 runs, 0 unsupported, 0 failed; aggregate threshold passed 9/9 | PASS |
| Suite expansion | `PYTHONPATH=src python - <<'PY' ... load_suite(...) ... PY` | `proof-perturbed-basin` has 9 `perturbed_tree` runs with `perturbed_true_tree_training`; probe suite has 4 high-noise runs | PASS |
| Bound evidence checksum scan | Python checksum scan over `basin-bound.json` row artifacts | rows=6, bad_hashes=0, raw_supported=5.0, repaired_supported=35.0 | PASS |
| CLI discovery | `PYTHONPATH=src python -m eml_symbolic_regression.cli list-benchmarks/list-campaigns/list-claims` | Listed both perturbed-basin benchmark suites, `proof-basin` campaign, and perturbed true-tree claim | PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| BASN-01 | 31-01 | User can generate exact EML target trees at declared depths and perturb active categorical slots under deterministic noise envelopes. | SATISFIED | `basin.py` defines deterministic exact targets; `fit_perturbed_true_tree()` embeds and applies `PerturbationConfig`; tests cover IDs, depths, node counts, domains, manifests, and wrapper status. |
| BASN-02 | 31-01, 31-02, 31-03 | User receives 100% verifier-owned recovery for the declared perturbed basin proof suite. | SATISFIED | Full suite rerun passed threshold 9/9 with evidence class `perturbed_true_tree_recovered`; committed Beer bounded rows also passed 2/2. |
| BASN-03 | 31-03 | User can run Beer-Lambert perturbation repair experiments and either recover high-noise cases or narrow supported perturbation bound with evidence. | SATISFIED | Bound report includes bounded noise 5 and probes 15/35; high-noise probes are visible and repaired-supported through 35 with committed raw artifacts/checksums. |
| BASN-04 | 31-02 | User can apply local snap/discrete repair around failed trained candidates and inspect changed slots/subtrees. | SATISFIED | `repair.py` records move kind, slot before/after, source, descendant/pruned assignments, subtree root, verifier status; benchmark artifacts include accepted move counts. |
| BASN-05 | 31-01, 31-02, 31-03 | User can verify same-AST, verified-equivalent, repaired, snapped-but-failed, soft-fit-only, unsupported outcomes remain distinct. | SATISFIED | `proof.py` evidence classes are distinct; `benchmark.py` classify/evidence/aggregate logic keeps fields separate; tests cover mixed synthetic rows and forbidden evidence classes. |

No additional Phase 31 BASN requirements were orphaned in `.planning/REQUIREMENTS.md`; all BASN-01 through BASN-05 are claimed by Phase 31 plans and verified above.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `src/eml_symbolic_regression/benchmark.py` | 533 | `placeholder` variable name | Info | Benign temporary `BenchmarkRun` used to compute stable run ID before assigning artifact path; not a stub. |
| Multiple implementation files | n/a | Empty list/dict initialization and `None` defaults | Info | Local accumulators/type defaults only; no user-visible hollow data path found. |

No TODO/FIXME/placeholder implementation text, no "not implemented" path, and no blocker stub pattern was found in Phase 31 implementation files.

### Human Verification Required

None. This phase is backend/CLI evidence generation with deterministic artifacts and automated checks; no visual, real-time, external service, or UX-only behavior remains unverified.

### Gaps Summary

No gaps found. The code implements the perturbed true-tree runner, deterministic exact targets, verifier-gated local repair, Beer-Lambert bound evidence, and evidence taxonomy separation. The declared proof suite reaches 100% verifier-owned recovery inside bounds, and committed Beer-Lambert evidence is durable and checksum-verified.

---

_Verified: 2026-04-15T20:39:00Z_
_Verifier: Claude (gsd-verifier)_
