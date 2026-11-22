"""Build the item-year panel from the extracted annex rows.

Unit: report x provision (annex row) x year. Each report lists one realisation year (year_0) and four
projection years (year_1..year_4). Items are linked across reports with a key built from tax type,
sub-table (own law vs other laws) and a normalised legal reference; when several rows share the same
legal reference, the description similarity decides the link. Links are a research construct: they are
recorded with a match method so that users can audit them.

Outputs: data/tax_expenditure_panel.csv (long, one row per report-item-year)
         data/interim/items_by_report.csv (one row per report-item)
"""
import difflib
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import tax_type, sub_table, load_rows  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
I = ROOT / "data" / "interim"
REPORT_META = pd.read_csv(ROOT / "data" / "source_inventory.csv").set_index("source_id")
REPORTS = ["VHR2016", "VHR2017", "VHR2018", "VHR2020", "VHR2021", "VHR2022", "VHR2023", "VHR2024", "VHR2025"]

ART_RE = re.compile(r"((?:Mükerrer|Mük\.?|Geçici|Geç\.?|Ek)?\s*(?:Madde|Md\.?)\s*[\w/\-–()\. ]{1,12})", re.I)
LAW_RE = re.compile(r"(\d{3,4})\s*(?:sayılı|s\.|Sayılı)")


def norm_txt(s):
    s = str(s or "").lower()
    s = s.replace("i̇", "i").replace("–", "-").replace("—", "-")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def legal_ref(article, description, sub):
    """Normalised legal reference. For own-law rows: article number pattern found in the article cell
    (falls back to the description, because the 2022 rotated pages sometimes mix the two cells).
    For other-law rows: law number + article if present."""
    a = re.sub(r"\s*([/\-–])\s*", r"\1", str(article or ""))     # '4/  1-b' -> '4/1-b'
    d = str(description or "")
    txt = a if re.search(r"\d", a) else a + " " + d
    if sub == "other":
        law = LAW_RE.search(a) or LAW_RE.search(d)
        art = re.search(r"(?:Madde|Md\.?|Mad\.)\s*([\w/\-–\.]+)", a + " " + d, re.I)
        geç = "gm" if re.search(r"Geçici|Geç\.", a, re.I) else ("em" if re.search(r"\bEk\b", a) else "m")
        return "law%s_%s%s" % (law.group(1) if law else "?", geç, art.group(1).lower() if art else "?")
    pre_m = re.search(r"(Mükerrer|Mük\.|Geçici|Geç\.)", txt, re.I)
    pre = {"mük": "mm", "geç": "gm"}.get(pre_m.group(1).lower()[:3], "m") if pre_m else "m"
    # 1) 'Madde 29/c', 'Geçici Madde 39'; 2) a slash token such as '29/c' (word order on some rotated
    #    pages is scrambled, separating 'Madde' from its number); 3) give up (unlinked by reference)
    m = re.search(r"(?:Madde|Md\.?)\s*(\d+(?:\s*[/\-–]\s*[\w\-]+)*)", txt, re.I) or \
        re.search(r"\b(\d{1,3}(?:/[\wçğıöşü\-]+)+)", txt) or re.match(r"\s*(\d{1,3}(?:-[\wçğıöşü]+)?)\b", a)
    if not m:
        return "?" + norm_txt(a)[:20]
    num = re.sub(r"\s+", "", m.group(1)).replace("–", "-").lower()
    return pre + num


def law_conflict(a, b):
    """True when both references name a law number and the numbers differ."""
    la, lb = re.match(r"law(\d+)_", a or ""), re.match(r"law(\d+)_", b or "")
    return bool(la and lb and la.group(1) != lb.group(1))


def main():
    rows = []
    for rid in REPORTS:
        r = load_rows(rid)
        r["report_id"] = rid
        r["tax_type"] = [tax_type(a, b) for a, b in zip(r.table, r.section)]
        r["sub_table"] = [sub_table(b) for b in r.section]
        rows.append(r)
    R = pd.concat(rows, ignore_index=True)
    R["legal_ref"] = [legal_ref(a, d, s) for a, d, s in zip(R.article, R.description, R.sub_table)]
    R["desc_norm"] = R.description.map(norm_txt)
    R["item_seq"] = R.groupby(["report_id", "tax_type", "sub_table"]).cumcount() + 1

    # link items across consecutive reports (in report order) by key + description similarity
    item_id, method = {}, {}
    next_id = 1
    prev = None
    for rid in REPORTS:
        cur = R[R.report_id == rid]
        used = set()
        for idx, row in cur.iterrows():
            best, best_s, how = None, 0.0, None
            if prev is not None:
                cand = prev[(prev.tax_type == row.tax_type) & (prev.sub_table == row.sub_table)]
                same = cand[cand.legal_ref == row.legal_ref]
                pool = same if len(same) else cand
                for jdx, c in pool.iterrows():
                    if jdx in used:
                        continue
                    s = difflib.SequenceMatcher(None, row.desc_norm, c.desc_norm).ratio()
                    if len(same):
                        s += 0.5          # same legal reference
                    if s > best_s:
                        best, best_s = jdx, s
                if best is not None and len(same) and best_s >= 0.5 + 0.35:
                    how = "legal_ref+description"
                elif best is not None and len(same) and len(same) == 1:
                    how = "legal_ref_only"
                elif best is not None and not len(same) and best_s >= 0.80 and \
                        (best_s >= 0.90 or not law_conflict(row.legal_ref, prev.loc[best, "legal_ref"])):
                    how = "description_only"
                else:
                    best = None
            if best is not None:
                item_id[idx] = item_id[best]; method[idx] = how; used.add(best)
            else:
                item_id[idx] = "TE%04d" % next_id; method[idx] = "new_id"; next_id += 1
        prev = cur
    R["item_id"] = pd.Series(item_id)
    R["link_method"] = pd.Series(method)
    R.to_csv(I / "items_by_report.csv", index=False)

    # long panel
    recs = []
    for _, r in R.iterrows():
        meta = REPORT_META.loc[r.report_id]
        for j in range(5):
            recs.append({
                "report_id": r.report_id, "report_publication_year": int(meta.publication_year),
                "item_id": r.item_id, "link_method": r.link_method,
                "tax_type": r.tax_type, "sub_table": r.sub_table, "annex_table": r.table, "section": r.section,
                "row_no": r.row_no, "legal_ref": r.legal_ref, "article_raw": r.article, "description": r.description,
                "fiscal_year": int(r[f"year_{j}"]),
                "estimate_type": "realisation" if j == 0 else "projection",
                "amount_thousand_try": r[f"value_{j}"], "cell_status": r[f"status_{j}"], "cell_raw": r[f"raw_{j}"],
                "estimate_quality_raw": r.quality if isinstance(r.quality, str) else None,
                "estimate_quality": r.quality_norm, "fix_note": r.fix_note,
                "source_page_pdf": r.page, "source_url": meta.url, "local_file": meta.local_path,
            })
    P = pd.DataFrame(recs)
    P.to_csv(ROOT / "data" / "tax_expenditure_panel.csv", index=False)
    print("report-items:", len(R), "items (linked ids):", R.item_id.nunique(), "panel rows:", len(P))
    print(R.groupby("report_id").agg(n=("item_id", "size"), new=("link_method", lambda s: (s == "new_id").sum())))


if __name__ == "__main__":
    main()
