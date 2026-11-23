"""Check the agent-readable layer of a built Clean Air site.

Run:  python3 tools/check_agent_files.py [dist]          (default site/dist)
      python3 tools/check_agent_files.py --self-test       (a damaged copy of the build must fail)

Checks:
  presence     llms.txt, llms-full.txt, for-ai.{html,json,txt}, sitemap.{xml,json,txt}, robots.txt, feed.xml,
               packs/index.json, downloads/data/{catalogue,claims,organisations-atlas}.json
  mirrors      every HTML page (except 404) has a .md mirror; the page declares it with rel="alternate" type="text/markdown";
               the mirror keeps every claim ID and every h2 heading of the HTML page (no silent omissions)
  links        every URL in llms.txt, sitemap.json and the pack index is under the configured base URL and maps to a file in dist
  corpus       llms-full.txt contains a section for every mirrored page and states the cutoff
  packs        every pack JSON parses, has a short answer, at least one known claim or an explicit statement, cutoff and URLs
  capabilities public files do not claim an API, endpoint, authentication or live data the static site does not have
  sync         every corrections.csv entry appears on the corrections page, in for-ai.json and in the feed; withdrawn claims
               are marked withdrawn in claims.json and never listed as "known" in a pack
  csv          every published CSV is free of spreadsheet formula triggers
  feed/xml     feed.xml and sitemap.xml are well-formed XML
"""
import csv, glob, io, json, os, re, shutil, sys, tempfile
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "site"))
from csvsafe import is_safe

BASE = os.environ.get("CLEAN_AIR_BASE_URL", json.load(open(os.path.join(ROOT, "site", "site.json")))["base_url"]).rstrip("/") + "/"
REQUIRED = ["llms.txt", "llms-full.txt", "for-ai/index.html", "for-ai.json", "for-ai.txt", "sitemap.xml", "sitemap.json", "sitemap.txt",
            "robots.txt", "feed.xml", "packs/index.json", "downloads/data/catalogue.json", "downloads/data/claims.json",
            "downloads/data/organisations-atlas.json", "about/corrections.html", "about/reuse.html"]
OVERCLAIM = re.compile(r"\b(REST API|our API|API endpoint|query endpoint|real-time|live data feed|log ?in to|API key|OAuth|content negotiation)\b", re.I)
NEGATED = re.compile(r"\b(no|not|without|none)\b[^.]{0,80}$", re.I)


def to_file(url, dist):
    if not url.startswith(BASE): return None
    return os.path.join(dist, url[len(BASE):].split("#")[0])


