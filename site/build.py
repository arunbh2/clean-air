"""Build the Clean Air static site from the research files.

Run:  python3 site/build.py            -> writes site/dist/
Needs: Python 3.10+, jinja2, markdown (see site/requirements.txt), PyYAML.

Every page is generated from /research (Markdown, CSV and site-content). The templates hold
layout and interface labels only; no findings are written here. Change a rating in
research/data/*.csv and rebuild, and the site changes with it.
"""
import csv, html, json, os, re, shutil
from collections import OrderedDict
import markdown, yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.environ.get("CLEAN_AIR_RESEARCH", os.path.join(ROOT, "research"))
DATA = os.path.join(RES, "data")
DIST = os.environ.get("CLEAN_AIR_DIST", os.path.join(HERE, "dist"))
CUTOFF = "22 November 2026"
CUTOFF_ISO = "2026-11-22"

env = Environment(loader=FileSystemLoader(os.path.join(HERE, "templates")),
                  autoescape=select_autoescape(["html"]), trim_blocks=True, lstrip_blocks=True)

# ---------- data ----------
def load(name):
    return list(csv.DictReader(open(os.path.join(DATA, name), encoding="utf-8")))

def front(path):
    t = open(path, encoding="utf-8").read()
    m = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", t, re.S)
    return (yaml.safe_load(m.group(1)), m.group(2)) if m else ({}, t)

claims = OrderedDict((r["claim_id"], r) for r in load("claims.csv"))
sources = OrderedDict((r["source_id"], r) for r in load("sources.csv"))
verif = {r["claim_id"]: r for r in load("verification.csv")}
checks = {r["source_id"]: r for r in load("source-checks.csv")}
settings = load("settings.csv")
groups = load("community-impacts.csv")
orgs = load("organisations.csv")
ints = load("interventions.csv")
emap = load("evidence-map.csv")
gaps = load("evidence-gaps.csv")
econ = load("economic-estimates.csv")
paths = load("pathways.csv")
portfolios = load("portfolios.csv")
S_BY = {s["setting_id"]: s for s in settings}
I_BY = {i["int_id"]: i for i in ints}
G_BY = {g["group_id"]: g for g in groups}
sections = json.load(open(os.path.join(RES, "site-content", "sections.json"), encoding="utf-8"))
def load_opt(name):
    return load(name) if os.path.exists(os.path.join(DATA, name)) else []
countries = load_opt("countries.csv")
programmes = load_opt("programmes.csv")
funders = load_opt("funders.csv")
glossary = load_opt("glossary.csv")
dpaths = load_opt("decision-pathways.csv")
C_BY = {c["country_id"]: c for c in countries}
P_BY = {p["programme_id"]: p for p in programmes}
F_BY = {f["funder_id"]: f for f in funders}
GAP_BY = {g["gap_id"]: g for g in gaps}
DP_BY = {d["pathway_id"]: d for d in dpaths}
ARROW = {"Strong": "well established", "Moderate": "supported but context dependent",
         "Limited/mixed": "plausible / needs testing", "No adequate evidence found": "not yet established in this setting"}
reports = {}
for f in sorted(os.listdir(os.path.join(RES, "report"))):
    fm, body = front(os.path.join(RES, "report", f))
    reports[fm["id"]] = (fm, body)

NAV = [("crisis", "crisis/index.html"), ("people", "people/index.html"), ("places", "places/index.html"),
       ("what-works", "what-works/index.html"), ("organisations", "organisations/index.html"),
       ("evidence", "evidence/index.html")]

# ---------- helpers ----------
def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def cite_html(cid, rel):
    c = claims.get(cid)
    if not c:
        return f"[{cid}]"
    srcs = ", ".join(sources[s]["publisher"] or sources[s]["author_org"] for s in c["source_ids"].split(";") if s in sources)
    tip = (c["claim"][:180] + ("…" if len(c["claim"]) > 180 else "")) + f" — {srcs}"
    return (f'<a class="cite" href="{rel}evidence/claims.html#{cid}" title="{html.escape(tip, quote=True)}" '
            f'aria-label="Evidence {cid}">{cid}</a>')

def cites(text, rel):
    return re.sub(r"\[(C\d{3})\]", lambda m: cite_html(m.group(1), rel), text)

def claim_links(ids, rel):
    ids = [i for i in (ids or "").split(";") if i and i != "—"]
    return " ".join(cite_html(i, rel) for i in ids)

