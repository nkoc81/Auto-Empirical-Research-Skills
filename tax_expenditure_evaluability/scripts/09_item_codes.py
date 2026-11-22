"""Attach narrative-section codes to annex items and derive C3/C4 for every report-item-year.

Mapping item -> section (same report):
  own-law items (sub_table 'main'): same tax group and same article key (prefix + article number, with the letter
    suffix for articles such as 'Mükerrer 20/A', '5/B', '32/A');
  ÖTV items: also by decree number (BKK/CK 'yyyy/nnnn');
  other-law items (sub_table 'other'): by law number, first in the 'Diğer Kanunlar' chapter, then in any section
    whose title names the law.
  BSMV, MTV, ÖİV items: the reports contain no narrative sections for these taxes.
Items without a section get C1, C2, C5-C9 = 0 with note 'no_narrative' (decision: not reported in the document).
Outputs: data/coding/item_section_map.csv, data/coding/item_year_codes.csv, data/coding/item_codes.csv
"""
import difflib
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CD = ROOT / "data" / "coding"
GROUP = {"GV": "GV", "KV": "KV", "KDV": "KDV", "ÖTV": "ÖTV"}
NARR = ["C1", "C2", "C5", "C6", "C7", "C8", "C9", "M", "B"]
LETTER_ART = re.compile(r"^(m|mm)(\d+)/([a-cç])(?![\wçğıöşü])")


def item_art_key(ref):
    ref = str(ref)
    m = LETTER_ART.match(ref)
    if m:
        return (m.group(1), f"{m.group(2)}/{m.group(3)}")
    m = re.match(r"^(mm|gm|em|m)(\d+)", ref)
    return (m.group(1), m.group(2)) if m else None


def section_keys(title, text):
    t = title
    keys, laws, decrees = set(), set(), set()
    for grp in re.findall(r"\(([^()]*(?:Madde|Md|BKK|Karar)[^()]*)\)", t, re.I) or [t]:
        for part in re.split(r",|ve", grp):
            p = part.strip()
            pre = "mm" if re.search(r"Mük", p, re.I) else "gm" if re.search(r"Geç", p, re.I) else "em" if re.search(r"\bEk\b", p) else "m"
            m = re.search(r"(\d+)(?:\s*/\s*([A-Ca-cÇç])\b)?", p)
            if m and not re.search(r"\d{4}/\d", p):
                num = m.group(1) + (f"/{m.group(2).lower()}" if m.group(2) else "")
                keys.add((pre, num))
        for d in re.findall(r"(\d{4}/\d{3,5})", grp):
            decrees.add(d)
    # bare numbers after the first article in lists such as '(Madde 26, 27, 28)'
    for grp in re.findall(r"\((?:Mükerrer |Geçici )?Madde ([\d,\s]+)\)", t):
        pre = "m"
        for n in re.findall(r"\d+", grp):
            keys.add((pre, n))
    head = t + " " + text[:400]
    laws.update(re.findall(r"(\d{3,4}) [Ss]ayılı", head))
    decrees.update(re.findall(r"(\d{4}/\d{3,5})", t))
    return keys, laws, decrees


