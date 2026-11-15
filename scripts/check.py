"""Validate generated pages and local links without third-party dependencies."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json

ROOT = Path(__file__).resolve().parents[1]
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
            if a['id'] in self.ids: self.errors.append('duplicate id: ' + a['id'])
            self.ids.add(a['id'])
        if tag == 'html': self.lang = a.get('lang') == 'en'
        if tag == 'meta' and a.get('name') == 'description': self.description = bool(a.get('content'))
        if tag == 'a' and a.get('aria-current') == 'page': self.active = True
        if tag == 'img' and not a.get('alt'): self.errors.append('missing image alt')
        for key in ('href', 'src'):
            if key in a: self.links.append(a[key])

pages = {p.resolve(): Page(p) for p in ROOT.rglob('*.html') if '.git' not in p.parts}
errors = []
for path, page in pages.items():
    for tag in ('h1','main','title','nav'):
        if page.tags.get(tag) != 1: page.errors.append(f'expected one {tag}')
    if not all((page.description,page.active,page.lang)): page.errors.append('missing metadata or active navigation')
    for href in page.links:
        u = urlsplit(href)
        if u.scheme or u.netloc: continue
        target = (path.parent / unquote(u.path)).resolve() if u.path else path
        if target.is_dir(): target /= 'index.html'
        if not target.exists(): page.errors.append(f'missing local target: {href}')
        elif u.fragment and target in pages and u.fragment not in pages[target].ids: page.errors.append(f'missing fragment: {href}')
    errors.extend(f'{path.relative_to(ROOT)}: {x}' for x in page.errors)
projects=json.loads((ROOT/'content/projects.json').read_text())
assert len({p['slug'] for p in projects}) == len(projects)
coverage=json.loads((ROOT/'content/coverage.json').read_text())
assert len({c['url'] for c in coverage}) == len(coverage)
selected=json.loads((ROOT/'content/selected-projects.json').read_text())
assert len(selected) == 3 and len(set(selected)) == 3
assert set(selected).issubset({p['slug'] for p in projects})
for c in coverage:
    assert c['image_alt'] and c['image_credit'] and c['image_source'].startswith('https://')
    assert (ROOT/'images'/c['image']).is_file(), c['title']
    assert c['image_width'] > 0 and c['image_height'] > 0
if errors: raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages; internal links, images, fragments, landmarks, metadata; {len(projects)} projects and {len(coverage)} unique coverage links.')
