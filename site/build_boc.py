# A Breath of Change integration (World Bank, 2025). Executed by site/build.py after the main and atlas pages and before
# build_map.py. Canonical data: research/breath-of-change/*.csv and research/site-content/*.md; every fact cites a claim.
BOC = os.path.join(RES, "breath-of-change")
def boc_load(n): return list(csv.DictReader(open(os.path.join(BOC, n), encoding="utf-8")))
BOC_ORIG, BOC_4I, BOC_DP = boc_load("origins.csv"), boc_load("four-is.csv"), boc_load("delivery-pathways.csv")
BOC_NAMED, BOC_CH, BOC_EXT = boc_load("report-named-orgs.csv"), boc_load("chapter-map.csv"), boc_load("extraction.csv")
BOC_NAMED_BY = {o["atlas_org_id"]: o for o in BOC_NAMED if o["atlas_org_id"]}
env.globals.update(BOC_NAMED_BY=BOC_NAMED_BY)
for f in ["origins.csv", "four-is.csv", "delivery-pathways.csv", "report-named-orgs.csv", "chapter-map.csv", "extraction.csv"]:
    open(os.path.join(DIST, "downloads", "data", "breath-of-change-" + f), "w", encoding="utf-8").write(
        safe_csv_text(open(os.path.join(BOC, f), encoding="utf-8").read()))
def boc_render(path, md_name, kind, section, crumbs, **ctx):
    fm_, body_ = site_md(md_name)
    render(path, "boc_page.html", fm_["title"], fm_["summary"], section, crumbs, fm=fm_, body_html=md(body_, "../" * path.count("/"), 0), kind=kind, **ctx)
boc_render("places/where-air-comes-from.html", "where-air-comes-from.md", "origins", "places", home_c + [("Places", "places/index.html")], origins=BOC_ORIG)
boc_render("what-works/four-is.html", "four-is.md", "fouris", "what-works", home_c + [("What works", "what-works/index.html")], fouris=BOC_4I, ints=ints)
boc_render("what-works/delivery.html", "delivery.md", "delivery", "what-works", home_c + [("What works", "what-works/index.html")], pathways=BOC_DP)
boc_render("evidence/breath-of-change.html", "breath-of-change.md", "guide", "evidence", home_c + [("Evidence", "evidence/index.html")],
           chapters=BOC_CH, extraction=BOC_EXT, named=BOC_NAMED)
afm_, abody_ = site_md("one-airshed.md")
render("places/one-airshed.html", "simple.html", afm_["title"], afm_["summary"], "places", home_c + [("Places", "places/index.html")], body_html=md(abody_, "../", 0))
