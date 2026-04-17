---
phase: 53-raw-hybrid-paper-campaign-and-claim-package
verified: 2026-04-17T17:14:08Z
status: passed
score: 5/5 must-haves verified
overrides_applied: 0
---

# Phase 53: Raw-Hybrid Paper Campaign and Claim Package Verification Report

**Phase Goal:** Generate the paper-facing raw-hybrid suite, reports, tables, claim boundaries, and docs after the new evidence exists.
**Verified:** 2026-04-17T17:14:08Z
**Status:** passed
**Re-verification:** No - initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | A raw-hybrid paper suite includes shallow blind boundaries, perturbed basin evidence, Beer-Lambert, Shockley, Arrhenius, and Michaelis diagnostics. | VERIFIED | `default_raw_hybrid_sources()` locks v1.6 proof aggregates, v1.9 Arrhenius/Michaelis evidence, repair evidence, v1.8 centered diagnostics, and v1.6 Beer-Lambert/Shockley/Planck/logistic/historical Michaelis runs. The committed package has 20 source locks and 7 scientific rows. |
| 2 | Reports keep pure blind, scaffolded, compile-only, warm-start, same-AST return, repaired, refit, and perturbed-basin regimes separate. | VERIFIED | `REGIME_KEYS` defines all eight regimes, `build_regime_summary()` writes structured buckets, and artifact checks found totals for all eight: pure_blind 25, scaffolded 20, compile_only 2, warm_start 7, same_ast_return 24, repaired 8, refit 36, perturbed_basin 23. |
| 3 | Scientific-law tables include formula, compile support, depth, macro hits, warm-start status, verifier status, and artifact paths. | VERIFIED | `SCIENTIFIC_LAW_COLUMNS` includes every required field. `scientific-law-table.json/.csv/.md` contain Beer-Lambert, Shockley, Arrhenius, Michaelis-Menten, Planck diagnostic, logistic diagnostic, and historical Michaelis diagnostic rows. |
| 4 | Centered-family material is framed as negative diagnostic evidence with same-family witness caveats. | VERIFIED | `centered-negative-diagnostics.md` says centered rows are negative diagnostic evidence, not a claim that centered families cannot work, and keeps the same-family witness caveat active. Forbidden claim wording is absent from generated reports. |
| 5 | README/docs updates cite successful artifacts and avoid blind-discovery overclaims. | VERIFIED | README and implementation docs cite `artifacts/paper/v1.9/raw-hybrid/` after the package exists, list package outputs, state warm-start/same-AST/etc. evidence is not blind discovery, and keep centered-family claims under the witness caveat. |

