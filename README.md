# EML Symbolic Regression

This repo implements a practical MVP of the paper-grounded idea in `sources/NORTH_STAR.md`: a hybrid symbolic-regression engine over complete EML trees.

The EML operator is:

```text
eml(x, y) = exp(x) - log(y)
```

The paper shows that EML plus the constant `1` can generate the scientific-calculator elementary-function basis, and that formulas can be represented as regular binary EML trees. This implementation turns that into a Python/PyTorch package with exact ASTs, soft master trees, snapping, verification, cleanup, and demos.

## What Is Implemented

- Canonical and training-mode EML semantics.
- Exact immutable EML AST nodes with deterministic JSON serialization.
- Paper identities for `exp(x)` and `ln(x)`.
- Complete depth-bounded soft EML master trees with PyTorch `complex128` gates.
- Adam-based candidate generation with restarts, annealing, entropy/size penalties, snapping, and manifests.
- Verifier-owned recovery status over train, held-out, extrapolation, and mpmath point checks.
- SymPy export and targeted cleanup/report helpers.
- A fail-closed SymPy subset compiler that emits exact EML ASTs with metadata, rule traces, assumptions, literal-constant provenance, and independent validation against ordinary SymPy evaluation.
- Constant-catalog soft master trees plus exact AST embedding with embed-to-snap round-trip checks.
- Compiler-driven warm-start training reports that perturb, train, snap, and verify through the existing optimizer/verifier boundary.
- Repeatable benchmark suites with per-run artifacts, aggregate JSON/Markdown reports, recovery-rate grouping, and explicit failure/unsupported taxonomy.
- Benchmark campaign presets that generate raw artifacts, aggregate evidence, tidy CSV tables, static SVG figures, and a self-contained `report.md`.
- Demo specs from `sources/FOR_DEMO.md`.
- CLI commands for paper checks, demo reports, benchmark evidence runs, and campaign reports.
- Pytest coverage for the MVP pipeline.

The implementation is intentionally honest about scope: exact EML recovery is demonstrated for paper-grounded shallow formulas, for Beer-Lambert via a compiler-generated warm start, and for normalized Arrhenius and Michaelis-Menten as exact compiler warm-start / same-AST basin evidence. Harder showcase demos remain verified catalog candidates or explicit unsupported/depth reports unless a trained exact EML candidate passes the verifier.

Verifier-gated cleanup can also produce repair evidence for failed exact candidates. Those repairs are classified as `repaired_candidate` only; they are not blind discovery, not compile-only evidence, not same-AST warm-start evidence, and not perturbed true-tree recovery.

## Quick Commands

Run the paper identity checks:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli verify-paper
```

List demo targets:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli list-demos
```

Write a demo report:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli demo planck --output artifacts/planck-report.json
```

Compile a supported demo formula into EML and validate it:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli demo beer_lambert --compile-eml --output artifacts/beer-compile-report.json
```

Run the compiler warm-start recovery path:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli demo beer_lambert --warm-start-eml --output artifacts/beer-lambert-warm-report.json
```

Run the normalized Arrhenius exact warm-start report:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli demo arrhenius --warm-start-eml --points 24 --output artifacts/arrhenius-warm-report.json
```

Run the normalized Michaelis-Menten exact warm-start report:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli demo michaelis_menten --warm-start-eml --points 24 --output artifacts/michaelis-warm-report.json
```

List benchmark suites:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli list-benchmarks
```

Run the CI-scale benchmark smoke suite:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark smoke --output-dir artifacts/benchmarks
```

Run a filtered evidence subset:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark v1.2-evidence --case beer-perturbation-sweep --seed 0 --output-dir artifacts/benchmarks
```

Reproduce the focused Arrhenius evidence artifact:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark v1.9-arrhenius-evidence --case arrhenius-warm --seed 0 --perturbation-noise 0.0 --output-dir artifacts/campaigns/v1.9-arrhenius-evidence
```

Reproduce the focused Michaelis-Menten evidence artifact:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark v1.9-michaelis-evidence --case michaelis-warm --seed 0 --perturbation-noise 0.0 --output-dir artifacts/campaigns/v1.9-michaelis-evidence
```

