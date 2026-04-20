# Implementation Notes

## Architecture

The package follows the roadmap in `.planning/ROADMAP.md`:

1. `semantics.py` defines canonical and training-mode EML behavior.
2. `expression.py` defines exact ASTs and non-EML catalog candidates used by showcase demos.
3. `master_tree.py` defines complete depth-bounded soft EML trees.
4. `optimize.py` turns a soft tree into an exact-candidate pool, preserves the legacy final snap, and selects the shipped exact tree from that pool.
5. `verify.py` owns recovery status.
6. `repair.py` runs bounded target-free snap-neighborhood cleanup and the older perturbed-basin target-aware repair path.
7. `cleanup.py` exports readable SymPy expressions and records cleanup reports.
8. `compiler.py` compiles a whitelisted SymPy subset into the existing exact EML `Expr` AST.
9. `master_tree.py` also supports literal-constant terminal banks, AST-to-logit embedding, replayable slot alternatives, and exact neighborhood expansion helpers.
10. `warm_start.py` embeds compiled ASTs, records deterministic perturbation metadata, trains through `fit_eml_tree()`, and classifies the post-snap outcome.
11. `benchmark.py` defines repeatable benchmark suites, run execution, post-snap constant refit, per-run artifacts, aggregate evidence reports, and recovery/failure taxonomy.
12. `campaign.py` defines campaign presets, guarded output folders, CSV exports, SVG figures, and `report.md` assembly.
13. `datasets.py` and `cli.py` expose the demo ladder from `sources/FOR_DEMO.md`.

## Recovery Contract

Training loss is not enough. The optimizer now emits a retained exact-candidate pool across restarts plus late hardening checkpoints, but a candidate is only `recovered` when:

- it is an exact EML AST,
- it is evaluated after snapping,
- train, held-out, extrapolation, and mpmath checks pass,
- the verifier emits `recovered`.

Non-EML catalog formulas can pass as `verified_showcase`; those reports are useful for demos and verifier coverage, but they are not labeled as EML recovery.

Compiler output is also not enough by itself. A compiled seed can verify as an exact EML AST, but public demo promotion requires the warm-start path to train, harden, snap, and verify the final exact AST. The optimizer manifest remains a candidate-generation artifact and never assigns `recovered`; verifier-owned ranking decides which exact candidate wins when evaluation splits are available.

If that selected exact candidate still fails, benchmark flows can now run a bounded target-free cleanup stage over serialized low-margin slot alternatives. Cleanup never overwrites the original selected candidate in place; it records attempted edits and only promotes a repaired candidate when verifier-owned ranking improves.

Selected-only cleanup remains the default direct repair behavior. Benchmark cases can opt into `expanded_candidate_pool` cleanup when they need focused repair evidence over selected, fallback, and retained exact-candidate roots. Expanded cleanup deduplicates candidate roots and candidate variants by serialized exact AST before verifier work, keeps the original optimizer selected and fallback manifests intact, and accepts a repair only when the verifier reports a recovered candidate. Accepted repairs are reported as `repaired_candidate` evidence only; they are not blind discovery, compile-only evidence, same-AST warm-start evidence, or perturbed true-tree recovery.

If the resulting exact candidate contains literal constants beyond the canonical `1` basis, benchmark flows can also run a frozen-structure post-snap refit stage. Refit exposes those literal leaves by stable AST path, keeps originally real constants on the real axis, records both pre-refit and post-refit exact candidates, and only promotes the refit candidate when verifier-owned ranking improves or matches the preserved fallback.

## Compiler Contract

The compiler accepts a deliberately narrow SymPy subset:

- variables from an explicit allow-list,
- finite constants under either `basis_only` or `literal_constants`,
- `exp` and principal-branch `log`,
- addition, subtraction, multiplication, division/reciprocal, and small integer powers through tested EML templates.

Unsupported functions, unknown variables, unsafe constants, excessive powers, and depth/node budget excesses raise `UnsupportedExpression` with a machine-readable reason code. Every compiled result includes source expression, normalized expression, variables, constants, assumptions, rule trace, depth, and node count.

`literal_constants` means fixed coefficients such as `-0.8`, `0.5`, and `2` are inserted as terminal constants and reported as such. It is not a pure `{1, eml}` synthesis claim.

