# Domain Pitfalls: v1.11 Paper-Strength Evidence and Figure Package

**Domain:** Paper evidence campaigns, ablations, baseline diagnostics, and publication figures for EML symbolic regression  
**Project:** EML Symbolic Regression  
**Researched:** 2026-04-19  
**Overall confidence:** HIGH for claim-boundary, verifier, unsupported-status, and plotting/reporting risks grounded in existing project artifacts; MEDIUM for phase sequencing because the v1.11 roadmap does not exist yet.

## Research Basis

v1.11 is not an algorithmic rescue milestone. The project already has verifier-owned recovery, regime-separated proof artifacts, raw-hybrid paper packaging, centered-family negative diagnostics, and focused v1.10 logistic/Planck compiler-shortening artifacts.

The current evidence base says:

- Pure blind recovery is measured but weak beyond shallow depths: v1.6 reports 2/18 shallow pure-blind proof recovery and 0/2 blind recovery at depths 4, 5, and 6, while perturbed true-tree basin recovery is 23/23.
- Scaffolded, same-AST, warm-start, repair, refit, compile-only, and perturbed-basin evidence are useful but explicitly not blind discovery.
- Centered-family evidence is negative under the local v1.8 setup, but that is not a proof that centered families cannot work.
- Logistic and Planck improved as compiler diagnostics in v1.10, but both focused aggregates still show `unsupported: 1`, `verifier_recovered: 0`, and `verifier_recovery_rate: 0.000`.
- v1.11 must update the paper package with current v1.10 diagnostics and add real training evidence only where the claim contract supports it.

## Recommended v1.11 Phase Map

Use these proposed phase labels when turning pitfalls into roadmap controls.

| Phase | Name | Scope |
|-------|------|-------|
| Phase 59 | Evidence Contracts and Source Locks | Lock v1.6, v1.9, and v1.10 source artifacts; define claim IDs, regimes, run budgets, smoke gates, and table schemas before running new campaigns. |
| Phase 60 | Claim-Safe Training Campaigns | Run shallow pure-blind, scaffolded, warm-start/same-AST, perturbed-basin, and low-budget logistic/Planck probes with verifier-owned outcomes. |
| Phase 61 | Ablation and Baseline Diagnostics | Add one-variable ablations for motifs, macro depth, warm-start versus blind, candidate pool, repair, refit, and lightweight conventional baselines. |
| Phase 62 | Figure and Table Data Pipeline | Generate machine-readable source tables, deterministic publication plots, captions, and plot QA checks from raw artifacts. |
| Phase 63 | Paper Package Assembly and Claim Audit | Regenerate the paper-facing package, update scientific-law tables, audit prose/figures against claim boundaries, and lock reproducibility commands. |

## Critical Pitfalls

### Pitfall 1: Mixing Evidence Regimes Into a Single "Recovery" Story

**What goes wrong:** Figures or paper tables merge pure blind, scaffolded, warm-start, same-AST, repair, refit, compile-only, and perturbed-basin outcomes into one recovery rate.

**Why it happens:** v1.11 wants "strong paper package" evidence, and the most visually attractive numbers are not all the same scientific claim. Existing claim boundaries explicitly say all hybrid modes except pure blind are not blind discovery.

**Consequences:** The paper overclaims the system as blind symbolic discovery. Reviewers can invalidate the evidence package by pointing out that same-AST return or repair was counted as discovery from data.

**Prevention:**
- Make `evidence_class`, `start_mode`, `return_kind`, `repair_status`, `refit_status`, and `verifier_status` mandatory in every v1.11 aggregate row.
- Require every rate table to declare its denominator and eligible evidence classes.
- Plot regimes as separate bars, facets, or tables; never stack them into an unlabeled total recovery rate.
- Add a final claim-audit script or checklist that rejects paper rows where "blind" includes non-blind evidence classes.

**Detection:** A paper package QA step should grep/generated-check all tables and figures for mixed denominators: if a plotted rate contains both `blind` and `same_ast` or `repaired_candidate`, the artifact must fail audit unless the caption explicitly calls it a hybrid aggregate.

**Phase mapping:** Phase 59 defines the contract; Phase 62 enforces it in figures; Phase 63 audits paper prose.

**Confidence:** HIGH. Sources: `artifacts/paper/v1.9/raw-hybrid/claim-boundaries.md`, `.planning/PROJECT.md`, `artifacts/proof/v1.6/proof-report.md`.

