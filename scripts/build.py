"""Generate dependency-free, readable HTML. Run from any directory."""
import json
from pathlib import Path
from html import escape as e

ROOT = Path(__file__).resolve().parents[1]
projects = json.loads((ROOT / 'content/projects.json').read_text())
coverage = json.loads((ROOT / 'content/coverage.json').read_text())
NAV = [('About', ''), ('Projects', 'projects/'), ('Research', 'research/'), ('Coverage', 'coverage/'), ('Contact', 'contact/')]

def link(label, url):
    return f'<a href="{e(url, quote=True)}">{e(label)}</a>'

def render(path, title, description, body, section):
    depth = len(Path(path).parts) - 1
    base = '../' * depth or './'
    nav = ''.join(f'<a href="{base}{url}"'+ (' aria-current="page"' if label == section else '') + f'>{label}</a>' for label, url in NAV)
    canonical = 'https://thaarak.github.io/portfolio/' + path.replace('index.html', '')
    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)} — Thaarak Sriram</title>
  <meta name="description" content="{e(description, quote=True)}">
  <meta property="og:title" content="{e(title, quote=True)} — Thaarak Sriram">
  <meta property="og:description" content="{e(description, quote=True)}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="https://thaarak.github.io/portfolio/images/portrait.jpg">
  <link rel="canonical" href="{canonical}">
  <link rel="icon" href="{base}images/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{base}style.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <div class="site">
    <header class="site-header">
      <a class="name" href="{base}">Thaarak Sriram</a>
      <nav aria-label="Main navigation">{nav}</nav>
    </header>
    <main id="main">{body.replace('@BASE@', base)}</main>
    <footer class="site-footer"><span>Thaarak Sriram</span><div>{link('Email', 'mailto:thaarak.sriram@gmail.com')}{link('GitHub', 'https://github.com/Thaarak')}{link('LinkedIn', 'https://www.linkedin.com/in/thaarak-sriram/')}</div></footer>
  </div>
</body>
</html>
'''
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)

def figure(p):
    if not p['image']: return ''
    return f'<figure><a href="@BASE@images/{p["image"]}"><img src="@BASE@images/{p["image"]}" alt="{e(p["alt"], quote=True)}" loading="lazy" width="1200" height="750"></a><figcaption>{e(p["caption"])}</figcaption></figure>'

home = '''<section class="introduction" aria-labelledby="intro-title">
  <div class="intro-copy"><h1 id="intro-title">Hi, I’m Thaarak.</h1>
    <p class="lead">I study data science and physics at UC San Diego. My work spans climate modeling, human–computer interaction, and AI evaluation.</p>
    <p>I’m interested in how we understand complex systems, and how we make the tools built around them useful and trustworthy.</p>
    <p>That takes a few forms: simulating weather interventions, building interfaces people can inspect, and working on climate education in my community.</p>
    <p class="inline-links"><a href="@BASE@projects/">Explore my projects</a><a href="@BASE@contact/">Get in touch</a></p>
  </div>
  <figure class="portrait"><img src="@BASE@images/portrait.jpg" alt="Thaarak Sriram" width="640" height="800" fetchpriority="high"><figcaption>San Diego, California</figcaption></figure>
</section>
<section class="home-section" aria-labelledby="working-title"><h2 id="working-title">What I’m working on</h2>
  <div><p>I do research in climate modeling and human–computer interaction, alongside building small software tools. I work primarily with Python, JAX, TypeScript, and React.</p><p>My <a href="@BASE@research/">research interests</a> connect the modeling and evaluation side of this work. The <a href="@BASE@projects/">project pages</a> collect public code, demos, and what I contributed.</p></div>