def main():
    I = pd.read_csv(ROOT / "data" / "interim" / "items_by_report.csv")
    S = pd.read_csv(CD / "section_codes.csv", dtype=str, keep_default_na=False, na_values=[""])
    import json
    N = {(r["report_id"], r["sec_no"]): r for r in map(json.loads, open(ROOT / "data" / "interim" / "narratives.jsonl", encoding="utf-8"))}
    sec_info = []
    for _, s in S.iterrows():
        n = N[(s.report_id, s.sec_no)]
        body = re.sub(r"\[\[p=\d+\]\]", " ", n["text"])
        head = re.sub(r"\s+", " ", body[:320])          # heading incl. wrapped lines
        k, l, d = section_keys(head, body)
        sec_info.append((s.report_id, s.sec_no, s.group, k, l, d, n["title"]))
    maps = []
    for _, it in I.iterrows():
        cands = [x for x in sec_info if x[0] == it.report_id]
        hit, how = None, "no_narrative"
        if it.tax_type in ("BSMV", "MTV", "ÖİV"):
            how = "no_narrative_tax_not_covered"
        elif it.sub_table == "main":
            ak = item_art_key(it.legal_ref)
            pool = [x for x in cands if x[2] == GROUP.get(it.tax_type)]
            if it.report_id == "VHR2017":
                # the 2017 report narrates only new or amended provisions: require the exact sub-article in the heading
                ref = re.sub(r"^(mm|gm|em|m)", "", str(it.legal_ref))
                pool = [x for x in pool if ref and ref in re.sub(r"\s+", "", x[6].lower()).replace("–", "-")]
            if ak:
                hit = next((x for x in pool if ak in x[3]), None)
                if hit is None and "/" in ak[1]:
                    hit = next((x for x in pool if (ak[0], ak[1].split("/")[0]) in x[3]), None)
                how = "article" if hit else how
            if hit is None and it.tax_type == "ÖTV":
                dec = re.findall(r"(\d{4}/\d{3,5})", f"{it.article} {it.description}")
                hit = next((x for x in pool if set(dec) & x[5]), None)
                how = "decree" if hit else how
        else:
            law = re.match(r"law(\d+)_", str(it.legal_ref))
            if law:
                L = law.group(1)
                hit = next((x for x in cands if x[2] == "DIGER" and L in x[4]), None) or \
                      next((x for x in cands if L in x[4] and x[2] == GROUP.get(it.tax_type)), None)
                how = "law" if hit else how
        if hit is None and how.startswith("no_narrative") and it.tax_type not in ("BSMV", "MTV", "ÖİV") and it.sub_table == "main":
            # fallback: description similar to a section title of the same group (or the other-laws chapter)
            grp = [x for x in cands if x[2] == GROUP.get(it.tax_type)]
            desc = str(it.description).lower()
            best = max(grp, key=lambda x: difflib.SequenceMatcher(None, desc, x[6].lower()[:len(desc) + 20]).ratio(), default=None)
            if best is not None and difflib.SequenceMatcher(None, desc, best[6].lower()[:len(desc) + 20]).ratio() >= 0.7:
                hit, how = best, "title_similarity"
        maps.append(dict(report_id=it.report_id, item_id=it.item_id, row_no=it.row_no, tax_type=it.tax_type,
                         sub_table=it.sub_table, legal_ref=it.legal_ref, description=str(it.description)[:120],
                         sec_no=hit[1] if hit else None, map_method=how))
    M = pd.DataFrame(maps)
    M.to_csv(CD / "item_section_map.csv", index=False)
    print("mapping:", M.map_method.value_counts().to_dict())
    print((M.sec_no.notna()).groupby([M.report_id]).mean().round(2).to_dict())

    # item-level narrative codes
    Sx = S.set_index(["report_id", "sec_no"])
    rows = []
    for _, m in M.iterrows():
        rec = m.to_dict()
        if m.sec_no is not None and isinstance(m.sec_no, str):
            s = Sx.loc[(m.report_id, m.sec_no)]
            rec["TE_status"] = s.TE_status
            for v in NARR:
                rec[v] = s[v]
                rec[v + "_page"] = s[v + "_page"]
            rec["narrative_note"] = "section " + m.sec_no
        else:
            rec["TE_status"] = "unknown"
            for v in NARR:
                rec[v] = "0"; rec[v + "_page"] = ""
            rec["narrative_note"] = m.map_method
        rows.append(rec)
    IC = pd.DataFrame(rows)

    # C3/C4 per item-year from the panel
    P = pd.read_csv(ROOT / "data" / "tax_expenditure_panel.csv")
    c3map = {"estimated": "2", "estimated_flagged": "1", "included_elsewhere": "1", "data_not_available": "0",
             "new_measure": "0", "blank": "0", "other_text": "0", "no_te_arising": "NA", "dash": "NA", "repealed": "NA"}
    P["C3"] = P.cell_status.fillna("blank").map(c3map)
    has_val = P.amount_thousand_try.notna()
    P["C4"] = "NA"
    est = P.C3.isin(["1", "2"]) & has_val
    P.loc[est & P.estimate_quality.notna(), "C4"] = "1"
    P.loc[est & P.estimate_quality.isna(), "C4"] = "0"
    key = ["report_id", "item_id"]
    Y = P.merge(IC.drop(columns=["row_no", "tax_type", "sub_table", "legal_ref", "description"]), on=key, how="left")
    Y.to_csv(CD / "item_year_codes.csv", index=False)
    # item-level (realisation-year) record
    R = Y[Y.estimate_type == "realisation"].copy()
    R.to_csv(CD / "item_codes.csv", index=False)
    print("item-year rows:", len(Y), "| item rows (realisation year):", len(R))
    print(pd.crosstab(R.report_id, R.C3))


if __name__ == "__main__":
    main()
