"""DOI listesinden CrossRef meta verisiyle APA 7 kaynakça girdisi üretir."""
import json, urllib.request, urllib.parse, time, html, re
def get(doi):
    u = 'https://api.crossref.org/works/' + urllib.parse.quote(doi)
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'citation-check/1.0'}), timeout=40))['message']
def ad(a):
    g = a.get('given', '') or ''
    ini = ' '.join(p[0] + '.' for p in re.split(r'[\s]+', g.replace('-', ' -')) if p and p[0].isalpha() or p.startswith('-'))
    ini = ' '.join((w[0] + '.') if not w.startswith('-') else ('-' + w[1] + '.') for w in g.replace('-', ' -').split() if w.strip('-'))
    ini = ini.replace(' -', '-')
    return f"{a.get('family','')}, {ini}".strip(', ') if a.get('family') else a.get('name', '')
def yazarlar(L):
    s = [ad(a) for a in L]
    if len(s) == 1: return s[0]
    if len(s) <= 20: return ', '.join(s[:-1]) + ', & ' + s[-1]
    return ', '.join(s[:19]) + ', . . . ' + s[-1]
rows = []
for doi in [l.strip() for l in open('secilen_doi.txt') if l.strip()]:
    m = get(doi); time.sleep(0.2)
    yil = (m.get('journal-issue', {}).get('published-print') or m.get('published-print') or m.get('issued'))['date-parts'][0][0]
    t = html.unescape(re.sub('<[^>]+>', '', m['title'][0]))
    rows.append(dict(doi=doi.lower(), yil=yil, ilk=m.get('author', [{}])[0].get('family', ''), n=len(m.get('author', [])),
        soyadlar=[a.get('family') for a in m.get('author', [])], yazar=yazarlar(m.get('author', [])), baslik=t,
        dergi=(m.get('container-title') or [''])[0], cilt=m.get('volume'), sayi=m.get('issue'), sayfa=m.get('page'),
        madde=m.get('article-number'), tur=m.get('type'), yayinci=m.get('publisher')))
json.dump(rows, open('kaynak_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for r in rows: print(r['yil'], r['tur'], '|', r['yazar'][:70], '|', r['baslik'][:60], '|', r['dergi'][:40], r['cilt'], r['sayi'], r['sayfa'], r['madde'])
