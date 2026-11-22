"""Functional test: changing a rating in research/data changes the generated site.

Copies /research to a temporary folder, changes the smog-tower recommendation from
"Not recommended" to "Fund now", builds into a temporary dist, and checks the page.
Run: python3 site/qa/rating_change_test.py
"""
import csv, os, re, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
tmp = tempfile.mkdtemp(prefix="clean-air-qa-")
res, dist = os.path.join(tmp, "research"), os.path.join(tmp, "dist")
shutil.copytree(os.path.join(ROOT, "research"), res)
p = os.path.join(res, "data", "interventions.csv")
rows = list(csv.DictReader(open(p))); F = list(rows[0].keys())
for r in rows:
    if r["int_id"] == "smog-towers": r["recommendation"] = "Fund now"; r["evidence_intervention"] = "Moderate"
w = csv.DictWriter(open(p, "w", newline=""), fieldnames=F); w.writeheader(); w.writerows(rows)
env = dict(os.environ, CLEAN_AIR_RESEARCH=res, CLEAN_AIR_DIST=dist)
subprocess.run([sys.executable, os.path.join(ROOT, "site", "build.py")], env=env, check=True, capture_output=True)
changed = open(os.path.join(dist, "what-works", "smog-towers.html")).read()
original = open(os.path.join(ROOT, "site", "dist", "what-works", "smog-towers.html")).read()
ok = ('badge fund-now">Fund now' in changed and 'badge moderate">Moderate' in changed
      and 'badge not-recommended">Not recommended' in original)
listing = open(os.path.join(dist, "what-works", "index.html")).read()
ok = ok and len(re.findall(r'data-rec="Fund now"', listing)) == 5
print("rating change propagates to site:", "pass" if ok else "FAIL")
shutil.rmtree(tmp)
sys.exit(0 if ok else 1)