### Pitfall 2: Promoting Logistic or Planck From Compiler Shortening Alone

**What goes wrong:** Logistic or Planck appears as supported/recovered in v1.11 tables because v1.10 reduced compile depth, even though focused v1.10 aggregates still classify both as unsupported with zero verifier recovery.

**Why it happens:** Logistic relaxed depth dropped from 27 to 15, and Planck relaxed depth dropped from 20 to 14. Those are useful diagnostics and nice figure material, but they did not pass the strict gate or verifier-owned recovery contract.

**Consequences:** A high-visibility table claims progress that the artifacts do not support. This directly violates the current milestone constraint: no Planck/logistic promotion without the full contract.

**Prevention:**
- Preserve separate columns for `strict_support`, `relaxed_depth`, `strict_depth_gate`, `compile_status`, `warm_start_attempted`, `verifier_status`, and `public_claim`.
- In scientific-law tables, render logistic and Planck as "unsupported diagnostic" unless a new Phase 60 run passes the unchanged verifier contract.
- For v1.11 low-budget probes, predeclare that failure or unsupported status is an expected valid outcome.
- Do not relax the strict gate silently. If a new comparable gate is introduced, report both old and new gates side by side.

**Detection:** Regenerate the paper-facing table from focused aggregate JSON/Markdown and assert that the v1.10 logistic and Planck rows remain unsupported unless a new v1.11 artifact has `verifier_recovered > 0` under a declared eligible mode.

**Phase mapping:** Phase 59 source locks and schema; Phase 60 optional probes; Phase 63 paper package audit.

**Confidence:** HIGH. Sources: `.planning/PROJECT.md`, `artifacts/campaigns/v1.10-logistic-evidence/aggregate.md`, `artifacts/campaigns/v1.10-planck-diagnostics/aggregate.md`.

### Pitfall 3: Burning Compute on Known Dead-End Runs

**What goes wrong:** v1.11 launches broad deep blind, centered-family, logistic, or Planck training campaigns before smoke gates show that the run can answer a new question.

**Why it happens:** The milestone asks for "real training" and "cool plots." Without preflight gates, it is tempting to run large campaigns for visual volume, even though existing artifacts already show depth degradation and unsupported logistic/Planck status.

**Consequences:** The project spends time producing expensive artifacts that mostly restate known failures. Worse, long failed runs can pressure the paper package into hiding negatives or changing claims after the fact.

**Prevention:**
- Phase 59 must predeclare campaign purpose, maximum budget, stop criteria, and expected artifact value for each suite.
- Require smoke/calibration runs before any full campaign: one or two seeds, small budgets, full artifact path, and verifier checks.
- Run deep blind only as bounded depth-curve evidence, not as an open-ended attempt to force recovery.
- For logistic/Planck, run low-budget probes only after compile/support diagnostics are written into the manifest.
- If a smoke run shows no new signal, package it as failure-taxonomy evidence instead of scaling it up.

**Detection:** Every full campaign should have a manifest field linking it to a passed smoke gate or an explicit "negative diagnostic only" approval. Missing gate provenance should block Phase 60 execution.

**Phase mapping:** Phase 59 owns run budgets and gates; Phase 60 obeys them.

**Confidence:** HIGH. Sources: `.planning/PROJECT.md`, `artifacts/proof/v1.6/proof-report.md`, `artifacts/paper/v1.9/raw-hybrid/centered-negative-diagnostics.md`.

### Pitfall 4: Counting Training Loss as Recovery

**What goes wrong:** A run is described as recovered because train loss is low, even though snapping, cleanup, held-out checks, extrapolation checks, or mpmath verification fail.

**Why it happens:** Plotting loss curves is compelling, and soft training can look successful before exact candidate verification. The project has repeatedly established that the optimizer is a candidate generator, not the recovery judge.

**Consequences:** The paper presents numerical interpolation as symbolic formula recovery. This is especially dangerous for scaffolded/warm-start runs where the initial structure can fit well without returning to a verified exact tree.

**Prevention:**
- Treat `best_train_loss` as a diagnostic, never as a recovery label.
- Every training plot must be paired with post-snap `verifier_status` and `candidate_kind`.
- Figures that show loss curves should mark snap points and final verification outcome.
- Aggregate tables must use verifier-owned `recovered`, `same_ast_return`, `verified_equivalent_ast`, `unsupported`, `failed`, and `execution_error` counts rather than loss thresholds.

