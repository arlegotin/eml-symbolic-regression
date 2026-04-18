---
phase: 57-planck-motif-search-and-power-compression
status: discussed
mode: autonomous-smart-discuss
created: 2026-04-18
requirements: [MOTIF-03, MOTIF-04, PLAN-01, PLAN-02, PLAN-03, PLAN-04, PLAN-05]
---

# Phase 57 Context: Planck Motif Search and Power Compression

## Goal

Reduce Planck compile depth through reusable power compression and bounded motif evidence, while preserving unsupported/stretch honesty unless the full support and verification contract passes.

## Locked Defaults

- Planck archived relaxed diagnostic from Phase 54 is depth `20`, node count `67`, with `scaled_exp_minus_one_template` and `direct_division_template`.
- The dominant numerator bottleneck is `x**3`, which currently compiles to depth `16`, node count `33`.
- `x**2` currently compiles to depth `8`, node count `17`; a replacement must not be kept if it is not shorter.
- Strict compiler gate remains `max_depth=13`, `max_nodes=256`.

## Implementation Decisions

- Add `low_degree_power_template` for positive integer powers only when the `exp(n*log(g))` exact EML construction is shorter than the existing repeated-multiplication path.
- At minimum, this should shorten cubes; squares should remain on the existing repeated-multiplication path if it is shorter.
- Keep the template structural over any compilable base `g`, not a Planck formula branch.
- Use `compile_and_validate()` tests as the validation gate for accepted power shortcuts.
- If Planck reaches strict support, allow later warm-start evidence; if it only improves depth, keep unsupported/stretch status.

## Existing Code Insights

### Reusable Assets

- `_compile_power()` already handles integer powers and `max_power`.
- `log_of()`, `multiply_expr()`, and `exp_of()` can build the exact identity `g**n = exp(n*log(g))`.
- Planck already uses `scaled_exp_minus_one_template` for `exp(x)-1` and `direct_division_template` for the numerator/denominator ratio.

### Established Patterns

- Macro diagnostics record macro hits and no-macro baseline deltas.
- Tests should assert Planck support status from actual compile output, not force promotion.

## Deferred Ideas

- General theorem proving is out of scope. Any motif-search helper should be small, bounded, and evidence-only.
- If Planck strict support appears, focused benchmark artifacts and optional warm-start evidence belong in Phase 58.

## Threat Model

- **Bad algebra**: `exp(n*log(g))` is branch-sensitive. Mitigation: accept via validation and existing verifier checks.
- **Non-improvement**: A square template would be worse than the current path. Mitigation: compare candidate depth/node count before recording the macro.
- **Overclaiming**: Planck compile support is not recovery unless warm-start/verifier evidence passes.
