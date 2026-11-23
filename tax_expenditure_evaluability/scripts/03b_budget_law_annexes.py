"""Check the budget-law tax expenditure annexes (2019 and 2020 budget laws) and compare them with the reports.

Input: data/interim/budget_law_annexes.csv. The two annexes were published as scanned images in the Official Gazette;
the values were transcribed by OCR plus visual checking (see the 'transcription' column).
Checks:
  1. row sums vs printed TOTAL for every year;
  2. comparison, line by line, with every report table (budget_law and amount tables) that gives the same fiscal year.
     A budget-law figure that equals a report figure for the same fiscal year (to the report's rounding of million TL)
     is the same estimate from the same vintage, reproduced twice, and must not be counted as an independent observation.
Output: outputs/tables/budget_law_annex_checks.csv, outputs/tables/budget_law_annex_comparison.csv
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "tables"
B = pd.read_csv(ROOT / "data" / "interim" / "budget_law_annexes.csv")
B["value_million"] = B.value_try / 1e6

chk = []
for (s, y), g in B.groupby(["source_id", "fiscal_year"]):
    parts = g[g.line != "TOTAL"].value_try.sum()
    tot = int(g[g.line == "TOTAL"].value_try.iloc[0])
    chk.append(dict(source_id=s, fiscal_year=y, sum_of_rows_try=int(parts), printed_total_try=tot, difference_try=int(parts - tot)))
C = pd.DataFrame(chk)
C.to_csv(OUT / "budget_law_annex_checks.csv", index=False)
print(C.to_string(index=False))

S = pd.read_csv(ROOT / "data" / "interim" / "report_summary_tables.csv")
S = S[(S.series == "report_basis") & (S.column == "value") & S.table_kind.isin(["budget_law", "amount"])]
rows = []
for _, b in B.iterrows():
    m = S[(S.fiscal_year == b.fiscal_year) & (S.line == b.line)]
    for _, s in m.iterrows():
        rows.append(dict(source_id=b.source_id, fiscal_year=b.fiscal_year, line=b.line, budget_law_million=round(b.value_million, 3),
                         report_id=s.report_id, report_table=s.table_no, report_table_kind=s.table_kind, report_value_million=s.value,
                         diff_million=round(b.value_million - s.value, 3)))
M = pd.DataFrame(rows)
M["same_estimate"] = M.diff_million.abs() <= 0.5          # equal at the report's rounding (million TL)
M.to_csv(OUT / "budget_law_annex_comparison.csv", index=False)
summ = M.groupby(["source_id", "fiscal_year", "report_id", "report_table_kind"]).same_estimate.all().unstack("report_table_kind")
print(summ.to_string())
for s in B.source_id.unique():
    years = sorted(B[B.source_id == s].fiscal_year.unique())
    rep = M[(M.source_id == s)].groupby("report_id").same_estimate.all()
    dup = list(rep[rep].index)
    print(s, "years", years, "-> identical to report tables:", dup or "none (these values appear in no report analysed)")

# ---- concept table for fiscal years 2019 and 2020 (each estimate named by its own document; totals, million TL)
S2 = pd.read_csv(ROOT / "data" / "interim" / "report_summary_tables.csv")
S2 = S2[(S2.series == "report_basis") & (S2.column == "value") & (S2.line == "TOTAL")]
def rep(rid, kind, y):
    v = S2[(S2.report_id == rid) & (S2.table_kind == kind) & (S2.fiscal_year == y)]
    return (float(v.value.iloc[0]), v.table_no.iloc[0], int(v.page.iloc[0])) if len(v) else (None, "", None)
def law(src, y):
    v = B[(B.source_id == src) & (B.fiscal_year == y) & (B.line == "TOTAL")]
    return float(v.value_try.iloc[0]) / 1e6
rows = []
for y, items in {
    2019: [("2018 report, projection (estimate made with 2017 data)", "VHR2018", "amount"),
           ("2018 report, table of amounts added to the 2019-2021 budget law", "VHR2018", "budget_law"),
           ("2019 budget law annex (Law 7156), budget estimate", "BL2019", None),
           ("2020 report, 'gerçekleşme' (realisation) estimate calculated from 2019 data", "VHR2020", "amount")],
    2020: [("2018 report, projection", "VHR2018", "amount"),
           ("2019 budget law annex, second-year estimate", "BL2019", None),
           ("2020 budget law annex (Law 7197), budget estimate", "BL2020", None),
           ("2020 report, projection (estimate made with 2019 data)", "VHR2020", "amount"),
           ("2021 report, 'gerçekleşme' (realisation) estimate calculated from 2020 data", "VHR2021", "amount")]}.items():
    for label, src, kind in items:
        if kind is None:
            val, where = law(src, y), "Official Gazette p. 1973 (PDF p. 45)" if src == "BL2019" else "Official Gazette p. 1973 (PDF p. 44)"
        else:
            val, tab, pg = rep(src, kind, y); where = f"{tab}, PDF p. {pg}"
        rows.append(dict(fiscal_year=y, estimate=label, document=src, location=where, total_million_try=round(val, 3)))
K = pd.DataFrame(rows)
for y in (2019, 2020):
    blsrc = "BL2019" if y == 2019 else "BL2020"
    base = K[(K.fiscal_year == y) & (K.document == blsrc)].total_million_try.iloc[0]
    K.loc[K.fiscal_year == y, "pct_vs_budget_law_of_year"] = ((K[K.fiscal_year == y].total_million_try / base - 1) * 100).round(2)
K.to_csv(OUT / "budget_law_vs_report_estimates_2019_2020.csv", index=False)
print(K.to_string(index=False))
