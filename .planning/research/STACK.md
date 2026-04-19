# Technology Stack: v1.11 Paper-Strength Evidence and Figure Package

**Project:** EML Symbolic Regression  
**Research dimension:** Stack additions/changes for v1.11 paper artifacts, plots, real training reruns, ablations, and scoped baseline diagnostics  
**Researched:** 2026-04-19  
**Overall confidence:** HIGH for core dependency posture and Matplotlib recommendation; MEDIUM for optional nonlinear baseline tooling

## Recommendation

Keep the v1.11 runtime stack mostly unchanged. The existing Python/PyTorch/NumPy/SymPy/mpmath/pytest stack already supports real training, exact snapping, verification, campaign reports, JSON/CSV artifacts, and deterministic benchmark suites. The milestone should add project-owned evidence-package, ablation, baseline-diagnostic, and figure-generation modules instead of importing a new symbolic-regression engine or dataframe/reporting framework.

The only stack change I recommend for v1.11 is an optional `paper` extra with Matplotlib for publication-quality static figures:

```toml
[project.optional-dependencies]
dev = [
  "pytest>=7.4",
]
paper = [
  "matplotlib>=3.7,<4",
]
```

Use Matplotlib only for paper-facing figures, not for training or benchmark execution. Keep the current hand-written SVG campaign plots as smoke/stability artifacts, and generate the richer v1.11 figure package from locked JSON/CSV evidence after runs finish.

Default v1.11 baseline diagnostics should be implemented with NumPy and project-owned code. Do not add PySR, scikit-learn, gplearn, DEAP, pandas, seaborn, Plotly, notebooks, Rust, CUDA kernels, or a dashboard. If a phase explicitly decides to include nonlinear parametric curve-fit diagnostics, add SciPy as a separate optional `baselines` extra and keep those rows labeled as conventional curve-fit diagnostics, not symbolic-regression competitors.

Recommended v1.11 stack shape:

```text
existing benchmark/proof/campaign runs
  -> v1.11 suite presets and ablation case metadata
  -> locked JSON/CSV evidence tables
  -> optional NumPy conventional-baseline diagnostics
  -> Matplotlib paper figure builder
  -> v1.11 paper package with source locks, figures, tables, and claim boundaries
```

## Local Baseline

Observed locally on 2026-04-19:

| Tool | Local / Project Version | v1.11 Recommendation | Confidence |
|------|-------------------------|----------------------|------------|
| Python | 3.11.5, `>=3.11,<3.13` in `pyproject.toml` | Keep as core | HIGH |
| PyTorch | 2.10.0, `torch>=2.10`; CUDA unavailable locally | Keep as core training stack | HIGH |
| NumPy | 1.26.4, `numpy>=1.26` | Keep as core; use for baseline diagnostics and table source arrays | HIGH |
| SymPy | 1.14.0, `sympy>=1.14` | Keep as compiler/symbolic export layer | HIGH |
| mpmath | 1.3.0, `mpmath>=1.3` | Keep as high-precision verifier | HIGH |
| pytest | 7.4.0, dev extra | Keep; add tests for paper package, ablations, figures, and baseline diagnostics | HIGH |
| Matplotlib | 3.7.2 installed, not declared | Add optional `paper` extra | HIGH |
| pandas | 2.0.3 installed, not declared | Do not add | HIGH |
| SciPy | 1.16.1 installed, not declared | Do not add by default; optional only for explicit nonlinear curve-fit diagnostics | MEDIUM |
| scikit-learn | 1.3.0 installed, not declared | Do not add | HIGH |
| seaborn | 0.12.2 installed, not declared | Do not add | HIGH |
| Plotly | 5.9.0 installed, not declared | Do not add | HIGH |

Local Matplotlib imported, but emitted a cache warning because `/Users/artemlegotin/.matplotlib` is not writable. Any v1.11 Matplotlib command should set `MPLCONFIGDIR` to a writable artifact/temp directory before importing Matplotlib, for example:

