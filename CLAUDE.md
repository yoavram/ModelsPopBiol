# Models in Population Biology

## Publishing assignments and solutions

Course materials (assignments, solutions, lectures) are published on the course website via the Lektor static site under `www/`.

To publish a new assignment or solution, update the corresponding calendar entry at `www/content/calendar/<ID>/contents.lr` — edit the `materials:` field to add or update links pointing to the file on GitHub (e.g. `https://github.com/yoavram/ModelsPopBiol/blob/master/solutions/A0.py`).

**Do not use Google Calendar** — "publish to calendar" always means `www/content/calendar/`.

## Notebooks

Course notebooks and assignments use **Marimo** (`.py` files), not Jupyter. Use the Notebook tool for `.ipynb` files and the standard file tools (Read/Edit/Write) for marimo `.py` files.

## Migrating assignments from Jupyter to Marimo

Source Jupyter notebooks live in the sibling repo at `../ModelsPopBiolSol/2023/{assignments,solutions}/A*.ipynb`; targets are `{assignments,solutions}/A*.py`. Use an already-migrated assignment (`assignments/A1.py`, `solutions/A1.py`) as the structural reference.

Key rules:
- Preserve `###` grading markers exactly — lines ending with `###` and cells starting with `###` are used by the autograder. Keep them in both the assignment skeleton and the solution.
- **All top-level names must be unique across cells**, otherwise marimo raises `MultipleDefinitionError` at app load. If the Jupyter source defines `ode` (or any name) in two cells, rename or alias one (e.g. `ode_crossfeed = ode`). Loop/unpacking variables that would collide with other cells should be prefixed `_`.
- Drop IPython magics like `%matplotlib inline`.
- Validate with `pixi run marimo-check <file>` (warnings about empty stub cells and single-line markdown indentation are expected; errors are not), then smoke-test with `pixi run python solutions/<X>.py`. The assignment file will error on its empty stubs — that's expected.

See `AGENTS.md` ("Migrating Jupyter Notebooks To Marimo") for the full workflow, widget patterns, and publishing.
