# Phase 29: Paper Claim Contract and Proof Dataset Harness - Research

**Researched:** 2026-04-15
**Domain:** Benchmark/proof-suite contract, deterministic dataset manifests, paper-claim taxonomy
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

Source: `.planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md` [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md]

### Locked Decisions

### Claim Taxonomy
- **D-01:** Treat verifier-owned training recovery as the only evidence class that can satisfy bounded 100% training-proof claims.
- **D-02:** Keep catalog verification, compile-only verification, blind training, compiler warm-start training, perturbed true-tree training, repaired candidates, unsupported cases, and failed cases as distinct artifact classes.
- **D-03:** Add a paper-claim matrix with stable claim IDs, paper-grounded statement text, source references, supported claim class, associated suite/cases, and threshold policy.
- **D-04:** Declare pass/fail thresholds before execution; bounded proof suites require 100% verifier-owned recovery, while depth-curve suites report measured behavior without treating expected deeper blind failures as regressions.

### Dataset Contract
- **D-05:** Generate deterministic train, held-out, and extrapolation splits with fixed seeds, sample counts, domains, variable name, formula ID, and normalization metadata.
- **D-06:** Preserve formula provenance in artifacts: symbolic expression, source document, FOR_DEMO or paper linkage, and whether the target is a normalized dimensionless law.
- **D-07:** Generate proof datasets on demand and serialize their metadata into run artifacts; do not commit bulky raw arrays unless a later evidence-lockdown phase explicitly requires them.
- **D-08:** Attach optimizer budgets, seeds, perturbation noise envelopes, and suite thresholds to the suite/case contract so CLI arguments cannot silently redefine proof claims.

### Artifact Schema
- **D-09:** Extend benchmark/proof artifacts rather than creating an unrelated reporting system; reuse existing `benchmark.py`, `campaign.py`, dataset split, verifier, and diagnostics patterns.
- **D-10:** Every run artifact should expose `claim_id`, `claim_class`, `training_mode`, `evidence_class`, `threshold`, `dataset`, `budget`, and `provenance` fields in stable JSON-friendly structures.
- **D-11:** Aggregates must count evidence classes separately, especially blind verifier recovery versus compile/catalog success, unsupported, soft-fit-only, snapped-but-failed, repaired, same-AST, and verified-equivalent outcomes.
- **D-12:** Validation should fail closed when a suite references an unknown claim, missing threshold, invalid split, unsupported training mode, or ambiguous evidence class.

### the agent's Discretion
- Choose exact dataclass names and helper function layout consistent with the current benchmark module.
- Choose whether the first implementation introduces a new module or keeps the contract in `benchmark.py`, provided downstream phases can import it cleanly.
- Choose concise test fixtures that prove the schema without running expensive training loops.

### Deferred Ideas (OUT OF SCOPE)
- Training improvements for `radioactive_decay`, scaled exponentials, and signed exponentials belong to Phase 30.
- Perturbed true-tree target generation and local repair belong to Phase 31.
- Depth 2 through 6 measured recovery curves belong to Phase 32.
- One-command proof report and evidence lockdown belong to Phase 33.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CLAIM-01 | User can inspect a paper-claim matrix that maps each v1.5 experiment to complete depth-bounded EML search, shallow blind recovery, perturbed-true-tree recovery, and blind depth degradation. [VERIFIED: .planning/REQUIREMENTS.md] | Add a stable `PaperClaim`/claim-matrix registry consumed by built-in proof suites and CLI inspection. [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md] |
| CLAIM-02 | User can generate deterministic proof datasets with seeds, splits, normalization metadata, target formulas, and source provenance. [VERIFIED: .planning/REQUIREMENTS.md] | Extend `DemoSpec`/dataset helpers to emit split metadata around the existing deterministic `make_splits(points, seed)` behavior. [VERIFIED: src/eml_symbolic_regression/datasets.py:28] |
| CLAIM-03 | User can distinguish blind training, compiler warm-start training, perturbed true-tree training, compile-only verification, catalog verification, unsupported cases, and failed cases in every proof artifact. [VERIFIED: .planning/REQUIREMENTS.md] | Add explicit `training_mode` and computed `evidence_class` fields; current code only has `start_mode`, `status`, `claim_status`, and `classification`. [VERIFIED: src/eml_symbolic_regression/benchmark.py:24] [VERIFIED: src/eml_symbolic_regression/benchmark.py:941] |
| CLAIM-04 | User receives explicit pass/fail thresholds for bounded 100% proof suites and measured depth-curve suites. [VERIFIED: .planning/REQUIREMENTS.md] | Add threshold policy metadata to claim/suite/case contracts and aggregate threshold evaluation without changing verifier tolerances. [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md] |
</phase_requirements>

