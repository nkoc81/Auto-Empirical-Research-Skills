"""Kaynakları CrossRef'te başlık+yazar ile arar; eşleşmeyi başlık benzerliğiyle değerlendirir."""
import json, sys, urllib.request, urllib.parse, difflib, re
def norm(s): return re.sub(r'[^a-z0-9 ]', '', s.lower())
out = []
for line in open(sys.argv[1], encoding='utf-8'):
    if not line.strip() or line.startswith('#'): continue
    yazar, yil, baslik = [x.strip() for x in line.split('|')]
    q = urllib.parse.urlencode({'query.bibliographic': baslik, 'query.author': yazar, 'rows': 15,
                                'select': 'DOI,title,author,issued,container-title,volume,issue,page,type,publisher,abstract'})
    try:
        it = json.load(urllib.request.urlopen(urllib.request.Request('https://api.crossref.org/works?' + q,
              headers={'User-Agent': 'citation-check/1.0'}), timeout=40))['message']['items']
    except Exception as e:
        out.append(dict(girdi=line.strip(), durum='HATA ' + str(e))); continue
    import time; time.sleep(0.3)
    sc = lambda x: difflib.SequenceMatcher(None, norm(baslik), norm((x.get('title') or [''])[0])).ratio()
    pref = lambda x: (round(sc(x), 1), x.get('type') in ('journal-article', 'book', 'monograph', 'book-chapter', 'report'),
                      bool(x.get('container-title')), x.get('issued', {}).get('date-parts', [[0]])[0][0] or 0)
    best = max(it, key=pref) if it else None
    sim = difflib.SequenceMatcher(None, norm(baslik), norm((best.get('title') or [''])[0])).ratio() if best else 0
    out.append(dict(girdi=line.strip(), benzerlik=round(sim, 2), doi=best.get('DOI') if best else None,
        baslik=(best.get('title') or [''])[0] if best else None,
        yazarlar=[(a.get('family'), a.get('given')) for a in best.get('author', [])] if best else None,
        yil=best.get('issued', {}).get('date-parts', [[None]])[0][0] if best else None,
        dergi=(best.get('container-title') or [''])[0] if best else None, cilt=best.get('volume') if best else None,
        sayi=best.get('issue') if best else None, sayfa=best.get('page') if best else None,
        tur=best.get('type') if best else None, yayinci=best.get('publisher') if best else None, ozet=(best.get('abstract') or '')[:1500] if best else None))
json.dump(out, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for o in out: print(o.get('benzerlik'), o.get('yil'), '|', o['girdi'][:70], '=>', (o.get('baslik') or '')[:60], '|', o.get('dergi'), o.get('cilt'), o.get('sayfa'))
