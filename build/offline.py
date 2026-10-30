# Build a single self-contained offline HTML (fonts, images, css, js all embedded).
import re, base64, os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = sys.argv[1]  # @fontsource node_modules dir
OUT = sys.argv[2]
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
html = open(os.path.join(R, 'index.html'), encoding='utf-8').read()
TH = 'U+0E01-0E5B,U+200C-200D,U+25CC'
LA = 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD'
fams = [('Noto Sans Thai', 'noto-sans-thai', (400, 500, 600, 700)), ('Prompt', 'prompt', (400, 500, 600, 700)),
        ('Itim', 'itim', (400,)), ('Sarabun', 'sarabun', (400, 600, 700, 800))]
css = ''
for fam, pkg, ws in fams:
    for w in ws:
        for sub, rng in (('thai', TH), ('latin', LA)):
            p = os.path.join(F, pkg, 'files', '%s-%s-%d-normal.woff2' % (pkg, sub, w))
            if not os.path.exists(p):
                print('missing', p); continue
            css += "@font-face{font-family:'%s';font-style:normal;font-weight:%d;font-display:block;src:url(data:font/woff2;base64,%s) format('woff2');unicode-range:%s}\n" % (fam, w, b64(p), rng)
html = re.sub(r'<link rel="preconnect"[^>]*>\s*', '', html)
html = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>', '<style>' + css + '</style>', html)
def inline_css(m):
    c = open(os.path.join(R, m.group(1)), encoding='utf-8').read()
    return '<style>' + c + '</style>'
html = re.sub(r'<link rel="stylesheet" href="(assets/[^"?]+)(?:\?[^"]*)?">', inline_css, html)
def inline_js(m):
    c = open(os.path.join(R, m.group(1)), encoding='utf-8').read().replace('</script', '<\\/script')
    return '<script>' + c + '</script>'
html = re.sub(r'<script src="([^"?]+)(?:\?[^"]*)?"></script>', inline_js, html)
cache = {}
def img(m):
    p = m.group(0)
    if p not in cache:
        ext = p.rsplit('.', 1)[1].lower()
        cache[p] = 'data:image/%s;base64,%s' % ('jpeg' if ext in ('jpg', 'jpeg') else ext, b64(os.path.join(R, p)))
    return cache[p]
html = re.sub(r'images/[A-Za-z0-9_.-]+\.(?:jpg|jpeg|png|svg)', img, html)
html = re.sub(r'<div class="dlrow pop".*?</a></div>', '', html, flags=re.S)
open(OUT, 'w', encoding='utf-8').write(html)
left = re.findall(r'(?:src|href)="(?!data:|#|https?:|mailto:)[^"]+"', html)
print('size MB', round(os.path.getsize(OUT) / 1e6, 1), 'external refs left:', left[:5], 'remote:', re.findall(r'https://fonts[^"\')]+', html)[:3])
