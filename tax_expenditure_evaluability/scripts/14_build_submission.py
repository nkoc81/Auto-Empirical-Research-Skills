"""Build the journal-submission files from paper/manuscript.md, paper/references.bib, outputs/tables/tables.md and
outputs/figures/*.png.

Outputs (paper/submission/):
  manuscript_anonymised.md / .docx  - blinded manuscript: text, references (APA 7, citeproc), tables, figures, appendix
  title_page.md / .docx             - non-blinded title page with repository link and declarations (placeholders
                                      where the information is the author's to supply)
Tables are reformatted for print only (nan -> en dash, thousands separators, file paths removed from notes);
no value is recomputed. Usage: python3 scripts/14_build_submission.py
"""
import re, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "paper"; OUT = P / "submission"; OUT.mkdir(exist_ok=True)

FIGS = [("fig1_te_gdp_vintages.png", "Figure 1. Reported tax expenditures as a share of GDP: realisation-year estimate of each report and the projections published in each report"),
        ("fig2_cost_information.png", "Figure 2. Item-level cost information in the realisation year, by report (criterion C3)"),
        ("fig3_estimate_quality.png", "Figure 3. Estimate-quality labels of estimated items, by report (criterion C4)"),
        ("fig4_criteria_heatmap.png", "Figure 4. Evaluability criteria by report: share of items coded 1 or 2 (in brackets: coded 2), upper-bound attribution")]

def fmt_cell(c):
    t = c.strip()
    if t.lower() in ("nan", "none", ""): return "–" if t else t
    if re.fullmatch(r"(19|20)\d{2}\.0+", t): return t.split(".")[0]          # years printed as floats
    m = re.fullmatch(r"-?\d+(\.\d+)?", t)
    if m and abs(float(t)) >= 10000:
        dec = len(t.split(".")[1]) if "." in t else 0
        dec = 0 if dec and set(t.split(".")[1]) == {"0"} else min(dec, 1)
        return f"{float(t):,.{dec}f}"
    return t

def _is_num(t):
    return re.fullmatch(r"-?\d+(\.\d+)?", t.strip()) is not None

