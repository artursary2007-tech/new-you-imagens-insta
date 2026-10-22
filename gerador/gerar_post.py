"""Gera imagens 1080x1350 no visual New You.
Uso: python3 gerar_post.py posts.json pasta_saida
posts.json = lista de objetos:
  {"arquivo": "nome.png", "tema": "light"|"dark", "tag": "CURIOSIDADE",
   "destaque": "texto grande curto (ex: 5–10<i>%</i>)", "titulo": "Título com <em>parte em itálico</em>",
   "texto": "parágrafo curto", "rodape": "Fonte: ..."}
Requer: playwright (python) com Chromium; fonte Lora em /usr/share/fonts/truetype/google-fonts.
"""
import base64, json, os, sys
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__))
b = lambda p: "data:image/png;base64," + base64.b64encode(open(os.path.join(D, p), 'rb').read()).decode()
M, MW = b('logo_mono.png'), b('logo_mono_w.png')
CSS = """@font-face{font-family:Lora;src:url('file:///usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf')}
@font-face{font-family:Lora;font-style:italic;src:url('file:///usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf')}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:Inter,sans-serif;color:#2B1740;
background:radial-gradient(900px 700px at 100% 0%,#EADCF7 0%,transparent 60%),radial-gradient(800px 800px at 0% 100%,#F1E6FA 0%,transparent 60%),#FAF8F4}
body.dark{color:#fff;background:radial-gradient(900px 800px at 90% 10%,#7A44B3 0%,transparent 60%),radial-gradient(900px 900px at 0% 100%,#4A2273 0%,transparent 65%),#2B1740}
.wrap{position:absolute;left:96px;right:96px;top:90px;bottom:180px;display:flex;flex-direction:column;justify-content:center}
.tag{align-self:flex-start;font:600 22px Inter;letter-spacing:.3em;color:#653399;background:rgba(101,51,153,.1);border-radius:999px;padding:14px 26px;margin-bottom:46px}
.dark .tag{color:#E3D2F3;background:rgba(255,255,255,.12)}
.big{font-family:Lora;font-weight:500;font-size:200px;line-height:.95;color:#653399;letter-spacing:-.02em}
.big i{font-size:.55em}.dark .big{color:#C9A8E8}
h1{font-family:Lora;font-weight:500;font-size:68px;line-height:1.1;margin-top:34px}
h1 em{font-style:italic;color:#653399}.dark h1 em{color:#C9A8E8}
p{font:400 33px/1.5 Inter;color:#4A3D5C;margin-top:34px;max-width:840px}.dark p{color:rgba(255,255,255,.82)}
.src{position:absolute;left:96px;bottom:84px;font:italic 400 22px Lora;color:#8A7B9C;max-width:720px}.dark .src{color:rgba(255,255,255,.55)}
.mono{position:absolute;right:80px;bottom:72px;height:74px}"""
posts = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1080, 'height': 1350})
    for p in posts:
        dark = p.get('tema') == 'dark'; big = p.get('destaque', '')
        bigsize = ' style="font-size:150px"' if len(big.replace('<i>', '').replace('</i>', '')) > 6 else ''
        bightml = f"<div class=big{bigsize}>{big}</div>" if big else ''
        html = f"<!doctype html><meta charset=utf-8><style>{CSS}</style><body class='{'dark' if dark else ''}'><div class=wrap><div class=tag>{p.get('tag','NEW YOU')}</div>{bightml}<h1>{p['titulo']}</h1><p>{p['texto']}</p></div><div class=src>{p.get('rodape','')}</div><img class=mono src='{MW if dark else M}'></body>"
        f = os.path.join(out, '_t.html'); open(f, 'w').write(html)
        pg.goto('file://' + os.path.abspath(f)); pg.wait_for_timeout(250)
        pg.screenshot(path=os.path.join(out, p['arquivo'])); os.remove(f); print(p['arquivo'])
    br.close()
