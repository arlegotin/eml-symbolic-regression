# Phase 49: Witness Registry and Centered Scaffold Correctness - Context

**Gathered:** 2026-04-17
**Status:** Ready for planning
**Mode:** Auto-selected defaults from `$gsd-autonomous`

<domain>
## Phase Boundary

Make scaffold and witness availability explicit by operator family, route benchmark and optimizer scaffold attempts through that availability contract, and prevent raw `exp`, `log`, and `scaled_exp` witnesses from being silently used under centered-family semantics.

</domain>

<decisions>
## Implementation Decisions

### Registry Contract
- Add an inspectable witness or initializer registry keyed by scaffold kind and operator family.
- Treat existing `exp`, `log`, and `scaled_exp` scaffold helpers as raw EML witnesses until a same-family centered witness is explicitly registered and tested.
- Keep raw EML defaults unchanged so existing shallow scaffolded and raw-hybrid evidence paths do not regress.
- Prefer fail-closed registry lookups over ad hoc conditionals at individual call sites.

### Centered Exclusion Semantics
- Centered `CEML_s`, `ZEML_s`, and continuation variants must drop raw scaffold attempts unless a same-family registry entry exists.
- Use the canonical reason code `centered_family_same_family_witness_missing` for scaffold exclusions in optimizer and benchmark artifacts.
- Preserve the existing `centered_family_same_family_seed_missing` reason for warm-start and perturbed-tree exact-seed gates.
- Tests should prove centered-family runs cannot directly reach raw scaffold helpers through benchmark budgets or optimizer attempt generation.

### Artifact and Test Coverage
- Benchmark budgets, run artifacts, aggregate metrics, and optimizer manifests should expose scaffold exclusions with operator-family context.
- Add focused tests near `tests/test_benchmark_contract.py`, `tests/test_benchmark_runner.py`, and optimizer cleanup/manifest coverage rather than broad campaign reruns.
- Existing v1.8 centered-family evidence should remain interpretable as negative diagnostic evidence with a corrected scaffold-confound boundary.
- Keep the implementation reusable for future same-family centered witnesses without enabling unsupported centered recovery by default.

### the agent's Discretion
Use the smallest registry shape that makes current scaffold availability auditable and blocks centered raw-witness contamination. Avoid formula-specific exceptions and avoid changing verifier-owned recovery semantics.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `OptimizerBudget` already carries `scaffold_initializers`, `scaffold_exclusions`, `operator_family`, and `operator_schedule`.
- `_operator_variant_budget` currently strips `scaled_exp` for non-raw family variants and records `scaled_exp:centered_family_incompatible_raw_witness`.
- `fit_eml_tree` centralizes scaffold attempt generation through `_training_attempts` and applies helpers through `_apply_scaffold`.
- Warm-start and perturbed-tree centered paths already fail closed with `centered_family_same_family_seed_missing`.

### Established Patterns
- Unsupported or excluded paths use explicit reason codes and keep denominator visibility in artifacts.
- Tests assert exact artifact payload fields, not only successful status.
- Family matrix suites clone raw cases over raw, fixed centered, and continuation operators while preserving regime labels.

### Integration Points
- `src/eml_symbolic_regression/optimize.py`
- `src/eml_symbolic_regression/benchmark.py`
- `src/eml_symbolic_regression/semantics.py`
- `tests/test_benchmark_contract.py`
- `tests/test_benchmark_runner.py`
- `tests/test_optimizer_cleanup.py`

</code_context>

<specifics>
## Specific Ideas

Introduce a raw-only registry entry for each current scaffold helper first, then use it from both benchmark suite expansion and optimizer training attempt construction. Centered-family scaffold exclusions should be visible before training starts and should survive through serialized artifacts.

</specifics>

<deferred>
## Deferred Ideas

Constructing actual centered-family witnesses for `exp`, `log`, scaled exponentials, and reciprocal motifs remains deferred to the centered-family theory track.

</deferred>
