"""Checks for the A Breath of Change integration (docs/breath-of-change-integration-brief.md, section 6).

Run:  python3 tools/check_boc.py [research_dir] [dist_dir]
      python3 tools/check_boc.py --self-test   (injects a wrong WHO target, a bogus funding record, an orphaned claim and a
                                               mismatched unit into scratch copies; every one must be caught)
Rules:
  target      "35 by 35" is always called aspirational or interim, and never equated with the WHO guideline (5 µg/m³)
  origins     geographic-origin and emitting-sector shares stay in separate rows and tables, each with period, method, page
              and a percentage unit; chart values the book did not print are marked, not estimated
  locators    every claim citing the book (S182) has a page locator and a row in the extraction register with printed and PDF pages
  funding     no funding record (programmes.csv, funding-flows.csv) rests on the book: a World Bank recommendation is not a grant
  kinds       claims registered as 'proposed measure' read as proposals ("propose"), and company-reported case studies say so;
              no systems-map edge rated Strong or Moderate rests only on proposal claims
"""
import csv, glob, os, re, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
TARGET = re.compile(r"35 by 35|35 µg/m³ by 2035|35 µg/m3 by 2035", re.I)
QUALIFY = re.compile(r"aspirational|interim|milestone|stepping|under consideration|considering", re.I)
EQUATE = re.compile(r"WHO(?:'s)? (?:air[- ]quality )?guideline (?:level |value )?(?:of |is |at )?35|35 by 35[^.]{0,60}\b(?:is|equals|matches|meets) the WHO (?:air[- ]quality )?guideline", re.I)


def rd(p): return list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.exists(p) else []


def text_blocks(dist):
    for f in glob.glob(os.path.join(dist, "**", "*.html"), recursive=True) + glob.glob(os.path.join(dist, "**", "*.md"), recursive=True):
        t = open(f, encoding="utf-8").read()
        t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", t, flags=re.S)
        for block in re.split(r"</p>|</li>|</td>|</dd>|\n\n", t):
            plain = re.sub(r"<[^>]+>", " ", block)
            plain = re.sub(r"\u201c[^\u201d]*\u201d", " ", plain)   # quoted source passages are the book's words, not the site's
            if TARGET.search(plain) or "guideline" in plain: yield os.path.relpath(f, dist), re.sub(r"\s+", " ", plain)


def check(res, dist=None):
    errs = []
    data, boc = os.path.join(res, "data"), os.path.join(res, "breath-of-change")
    claims = {c["claim_id"]: c for c in rd(os.path.join(data, "claims.csv"))}
    ext = {r["claim_id"]: r for r in rd(os.path.join(boc, "extraction.csv"))}
    for cid, r in ext.items():
        if cid not in claims: errs.append(f"locators: extraction register row {cid} has no claim")
        if r["source_id"] == "S182" and (not r["printed_pages"] or not r["pdf_pages"]): errs.append(f"locators: {cid} lacks printed or PDF pages")
    for cid, c in claims.items():
        if "S182" in c["source_ids"].split(";"):
            if not re.search(r"\bpp?\. ?[\divxl]", c["locator"]): errs.append(f"locators: {cid} cites the book without a page locator")
            if cid not in ext: errs.append(f"locators: {cid} cites the book but has no extraction-register row")
        kind = c.get("notes", "")
        if "claim kind: proposed measure" in kind and "propos" not in c["claim"].lower(): errs.append(f"kinds: {cid} is a proposal but does not read as one")
        if "company-reported" in kind and not re.search(r"report|company", c["claim"], re.I): errs.append(f"kinds: {cid} is company-reported but does not say so")
    for row in rd(os.path.join(boc, "origins.csv")):
        if row["metric"] not in ("geographic origin", "emitting sector"): errs.append(f"origins: unknown metric '{row['metric']}' for {row['jurisdiction']}")
        if not row["period"] or not row["method"] or not row["printed_page"]: errs.append(f"origins: {row['jurisdiction']}/{row['category']} lacks period, method or page")
        numeric = re.search(r"\d", row["value"]) and "not printed" not in row["value"]
        if numeric and "%" not in row["unit"]: errs.append(f"origins: {row['jurisdiction']}/{row['category']} value {row['value']} has unit '{row['unit']}', not a percentage")
        if not numeric and "not printed" not in row["value_status"] and "chart only" not in row["value_status"]: errs.append(f"origins: {row['jurisdiction']} non-numeric value without a 'not printed' status")
    proposal_claims = {cid for cid, c in claims.items() if "claim kind: proposed" in c.get("notes", "")}
    boc_claims = {cid for cid, c in claims.items() if "S182" in c["source_ids"]}
    for f in ("programmes.csv", "funding-flows.csv"):
        for i, r in enumerate(rd(os.path.join(data, f)), 2):
            srcs = set((r.get("source_ids", "") + ";" + r.get("public_source_ids", "")).split(";"))
            cl = set(r.get("claim_ids", "").split(";"))
            if "S182" in srcs or cl & boc_claims: errs.append(f"funding: {f}:{i} rests on A Breath of Change; a recommendation is not a funding record")
    for e in rd(os.path.join(res, "systems-map", "edges.csv")):
        cs = [x for x in e["claim_ids"].split(";") if x]
        if cs and set(cs) <= proposal_claims and e["strength"] in ("Strong", "Moderate"): errs.append(f"kinds: edge {e['edge_id']} rated {e['strength']} rests only on proposals")
    if dist:
        tables = 0
        page = os.path.join(dist, "places", "where-air-comes-from.html")
        if os.path.exists(page):
            for t in re.findall(r"<table.*?</table>", open(page, encoding="utf-8").read(), re.S):
                tables += 1
                if ">Local<" in t and "Household cooking" in t: errs.append("origins: one table mixes geographic origin and emitting sector")
            if tables < 2: errs.append("origins: origin and sector shares are not in two separate tables")
        for rel, b in text_blocks(dist):
            if EQUATE.search(b): errs.append(f"target: {rel} equates 35 µg/m³ with the WHO guideline: '{b[:120]}'")
            elif TARGET.search(b) and not QUALIFY.search(b) and "35 by 35" in b: errs.append(f"target: {rel} mentions 35 by 35 without calling it aspirational or interim: '{b[:120]}'")
    return errs


