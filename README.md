# Thaarak Sriram — portfolio

A static personal site with four pages: About, Research, Projects and Press. Plain HTML and CSS, one self-hosted typeface, no JavaScript, and nothing loaded from other servers.

## Preview

```sh
python3 scripts/build.py
python3 -m http.server 4173 --bind 127.0.0.1
```

Open http://127.0.0.1:4173. All links are relative, so the same files work at `/` and at GitHub Pages' `/portfolio/` path.

## Edit

| To change | Edit |
| --- | --- |
| Home page text, the "Lately" list, the quote | `content/pages/home.html` |
| Research page text and the list of papers and talks | `content/pages/research.html` |
| Projects (text, figures, links) and "Smaller things" | `content/projects.json` |
| Press stories and their sources | `content/press.json` |
| Navigation, footer links, page descriptions | `scripts/build.py` |
| Type, color, spacing, layout | `style.css` |

Run `python3 scripts/build.py` after any change and commit the generated HTML with it. Python is only an authoring tool; hosting serves the files as they are.

A project's figure is one of three kinds: `image` (a screenshot in `images/`), `paper` (a typeset title block) or `table` (a small results table).

## Check

```sh
python3 scripts/check.py
```

Checks local links, image paths and dimensions, fragment targets, page metadata and landmarks, and that no press link is listed twice.

## Hosting

The live site is https://thaarak.github.io/portfolio/. GitHub Pages publishes the repository root from `main`, and `.nojekyll` makes it serve the HTML untouched. Work on a branch, run the build and the check, then merge to `main` to publish.

See `DESIGN.md` for the design reasoning and `SOURCES.md` for where the content comes from.
