---
phase: 51-reciprocal-and-saturation-compiler-motifs
status: discussed
mode: autonomous-smart-discuss
created: 2026-04-17
requirements: [MIC-01, MIC-02, MIC-03, MIC-04]
---

# Phase 51 Context: Reciprocal and Saturation Compiler Motifs

## Goal

Add reusable reciprocal-shift and saturation-ratio compiler motifs to reduce Michaelis-Menten depth and support honest recovery diagnostics.

## Locked Defaults

- Target demo: `michaelis_menten`.
- Target formula: `2*x/(x + 0.5)`.
- Current best diagnostic: strict compile is unsupported at `max_depth=13`, but relaxed compile succeeds at depth `<= 14` and already records `direct_division_template`.
- Primary motifs:
  - `reciprocal_shift_template` for structures like `1/(x + b)`.
  - `saturation_ratio_template` for structures like `(a*x)/(b + x)`.
- Macro work must be reusable motif logic, not a one-off recognizer for `michaelis_menten`.
- If strict support reaches the current gate, add a Michaelis-Menten exact warm-start recovery path; otherwise record material depth/node reduction with honest unsupported status.
- Preserve existing Planck stretch behavior and Arrhenius same-AST evidence classification.

## Success Criteria

1. Reciprocal-shift motifs such as `1/(x+b)` compile or fail closed with improved diagnostics.
2. Saturation-ratio motifs such as `(a*x)/(b+x)` use reusable compiler logic rather than formula-specific hardcoding.
3. Before/after diagnostics record depth, node count, rule trace, and macro hits for reciprocal-shift and Michaelis targets.
4. Michaelis-Menten is exact-recovered if strict support reaches the gate; otherwise artifacts preserve an honest unsupported status with measured depth reduction.

## Requirements

- **MIC-01**: Developer can compile reciprocal-shift motifs such as `1/(x + b)` or inspect a fail-closed diagnostic explaining remaining unsupported structure.
- **MIC-02**: Developer can compile or rewrite saturation-ratio motifs such as `(a*x)/(b + x)` through reusable compiler logic rather than a one-off formula recognizer.
- **MIC-03**: Developer can compare before/after compiler diagnostics for `1/(x+0.5)` and `2*x/(x+0.5)`, including depth, node count, rule trace, and macro hits.
- **MIC-04**: Developer can run Michaelis-Menten warm-start recovery if strict support reaches the gate, or see an honest unsupported artifact if the macro work only reduces depth.

## Existing Evidence

- `src/eml_symbolic_regression/compiler.py` already has:
  - `direct_division_template` for true numerator-over-denominator motifs,
  - `scaled_exp_minus_one_template` for Shockley/Planck-style `scale*(exp(arg)-1)` motifs,
  - macro diagnostics with hits, misses, baseline depth, baseline node count, depth delta, and node delta.
- `tests/test_compiler_warm_start.py::test_michaelis_relaxed_diagnostic_reports_direct_division_macro` currently expects `michaelis_menten` to be strict unsupported and relaxed depth `<= 14` with `direct_division_template`.
- `tests/test_compiler_warm_start.py::test_cli_reports_michaelis_menten_depth_gate_without_promotion` currently expects CLI `compiled_seed == "unsupported"` and `warm_start_eml.status == "unsupported"` for Michaelis-Menten.
- Phase 50 added Arrhenius without compiler-specific special casing; Phase 51 should preserve that standard for Michaelis motifs.

## Implementation Boundaries

- Allowed compiler changes should live in reusable macro helpers in `compiler.py` and tests around those helpers.
- Do not add a formula-id conditional for `michaelis_menten`.
- Do not relax the default strict gate silently. If a max-depth or node budget changes in any evidence path, that must be explicit in the artifact and documentation.
- Do not weaken verifier-owned recovery: `recovered` still requires held-out/extrapolation/high-precision verification.
- Preserve evidence regimes: compile-only, warm-start, same-AST return, unsupported, repaired, and blind discovery remain separate.

## Suggested Evidence Path

- Add unit tests for `sp.Pow(x + sp.Float("0.5"), -1)` or `1/(x + 0.5)` proving `reciprocal_shift_template` behavior.
- Add unit tests for `2*x/(x + 0.5)` proving `saturation_ratio_template` behavior and macro diagnostics.
- Update Michaelis-Menten CLI/benchmark behavior according to actual strict result:
  - If strict compile passes within depth `13`, add warm-start same-AST/recovery tests and update diagnostics from unsupported to recovered evidence.
  - If strict compile remains above depth `13`, add artifact tests that show reduced depth/node count and preserve unsupported status.
- Add a focused benchmark/report path if strict or materially improved diagnostics need durable evidence for Phase 53.

## Open Questions (AUTO-RESOLVED)

1. **Should this phase require Michaelis-Menten recovery?** No. The roadmap says "if strict support reaches the gate; otherwise material depth reduction and honest unsupported status." The plan should target strict support but remain honest if reusable motifs only reduce depth.
2. **Should Planck be touched?** Only through regression tests to preserve stretch/unsupported behavior. Planck is not a Phase 51 flagship.
3. **Should we add broad campaign rows now?** No. Use focused compiler/CLI/benchmark diagnostics first; paper-facing packaging belongs to Phase 53.

## Threat Model

- **Information integrity**: A depth reduction must not be reported as exact recovery unless the verifier says `recovered`.
- **Tampering/overfitting**: Macro matching must recognize reusable symbolic structure, not the `michaelis_menten` demo id or exact string only.
- **Regression**: New motif rules must not degrade Beer-Lambert, Shockley, Arrhenius, Michaelis unsupported diagnostics, or Planck stretch diagnostics.
- **Claim safety**: If Michaelis becomes warm-start recovered, label it as compiler/warm-start evidence unless a blind path actually succeeds.