**Detection:** Add a table-generation check that refuses to compute `recovery_rate` from loss columns. Recovery rates must derive only from verifier/count fields.

**Phase mapping:** Phase 59 evidence schema; Phase 60 campaign outputs; Phase 62 loss plots.

**Confidence:** HIGH. Sources: `.planning/PROJECT.md`, `artifacts/proof/v1.6/proof-report.md`.

### Pitfall 5: Cherry-Picking Seeds or Showing Only Best Runs

**What goes wrong:** The paper package highlights attractive examples while hiding failed seeds, unsupported rows, or execution errors.

**Why it happens:** v1.11 wants publication-quality figures, and best-of plots are visually cleaner than full-seed distributions. The existing evidence has mixed outcomes and must remain honest.

**Consequences:** Results become non-reproducible and look stronger than the generated artifacts. Reviewers will ask for seed counts and failure rates.

**Prevention:**
- Predeclare seed sets and budgets in Phase 59 before running Phase 60.
- Plot all seeds or summarize all seeds with visible `n`, mean/median, and failure counts.
- Allow "representative run" plots only when the caption names the selection rule and links to the aggregate distribution.
- Include unsupported and failed rows in source tables even when the public figure emphasizes successful cases.

**Detection:** Figure source tables must include `seed`, `run_id`, `status`, and `selection_role` columns. Any figure with a single run must identify whether it is best, median, first, or hand-selected.

**Phase mapping:** Phase 59 campaign design; Phase 60 run manifests; Phase 62 plot QA; Phase 63 paper audit.

**Confidence:** HIGH. Sources: `artifacts/proof/v1.6/proof-report.md`, `.planning/PROJECT.md`.

### Pitfall 6: Letting Figure Polish Hide Negative Evidence

**What goes wrong:** Plots omit unsupported rows, use ambiguous colors, suppress denominators, or visually imply improvement where the table says no recovery.

**Why it happens:** "Cool plots" can accidentally become marketing graphics. Existing v1.10 logistic/Planck rows are negative diagnostics but still useful; centered-family rows are also negative diagnostics with caveats.

**Consequences:** The paper package looks compelling but becomes scientifically fragile. Negative diagnostics are part of the honest contribution and should be visible.

**Prevention:**
- Use a stable visual grammar: recovered, same-AST, verified-equivalent, unsupported, failed, and execution-error statuses must have distinct encodings.
- Put `n` and eligibility rules in captions or directly in figure labels.
- For depth-delta plots, separate "compiler depth reduction" from "training recovery."
- Include a failure taxonomy figure or table so negative outcomes are not invisible.
- Avoid stacked totals where unsupported bars disappear into a total success narrative.

**Detection:** Each figure should have a machine-readable figure manifest declaring source table, included statuses, excluded statuses, denominator, and caption claim.

**Phase mapping:** Phase 62 primary; Phase 63 audit.

**Confidence:** HIGH. Sources: `.planning/PROJECT.md`, `artifacts/paper/v1.9/raw-hybrid/centered-negative-diagnostics.md`, v1.10 focused aggregates.

### Pitfall 7: Ablations That Change Multiple Variables at Once

**What goes wrong:** The milestone claims a motif, repair step, candidate-pool change, or warm-start setting helped, but the before/after runs also changed budgets, seed sets, datasets, gates, cleanup, or plotting filters.

**Why it happens:** The codebase has many interacting recovery mechanisms. It is easy to compare "new package" versus "old package" and call the difference an ablation.

**Consequences:** The ablation cannot support causal claims. A reviewer cannot tell whether improvement came from compiler motifs, macro depth, candidate pool, repair, refit, or a larger budget.

**Prevention:**
- Phase 61 should define one-variable ablation pairs with identical seeds, data splits, optimizer budgets, strict gates, verifier thresholds, and figure filters.
- For compiler motif ablations, report compile depth/node deltas separately from training outcomes.
- For repair/refit/candidate-pool ablations, preserve fallback candidates and report weak-dominance behavior: selected candidate before, selected after, verifier status before, verifier status after.
- Label inconclusive ablations as inconclusive rather than forcing a win/loss story.

**Detection:** Every ablation row must include `control_artifact`, `treatment_artifact`, `changed_variable`, and `held_constant` fields. Missing fields should fail aggregate generation.

**Phase mapping:** Phase 61 primary; Phase 62 tables/plots; Phase 63 paper prose.

**Confidence:** HIGH. Sources: `.planning/PROJECT.md`, v1.9 repair evidence decision, v1.10 motif evidence context.

