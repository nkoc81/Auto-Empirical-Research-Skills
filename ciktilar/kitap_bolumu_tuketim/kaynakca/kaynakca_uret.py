import json, re, time, html, urllib.request, urllib.parse, unicodedata, sys
sys.path.insert(0, '../../kitap_bolumu_ndg/kaynakca')
def get(doi):
    u = 'https://api.crossref.org/works/' + urllib.parse.quote(doi)
    for _ in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'citation-check/1.0'}), timeout=40))['message']
        except Exception: time.sleep(5)
    raise RuntimeError(doi)
DOIS = ['10.1093/qje/qjw025', '10.2307/146179', '10.1093/ej/ueaa056', '10.1086/528721', '10.1257/aer.20181735', '10.1257/000282803321455377',
 '10.1257/000282803321455386', '10.1111/j.1468-0297.2006.01106.x', '10.1016/j.jpubeco.2004.05.003', '10.1257/pol.2.2.142', '10.17310/ntj.2000.4s1.08',
 '10.1257/pandp.20231088', '10.1257/jel.20151233', '10.1086/423252', '10.1086/689575', '10.1257/aer.p20171147', '10.1257/pol.1.2.163',
 '10.1257/mac.6.4.107', '10.1257/mac.6.4.84', '10.1353/cpp.2011.0036',
 # önceki bölümlerde doğrulanmış
 '10.1257/aer.103.6.2530', '10.1093/rof/rfad010', '10.1093/qje/qjy014', '10.1257/mac.20190211', '10.1257/aer.20240138',
 '10.1146/annurev-economics-080217-053444', '10.1146/annurev.economics.050708.142933', '10.1093/qje/qjad053', '10.1257/089533003769204380',
 '10.1146/annurev-economics-080218-030237', '10.1257/pol.20200143', '10.1111/roiw.12728', '10.1093/qje/qjag042']
OZEL = {'Kenya', 'Kenya:', 'US', 'U.S.', 'COVID-19', 'UK', 'MPC', 'MPCs', 'MPCs:', 'Alaska', 'Permanent', 'Fund', 'Fund:', 'Finnish', 'European',
        'Union', 'States', 'States:', 'United', 'Kingdom', 'Americans', 'PROGRESA', 'Progresa/Oportunidades', 'Canadian', 'Social', 'Security',
        '“3rd'}
KEEP_LOWER_AFTER = True
def cumle(t):
    t = html.unescape(re.sub('<[^>]+>', '', t)).replace('*', '').strip()
    ws, out, bas = t.split(), [], True
    for w in ws:
        cl = w.strip('“”"‘’(),:;?$')
        if bas: out.append(w[0].upper() + w[1:] if w[0] not in '“"' else w[0] + w[1].upper() + w[2:])
        elif (cl.isupper() and len(cl) > 1) or any(c.isdigit() for c in cl) or w in OZEL or cl in OZEL: out.append(w)
        else: out.append(w.lower())
        bas = w.endswith(':') or w.endswith('?')
    s = ' '.join(out)
    for a, b in [('the Earned Income Tax Credit', 'the earned income credit'), ('Social Security Recipients', 'Social Security recipients'),
                 ('Monthly and Lump-Sum Child Tax Credit', 'monthly and lump-sum Child Tax Credit'), ('Universal Basic', 'Universal basic'),
                 ('Basic Income Experiment', 'basic income experiment'), ('the earned Income credit', 'the earned income credit'),
                 ('Guaranteed Annual Income', 'guaranteed annual income'), ('a guaranteed Income', 'a guaranteed income'),
                 ('Income changes', 'income changes'), ('unearned Income', 'unearned income'), ('negative Income Tax', 'negative income tax'),
                 ('Social Security', 'Social Security'), ('Two U.S. States', 'two U.S. states'), ('From Two U.S. States', 'from two U.S. states')]:
        s = s.replace(a, b)
    return s
def ini(g): return ' '.join('-'.join(q[0] + '.' for q in p.split('-') if q) for p in (g or '').split())
def yazar(L):
    s = [f"{a['family']}, {ini(a.get('given'))}".strip(', ') for a in L]
    return s[0] if len(s) == 1 else ', '.join(s[:-1]) + ', & ' + s[-1]