## Summary

Phase 29 should be planned as an additive contract layer on the existing benchmark runner, not as a new experiment system. `BenchmarkCase`, `BenchmarkSuite`, `BenchmarkRun`, run artifacts, aggregate reports, campaign manifests, and CLI benchmark/campaign commands already provide the execution and artifact backbone. [VERIFIED: src/eml_symbolic_regression/benchmark.py:133] [VERIFIED: src/eml_symbolic_regression/benchmark.py:591] [VERIFIED: src/eml_symbolic_regression/campaign.py:112]

The missing piece is explicit proof metadata: stable paper claim IDs, suite/case threshold policies, deterministic dataset manifests, provenance, training modes, and evidence classes. Current code can infer some outcome classes with `classify_run()`, but the artifact does not yet expose the v1.5 fields required by CLAIM-01 through CLAIM-04. [VERIFIED: src/eml_symbolic_regression/benchmark.py:891] [VERIFIED: src/eml_symbolic_regression/benchmark.py:941] [VERIFIED: .planning/REQUIREMENTS.md]

**Primary recommendation:** extend `benchmark.py` and `datasets.py` with small frozen dataclasses and JSON-friendly `as_dict()` helpers, add CLI inspection/generation commands, and update aggregate/campaign tables to carry claim, threshold, dataset, provenance, training mode, and evidence class metadata. [VERIFIED: src/eml_symbolic_regression/benchmark.py:46] [VERIFIED: src/eml_symbolic_regression/datasets.py:17] [VERIFIED: src/eml_symbolic_regression/campaign.py:446]

## Project Constraints

- No `CLAUDE.md` file is present in the repo root. [VERIFIED: `ls CLAUDE.md`]
- No project skill directories were present under `.claude/skills` or `.agents/skills`. [VERIFIED: `find .claude/skills .agents/skills -maxdepth 2 -name SKILL.md -print`]
- Repo instructions require paper fidelity for EML semantics, complete-tree construction, snapping, and complex arithmetic. [VERIFIED: AGENTS.md]
- Repo instructions require that a candidate is not "recovered" from training loss alone and must pass held-out, extrapolation, and high-precision checks. [VERIFIED: AGENTS.md] [VERIFIED: src/eml_symbolic_regression/verify.py:70]
- Repo instructions require scope realism because the paper reports rapid degradation beyond shallow blind depths. [VERIFIED: AGENTS.md] [CITED: sources/paper.pdf, Section 4.3 via pdftotext]
- GSD repo instructions say file-changing work should stay inside the GSD workflow; this research file is part of the requested Phase 29 GSD artifact. [VERIFIED: AGENTS.md] [VERIFIED: `.planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md`]

## Standard Stack

### Core
| Component | Version | Purpose | Why Standard |
|-----------|---------|---------|--------------|
| Python | 3.11.5 | Contract dataclasses, CLI commands, JSON artifacts. [VERIFIED: `python --version`] | Project requires Python `>=3.11,<3.13` and current code is Python package/CLI. [VERIFIED: pyproject.toml] |
| Standard library `dataclasses`, `json`, `pathlib`, `argparse` | Python 3.11.5 bundled | Suite/claim/dataset contracts and CLI additions. [VERIFIED: src/eml_symbolic_regression/benchmark.py:5] [VERIFIED: src/eml_symbolic_regression/cli.py] | Current benchmark/campaign code already uses frozen dataclasses and JSON files. [VERIFIED: src/eml_symbolic_regression/benchmark.py:46] [VERIFIED: src/eml_symbolic_regression/campaign.py:34] |
| NumPy | 1.26.4 | Deterministic split sampling and array metadata. [VERIFIED: local import version] | `DemoSpec.make_splits()` already uses NumPy `default_rng`, `linspace`, and deterministic jitter. [VERIFIED: src/eml_symbolic_regression/datasets.py:28] |
| PyTorch | 2.10.0 | Existing training paths used by proof suites. [VERIFIED: local import version] | Existing benchmark execution routes blind and warm-start runs through PyTorch-backed optimizer paths. [VERIFIED: src/eml_symbolic_regression/benchmark.py:640] [VERIFIED: src/eml_symbolic_regression/benchmark.py:691] |
| SymPy | 1.14.0 | Formula provenance and source expression strings. [VERIFIED: local import version] | Existing demo candidates are SymPy-backed for source formulas such as Beer-Lambert, radioactive decay, Shockley, and Planck. [VERIFIED: src/eml_symbolic_regression/datasets.py:48] |
| mpmath | 1.3.0 | High-precision verifier checks. [VERIFIED: local import version] | `verify_candidate()` evaluates sampled contexts at 80 decimal digits. [VERIFIED: src/eml_symbolic_regression/verify.py:95] |

