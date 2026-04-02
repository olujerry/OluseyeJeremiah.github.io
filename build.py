#!/usr/bin/env python3
"""
build.py — reads articles.json → writes index.html
Run locally:  python build.py
GitHub Actions runs this automatically on every push or weekly.
"""
import json, html, sys
from datetime import datetime, UTC
from pathlib import Path

articles_path = Path(__file__).parent / "articles.json"
with open(articles_path, encoding="utf-8") as f:
    articles = json.load(f)

total = len(articles)
platforms = sorted(set(a["platform"] for a in articles))

PLATFORM_CFG = {
    "DataCamp":    {"color":"#0f5bb5","bg":"#eef4fd","pid":"dc"},
    "freeCodeCamp":{"color":"#15803d","bg":"#f0faf4","pid":"fcc"},
    "Hackmamba":   {"color":"#c2410c","bg":"#fff7ed","pid":"hm"},
    "Medium":      {"color":"#15803d","bg":"#f0faf4","pid":"med"},
    "Twilio":      {"color":"#92400e","bg":"#fef9e6","pid":"twi"},
    "Strapi":      {"color":"#0e7490","bg":"#f0fdff","pid":"str"},
    "Dev.to":      {"color":"#6d28d9","bg":"#f5f3ff","pid":"dev"},
    "Hashnode":    {"color":"#2563eb","bg":"#eff6ff","pid":"hn"},
}

SEE_ALL = {
    "freeCodeCamp": ("All freeCodeCamp articles","https://www.freecodecamp.org/news/author/oluseye-jeremiah/"),
    "DataCamp":     ("All DataCamp articles","https://www.datacamp.com/blog"),
    "Medium":       ("All Medium articles","https://medium.com/@oluseyejeremiah"),
    "Twilio":       ("All Twilio articles","https://www.twilio.com/en-us/blog/authors/author.oluseye-jeremiah"),
    "Hackmamba":    ("All Hackmamba articles","https://dev.to/actiandev"),
}

PLATFORM_LINKS = {
    "DataCamp":    ("https://www.datacamp.com/blog","AI, ML, SQL, Git"),
    "freeCodeCamp":("https://www.freecodecamp.org/news/author/oluseye-jeremiah/","Python, SQL, Data · 14+ articles"),
    "Hackmamba":   ("https://dev.to/actiandev","AI, Developer tools · 50+ articles"),
    "Medium":      ("https://medium.com/@oluseyejeremiah","ML, AI, Cloud"),
    "Twilio":      ("https://www.twilio.com/en-us/blog/authors/author.oluseye-jeremiah","API, Voice, AI"),
    "Strapi":      ("https://strapi.io/user/oluseye-jeremiah","Next.js, Headless CMS"),
    "Hashnode":    ("https://oluseyejeremiah.hashnode.dev","Data Science, Cloud"),
    "Dev.to":      ("https://dev.to/oluseyej","AI Agents, Dev Tools"),
}

def pid(p):
    return PLATFORM_CFG.get(p,{}).get("pid", p.lower().replace(" ",""))

def render_card(a, idx):
    p    = a["platform"]
    cfg  = PLATFORM_CFG.get(p, {"color":"#555","bg":"#f5f5f5","pid":"x"})
    feat = a.get("featured", False)
    tags = "".join(f'<span class="t">{html.escape(t)}</span>' for t in a.get("tags",[]))
    note = "Featured" if feat else str(idx)
    span = " card-feat" if feat else ""
    sty  = f'background:{cfg["bg"]};color:{cfg["color"]};'
    return f"""
    <a class="card{span}" data-p="{pid(p)}" href="{html.escape(a['url'])}" target="_blank" rel="noopener">
      <div class="card-top">
        <span class="platform" style="{sty}">{html.escape(p)}</span>
        <span class="card-num">{html.escape(note)}</span>
      </div>
      <h2 class="card-title">{html.escape(a['title'])}</h2>
      <p class="card-excerpt">{html.escape(a.get('excerpt',''))}</p>
      <div class="card-foot">
        <div class="tags">{tags}</div>
        <span class="read-btn">Read{"&nbsp;article" if feat else ""}</span>
      </div>
    </a>"""

