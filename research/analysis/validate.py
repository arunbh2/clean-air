"""Check referential integrity of the research registers and tables.

Run: python3 research/analysis/validate.py
- every claim's source_ids exist in sources.csv
- every claim_ids / source_ids / intervention_ids reference in the tables resolves
- every [Cnnn] cited in report Markdown resolves
- ratings use only the four permitted labels
Exits non-zero on any error.
"""
import csv, glob, os, re, sys
D = os.path.join(os.path.dirname(__file__), "..", "data")
R = os.path.join(os.path.dirname(__file__), "..")
load = lambda n: list(csv.DictReader(open(os.path.join(D, n))))
src = {r["source_id"] for r in load("sources.csv")}
claims = {r["claim_id"]: r for r in load("claims.csv")}
ints = {r["int_id"] for r in load("interventions.csv")}
settings = {r["setting_id"] for r in load("settings.csv")}
errs, warns = [], []
for c in claims.values():
    for s in filter(None, c["source_ids"].split(";")):
        if s not in src: errs.append(f"{c['claim_id']}: unknown source {s}")
RATINGS = {"Strong","Moderate","Limited/mixed","No adequate evidence found","Limited","—"}
for f in glob.glob(os.path.join(D, "*.csv")):
    name = os.path.basename(f)
    if name in ("sources.csv", "claims.csv"): continue
    for i, r in enumerate(csv.DictReader(open(f)), 2):
        for col in ("claim_ids",):
            for cid in filter(lambda x: x and x != "—", r.get(col, "").split(";")):
                if cid not in claims: errs.append(f"{name}:{i} unknown claim {cid}")
                elif claims[cid]["status"] == "provisional": warns.append(f"{name}:{i} cites provisional {cid}")
        for sid in filter(lambda x: x and x != "—", r.get("source_ids", "").split(";")):
            if sid not in src: errs.append(f"{name}:{i} unknown source {sid}")
        for sid in filter(None, r.get("related_settings", "").split(";")):
            if sid not in settings: errs.append(f"{name}:{i} unknown setting {sid}")
        for iid in filter(None, (r.get("intervention_ids", "") + ";" + r.get("related_interventions", "")).split(";")):
            if iid not in ints: errs.append(f"{name}:{i} unknown intervention {iid}")
        for col in ("evidence_confidence","confidence","rating_problem_exists","evidence_problem","confidence"):
            v = r.get(col)
            if v and v.split(" (")[0] not in RATINGS: errs.append(f"{name}:{i} bad rating '{v}' in {col}")
for md in glob.glob(os.path.join(R, "report", "*.md")) + glob.glob(os.path.join(R, "*.md")) + glob.glob(os.path.join(R, "site-content", "*.md")) + glob.glob(os.path.join(R, "site-content", "*", "*.md")):
    for cid in re.findall(r"\[(C\d{3})\]", open(md).read()):
        if cid not in claims: errs.append(f"{os.path.basename(md)}: unknown claim {cid}")

# ---- expansion collections (countries, programmes, funders, pathways, glossary) ----
def ids_of(name, key):
    rows = load(name); seen = set()
    for r in rows:
        if r[key] in seen: errs.append(f"{name}: duplicate id {r[key]}")
        seen.add(r[key])
    return rows, seen
if os.path.exists(os.path.join(D, "programmes.csv")):
    progs, prog_ids = ids_of("programmes.csv", "programme_id")
    funders, funder_ids = ids_of("funders.csv", "funder_id")
    countries, country_ids = ids_of("countries.csv", "country_id")
    CATS = {"philanthropic", "development-public", "private-blended", "prospective"}
    for r in progs:
        pid = r["programme_id"]
        for f in filter(None, r["funder_ids"].split(";")):
            if f not in funder_ids: errs.append(f"programmes.csv {pid}: unknown funder {f}")
        if r["funding_category"] not in CATS: errs.append(f"programmes.csv {pid}: bad funding_category")
        if r["country"] not in country_ids and r["country"] != "regional": errs.append(f"programmes.csv {pid}: unknown country {r['country']}")
        if r["amount"] and not (r["amount_type"] and r["currency"] and r["source_ids"]):
            errs.append(f"programmes.csv {pid}: amount without amount_type, currency or source")
        if not r["relationship_verification"]: errs.append(f"programmes.csv {pid}: missing relationship_verification")
        if not r["source_ids"]: errs.append(f"programmes.csv {pid}: no source")
        if "snippet" in r["relationship_verification"] and r["amount"]:
            errs.append(f"programmes.csv {pid}: amount resting on a search snippet")
    for r in funders:
        for x in filter(None, r["programme_ids"].split(";")):
            if x not in prog_ids: errs.append(f"funders.csv {r['funder_id']}: unknown programme {x}")
    for r in countries:
        for x in filter(None, r["programme_ids"].split(";")):
            if x not in prog_ids: errs.append(f"countries.csv {r['country_id']}: unknown programme {x}")
        if r["coverage_status"] != "research queue" and not r["claim_ids"]:
            errs.append(f"countries.csv {r['country_id']}: dossier without claims")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["last_reviewed"]): errs.append(f"countries.csv {r['country_id']}: bad last_reviewed date")
    for r in load("decision-pathways.csv"):
        for x in filter(None, r["example_programme_ids"].split(";")):
            if x not in prog_ids: errs.append(f"decision-pathways.csv {r['pathway_id']}: unknown programme {x}")
        for x in filter(None, r["related_intervention_ids"].split(";")):
            if x not in ints: errs.append(f"decision-pathways.csv {r['pathway_id']}: unknown intervention {x}")
    for r in load("interventions.csv"):
        for x in filter(None, r.get("regional_cases", "").split(";")):
            if x not in prog_ids: errs.append(f"interventions.csv {r['int_id']}: unknown programme {x}")
    for name in ("sources.csv",):
        for r in load(name):
            if not r["url"].startswith("http"): errs.append(f"{name} {r['source_id']}: URL missing")

print(f"{len(claims)} claims, {len(src)} sources, {len(ints)} interventions")
for w in sorted(set(warns)): print("WARN", w)
for e in errs: print("ERROR", e)
sys.exit(1 if errs else 0)