### Supporting
| Component | Version | Purpose | When to Use |
|-----------|---------|---------|-------------|
| pytest | 7.4.0 | Fast contract and CLI smoke tests. [VERIFIED: `pytest --version`] | Use for Phase 29 schema, validation, dataset metadata, aggregate, and CLI tests. [VERIFIED: pyproject.toml] [VERIFIED: tests/test_benchmark_contract.py] |
| Existing `campaign.py` CSV/report writers | Project code | Carry claim/evidence/threshold fields into later proof reports. [VERIFIED: src/eml_symbolic_regression/campaign.py:173] | Extend only after `aggregate_evidence()` exposes new fields. [VERIFIED: src/eml_symbolic_regression/benchmark.py:828] |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Frozen dataclasses in current modules | Pydantic schemas | Do not add for Phase 29; current repo already validates with dataclasses and `BenchmarkValidationError`, and `AGENTS.md` stack guidance says Pydantic is not an initial dependency. [VERIFIED: AGENTS.md] [VERIFIED: src/eml_symbolic_regression/benchmark.py:29] |
| Additive benchmark extension | Separate proof-reporting framework | Do not use; Phase 29 decision D-09 explicitly says to extend benchmark/proof artifacts and reuse current benchmark/campaign/dataset/verifier patterns. [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md] |
| Storing raw dataset arrays | Manifest metadata plus reproducible generator | Do not store arrays in Phase 29; D-07 says generate on demand and serialize metadata unless a later evidence-lockdown phase requires raw arrays. [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md] |

**Installation:**
```bash
# No new dependencies are required for Phase 29. [VERIFIED: pyproject.toml]
python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py tests/test_benchmark_reports.py tests/test_campaign.py
```

## Architecture Patterns

### Recommended Project Structure
```text
src/eml_symbolic_regression/
|-- benchmark.py     # claim matrix, thresholds, suite/case/run/artifact fields [VERIFIED: current owner]
|-- datasets.py      # formula provenance and deterministic proof dataset manifests [VERIFIED: current owner]
|-- campaign.py      # aggregate/table/report propagation after benchmark exposes fields [VERIFIED: current owner]
`-- cli.py           # list-claims and proof-dataset inspection commands [VERIFIED: current CLI owner]

tests/
|-- test_benchmark_contract.py  # schema and fail-closed validation [VERIFIED: existing]
|-- test_benchmark_runner.py    # artifact field smoke coverage [VERIFIED: existing]
|-- test_benchmark_reports.py   # aggregate evidence counts [VERIFIED: existing]
`-- test_campaign.py            # manifest/table propagation [VERIFIED: existing]
```

### Pattern 1: Additive Contract Fields

**What:** Add `claim_id`, `claim_class`, `training_mode`, `threshold`, and provenance/dataset metadata to `BenchmarkCase`, `BenchmarkRun`, base run payloads, run summaries, and aggregates. [VERIFIED: src/eml_symbolic_regression/benchmark.py:133] [VERIFIED: src/eml_symbolic_regression/benchmark.py:606] [VERIFIED: src/eml_symbolic_regression/benchmark.py:891]

**When to use:** Use this for all built-in v1.5 proof suites and expose defaults for older benchmark suites so existing smoke/standard/showcase paths keep working. [VERIFIED: src/eml_symbolic_regression/benchmark.py:441] [VERIFIED: tests/test_benchmark_runner.py]

**Planning note:** The planner should schedule compatibility tests for old built-in suites plus strict tests for new proof suites, because D-12 requires fail-closed proof validation while old v1.3 benchmark suites still exist. [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md] [VERIFIED: src/eml_symbolic_regression/benchmark.py:496]

### Pattern 2: Evidence Class Is Derived, Not User Supplied

**What:** Compute `evidence_class` from payload status, claim status, training mode, verifier report, repair status, and unsupported/error conditions. [VERIFIED: src/eml_symbolic_regression/benchmark.py:941]

