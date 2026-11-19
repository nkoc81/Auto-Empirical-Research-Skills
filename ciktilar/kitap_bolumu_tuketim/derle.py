"""Kaynakçayı ekler, atıf-kaynakça eşleşmesini denetler, kelime sayar, Word'e çevirir."""
import json, re, subprocess, sys
K = json.load(open('kaynakca/kaynakca.json', encoding='utf-8'))
g = open('bolum_govde.md', encoding='utf-8').read()
ana = g.split('# Kaynakça')[0]
sorun = False
# 1) Her kaynak metinde geçiyor mu? (parantez içi "Ad, yıl" ya da anlatı "Ad (yıl)")
for r in K:
    a, y = r['anahtar'].rsplit(', ', 1)
    if not (re.search(re.escape(a) + r",? (?:[^()]*?, )?" + re.escape(str(y)), ana) or re.search(re.escape(a) + r" \(" + re.escape(str(y)), ana)
            or re.search(re.escape(a) + r", (?:n\.d\., )?\d{4}", ana) and str(y) in ana):
        print('METİNDE YOK:', r['anahtar']); sorun = True
# 2) Metindeki her atıf kaynakçada var mı?
adlar = {r['anahtar'].rsplit(', ', 1)[0]: set() for r in K}
for r in K: adlar[r['anahtar'].rsplit(', ', 1)[0]].add(str(r['yil']))
for m in re.finditer(r"([A-ZÇÖÜŞİ][\wÀ-ž.\-’ ]+?(?: ve [A-ZÀ-ž][\wÀ-ž\-’]+| vd\.)?)(?:,| \() ((?:n\.d\.|\d{4})(?:, (?:n\.d\.|\d{4}))*)", ana):
    ad = m.group(1).strip()
    ad = re.sub(r'^(?:.*\(|.*; )', '', ad)
    for y in re.findall(r'n\.d\.|\d{4}', m.group(2)):
        cand = [k for k in adlar if ad.endswith(k)]
        if cand and y not in adlar[max(cand, key=len)]:
            print('KAYNAKÇADA YOK:', ad, y); sorun = True
tam = g.replace('KAYNAKCA_YER_TUTUCU', '\n\n'.join(r['metin'] for r in K))
open('bolum_tam.md', 'w', encoding='utf-8').write(tam)
govde = re.sub(r'^---.*?---', '', ana, flags=re.S)
print('Kelime (kaynakça hariç, tablo dahil):', len(re.findall(r"\w[\w’'\-]*", govde)))
print('Kelime (tablo hariç):', len(re.findall(r"\w[\w’'\-]*", '\n'.join(l for l in govde.splitlines() if not l.startswith('|')))))
print('Kaynak sayısı:', len(K), '| 2021+:', sum(1 for r in K if isinstance(r['yil'], int) and r['yil'] >= 2021))
subprocess.run(['pandoc', 'bolum_tam.md', '-o', 'Gelir_Destegi_Turleri_ve_Hanehalki_Tuketimi.docx'], check=True)
sys.exit(1 if sorun else 0)