**Score:** 5/5 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/eml_symbolic_regression/raw_hybrid_paper.py` | Package writer, source validation, locks, reports, tables, claim boundaries | VERIFIED | Exists, 872 lines. Writes nine outputs, validates sources, computes SHA-256 locks, and renders regime/table/claim artifacts. |
| `src/eml_symbolic_regression/cli.py` | `raw-hybrid-paper` CLI entry point | VERIFIED | Imports and calls `write_raw_hybrid_paper_package`; parser exposes `--output-dir`, `--require-existing`/`--allow-missing`, and `--overwrite`. |
| `tests/test_raw_hybrid_paper.py` | Unit/contract tests | VERIFIED | 318 lines covering source validation, source locks, manifest, regimes, law rows, centered caveats, CLI parsing, overwrite safety, and shell quoting. |
| `tests/test_raw_hybrid_paper_regression.py` | File-backed package regression locks | VERIFIED | 170 lines reading committed package files, recomputing source hashes, locking regimes/rows, and checking forbidden wording. |
| `artifacts/paper/v1.9/raw-hybrid/manifest.json` | Package manifest and reproduction command | VERIFIED | Schema `eml.raw_hybrid_paper.v1`, preset `v1.9-raw-hybrid-paper`, 7 scientific rows, command includes `raw-hybrid-paper --require-existing --overwrite`. |
| `artifacts/paper/v1.9/raw-hybrid/source-locks.json` | Source SHA-256 locks | VERIFIED | Structural check recomputed all 20 source hashes successfully. |
| `artifacts/paper/v1.9/raw-hybrid/regime-summary.json` | Structured regime buckets | VERIFIED | Contains all eight required regime keys with non-empty key buckets and pure-blind rows constrained to `start_mode == "blind"`. |
| `artifacts/paper/v1.9/raw-hybrid/raw-hybrid-report.md` | Human-readable regime-separated report | VERIFIED | Contains all eight report sections and per-run source/mode/evidence/status/artifact rows. Note: `gsd-tools verify artifacts` had one case-sensitive marker miss for literal `Regime`; manual and regression checks verify the intended regime separation. |
| `artifacts/paper/v1.9/raw-hybrid/scientific-law-table.json` | Machine-readable scientific-law table | VERIFIED | Contains required columns and required law rows. |
| `artifacts/paper/v1.9/raw-hybrid/scientific-law-table.csv` | CSV scientific-law table | VERIFIED | Header includes all required columns. |
| `artifacts/paper/v1.9/raw-hybrid/scientific-law-table.md` | Markdown scientific-law table | VERIFIED | Lists required law rows, compile support/depth, macro hits, statuses, regimes, and artifact paths. |
| `artifacts/paper/v1.9/raw-hybrid/claim-boundaries.md` | Claim-boundary language | VERIFIED | States warm-start, same-AST, scaffolded, repaired, refit, compile-only, and perturbed-basin evidence is not blind discovery. |
| `artifacts/paper/v1.9/raw-hybrid/centered-negative-diagnostics.md` | Centered-family caveat report | VERIFIED | Reports centered evidence as negative diagnostics with same-family witness caveat and no impossibility claim. |
| `README.md` | User-facing package command and claim-safe summary | VERIFIED | Documents the command and package root, and avoids blind-discovery overclaims. |
| `docs/IMPLEMENTATION.md` | Implementation package contract docs | VERIFIED | Documents source locks, artifact inventory, scientific-law columns, claim boundaries, and centered caveat. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `src/eml_symbolic_regression/cli.py` | `src/eml_symbolic_regression/raw_hybrid_paper.py` | Import and call `write_raw_hybrid_paper_package` | WIRED | `gsd-tools verify key-links` passed for 53-01. |
| `src/eml_symbolic_regression/raw_hybrid_paper.py` | v1.6 proof aggregate artifacts | Required source definitions | WIRED | Source list includes shallow pure-blind, scaffolded, basin, basin-probe, and depth-curve aggregates. |
| `src/eml_symbolic_regression/raw_hybrid_paper.py` | v1.9 Arrhenius/Michaelis evidence | Scientific-law source definitions | WIRED | Source list includes focused aggregate and run files for both laws. |
| `src/eml_symbolic_regression/raw_hybrid_paper.py` | v1.8 centered decision artifacts | Centered diagnostic source definitions | WIRED | Source list includes decision JSON/Markdown and completeness boundary. |
| `artifacts/paper/v1.9/raw-hybrid/manifest.json` | `source-locks.json` | Manifest output path and `source_locks` field | WIRED | `gsd-tools verify key-links` passed for 53-02. |
| `scientific-law-table.json` | Arrhenius/Michaelis run artifacts | `artifact_path` rows | WIRED | Structural check confirmed paths and required row fields. |
| README/docs/tests | Generated package artifacts | Documented paths and file-backed regression reads | WIRED | `gsd-tools verify key-links` passed for 53-03. |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `raw_hybrid_paper.py` package writer | `sources`, `source_payloads`, `regime_summary`, `law_rows`, `centered_diagnostics` | `default_raw_hybrid_sources()` -> `_load_sources()` over committed JSON/Markdown artifacts | Yes | FLOWING - required sources fail closed; locks hash real files. |
| `regime-summary.json` and `raw-hybrid-report.md` | Regime buckets and run rows | `_source_runs()` / `_regime_run_row()` / `_regimes_for_run()` from proof/campaign/repair aggregates | Yes | FLOWING - structured check found non-empty required buckets and pure-blind exclusions. |
| `scientific-law-table.*` | Law row fields | Scientific-law run JSON payloads and declared `RawHybridSource` metadata | Yes | FLOWING - required rows include formulas, compile support/depth, macro hits, warm-start/verifier status, regime, and artifact path. |
| `source-locks.json` | Source lock rows | `_source_lock()` over each declared source path | Yes | FLOWING - recomputed 20 SHA-256 hashes matched. |
| `centered-negative-diagnostics.md` | Centered decision summary/operator groups | v1.8 `decision-memo.json` | Yes | FLOWING - report includes raw/best-centered recovery rates and operator rows. |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Raw-hybrid unit and file-backed regression tests pass | `PYTHONPATH=src python -m pytest tests/test_raw_hybrid_paper.py tests/test_raw_hybrid_paper_regression.py -q` | `16 passed in 1.93s` | PASS |
| Existing paper-decision/campaign shell-quoting tests still pass | `PYTHONPATH=src python -m pytest tests/test_paper_decision.py tests/test_campaign.py::test_reproduction_command_quotes_shell_sensitive_values -q` | `4 passed in 0.93s` | PASS |
| CLI can generate package from required evidence | `PYTHONPATH=src python -m eml_symbolic_regression.cli raw-hybrid-paper --output-dir /tmp/eml-raw-hybrid-verify --require-existing --overwrite` | Wrote manifest, report, law table, claim boundaries, and source locks | PASS |
| Committed package structure, locks, rows, regimes, and claim wording validate | `python -c <structural raw-hybrid package checks>` | `structural checks passed: 20 source locks, 7 scientific rows` | PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| RHY-01 | 53-01, 53-02 | Developer can run a paper-facing raw-hybrid suite/preset including required evidence categories. | SATISFIED | CLI command exists, smoke generation passed, package locks shallow blind, perturbed basin, Beer-Lambert, Shockley, Arrhenius, and Michaelis sources. |
| RHY-02 | 53-01, 53-02, 53-03 | Reports keep pure blind, scaffolded, compile-only, warm-start, same-AST return, repaired, refit, and perturbed-basin regimes separate. | SATISFIED | `regime-summary.json` has all eight structured buckets; report has all eight sections; regression tests guard bucket leakage. |
| RHY-03 | 53-01, 53-02, 53-03 | Scientific-law tables include formula, compile support/depth, macro hits, warm-start status, verifier status, and artifact path. | SATISFIED | Scientific-law JSON/CSV/Markdown all include required columns; rows cover required laws and diagnostics. |
| RHY-04 | 53-01, 53-02, 53-03 | Centered-family results are only negative diagnostics with same-family witness caveat. | SATISFIED | Centered diagnostics and docs use negative diagnostic/witness caveat wording and avoid impossibility claims. |
| RHY-05 | 53-03 | README or implementation docs updated only after successful artifacts exist, avoiding warm-start-as-blind-discovery claims. | SATISFIED | README and docs cite the package root and artifacts, state exact warm-start/same-AST evidence is not blind discovery, and regression tests forbid overclaim phrases. |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `tests/test_raw_hybrid_paper_regression.py` | 78 | Forbidden claim phrases appear in `FORBIDDEN_PHRASES` deny-list | Info | Intentional regression guard; generated report/claim/centered files do not contain those phrases. |
| `src/eml_symbolic_regression/raw_hybrid_paper.py` | 369, 504, 660, 805 | Empty list/dict initialization or fallback return | Info | Normal collection initialization/fallback behavior; data-flow trace confirms package outputs are populated from source artifacts. |

### Human Verification Required

None. This phase produces package/code/docs artifacts without visual, real-time, external-service, or UX flows requiring human-only validation.

### Gaps Summary

No blocking gaps found. All five RHY requirements are satisfied by source code, generated artifacts, documentation, regression tests, and focused behavior checks.

One non-blocking tool note: the generic GSD artifact checker reported `raw-hybrid-report.md` missing the exact uppercase marker `Regime` from the plan artifact hint. The actual report contains the required eight regime sections, the structured JSON regime buckets pass direct validation, and regression tests lock the separation behavior, so this is not a goal gap.

---

_Verified: 2026-04-17T17:14:08Z_
_Verifier: Claude (gsd-verifier)_
