"""kaynak_meta.json (CrossRef) + elle doğrulanmış ekler -> APA 7 kaynakça (Markdown) ve atıf anahtarları."""
import json, re
DUSUR = {'10.34196/ijm.00208', '10.1787/568bb35b-en', '10.2139/ssrn.2558365'}  # yıl/numara doğrulanamadı
YIL_DUZELT = {'10.1093/qje/qjab028': 2022, '10.1093/qje/qjac038': 2023}  # QJE basılı sayı yılı
OZEL = ['Europe', 'European', 'EU', 'US', 'U.S.', 'United', 'States', 'Kenya', 'Finnish', 'Germany', 'Sweden', 'Swedish',
        'Denmark', 'Spain', 'Alaska', 'Permanent', 'Fund', 'OECD', 'EITC', 'Earned', 'Income', 'Tax', 'Credit', 'Americans',
        'BI', 'SPIN', 'Korpi', 'Palme’s', 'Palme', 'HHoT', 'EUROMOD', 'Black-White', 'Temporary', 'Assistance', 'Needy', 'Families',
        'II', 'Iran', 'Europe:', 'Kenya:', 'Germany:', 'Sweden:', 'States:', 'Fund:', 'Two', 'U.S.']
def cumle(t, proper=True):
    t = t.rstrip('*').strip()
    ws = t.split(' '); out = []
    bas = True
    for w in ws:
        cl = w.strip('“”"‘’(),:;?')
        if bas: out.append(w[0].upper() + w[1:])
        elif cl.isupper() and len(cl) > 1 or any(c.isdigit() for c in cl) or w in OZEL or cl in OZEL: out.append(w)
        elif re.match(r'^[A-Z][a-z]+[A-Z]', cl): out.append(w)
        else: out.append(w.lower())
        bas = w.endswith(':') or w.endswith('?')
    return ' '.join(out)
def soyad_ad(s):
    s = re.sub(r'\b([A-ZÄÖÜ]{2,})\b', lambda m: m.group(1).capitalize(), s)
    return s
M = [m for m in json.load(open('kaynak_meta.json', encoding='utf-8')) if m['doi'] not in DUSUR]
refs = []
for m in M:
    yil = YIL_DUZELT.get(m['doi'], m['yil'])
    yz = soyad_ad(m['yazar'])
    soy = [soyad_ad(x) for x in m['soyadlar']]
    if m['ilk'] == 'Whitmore Schanzenbach': soy[0] = 'Schanzenbach'; yz = yz.replace('Whitmore Schanzenbach, D.', 'Schanzenbach, D. W.')
    t = cumle(m['baslik'])
    if m['tur'] == 'journal-article' and 'IMF' not in m['dergi']:
        loc = f"*{m['dergi']}*, *{m['cilt']}*" + (f"({m['sayi']})" if m['sayi'] and m['sayi'] != m['cilt'] else '')
        loc += f", {m['sayfa'].replace('-', '–')}" if m['sayfa'] and not m['madde'] else (f", Article {m['madde']}" if m['madde'] else '')
        s = f"{yz} ({yil}). {t}. {loc}. https://doi.org/{m['doi']}"
    elif 'IMF' in m['dergi']:
        s = f"{yz} ({yil}). *{t}* (IMF Working Paper No. 21/179). International Monetary Fund. https://doi.org/{m['doi']}"
    elif m['tur'] == 'book':
        s = f"{yz} ({yil}). *{t}*. World Bank. https://doi.org/{m['doi']}"
    elif m['tur'] == 'book-chapter':
        s = f"{yz} ({yil}). {t}. In K. F. Zimmermann (Ed.), *{m['dergi']}* (pp. {m['sayfa'].replace('-', '–')}). Springer. https://doi.org/{m['doi']}"
    refs.append(dict(soy=soy, yil=yil, metin=s))
