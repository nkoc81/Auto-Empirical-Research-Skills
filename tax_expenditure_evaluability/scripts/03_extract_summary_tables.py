"""Extract the aggregate summary tables printed in the body of each report.

Tables captured (names vary by report):
  budget_law   - "... Merkezi Yönetim Bütçe Kanununa Eklenen Vergi Harcaması Tahminleri" (million TL)
  amount       - "... Vergi Harcaması (Gerçekleşmesi ve) Tahminleri (Milyon TL)"
  pct_gdp      - "... Tahminlerinin GSYH'ye Oranı (%)"
  pct_taxrev   - "... Tahminlerinin (Genel Bütçe) Vergi Gelirlerine Oranı (%)"
  same_tax     - "... Aynı Vergi Türünden Tahsilata Oranı" (TE amount, collection, ratio)
These are the official aggregate figures; they are used for TE/GDP and TE/tax-revenue ratios instead of
recomputing denominators. Source: pdftotext -layout output (data/text), page = form-feed count + 1.
Output: data/interim/report_summary_tables.csv
"""
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "data" / "text"
FILES = {
    "VHR2016": "Vergi-Harcamalar_-Raporu-2016-.txt", "VHR2017": "Vergi-Harcamalar_-Raporu-2017.txt",
    "VHR2018": "Vergi-Harcamalar_-Raporu-2018.txt", "VHR2020": "VHR_2020.txt", "VHR2021": "VHR_2021.txt",
    "VHR2022": "VHR_2022.txt", "VHR2023": "VHR_2023.txt", "VHR2024": "VHR_2024.txt", "VHR2025": "VHR_2025.txt",
}
FIX = {"Ġ": "İ", "Ģ": "Ş", "‟": "’"}
NUM = re.compile(r"^-?\d{1,3}(?:\.\d{3})*(?:,\d+)?$|^-?\d+(?:,\d+)?$")


def kind_of(caption):
    c = caption.lower()
    if "aynı vergi" in c:
        return "same_tax"
    if "bütçe kanununa eklenen" in c:
        return "budget_law"
    if "gsyh" in c:
        return "pct_gdp"
    if "vergi gelirlerine" in c:
        return "pct_taxrev"
    if "giderlerine" in c:
        return "pct_expenditure"
    if "kalem" in c:
        return "item_count"
    if "tahmin" in c or "gerçekleş" in c:
        return "amount"
    return None


def to_num(s):
    return float(s.replace(".", "").replace(",", "."))


def label_norm(lab):
    l = lab.upper().replace("İ", "I").replace("Ş", "S").replace("Ğ", "G").replace("Ü", "U").replace("Ö", "O").replace("Ç", "C")
    for key, out in [("GENEL TOPLAM", "TOTAL"), ("TOPLAM", "TOTAL"), ("GELIR VERG", "GV"), ("KURUMLAR", "KV"),
                     ("KATMA", "KDV"), ("OZEL TUKETIM", "OTV"), ("DIGER", "OTHER_LAWS"), ("MOTORLU", "MTV"),
                     ("BANKA", "BSMV"), ("OZEL ILETISIM", "OIV")]:
        if key in l:
            return out
    return None


def parse(rid, fname):
    raw = (T / fname).read_text(encoding="utf-8", errors="replace")
    for a, b in FIX.items():
        raw = raw.replace(a, b)
    pages = raw.split("\f")
    lines = []
    for p, txt in enumerate(pages, start=1):
        for ln in txt.split("\n"):
            lines.append((p, ln))
    out = []
    i = 0
    while i < len(lines):
        p, ln = lines[i]
        m = re.match(r"\s*Tablo\s*(\d+)[\s:.]+(\d+)?[\s:.]*(.*)", ln)
        # skip table of contents (dotted leaders)
        if m and "....." not in ln and re.search(r"Vergi Harcama", ln + lines[min(i + 1, len(lines) - 1)][1]):
            cap = ln.strip() + " " + lines[i + 1][1].strip()
            k = kind_of(cap)
            if k is None:
                i += 1
                continue
            years, pending, j = None, None, i + 1
            while j < min(i + 40, len(lines)):
                pj, lj = lines[j]
                toks = lj.split()
                ys = [t for t in toks if re.fullmatch(r"20\d\d", t)]
                if years is None and len(ys) >= 2:
                    years = [int(y) for y in ys]
                    j += 1
                    continue
                nums = [t for t in toks if NUM.match(t)]
                labtoks = [t for t in toks if not NUM.match(t)]
                if years is not None and nums and (labtoks or pending):
                    lab = " ".join(labtoks) if labtoks else pending
                    if pending and labtoks and label_norm(lab) is None:
                        lab = pending + " " + lab
                    code = label_norm(lab)
                    if code:
                        vals = [to_num(t) for t in nums]
                        if k == "same_tax":
                            cols = ["te_amount", "collection", "ratio_pct"][: len(vals)]
                            for c, v in zip(cols, vals):
                                out.append(dict(report_id=rid, table_kind=k, caption=cap, page=pj, line=code,
                                                fiscal_year=years[0] if years else None, column=c, value=v))
                        else:
                            for y, v in zip(years, vals[-len(years):] if len(vals) >= len(years) else vals):
                                out.append(dict(report_id=rid, table_kind=k, caption=cap, page=pj, line=code,
                                                fiscal_year=y, column="value", value=v))
                    pending = None
                    if code == "TOTAL":
                        break
                elif years is not None and labtoks and not nums:
                    pending = (pending + " " if pending else "") + " ".join(labtoks)
                j += 1
            i = j
        i += 1
    return out


def main():
    rows = []
    for rid, f in FILES.items():
        rows += parse(rid, f)
    D = pd.DataFrame(rows)
    D["table_no"] = D.caption.str.extract(r"Tablo\s*(\d+(?:\s*\d+)?)")[0].str.replace(r"\s+", ".", regex=True).radd("Tablo ")
    # the 2016 report prints two series: the old budget-annex series (Tablo 4.4-4.8, 2007 methodology
    # scaled by nominal aggregates) and the 'new determination' (Tablo 4.9-4.14) on which its annex is based
    # 'same_tax' tables have a different layout (two-line headers); not needed for the analysis -> dropped
    D = D[D.table_kind != "same_tax"].copy()
    D["series"] = "report_basis"
    old = (D.report_id == "VHR2016") & ~D.caption.str.contains("Yeni Belirlemeye|Yılı Vergi Harcaması Gerçek")
    D.loc[old, "series"] = "old_budget_annex_basis"
    # same_tax tables have no year header with >=2 years: take year from caption
    st = D.table_kind == "same_tax"
    D.loc[st, "fiscal_year"] = D.loc[st, "caption"].str.extract(r"(20\d\d) Yılı")[0].astype(float)
    D.to_csv(ROOT / "data" / "interim" / "report_summary_tables.csv", index=False)
    print(D.groupby(["report_id", "table_kind"]).size().unstack(fill_value=0))
    print(D[(D.line == "TOTAL") & (D.column != "collection")].pivot_table(
        index=["report_id", "table_kind"], columns="fiscal_year", values="value", aggfunc="first"))


if __name__ == "__main__":
    main()