**When to use:** Use derived evidence classes in aggregates and thresholds so a suite JSON cannot falsely label compile-only or catalog verification as training proof. [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md] [VERIFIED: .planning/REQUIREMENTS.md]

**Example evidence classes to define:** `blind_training_recovered`, `compiler_warm_start_recovered`, `perturbed_true_tree_recovered`, `compile_only_verified`, `catalog_verified`, `same_ast_return`, `verified_equivalent_ast`, `repaired_candidate`, `unsupported`, `snapped_but_failed`, `soft_fit_only`, `failed`, and `execution_failure`. [VERIFIED: .planning/REQUIREMENTS.md] [VERIFIED: src/eml_symbolic_regression/benchmark.py:941] [VERIFIED: tests/test_compiler_warm_start.py:132]

### Pattern 3: Dataset Manifest, Not Dataset Dump

**What:** Add a JSON-friendly manifest around `DemoSpec.make_splits()` containing formula ID, variable, split names, domains, sample counts, seed, jitter policy, tolerance, symbolic expression, source document, normalized/dimensionless flag, and optional deterministic hash/signature. [VERIFIED: src/eml_symbolic_regression/datasets.py:17] [VERIFIED: src/eml_symbolic_regression/datasets.py:28]

**When to use:** Use manifests in run artifacts and in a CLI dataset-generation command so users can inspect datasets without running expensive training. [VERIFIED: .planning/REQUIREMENTS.md] [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md]

**Do not include:** raw arrays by default in Phase 29 artifacts, because D-07 defers bulky raw-array persistence to a later evidence-lockdown phase. [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md]

### Pattern 4: Threshold Policy Is Declared Before Runs

**What:** Store threshold policy as structured data on claim/suite/case contracts, not as CLI flags or report prose. [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md]

**Required policy shapes:** `bounded_100_percent` should require every eligible run to land in allowed verifier-owned training evidence classes; `measured_depth_curve` should report rates and counts without treating expected deeper blind failures as regressions. [VERIFIED: .planning/REQUIREMENTS.md] [CITED: sources/paper.pdf, Section 4.3 via pdftotext]

**Planning note:** Keep verifier numeric tolerances in `DatasetConfig` and proof pass/fail thresholds in a separate threshold object, because D-04 is about claim thresholds and `.planning/REQUIREMENTS.md` says not to redefine `recovered` by loosening verifier thresholds. [VERIFIED: src/eml_symbolic_regression/benchmark.py:46] [VERIFIED: .planning/REQUIREMENTS.md]

### Anti-Patterns to Avoid

- **Claiming catalog or compile-only verification as training proof:** The requirements explicitly mark this out of scope. [VERIFIED: .planning/REQUIREMENTS.md]
- **Letting CLI filters redefine proof scope:** D-08 says budgets, seeds, perturbation noise, and thresholds belong to the suite/case contract. [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md]
- **Using status strings as the only taxonomy:** Current `status`, `claim_status`, and `classification` are not enough to represent v1.5 `training_mode` and `evidence_class` requirements. [VERIFIED: src/eml_symbolic_regression/benchmark.py:891] [VERIFIED: .planning/REQUIREMENTS.md]
- **Running expensive recovery campaigns in Phase 29 tests:** Phase context says Phase 29 should favor small deterministic fixtures and metadata assertions. [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md]

## Claim Matrix Seed

