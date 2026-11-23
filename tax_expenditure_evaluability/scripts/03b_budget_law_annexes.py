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
    print(s, "years", years, "-> identical to report tables:", dup or "none (no report reproduces this vintage)")
