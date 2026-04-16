# Phase 31: Perturbed Basin Training and Local Repair - Research

**Researched:** 2026-04-15
**Domain:** Perturbed exact EML tree training, basin proof suites, verifier-gated local snap repair
**Confidence:** MEDIUM

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

Source: `.planning/phases/31-perturbed-basin-training-and-local-repair/31-CONTEXT.md` [VERIFIED: 31-CONTEXT.md]

### Perturbed Basin Claim Scope

- **D-01:** Treat perturbed true-tree training as same-basin recovery evidence, not discovery evidence. Starting from the exact tree and perturbing its active categorical choices is valid for `paper-perturbed-true-tree-basin`.
- **D-02:** Declare all perturbation bounds before execution in the suite contract: target inventory, EML depth, active-slot noise values, seeds, optimizer budgets, and accepted evidence classes.
- **D-03:** Keep the first proof inventory small and deterministic. Prefer source-document formulas already compiled into exact EML plus a synthetic exact-tree set that covers multiple depths without creating an expensive random-tree campaign.
- **D-04:** Do not let Phase 30 scaffolded blind evidence satisfy Phase 31. Perturbed runs must use `training_mode == "perturbed_true_tree_training"` or an explicitly repaired evidence class.

### Beer-Lambert and Bound Narrowing

- **D-05:** Beer-Lambert high-noise cases are first-class Phase 31 targets because v1.4 showed failures at high perturbation noise from active-slot changes.
- **D-06:** If all declared Beer-Lambert noise levels recover after training and/or repair, record the bound as supported. If high noise still fails, narrow the supported bound to the largest noise envelope with committed evidence and leave the failing level visible as measured unsupported evidence.
- **D-07:** Do not hide a high-noise failure by dropping it silently from reports. Any narrowed bound must cite raw run artifacts, failure classification, and the exact reason the larger bound is not claimed.

### Local Repair Semantics

- **D-08:** Local repair may inspect snapped candidates, nearby slot alternatives, subtree replacements, or exact target-neighborhood moves, but it must serialize what changed and why.
- **D-09:** A repaired candidate must be classified separately as `repaired_candidate`; it must not be reported as same-AST return or raw perturbed true-tree recovery.
- **D-10:** Same-AST return, verified-equivalent AST, repaired AST, snapped-but-failed, soft-fit-only, unsupported, and execution failure must remain separate in artifacts and aggregates.

### Runtime and Verification

- **D-11:** Favor CI-scale deterministic bounds over broad campaigns. Use small seeds/noise grids that prove the claim while keeping tests practical.
- **D-12:** Verification remains verifier-owned: training loss, same-AST checks, or repair success alone cannot mark a candidate recovered without held-out, extrapolation, and high-precision checks.

### Claude's Discretion

- Choose exact synthetic tree inventory and noise grid after researching current compiler/master-tree/warm-start capabilities.
- Choose whether local repair lives in `warm_start.py`, a new `repair.py`, or benchmark orchestration, based on existing module boundaries.
- Choose the smallest deterministic Beer-Lambert bound that is supported by evidence if the current high-noise envelope is still too broad.

### Deferred Ideas (OUT OF SCOPE)

- Pure blind scaled-exponential recovery remains a Phase 30 blocker and should not be solved inside Phase 31.
- Depth 2 through 6 blind-vs-perturbed recovery curves belong to Phase 32; Phase 31 should produce the perturbed-basin primitives and bounded proof suite needed by that phase.
- Final proof campaign report and committed evidence lockdown belong to Phase 33.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| BASN-01 | User can generate exact EML target trees at declared depths and perturb their active categorical slots under deterministic noise envelopes. [VERIFIED: .planning/REQUIREMENTS.md:27] | Build a small target inventory/generator around existing `Expr`, `SoftEMLTree.embed_expr()`, and `perturb_tree_logits()` instead of inventing a second tree representation. [VERIFIED: expression.py] [VERIFIED: master_tree.py:431-450] [VERIFIED: warm_start.py:66-100] |
| BASN-02 | User receives 100% verifier-owned recovery for the declared perturbed-true-tree basin proof suite with per-depth and per-noise thresholds documented before execution. [VERIFIED: .planning/REQUIREMENTS.md:28] | Add a first-class `perturbed_true_tree_training` runner path and suite; the proof contract already has the claim and bounded threshold vocabulary, but no executable suite exists yet. [VERIFIED: proof.py:17-38] [VERIFIED: proof.py:257-272] [VERIFIED: benchmark.py:33-38] |
| BASN-03 | User can run Beer-Lambert perturbation repair experiments that either recover all declared high-noise cases or formally narrow the supported perturbation bound with evidence. [VERIFIED: .planning/REQUIREMENTS.md:29] | Existing v1.4 evidence shows Beer-Lambert succeeds through noise `5.0`, partially fails at `15.0`, and fails at `35.0`; Phase 31 should rerun, repair, and publish the narrowed bound if high noise remains unsupported. [VERIFIED: artifacts/campaigns/v1.4-showcase/aggregate.json] [VERIFIED: /tmp/eml-phase31-beer-probe/v1.2-evidence/aggregate.json] |
| BASN-04 | User can apply local snap/discrete repair around failed trained candidates and inspect which slots or subtrees changed. [VERIFIED: .planning/REQUIREMENTS.md:30] | Add a verifier-gated `repair.py` module that reconstructs snapped slot assignments, tries bounded target-neighborhood or local alternatives, and serializes every move. [VERIFIED: master_tree.py:271-277] [VERIFIED: benchmark.py:1257-1270] [ASSUMED] |
| BASN-05 | User can verify that same-AST return, verified-equivalent AST, repaired AST, snapped-but-failed, soft-fit-only, and unsupported outcomes remain distinct. [VERIFIED: .planning/REQUIREMENTS.md:31] | Preserve existing evidence classes and add tests that mix same-AST, perturbed recovered, repaired, snapped failed, soft-fit-only, unsupported, and execution failure rows in one aggregate. [VERIFIED: proof.py:25-39] [VERIFIED: tests/test_benchmark_reports.py:67-185] |
</phase_requirements>

## Summary

