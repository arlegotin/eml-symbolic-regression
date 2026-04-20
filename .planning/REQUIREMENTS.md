# Requirements: EML Symbolic Regression v1.13

**Defined:** 2026-04-20
**Core Value:** Recover verified, human-readable elementary formulas from data using the paper's uniform EML tree representation.

## v1.13 Requirements

### Clean-Room Reproduction

- [x] **REPRO-01**: Maintainer can run one documented command from an empty checkout to rebuild every publication figure, table, aggregate, manifest, and source-lock artifact.
- [x] **REPRO-02**: Maintainer can execute the rebuild in a locked environment using committed lockfile and container support.
- [x] **REPRO-03**: Publication reproduction does not require preexisting generated artifacts or `--require-existing` inputs.
- [x] **REPRO-04**: Publication manifests record immutable provenance for every generated artifact, including git revision, command, environment identity, input hashes, output hashes, and generated-at timestamp.
- [x] **REPRO-05**: Publication artifacts fail validation if placeholder metadata such as `1970-01-01T00:00:00+00:00` or `"snapshot"` appears outside explicitly labeled deterministic-test fixtures.

### Automated Tests and CI

- [ ] **TEST-01**: Contributor can run unit tests covering EML semantics, complex principal-branch behavior, compiler output, verifier contracts, and artifact manifest validation.
- [ ] **TEST-02**: Contributor can run integration tests covering a minimal evidence-regression pipeline from training through artifact generation.
- [ ] **TEST-03**: CI runs the unit suite, selected integration/evidence smoke tests, clean-room reproduction smoke, and public snapshot checks on relevant branch and pull-request events.
- [ ] **TEST-04**: CI preserves branch discipline by validating that `dev` has full source/test coverage and that `main` receives only the intended public snapshot contents.

### Verifier and Split Discipline

- [x] **VERIF-01**: Verifier attempts symbolic equivalence or targeted simplification for candidates where SymPy/exported expression forms support it.
- [x] **VERIF-02**: Verifier labels every accepted candidate by evidence level, separating symbolic proof, dense numeric falsification, interval/certificate checks, and final confirmation.
- [x] **VERIF-03**: Verifier checks non-symbolic candidates on fresh dense randomized points that are not reused from training, held-out, extrapolation, or selection grids.
- [x] **VERIF-04**: Verifier probes adversarial domain points, near singularities, and complex branch-cut neighborhoods relevant to each candidate's intended domain.
- [x] **VERIF-05**: Verifier reports interval or certificate-style evidence on the intended real domain where feasible, and records unsupported certificate status otherwise.
- [x] **SPLIT-01**: Candidate generation, candidate ranking, and exact-candidate cleanup do not use final confirmation data.
- [x] **SPLIT-02**: Final confirmation data is generated or revealed only after candidate selection unless symbolic equivalence has already been established.
- [x] **SPLIT-03**: Artifacts distinguish training, selection, held-out diagnostic, extrapolation diagnostic, verifier, and final-confirmation metrics.

### Training and Verified Semantics

- [x] **SEM-01**: Maintainer can run a faithful-semantics training mode whose optimized objective matches verifier semantics on supported domains, or a documented fallback explains why it is unavailable.
- [x] **SEM-02**: Maintainer can run clamp/log-guard ablations that quantify whether surrogate training semantics create spurious recoveries.
- [x] **SEM-03**: Publication artifacts report clamp, guard, NaN/Inf, branch, and post-snap mismatch diagnostics for every training run.
- [x] **SEM-04**: Scientific-law claims include real-domain and branch-validity certificates or explicit unsupported-certificate labels.

### Benchmark Tracks and Evidence Breadth

- [ ] **TRACK-01**: Every publication benchmark target runs in a paper-faithful basis-only track using only the declared EML basis and allowed variables.
- [ ] **TRACK-02**: Every publication benchmark target runs in a literal-constant-augmented track with constants policy, literal catalog, and warm-start/scaffold status explicit in artifacts.
- [ ] **TRACK-03**: Aggregate reports keep basis-only and literal-constant-augmented denominators separate.
- [ ] **BASE-01**: Maintainer can run EML and conventional symbolic-regression baselines through one standardized harness using identical datasets, seeds, budgets, constants policies, and blind/warm-start conditions.
- [ ] **BASE-02**: Baseline integrations are dependency-checked, source-locked, fail-closed, and reported without changing EML recovery denominators.
- [ ] **DATA-01**: Benchmark datasets include noisy synthetic sweeps, parameter-identifiability stress tests, multivariable cases, unit-aware formulations, and real datasets with independent test splits.
- [ ] **DATA-02**: Dataset manifests record generator or source, units, noise policy, split policy, domain constraints, and whether the target is synthetic, semi-synthetic, or real.