refs = []
for d in DOIS:
    m = get(d); time.sleep(0.4)
    yil = (m.get('journal-issue', {}).get('published-print') or m.get('published-print') or m['issued'])['date-parts'][0][0]
    A = m['author']
    for a in A:
        if a.get('family') == 'R. Baker': a['family'], a['given'] = 'Baker', 'S. R.'
        if a.get('family', '').isupper(): a['family'] = a['family'].capitalize()
    t = cumle(m['title'][0])
    loc = f"*{html.unescape(m['container-title'][0])}*, *{m['volume']}*" + (f"({m['issue']})" if m.get('issue') else '')
    if m.get('page'): loc += f", {m['page'].replace('-', '–')}"
    elif m.get('article-number'): loc += f", Article {m['article-number']}"
    refs.append(dict(soy=[a['family'] for a in A], yil=yil, metin=f"{yazar(A)} ({yil}). {t}{'' if t.endswith('?') else '.'} {loc}. https://doi.org/{d.lower()}"))
YIL = {'Fuster': 2021, 'Kueng': 2018, 'Golosov': 2024, 'Agarwal': 2007}
for r in refs:
    if r['soy'][0] in YIL and r['yil'] != YIL[r['soy'][0]]:
        r['metin'] = r['metin'].replace(f"({r['yil']})", f"({YIL[r['soy'][0]]})", 1); r['yil'] = YIL[r['soy'][0]]
    for a, b in [('the earned income credit', 'the Earned Income Credit'), ('lump-sum child tax credit', 'lump-sum Child Tax Credit'),
                 ('United Kingdom child benefit', 'United Kingdom Child Benefit'), ('*53*(4.2)', '*53*(4)'), ('(2-3)', '(2–3)')]:
        r['metin'] = r['metin'].replace(a, b)
    r['metin'] = r['metin'].replace('Kueng, L. (2018)', 'Kueng, L. (2018)')
