"""Checks for Latest Signals (docs/live-signals-master-brief.md, section 10, points 10-13).

Run:  python3 tools/check_signals.py [research_dir] [dist_dir]
      python3 tools/check_signals.py --self-test   (injects faults into scratch copies; every family must fire)
Families:
  data       store, registry and review decisions validate (tools/signals/validate.py)
  feeds      the site's feed.xml still holds only site updates and corrections; signals/feed.xml holds only dated external records
  parity     every public record appears in HTML (as an anchor), JSON and the Markdown mirror, with the same link
  links      every record link is an HTTPS URL; no javascript:, data:, localhost or site-root links on signal pages
  evidence   no evidence-strength badge inside a signal; no signal URL in a verified funding record; ingestion cannot create claims
  refresh    the refresh time shown equals status.json, and the page says "delayed" when the last success is too old
  routes     signal pages, feeds and exports sit under the configured base URL
"""
import csv, glob, json, os, re, shutil, sys, tempfile
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "signals"))
import validate  # noqa: E402

ATOM = "{http://www.w3.org/2005/Atom}"


def rd(p): return list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.exists(p) else []


def check(res, dist):
    errs = []
    base = os.environ.get("CLEAN_AIR_BASE_URL", json.load(open(os.path.join(ROOT, "site", "site.json")))["base_url"]).rstrip("/") + "/"
    store = json.load(open(os.path.join(res, "signals", "signals.json"), encoding="utf-8"))
    status = json.load(open(os.path.join(res, "signals", "status.json"), encoding="utf-8"))
    errs += ["data: " + e for e in validate.validate_store(store, res) + validate.validate_registry(res) + validate.validate_reviews(res, {r["signal_id"] for r in store["records"]})]
    need = ["signals/index.html", "signals/sources.html", "signals/how-it-works.html", "signals/recently-indexed.html", "signals/awaiting-assessment.html",
            "signals/missing.html", "signals/feed.xml", "downloads/data/signals.json", "downloads/data/signals.csv", "downloads/schemas/signals.schema.json"]
    for n in need:
        if not os.path.exists(os.path.join(dist, n)): errs.append(f"routes: {n} was not generated")
    if errs and any(e.startswith("routes") for e in errs): return errs
    # feeds
    site_feed = ET.parse(os.path.join(dist, "feed.xml")).getroot()
    if "updates and corrections" not in (site_feed.findtext(ATOM + "title") or ""): errs.append("feeds: feed.xml title changed; it is reserved for site updates and corrections")
    n_expected = len(rd(os.path.join(res, "data", "changelog.csv"))) + len(rd(os.path.join(res, "data", "corrections.csv")))
    entries = site_feed.findall(ATOM + "entry")
    if len(entries) != n_expected: errs.append(f"feeds: feed.xml has {len(entries)} entries, expected {n_expected} (changelog + corrections only)")
    for e in entries:
        if "/signals/" in (e.findtext(ATOM + "id") or "") or "sig-" in (e.findtext(ATOM + "id") or ""): errs.append("feeds: feed.xml contains a signal entry")
    sf = ET.parse(os.path.join(dist, "signals", "feed.xml")).getroot()
    for e in sf.findall(ATOM + "entry"):
        href = e.find(ATOM + "link").get("href", "")
        if not href.startswith("https://"): errs.append(f"feeds: signals feed entry link is not HTTPS: {href[:80]}")
        if not re.match(r"\d{4}-\d{2}-\d{2}T", e.findtext(ATOM + "published") or ""): errs.append("feeds: signals feed entry without a publication date")
        if not (e.findtext(ATOM + "id") or "").startswith(base + "signals/sig-"): errs.append("feeds: signals feed entry id outside the base URL")
    # parity
    exp = json.load(open(os.path.join(dist, "downloads", "data", "signals.json"), encoding="utf-8"))
    pages = {}
    for f in glob.glob(os.path.join(dist, "signals", "**", "*.html"), recursive=True): pages[os.path.relpath(f, dist)] = open(f, encoding="utf-8").read()
    anchors = {}
    for rel, t in pages.items():
        for m in re.finditer(r'<li class="sig"([^>]*)>(.*?)</li>', t, re.S):
            i = re.search(r'\bid="(sig-[0-9a-f]{12})"', m.group(1))
            if i: anchors.setdefault(i.group(1), []).append((rel, m.group(2)))
    for r in exp["records"]:
        page_rel = r["page_url"][len(base):].split("#")[0]
        if not r["page_url"].startswith(base): errs.append(f"routes: {r['signal_id']} page_url outside the base URL")
        hits = [x for x in anchors.get(r["signal_id"], []) if x[0] == page_rel]
        if not hits: errs.append(f"parity: {r['signal_id']} has no anchor on {page_rel}"); continue
        if f'href="{r["canonical_url"].replace("&", "&amp;")}"' not in hits[0][1]: errs.append(f"parity: {r['signal_id']} link on {page_rel} differs from JSON")
        mdp = os.path.join(dist, page_rel[:-5] + ".md")
        if os.path.exists(mdp) and r["title_original"][:40].replace("_", "") not in open(mdp, encoding="utf-8").read().replace("_", "").replace("\\", ""):
            errs.append(f"parity: {r['signal_id']} title missing from the Markdown mirror {page_rel[:-5]}.md")
    pub_ids = {r["signal_id"] for r in store["records"]} - {d["signal_id"] for d in rd(os.path.join(res, "signals", "review-decisions.csv")) if d["review_status"] in ("excluded", "withdrawn")}
    if pub_ids != {r["signal_id"] for r in exp["records"]}: errs.append("parity: signals.json does not hold exactly the public records of the store")
    # links and evidence markers inside signal items, on every page that shows signals
    allpages = glob.glob(os.path.join(dist, "**", "*.html"), recursive=True)
    for f in allpages:
        t = open(f, encoding="utf-8").read()
        if 'class="sig"' not in t: continue
        rel = os.path.relpath(f, dist)
        for li in re.findall(r'<li class="sig".*?</li>', t, re.S):
            for h in re.findall(r'<h3 class="sig-title"><a href="([^"]+)"', li):
                if not h.startswith("https://") or "localhost" in h: errs.append(f"links: {rel} has a signal link that is not an external HTTPS URL: {h[:60]}")
            if re.search(r'class="badge|class="rec-badge', li): errs.append(f"evidence: {rel} shows an evidence badge inside a signal")
        if rel.startswith("signals/") and re.search(r'href="(/(?!/)|javascript:|data:|http://localhost)', t): errs.append(f"links: {rel} has a site-root, javascript:, data: or localhost link")
    # funding records never rest on a signal
    urls = {r["canonical_url"] for r in store["records"]}
    for fn in ("programmes.csv", "funding-flows.csv"):
        for i, row in enumerate(rd(os.path.join(res, "data", fn)), 2):
            if set(row.values()) & urls or any("sig-" in v for v in row.values()): errs.append(f"evidence: {fn}:{i} rests on a signal; verified funding records need the funding protocol")
    # refresh
    idx = pages.get("signals/index.html", "")
    m = re.search(r'data-refreshed="([^"]*)"', idx)
    if not m or m.group(1) != (status.get("last_successful_refresh") or ""): errs.append("refresh: the index shows a refresh time different from status.json")
    if "Feed refresh delayed" not in idx: errs.append("refresh: the delayed-refresh message is missing from the index")
    if exp.get("last_successful_refresh") != status.get("last_successful_refresh"): errs.append("refresh: signals.json last_successful_refresh differs from status.json")
    idx_text = re.sub(r'\s(?:title|aria-label|data-[\w-]+)="[^"]*"', "", idx)   # claim tooltips quote register text (e.g. "real-time stations"); check page copy only
    if re.search(r"updated just now|live feed|real-time", idx_text, re.I): errs.append("refresh: the index claims live or real-time updating")
    return errs