Phase 31 should not reuse the current compiler warm-start mode as the proof runner. `TRAINING_MODES` already includes `perturbed_true_tree_training`, and `EVIDENCE_CLASSES` already includes `perturbed_true_tree_recovered` and `repaired_candidate`, but `START_MODES` only exposes `catalog`, `compile`, `blind`, and `warm_start`. [VERIFIED: proof.py:17-38] [VERIFIED: benchmark.py:33] The current training-mode validator requires `warm_start` cases to use `compiler_warm_start_training`, so a proof case with `start_mode="warm_start"` and `training_mode="perturbed_true_tree_training"` fails closed. [VERIFIED: benchmark.py:552-582] This means Phase 31 needs a real perturbed-tree execution path, not just new suite metadata. [VERIFIED: benchmark.py:871-977]

The existing perturbation core is strong enough to reuse. `fit_warm_started_eml_tree()` compiles or receives an exact EML expression, embeds it into a `SoftEMLTree`, applies deterministic Gaussian perturbation to logits, trains, snaps, verifies, and records same-AST/equivalent/failure diagnosis. [VERIFIED: warm_start.py:107-174] `PerturbationReport` already records active slot changes plus pre/post snap payloads. [VERIFIED: warm_start.py:29-43] `SoftEMLTree.embed_expr()` already checks depth, variables, constants, and round-trip snap equality. [VERIFIED: master_tree.py:431-450]

Beer-Lambert high noise is still the key risk. The committed v1.4 showcase campaign has 15 Beer-Lambert warm-start perturbation runs: noise `2.5` and `5.0` recover for all seeds, noise `15.0` fails for seed `1`, and noise `35.0` fails for all seeds. [VERIFIED: artifacts/campaigns/v1.4-showcase/aggregate.json] A current-code smoke rerun of `v1.2-evidence` for seed `0` recovered noise `0.0` and `5.0`, but noise `35.0` failed as `snapped_but_failed` with `changed_slot_count=5` and mechanism `active_slot_perturbation`. [VERIFIED: /tmp/eml-phase31-beer-probe/v1.2-evidence/aggregate.json] [VERIFIED: /tmp/eml-phase31-beer-probe/v1.2-evidence/v1-2-evidence-beer-perturbation-sweep-89ce454cb407.json]

**Primary recommendation:** implement Phase 31 in three plans: first-class perturbed-tree suite/runner and deterministic target inventory; verifier-gated local snap repair with full move provenance; Beer-Lambert bound-evidence report that either raises the supported high-noise bound after repair or explicitly narrows it to the largest recovered noise. [VERIFIED: 31-CONTEXT.md] [ASSUMED]

## Project Constraints (from AGENTS.md and Planning Docs)

- `CLAUDE.md` does not exist in the repository, so there are no CLAUDE-specific directives to copy. [VERIFIED: `test -f CLAUDE.md` returned exit code 1]
- `.claude/skills/` and `.agents/skills/` do not exist in the repository, so no project-local skill rules apply. [VERIFIED: `test -d .claude/skills`; `test -d .agents/skills` returned exit code 1]
- EML semantics, complete-tree construction, snapping, and complex arithmetic must stay grounded in the paper and `sources/NORTH_STAR.md`. [VERIFIED: AGENTS.md] [CITED: sources/NORTH_STAR.md]
- Training defaults to PyTorch `complex128`, with clamps only in training mode and faithful verification afterwards. [VERIFIED: AGENTS.md] [VERIFIED: master_tree.py:174-222] [VERIFIED: verify.py:70-125]
- A candidate is recovered only after held-out, extrapolation, and high-precision checks pass. [VERIFIED: AGENTS.md] [VERIFIED: verify.py:70-125]
- v1.5 must avoid universal deep blind recovery claims; `sources/NORTH_STAR.md` records strong perturbed-correct basin behavior but sharp blind degradation with depth. [VERIFIED: AGENTS.md] [CITED: sources/NORTH_STAR.md:45] [CITED: sources/NORTH_STAR.md:138]
- Demos and proof targets should stay normalized and dimensionless where possible. [VERIFIED: AGENTS.md] [CITED: sources/FOR_DEMO.md]
- `.planning/config.json` sets `workflow.nyquist_validation` to `false`, so this research omits the Validation Architecture section. [VERIFIED: .planning/config.json]
- `.planning/config.json` has no `security_enforcement: false` key, so the Security Domain section is included under the GSD default. [VERIFIED: .planning/config.json]

## Standard Stack

### Core

| Library / Module | Version / Contract | Purpose | Why Standard |
|------------------|--------------------|---------|--------------|
| Python | Local `3.11.5`; project requires `>=3.11,<3.13`. [VERIFIED: local version probe] [VERIFIED: pyproject.toml] | Package runtime, CLI, benchmark orchestration, tests. [VERIFIED: pyproject.toml] | Existing project runtime; no new language is needed. [VERIFIED: pyproject.toml] |
| PyTorch | Local `2.10.0`; project dependency `torch>=2.10`. [VERIFIED: local import version probe] [VERIFIED: pyproject.toml] | Soft EML logits, complex128 evaluation, Adam optimization. [VERIFIED: optimize.py:16-130] | Existing training path and paper-aligned implementation stack. [VERIFIED: AGENTS.md] [CITED: sources/NORTH_STAR.md:138] |
| NumPy | Local `1.26.4`; project dependency `numpy>=1.26`. [VERIFIED: local import version probe] [VERIFIED: pyproject.toml] | Dataset splits, target arrays, post-snap loss, verifier residuals. [VERIFIED: datasets.py] [VERIFIED: verify.py:84-93] | Existing deterministic split and verification path. [VERIFIED: datasets.py:28-50] |
| SymPy | Local `1.14.0`; project dependency `sympy>=1.14`. [VERIFIED: local import version probe] [VERIFIED: pyproject.toml] | Source formula provenance and compiler validation for source-document targets. [VERIFIED: datasets.py:54-193] [VERIFIED: compiler.py:270-316] | Existing compiler/catalog layer already uses SymPy expressions. [VERIFIED: datasets.py] |
| mpmath | Local `1.3.0`; project dependency `mpmath>=1.3`. [VERIFIED: local import version probe] [VERIFIED: pyproject.toml] | High-precision verification points. [VERIFIED: verify.py:95-113] | The verifier already uses 80-digit mpmath checks before `recovered`. [VERIFIED: verify.py:95-113] |
| pytest | Local `7.4.0`; dev dependency `pytest>=7.4`. [VERIFIED: local import version probe] [VERIFIED: pyproject.toml] | Regression tests for suite contracts, repair, runner artifacts, and aggregate thresholds. [VERIFIED: tests/test_benchmark_contract.py] [VERIFIED: tests/test_benchmark_runner.py] | Existing project test stack; no new test framework needed. [VERIFIED: pyproject.toml] |

### Supporting