# filter buttons
filter_btns = '<button class="fb on" onclick="filter(\'all\',this)">All</button>\n'
for p in platforms:
    filter_btns += f'    <button class="fb" onclick="filter(\'{pid(p)}\',this)">{html.escape(p)}</button>\n'

# see-all buttons
see_all_html = ""
for p,(label,url) in SEE_ALL.items():
    see_all_html += f'<a class="see-all" href="{url}" target="_blank" rel="noopener">{label}</a>\n    '

# platform list
plat_html = ""
for p,(url,desc) in PLATFORM_LINKS.items():
    color = PLATFORM_CFG.get(p,{}).get("color","#888")
    plat_html += f"""
      <a class="plat-row" href="{url}" target="_blank" rel="noopener">
        <div class="plat-dot" style="background:{color};"></div>
        <span class="plat-name">{html.escape(p)}</span>
        <span class="plat-desc">{html.escape(desc)}</span>
        <span class="plat-arr">↗</span>
      </a>"""

# cards
idx = 1
cards_html = ""
for a in articles:
    cards_html += render_card(a, idx)
    if not a.get("featured"):
        idx += 1

now = datetime.now(UTC).strftime("%B %d, %Y")

CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
:root{
  --bg:#fafaf9;--white:#fff;--ink:#111110;--mid:#444440;--muted:#888884;
  --border:#e8e7e4;--border2:#d0cfc9;
  --accent:#0f5bb5;--accent-bg:#eef4fd;--accent-bd:#c3d8f5;
  --green:#15803d;
  --serif:'Playfair Display',serif;--sans:'Inter',sans-serif;
}
body{font-family:var(--sans);background:var(--bg);color:var(--ink);font-size:15px;line-height:1.6;}
a{color:inherit;text-decoration:none;}

/* hero */
.hero{background:var(--white);border-bottom:1px solid var(--border);padding:4rem 2rem 3rem;}
.hero-inner{max-width:1060px;margin:0 auto;}
.tag-row{display:flex;align-items:center;gap:10px;margin-bottom:1.5rem;flex-wrap:wrap;}
.tag-label{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--accent);font-weight:600;}
.tag-dot{width:4px;height:4px;border-radius:50%;background:var(--border2);}
.name{font-family:var(--serif);font-size:clamp(2.2rem,5vw,3.8rem);font-weight:700;line-height:1.1;letter-spacing:-.02em;margin-bottom:1rem;}
.name em{font-style:italic;font-weight:400;color:var(--muted);}
.bio{font-size:14.5px;color:var(--mid);line-height:1.85;max-width:600px;margin-bottom:1.5rem;}
.bio strong{color:var(--ink);font-weight:600;}
.chips{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:2rem;}
.chip{font-size:11.5px;font-weight:500;padding:5px 13px;border-radius:100px;background:var(--accent-bg);color:var(--accent);border:1px solid var(--accent-bd);}
.stats{display:flex;gap:2.5rem;flex-wrap:wrap;padding-top:1.75rem;border-top:1px solid var(--border);}
.st{display:flex;flex-direction:column;gap:3px;}
.st-n{font-family:var(--serif);font-size:1.7rem;font-weight:700;}
.st-l{font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);}
.updated{font-size:11px;color:var(--muted);margin-top:1rem;}
.updated span{color:var(--green);font-weight:600;}

/* filter */
.fbar{position:sticky;top:0;z-index:20;background:rgba(250,250,249,.95);backdrop-filter:blur(10px);border-bottom:1px solid var(--border);}
.fi{max-width:1060px;margin:0 auto;padding:0 2rem;display:flex;overflow-x:auto;scrollbar-width:none;align-items:stretch;}
.fi::-webkit-scrollbar{display:none;}
.fb{font-family:var(--sans);font-size:12.5px;padding:13px 14px;border:none;background:none;color:var(--muted);cursor:pointer;white-space:nowrap;border-bottom:2px solid transparent;transition:all .15s;}
.fb:hover{color:var(--ink);}
.fb.on{color:var(--accent);border-bottom-color:var(--accent);font-weight:600;}
.fcount{margin-left:auto;display:flex;align-items:center;font-size:12px;color:var(--muted);padding-left:1rem;white-space:nowrap;}