### Pitfall 8: Treating Repair or Refit as Blind Discovery

**What goes wrong:** Expanded cleanup, candidate pooling, repair, or post-snap constant refit is counted as if the optimizer discovered the formula from a blind start.

**Why it happens:** Repair/refit can produce verified exact candidates after an optimizer near miss. That is valuable hybrid recovery evidence, but it is not the same as pure blind recovery.

**Consequences:** The paper collapses the central hybrid contribution into an overclaim. It also makes ablations harder to interpret because repair may rescue a run after the training stage failed.

**Prevention:**
- Preserve separate `raw_status`, `repair_status`, `refit_status`, and final `public_claim`.
- In ablation plots, show repair/refit as downstream stages after snap, not as part of blind training success.
- Keep `repaired_candidate` and refit-derived evidence out of pure blind denominators.
- For any repair win, include candidate provenance: selected, fallback, retained, neighborhood, or refit source.

**Detection:** Claim audit should reject any row where `public_claim = blind_recovered` and `repair_status != none` or `refit_status != none`.

**Phase mapping:** Phase 59 schema; Phase 61 ablations; Phase 63 audit.

**Confidence:** HIGH. Sources: `artifacts/paper/v1.9/raw-hybrid/claim-boundaries.md`, `.planning/PROJECT.md`.

### Pitfall 9: Weak or Unfair Baseline Diagnostics

**What goes wrong:** v1.11 either omits baselines entirely or adds an external/conventional baseline that is unfair, under-specified, or too broad for the milestone.

**Why it happens:** The project previously deferred matched-budget external benchmark competitions. The current milestone asks for lightweight baseline diagnostics, which can easily sprawl into a separate benchmark project.

**Consequences:** A weak baseline figure can hurt the paper more than no baseline. A broad benchmark race can consume the milestone and distract from EML evidence.

**Prevention:**
- Keep Phase 61 baselines diagnostic, not definitive: simple curve-fit sanity checks, conventional symbolic-regression smoke if already feasible, or "not run" with a clear reason.
- Match data splits, noise assumptions, formula domains, and evaluation metrics when a baseline is included.
- State what the baseline is meant to answer, such as "is this target numerically easy?" or "does a conventional model fit the data without symbolic EML recovery?"
- Do not compare pure blind EML to a baseline that receives formula scaffolds, or vice versa, without labeling the assistance.
- Defer matched-budget competitions unless a full baseline contract is created.

**Detection:** Baseline report rows must include method, version/command if applicable, data split, budget, allowed operators/features, assistance level, and reason why the comparison is diagnostic rather than definitive.

**Phase mapping:** Phase 61 primary; Phase 63 paper framing.

**Confidence:** MEDIUM-HIGH. Sources: `.planning/PROJECT.md` out-of-scope baseline competition decision and v1.11 active requirement for lightweight diagnostics.

### Pitfall 10: Stale Paper Tables and Source Drift

**What goes wrong:** v1.11 regenerates plots but leaves scientific-law tables or prose using stale v1.6/v1.9 depths, statuses, or artifact paths.

**Why it happens:** The raw-hybrid package already exists, while v1.10 focused artifacts live separately. Manual copying makes drift likely.

**Consequences:** The paper contradicts the repository: logistic/Planck may show old depths, missing macro hits, or incorrect support status. This weakens trust even if claims are conservative.

**Prevention:**
- Phase 59 should lock all source artifacts and SHA/path provenance used by the paper package.
- Phase 63 should regenerate tables from machine-readable source tables, not hand-edited Markdown.
- Add a stale-source check: paper rows for logistic and Planck must reference v1.10 or newer artifacts.
- Keep archived v1.4/v1.5/v1.6 anchors immutable and link to them rather than overwriting.

**Detection:** Paper package manifest should list every source artifact and hash. A missing v1.10 logistic/Planck source for the scientific-law table should fail Phase 63.

**Phase mapping:** Phase 59 source locks; Phase 63 package assembly.

**Confidence:** HIGH. Sources: `.planning/PROJECT.md`, `artifacts/proof/v1.6/proof-report.md`, v1.10 focused aggregates.

## Moderate Pitfalls

### Pitfall 11: Overinterpreting Centered-Family Negative Diagnostics

**What goes wrong:** The paper states or implies centered families cannot work because v1.8 centered experiments recovered 0.0 under the local setup.

**Prevention:** Use the existing wording: centered rows are negative diagnostic evidence under missing same-family witnesses, not a universal impossibility result. Keep raw scaffold helpers clearly raw-only.

