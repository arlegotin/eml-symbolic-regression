# Phase 53: Raw-Hybrid Paper Campaign and Claim Package - Pattern Map

**Mapped:** 2026-04-17
**Files analyzed:** 18 target files / artifact families
**Analogs found:** 18 / 18
**Context source:** `53-CONTEXT.md`; no `53-RESEARCH.md` was present.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `src/eml_symbolic_regression/benchmark.py` | config registry, benchmark service | batch, file-I/O | `builtin_suite()` v1.5/v1.9 suites and `execute_benchmark_run()` | exact |
| `src/eml_symbolic_regression/campaign.py` | campaign preset and report service | batch, file-I/O | `_PRESETS`, `run_campaign()`, `write_campaign_tables()` | exact |
| `src/eml_symbolic_regression/paper_decision.py` | paper decision package service | batch, file-I/O | `write_paper_decision_package()` for `artifacts/paper/v1.8` | role-match |
| `src/eml_symbolic_regression/proof_campaign.py` or new `src/eml_symbolic_regression/raw_hybrid_paper.py` | artifact bundle orchestrator | batch, file-I/O | `run_proof_campaign()` | role-match |
| `src/eml_symbolic_regression/proof.py` | proof contract model/config | validation, request-response | `EVIDENCE_CLASSES`, `threshold_policies()`, `claim_matrix()` | role-match; prefer no threshold edits |
| `src/eml_symbolic_regression/diagnostics.py` | diagnostic artifact utility | batch, file-I/O | `write_perturbed_basin_bound_report()` and durable artifact hashes | role-match |
| `src/eml_symbolic_regression/family_triage.py` | centered-family diagnostic reporter | batch, file-I/O | `_classification_for_run()`, `_go_no_go()` | role-match |
| `src/eml_symbolic_regression/witnesses.py` | witness registry/model | transform, validation | `resolve_scaffold_plan()` same-family witness exclusion | exact for centered caveat |
| `src/eml_symbolic_regression/cli.py` | CLI route/controller | request-response, file-I/O | `campaign`, `proof-campaign`, `paper-decision` subcommands | role-match |
| `tests/test_benchmark_contract.py` | test | config validation, batch | built-in suite registry and focused v1.9 suite tests | exact |
| `tests/test_campaign.py` | test | batch, file-I/O | preset, table, report, proof-campaign tests | exact |
| `tests/test_benchmark_reports.py` | test | aggregation, classification | taxonomy, threshold, repair-status aggregate tests | exact |
| `tests/test_paper_decision.py` | test | batch, file-I/O | paper decision package tests | exact |
| `tests/test_proof_contract.py` | test | validation | claim matrix / threshold contract tests | exact if proof contracts change |
| `tests/test_proof_campaign.py` or new `tests/test_raw_hybrid_paper.py` | test | batch, file-I/O | proof campaign bundle and CLI tests | role-match |
| `README.md` | docs | reporting | current artifact-backed v1.9 evidence wording | exact |
| `docs/IMPLEMENTATION.md` | docs | reporting | recovery contract, benchmark reports, v1.9 artifact docs | exact |
| `artifacts/paper/v1.9/*` and `artifacts/campaigns/v1.9-raw-hybrid-paper/*` | generated artifacts | file-I/O | `artifacts/paper/v1.8/*`, `artifacts/proof/v1.6/*`, focused v1.9 campaign artifacts | role-match |

## Pattern Assignments

### `src/eml_symbolic_regression/benchmark.py` (config registry, batch/file-I/O)

**Analog:** `src/eml_symbolic_regression/benchmark.py`

**Use for:** raw-hybrid benchmark suite membership, campaign case ownership, evidence taxonomy source fields, run artifact payloads, aggregate report inputs.

**Imports pattern** (lines 22-39):

```python
from .basin import fit_perturbed_true_tree
from .compiler import CompilerConfig, UnsupportedExpression, compile_and_validate, diagnose_compile_expression
from .datasets import demo_specs, proof_dataset_manifest
from .expression import ConstantOccurrence, Expr, expr_from_document, format_constant_value, parse_constant_value
from .optimize import TrainingConfig, fit_eml_tree
from .proof import (
    EVIDENCE_CLASSES,
    TRAINING_MODES,
    ProofContractError,
    paper_claim,
    threshold_policy,
    validate_claim_reference,
)
from .repair import RepairConfig, cleanup_failed_candidate, repair_perturbed_candidate
from .verify import verify_candidate
```

**Built-in suite registry pattern** (lines 42-72):

```python
BUILTIN_SUITES = (
    "smoke",
    "for-demo-diagnostics",
    "v1.2-evidence",
    "v1.3-standard",
    "v1.5-shallow-pure-blind",
    "v1.5-shallow-proof",
    "proof-perturbed-basin",
    "proof-perturbed-basin-beer-probes",
    "proof-depth-curve",
    "v1.8-family-raw-baseline",
    "v1.8-family-smoke",
    "v1.8-family-calibration",
    "v1.9-arrhenius-evidence",
    "v1.9-michaelis-evidence",
    "v1.9-repair-evidence",
)
```

For Phase 53, add a suite ID here only if the raw-hybrid package needs to run a new combined suite instead of consuming existing aggregate artifacts. A likely name is `v1.9-raw-hybrid-paper`.

**Focused v1.9 suite pattern** (Arrhenius lines 1518-1535; Michaelis lines 1536-1553):

```python
if name == "v1.9-arrhenius-evidence":
    return BenchmarkSuite(
        id="v1.9-arrhenius-evidence",
        description="Focused v1.9 Arrhenius exact warm-start evidence for normalized exp(-0.8/x).",
        cases=(
            _case(
                "arrhenius-warm",
                "arrhenius",
                "warm_start",
                seeds=(0,),
                perturbation_noise=(0.0,),
                points=24,
                warm_steps=1,
                tags=("v1.9", "arrhenius", "warm_start", "same_ast"),
                expect_recovery=True,
            ),
        ),
    )
```

```python
if name == "v1.9-michaelis-evidence":
    return BenchmarkSuite(
        id="v1.9-michaelis-evidence",
        description="Focused v1.9 Michaelis-Menten exact warm-start evidence for normalized 2*x/(x+0.5).",
        cases=(
            _case(
                "michaelis-warm",
                "michaelis_menten",
                "warm_start",
                seeds=(0,),
                perturbation_noise=(0.0,),
                points=24,
                warm_steps=1,
                tags=("v1.9", "michaelis", "warm_start", "same_ast"),
                expect_recovery=True,
            ),
        ),
    )
```

