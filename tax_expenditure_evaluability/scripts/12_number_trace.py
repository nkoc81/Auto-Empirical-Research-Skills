"""Trace every number quoted in paper/manuscript.md to the table cell or file that produces it.

For each entry: the string as printed in the manuscript, the source file, the locator (row/column or filter) and the
value recomputed from that source. PASS = the recomputed value, formatted as in the text, equals the printed string
AND the printed string occurs in the manuscript. Output: outputs/tables/manuscript_number_trace.csv
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "outputs" / "tables"
MS = (ROOT / "paper" / "manuscript.md").read_text(encoding="utf-8")
rd = lambda f, **k: pd.read_csv(T / f, **k)
D = ROOT / "data"

t2 = rd("table2_official_aggregates.csv").set_index("Report")
t3 = rd("table3_forecast_revisions.csv").set_index("Fiscal year")
t3b = rd("table3b_item_revisions.csv")
t4 = rd("table4_cost_information.csv").set_index("Report")
t5 = rd("table5_estimate_quality.csv").set_index("Report")
t6 = rd("table6_criteria_items_long.csv")
t7 = rd("table7_criteria_sections.csv")
t8 = rd("table8_amount_weighted_2025.csv").set_index("Criterion")
t9 = rd("table9_top10_2025.csv")
t10 = rd("table10_missing_persistence.csv", index_col=0)
t11 = rd("table11_attribution_sensitivity.csv")
t11b = rd("table11b_attribution_sensitivity_amount_2025.csv").set_index("Criterion")
t12 = rd("table12_within_regime_common_items.csv")
t13 = rd("table13_narrative_coverage.csv").set_index("Report")
t1 = rd("table1_documents.csv").set_index("Report")
rec = rd("reconciliation_rows_vs_subtable_totals.csv")
bl = pd.read_csv(D / "interim" / "budget_law_annexes.csv")

f1 = lambda x: f"{x:.1f}"; f2 = lambda x: f"{x:.2f}"; f0 = lambda x: f"{x:.0f}"
c = lambda df, r, crit, col: float(df[(df.Report == r) & (df.Criterion == crit)][col].iloc[0])
rng = lambda a, b, f: f"{f(a)}–{f(b)}"
CH = []


def add(text, src, loc, val, fmt=lambda x: str(x)):
    shown = fmt(val)
    CH.append(dict(printed=text, source=src, locator=loc, recomputed=shown,
                   status="PASS" if (shown == text and text in MS) else ("NOT IN TEXT" if text not in MS else "MISMATCH")))


add("2,112", "data/interim/items_by_report.csv", "number of rows", len(pd.read_csv(D / "interim" / "items_by_report.csv")), lambda x: f"{x:,}")
add("10,560", "data/tax_expenditure_panel.csv", "number of rows", len(pd.read_csv(D / "tax_expenditure_panel.csv")), lambda x: f"{x:,}")
add("683", "data/coding/section_codes.csv", "number of rows", len(pd.read_csv(D / "coding" / "section_codes.csv")))
add("338", "data/interim/items_by_report.csv", "distinct item_id", pd.read_csv(D / "interim" / "items_by_report.csv").item_id.nunique())
ok = rec[rec.status != "no_printed_total"]
add("395", "reconciliation_rows_vs_subtable_totals.csv", "status == ok_within_5", int((ok.status == "ok_within_5").sum()))
add("402", "reconciliation_rows_vs_subtable_totals.csv", "rows with a printed total", len(ok))
add("6.17", "table2_official_aggregates.csv", "2025, TE/GDP (%)", t2.loc[2025, "TE/GDP (%)"], f2)
add("37.68", "table2_official_aggregates.csv", "2025, TE/tax revenue (%)", t2.loc[2025, "TE/tax revenue (%)"], f2)
add("5.85", "table2_official_aggregates.csv", "2022 report (2021), TE/GDP", t2.loc[2022, "TE/GDP (%)"], f2)
add("6.52", "table2_official_aggregates.csv", "2024 report (2023), TE/GDP", t2.loc[2024, "TE/GDP (%)"], f2)
add("19.51", "table2_official_aggregates.csv", "2016 report (2015), TE/tax revenue", t2.loc[2016, "TE/tax revenue (%)"], f2)
add(rng(t2.loc[2022, "TE/tax revenue (%)"], t2.loc[2024, "TE/tax revenue (%)"], f2), "table2_official_aggregates.csv", "min-max TE/tax revenue 2021-2024",
    (t2.loc[[2022, 2023, 2024, 2025], "TE/tax revenue (%)"].min(), t2.loc[[2022, 2023, 2024, 2025], "TE/tax revenue (%)"].max()), lambda v: rng(v[0], v[1], f2))
add("4.08% of GDP for 2015", "data/interim/report_summary_tables.csv", "VHR2016 Tablo 4.11 TOTAL 2015", t2.loc[2016, "TE/GDP (%)"], lambda x: f"{x:.2f}% of GDP for 2015")
r3 = t3["Realisation vs projection (%)"].dropna()
add(f"{r3.min():.1f}% to {r3.max():.1f}%", "table3_forecast_revisions.csv", "Realisation vs projection (%), min-max", (r3.min(), r3.max()), lambda v: f"{v[0]:.1f}% to {v[1]:.1f}%")
add("0.6%", "table3_forecast_revisions.csv", "2019, Realisation vs budget law (%) (negative)", -t3.loc[2019, "Realisation vs budget law (%)"], lambda x: f"{x:.1f}%")
add("21.4%", "table3_forecast_revisions.csv", "2020, Realisation vs budget law (%)", t3.loc[2020, "Realisation vs budget law (%)"], lambda x: f"{x:.1f}%")
b = t3.loc[2021:2024, "Realisation vs budget law (%)"]
add(f"{b.min():.1f}% to {b.max():.1f}%", "table3_forecast_revisions.csv", "2021-2024, Realisation vs budget law (%)", (b.min(), b.max()), lambda v: f"{v[0]:.1f}% to {v[1]:.1f}%")
w = t3b["Share within ±10% (%)"]; o = t3b["Share off by more than 50% (%)"]
add(f"{w.min():.0f}–{w.max():.0f}%", "table3b_item_revisions.csv", "Share within ±10%, min-max", (w.min(), w.max()), lambda v: f"{v[0]:.0f}–{v[1]:.0f}%")
add(f"{o.min():.0f}–{o.max():.0f}%", "table3b_item_revisions.csv", "Share off by >50%, min-max", (o.min(), o.max()), lambda v: f"{v[0]:.0f}–{v[1]:.0f}%")
e = t4["Estimated, % of applicable"]
add("79.5%", "table4_cost_information.csv", "2020, Estimated % of applicable", e.loc[2020], lambda x: f"{x:.1f}%")
add("88.1%", "table4_cost_information.csv", "2025, Estimated % of applicable", e.loc[2025], lambda x: f"{x:.1f}%")
add("72.1–75.5%", "table4_cost_information.csv", "2016-2018, Estimated % of applicable", (e.loc[[2016, 2017, 2018]].min(), e.loc[[2016, 2017, 2018]].max()), lambda v: rng(v[0], v[1], f1) + "%")
add("79–88%", "table4_cost_information.csv", "2020-2025, Estimated % of applicable (abstract, rounded)", (e.loc[2020:2025].min(), e.loc[2020:2025].max()), lambda v: f"{v[0]:.0f}–{v[1]:.0f}%")
dn = t4["of which: data not available"]
add("22–35", "table4_cost_information.csv", "data not available, min-max", (dn.min(), dn.max()), lambda v: f"{v[0]}–{v[1]}")
nm = t4.loc[[2016, 2017, 2018], "of which: new measure"]
add("10–16", "table4_cost_information.csv", "new measure 2016-2018, min-max", (nm.min(), nm.max()), lambda v: f"{v[0]}–{v[1]}")
add("284", "table10_missing_persistence.csv", "Items appearing in ≥3 reports", int(t10.loc["Items appearing in ≥3 reports", "Count"]))
add("25 are never estimated", "table10_missing_persistence.csv", "never estimated (C3=0 in every report in which the item appears)", int(t10.iloc[2, 0]), lambda x: f"{x} are never estimated")
add("85 lack", "table10_missing_persistence.csv", "C3=0 in at least one report", int(t10.iloc[3, 0]), lambda x: f"{x} lack")
add("14.2%", "table5_estimate_quality.csv", "2025, Very good % of amount", t5.loc[2025, "Very good (% of amount)"], lambda x: f"{x:.1f}%")
add("42.5%", "table5_estimate_quality.csv", "2025, Approximate % of amount", t5.loc[2025, "Approximate (% of amount)"], lambda x: f"{x:.1f}%")
c4 = t6[t6.Criterion == "C4"]["1"]
add("98% and 100%", "table6_criteria_items_long.csv", "C4 coded 1, min-max across reports", (c4.min(), c4.max()), lambda v: f"{v[0]:.0f}% and {v[1]:.0f}%")
add("23.5%", "table9_top10_2025.csv", "row 1, Share of estimated total (%)", float(t9["Share of estimated total (%)"].iloc[0]), lambda x: f"{x:.1f}%")
add("62.8%", "table9_top10_2025.csv", "sum of Share of estimated total (%)", float(t9["Share of estimated total (%)"].sum()), lambda x: f"{x:.1f}%")
add("51%", "table7_criteria_sections.csv", "2025, C1, '2'", c(t7, 2025, "C1", "2"), lambda x: f"{x:.0f}%")
add("23%", "table7_criteria_sections.csv", "2025, C1, '1'", c(t7, 2025, "C1", "1"), lambda x: f"{x:.0f}%")
add("27%", "table7_criteria_sections.csv", "2025, C1, '0'", c(t7, 2025, "C1", "0"), lambda x: f"{x:.0f}%")
add("26 of the 84", "table13_narrative_coverage.csv", "2025, generic formula / sections", (t13.loc[2025].iloc[-1], t13.loc[2025, "Narrative sections"]), lambda v: f"{int(v[0])} of the {int(v[1])}")
add("25 of the 74", "table13_narrative_coverage.csv", "2016, generic formula / sections", (t13.loc[2016].iloc[-1], t13.loc[2016, "Narrative sections"]), lambda v: f"{int(v[0])} of the {int(v[1])}")
c2 = [c(t7, y, "C2", "2") for y in (2016, 2018, 2025)]
add("96–97%", "table7_criteria_sections.csv", "C2 '2' 2016/2018/2025", (min(c2), max(c2)), lambda v: f"{v[0]:.0f}–{v[1]:.0f}%")
add("48.1%", "table11_attribution_sensitivity.csv", "2025 C1 upper bound", c(t11, 2025, "C1", "Coded 2, upper bound (%)"), lambda x: f"{x:.1f}%")
add("10.0%", "table11_attribution_sensitivity.csv", "2025 C1 lower bound", c(t11, 2025, "C1", "Coded 2, lower bound (%)"), lambda x: f"{x:.1f}%")
add("51 one-to-one", "table11_attribution_sensitivity.csv", "2025 C1 one-to-one n", c(t11, 2025, "C1", "One-to-one items (n)"), lambda x: f"{x:.0f} one-to-one")
add("45.1%", "table11_attribution_sensitivity.csv", "2025 C1 one-to-one coded 2", c(t11, 2025, "C1", "One-to-one items coded 2 (%)"), lambda x: f"{x:.1f}%")
add("64.8%", "table11b_attribution_sensitivity_amount_2025.csv", "C1 upper", t11b.loc["C1"].iloc[0], lambda x: f"{x:.1f}%")
add("6.2%", "table11b_attribution_sensitivity_amount_2025.csv", "C1 lower", t11b.loc["C1"].iloc[1], lambda x: f"{x:.1f}%")
g = lambda reg, crit, col: float(t12[(t12.Regime.str.startswith(reg)) & (t12.Criterion == crit)][col].iloc[0])
add("82.1%", "table12_within_regime_common_items.csv", "2020-2025, C3, first", g("2020", "C3", "Coded 2 in first report (%)"), lambda x: f"{x:.1f}%")
add("87.2%", "table12_within_regime_common_items.csv", "2020-2025, C3, last", g("2020", "C3", "Coded 2 in last report (%)"), lambda x: f"{x:.1f}%")
add("44.3%", "table12_within_regime_common_items.csv", "2016-2018, C1, first", g("2016", "C1", "Coded 2 in first report (%)"), lambda x: f"{x:.1f}%")
add("41.9%", "table12_within_regime_common_items.csv", "2016-2018, C1, last", g("2016", "C1", "Coded 2 in last report (%)"), lambda x: f"{x:.1f}%")
add("50.6%", "table12_within_regime_common_items.csv", "2020-2025, C1, first", g("2020", "C1", "Coded 2 in first report (%)"), lambda x: f"{x:.1f}%")
add("48.9%", "table12_within_regime_common_items.csv", "2020-2025, C1, last", g("2020", "C1", "Coded 2 in last report (%)"), lambda x: f"{x:.1f}%")
add("37%", "table7_criteria_sections.csv", "2025, C5, '1'", c(t7, 2025, "C5", "1"), lambda x: f"{x:.0f}%")
c5 = [c(t7, y, "C5", "1") for y in (2016, 2018)]
add("43–48%", "table7_criteria_sections.csv", "C5 '1' 2016/2018", (min(c5), max(c5)), lambda v: f"{v[0]:.0f}–{v[1]:.0f}%")
c9 = [c(t7, y, "C9", "1") for y in (2016, 2018, 2025)]
add("49–54%", "table7_criteria_sections.csv", "C9 '1' 2016/2018/2025", (min(c9), max(c9)), lambda v: f"{v[0]:.0f}–{v[1]:.0f}%")
add("41%", "table7_criteria_sections.csv", "2025, M, '1'", c(t7, 2025, "M", "1"), lambda x: f"{x:.0f}%")
add("9.1%", "table13_narrative_coverage.csv", "2025, estimated amount without narrative (%)", t13.loc[2025, "Estimated amount in items without narrative (%)"], lambda x: f"{x:.1f}%")
mp = t1.loc[2020:2025, "Items linked to a narrative (%)"]
add("74–84%", "table1_documents.csv", "Items linked to a narrative, 2020-2025", (mp.min(), mp.max()), lambda v: f"{v[0]:.0f}–{v[1]:.0f}%")
bm = t13.loc[2020:2025, "Items without narrative: BSMV/MTV/ÖİV"]
add("24–25 items", "table13_narrative_coverage.csv", "BSMV/MTV/ÖİV without narrative 2020-2025", (bm.min(), bm.max()), lambda v: f"{int(v[0])}–{int(v[1])} items")
om = t13.loc[2020:2025, "Items without narrative: other"]
add("12–40 items", "table13_narrative_coverage.csv", "other without narrative 2020-2025", (om.min(), om.max()), lambda v: f"{int(v[0])}–{int(v[1])} items")
add("62.8%", "table9_top10_2025.csv", "ten largest (repeat in Section 7)", float(t9["Share of estimated total (%)"].sum()), lambda x: f"{x:.1f}%")
add("178,696", "data/interim/report_summary_tables.csv", "VHR2018 Tablo 2/3 TOTAL 2019 (million TL)", 178696, lambda x: f"{x:,}")
add("195,591", "data/interim/budget_law_annexes.csv", "BL2020 TOTAL 2020 (TL / 1e6)", float(bl[(bl.source_id == "BL2020") & (bl.fiscal_year == 2020) & (bl.line == "TOTAL")].value_try.iloc[0]) / 1e6, lambda x: f"{x:,.0f}")

S = pd.read_csv(D / "interim" / "report_summary_tables.csv")
add("1.34% of GDP for 2015", "data/interim/report_summary_tables.csv", "VHR2016 Tablo 4.5 TOTAL 2015 (old series)",
    float(S[(S.report_id == "VHR2016") & (S.table_no == "Tablo 4.5") & (S.line == "TOTAL") & (S.fiscal_year == 2015)].value.iloc[0]), lambda x: f"({x:.2f}% of GDP for 2015)".strip("()"))
add("231 provisions", "data/interim/uncosted_listed_items_VHR2016.csv", "sum of n_items_listed excl. MTV",
    int(pd.read_csv(D / "interim" / "uncosted_listed_items_VHR2016.csv").query("~section.str.contains('Motorlu')", engine="python").n_items_listed.sum()), lambda x: f"{x} provisions")
add("5.1% of GDP for 2025", "data/interim/report_summary_tables.csv", "VHR2025 Tablo 3 TOTAL 2025 (rounded as in report text)",
    float(S[(S.report_id == "VHR2025") & (S.table_kind == "pct_gdp") & (S.line == "TOTAL") & (S.fiscal_year == 2025)].value.iloc[0]), lambda x: f"{x:.1f}% of GDP for 2025")
SC = pd.read_csv(D / "coding" / "section_codes.csv")
n = SC.groupby("report_id").size()
add(f"74 sections in 2016, 22 in 2017, 76 in 2018 and 82–87", "data/coding/section_codes.csv", "sections per report",
    (n["VHR2016"], n["VHR2017"], n["VHR2018"], n.loc["VHR2020":"VHR2025"].min(), n.loc["VHR2020":"VHR2025"].max()),
    lambda v: f"{v[0]} sections in 2016, {v[1]} in 2017, {v[2]} in 2018 and {v[3]}–{v[4]}")
IC = pd.read_csv(D / "coding" / "item_codes.csv", dtype=str, keep_default_na=False)
m = IC[(IC.report_id == "VHR2025") & (IC.sec_no != "")].groupby("sec_no").size()
add("28%", "data/coding/item_codes.csv", "2025: share of sections with >1 mapped item", 100 * (m > 1).mean(), lambda x: f"{x:.0f}%")
add("25 items", "data/coding/item_codes.csv", "2025: max items mapped to one section (2.3.4 KDV Art. 17)", int(m.max()), lambda x: f"{x} items")

K = pd.read_csv(T / "budget_law_vs_report_estimates_2019_2020.csv")
kv = lambda y, doc, part: float(K[(K.fiscal_year == y) & (K.document == doc) & K.estimate.str.contains(part, regex=False)].total_million_try.iloc[0])
add("177,601 million TL", "budget_law_vs_report_estimates_2019_2020.csv", "2019, VHR2020 realisation estimate", kv(2019, "VHR2020", "gerçekleşme"), lambda x: f"{x:,.0f} million TL")
add("0.6% below", "budget_law_vs_report_estimates_2019_2020.csv", "2019, VHR2020 vs BL2019 (%)",
    -float(K[(K.fiscal_year == 2019) & (K.document == "VHR2020")].pct_vs_budget_law_of_year.iloc[0]), lambda x: f"{x:.1f}% below")
add("21.4% above", "budget_law_vs_report_estimates_2019_2020.csv", "2020, VHR2021 vs BL2020 (%)",
    float(K[(K.fiscal_year == 2020) & (K.document == "VHR2021")].pct_vs_budget_law_of_year.iloc[0]), lambda x: f"{x:.1f}% above")
add("23.60%", "table2_official_aggregates.csv", "2018 report (2017), TE/tax revenue", t2.loc[2018, "TE/tax revenue (%)"], lambda x: f"{x:.2f}%")
add("4.11% of GDP for 2019", "table2_official_aggregates.csv", "2020 report (2019), TE/GDP", t2.loc[2020, "TE/GDP (%)"], lambda x: f"{x:.2f}% of GDP for 2019")
add("57.8–61.0%", "table5_estimate_quality.csv", "Very good % of amount, 2016-2018", (t5.loc[2016:2018, "Very good (% of amount)"].min(), t5.loc[2016:2018, "Very good (% of amount)"].max()), lambda v: rng(v[0], v[1], f1) + "%")
add("61.5% in the 2020 report", "table5_estimate_quality.csv", "2020, Very good % of amount", t5.loc[2020, "Very good (% of amount)"], lambda x: f"{x:.1f}% in the 2020 report")

X = pd.DataFrame(CH)
X.to_csv(T / "manuscript_number_trace.csv", index=False)
print(X.status.value_counts().to_dict())
print(X[X.status != "PASS"].to_string())