| Claim ID | Paper-grounded statement | Claim Class | Suite/Cases to Attach |
|----------|--------------------------|-------------|-----------------------|
| `paper-complete-depth-bounded-search` | EML trees form a complete depth-bounded family for the paper's elementary-function basis. [CITED: sources/paper.pdf, Section 4.3 via pdftotext] | `contract_context` or `supported_representation_claim`; this is not itself a training recovery pass condition. [VERIFIED: .planning/REQUIREMENTS.md] | All proof suites should reference this as representation context. [VERIFIED: .planning/ROADMAP.md] |
| `paper-shallow-blind-recovery` | The paper demonstrates exact recovery at shallow depths and reports blind success is much stronger at shallow depth than deeper depth. [CITED: sources/paper.pdf, Section 4.3 via pdftotext] | `bounded_100_percent_training_proof` for the declared v1.5 shallow suite only. [VERIFIED: .planning/REQUIREMENTS.md] | Phase 30 suite covering `exp`, `log`, `radioactive_decay`, Beer-Lambert-style scaled exponentials, and signed/scaled variants. [VERIFIED: .planning/REQUIREMENTS.md] |
| `paper-perturbed-true-tree-basin` | The paper reports perturbed correct EML weights return to exact values reliably, including depths 5 and 6. [CITED: sources/paper.pdf, Section 4.3 via pdftotext] | `bounded_100_percent_training_proof` for declared perturbation/noise bounds. [VERIFIED: .planning/REQUIREMENTS.md] | Phase 31 perturbed true-tree and Beer-Lambert basin suites. [VERIFIED: .planning/ROADMAP.md] |
| `paper-blind-depth-degradation` | The paper reports blind recovery drops with depth and no depth-6 blind recovery in 448 attempts. [CITED: sources/paper.pdf, Section 4.3 via pdftotext] | `measured_depth_curve`, not a bounded 100% proof. [VERIFIED: .planning/REQUIREMENTS.md] | Phase 32 depth 2 through 6 blind and perturbed suites. [VERIFIED: .planning/ROADMAP.md] |

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Suite expansion and run IDs | A separate proof runner. | `BenchmarkSuite.expanded_runs()` and existing stable `run_id` hashing with added claim/threshold inputs if needed. [VERIFIED: src/eml_symbolic_regression/benchmark.py:360] [VERIFIED: src/eml_symbolic_regression/benchmark.py:226] | Existing tests already assert stable IDs and artifact paths. [VERIFIED: tests/test_benchmark_contract.py] |
| Recovery classification | Ad hoc report string matching. | Central `evidence_class` helper beside `classify_run()`. [VERIFIED: src/eml_symbolic_regression/benchmark.py:941] | Aggregates and campaign tables already consume normalized run summaries. [VERIFIED: src/eml_symbolic_regression/benchmark.py:828] [VERIFIED: src/eml_symbolic_regression/campaign.py:173] |
| Dataset generation | New random samplers per proof case. | `DemoSpec.make_splits()` plus a metadata manifest helper. [VERIFIED: src/eml_symbolic_regression/datasets.py:28] | The existing split generator already emits train, heldout, and extrapolation splits from a fixed seed. [VERIFIED: src/eml_symbolic_regression/datasets.py:37] |
| Verifier pass/fail | New threshold that bypasses verifier reports. | `verify_candidate()` for recovered/failed status, with claim thresholds layered above. [VERIFIED: src/eml_symbolic_regression/verify.py:70] | Requirements forbid redefining `recovered` by loosening verifier thresholds. [VERIFIED: .planning/REQUIREMENTS.md] |
| Campaign outputs | A new proof report generator in Phase 29. | Existing aggregate JSON/Markdown and campaign manifest/table plumbing. [VERIFIED: src/eml_symbolic_regression/campaign.py:112] | One-command proof report is deferred to Phase 33. [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md] |

**Key insight:** Phase 29 should create the proof contract and cheap proof-dataset harness; it should not attempt to make `radioactive_decay`, high-noise Beer-Lambert, or depth-curve recovery pass. [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md]

## Common Pitfalls

### Pitfall 1: Mixing Evidence Classes
**What goes wrong:** Compile-only or catalog verification gets counted as proof-suite training recovery. [VERIFIED: .planning/REQUIREMENTS.md]
**Why it happens:** Current `verifier_recovered` counts any run whose `claim_status` is `recovered`, regardless of whether the run was blind, compile, or warm-start. [VERIFIED: src/eml_symbolic_regression/benchmark.py:968]
**How to avoid:** Add threshold-specific allowed `evidence_class` sets and report counts by evidence class. [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md]
**Warning signs:** Aggregate totals show a 100% rate while compile/catalog rows are included in the denominator or numerator. [VERIFIED: src/eml_symbolic_regression/campaign.py:533]

### Pitfall 2: Treating Depth-Curve Failures as Regressions
**What goes wrong:** Expected deeper blind failures make the phase look broken even though the paper predicts degradation. [CITED: sources/paper.pdf, Section 4.3 via pdftotext]
**Why it happens:** A single "must recover" threshold is applied to both bounded proof suites and measured depth-curve suites. [VERIFIED: .planning/REQUIREMENTS.md]
**How to avoid:** Define separate threshold policies for `bounded_100_percent` and `measured_depth_curve`. [VERIFIED: .planning/REQUIREMENTS.md]
**Warning signs:** Phase 32 depth 5/6 blind rows are marked as product regressions instead of measured evidence. [VERIFIED: .planning/ROADMAP.md]

