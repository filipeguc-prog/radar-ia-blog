#!/usr/bin/env python3
"""
Radar IA — adiciona um novo post a data/posts.json e reconstroi o site.

Uso:
  python3 scripts/add_post.py \
    --title "Titulo da materia" \
    --category "IA & Modelos" \
    --excerpt "Resumo curto (1-2 frases)" \
    --content-file artigo.html \
    --source-title "Nome da fonte" --source-url "https://..." \
    [--source-title "Outra fonte" --source-url "https://..."] \
    [--date 2026-07-09] [--read-min 6] [--slug meu-slug-customizado]

--content-file deve conter o corpo do artigo em HTML (paragrafos <p>, subtitulos <h2>...).
Fontes podem ser repetidas em pares --source-title/--source-url (na mesma ordem).
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(ROOT, "data", "posts.json")


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--category", required=True)
    ap.add_argument("--excerpt", required=True)
    ap.add_argument("--content-file", required=True, help="arquivo com o HTML do corpo do artigo")
    ap.add_argument("--date", default=date.today().isoformat())
    ap.add_argument("--read-min", type=int, default=5)
    ap.add_argument("--slug", default=None)
    ap.add_argument("--source-title", action="append", default=[])
    ap.add_argument("--source-url", action="append", default=[])
    ap.add_argument("--no-build", action="store_true", help="nao rodar build.py automaticamente")
    args = ap.parse_args()

    with open(args.content_file, encoding="utf-8") as f:
        content_html = f.read().strip()

    slug = args.slug or slugify(args.title)

    if len(args.source_title) != len(args.source_url):
        print("ERRO: numero de --source-title e --source-url deve ser igual.", file=sys.stderr)
        sys.exit(1)
    sources = [{"title": t, "url": u} for t, u in zip(args.source_title, args.source_url)]

    with open(DATA_FILE, encoding="utf-8") as f:
        posts = json.load(f)

    if any(p["slug"] == slug for p in posts):
        print(f"ERRO: ja existe um post com slug '{slug}'. Use --slug para escolher outro.", file=sys.stderr)
        sys.exit(1)

    posts.append({
        "slug": slug,
        "title": args.title,
        "category": args.category,
        "date": args.date,
        "read_min": args.read_min,
        "excerpt": args.excerpt,
        "content_html": content_html,
        "sources": sources,
    })

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    print(f"Post adicionado: {slug}")

    if not args.no_build:
        subprocess.run([sys.executable, os.path.join(ROOT, "build.py")], check=True)


if __name__ == "__main__":
    main()