The compiler now routes supported shortcuts through an explicit macro layer. Current macro rules are `scaled_exp_minus_one_template` for Shockley-style `scale * (exp(a) - 1)` shapes, `direct_division_template` for true numerator-over-denominator motifs and Arrhenius reciprocal-temperature exponents, `reciprocal_shift_template` for reciprocal shifts such as `1/(x+b)`, and `saturation_ratio_template` for saturation ratios such as `c*x/(x+b)`. Compiler metadata records macro hits, misses, and the depth/node delta against a no-macro baseline so a shortcut can be audited instead of hidden behind an ad hoc branch.

## Warm Starts

`SoftEMLTree(depth, variables, constants)` defaults to the original pure terminal bank `(1,)`. When a compiled formula uses literal constants, the same finite constant catalog must be supplied to the soft tree. Embedding maps each exact AST slot to a logit choice and immediately snaps back to prove the seed is representable before perturbation.

`fit_warm_started_eml_tree()` then:

1. embeds the compiled AST,
2. records the terminal bank and assignments,
3. applies deterministic logit perturbation,
4. trains through the existing Adam optimizer,
5. emits a retained exact-candidate pool from the legacy final snap plus late hardening checkpoints,
6. serializes replayable low-margin slot alternatives for the selected exact candidate,
7. delegates recovery status to `verify_candidate()`.

Warm-start outcomes are separated as `same_ast_return`, `verified_equivalent_ast`, `snapped_but_failed`, `soft_fit_only`, or `failed`.

## Benchmark Evidence Contract

Benchmark suites use schema `eml.benchmark_suite.v1`. A suite expands cases into deterministic runs using formula ID, start mode, seed, perturbation noise, dataset config, optimizer budget, and artifact root. Run IDs are hash-stabilized from that canonical identity, so repeated expansion produces the same artifact paths.

Built-in suites:

- `smoke`: one blind run, one warm-start run, and one unsupported/stretch diagnostic for CI-scale coverage.
- `v1.2-evidence`: shallow blind baselines, Beer-Lambert perturbation sweep, Michaelis-Menten warm-start diagnostics, and Planck stretch diagnostics.
- `for-demo-diagnostics`: selected `sources/FOR_DEMO.md` formulas, including unsupported/stretch formulas as evidence rather than hidden failures.
- `v1.3-standard`: the default campaign matrix with shallow blind baselines, Beer-Lambert perturbations, Michaelis-Menten, Planck, and selected FOR_DEMO diagnostics.
- `v1.3-showcase`: an expanded campaign matrix with more seeds, more Beer-Lambert perturbation levels, and full FOR_DEMO diagnostics.
- `v1.9-arrhenius-evidence`: a single focused `arrhenius-warm` run for normalized Arrhenius exact compiler warm-start evidence.
- `v1.9-michaelis-evidence`: a single focused `michaelis-warm` run for normalized Michaelis-Menten exact compiler warm-start / same-AST evidence.
- `v1.9-repair-evidence`: focused near-miss default-vs-expanded cleanup pairs for repair-only evidence with no proof threshold policy.
- `v1.13-paper-basis-only`: every publication target under the paper-faithful `{1, eml, variables}` basis-only compiler policy.
- `v1.13-paper-literal-constants`: every publication target under the applied literal-constant policy with declared literal catalogs and warm-start rows.
- `v1.13-paper-tracks`: combined basis-only and literal-constant rows with aggregate denominators kept separate.

Each run writes schema `eml.benchmark_run.v1` with:

- run identity and artifact path,
- dataset and optimizer configuration,
- benchmark track metadata, including constants policy, literal catalog, and scaffold initializer status,
- start mode, seed, perturbation noise, and tags,
- stage statuses,
- normalized metrics such as best loss, post-snap loss, snap margin, active slot changes, verifier status, repair status, repair variant count, and high-precision error when available,
- timing and environment provenance,
- structured errors for unsupported or failed execution paths.

When a blind, warm-start, or perturbed-basin exact candidate fails verification, the run artifact can now include a `repair` section with attempted slot or subtree edits, their margins/probability gaps, accepted moves, and the repaired verifier report if cleanup wins. The original selected and fallback candidates from the optimizer manifest remain intact for weak-dominance comparisons.