Reproduce the focused repair evidence artifacts:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark v1.9-repair-evidence --output-dir artifacts/campaigns/v1.9-repair-evidence
```

List campaign presets:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli list-campaigns
```

Generate a full campaign folder with CSVs, figures, and `report.md`:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli campaign smoke --output-root artifacts/campaigns
```

Generate the measured depth-curve proof campaign:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli campaign proof-depth-curve --output-root artifacts/campaigns
```

Generate the full current proof bundle and claim report:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli proof-campaign --output-root artifacts/proof/v1.6 --overwrite
```

Reproduce the committed v1.3 smoke report:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli campaign smoke --output-root artifacts/campaigns --label v1.3-smoke --overwrite
```

Compare archived baseline campaigns against candidate campaigns (example: v1.3 versus v1.4):

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli diagnostics compare --baseline artifacts/campaigns/v1.3-standard --candidate artifacts/campaigns/v1.4-standard --baseline artifacts/campaigns/v1.3-showcase --candidate artifacts/campaigns/v1.4-showcase --output-dir artifacts/campaigns/comparison-v1.3-v1.4
```

Try soft EML training on a shallow demo:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli demo exp --train-eml --depth 1 --steps 80 --restarts 2 --output artifacts/exp-trained.json
```

Run tests:

```bash
python -m pytest
```

## Demo Statuses

- `recovered`: an exact EML AST passed verifier checks.
- `verified_showcase`: a non-EML catalog formula from the demo spec passed verifier checks. This is useful for testing data, verification, cleanup, and reports, but it is not presented as EML discovery.
- `failed`: verifier checks failed; the report includes a reason code.
- `compiled_seed`: the source formula compiled to an exact EML AST and that AST verified numerically. This is a seed/provenance stage, not a trained recovery claim by itself.
- `warm_start_attempt`: the compiler seed was embedded into a compatible soft tree, optionally perturbed, trained through the existing optimizer, snapped, and classified.
- `trained_exact_recovery`: the post-training snapped exact EML AST passed the verifier. Demo reports promote top-level `claim_status` to `recovered` only at this stage.
- `unsupported`: the compiler or warm-start gate failed closed, usually because an operator, constant policy, depth, node budget, or warm-start depth limit was exceeded.

## Benchmark Evidence

Benchmark runs use the built-in suites `smoke`, `v1.2-evidence`, `for-demo-diagnostics`, and focused evidence suites such as `v1.9-arrhenius-evidence`, `v1.9-michaelis-evidence`, and `v1.9-repair-evidence`, or a custom JSON suite with schema `eml.benchmark_suite.v1`. Each expanded run writes a JSON artifact containing the suite/run identity, formula, start mode, seed, perturbation, optimizer config, stage statuses, normalized losses/snap metrics when training ran, verifier status, timing, and errors.

The CLI also writes:

- `suite-result.json`: all run payloads for the command.
- `aggregate.json`: grouped recovery/failure counts.
- `aggregate.md`: a compact human-readable report.

Interpretation rules:

- `verifier_recovered` means the snapped exact candidate passed the verifier.
- `same_ast_return` means a warm-started run snapped back to the compiled seed; this is useful basin-stability evidence, not blind discovery.
- `verified_equivalent_ast` means a warm-started run snapped to a different exact AST that still verified.
- `repaired_candidate` means verifier-gated cleanup found and verified a repair candidate; it is repair evidence, not blind discovery, compile-only evidence, same-AST warm-start evidence, or perturbed true-tree recovery.
- `unsupported` and failed cases are kept in the denominator; they are part of the evidence.
- `verifier_recovery_rate` is computed from verifier-owned recovery, not from training loss.

The focused Arrhenius artifact is rooted at `artifacts/campaigns/v1.9-arrhenius-evidence/v1.9-arrhenius-evidence/`. It contains suite `v1.9-arrhenius-evidence` case `arrhenius-warm` for demo id `arrhenius`, normalized formula `exp(-0.8/x)`, domains `(0.5, 3.0)`, `(0.6, 2.7)`, and `(3.1, 4.2)`, compiler macro `direct_division_template`, warm-start status `same_ast_return`, verifier status `recovered`, and evidence class `same_ast`. This is exact compiler warm-start / same-AST basin evidence, not blind discovery.

