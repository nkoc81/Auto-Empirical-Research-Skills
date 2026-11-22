"""Extract item-level tax expenditure tables (Annex I-1 ... I-5) from Turkish Tax Expenditure Reports.

For each report the script locates the annex list pages, infers column positions from the
header row on every page (Sıra No | Madde/Kanun | Açıklama | 5 year columns | Tahmin Kalitesi),
and assigns words to rows anchored on the "Sıra No" integers. Every extracted row keeps the
PDF page number so that each observation can be traced back to the source table.

Output: data/interim/annex_rows_<report>.csv and data/interim/annex_totals_<report>.csv
Usage : python scripts/01_extract_annex_tables.py [report_id ...]
"""
import re
import sys
from pathlib import Path

import pandas as pd
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "interim"
OUT.mkdir(parents=True, exist_ok=True)

# report_id -> pdf path. Report id = year in the report title (publication label).
REPORTS = {
    "VHR2016": RAW / "hmb" / "Vergi-Harcamalar_-Raporu-2016-.pdf",
    "VHR2017": RAW / "hmb" / "Vergi-Harcamalar_-Raporu-2017.pdf",
    "VHR2018": RAW / "hmb" / "Vergi-Harcamalar_-Raporu-2018.pdf",
    "VHR2020": RAW / "gib" / "VHR_2020.pdf",
    "VHR2021": RAW / "gib" / "VHR_2021.pdf",
    "VHR2022": RAW / "gib" / "VHR_2022.pdf",
    "VHR2023": RAW / "gib" / "VHR_2023.pdf",
    "VHR2024": RAW / "gib" / "VHR_2024.pdf",
    "VHR2025": RAW / "gib" / "VHR_2025.pdf",
}

# Glyph repairs for the 2017 report (font without proper Unicode mapping for some Turkish letters)
REPAIR = {"Ɣ": "ş", "Œ": "ğ", "7yi": "İyi", "Ġ": "İ", "Ģ": "Ş", "\uf0f5": "ı", "Ͳ": "-", "\x03": " "}

YEAR_RE = re.compile(r"^(19|20)\d\d$")
NUM_RE = re.compile(r"^-?\d{1,3}(\.\d{3})*(,\d+)?$|^-?\d+$")
TAX_SECTION_RE = re.compile(r"^\d\s*[-–Ͳ]\s*\S")


def repair(s):
    for a, b in REPAIR.items():
        s = s.replace(a, b)
    return s


def is_list_page(text):
    """A list page carries a 'Sıra No' header, at least five year labels and a quality column."""
    t = repair(text)
    return bool(re.search(r"S[ıi]?ra\b", t)) and len(re.findall(r"\b20\d\d\b", t)) >= 5 \
        and "Kalite" in t and "Fonksiyonel" not in t


GLYPHMAP = None   # set for the 2018 report (see scripts/00_decode_2018_glyphs.py)


def glyph_words(page, d, rotated):
    """Word builder for glyph-id encoded text (2018 report): characters come from rawdict, glyph 3 is
    the space glyph, every other glyph is translated with GLYPHMAP."""
    H, W = page.rect.height, page.rect.width
    out = []
    for b in d["blocks"]:
        for l in b.get("lines", []):
            for sp in l["spans"]:
                cur, box = [], None
                chars = sp["chars"] + [{"c": chr(3), "bbox": None}]
                for c in chars:
                    g = ord(c["c"])
                    if g == 3:
                        if cur:
                            txt = repair("".join(cur))
                            x0, y0, x1, y1 = box
                            if rotated:
                                out.append({"text": txt, "x0": H - y1, "x1": H - y0, "top": x0, "bottom": x1})
                            else:
                                out.append({"text": txt, "x0": x0, "x1": x1, "top": y0, "bottom": y1})
                        cur, box = [], None
                        continue
                    ch = GLYPHMAP.get(g, c["c"]) if "Calibri" in sp["font"] else c["c"]
                    cur.append(ch)
                    bb = c["bbox"]
                    box = bb if box is None else (min(box[0], bb[0]), min(box[1], bb[1]), max(box[2], bb[2]), max(box[3], bb[3]))
    W2 = W if rotated else H
    text = "\n".join(" ".join(w["text"] for w in l) for l in lines_of(out))
    return out, text, W2, rotated