def check(dist):
    errs = []
    for f in REQUIRED:
        if not os.path.exists(os.path.join(dist, f)): errs.append(f"presence: {f} missing")
    if errs: return errs
    html_pages = [l for l in open(os.path.join(dist, "sitemap.txt")).read().split() if l != "404.html"]
    for p in html_pages:
        h = open(os.path.join(dist, p), encoding="utf-8").read()
        mpath = os.path.join(dist, p[:-5] + ".md")
        if not os.path.exists(mpath): errs.append(f"mirrors: {p} has no Markdown mirror"); continue
        if f'rel="alternate" type="text/markdown" href="{BASE}{p[:-5]}.md"' not in h: errs.append(f"mirrors: {p} does not declare its mirror")
        m = open(mpath, encoding="utf-8").read()
        main = h.split("<main", 1)[-1].split("</main>", 1)[0]
        cids = set(re.findall(r"claims\.html#(C\d{3})", main)); mids = set(re.findall(r"claims\.html#(C\d{3})", m))
        if cids - mids: errs.append(f"mirrors: {p}.md drops claim IDs {sorted(cids - mids)[:5]}")
        for h2 in re.findall(r"<h2[^>]*>(.*?)</h2>", main, re.S):
            t = re.sub(r"<[^>]+>", "", h2).strip()
            if t and t not in m: errs.append(f"mirrors: {p}.md lacks heading '{t[:50]}'"); break
        if "research_cutoff:" not in m: errs.append(f"mirrors: {p}.md lacks cutoff metadata")
    llms = open(os.path.join(dist, "llms.txt"), encoding="utf-8").read()
    if not llms.startswith("# "): errs.append("links: llms.txt does not start with an H1")
    if "> " not in llms: errs.append("links: llms.txt lacks a summary blockquote")
    urls = re.findall(r"\]\((https?://[^)]+)\)", llms)
    sm = json.load(open(os.path.join(dist, "sitemap.json")))
    urls += [x["html"] for x in sm["pages"]] + [x["markdown"] for x in sm["pages"]] + sm["data"]
    pidx = json.load(open(os.path.join(dist, "packs", "index.json")))
    for pk in pidx["packs"]: urls += [pk["json_url"], pk["html_url"], pk["markdown_url"]]
    for u in urls:
        f = to_file(u, dist)
        if f is None: errs.append(f"links: {u} is not under base {BASE}")
        elif not os.path.exists(f): errs.append(f"links: {u} -> missing file")
    full = open(os.path.join(dist, "llms-full.txt"), encoding="utf-8").read()
    for p in html_pages:
        if f"===== PAGE: {BASE}{p} =====" not in full: errs.append(f"corpus: llms-full.txt lacks {p}"); break
    if "Research cutoff: 2026-11-22" not in full: errs.append("corpus: llms-full.txt does not state the cutoff")
    claims = json.load(open(os.path.join(dist, "downloads", "data", "claims.json")))
    withdrawn = {c["claim_id"] for c in claims["claims"] if c["status"] == "withdrawn"}
    if not pidx["packs"]: errs.append("packs: no packs")
    for pk in pidx["packs"]:
        d = json.load(open(to_file(pk["json_url"], dist)))
        for k in ("short_answer", "known", "uncertainties", "source_ids", "research_cutoff", "html_url", "markdown_url"):
            if k not in d: errs.append(f"packs: {pk['pack_id']} lacks {k}")
        if not d.get("short_answer"): errs.append(f"packs: {pk['pack_id']} has an empty answer")
        if not d.get("known") and not d.get("uncertainties"): errs.append(f"packs: {pk['pack_id']} has neither known claims nor stated uncertainty")
        bad = {c["claim_id"] for c in d.get("known", [])} & withdrawn
        if bad: errs.append(f"sync: pack {pk['pack_id']} lists withdrawn claims {sorted(bad)} as known")
    for f in ["llms.txt", "for-ai.txt", "for-ai.json", "robots.txt", "downloads/data/catalogue.json", "about/reuse.md"]:
        t = open(os.path.join(dist, f), encoding="utf-8").read()
        for m in OVERCLAIM.finditer(t):
            if not NEGATED.search(t[max(0, m.start() - 120):m.start()]): errs.append(f"capabilities: {f} claims '{m.group(0)}' without negation")
    corr_csv = os.path.join(dist, "downloads", "data", "corrections.csv")
    if os.path.exists(corr_csv):
        rows = list(csv.DictReader(open(corr_csv, encoding="utf-8")))
        page = open(os.path.join(dist, "about", "corrections.html"), encoding="utf-8").read()
        fa = json.load(open(os.path.join(dist, "for-ai.json")))
        feed = open(os.path.join(dist, "feed.xml"), encoding="utf-8").read()
        for r in rows:
            cid = r["correction_id"]
            if f'id="{cid}"' not in page: errs.append(f"sync: {cid} missing from corrections page")
            if cid not in {x["correction_id"] for x in fa.get("corrections", [])}: errs.append(f"sync: {cid} missing from for-ai.json")
            if f"#{cid}" not in feed: errs.append(f"sync: {cid} missing from feed.xml")
            if r["change_type"] == "withdrawn" and r["record_id"] not in withdrawn: errs.append(f"sync: {r['record_id']} withdrawn in corrections but not in claims.json")
    for f in glob.glob(os.path.join(dist, "downloads", "data", "*.csv")):
        bad = is_safe(open(f, encoding="utf-8").read())
        if bad: errs.append(f"csv: {os.path.basename(f)} has formula-trigger cells, e.g. row {bad[0][0]}: {bad[0][2][:30]!r}")
    for f in ["feed.xml", "sitemap.xml"]:
        try: ET.parse(os.path.join(dist, f))
        except ET.ParseError as e: errs.append(f"xml: {f} is not well-formed ({e})")
    for f in glob.glob(os.path.join(dist, "downloads", "schemas", "*.json")):
        s = json.load(open(f))
        if "$schema" not in s or "properties" not in s: errs.append(f"schema: {os.path.basename(f)} malformed")
    return errs


def self_test():
    """Copy the real build, damage it in four ways, and require each damage to be caught."""
    dist = os.path.join(ROOT, "site", "dist")
    if not os.path.exists(os.path.join(dist, "llms.txt")):
        print("agent self-test: build the site first"); return 1
    tmp = tempfile.mkdtemp(prefix="ca-agent-")
    bad = os.path.join(tmp, "dist"); shutil.copytree(dist, bad)
    os.remove(os.path.join(bad, "evidence", "claims.md"))                                         # missing mirror
    with open(os.path.join(bad, "llms.txt"), "a") as f: f.write(f"\n- [Ghost]({BASE}no-such-page.md)\n")  # dead link
    with open(os.path.join(bad, "for-ai.txt"), "a") as f: f.write("\nQuery our REST API for live data.\n")  # over-claim
    with open(os.path.join(bad, "downloads", "data", "sources.csv"), "a") as f: f.write('S999,"=HYPERLINK(""http://x"")",a,b,c,d,e,f,g,h,i\n')  # injection
    e = check(bad)
    kinds = {x.split(":")[0] for x in e}
    need = {"mirrors", "links", "capabilities", "csv"}
    print(f"agent self-test: damaged build -> {len(e)} errors, kinds {sorted(kinds)}")
    shutil.rmtree(tmp)
    return 0 if need <= kinds else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv: sys.exit(self_test())
    dist = next((a for a in sys.argv[1:] if not a.startswith("-")), os.path.join(ROOT, "site", "dist"))
    e = check(dist)
    for x in e[:200]: print("ERROR", x)
    print(f"agent files: {len(e)} errors")
    sys.exit(1 if e else 0)