/* grid */
.main{max-width:1060px;margin:0 auto;padding:2.5rem 2rem 5rem;}
.sh{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);font-weight:600;margin-bottom:1.5rem;display:flex;align-items:center;gap:12px;}
.sh::after{content:'';flex:1;height:1px;background:var(--border);}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--border);border:1px solid var(--border);}
@media(max-width:800px){.grid{grid-template-columns:repeat(2,1fr);}}
@media(max-width:520px){.grid{grid-template-columns:1fr;}}
.card-feat{grid-column:span 2;}
@media(max-width:800px){.card-feat{grid-column:span 1;}}
.card{background:var(--white);padding:1.5rem;display:flex;flex-direction:column;gap:.8rem;transition:background .15s;}
.card:hover{background:#fdfcfa;}
.card-top{display:flex;align-items:center;justify-content:space-between;gap:.5rem;}
.platform{font-size:10px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;padding:3px 10px;border-radius:100px;}
.card-num{font-size:11px;color:var(--border2);font-weight:500;}
.card-title{font-family:var(--serif);font-size:.97rem;font-weight:700;line-height:1.35;color:var(--ink);}
.card-feat .card-title{font-size:1.15rem;}
.card-excerpt{font-size:13px;color:var(--muted);line-height:1.75;flex:1;}
.card-foot{margin-top:auto;display:flex;align-items:center;justify-content:space-between;padding-top:.85rem;border-top:1px solid var(--border);flex-wrap:wrap;gap:.5rem;}
.tags{display:flex;gap:5px;flex-wrap:wrap;}
.t{font-size:10.5px;background:var(--bg);color:var(--muted);padding:2px 9px;border-radius:100px;border:1px solid var(--border);}
.read-btn{font-size:12px;font-weight:600;color:var(--accent);display:inline-flex;align-items:center;gap:4px;white-space:nowrap;transition:gap .15s;}
.read-btn:hover{gap:7px;}
.read-btn::after{content:'→';}

/* see all */
.see-all-row{display:flex;gap:1rem;flex-wrap:wrap;margin-top:2rem;}
.see-all{font-size:13px;font-weight:600;color:var(--accent);border:1px solid var(--accent-bd);border-radius:6px;padding:9px 20px;background:var(--accent-bg);display:inline-flex;align-items:center;gap:6px;transition:background .15s;}
.see-all:hover{background:#ddeafb;}
.see-all::after{content:'↗';font-size:12px;}

/* about */
.about{margin-top:3rem;padding-top:2.5rem;border-top:1px solid var(--border);display:grid;grid-template-columns:1fr 1fr;gap:3rem;}
@media(max-width:680px){.about{grid-template-columns:1fr;gap:2rem;}}
.al{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);font-weight:600;margin-bottom:1rem;}
.an{font-family:var(--serif);font-size:1.4rem;font-weight:700;margin-bottom:.75rem;}
.at{font-size:13.5px;color:var(--mid);line-height:1.9;}
.at strong{color:var(--ink);font-weight:600;}
.plist{display:flex;flex-direction:column;gap:8px;}
.plat-row{display:flex;align-items:center;gap:11px;padding:10px 14px;border:1px solid var(--border);border-radius:7px;transition:background .15s,border-color .15s;}
.plat-row:hover{background:var(--accent-bg);border-color:var(--accent-bd);}
.plat-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}
.plat-name{font-size:13px;font-weight:600;color:var(--ink);}
.plat-desc{font-size:11.5px;color:var(--muted);margin-left:auto;}
.plat-arr{font-size:12px;color:var(--border2);}

