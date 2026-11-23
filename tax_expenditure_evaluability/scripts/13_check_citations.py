"""Check citation keys in paper/manuscript.md against paper/references.bib.
Prints: keys cited but missing from the bib, bib entries never cited, number of citations per key, and every
locator used with each key (for manual page checks). Exit code 1 if any key is missing or unused.
Usage: python3 scripts/13_check_citations.py"""
import re, sys, collections
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
md = (ROOT / "paper" / "manuscript.md").read_text(encoding="utf-8")
bib = (ROOT / "paper" / "references.bib").read_text(encoding="utf-8")
body = md.split("\n---\n", 1)[1] if md.startswith("---") else md
bibkeys = re.findall(r"^@\w+\{([^,]+),", bib, flags=re.M)
KEY = r"@([A-Za-z][\w:-]*\d{4}[a-z]?)"
cites = []
for grp in re.findall(r"\[([^\[\]]*@[^\[\]]*)\]", body):          # bracketed citations: [@a, p. 1; @b]
    for part in grp.split(";"):
        m = re.search(KEY + r"(?:,\s*(.+))?", part)
        if m: cites.append((m.group(1), (m.group(2) or "").strip()))
nobr = re.sub(r"\[[^\[\]]*@[^\[\]]*\]", "", body)
cites += [(k, "") for k in re.findall(r"(?<![\w.\[])" + KEY, nobr)]  # narrative citations: @a
count = collections.Counter(k for k, _ in cites)
loc = collections.defaultdict(set)
for k, l in cites:
    if l: loc[k].add(l.strip())
missing = sorted(set(count) - set(bibkeys))
unused = sorted(set(bibkeys) - set(count))
dups = [k for k, c in collections.Counter(bibkeys).items() if c > 1]
print(f"Distinct keys cited: {len(count)} | citation instances: {sum(count.values())} | bib entries: {len(bibkeys)}")
print("Cited but not in bib:", missing or "none")
print("In bib but never cited:", unused or "none")
print("Duplicate bib keys:", dups or "none")
for k in sorted(count):
    print(f"  {k:18} {count[k]:3}x  locators: {'; '.join(sorted(loc[k])) or '-'}")
sys.exit(1 if missing or unused or dups else 0)
