"""Descriptive analysis: tables (outputs/tables) and figures (outputs/figures).

All quantities are descriptive statements about what the official reports contain. No effect or effectiveness
estimate is produced. Nominal TL amounts are not compared across years; ratios to GDP / tax revenue are the
reports' own published ratios. Amount-weighted shares use one report's realisation-year amounts only.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TB = ROOT / "outputs" / "tables"; FG = ROOT / "outputs" / "figures"
TB.mkdir(parents=True, exist_ok=True); FG.mkdir(parents=True, exist_ok=True)
ORDER = ["VHR2016", "VHR2017", "VHR2018", "VHR2020", "VHR2021", "VHR2022", "VHR2023", "VHR2024", "VHR2025"]
LAB = {r: r[3:] for r in ORDER}
INV = pd.read_csv(ROOT / "data" / "source_inventory.csv").set_index("source_id")
REAL = {r: int(INV.loc[r, "realisation_year"]) for r in ORDER}
CRIT = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"]
CNAME = {"C1": "Policy objective", "C2": "Beneficiaries defined", "C3": "Item-level cost estimate",
         "C4": "Estimate quality/uncertainty", "C5": "Expected outcome", "C6": "Indicator/outcome data",
         "C7": "Additionality/counterfactual", "C8": "Cost-effectiveness/alternatives", "C9": "Regular review/sunset"}
# palette (validated with the dataviz validator): ordinal blue for codes 2/1/0, neutral grey for NA
BLUE = {"2": "#184f95", "1": "#3987e5", "0": "#86b6ef"}; GREY = "#c9c7bf"; INK = "#2b2b2a"; MUTED = "#6b6a64"
CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
                     "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False, "font.family": "DejaVu Sans"})
MD = []


def md(title, df, note, floatfmt=None):
    MD.append(f"### {title}\n\n" + df.to_markdown(index=True, floatfmt=floatfmt or ".1f") + f"\n\n*Note:* {note}\n")


def save(df, name):
    df.to_csv(TB / name)


# ---------------------------------------------------------------- Table 1: documents
P = pd.read_csv(ROOT / "data" / "tax_expenditure_panel.csv")
S = pd.read_csv(ROOT / "data" / "coding" / "section_codes.csv", dtype=str, keep_default_na=False, na_values=[""])
IC = pd.read_csv(ROOT / "data" / "coding" / "item_codes.csv", dtype={c: str for c in CRIT + ["M", "B"]}, keep_default_na=False, na_values=[""])
IY = pd.read_csv(ROOT / "data" / "coding" / "item_year_codes.csv", dtype={"C3": str, "C4": str}, keep_default_na=False, na_values=[""])
t1 = pd.DataFrame({
    "Publisher": [("MoF" if r in ("VHR2016", "VHR2017") else "MoTF" if r == "VHR2018" else "RA (GİB)") for r in ORDER],
    "PDF date": [INV.loc[r, "pdf_creation_date"] for r in ORDER],
    "Pages": [int(INV.loc[r, "pages"]) for r in ORDER],
    "Realisation year": [REAL[r] for r in ORDER],
    "Projection years": [f"{REAL[r]+1}-{REAL[r]+4}" for r in ORDER],
    "Annex items": [int((P[P.estimate_type == 'realisation'].report_id == r).sum()) for r in ORDER],
    "Narrative sections": [int((S.report_id == r).sum()) for r in ORDER],
    "Items linked to a narrative (%)": [100 * IC[IC.report_id == r].sec_no.notna().mean() for r in ORDER],
}, index=[LAB[r] for r in ORDER]); t1.index.name = "Report"
save(t1, "table1_documents.csv")
md("Table 1. Official tax expenditure reports analysed", t1,
   "MoF = Ministry of Finance; MoTF = Ministry of Treasury and Finance; RA = Revenue Administration. The 2019 report "
   "could not be found, so 2018 has no realisation estimate. The 2017 report narrates only new provisions. "
   "Sources: data/source_inventory.csv, data/tax_expenditure_panel.csv, data/coding/section_codes.csv.")

# ---------------------------------------------------------------- Table 2 / Fig 1: official aggregates
ST = pd.read_csv(ROOT / "data" / "interim" / "report_summary_tables.csv")
ST = ST[(ST.series == "report_basis") & (ST.line == "TOTAL") & (ST.column == "value")]
rows = []
for r in ORDER:
    y = REAL[r]
    g = ST[(ST.report_id == r)]
    def val(kind, yy):
        v = g[(g.table_kind == kind) & (g.fiscal_year == yy)].value
        return float(v.iloc[0]) if len(v) else np.nan
    rows.append(dict(Report=LAB[r], **{"Realisation year": y, "TE (million TL)": val("amount", y),
                                       "TE/GDP (%)": val("pct_gdp", y), "TE/tax revenue (%)": val("pct_taxrev", y),
                                       "Report-year projection TE/GDP (%)": val("pct_gdp", y + 1)}))
t2 = pd.DataFrame(rows).set_index("Report")
t2["Realisation year"] = t2["Realisation year"].astype(int)
# the 2017 report prints no aggregate table: realisation total from annex sub-table totals
rec = pd.read_csv(TB / "reconciliation_annex_vs_body.csv")
a17 = rec[(rec.report_id == "VHR2017") & (rec.body_line == "TOTAL") & (rec.fiscal_year == 2016)].annex_million
t2.loc["2017", "TE (million TL)"] = float(a17.iloc[0]) if len(a17) else np.nan
save(t2, "table2_official_aggregates.csv")
md("Table 2. Official aggregate tax expenditure estimates (realisation year of each report)", t2,
   "Ratios are those published in the reports' body tables (GDP and general budget tax revenue as used by the reports). "
   "The 2017 report publishes no aggregate table; its total is the sum of annex sub-table totals and no ratio is available. "
   "Million TL are nominal and are not comparable across years. Revenue-forgone, no-behavioural-response estimates. "
   "Source: data/interim/report_summary_tables.csv.", floatfmt=".2f")

fig, ax = plt.subplots(figsize=(6.6, 3.4))
for r in ORDER:
    g = ST[(ST.report_id == r) & (ST.table_kind == "pct_gdp")].sort_values("fiscal_year")
    if g.empty:
        continue
    ax.plot(g.fiscal_year, g.value, color="#86b6ef", lw=1.2, zorder=1)
real = t2.dropna(subset=["TE/GDP (%)"])
xs, ys = real["Realisation year"].values, real["TE/GDP (%)"].values
ax.plot(xs[xs >= 2019], ys[xs >= 2019], color="#184f95", lw=2, zorder=3)      # connect consecutive years only
ax.scatter(xs, ys, s=30, color="#184f95", zorder=4, edgecolor="white", linewidth=1.5)
for x, y in zip(xs, ys):
    ax.annotate(f"{y:.2f}", (x, y), textcoords="offset points", xytext=(-4, 7), ha="right", fontsize=7.5, color=INK,
                bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none", alpha=0.85))
ax.axvline(2018, color=GREY, lw=1, ls=":"); ax.text(2018, ax.get_ylim()[0] + 0.1, "no 2018\nrealisation;\n2016: no ratio", fontsize=7, color=MUTED, ha="center")
ax.set_ylabel("Tax expenditure, % of GDP"); ax.set_xlabel("Fiscal year")
ax.set_xticks(range(2015, 2029, 1)); ax.tick_params(axis="x", labelsize=7.5)
ax.grid(axis="y", color="#ecebe6", lw=0.8); ax.set_axisbelow(True)
from matplotlib.lines import Line2D
ax.legend([Line2D([], [], color="#184f95", lw=2, marker="o"), Line2D([], [], color="#86b6ef", lw=1.2)],
          ["Realisation-year estimate (each report)", "Projections published in each report"], frameon=False, fontsize=7.5, loc="upper left")
fig.tight_layout(); fig.savefig(FG / "fig1_te_gdp_vintages.png", dpi=300); plt.close(fig)

# ---------------------------------------------------------------- Table 3: forecast revisions (aggregate)
AM = ST[ST.table_kind == "amount"].set_index(["report_id", "fiscal_year"]).value
BL = pd.read_csv(ROOT / "data" / "interim" / "report_summary_tables.csv")
BL = BL[(BL.table_kind == "budget_law") & (BL.line == "TOTAL") & (BL.series == "report_basis")].set_index(["report_id", "fiscal_year"]).value
GD = ST[ST.table_kind == "pct_gdp"].set_index(["report_id", "fiscal_year"]).value
rv = []
nxt = {ORDER[i]: ORDER[i + 1] for i in range(len(ORDER) - 1)}
for r in ORDER:
    y = REAL[r] + 1                       # first projection year of report r
    later = [q for q in ORDER if REAL[q] == y]
    if not later:
        continue
    q = later[0]
    proj = AM.get((r, y), np.nan); realv = AM.get((q, y), np.nan)
    if r == "VHR2017":                    # no body table: use the annex sub-table totals
        a = rec[(rec.report_id == r) & (rec.body_line == "TOTAL") & (rec.fiscal_year == y)].annex_million
        proj = float(a.iloc[0]) if len(a) else np.nan
    if q == "VHR2017":
        realv = t2.loc["2017", "TE (million TL)"]
    prev = [p for p in ORDER if REAL[p] == y - 2]
    budget = BL.get((prev[0], y), np.nan) if prev else np.nan
    rv.append({"Fiscal year": y, "Projection (report)": LAB[r], "Projection (million TL)": proj,
               "Budget-law estimate (report)": LAB[prev[0]] if prev else "", "Budget-law estimate (million TL)": budget,
               "Realisation (report)": LAB[q], "Realisation (million TL)": realv,
               "Realisation vs projection (%)": 100 * (realv / proj - 1) if proj == proj else np.nan,
               "Realisation vs budget law (%)": 100 * (realv / budget - 1) if budget == budget else np.nan,
               "Projection TE/GDP (%)": GD.get((r, y), np.nan), "Realisation TE/GDP (%)": GD.get((q, y), np.nan)})
t3 = pd.DataFrame(rv).set_index("Fiscal year")
save(t3, "table3_forecast_revisions.csv")
md("Table 3. Same-year comparison of projections, budget-law estimates and later realisation estimates", t3,
   "Each row compares estimates for the same fiscal year published in different reports (same-year prices, so the "
   "nominal comparison is meaningful). Budget-law estimates are the first-year figures of the budget-law table printed "
   "in the report published two years before the realisation estimate. Differences reflect macro assumptions, legal "
   "changes and data/method updates together; they are not a measure of policy effects.", floatfmt=".1f")

# item-level revisions (strong links only)
rows = []
for r in ORDER:
    y = REAL[r] + 1
    later = [q for q in ORDER if REAL[q] == y]
    if not later:
        continue
    q = later[0]
    a = IY[(IY.report_id == r) & (IY.fiscal_year == y) & (IY.C3 == "2")][["item_id", "amount_thousand_try"]]
    b = IY[(IY.report_id == q) & (IY.fiscal_year == y) & (IY.C3 == "2") & (IY.link_method == "legal_ref+description")][["item_id", "amount_thousand_try"]]
    m = a.merge(b, on="item_id", suffixes=("_proj", "_real"))
    m = m[(m.amount_thousand_try_proj > 0) & (m.amount_thousand_try_real > 0)]
    lr = np.log(m.amount_thousand_try_real / m.amount_thousand_try_proj)
    rows.append({"Fiscal year": y, "Reports": f"{LAB[r]} -> {LAB[q]}", "Linked items": len(m),
                 "Median ratio realisation/projection": float(np.exp(lr.median())) if len(m) else np.nan,
                 "Share within ±10% (%)": 100 * float((lr.abs() <= np.log(1.1)).mean()) if len(m) else np.nan,
                 "Share off by more than 50% (%)": 100 * float(((lr > np.log(1.5)) | (lr < np.log(1 / 1.5))).mean()) if len(m) else np.nan})
t3b = pd.DataFrame(rows).set_index("Fiscal year")
save(t3b, "table3b_item_revisions.csv")
md("Table 3b. Item-level projection versus later realisation estimate (strongly linked items)", t3b,
   "Items linked by legal reference and description, estimated (C3 = 2) and positive in both reports. 'Off by more "
   "than 50%' = realisation above 1.5 times or below 1/1.5 of the projection.", floatfmt=".2f")

# ---------------------------------------------------------------- Table 4 / Fig 2: cost information per item (C3)
R = IC.copy()
c3lab = {"2": "Estimated", "1": "Partial / combined", "0": "No estimate", "NA": "Not applicable"}
t4 = pd.crosstab(R.report_id.map(LAB), R.C3.map(c3lab))[list(c3lab.values())]
st = pd.crosstab(R.report_id.map(LAB), R.cell_status.fillna("blank"))
t4["of which: data not available"] = st.get("data_not_available", 0)
t4["of which: new measure"] = st.get("new_measure", 0)
t4["Total items"] = t4[list(c3lab.values())].sum(axis=1)
t4 = t4.astype(int); t4.index.name = "Report"
t4["Estimated, % of applicable"] = 100 * t4["Estimated"] / (t4["Total items"] - t4["Not applicable"])
save(t4, "table4_cost_information.csv")
md("Table 4. Item-level cost information in the realisation year (criterion C3)", t4,
   "Counts of annex items. 'No estimate' = 'Veri temin edilememiştir' (data could not be obtained), 'Yeni uygulama' "
   "(new measure) or blank; 'Not applicable' = 'Vergi harcaması oluşmamıştır' (no tax expenditure arises), dash or repealed. "
   "Source: data/coding/item_codes.csv.", floatfmt=".1f")

fig, ax = plt.subplots(figsize=(6.6, 3.2))
cols = [("Estimated", BLUE["2"]), ("Partial / combined", BLUE["1"]), ("No estimate", BLUE["0"]), ("Not applicable", GREY)]
left = np.zeros(len(t4))
yl = list(t4.index)
for c, colr in cols:
    v = t4[c].values
    ax.barh(yl, v, left=left, color=colr, edgecolor="white", linewidth=1.5, height=0.62, label=c)
    left += v
for i, (e, tot) in enumerate(zip(t4["Estimated, % of applicable"], t4["Total items"])):
    ax.text(tot + 3, i, f"{e:.0f}% estimated", va="center", fontsize=7.5, color=INK)
ax.invert_yaxis(); ax.set_xlabel("Annex items (realisation year)"); ax.set_xlim(0, 300)
ax.legend(frameon=False, fontsize=7.5, ncol=4, loc="lower center", bbox_to_anchor=(0.45, 1.0))
ax.grid(axis="x", color="#ecebe6", lw=0.8); ax.set_axisbelow(True)
fig.tight_layout(); fig.savefig(FG / "fig2_cost_information.png", dpi=300); plt.close(fig)

# ---------------------------------------------------------------- Table 5 / Fig 3: estimate quality
E = R[R.C3.isin(["1", "2"]) & R.amount_thousand_try.notna()].copy()
qlab = {"very_good": "Very good", "good": "Good", "approximate": "Approximate"}
E["q"] = E.estimate_quality.map(qlab).fillna("No label")
qc = pd.crosstab(E.report_id.map(LAB), E.q)[["Very good", "Good", "Approximate", "No label"]]
qa = E.pivot_table(index=E.report_id.map(LAB), columns="q", values="amount_thousand_try", aggfunc="sum").fillna(0)
qa = 100 * qa.div(qa.sum(axis=1), axis=0)
qc.index.name = "Report"; qa.index.name = "Report"
t5 = qc.join(qa[["Very good", "Good", "Approximate", "No label"]].add_suffix(" (% of amount)"))
save(t5, "table5_estimate_quality.csv")
md("Table 5. Estimate-quality labels of estimated items in the realisation year (criterion C4)", t5,
   "Counts of items with an estimate, and shares of the summed realisation-year amount within each report "
   "(within-report shares only). The reports do not define the criteria behind the three labels and publish no "
   "ranges or standard errors; every labelled item is therefore coded C4 = 1.", floatfmt=".1f")

fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.1), sharey=True)
qcol = [("Very good", BLUE["2"]), ("Good", BLUE["1"]), ("Approximate", BLUE["0"]), ("No label", GREY)]
for ax, tab, ttl in [(axes[0], 100 * qc.div(qc.sum(axis=1), axis=0), "Share of estimated items (%)"),
                     (axes[1], qa[["Very good", "Good", "Approximate", "No label"]], "Share of estimated amount (%)")]:
    left = np.zeros(len(tab))
    for c, colr in qcol:
        v = tab[c].values
        ax.barh(list(tab.index), v, left=left, color=colr, edgecolor="white", linewidth=1.5, height=0.62, label=c)
        left += v
    ax.set_xlim(0, 100); ax.set_title(ttl, fontsize=8.5, color=INK, loc="left")
axes[0].invert_yaxis()
axes[0].legend(frameon=False, fontsize=7.5, ncol=4, loc="lower left", bbox_to_anchor=(0.0, 1.08))
fig.tight_layout(); fig.savefig(FG / "fig3_estimate_quality.png", dpi=300); plt.close(fig)

# ---------------------------------------------------------------- Table 6 / Fig 4: criteria by report (items)
def shares(d, c):
    v = d[c].astype(str)
    app = v[v != "NA"]
    n = len(app)
    return pd.Series({"n": n, "2": 100 * (app == "2").mean() if n else np.nan, "1": 100 * (app == "1").mean() if n else np.nan,
                      "0": 100 * (app == "0").mean() if n else np.nan, "NA": int((v == "NA").sum())})
recs = []
for r in ORDER:
    d = R[R.report_id == r]
    for c in CRIT:
        s = shares(d, c)
        recs.append(dict(Report=LAB[r], Criterion=c, **s.to_dict()))
T6 = pd.DataFrame(recs)
save(T6.set_index(["Report", "Criterion"]), "table6_criteria_items_long.csv")
wide = T6.assign(cell=lambda d: d.apply(lambda x: f"{x['2']:.0f} / {x['1']:.0f} / {x['0']:.0f}", axis=1)).pivot(index="Criterion", columns="Report", values="cell")
wide.index = [f"{c} {CNAME[c]}" for c in wide.index]
den = T6.pivot(index="Criterion", columns="Report", values="n").astype(int)
md("Table 6. Item-level evaluability codes by report: % coded 2 / 1 / 0 (realisation year)", wide,
   "Denominator = annex items of the report excluding NA (C3/C4: NA = no tax expenditure arises, dash or no estimate; "
   "narrative criteria: NA = the report states the provision is not a tax expenditure). Items without a narrative "
   "section (incl. all BSMV, MTV and ÖİV items) are coded 0 on C1, C2, C5-C9. Narrative codes are section-level codes "
   "attributed to items (decision D1). Denominators by criterion and report: table6_criteria_items_long.csv.")
save(den, "table6_denominators.csv")

H = T6.pivot(index="Criterion", columns="Report", values="2").reindex(CRIT)
H1 = T6.pivot(index="Criterion", columns="Report", values="1").reindex(CRIT)
fig, ax = plt.subplots(figsize=(6.8, 3.9))
any1 = (H + H1).values
im = ax.imshow(any1, cmap=matplotlib.colors.LinearSegmentedColormap.from_list("b", ["#f4f8fd", "#86b6ef", "#184f95"]), vmin=0, vmax=100, aspect="auto")
for i in range(any1.shape[0]):
    for j in range(any1.shape[1]):
        v, v2 = any1[i, j], H.values[i, j]
        ax.text(j, i, f"{v:.0f}\n({v2:.0f})", ha="center", va="center", fontsize=6.5, color="white" if v > 60 else INK)
ax.set_xticks(range(len(H.columns))); ax.set_xticklabels(H.columns)
ax.set_yticks(range(len(CRIT))); ax.set_yticklabels([f"{c} {CNAME[c]}" for c in CRIT], fontsize=7.5)
for s in ax.spines.values():
    s.set_visible(False)
cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02); cb.set_label("% of items coded 1 or 2", fontsize=7.5); cb.ax.tick_params(labelsize=7)
ax.set_title("Cell: % coded ≥1  (in brackets: % coded 2, explicit item-level)", fontsize=8, color=MUTED, loc="left")
fig.tight_layout(); fig.savefig(FG / "fig4_criteria_heatmap.png", dpi=300); plt.close(fig)

# ---------------------------------------------------------------- Table 7: section-level codes (2016, 2025)
recs = []
for r in ["VHR2016", "VHR2018", "VHR2025"]:
    d = S[S.report_id == r]
    for c in ["C1", "C2", "C5", "C6", "C7", "C8", "C9", "M", "B"]:
        s = shares(d, c)
        recs.append(dict(Report=LAB[r], Criterion=c, **s.to_dict()))
T7l = pd.DataFrame(recs)
save(T7l.set_index(["Criterion", "Report"]), "table7_criteria_sections.csv")
T7 = T7l.assign(cell=lambda d: d.apply(lambda x: f"{x['2']:.0f} / {x['1']:.0f} / {x['0']:.0f}", axis=1)).pivot(index="Criterion", columns="Report", values="cell")
T7.loc["n sections (excl. NA)"] = T7l.groupby("Report").n.first().astype(int).astype(str)
T7.loc["NA (report: not a tax expenditure)"] = T7l.groupby("Report").NA.first().astype(int).astype(str)
md("Table 7. Section-level codes (narrative sections), % coded 2 / 1 / 0", T7,
   "Unit: numbered narrative section. n = sections excluding those the report classifies as not a tax expenditure (NA). "
   "M = estimation method described; B = beneficiary count reported (auxiliary variables).")

# ---------------------------------------------------------------- Table 8: amount-weighted (latest report)
L = R[(R.report_id == "VHR2025") & (R.C3 == "2")].copy()
tot = L.amount_thousand_try.sum()
rows = []
for c in ["C1", "C2", "C5", "C6", "C7", "C8", "C9"]:
    rows.append({"Criterion": f"{c} {CNAME[c]}", "Items coded 2 (% of amount)": 100 * L[L[c] == "2"].amount_thousand_try.sum() / tot,
                 "Items coded 1 (% of amount)": 100 * L[L[c] == "1"].amount_thousand_try.sum() / tot,
                 "Items coded 0 (% of amount)": 100 * L[L[c] == "0"].amount_thousand_try.sum() / tot})
t8 = pd.DataFrame(rows).set_index("Criterion")
save(t8, "table8_amount_weighted_2025.csv")
md("Table 8. Evaluability weighted by estimated cost, 2025 report (2024 realisation)", t8,
   f"Shares of the summed 2024 realisation amounts of estimated items ({tot/1e3:,.0f} million TL across {len(L)} items; "
   "NA items included in neither numerator nor shown). Within-report shares only.", floatfmt=".1f")

# ---------------------------------------------------------------- Table 9: largest items (latest report)
top = L.sort_values("amount_thousand_try", ascending=False).head(10)
t9 = pd.DataFrame({"Tax": top.tax_type.values, "Provision (annex description)": top.description.str.slice(0, 70).values,
                   "Share of estimated total (%)": (100 * top.amount_thousand_try / tot).values,
                   "Quality": top.estimate_quality.map(qlab).fillna("-").values,
                   "C1": top.C1.values, "C5": top.C5.values, "C6": top.C6.values, "C7": top.C7.values, "C8": top.C8.values,
                   "C9": top.C9.values, "Narrative": top.narrative_note.values}, index=range(1, 11))
save(t9, "table9_top10_2025.csv")
md("Table 9. Ten largest items in the 2025 report (2024 realisation) and their codes", t9,
   f"Together {t9['Share of estimated total (%)'].sum():.1f}% of the estimated total. Source page references in data/coding/item_codes.csv.",
   floatfmt=".1f")

# ---------------------------------------------------------------- Table 10: persistence of missing estimates and churn
IB = pd.read_csv(ROOT / "data" / "interim" / "items_by_report.csv")
G = R.groupby("item_id").agg(n_reports=("report_id", "nunique"), n_noest=("C3", lambda s: (s == "0").sum()),
                             n_est=("C3", lambda s: (s == "2").sum()))
t10 = pd.DataFrame({
    "Distinct items (linked ids)": [len(G)],
    "Items appearing in ≥3 reports": [int((G.n_reports >= 3).sum())],
    "...of which never estimated (C3=0 in every report)": [int(((G.n_reports >= 3) & (G.n_noest == G.n_reports)).sum())],
    "...of which C3=0 in at least one report": [int(((G.n_reports >= 3) & (G.n_noest > 0)).sum())],
}).T.rename(columns={0: "Count"})
churn = []
for a, b in zip(ORDER[:-1], ORDER[1:]):
    A, B = set(IB[IB.report_id == a].item_id), set(IB[IB.report_id == b].item_id)
    churn.append({"From": LAB[a], "To": LAB[b], "Items in later report": len(B), "Not in earlier report": len(B - A), "Dropped": len(A - B)})
t10b = pd.DataFrame(churn).set_index(["From", "To"])
save(t10, "table10_missing_persistence.csv"); save(t10b, "table10b_item_churn.csv")
md("Table 10. Persistence of missing cost estimates across reports", t10,
   "Item identities across reports are a research construct (data/interim/items_by_report.csv, link_method).", floatfmt=".0f")
md("Table 10b. Items entering and leaving the annex lists between consecutive reports", t10b,
   "Counts by linked item id. Entries combine new provisions, newly listed existing provisions and linking failures; "
   "the 2017-2018 and 2018-2020 steps also reflect the missing 2019 report.", floatfmt=".0f")

(TB / "tables.md").write_text("# Tables (generated by scripts/10_analysis.py)\n\n" + "\n".join(MD), encoding="utf-8")
print("\n".join(MD)[:200000])