Use this pattern for scientific-law rows that are exact compiler warm-start evidence. Do not label these rows as blind recovery.

**Repair-only suite pattern** (lines 1554-1613):

```python
expanded_repair = BenchmarkRepairConfig(preset="expanded_candidate_pool")
if name == "v1.9-repair-evidence":
    return BenchmarkSuite(
        id="v1.9-repair-evidence",
        description="Focused v1.9 verifier-gated cleanup expansion evidence.",
        cases=(
            _case(
                "radioactive-blind-default-repair",
                "radioactive_decay",
                "blind",
                seeds=(11,),
                tags=("v1.9", "repair", "near_miss", "default_cleanup"),
                repair=BenchmarkRepairConfig(enabled=True),
            ),
            _case(
                "radioactive-blind-expanded-repair",
                "radioactive_decay",
                "blind",
                seeds=(11,),
                tags=("v1.9", "repair", "near_miss", "expanded_cleanup"),
                repair=expanded_repair,
            ),
        ),
    )
```

Use the same tags/provenance convention if Phase 53 adds package-only cases. The existing v1.9 repair evidence is no-improvement repair evidence and should remain separate from recovered rows.

**Run artifact write pattern** (lines 1639-1660):

```python
def run_benchmark_suite(suite: BenchmarkSuite, *, run_filter: RunFilter | None = None) -> BenchmarkSuiteResult:
    results = tuple(execute_benchmark_run(run) for run in filter_runs(suite.expanded_runs(), run_filter))
    return BenchmarkSuiteResult(suite, results)


def execute_benchmark_run(run: BenchmarkRun) -> BenchmarkRunResult:
    started = time.perf_counter()
    payload = _execute_benchmark_run_payload(run)
    payload["evidence_class"] = evidence_class_for_payload(payload)
    payload["metrics"] = _extract_run_metrics(payload)
    payload["timing"] = {"elapsed_seconds": time.perf_counter() - started}
    _write_json(run.artifact_path, payload)
    return BenchmarkRunResult(run, str(payload["status"]), run.artifact_path, payload)
```

Paper packages should cite these per-run JSON artifacts rather than recomputing outcome semantics.

**Compiler diagnostic pattern for scientific-law rows** (lines 2511-2541):

```python
compiler_config = CompilerConfig(
    operator=run.operator,
    max_depth=run.optimizer.max_compile_depth,
    constant_policy="literal_constants",
    proof_spec=run.proof_spec,
    max_macro_attempts=run.optimizer.max_macro_attempts,
)
try:
    compiled = compile_and_validate(spec.candidate.to_sympy(), compiler_config, validation_inputs)
    report = verify_candidate(compiled.expression, splits, tolerance=run.dataset.tolerance)
    return {
        "stage_statuses": {"compiled_seed": report.status},
        "compiled_eml": compiled.as_dict(),
        "compiled_eml_verification": report.as_dict(),
        "_compiled": compiled,
        "claim_status": report.status,
    }
except UnsupportedExpression as exc:
    return {
        "stage_statuses": {"compiled_seed": "unsupported"},
        "compiled_eml": {
            "status": "unsupported",
            **exc.as_dict(),
            "diagnostic": diagnose_compile_expression(spec.candidate.to_sympy(), compiler_config, validation_inputs),
        },
        "claim_status": "unsupported",
    }
```

Scientific-law tables should derive compile support, compile depth, macro/template hits, and verifier status from `compiled_eml`, `compiled_eml_verification`, `status`, `claim_status`, and `metrics`, not from display strings.

**Metric extraction pattern** (lines 2564-2720):

```python
metrics.update(
    {
        "operator_family": operator_spec.get("family"),
        "operator_schedule": operator_spec.get("schedule"),
        "unsupported_reason": _unsupported_reason_from_payload(payload),
        "best_loss": training.get("best_loss"),
        "post_snap_loss": selected.get("post_snap_loss"),
        "candidate_pool_size": candidate_count,
        "selected_candidate_id": selected.get("candidate_id"),
        "fallback_candidate_id": fallback.get("candidate_id"),
        "warm_start_mechanism": warm_start.get("mechanism"),
        "warm_start_status": warm_start.get("status"),
        "repair_status": repair.get("status"),
        "repair_candidate_root_count": repair.get("candidate_root_count"),
        "repair_deduped_variant_count": repair.get("deduped_variant_count"),
        "repair_accepted_candidate_id": accepted_repair.get("candidate_id"),
        "repair_verifier_status": repair_verification.get("status"),
        "refit_status": refit.get("status"),
        "refit_accepted": refit.get("accepted"),
        "refit_verifier_status": refit_verification.get("status"),
    }
)
```

Phase 53 reports should keep these columns visible so pure blind, scaffolded, compile-only, warm-start, same-AST return, repaired, refit, and perturbed-basin evidence cannot collapse into one metric.

**Aggregate report pattern** (lines 2725-2770):

```python
def write_aggregate_reports(result: BenchmarkSuiteResult, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    aggregate = aggregate_evidence(result)
    json_path = output_dir / "aggregate.json"
    markdown_path = output_dir / "aggregate.md"
    _write_json(json_path, aggregate)
    markdown_path.write_text(render_aggregate_markdown(aggregate), encoding="utf-8")
    return {"json": json_path, "markdown": markdown_path}
```

```python
return {
    "schema": "eml.benchmark_aggregate.v1",
    "suite": result.suite.as_dict(),
    "counts": _aggregate_counts(runs),
    "by_formula": _group_counts(runs, ("formula",)),
    "by_start_mode": _group_counts(runs, ("start_mode",)),
    "by_evidence_class": _group_counts(runs, ("evidence_class",)),
    "by_return_kind": _group_counts(runs, ("return_kind",)),
    "by_raw_status": _group_counts(runs, ("raw_status",)),
    "by_repair_status": _group_counts(runs, ("repair_status",)),
    "depth_curve": _depth_curve_summary(runs),
    "thresholds": _threshold_summary(runs),
    "runs": runs,
}
```

Use aggregate JSON as the package source of truth for paper-facing summaries.

**Return-kind classification pattern** (lines 3033-3070):

```python
if repair_status in {"repaired", "accepted"}:
    return "repaired_candidate"
if status == "recovered" and start_mode in {"warm_start", "perturbed"}:
    changed_slots = _changed_slots_from_payload(payload)
    if changed_slots == 0:
        return "same_ast_return"
    if changed_slots is not None:
        return "verified_equivalent_ast"
if status == "recovered" and start_mode == "blind":
    if scaffold_plan and scaffold_plan != "none":
        return "scaffolded_blind_recovery"
    return "blind_recovery"
```

