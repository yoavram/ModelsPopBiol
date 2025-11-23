# Repository Guidelines

## Overview
Static site for Models in Population Biology (Tel Aviv University) built with **Lektor** (Python/Jinja). Source lives under `www/`; the site is served at `https://modelspopbiol.yoavram.com/`. Lektor turns content (`.lr` files) into static HTML using models and templates.

## Project Structure & Module Organization
- `content/`: Lektor content. Root page is `content/contents.lr`; subsections include `assignments/`, `calendar/`, and `project/`. Each page or event has its own folder with `contents.lr` declaring `_model`/`_template`.
- `templates/`: Jinja2 templates. `layout.html` holds navigation, head, and footer; `index.html`, `page.html`, `calendar.html`, and `event.html` render specific views; shared macros in `templates/macros/`.
- `models/`: Data models (`*.ini`) that define fields for pages, calendars, and events—ensure new content matches the right model.
- `assets/static/`: CSS, fonts, images served via `/static/` (e.g., `style.css`, `LifeSciLogo.png`).

## Build, Test, and Development Commands
- `pip install lektor` (first run): Install the generator.
- `lektor serve --port 5000`: Live dev server with auto-reload at `http://localhost:5000`.
- `lektor build -O build`: Generate static output for review; treat warnings as blockers.
- `lektor deploy`: Only if a deploy target is configured; otherwise push built output per hosting instructions.

## Coding Style & Naming Conventions
- HTML/Jinja: 2-space indent; keep block structure and whitespace control tags intact. Use concise names (`this`, `child`) and existing macros for repeated UI.
- CSS (`assets/static/style.css`): Two-space indentation; leverage Bootstrap 4.1 utilities before adding custom rules.
- Content: Lowercase slugs for folders (`content/calendar/new-event/contents.lr`); set `_model`/`_template` explicitly when deviating from defaults.

## Testing Guidelines
- No automated tests. Use `lektor build` to catch template/content errors and broken references.
- Manually verify in `lektor serve`: navigation, dates, links (Moodle, GitHub archives), and responsive layout on mobile widths.
- For new events/assignments/projects, double-check dates and that linked assets resolve under `/static/`.

## Commit & Pull Request Guidelines
- Commit messages: short, imperative (`update calendar dates`, `remove assignment solutions`); keep related changes together.
- PRs: describe scope (content vs templates vs assets) and manual checks performed (`lektor build`, pages clicked). Include screenshots/GIFs for visual changes and link relevant course issues/deployment notes.
- Do not commit secrets or private course materials; host student-facing assets in `assets/static/` and link via the Jinja `url` filter.
