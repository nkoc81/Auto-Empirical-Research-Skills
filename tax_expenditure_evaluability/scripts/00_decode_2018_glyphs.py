"""Learn a glyph-id -> character map for the 2018 Tax Expenditure Report annex tables.

The annex tables of the 2018 report embed subset Calibri fonts without a ToUnicode map, so text
extraction returns raw glyph ids. Glyph ids are stable across the subsets (they are the ids of the
full Calibri font). We learn the map by (i) seeding it with header strings whose wording is known
from the other reports and (ii) iteratively matching partially decoded words against the vocabulary
of the 2016, 2017 and 2020 annex tables, accepting only unique, consistent matches.
The learned map and its provenance are written to data/interim/glyphmap_2018.json.
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import pymupdf
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "data/raw/hmb/Vergi-Harcamalar_-Raporu-2018.pdf"
OUT = ROOT / "data/interim/glyphmap_2018.json"

doc = pymupdf.open(PDF)
pages = range(306, 388)            # 0-based indices of annex list pages (PDF pages 307-388)
words = []                          # list of glyph-id tuples
for i in pages:
    d = doc[i].get_text("rawdict")
    for b in d["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if "Calibri" not in s["font"]:
                    continue
                cur = []
                for c in s["chars"]:
                    g = ord(c["c"])
                    if g in (3,):
                        if cur:
                            words.append(tuple(cur)); cur = []
                    else:
                        cur.append(g)
                if cur:
                    words.append(tuple(cur))
wc = Counter(words)

# seeds: unambiguous header strings observed in the decoded output of pdfplumber (see README)
seed_pairs = [([94, 358, 396, 258], "Sıra"), ([69, 381, 855], "No:"), ([68, 258, 282, 282, 286], "Madde"),
              ([69, 437, 373, 258, 396, 258, 400, 358], "Numarası"), ([4, 277, 358, 364, 367, 258, 373, 258], "Açıklama")]
gm = {}
for gs, txt in seed_pairs:
    for g, ch in zip(gs, txt):
        gm[g] = ch
for d, g in enumerate(range(1004, 1014)):
    gm[g] = str(d)
gm[856] = "."
gm[32] = ""      # zero-width glyph observed inside thousands separators

# vocabulary from the other reports' extracted rows (descriptions, articles, statuses, headers)
voc = Counter()
for rid in ["VHR2016", "VHR2017", "VHR2020", "VHR2021"]:
    f = ROOT / f"data/interim/annex_rows_{rid}.csv"
    if f.exists():
        r = pd.read_csv(f)
        for col in ["article", "description", "quality"] + [f"raw_{i}" for i in range(5)]:
            for v in r[col].dropna().astype(str):
                for w in v.split():
                    voc[w] += 1
for w in ("EK I-1 I-2 I-3 I-4 I-5 Gelir Kurumlar Katma Değer Özel Tüketim Vergisi Uygulamasındaki Vergi Harcamaları Listesi "
          "Kanunu Diğer Kanunlar (Bin TL) Tahmin Kalitesi Tahminin GENEL TOPLAM Kanun Adı Banka Sigorta Muameleleri "
          "Motorlu Taşıtlar İletişim Hükümleri Yeni uygulama Çok İyi Yaklaşık").split():
    voc[w] += 50
vocab = list(voc)
by_len = defaultdict(list)
for w in vocab:
    by_len[len(w)].append(w)

prov = {g: "seed" for g in gm}
changed = True
it = 0
while changed and it < 50:
    changed = False
    it += 1
    proposals = defaultdict(Counter)
    for w, n in wc.most_common():
        w2 = [g for g in w if gm.get(g, None) != ""]
        unknown = [g for g in w2 if g not in gm]
        if not unknown or len(set(unknown)) > 3:
            continue
        cands = []
        for v in by_len[len(w2)]:
            ok, loc = True, {}
            for g, ch in zip(w2, v):
                if g in gm:
                    if gm[g] != ch:
                        ok = False; break
                else:
                    if loc.get(g, ch) != ch or (ch in gm.values() and ch not in loc.values()):
                        ok = False; break
                    loc[g] = ch
            if ok:
                cands.append((v, loc))
        if len(cands) == 1:
            for g, ch in cands[0][1].items():
                proposals[g][ch] += n
    for g, cnt in proposals.items():
        ch, n = cnt.most_common(1)[0]
        if len(cnt) == 1 and ch not in gm.values():
            gm[g] = ch; prov[g] = f"vocab_iter{it}"; changed = True

# manual corrections from context (see printed contexts in PROJECT_STATUS.md):
#   876 appears in "Madde 22/1" -> '/', 895 closes "(Bin TL)" -> ')', 884 in "Madde 7 – 1/b" -> '–',
#   1081 in "harcamalarının % 100'ü" -> '%', 41 in "KATMA DEĞER" -> 'Ğ'
for g, ch in {876: "/", 895: ")", 884: "–", 1081: "%", 41: "Ğ"}.items():
    gm[g] = ch; prov[g] = "manual_context"

unknown = Counter()
for w, n in wc.items():
    for g in w:
        if g not in gm:
            unknown[g] += n
tot = sum(n * len(w) for w, n in wc.items())
cov = 1 - sum(unknown.values()) / tot
json.dump({"map": {str(k): v for k, v in sorted(gm.items())}, "provenance": {str(k): v for k, v in prov.items()},
           "coverage_share_of_glyphs": cov, "unknown_glyphs": dict(unknown.most_common())},
          open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("mapped glyphs:", len(gm), "coverage:", round(cov, 4), "unknown top:", unknown.most_common(15))