This is the core separation required by RHY-02.

### `src/eml_symbolic_regression/campaign.py` (campaign preset and reports, batch/file-I/O)

**Analog:** `src/eml_symbolic_regression/campaign.py`

**Use for:** campaign preset addition, aggregate report wiring, campaign tables, paper-facing report sections, scientific-law table extension.

**Imports pattern** (lines 18-26):

```python
from .benchmark import (
    BenchmarkSuite,
    RunFilter,
    _code_version,
    aggregate_evidence,
    load_suite,
    run_benchmark_suite,
    write_aggregate_reports,
)
```

Do not duplicate benchmark execution logic in the paper package. Campaign code should call the benchmark API and then render tables/reports.

**Preset pattern** (lines 82-195):

```python
_PRESETS: dict[str, CampaignPreset] = {
    "proof-shallow-pure-blind": CampaignPreset(
        name="proof-shallow-pure-blind",
        suite="v1.5-shallow-pure-blind",
        description="Measured shallow pure-blind recovery boundary.",
        tier="proof",
        guardrail="Do not mix scaffolded or warm-start rows into this denominator.",
    ),
    "arrhenius-evidence": CampaignPreset(
        name="arrhenius-evidence",
        suite="v1.9-arrhenius-evidence",
        description="Focused Arrhenius exact compiler warm-start/same-AST evidence.",
        tier="evidence",
        guardrail="Report as exact warm-start evidence, not blind discovery.",
    ),
}
```

Add any Phase 53 preset here with a guardrail that matches RHY-02/RHY-05. The likely preset name is `raw-hybrid-paper`, backed by `v1.9-raw-hybrid-paper` or a package orchestrator that consumes existing focused campaign outputs.

**Campaign execution and output pattern** (lines 209-269):

```python
base_suite = load_suite(preset.suite)
suite = BenchmarkSuite(
    id=base_suite.id,
    description=base_suite.description,
    cases=base_suite.cases,
    artifact_root=campaign_dir / "runs",
)
result = run_benchmark_suite(suite, run_filter=run_filter)
suite_result_path = campaign_dir / "suite-result.json"
_write_json(suite_result_path, result.as_dict())
aggregate_paths = write_aggregate_reports(result, campaign_dir)
aggregate = aggregate_evidence(result)
table_paths = write_campaign_tables(aggregate, campaign_dir / "tables")
figure_paths = write_campaign_plots(aggregate, campaign_dir / "figures")
manifest = _manifest_payload(
    preset=preset,
    suite=suite,
    campaign_dir=campaign_dir,
    label=label,
    overwrite=overwrite,
    run_filter=run_filter,
    aggregate=aggregate,
    suite_result_path=suite_result_path,
    aggregate_paths=aggregate_paths,
    table_paths=table_paths,
    figure_paths=figure_paths,
)
report_path = write_campaign_report(campaign_dir, manifest, aggregate, table_paths, figure_paths)
```

Generated artifact paths for Phase 53 should follow this layout unless the package is explicitly a higher-level `artifacts/paper/v1.9` bundle.

**Table writer pattern** (lines 272-328):

```python
def write_campaign_tables(aggregate: Mapping[str, object], output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    runs = list(aggregate.get("runs", ()))
    paths = {
        "runs_csv": output_dir / "runs.csv",
        "group_formula_csv": output_dir / "group-formula.csv",
        "group_start_mode_csv": output_dir / "group-start-mode.csv",
        "operator_family_recovery_csv": output_dir / "operator-family-recovery.csv",
        "operator_family_diagnostics_csv": output_dir / "operator-family-diagnostics.csv",
        "headline_json": output_dir / "headline-metrics.json",
        "failures_csv": output_dir / "failures.csv",
    }
    run_rows = [_run_csv_row(run) for run in runs]
    _write_csv(paths["runs_csv"], run_rows, _RUN_COLUMNS)
    _write_csv(paths["group_formula_csv"], _group_rows(runs, "formula"), _GROUP_COLUMNS)
    _write_csv(paths["group_start_mode_csv"], _group_rows(runs, "start_mode"), _GROUP_COLUMNS)
    family_recovery_rows = _operator_family_recovery_rows(runs)
    _write_csv(paths["operator_family_recovery_csv"], family_recovery_rows, _OPERATOR_FAMILY_RECOVERY_COLUMNS)
    _write_json(paths["headline_json"], _headline_metrics(runs))
    return paths
```

Scientific-law tables should be implemented as an additional table writer here or in the paper package using the same `_write_csv`, `_write_markdown_table`, and JSON payload conventions.

**Run table columns to preserve** (lines 569-614):

```python
_RUN_COLUMNS = (
    "campaign",
    "suite",
    "case",
    "run_id",
    "formula",
    "start_mode",
    "training_mode",
    "evidence_class",
    "return_kind",
    "raw_status",
    "repair_status",
    "repair_verifier_status",
    "repair_candidate_root_count",
    "repair_deduped_variant_count",
    "refit_status",
    "refit_accepted",
    "threshold_policy",
    "dataset_manifest_sha256",
    "warm_start_mechanism",
    "artifact_path",
)
```

Do not drop these fields from any paper-facing table; RHY-02 depends on them.

**Run row extraction pattern** (lines 721-773):

```python
def _run_csv_row(run: Mapping[str, object]) -> dict[str, object]:
    metrics = _mapping(run.get("metrics"))
    return {
        "suite": run.get("suite"),
        "case": run.get("case"),
        "run_id": run.get("run_id"),
        "formula": run.get("formula"),
        "start_mode": run.get("start_mode"),
        "training_mode": run.get("training_mode"),
        "status": run.get("status"),
        "claim_status": run.get("claim_status"),
        "evidence_class": run.get("evidence_class"),
        "return_kind": run.get("return_kind"),
        "raw_status": run.get("raw_status"),
        "repair_status": run.get("repair_status"),
        "repair_verifier_status": metrics.get("repair_verifier_status"),
        "artifact_path": run.get("artifact_path"),
    }
```

Scientific-law rows should copy this style: extract from aggregate run dictionaries, preserve raw artifact path, and avoid reclassifying statuses manually.

**Report non-overclaim wording pattern** (lines 1132-1184, 1187-1211, 1333-1364):

