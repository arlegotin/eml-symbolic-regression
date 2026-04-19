---
quick_id: 260419-ukc
slug: rewrite-readme-to-make-it-clear-engaging
status: planned
created: 2026-04-19
workflow: gsd-quick
type: execute
wave: 1
depends_on: []
autonomous: true
files_modified:
  - README.md
source_files:
  - .planning/STATE.md
  - AGENTS.md
  - README.md
  - docs/IMPLEMENTATION.md
  - pyproject.toml
  - sources/NORTH_STAR.md
  - sources/FOR_DEMO.md
must_haves:
  truths:
    - "A new reader understands what EML is, why this repo uses a hybrid pipeline, and what problem the package is trying to solve."
    - "A user can install the package, run the CLI, list demos, run a demo, run a benchmark smoke suite, and run tests from README instructions."
    - "The README keeps blind recovery, warm-start, same-AST, repaired, compile-only, verified_showcase, and unsupported evidence regimes separate."
  artifacts:
    - path: "README.md"
      provides: "Clear project narrative, technical architecture, usage guide, demo/evidence taxonomy, and limits"
  key_links:
    - from: "README.md"
      to: "pyproject.toml"
      via: "install and console-script instructions use the declared package metadata and eml-sr entry point"
    - from: "README.md"
      to: "docs/IMPLEMENTATION.md"
      via: "pipeline, recovery contract, compiler/warm-start contract, and benchmark taxonomy are summarized without changing meaning"
    - from: "README.md"
      to: "sources/FOR_DEMO.md"
      via: "demo discussion uses the same normalized, dimensionless, feasibility-aware constraints"
---

# Quick Task Plan: Rewrite README for Clarity, Engagement, and Use

## Objective

Rewrite `README.md` into a clear, engaging, technically useful entry point for the project. The README should explain the EML idea, the implemented hybrid symbolic-regression pipeline, how to run the package, how to interpret demos and evidence, and where the honest claim boundaries are.

This is a documentation rewrite only. Do not modify package code, tests, artifacts, or project planning state as part of this quick task unless the executor discovers that a command shown in the README is demonstrably stale and needs documentation-only correction.

## Source Audit

| Source | ID | Requirement | Plan | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| GOAL | QUICK-GOAL | Rewrite README to make it clear, engaging, useful, technical, and usage-oriented | 260419-ukc | COVERED | Tasks 1-3 rewrite structure, technical content, and commands |
| REQ | N/A | No ROADMAP requirement IDs are assigned to this quick task | 260419-ukc | COVERED | Quick task is separate from milestone roadmap |
| RESEARCH | IMPLEMENTATION | Recovery is verifier-owned; optimizer manifests, compiler output, warm starts, repair, and refit do not assign recovered status by themselves | 260419-ukc | COVERED | Tasks 1 and 3 make this explicit |
| RESEARCH | NORTH_STAR | Explain EML, complete depth-bounded master trees, complex128 training, snapping, cleanup, and high-precision verification | 260419-ukc | COVERED | Tasks 1 and 2 incorporate these details |
| RESEARCH | FOR_DEMO | Demo discussion must favor normalized, dimensionless, feasible laws and avoid high-depth or unit-heavy overclaims | 260419-ukc | COVERED | Tasks 1 and 3 include demo guidance |
| CONTEXT | STATE-01 | Project remains a verifier-gated hybrid EML methods/evidence package, not a broad blind-symbolic-regression superiority claim | 260419-ukc | COVERED | Task 3 checks claim language |
| CONTEXT | USER-01 | Do not present warm-start, same-AST, repaired, compile-only, or unsupported evidence as blind discovery | 260419-ukc | COVERED | Task 3 is dedicated to this boundary |

No source audit gaps are present.

## Tasks

### Task 1: Rewrite the README narrative and technical structure

<files>README.md</files>

<action>
Replace the current command-heavy README with a reader-first structure that still preserves the important technical detail. Use the following outline unless the existing prose strongly suggests a clearer ordering:

1. Project title and one-paragraph thesis.
2. "What is EML?" with `eml(x, y) = exp(x) - log(y)` and the complete depth-bounded tree idea.
3. "What this package does" describing the pipeline: data -> soft complete EML tree -> PyTorch complex128 optimization -> hardening/snapping -> exact AST -> SymPy cleanup -> verifier-owned recovery report.
4. "What counts as recovered" explaining train, held-out, extrapolation, and mpmath/high-precision checks.
5. "Install and quick start" with commands from `pyproject.toml` and the current CLI surface.
6. "Demos and evidence" summarizing demo IDs and evidence regimes from `sources/FOR_DEMO.md` and `docs/IMPLEMENTATION.md`.
7. "Limits and claim boundaries" keeping unsupported/stretch diagnostics visible.
8. "Repository map" pointing to `sources/NORTH_STAR.md`, `docs/IMPLEMENTATION.md`, `sources/FOR_DEMO.md`, `artifacts/`, `src/`, and `tests/`.

