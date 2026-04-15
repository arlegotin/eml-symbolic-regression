# Implementation Notes

## Architecture

The package follows the roadmap in `.planning/ROADMAP.md`:

1. `semantics.py` defines canonical and training-mode EML behavior.
2. `expression.py` defines exact ASTs and non-EML catalog candidates used by showcase demos.
3. `master_tree.py` defines complete depth-bounded soft EML trees.
4. `optimize.py` turns a soft tree into snapped candidates.
5. `verify.py` owns recovery status.
6. `cleanup.py` exports readable SymPy expressions and records cleanup reports.
7. `compiler.py` compiles a whitelisted SymPy subset into the existing exact EML `Expr` AST.
8. `master_tree.py` also supports literal-constant terminal banks and AST-to-logit embedding.
9. `warm_start.py` embeds compiled ASTs, records deterministic perturbation metadata, trains through `fit_eml_tree()`, and classifies the post-snap outcome.
10. `benchmark.py` defines repeatable benchmark suites, run execution, per-run artifacts, aggregate evidence reports, and recovery/failure taxonomy.
11. `datasets.py` and `cli.py` expose the demo ladder from `sources/FOR_DEMO.md`.

## Recovery Contract

Training loss is not enough. A candidate is only `recovered` when:

- it is an exact EML AST,
- it is evaluated after snapping,
- train, held-out, extrapolation, and mpmath checks pass,
- the verifier emits `recovered`.

Non-EML catalog formulas can pass as `verified_showcase`; those reports are useful for demos and verifier coverage, but they are not labeled as EML recovery.

Compiler output is also not enough by itself. A compiled seed can verify as an exact EML AST, but public demo promotion requires the warm-start path to train, snap, and verify the final exact AST. The optimizer manifest remains a candidate-generation artifact and never assigns `recovered`.

## Compiler Contract

The compiler accepts a deliberately narrow SymPy subset:

- variables from an explicit allow-list,
- finite constants under either `basis_only` or `literal_constants`,
- `exp` and principal-branch `log`,
- addition, subtraction, multiplication, division/reciprocal, and small integer powers through tested EML templates.

Unsupported functions, unknown variables, unsafe constants, excessive powers, and depth/node budget excesses raise `UnsupportedExpression` with a machine-readable reason code. Every compiled result includes source expression, normalized expression, variables, constants, assumptions, rule trace, depth, and node count.

`literal_constants` means fixed coefficients such as `-0.8`, `0.5`, and `2` are inserted as terminal constants and reported as such. It is not a pure `{1, eml}` synthesis claim.

## Warm Starts

`SoftEMLTree(depth, variables, constants)` defaults to the original pure terminal bank `(1,)`. When a compiled formula uses literal constants, the same finite constant catalog must be supplied to the soft tree. Embedding maps each exact AST slot to a logit choice and immediately snaps back to prove the seed is representable before perturbation.

`fit_warm_started_eml_tree()` then:

1. embeds the compiled AST,
2. records the terminal bank and assignments,
3. applies deterministic logit perturbation,
4. trains through the existing Adam optimizer,
5. snaps the final model,
6. delegates recovery status to `verify_candidate()`.

Warm-start outcomes are separated as `same_ast_return`, `verified_equivalent_ast`, `snapped_but_failed`, `soft_fit_only`, or `failed`.

## Benchmark Evidence Contract

Benchmark suites use schema `eml.benchmark_suite.v1`. A suite expands cases into deterministic runs using formula ID, start mode, seed, perturbation noise, dataset config, optimizer budget, and artifact root. Run IDs are hash-stabilized from that canonical identity, so repeated expansion produces the same artifact paths.

Built-in suites:

- `smoke`: one blind run, one warm-start run, and one unsupported/stretch diagnostic for CI-scale coverage.
- `v1.2-evidence`: shallow blind baselines, Beer-Lambert perturbation sweep, Michaelis-Menten warm-start diagnostics, and Planck stretch diagnostics.
- `for-demo-diagnostics`: selected `sources/FOR_DEMO.md` formulas, including unsupported/stretch formulas as evidence rather than hidden failures.

Each run writes schema `eml.benchmark_run.v1` with:

- run identity and artifact path,
- dataset and optimizer configuration,
- start mode, seed, perturbation noise, and tags,
- stage statuses,
- normalized metrics such as best loss, post-snap loss, snap margin, active slot changes, verifier status, and high-precision error when available,
- timing and environment provenance,
- structured errors for unsupported or failed execution paths.

Aggregate reports use schema `eml.benchmark_aggregate.v1` and are written as both JSON and Markdown. Recovery rates are grouped by formula, start mode, perturbation level, depth, and seed group. `claim_status == "recovered"` is the only source of verifier-owned recovery counts.

The taxonomy intentionally separates:

- `blind_recovery`
- `same_ast_warm_start_return`
- `verified_equivalent_warm_start_recovery`
- `snapped_but_failed`
- `soft_fit_only`
- `unsupported`
- `execution_failure`

This prevents a same-AST return or low training loss from being read as blind symbolic discovery.

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
- `planck`

`exp` and `log` are exact EML candidates. The remaining demos are catalog showcase formulas with verifier reports, ready for future EML warm-start/curriculum work.

Beer-Lambert now has a compiler-driven warm-start path:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli demo beer_lambert --warm-start-eml
```

At the default gates, Michaelis-Menten and Planck remain honest stretch reports: their catalog formulas verify, but their compiler/warm-start stages report unsupported depth instead of promotion.