| Module | Current Capability | Phase 31 Use |
|--------|--------------------|--------------|
| `warm_start.py` | `PerturbationConfig`, `perturb_tree_logits()`, `fit_warm_started_eml_tree()`, `WarmStartResult`, active-slot diagnosis. [VERIFIED: warm_start.py:23-215] | Reuse low-level embedding, perturbation, train, snap, and diagnosis logic; add a perturbed-true-tree wrapper that does not classify as compiler warm start. [ASSUMED] |
| `master_tree.py` | Slot catalogs, `set_slot()`, `snap()`, `embed_expr_into_tree()`, exact scaled-exp forcing. [VERIFIED: master_tree.py:163-277] [VERIFIED: master_tree.py:343-450] | Generate exact target trees, replay snapped slot choices, and construct bounded repair candidates. [ASSUMED] |
| `benchmark.py` | Suite contracts, run artifacts, metrics, evidence classes, threshold aggregation. [VERIFIED: benchmark.py:170-306] [VERIFIED: benchmark.py:812-1397] | Add a new runner mode or equivalent path for `perturbed_true_tree_training`, a `proof-perturbed-basin` suite, and repair payload propagation. [ASSUMED] |
| `proof.py` | Claim `paper-perturbed-true-tree-basin`, `bounded_100_percent`, evidence class vocabulary. [VERIFIED: proof.py:149-164] [VERIFIED: proof.py:257-272] | Update claim case inventory and tests once Phase 31 declares concrete target IDs. [ASSUMED] |
| `diagnostics.py` | Selects Beer-Lambert perturbation failures and compares campaign categories. [VERIFIED: diagnostics.py:23-146] [VERIFIED: diagnostics.py:489-493] | Add or reuse focused bound-narrowing evidence helpers for high-noise Beer-Lambert runs. [ASSUMED] |
| `campaign.py` | CSV/report/plot propagation for evidence classes, thresholds, perturbation noise, active slot counts. [VERIFIED: campaign.py:174-264] [VERIFIED: campaign.py:472-558] | Add a proof-basin campaign preset only after the benchmark suite is stable. [ASSUMED] |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| First-class perturbed start mode | Reuse `start_mode="warm_start"` with `training_mode="perturbed_true_tree_training"` | Current validation rejects training modes that do not match start mode defaults, so this would fail closed until validation changes. [VERIFIED: benchmark.py:552-582] |
| New `repair.py` module | Put repair inside `warm_start.py` | `warm_start.py` is currently compile/embedding/perturbation oriented, while repair needs independent provenance, candidate enumeration, and benchmark payload integration. [VERIFIED: warm_start.py:1-215] [ASSUMED] |
| Broad random tree campaign | Small deterministic target inventory | Phase 31 explicitly favors CI-scale deterministic bounds and defers depth-curve breadth to Phase 32. [VERIFIED: 31-CONTEXT.md:41-49] [VERIFIED: 31-CONTEXT.md:112-114] |
| Claim high-noise Beer-Lambert immediately | Rerun, repair, then narrow if needed | Existing evidence shows noise `35.0` fails under current behavior, so claiming that bound now would be unsupported. [VERIFIED: artifacts/campaigns/v1.4-showcase/aggregate.json] [VERIFIED: /tmp/eml-phase31-beer-probe/v1.2-evidence/aggregate.json] |

**Installation:**

No new dependencies are recommended for Phase 31. [VERIFIED: pyproject.toml] Existing environment versions were verified locally: Python `3.11.5`, PyTorch `2.10.0`, NumPy `1.26.4`, SymPy `1.14.0`, mpmath `1.3.0`, and pytest `7.4.0`. [VERIFIED: local version probes]

## Architecture Patterns

### Recommended Project Structure

```text
src/eml_symbolic_regression/
├── basin.py          # New: exact target-tree inventory/generation and perturbed true-tree run wrapper. [ASSUMED]
├── repair.py         # New: verifier-gated local snap/discrete repair reports. [ASSUMED]
├── warm_start.py     # Reuse: low-level logit perturbation and embedding diagnostics. [VERIFIED: warm_start.py]
├── master_tree.py    # Reuse/extend: slot replay helpers for snap candidates and repair. [VERIFIED: master_tree.py]
├── benchmark.py      # Extend: start mode, built-in suite, artifact payloads, evidence mapping. [VERIFIED: benchmark.py]
├── proof.py          # Extend: concrete Phase 31 case inventory tests. [VERIFIED: proof.py]
├── diagnostics.py    # Extend: Beer-Lambert bound narrowing report helpers. [VERIFIED: diagnostics.py]
└── campaign.py       # Extend after runner stability: proof-basin campaign preset. [VERIFIED: campaign.py]

tests/
├── test_basin_targets.py             # New: target generation, deterministic manifests, exact depths. [ASSUMED]
├── test_basin_training.py            # New: perturbed runner artifact/evidence-class behavior. [ASSUMED]
├── test_repair.py                    # New: repair move serialization and verifier gating. [ASSUMED]
├── test_benchmark_contract.py        # Extend: suite ID, case IDs, start-mode validation. [VERIFIED: tests/test_benchmark_contract.py]
├── test_benchmark_runner.py          # Extend: perturbed/repaired artifact fields. [VERIFIED: tests/test_benchmark_runner.py]
├── test_benchmark_reports.py         # Extend: threshold/evidence-class separation. [VERIFIED: tests/test_benchmark_reports.py]
└── test_diagnostics.py               # Extend: high-noise Beer bound selection/reporting. [VERIFIED: tests/test_diagnostics.py]
```

### Pattern 1: Add a Real Perturbed-True-Tree Runner

**What:** Add a first-class executable mode, recommended name `perturbed_tree`, whose default training mode is `TRAINING_MODES["perturbed_true_tree_training"]`. [ASSUMED] Existing `START_MODES` does not include this mode. [VERIFIED: benchmark.py:33] Existing `_default_training_mode()` maps `warm_start` to `compiler_warm_start_training`, not `perturbed_true_tree_training`. [VERIFIED: benchmark.py:552-558]

**When to use:** Use this mode for all proof cases that count toward `paper-perturbed-true-tree-basin`; do not use it for compile-only diagnostics or Phase 30 scaffolded blind evidence. [VERIFIED: 31-CONTEXT.md:23-26] [VERIFIED: 31-CONTEXT.md:56-59]