The Phase 52 repair evidence command is:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark v1.9-repair-evidence --output-dir artifacts/campaigns/v1.9-repair-evidence
```

The generated repair evidence root is `artifacts/campaigns/v1.9-repair-evidence/v1.9-repair-evidence/`. The validated pair summary is `artifacts/campaigns/v1.9-repair-evidence/repair-evidence-summary.json`, with a readable companion at `artifacts/campaigns/v1.9-repair-evidence/repair-evidence-summary.md`. The committed run measured 2 default-vs-expanded pairs: default selected-only cleanup repaired 0, expanded candidate-pool cleanup repaired 0, expanded cleanup produced 0 improvements, final status regressed in 0 pairs, and selected/fallback optimizer manifests were preserved for all runs. This no-improvement result is still valid repair evidence because fallback preservation and verifier-owned taxonomy were checked.

Run artifacts can also include a `refit` section. That section records:

- the pre-refit exact candidate and its verifier-owned metrics,
- the post-refit exact candidate with updated literal coefficients,
- the constant-path diff for every refittable literal,
- the final anomaly summary from refit optimization,
- and the accept/reject decision against the preserved fallback candidate.

Training anomaly summaries now distinguish `exp` clamp counts from `exp` overflow pressure, and they separately record `log` small-magnitude inputs, non-positive-real inputs, branch-cut hits, non-finite log inputs, and any training-only log-safety penalty that was applied. Optimizer manifests also include a `semantics_alignment` section. It states whether the objective used `faithful` verifier-matching semantics or default `guarded` training semantics, records the guarded fallback reason when applicable, summarizes anomaly totals, and surfaces post-snap verifier and certificate status fields for publication audits.

Aggregate reports use schema `eml.benchmark_aggregate.v1` and are written as both JSON and Markdown. Recovery rates are grouped by formula, start mode, benchmark track, constants policy, perturbation level, depth, and seed group. Mixed-track suites also include a top-level `tracks` denominator table so basis-only and literal-constant rows cannot share a recovery denominator. `claim_status == "recovered"` is the only source of verifier-owned recovery counts.

The v1.13 track contract is:

- `basis_only`: compiler policy `basis_only`, no non-1 terminal constants, and no silent fallback to literal constants. Literal-coefficient formulas may be unsupported in this track; that unsupported row remains part of the basis-only denominator.
- `literal_constants`: compiler policy `literal_constants`, a declared literal catalog in `benchmark_track.literal_catalog`, and explicit scaffold initializer status in `benchmark_track.scaffold_status`. These rows are applied convenience evidence, not bare `{1, eml, variables}` synthesis.

The taxonomy intentionally separates:

- `blind_recovery`
- `same_ast_warm_start_return`
- `verified_equivalent_warm_start_recovery`
- `repaired_candidate`
- `snapped_but_failed`
- `soft_fit_only`
- `unsupported`
- `execution_failure`

This prevents a same-AST return, repaired candidate, or low training loss from being read as blind symbolic discovery.

The generated Arrhenius evidence root is `artifacts/campaigns/v1.9-arrhenius-evidence/v1.9-arrhenius-evidence/`. The suite `v1.9-arrhenius-evidence` contains case `arrhenius-warm`, demo id `arrhenius`, normalized formula `exp(-0.8/x)`, positive domains `(0.5, 3.0)`, `(0.6, 2.7)`, and `(3.1, 4.2)`, macro hit `direct_division_template`, warm-start status `same_ast_return`, verifier status `recovered`, and evidence class `same_ast`. This is exact compiler warm-start / same-AST basin evidence, not blind discovery.

The generated Michaelis-Menten evidence root is `artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/`. The suite `v1.9-michaelis-evidence` contains case `michaelis-warm`, demo id `michaelis_menten`, normalized formula `2*x/(x+0.5)`, domains `(0.05, 5.0)`, `(0.08, 4.5)`, and `(5.1, 7.0)`, macro hit `saturation_ratio_template`, compile depth `12`, node count `41`, warm-start status `same_ast_return`, verifier status `recovered`, and evidence class `same_ast`. This is exact compiler warm-start / same-AST basin evidence, not blind discovery.

## Raw-Hybrid Paper Package Contract

`src/eml_symbolic_regression/raw_hybrid_paper.py` is a synthesis-only package writer. The CLI command is:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli raw-hybrid-paper --output-dir artifacts/paper/v1.9/raw-hybrid --require-existing
```

