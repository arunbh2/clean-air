"""Generate docs/SOURCE_REGISTER.md from research/data/sources.csv and source-checks.csv.
Run: python3 research/analysis/source_register.py"""
import csv, os
R = os.path.join(os.path.dirname(__file__), "..")
src = list(csv.DictReader(open(os.path.join(R, "data", "sources.csv"))))
chk = {r["source_id"]: r for r in csv.DictReader(open(os.path.join(R, "data", "source-checks.csv")))}
cl = list(csv.DictReader(open(os.path.join(R, "data", "claims.csv"))))
uses = {}
for c in cl:
    for s in c["source_ids"].split(";"):
        uses.setdefault(s, []).append(c["claim_id"])
out = ["# Source register", "", "Generated from `research/data/sources.csv`. Do not edit by hand; run `python3 research/analysis/source_register.py`.", "",
       f"Research cutoff 22 November 2026 · {len(src)} sources", "",
       "| ID | Title | Publisher | Published | Type | Access | Reachable at last check | Claims |", "|---|---|---|---|---|---|---|---|"]
for s in src:
    k = chk.get(s["source_id"], {})
    t = s["title"].replace("|", "/")
    out.append(f"| {s['source_id']} | [{t}]({s['url']}) | {s['publisher']} | {s['pub_date']} | {s['source_type']} | {s['access_status']} | {k.get('reachable','not checked')} ({k.get('checked','')}) | {', '.join(uses.get(s['source_id'], []))} |")
open(os.path.join(R, "..", "docs", "SOURCE_REGISTER.md"), "w").write("\n".join(out) + "\n")
print(len(src), "sources written")
