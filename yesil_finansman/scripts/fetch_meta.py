"""Fetch bibliographic metadata (CrossRef) and abstracts (OpenAlex, then Semantic Scholar) for a list of DOIs.

Usage: python3 scripts/fetch_meta.py dois.txt   (one 'key<TAB>doi' per line)
Raw JSON is cached in dogrulama/cache/. Output: dogrulama/meta_<listname>.json
Nothing is inferred: missing fields stay empty.
"""
import json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
C = ROOT / "dogrulama" / "cache"; C.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "academic-reference-check/1.0"}


def get(url, fname):
    f = C / fname
    if f.exists():
        return json.loads(f.read_text())
    for _ in range(3):
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40))
            f.write_text(json.dumps(d, ensure_ascii=False)); time.sleep(0.6); return d
        except urllib.error.HTTPError as e:
            if e.code == 404:
                f.write_text("null"); return None
            time.sleep(4)
        except Exception:
            time.sleep(4)
    return None


def inv(ab):
    if not ab:
        return ""
    pos = {}
    for w, ps in ab.items():
        for p in ps:
            pos[p] = w
    return " ".join(pos[i] for i in sorted(pos))


def main():
    lst = Path(sys.argv[1]); out = {}
    for line in lst.read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        key, doi = line.split("\t")[:2]
        safe = re.sub(r"[^\w.-]", "_", doi.lower())
        cr = get("https://api.crossref.org/works/" + urllib.parse.quote(doi), f"cr_{safe}.json")
        cr = (cr or {}).get("message") if cr else None
        oa = get("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi), f"oa_{safe}.json")
        ab = inv((oa or {}).get("abstract_inverted_index")) if oa else ""
        src = "openalex" if ab else ""
        if not ab:
            ss = get("https://api.semanticscholar.org/graph/v1/paper/DOI:" + urllib.parse.quote(doi) + "?fields=title,abstract,tldr", f"ss_{safe}.json")
            ab = (ss or {}).get("abstract") or ""
            src = "semanticscholar" if ab else ""
        rec = {"key": key, "doi": doi, "crossref_found": cr is not None}
        if cr:
            rec.update(title=(cr.get("title") or [""])[0], authors=[f"{a.get('family','')}, {a.get('given','')}" for a in cr.get("author", [])],
                       year=((cr.get("published-print") or cr.get("published-online") or cr.get("issued") or {}).get("date-parts") or [[None]])[0][0],
                       issued=(cr.get("issued", {}).get("date-parts") or [[None]])[0], journal=(cr.get("container-title") or [""])[0],
                       volume=cr.get("volume"), issue=cr.get("issue"), page=cr.get("page"), article_number=cr.get("article-number"),
                       type=cr.get("type"), publisher=cr.get("publisher"))
            if not ab and cr.get("abstract"):
                ab = re.sub(r"<[^>]+>", " ", cr["abstract"]); src = "crossref"
        rec["cited_by_openalex"] = (oa or {}).get("cited_by_count") if oa else None
        rec["abstract"] = re.sub(r"\s+", " ", ab).strip(); rec["abstract_source"] = src
        out[key] = rec
    (ROOT / "dogrulama" / f"meta_{lst.stem}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    for k, r in out.items():
        print(k, "| CR" if r["crossref_found"] else "| NO-CR", "|", r.get("year"), "|", (r.get("title") or "")[:60], "| abs:", r["abstract_source"] or "-")


if __name__ == "__main__":
    main()