**Phase mapping:** Phase 63 paper audit; Phase 62 figure captions if centered diagnostics are plotted.

**Confidence:** HIGH. Sources: `artifacts/paper/v1.9/raw-hybrid/centered-negative-diagnostics.md`, `.planning/PROJECT.md`.

### Pitfall 12: Hiding Domain, Singularity, or Numerical-Guard Caveats

**What goes wrong:** Training or figure domains cross singularities/branch-sensitive regions, or plots show training-mode guarded behavior as if it were faithful verification behavior.

**Prevention:** Store train/held-out/extrapolation domains in every run and figure source table. Plot only the declared safe domains for scientific-law visuals unless the figure is explicitly about failure near singularities. Captions should distinguish training guards from faithful verifier checks.

**Phase mapping:** Phase 60 campaign manifests; Phase 62 plot generation.

**Confidence:** HIGH. Sources: `.planning/PROJECT.md` numerics and verification constraints.

### Pitfall 13: Hyperparameter Tuning on the Final Evidence Set

**What goes wrong:** The team tunes budgets, seeds, schedules, repair settings, or plot filters after seeing final outcomes and then reports the result as if it were predeclared.

**Prevention:** Split calibration/smoke artifacts from final evidence artifacts. Phase 59 should define which knobs may be tuned during calibration and freeze final configs before Phase 60 full runs.

**Phase mapping:** Phase 59 contracts; Phase 60 execution.

**Confidence:** MEDIUM-HIGH. Sources: `.planning/PROJECT.md` run discipline and proof-campaign history.

### Pitfall 14: Losing Reproducibility Behind Pretty Figures

**What goes wrong:** The paper contains attractive SVG/PNG plots, but the raw JSON, CSV, commands, seeds, or environment metadata needed to regenerate them are missing.

**Prevention:** Phase 62 must write figure source tables and figure manifests next to every plot. Phase 63 must include exact commands for regenerating the paper package from a clean checkout.

**Phase mapping:** Phase 62 primary; Phase 63 reproducibility lock.

**Confidence:** HIGH. Sources: `.planning/PROJECT.md`, v1.3/v1.6 artifact conventions.

### Pitfall 15: Ambiguous Failure Taxonomy

**What goes wrong:** Unsupported, failed verification, failed training, execution error, timeout, skipped by gate, and not attempted all collapse into "failed."

**Prevention:** Use reason codes consistently. At minimum distinguish `unsupported`, `failed_training`, `snap_not_verified`, `verification_failed`, `execution_error`, `timeout`, `skipped_by_gate`, and `not_attempted`.

**Phase mapping:** Phase 59 schema; Phase 60 runs; Phase 62 failure plots.

**Confidence:** HIGH. Sources: v1.10 focused aggregates, `.planning/PROJECT.md`.

### Pitfall 16: Macro Depth Deltas Masquerading as Training Evidence

**What goes wrong:** Compiler motif plots show large depth reductions and the paper text treats that as evidence of recovered formulas.

**Prevention:** Use separate sections and colors for "representation/compiler diagnostics" and "training/verifier outcomes." A depth delta can support a "made support more plausible" claim, not a "recovered" claim.

**Phase mapping:** Phase 61 ablations; Phase 62 plots; Phase 63 prose audit.

**Confidence:** HIGH. Sources: v1.10 logistic/Planck aggregates and `.planning/PROJECT.md`.

## Minor Pitfalls

### Pitfall 17: Figure Captions Without Artifact Paths

**What goes wrong:** A reader cannot trace a figure back to the raw campaign or run artifacts.

**Prevention:** Every figure manifest and caption should include a short source label that resolves to an artifact directory or table.

**Phase mapping:** Phase 62.

### Pitfall 18: Inconsistent Naming Across Paper Artifacts

**What goes wrong:** The same regime is called "warm-start," "same-AST," "compiler-assisted," and "hybrid" in different places without clear distinctions.

**Prevention:** Phase 59 should define a glossary and Phase 63 should run a terminology pass over tables, captions, and claim boundaries.

**Phase mapping:** Phase 59; Phase 63.

### Pitfall 19: Overloading CI With Full Evidence Runs

**What goes wrong:** Tests become slow or flaky because publication campaigns are run in ordinary CI.

**Prevention:** Keep CI to schema, smoke, deterministic mini-artifact, and plot-regression checks. Full v1.11 campaigns should be explicit commands with archived outputs.

