"""Build the improved paper (.docx) from calisma/metin_gelistirilmis.md, using the ORIGINAL docx as a template
(same page size, margins, fonts and heading styles). The original file is only read, never written.
Usage: python3 scripts/build_docx.py"""
import copy, re
from pathlib import Path
import docx
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "kaynak" / "Yerel_Yonetimlerde_Yesil_Finansman 23.11.2026 son.docx"
MD = ROOT / "calisma" / "metin_gelistirilmis.md"
OUT = ROOT / "04_Yerel_Yesil_Finansman_Gelistirilmis.docx"

d = docx.Document(SRC)
body = d.element.body
for el in list(body):
    if el.tag != qn("w:sectPr"):
        body.remove(el)

def add_runs(p, text, size=None):
    for tok in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text):
        if not tok: continue
        if tok.startswith("**"): r = p.add_run(tok[2:-2]); r.bold = True
        elif tok.startswith("*"): r = p.add_run(tok[1:-1]); r.italic = True
        else: r = p.add_run(tok)
        if size: r.font.size = Pt(size)
    return p

md = MD.read_text(encoding="utf-8")
md = re.sub(r"^---.*?---\s*", "", md, flags=re.S)
p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("YEREL YÖNETİMLERDE YEŞİL FİNANSMAN VE SÜRDÜRÜLEBİLİRLİK"); r.bold = True; r.font.size = Pt(15)
p = d.add_paragraph("XII. International Academic Studies Congress · Stuttgart · 24–26 Kasım 2026"); p.alignment = WD_ALIGN_PARAGRAPH.CENTER

has_h2 = "Heading 2" in [s.name for s in d.styles]
in_ref = False
blocks = md.split("\n\n")
i = 0
while i < len(blocks):
    b = blocks[i].strip(); i += 1
    if not b: continue
    if b.startswith("# "):
        d.add_paragraph(b[2:].strip(), style="Heading 1"); in_ref = b[2:].strip() == "KAYNAKÇA"; continue
    if b.startswith("## "):
        p = d.add_paragraph(style="Heading 2" if has_h2 else None)
        if has_h2: p.add_run(b[3:].strip())
        else: rr = p.add_run(b[3:].strip()); rr.bold = True
        continue
    if b.startswith("|"):
        rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in b.splitlines() if not re.match(r"^\|[-|\s]+\|$", ln.strip())]
        t = d.add_table(rows=len(rows), cols=len(rows[0]))
        t.style = d.styles["Table Grid"] if "Table Grid" in [s.name for s in d.styles] else None
        for ri, row in enumerate(rows):
            for ci, txt in enumerate(row):
                c = t.cell(ri, ci); c.text = ""
                cp = c.paragraphs[0]; cp.paragraph_format.space_after = Pt(0)
                add_runs(cp, f"**{txt}**" if ri == 0 else txt, size=8)
        if t.style is None:   # add borders manually
            tblPr = t._tbl.tblPr
            borders = docx.oxml.parse_xml('<w:tblBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">' +
                "".join(f'<w:{e} w:val="single" w:sz="4" w:space="0" w:color="000000"/>' for e in ("top","left","bottom","right","insideH","insideV")) + "</w:tblBorders>")
            tblPr.append(borders)
        d.add_paragraph()
        continue
    if re.match(r"^\d+\.\s", b):
        for ln in b.splitlines():
            p = d.add_paragraph(); p.paragraph_format.left_indent = Cm(0.63); p.paragraph_format.first_line_indent = Cm(-0.63)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY; add_runs(p, ln.strip())
        continue
    p = d.add_paragraph()
    text = " ".join(b.splitlines())
    if in_ref:
        p.paragraph_format.left_indent = Cm(1.27); p.paragraph_format.first_line_indent = Cm(-1.27)
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    add_runs(p, text)
d.core_properties.title = "Yerel Yönetimlerde Yeşil Finansman ve Sürdürülebilirlik"
d.save(OUT)
print("saved", OUT)
