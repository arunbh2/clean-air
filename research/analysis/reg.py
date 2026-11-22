"""Append-only helpers for the source and claim registers.

Usage (from a script or heredoc):
    from reg import S, C
    s = S(title=..., org=..., publisher=..., pub_date=..., url=..., type=..., access=..., lang="en", notes="")
    C(section="01", claim="...", sources=[s], locator="p.3", etype="official-document", geo="India", period="2009", status="read")
S() returns the existing ID when the URL is already registered.
"""
import csv, os
D = os.path.join(os.path.dirname(__file__), "..", "data")
SRC = os.path.join(D, "sources.csv"); CLM = os.path.join(D, "claims.csv")
SF = ["source_id","title","author_org","publisher","pub_date","url","accessed","source_type","language","access_status","notes"]
CF = ["claim_id","section","claim","source_ids","locator","evidence_type","geography","period","status","notes"]
ACCESSED = "2026-11-22"
SOURCE_TYPES = {"official-dataset","official-document","legal-instrument","primary-study","systematic-review","evaluation",
                "modelled-estimate","community-research","organisational-report","journalism","testimony","programme-description","reference"}
ACCESS = {"full-text-read","abstract-only","search-snippet-only","unreachable"}
def _rows(p, f):
    if not os.path.exists(p):
        with open(p,"w",newline="") as fh: csv.writer(fh).writerow(f)
    return list(csv.DictReader(open(p)))
def S(title, org, publisher, pub_date, url, type, access, lang="en", notes=""):
    assert type in SOURCE_TYPES, type; assert access in ACCESS, access
    rows = _rows(SRC, SF)
    for r in rows:
        if r["url"] == url: return r["source_id"]
    sid = f"S{len(rows)+1:03d}"
    with open(SRC,"a",newline="") as fh:
        csv.writer(fh).writerow([sid,title,org,publisher,pub_date,url,ACCESSED,type,lang,access,notes])
    return sid
def C(section, claim, sources, locator="", etype="", geo="", period="", status="read", notes=""):
    assert status in {"read","provisional"}
    rows = _rows(CLM, CF)
    cid = f"C{len(rows)+1:03d}"
    with open(CLM,"a",newline="") as fh:
        csv.writer(fh).writerow([cid,section,claim,";".join(sources),locator,etype,geo,period,status,notes])
    return cid
