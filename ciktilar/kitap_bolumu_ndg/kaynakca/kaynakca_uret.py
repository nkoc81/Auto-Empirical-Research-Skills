"""CrossRef meta verisinden ve elle doğrulanmış resmî kaynaklardan APA 7 kaynakça üretir."""
import json, re, time, html, urllib.request, urllib.parse, unicodedata
DOI = ['10.3982/ECTA17945?', ]
def get(doi):
    u = 'https://api.crossref.org/works/' + urllib.parse.quote(doi)
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'citation-check/1.0'}), timeout=40))['message']
dog = {x['girdi'].split('|')[0]: x for x in json.load(open('dogrulama.json', encoding='utf-8'))}
SEC = ['Egger', 'Jones Marinescu', 'Verho', 'Filmer', 'Daruich', 'Almeida', 'Fagereng', 'Baker', 'Boehm', 'Fuster',
       'di Giovanni', 'Guerrieri', 'Baum-Snow', 'Eerola', 'Cunha', 'Gibbons', 'Kueng', 'Parker Souleles', 'Jappelli',
       'Moffitt', 'Hoynes', 'Vivalt', 'Orchard', 'Golosov']
dois = []
for k in SEC:
    m = [v for kk, v in dog.items() if kk.startswith(k)]
    assert m and m[0].get('doi'), k
    dois.append(m[0]['doi'])
dois += ['10.1257/mac.20230195', '10.1162/qjec.2010.125.3.1253', '10.1146/annurev-economics-080217-053444', '10.1353/eca.2022.a901276']
OZEL = {'Kenya', 'Kenya:', 'US', 'U.S.', 'COVID-19', 'COVID-19:', 'UK', 'MPC', 'MPCs', 'MPCs:', 'Norway', 'Alaska', 'Permanent', 'Fund', 'Fund:',
        'Finnish', 'Europe', 'European', 'Union', 'States', 'States:', 'United', 'Americans', 'Two',
        'U.S.?'}
def cumle(t):
    t = html.unescape(re.sub('<[^>]+>', '', t)).replace('*', '').strip()
    ws, out, bas = t.split(), [], True
    for w in ws:
        cl = w.strip('“”"‘’(),:;?$')
        if bas: out.append(w[0].upper() + w[1:])
        elif (cl.isupper() and len(cl) > 1) or any(c.isdigit() for c in cl) or w in OZEL or cl in OZEL: out.append(w)
        else: out.append(w.lower())
        bas = w.endswith(':') or w.endswith('?')
    s = ' '.join(out)
    s = s.replace('Universal Basic', 'Universal basic')
    return s
def ini(g):
    parts = [p for p in re.split(r'\s+', g or '') if p]
    out = []
    for p in parts:
        out.append('-'.join(q[0] + '.' for q in p.split('-') if q))
    return ' '.join(out)
def yazar(L):
    s = [f"{a['family']}, {ini(a.get('given'))}".strip(', ') for a in L]
    return s[0] if len(s) == 1 else ', '.join(s[:-1]) + ', & ' + s[-1]
refs = []
for d in dois:
    m = get(d); time.sleep(0.2)
    yil = (m.get('journal-issue', {}).get('published-print') or m.get('published-print') or m['issued'])['date-parts'][0][0]
    A = m['author']
    loc = f"*{html.unescape(m['container-title'][0])}*, *{m['volume']}*" + (f"({m['issue']})" if m.get('issue') else '')
    loc += f", {m['page'].replace('-', '–')}" if m.get('page') else ''
    refs.append(dict(soy=[a['family'] for a in A], yil=yil, metin=f"{yazar(A)} ({yil}). {cumle(m['title'][0])}{'' if cumle(m['title'][0]).endswith('?') else '.'} {loc}. https://doi.org/{d.lower()}"))
# düzeltmeler (basılı sayı yılları)
YIL = {'Fuster': 2021, 'Eerola': 2021, 'Cunha': 2019, 'Golosov': 2024, 'Kueng': 2018}
for r in refs:
    if r['soy'][0] in YIL and r['yil'] != YIL[r['soy'][0]]:
        r['metin'] = r['metin'].replace(f"({r['yil']})", f"({YIL[r['soy'][0]]})", 1); r['yil'] = YIL[r['soy'][0]]
for r in refs:
    r['metin'] = r['metin'].replace('R. Baker, S.,', 'Baker, S. R.,').replace('(4-5)', '(4–5)')
    if r['soy'][0] == 'R. Baker': r['soy'][0] = 'Baker'
for r in refs:  # Brookings künyesi
    r['metin'] = r['metin'].replace('*Brookings Papers on Economic Activity*, *2022*(2)', '*Brookings Papers on Economic Activity*, *2022*(2)')