```python
import os
from pathlib import Path

def configure_matplotlib_cache(output_dir: Path) -> None:
    os.environ.setdefault("MPLCONFIGDIR", str(output_dir / ".matplotlib-cache"))
```

Then force a file backend before importing `pyplot`:

```python
import matplotlib

matplotlib.use("Agg")
```

## Recommended Additions

### Optional `paper` Extra: Matplotlib

| Technology | Version Policy | Purpose | Why |
|------------|----------------|---------|-----|
| Matplotlib | `>=3.7,<4`; local 3.7.2 works | Static paper figures as SVG/PDF/PNG | Official docs support non-interactive hardcopy backends for PNG/SVG/PDF, and `savefig` writes image/vector outputs. This is the smallest justified plotting addition for multi-panel publication figures, uncertainty/error-bar plots, and consistent typography. |

Integration points:

| Module | Change |
|--------|--------|
| `pyproject.toml` | Add optional `paper` extra only. Do not put Matplotlib in mandatory runtime dependencies. |
| `src/eml_symbolic_regression/paper_figures.py` | New module that reads locked JSON/CSV evidence and writes `.svg`, `.pdf`, and optional high-DPI `.png` figures. |
| `src/eml_symbolic_regression/cli.py` | Add a paper-facing command such as `paper-figures` or fold it into `paper-package-v1.11`. |
| `src/eml_symbolic_regression/campaign.py` | Keep existing deterministic SVG plots for campaign reports; optionally call `paper_figures.py` only for v1.11 package output. |
| `tests/test_paper_figures.py` | Smoke-test figure generation with tiny fixture evidence and assert expected files exist and are non-empty. |

Implementation rules:

- Use `Agg` / non-interactive output only.
- Set `MPLCONFIGDIR` before importing `matplotlib.pyplot`.
- Save source tables next to every figure as `.json` or `.csv`.
- Save SVG and PDF for manuscript use; PNG is convenience only.
- Do not make Matplotlib imports happen on normal CLI startup unless the figure command is invoked.

### Project-Owned v1.11 Evidence Package

Do not mutate the v1.9 raw-hybrid paper package in place. Add a new package writer for v1.11, or generalize `raw_hybrid_paper.py` with a new preset/schema while preserving v1.9 regression tests.

Recommended module:

```text
src/eml_symbolic_regression/paper_package.py
```

Recommended output root:

```text
artifacts/paper/v1.11/evidence-package/
```

Recommended generated artifacts:

| Artifact | Purpose |
|----------|---------|
| `manifest.json` | Schema, command, code version, environment, source list, output paths |
| `source-locks.json` | SHA-256 locks for all training, ablation, baseline, v1.10 logistic/Planck, and figure source files |
| `scientific-law-table.json/.csv/.md` | Paper table refreshed with v1.10 logistic/Planck diagnostics |
| `regime-summary.json/.md` | Separate pure-blind, scaffolded, warm-start, same-AST, perturbed, repair/refit, and unsupported regimes |
| `ablation-summary.json/.csv/.md` | Compiler motif, macro depth, warm-start-vs-blind, pool/repair/refit deltas |
| `baseline-diagnostics.json/.csv/.md` | Conventional diagnostics, clearly scoped and not a broad SR benchmark |
| `figure-index.json/.md` | Figure IDs, captions, source files, source hashes, and claim boundaries |
| `claim-boundaries.md` | Explicit no-overclaim rules carried forward from v1.9 |

Keep `raw_hybrid_paper.py` as the v1.9 compatibility writer unless refactoring is necessary. v1.11 should have its own preset id, for example `v1.11-paper-evidence-package`.

### Benchmark and Campaign Suite Additions

No new training framework is needed. Add v1.11 suites/presets to existing `benchmark.py` and `campaign.py`.

Recommended benchmark suite families:

| Suite Family | Stack Used | Purpose |
|--------------|------------|---------|
| `v1.11-training-refresh-*` | existing PyTorch optimizer, verifier, JSON artifacts | Claim-safe reruns for shallow pure-blind, scaffolded, warm-start/same-AST, perturbed-basin, and focused logistic/Planck probes |
| `v1.11-ablation-*` | existing compiler diagnostics, benchmark metadata, verifier | Measure motif on/off, macro depth deltas, warm-start versus blind, candidate-pool repair/refit behavior |
| `v1.11-baseline-diagnostics` | NumPy project-owned diagnostics, optional SciPy only if explicitly chosen | Scoped conventional baselines over the same deterministic train/held-out/extrapolation splits |
| `v1.11-paper-package-sources` | JSON/CSV source locks | Stable inputs for the final paper package |

Do not add parallel execution infrastructure unless a phase proves it is needed. Current suite sizes are small enough that deterministic sequential runs are easier to audit. If later needed, use Python `multiprocessing` already imported in `benchmark.py`, with explicit per-run artifact isolation and source locks.

### NumPy-First Baseline Diagnostics

Implement conventional baselines as a local module, not a third-party symbolic-regression dependency:

```text
src/eml_symbolic_regression/baselines.py
```

Default baselines should use NumPy only:

| Baseline | NumPy API | Scope |
|----------|-----------|-------|
| Mean predictor | `np.mean` | sanity floor |
| Linear least squares | `np.linalg.lstsq` | simple trend baseline |
| Low-degree polynomial | `numpy.polynomial.Polynomial.fit` preferred over old `np.polyfit` | curve-fit diagnostic, not formula recovery |
| Log-linear transforms | `np.log`, `np.linalg.lstsq` with domain checks | exp/decay diagnostics on positive targets only |
| Known-form residual evaluator | existing demo formulas and splits | compare held-out/extrapolation residual scale without claiming discovery |

Baseline artifact schema should include:

- baseline id and type,
- formula id and split manifest,
- parameter count,
- fitted coefficients,
- train, held-out, extrapolation MSE/MAE/max error,
- domain exclusions,
- failure reason if a transform is invalid,
- package versions used.

Only add SciPy if v1.11 explicitly needs nonlinear parametric curve fits such as bounded logistic or Planck-shaped templates. If added, keep it optional:

```toml
[project.optional-dependencies]
baselines = [
  "scipy>=1.16",
]
```

SciPy curve-fit rows must record initial guesses, bounds, convergence status, warnings, covariance condition diagnostics, and the fact that these are parametric conventional fits, not symbolic-recovery competitors.

### Ablation Support

Ablations should be suite metadata and local code switches, not new dependencies.

Recommended switches:

| Ablation | Integration Point | Output |
|----------|-------------------|--------|
| Motifs on/off | `CompilerConfig` / compiler macro layer | compile depth, node count, macro hits, unsupported reason |
| Strict vs relaxed depth diagnostics | existing compile diagnostics with explicit gate labels | no silent promotion |
| Warm-start vs blind | `BenchmarkCase.start_mode`, same formula/seed/split | regime-separated recovery table |
| Candidate-pool repair/refit | existing `repair` and refit metadata in benchmark payloads | weak-dominance/no-regression table |
| Logistic/Planck probes | existing v1.10 suites plus v1.11 focused probes | unsupported diagnostics unless verifier contract passes |

If current compiler config cannot disable individual macros, add project-owned flags such as:

```python
CompilerConfig(enabled_macros=("direct_division_template", "saturation_ratio_template"))
```

Avoid monkeypatching or environment-variable-only ablations; they are hard to lock and reproduce in artifacts.

## What Not To Add