MD = markdown.Markdown(extensions=["tables", "sane_lists", "toc"], extension_configs={"toc": {"permalink": False}})

def md(text, rel, shift=0):
    MD.reset()
    out = MD.convert(cites(text, rel))
    if shift:
        def bump(m):
            n = min(int(m.group(2)) + shift, 6)
            return f"<{m.group(1)}h{n}"
        out = re.sub(r"<(/?)h([1-6])", bump, out)
    out = re.sub(r"<table>", '<table class="data">', out)
    # link file references in prose to their published equivalents
    out = re.sub(r"<code>data/([a-z0-9\-]+)\.csv</code>",
                 lambda m: f'<a href="{rel}downloads/data/{m.group(1)}.csv"><code>{m.group(1)}.csv</code></a>', out)
    out = out.replace("<code>VERIFICATION.md</code>", f'<a href="{rel}evidence/verification.html">verification record</a>')
    return out

def md_inline(text, rel):
    MD.reset()
    h = MD.convert(cites(text or "", rel))
    return re.sub(r"^<p>(.*)</p>$", r"\1", h.strip(), flags=re.S)

from bs4 import BeautifulSoup, NavigableString
NO_AUTOLINK = {"association", "exposure", "dose", "board-approval", "modelled-estimate", "causal-evidence"}  # common words: glossary page only
GLOSS = sorted([g for g in glossary if g["slug"] not in NO_AUTOLINK], key=lambda g: -len(g["term"]))
def glossify(html_text, rel):
    """Link the first use of each glossary term on a page ("Explain that")."""
    if not GLOSS: return html_text
    soup = BeautifulSoup(html_text, "html.parser"); used = set()
    skip = ["a", "code", "h1", "h2", "h3", "h4", "summary", "th", "caption", "script", "style", "title", "button", "label", "option"]
    queue = [n for n in soup.find_all(string=True) if not n.find_parent(skip)]
    while queue:
        node = queue.pop(0); text = str(node); best = None
        for g in GLOSS:
            if g["slug"] in used: continue
            label = g["term"].split(" (")[0]
            flags = 0 if sum(ch.isupper() for ch in label) >= 2 else re.I
            m = re.search(r"(?<![\\w-])" + re.escape(label) + r"(?![\\w-])", text, flags)
            if m and (best is None or m.start() < best[0].start()): best = (m, g)
        if not best: continue
        m, g = best; used.add(g["slug"])
        link = soup.new_tag("a", href=f"{rel}crisis/glossary.html#{g['slug']}")
        link["class"] = "term"; link["title"] = g["plain"]; link.string = m.group(0)
        before, after = soup.new_string(text[:m.start()]), soup.new_string(text[m.end():])
        node.replace_with(before); before.insert_after(link); link.insert_after(after)
        queue.insert(0, after)
    return str(soup)
def rating_class(v):
    v = (v or "").lower()
    if "limited effect" in v or "no meaningful effect" in v or "of no effect" in v: return "negative"
    if v.startswith("strong"): return "strong"
    if v.startswith("moderate"): return "moderate"
    if v.startswith("limited"): return "limited"
    if v.startswith("no adequate"): return "none"
    return ""

def badge(v):
    if not v or v == "—": return ""
    return f'<span class="badge {rating_class(v)}">{html.escape(v)}</span>'

def rec_badge(v):
    return f'<span class="badge {slug(v)}">{html.escape(v)}</span>' if v else ""

env.globals.update(ARROW=ARROW, badge=badge, rec_badge=rec_badge, CUTOFF=CUTOFF, CUTOFF_ISO=CUTOFF_ISO, sections=sections, NAV=NAV)
env.filters["md"] = lambda t, rel: md_inline(t, rel)
env.filters["claims"] = lambda ids, rel: claim_links(ids, rel)
env.filters["slug"] = slug

def toc_for(html_text):
    items = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', html_text)
    return items

