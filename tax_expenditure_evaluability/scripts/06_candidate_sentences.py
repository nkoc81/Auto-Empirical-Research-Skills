"""Retrieve candidate sentences per narrative section and criterion (retrieval only; codes are assigned by the coder).

Output: data/interim/coding_candidates.jsonl  (one record per report-section)
Usage:  python scripts/06_candidate_sentences.py [--show REPORT_ID [SEC_FROM SEC_TO]]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CUES = {
    "C1_purpose": r"amac|amaç|amaçla|hedefle|maksad|özendir|teşvik etmek|teşvik edilmesi|desteklen|korunma|korumak|kolaylaştır|kolaylık sağla|yaygınlaştır|geliştirilmesi",
    "C2_benef": r"yararlan|faydalan|mükellefler(?:in)?\b|kişiler|kurum(?:lar)?ı?n?\b|işletmeler|sektör",
    "C5_outcome": r"artır|istihdam|yatırım|ihracat|rekabet|büyüme|kalkınma|tasarruf|derinleş|azaltıl|gelişim|üretim|verimlilik",
    "C6_data": r"\b\d[\d.]*\s*(adet|kişi|mükellef|firma|şirket|belge|işletme|proje)|sayısı|gösterge",
    "C7_addit": r"ilave|olmasaydı|kendiliğinden|karşı.?olgusal|etkisi|etkileri|etki analiz|ek katkı",
    "C8_costeff": r"maliyet|etkinli|verimli|alternatif|doğrudan (kamu )?harcama|hibe|nakdi destek",
    "C9_review": r"sona er|tarihine kadar|tarihinden itibaren|yürürlük|süreyle|yıl süre|uzatıl|gözden geçir|değerlendiril|izlen|kaldırıl|mülga",
    "M_method": r"hesaplan|hesaplama|beyanname|efektif|tarife|vergi harcaması (olacaktır|tutarı)|veri(ler)?\b|tespit edil",
}


def sentences(text):
    """Return (sentence, is_legal_text, pdf_page) triples; '[[p=N]]' markers give the page."""
    t = re.sub(r"-\n\s*", "", text)
    t = re.sub(r"\n\s*\d{1,3}\s*\n", "\n", t)          # page numbers
    t = re.sub(r"\s+", " ", t)
    out, depth, buf, page, pages = [], 0, "", None, []
    t = re.sub(r"\[\[p=(\d+)\]\]", lambda m: "\x00%s\x00" % m.group(1), t)
    parts = t.split("\x00")
    stream = []
    for k, part in enumerate(parts):
        if k % 2 == 1:
            stream.append(("P", int(part)))
        else:
            stream.extend(("C", ch) for ch in part)
    start_page = None
    for kind, ch in stream:
        if kind == "P":
            page = ch
            continue
        if start_page is None and ch.strip():
            start_page = page
        buf += ch
        if ch == "“":
            depth += 1
        elif ch == "”":
            depth = max(0, depth - 1)
            if depth == 0:                      # a quoted statute ends: close the sentence here
                out.append(re.sub(r"\s+", " ", buf).strip()); pages.append(start_page); buf = ""; start_page = None
                continue
        if ch == "." and depth == 0 and len(buf) > 40:
            out.append(re.sub(r"\s+", " ", buf).strip()); pages.append(start_page); buf = ""; start_page = None
    if buf.strip():
        out.append(re.sub(r"\s+", " ", buf).strip()); pages.append(start_page)
    res = []
    for s, pg in zip(out, pages):
        legal = s.count("“") > 0 and (s.find("“") < 25 or len(re.sub(r"“.*?”", "", s)) < 0.3 * len(s))
        res.append((s, legal, pg))
    return res


def main():
    R = [json.loads(l) for l in open(ROOT / "data" / "interim" / "narratives.jsonl", encoding="utf-8")]
    out = []
    for r in R:
        sents = sentences(r["text"])
        cand = {}
        for k, pat in CUES.items():
            cand[k] = [i for i, (s, legal, _) in enumerate(sents) if re.search(pat, s, re.I) and (not legal or k == "C9_review")]
        out.append(dict(report_id=r["report_id"], sec_no=r["sec_no"], title=r["title"], group=r["group"],
                        page_start=r["page_start"], page_end=r["page_end"],
                        sentences=[s for s, _, _ in sents], legal=[l for _, l, _ in sents],
                        pages=[p for _, _, p in sents], cand=cand))
    with open(ROOT / "data" / "interim" / "coding_candidates.jsonl", "w", encoding="utf-8") as f:
        for o in out:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    if "--show" in sys.argv:
        rid = sys.argv[sys.argv.index("--show") + 1]
        rng = sys.argv[sys.argv.index("--show") + 2:]
        for o in out:
            if o["report_id"] != rid:
                continue
            if rng and not (tuple(map(int, rng[0].split("."))) <= tuple(map(int, o["sec_no"].split("."))) <= tuple(map(int, rng[1].split(".")))):
                continue
            print(f"\n##### {o['sec_no']} {o['title']} [pp.{o['page_start']}-{o['page_end']}] n_sent={len(o['sentences'])}")
            shown = sorted(set(i for k in ("C1_purpose", "C5_outcome", "C6_data", "C7_addit", "C8_costeff", "M_method") for i in o["cand"][k]))
            for i in shown:
                tags = ",".join(k.split("_")[0] for k in o["cand"] if i in o["cand"][k])
                print(f"  [{i}|{tags}] {o['sentences'][i][:420]}")
            rv = [o["sentences"][i][:200] for i in o["cand"]["C9_review"] if re.search(r"sona er|tarihine kadar|süreyle|yıl süre|uzatıl|gözden geçir|mülga|kaldırıl", o["sentences"][i], re.I)]
            if rv:
                print("  C9:", " || ".join(rv[:3]))


if __name__ == "__main__":
    main()
