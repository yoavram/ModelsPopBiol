Codex CLI handoff: Migrate ModelsPopBiol course to marimo + pixi (pilot)

Goal

Transition the course workflow from Jupyter/miniforge to marimo notebooks + pixi, with an explicit assumption that students will increasingly work with Python + a coding agent (Gemini Pro or GitHub Copilot). We will likely mix delivery modes: molab links, marimo editor, and VS Code.

Repo: https://github.com/yoavram/ModelsPopBiol
Course site: https://modelspopbiol.yoavram.com/

Branch

Work on a new branch:
	•	marimo

Stage 1: Setup (pixi + marimo project scaffolding)

Deliverables
	1.	pixi.toml and pixi.lock for a cross-platform environment (macOS Intel/ARM, Windows, Ubuntu).
	2.	A minimal “how to run” doc for students and instructors.
	3.	Optional but recommended: VS Code tasks to avoid terminal use beyond first install.

Steps
	1.	Create branch

git checkout -b marimo

	2.	Create pixi.toml (course-wide env)

	•	Use conda-forge.
	•	Platforms: linux-64, osx-64, osx-arm64, win-64.
	•	Choose a modern Python (recommend >=3.10 unless course content requires older).
	•	Add core dependencies needed by the first two notebooks (and likely the course):
	•	python, marimo, numpy, pandas, matplotlib, seaborn, scipy, sympy
	•	Do not include site tooling (lektor) unless needed for build steps.

Example skeleton (adjust versions minimally; prefer open ranges with major pins only if necessary):

[project]
name = "modelspopbiol"
channels = ["conda-forge"]
platforms = ["linux-64", "osx-64", "osx-arm64", "win-64"]

[dependencies]
python = ">=3.10"
marimo = "*"
numpy = "*"
pandas = "*"
matplotlib = "*"
seaborn = "*"
scipy = "*"
sympy = "*"

[tasks]
marimo = "marimo"

	3.	Resolve and lock

pixi install
pixi run python -c "import marimo, numpy, pandas, matplotlib, seaborn, scipy, sympy; print('ok')"

Commit pixi.toml and pixi.lock.
	4.	Add docs
Create docs/marimo/README.md (or update main README.md) with:

	•	Student setup (pixi + VS Code + extensions)
	•	Running a notebook:
	•	pixi run marimo edit path/to/notebook.py
	•	VS Code: select interpreter under .pixi/envs/... then open .py marimo notebook
	•	Notes on agent use (Copilot/Gemini) and expectations.

	5.	Optional: VS Code tasks
Add .vscode/tasks.json with click-to-run commands, e.g.:

	•	“Pixi install”
	•	“Marimo edit (current file)”
	•	“Marimo run (current file)”

Acceptance criteria for Stage 1
	•	Fresh clone + pixi install works on at least one platform in CI or local test.
	•	pixi run marimo tutorial intro works.
	•	Docs exist and are accurate.

⸻

Stage 2: Convert first two notebooks

Target notebooks:
	•	notebooks/population-growth.ipynb
	•	notebooks/predator-prey.ipynb

Deliverables
	1.	Converted marimo notebooks committed to repo.
	2.	The two marimo notebooks run end-to-end via pixi run marimo edit ....
	3.	For predator-prey: remove/replace ipywidgets usage with marimo UI inputs.

Steps
	1.	Destination folder:

	•	`notebooks` and keep original .ipynb in place.

	2.	Convert notebook 1

pixi run marimo convert notebooks/population-growth.ipynb > notebooks/population-growth.py

Open and validate:

pixi run marimo edit notebooks/population-growth.py

Fix any issues:
	•	Jupyter magics (%matplotlib inline, %%time, etc.) must be removed.
	•	Ensure figures render in marimo app view by outputting a figure object from plotting cells:
	•	use `plt.gcf()` for stateful/static plotting
	•	use `fig` when a figure object is available
	•	do not use `plt.show()` for notebook output (it targets console output)
	•	In marimo markdown cells, use single-line display equations `$$ ... $$` with a blank line before and after each equation line.

	3.	Convert notebook 2

pixi run marimo convert notebooks/predator-prey.ipynb > notebooks/predator-prey.py
pixi run marimo edit notebooks/predator-prey.py

	4.	Replace ipywidgets in predator-prey

	•	Identify all ipywidgets imports and widget construction.
	•	Replace with marimo inputs:
	•	sliders: mo.ui.slider(...)
	•	dropdowns: mo.ui.dropdown(...)
	•	buttons: mo.ui.button(...)
	•	Ensure widget values drive recomputation properly (marimo reactive graph).
	•	Keep the pedagogical intent: interactive parameter exploration.

	5.	Data file paths

	•	If notebooks load data from data/ or other paths, ensure paths are robust:
	•	Use paths relative to notebook location.
	•	Avoid assuming CWD.

	6.	Add molab links (pilot)

	•	Add links in a prominent place (README, course calendar pages) for the two converted notebooks.
	•	Prefer linking to the marimo .py notebook in the marimo branch (or after merge, default branch).
	•	If molab expects a specific URL format, follow marimo’s documented GitHub entrypoint.

Acceptance criteria for Stage 2
	•	Both notebooks run successfully locally with:
	•	pixi run marimo edit notebooks/population-growth.py
	•	pixi run marimo edit notebooks/predator-prey.py
	•	Predator-prey has no ipywidgets dependency.
	•	Minimal user instructions updated accordingly.

⸻

Notes on “agent-friendly” course design

When editing notebooks, prioritize:
	•	Clear, linear-narrative markdown cells + small code cells.
	•	Minimize hidden state; rely on marimo’s dataflow.
	•	Keep functions in importable modules if they are reused across notebooks (optional later stage).
	•	Prefer explicit randomness control (seed parameters) for reproducibility.

Students’ agent access:
	•	Either Gemini Pro (student free year) or GitHub Copilot (Student Pack). Plan text in docs encouraging students to use agents for:
	•	refactors
	•	debugging errors
	•	writing tests for small functions
	•	exploring parameter sweeps

⸻

Stage 2 conversion insights (from `population-growth`, `predator-prey`, `stability`)

1. `import marimo as mo` rule:
   • Put `import marimo as mo` as the first line in the first existing imports cell.
   • Do not create a dedicated one-line cell just for `import marimo as mo`.
2. Math markdown reliability:
   • For single equations, use `$$ ... $$`.
   • For multi-step derivations, use one display block with `\begin{aligned} ... \end{aligned}`.
   • Do not split one derivation across multiple consecutive `$$ ... $$` lines.
   • Keep one blank line before opening `$$` and after closing `$$`.
3. Matplotlib output in marimo app view:
   • Return/output a figure object from the plotting cell (`plt.gcf()` or `fig`).
   • Do not use `plt.show()` for notebook output (console-focused).
4. Post-conversion cleanup:
   • Run `pixi run marimo check notebooks/<name>.py` after every converted notebook.
   • Expect auto-renamed variables from conversion when names collide; rename for readability when needed.
5. UI migration pattern:
   • Replace `ipywidgets` with `mo.ui.*` controls and wire values directly into computation cells.
   • For ODE demos, expose solver method/tolerances and perturbation controls to preserve exploratory pedagogy.

⸻

Questions / information needed (only if blocked)
	•	Desired Python version target (3.10 vs 3.11 vs 3.12) for the course refresh.
	•	Whether you want to keep Binder/legacy runtime (runtime.txt) operational during the pilot, or deprecate it immediately.
	•	Where you want the marimo notebooks referenced from the website (calendar pages vs a dedicated “Marimo” page).