**Implementation shape:** Reuse the internals of `fit_warm_started_eml_tree()` but expose a basin-specific result status and artifact namespace such as `perturbed_true_tree`. [VERIFIED: warm_start.py:107-174] The payload should keep `return_kind` or `basin_status` distinct from `evidence_class` so BASN-05 can report same-AST, verified-equivalent, repaired, snapped-failed, soft-fit-only, unsupported, and execution failure separately. [VERIFIED: .planning/REQUIREMENTS.md:31] [ASSUMED]

### Pattern 2: Deterministic Exact-Tree Inventory Before Broad Campaigns

**What:** Put the target inventory in code as deterministic specs with `target_id`, `depth`, `seed`, `expression`, variable names, constants, domains, and provenance. [ASSUMED] Current demo formula specs already carry variable, source document, domains, candidate, and provenance metadata. [VERIFIED: datasets.py:18-61]

**Recommended first inventory:** Use a small synthetic exact EML set at depths 1, 2, and 3 plus Beer-Lambert as the source-document high-noise case. [ASSUMED] This matches the Phase 31 context preference for a small deterministic inventory rather than a random-tree campaign. [VERIFIED: 31-CONTEXT.md:25]

**Depth safety:** Keep synthetic target domains narrow enough that composed `exp`/`log` values stay finite under both training and verification. [CITED: sources/NORTH_STAR.md:430-490] This is especially important because existing verification mode does not hide non-finite candidate behavior. [VERIFIED: verify.py:84-113]

### Pattern 3: Repair as Verifier-Gated Candidate Enumeration

**What:** Add `repair.py` with immutable dataclasses such as `RepairConfig`, `RepairMove`, and `RepairReport`. [ASSUMED] Each repair should include original status, candidate AST, moves attempted, accepted move, repaired AST, verifier report, and reason. [ASSUMED]

**Minimum repair strategies:** Try a bounded one-slot target-neighborhood revert for slots where snapped choices diverge from the embedded target, then optionally try one-slot alternatives from `slot_catalog()` for low-margin or changed active slots. [ASSUMED] Existing artifacts already expose active slot changes, and `SoftEMLTree.set_slot()` can replay slot choices into a tree. [VERIFIED: warm_start.py:66-100] [VERIFIED: master_tree.py:271-277]

**Claim hygiene:** Set `status="repaired_candidate"` or `repair_status="repaired"` only after `verify_candidate()` passes. [VERIFIED: benchmark.py:1257-1270] Do not mutate raw training status from `snapped_but_failed` into `perturbed_true_tree_recovered`; emit a separate repaired result so BASN-05 stays inspectable. [VERIFIED: 31-CONTEXT.md:36-38]

### Pattern 4: Bound Narrowing Is an Artifact, Not a Comment

**What:** Add a small Beer-Lambert bound report that groups raw and repaired outcomes by noise, seed, active slot changes, and verifier status. [ASSUMED] Existing campaign reports already group by perturbation noise and expose active/changed slot counts in CSV columns. [VERIFIED: campaign.py:189-205] [VERIFIED: campaign.py:472-558]

**When to use:** Run this report for the declared Beer-Lambert grid after repair. If high noise still fails, write a machine-readable supported bound such as `raw_supported_noise_max` and `repaired_supported_noise_max`, with failing artifacts linked. [ASSUMED] This follows Phase 31 D-06 and D-07. [VERIFIED: 31-CONTEXT.md:30-32]

### Pattern 5: Thresholds Must Count Evidence Classes, Not Verifier Status Alone

**What:** Keep `_threshold_summary()` as the authority for bounded pass/fail decisions. [VERIFIED: benchmark.py:1328-1388] The `bounded_100_percent` policy allows `perturbed_true_tree_recovered`, `repaired_candidate`, and `verified_equivalent`, but not `same_ast`. [VERIFIED: proof.py:149-164] [VERIFIED: tests/test_proof_contract.py:51-70]

**Planner action:** Add tests that prove same-AST rows remain visible and do not silently become counted proof evidence unless Phase 31 explicitly introduces a separate, verifier-owned `perturbed_true_tree_recovered` row with distinct `return_kind`. [VERIFIED: tests/test_benchmark_reports.py:67-185] [ASSUMED]

## Recommended Plan Structure

### Plan 31-01: Perturbed True-Tree Suite and Runner Contract

- Add concrete `proof-perturbed-basin` built-in suite cases and update `BUILTIN_SUITES`. [VERIFIED: benchmark.py:33-38] [ASSUMED]
- Add a first-class runner mode for `perturbed_true_tree_training` rather than reusing compiler warm start. [VERIFIED: benchmark.py:552-582] [ASSUMED]
- Add exact target-tree inventory/generation in a small module such as `basin.py`, using existing `Expr` objects and `SoftEMLTree.embed_expr()`. [VERIFIED: expression.py] [VERIFIED: master_tree.py:431-450] [ASSUMED]
- Update `proof.py` tests so `paper-perturbed-true-tree-basin` declares the concrete Phase 31 case IDs, or intentionally clears `case_ids` if the suite uses generated case IDs. [VERIFIED: proof.py:257-272] [VERIFIED: benchmark.py:461-485] [ASSUMED]
- Add runner tests for deterministic perturbation, correct `training_mode`, dataset manifest propagation, and evidence-class derivation. [VERIFIED: tests/test_benchmark_runner.py] [ASSUMED]

### Plan 31-02: Local Snap/Discrete Repair

- Add `repair.py` with verifier-gated repair dataclasses and bounded move enumeration. [ASSUMED]
- Reconstruct a tree from snap decisions, try target-neighborhood slot reverts and local one-slot alternatives, and verify repaired candidates before marking `repaired_candidate`. [VERIFIED: master_tree.py:247-277] [VERIFIED: verify.py:70-125] [ASSUMED]
- Integrate repair payloads into benchmark artifacts under a separate key such as `local_repair`, preserving raw `perturbed_true_tree` status. [VERIFIED: benchmark.py:812-827] [ASSUMED]
- Extend `evidence_class_for_payload()` only as needed; it already maps `status == "repaired_candidate"` or `repair_status == "repaired"` to `repaired_candidate`. [VERIFIED: benchmark.py:1257-1270]
- Add tests that repaired candidates show changed slots/subtrees, verifier report, original failed status, and aggregate threshold counting. [VERIFIED: tests/test_benchmark_reports.py:132-185] [ASSUMED]

### Plan 31-03: Beer-Lambert Bound Evidence and Guardrails