**Phase mapping:** Phase 60; Phase 62.

### Pitfall 20: Paper Package Without a Negative-Results Narrative

**What goes wrong:** The package includes negative rows but does not explain why they matter.

**Prevention:** Phase 63 should frame failures as boundary evidence: blind depth degradation, unsupported logistic/Planck diagnostics, and centered-family caveats are part of the honest scientific contribution.

**Phase mapping:** Phase 63.

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|----------------|------------|
| Phase 59: Evidence Contracts and Source Locks | Starting runs before claims, denominators, budgets, and source locks are defined | Freeze claim taxonomy, seed policy, budget classes, source artifact hashes, and table schemas first. |
| Phase 59: Evidence Contracts and Source Locks | Paper package uses stale v1.6/v1.9 logistic or Planck data | Require v1.10 or newer source artifacts for logistic/Planck scientific-law rows. |
| Phase 60: Claim-Safe Training Campaigns | Broad deep blind or unsupported probes consume compute without new information | Use smoke gates, bounded budgets, and negative-diagnostic approvals before full runs. |
| Phase 60: Claim-Safe Training Campaigns | Loss curves are counted as symbolic recovery | Recovery labels must come only after snap, cleanup, held-out, extrapolation, and mpmath verification. |
| Phase 60: Claim-Safe Training Campaigns | Same-AST or zero-noise returns look like robust training | Report perturbation scale, gate flips, snap margins, and whether the argmax changed before training. |
| Phase 61: Ablation and Baseline Diagnostics | Before/after comparisons change too many variables | Require one changed variable per ablation pair and record all held-constant settings. |
| Phase 61: Ablation and Baseline Diagnostics | Lightweight baseline becomes an unfair benchmark competition | Scope baselines as diagnostics with matched splits and transparent assistance/budget labels. |
| Phase 62: Figure and Table Data Pipeline | Pretty figures hide denominators, failures, or unsupported rows | Generate plots from source tables with status fields, `n`, eligibility rules, and figure manifests. |
| Phase 62: Figure and Table Data Pipeline | Depth-reduction plots imply training recovery | Separate compiler diagnostics from verifier-owned recovery plots. |
| Phase 63: Paper Package Assembly and Claim Audit | Prose overclaims warm-start/scaffolded/repair evidence as blind discovery | Run a claim-boundary audit against every table, caption, and summary paragraph. |
| Phase 63: Paper Package Assembly and Claim Audit | Centered negative diagnostics become universal negative theorem language | Preserve the same-family witness caveat and local-setup language. |

## Roadmap Implications

v1.11 should be ordered as evidence-contract first, then training, then ablations/baselines, then figures, then paper packaging. Running training before Phase 59 will create artifacts whose claims are hard to defend. Generating figures before Phase 60/61 will incentivize manual graph curation. Writing the paper package before Phase 62 will make stale data and denominator drift likely.

Recommended gates:

1. **Before Phase 60:** Claim taxonomy, source locks, seed policy, budget classes, and smoke gates exist.
2. **Before Phase 61:** Campaign outputs expose enough fields to form one-variable ablations.
3. **Before Phase 62:** Source tables exist for every planned figure.
4. **Before Phase 63:** Figures and tables can regenerate from raw artifacts without manual edits.
5. **Before milestone close:** Logistic and Planck public claims match the latest verifier-owned artifacts and remain unsupported unless a new full-contract recovery artifact exists.

## Sources

- `.planning/PROJECT.md` - v1.11 goal, active requirements, out-of-scope constraints, claim boundaries, run discipline, and logistic/Planck status.
- `artifacts/paper/v1.9/raw-hybrid/claim-boundaries.md` - explicit separation of blind, warm-start, same-AST, scaffolded, repaired, refit, compile-only, and perturbed-basin evidence.
- `artifacts/paper/v1.9/raw-hybrid/centered-negative-diagnostics.md` - centered-family negative diagnostics and same-family witness caveat.
- `artifacts/proof/v1.6/proof-report.md` - measured blind weakness, perturbed-basin strength, proof claim policies, depth curve, and archived anchors.
- `artifacts/campaigns/v1.10-logistic-evidence/aggregate.md` - logistic remains unsupported with zero verifier recovery in the focused v1.10 aggregate.
- `artifacts/campaigns/v1.10-planck-diagnostics/aggregate.md` - Planck remains unsupported with zero verifier recovery in the focused v1.10 aggregate.