def self_test():
    tmp = tempfile.mkdtemp(prefix="ca-sig-"); res = os.path.join(tmp, "research"); dist = os.path.join(tmp, "dist")
    shutil.copytree(os.path.join(ROOT, "research"), res, ignore=shutil.ignore_patterns("exports", "report", "__pycache__"))
    shutil.copytree(os.path.join(ROOT, "site", "dist"), dist, ignore=shutil.ignore_patterns("llms-full.txt", "packs"))
    store = json.load(open(os.path.join(res, "signals", "signals.json"), encoding="utf-8"))
    r0 = store["records"][0]
    # feeds: a signal leaks into the site feed
    f = os.path.join(dist, "feed.xml"); t = open(f, encoding="utf-8").read()
    open(f, "w", encoding="utf-8").write(t.replace("</feed>", f"<entry><title>x</title><id>https://x/signals/{r0['signal_id']}</id></entry></feed>"))
    # links + evidence: a javascript link and an evidence badge inside a signal on the index
    f = os.path.join(dist, "signals", "index.html"); t = open(f, encoding="utf-8").read()
    t = t.replace('<h3 class="sig-title"><a href="https://', '<h3 class="sig-title"><a href="javascript:alert(1)//https://', 1)
    t = t.replace('<p class="sig-status">', '<p class="sig-status"><span class="badge strong">Strong</span>', 1)
    t = re.sub(r'data-refreshed="[^"]*"', 'data-refreshed="2020-01-01T00:00:00Z"', t)           # refresh: wrong stamp
    open(f, "w", encoding="utf-8").write(t)
    # parity: drop one record's anchor from its archive page
    exp = json.load(open(os.path.join(dist, "downloads", "data", "signals.json"), encoding="utf-8"))
    pr = exp["records"][-1]["page_url"].split("/clean-air/")[-1].split("#")[0]
    p = os.path.join(dist, pr); t = open(p, encoding="utf-8").read()
    open(p, "w", encoding="utf-8").write(t.replace(f'id="{exp["records"][-1]["signal_id"]}"', 'id="sig-000000000000"'))
    # evidence: a funding record citing a signal URL; data: ingestion-side promotion
    with open(os.path.join(res, "data", "programmes.csv"), "a", encoding="utf-8") as fh: fh.write(f"P98,{r0['canonical_url']}\n")
    store["records"][0]["review_status"] = "evidence_promoted"
    json.dump(store, open(os.path.join(res, "signals", "signals.json"), "w", encoding="utf-8"))
    e = check(res, dist); shutil.rmtree(tmp)
    fams = {x.split(":")[0] for x in e}
    print(f"signals self-test: injected faults -> {len(e)} errors, families {sorted(fams)}")
    for x in e[:10]: print("   ", x)
    return 0 if {"data", "feeds", "parity", "links", "evidence", "refresh"} <= fams else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv: sys.exit(self_test())
    a = [x for x in sys.argv[1:] if not x.startswith("-")]
    e = check(a[0] if a else os.path.join(ROOT, "research"), a[1] if len(a) > 1 else os.path.join(ROOT, "site", "dist"))
    for x in e[:80]: print("ERROR", x)
    print(f"signals: {len(e)} errors")
    sys.exit(1 if e else 0)