def page_words(page):
    """Words with pdfplumber-style keys. Pages whose text runs bottom-to-top (tables printed rotated by
    90 degrees, as in the 2020-2023 reports) are mapped to a reading-order coordinate system."""
    d = page.get_text("dict")
    dirs = [l["dir"] for b in d["blocks"] for l in b.get("lines", [])]
    rotated = sum(1 for x in dirs if abs(x[1]) > 0.9) > 0.6 * max(1, len(dirs))
    H, W = page.rect.height, page.rect.width
    out = []
    if GLYPHMAP is not None:
        return glyph_words(page, page.get_text("rawdict"), rotated)
    for x0, y0, x1, y1, txt, *_ in page.get_text("words"):
        if rotated:
            box = (H - y1, H - y0, x0, x1)
        else:
            box = (x0, x1, y0, y1)
        if GLYPHMAP is not None:
            txt = "".join(" " if ord(c) == 3 else GLYPHMAP.get(ord(c), c) for c in txt)
        txt = repair(txt)
        parts = txt.split(" ")          # the 2017 report encodes spaces as \x03 inside a single "word"
        n = max(1, len(txt))
        pos = 0
        for part in parts:
            if part:
                a = box[0] + (box[1] - box[0]) * pos / n
                b = box[0] + (box[1] - box[0]) * (pos + len(part)) / n
                out.append({"text": part, "x0": a, "x1": b, "top": box[2], "bottom": box[3]})
            pos += len(part) + 1
    height = W if rotated else H
    text = "\n".join(" ".join(w["text"] for w in l) for l in lines_of(out))
    return out, text, height, rotated


def lines_of(words, tol=3):
    out = []
    for w in sorted(words, key=lambda w: (w["top"], w["x0"])):
        if out and abs(out[-1][0]["top"] - w["top"]) < tol:
            out[-1].append(w)
        else:
            out.append([w])
    return [sorted(l, key=lambda w: w["x0"]) for l in out]


def header_blocks(words):
    """Find every header line carrying >=5 year labels; return list of header dicts."""
    hs = []
    for l in lines_of(words):
        ys = [w for w in l if YEAR_RE.match(w["text"])]
        if len(ys) >= 5:
            ys = ys[:5]
            hs.append(dict(ytop=max(w["bottom"] for w in ys), yline=min(w["top"] for w in ys),
                           yx=[(w["x0"] + w["x1"]) / 2 for w in ys], years=[int(w["text"]) for w in ys]))
    for h in hs:
        near = [w for w in words if abs(w["top"] - h["yline"]) < 22]
        q = [w for w in near if repair(w["text"]).startswith("Kalitesi")]
        h["qx"] = (q[0]["x0"] + q[0]["x1"]) / 2 if q else h["yx"][-1] + (h["yx"][-1] - h["yx"][-2])
        sno = [w for w in near if w["text"].startswith(("Sıra", "Sra", "SraNo"))]
        sl = sno[0]["top"] if sno else None
        art = [w for w in near if w["text"].startswith(("Madde", "Kanun", "MaddeNumaras", "Düzenlemenin"))
               and (sl is None or abs(w["top"] - sl) < 13) and (not sno or w["x0"] > sno[0]["x1"])]
        h["sno_x0"] = sno[0]["x0"] if sno else 50
        nos = [w for w in near if w["text"].startswith(("Sıra", "Sra", "No", "SraNo")) and w["x0"] < h["sno_x0"] + 40]
        h["sno_x1"] = max((w["x1"] for w in nos), default=h["sno_x0"] + 30)
        h["art_x0"] = art[0]["x0"] if art else None
        dsc = [w for w in near if repair(w["text"]).startswith(("Açıklama", "Açklama", "Açıkla"))
               and (sl is None or abs(w["top"] - sl) < 13)]
        if art:
            ah = [w for w in near if abs(w["top"] - art[0]["top"]) < 13 and w["x0"] >= art[0]["x0"]
                  and (not dsc or w["x1"] < dsc[0]["x0"]) and w["x1"] < h["yx"][0] - 30
                  and not YEAR_RE.match(w["text"])]
            h["art_x1"] = max((w["x1"] for w in ah), default=art[0]["x1"])
        else:
            h["art_x1"] = None
    return hs


def find_desc_start(body, h):
    """Description column start = left-most text-segment start (seen at least twice) lying right of
    the article-column header. Segments are runs of words separated by gaps > 6 pt."""
    from collections import Counter
    left_edge = h["yx"][0] - (h["yx"][1] - h["yx"][0]) / 2
    lim = h.get("art_x1") or ((h["art_x0"] or 60) + 40)
    starts = Counter()
    for l in lines_of([w for w in body if w["x1"] < left_edge]):
        prev = None
        for w in l:
            if (prev is None or w["x0"] - prev["x1"] > 6) and w["x0"] > lim - 2:
                starts[round(w["x0"] / 2) * 2] += 1
            prev = w
    good = sorted(x for x, n in starts.items() if n >= 2)
    return (good[0] - 2) if good else (lim + 5)