```python
if regimes == {"perturbed"}:
    return (
        "This campaign probes local basin and repair behavior, not blind-discovery performance. "
        "Recovered rows begin from exact target-tree perturbations and should be cited only as basin evidence."
    )
if regimes == {"warm_start"}:
    return (
        "All recovered rows in this campaign use compiler warm-starts. "
        "Those are recovery and basin checks, not blind-discovery claims."
    )
return (
    "This mixed campaign contains multiple evidence paths. The tables and aggregate counts keep them separated "
    "by start mode, training mode, evidence class, raw status, repair status, and return kind; they should not be "
    "merged into a single recovery denominator."
)
```

```python
lines.extend(
    [
        "## Regime Summary",
        "",
        "| Regime | Runs | Recovered | Unsupported | Failed | Same-AST | Repaired |",
        "|--------|------|-----------|-------------|--------|----------|----------|",
    ]
)
```

Copy this style into the Phase 53 paper report. It already says same-AST and repaired evidence are useful but not discovery claims.

### `src/eml_symbolic_regression/paper_decision.py` (paper decision package, batch/file-I/O)

**Analog:** `src/eml_symbolic_regression/paper_decision.py`

**Use for:** paper-facing decision memo, safe/unsafe claim docs, figure/table inventory, completeness boundary, v1.9 claim package location.

**Claim boundary constants** (lines 11-35):

```python
DEFAULT_PAPER_OUTPUT_ROOT = Path("artifacts/paper/v1.8")

SAFE_CLAIMS = (
    "Raw EML is the current searchability baseline for the measured family campaigns.",
    "Centered-family variants are diagnostic/negative evidence unless calibration campaigns beat raw.",
    "Report pure blind, scaffolded, warm-start, repaired, and perturbed-basin evidence as separate regimes.",
)

UNSAFE_CLAIMS = (
    "Centered-family EML universally improves symbolic recovery.",
    "Centered-family blind failures prove no centered-family representation exists.",
    "Do not merge pure blind, scaffolded, compile-only, warm-start, repaired, and perturbed-basin evidence into one recovery metric.",
)
```

For Phase 53, use `artifacts/paper/v1.9` and update safe/unsafe claims to mention raw-hybrid scientific-law evidence, exact compiler warm-start/same-AST status, repair-only no-improvement status, and the centered same-family witness caveat.

**Package writer pattern** (lines 60-87):

```python
def write_paper_decision_package(
    aggregate_paths: Sequence[Path],
    *,
    output_dir: Path = DEFAULT_PAPER_OUTPUT_ROOT,
) -> PaperDecisionPaths:
    output_dir.mkdir(parents=True, exist_ok=True)
    aggregates = [_load_json(path) for path in aggregate_paths]
    summary = _summarize_aggregates(aggregates, aggregate_paths)
    decision = _decision_payload(summary)
    paths = PaperDecisionPaths(
        output_dir=output_dir,
        decision_json=output_dir / "decision-memo.json",
        decision_markdown=output_dir / "decision-memo.md",
        safe_claims=output_dir / "safe-claims.md",
        unsafe_claims=output_dir / "unsafe-claims.md",
        figure_inventory=output_dir / "figure-table-inventory.md",
        completeness_boundary=output_dir / "completeness-boundary.md",
    )
    _write_json(paths.decision_json, decision)
    paths.decision_markdown.write_text(_decision_markdown(decision), encoding="utf-8")
    paths.safe_claims.write_text(_claims_doc("Safe Claims", SAFE_CLAIMS, summary), encoding="utf-8")
    paths.unsafe_claims.write_text(_claims_doc("Unsafe Claims", UNSAFE_CLAIMS, summary), encoding="utf-8")
    paths.figure_inventory.write_text(_figure_inventory_markdown(summary), encoding="utf-8")
    paths.completeness_boundary.write_text(_completeness_boundary_markdown(decision), encoding="utf-8")
    return paths
```

A v1.9 package can extend this writer or use a sibling module. Keep the one-call writer that returns all generated paths.

**Aggregate summary pattern** (lines 96-131):

```python
for aggregate, path in zip(aggregates, paths):
    runs = list(aggregate.get("runs", ()))
    for run in runs:
        family = str(run.get("operator_family") or "unknown")
        row = summary["operator_families"].setdefault(
            family,
            {"runs": 0, "recovered": 0, "unsupported": 0, "failed": 0, "aggregate_paths": []},
        )
        row["runs"] += 1
        if run.get("claim_status") == "recovered":
            row["recovered"] += 1
        elif run.get("claim_status") == "unsupported":
            row["unsupported"] += 1
        else:
            row["failed"] += 1
```

For v1.9, summarize by formula/start mode/evidence class/return kind in addition to operator family so RHY-02 and RHY-03 remain visible.

**Decision payload pattern** (lines 134-174):

```python
return {
    "schema": "eml.paper_decision.v1",
    "recommendation": recommendation,
    "rationale": rationale,
    "raw_family": raw,
    "centered_families": centered,
    "decision_options": {
        "publish_raw_eml_searchability_note": bool(raw["recovery_rate"] > 0 and not centered_better),
        "publish_centered_improvement_claim": bool(centered_better),
        "wait_for_calibration": bool(not raw["runs"] or not centered),
    },
    "claim_boundary": {
        "pure_blind_separate": True,
        "warm_start_separate": True,
        "repair_separate": True,
        "perturbed_basin_separate": True,
    },
}
```

Preserve the `claim_boundary` fail-safe. Add v1.9 fields only if they support paper claims without changing denominator policy.

**Completeness boundary pattern** (lines 217-231):

```python
return "\n".join(
    [
        "# Completeness Boundary",
        "",
        "Status: incomplete for centered-family improvement claims.",
        "",
        "Centered-family unsupported rows currently include missing same-family warm-start witness cases. "
        "Those rows are evidence that the integration is incomplete, not evidence that the centered family "
        "cannot represent the target.",
    ]
)
```

Use this exact caveat structure for RHY-04.

### `src/eml_symbolic_regression/proof_campaign.py` or new `raw_hybrid_paper.py` (artifact bundle orchestrator, batch/file-I/O)

**Analog:** `src/eml_symbolic_regression/proof_campaign.py`

**Use for:** one-command paper package generation, campaign locks, manifest, bundle report, separation from archived anchors.

**Preset orchestration pattern** (lines 18-33, 56-108):