### Publication Package and Release

- [ ] **PUB-01**: Maintainer can run the full v1.13 training/evidence campaign and produce all required publication artifacts in the committed artifact layout.
- [ ] **PUB-02**: Publication package includes a root manifest linking generated artifacts, source locks, claim audit, reproduction command, environment lock/container identity, and branch provenance.
- [ ] **PUB-03**: Claim audit blocks publication if any recovery claim lacks verifier evidence, final confirmation status, constants-track label, baseline context, or source lock.
- [ ] **PUB-04**: `main` branch receives the final public code, tests, CI, reproduction entrypoints, and selected artifacts after the full rebuild passes on `dev`.

## Future Requirements

### Formal Assurance

- **FORMAL-01**: Candidate equivalence can be discharged by a theorem prover for a selected subset of expressions.
- **FORMAL-02**: Interval/certificate generation covers all supported elementary operators and all benchmark domains without unsupported-certificate fallbacks.

### Acceleration

- **ACCEL-01**: Rust or CUDA acceleration can rebuild publication campaigns faster without changing exact semantics or artifact provenance.

### Manuscript Packaging

- **MS-01**: The paper draft expands into venue-specific prose, related work, bibliography, appendices, and submission assets after v1.13 validation passes.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Broad blind symbolic-regression superiority claims | The milestone can claim only the evidence generated by the standardized harness and matched baselines. |
| New one-off formula recognizers | Compiler/search improvements must remain structural and reusable, not target-name branches. |
| Full theorem-prover equivalence as a release blocker | Layered symbolic/numeric/certificate validation is required now; formal proof is future work unless deliberately scoped. |
| Web UI or dashboards | Publication credibility depends on reproducible CLI/package artifacts and CI first. |
| Rewriting archived v1.4-v1.12 evidence | Historical artifacts remain comparison anchors; v1.13 creates new source-locked evidence instead. |
| Publishing `main` before the full rebuild passes | Public branch updates happen only after the release gate validates code, tests, artifacts, and provenance. |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| REPRO-01 | Phase 69 | Complete |
| REPRO-02 | Phase 69 | Complete |
| REPRO-03 | Phase 69 | Complete |
| REPRO-04 | Phase 69 | Complete |
| REPRO-05 | Phase 69 | Complete |
| TEST-01 | Phase 72 | Pending |
| TEST-02 | Phase 72 | Pending |
| TEST-03 | Phase 72 | Pending |
| TEST-04 | Phase 72 | Pending |
| VERIF-01 | Phase 70 | Complete |
| VERIF-02 | Phase 70 | Complete |
| VERIF-03 | Phase 70 | Complete |
| VERIF-04 | Phase 70 | Complete |
| VERIF-05 | Phase 70 | Complete |
| SPLIT-01 | Phase 70 | Complete |
| SPLIT-02 | Phase 70 | Complete |
| SPLIT-03 | Phase 70 | Complete |
| SEM-01 | Phase 71 | Complete |
| SEM-02 | Phase 71 | Complete |
| SEM-03 | Phase 71 | Complete |
| SEM-04 | Phase 71 | Complete |
| TRACK-01 | Phase 73 | Pending |
| TRACK-02 | Phase 73 | Pending |
| TRACK-03 | Phase 73 | Pending |
| BASE-01 | Phase 75 | Pending |
| BASE-02 | Phase 75 | Pending |
| DATA-01 | Phase 74 | Pending |
| DATA-02 | Phase 74 | Pending |
| PUB-01 | Phase 76 | Pending |
| PUB-02 | Phase 76 | Pending |
| PUB-03 | Phase 76 | Pending |
| PUB-04 | Phase 76 | Pending |

**Coverage:**
- v1.13 requirements: 32 total
- Mapped to phases: 32
- Unmapped: 0

---
*Requirements defined: 2026-04-20*
*Last updated: 2026-04-20 after roadmap traceability*