- Rerun Beer-Lambert noise grid under current Phase 31 runner with raw outcomes and repair outcomes. [ASSUMED]
- Start with a raw bounded claim no higher than noise `5.0` unless Phase 31 repair/training evidence proves `15.0` or `35.0`. [VERIFIED: artifacts/campaigns/v1.4-showcase/aggregate.json] [VERIFIED: /tmp/eml-phase31-beer-probe/v1.2-evidence/aggregate.json] [ASSUMED]
- Keep high-noise `15.0` and `35.0` visible as bound-probe or repair-experiment rows even if they are outside the supported bounded threshold. [VERIFIED: 31-CONTEXT.md:30-32] [ASSUMED]
- Add diagnostics/report tests for supported bound JSON/Markdown, failed high-noise artifact links, `active_slot_perturbation` counts, and repaired vs raw evidence-class separation. [VERIFIED: diagnostics.py:123-146] [VERIFIED: campaign.py:849-862] [ASSUMED]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| EML AST model | A second AST/tree schema | `Expr`, `Const`, `Var`, `Eml`, and `Expr.to_document()`. [VERIFIED: expression.py:31-156] | Existing AST already evaluates in NumPy, Torch, mpmath, and serializes metadata. [VERIFIED: expression.py] |
| Soft-tree embedding | Manual path-by-path hardcoding for every target | `SoftEMLTree.embed_expr()` and `embed_expr_into_tree()`. [VERIFIED: master_tree.py:377-450] | Existing embedding validates depth, variables, constants, and round-trip equality. [VERIFIED: master_tree.py:431-450] |
| Logit perturbation | Custom random noise code | `PerturbationConfig` and `perturb_tree_logits()`. [VERIFIED: warm_start.py:23-100] | Existing helper is deterministic by seed and records active slot changes. [VERIFIED: tests/test_compiler_warm_start.py:159-176] |
| Recovery decision | A custom `recovered=True` flag | `verify_candidate()` plus derived `evidence_class`. [VERIFIED: verify.py:70-125] [VERIFIED: benchmark.py:1257-1294] | Verifier-owned recovery requires split checks and high precision. [VERIFIED: verify.py:84-113] |
| Bounded threshold math | A new report-only pass/fail calculation | `aggregate_evidence()` and `_threshold_summary()`. [VERIFIED: benchmark.py:1086-1108] [VERIFIED: benchmark.py:1328-1388] | Existing threshold logic counts policy-allowed evidence classes. [VERIFIED: proof.py:149-164] |
| Local repair proof | Silent AST replacement with the true tree | `RepairReport` plus `repaired_candidate` evidence class. [VERIFIED: benchmark.py:1257-1270] [ASSUMED] | Requirement BASN-05 needs raw, repaired, failed, and unsupported outcomes distinct. [VERIFIED: .planning/REQUIREMENTS.md:31] |
| High-noise claim narrative | Manual prose without raw links | Existing benchmark/campaign artifacts and diagnostics filters. [VERIFIED: benchmark.py:1076-1136] [VERIFIED: diagnostics.py:123-146] | Phase 31 D-07 requires raw artifacts and exact failure classification. [VERIFIED: 31-CONTEXT.md:30-32] |

**Key insight:** Phase 31 is about proving same-basin behavior under declared perturbation bounds, so target knowledge is allowed at initialization and repair time only when the artifact says so explicitly. [VERIFIED: 31-CONTEXT.md:10-12] [ASSUMED]

## Common Pitfalls

### Pitfall 1: Metadata-Only Perturbed Mode

**What goes wrong:** A suite sets `training_mode="perturbed_true_tree_training"` on a `warm_start` case and expects it to run. [ASSUMED]

**Why it happens:** The current validator requires each start mode to match its default training mode, and `warm_start` maps to `compiler_warm_start_training`. [VERIFIED: benchmark.py:552-582]

**How to avoid:** Add a first-class start mode or explicitly change the validation/routing contract with tests. [ASSUMED]

**Warning signs:** `BenchmarkValidationError(reason="invalid_proof_contract")` before execution, or artifacts classified as `compiler_warm_start_recovered` instead of `perturbed_true_tree_recovered`. [VERIFIED: benchmark.py:569-582] [VERIFIED: benchmark.py:1285-1294]

### Pitfall 2: Same-AST Claim Leakage

**What goes wrong:** A same-AST return is counted as bounded proof without preserving that it simply snapped back to the target AST. [ASSUMED]

**Why it happens:** Existing warm-start runs can have `status="same_ast_return"` and `claim_status="recovered"`, while bounded policies do not allow `same_ast` evidence. [VERIFIED: /tmp/eml-phase31-beer-probe/v1.2-evidence/aggregate.json] [VERIFIED: proof.py:149-164]

**How to avoid:** Store raw `return_kind` separately from `evidence_class`, and test threshold rows against mixed evidence classes. [VERIFIED: tests/test_benchmark_reports.py:67-185] [ASSUMED]

**Warning signs:** Aggregate `passed` equals `eligible` even when evidence-class counts include `same_ast`. [VERIFIED: tests/test_proof_contract.py:51-70]

### Pitfall 3: Overclaiming Beer-Lambert High Noise

**What goes wrong:** The suite declares noise `15.0` or `35.0` inside the 100% bound before repair evidence supports it. [ASSUMED]

**Why it happens:** v1.3/v1.4 warm-start campaigns include high-noise rows, but those rows were diagnostic and not Phase 31 proof-bound rows. [VERIFIED: artifacts/campaigns/v1.4-showcase/aggregate.json] [VERIFIED: 31-CONTEXT.md:102-105]

**How to avoid:** Use the largest proven noise as the bounded threshold and keep larger noises as visible bound probes or unsupported measured evidence. [VERIFIED: 31-CONTEXT.md:30-32] [ASSUMED]

**Warning signs:** Noise `35.0` rows have `snapped_but_failed`, nonzero changed active slots, and mechanism `active_slot_perturbation`. [VERIFIED: /tmp/eml-phase31-beer-probe/v1.2-evidence/aggregate.json]

### Pitfall 4: Repair That Hides Provenance

**What goes wrong:** Repair replaces a failed snap with the target tree and reports it as raw perturbed recovery. [ASSUMED]

**Why it happens:** Exact target-neighborhood repair has access to embedded target choices, so it can trivially undo active-slot changes if no provenance guard exists. [VERIFIED: warm_start.py:66-100] [ASSUMED]

**How to avoid:** Serialize every move and classify accepted repaired candidates as `repaired_candidate`, never `same_ast_return` or raw `perturbed_true_tree_recovered`. [VERIFIED: 31-CONTEXT.md:36-38] [VERIFIED: benchmark.py:1257-1270]

