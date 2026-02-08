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
