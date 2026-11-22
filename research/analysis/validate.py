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
for md in glob.glob(os.path.join(R, "report", "*.md")) + glob.glob(os.path.join(R, "*.md")) + glob.glob(os.path.join(R, "site-content", "*.md")):
    for cid in re.findall(r"\[(C\d{3})\]", open(md).read()):
        if cid not in claims: errs.append(f"{os.path.basename(md)}: unknown claim {cid}")
print(f"{len(claims)} claims, {len(src)} sources, {len(ints)} interventions")
for w in sorted(set(warns)): print("WARN", w)
for e in errs: print("ERROR", e)
sys.exit(1 if errs else 0)
