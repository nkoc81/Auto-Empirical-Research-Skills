"""Split the provision chapter of each report into narrative sections (one per article heading).

Headings look like '2.1.5. Genç girişimcilerde kazanç istisnası (Mükerrer Madde 20)' (2016: '3.2.5.').
A heading is accepted only if its number is the next one in sequence within the chapter, which removes
false positives such as '3.300 TL'. PDF page = form-feed count in the pdftotext output + 1.
Output: data/interim/narratives.jsonl (report_id, sec_no, title, group, page_start, page_end, text)
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "data" / "text"
FILES = {
    "VHR2016": "Vergi-Harcamalar_-Raporu-2016-.txt", "VHR2017": "Vergi-Harcamalar_-Raporu-2017.txt",
    "VHR2018": "Vergi-Harcamalar_-Raporu-2018.txt", "VHR2020": "VHR_2020.txt", "VHR2021": "VHR_2021.txt",
    "VHR2022": "VHR_2022.txt", "VHR2023": "VHR_2023.txt", "VHR2024": "VHR_2024.txt", "VHR2025": "VHR_2025.txt",
}
FIX = {"Ġ": "İ", "Ģ": "Ş", "‟": "’", "İ": "İ", "Œ": "ğ", "Ɣ": "ş", "": "ı", "7yi": "İyi"}
HEAD = re.compile(r"^\s*(\d)\.(\d{1,2})\.(\d{1,2})\.?\s*(\S.*)$")
GROUP_HEAD = re.compile(r"^\s*(\d)\.(\d)\.?\s*([A-ZÇĞİÖŞÜ].*)$")


def load(rid):
    raw = (T / FILES[rid]).read_text(encoding="utf-8", errors="replace")
    for a, b in FIX.items():
        raw = raw.replace(a, b)
    lines = []
    for p, txt in enumerate(raw.split("\f"), start=1):
        for ln in txt.split("\n"):
            lines.append((p, ln))
    return lines


def group_of(title):
    t = re.sub(r"\s+", " ", title).lower()
    for k, g in [("gelir vergisi", "GV"), ("kurumlar vergisi", "KV"), ("katma değer", "KDV"),
                 ("özel tüketim", "ÖTV"), ("diğer kanun", "DIGER"), ("banka", "BSMV")]:
        if k in t:
            return g
    return None


def extract(rid):
    L = load(rid)
    # body starts after the table of contents: skip lines with dotted leaders
    heads, groups = [], {}
    last = None
    for i, (p, ln) in enumerate(L):
        if "....." in ln or "…" in ln:
            continue
        g = GROUP_HEAD.match(ln)
        if g and group_of(g.group(3)) and len(ln.strip()) < 120 and p > 8:
            groups[(int(g.group(1)), int(g.group(2)))] = group_of(g.group(3))
        m = HEAD.match(ln)
        if not m or p <= 8:
            continue
        a, b, c = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if (a, b) not in groups:          # only sections inside a tax-law chapter
            continue
        key = (a, b, c)
        ok = last is None or key == (last[0], last[1], last[2] + 1) or (key[:2] > last[:2] and c == 1)
        if not ok:
            continue
        title = m.group(4).strip()
        # headings may wrap onto the next line
        if i + 1 < len(L) and not re.search(r"\)\s*\d*$", title) and len(L[i + 1][1].strip()) < 90:
            nxt = L[i + 1][1].strip()
            if nxt and not HEAD.match(L[i + 1][1]):
                title += " " + nxt
        heads.append((i, key, title, p))
        last = key
    # chapter end: the summary chapter heading ('3.1. Vergi Harcaması Çalışması...' / '4.1. Genel Değerlendirme')
    end_idx = next((i for i, (p, ln) in enumerate(L) if i > (heads[-1][0] if heads else 0)
                    and re.match(r"^\s*(3\.1\.?|4\.1\.?)\s+(Vergi Harcaması Çalışması|Genel Değerlendirme)", ln)), len(L))
    out = []
    for n, (i, key, title, p) in enumerate(heads):
        j = heads[n + 1][0] if n + 1 < len(heads) else end_idx
        body, cur = [], None
        for pg, ln in L[i:j]:
            if pg != cur:
                body.append("[[p=%d]]" % pg); cur = pg
            body.append(ln)
        text = re.sub(r"[ \t]+", " ", "\n".join(body)).strip()   # '[[p=N]]' marks the start of PDF page N
        out.append(dict(report_id=rid, sec_no="%d.%d.%d" % key, title=re.sub(r"\s+", " ", title),
                        group=groups.get(key[:2]), page_start=p, page_end=L[j - 1][0], n_chars=len(text), text=text))
    return out


def main():
    allrows = []
    for rid in FILES:
        rows = extract(rid)
        allrows += rows
        g = {}
        for r in rows:
            g[r["group"]] = g.get(r["group"], 0) + 1
        print(rid, len(rows), g, "first:", rows[0]["sec_no"] if rows else None, "last:", rows[-1]["sec_no"] if rows else None)
    with open(ROOT / "data" / "interim" / "narratives.jsonl", "w", encoding="utf-8") as f:
        for r in allrows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
