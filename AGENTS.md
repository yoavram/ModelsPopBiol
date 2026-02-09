# Repository Guidelines

## Project Structure & Module Organization
- `notebooks/`: Lecture notebooks; keep runnable top-to-bottom with minimal assumptions about working dir (`/Users/.../ModelsPopBiol`). Use `data/` and `resources/` for supporting files.
- `assignments/`: Student-facing notebooks. `solutions/` holds released keys; private solutions live in `ModelsPopBiolSol` (separate repo).
- `www/`: Lektor static site source (`content/`, `templates/`, `models/`, `assets/static/`). Site pages are defined by `.lr` files with `_model` and `_template` fields.
- Root configs: `environment.yaml` (full conda stack for modeling) and `requirements.txt` (minimal Lektor-only setup).

## Build, Test, and Development Commands
- `mamba env create -n modelspopbiol -f environment.yaml` (preferred) or `conda env create -n modelspopbiol -f environment.yaml`: Provision full teaching stack (JAX/PyMC, plotting, Jupyter); `mamba activate modelspopbiol` before working.
- `pip install -r requirements.txt`: Install just the static site toolchain if you are only updating `www/`.
- `jupyter lab` (or `jupyter notebook`): Run and validate notebooks locally; prefer the env above.
- `lektor serve --port 5000`: Live preview of the course site at `http://localhost:5000`.
- `lektor build -O build`: Generate static output for review; treat warnings as blockers before deploying or pushing.

## Coding Style & Naming Conventions
- Python notebooks: PEP 8, 4-space indent, descriptive lower_snake_case names. Keep outputs lightweight; prefer vectorized NumPy/Pandas over loops when feasible.
- Content slugs: lowercase with hyphens (`content/calendar/week-03/contents.lr`). Set `_model`/`_template` explicitly when adding new pages or events.
- HTML/Jinja in `www/templates/`: 2-space indent; reuse macros and blocks instead of duplicating markup. CSS in `assets/static/style.css` also uses 2 spaces; lean on existing Bootstrap utilities first.

## LaTeX In Marimo Markdown
- In `mo.md(r"""...""")` cells, prefer display equations as single-line `$$ ... $$` blocks.
- Keep one display equation per line.
- Keep a blank line before and after every `$$ ... $$` line.
- Keep inline math as `$...$`.
- Avoid multiline display constructs (for example `\[ ... \]`, `\begin{aligned} ... \end{aligned}`, or explicit `\\` line breaks) when rendering is critical, because they may be shown as raw text in some marimo views.

## Plot Rendering In Marimo
- In cells that generate matplotlib figures, output a figure object for notebook rendering.
- Use `plt.gcf()` for stateful/static plotting.
- Use `fig` when a figure object already exists (for example after `fig, ax = plt.subplots(...)`).
- Do not use `plt.show()` for notebook output (it targets the console area).

## Testing Guidelines
- No automated unit suite. For notebooks, run all cells to completion (Kernel → Restart & Run All) and confirm figures render with current dependencies.
- For site changes, run `lektor build` and spot-check in `lektor serve`: navigation, dated items, external links, and `/static/` assets on mobile and desktop widths.
- Keep datasets small and versionable; document any new files in `data/` within the relevant notebook markdown cell.

## Commit & Pull Request Guidelines
- Commit messages: short, imperative (`update predator-prey notebook`, `fix calendar template spacing`). Group related content and styling changes together.
- PRs should state scope (notebooks vs site vs assets vs data) and list commands run (`lektor build`, notebook execution). Include screenshots/GIFs for visual/template changes.
- Avoid committing secrets; keep unreleased solutions in `ModelsPopBiolSol` and only publish vetted keys in `solutions/`.

## Marimo Notebook Summaries
1. `notebooks/bayesian.py`: model: Poisson and over-dispersed Poisson count models; skills: direct posterior computation, Monte Carlo, rejection sampling, MCMC (`emcee`), PyMC/ADVI, ArviZ diagnostics; theory: Bayes theorem, priors/posteriors, Bayesian workflow under over-dispersion.
2. `notebooks/bayesian_ode.py`: model: nonlinear predator-prey ODE for inference; skills: `solve_ivp`, JAX `odeint`, MLE optimization, PyMC model fitting for dynamic systems; theory: frequentist vs Bayesian inference in nonlinear dynamical models.
3. `notebooks/exponential-growth.py`: model: exponential growth as log-linear GLM; skills: least squares, MLE, gradient descent, SciPy/statsmodels fitting, PyMC posterior predictive checks; theory: GLM interpretation, priors, uncertainty.
4. `notebooks/gillespie.py`: model: SIR epidemic model (deterministic and stochastic); skills: analytic/numerical ODE solutions and Gillespie simulation; theory: continuous-time Markov jump processes and stochastic epidemic dynamics.
5. `notebooks/lfi.py`: model: over-dispersed Poisson and dolphin social-network simulation models; skills: rejection-ABC, MCMC-ABC, SMC-ABC, PyMC ABC, posterior predictive checks; theory: likelihood-free Bayesian inference with summary statistics.
6. `notebooks/logistic-model.py`: model: logistic regression on COVID-19 fatality data; skills: data wrangling, stable likelihood coding, gradient descent, sklearn ROC/threshold analysis, Bayesian logistic regression (PyMC/Bambi); theory: binary-response modeling and MLE/Bayesian comparison.
7. `notebooks/matplotlib-basics.py`: model: none (visualization-focused); skills: Matplotlib figure/axes API, subplot layout, styling, plotting real tabular data; theory: plotting anatomy and visualization best practices.
8. `notebooks/mle.py`: model: Poisson and negative-binomial count models; skills: likelihood construction, MLE, goodness-of-fit checks, likelihood surfaces, bootstrap uncertainty; theory: frequentist inference, over-dispersion, model adequacy.
9. `notebooks/numpy-basics.py`: model: none (numerical foundations); skills: array creation, indexing/slicing, vectorization, descriptive statistics, random sampling, file IO; theory: array-based scientific computing principles.
10. `notebooks/pandas-seaborn.py`: model: linear relationship analysis for life-history traits; skills: Pandas data manipulation, Seaborn statistical visualization, SciPy linear regression; theory: exploratory data analysis and linear trend interpretation.
11. `notebooks/population-genetics.py`: model: deterministic discrete-time haploid and diploid selection models with mutation; skills: recurrence simulation, equilibrium/fixation analysis, comparative plotting; theory: selection, dominance, polymorphism, mutation-selection balance, local stability.
12. `notebooks/population-growth.py`: model: exponential, logistic, and generalized logistic growth; skills: parameterized trajectory simulation and visualization; theory: carrying capacity, intrinsic growth, and model assumptions.
13. `notebooks/predator-prey.py`: model: Lotka-Volterra-type predator-prey ODE system; skills: numerical integration, phase-plane analysis, equilibrium computation, symbolic Jacobian/eigenvalue analysis via SymPy; theory: multivariate nonlinear dynamics, local stability, stochastic effects.
14. `notebooks/python.py`: model: none (programming foundations); skills: Python syntax, types, operators, conditionals, loops, functions; theory: core programming concepts for scientific computing.
15. `notebooks/stability.py`: model: generic local stability framework for one- and multi-variable ODEs; skills: mathematically guided stability checks; theory: fixed points, Jacobian linearization, eigenvalue-based local stability criteria.
16. `notebooks/wright-fisher.py`: model: stochastic Wright-Fisher population genetics; skills: pure Python/NumPy simulation, repeated runs, Numba acceleration, diffusion-approximation calculations; theory: genetic drift, fixation probability/time, deterministic vs diffusion approximations.