def col_of(xc, h):
    cols = ["y%d" % i for i in range(5)] + ["quality"]
    centres = h["yx"] + [h["qx"]]
    left_edge = h["yx"][0] - (h["yx"][1] - h["yx"][0]) / 2
    if xc < left_edge:
        if xc < h["sno_x1"] + 4:
            return "sno"
        if h.get("desc_x0") is not None and xc < h["desc_x0"]:
            return "article"
        return "desc"
    for i, c in enumerate(centres):
        lo = (centres[i - 1] + c) / 2 if i > 0 else left_edge
        hi = (c + centres[i + 1]) / 2 if i + 1 < len(centres) else 1e9
        if lo <= xc < hi:
            return cols[i]
    return "quality"


def join(ws, h=None, col=None):
    ws = sorted(ws, key=lambda w: (round(w["top"] / 3), w["x0"]))
    return repair(" ".join(w["text"] for w in ws)).strip()


def parse_value(s):
    s = s.strip()
    if not s:
        return None, "blank"
    if s in ("-", "–", "—"):
        return None, "dash"
    compact = s.replace(" ", "")
    if NUM_RE.match(compact):
        return int(compact.replace(".", "").split(",")[0]), "estimated"
    toks = [x for x in s.split() if NUM_RE.match(x)]
    grouped = [x for x in toks if "." in x]
    if len(toks) > 1 and len(grouped) == 1 and len(toks) == len(s.split()):
        # e.g. "242 708.182": stray fragment next to the formatted amount; keep the formatted amount, flag it
        return int(grouped[0].replace(".", "")), "estimated_flagged"
    low = s.lower().replace(" ", "")
    if "içindeyer" in low or "dahiledil" in low or "içindedir" in low:
        return None, "included_elsewhere"
    fmt = [x for x in s.split() if re.match(r"^\d{1,3}(\.\d{3})+$", x)]
    if len(fmt) == 1 and s.split()[0] == fmt[0]:
        # amount followed by stray text that belongs to a neighbouring cell or a footnote
        return int(fmt[0].replace(".", "")), "estimated_flagged"
    if "oluşma" in low or "oluma" in low or "oluƔma" in low:
        return None, "no_te_arising"
    if "temin" in low or "edilemi" in low:
        return None, "data_not_available"
    if "dikkate" in low or "kapsamında" in low:
        return None, "included_elsewhere"
    if "yeni" in low:
        return None, "new_measure"
    if "yürürlük" in low or "kaldır" in low or "mülga" in low:
        return None, "repealed"
    return None, "other_text"