### Pitfall 3: Non-Reproducible Dataset Provenance
**What goes wrong:** A user cannot reproduce a proof dataset from an artifact because the artifact lacks seed, domains, point counts, or formula provenance. [VERIFIED: .planning/REQUIREMENTS.md]
**Why it happens:** Current run artifacts include `dataset.points` and `dataset.tolerance` but not domains, split sizes, source document, normalized flag, symbolic expression, or jitter policy. [VERIFIED: src/eml_symbolic_regression/benchmark.py:241] [VERIFIED: src/eml_symbolic_regression/datasets.py:28]
**How to avoid:** Add a dataset manifest object generated from `DemoSpec` and `DatasetConfig`. [VERIFIED: src/eml_symbolic_regression/datasets.py:17]
**Warning signs:** Two artifacts with the same formula and seed cannot explain why held-out/extrapolation domains differ. [VERIFIED: src/eml_symbolic_regression/datasets.py:24]

### Pitfall 4: Breaking Existing Benchmark Suites
**What goes wrong:** Adding mandatory proof fields makes `smoke`, `v1.3-standard`, and `v1.3-showcase` invalid. [VERIFIED: src/eml_symbolic_regression/benchmark.py:441]
**Why it happens:** Proof-only required fields are enforced globally. [VERIFIED: src/eml_symbolic_regression/benchmark.py:348]
**How to avoid:** Make fields additive for old benchmark suites and strict for v1.5 proof suites. [VERIFIED: tests/test_benchmark_contract.py]
**Warning signs:** Existing tests for custom v1 suite JSON fail before any proof-suite validation test runs. [VERIFIED: tests/test_benchmark_contract.py]

## Code Examples

### Existing Dataclass Serialization Pattern
```python
@dataclass(frozen=True)
class DatasetConfig:
    points: int = 32
    tolerance: float = 1e-8

    def as_dict(self) -> dict[str, Any]:
        return {"points": self.points, "tolerance": self.tolerance}
```
Source: `src/eml_symbolic_regression/benchmark.py` [VERIFIED: src/eml_symbolic_regression/benchmark.py:46]

### Existing Deterministic Split Pattern
```python
rng = np.random.default_rng(seed)
values = np.linspace(low, high, count)
jitter = (high - low) * 0.002 * rng.standard_normal(count)
return np.sort(values + jitter).astype(np.float64)
```
Source: `src/eml_symbolic_regression/datasets.py` [VERIFIED: src/eml_symbolic_regression/datasets.py:28]

### Existing Outcome Classification Pattern
```python
if start_mode == "blind" and claim_status == "recovered":
    return "blind_recovery"
if status == "same_ast_return":
    return "same_ast_warm_start_return"
if status == "verified_equivalent_ast":
    return "verified_equivalent_warm_start_recovery"
```
Source: `src/eml_symbolic_regression/benchmark.py` [VERIFIED: src/eml_symbolic_regression/benchmark.py:941]

### Recommended Threshold Shape
```python
ThresholdPolicy(
    id="bounded_100_percent",
    required_rate=1.0,
    allowed_evidence_classes=("blind_training_recovered",),
    fail_on_unsupported=True,
    fail_on_execution_error=True,
)
```
Recommendation derived from D-01, D-04, D-10, and CLAIM-04. [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md] [VERIFIED: .planning/REQUIREMENTS.md]

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Broad benchmark recovery rates as evidence | Claim-labeled proof suites with explicit thresholds | v1.5 roadmap created 2026-04-15 [VERIFIED: .planning/ROADMAP.md] | Prevents v1.4 campaign gains from being misread as bounded paper-proof claims. [VERIFIED: .planning/STATE.md] |
| Same-AST warm-start return grouped near recovery | Same-AST, verified-equivalent, repaired, and verifier-owned recovery counted separately | v1.1-v1.4 history and Phase 29 decisions [VERIFIED: .planning/PROJECT.md] [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md] | Protects the distinction between basin evidence and blind discovery. [VERIFIED: src/eml_symbolic_regression/campaign.py:637] |
| Dataset config only includes points/tolerance | Proof dataset manifest includes seed, domains, split sizes, formula provenance, normalization metadata, and source linkage | Phase 29 target [VERIFIED: .planning/REQUIREMENTS.md] | Makes CLAIM-02 reproducible without committing raw arrays. [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md] |
| One recovery threshold | Separate bounded 100% proof and measured depth-curve policies | Phase 29 target [VERIFIED: .planning/REQUIREMENTS.md] | Aligns product claims with the paper's shallow-vs-deep recovery behavior. [CITED: sources/paper.pdf, Section 4.3 via pdftotext] |