| Candidate Addition | Recommendation | Why |
|-------------------|----------------|-----|
| PySR / SymbolicRegression.jl | Do not add for v1.11 | This milestone is paper-strength evidence for the EML hybrid pipeline, not a matched-budget SR competition. |
| gplearn / DEAP / genetic programming frameworks | Do not add | Would create a broad baseline benchmark surface and distract from claim-safe EML evidence. |
| scikit-learn | Do not add | NumPy is enough for the scoped conventional baseline diagnostics; sklearn would add ML pipeline concepts that are not needed. |
| pandas | Do not add | Existing reports already write CSV/JSON with stdlib; table schemas are explicit and small. |
| seaborn | Do not add | Matplotlib is sufficient and keeps styling deterministic. |
| Plotly / dashboards | Do not add | v1.11 asks for paper artifacts, not interactive exploration. |
| Jupyter notebooks | Do not add as required artifacts | Notebook state is harder to lock than CLI-generated JSON/CSV/figures. |
| LaTeX/PGF dependency | Defer | Matplotlib SVG/PDF is enough; manuscript-specific LaTeX integration should not block reproducible evidence. |
| Inkscape/ImageMagick conversion | Do not add | Matplotlib can emit SVG/PDF/PNG directly. |
| Rust / PyO3 | Defer | Useful for future exhaustive verification speed, not needed for v1.11 evidence packaging. |
| Custom CUDA kernels | Do not add | CUDA is unavailable locally and current constraints explicitly defer kernel work. |
| Ray/Dask/joblib | Do not add | Deterministic, inspectable sequential campaigns are preferable until run time becomes a measured blocker. |

## Integration Plan

### Phase 1: Package and Source Locks

Add a v1.11 paper package writer that consumes existing artifacts and new v1.11 outputs. It should refresh the scientific-law table with v1.10 logistic and Planck diagnostics instead of stale v1.6 depths.

Touch points:

- `raw_hybrid_paper.py` only if generalized safely.
- Prefer new `paper_package.py`.
- Add CLI command, for example:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli paper-package-v1.11 --output-dir artifacts/paper/v1.11/evidence-package --require-existing
```

### Phase 2: Training and Ablation Suites

Extend `benchmark.py` with v1.11 suite ids and metadata. Reuse existing `BenchmarkCase`, `OptimizerBudget`, `BenchmarkRepairConfig`, and proof contract fields. Add only small config fields needed for macro ablations.

Touch points:

- `BUILTIN_SUITES`
- `builtin_suite()`
- aggregate evidence grouping only if a new ablation dimension needs a table
- tests mirroring existing focused v1.9/v1.10 suite tests

### Phase 3: Baseline Diagnostics

Add NumPy-first `baselines.py` and a CLI/report path. Baselines should read the same demo split contracts and emit locked artifacts. They should not participate in `claim_status == "recovered"`.

Recommended CLI:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli baseline-diagnostics v1.11 --output-dir artifacts/baselines/v1.11
```

### Phase 4: Paper Figures

Add Matplotlib-backed figure generation after source tables exist. Figures should be deterministic, file-backed, and sourced from locked JSON/CSV tables.

Recommended CLI:

```bash
MPLCONFIGDIR=artifacts/paper/v1.11/evidence-package/.matplotlib-cache \
PYTHONPATH=src python -m eml_symbolic_regression.cli paper-figures \
  --source artifacts/paper/v1.11/evidence-package/manifest.json \
  --output-dir artifacts/paper/v1.11/evidence-package/figures
```

Recommended figure outputs:

| Figure | Source |
|--------|--------|
| Regime recovery by evidence class | `regime-summary.json` |
| Blind depth degradation | proof depth-curve aggregate |
| Scientific-law support table plot | `scientific-law-table.csv` |
| Motif depth deltas | compiler ablation summary |
| Warm-start versus blind outcomes | v1.11 training refresh aggregate |
| Candidate pool / repair / refit behavior | ablation summary |
| Failure taxonomy | campaign/aggregate failure rows |

## Dependency Policy

Recommended `pyproject.toml` after v1.11 stack change:

```toml
[project]
dependencies = [
  "torch>=2.10",
  "numpy>=1.26",
  "sympy>=1.14",
  "mpmath>=1.3",
]

[project.optional-dependencies]
dev = [
  "pytest>=7.4",
]
paper = [
  "matplotlib>=3.7,<4",
]
```

Conditional only if nonlinear curve-fit baselines become a phase requirement:

```toml
[project.optional-dependencies]
baselines = [
  "scipy>=1.16",
]
```

Do not combine `paper` and `baselines` into the default install. Paper readers should be able to regenerate evidence tables without a plotting stack, and core users should be able to run EML training without baseline diagnostics.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| No new core training dependencies | HIGH | Existing `benchmark.py`, `campaign.py`, `cli.py`, and docs already support real PyTorch training, verification, JSON/CSV reports, and campaign artifacts. |
| Matplotlib as optional paper extra | HIGH | Local 3.7.2 is installed; official docs support non-interactive file backends and `savefig` outputs for SVG/PDF/PNG. |
| NumPy-first baseline diagnostics | HIGH | NumPy already installed and declared; `lstsq` and polynomial fitting cover scoped conventional diagnostics without importing ML/SR frameworks. |
| Avoiding pandas/seaborn/Plotly | HIGH | Existing data tables are small explicit schemas; interactive or dataframe stacks add more dependency surface than value. |
| Optional SciPy for nonlinear fits | MEDIUM | SciPy is locally installed and suitable for curve fitting, but adding it should be a phase-specific choice because it is a heavier dependency and can create overclaim risk. |
| No parallel/distributed runner | MEDIUM | Sequential deterministic runs are preferable now; revisit only if v1.11 evidence generation time becomes a measured blocker. |

## Sources

- `.planning/PROJECT.md` - v1.11 scope: paper-strength evidence, real claim-safe training, ablations, plot-rich artifacts, scoped baselines, no overclaiming.
- `.planning/STATE.md` - v1.11 context and note that external baseline dependencies may be unavailable.
- `README.md` - existing CLI, benchmark, campaign, paper package, proof bundle, and interpretation contracts.
- `docs/IMPLEMENTATION.md` - current module boundaries, verifier-owned recovery contract, benchmark/campaign artifacts, raw-hybrid paper package contract.
- `src/eml_symbolic_regression/benchmark.py` - current suite schema, v1.10 logistic/Planck focused suites, optimizer budget, proof contract validation, artifact payloads.
- `src/eml_symbolic_regression/campaign.py` - current campaign presets, CSV exports, hand-written SVG plots, manifest/report structure.
- `src/eml_symbolic_regression/cli.py` - current benchmark, campaign, diagnostics, proof, paper-decision, and raw-hybrid-paper commands.
- `src/eml_symbolic_regression/raw_hybrid_paper.py` - current v1.9 paper package synthesis and source-lock pattern.
- `pyproject.toml` - current mandatory dependencies and dev extra.
- Local environment probe on 2026-04-19 - Python 3.11.5, PyTorch 2.10.0, NumPy 1.26.4, SymPy 1.14.0, mpmath 1.3.0, pytest 7.4.0, Matplotlib 3.7.2, pandas 2.0.3, SciPy 1.16.1, scikit-learn 1.3.0, seaborn 0.12.2, Plotly 5.9.0, CUDA unavailable.
- Matplotlib backend docs: https://matplotlib.org/stable/users/explain/figure/backends.html
- Matplotlib `savefig` docs: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html
- NumPy `linalg.lstsq` docs: https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html
- NumPy polynomial fitting docs: https://numpy.org/doc/stable/reference/generated/numpy.polyfit.html
- SciPy `curve_fit` docs, conditional only: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html

Context7 MCP tools were not available in this environment. The CLI fallback command for Context7 was attempted for Matplotlib documentation but produced no output before being stopped; official documentation was used instead.
