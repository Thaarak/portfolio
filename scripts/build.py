"""Generate the site's four pages from the files in content/.

Run from anywhere:  python3 scripts/build.py
Prose for Home and Research lives in content/pages/*.html.
Projects and press entries live in content/*.json.
"""
import json
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://thaarak.github.io/portfolio/'
NAME = 'Thaarak Sriram'
EMAIL = 'thaarak.sriram@gmail.com'
NAV = [('About', ''), ('Research', 'research/'), ('Projects', 'projects/'), ('Press', 'press/')]
ELSEWHERE = [
    ('Email', f'mailto:{EMAIL}'),
    ('GitHub', 'https://github.com/Thaarak'),
    ('LinkedIn', 'https://www.linkedin.com/in/thaarak-sriram/'),
    ('X', 'https://x.com/SriramThaa'),
]


def e(text):
    return escape(text, quote=True)


def link(label, url):
    return f'<a href="{e(url)}">{e(label)}</a>'


def load(name):
    return json.loads((ROOT / 'content' / name).read_text())


def fragment(name):
    return (ROOT / 'content' / 'pages' / name).read_text()


def render(path, section, description, body):
    depth = len(Path(path).parts) - 1
    base = '../' * depth or './'
    title = NAME if section == 'About' else f'{section} · {NAME}'
    nav = ''.join(
        f'<a href="{base}{url}"' + (' aria-current="page"' if label == section else '') + f'>{label}</a>'
        for label, url in NAV
    )
    elsewhere = ' · '.join(link(label, url) for label, url in ELSEWHERE)
    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{SITE}images/portrait.jpg">
  <link rel="canonical" href="{SITE}{path.replace('index.html', '')}">
  <link rel="icon" href="{base}images/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="{base}fonts/newsreader-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{base}style.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="masthead">
    <div class="shell">
      <a class="name" href="{base}">{NAME}</a>
      <nav aria-label="Main">{nav}</nav>
    </div>
  </header>
  <main id="main">
{body.replace('@BASE@', base)}
  </main>
  <footer class="foot">
    <div class="shell">
      <p class="elsewhere">{elsewhere}</p>
      <p class="where">Livermore, then La Jolla. Updated {date.today():%B %Y}.</p>
    </div>
  </footer>
</body>
</html>
'''
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)


# Projects ------------------------------------------------------------------

def project_figure(p):
    f = p['figure']
    caption = f'<figcaption>{e(f["caption"])}</figcaption>' if f.get('caption') else ''
    if f['type'] == 'image':
        src = f'@BASE@images/{f["src"]}'
        inner = (f'<a class="shot" href="{src}"><img src="{src}" alt="{e(f["alt"])}" '
                 f'width="{f["width"]}" height="{f["height"]}" loading="lazy"></a>')
    elif f['type'] == 'paper':
        inner = (f'<div class="paper"><p class="t">{e(f["title"])}</p><p class="s">{e(f["subtitle"])}</p>'
                 f'<p class="a">{e(f["authors"])}</p><p class="v">{e(f["venue"])}</p></div>')
    else:
        head = ''.join(f'<th scope="col">{e(h)}</th>' for h in f['head'])
        rows = ''.join('<tr>' + ''.join(f'<td>{e(c)}</td>' for c in row) + '</tr>' for row in f['rows'])
        inner = f'<div class="sheet"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'
    return f'<figure>{inner}{caption}</figure>'


def projects_page():
    data = load('projects.json')
    body = f'<div class="shell page">\n<h1 class="vh">Projects</h1>\n<p class="lead">{e(data["lead"])}</p>\n'
    for p in data['projects']:
        paras = ''.join(f'<p>{para}</p>' for para in p['paras'])  # paragraphs may contain links
        caveat = f'<p class="caveat">{e(p["note"])}</p>' if p['note'] else ''
        links = ''.join(link(*pair) for pair in p['links'])
        body += (f'<article class="project" id="{p["slug"]}">{project_figure(p)}'
                 f'<div><h2>{e(p["name"])}</h2><p class="meta">{e(p["meta"])}</p>'
                 f'{paras}{caveat}<p class="links">{links}</p></div></article>\n')
    items = ''.join(f'<li>{link(name, url)}<span>{e(text)}</span></li>' for name, url, text in data['smaller'])
    body += f'<section class="smaller" aria-labelledby="smaller"><h2 id="smaller">Smaller things</h2><ul class="log">{items}</ul></section>\n</div>'
    render('projects/index.html', 'Projects',
           'Software by Thaarak Sriram: Morro, OceanOps, CourseLens and others, with what each does and which part was his.',
           body)
    return len(data['projects'])


# Press ---------------------------------------------------------------------

def press_page():
    data = load('press.json')
    body = f'<div class="shell page">\n<h1 class="vh">Press</h1>\n<p class="lead">{e(data["lead"])}</p>\n'
    count = 0
    for s in data['stories']:
        sources = ''
        for src in s['sources']:
            count += 1
            sources += (f'<li><span class="pub">{e(src["publisher"])}</span>{link(src["title"], src["url"])}'
                        f'<span class="detail">{e(src["detail"])}</span></li>')
        text = f'<p class="text">{e(s["text"])}</p>' if s['text'] else ''
        photo = ''
        if s.get('photo'):
            ph = s['photo']
            photo = (f'<figure class="photo"><img src="@BASE@images/{ph["src"]}" alt="{e(ph["alt"])}" '
                     f'width="{ph["width"]}" height="{ph["height"]}" loading="lazy">'
                     f'<figcaption>{link(ph["credit"], ph["credit_url"])}</figcaption></figure>')
        classes = 'story' + (' has-photo' if photo else '') + (' has-text' if text else '')
        body += (f'<section class="{classes}" id="{s["slug"]}" aria-labelledby="{s["slug"]}-title">'
                 f'<p class="years">{e(s["years"])}</p>'
                 f'<div class="body"><div><h2 id="{s["slug"]}-title">{e(s["title"])}</h2>{text}'
                 f'<ul class="sources">{sources}</ul></div>{photo}</div></section>\n')
    body += f'<p class="aside-note">{e(data["note"])} <a href="mailto:{EMAIL}">Email me</a>.</p>\n</div>'
    render('press/index.html', 'Press',
           'Articles, announcements and videos about work Thaarak Sriram has been part of, grouped by story.',
           body)
    return count


render('index.html', 'About',
       'Thaarak Sriram studies data science and physics at UC San Diego and does research on climate models and on how people review the work of AI coding agents.',
       fragment('home.html'))
render('research/index.html', 'Research',
       'Research by Thaarak Sriram: marine cloud brightening in a differentiable climate model, and how instructors review course updates made by AI coding agents.',
       fragment('research.html'))
n_projects = projects_page()
n_sources = press_page()
print(f'Built 4 pages: {n_projects} projects, {n_sources} press links.')