/* footer */
footer{border-top:1px solid var(--border);max-width:1060px;margin:0 auto;padding:1.5rem 2rem;display:flex;justify-content:space-between;align-items:center;font-size:11.5px;color:var(--muted);flex-wrap:wrap;gap:.75rem;}
.fd{display:flex;align-items:center;gap:7px;}
.fdot{width:7px;height:7px;border-radius:50%;background:var(--green);animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:.3;}}
"""

JS = """
function filter(p, btn) {
  document.querySelectorAll('.fb').forEach(b => b.classList.remove('on'));
  btn.classList.add('on');
  let n = 0;
  document.querySelectorAll('#grid .card').forEach(c => {
    const show = p === 'all' || c.dataset.p === p;
    c.style.display = show ? 'flex' : 'none';
    if (show) n++;
  });
  document.getElementById('cnt').textContent = n;
}
"""

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Oluseye Jeremiah Oluwapelumi — Writing Portfolio</title>
<link rel="icon" type="image/x-icon" href="favicon.ico">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link href="https://fonts.googleapis.com
<style>{CSS}</style>
</head>
<body>

<header class="hero">
  <div class="hero-inner">
    <div class="tag-row">
      <span class="tag-label">Technical Writing Portfolio</span>
      <span class="tag-dot"></span>
      <span class="tag-label" style="color:var(--muted);font-weight:400;">AI · Data Science · Developer Tooling</span>
    </div>
    <h1 class="name">Oluseye Jeremiah<br><em>Oluwapelumi.</em></h1>
    <p class="bio">
      <strong>BSc Computer Science · MSc Data Science</strong>, University of Ibadan.
      Technical writer published across 8+ platforms — translating complex AI, data science,
      and developer concepts into clear, practical content for technical and business audiences.
      Ex-Microsoft Learn Student Ambassador · Ex-GDSC Core Team Member.
    </p>
    <div class="chips">
      <span class="chip">Artificial Intelligence</span>
      <span class="chip">Machine Learning</span>
      <span class="chip">LLMs &amp; RAG</span>
      <span class="chip">Python &amp; SQL</span>
      <span class="chip">Data Workflows</span>
      <span class="chip">Developer Tooling</span>
      <span class="chip">B2B Tech Content</span>
      <span class="chip">SEO Articles</span>
    </div>
    <div class="stats">
      <div class="st"><span class="st-n">8+</span><span class="st-l">Platforms</span></div>
      <div class="st"><span class="st-n">{total}+</span><span class="st-l">Articles</span></div>
      <div class="st"><span class="st-n">Top</span><span class="st-l">fCC Contributor '23</span></div>
      <div class="st"><span class="st-n">MSc</span><span class="st-l">Data Science</span></div>
    </div>
    <p class="updated">Last updated: <span>{now}</span></p>
  </div>
</header>

<div class="fbar">
  <div class="fi">
    {filter_btns}
    <span class="fcount"><span id="cnt">{total}</span> articles</span>
  </div>
</div>

<div class="main">
  <p class="sh">Selected work</p>
  <div class="grid" id="grid">
    {cards_html}
  </div>

  <div class="see-all-row">
    {see_all_html}
  </div>

  <div class="about">
    <div>
      <p class="al">About</p>
      <h2 class="an">Oluseye Jeremiah Oluwapelumi</h2>
      <p class="at">
        <strong>BSc Computer Science · MSc Data Science</strong>, University of Ibadan, Nigeria.<br><br>
        Technical writer published across DataCamp, freeCodeCamp (Top Contributor 2023),
        Hackmamba, Twilio, Strapi, Medium, Hashnode, and Dev.to — covering AI models,
        machine learning, data engineering, developer tooling, and full-stack tutorials.<br><br>
        Ex-Microsoft Learn Student Ambassador · Ex-GDSC Core Team Member.
        ML educator through Inventors. Researcher working on <strong>MalarAI</strong> —
        mobile deep learning platform for malaria detection.
      </p>
    </div>
    <div>
      <p class="al">Published on</p>
      <div class="plist">
        {plat_html}
      </div>
    </div>
  </div>
</div>

<footer>
  <span>© 2025 Oluseye Jeremiah Oluwapelumi</span>
  <div class="fd"><div class="fdot"></div><span>Open to technical writing opportunities</span></div>
</footer>

<script>{JS}</script>
</body>
</html>"""

out = Path(__file__).parent / "index.html"
out.write_text(HTML, encoding="utf-8")
print(f"✅  Built index.html — {total} articles, {now}")
