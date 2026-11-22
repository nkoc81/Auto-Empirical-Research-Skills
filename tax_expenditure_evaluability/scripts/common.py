"""Shared helpers: tax-type assignment and sub-table keys."""
import re

TABLE_TAX = {"1": "GV", "2": "KV", "3": "KDV", "4": "ÖTV", "5": "DIGER"}


def tax_type(table, section):
    """Tax type of an annex row. Section labels identify BSMV/MTV/ÖİV sub-tables (Annex I-5), whose
    continuation pages do not repeat the annex title."""
    sec = str(section or "")
    if re.search(r"Banka|Sigorta", sec):
        return "BSMV"
    if re.search(r"Motorlu", sec):
        return "MTV"
    if re.search(r"[İI7]letişim|letiim", sec):
        return "ÖİV"
    m = re.search(r"EK I-(\d)", str(table or ""))
    return TABLE_TAX.get(m.group(1), "UNKNOWN") if m else "UNKNOWN"


def sub_table(section):
    """'main' for the tax's own law, 'other' for provisions in other laws (section '2- Diğer Kanunlar' or
    'ile ilgili diğer kanunlar')."""
    sec = str(section or "")
    return "other" if re.search(r"[Dd]iğer", sec) else "main"


# ---------------------------------------------------------------------------------------------
import pandas as _pd
from pathlib import Path as _Path

_I = _Path(__file__).resolve().parents[1] / "data" / "interim"
_SHIFT = re.compile(r"^\s*(-|\d[\d.]*)\s+(.*)$")


def quality_norm(q):
    """Map printed estimate-quality labels to very_good / good / approximate (None if absent).
    Stray tokens that the extractor attached to the label are ignored here (see load_rows)."""
    q = str(q or "")
    if re.search(r"Çok\s*[İi]yi", q):
        return "very_good"
    if re.search(r"[İ]yi|\biyi\b", q):
        return "good"
    if re.search(r"Yaklaşık", q):
        return "approximate"
    return None


def load_rows(rid):
    """Annex rows of a report after two documented corrections:
    (a) when the last-year cell is blank and the quality cell starts with a number or '-', that token
        belongs to the last-year column (it was printed close to the quality column);
    (b) rows transcribed by hand (data/interim/manual_rows_<rid>.csv) are appended."""
    r = _pd.read_csv(_I / f"annex_rows_{rid}.csv")
    r["fix_note"] = ""
    for idx, row in r.iterrows():
        m = _SHIFT.match(str(row.quality)) if isinstance(row.quality, str) else None
        if m and (row.status_4 == "blank" or _pd.isna(row.raw_4)):
            tok = m.group(1)
            r.at[idx, "raw_4"] = tok
            if tok == "-":
                r.at[idx, "status_4"] = "dash"; r.at[idx, "value_4"] = float("nan")
            else:
                r.at[idx, "status_4"] = "estimated"; r.at[idx, "value_4"] = float(tok.replace(".", ""))
            r.at[idx, "quality"] = m.group(2)
            r.at[idx, "fix_note"] = "last-year token moved from quality cell"
    man = _I / f"manual_rows_{rid}.csv"
    if man.exists():
        m = _pd.read_csv(man).rename(columns={"manual_note": "fix_note"})
        m["fix_note"] = "manual transcription: " + m.fix_note.astype(str)
        r = _pd.concat([r, m], ignore_index=True)
    r["quality_norm"] = r.quality.map(quality_norm)
    return r