The command validates declared source artifacts, refuses a non-empty output directory unless `--overwrite` is passed, and does not run training, benchmarks, campaigns, proof campaigns, or paper-decision generation. Its source locks hash specific files, not directories, and write source id, role, path, required flag, and SHA-256 into `artifacts/paper/v1.9/raw-hybrid/source-locks.json`.

The generated package root is `artifacts/paper/v1.9/raw-hybrid/`. It contains:

- `manifest.json`: schema `eml.raw_hybrid_paper.v1`, preset `v1.9-raw-hybrid-paper`, reproduction command, output paths, source list, regime counts, and scientific-law row count.
- `source-locks.json`: file-level evidence locks for v1.6 proof aggregates, v1.8 centered-family decision artifacts, v1.9 Arrhenius/Michaelis/repair evidence, and v1.6 Beer-Lambert/Shockley/Planck/logistic diagnostics.
- `regime-summary.json`: separate `pure_blind`, `scaffolded`, `compile_only`, `warm_start`, `same_ast_return`, `repaired`, `refit`, and `perturbed_basin` buckets.
- `raw-hybrid-report.md`: human-readable report with the same regime separation.
- `scientific-law-table.json`, `scientific-law-table.csv`, and `scientific-law-table.md`: rows for Beer-Lambert, Shockley, Arrhenius, Michaelis-Menten, Planck diagnostic, logistic diagnostic, and historical Michaelis context.
- `claim-boundaries.md`: explicit boundaries stating that warm-start, same-AST, scaffolded, repaired, refit, compile-only, and perturbed-basin evidence is not blind discovery.
- `centered-negative-diagnostics.md`: centered-family negative diagnostic evidence with the same-family witness caveat.

The `scientific-law-table` columns are `law`, `formula`, `compile_support`, `compile_depth`, `macro_hits`, `warm_start_status`, `verifier_status`, `evidence_regime`, and `artifact_path`. Beer-Lambert, Shockley, Arrhenius, and Michaelis-Menten are supported same-AST warm-start diagnostics. Arrhenius and Michaelis-Menten remain exact compiler warm-start / same-AST evidence, not blind discovery. Planck and logistic are unsupported/stretch compile diagnostics, not solved rows.

The package deliberately reports centered-family material only as negative diagnostics under missing same-family witnesses. It does not claim centered-family impossibility.

## v1.13 Publication Rebuild Contract