**Warning signs:** Repaired artifacts lack `moves_attempted`, `accepted_move`, `original_status`, or verifier report. [ASSUMED]

### Pitfall 5: Synthetic Trees With Bad Numerics

**What goes wrong:** A generated exact tree is mathematically valid but overflows or crosses branch-sensitive regions during training/verification. [ASSUMED]

**Why it happens:** EML contains `exp` and `log`, and `sources/NORTH_STAR.md` warns that composed exponentials overflow and require training-only clamps. [CITED: sources/NORTH_STAR.md:430-490]

**How to avoid:** Keep initial synthetic depths and domains small, generate deterministic dataset manifests, and fail target generation if verification is non-finite. [VERIFIED: datasets.py:201-240] [VERIFIED: verify.py:84-113] [ASSUMED]

**Warning signs:** `post_snap_loss` is non-finite, verifier reason is `mpmath_failed`, or `semantics.py` emits overflow warnings during otherwise simple proof runs. [VERIFIED: warm_start.py:212-220] [VERIFIED: current Beer probe command output]

### Pitfall 6: Phase 30 Evidence Contamination

**What goes wrong:** Scaffolded shallow blind recovery is reused to satisfy perturbed-basin proof. [ASSUMED]

**Why it happens:** Phase 30 added `scaffolded_blind_training_recovered` to avoid counting exact scaffold starts as pure blind recovery. [VERIFIED: 30-REVIEW.md]

**How to avoid:** Require `training_mode == "perturbed_true_tree_training"` or `evidence_class == "repaired_candidate"` for Phase 31 bounded rows. [VERIFIED: 31-CONTEXT.md:23-26] [VERIFIED: proof.py:149-164]

**Warning signs:** Phase 31 aggregates include `scaffolded_blind_training_recovered`, `compile_only_verified`, or `catalog_verified` in bounded pass counts. [VERIFIED: proof.py:149-164] [VERIFIED: tests/test_benchmark_reports.py:132-185]

## Code Examples

Verified patterns from current sources and proposed Phase 31 adaptations:

### Existing Deterministic Perturbation Helper

```python
from eml_symbolic_regression.master_tree import EmbeddingConfig, SoftEMLTree
from eml_symbolic_regression.warm_start import PerturbationConfig, perturb_tree_logits

tree = SoftEMLTree(compiled.metadata.depth, (spec.variable,), compiled.metadata.constants)
embedding = tree.embed_expr(compiled.expression, EmbeddingConfig(strength=30.0))
report = perturb_tree_logits(tree, PerturbationConfig(seed=123, noise_scale=0.01), embedding)
```

This mirrors the existing seeded perturbation test and preserves active-slot change records. [VERIFIED: tests/test_compiler_warm_start.py:159-176]

### Existing Warm-Start Training Shape to Reuse Internally

```python
warm = fit_warm_started_eml_tree(
    train.inputs,
    train.target,
    config,
    compiled.expression,
    perturbation_config=PerturbationConfig(seed=run.seed, noise_scale=run.perturbation_noise),
    verification_splits=splits,
    tolerance=run.dataset.tolerance,
    compiler_metadata=compiled.metadata.as_dict(),
)
```

This is the current benchmark warm-start execution path; Phase 31 should reuse its mechanics but not its compiler-warm-start classification. [VERIFIED: benchmark.py:955-973]

### Proposed Start-Mode Mapping

```python
START_MODES = ("catalog", "compile", "blind", "warm_start", "perturbed_tree")

def _default_training_mode(start_mode: str) -> str:
    modes = {
        "catalog": TRAINING_MODES["catalog_verification"],
        "compile": TRAINING_MODES["compile_only_verification"],
        "blind": TRAINING_MODES["blind_training"],
        "warm_start": TRAINING_MODES["compiler_warm_start_training"],
        "perturbed_tree": TRAINING_MODES["perturbed_true_tree_training"],
    }
    return modes[start_mode]
```

This is a recommended Phase 31 change because the current mapping has no executable perturbed-tree mode. [VERIFIED: benchmark.py:552-558] [ASSUMED]

### Proposed Repair Report Shape

```python
@dataclass(frozen=True)
class RepairMove:
    slot: str
    before: str
    after: str
    source: str
    verified: bool

@dataclass(frozen=True)
class RepairReport:
    status: str
    original_status: str
    moves_attempted: tuple[RepairMove, ...]
    accepted_move: RepairMove | None
    verification: VerificationReport | None
```

This shape is not implemented yet; it is recommended so repair remains serializable and distinct from raw recovery. [ASSUMED] The benchmark evidence mapper already reserves `repaired_candidate`. [VERIFIED: benchmark.py:1257-1270]

## State of the Art

| Old Approach | Current / Phase 31 Approach | When Changed | Impact |
|--------------|-----------------------------|--------------|--------|
| Treat compiler warm start and perturbed true-tree as one warm-start bucket. [VERIFIED: benchmark.py:914-977] | Add a first-class `perturbed_true_tree_training` runner/evidence path. [VERIFIED: proof.py:17-38] [ASSUMED] | Phase 31. [VERIFIED: .planning/ROADMAP.md:81-90] | Prevents compiler-assisted results from satisfying the basin proof by accident. [VERIFIED: 31-CONTEXT.md:23-26] |
| Count verifier recovery rate without evidence-class policy. [ASSUMED] | Count bounded thresholds through allowed evidence classes in `_threshold_summary()`. [VERIFIED: benchmark.py:1328-1388] | Phase 29. [VERIFIED: 29-VERIFICATION.md] | Catalog, compile-only, same-AST, repaired, and perturbed evidence remain distinct. [VERIFIED: 29-VERIFICATION.md] |
| Diagnose Beer-Lambert high-noise failures as campaign failures only. [VERIFIED: artifacts/campaigns/v1.4-showcase/aggregate.json] | Produce a supported-bound artifact with high-noise failures visible. [VERIFIED: 31-CONTEXT.md:30-32] [ASSUMED] | Phase 31. [VERIFIED: .planning/ROADMAP.md:81-90] | Avoids hiding unsupported high-noise bounds. [VERIFIED: 31-CONTEXT.md:30-32] |
| No local snap/discrete repair module exists. [VERIFIED: `rg "class .*Repair|def .*repair" src/eml_symbolic_regression` found no implemented repair module] | Add verifier-gated local repair with move provenance. [ASSUMED] | Phase 31. [VERIFIED: .planning/REQUIREMENTS.md:30] | Near-miss candidates can be repaired or explained without claim leakage. [VERIFIED: 31-CONTEXT.md:36-38] |

