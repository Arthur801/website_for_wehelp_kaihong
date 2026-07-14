# Repository Guidelines

## Project Structure & Module Organization

This repository contains weekly WeHelp assignments rather than one packaged application. Keep work scoped to its assignment directory:

- `week1/`–`week3/`: static HTML/CSS/JavaScript exercises; `week3/` also contains Python data work and CSV inputs.
- `week4/` and `week6/`: FastAPI applications. Each keeps route code in `main.py`, templates in `templates/`, and browser assets in `static/`.
- `week5/`: SQL assignment in `data.sql`, supporting screenshots, and its own README.
- Root `index.html` and `style.css`: standalone site files. `Pipfile` holds Python environment metadata.

Do not move files between weeks or combine static assets across applications: FastAPI directories are resolved relative to the directory where the app is run.

## Build, Test, and Development Commands

Use the project’s Pipenv environment for Python work:

```bash
pipenv install
cd week6 && pipenv run uvicorn main:app --reload
cd week4 && pipenv run uvicorn main:app --reload
```

The last two commands serve the relevant FastAPI assignment with automatic reload. Install required runtime dependencies in the same environment before running it. There is no automated test suite or build step; manually exercise affected routes and browser interactions.

## Coding Style & Naming Conventions

Follow the surrounding code’s language and layout. Use four spaces for Python indentation, `snake_case` for functions and variables, `UPPER_CASE` for constants such as `USER_DATABASE`, and descriptive route-handler names. Keep FastAPI routes asynchronous where the module does. Use lowercase, hyphen-free names such as `main.py`, `index.html`, and `script.js`; place templates and assets in the matching week folder. No formatter or linter is configured.

## Testing Guidelines

For FastAPI changes, start the affected app and verify success and error paths, session-dependent pages, redirects, and static asset loading. For SQL changes, validate statements against the assignment schema and update related screenshots only when output changes. If adding tests, use `pytest`, place them in a nearby `tests/` directory, and name files `test_*.py`.

## Commit & Pull Request Guidelines

History uses short imperative summaries (`Finish week 5 assignment`, `Add data.sql in week5`) and occasional Conventional Commit prefixes (`chore: retry GitHub Pages deployment`). Use a concise subject that states the affected assignment and change, e.g. `week6: validate signup input`. Keep commits focused. Pull requests should explain the assignment impact, list manual verification, link related issues when applicable, and include screenshots for visible HTML/CSS changes.
