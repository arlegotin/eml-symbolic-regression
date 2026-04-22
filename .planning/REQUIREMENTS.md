# Requirements: EML Symbolic Regression v1.17

**Milestone:** v1.17 Snap-First Exact Recovery and Candidate Neighborhood Search
**Created:** 2026-04-22
**Status:** Complete on 2026-04-22; final package decision `still_inconclusive`
**Source context:** v1.16 final decision `inconclusive`, with 12 loss-only paired pilot rows and 0 verifier-gated exact recoveries

## Goal

Turn v1.16's loss-only and near-miss evidence into a precise snap/candidate-search investigation. v1.17 should determine whether low-margin snap alternatives and bounded exact-tree neighborhoods can produce verifier-gated exact recovery on natural-bias targets before any broader i*pi/GEML campaign is reopened.

## Success Definition

The milestone succeeds if it produces a source-locked answer to a narrower question: can snap-first diagnostics plus target-agnostic exact-neighborhood search recover at least one verifier-gated exact candidate from the v1.16-style natural-bias setting? A positive signal must be exact-verifier owned. If no exact signal appears, the package must explain whether the blocker is margin ambiguity, candidate explosion, branch pathology, verifier mismatch, or a deeper representational/search limitation.

## Snap Diagnostics and Margins

- **SNAP-01**: Record per-slot snap probabilities, margins, selected alternatives, and low-confidence alternatives for selected, fallback, and loss-only candidates.
- **SNAP-02**: Classify snap mismatch rows by active-node changes, low-margin slot patterns, soft-versus-hard error deltas, and branch/fidelity diagnostics.
- **SNAP-03**: Produce deterministic snap-neighborhood manifests for v1.16 failed and loss-only pilot rows, including budgets and source locks.

## Exact Neighborhood Search

- **NBR-01**: Generate bounded one-slot and two-slot exact AST alternatives around snapped candidates without target formula leakage.
- **NBR-02**: Verify every neighborhood candidate through the same train, held-out, extrapolation, symbolic, and high-precision gates before promotion.
- **NBR-03**: Preserve fallback and original snapped candidates with provenance for accepted moves, rejected moves, and unchanged candidates.
- **NBR-04**: Cap candidate explosion with deterministic budgets, stable ordering, and source-locked limits.

## Candidate Ranking and Promotion

- **RANK-01**: Rank candidates by exact verifier status first, symbolic/equivalence evidence second, and post-snap loss only as a diagnostic.
- **RANK-02**: Expose why the winning candidate was selected and why lower-loss candidates were rejected when they fail exact recovery.
- **RANK-03**: Keep loss-only, repaired, compile-only, same-AST, fallback, and original-snap accounting fields separate in every table.

## Focused Evidence

- **EVID-01**: Run a tiny v1.17 snap-neighborhood smoke on selected v1.16 natural-bias rows before any broader campaign.
- **EVID-02**: Compare raw and i*pi EML under matched budgets and negative controls only after neighborhood search is enabled.
- **EVID-03**: Gate any pilot or full campaign expansion on at least one verifier-gated exact-recovery signal.

## Evidence Package

- **PACK-01**: Produce a v1.17 evidence package with before/after exact recovery, failure taxonomy, source locks, manifests, and reproduction commands.
- **PACK-02**: Classify the final result as `exact_signal_found`, `still_inconclusive`, or `negative` under predefined criteria.
- **PACK-03**: Keep the v1.16 final package intact and make any v1.17 comparison explicitly additive.

## Future Requirements

- **FUT-01**: Learn continuous `a` values only after fixed exact recovery signal is established.
- **FUT-02**: Reopen larger standardized hardware campaigns only after the v1.17 gate justifies them.
- **FUT-03**: Add theorem or certificate machinery for exact-neighborhood promotions that become paper-critical.

## Out of Scope

- Weakening the verifier or counting post-snap loss as recovery.
- Exact target seeding, formula-name recognizers, hard-coded target trees, or hidden oracle simplification.
- Large blind i*pi/GEML campaigns before the tiny snap-neighborhood smoke produces exact signal.
- Positive paper claims from loss-only, repaired-only, compile-only, or same-AST evidence.
- Dropping negative controls or unmatched raw EML comparisons because they weaken the result.
- Rewriting the v1.16 source-locked package to imply a stronger outcome.

## Milestone Gate

v1.17 passes if the final package truthfully answers whether snap-first exact-neighborhood search produced any verifier-gated exact-recovery signal. `exact_signal_found` requires at least one exact recovered candidate under the declared gate. `still_inconclusive` is acceptable only with source-locked diagnostics and next-step blockers. `negative` is acceptable if the evidence shows the approach fails under the declared budgets and controls.
