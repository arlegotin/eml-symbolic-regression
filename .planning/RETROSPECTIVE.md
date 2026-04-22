# Project Retrospective

*A living document updated after each milestone. Lessons feed forward into future planning.*

## Milestone: v1.3 — Benchmark Campaign and Evidence Report

**Shipped:** 2026-04-15
**Phases:** 5 | **Plans:** 5 | **Sessions:** 1

### What Was Built

- Campaign presets for smoke, standard, and showcase benchmark runs.
- Campaign folders with raw run artifacts, aggregate JSON/Markdown, tidy CSVs, SVG figures, manifest, and `report.md`.
- A committed smoke evidence bundle at `artifacts/campaigns/v1.3-smoke/`.
- Documentation for command usage, output schema, plot meanings, and honest interpretation.

### What Worked

- Reusing the benchmark aggregate model kept CSV, plot, and report generation consistent.
- Standard-library CSV and SVG output avoided dependency churn while producing useful artifacts.
- The smoke campaign gave an end-to-end proof without committing a large or slow evidence set.

### What Was Inefficient

- GSD summary extraction did not understand the local summary format, so milestone accomplishments needed manual correction.
- Runtime metrics are read back from raw JSON artifacts; a future aggregate schema could carry timing directly.

### Patterns Established

- Evidence artifacts should keep unsupported and failed cases in the denominator.
- Same-AST warm-start return should remain separate from blind recovery in every table, chart, and report.
- Static reports are enough to validate metric choices before building dashboards.

### Key Lessons

1. The next useful technical work is optimizer/compiler improvement, not more reporting infrastructure.
2. Every future algorithm change should rerun the same campaign presets for before/after comparison.
3. Report generation should be treated as part of the benchmark contract, not as a manually edited artifact.

### Cost Observations

- Model mix: local Codex orchestration with no external subagents.
- Sessions: 1
- Notable: Phase-sized commits kept recovery straightforward despite a broad milestone.

---

## Milestone: v1.6 — Hybrid Search Pipeline and Exact Candidate Recovery

**Shipped:** 2026-04-16
**Phases:** 5 | **Plans:** 5 | **Sessions:** 2

### What Was Built

- Verifier-gated exact-candidate pooling across restarts and hardening checkpoints.
- Target-free low-margin snap-neighborhood cleanup with fallback-preserving exact candidate artifacts.
- Post-snap constant refit and richer `exp`/`log` anomaly diagnostics.
- Macro-aware compiler shortening with conservative warm-start coverage expansion.
- Regime-aware proof/campaign reports, immutable anchor locks, and final `artifacts/proof/v1.6` evidence bundle.

### What Worked

- Treating the optimizer as a candidate generator kept final recovery decisions verifier-owned.
- Preserving fallback candidates made hybrid-stage upgrades safer to evaluate.
- Report-level regression tests caught publication-facing truthfulness issues before closeout.
- Checking report mtimes and aggregates prevented mixed-provenance proof artifacts from being mistaken for final evidence.

### What Was Inefficient

- The final proof bundle had to be rerun multiple times because report prose defects were found only during artifact inspection.
- The GSD `audit-open` command failed with `output is not defined`, so open-artifact audit could not be used as intended.
- Large proof/campaign artifacts make closeout slower and should be frozen deliberately before paper work begins.

### Patterns Established

- Every recovery claim must identify its evidence regime: pure blind, scaffolded blind, warm start, compile-only, catalog, or perturbed basin.
- Human-readable reports must be checked against aggregate JSON before they are cited.
- Publication evidence should be generated from a final code state and then locked with hashes.

### Key Lessons

1. The paper should frame EML training as a verified pipeline with separated evidence regimes, not as universal blind symbolic regression.
2. Pure-blind weakness is a useful scientific result and should remain visible in the manuscript.
3. Claims-to-evidence mapping should happen before any further optimizer work.

### Cost Observations

- Model mix: local Codex orchestration with focused terminal verification.
- Sessions: 2
- Notable: The long proof reruns were worth doing before tagging because they caught a final publication-facing typo and locked the authoritative evidence bundle.

---

## Milestone: v1.13 — Publication-grade reproduction and validation

**Shipped:** 2026-04-20
**Phases:** 8 | **Plans:** 8 | **Sessions:** 1

### What Was Built

- Clean-room publication rebuild path with lockfile/container provenance, source locks, validation, and smoke/full modes.
- Layered verifier and split-discipline upgrades for symbolic, dense randomized, adversarial, certificate, evidence-level, and final-confirmation reporting.
- Guarded versus faithful training semantics controls with manifest diagnostics for guard/anomaly/post-snap mismatch evidence.
- CI/public snapshot validation, basis-only and literal-constant benchmark tracks, expanded dataset manifests, and matched baseline harness.
- Final v1.13 evidence package under `artifacts/paper/v1.13/` with a passing claim audit, release gate, and milestone audit.

### What Worked

- Using the Phase 76 rebuild as the release gate forced the campaign, baselines, dataset manifests, audit, and public snapshot checks to agree.
- Keeping basis-only and literal-constant denominators separate made the final evidence more honest without blocking applied literal-constant demos.
- Fail-closed optional baseline adapters kept the harness reproducible in the local environment while making missing dependencies explicit.
- Excluding raw campaign run payloads from source locks kept the committed evidence package small and reviewable.

### What Was Inefficient

