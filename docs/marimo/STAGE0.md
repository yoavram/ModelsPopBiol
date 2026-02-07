# Stage 0: Preflight for pixi + marimo migration

Date: 2026-02-07
Branch: `marimo`
Scope: pilot migration for first two notebooks

## 1) Current state snapshot (validated)

1. The repository is on branch `marimo`.
2. `pixi` is installed locally (`pixi 0.57.0`), but there is no `pixi.toml` or `pixi.lock` in the repo yet.
3. `marimo` is not available globally in `PATH` yet (expected before pixi env setup).
4. Pilot targets still use Jupyter-specific features:
   - `notebooks/population-growth.ipynb` includes `%matplotlib inline`.
   - `notebooks/predator-prey.ipynb` includes `%matplotlib inline` and `ipywidgets.interact(...)`.
5. Course setup docs are still mamba/conda + Jupyter based:
   - `www/content/setup/contents.lr`
6. Pilot lecture links still point to `.ipynb` notebooks:
   - `www/content/calendar/L2/contents.lr`
   - `www/content/calendar/L3/contents.lr`
7. Legacy Binder runtime file exists:
   - `runtime.txt` (Python `3.8`)

## 2) Guardrails for migration execution

1. Keep changes incremental and reviewable:
   - Stage 1: environment + docs scaffolding only.
   - Stage 2: convert exactly two notebooks (`population-growth`, `predator-prey`).
   - Stage 3: website/link updates for pilot visibility.
2. Keep legacy `.ipynb` files during pilot; do not remove them in first pass.
3. Use lockfile discipline:
   - Maintainers update lock with `pixi install`.
   - Reproducibility check uses `pixi install --locked`.
4. Avoid accidental scope creep:
   - Do not migrate assignments/project pages in pilot unless explicitly requested.
   - Do not include Lektor/site-build dependencies in pixi course env unless needed for notebook execution.
5. Keep commits atomic and stage-specific.

## 3) Stage 1 decisions (confirmed)

1. Python target for pixi environment:
   - Decision: use Python `3.11`.
   - Rationale: best compatibility margin across conda-forge and scientific stack while still modern.
2. Legacy Binder policy (`runtime.txt`):
   - Decision: Binder is no longer needed in the migration.
3. Where to expose marimo/molab links in pilot:
   - Decision: calendar pages only (`L2`, `L3`).
   - Timing: postpone to Stage 1b.

## 4) Stage 0 exit criteria

1. This preflight document is committed.
2. The three migration decisions are confirmed.
3. Stage 0 is complete; Stage 1 can begin.