Phase 69 adds a clean-room publication rebuild entrypoint:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli publication-rebuild --output-dir artifacts/paper/v1.13 --smoke --overwrite
```

The `--smoke` mode is a fast package-shape and provenance check. It writes a v1.13 publication root with `manifest.json`, `source-locks.json`, `reproduction.md`, `validation.json`, and `validation.md`. The full publication evidence campaign is not claimed by Phase 69 alone; the final full rebuild, claim audit, and release gate belong to the later publication rebuild/release phase.

The publication manifest uses schema `eml.v113_publication_rebuild.v1` and records:

- the exact reproduction command;
- `generated_at`;
- git revision, branch, dirty-state, and short status;
- Python/platform identity;
- `requirements-lock.txt` path and SHA-256 when present;
- `Dockerfile` path and SHA-256 when present;
- source input hashes;
- generated output hashes;
- validation status and validation artifact paths.

`requirements-lock.txt` captures the committed Python dependency set used by the local publication smoke path. `Dockerfile` installs that lockfile, copies the package sources, sets `PYTHONPATH=src`, and runs the same `publication-rebuild` command as its default command. The container path is support infrastructure for reproducibility; normal local tests do not require Docker.

Publication validation rejects placeholder metadata such as `1970-01-01T00:00:00+00:00` and `"snapshot"` outside explicitly allowed deterministic-test fixtures. Stable snapshot constants may still exist for deterministic tests, but publication manifests must not silently promote those placeholders as real provenance.

## Campaign Report Contract

Campaign presets are the showcase layer over benchmark suites:

- `smoke` maps to the smoke suite and is intended for CI and quick sanity checks.
- `standard` maps to `v1.3-standard` and is the default reportable campaign.
- `showcase` maps to `v1.3-showcase` and makes the larger budget explicit.

Campaign output is rooted at `artifacts/campaigns/<label-or-timestamp>/`. Stable labels are guarded: if a folder already exists, the command fails unless `--overwrite` is passed. A successful campaign writes:

- `campaign-manifest.json` with preset metadata, filters, command, code version, environment, and output paths.
- `suite-result.json`, `aggregate.json`, and `aggregate.md`.
- `runs/<suite-id>/*.json` raw artifacts.
- `tables/runs.csv` with formula, start mode, seed, depth, steps, perturbation noise, losses, verifier status, recovery class, runtime, changed slots, reason, and artifact path.
- grouped CSVs by formula, start mode, perturbation noise, depth, and failure class.
- `tables/headline-metrics.json` and `.csv`.
- `tables/failures.csv` with reason codes and artifact links.
- deterministic SVG figures for recovery rates, loss comparison, Beer-Lambert perturbation behavior, runtime/depth/budget, and failure taxonomy.
- `report.md` with headline metrics, figure/table links, raw artifact links, exact reproduction command, strengths, limitations, failed/unsupported cases, and next experiments.

The report deliberately separates blind recovery from same-AST warm-start return, verified-equivalent warm-start recovery, unsupported gates, and failed fits. It is a reproducible evidence bundle, not a claim that arbitrary deep formulas are solved.

Benchmark suites can be rerun under a uniform semantics mode with `benchmark --semantics-mode guarded` or `benchmark --semantics-mode faithful`. The default `guarded` mode preserves existing run IDs; `faithful` mode produces distinct run IDs so clamp/log-guard ablations can be compared without overwriting guarded evidence.

## Paper-Grounded Fixtures

The test suite includes the two identities most important for the MVP:

```text
exp(x) = eml(x, 1)
ln(x) = eml(1, eml(eml(1, x), 1))
```

It also checks the paper's univariate parameter count for complete master trees:

```text
P(n) = 5 * 2^n - 6
```

## Demo Ladder

The built-in demos mirror `sources/FOR_DEMO.md`:

- `exp`
- `log`
- `beer_lambert`
- `radioactive_decay`
- `michaelis_menten`
- `logistic`
- `shockley`
- `damped_oscillator`
- `arrhenius`
- `planck`

`exp` and `log` are exact EML candidates. The remaining demos are catalog showcase formulas with verifier reports, with selected formulas promoted only when exact compiler warm-start evidence or another verifier-owned exact EML path exists.

Beer-Lambert, Shockley, normalized Arrhenius, and normalized Michaelis-Menten now have compiler-driven warm-start paths:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli demo beer_lambert --warm-start-eml
PYTHONPATH=src python -m eml_symbolic_regression.cli demo shockley --warm-start-eml --points 24
PYTHONPATH=src python -m eml_symbolic_regression.cli demo arrhenius --warm-start-eml --points 24 --output artifacts/arrhenius-warm-report.json
PYTHONPATH=src python -m eml_symbolic_regression.cli demo michaelis_menten --warm-start-eml --points 24 --output artifacts/michaelis-warm-report.json
```

Arrhenius uses normalized dimensionless input `x` and formula `exp(-0.8/x)`. Its focused benchmark command is:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark v1.9-arrhenius-evidence --case arrhenius-warm --seed 0 --perturbation-noise 0.0 --output-dir artifacts/campaigns/v1.9-arrhenius-evidence
```

Michaelis-Menten uses normalized dimensionless input `x` and formula `2*x/(x+0.5)`. Its focused benchmark command is:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark v1.9-michaelis-evidence --case michaelis-warm --seed 0 --perturbation-noise 0.0 --output-dir artifacts/campaigns/v1.9-michaelis-evidence
```

At the default gates, Planck remains an honest stretch report: its catalog formula verifies, the relaxed compiler diagnostics show the macro-shortened exact tree, but the shipped compile/warm-start stage still reports unsupported depth instead of promotion. Michaelis-Menten is promoted only by the strict same-AST warm-start evidence above, not as blind discovery.
