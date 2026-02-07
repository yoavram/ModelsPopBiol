# Marimo + Pixi Pilot Guide

This pilot replaces the first two lecture notebooks with marimo notebooks and uses pixi for a reproducible environment.

## 1) Install prerequisites

1. Install pixi: <https://pixi.sh/latest/>
2. Install VS Code: <https://code.visualstudio.com/>
3. Install VS Code extensions:
   - Python (Microsoft)
   - Jupyter (Microsoft, optional for legacy `.ipynb` files)

## 2) Create the environment

Run from the repository root:

```bash
pixi install --locked
```

For maintainers updating dependencies/lock:

```bash
pixi install
```

## 3) Open marimo notebooks

```bash
pixi run marimo edit notebooks/population-growth.py
pixi run marimo edit notebooks/predator-prey.py
```

## 4) VS Code interpreter

Use the pixi Python interpreter:

1. macOS/Linux: `.pixi/envs/default/bin/python`
2. Windows: `.pixi\\envs\\default\\python.exe`

## 5) Agent use expectations

You are encouraged to use coding agents (GitHub Copilot / Gemini) for:

1. Refactoring code into smaller functions.
2. Debugging runtime or plotting errors.
3. Exploring parameter sweeps.
4. Writing tests for reusable helper functions.

Use agent output critically and verify numerical/biological interpretation.