</section>
<section class="home-section" aria-labelledby="selected-title"><h2 id="selected-title">Selected projects</h2><div class="selected-list">'''
for p in projects[:3]:
    home += f'<article><h3><a href="@BASE@projects/{p["slug"]}/">{e(p["name"])}</a></h3><p>{e(p["summary"])}</p></article>'
home += '''<p><a href="@BASE@projects/">All projects</a></p></div></section>
<section class="home-section" aria-labelledby="beyond-title"><h2 id="beyond-title">Climate work, closer to home</h2><div>
<p>Before UC San Diego, I helped organize the Livermore Youth Climate Summit and establish the Tri-Valley Youth Climate Action Program. With three other students, I helped develop a climate-literacy resolution adopted by our school district in October 2024.</p>
<p>The <a href="@BASE@coverage/">coverage page</a> brings together reporting on that work, award announcements, and conversations.</p></div></section>'''
render('index.html', 'About', 'Data science and physics at UC San Diego. Climate modeling, human–computer interaction, and public software projects.', home, 'About')

body = '''<header class="page-intro"><h1>Projects</h1><p class="lead">Things I’ve built, and what I learned building them.</p><p>Public projects, team collaborations, and smaller experiments. Each entry describes my contribution and links to the code.</p></header><div class="project-list">'''
for p in projects:
    img = f'<a class="project-image" href="@BASE@projects/{p["slug"]}/"><img src="@BASE@images/{p["image"]}" alt="{e(p["alt"], quote=True)}" loading="lazy" width="600" height="375"></a>' if p['image'] else '<div class="project-diagram" aria-label="Pipeline: registry records, qualification, scoring, shortlist"><span>Registry records</span><span>Qualify</span><span>Score & explain</span><span>Shortlist</span></div>'
    body += f'<article class="project-row">{img}<div><p class="meta">{p["area"]}</p><h2><a href="@BASE@projects/{p["slug"]}/">{p["name"]}</a></h2><p>{p["summary"]}</p><a href="@BASE@projects/{p["slug"]}/">About the project</a></div></article>'
body += '''</div><section class="reading-width"><h2>Earlier work</h2><p>I was also part of <a href="https://gravitechx.weebly.com/student-leads.html">GravitechX</a>, Livermore High School’s robotics team. My GitHub includes a <a href="https://github.com/Thaarak/2023-Coding">fork of the team’s 2023 Java robot code</a>.</p><p>This website is also <a href="https://github.com/Thaarak/portfolio">on GitHub</a>.</p></section>'''
render('projects/index.html', 'Projects', 'Public software projects by Thaarak Sriram, with demos, screenshots, and individual contributions.', body, 'Projects')
for i,p in enumerate(projects):
    links = [[ 'Source code', 'https://github.com/Thaarak/'+p['repo']]] + p['links']
    body = f'''<a class="back-link" href="@BASE@projects/">All projects</a><header class="page-intro"><p class="meta">{p['area']}</p><h1>{p['name']}</h1><p class="lead">{p['summary']}</p><div class="inline-links">{''.join(link(*x) for x in links)}</div></header>{figure(p)}<div class="reading-width project-copy"><h2>The project</h2><p>{p['body']}</p><h2>My contribution</h2><p>{p['contribution']}</p><h2>Context</h2><p>{p['context']}</p><p class="note">{p['limits']}</p></div>'''
    if i+1 < len(projects):
        nxt=projects[i+1]
        body+=f'<p class="next-project">Next project: <a href="@BASE@projects/{nxt["slug"]}/">{nxt["name"]}</a></p>'
    render(f'projects/{p["slug"]}/index.html', p['name'], p['summary'], body, 'Projects')

body='''<header class="page-intro"><h1>Research</h1><p class="lead">Climate models, AI systems, and the people using them.</p></header><div class="reading-width"><section><h2>Climate modeling</h2><p>I’m interested in how physical models and machine learning can help us understand the climate, and how to evaluate what those models tell us.</p><p>My public project <a href="@BASE@projects/morro/">Morro</a> explores forecasts and simulated cloud-seeding interventions. It compares perturbed and unperturbed weather-model runs, with a dashboard for examining the differences.</p></section><section><h2>Human–computer interaction</h2><p>I also work in human–computer interaction, with an interest in evaluating AI systems and making them safer to use. I’m part of UC San Diego’s <a href="https://dstl.ucsd.edu/">Data Science Teaching and Learning Lab</a>.</p><p>Some of that interest shows up in my software: <a href="@BASE@projects/arnold/">Arnold</a> asks people to review a meal entry before saving it, and <a href="@BASE@projects/wendy/">Wendy</a> separates drafting an inquiry from sending one.</p></section><section><h2>Earlier research</h2><p>At UC Santa Barbara’s 2024 Summer Research Academies, I worked with Haeum Lee and Simran Karkhanis on <em>Soil and Solar: Analyzing the Social Barriers to Agrivoltaics Implementation in the United States</em>.</p><p>Our capstone talk is listed in the <a href="https://www.summer.ucsb.edu/sites/default/files/documents/SRA/2024%20SRA%20Program.pdf">2024 program</a> (page 11).</p></section><section><h2>From models to decisions</h2><p>The questions I keep returning to are practical: What can we check? What does a result actually show? How much should someone trust it?</p><p>For public code and demonstrations, see my <a href="@BASE@projects/">projects</a>. For research conversations, <a href="mailto:thaarak.sriram@gmail.com">email me</a>.</p></section></div>'''
render('research/index.html','Research','Research interests in climate modeling, human–computer interaction, and AI evaluation.',body,'Research')

body='''<header class="page-intro"><h1>Coverage & conversations</h1><p class="lead">A collection of stories about work I’ve been part of.</p><p>Much of this began with climate education in Livermore. These articles tell the story of a shared effort by students, mentors, and our community.</p></header>'''
for kind in ['Reporting','Announcements','Conversations']:
    body+=f'<section class="coverage-section"><h2>{kind}</h2><div>'
    for c in coverage:
        if c['kind'] != kind: continue
        body+=f'<article class="coverage-entry"><p class="meta">{e(c["publisher"])} <span class="date">{e(c["date"])}</span></p><h3>{link(c["title"],c["url"])}</h3><p>{e(c["summary"])}</p></article>'
    body+='</div></section>'
body+='<p class="note">The climate-storytelling appearance is also listed on <a href="https://quest-science.org/press-coverage/">Quest Science Center’s coverage page</a>. Articles remain on their publishers’ websites; some links open PDF editions.</p>'
render('coverage/index.html','Coverage','Reporting, announcements, and conversations featuring Thaarak Sriram’s climate education and community work.',body,'Coverage')

body='''<header class="page-intro"><h1>Get in touch</h1><p class="lead">For a project, a research question, or a conversation.</p></header><div class="reading-width"><p>The best way to reach me is by email.</p><p class="contact-email"><a href="mailto:thaarak.sriram@gmail.com">thaarak.sriram@gmail.com</a></p><p>I’m based in San Diego and study at UC San Diego.</p><dl class="contact-links"><dt>Code</dt><dd><a href="https://github.com/Thaarak">GitHub</a></dd><dt>Professional background</dt><dd><a href="https://www.linkedin.com/in/thaarak-sriram/">LinkedIn</a></dd><dt>Elsewhere</dt><dd><a href="https://x.com/SriramThaa">X</a></dd></dl></div>'''
render('contact/index.html','Contact','Contact Thaarak Sriram about research, software projects, and collaboration.',body,'Contact')
print(f'Generated {5+len(projects)} pages.')
