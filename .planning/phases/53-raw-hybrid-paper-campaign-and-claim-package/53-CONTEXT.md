# Phase 53 Context: Raw-Hybrid Paper Campaign and Claim Package

## Mode

Autonomous smart-discuss defaults were selected because `$gsd-autonomous` is running non-interactively.

## Phase Goal

Generate the paper-facing raw-hybrid suite, reports, tables, claim boundaries, and docs after the new evidence exists.

## Success Criteria

1. A raw-hybrid paper suite includes shallow blind boundaries, perturbed basin evidence, Beer-Lambert, Shockley, Arrhenius, and Michaelis diagnostics.
2. Reports keep pure blind, scaffolded, compile-only, warm-start, same-AST return, repaired, refit, and perturbed-basin regimes separate.
3. Scientific-law tables include formula, compile support, compile depth, macro hits, warm-start status, verifier status, and artifact paths.
4. Centered-family material is framed as negative diagnostic evidence with the same-family witness caveat.
5. README/docs updates cite successful artifacts and avoid blind-discovery overclaims.

## Requirements

| ID | Requirement | Status |
| --- | --- | --- |
| RHY-01 | Developer can run a paper-facing raw-hybrid suite or campaign preset that includes shallow blind boundaries, perturbed basin evidence, Beer-Lambert, Shockley, Arrhenius, and Michaelis diagnostics. | Planned |
| RHY-02 | Generated reports keep pure blind, scaffolded, compile-only, warm-start, same-AST return, repaired, refit, and perturbed-basin regimes separate. | Planned |
| RHY-03 | Generated scientific-law tables include formula, compile support, compile depth, macro hits, warm-start status, verifier status, and artifact path. | Planned |
| RHY-04 | Centered-family results are reported only as negative diagnostics with the same-family witness caveat, not as an intrinsic impossibility claim. | Planned |
| RHY-05 | README or implementation docs are updated only after successful artifacts exist, with claim language that avoids presenting warm-start recovery as blind discovery. | Planned |

## Existing Evidence Inputs

- v1.5/v1.6 proof bundles provide shallow pure-blind boundaries, scaffolded shallow proof, perturbed-basin evidence, and depth degradation evidence.
- v1.8 paper decision artifacts provide centered-family negative diagnostics and the same-family witness caveat.
- Phase 49 added explicit raw-only scaffold witness registry and centered scaffold exclusion reason codes.
- Phase 50 generated focused Arrhenius same-AST warm-start evidence under `artifacts/campaigns/v1.9-arrhenius-evidence/`.
- Phase 51 generated focused Michaelis-Menten same-AST warm-start evidence under `artifacts/campaigns/v1.9-michaelis-evidence/`.
- Phase 52 generated focused expanded cleanup evidence under `artifacts/campaigns/v1.9-repair-evidence/`, measuring no repair improvement but preserved fallback behavior and taxonomy.

## Decisions

- Package and report existing measured evidence; do not silently rerun broad historical campaigns unless a focused Phase 53 suite requires it.
- Keep evidence regimes separated in data, tables, prose, and claim language.
- Treat Arrhenius and Michaelis as exact compiler warm-start / same-AST basin evidence, not blind discovery.
- Treat Phase 52 repair evidence as repair-only evidence; its focused real suite measured no improvements and that negative result should remain visible.
- Treat centered-family material as negative diagnostic evidence under missing same-family witnesses, not an impossibility theorem.
- Prefer a reproducible paper-facing suite/preset and durable artifacts under a v1.9 paper path, rather than editing archived v1.5/v1.6/v1.8 evidence.

## Non-Goals

- Do not change proof thresholds or claim denominators from previous milestones.
- Do not present warm-start, same-AST, compiler-seed, repair, refit, or scaffolded evidence as pure blind discovery.
- Do not claim centered families are intrinsically impossible.
- Do not claim Planck or logistic solved status.
- Do not regenerate README/docs claim text before successful Phase 53 artifacts exist.

## Open Questions For Research

1. Should Phase 53 generate one new `v1.9-raw-hybrid-paper` suite/campaign artifact, or should it synthesize a package from existing committed aggregates plus focused v1.9 evidence artifacts?
2. Which existing report generator is the closest fit for regime-separated raw-hybrid tables: `campaign.py`, `paper_decision.py`, a new module, or a small extension of both?
3. What is the minimal runnable suite that satisfies RHY-01 without duplicating large historical proof campaigns?
4. Which scientific-law rows should be included for Beer-Lambert, Shockley, Arrhenius, Michaelis, and unsupported/stretch cases, and where should compile diagnostics be sourced from?

## Candidate Implementation Areas

- `src/eml_symbolic_regression/benchmark.py`
- `src/eml_symbolic_regression/campaign.py`
- `src/eml_symbolic_regression/paper_decision.py`
- `src/eml_symbolic_regression/proof.py`
- `src/eml_symbolic_regression/diagnostics.py`
- `tests/test_benchmark_contract.py`
- `tests/test_campaign.py`
- `tests/test_proof_contract.py`
- `README.md`
- `docs/IMPLEMENTATION.md`
- `artifacts/paper/v1.9/`
