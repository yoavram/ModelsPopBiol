# Implement `notebooks/age-structure.py`: Orca Age-Structured Demography (Marimo)

## 1. Summary
1. Build a new lecture Marimo notebook at `/Users/yoavram/Work/Teaching/ModelsPopBiol/notebooks/age-structure.py`.
2. Use `Orcinus_orca` as the focal species.
3. Use a committed data snapshot strategy: extract Orca life-table records once from your downloaded MALDDABA Rdata into repo-local CSV(s), then notebook reads only repo files.
4. Keep interactivity moderate: a few high-value controls (vital-rate multipliers + deterministic bad-year schedule), not a full scenario builder.
5. Preserve project Marimo conventions: cell graph style, LaTeX formatting rules, figure rendering via `fig`/`plt.gcf()`, and strict global-name uniqueness.

## 2. Deliverables (Implementation Scope)
1. New notebook:
  1. `/Users/yoavram/Work/Teaching/ModelsPopBiol/notebooks/age-structure.py`
2. New data files:
  1. `/Users/yoavram/Work/Teaching/ModelsPopBiol/data/orca_life_table.csv`
  2. `/Users/yoavram/Work/Teaching/ModelsPopBiol/data/orca_demographic_metric.csv`
  3. `/Users/yoavram/Work/Teaching/ModelsPopBiol/data/orca_data_used.csv`
3. Optional but recommended reproducibility helper:
  1. `/Users/yoavram/Work/Teaching/ModelsPopBiol/scripts/extract_orca_life_table.R`
  2. Reads `/Users/yoavram/Downloads/life_table_data/malddaba_life_table.Rdata` and writes the CSV snapshots above.

## 3. Data Interface Specification
1. Input source (one-time extraction):
  1. `result_list` in Rdata; filter species == `Orcinus_orca`.
2. CSV schemas (post-extraction):
  1. `orca_life_table.csv` columns:
    1. `Combined_life_table_id` (int)
    2. `Age` (int, 0..90)
    3. `Sx` (float)
    4. `lx` (float)
    5. `mx` (float)
  2. `orca_demographic_metric.csv` columns:
    1. `AFR`, `R0`, `r`, `Tb`, `Tc`
  3. `orca_data_used.csv` columns:
    1. Retain original MALDDABA provenance columns (IDs, censoring/modeling flags, `Age_interval`).
3. Notebook-internal normalized frame:
  1. Add derived columns in notebook (not persisted):
    1. `dx = lx * (1 - Sx)` (if needed for teaching checks),
    2. `female_births = mx`,
    3. Class labels for aggregated stage model.

## 4. Notebook Architecture (Marimo-Specific, Decision-Complete)
1. File scaffold:
  1. `import marimo`
  2. `__generated_with = "<current marimo version>"`
  3. `app = marimo.App()`
  4. Terminal `if __name__ == "__main__": app.run()`
2. Cell graph pattern:
  1. First import cell returns only shared globals (`mo`, `np`, `pd`, `plt`, `sns`).
  2. Markdown cells use `@app.cell(hide_code=True)` and `mo.md(r"""...""")`.
  3. Compute cells return only values needed downstream.
  4. Any temporary variable inside a cell must use `_` prefix (for example `_df`, `_ax`, `_vals`) and should not be returned.
3. Global-name uniqueness rule:
  1. No reassignment of exported names across cells.
  2. If a concept evolves, create versioned globals (`lt_raw`, `lt_clean`, `lt_stage`) instead of reusing the same global name.
4. Plot rendering rule:
  1. Return `fig` when using OO API.
  2. Otherwise return `plt.gcf()`.
  3. Never `plt.show()`.
5. LaTeX markdown rule:
  1. Display equations as one-line `$$ ... $$` blocks with blank lines around each block.

## 5. Content Plan (Mapped to Approved Class Outline)
1. `# Age-structured population models`
  1. Explain why total abundance alone is insufficient; introduce Orca context.
2. `# Data and life table`
  1. Load `orca_life_table.csv`; show first/last ages and monotonicity sanity checks.
  2. Present provenance from `orca_data_used.csv`.
3. `# Leslie matrix model`
  1. Convert full-age schedule into teachable stage model (default 4 classes):
    1. Juvenile (0-10),
    2. Early reproductive (11-24),
    3. Prime reproductive (25-44),
    4. Older reproductive/post-reproductive (45+).
  2. Build stage transition + fertility matrix from aggregated Orca rates.
