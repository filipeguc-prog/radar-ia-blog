#!/usr/bin/env python3
"""
Radar IA — static site generator.

Reads data/posts.json and regenerates the whole site into dist/.
Run: python3 build.py

This script is intentionally dependency-free (stdlib only) so it keeps
working unattended inside the weekly automation task, without needing
`pip install` first.
"""
import json
import os
import re
import shutil
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(ROOT, "data", "posts.json")
DIST = os.path.join(ROOT, "dist")
ASSETS_SRC = os.path.join(ROOT, "assets")

SITE_NAME = "Radar IA"
SITE_TAGLINE = "Tecnologia e Inteligência Artificial, direto ao ponto"
SITE_DESCRIPTION = (
    "Radar IA cobre, toda semana, as noticias e analises mais relevantes de "
    "inteligencia artificial e tecnologia: lancamentos de modelos, hardware, "
    "governanca e o que isso muda na pratica."
)
# EDIT ME again if you move to a custom domain later:
SITE_URL = "https://dancing-sundae-71c0ca.netlify.app"
# EDIT ME once your AdSense account is approved:
ADSENSE_PUBLISHER_ID = "ca-pub-0000000000000000"  # placeholder — replace with your real pub id
ADSENSE_SLOT_HEADER = "0000000000"  # placeholder ad slot ids
ADSENSE_SLOT_INARTICLE = "0000000000"

MONTHS_PT = ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"]


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def fmt_date(iso):
    d = datetime.strptime(iso, "%Y-%m-%d")
    return f"{d.day} de {MONTHS_PT[d.month-1]} de {d.year}"


def load_posts():
    with open(DATA_FILE, encoding="utf-8") as f:
        posts = json.load(f)
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


ADSENSE_HEAD_SNIPPET = f"""
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUBLISHER_ID}" crossorigin="anonymous"></script>
"""

ADSENSE_UNIT_SNIPPET = f"""
  <ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE_PUBLISHER_ID}" data-ad-slot="{ADSENSE_SLOT_INARTICLE}" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
"""


def base_head(title, description, path=""):
    canonical = f"{SITE_URL}{path}"
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/style.css">
<link rel="icon" href="data:,">
{ADSENSE_HEAD_SNIPPET}
</head>
"""


def header_html():
    return f"""
<header class="site">
  <div class="bar">
    <a href="/" class="logo"><span class="dot"></span>{SITE_NAME}</a>
    <nav class="main">
      <a href="/">Início</a>
      <a href="/#ultimas">Últimas</a>
      <a href="/sobre.html">Sobre</a>
      <a href="/contato.html">Contato</a>
    </nav>
    <button class="nav-toggle" aria-label="Menu">☰</button>
  </div>
</header>
"""


def footer_html():
    year = datetime.now().year
    return f"""
<footer>
  <div class="wrap">
    <div class="cols">
      <div>
        <div class="logo" style="margin-bottom:10px"><span class="dot"></span>{SITE_NAME}</div>
        <p style="max-width:340px">{SITE_DESCRIPTION}</p>
      </div>
      <div class="links">
        <a href="/sobre.html">Sobre</a>
        <a href="/privacidade.html">Privacidade &amp; Cookies</a>
        <a href="/contato.html">Contato</a>
      </div>
    </div>
    <p style="margin-top:32px">© {year} {SITE_NAME}. Todos os direitos reservados.</p>
  </div>
</footer>
<script src="/assets/script.js"></script>
"""


def card_html(post, featured=False):
    cls = "card featured" if featured else "card"
    return f"""
<a class="{cls}" href="/posts/{post['slug']}.html">
  <div class="thumb"></div>
  <span class="tag">{post['category']}</span>
  <h3>{post['title']}</h3>
  <p class="excerpt">{post['excerpt']}</p>
  <div class="meta"><span>{fmt_date(post['date'])}</span><span class="sep">•</span><span>{post['read_min']} min de leitura</span></div>
</a>
"""


def render_index(posts):
    featured = posts[0]
    rest = posts[1:]
    cards = "\n".join(card_html(p) for p in rest)
    html = base_head(
        f"{SITE_NAME} — {SITE_TAGLINE}",
        SITE_DESCRIPTION,
        "/",
    )
    html += f"""
<body>
<div class="glow"></div>
{header_html()}
<main class="wrap">
  <section class="hero">
    <span class="eyebrow">Atualizado semanalmente</span>
    <h1>O seu <span class="grad">radar</span> sobre Inteligência Artificial e tecnologia</h1>
    <p class="sub">{SITE_TAGLINE}. Curadoria e análise das notícias que realmente importam, sem enrolação.</p>
  </section>

  <div class="ad-slot">Espaço de anúncio (topo) — configure seu Ad Slot ID em build.py</div>

  <section id="ultimas">
    <div class="section-title"><h2>Destaque da semana</h2></div>
    <div class="grid featured">
      {card_html(featured, featured=True)}
      <div style="display:flex;flex-direction:column;gap:22px">
        {"".join(card_html(p) for p in rest[:2])}
      </div>
    </div>

    <div class="section-title"><h2>Últimas notícias</h2></div>
    <div class="grid">
      {"".join(card_html(p) for p in rest[2:])}
    </div>
  </section>
</main>
{footer_html()}
</body>
</html>"""
    return html


def render_post(post):
    html = base_head(
        f"{post['title']} — {SITE_NAME}",
        post["excerpt"],
        f"/posts/{post['slug']}.html",
    )
    sources_html = ""
    if post.get("sources"):
        items = "\n".join(
            f'<li><a href="{s["url"]}" target="_blank" rel="noopener nofollow">{s["title"]}</a></li>'
            for s in post["sources"]
        )
        sources_html = f"""