**Deprecated/outdated:**
- Treating broad campaign recovery as proof of paper training claims is outdated for v1.5; the roadmap says v1.5 must turn paper-grounded claims into executable training evidence. [VERIFIED: .planning/ROADMAP.md]
- Treating compile-only success as training proof is explicitly out of scope. [VERIFIED: .planning/REQUIREMENTS.md]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| Python | Package, CLI, tests | yes [VERIFIED: `python --version`] | 3.11.5 | None needed |
| pytest | Contract and CLI tests | yes [VERIFIED: `pytest --version`] | 7.4.0 | None needed |
| NumPy | Dataset split generation | yes [VERIFIED: local import version] | 1.26.4 | None needed |
| PyTorch | Existing training modes | yes [VERIFIED: local import version] | 2.10.0 | Avoid new training in Phase 29 tests |
| SymPy | Formula provenance | yes [VERIFIED: local import version] | 1.14.0 | Use existing candidate strings if import unavailable |
| mpmath | Verifier checks | yes [VERIFIED: local import version] | 1.3.0 | None for recovery claims |

**Missing dependencies with no fallback:** None found. [VERIFIED: local environment probes]

**Missing dependencies with fallback:** None found. [VERIFIED: local environment probes]

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | no [VERIFIED: local CLI/package scope] | No authentication surface in Phase 29. [VERIFIED: src/eml_symbolic_regression/cli.py] |
| V3 Session Management | no [VERIFIED: local CLI/package scope] | No sessions in Phase 29. [VERIFIED: src/eml_symbolic_regression/cli.py] |
| V4 Access Control | no [VERIFIED: local CLI/package scope] | Local artifact paths only; campaign overwrite is explicit. [VERIFIED: src/eml_symbolic_regression/campaign.py:120] |
| V5 Input Validation | yes [VERIFIED: benchmark JSON loading] | Use `BenchmarkValidationError`, enumerated modes/classes, positive numeric validation, known claim IDs, and strict threshold policies. [VERIFIED: src/eml_symbolic_regression/benchmark.py:29] [VERIFIED: src/eml_symbolic_regression/benchmark.py:165] |
| V6 Cryptography | no [VERIFIED: local CLI/package scope] | Do not add cryptography for Phase 29. [VERIFIED: .planning/REQUIREMENTS.md] |

### Known Threat Patterns for This Stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Malformed proof-suite JSON silently weakens a threshold | Tampering | Validate known claim IDs, known threshold policy IDs, positive budgets, non-empty seeds, and compatible training modes. [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md] |
| Artifact overwrite hides prior evidence | Tampering | Preserve campaign overwrite guardrails and avoid changing `run_campaign()` overwrite semantics. [VERIFIED: src/eml_symbolic_regression/campaign.py:120] |
| Ambiguous artifact provenance weakens reproducibility | Repudiation | Include code version, claim ID, dataset manifest, budget, threshold, and provenance in run payloads. [VERIFIED: src/eml_symbolic_regression/benchmark.py:606] [VERIFIED: .planning/REQUIREMENTS.md] |

## Testing and Verification Guidance

Validation architecture is omitted because `.planning/config.json` explicitly sets `workflow.nyquist_validation` to `false`. [VERIFIED: .planning/config.json]

Recommended Phase 29 tests:

- Add claim-matrix registry tests: stable IDs, required source refs, claim classes, threshold policies, and no orphaned v1.5 suite/case references. [VERIFIED: .planning/REQUIREMENTS.md]
- Add dataset-manifest tests: same formula/seed/points produces identical metadata/hash; different seed changes deterministic split signature; train/heldout/extrapolation metadata includes domains and counts. [VERIFIED: src/eml_symbolic_regression/datasets.py:28]
- Add proof-suite validation tests: unknown claim ID, missing threshold, invalid training mode, non-warm perturbation, and ambiguous evidence class fail closed. [VERIFIED: src/eml_symbolic_regression/benchmark.py:165] [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md]
- Add artifact smoke tests using filtered cheap cases: one blind, one compile-only, one catalog, one compiler warm-start, and one unsupported path should expose all required proof fields. [VERIFIED: tests/test_benchmark_runner.py]
- Add aggregate tests: evidence classes are counted separately from `verifier_recovered`; bounded policy pass/fail is computed from allowed evidence classes, not raw `claim_status`. [VERIFIED: src/eml_symbolic_regression/benchmark.py:968]
- Add CLI tests for `list-claims` and proof dataset generation without expensive training. [VERIFIED: src/eml_symbolic_regression/cli.py] [VERIFIED: .planning/REQUIREMENTS.md]

