# Thaarak Sriram — portfolio

A static personal website: About, Projects, Research, Coverage, and Contact, with nine project detail pages. Plain HTML and CSS; no browser JavaScript, package installation, third-party fonts, or API keys.

## Preview

```sh
python3 scripts/build.py
python3 -m http.server 4173 --bind 127.0.0.1
```

Open http://127.0.0.1:4173. All links are relative, so the same files work at `/` or GitHub Pages' `/portfolio/` path.

## Edit

- `content/selected-projects.json`: homepage selection, matching the three GitHub pins checked November 15, 2026.
- `content/projects.json`: project descriptions, contributions, images, and demo links.
- `content/coverage.json`: article metadata and original publisher links, grouped by reporting, announcements, and conversations.
- `scripts/build.py`: shared HTML layout and About, Research, and Contact copy.
- `style.css`: typography, spacing, and responsive layout.
- `images/`: original portrait (preserved), optimized portrait, and public project screenshots.

Run `python3 scripts/build.py` after content or template changes and commit the generated HTML. Hosting serves these files directly; Python is only an authoring tool.

## Check

```sh
python3 scripts/check.py
```

Checks internal links, image paths, fragment targets, page metadata, and landmark structure. Run this check after regenerating the pages.

## Hosting

The live site is https://thaarak.github.io/portfolio/. GitHub Pages publishes the repository root from `main`. The `.nojekyll` file serves the generated HTML directly. Develop changes on `codex/portfolio-v1`, run the build and checks, then merge to `main` to publish.

See `SOURCES.md` for content provenance and `DESIGN.md` for the first-version design rationale.
