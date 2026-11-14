"""Kaynakçayı makaleye ekler, atıf-kaynakça eşleşmesini denetler, kelime sayar, Word'e çevirir."""
import json, re, subprocess, sys
from pathlib import Path
M = Path(__file__).resolve().parents[1] / 'makale'
K = json.load(open(M.parent / 'kaynakca/kaynakca.json', encoding='utf-8'))
govde = (M / 'makale_govde.md').read_text(encoding='utf-8')
ana = govde.split('# Kaynakça')[0]
# Metin içi atıflar
ad = r"(?:de |van den |vom )?[A-ZÄÖÜÇŞİ][\w’'\-ÄÖÜäöüçşğıœæøåéèíóú]+"
y = r"(\d{4}[a-z]?)"
bul = set()
for m in re.finditer(rf"({ad})(?: ve ({ad})| vd\.)?,? \(?((?:\d{{4}}[a-z]?)(?:, \d{{4}}[a-z]?)*)\)?", ana):
    yillar = re.findall(r"\d{4}[a-z]?", m.group(3))
    ilk, iki = m.group(1), m.group(2)
    tip = 'vd' if ' vd.' in m.group(0) else ('ve' if iki else 'tek')
    for yy in yillar:
        bul.add((ilk, iki, tip, yy))
# Kaynakça anahtarları
def kk(a):
    m = re.match(r"(.+?)(?: ve (.+?)| vd\.)?, (\d{4}[a-z]?)$", a)
    return m.group(1), m.group(2), ('vd' if ' vd.' in a else ('ve' if m.group(2) else 'tek')), m.group(3)
ref = {kk(r['anahtar']) for r in K}
# OECD, 2026a, 2026b gibi ardışık yıl harfleri
for m in re.finditer(r"\((OECD|Eurostat), (\d{4}[a-z])(?:, (\d{4}[a-z]))?\)", ana):
    for yy in m.groups()[1:]:
        if yy: bul.add((m.group(1), None, 'tek', yy))
bul = {b for b in bul if b in ref or (b[0] in {r[0] for r in ref} and b[3].startswith(('19', '20')))}
eksik = bul - ref
atil = ref - bul
print('Metinde olup kaynakçada olmayan:', sorted(eksik))
print('Kaynakçada olup metinde atıf yapılmayan:', sorted(atil))
tam = govde.replace('KAYNAKCA_YER_TUTUCU', '\n\n'.join(r['metin'] for r in K))
(M / 'makale_tam.md').write_text(tam, encoding='utf-8')
# Kelime sayımı: öz + gövde, tablolar ve kaynakça hariç
metin = re.sub(r'^---.*?---', '', ana, flags=re.S)
metin = '\n'.join(l for l in metin.splitlines() if not l.strip().startswith('|') and not l.strip().startswith('$$'))
print('Kelime (kaynakça ve tablolar hariç):', len(re.findall(r"\w[\w’'\-]*", metin)))
print('Kelime (kaynakça hariç, tablolar dahil):', len(re.findall(r"\w[\w’'\-]*", re.sub(r'^---.*?---', '', ana, flags=re.S))))
if eksik or atil: sys.exit(1)
