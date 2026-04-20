# Phase 72: Automated Test Suite and CI Hardening - Context

**Gathered:** 2026-04-20
**Status:** Ready for planning
**Mode:** Autonomous smart discuss; recommended choices accepted by agent discretion

<domain>
## Phase Boundary

This phase makes existing algorithmic coverage enforceable in CI and adds a minimal evidence-regression path that exercises train -> snap -> verify -> artifact generation. It also adds branch/public-snapshot validation so `dev` keeps full source/test/planning context while the generated public snapshot excludes local-only artifacts and keeps CI.

</domain>

<decisions>
## Implementation Decisions

### Test Coverage
- Reuse the existing unit suites for semantics, compiler contracts, verifier evidence, split isolation, benchmark manifests, and publication validation.
- Add one small evidence-regression test instead of introducing a long training campaign.
- Keep test budgets small and deterministic.

### CI Scope
- Add a GitHub Actions CI workflow for `dev`, `main`, pull requests, and manual dispatch.
- Run focused core unit tests, selected integration smoke tests, clean-room publication smoke, and branch/public-snapshot validation as separate jobs.
- Avoid making CI depend on locally generated private artifacts beyond committed source/test fixtures.

### Branch Discipline
- Keep the `publish-main` workflow dev-only.
- Preserve public CI on the generated `main` snapshot while removing the publishing workflow and private planning/source directories.
- Validate the public snapshot contract by simulating the publish filter in CI.

### the agent's Discretion
- Implement branch validation as a small Python script with tests so the CI policy is locally testable.
- Keep workflow commands plain `pip`/`pytest` rather than introducing another CI tool.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- Existing tests already cover EML semantics, branch diagnostics, compiler and warm-start behavior, verifier evidence levels, split isolation, benchmark manifests, publication rebuild validation, and public-package artifacts.
- `scripts/publication-rebuild.sh` already exercises the Phase 69 clean-room smoke rebuild.
- `.github/workflows/publish-main.yml` already publishes a sanitized `main` snapshot from `dev`.

### Established Patterns
- CI can install the package with `pip install -e ".[dev]"` from `pyproject.toml`.
- Tests use pytest and `PYTHONPATH=src`.
- Public snapshot filtering currently removes raw runs, raw-runs, aggregate JSON payloads, source bundles, and large training traces.

### Integration Points
- New CI workflow lives in `.github/workflows/ci.yml`.
- Branch validation script lives in `scripts/validate-ci-contract.py`.
- Evidence regression test lives in `tests/test_evidence_regression.py`.
- Public snapshot publishing filter is maintained in `.github/workflows/publish-main.yml`.

</code_context>

<specifics>
## Specific Ideas

Make CI useful but bounded: run the high-signal fast suites and a few integration smoke tests, not the full expensive paper artifact suite on every push.

</specifics>

<deferred>
## Deferred Ideas

- Full publication evidence rebuild remains Phase 76.
- Expanding CI to a large matrix of Python/PyTorch versions is deferred until the project has stable runtime budgets.
</deferred>