The focused Michaelis-Menten artifact is rooted at `artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/`. It contains suite `v1.9-michaelis-evidence` case `michaelis-warm` for demo id `michaelis_menten`, normalized formula `2*x/(x+0.5)`, domains `(0.05, 5.0)`, `(0.08, 4.5)`, and `(5.1, 7.0)`, compiler macro `saturation_ratio_template`, compile depth `12`, node count `41`, warm-start status `same_ast_return`, verifier status `recovered`, and evidence class `same_ast`. This is exact compiler warm-start / same-AST basin evidence, not blind discovery.

The focused repair evidence root is `artifacts/campaigns/v1.9-repair-evidence/v1.9-repair-evidence/`. It contains suite `v1.9-repair-evidence` with paired default selected-only cleanup and `expanded_candidate_pool` cleanup runs for radioactive-decay blind and Beer-Lambert warm-start near misses. The validated summaries are `artifacts/campaigns/v1.9-repair-evidence/repair-evidence-summary.json` and `artifacts/campaigns/v1.9-repair-evidence/repair-evidence-summary.md`. The committed run measured 2 pairs, 0 default repairs, 0 expanded repairs, 0 expanded improvements, 0 final-status regressions, and preserved selected/fallback optimizer manifests for every run. Expanded candidate-pool cleanup therefore produced no measured improvement in this focused suite, but it preserved fallback behavior and stayed in repair-only taxonomy.

## Campaign Reports

Campaigns are the presentation layer over benchmark suites. The built-in presets are:

- `smoke`: CI-scale run with one blind baseline, one warm-start recovery path, and one unsupported diagnostic.
- `standard`: default showcase matrix with shallow blind baselines, Beer-Lambert perturbation sweeps, Michaelis-Menten diagnostics, Planck diagnostics, and selected FOR_DEMO cases.
- `showcase`: expanded seeds and perturbation levels for presentation-grade evidence.
- `proof-shallow`: bounded scaffolded shallow proof suite.
- `proof-shallow-pure-blind`: measured pure-blind shallow proof suite with scaffold initializers disabled.
- `proof-basin`: bounded perturbed-basin proof suite.
- `proof-basin-probes`: visible Beer-Lambert high-noise probe rows outside the bounded basin denominator.
- `proof-depth-curve`: measured blind-vs-perturbed depth-curve suite over deterministic exact EML targets at depths 2 through 6.

Each campaign folder contains:

- `campaign-manifest.json`: preset, suite, filters, command, code version, and output paths.
- `suite-result.json`, `aggregate.json`, `aggregate.md`: raw suite and aggregate evidence.
- `runs/<suite>/`: per-run JSON artifacts.
- `tables/`: `runs.csv`, grouped recovery CSVs, `headline-metrics.json/.csv`, and `failures.csv`.
- `figures/`: deterministic SVG charts for recovery, losses, Beer-Lambert perturbations, runtime/budget, and failure taxonomy.
- `report.md`: self-contained evidence report with numbers, charts, limitations, next experiments, and the exact reproduction command.

The one-command proof bundle can be rooted at a milestone-specific path such as `artifacts/proof/v1.6/`. It aggregates the proof campaigns above, writes a combined `proof-report.md`, preserves the perturbed-basin bound report, records `anchor-locks.json` for archived comparison roots, and includes a guarded comparison section against the broader v1.4 campaign baselines without mixing denominators.

The committed smoke report is at `artifacts/campaigns/v1.3-smoke/report.md`. Current smoke metrics are intentionally modest: 3 runs total, 1 verifier recovery via same-AST warm start, 1 blind snapped-but-failed run, and 1 unsupported Planck depth gate.

## Limits

This repo does not promise blind recovery of arbitrary deep formulas. The paper reports that blind recovery degrades sharply with depth and that depth-6 blind recovery was not observed in the reported attempts. Warm-start success is a different claim: it shows return-to-solution from a compiler-provided scaffold, with fixed literal constants when the source formula contains coefficients.

The default compiler/warm-start gates intentionally keep Planck honest: its catalog formula verifies, but its compiled EML tree remains a stretch/unsupported report under the shipped warm-start promotion budget. Michaelis-Menten now has focused same-AST warm-start evidence under the strict v1.9 gate, but it is not a blind discovery claim.
