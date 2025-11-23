# Repository Guidelines

## Project Structure & Module Organization
- `content/`: Lektor content in `.lr` files. Root page lives in `content/contents.lr`; child sections like `assignments/`, `calendar/`, and `project/` hold page/event data. New pages get their own folder plus `contents.lr`.
- `templates/`: Jinja2 templates. `layout.html` defines navigation and shared head/footer, while `index.html`, `page.html`, `calendar.html`, and `event.html` render specific views. Macros live in `templates/macros/`.
- `models/`: Lektor data models (`*.ini`) that define fields for pages, calendars, and events. Align new content with the matching model.
- `assets/static/`: CSS, fonts, and images served under `/static/` (e.g., `style.css`, `LifeSciLogo.png`).

## Build, Test, and Development Commands
- `pip install lektor` (once): Installs the static site generator.
- `lektor serve --port 5000`: Run a live dev server with auto-reload at `http://localhost:5000`.
- `lektor build -O build`: Produce static output for manual inspection; treat build warnings as blockers.
- `lektor deploy`: Use only if a deploy target is configured; otherwise push changes to the hosting branch as instructed.

## Coding Style & Naming Conventions
- Keep HTML/Jinja indentation at 2 spaces; preserve existing block structure and whitespace control (`{% ... %}` vs `{{ ... }}`).
- CSS in `assets/static/style.css` follows compact, two-space indentation; group related rules and prefer utility classes already present from Bootstrap 4.1.
- Content filenames use lowercase slugs (`content/calendar/new-event/contents.lr`). Set `_model` and `_template` explicitly when diverging from defaults.
- Favor concise variable names in templates (`this`, `child`) and reuse shared macros when adding pagination or repeated UI.

## Testing Guidelines
- No automated tests; rely on `lektor build` to surface template/content errors. Fix any warnings before committing.
- Manually click through modified pages in `lektor serve`, checking navigation, dates, and external links (Moodle/GitHub archives) on desktop and mobile widths.
- When adding events or assignments, confirm dates/times render correctly and that downloadable assets resolve under `/static/`.

## Commit & Pull Request Guidelines
- Commit messages in this repo are short, imperative statements (`update calendar dates`, `remove assignment solutions`). Follow that style and keep related changes in one commit when possible.
- PRs should describe the change, the affected sections (content vs templates vs assets), and manual verification performed (`lektor build`, pages clicked).
- Include before/after screenshots or recorded GIFs for visual changes to templates or styles; link any related course issue or deployment note.
- Avoid committing secrets or private course materials; keep student-facing assets in `assets/static/` and reference them via the Jinja `url` filter.
