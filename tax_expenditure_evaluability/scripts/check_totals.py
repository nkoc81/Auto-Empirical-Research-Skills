"""Compare the sum of extracted item rows with the GENEL TOPLAM line of each sub-table."""
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import tax_type, sub_table
I = Path(__file__).resolve().parents[1] / "data" / "interim"
out = []
for rid in sys.argv[1:]:
    r = pd.read_csv(I / f"annex_rows_{rid}.csv"); t = pd.read_csv(I / f"annex_totals_{rid}.csv")
    for d in (r, t):
        d["tax"] = [tax_type(a, b) for a, b in zip(d.table, d.section)]
        d["sub"] = [sub_table(b) for b in d.section]
    s = r.groupby(["tax", "sub"])[[f"value_{i}" for i in range(5)]].sum()
    tt = t.groupby(["tax", "sub"])[[f"value_{i}" for i in range(5)]].first()
    c = s.join(tt, rsuffix="_tot", how="outer")
    for i in range(5):
        c[f"d{i}"] = c[f"value_{i}"] - c[f"value_{i}_tot"]
    c["report_id"] = rid
    out.append(c.reset_index())
    print(rid, "rows", len(r)); print(c[["value_0", "value_0_tot", "d0", "d1", "d2", "d3", "d4"]].round(0).to_string())
if out and "--save" in sys.argv[0:0] + []:
    pass
