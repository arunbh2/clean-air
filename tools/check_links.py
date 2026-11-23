"""Internal links, anchors and external-URL shape for the built site (no network needed).

Run:  python3 tools/check_links.py [dist]       |   python3 tools/check_links.py --self-test
- every relative href/src in every HTML page resolves to a file in dist, and every #anchor to an id on that page
- every absolute link under the site's base URL (Markdown mirrors, canonical, llms.txt) maps to a file in dist
- every external http(s) URL is well formed (scheme, host, no spaces). Whether a remote site answers is NOT
  tested here: that is recorded per source in research/data/source-checks.csv as opened / could not be checked
  automatically, because remote sites that block bots would otherwise make CI fail for reasons unrelated to the site.
- reader pages (groups, interventions, countries, packs, profiles, section indexes) open with a plain-language
  first answer (.simple-answer / "In one sentence") and link onward (no dead ends)
"""
import glob, json, os, re, shutil, sys, tempfile
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.environ.get("CLEAN_AIR_BASE_URL", json.load(open(os.path.join(ROOT, "site", "site.json")))["base_url"]).rstrip("/") + "/"
FIRST_ANSWER = [r"^[a-z-]+/index\.html$", r"^people/(?!journey).+\.html$", r"^what-works/(?!index|compare|not-a-solution).+\.html$",
                r"^places/(?!index|compare|south-asia|southeast-asia).+\.html$", r"^packs/.+/.+\.html$", r"^organisations/o/.+\.html$",
                r"^organisations/funding/p\d+\.html$"]
FIRST_ANSWER_EXEMPT = {"evidence/index.html", "start/index.html", "for-ai/index.html", "packs/index.html", "about/index.html"}


def check(dist):
    errs, ids, cache = [], {}, {}
    pages = sorted(os.path.relpath(p, dist) for p in glob.glob(os.path.join(dist, "**", "*.html"), recursive=True))
    def ids_of(rel):
        if rel not in ids:
            t = open(os.path.join(dist, rel), encoding="utf-8").read()
            ids[rel] = set(re.findall(r'\bid="([^"]+)"', t))
        return ids[rel]
    for rel in pages:
        t = open(os.path.join(dist, rel), encoding="utf-8").read()
        for attr, href in re.findall(r'\b(href|src)="([^"]*)"', t):
            if not href or href.startswith(("mailto:", "data:", "javascript:")): continue
            if href.startswith(("http://", "https://")):
                u = urlparse(href)
                if not u.netloc or " " in href or "." not in u.netloc: errs.append(f"external: {rel}: malformed URL {href[:80]}")
                if href.startswith(BASE):
                    f = href[len(BASE):].split("#")[0]
                    if f and not os.path.exists(os.path.join(dist, f)): errs.append(f"internal: {rel}: {href} -> missing file")
                continue
            path, _, frag = href.partition("#")
            target = os.path.normpath(os.path.join(os.path.dirname(rel), path)) if path else rel
            if not os.path.exists(os.path.join(dist, target)): errs.append(f"internal: {rel}: {href} -> missing {target}"); continue
            if frag and target.endswith(".html") and frag not in ids_of(target): errs.append(f"anchor: {rel}: {href} -> no id '{frag}'")
        if rel not in FIRST_ANSWER_EXEMPT and any(re.match(p, rel) for p in FIRST_ANSWER):
            main = t.split("<main", 1)[-1]
            if not re.search(r'class="[^"]*simple-answer|In one sentence', main): errs.append(f"reader: {rel} has no plain-language first answer")
            if len(re.findall(r'<a href="(?!https?:)[^"#][^"]*"', main)) < 3: errs.append(f"reader: {rel} is a dead end (fewer than 3 onward links)")
    return errs, len(pages)


def self_test():
    tmp = tempfile.mkdtemp(prefix="ca-links-"); d = os.path.join(tmp, "dist"); os.makedirs(os.path.join(d, "people"))
    open(os.path.join(d, "people", "x.html"), "w").write('<main><h1>X</h1><p><a href="missing.html">a</a> <a href="#nowhere">b</a> '
                                                         '<a href="https://exa mple">c</a></p></main>')
    e, _ = check(d); shutil.rmtree(tmp)
    kinds = {x.split(":")[0] for x in e}
    print(f"links self-test: bad fixture -> {len(e)} errors, kinds {sorted(kinds)}")
    return 0 if {"internal", "anchor", "external", "reader"} <= kinds else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv: sys.exit(self_test())
    dist = next((a for a in sys.argv[1:] if not a.startswith("-")), os.path.join(ROOT, "site", "dist"))
    e, n = check(dist)
    for x in e[:100]: print("ERROR", x)
    print(f"links and reader paths: {len(e)} errors across {n} pages")
    sys.exit(1 if e else 0)