```python
DEFAULT_PROOF_OUTPUT_ROOT = Path("artifacts/proof/v1.6")

PROOF_CAMPAIGN_PRESETS = (
    "proof-shallow-pure-blind",
    "proof-shallow-scaffolded",
    "proof-perturbed-basin",
    "proof-depth-curve",
)


def run_proof_campaign(
    *,
    output_root: Path = DEFAULT_PROOF_OUTPUT_ROOT,
    overwrite: bool = False,
    campaign_presets: Sequence[str] = PROOF_CAMPAIGN_PRESETS,
    run_filters: Mapping[str, RunFilter] | None = None,
) -> ProofCampaignResult:
    campaigns_dir = output_root / "campaigns"
    campaign_results = []
    for preset in campaign_presets:
        result = run_campaign(
            preset,
            output_root=campaigns_dir,
            label=preset,
            overwrite=overwrite,
            run_filter=run_filters.get(preset),
        )
        campaign_results.append(result)
    manifest = _proof_manifest_payload(
        output_root=output_root,
        campaigns=campaign_results,
        basin_bound_paths=basin_bound_paths,
        baseline_campaigns=baseline_campaigns,
        archived_anchor_roots=archived_anchor_roots,
        reproduction_command=reproduction_command
        or f"PYTHONPATH=src python -m eml_symbolic_regression.cli proof-campaign --output-root {output_root}",
    )
    _write_json(manifest_path, manifest)
```

If Phase 53 gets a new package command, copy this high-level orchestration rather than embedding it in `campaign.py`.

**Report boundary pattern** (lines 111-246):

```python
lines = [
    "# v1.6 Proof Campaign Report",
    "",
    "This bundle keeps bounded proof claims, measured blind boundaries, and older showcase artifacts separate.",
    "",
    "## Reproduce",
    "",
    f"`{manifest.get('reproduce_command')}`",
    "",
    "## Regime Summary",
]
```

```python
lines.extend(
    [
        "## Out of Scope",
        "",
        "- Complete search is a representation/algorithmic context claim, not an empirical recovery guarantee.",
        "- Universal blind recovery is out of scope; measured depth degradation is reported separately.",
        "- Compile-only and catalog artifacts do not satisfy training-proof recovery claims.",
    ]
)
```

Phase 53 should use similar sections for raw-hybrid claim boundaries and paper-safe wording.

**Manifest and lock pattern** (lines 249-316, 382-399):

```python
return {
    "schema": "eml.proof_campaign.v1",
    "output_root": str(output_root),
    "generated_at": _utc_now(),
    "code_version": _code_version(),
    "campaigns": campaign_payloads,
    "claims": claim_rows,
    "regime_summary": _regime_summary_rows(all_runs),
    "depth_curve": depth_curve_rows,
    "campaign_locks": [_campaign_lock(result.output_dir) for result in campaign_results],
    "out_of_scope_claims": out_of_scope,
}
```

```python
for relative in (
    "aggregate.json",
    "suite-result.json",
    "campaign-manifest.json",
    "report.md",
    "tables/runs.csv",
    "tables/failures.csv",
):
    path = campaign_dir / relative
    if path.exists():
        files.append({"path": str(path), "sha256": _sha256(path)})
```

The Phase 53 paper package should hash or lock every aggregate, suite result, manifest, report, and table that it cites.

### `src/eml_symbolic_regression/proof.py` (proof contract model/config, validation)

**Analog:** `src/eml_symbolic_regression/proof.py`

**Use for:** evidence class taxonomy and denominator separation. Phase 53 should normally consume these contracts, not edit them.

**Evidence taxonomy pattern** (lines 19-42):

```python
TRAINING_MODES = (
    "blind_training",
    "scaffolded_training",
    "compiler_warm_start",
    "catalog",
    "perturbed_tree",
)

EVIDENCE_CLASSES = (
    "catalog_reference",
    "compile_only",
    "blind_training_recovered",
    "scaffolded_training_recovered",
    "compiler_warm_start_recovered",
    "perturbed_true_tree_recovered",
    "repaired_candidate",
    "same_ast",
    "verified_equivalent_ast",
    "unsupported",
    "failed",
)
```

Paper tables should use these values directly.

**Claim contract pattern** (lines 113-148):

```python
@dataclass(frozen=True)
class PaperClaim:
    id: str
    title: str
    claim_class: str
    threshold_policy_id: str
    required_training_modes: tuple[str, ...]
    allowed_evidence_classes: tuple[str, ...]
    denominator_scope: str
    numerator_scope: str
    notes: tuple[str, ...] = ()
```

If a new v1.9 paper claim is truly necessary, define it with this dataclass and add contract tests. Context says do not change thresholds/denominators, so prefer package-level claim docs over new proof contracts.

**Existing claim boundary pattern** (lines 258-356):

```python
"paper-shallow-blind-recovery": PaperClaim(
    id="paper-shallow-blind-recovery",
    title="Measured pure-blind recovery on shallow laws",
    claim_class="measured",
    threshold_policy_id="measured_pure_blind_recovery",
    required_training_modes=("blind_training",),
    allowed_evidence_classes=("blind_training_recovered", "failed", "unsupported"),
    denominator_scope="Only pure random-initialized blind runs in the declared shallow suite.",
    numerator_scope="Rows with evidence_class=blind_training_recovered.",
    notes=(
        "Scaffolded or initialized runs are not counted in this measured blind denominator.",
        "The result is a measured rate, not a bounded completeness theorem.",
    ),
),
```

```python
"paper-perturbed-true-tree-basin": PaperClaim(
    id="paper-perturbed-true-tree-basin",
    title="Verifier-gated recovery basin around known EML witnesses",
    claim_class="bounded",
    threshold_policy_id="bounded_100_percent",
    required_training_modes=("perturbed_tree",),
    allowed_evidence_classes=("perturbed_true_tree_recovered", "repaired_candidate", "same_ast", "failed", "unsupported"),
    denominator_scope="Only declared nonzero perturbation neighborhoods around exact EML witnesses.",
    numerator_scope="Rows with verifier-gated recovery under the declared perturbation grid.",
    notes=(
        "This is basin evidence, not a blind-discovery claim.",
        "Same-AST return after nonzero perturbation may count only under this perturbed-tree proof, never as blind recovery.",
    ),
),
```

**Threshold count guard pattern** (lines 3216-3226):

```python
if claim_id == "paper-shallow-blind-recovery":
    return ("blind_training_recovered",)
if claim_id == "paper-shallow-scaffolded-recovery":
    return ("scaffolded_training_recovered",)
if claim_id == "paper-perturbed-true-tree-basin":
    return ("perturbed_true_tree_recovered", "repaired_candidate")
return tuple(allowed)
```

