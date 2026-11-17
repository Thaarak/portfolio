"""Check the generated pages: local links, images, fragments, landmarks, metadata."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', '.gstack', 'content', 'node_modules'}


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.links, self.ids, self.tags, self.errors = path, [], set(), {}, []
        self.description = self.active = self.lang = False
        self.feed(path.read_text())

    def handle_starttag(self, tag, pairs):
        a = dict(pairs)
        self.tags[tag] = self.tags.get(tag, 0) + 1
        if 'id' in a:
            if a['id'] in self.ids:
                self.errors.append('duplicate id: ' + a['id'])
            self.ids.add(a['id'])
        if tag == 'html':
            self.lang = a.get('lang') == 'en'
        if tag == 'meta' and a.get('name') == 'description':
            self.description = bool(a.get('content'))
        if tag == 'a' and a.get('aria-current') == 'page':
            self.active = True
        if tag == 'img':
            if not a.get('alt'):
                self.errors.append('image without alt text')
            if not (a.get('width') and a.get('height')):
                self.errors.append('image without width and height: ' + a.get('src', ''))
        for key in ('href', 'src'):
            if key in a:
                self.links.append(a[key])


pages = {p.resolve(): Page(p) for p in ROOT.rglob('*.html') if not SKIP & set(p.relative_to(ROOT).parts)}
errors = []
for path, page in pages.items():
    for tag in ('h1', 'main', 'title', 'nav'):
        if page.tags.get(tag) != 1:
            page.errors.append(f'expected exactly one <{tag}>')
    if not (page.description and page.active and page.lang):
        page.errors.append('missing description, lang, or active nav link')
    for href in page.links:
        u = urlsplit(href)
        if u.scheme or u.netloc:
            continue
        target = (path.parent / unquote(u.path)).resolve() if u.path else path
        if target.is_dir():
            target /= 'index.html'
        if not target.exists():
            page.errors.append(f'missing local target: {href}')
        elif u.fragment and target in pages and u.fragment not in pages[target].ids:
            page.errors.append(f'missing fragment: {href}')
    errors.extend(f'{path.relative_to(ROOT)}: {x}' for x in page.errors)

projects = json.loads((ROOT / 'content/projects.json').read_text())['projects']
slugs = [p['slug'] for p in projects]
if len(set(slugs)) != len(slugs):
    errors.append('content/projects.json: duplicate slug')

press = json.loads((ROOT / 'content/press.json').read_text())['stories']
urls = [s['url'] for story in press for s in story['sources']]
if len(set(urls)) != len(urls):
    errors.append('content/press.json: the same link is listed twice')
for u in urls:
    if not u.startswith('https://'):
        errors.append(f'content/press.json: not an https link: {u}')

if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages, {len(projects)} projects, {len(urls)} press links. '
      'Local links, images, fragments, landmarks and metadata are in order.')