# Elle eklenen, ayrıca doğrulanmış kaynaklar
refs.append(dict(soy=['Bartik', 'Rhodes', 'Broockman', 'Krause', 'Miller', 'Vivalt'], yil=2024, metin=
 "Bartik, A. W., Rhodes, E., Broockman, D. E., Krause, P. K., Miller, S., & Vivalt, E. (2024). *The impact of unconditional cash transfers on consumption and household balance sheets: Experimental evidence from two US states* (NBER Working Paper No. 32784). National Bureau of Economic Research. https://doi.org/10.3386/w32784"))
VERI = [
 (['Eurostat'], '2026a', "Eurostat. (2026a). *Employment by educational attainment level – annual data* (lfsi_educ_a) [Data set]. Retrieved November 14, 2026, from https://ec.europa.eu/eurostat/databrowser/product/view/lfsi_educ_a"),
 (['Eurostat'], '2026b', "Eurostat. (2026b). *Employment rate by educational attainment level and household composition* (lfst_hheredty) [Data set]. Retrieved November 14, 2026, from https://ec.europa.eu/eurostat/databrowser/product/view/lfst_hheredty"),
 (['Eurostat'], '2026c', "Eurostat. (2026c). *Gross domestic product (GDP) and main components (output, expenditure and income) – annual data* (nama_10_gdp) [Data set]. Retrieved November 14, 2026, from https://ec.europa.eu/eurostat/databrowser/product/view/nama_10_gdp"),
 (['Eurostat'], '2026d', "Eurostat. (2026d). *LFS main indicators (lfsi): Reference metadata in Euro SDMX Metadata Structure (ESMS)*. Retrieved November 14, 2026, from https://ec.europa.eu/eurostat/cache/metadata/en/lfsi_esms.htm"),
 (['Eurostat'], '2026e', "Eurostat. (2026e). *Educational attainment of population (edat1): Reference metadata in Euro SDMX Metadata Structure (ESMS)*. Retrieved November 14, 2026, from https://ec.europa.eu/eurostat/cache/metadata/en/edat1_esms.htm"),
 (['OECD'], '2026a', "OECD. (2026a). *Adequacy of minimum income benefits* (DSD_TAXBEN_IA@DF_IA) [Data set]. OECD Data Explorer. Retrieved November 14, 2026, from https://sdmx.oecd.org/public/rest/data/OECD.ELS.JAI,DSD_TAXBEN_IA@DF_IA,1.0/all"),
 (['OECD'], '2026b', "OECD. (2026b). *Effective tax rates on taking up work when claiming minimum income benefits* (DSD_TAXBEN_PTR@DF_PTRSA) [Data set]. OECD Data Explorer. Retrieved November 14, 2026, from https://sdmx.oecd.org/public/rest/data/OECD.ELS.JAI,DSD_TAXBEN_PTR@DF_PTRSA,1.0/all"),
]
for s, y, t in VERI: refs.append(dict(soy=s, yil=y, metin=t))
def anahtar(r):
    s = r['soy']
    if len(s) == 1: return f"{s[0]}, {r['yil']}"
    if len(s) == 2: return f"{s[0]} ve {s[1]}, {r['yil']}"
    return f"{s[0]} vd., {r['yil']}"
import unicodedata
srt = lambda r: (unicodedata.normalize('NFKD', r['metin']).encode('ascii', 'ignore').decode().lower())
refs.sort(key=srt)
json.dump([dict(anahtar=anahtar(r), metin=r['metin'], yil=r['yil']) for r in refs], open('kaynakca.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open('kaynakca.md', 'w', encoding='utf-8').write('\n\n'.join(r['metin'] for r in refs) + '\n')
akademik = [r for r in refs if r['soy'][0] not in ('Eurostat', 'OECD')]
print(len(refs), 'toplam;', len(akademik), 'akademik;', sum(1 for r in akademik if int(str(r['yil'])[:4]) >= 2020), '>=2020;',
      sum(1 for r in akademik if int(str(r['yil'])[:4]) >= 2021), '>=2021')
for r in refs: print(anahtar(r))
