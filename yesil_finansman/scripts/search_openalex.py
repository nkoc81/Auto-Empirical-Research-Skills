"""Search OpenAlex for candidate literature per topic (journal articles, English).
Writes dogrulama/aday_<topic>.json with title, year, venue, doi, cited_by_count, abstract.
Selection for the paper is done by reading the abstracts; this script only retrieves candidates."""
import json, sys, time, urllib.parse, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "academic-reference-check/1.0"}
TOPICS = {
 "t1_local_env_invest": "municipal climate investment financing local government",
 "t2_muni_green_bond": "green municipal bonds greenium",
 "t3_green_budget_local": "green budgeting local government climate budget",
 "t4_eco_fiscal_transfer": "ecological fiscal transfers",
 "t5_credit_climate_risk": "municipal bonds climate risk credit rating",
 "t6_nbs_finance": "financing nature-based solutions urban green infrastructure",
 "t7_dev_bank_blended": "subnational climate finance development banks blended finance cities",
 "t8_green_gentrification": "green gentrification urban greening displacement",
 "t9_fiscal_federalism_climate": "fiscal federalism climate change subnational governments",
 "t10_green_bond_outcomes": "green bonds environmental impact emissions outcomes",
}


def inv(ab):
    if not ab: return ""
    pos = {p: w for w, ps in ab.items() for p in ps}
    return " ".join(pos[i] for i in sorted(pos))


def run(key, q, frm=2018):
    url = ("https://api.openalex.org/works?per-page=40&sort=cited_by_count:desc&search=" + urllib.parse.quote(q) +
           f"&filter=from_publication_date:{frm}-01-01,type:article,language:en")
    d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
    out = []
    for w in d.get("results", []):
        out.append(dict(title=w.get("title"), year=w.get("publication_year"), doi=(w.get("doi") or "").replace("https://doi.org/", ""),
                        venue=((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
                        cited=w.get("cited_by_count"), authors=[a["author"]["display_name"] for a in w.get("authorships", [])][:6],
                        abstract=inv(w.get("abstract_inverted_index"))))
    (ROOT / "dogrulama" / f"aday_{key}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    return out


if __name__ == "__main__":
    for k, q in TOPICS.items():
        r = run(k, q); time.sleep(1)
        print("==", k, len(r))
        for x in r[:40]:
            print(f"  {x['year']} | {x['cited']:>5} | {(x['venue'] or '')[:28]:28} | {(x['title'] or '')[:95]}")