EL = [
 (['Bartik', 'Rhodes', 'Broockman', 'Krause', 'Miller', 'Vivalt'], 2024, "Bartik, A. W., Rhodes, E., Broockman, D. E., Krause, P. K., Miller, S., & Vivalt, E. (2024). *The impact of unconditional cash transfers on consumption and household balance sheets: Experimental evidence from two US states* (NBER Working Paper No. 32784). National Bureau of Economic Research. https://doi.org/10.3386/w32784"),
 (['Coibion', 'Gorodnichenko', 'Weber'], 2020, "Coibion, O., Gorodnichenko, Y., & Weber, M. (2020). *How did U.S. consumers use their stimulus payments?* (NBER Working Paper No. 27693). National Bureau of Economic Research. https://doi.org/10.3386/w27693"),
 (['Nichols', 'Rothstein'], 2015, "Nichols, A., & Rothstein, J. (2015). *The earned income tax credit (EITC)* (NBER Working Paper No. 21211). National Bureau of Economic Research. https://doi.org/10.3386/w21211"),
 (['Coady', 'Jahan', 'Shang', 'Matsumoto'], 2021, "Coady, D., Jahan, S., Shang, B., & Matsumoto, R. (2021). *Guaranteed minimum income schemes in Europe: Landscape and design* (IMF Working Paper No. 2021/179). International Monetary Fund. https://doi.org/10.5089/9781513584379.001"),
 (['Ko', 'Moffitt'], 2024, "Ko, W., & Moffitt, R. A. (2024). Take-up of social benefits. In K. F. Zimmermann (Ed.), *Handbook of labor, human resources and population economics* (pp. 1–42). Springer. https://doi.org/10.1007/978-3-319-57365-6_372-3"),
 (['Van Parijs', 'Vanderborght'], 2017, "Van Parijs, P., & Vanderborght, Y. (2017). *Basic income: A radical proposal for a free society and a sane economy*. Harvard University Press."),
 (['Council of the European Union'], 2023, "Council of the European Union. (2023). Council Recommendation of 30 January 2023 on adequate minimum income ensuring active inclusion (2023/C 41/01). *Official Journal of the European Union*, *C 41*, 1–12. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=uriserv:OJ.C_.2023.041.01.0001.01.ENG"),
 (['Socialstyrelsen'], 'n.d.', "Socialstyrelsen. (n.d.). *Ekonomiskt bistånd – för privatpersoner*. Retrieved November 19, 2026, from https://www.socialstyrelsen.se/kunskapsstod-och-regler/omraden/ekonomiskt-bistand/ekonomiskt-bistand-for-privatpersoner/"),
 (['Socialstyrelsen'], 2025, "Socialstyrelsen. (2025). *Riksnormen för försörjningsstöd 2025*. https://socialstyrelsen.se/globalassets/sharepoint-dokument/dokument-webb/ovrigt/riksnormen-for-forsorjningsstod-2025.pdf"),
 (['Borger.dk'], 'n.d.', "Borger.dk. (n.d.). *Kontanthjælp*. Retrieved November 19, 2026, from https://www.borger.dk/arbejde-dagpenge-ferie/Dagpenge-kontanthjaelp-og-sygedagpenge/Kontanthjaelp/kontanthjaelp"),
 (['Københavns Kommune'], 'n.d.', "Københavns Kommune. (n.d.). *Typiske spørgsmål om kontanthjælp*. Retrieved November 19, 2026, from https://www.kk.dk/borger/jobsoegning-og-ledighed/kontanthjaelp-og-anden-oekonomisk-hjaelp/typiske-spoergsmaal-om-kontanthjaelp"),
 (['Ministry of Social Affairs and Health'], 2020, "Ministry of Social Affairs and Health. (2020, May 6). *Results of Finland’s basic income experiment: Small employment effects, better perceived economic security and mental wellbeing* [Press release]. https://stm.fi/en/-/perustulokokeilun-tulokset-tyollisyysvaikutukset-vahaisia-toimeentulo-ja-psyykkinen-terveys-koettiin-paremmaksi"),
 (['GOV.UK'], 'n.d.-a', "GOV.UK. (n.d.-a). *Universal Credit: How you’re paid*. Retrieved November 19, 2026, from https://www.gov.uk/universal-credit/how-youre-paid"),
 (['GOV.UK'], 'n.d.-b', "GOV.UK. (n.d.-b). *Universal Credit: Further information for couples*. Retrieved November 19, 2026, from https://www.gov.uk/government/publications/universal-credit-and-couples-an-introduction/universal-credit-further-information-for-couples"),
 (['Internal Revenue Service'], 'n.d.', "Internal Revenue Service. (n.d.). *2021 Child Tax Credit and advance Child Tax Credit payments — Topic A: General information*. Retrieved November 19, 2026, from https://www.irs.gov/credits-deductions/2021-child-tax-credit-and-advance-child-tax-credit-payments-topic-a-general-information"),
 (['5615 sayılı Kanun'], 2007, "5615 sayılı Gelir Vergisi Kanunu ile Bazı Kanunlarda Değişiklik Yapılmasına Dair Kanun. (2007, 4 Nisan). *Resmî Gazete* (Sayı: 26483)."),
 (['7349 sayılı Kanun'], 2021, "7349 sayılı Gelir Vergisi Kanunu ile Bazı Kanunlarda Değişiklik Yapılmasına Dair Kanun. (2021, 25 Aralık). *Resmî Gazete* (Sayı: 31700)."),
]
for s, y, t in EL: refs.append(dict(soy=s, yil=y, metin=t))
def anahtar(r):
    s = r['soy']
    return f"{s[0]}, {r['yil']}" if len(s) == 1 else (f"{s[0]} ve {s[1]}, {r['yil']}" if len(s) == 2 else f"{s[0]} vd., {r['yil']}")
refs.sort(key=lambda r: (r['metin'][0].isdigit(), unicodedata.normalize('NFKD', r['metin']).encode('ascii', 'ignore').decode().lower().replace('van parijs', 'parijs')))
json.dump([dict(anahtar=anahtar(r), yil=r['yil'], metin=r['metin']) for r in refs], open('kaynakca.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(refs)); [print(anahtar(r), '||', r['metin'][:170]) for r in refs]
