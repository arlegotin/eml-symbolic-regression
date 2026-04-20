# Phase 71: Training and Verification Semantics Alignment - Context

**Gathered:** 2026-04-20
**Status:** Ready for planning
**Mode:** Autonomous smart discuss; recommended choices accepted by agent discretion

<domain>
## Phase Boundary

This phase aligns the differentiable optimizer's training semantics with the verifier's canonical semantics where feasible, and makes every remaining guarded-training fallback visible in run artifacts and benchmark controls. It focuses on semantics mode selection, diagnostics, and evidence plumbing; it does not run the full publication evidence campaign.

</domain>

<decisions>
## Implementation Decisions

### Semantics Mode
- Add an explicit `guarded` versus `faithful` training semantics mode.
- Keep `guarded` as the default to preserve existing benchmark behavior and numerical stability.
- In `faithful` mode, training forwards use the same unclamped exp/log arithmetic as verification while still recording diagnostics.
- Reject unknown mode values at config boundaries so artifacts cannot silently encode ambiguous semantics.

### Artifact Evidence
- Add a training manifest section that states the semantics mode, whether the objective is verifier-faithful, and why guarded fallback was used.
- Summarize clamp, guard, NaN/Inf, branch, shifted-singularity, and post-snap mismatch diagnostics from existing trace and verifier fields.
- Preserve per-step and per-restart anomaly traces; add summary-level fields for publication tables and audits.
- Include verifier certificate fields already introduced in Phase 70 when scientific-law rows consume run artifacts.

### Ablation Control
- Wire semantics mode through benchmark optimizer budgets so the same suite can be run under `guarded` and `faithful` settings.
- Add CLI override support for lightweight demo and benchmark runs.
- Treat full publication-matrix ablation execution as a Phase 76 rebuild activity; this phase supplies the contract and smoke verification.
- Keep ablation outputs comparable through existing run IDs, aggregate metrics, and manifest schemas.

### the agent's Discretion
- Use existing `TrainingSemanticsConfig`, `TrainingConfig`, `OptimizerBudget`, and manifest patterns rather than introducing a separate experiment framework.
- Add focused tests around semantics behavior, manifest payloads, benchmark parsing, and CLI parsing.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/eml_symbolic_regression/semantics.py` already separates training and verification calls and records rich `AnomalyStats`.
- `src/eml_symbolic_regression/optimize.py` already serializes config, per-step traces, restart anomalies, exact candidate pool, verifier reports, and post-snap losses.
- `src/eml_symbolic_regression/benchmark.py` already carries clamp/log guard settings through `OptimizerBudget` into `TrainingConfig` and extracts anomaly metrics for aggregates.
- Phase 70 added verifier evidence fields including symbolic, dense random, adversarial, certificate, evidence-level, and metric-role labels.

### Established Patterns
- Frozen dataclass configs are serialized with explicit `as_dict()` or config-payload helpers.
- Benchmark configs fail closed through `BenchmarkValidationError`.
- CLI is `argparse` based with simple flags and JSON artifacts.
- Tests prefer fast synthetic smoke cases with small step/restart budgets.

### Integration Points
- `TrainingSemanticsConfig` controls low-level PyTorch EML semantics.
- `TrainingConfig.semantics_config()` bridges optimizer config into model and expression evaluation.
- `_training_config_from_budget()` bridges benchmark budgets into optimizer configs.
- `run_demo()` creates direct and warm-start `TrainingConfig` instances.

</code_context>

<specifics>
## Specific Ideas

Implement the smallest complete contract: explicit semantics mode, faithful behavior tests, manifest summary diagnostics, benchmark budget parsing/serialization, benchmark CLI override, and demo CLI support.

</specifics>

<deferred>
## Deferred Ideas

- Full guarded-versus-faithful publication matrix execution is deferred to Phase 76.
- Full formal interval certificates remain deferred under `FORMAL-02`; Phase 71 consumes the Phase 70 certificate labels.

</deferred>
