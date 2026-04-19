# Phase 67: Bounded Baseline and Logistic Strict-Support Probes - Plan

**Created:** 2026-04-19  
**Status:** Ready for execution

## Goal

Attempt a bounded conventional symbolic-regression baseline and logistic strict-support upgrade without blocking the paper package or weakening claim boundaries.

## Tasks

1. Add a paper-probe generator that writes baseline status, logistic strict-support diagnostics, and a manifest.
2. Detect locally available conventional symbolic-regression modules without installing new dependencies.
3. If no local baseline is available, record an explicit unavailable/deferred row with limitation text.
4. Run the logistic compiler diagnostic at strict gate 13 and capture relaxed depth/macro validation metadata.
5. Add CLI wiring for the bounded probes.
6. Add focused tests for baseline status rows, logistic fail-closed rows, artifact generation, and CLI registration.
7. Generate the actual Phase 67 draft artifacts and update requirement status.

## Verification

- Baseline status is one of `completed`, `deferred`, or `unavailable`.
- Baseline rows state they are diagnostic-only and excluded from EML recovery denominators.
- Logistic strict gate remains 13.
- Logistic remains `promotion: no` unless strict compile and verifier recovery both pass.
- Focused tests pass.

## Risks

- A local baseline package may be absent; that is a valid bounded outcome if recorded clearly.
- Logistic strict support may fail by depth two; the phase should document the gap rather than relax the gate.