Write for a technically literate reader who has not followed the project history. Keep the tone direct and concrete. Do not add marketing claims, broad superiority claims, or unsupported recovery claims.
</action>

<verify>
<automated>rg -n "eml\\(x, y\\)|complete depth-bounded|complex128|snapping|verifier|mpmath|claim boundaries" README.md</automated>
</verify>

<done>
`README.md` has a coherent top-to-bottom narrative, explains the EML mechanism and pipeline, and is no longer primarily a long list of commands.
</done>

### Task 2: Make the usage section runnable and concise

<files>README.md</files>

<action>
Add a compact usage section that reflects `pyproject.toml`:

- Python requirement `>=3.11,<3.13`.
- Editable install command using the declared dev extra: `python -m pip install -e ".[dev]"`.
- Console script examples using `eml-sr`, because `pyproject.toml` declares `eml-sr = "eml_symbolic_regression.cli:main"`.
- Source-tree fallback examples using `PYTHONPATH=src python -m eml_symbolic_regression.cli ...`.

Keep the command set focused: verify paper identities, list demos, run one supported demo path, run one warm-start demo path, list benchmarks, run the smoke benchmark, generate a smoke campaign, and run tests. Avoid copying every historical evidence command from the current README into the quick-start section; move any milestone-specific reproduction guidance into a clearly labeled evidence/artifact section only when it helps interpretation.
</action>

<verify>
<automated>PYTHONPATH=src python -m eml_symbolic_regression.cli --help</automated>
<automated>PYTHONPATH=src python -m eml_symbolic_regression.cli list-demos</automated>
<automated>PYTHONPATH=src python -m eml_symbolic_regression.cli list-benchmarks</automated>
</verify>

<done>
The README gives a new user a short, accurate path from install to CLI smoke checks without changing code or inventing commands.
</done>

### Task 3: Audit evidence language and verify the docs-only change

<files>README.md</files>

<action>
Do a final evidence-boundary pass over the rewritten README. It must say plainly that:

- training loss alone is not recovery;
- compiler output alone is not trained recovery;
- warm-start, same-AST, scaffolded, repaired, refit, compile-only, verified_showcase, perturbed-basin, and unsupported results are separate evidence regimes;
- Arrhenius and Michaelis-Menten are exact compiler warm-start / same-AST evidence, not blind discovery;
- Planck and logistic remain unsupported/stretch diagnostics unless strict support and verifier contracts pass;
- repaired candidates are repair evidence only.

Remove or rewrite any sentence that could be read as blind discovery of arbitrary deep formulas, broad superiority over conventional symbolic regression, or solved status for unsupported demos. Keep the README useful and engaging, but let the verifier contract set the claims.
</action>

<verify>
<automated>python -m pytest</automated>
<automated>rg -n "not blind discovery|training loss alone|same-AST|repaired candidate|unsupported|verifier" README.md</automated>
</verify>

<done>
The README is documentation-only, accurate against the implementation contract, and preserves the project's honest claim boundaries.
</done>

## Threat Model

| Threat ID | Category | Component | Disposition | Mitigation Plan |
| --- | --- | --- | --- | --- |
| T-260419-ukc-01 | Tampering | README evidence language | mitigate | Task 3 audits claims against `docs/IMPLEMENTATION.md`, `.planning/STATE.md`, and the user's explicit constraints |
| T-260419-ukc-02 | Repudiation | README commands | mitigate | Task 2 verifies CLI command availability through automated help/list commands |
| T-260419-ukc-03 | Information disclosure | README artifact paths | accept | README references committed project artifacts and public repo files only; no secrets or private data are introduced |

## Success Criteria

- `README.md` explains the project, the EML operator, the hybrid pipeline, verifier-owned recovery, demo/evidence regimes, usage commands, and limits.
- The rewrite is engaging but not promotional: no broad blind-discovery claim, no arbitrary-deep recovery promise, and no unsupported demo promoted as solved.
- Automated verification commands in the tasks pass or any failure is recorded in the quick-task summary with the exact reason.
- Execution produces `.planning/quick/260419-ukc-rewrite-readme-to-make-it-clear-engaging/SUMMARY.md`.
