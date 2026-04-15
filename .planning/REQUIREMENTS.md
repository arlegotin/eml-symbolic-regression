# Requirements: EML Symbolic Regression Milestone v1.4

**Defined:** 2026-04-15
**Milestone:** v1.4 Recovery Performance Improvements
**Core Value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.

## Milestone v1.4 Requirements

Requirements for this milestone only. Completed v1, v1.1, v1.2, and v1.3 requirements are recorded as validated capabilities in `.planning/PROJECT.md` and `.planning/milestones/`.

### Baseline Diagnostics

- [x] **DIAG-01**: User can inspect a baseline triage summary that compares v1.3 `standard` and `showcase` failures by formula, mode, perturbation level, and recovery class.
- [x] **DIAG-02**: User can trace each target failure class back to representative raw run artifacts and optimizer/verifier metrics.
- [x] **DIAG-03**: User can run focused diagnostic subsets for blind failures, Beer-Lambert perturbation failures, and compiler/depth gates without rerunning the full campaigns.
- [x] **DIAG-04**: User can preserve the committed v1.3 baseline metrics as immutable before/after comparison inputs.

### Blind Optimizer Robustness

- [x] **BLIND-01**: User can run reproducible blind optimizer experiments over `exp`, `log`, and `radioactive_decay` with explicit seeds, budgets, losses, snap metrics, and verifier statuses.
- [x] **BLIND-02**: User can compare optimizer variants against the v1.3 blind baseline using the same verifier-owned recovery contract.
- [x] **BLIND-03**: User receives an improved default blind optimizer or benchmark budget that increases verifier recovery or materially improves post-snap loss on at least one v1.3 blind failure family without regressing existing recovered cases.
- [x] **BLIND-04**: User can read diagnostics explaining remaining blind failures, including whether the issue is soft loss, snap instability, expression depth, or verifier mismatch.

### Warm-Start Perturbation Robustness

- [ ] **PERT-01**: User can run Beer-Lambert warm-start perturbation diagnostics across the v1.3 noise levels with changed-slot counts, final snap status, and verifier status.
- [ ] **PERT-02**: User receives a warm-start training or snapping improvement that improves recovery at high perturbation or explicitly narrows the failure mechanism with reproducible evidence.
- [ ] **PERT-03**: User can distinguish same-AST return, verified-equivalent recovery, snapped-but-failed, and soft-fit-only outcomes in all perturbation diagnostics.
- [ ] **PERT-04**: User can rerun the Beer-Lambert perturbation sweep without weakening literal-constant provenance or verifier-owned recovery semantics.

### Compiler Coverage and Depth Reduction

- [ ] **COV-01**: User can inspect compiler depth, node count, rule trace, and unsupported reason diagnostics for Michaelis-Menten, logistic, Shockley, damped oscillator, and Planck formulas.
- [ ] **COV-02**: User receives at least one compiler coverage improvement that moves a v1.3 unsupported/depth-gated FOR_DEMO formula to a verified compiled EML AST or a documented lower-depth candidate.
- [ ] **COV-03**: User receives clear handling for damped oscillator's unsupported operator path, either through a supported transformation or an explicit deferred reason with tests.
- [ ] **COV-04**: User can trust that compiler improvements remain fail-closed: unsupported formulas still emit structured reasons rather than silently producing invalid EML trees.

### Before/After Campaign Evaluation

- [ ] **EVAL-01**: User can rerun `standard` and `showcase` campaigns after optimizer/compiler changes under v1.4-labeled output folders.
- [ ] **EVAL-02**: User receives a before/after comparison report that computes deltas against v1.3 `standard` and `showcase` baselines for recovery, unsupported rate, failure rate, losses, and runtime.
- [ ] **EVAL-03**: User can see whether v1.4 improved, regressed, or left unchanged each target category: blind recovery, Beer-Lambert perturbation robustness, and compiler coverage.
- [ ] **EVAL-04**: User can reproduce the comparison with one documented command from a clean checkout.
- [ ] **EVAL-05**: User can run tests that lock the diagnostic, optimizer/comparison, compiler, and campaign comparison behavior.

## Future Requirements

Deferred to later milestones.

### External Evidence and Baselines

- **FUT-16**: User can run external noisy real-world datasets after v1.4 improves synthetic/source-document campaign performance.
- **FUT-17**: User can compare EML recovery against external symbolic-regression baselines.
- **FUT-18**: User can use an interactive dashboard after static before/after reports prove the right metrics.
- **FUT-19**: User can use GPU/profiling acceleration after algorithmic improvements are validated.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Changing verifier tolerance to inflate recovery | v1.4 must improve actual recovery, not redefine success. |
| External noisy real-world datasets | The current baseline shows core optimizer/compiler gaps on controlled formulas; fix those first. |
| Claiming general symbolic-regression superiority | The milestone measures targeted improvements against current baselines only. |
| Interactive dashboards | Static comparison reports are enough for before/after validation. |
| Large GPU-specific rewrites | The current bottleneck is recovery quality, not proven hardware throughput. |
| Manual figure/report editing | Evidence must be generated from campaign artifacts. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| DIAG-01 | Phase 24 | Complete |
| DIAG-02 | Phase 24 | Complete |
| DIAG-03 | Phase 24 | Complete |
| DIAG-04 | Phase 24 | Complete |
| BLIND-01 | Phase 25 | Complete |
| BLIND-02 | Phase 25 | Complete |
| BLIND-03 | Phase 25 | Complete |
| BLIND-04 | Phase 25 | Complete |
| PERT-01 | Phase 26 | Pending |
| PERT-02 | Phase 26 | Pending |
| PERT-03 | Phase 26 | Pending |
| PERT-04 | Phase 26 | Pending |
| COV-01 | Phase 27 | Pending |
| COV-02 | Phase 27 | Pending |
| COV-03 | Phase 27 | Pending |
| COV-04 | Phase 27 | Pending |
| EVAL-01 | Phase 28 | Pending |
| EVAL-02 | Phase 28 | Pending |
| EVAL-03 | Phase 28 | Pending |
| EVAL-04 | Phase 28 | Pending |
| EVAL-05 | Phase 28 | Pending |

**Coverage:**
- v1.4 requirements: 21 total
- Mapped to phases: 21
- Unmapped: 0

---
*Requirements defined: 2026-04-15*
*Last updated: 2026-04-15 after completing Phase 25 blind optimizer improvements*
