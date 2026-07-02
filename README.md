# Radar IA — blog sobre Tecnologia & Inteligência Artificial

Site estático (HTML/CSS/JS puro), gerado por um script Python, pronto para publicar em qualquer
hospedagem estática gratuita (Netlify, Vercel, Cloudflare Pages, GitHub Pages) e para monetizar com
Google AdSense.

## Estrutura

```
radar-ia/
├── data/posts.json      # todos os posts (título, texto, categoria, fontes...)
├── assets/               # CSS e JS do site
├── build.py               # gera o site final a partir de posts.json
├── scripts/add_post.py    # adiciona um novo post e reconstrói o site
├── dist/                  # ⬅️ SITE PRONTO — é essa pasta que vai para a hospedagem
└── README.md
```

## Como visualizar localmente

```
cd radar-ia
python3 -m http.server 8000 --directory dist
# abra http://localhost:8000
```

## Como publicar (Netlify — recomendado)

1. Conecte o conector Netlify no Cowork (botão "Conectar" que foi sugerido no chat).
2. Me diga "publica no Netlify" — eu faço o deploy da pasta `dist/` e te devolvo o link ao vivo.
3. Depois, em Netlify, você pode apontar um domínio próprio (ex: radaria.com.br) nas configurações do site.

Alternativas: GitHub Pages, Vercel, Cloudflare Pages, ou o servidor onde está seu blog atual — basta
subir o conteúdo da pasta `dist/`.

## Antes de ativar o AdSense

Edite estas constantes no topo de `build.py` com os dados reais da sua conta AdSense (depois de aprovada):

```python
SITE_URL = "https://seu-dominio-real.com"
ADSENSE_PUBLISHER_ID = "ca-pub-XXXXXXXXXXXXXXXX"   # seu Publisher ID real
ADSENSE_SLOT_INARTICLE = "XXXXXXXXXX"                # ID do bloco de anúncio criado no AdSense
```

Depois rode `python3 build.py` de novo para regravar o `dist/` com os IDs corretos, e publique.
O arquivo `dist/ads.txt` e os blocos `<ins class="adsbygoogle">` já são gerados automaticamente
a partir dessas constantes — você não precisa editar HTML na mão.

Já existe no site, prontas para a revisão do AdSense:
- Página de **Política de Privacidade e Cookies** (`/privacidade.html`) — obrigatória para o Google aprovar anúncios.
- Página **Sobre** e **Contato**.
- `robots.txt` e `sitemap.xml` para facilitar a indexação no Google.

## Como adicionar um post manualmente

```
python3 scripts/add_post.py \
  --title "Título da matéria" \
  --category "IA & Modelos" \
  --excerpt "Resumo de 1-2 frases" \
  --content-file caminho/para/texto.html \
  --source-title "Nome da fonte" --source-url "https://..."
```

O script já roda `build.py` no final.

## Automação semanal

Uma tarefa agendada (`radar-ia-post-semanal`) roda toda semana e:
1. Pesquisa as principais notícias de IA/tecnologia da semana.
2. Escreve um artigo original (600-900 palavras) com fontes citadas.
3. Roda `scripts/add_post.py` para publicar o post e reconstruir o site.
4. Reimplanta o site (Netlify) automaticamente.

Você pode editar o horário/dia ou pausar essa tarefa a qualquer momento pedindo no chat.
