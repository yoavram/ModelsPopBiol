# Age-Structured Models Class Plan

## 1. Class Identity
1. Proposed title: `Population Demography: Age-Structured Models (Leslie and Lefkovitch)`.
2. Position in course: after `population-growth` and before (or alongside) stochastic genetics/inference modules.
3. Duration target: one full lecture notebook plus one assignment.

## 2. Why This Class
1. Existing classes cover unstructured growth and multivariate dynamics, but not explicit age composition.
2. This class introduces structure-dependent demography where identical total abundance can imply different futures.
3. It creates a bridge from deterministic matrix models to stochastic/environmental risk analysis.

## 3. Learning Objectives
1. Build and interpret a Leslie matrix from a life table.
2. Compute and interpret dominant eigenvalue, stable age distribution, and reproductive value.
3. Distinguish transient dynamics (short-term behavior driven by initial age composition) from asymptotic dynamics (long-run behavior governed by the dominant eigenvalue and stable age structure).
4. Run sensitivity and elasticity analyses to identify intervention leverage points across life stages.
5. Evaluate demographic resilience under environmental variability by quantifying recovery time and long-run growth under repeated stress.

## 4. Two Scientific Questions
1. Which vital-rate intervention yields the largest increase in long-term population growth rate ($\lambda$): juvenile survival, adult survival, maturation transition probability (juvenile-to-reproductive class), or fecundity?
2. Under periodic or stochastic bad years that depress juvenile survival, when does the population recover versus enter long-term decline?

## 5. Core Model
1. Baseline discrete-time model:

$$ \mathbf{n}_{t+1} = \mathbf{A}\mathbf{n}_t $$

2. Leslie matrix setup:
  1. First row: age-specific fertilities.
  2. Subdiagonal: age-specific survival transitions.
  3. Optional terminal class: plus-group handling (aggregate all ages above a cutoff into one final class, with survival allowing persistence in that class).

## 6. Notebook Structure (Marimo)
1. `# Age-structured population models`
### Motivation and biological contexts
  1. Plants, vertebrates, and insects as motivating examples.
  2. Why age structure changes predictions.

2. `# Data and life table`
### Data setup
  1. Define census timing and age classes.
  2. Convert survival/fecundity data into model-ready parameters.

3. `# Leslie matrix model`
### Core implementation
  1. Construct matrix `A`.
  2. Project cohorts and total abundance.
  3. Compare with scalar exponential growth.

4. `# Asymptotic theory`
### Long-run quantities
  1. Dominant eigenvalue $\lambda$.
  2. Stable age distribution (right eigenvector).
  3. Reproductive value (left eigenvector).

5. `# Transient dynamics`
### Non-asymptotic behavior
  1. Contrast multiple initial age distributions with identical $N_0$.
  2. Quantify time-to-convergence.

6. `# Sensitivity and elasticity`
### Intervention leverage analysis
  1. Finite perturbation method for each matrix element.
  2. Aggregate by life stage and compare intervention leverage.

7. `# Scientific question 1`
### Which vital rate should be targeted first?
  1. Intervention ranking under a realistic budget constraint.
  2. Biological interpretation and management recommendation.

8. `# Periodic environmental forcing (deterministic)`
### Good-year / bad-year structure
  1. Apply deterministic periodic shocks to selected vital rates.
  2. Analyze trajectory shifts and threshold behavior.

9. `# Scientific question 2`
### Recovery versus decline under repeated bad years
  1. Recovery thresholds under deterministic repeated stress.
  2. Tipping behavior and mitigation strategy.

10. `# Limitations and extensions`
### Scope and next steps
  1. Density dependence.
  2. Two-sex models and mating limitations.
  3. Process and observation uncertainty.

11. `# References`
12. `# Colophon`

## 7. Computational Skills to Teach
1. Vectorized matrix projection (`NumPy`) for demographic dynamics.
2. Eigen-analysis and normalization conventions for biological interpretation.
3. Structured scenario sweeps (parameter grids and policy interventions).
4. Elasticity and sensitivity calculation via finite differences.
5. Clear plotting of abundance, age composition, and uncertainty bands.

## 8. Theory Emphasis
1. Asymptotic growth is an emergent property of structure, not just total counts.
2. Stable age distribution is a dynamic attractor; transients can dominate short-term decisions.
3. Reproductive value provides a principled weighting of age classes.
4. Elasticity is often more decision-relevant than raw sensitivity.
5. Environmental variability can reverse deterministic conclusions.

## 9. Real Parameterization Plan (bioRxiv-guided)
1. Target source for realistic vital rates: [bioRxiv preprint](https://www.biorxiv.org/content/10.1101/2025.07.01.662579v1), which presents `malddaba` (a multi-species mammal demographic database; currently 170 species rather than one focal species).
2. Chosen focal species for class parameterization: `Orcinus_orca` (orca), using full age-specific longitudinal survival and reproduction (`Mx`) records in malddaba.
3. Why this choice:
  1. Very broad observed age range (0-90) supports clear age-structured modeling.
  2. Survival and fecundity are available in the same population context.
  3. The species is biologically engaging and suitable for high-impact classroom discussion.
4. Backup options if extraction is cleaner:
  1. `Pan_troglodytes` (great ape option; full life table with `Sx` and `Mx`).
  2. `Gorilla_beringei` (great ape option; full life table with `Sx` and `Mx`).
5. Data extraction workflow:
  1. Identify life table/vital-rate tables in the manuscript or supplement.
  2. Map reported rates into class-specific fertility and transition probabilities.
  3. Document all assumptions (time step, plus-group, stage-to-age mapping).
6. Calibration outputs:
  1. Baseline `A` matrix.
  2. Reproduction of one headline trajectory or growth estimate from the paper.
  3. Scenario analyses tied to the two scientific questions.
7. Fallback if complete tables are unavailable:
  1. Build a reduced 3-5 class approximation.
  2. Provide a transparent mapping and sensitivity check for omitted classes.

## 10. Exercise Plan
1. Build a Leslie matrix from a supplied life table and validate dimensions/probability constraints.
2. Compute $\lambda$, stable age distribution, and reproductive value.
3. Run one-at-a-time perturbations and compare sensitivity vs elasticity rankings.
4. Simulate deterministic repeated bad years and identify recovery/decline conditions.

## 11. Assignment Plan
1. Students choose one management objective (maximize growth, increase resilience, reduce extinction risk).
2. Students test two intervention strategies targeting different life stages.
3. Deliverables:
  1. One figure comparing intervention outcomes.
  2. One table of elasticity-informed priorities.
  3. A short memo with a quantitative recommendation.

## 12. Comparison to Existing Course Notebooks
1. Mirrors deterministic progression style from `notebooks/population-growth.py`.
2. Reuses equilibrium/stability framing from `notebooks/population-genetics.py`.
3. Reuses deterministic-vs-stochastic comparison style from `notebooks/wright-fisher.py`.
4. Reuses data-to-model workflow style from `notebooks/exponential-growth.py` and `notebooks/mle.py`.

## 13. Implementation Notes for Later (Not Yet Implemented)
1. Keep equations in single-line `$$ ... $$` blocks in Marimo markdown.
2. Return figure objects (`fig` or `plt.gcf()`) rather than using `plt.show()`.
3. Keep code cells short and aligned with one conceptual step per section.