def extract(report_id, pdf_path):
    global GLYPHMAP
    GLYPHMAP = None
    if report_id == "VHR2018":
        import json
        GLYPHMAP = {int(k): v for k, v in json.load(open(ROOT / "data/interim/glyphmap_2018.json",
                                                         encoding="utf-8"))["map"].items()}
    rows, totals = [], []
    section, table_title = None, None
    prev_h, prev_page, prev_rot = None, None, None
    doc = pymupdf.open(pdf_path)
    if True:
        for pno, page in enumerate(doc, start=1):
            words, text, page_h, rotated = page_words(page)
            cont = False
            if not is_list_page(text):
                t0 = repair(text)
                if prev_h is not None and prev_page == pno - 1 and prev_rot == rotated \
                        and not re.search(r"EK\s*I{2,3}|EK\s*IV|Fonksiyonel|KAYNAK", t0) \
                        and len(re.findall(r"\d{1,3}(?:\.\d{3})+", t0)) >= 3:
                    cont = True          # continuation page printed without the table header
                else:
                    continue
            hs = header_blocks(words) if not cont else []
            if cont:
                hh = dict(prev_h); hh["ytop"] = 30; hh["yline"] = 25
                hs = [hh]
            if not hs:
                continue
            # drop printed page numbers: lone short integers left of the table or alone on their line
            lns = lines_of(words)
            alone = {id(l[0]) for l in lns if len(l) == 1}
            words = [w for w in words if not (w["text"].isdigit() and len(w["text"]) <= 4 and
                                              (w["x1"] < hs[0]["sno_x0"] - 3 or
                                               (id(w) in alone and (w["top"] > page_h - 110 or w["top"] < 50)
                                                and not (hs[0]["sno_x0"] - 8 <= (w["x0"] + w["x1"]) / 2 <= hs[0]["sno_x1"] + 6))))]
            if not cont:
                hs = header_blocks(words)
            prev_h, prev_page, prev_rot = dict(hs[-1]), pno, rotated
            t = repair(text).replace("\n", " ")
            m = re.search(r"EK\s*I\s*[-–Ͳ]?\s*([1-5])\s+(\S.*?(?:Listesi|Hükümler\S*))", t)
            if m:
                new_title = "EK I-%s %s" % (m.group(1), m.group(2).strip())
                if table_title is None or new_title[:6] != table_title[:6]:
                    section = None          # a new annex table starts: do not carry the previous section label
                table_title = new_title
            # section labels ("1- Gelir Vergisi Kanunu", "2- Diğer Kanunlar") with their vertical position
            labels = []
            for l in lines_of(words):
                txt = repair(" ".join(w["text"] for w in l))
                mm = re.match(r"^(\d)\s*[-–Ͳ]\s*([^()]+?)(?:\s*\(Bin TL\).*|\s+Tahmin.*)?$", txt)
                if mm and l[0]["x0"] < hs[0]["sno_x0"] + 25 and l[0]["top"] < hs[-1]["yline"] \
                        and not re.match(r"^\d\s*[-–Ͳ]\s*\d", txt):
                    labels.append((l[0]["top"], "%s- %s" % (mm.group(1), mm.group(2).strip())))
            for bi, h in enumerate(hs):
                block_end = hs[bi + 1]["yline"] - 30 if bi + 1 < len(hs) else page_h - 45
                for y, lab in labels:
                    if y < h["yline"] and (bi == 0 or y > hs[bi - 1]["ytop"]):
                        section = lab
                if section is None:
                    section = "1- (ana kanun)"
                body = [w for w in words if h["ytop"] + 1 < w["top"] < block_end]
                body = [w for w in body if not any(abs(w["top"] - y) < 2 for y, _ in labels)]
                h["desc_x0"] = find_desc_start(body, h)
                start_y = h["ytop"]
                gt = [w for w in body if (w["text"].upper().replace(" ", "") == "GENELTOPLAM") or
                      (w["text"].upper() == "GENEL" and any(abs(v["top"] - w["top"]) < 3 and v["text"].upper() == "TOPLAM"
                                                             for v in body))]
                if gt:
                    gy = gt[0]["top"]
                    # totals may sit on the GENEL line or on a line just above/below it
                    line = [w for w in body if abs(w["top"] - gy) < 9]
                    tot = {"report_id": report_id, "page": pno, "table": table_title, "section": section}
                    vals = {}
                    for w in line:
                        c = col_of((w["x0"] + w["x1"]) / 2, h)
                        if c.startswith("y"):
                            vals[c] = vals.get(c, "") + w["text"]
                    for i in range(5):
                        v, st = parse_value(vals.get("y%d" % i, ""))
                        tot["year_%d" % i], tot["value_%d" % i] = h["years"][i], v
                    totals.append(tot)
                    start_y = max(w["bottom"] for w in line) + 0.5
                    body = [w for w in body if w["top"] > start_y]
                anchors = sorted([w for w in body if w["text"].isdigit()
                                  and h["sno_x0"] - 8 <= (w["x0"] + w["x1"]) / 2 <= h["sno_x1"] + 6],
                                 key=lambda w: w["top"])
                centres = [(a["top"] + a["bottom"]) / 2 for a in anchors]
                for i, a in enumerate(anchors):
                    lo = start_y if i == 0 else (centres[i - 1] + centres[i]) / 2
                    hi = block_end if i + 1 == len(anchors) else (centres[i] + centres[i + 1]) / 2
                    band = [w for w in body if lo <= (w["top"] + w["bottom"]) / 2 < hi and w is not a]
                    cells = {}
                    for w in band:
                        cells.setdefault(col_of((w["x0"] + w["x1"]) / 2, h), []).append(w)
                    rec = {"report_id": report_id, "page": pno, "table": table_title, "section": section,
                           "row_no": int(a["text"]), "article": join(cells.get("article", [])),
                           "description": join(cells.get("desc", [])), "quality": join(cells.get("quality", []))}
                    for j in range(5):
                        raw = join(cells.get("y%d" % j, []))
                        v, st = parse_value(raw)
                        rec["year_%d" % j], rec["value_%d" % j], rec["status_%d" % j], rec["raw_%d" % j] = \
                            h["years"][j], v, st, raw
                    rows.append(rec)
    pd.DataFrame(rows).to_csv(OUT / f"annex_rows_{report_id}.csv", index=False)
    pd.DataFrame(totals).to_csv(OUT / f"annex_totals_{report_id}.csv", index=False)
    return pd.DataFrame(rows), pd.DataFrame(totals)


if __name__ == "__main__":
    ids = sys.argv[1:] or list(REPORTS)
    for rid in ids:
        r, t = extract(rid, REPORTS[rid])
        print(rid, "rows:", len(r), "total lines:", len(t))