**Deprecated/outdated:**

- Treating `same_ast_return` alone as bounded proof is not valid because `bounded_100_percent` excludes `same_ast`. [VERIFIED: proof.py:149-164] [VERIFIED: tests/test_proof_contract.py:51-70]
- Hiding high-noise Beer-Lambert failures by dropping them from reports contradicts Phase 31 D-07. [VERIFIED: 31-CONTEXT.md:30-32]
- Using Phase 30 `scaffolded_blind_training_recovered` evidence for Phase 31 contradicts Phase 31 D-04. [VERIFIED: 31-CONTEXT.md:23-26] [VERIFIED: 30-REVIEW.md]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | A new `perturbed_tree` start mode is the least invasive way to execute `perturbed_true_tree_training`. | Architecture Patterns / Recommended Plan Structure | If maintainers prefer overloading `warm_start`, validation and evidence-class tests need a different design. |
| A2 | The first synthetic target inventory should be depths 1, 2, and 3 plus Beer-Lambert. | Architecture Patterns | If this is too narrow, BASN-02 may need more cases; if too broad, tests may become slow or numerically unstable. |
| A3 | Repair may use exact target-neighborhood moves as long as the artifact records provenance and uses `repaired_candidate`. | Architecture Patterns / Common Pitfalls | If target-neighborhood repair is considered too leaky, repair must restrict itself to target-blind local alternatives. |
| A4 | Beer-Lambert raw supported bound should start no higher than noise `5.0` until Phase 31 reruns prove a higher bound. | Recommended Plan Structure | If repair or training recovers noise `15.0` or `35.0`, the supported bound can be widened after evidence exists. |
| A5 | A machine-readable bound report can be implemented in diagnostics/campaign layers without a new external report dependency. | Recommended Plan Structure | If the report belongs only in Phase 33, Phase 31 should still emit raw aggregate fields for Phase 33 to consume. |

## Open Questions (RESOLVED)

1. **RESOLVED: Nonzero same-AST return counts as `perturbed_true_tree_recovered` only on the new perturbed-tree proof path, with `return_kind` preserved.**
   - What we know: `bounded_100_percent` currently excludes `same_ast`, and Phase 31 requires same-AST outcomes to remain distinct. [VERIFIED: proof.py:149-164] [VERIFIED: .planning/REQUIREMENTS.md:31]
   - What's unclear: Whether a nonzero perturbation that trains back to the same AST should be counted as raw perturbed recovery or only as same-AST evidence. [ASSUMED]
   - Recommendation: Store both fields and test the threshold rule explicitly before running the proof suite. [ASSUMED]

2. **RESOLVED: High-noise Beer-Lambert probes live outside bounded proof rows until evidence supports them.**
   - What we know: Phase 31 requires high-noise failures to stay visible and not silently dropped. [VERIFIED: 31-CONTEXT.md:30-32]
   - What's unclear: The cleanest artifact layout for rows outside the supported bound. [ASSUMED]
   - Recommendation: Keep bounded rows in `proof-perturbed-basin` and write separate bound-probe rows/report for `15.0` and `35.0` until repair proves them. [ASSUMED]

3. **RESOLVED: Local repair may use target-neighborhood moves, but accepted repairs remain `repaired_candidate`.**
   - What we know: Phase 31 D-08 allows exact target-neighborhood moves if serialized. [VERIFIED: 31-CONTEXT.md:36]
   - What's unclear: Whether the final proof narrative should separate target-neighborhood repair from generic local repair. [ASSUMED]
   - Recommendation: Add a `source` field on every repair move, such as `embedded_target_slot` or `slot_catalog_neighbor`, and group reports by source. [ASSUMED]

## Open Question Resolutions

Resolved by autonomous orchestrator on 2026-04-15:

1. **Nonzero same-AST return counts as perturbed true-tree recovery only when the run is executed under the new perturbed-tree proof path and records `return_kind == "same_ast_return"`.**
   - Rationale: The perturbed-basin claim is explicitly about returning to the true tree's basin, so returning to the same AST after a declared nonzero perturbation is positive basin evidence. The artifact must still keep `return_kind` distinct for BASN-05 reporting.

2. **High-noise Beer-Lambert probes live outside the bounded proof rows until evidence supports them.**
   - Rationale: The bounded `proof-perturbed-basin` suite should contain only the declared supported bound. Noise `15.0` and `35.0` remain visible through a bound-probe report or suite so Phase 31 can justify a narrowed bound without hiding failures.

3. **Local repair may use target-neighborhood moves, but those repairs are a separate evidence class.**
   - Rationale: Target-aware repair is acceptable for diagnosing and fixing a perturbed true-tree near miss, but it must serialize `source`, changed slots/subtrees, original status, repaired expression, and verifier report, and it must classify accepted repairs as `repaired_candidate`.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| Python | Package, CLI, benchmarks, tests. [VERIFIED: pyproject.toml] | yes [VERIFIED: local version probe] | 3.11.5 [VERIFIED: local version probe] | None needed |
| PyTorch | Soft tree training and logit perturbation. [VERIFIED: optimize.py] [VERIFIED: warm_start.py] | yes [VERIFIED: local import version probe] | 2.10.0 [VERIFIED: local import version probe] | None recommended |
| NumPy | Dataset generation and verifier residuals. [VERIFIED: datasets.py] [VERIFIED: verify.py] | yes [VERIFIED: local import version probe] | 1.26.4 [VERIFIED: local import version probe] | None recommended |
| SymPy | Source formula candidates and compiler validation. [VERIFIED: datasets.py] [VERIFIED: compiler.py] | yes [VERIFIED: local import version probe] | 1.14.0 [VERIFIED: local import version probe] | None recommended |
| mpmath | High-precision verifier checks. [VERIFIED: verify.py:95-113] | yes [VERIFIED: local import version probe] | 1.3.0 [VERIFIED: local import version probe] | None recommended |
| pytest | Regression tests. [VERIFIED: pyproject.toml] | yes [VERIFIED: local import version probe] | 7.4.0 [VERIFIED: local import version probe] | None recommended |
| jq | Local artifact inspection during research. [VERIFIED: jq commands succeeded] | yes [VERIFIED: jq commands succeeded] | not required for implementation [VERIFIED: no pyproject dependency] | Python/json tooling in tests |

**Missing dependencies with no fallback:** None found for Phase 31 implementation. [VERIFIED: local version probes]

