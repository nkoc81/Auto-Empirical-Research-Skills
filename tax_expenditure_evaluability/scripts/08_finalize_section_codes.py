"""Apply the coder's overrides to the rule-based section codes and list differences between consecutive reports.

* An override (data/coding/overrides.csv) applies to its own report-section and, following decision D10, to
  the same-title section of any other report where the rule fired on the identical evidence sentence.
* Output: data/coding/section_codes.csv (final), data/coding/consecutive_report_differences.csv (for review)
"""
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CD = ROOT / "data" / "coding"
ORDER = ["VHR2016", "VHR2017", "VHR2018", "VHR2020", "VHR2021", "VHR2022", "VHR2023", "VHR2024", "VHR2025"]
VARS = ["C1", "C2", "C5", "C6", "C7", "C8", "C9", "M", "B"]


def tnorm(t):
    t = str(t).lower().replace("ş", "s").replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ö", "o").replace("ç", "c")
    t = re.sub(r"\(.*?\)|\d+", " ", t)
    return re.sub(r"[^a-z]+", " ", t).strip()[:60]


def enorm(e):
    e = str(e).lower()
    e = re.sub(r"\d+", "#", e)
    return re.sub(r"[^a-zçğıöşü#]+", " ", e).strip()[:200]


def main():
    D = pd.read_csv(CD / "section_codes_auto.csv", dtype=str, keep_default_na=False, na_values=[""])
    D["title_key"] = D.title.map(tnorm)
    D["code_source"] = "rule"
    D["override_note"] = ""
    O = pd.read_csv(CD / "overrides.csv", dtype=str, keep_default_na=False)
    for _, o in O.iterrows():
        src = D[(D.report_id == o.report_id) & (D.sec_no == o.sec_no)]
        if src.empty:
            raise SystemExit(f"override target not found: {o.report_id} {o.sec_no}")
        s = src.iloc[0]
        ev_key = enorm(s[f"{o.variable}_evidence"]) if f"{o.variable}_evidence" in D else None
        if str(o.get("scope", "")) == "same_title":      # judgement about the section's content (text near-identical)
            same = D.title_key == s.title_key
        else:
            same = (D.title_key == s.title_key) & (((D.report_id == o.report_id) & (D.sec_no == o.sec_no)) |
                                                   (D[f"{o.variable}_evidence"].map(enorm) == ev_key))
        idx = D[same].index
        D.loc[idx, o.variable] = o.new_value
        D.loc[idx, "code_source"] = "rule+override"
        D.loc[idx, "override_note"] = D.loc[idx, "override_note"] + f"{o.variable}={o.new_value} ({o.decision}); "
    # C6/C7/B: the only rule hits were reviewed and rejected (decision D3); keep as rule output otherwise
    D.to_csv(CD / "section_codes.csv", index=False)

    # differences between consecutive reports for same-title sections
    rows = []
    for a, b in list(zip(ORDER[:-1], ORDER[1:])) + [("VHR2016", "VHR2018")]:
        A = D[D.report_id == a].set_index("title_key")
        B = D[D.report_id == b].set_index("title_key")
        for k in B.index.intersection(A.index):
            ra, rb = A.loc[k], B.loc[k]
            if isinstance(ra, pd.DataFrame) or isinstance(rb, pd.DataFrame):
                continue
            for v in VARS:
                if str(ra[v]) != str(rb[v]):
                    rows.append(dict(from_report=a, to_report=b, sec_from=ra.sec_no, sec_to=rb.sec_no, title=rb.title[:80],
                                     variable=v, code_from=ra[v], code_to=rb[v],
                                     evidence_from=str(ra[f"{v}_evidence"])[:200], evidence_to=str(rb[f"{v}_evidence"])[:200]))
    X = pd.DataFrame(rows)
    X.to_csv(CD / "consecutive_report_differences.csv", index=False)
    print("final codes:", len(D), "| differences between consecutive reports:", len(X))
    if len(X):
        print(X.groupby(["from_report", "to_report", "variable"]).size().unstack(fill_value=0))


if __name__ == "__main__":
    main()
