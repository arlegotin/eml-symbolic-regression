# Phase 87: GEML Evidence Package and Claim Boundary - Context

**Gathered:** 2026-04-22
**Status:** Ready for planning
**Mode:** Smart discuss auto-defaults

<domain>
## Phase Boundary

The milestone should end with a source-locked, claim-safe GEML/i*pi EML decision package. The package must be honest about whether the matched protocol has enough evidence for a paper section and must block overclaiming.

In scope:

- Package the Phase 83 i*pi restricted theory note.
- Package Phase 85 benchmark suite manifests and Phase 86 paired campaign tables when available.
- Classify paired outcomes by target family, including negative controls.
- Produce source locks, reproduction commands, claim-audit artifacts, and a claim-boundary summary.
- State the decision: promising, negative, or inconclusive under the matched protocol.

Out of scope:

- Running a broad expensive campaign automatically.
- Converting the result into manuscript prose beyond a concise claim-boundary summary.
</domain>

<decisions>
## Implementation Decisions

- Add a reusable package builder module instead of ad-hoc static files.
- Treat missing or smoke-only campaign evidence as `inconclusive`, not failure.
- Use forbidden-claim checks for global superiority, broad blind recovery, and full universality.
- Source-lock all package inputs and outputs with SHA-256.
- Keep the package rooted at `artifacts/paper/v1.15-geml/`.
</decisions>

<code_context>
## Existing Code Insights

- `publication.py` and `paper_package.py` establish source-lock, claim-audit, release-gate, and manifest patterns.
- Phase 83 writes `artifacts/theory/v1.15/ipi-restricted-theory.json` and `.md`.
- Phase 85 registers `v1.15-geml-oscillatory` and `v1.15-geml-oscillatory-smoke`.
- Phase 86 writes `geml-paired-comparison.csv`, `geml-paired-summary.json`, and `geml-paired-comparison.md` for campaigns.
</code_context>

<specifics>
## Specific Ideas

- Add `src/eml_symbolic_regression/geml_package.py`.
- Write:
  - `manifest.json`
  - `source-locks.json`
  - `target-family-classification.json`
  - `target-family-classification.csv`
  - `target-family-classification.md`
  - `claim-audit.json`
  - `claim-audit.md`
  - `claim-boundary.md`
  - `reproduction.md`
- Tests should verify package creation, claim-audit blocking, and source locks.
</specifics>

<deferred>
## Deferred Ideas

- A full paper-section draft is deferred until the package contains full matched campaign evidence, not only protocol or smoke evidence.
</deferred>