This is the strongest existing guard against RHY-02 overclaiming.

### `src/eml_symbolic_regression/diagnostics.py` (diagnostic artifact utility, batch/file-I/O)

**Analog:** `src/eml_symbolic_regression/diagnostics.py`

**Use for:** Beer-Lambert perturbed basin bound report, artifact checksums, probe rows outside proof denominators.

**Bound report writer pattern** (lines 65-172):

```python
def build_perturbed_basin_bound_report(
    bounded_aggregate_path: Path,
    probe_aggregate_path: Path,
    *,
    formula: str = "beer_lambert",
    declared_bound: float = 0.005,
) -> dict[str, object]:
    bounded = _load_json(bounded_aggregate_path)
    probe = _load_json(probe_aggregate_path)
    bounded_rows = _bound_report_rows(bounded, source="bounded")
    probe_rows = _bound_report_rows(probe, source="probe")
    return {
        "schema": "eml.perturbed_basin_bound_report.v1",
        "formula": formula,
        "declared_bound": declared_bound,
        "bounded_aggregate": str(bounded_aggregate_path),
        "probe_aggregate": str(probe_aggregate_path),
        "rows": bounded_rows + probe_rows,
        "status": status,
    }
```

```python
def write_perturbed_basin_bound_report(
    bounded_aggregate_path: Path,
    probe_aggregate_path: Path | None,
    output_dir: Path,
) -> dict[str, Path]:
    bounded_aggregate = json.loads(Path(bounded_aggregate_path).read_text(encoding="utf-8"))
    probe_aggregate = None
    if probe_aggregate_path is not None:
        probe_aggregate = json.loads(Path(probe_aggregate_path).read_text(encoding="utf-8"))
    report = build_perturbed_basin_bound_report(bounded_aggregate, probe_aggregate)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "basin-bound.json"
    markdown_path = output_dir / "basin-bound.md"
    _write_json(json_path, report)
    markdown_path.write_text(render_perturbed_basin_bound_markdown(report), encoding="utf-8")
```

Use this if Phase 53 needs to include Beer-Lambert boundary evidence in the paper package.

**Probe separation wording pattern** (lines 175-228):

```python
lines = [
    "# Perturbed Basin Bound Report",
    "",
    f"Declared bound: `{report.get('declared_bound')}`.",
    "",
    "High-noise probe rows are reported as diagnostics and are not part of the bounded proof denominator.",
]
```

**Durable artifact hash pattern** (lines 562-593, 725-730, 853-871):

```python
return {
    "source": source,
    "suite": run.get("suite"),
    "case": run.get("case"),
    "run_id": run.get("run_id"),
    "claim_status": run.get("claim_status"),
    "evidence_class": run.get("evidence_class"),
    "return_kind": run.get("return_kind"),
    "raw_status": run.get("raw_status"),
    "repair_status": run.get("repair_status"),
    "artifact_path": artifact_path,
    "artifact_sha256": _artifact_sha256(artifact_path),
}
```

```python
def _has_durable_artifact(row: Mapping[str, object]) -> bool:
    artifact_path = str(row.get("artifact_path") or "")
    artifact_hash = str(row.get("artifact_sha256") or "")
    return _is_durable_artifact_path(artifact_path) and bool(artifact_hash)
```

Paper package citations should include both path and SHA-256 for evidence rows when possible.

### `src/eml_symbolic_regression/family_triage.py` and `src/eml_symbolic_regression/witnesses.py` (centered-family negative diagnostics)

**Analog:** `src/eml_symbolic_regression/family_triage.py`, `src/eml_symbolic_regression/witnesses.py`

**Use for:** RHY-04 centered-family framing and same-family witness caveat.

**Centered classification pattern** (`family_triage.py` lines 141-183):

```python
if claim_status == "unsupported":
    reason = str(run.get("unsupported_reason") or "")
    if reason in {"centered_family_warm_start_rules_missing", "centered_family_same_family_seed_missing"}:
        return {
            "category": "missing_integration",
            "action": "accepted_fail_closed_until_same_family_seed_exists",
            "reason": reason,
        }
    if reason == "centered_family_target_seed_missing":
        return {
            "category": "missing_target_witness",
            "action": "accepted_fail_closed_until_same_family_target_exists",
            "reason": reason,
        }
```

**Go/no-go wording pattern** (`family_triage.py` lines 186-217):

```python
if missing_integration:
    recommendation = (
        "Proceed only with campaigns whose centered paths are explicitly supported or fail-closed; "
        "do not treat centered warm-start unsupported rows as recovery failures hidden from denominators."
    )
elif negative_signal:
    recommendation = (
        "Proceed with measured negative centered-family evidence and keep claims conservative."
    )
```

**Same-family witness caveat source** (`witnesses.py` lines 10, 79-94):

```python
CENTERED_FAMILY_SAME_FAMILY_WITNESS_MISSING = "centered_family_same_family_witness_missing"
```

```python
elif kind in known_kinds and not operator.is_raw:
    exclusions.append(scaffold_exclusion_code(kind, CENTERED_FAMILY_SAME_FAMILY_WITNESS_MISSING))
```

Phase 53 claim docs should say centered-family evidence is negative diagnostic evidence with a same-family witness caveat, not a proof of non-representability.

### `src/eml_symbolic_regression/cli.py` (CLI route/controller, request-response/file-I/O)

**Analog:** `src/eml_symbolic_regression/cli.py`

**Use for:** optional raw-hybrid paper command, existing campaign/proof/paper-decision command style.

**Paper decision command pattern** (lines 413-418):

```python
def paper_decision_command(args: argparse.Namespace) -> int:
    paths = write_paper_decision_package(
        tuple(Path(path) for path in args.aggregate or ()),
        output_dir=Path(args.output_dir),
    )
    print(f"paper decision: {paths.as_dict()}")
    return 0
```

**Parser pattern** (lines 520-523):

```python
paper_decision = sub.add_parser("paper-decision", help="Write the paper decision memo package.")
paper_decision.add_argument("--aggregate", action="append", help="Benchmark aggregate JSON to summarize. Repeatable.")
paper_decision.add_argument("--output-dir", default=str(DEFAULT_PAPER_OUTPUT_ROOT), help="Directory for decision memo outputs.")
paper_decision.set_defaults(func=paper_decision_command)
```

If Phase 53 adds a new command, mirror the `campaign`, `proof-campaign`, or `paper-decision` command instead of introducing a new CLI framework.

