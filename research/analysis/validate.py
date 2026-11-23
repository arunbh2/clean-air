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

# orphan claims (not cited anywhere) -> warning
cited = set()
for f in glob.glob(os.path.join(D, "*.csv")):
    if os.path.basename(f) in ("claims.csv", "verification.csv"): continue
    cited |= set(re.findall(r"C\d{3}", open(f).read()))
for md_ in glob.glob(os.path.join(R, "**", "*.md"), recursive=True) + glob.glob(os.path.join(R, "..", "site", "templates", "*.html")):
    cited |= set(re.findall(r"C\d{3}", open(md_).read()))
for cid in claims:
    if cid not in cited: warns.append(f"orphan claim {cid} (not cited in tables or text)")
# ---- organisations atlas gates ----
CUT = "2026-11-22"
S_ROWS = {r["source_id"]: r for r in load("sources.csv")}
for s in S_ROWS.values():
    d = s["pub_date"][:10]
    if re.match(r"\d{4}", d) and d > CUT and not d.startswith(CUT[:4] + "-11-2"): errs.append(f"{s['source_id']}: published after cutoff ({d})")
    if not re.match(r"https?://", s["url"]): errs.append(f"{s['source_id']}: malformed URL")
if os.path.exists(os.path.join(D, "projects.csv")):
    orgs = load("organisations.csv"); O = {}
    CATS = {"community", "ngo", "research", "public", "funder", "multilateral", "private", "network"}
    countries_ok = {r["country_id"] for r in load("countries.csv")} | {"global", "regional", "maldives", "timor-leste"}
    for i, o in enumerate(orgs, 2):
        if o["org_id"] in O: errs.append(f"organisations.csv:{i} duplicate id {o['org_id']}")
        O[o["org_id"]] = o
        if not o.get("slug") or not re.fullmatch(r"[a-z0-9-]+", o["slug"]): errs.append(f"organisations.csv:{i} missing/bad slug")
        if o.get("category") not in CATS: errs.append(f"organisations.csv:{i} bad category {o.get('category')}")
        for cc in filter(None, (o.get("countries_active", "") + ";" + o.get("hq_country", "")).split(";")):
            if cc not in countries_ok: errs.append(f"organisations.csv:{i} unknown country {cc}")
        if o.get("website") and not o["website"].startswith("https://"): errs.append(f"organisations.csv:{i} insecure or malformed website")
        if not o.get("summary"): errs.append(f"organisations.csv:{i} empty summary")
        if o.get("category") == "private" and re.search(r"\b(proven|effective|best|impactful|verified)\b", o.get("summary", "") + o.get("why_it_matters", ""), re.I):
            errs.append(f"organisations.csv:{i} promotional wording in company record")
        if o.get("category") == "private" and o.get("record_origin", "").startswith("atlas") and "independent" in o.get("source_class", "") and not o.get("independent_test"):
            errs.append(f"organisations.csv:{i} claims independent source without a named test")
    projs = {r["project_id"]: r for r in load("projects.csv")}
    progs = {r["programme_id"] for r in load("programmes.csv")}
    for pid, p in projs.items():
        if not p["claim_ids"]: errs.append(f"projects.csv {pid}: no claims")
        if p["cost_amount"] and not (p["cost_currency"] and p["cost_type"] and p["source_ids"]): errs.append(f"projects.csv {pid}: amount without currency/type/source")
        if p["status"].startswith(("operating", "active")) and p["end_date"] and p["end_date"] < CUT[:7]: errs.append(f"projects.csv {pid}: ended but labelled {p['status']}")
        if p["air_quality_objective"] not in ("primary", "co-benefit", "unverified co-benefit"): errs.append(f"projects.csv {pid}: bad air_quality_objective")
        if re.search(r"\d", p["outcomes_measured"]) and "independent" not in p["evaluation_type"].lower() and "organisation-reported" not in p["outputs_reported"]:
            warns.append(f"projects.csv {pid}: numeric outcome without independent evaluation — check wording")
    ROLES_OK = {"grantmaker", "co-funder", "lender", "borrower", "implementer", "delivery partner", "technical partner", "supplier", "evaluator",
                "regulator", "public duty holder", "operator", "network member"}
    for i, r in enumerate(load("organisation-project-roles.csv"), 2):
        if r["organisation_id"] not in O: errs.append(f"roles:{i} unknown organisation {r['organisation_id']}")
        if r["project_id"] not in projs and r["project_id"] not in progs: errs.append(f"roles:{i} unknown project {r['project_id']}")
        if r["role"] not in ROLES_OK: errs.append(f"roles:{i} missing or unknown role '{r['role']}'")
        if not r["source_ids"]: errs.append(f"roles:{i} no source")
    for i, f in enumerate(load("funding-flows.csv"), 2):
        for k in ("funder_organisation_id", "recipient_organisation_id"):
            if f[k] and f[k] not in O: errs.append(f"flows:{i} unknown organisation {f[k]}")
        if f["project_id"] and f["project_id"] not in projs and f["project_id"] not in progs: errs.append(f"flows:{i} unknown project {f['project_id']}")
        if not f["public_source_ids"]: errs.append(f"flows:{i} no source")
        for sid in f["public_source_ids"].split(";"):
            if sid not in src: errs.append(f"flows:{i} unknown source {sid}")
            elif f["amount"] and S_ROWS[sid]["access_status"] == "search-snippet-only": errs.append(f"flows:{i} amount rests on a snippet")
        if f["amount"] and not (f["original_currency"] and f["approval_year"] and f["commitment_or_disbursement"]): errs.append(f"flows:{i} amount without currency/year/stage")
    print(f"atlas: {len(O)} organisations, {len(projs)} projects, {len(load('organisation-project-roles.csv'))} roles, {len(load('funding-flows.csv'))} flows")
print(f"{len(claims)} claims, {len(src)} sources, {len(ints)} interventions")
for w in sorted(set(warns)): print("WARN", w)
for e in errs: print("ERROR", e)
sys.exit(1 if errs else 0)
