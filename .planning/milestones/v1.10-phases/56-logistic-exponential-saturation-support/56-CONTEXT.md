---
phase: 56-logistic-exponential-saturation-support
status: discussed
mode: autonomous-smart-discuss
created: 2026-04-18
requirements: [MOTIF-02, LOGI-01, LOGI-02, LOGI-03, LOGI-04, LOGI-05]
---

# Phase 56 Context: Logistic Exponential-Saturation Support

## Goal

Add a reusable structural exponential-saturation motif for logistic-like laws and attempt warm-start only if the unchanged strict gate passes.

## Locked Defaults

- No formula-name or demo-name recognizers.
- No exact-constant recognizer for `1.3` or `2`.
- Strict compile gate remains `max_depth=13`, `max_nodes=256`.
- Logistic archived diagnostic from Phase 54 is relaxed depth `27`, node count `77`, no macro hits.
- Phase 55 generalized `g+b` and `c*g/(g+b)` but did not match the actual logistic normalized form `1/(1+2*exp(-1.3*x))`.

## Implementation Decisions

- Add `exponential_saturation_template` for direct structures like `1/(1+c*exp(a))`.
- Also accept the equivalent ratio structure `exp(a)/(exp(a)+c)` as the same structural family when it can be validated.
- Build the motif as an exact EML AST and validate it; do not bypass `compile_and_validate()`.
- If logistic remains above depth `13`, keep it unsupported under strict compile and do not run or claim warm-start recovery in this phase.
- Preserve macro diagnostics with baseline depth/node deltas so the improvement from archived depth `27` is visible.

## Existing Code Insights

### Reusable Assets

- `add_expr`, `Eml`, `exp_of`, and literal constants can express the exact identity:
  - `1/(1+c*exp(a)) = exp(1 - log(e*(1+c*exp(a))))`.
- `_macro_diagnostics()` already compares macro depth against no-macro baseline.
- `diagnose_compile_expression()` already reports strict unsupported plus relaxed metadata.

### Established Patterns

- A macro is accepted by tests only after `compile_and_validate()` passes on demo-domain inputs.
- Compile-only improvement remains unsupported when strict depth exceeds the configured gate.
- Same-AST warm-start evidence is allowed only after strict compile support.

## Deferred Ideas

- If strict support does not land, focused suite/artifact work moves to Phase 58 as compile diagnostic evidence.
- Lowering scalar multiplication depth is not part of Phase 56; it would be a separate compiler motif.

## Threat Model

- **Overclaiming**: A depth reduction must not become `recovered` or `same_ast_return` unless warm-start verification runs and passes.
- **Overfitting**: Matching must inspect symbolic structure, not `logistic` or exact constants.
- **Regression**: Existing Shockley, Arrhenius, Michaelis-Menten, and Planck diagnostics must remain intact.
