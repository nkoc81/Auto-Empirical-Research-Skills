"""Reconciliation checks (all amounts in thousand TL unless stated).

1. Item rows vs the GENEL TOPLAM line of each annex sub-table (tax x own-law/other-law).
2. Annex totals by tax vs the aggregate table printed in the report body (million TL).
   Body lines: GV, KV, KDV, ÖTV (each = own law + 'other laws' sub-table of that annex) and
   'Diğer Kanunlar' (= BSMV + MTV + ÖİV, Annex I-5). The 2016 report prints BSMV, MTV, ÖİV separately.
Outputs: outputs/tables/reconciliation_rows_vs_subtable_totals.csv
         outputs/tables/reconciliation_annex_vs_body.csv
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import tax_type, sub_table, load_rows  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
I = ROOT / "data" / "interim"
OUT = ROOT / "outputs" / "tables"
OUT.mkdir(parents=True, exist_ok=True)
REPORTS = ["VHR2016", "VHR2017", "VHR2018", "VHR2020", "VHR2021", "VHR2022", "VHR2023", "VHR2024", "VHR2025"]
BODY_LINE = {"GV": "GV", "KV": "KV", "KDV": "KDV", "ÖTV": "OTV", "BSMV": "OTHER_LAWS", "MTV": "OTHER_LAWS",
             "ÖİV": "OTHER_LAWS", "DIGER": "OTHER_LAWS"}


def long(df, valname):
    recs = []
    for _, r in df.iterrows():
        for i in range(5):
            recs.append(dict(report_id=r.report_id, tax=r.tax, sub=r["sub"], fiscal_year=int(r[f"year_{i}"]),
                             col=i, **{valname: r[f"value_{i}"]}))
    return pd.DataFrame(recs)


def main():
    a_rows, a_tot = [], []
    for rid in REPORTS:
        r = load_rows(rid); t = pd.read_csv(I / f"annex_totals_{rid}.csv")
        for d in (r, t):
            d["report_id"] = rid
            d["tax"] = [tax_type(a, b) for a, b in zip(d.table, d.section)]
            d["sub"] = [sub_table(b) for b in d.section]
        a_rows.append(long(r, "rows_sum")); a_tot.append(long(t.groupby(["tax", "sub"]).first().reset_index(), "annex_total"))
    R = pd.concat(a_rows).groupby(["report_id", "tax", "sub", "fiscal_year", "col"], as_index=False).rows_sum.sum(min_count=1)
    T = pd.concat(a_tot)
    C = R.merge(T, how="outer", on=["report_id", "tax", "sub", "fiscal_year", "col"])
    C["diff"] = C.rows_sum - C.annex_total
    C["status"] = "no_printed_total"
    C.loc[C.annex_total.notna(), "status"] = "ok_within_5"
    C.loc[C.annex_total.notna() & (C["diff"].abs() > 5), "status"] = "residual"
    C.to_csv(OUT / "reconciliation_rows_vs_subtable_totals.csv", index=False)
    print(C.groupby(["report_id", "status"]).size().unstack(fill_value=0))
    print(C[C.status == "residual"].to_string())

    # 2. annex vs body; use printed sub-table totals where available, otherwise the row sum
    C["annex_value"] = C.annex_total.fillna(C.rows_sum)
    C["body_line"] = C.tax.map(BODY_LINE)
    S = pd.read_csv(I / "report_summary_tables.csv")
    S = S[(S.table_kind == "amount") & (S.series == "report_basis")]
    rows = []
    for rid in REPORTS:
        A = C[C.report_id == rid]
        B = S[S.report_id == rid]
        if rid == "VHR2016":     # body lists BSMV/MTV/ÖİV separately; other-law items are inside the main taxes
            A = A.assign(body_line=A.tax.map({"GV": "GV", "KV": "KV", "KDV": "KDV", "ÖTV": "OTV", "BSMV": "BSMV",
                                                "MTV": "MTV", "ÖİV": "OIV"}))
        agg = A.groupby(["body_line", "fiscal_year"]).annex_value.sum().div(1000).reset_index()
        tot = agg.groupby("fiscal_year").annex_value.sum().reset_index().assign(body_line="TOTAL")
        agg = pd.concat([agg, tot])
        m = agg.merge(B[["line", "fiscal_year", "value", "page"]].rename(columns={"line": "body_line", "value": "body_million"}),
                      how="outer", on=["body_line", "fiscal_year"])
        m["report_id"] = rid
        rows.append(m)
    M = pd.concat(rows)
    M["annex_million"] = M.annex_value
    M["diff_million"] = M.annex_million - M.body_million
    M["diff_pct"] = 100 * M.diff_million / M.body_million
    M = M[["report_id", "body_line", "fiscal_year", "annex_million", "body_million", "diff_million", "diff_pct", "page"]]
    M.to_csv(OUT / "reconciliation_annex_vs_body.csv", index=False)
    pd.set_option("display.width", 200)
    print(M[M.body_line == "TOTAL"].round(2).to_string())
    print("lines with |diff|>1 million TL:")
    print(M[M.diff_million.abs() > 1].round(2).to_string())


if __name__ == "__main__":
    main()
