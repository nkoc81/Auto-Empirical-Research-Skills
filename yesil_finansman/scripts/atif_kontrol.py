"""Cross-check in-text citations against the reference list (APA 7, Turkish 've'/'vd.').
Usage: python3 scripts/atif_kontrol.py calisma/metin_gelistirilmis.md
Prints: citations without reference, references never cited, word counts, DOI duplicates."""
import re, sys, collections
s = open(sys.argv[1], encoding="utf-8").read()
body, refs = s.split("# KAYNAKÇA")
body = re.sub(r"^---.*?---", "", body, flags=re.S)
main = body.split("# 1. GİRİŞ")[1]
oz = body.split("# 1. GİRİŞ")[0]
ref_entries = [r.strip() for r in refs.strip().split("\n\n") if r.strip()]

def surname_key(name):
    k = name.strip().rstrip(".").lower().replace("’", "'")
    return re.sub(r"'(n[ıiuü]n|[ıiuü]n|nde|de|ye|e|a)$", "", k)

refkeys = {}
for r in ref_entries:
    m = re.match(r"(.+?)\((\d{4})\)\.", r)
    auth, yr = m.group(1), m.group(2)
    parts = [p.strip() for p in re.split(r",\s*(?:&\s*)?|\s&\s", auth) if p.strip() and p.strip() != "…"]
    sur = [p for p in parts if not re.fullmatch(r"([A-ZÇŞÖÜİ]\.\s?-?)+( de [A-Za-z]\.)?( [A-Z]\.)*|[A-Z]\.-[A-Z]\.|…", p)]
    sur = [x for x in sur if not re.fullmatch(r"(?:[A-ZÇŞÖÜİ][a-z]?\.\s?)+(?:\s?[a-z]+\s[A-Z][a-z]?\.\s?[A-Z]?\.?)?", x)]
    first = sur[0] if sur else parts[0]
    n = len(sur)
    if first.startswith("World Commission"): first, n = "WCED", 1
    refkeys[(surname_key(first), yr)] = dict(ref=r[:90], n=n, cited=0, second=surname_key(sur[1]) if n == 2 else None)

# in-text patterns: "X (2020)", "X ve Y (2020)", "X vd. (2020)", "(X, 2020; Y ve Z, 2021)", "OECD (2022, 2024)"
cites = []
name = r"(?:[A-Z]\.\s)?(?:de |den |Op de |Short )?[A-ZÇŞÖÜİ][\w'’\-ıİşŞğĞüÜöÖçÇ]+(?:\s[A-ZÇŞÖÜİ][\w\-ıİşŞğĞüÜöÖçÇ]+)?"
for m in re.finditer(rf"({name})(?:\s(ve)\s({name})|\s(vd\.))?(?:'(?:n[ıiuü]n|[ıiuü]n|e|a|nde|de|ye))?\s\((\d{{4}}(?:,\s\d{{4}})*)\)", main):
    for y in re.findall(r"\d{4}", m.group(5)):
        cites.append((m.group(1), m.group(3), bool(m.group(4)), y))
for grp in re.findall(r"\(([^()]*\d{4}[^()]*)\)", main):
    for c in grp.split(";"):
        m = re.match(rf"\s*({name})(?:\s(ve)\s({name})|\s(vd\.))?,\s(\d{{4}}(?:,\s\d{{4}})*)\s*$", c)
        if m:
            for y in re.findall(r"\d{4}", m.group(5)):
                cites.append((m.group(1), m.group(3), bool(m.group(4)), y))

missing = []
for first, second, vd, y in cites:
    k1 = surname_key(re.sub(r"^[A-Z]\.\s", "", first))
    hit = [k for k in refkeys if k[1] == y and (k[0] == k1 or k[0].endswith(k1) or k1.endswith(k[0]))]
    if not hit:
        missing.append(f"{first}{' ve '+second if second else ''}{' vd.' if vd else ''} ({y})"); continue
    for k in hit:
        refkeys[k]["cited"] += 1
        r = refkeys[k]
        if r["n"] >= 3 and not vd: missing.append(f"FORMAT: {first} ({y}) should use 'vd.'")
        if r["n"] == 2 and (vd or not second): missing.append(f"FORMAT: {first} ({y}) should name both authors")
        if r["n"] == 1 and (vd or second): missing.append(f"FORMAT: {first} ({y}) single author")

print("Citation instances found:", len(cites))
print("Citations without matching reference / format problems:", sorted(set(missing)) or "none")
unc = [v["ref"] for v in refkeys.values() if v["cited"] == 0]
print("References never cited in body:", unc or "none")
print("Reference entries:", len(ref_entries))
dois = re.findall(r"https://doi.org/(\S+)", refs)
print("DOIs:", len(dois), "duplicates:", [d for d, c in collections.Counter(d.lower() for d in dois).items() if c > 1] or "none")
words = lambda t: len(re.findall(r"\w+", re.sub(r"[#*|\-]", " ", t)))
print("Words: abstract", words(oz.split("**Anahtar")[0].replace("ÖZ", "")), "| main text (Giriş→Sonuç, incl. table)", words(main))
for k, v in sorted(refkeys.items()):
    print(f"  {v['cited']:2}x  {k[0]} {k[1]}")
