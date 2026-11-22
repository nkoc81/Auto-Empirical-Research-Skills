"""Diagnostics: gaps/duplicates in row numbers within each sub-table and suspicious raw cells."""
import sys
import pandas as pd
from pathlib import Path
I = Path(__file__).resolve().parents[1] / "data" / "interim"
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 50)
for rid in sys.argv[1:]:
    r = pd.read_csv(I / f"annex_rows_{rid}.csv")
    r["tax"] = r.table.str.extract(r"EK I-(\d)")[0]
    print("=====", rid)
    for (t, s), g in r.groupby(["tax", "section"], sort=False):
        nums = list(g.row_no)
        exp = list(range(1, max(nums) + 1))
        miss = sorted(set(exp) - set(nums)); dup = sorted({x for x in nums if nums.count(x) > 1})
        if miss or dup:
            print(f"tax {t} | {s} | n={len(g)} max={max(nums)} missing={miss[:15]} dup={dup[:10]}")
    for i in range(5):
        bad = r[r[f"status_{i}"].isin(["other_text", "estimated_flagged"])]
        if len(bad):
            print("col", i); print(bad[["page", "tax", "row_no", "article", f"raw_{i}", f"status_{i}"]].to_string())
