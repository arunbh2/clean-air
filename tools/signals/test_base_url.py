"""Latest Signals under a different base URL (brief section 10, point 12): build into a scratch directory with
CLEAN_AIR_BASE_URL set to another host and path, then require every signals output to follow it and none to keep the old host."""
import glob, json, os, subprocess, sys, tempfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
old = json.load(open(os.path.join(ROOT, "site", "site.json")))["base_url"]
new = "https://clean-air.example.org/moved/"
tmp = tempfile.mkdtemp(prefix="ca-base-")
env = dict(os.environ, CLEAN_AIR_BASE_URL=new, CLEAN_AIR_DIST=os.path.join(tmp, "dist"))
r = subprocess.run([sys.executable, os.path.join(ROOT, "site", "build.py")], env=env, capture_output=True, text=True)
errs = [] if r.returncode == 0 else ["build failed: " + r.stderr[-500:]]
if not errs:
    files = glob.glob(os.path.join(tmp, "dist", "signals", "**", "*.*"), recursive=True) + [os.path.join(tmp, "dist", "downloads", "data", "signals.json")]
    for f in files:
        t = open(f, encoding="utf-8").read()
        if old in t: errs.append(f"{os.path.relpath(f, tmp)} still uses {old}")
    d = json.load(open(os.path.join(tmp, "dist", "downloads", "data", "signals.json")))
    if not all(x["page_url"].startswith(new) for x in d["records"]): errs.append("signals.json page_url does not follow the base URL")
    feed = open(os.path.join(tmp, "dist", "signals", "feed.xml"), encoding="utf-8").read()
    if f'href="{new}signals/feed.xml" rel="self"' not in feed: errs.append("signals feed self link does not follow the base URL")
    c = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "check_signals.py"), os.path.join(ROOT, "research"), os.path.join(tmp, "dist")], env=env, capture_output=True, text=True)
    if c.returncode: errs.append("check_signals under the new base URL: " + c.stdout[-400:])
shutil.rmtree(tmp)
for e in errs: print("ERROR", e)
print(f"signals base-URL test: {len(errs)} errors (built with {new})")
sys.exit(1 if errs else 0)