## Assumptions Log

All factual claims in this research were verified against local project files, local command output, or the local paper PDF text extracted during this session. No assumption-tagged claims are intentionally present. [VERIFIED: mandatory file reads and local probes]

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| none | No assumed factual claims. [VERIFIED: this research pass] | All sections | None |

## Open Questions

1. **Exact Phase 30 signed/scaled exponential inventory**
   - What we know: Phase 30 must cover `exp`, `log`, `radioactive_decay`, Beer-Lambert-style scaled exponentials, and signed/scaled exponential variants. [VERIFIED: .planning/REQUIREMENTS.md]
   - What's unclear: The exact signed/scaled formula IDs and budgets are not specified in current Phase 29 context. [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md]
   - Recommendation: Phase 29 should define claim and threshold slots for the family, while Phase 30 fills the exact recovery suite inventory. [VERIFIED: .planning/ROADMAP.md]

2. **Perturbed true-tree training mode execution path**
   - What we know: Current execution modes are `catalog`, `compile`, `blind`, and `warm_start`. [VERIFIED: src/eml_symbolic_regression/benchmark.py:24]
   - What's unclear: Phase 31 owns exact EML target-tree generation and perturbed true-tree execution. [VERIFIED: .planning/ROADMAP.md]
   - Recommendation: Phase 29 should define the `perturbed_true_tree_training` contract/evidence class now, but not implement full target-tree generation. [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md]

## Sources

### Primary (HIGH confidence)
- `.planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md` - locked Phase 29 decisions, deferred scope, integration points. [VERIFIED: file read]
- `.planning/REQUIREMENTS.md` - CLAIM-01 through CLAIM-04 and v1.5 out-of-scope boundaries. [VERIFIED: file read]
- `.planning/ROADMAP.md` - Phase 29 goal, success criteria, dependencies, and downstream phase split. [VERIFIED: file read]
- `.planning/STATE.md` - v1.5 milestone state and warning against universal blind recovery claims. [VERIFIED: file read]
- `AGENTS.md` - project constraints and GSD workflow instructions. [VERIFIED: file read]
- `sources/paper.pdf` - EML definition, complete depth-bounded search, PyTorch proof-of-concept, shallow/deep recovery behavior. [CITED: local PDF via `pdftotext`]
- `sources/NORTH_STAR.md` - implementation blueprint and recovery semantics. [VERIFIED: file read]
- `sources/FOR_DEMO.md` - demo formula guidance and normalization cautions. [VERIFIED: file read]
- `src/eml_symbolic_regression/benchmark.py` - suite, case, run, artifact, aggregate, and classification contracts. [VERIFIED: file read]
- `src/eml_symbolic_regression/datasets.py` - deterministic split generation and demo formula definitions. [VERIFIED: file read]
- `src/eml_symbolic_regression/campaign.py` - campaign manifests, tables, figures, and reports. [VERIFIED: file read]
- `src/eml_symbolic_regression/verify.py` - verifier-owned recovery checks. [VERIFIED: file read]

### Secondary (MEDIUM confidence)
- Current tests under `tests/test_benchmark_contract.py`, `tests/test_benchmark_runner.py`, `tests/test_benchmark_reports.py`, `tests/test_campaign.py`, and `tests/test_compiler_warm_start.py` - existing contract, runner, aggregate, campaign, and warm-start expectations. [VERIFIED: file reads]

### Tertiary (LOW confidence)
- None. [VERIFIED: no unverified web-only sources used]

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - no new dependencies are recommended, and local versions were verified with command probes. [VERIFIED: local environment probes]
- Architecture: HIGH - recommendations extend the files that already own suite, dataset, artifact, aggregate, CLI, and campaign behavior. [VERIFIED: src/eml_symbolic_regression/benchmark.py] [VERIFIED: src/eml_symbolic_regression/datasets.py] [VERIFIED: src/eml_symbolic_regression/campaign.py]
- Pitfalls: HIGH - pitfalls come directly from Phase 29 locked decisions, v1.5 requirements, and current aggregate/classification behavior. [VERIFIED: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-CONTEXT.md] [VERIFIED: src/eml_symbolic_regression/benchmark.py:941]

**Research date:** 2026-04-15
**Valid until:** 2026-05-15 for contract/planning guidance, or until benchmark artifacts/schema change. [VERIFIED: local codebase state on 2026-04-15]