**Missing dependencies with fallback:** None found for Phase 31 implementation. [VERIFIED: local version probes]

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | no [VERIFIED: Phase 31 is local CLI/package work] | No authentication surface is introduced. [VERIFIED: cli.py] |
| V3 Session Management | no [VERIFIED: Phase 31 is local CLI/package work] | No sessions are introduced. [VERIFIED: cli.py] |
| V4 Access Control | no [VERIFIED: local artifact paths only] | Preserve existing local file-writing behavior and avoid adding network or multi-user state. [VERIFIED: benchmark.py:1012-1016] [VERIFIED: campaign.py:120-158] |
| V5 Input Validation | yes [VERIFIED: benchmark suite JSON can be user supplied] | Continue fail-closed validation in `BenchmarkCase`, `DatasetConfig`, `OptimizerBudget`, and proof contract checks. [VERIFIED: benchmark.py:62-146] [VERIFIED: benchmark.py:215-295] |
| V6 Cryptography | no [VERIFIED: no crypto behavior in Phase 31 scope] | Do not add cryptography; keep deterministic hashes for manifests only. [VERIFIED: datasets.py:201-240] |

### Known Threat Patterns for Local Benchmark Artifacts

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Oversized custom suite requests excessive depth/noise/seeds. [ASSUMED] | Denial of Service | Validate positive budgets, add Phase 31 suite guardrails, and keep CI proof suite small. [VERIFIED: benchmark.py:121-146] [VERIFIED: 31-CONTEXT.md:41-43] |
| Caller-supplied suite injects an evidence class. [VERIFIED: benchmark.py:194-199] | Tampering | Keep rejecting suite-supplied `evidence_class`; derive from payload after execution. [VERIFIED: benchmark.py:194-199] [VERIFIED: benchmark.py:812-827] |
| Repair overwrites raw failure status. [ASSUMED] | Repudiation / Tampering | Store raw and repaired statuses separately and classify repaired rows as `repaired_candidate`. [VERIFIED: 31-CONTEXT.md:36-38] [VERIFIED: benchmark.py:1257-1270] |
| Output path overwrites prior evidence. [VERIFIED: benchmark.py:1012-1016] | Tampering | Use campaign overwrite guardrails where campaigns are used; for benchmark scratch output, tests should use temp dirs. [VERIFIED: campaign.py:120-129] [VERIFIED: tests/test_benchmark_runner.py] |

## Sources

### Primary (HIGH confidence)

- `.planning/phases/31-perturbed-basin-training-and-local-repair/31-CONTEXT.md` - locked Phase 31 decisions, Beer-Lambert bound narrowing, repair semantics, deferred scope. [VERIFIED]
- `.planning/REQUIREMENTS.md` - BASN-01 through BASN-05 and milestone proof requirements. [VERIFIED]
- `.planning/ROADMAP.md` - Phase 31 goal, success criteria, and dependency graph. [VERIFIED]
- `.planning/STATE.md` - v1.4 Beer-Lambert evidence summary and Phase 30 blocker. [VERIFIED]
- `.planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-VERIFICATION.md` - proof contract, evidence classes, threshold behavior. [VERIFIED]
- `.planning/phases/30-bounded-shallow-blind-training-recovery/30-REVIEW.md` - scaffolded blind recovery separation and unresolved SHAL-02 blocker. [VERIFIED]
- `src/eml_symbolic_regression/warm_start.py` - perturbation config, active slot reports, warm-start train/snap/verify manifest. [VERIFIED]
- `src/eml_symbolic_regression/benchmark.py` - start modes, validation, runner dispatch, evidence classes, threshold aggregation. [VERIFIED]
- `src/eml_symbolic_regression/proof.py` - paper claims, training modes, evidence classes, bounded policy. [VERIFIED]
- `src/eml_symbolic_regression/master_tree.py` - soft tree slots, embedding, snapping, slot setting. [VERIFIED]
- `src/eml_symbolic_regression/verify.py` - verifier-owned recovery contract. [VERIFIED]
- `artifacts/campaigns/v1.4-showcase/aggregate.json` - committed Beer-Lambert high-noise evidence. [VERIFIED]
- `/tmp/eml-phase31-beer-probe/v1.2-evidence/aggregate.json` - current-code Beer-Lambert seed-0 perturbation smoke. [VERIFIED]

### Secondary (MEDIUM confidence)

- `sources/NORTH_STAR.md` - implementation blueprint and paper-grounded qualitative claims about perturbed-correct recovery and numerical instability. [CITED]
- `sources/FOR_DEMO.md` - Beer-Lambert/demo normalization context. [CITED]
- `tests/test_compiler_warm_start.py`, `tests/test_benchmark_contract.py`, `tests/test_benchmark_runner.py`, `tests/test_benchmark_reports.py`, `tests/test_diagnostics.py`, `tests/test_proof_contract.py` - existing behavior and regression patterns. [VERIFIED]

### Tertiary (LOW confidence)

- None. No web-only sources were used. [VERIFIED: research used local files and local command probes]

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH - versions and dependencies were verified locally, and no new dependencies are recommended. [VERIFIED: local version probes] [VERIFIED: pyproject.toml]
- Existing perturbation capability: HIGH - `warm_start.py`, tests, and current Beer probe all verify deterministic perturbation and active-slot reporting. [VERIFIED: warm_start.py] [VERIFIED: tests/test_compiler_warm_start.py] [VERIFIED: /tmp/eml-phase31-beer-probe/v1.2-evidence/aggregate.json]
- Perturbed runner architecture: MEDIUM - the need is verified, but the exact `start_mode` name and payload shape are recommended design choices. [VERIFIED: benchmark.py:552-582] [ASSUMED]
- Local repair architecture: MEDIUM - evidence class support exists, but repair implementation is new and must be proven by tests. [VERIFIED: benchmark.py:1257-1270] [ASSUMED]
- Beer-Lambert supported bound: MEDIUM - existing artifacts support a raw bound through noise `5.0`, but Phase 31 must rerun under final proof semantics before locking the claim. [VERIFIED: artifacts/campaigns/v1.4-showcase/aggregate.json] [ASSUMED]
- Pitfalls: HIGH - current validation, evidence taxonomy, and Beer high-noise failures directly expose the main failure modes. [VERIFIED: benchmark.py] [VERIFIED: proof.py] [VERIFIED: artifacts/campaigns/v1.4-showcase/aggregate.json]

**Research date:** 2026-04-15

**Valid until:** 2026-05-15 for local code patterns, or until Phase 31 changes benchmark start modes, evidence classes, or Beer-Lambert suite bounds. [ASSUMED]