<div class="sources">
  <h4>Fontes</h4>
  <ul>{items}</ul>
</div>"""
    html += f"""
<body>
<div class="glow"></div>
<div class="reading-progress"></div>
{header_html()}
<main class="wrap">
  <div class="post-head">
    <span class="tag">{post['category']}</span>
    <h1>{post['title']}</h1>
    <div class="meta"><span>{fmt_date(post['date'])}</span><span class="sep">•</span><span>{post['read_min']} min de leitura</span></div>
  </div>
  <article class="content">
    {post['content_html']}
  </article>
  <div class="wrap" style="max-width:760px;margin:0 auto">
    <div class="ad-slot">{ADSENSE_UNIT_SNIPPET}</div>
  </div>
  {sources_html}
</main>
{footer_html()}
</body>
</html>"""
    return html


def render_simple_page(title, body_html, path):
    html = base_head(f"{title} — {SITE_NAME}", SITE_DESCRIPTION, path)
    html += f"""
<body>
<div class="glow"></div>
{header_html()}
<main class="wrap">
  <div class="page">
    <h1>{title}</h1>
    {body_html}
  </div>
</main>
{footer_html()}
</body>
</html>"""
    return html


def render_about():
    body = f"""
<p>O <strong>{SITE_NAME}</strong> é um blog independente dedicado a cobrir, de forma clara e sem jargão desnecessário,
o que está acontecendo no mundo da Inteligência Artificial e da tecnologia — de lançamentos de modelos e hardware
a decisões de governança que afetam o dia a dia de quem usa (ou vai usar) essas ferramentas.</p>
<h2>Como trabalhamos</h2>
<p>Toda semana selecionamos os desenvolvimentos mais relevantes do período, verificamos as fontes originais e
publicamos um resumo autoral, com links diretos para as fontes usadas em cada matéria.</p>
<h2>Contato</h2>
<p>Sugestões de pauta ou correções podem ser enviadas pela nossa <a href="/contato.html">página de contato</a>.</p>
"""
    return render_simple_page("Sobre o Radar IA", body, "/sobre.html")


def render_privacy():
    body = f"""
<p>Esta Política de Privacidade explica como o {SITE_NAME} trata dados ao longo da navegação no site.</p>
<h2>Cookies e publicidade</h2>
<p>Este site utiliza o Google AdSense para exibir anúncios. O Google e seus parceiros podem usar cookies
para exibir anúncios com base em visitas anteriores do usuário a este ou a outros sites. O uso de cookies de
publicidade permite ao Google e a seus parceiros veicular anúncios para os usuários com base na visita a este
site e/ou a outros sites na Internet.</p>
<p>Os usuários podem desativar a publicidade personalizada acessando as
<a href="https://adssettings.google.com/" target="_blank" rel="noopener">Configurações de anúncios do Google</a>.
Alternativamente, os usuários podem desativar o uso de cookies de terceiros para publicidade personalizada
acessando <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">www.aboutads.info</a>.</p>
<h2>Dados coletados</h2>
<p>Podemos coletar dados de navegação básicos (como páginas visitadas e tempo de permanência) por meio de
ferramentas de analytics, com o único objetivo de entender quais conteúdos são mais úteis aos leitores.</p>
<h2>Contato</h2>
<p>Dúvidas sobre esta política podem ser enviadas pela nossa <a href="/contato.html">página de contato</a>.</p>
<p style="color:var(--text-dim);font-size:13px;margin-top:32px">Última atualização: {fmt_date(datetime.now().strftime('%Y-%m-%d'))}.</p>
"""
    return render_simple_page("Política de Privacidade & Cookies", body, "/privacidade.html")


def render_contact():
    body = f"""
<p>Quer sugerir uma pauta, relatar um erro ou propor uma parceria? Escreva para:</p>
<p style="font-size:20px;font-weight:700">contato@{SITE_URL.replace('https://','').replace('http://','')}</p>
<p style="color:var(--text-dim);font-size:13px">(Endereço de e-mail ilustrativo — troque pelo seu e-mail real antes de publicar.)</p>
"""
    return render_simple_page("Contato", body, "/contato.html")


def render_ads_txt():
    return f"google.com, {ADSENSE_PUBLISHER_ID}, DIRECT, f08c47fec0942fa0\n"


def render_robots():
    return f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n"


def render_sitemap(posts):
    urls = ["", "/sobre.html", "/privacidade.html", "/contato.html"] + [f"/posts/{p['slug']}.html" for p in posts]
    items = "\n".join(f"  <url><loc>{SITE_URL}{u}</loc></url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>\n'


def build():
    posts = load_posts()

    os.makedirs(DIST, exist_ok=True)
    os.makedirs(os.path.join(DIST, "posts"), exist_ok=True)
    shutil.copytree(ASSETS_SRC, os.path.join(DIST, "assets"), dirs_exist_ok=True)

    with open(os.path.join(DIST, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_index(posts))

    for p in posts:
        with open(os.path.join(DIST, "posts", f"{p['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(render_post(p))

    with open(os.path.join(DIST, "sobre.html"), "w", encoding="utf-8") as f:
        f.write(render_about())
    with open(os.path.join(DIST, "privacidade.html"), "w", encoding="utf-8") as f:
        f.write(render_privacy())
    with open(os.path.join(DIST, "contato.html"), "w", encoding="utf-8") as f:
        f.write(render_contact())
    with open(os.path.join(DIST, "ads.txt"), "w", encoding="utf-8") as f:
        f.write(render_ads_txt())
    with open(os.path.join(DIST, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(render_robots())
    with open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(render_sitemap(posts))

    print(f"Build OK — {len(posts)} posts -> {DIST}")


if __name__ == "__main__":
    build()