def _fmt_table(rows):
    """rows: list of cell lists (header first). Column-wise formatting; returns pipe-table lines."""
    head, data = rows[0], rows[1:]
    ncol = len(head)
    for j in range(ncol):
        col = [r[j].strip() for r in data if j < len(r)]
        nums = [c for c in col if _is_num(c)]
        intcol = nums and all(re.fullmatch(r"-?\d+(\.0+)?", c) for c in nums)
        for r in data:
            c = r[j].strip()
            if c.lower() in ("nan", "none"): r[j] = "–"
            elif intcol and _is_num(c):
                v = int(float(c)); r[j] = f"{v:,}" if abs(v) >= 10000 and "year" not in head[j].lower() and head[j].strip().lower() not in ("report", "fiscal year") else str(v)
            else: r[j] = fmt_cell(c)
    width = [max(8, max(len(w) for w in (head[j] + " " + " ".join(r[j] for r in data)).split()) + 2,
                 min(40, max(len(r[j]) for r in rows) // 2)) for j in range(ncol)]
    out = ["| " + " | ".join(h.strip() for h in head) + " |",
           "|" + "|".join(("-" * w + ":") if any(_is_num(r[j].replace(",", "").replace("–", "0")) for r in data) else ("-" * (w + 1)) for j, w in enumerate(width)) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in data]
    return out

def tidy_tables(md):
    md = md.split("\n", 1)[1]                                              # drop generator heading
    out, buf = [], []
    def flush():
        if buf:
            rows = [ln.strip().strip("|").split("|") for ln in buf if not re.fullmatch(r"\|[-:| ]+\|", ln.strip())]
            out.extend(_fmt_table(rows)); buf.clear()
    for ln in md.splitlines():
        if ln.startswith("|"):
            buf.append(ln); continue
        flush()
        if ln.startswith("*Note:*"):
            ln = re.sub(r"\s*Sources?:\s*(?:[\w/]+\.(?:csv|md|py)(?:,\s*|\s+and\s+)?)+\.?", " Source: replication package.", ln)
            ln = re.sub(r"Source page references in [\w/]+\.csv\.?", "Source page references are given in the replication package.", ln)
            ln = re.sub(r"\s*\((?:scripts|data|outputs)/[^)]*\)", "", ln)
            ln = re.sub(r"Denominators by criterion and report: [\w/]+\.csv\.?", "Denominators by criterion and report are given in the replication package.", ln)
            ln = re.sub(r"[\w/]+\.(csv|py)", "the replication package", ln)
        ln = re.sub(r"^### (Table \w+)\. ", r"**\1.** ", ln)
        out.append(ln)
    flush()
    return "\n".join(out)

ms = (P / "manuscript.md").read_text(encoding="utf-8")
head, rest = ms.split("\n---\n", 1)
yaml = head + "\nreference-section-title: References\n---\n" if False else head + "\n---\n"
body = rest
# drop the author line from YAML for the blinded version
yaml = re.sub(r'\nauthor: .*', "", yaml)
pre, post = body.split("## Appendix", 1)
tables = tidy_tables((ROOT / "outputs" / "tables" / "tables.md").read_text(encoding="utf-8"))
figs = "\n\n".join(f"**{cap.split('. ',1)[0]}.** {cap.split('. ',1)[1]}\n\n![]({(ROOT/'outputs'/'figures'/f).as_posix()}){{width=100%}}" for f, cap in FIGS)
anon = yaml + pre + "## Tables\n\n" + tables + "\n\n## Figures\n\n" + figs + "\n\n## Appendix" + post
(OUT / "manuscript_anonymised.md").write_text(anon, encoding="utf-8")

title = f"""---
title: "Evaluability of Tax Expenditures in Türkiye: An Assessment of Official Reporting Against the IMF Evaluation Framework"
---

## Title page

**Author:** [Name], [Affiliation], [ORCID]

**Corresponding author:** [Name, postal address, e-mail]

**Word count:** {len(re.findall(r"[A-Za-zÀ-ž0-9]+", pre.split("## References")[0]))} words (main text including abstract, excluding references, tables, figures and appendix)

## Declarations

**Data and code availability.** The replication package (source documents, extracted data, coding files and scripts) is available at https://github.com/nkoc81/Auto-Empirical-Research-Skills (folder `tax_expenditure_evaluability`). [Before submission: merge the working branch into the default branch, create a tagged release and an archived copy with a DOI (for example, via Zenodo) and insert the DOI here. No DOI has been created yet.]

**Funding.** [To be completed by the author.]

**Competing interests.** [To be completed by the author.]

**Use of AI tools.** [To be completed by the author in line with the journal's policy.]

**Acknowledgements.** [Optional.]
"""
(OUT / "title_page.md").write_text(title, encoding="utf-8")

def postprocess(path):
    import copy, docx
    from docx.shared import Pt
    from docx.enum.section import WD_ORIENT
    from docx.oxml.ns import qn
    d = docx.Document(path)
    for t in d.tables:
        t.autofit = True
        for row in t.rows:
            for c in row.cells:
                for p in c.paragraphs:
                    p.paragraph_format.space_after = Pt(0)
                    for r in p.runs: r.font.size = Pt(8)
    # landscape from the "Tables" heading to the end
    paras = d.paragraphs
    idx = next(i for i, p in enumerate(paras) if p.style.name.startswith("Heading") and p.text.strip() == "Tables")
    body_sect = d.element.body.find(qn("w:sectPr"))
    prev = paras[idx - 1]
    pPr = prev._p.get_or_add_pPr()
    pPr.append(copy.deepcopy(body_sect))                    # ends the portrait section here
    from docx.shared import Cm
    for i, sec in enumerate(d.sections):                    # A4; last section (tables, figures, appendix) landscape
        land = i == len(d.sections) - 1
        sec.orientation = WD_ORIENT.LANDSCAPE if land else WD_ORIENT.PORTRAIT
        sec.page_width, sec.page_height = (Cm(29.7), Cm(21.0)) if land else (Cm(21.0), Cm(29.7))
        for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"): setattr(sec, m, Cm(2.5))
    d.save(path)

csl = P / "csl" / "apa.csl"
for name in ("manuscript_anonymised", "title_page"):
    cmd = ["pandoc", str(OUT / f"{name}.md"), "-o", str(OUT / f"{name}.docx"), "--resource-path", str(ROOT)]
    if name == "manuscript_anonymised":
        cmd += ["--citeproc", "--bibliography", str(P / "references.bib"), "--csl", str(csl), "--metadata", "link-citations=true"]
    subprocess.run(cmd, check=True, cwd=P)
    if name == "manuscript_anonymised":
        postprocess(OUT / f"{name}.docx")
    print("wrote", OUT / f"{name}.docx")