def self_test():
    tmp = tempfile.mkdtemp(prefix="ca-boc-"); res = os.path.join(tmp, "research"); dist = os.path.join(tmp, "dist")
    shutil.copytree(os.path.join(ROOT, "research"), res, ignore=shutil.ignore_patterns("exports", "report", "__pycache__"))
    with open(os.path.join(res, "data", "programmes.csv"), "a", encoding="utf-8") as f:   # bogus funding record built on the book
        f.write("P99,Regional clean air fund (fixture),regional,IGP-HF,world-bank,development-public,Grant,,,,Cross-sector,,1000000000,USD,proposed,2026,awarded,operating,cut PM2.5 by half,primary,verified,public good,PM2.5 halved,independent,S182,C262,fixture\n")
    with open(os.path.join(res, "breath-of-change", "extraction.csv"), "a", encoding="utf-8") as f:   # orphaned claim ID
        f.write("C999,S182,Ch. 2,22,74,attribution model,IGP-HF,2020-24,,add,places,\n")
    with open(os.path.join(res, "breath-of-change", "origins.csv"), "a", encoding="utf-8") as f:     # mismatched unit
        f.write("Delhi,India,emitting sector,Transport,39,µg/m³,2020-24,GAINS model,xxi,21,stated in text\n")
    os.makedirs(os.path.join(dist, "places"))
    open(os.path.join(dist, "places", "fixture.html"), "w").write("<main><p>The region aims for 35 by 35, which is the WHO guideline of 35 µg/m³.</p><p>Countries back 35 by 35.</p></main>")
    e = check(res, dist); shutil.rmtree(tmp)
    kinds = {x.split(":")[0] for x in e}
    print(f"breath-of-change self-test: injected faults -> {len(e)} errors, families {sorted(kinds)}")
    for x in e[:8]: print("   ", x)
    return 0 if {"funding", "locators", "origins", "target"} <= kinds else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv: sys.exit(self_test())
    a = [x for x in sys.argv[1:] if not x.startswith("-")]
    res = a[0] if a else os.path.join(ROOT, "research"); dist = a[1] if len(a) > 1 else os.path.join(ROOT, "site", "dist")
    e = check(res, dist if os.path.exists(dist) else None)
    for x in e: print("ERROR", x)
    print(f"breath of change: {len(e)} errors")
    sys.exit(1 if e else 0)