pages = []
def render(path, template, title, description, section=None, crumbs=None, **ctx):
    depth = path.count("/")
    rel = "../" * depth
    out = env.get_template(template).render(rel=rel, path=path, title=title, description=description,
                                            section=section, crumbs=crumbs or [], **ctx)
    if ctx.get("glossify", True) and "<main" in out:
        a, rest = out.split("<main", 1); mid, b = rest.split("</main>", 1)
        out = a + "<main" + glossify(mid, rel) + "</main>" + b
    full = os.path.join(DIST, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(out)
    pages.append(path)

def report_html(rid, rel, shift=1):
    fm, body = reports[rid]
    return fm, md(body, rel, shift)

# ---------- build ----------
if os.path.exists(DIST): shutil.rmtree(DIST)
shutil.copytree(os.path.join(HERE, "static"), DIST)

# downloads
dl = os.path.join(DIST, "downloads"); os.makedirs(os.path.join(dl, "data"), exist_ok=True)
for f in sorted(os.listdir(DATA)):
    if f.endswith(".csv"): shutil.copy(os.path.join(DATA, f), os.path.join(dl, "data", f))
exports = []
ex_dir = os.path.join(RES, "exports")
for f in sorted(os.listdir(ex_dir)):
    if f.endswith(".pdf") or f.endswith(".md"):
        shutil.copy(os.path.join(ex_dir, f), os.path.join(dl, f)); exports.append(f)

# home
hfm, hbody = front(os.path.join(RES, "site-content", "home.md"))
prio_groups = [g for g in groups if g.get("priority_rank")]
mfm, _ = front(os.path.join(RES, "site-content", "home-modules.md"))
render("index.html", "home.html", "Clean Air", hfm["lede"], None, home=hfm, mods=mfm, I_BY=I_BY, GAP_BY=GAP_BY,
       body_html=md(hbody, "", 0), prio_groups=prio_groups)

# section pages built from report sections
def section_page(key, extra_template=None, **ctx):
    sec = sections[key]; rel = "../"
    arts = []
    for rid in sec["report"]:
        fm, h = report_html(rid, rel, 1)
        arts.append({"fm": fm, "html": h, "toc": toc_for(re.sub(r"<h3", "<h2", h))})
    render(f"{key}/index.html", extra_template or "section.html", sec["label"], sec["intro"], key,
           [("Clean Air", "index.html")], sec=sec, articles=arts, **ctx)

section_page("crisis")
section_page("people", "people.html", groups=groups)
section_page("places", "places.html", settings=settings)
section_page("what-works", "works.html", ints=ints)
section_page("organisations", "orgs.html", orgs=orgs)
section_page("support", "support.html", portfolios=portfolios, I_BY=I_BY, exports=exports)

# group pages
for g in groups:
    rs = [S_BY[s] for s in g["related_settings"].split(";") if s in S_BY]
    ri = [I_BY[i] for i in g["related_interventions"].split(";") if i in I_BY]
    render(f"people/{g['group_id']}.html", "group.html", g["group"],
           f"Exposure, impacts and protection for {g['group'].lower()}.", "people",
           [("Clean Air", "index.html"), ("People and livelihoods", "people/index.html")], g=g, rsettings=rs, rints=ri)

# setting pages
for s in settings:
    rg = [g for g in groups if s["setting_id"] in g["related_settings"].split(";")]
    render(f"places/{s['setting_id']}.html", "setting.html", s["name"], s["why_chosen"][:160], "places",
           [("Clean Air", "index.html"), ("Places", "places/index.html")], s=s, rgroups=rg)

# intervention pages
for i in ints:
    rg = [g for g in groups if i["int_id"] in g["related_interventions"].split(";")]
    rp = [p for p in portfolios if i["int_id"] in p["intervention_ids"].split(";")]
    em = [e for e in emap if set(e["claim_ids"].split(";")) & set(i["claim_ids"].split(";")) and e["kind"] == "intervention"]
    render(f"what-works/{i['int_id']}.html", "intervention.html", i["intervention"], i["what_it_does"][:160], "what-works",
           [("Clean Air", "index.html"), ("What works", "what-works/index.html")], i=i, rgroups=rg, rports=rp, emap=em)

# portfolio pages
for p in portfolios:
    pi = [I_BY[x] for x in p["intervention_ids"].split(";") if x in I_BY]
    render(f"support/{p['portfolio_id'].lower()}.html", "portfolio.html", p["name"], p["problem_and_population"][:160], "support",
           [("Clean Air", "index.html"), ("Where support could make a difference", "support/index.html")], p=p, pints=pi)

# decision brief and downloads
bfm, bbody = front(os.path.join(RES, "decision-brief.md"))
render("support/brief.html", "brief.html", "Decision brief", bfm.get("summary", ""), "support",
       [("Clean Air", "index.html"), ("Where support could make a difference", "support/index.html")],
       body_html=md(bbody, "../", 0), exports=exports)
render("support/downloads.html", "downloads.html", "Downloads", "Report, decision brief and every data table.", "support",
       [("Clean Air", "index.html"), ("Where support could make a difference", "support/index.html")],
       exports=exports, tables=sorted(f for f in os.listdir(DATA) if f.endswith(".csv")))

# evidence pages
ev_crumbs = [("Clean Air", "index.html"), ("Evidence", "evidence/index.html")]
section_page("evidence", "evidence.html")
render("evidence/claims.html", "claims.html", "Claim register", "Every factual claim, its sources and its verification status.",
       "evidence", ev_crumbs, claims=claims.values(), sources=sources, verif=verif)
render("evidence/sources.html", "sources.html", "Source register", "Every source with its URL, dates, type and access status.",
       "evidence", ev_crumbs, sources=sources.values(), checks=checks, claims=claims)
render("evidence/map.html", "map.html", "Evidence map", "Confidence that problems exist and that responses work, rated separately.",
       "evidence", ev_crumbs, emap=emap)
render("evidence/gaps.html", "gaps.html", "Evidence gaps", "Questions where an answer would change a funding decision.",
       "evidence", ev_crumbs, gaps=gaps)
render("evidence/economics.html", "economics.html", "Economic estimates", "Every economic figure with its population, method and limits.",
       "evidence", ev_crumbs, econ=econ)
render("evidence/pathways.html", "pathways.html", "Consequence pathways", "Each link from exposure to hardship, rated separately.",
       "evidence", ev_crumbs, paths=paths)
vfm, vbody = front(os.path.join(RES, "VERIFICATION.md"))
render("evidence/verification.html", "simple.html", "Verification record", "How every source and claim was re-checked.",
       "evidence", ev_crumbs, body_html=md(re.sub(r"\A# .*\n", "", vbody), "../", 0))
render("404.html", "simple.html", "Page not found", "Page not found.", None, [],
       body_html='<p>This page does not exist. Try the <a href="index.html">home page</a>.</p>')


# ---------- expansion pages ----------
def site_md(path):
    fm, body = front(os.path.join(RES, "site-content", path)); return fm, body
def fmt_amount(p):
    if not p["amount"]: return "Not published" if p["amount_type"] else "Not established"
    n = float(p["amount"]); cur = p["currency"]
    txt = f"{cur} {n/1e9:,.2f} billion" if n >= 1e9 else (f"{cur} {n/1e6:,.2f} million" if n >= 1e6 else f"{cur} {n:,.0f}")
    return f"{txt} ({p['amount_type']})"
env.globals.update(fmt_amount=fmt_amount, C_BY=C_BY, P_BY=P_BY, F_BY=F_BY, I_BY=I_BY, G_BY=G_BY, S_BY=S_BY, GAP_BY=GAP_BY, DP_BY=DP_BY)
home_c = [("Clean Air", "index.html")]
# Start here, glossary
sfm, sbody = site_md("start.md")
render("start/index.html", "simple.html", sfm["title"], sfm["summary"], None, home_c, body_html=md(sbody, "../", 0))
render("crisis/glossary.html", "glossary.html", "Glossary", "Plain-language definitions of the terms used on this site.", "crisis",
       home_c + [("The crisis", "crisis/index.html")], terms=sorted(glossary, key=lambda g: g["term"].lower()), glossify=False)
# journeys
for story in sorted(os.listdir(os.path.join(RES, "site-content", "stories"))):
    fm, body = site_md(os.path.join("stories", story))
    out = "people/journey-street-vendor.html" if fm["id"] == "journey-street-vendor" else "support/journey-funder.html"
    sec = fm["section"]; crumbs = home_c + [(sections[sec]["label"], f"{sec}/index.html")]
    render(out, "story.html", fm["title"], fm["answer"], sec, crumbs, st=fm, body_html=md(body, "../", 0))
# countries and regions
active = [c for c in countries if c["coverage_status"] != "research queue"]
for c in active:
    if c["country_id"] == "india": continue
    progs = [P_BY[x] for x in c["programme_ids"].split(";") if x in P_BY]
    rel_s = [S_BY[x] for x in c["related_settings"].split(";") if x in S_BY]
    rel_i = sorted({i for p in progs for i in p["intervention_ids"].split(";") if i in I_BY})
    render(f"places/{c['country_id']}.html", "country.html", c["name"], c["takeaway"], "places",
           home_c + [("Places", "places/index.html")], c=c, progs=progs, rsettings=rel_s, rints=[I_BY[i] for i in rel_i])
for region, slug_ in [("South Asia", "south-asia"), ("Southeast Asia", "southeast-asia")]:
    rc = [c for c in countries if c["region"] == region]
    render(f"places/{slug_}.html", "region.html", region, f"{region}: country dossiers and what is still in the research queue.", "places",
           home_c + [("Places", "places/index.html")], region=region, rcountries=rc, claims=claims)
render("places/compare.html", "compare_places.html", "Comparing countries fairly", "Comparable indicators only: one source, one method, one year.", "places",
       home_c + [("Places", "places/index.html")], cs=active)
# funding atlas
fa_c = home_c + [("Organisations", "organisations/index.html"), ("Who funded what?", "organisations/funding/index.html")]
render("organisations/funding/index.html", "funding.html", "Who funded what?", "Verified grants, loans, technical assistance and public budgets, with stage, amount type and source.", "organisations",
       home_c + [("Organisations", "organisations/index.html")], progs=programmes, funders=funders)
for p_ in programmes:
    render(f"organisations/funding/{p_['programme_id'].lower()}.html", "programme.html", p_["title"], p_["beneficiaries"], "organisations", fa_c, p=p_)
for f in funders:
    fp = [P_BY[x] for x in f["programme_ids"].split(";") if x in P_BY]
    render(f"organisations/funders/{f['funder_id']}.html", "funder.html", f["name"], f["role_in_this_edition"], "organisations", fa_c, f=f, fprogs=fp)
# what works: compare and not-a-solution
ww_c = home_c + [("What works", "what-works/index.html")]
render("what-works/compare.html", "compare.html", "Compare interventions", "Compare up to three interventions side by side, without a single score.", "what-works", ww_c, ints=ints)
render("what-works/not-a-solution.html", "not_solution.html", "What not to mistake for a solution", "Popular measures that the evidence does not support as air-quality investments, and why.", "what-works", ww_c,
       nots=[i for i in ints if i["recommendation"] == "Not recommended"])
# decision pathways
sp_c = home_c + [("Where support could make a difference", "support/index.html")]
render("support/pathways/index.html", "pathways_index.html", "For funders and decision-makers", "Six decision pathways, from protecting people now to building investable systems.", "support", sp_c, dps=dpaths)
for d in dpaths:
    render(f"support/pathways/{d['pathway_id'].lower()}.html", "pathway.html", d["name"], d["plain_question"], "support",
           sp_c + [("Pathways", "support/pathways/index.html")], d=d,
           dprogs=[P_BY[x] for x in d["example_programme_ids"].split(";") if x in P_BY],
           dints=[I_BY[x] for x in d["related_intervention_ids"].split(";") if x in I_BY])
# footer pages
for pg in sorted(os.listdir(os.path.join(RES, "site-content", "pages"))):
    fm, body = site_md(os.path.join("pages", pg))
    render(f"about/{pg.replace('.md', '.html')}", "simple.html", fm["title"], fm["summary"], None, home_c, body_html=md(body, "../", 0))
# coverage dashboard
from collections import Counter
cov = {
  "claims": len(claims), "claims_read": sum(1 for c in claims.values() if c["status"] == "read"),
  "claims_prov": [c for c in claims.values() if c["status"] == "provisional"],
  "sources": len(sources), "src_access": Counter(s["access_status"] for s in sources.values()),
  "src_type": Counter(s["source_type"] for s in sources.values()),
  "unreachable": [checks[k] for k in checks if checks[k]["reachable"] != "yes"],
  "countries": Counter(c["coverage_status"].split(" (")[0] for c in countries),
  "prog_cat": Counter(p["funding_category"] for p in programmes),
  "prog_ver": Counter(p["relationship_verification"].split(":")[0] for p in programmes),
  "prog_noamt": [p for p in programmes if not p["amount"]],
  "int_class": Counter(i.get("intervention_class", "") for i in ints),
  "int_ev": Counter(i["evidence_intervention"].split(" (")[0] for i in ints),
  "funder_queue": [f for f in funders if f["verification"] == "research queue"],
  "gaps": len(gaps), "glossary": len(glossary), "pathways": len(dpaths),
  "verified": sum(1 for v in verif.values() if v.get("manual_verdict") == "supported"),
}
render("evidence/coverage.html", "coverage.html", "Coverage and quality", "What this edition covers, how well it is sourced, and what is still open.", "evidence",
       home_c + [("Evidence", "evidence/index.html")], cov=cov, countries=countries)

# sitemap
open(os.path.join(DIST, "sitemap.txt"), "w").write("\n".join(sorted(pages)) + "\n")
print(f"built {len(pages)} pages into {DIST}")