EL = [
 (['Bartik', 'Rhodes', 'Broockman', 'Krause', 'Miller', 'Vivalt'], 2024, "Bartik, A. W., Rhodes, E., Broockman, D. E., Krause, P. K., Miller, S., & Vivalt, E. (2024). *The impact of unconditional cash transfers on consumption and household balance sheets: Experimental evidence from two US states* (NBER Working Paper No. 32784). National Bureau of Economic Research. https://doi.org/10.3386/w32784"),
 (['Coady', 'Jahan', 'Shang', 'Matsumoto'], 2021, "Coady, D., Jahan, S., Shang, B., & Matsumoto, R. (2021). *Guaranteed minimum income schemes in Europe: Landscape and design* (IMF Working Paper No. 2021/179). International Monetary Fund. https://doi.org/10.5089/9781513584379.001"),
 (['Ferrante', 'Graves', 'Iacoviello'], 2023, "Ferrante, F., Graves, S., & Iacoviello, M. (2023). *The inflationary effects of sectoral reallocation* (International Finance Discussion Papers No. 1369). Board of Governors of the Federal Reserve System. https://doi.org/10.17016/ifdp.2023.1369"),
 (['Ko', 'Moffitt'], 2024, "Ko, W., & Moffitt, R. A. (2024). Take-up of social benefits. In K. F. Zimmermann (Ed.), *Handbook of labor, human resources and population economics* (pp. 1–42). Springer. KO_DOI"),
 (['Van Parijs', 'Vanderborght'], 2017, "Van Parijs, P., & Vanderborght, Y. (2017). *Basic income: A radical proposal for a free society and a sane economy*. Harvard University Press."),
 (['Council of the European Union'], 2023, "Council of the European Union. (2023). Council Recommendation of 30 January 2023 on adequate minimum income ensuring active inclusion (2023/C 41/01). *Official Journal of the European Union*, *C 41*, 1–12. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=uriserv:OJ.C_.2023.041.01.0001.01.ENG"),
 (['Socialstyrelsen'], 'n.d.', "Socialstyrelsen. (n.d.). *Ekonomiskt bistånd – för privatpersoner*. Retrieved November 18, 2026, from https://www.socialstyrelsen.se/kunskapsstod-och-regler/omraden/ekonomiskt-bistand/ekonomiskt-bistand-for-privatpersoner/"),
 (['Socialstyrelsen'], 2025, "Socialstyrelsen. (2025). *Riksnormen för försörjningsstöd 2025*. https://socialstyrelsen.se/globalassets/sharepoint-dokument/dokument-webb/ovrigt/riksnormen-for-forsorjningsstod-2025.pdf"),
 (['Borger.dk'], 'n.d.', "Borger.dk. (n.d.). *Kontanthjælp*. Retrieved November 18, 2026, from https://www.borger.dk/arbejde-dagpenge-ferie/Dagpenge-kontanthjaelp-og-sygedagpenge/Kontanthjaelp/kontanthjaelp"),
 (['Københavns Kommune'], 'n.d.', "Københavns Kommune. (n.d.). *Typiske spørgsmål om kontanthjælp*. Retrieved November 18, 2026, from https://www.kk.dk/borger/jobsoegning-og-ledighed/kontanthjaelp-og-anden-oekonomisk-hjaelp/typiske-spoergsmaal-om-kontanthjaelp"),
 (['Ministry of Social Affairs and Health'], 2020, "Ministry of Social Affairs and Health. (2020, May 6). *Results of Finland’s basic income experiment: Small employment effects, better perceived economic security and mental wellbeing* [Press release]. https://stm.fi/en/-/perustulokokeilun-tulokset-tyollisyysvaikutukset-vahaisia-toimeentulo-ja-psyykkinen-terveys-koettiin-paremmaksi"),
]
ko = [v for kk, v in dog.items() if kk.startswith('Ko Moffitt')][0]['doi']
for s, y, t in EL: refs.append(dict(soy=s, yil=y, metin=t.replace('KO_DOI', 'https://doi.org/' + ko.lower())))
def anahtar(r):
    s = r['soy']
    return f"{s[0]}, {r['yil']}" if len(s) == 1 else (f"{s[0]} ve {s[1]}, {r['yil']}" if len(s) == 2 else f"{s[0]} vd., {r['yil']}")
refs.sort(key=lambda r: unicodedata.normalize('NFKD', r['metin']).encode('ascii', 'ignore').decode().lower().replace('van parijs', 'parijs'))
json.dump([dict(anahtar=anahtar(r), yil=r['yil'], metin=r['metin']) for r in refs], open('kaynakca.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
n = len(refs); y21 = sum(1 for r in refs if isinstance(r['yil'], int) and r['yil'] >= 2021)
print(n, 'kaynak;', y21, '2021+'); [print(anahtar(r), '||', r['metin'][:150]) for r in refs]
