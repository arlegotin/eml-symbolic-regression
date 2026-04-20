# Phase 69: Clean-Room Reproduction Path and Provenance - Context

**Gathered:** 2026-04-20
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase delivers the first publication-grade clean-room reproduction path for the paper-facing evidence package. It must let a fresh checkout rebuild figures, tables, aggregates, manifests, source locks, and validation records from declared source inputs in a locked environment, without relying on preexisting generated publication artifacts or `--require-existing` for the publication path.

</domain>

<decisions>
## Implementation Decisions

### Rebuild Entry Point
- Add a first-class documented rebuild command or script for the v1.13 publication package rather than requiring users to chain older paper commands manually.
- The command must have a cheap smoke mode suitable for tests and CI, and a full mode that is the publication contract.
- The rebuild path should create v1.13 outputs under a new versioned artifact root instead of overwriting archived v1.11 or v1.12 anchors.
- The publication path must not require `--require-existing`; any remaining existing-artifact checks must be confined to explicitly named legacy or fixture modes.

### Locked Environment
- Use committed, standard Python packaging artifacts already compatible with `pyproject.toml`; add only the minimum lock/container support needed for reproducible rebuilds.
- Container entrypoints should run the same rebuild command used outside the container so the command remains the source of truth.
- Environment identity must be captured in generated manifests even when the local run is not inside a container.
- Avoid network-dependent rebuild behavior in the default smoke path; full external dependency work belongs in later baseline phases unless already locally available.

### Provenance and Validation
- Every generated publication artifact needs immutable provenance: git revision, command, environment identity, generated-at timestamp, input hashes, output hashes, and artifact role.
- Placeholder metadata such as `1970-01-01T00:00:00+00:00` and `"snapshot"` must fail publication validation unless the path is explicitly identified as a deterministic-test fixture.
- Source locks should hash concrete files, not broad directories, and should distinguish source inputs from generated outputs.
- Validation should be executable as a standalone command or test helper so Phase 72 CI can reuse it directly.

### Non-Destructive Evidence Policy
- Preserve archived v1.4-v1.12 evidence and never rewrite historical package roots as part of the v1.13 publication rebuild.
- If old artifacts are consumed as fixed anchors, record them as source inputs with hashes and roles rather than silently treating them as regenerated evidence.
- New v1.13 generated artifacts should be traceable enough that Phase 76 can audit claims and publish a curated `main` snapshot from them.
- Keep the claim language conservative: this phase proves rebuild and provenance mechanics, not new recovery performance.

### the agent's Discretion
The agent may choose the exact module names, helper function boundaries, lockfile format, and script layout, provided they follow the existing CLI/package style and keep the rebuild command, manifest validation, and artifact layout explicit and testable.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/eml_symbolic_regression/cli.py` already owns paper-facing subcommands, including `paper-package`, `paper-assets`, `paper-supplement`, and raw-hybrid paper generation.
- `src/eml_symbolic_regression/paper_package.py` writes v1.11 manifests, source locks, claim audits, reproduction docs, and readiness docs from locked source artifacts.
- `src/eml_symbolic_regression/paper_v112.py` writes v1.12 draft, supplement, training-detail, and paper-facing assets under versioned artifact roots.
- `src/eml_symbolic_regression/campaign.py` and `src/eml_symbolic_regression/benchmark.py` already produce aggregate reports and manifests that can be reused as provenance inputs.
- `tests/test_paper_package.py`, `tests/test_paper_v112.py`, `tests/test_campaign.py`, and related manifest tests provide local patterns for artifact-writing regression coverage.

### Established Patterns
- Project code uses dataclasses for artifact path bundles, JSON manifests with `schema` fields, deterministic JSON formatting, and versioned artifact directories under `artifacts/`.
- CLI commands are implemented with `argparse` in `cli.py` and return integer status codes.
- Artifact writers generally refuse to overwrite existing outputs unless an explicit `overwrite` option is passed.
- The repo prefers source-locked, regime-separated evidence over claim promotion from training loss or convenience artifacts.

### Integration Points
- Add new CLI surface in `cli.py` and implementation in a focused module alongside `paper_package.py` and `paper_v112.py`.
- Wire tests through pytest without introducing a new test runner.
- Add or update developer-facing docs in README or `docs/IMPLEMENTATION.md` only where needed to expose the rebuild command.
- Existing `.github/workflows/publish-main.yml` is relevant as a later consumer, but this phase should not publish to `main`.

</code_context>

<specifics>
## Specific Ideas

- Prefer a command shaped like `eml-sr publication-rebuild --preset v1.13 --output-dir artifacts/paper/v1.13 --smoke` if it fits existing CLI conventions.
- Consider a validation helper that scans generated manifests for forbidden placeholder metadata and verifies declared hashes.
- Keep deterministic snapshot constants in `benchmark.py` legal only for stable fixture/test paths, not publication manifests.

</specifics>

<deferred>
## Deferred Ideas

- Full matched conventional baseline execution belongs to Phase 75.
- Full publication evidence rebuild and public `main` synchronization belongs to Phase 76.
- Broad CI wiring for all gates belongs to Phase 72, though Phase 69 should expose commands/tests CI can call later.

</deferred>