- `gsd-tools audit-open` still fails through the CLI path with `output is not defined`; the structured audit had to be invoked through the underlying module.
- `gsd-tools phase complete` and `milestone complete` still corrupt or stale some generated roadmap/state text, so closeout required manual repair.
- Full publication rebuilds create large raw run payloads before pruning; the release path should make curated versus scratch output clearer.

### Patterns Established

- Publication artifacts should include both a claim audit and a release gate, not just a manifest.
- Baseline rows must stay outside EML recovery denominators.
- Final confirmation and verifier evidence should be machine-readable release blockers.
- Public `main` publication should be workflow-gated, not a local force-push.

### Key Lessons

1. The project is now ready for manuscript packaging work, but only with the v1.13 claim boundaries.
2. External baseline depth can improve only after dependencies are deliberately installed; silent absence is no longer acceptable.
3. Release artifacts need a curated output policy so large scratch payloads do not become accidental source-lock or git history baggage.

### Cost Observations

- Model mix: local Codex orchestration with no spawned subagents.
- Sessions: 1
- Notable: The full release rebuild and artifact pruning were the expensive path; focused regression tests stayed fast.

---

## Milestone: v1.15 — GEML family and i*pi EML exploration

**Shipped:** 2026-04-22
**Phases:** 6 | **Plans:** 6 | **Sessions:** 1

### What Was Built

- Fixed-parameter `GEML_a` semantics with raw EML and i*pi EML named specializations.
- Restricted i*pi theory artifacts with branch convention, branch diagnostics, and explicit non-claims.
- Family-aware training, snapping, candidate selection, verifier metrics, and manifest fields.
- Matched raw EML versus i*pi EML benchmark suites over oscillatory targets and negative controls.
- Paired campaign tables and final `artifacts/paper/v1.15-geml/` claim-boundary package.

### What Worked

- Treating i*pi EML as one fixed `GEML_a` specialization kept the implementation coherent and avoided a one-off operator path.
- The claim audit made the final inconclusive decision explicit instead of relying on prose discipline.
- Running the smoke campaign before packaging exposed a real target-family classification gap while it was still cheap to fix.

### What Was Inefficient

- Generated run artifacts dominate the diff size even for a four-row smoke campaign.
- The GSD `audit-open` command still fails with `output is not defined`, so closeout had to record that tool failure and proceed manually.
- Summary/frontmatter conventions remain inconsistent with the milestone audit workflow; requirement coverage had to be cross-checked from VERIFICATION files.

### Patterns Established

- Operator-family research milestones should end with a claim-boundary package, not only benchmark tables.
- Loss-only signals should be separated from verifier-gated exact recovery in paired comparisons.
- Negative controls must be present before interpreting any structural-bias signal.

### Key Lessons

1. The current i*pi evidence is useful but inconclusive; the project should not promote it to a positive paper section without the full matched campaign or stronger recovery.
2. Branch contracts belong in artifacts and audits, not only in implementation comments.
3. Family semantics and benchmark evidence can advance without changing the core verifier-owned recovery standard.

### Cost Observations

- Model mix: local Codex orchestration with no spawned subagents.
- Sessions: 1
- Notable: The campaign/package loop was cheap enough to regenerate after fixing classification and summary accounting.

---

## Cross-Milestone Trends

### Process Evolution

| Milestone | Sessions | Phases | Key Change |
|-----------|----------|--------|------------|
| v1.1 | 1 | 6 | Compiler warm starts moved claims from catalog verification to trained exact EML recovery. |
| v1.2 | 1 | 5 | Benchmark evidence replaced anecdotal training checks. |
| v1.3 | 1 | 5 | Campaign reports made benchmark evidence presentation-ready. |
| v1.6 | 2 | 5 | Hybrid exact-candidate recovery and regime-aware proof evidence became paper-grade. |
| v1.13 | 1 | 8 | Publication-grade rebuild, audit, baseline, dataset, CI, and release-gate contracts replaced ad hoc paper packaging. |
| v1.15 | 1 | 6 | GEML operator-family research shipped with restricted theory, matched protocols, paired evidence, and claim-boundary packaging. |

### Cumulative Quality

| Milestone | Tests | Coverage | Zero-Dep Additions |
|-----------|-------|----------|-------------------|
| v1.1 | 24 | Focused regression coverage | Compiler metadata and warm-start manifests |
| v1.2 | 38 | Benchmark contract and runner coverage | Aggregate Markdown evidence |
| v1.3 | 45 | Campaign, CSV, plot, report, and CLI coverage | CSV export, SVG figures, Markdown report |
| v1.6 | 120+ | Candidate pooling, cleanup, refit, compiler, campaign, proof, and report coverage | Hash-locked proof and comparison artifacts |
| v1.13 | 150+ | CI contract, evidence regression, verifier, benchmark, publication, baseline, and dataset coverage | Claim audit, release gate, dataset manifests, baseline reports |
| v1.15 | 150+ | GEML semantics, branch diagnostics, optimizer metrics, benchmark suites, campaign tables, and package audit coverage | GEML package, target-family tables, source locks |

### Top Lessons

1. Recovery claims stay credible only when the verifier owns the final status.
2. Measurement should precede optimizer changes when the failure modes are not yet clear.
3. Reproducible artifacts are more useful than one-off demo output for this project.
4. Manuscript claims should be written from aggregate-backed evidence rows, not from narrative report prose alone.
5. Release credibility needs a machine-readable claim audit and public snapshot gate before any branch publication.
6. New operator-family hypotheses should ship with negative controls and explicit claim boundaries before paper-positive framing.
