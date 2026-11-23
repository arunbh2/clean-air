"""One canonical edit must reach every output in one build.

Run: python3 tools/test_propagation.py

In a scratch copy of research/ (the real files are never touched) the test:
  1. edits the text of claim C202 (cited by the low-cost sensors worked question and the CSTEP profile);
  2. withdraws claim C195 (cited by the Delhi informal workers question) and adds a corrections.csv entry,
     using clearly fake fixture wording that is never published;
then builds into a scratch dist and requires:
  - the edited text in the claim register (HTML and Markdown), llms-full.txt, claims.json, the published claims.csv,
    the sensors pack (HTML, Markdown, JSON) and the CSTEP profile;
  - C195 marked withdrawn in the claim register, claims.json and llms-full.txt; absent from the Delhi pack's known claims
    and listed in its withdrawn claims; the correction visible on the corrections page, in for-ai.json and in feed.xml;
  - the agent-file checker still passing on the scratch build.
"""
import csv, io, json, os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = "PROPAGATION-TEST-MARKER (fixture text, never published)"


def main():
    tmp = tempfile.mkdtemp(prefix="ca-prop-")
    res, dist = os.path.join(tmp, "research"), os.path.join(tmp, "dist")
    shutil.copytree(os.path.join(ROOT, "research"), res, ignore=shutil.ignore_patterns("exports", "__pycache__"))
    os.makedirs(os.path.join(res, "exports"))
    for f in os.listdir(os.path.join(ROOT, "research", "exports")):
        if f.endswith(".md"): shutil.copy(os.path.join(ROOT, "research", "exports", f), os.path.join(res, "exports", f))
    p = os.path.join(res, "data", "claims.csv")
    rows = list(csv.DictReader(open(p, encoding="utf-8"))); fields = list(rows[0].keys())
    for r in rows:
        if r["claim_id"] == "C202": r["claim"] = r["claim"] + " " + MARK
        if r["claim_id"] == "C195": r["status"] = "withdrawn"
    w = csv.DictWriter(open(p, "w", encoding="utf-8", newline=""), fieldnames=fields, lineterminator="\n"); w.writeheader(); w.writerows(rows)
    with open(os.path.join(res, "data", "corrections.csv"), "a", encoding="utf-8") as f:
        f.write('CRTEST,2026-11-23,claim,C195,withdrawn,Fixture: earlier wording,,Fixture reason for a test withdrawal (never published),,\n')
    env = dict(os.environ, CLEAN_AIR_RESEARCH=res, CLEAN_AIR_DIST=dist)
    out = subprocess.run([sys.executable, os.path.join(ROOT, "site", "build.py")], env=env, capture_output=True, text=True)
    if out.returncode: print(out.stdout[-2000:], out.stderr[-2000:]); return 1
    errs = []
    def has(rel, needle, want=True):
        t = open(os.path.join(dist, rel), encoding="utf-8").read()
        if (needle in t) != want: errs.append(f"{rel}: {'missing' if want else 'unexpected'} {needle[:60]!r}")
        return t
    for rel in ["evidence/claims.html", "evidence/claims.md", "llms-full.txt", "downloads/data/claims.json", "downloads/data/claims.csv",
                "packs/questions/low-cost-sensors.html", "packs/questions/low-cost-sensors.md", "packs/questions/low-cost-sensors.json",
                "organisations/o/cstep.html", "organisations/o/cstep.md"]:
        has(rel, MARK)
    ch = open(os.path.join(dist, "evidence/claims.html"), encoding="utf-8").read()
    row = ch.split('id="C195"', 1)[1].split("</tr>", 1)[0]
    if "Withdrawn" not in row: errs.append("claims.html: C195 not marked withdrawn")
    cj = {c["claim_id"]: c for c in json.load(open(os.path.join(dist, "downloads/data/claims.json")))["claims"]}
    if cj["C195"]["status"] != "withdrawn" or cj["C195"]["verification_state"] != "withdrawn": errs.append("claims.json: C195 not withdrawn")
    if "CRTEST" not in cj["C195"]["corrections"]: errs.append("claims.json: C195 lacks its correction link")
    pk = json.load(open(os.path.join(dist, "packs/questions/delhi-informal-workers.json")))
    if any(c["claim_id"] == "C195" for c in pk["known"]): errs.append("Delhi pack still lists withdrawn C195 as known")
    if not any(w["claim_id"] == "C195" for w in pk["withdrawn_claims"]): errs.append("Delhi pack does not list C195 as withdrawn")
    has("packs/questions/delhi-informal-workers.md", "C195 was withdrawn")
    has("about/corrections.html", 'id="CRTEST"'); has("about/corrections.md", "CRTEST")
    has("for-ai.json", "CRTEST"); has("feed.xml", "#CRTEST"); has("llms-full.txt", "CRTEST")
    chk = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "check_agent_files.py"), dist], capture_output=True, text=True)
    if chk.returncode: errs.append("check_agent_files failed on the propagated build: " + chk.stdout[-400:])
    shutil.rmtree(tmp)
    for e in errs: print("ERROR", e)
    print(f"propagation: {len(errs)} errors (1 edited claim and 1 withdrawal traced through HTML, Markdown, llms-full, JSON, CSV, packs, corrections, feed)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