4. `# Asymptotic theory`
  1. Compute dominant eigenvalue `lambda_dom`.
  2. Compute stable stage distribution (right eigenvector normalized to sum=1).
  3. Compute reproductive value (left eigenvector normalized with first class or dot-product normalization).
5. `# Transient dynamics`
  1. Compare at least 3 initial compositions with equal total `N0`.
  2. Show short-run divergence and convergence to stable composition.
6. `# Sensitivity and elasticity`
  1. Numerical finite-difference sensitivities for each nonzero matrix element.
  2. Elasticity matrix and ranked life-stage levers.
7. `# Scientific question 1`
  1. Apply intervention multipliers to:
    1. Juvenile survival,
    2. Adult survival,
    3. Maturation transition,
    4. Fertility.
  2. Rank by gain in `lambda_dom` under equal proportional effort.
8. `# Periodic environmental forcing (deterministic)`
  1. Implement deterministic cycle (default: every 4th year bad year).
  2. Bad-year effect defaults: juvenile survival multiplier and optional fertility multiplier.
  3. Compare long-run growth and extinction-proxy thresholds versus baseline.
9. `# Scientific question 2`
  1. Identify recovery vs decline regimes over a grid of bad-year severity/frequency.
  2. Report threshold frontier.
10. `# Limitations and extensions`
  1. Density dependence, two-sex structure, observation error, and next-session stochastic extension.
11. `# References` and `# Colophon`.

## 6. Interactivity Spec (Moderate)
1. Widgets (`mo.ui.*`) to include:
  1. `n_years` (projection horizon),
  2. `N0` (initial total),
  3. Intervention multipliers for 4 levers,
  4. Bad-year period (integer),
  5. Bad-year severity multiplier(s).
2. Widget outputs:
  1. Baseline vs intervention trajectories,
  2. Composition plots,
  3. Elasticity bar chart,
  4. Deterministic stress heatmap.
3. Keep default values biologically plausible and numerically stable.

## 7. Public Interfaces / Types Changes
1. New teaching-data interfaces (CSV contracts):
  1. `data/orca_life_table.csv` with fixed required columns (`Age`, `Sx`, `lx`, `mx`).
  2. `data/orca_demographic_metric.csv` with one-row demographic summary.
  3. `data/orca_data_used.csv` for provenance and method flags.
2. No runtime dependency on R in notebook itself (R only for one-time extraction script).
3. No changes to existing notebooks/APIs.

## 8. Validation and Test Scenarios
1. Data integrity tests (in notebook cells, visible or hidden):
  1. `Age` strictly increasing by 1.
  2. `Sx` in [0,1], `lx` non-increasing, `mx >= 0`.
  3. No missing values in required columns.
2. Matrix sanity tests:
  1. Nonnegative matrix entries.
  2. `lambda_dom` real and positive.
  3. Stable distribution sums to 1 and nonnegative.
3. Behavioral tests:
  1. Increasing juvenile/adult survival multipliers should not decrease `lambda_dom`.
  2. More frequent/severe bad years should not improve deterministic long-run growth.
  3. Transient runs with equal `N0` but different compositions should differ in short term.
4. Rendering checks:
  1. Notebook runs top-to-bottom in Marimo without name-collision errors.
  2. All plotting cells return `fig`/`plt.gcf()`.
  3. Markdown math renders (no multiline `aligned` blocks).

## 9. Implementation Order
1. Add extraction script + generate CSV snapshots.
2. Create notebook scaffold and imports.
3. Implement data load + validation cells.
4. Implement matrix construction + eigendecomposition cells.
5. Implement transient scenarios + visualizations.
6. Implement sensitivity/elasticity cells.
7. Implement deterministic periodic forcing section + threshold analysis.
8. Add markdown narrative, references, colophon.
9. Final run-through and style consistency checks.

## 10. Assumptions and Defaults (Explicit)
1. Species fixed to Orca (`Orcinus_orca`) for this first implementation.
2. First deliverable is lecture notebook only (assignment split may follow later).
3. Data strategy is committed CSV snapshot, not runtime Rdata loading.
4. Deterministic periodic forcing is included; stochastic forcing deferred to a later session.
5. Moderate widget interactivity is the target.
6. Stage aggregation defaults to 4 classes unless Orca data behavior suggests a numerically unstable split (then fallback to 3 classes with explicit note).