### Tests to Extend

#### `tests/test_benchmark_contract.py`

**Analog:** built-in suite registry and focused v1.9 suite contract tests.

Use this file to verify:

- `v1.9-raw-hybrid-paper` is listed in `BUILTIN_SUITES` if added.
- Suite cases include the required evidence families from RHY-01.
- Arrhenius and Michaelis stay exact compiler warm-start/same-AST evidence.
- Repair rows stay repair-only and do not expect recovery if the existing evidence remains no-improvement.

Existing exact patterns:

- Built-in suite registry test lines 93-126.
- Arrhenius suite test lines 134-162.
- Michaelis suite test lines 165-196.
- Repair suite test lines 256-267.

#### `tests/test_campaign.py`

**Analog:** campaign preset, table, report, proof bundle tests.

Use this file to verify:

- New campaign preset maps to the intended suite and guardrail.
- `write_campaign_tables()` emits any scientific-law table with formula, compile support, compile depth, macro hits, warm-start status, verifier status, and artifact path.
- Report wording keeps pure blind, scaffolded, compile-only, warm-start, same-AST, repaired, refit, and perturbed-basin regimes separate.
- Mixed raw-hybrid report includes strengths/limitations without blind-discovery overclaims.

Existing patterns:

- `test_campaign_presets_map_to_budgeted_suites` lines 76-143.
- `test_campaign_writes_manifest_suite_result_and_aggregate` lines 145-166.
- `test_campaign_tables_preserve_perturbed_repair_status_columns` lines 335-386.
- `test_proof_campaign_tables_and_manifest_preserve_claim_metadata` lines 389-428.
- `test_proof_basin_report_names_probe_suite_and_status_taxonomy` lines 430-482.
- `test_campaign_writes_self_contained_report` lines 530-557.
- `test_strengths_paragraph_*` lines 582-696.
- `test_limitations_section_counts_*` lines 699-720.

#### `tests/test_benchmark_reports.py`

**Analog:** aggregate taxonomy and threshold-denominator tests.

Use this file to verify:

- Aggregate rows classify `same_ast_return`, `verified_equivalent_ast`, `repaired_candidate`, unsupported, failed, pure blind, scaffolded, and perturbed rows distinctly.
- Threshold summaries do not count warm-start or same-AST rows into pure blind claims.
- Paper-facing aggregate input contains fields required for the scientific-law table.

Existing patterns:

- `_synthetic_result` helper lines 23-76.
- `test_aggregate_evidence_separates_unsupported_and_same_ast` lines 79-94.
- `test_aggregate_run_rows_preserve_hybrid_selection_and_refit_metrics` lines 97-124.
- `test_shallow_pure_blind_threshold_reports_only_random_initialized_recovery` lines 158-236.
- `test_perturbed_bounded_threshold_counts_repaired_candidates` lines 290-348.
- `test_aggregate_evidence_keeps_perturbed_raw_and_repair_taxonomy_distinct` lines 387-511.

#### `tests/test_paper_decision.py`

**Analog:** paper package claim-boundary tests.

Use this file or a new `tests/test_raw_hybrid_paper.py` to verify:

- The v1.9 package writes JSON/Markdown claim docs under `artifacts/paper/v1.9`.
- Safe claims mention exact compiler warm-start/same-AST and repair-only no-improvement evidence precisely.
- Unsafe claims prohibit a single merged recovery denominator.
- Centered-family output includes the same-family witness caveat.

Existing patterns:

- `test_paper_decision_waits_when_centered_evidence_is_missing` lines 29-48.
- `test_paper_decision_can_select_publish_when_centered_beats_raw` lines 50-68.
- `test_paper_decision_selects_raw_note_when_centered_does_not_beat_raw` lines 71-89.

#### `tests/test_proof_contract.py`

**Analog:** proof claim/threshold validation tests.

Extend only if `proof.py` changes. Phase 53 context says no threshold or denominator changes, so the preferred outcome is no new proof contract edits.

#### `tests/test_proof_campaign.py` or new `tests/test_raw_hybrid_paper.py`

**Analog:** one-command artifact bundle tests.

Use this if Phase 53 adds a package orchestrator command:

- `test_run_proof_campaign_writes_bundle_and_claim_report` lines 15-53.
- `test_cli_proof_campaign_command_writes_bundle` lines 55-94.

Mirror these tests for a raw-hybrid package command and assert manifest/report/table outputs plus locked source artifacts.

### Docs and Artifact Outputs

#### `README.md`

**Analog:** current artifact-backed evidence wording.

Use these sections:

- Lines 31-33: current scope wording says shallow exact recovery, Beer-Lambert compiler warm start, Arrhenius/Michaelis exact compiler warm-start/same-AST, and repair-only evidence.
- Lines 97-112: reproduction commands for focused v1.9 evidence campaigns.
- Lines 175-188: evidence class explanations for `same_ast_return`, `verified_equivalent_ast`, and `repaired_candidate`.
- Lines 192-196: current v1.9 Arrhenius/Michaelis/repair artifact facts.
- Lines 226-228: no arbitrary deep blind recovery; warm-start success is distinct.

Docs updates should happen only after the v1.9 paper artifacts exist and should link to those exact artifact paths.

#### `docs/IMPLEMENTATION.md`

**Analog:** implementation contract and report docs.

Use these sections:

- Lines 21-36: recovery contract and cleanup taxonomy.
- Lines 77-84: benchmark suite registry docs.
- Lines 98-104: repair evidence command and no-improvement result.
- Lines 116-129: aggregate reports/evidence classes and warning that same-AST/repaired/low loss is not blind discovery.
- Lines 131-133: Arrhenius/Michaelis artifact facts.
- Lines 187-210: demo commands and boundary examples.

#### `artifacts/paper/v1.9/*`

**Analog generated outputs:**

- `artifacts/paper/v1.8/decision-memo.json`
- `artifacts/paper/v1.8/decision-memo.md`
- `artifacts/paper/v1.8/safe-claims.md`
- `artifacts/paper/v1.8/unsafe-claims.md`
- `artifacts/paper/v1.8/figure-table-inventory.md`
- `artifacts/paper/v1.8/completeness-boundary.md`
- `artifacts/proof/v1.6/proof-campaign.json`
- `artifacts/proof/v1.6/proof-report.md`
- `artifacts/proof/v1.6/anchor-locks.json`

Likely Phase 53 outputs:

- `artifacts/paper/v1.9/raw-hybrid-paper-package.json`
- `artifacts/paper/v1.9/raw-hybrid-paper-report.md`
- `artifacts/paper/v1.9/safe-claims.md`
- `artifacts/paper/v1.9/unsafe-claims.md`
- `artifacts/paper/v1.9/scientific-law-table.csv`
- `artifacts/paper/v1.9/scientific-law-table.md`
- `artifacts/paper/v1.9/scientific-law-table.json`
- `artifacts/paper/v1.9/claim-boundaries.md`
- `artifacts/paper/v1.9/source-artifact-locks.json`

Use existing JSON schema names with a new versioned schema string, for example `eml.raw_hybrid_paper_package.v1`.

## Shared Patterns

### Evidence Taxonomy and Regime Separation

**Sources:** `src/eml_symbolic_regression/proof.py`, `src/eml_symbolic_regression/benchmark.py`, `src/eml_symbolic_regression/campaign.py`

**Apply to:** all reports, tables, claim docs, docs updates.

Use `training_mode`, `evidence_class`, `return_kind`, `raw_status`, `repair_status`, and `start_mode` as separate table/report dimensions. Do not merge pure blind, scaffolded, compile-only, warm-start, same-AST return, repaired, refit, and perturbed-basin rows into one denominator.

### Recovery Means Verifier-Gated Claim Status

**Sources:** `benchmark.execute_benchmark_run()`, `benchmark._extract_run_metrics()`, `campaign._run_csv_row()`

**Apply to:** scientific-law tables and claim package summaries.

Rows should cite `claim_status`, `compiled_eml_verification.status`, `warm_start.status`, `repair_status`, and `refit_verifier_status`. Avoid declaring recovery from loss values or compile support alone.

### Proof Contracts Are Mostly Read-Only for Phase 53

**Sources:** `proof.threshold_policies()`, `proof.claim_matrix()`, `benchmark._counted_evidence_classes_for_claim()`

**Apply to:** any proof/claim logic.

Context explicitly says no threshold or denominator changes. Prefer paper-package claim docs over modifying proof contracts. If a new contract is unavoidable, add tests in `tests/test_proof_contract.py` and make the denominator/numerator scopes explicit.

### Artifact Provenance and Locks

**Sources:** `diagnostics._has_durable_artifact()`, `diagnostics._artifact_sha256()`, `proof_campaign._campaign_lock()`

**Apply to:** `artifacts/paper/v1.9/*`.

Each claim package should cite source aggregate/run artifacts by path and hash. Lock campaign outputs, aggregate outputs, reports, and tables.

### Centered-Family Negative Evidence Caveat

**Sources:** `family_triage.py`, `witnesses.py`, existing `artifacts/paper/v1.8/completeness-boundary.md`.

**Apply to:** RHY-04 claim boundaries and docs.

Frame centered-family evidence as negative diagnostic evidence. If unsupported rows are due to missing same-family warm-start witnesses or target witnesses, state that as an integration/witness caveat, not as proof that centered-family EML cannot represent the law.

### Docs Are Artifact-Backed

**Sources:** `README.md`, `docs/IMPLEMENTATION.md`

**Apply to:** RHY-05 docs updates.

Update docs only after successful artifacts exist. Use exact artifact paths and conservative wording. Mention blind discovery limits, exact compiler warm-start/same-AST status, repair-only evidence, and separate proof/campaign denominators.

## Existing Evidence Inputs to Consume

| Evidence | Artifact Path | Notes |
|----------|---------------|-------|
| v1.6 proof campaign | `artifacts/proof/v1.6/` | Bounded proof claims, measured shallow blind boundaries, perturbed basin reports. |
| v1.8 paper decision | `artifacts/paper/v1.8/` | Raw searchability note and centered-family negative diagnostic framing. |
| v1.8 family campaigns | `artifacts/campaigns/v1.8-family-smoke-triage/`, `artifacts/campaigns/v1.8-family-calibration/` | Centered-family diagnostics and caveats. |
| Arrhenius v1.9 evidence | `artifacts/campaigns/v1.9-arrhenius-evidence/v1.9-arrhenius-evidence/` | Exact compiler warm-start/same-AST evidence for normalized `exp(-0.8/x)`. |
| Michaelis v1.9 evidence | `artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/` | Exact compiler warm-start/same-AST evidence for normalized `2*x/(x + 0.5)`. |
| Repair v1.9 evidence | `artifacts/campaigns/v1.9-repair-evidence/v1.9-repair-evidence/` and `artifacts/campaigns/v1.9-repair-evidence/repair-evidence-summary.*` | Repair-only no-improvement evidence; keep separate from recovered rows. |

## Likely File Ownership

| Concern | Owner | Notes |
|---------|-------|-------|
| Built-in raw-hybrid suite membership | `benchmark.py` | Add only if Phase 53 needs a runnable suite. Keep per-case tags and expectations local to `_case()` definitions. |
| Campaign preset and single-suite report/table outputs | `campaign.py` | Add `raw-hybrid-paper` preset and scientific-law table writer here if the table belongs to one campaign aggregate. |
| Multi-artifact paper package | `paper_decision.py` or new `raw_hybrid_paper.py` | Use `paper_decision.py` for claim docs; use a new module only if orchestration grows beyond a decision memo. |
| Proof thresholds and claim IDs | `proof.py` | Prefer no edits. Existing contracts already separate measured blind, scaffolded, perturbed, and context claims. |
| Beer-Lambert basin boundary and durable artifact hashing | `diagnostics.py` | Reuse path/hash conventions for cited artifacts. |
| Centered-family caveat | `family_triage.py`, `witnesses.py` | Consume existing reason codes and caveat wording. |
| CLI exposure | `cli.py` | Add a subcommand only if a package writer/orchestrator is added. |
| README and implementation docs | `README.md`, `docs/IMPLEMENTATION.md` | Update after successful artifact generation only. |

## No Analog Found

No target file is without a usable analog. The weakest match is the dedicated scientific-law table: no exact table currently exists, but `campaign.write_campaign_tables()`, `_RUN_COLUMNS`, `_run_csv_row()`, and operator-family table writers provide a close role-match.

## Metadata

**Analog search scope:** `src/eml_symbolic_regression/`, `tests/`, `README.md`, `docs/`, `artifacts/`, `.planning/phases/50-*`, `.planning/phases/51-*`, `.planning/phases/52-*`.

**Files scanned:** 26 source/test/doc/artifact/planning files plus focused artifact directories.

**Pattern extraction date:** 2026-04-17
