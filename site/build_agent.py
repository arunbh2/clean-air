# Second half of the build: evidence packs, the page for AI assistants, the corrections register, and the
# machine-readable layer (Markdown mirrors, llms.txt, llms-full.txt, sitemaps, feed, data catalogue, schemas).
# Executed by site/build.py in the same namespace, after every content page has been rendered, so every
# output below is generated from the same canonical records (research/) as the HTML pages.
# Nothing here writes facts of its own: text comes from research/data/*.csv and research/site-content/*.md.
import datetime, xml.sax.saxutils as sx

MD_FOR = lambda p: p[:-5] + ".md"


def funding_stage(term):
    """Map a source's own stage wording to the brief's vocabulary without inferring missing stages."""
    t = (term or "").lower()
    if not t: return "stage not stated"
    if t.startswith("announced"): return "announced"
    if "approved" in t: return "approved"
    if t.startswith("awarded"): return "committed (awarded)"
    if "paid" in t or "disbursed" in t: return "disbursed"
    if "legally" in t: return "legal obligation (not a funding stage)"
    return "stage not specified in source"


def src_entry(sid):
    s = sources.get(sid)
    if not s: return {"source_id": sid}
    return {"source_id": sid, "title": s["title"], "publisher": s["publisher"] or s["author_org"], "pub_date": s["pub_date"],
            "url": s["url"], "accessed": s["accessed"], "source_type": s["source_type"], "access_status": s["access_status"],
            "register_url": f"{BASE_URL}evidence/sources.html#{sid}"}


def claim_entry(cid):
    c = claims[cid]
    return {"claim_id": cid, "text": c["claim"], "place": c["geography"], "period": c["period"], "status": c["status"],
            "verification_state": c["_state"], "verification_label": c["_state_label"], "provenance": c["_provenance"],
            "locator": c["locator"], "supporting_excerpt": c["_excerpt"], "source_ids": split(c["source_ids"]),
            "sources": [src_entry(s) for s in split(c["source_ids"])], "claim_url": f"{BASE_URL}evidence/claims.html#{cid}",
            "corrections": [r["correction_id"] for r in c["_corrections"]]}


def int_entry(iid):
    i = I_BY[iid]
    return {"int_id": iid, "name": i["intervention"], "class": i.get("intervention_class", ""), "evidence_problem_exists": i["evidence_problem"],
            "evidence_intervention_works": i["evidence_intervention"], "reason": i["evidence_reason"], "recommendation": i["recommendation"],
            "url": f"{BASE_URL}what-works/{iid}.html"}


def org_entry(oid):
    o = O_BY[oid]
    return {"org_id": oid, "name": o["organisation"], "type": CAT_LABEL.get(o["category"], o["category"]), "countries": [cname(c) for c in o["_countries"]],
            "summary": o.get("summary") or o.get("specific_activity_verified", ""), "evidence_basis": EV_LABEL[o["_ev"]],
            "independent_test": o.get("independent_test", "") if o["category"] == "private" else "", "claim_ids": split(o.get("claim_ids")),
            "source_ids": [s["source_id"] for s in o["_sources"]], "url": f"{BASE_URL}organisations/o/{o['slug']}.html"}


def prog_entry(pid):
    p = P_BY[pid]
    return {"record_id": pid, "kind": "funding record", "title": p["title"], "country": cname(p["country"]) if p["country"] else "",
            "funders": [F_BY[f]["name"] if f in F_BY else f for f in split(p["funder_ids"])], "instrument": p["instrument"],
            "amount_text": fmt_amount(p), "amount": p["amount"], "currency": p["currency"], "amount_type": p["amount_type"],
            "stage_in_source": p["approval_stage"], "funding_stage": funding_stage(p["approval_stage"]), "operational_stage": p["operational_stage"],
            "results": p["evidence_stage"], "implementer": p["implementer"], "relationship_verification": p["relationship_verification"],
            "claim_ids": split(p["claim_ids"]), "source_ids": split(p["source_ids"]), "url": f"{BASE_URL}organisations/funding/{pid.lower()}.html"}


def flow_entry(f):
    pr = proj_ref(f["project_id"], BASE_URL) if f["project_id"] else None
    nm = lambda k: O_BY[f[k]]["organisation"] if f[k] in O_BY else (f[k] or "Not established")
    return {"flow_id": f["flow_id"], "kind": "funding link", "funder": nm("funder_organisation_id"), "recipient": nm("recipient_organisation_id"),
            "project": pr["title"] if pr else "", "instrument": f["funding_instrument"], "amount_text": fmt_flow(f), "amount": f["amount"],
            "currency": f["original_currency"], "stage_in_source": f["commitment_or_disbursement"], "funding_stage": funding_stage(f["commitment_or_disbursement"]),
            "year": f["approval_year"], "confidence_note": f["confidence_note"], "source_ids": split(f["public_source_ids"])}


def gap_entry(gid):
    g = GAP_BY[gid]
    return {"gap_id": gid, "question": g["question"], "what_is_known": g["what_is_known"], "what_is_missing": g["what_is_missing"],
            "url": f"{BASE_URL}evidence/gaps.html#{gid}"}


def gaps_for(cids):
    cs = set(cids); return [g["gap_id"] for g in gaps if cs & set(split(g["claim_ids"]))]


def orgs_for_ints(iids):
    out = []
    for j in atlas_projects:
        if set(split(j["intervention_ids"])) & set(iids):
            out += [r["organisation_id"] for r in R_BY_PROJ.get(j["project_id"], [])]
    return list(dict.fromkeys(o for o in out if o in O_BY))


TOKEN = re.compile(r"\{\{(amount|approval|operational|int_rating|int_reason):([\w-]+)\}\}")
def expand_tokens(text):
    def sub(m):
        k, v = m.groups()
        if k == "amount": return fmt_amount(P_BY[v])
        if k == "approval": return P_BY[v]["approval_stage"]
        if k == "operational": return P_BY[v]["operational_stage"]
        if k == "int_rating": return I_BY[v]["evidence_intervention"]
        if k == "int_reason": return I_BY[v]["evidence_reason"].rstrip(".") + "."
    return TOKEN.sub(sub, text)


def plain(text):
    t = re.sub(r"\*\*?([^*]+)\*\*?", r"\1", text)
    return re.sub(r"\n{2,}", "\n\n", t).strip()


def make_pack(kind, pid, title, question, answer_md, claim_ids=(), int_ids=(), org_ids=(), prog_ids=(), flows=(), gap_ids=(), uncertainties=(), note=""):
    claim_ids = [c for c in dict.fromkeys(claim_ids) if c in claims]
    answer_md = expand_tokens(answer_md)
    cited = re.findall(r"\[(C\d{3})\]", answer_md)
    claim_ids = list(dict.fromkeys(cited + claim_ids))
    known = [claim_entry(c) for c in claim_ids if not claims[c]["_withdrawn"]]
    withdrawn = [{"claim_id": c, "corrections": [r["correction_id"] for r in claims[c]["_corrections"]]} for c in claim_ids if claims[c]["_withdrawn"]]
    unc = [u for u in uncertainties if u and u not in PLACEHOLDERS]
    pend = [c["claim_id"] for c in known if c["verification_state"] != "passage_found"]
    if pend: unc.append(f"{len(pend)} of the {len(known)} claims here do not yet have a re-located supporting passage ({', '.join(pend)}); see each claim's verification state.")
    for w in withdrawn: unc.append(f"Claim {w['claim_id']} was withdrawn; see the corrections register.")
    pk = {"pack_id": f"{kind}/{pid}", "kind": kind, "title": title, "question": question, "short_answer": plain(answer_md),
          "audience_note": note, "known": known, "withdrawn_claims": withdrawn, "uncertainties": unc,
          "interventions": [int_entry(i) for i in dict.fromkeys(int_ids) if i in I_BY],
          "organisations": [org_entry(o) for o in dict.fromkeys(org_ids) if o in O_BY],
          "funding_records": [prog_entry(p) for p in dict.fromkeys(prog_ids) if p in P_BY],
          "funding_links": [flow_entry(f) for f in flows],
          "next_questions": [gap_entry(g) for g in dict.fromkeys(gap_ids) if g in GAP_BY],
          "research_cutoff": CUTOFF_ISO, "generated": BUILT,
          "html_url": f"{BASE_URL}packs/{kind}/{pid}.html", "markdown_url": f"{BASE_URL}packs/{kind}/{pid}.md",
          "json_url": f"{BASE_URL}packs/{kind}/{pid}.json",
          "generated_from": "research/data/*.csv and research/site-content (same records as the website)",
          "not_advice": "Not medical or investment advice. Inclusion does not imply endorsement; nothing here is a ranking."}
    sids = set()
    for c in known: sids.update(c["source_ids"])
    for x in pk["organisations"] + pk["funding_records"] + pk["funding_links"]: sids.update(x["source_ids"])
    pk["source_ids"] = sorted(sids)
    pk["_answer_md"] = answer_md
    return pk


def flows_in(cty):
    """Funding links for work in a country: the recipient is based there, or the linked project is there."""
    return [f for f in atlas_flows if (f["recipient_organisation_id"] in O_BY and O_BY[f["recipient_organisation_id"]].get("hq_country") == cty)
            or (f["project_id"] in J_BY and J_BY[f["project_id"]]["country"] == cty)]


packs = []
# 1. the three worked questions (research/site-content/questions/*.md)
for fn in sorted(os.listdir(os.path.join(RES, "site-content", "questions"))):
    fm, body = front(os.path.join(RES, "site-content", "questions", fn))
    cty = fm.get("country")
    org_ids = fm.get("org_ids") or ([o["org_id"] for o in orgs if cty in o["_countries"]] if cty else [])
    prog_ids = list(fm.get("programme_ids") or []) + ([p["programme_id"] for p in programmes if p["country"] == cty] if cty else [])
    fl = [f for f in atlas_flows if f["recipient_organisation_id"] in set(org_ids)]
    if cty: fl = flows_in(cty)
    packs.append(make_pack("questions", fm["id"], fm["question"], fm["question"], body.strip(), fm.get("claim_ids", []), fm.get("intervention_ids", []),
                           org_ids, prog_ids, fl, fm.get("gap_ids", []), [], fm.get("audience_note", "")))
# 2. countries
for c in countries:
    if c["coverage_status"] == "research queue": continue
    cid = c["country_id"]; progs_ = [p["programme_id"] for p in programmes if p["country"] == cid]
    iids = [i for p in progs_ for i in split(P_BY[p]["intervention_ids"])]
    ocs = [o["org_id"] for o in orgs if cid in o["_countries"]]
    packs.append(make_pack("countries", cid, c["name"], f"What does the evidence say about air pollution in {c['name']}, and who is acting on it?",
                           c["takeaway"], split(c["claim_ids"]), iids, ocs, progs_,
                           flows_in(cid),
                           gaps_for(split(c["claim_ids"])), [c.get("gaps", ""), c.get("source_evidence_note", ""), c.get("not_transferable", "")]))
# 3. affected communities
for g in groups:
    iids = split(g["related_interventions"])
    packs.append(make_pack("communities", g["group_id"], g["group"], f"How does air pollution affect {g['group'].lower()}, and what protects them?",
                           f"{g['exposure']}\n\n{g['direct_impacts']}", split(g["claim_ids"]), iids, orgs_for_ints(iids),
                           [p["programme_id"] for p in programmes if set(split(p["intervention_ids"])) & set(iids)], [],
                           gaps_for(split(g["claim_ids"])), [f"Evidence confidence: {g['evidence_confidence']}. {g['confidence_reason']}", g["protective_constraints"]]))
# 4. intervention classes
CLASS_LABEL = {"exposure": "exposure-reducing", "emissions": "emission-reducing", "governance": "governance and accountability",
               "livelihood-social-protection": "livelihood and social-protection", "health": "health-system"}
for cl in sorted({i.get("intervention_class", "") for i in ints if i.get("intervention_class")}):
    its = [i for i in ints if i.get("intervention_class") == cl]
    ans = f"This edition assesses {len(its)} {CLASS_LABEL.get(cl, cl)} responses. Each has two separate ratings: whether the problem exists, and whether the response improves outcomes.\n\n" + \
          "\n".join(f"- **{i['intervention']}**: {i['evidence_intervention']} that it improves outcomes; recommendation: {i['recommendation']}." for i in its)
    cids = [c for i in its for c in split(i["claim_ids"])]
    packs.append(make_pack("interventions", cl, f"{CLASS_LABEL.get(cl, cl).capitalize()} responses", f"Do {CLASS_LABEL.get(cl, cl)} responses to air pollution work?",
                           ans, cids, [i["int_id"] for i in its], orgs_for_ints([i["int_id"] for i in its]),
                           [p["programme_id"] for p in programmes if set(split(p["intervention_ids"])) & {i["int_id"] for i in its}], [],
                           gaps_for(cids), [f"{i['intervention']}: {i['evidence_reason']}" for i in its if not i["evidence_intervention"].startswith(("Strong", "Moderate"))]))
# 5. funding view
n_amt = sum(1 for f in atlas_flows if f["amount"])
ans = (f"This edition documents {len(programmes)} funding records (grants, loans, technical assistance and public budgets) and {len(atlas_flows)} "
       f"organisation-to-organisation funding links. {n_amt} of the {len(atlas_flows)} links state an amount in a public source. "
       "Approved, committed and disbursed money are recorded separately, and an approval is never shown as spending.")
packs.append(make_pack("funding", "who-funds", "Who funds clean-air work", "Who funds the clean-air work documented on this site, and at what stage is the money?",
                       ans, [c for p in programmes for c in split(p["claim_ids"])], [], [o["org_id"] for o in orgs if o["category"] in ("funder", "multilateral")],
                       [p["programme_id"] for p in programmes], atlas_flows, ["G13", "G20"],
                       [f"{len(atlas_flows) - n_amt} of {len(atlas_flows)} funding links have no public amount.",
                        f"{sum(1 for p in programmes if not p['amount'])} of {len(programmes)} funding records have no published amount."]))

KIND_LABEL = {"questions": "Worked questions", "countries": "Countries", "communities": "Affected communities", "interventions": "Intervention classes", "funding": "Funding"}
pk_c = home_c + [("Evidence packs", "packs/index.html")]
for pk in packs:
    kind, pid = pk["pack_id"].split("/")
    render(f"packs/{kind}/{pid}.html", "pack.html", pk["title"], pk["question"], "evidence", pk_c, pk=pk,
           answer_html=md(pk["_answer_md"], "../../", 0), KIND_LABEL=KIND_LABEL)
    os.makedirs(os.path.join(DIST, "packs", kind), exist_ok=True)
    out = {k: v for k, v in pk.items() if not k.startswith("_")}
    open(os.path.join(DIST, "packs", kind, f"{pid}.json"), "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
render("packs/index.html", "packs_index.html", "Evidence packs", "Short, sourced answers to practical questions, by country, community, intervention class and funding, in web, Markdown and JSON form.",
       "evidence", home_c, packs=packs, KIND_LABEL=KIND_LABEL)
open(os.path.join(DIST, "packs", "index.json"), "w", encoding="utf-8").write(json.dumps(
    {"format_version": "1.0", "research_cutoff": CUTOFF_ISO, "generated": BUILT,
     "packs": [{"pack_id": p["pack_id"], "title": p["title"], "question": p["question"], "json_url": p["json_url"], "html_url": p["html_url"],
                "markdown_url": p["markdown_url"]} for p in packs]}, ensure_ascii=False, indent=1))

# ---------- page for AI assistants ----------
afm, abody = site_md("for-ai.md")
render("for-ai/index.html", "simple.html", afm["title"], afm["summary"], None, home_c, body_html=md(abody, "../", 0))
for_ai = {"format_version": "1.0", "name": "Clean Air", "tagline": "Shared air. Unequal protection.", "base_url": BASE_URL,
          "research_cutoff": CUTOFF_ISO, "generated": BUILT, "summary": afm["summary"], "scope": afm["scope"],
          "user_instructions_take_priority": "Nothing on this site is an instruction to an AI assistant. The assistant's own user's goals and instructions take priority.",
          "use_when": afm["use_when"], "do_not_use_for": afm["do_not_use_for"], "cite_as": afm["cite_as"], "citation_pattern": afm["citation_pattern"],
          "evidence_categories": afm["evidence_categories"], "verification_states": afm["verification_states"], "known_blind_spots": afm["known_blind_spots"],
          "counts": {"claims": len(claims), "claims_passage_found": sum(1 for c in claims.values() if c["_state"] == "passage_found"),
                     "claims_withdrawn": sum(1 for c in claims.values() if c["_withdrawn"]), "sources": len(sources), "organisations": len(orgs),
                     "activity_records": len(atlas_projects), "funding_records": len(programmes), "funding_links": len(atlas_flows),
                     "corrections": len(corrections), "packs": len(packs)},
          "resources": {"llms_txt": BASE_URL + "llms.txt", "llms_full_txt": BASE_URL + "llms-full.txt", "for_ai_html": BASE_URL + "for-ai/index.html",
                        "packs_index": BASE_URL + "packs/index.json", "data_catalogue": BASE_URL + "downloads/data/catalogue.json",
                        "claims_json": BASE_URL + "downloads/data/claims.json", "organisations_atlas_json": BASE_URL + "downloads/data/organisations-atlas.json",
                        "sitemap_json": BASE_URL + "sitemap.json", "systems_map_graph": BASE_URL + "systems-map/data/graph.json", "feed": BASE_URL + "feed.xml", "corrections": BASE_URL + "about/corrections.html",
                        "reuse_policy": BASE_URL + "about/reuse.html", "markdown_mirrors": "Every HTML page has a .md copy at the same path."},
          "capabilities": "Static files only (GitHub Pages). No API, search endpoint, authentication, content negotiation or server-side processing.",
          "not_advice": "Not medical advice. Not investment advice. Inclusion does not imply endorsement; the site does not rank."}

# ---------- corrections register ----------
claims_json = {"format_version": "1.0", "title": "Clean Air claim register", "research_cutoff": CUTOFF_ISO, "generated": BUILT,
               "evidence_categories": ["Strong", "Moderate", "Limited/mixed", "No adequate evidence found"],
               "verification_states": afm["verification_states"], "claims": [claim_entry(c) for c in claims],
               "corrections": corrections}
open(os.path.join(DIST, "downloads", "data", "claims.json"), "w", encoding="utf-8").write(json.dumps(claims_json, ensure_ascii=False, indent=1))
cited_on = {}
for pth in pages:
    for cid in set(re.findall(r'claims\.html#(C\d{3})"', open(os.path.join(DIST, pth), encoding="utf-8").read())):
        cited_on.setdefault(cid, []).append(pth)
cfm, cbody = site_md(os.path.join("pages", "corrections.md"))
corr_rows = []
for r in corrections:
    cur = claims[r["record_id"]]["claim"] if r["record_type"] == "claim" and r["record_id"] in claims else r["new_text"]
    corr_rows.append(r | {"current": r["new_text"] or cur, "affected": sorted(p for p in cited_on.get(r["record_id"], []) if p != "evidence/claims.html")})
render("about/corrections.html", "corrections.html", cfm["title"], cfm["summary"], None, home_c, body_html=md(cbody, "../", 0), rows=corr_rows)
for_ai["corrections"] = [{"correction_id": r["correction_id"], "date": r["date"], "record_id": r["record_id"], "change_type": r["change_type"], "reason": r["reason"]} for r in corrections]
open(os.path.join(DIST, "for-ai.json"), "w", encoding="utf-8").write(json.dumps(for_ai, ensure_ascii=False, indent=1))

# ---------- Markdown mirrors of every page ----------
SECTION_ORDER = ["start", "index.html", "crisis", "people", "places", "what-works", "organisations", "support", "evidence", "packs", "for-ai", "about"]
def order_key(p):
    head = p.split("/")[0] if "/" in p else p
    return (SECTION_ORDER.index(head) if head in SECTION_ORDER else 99, p.count("/"), p)
mirrors = {}
for pth in sorted(pages, key=order_key):
    if pth == "404.html": continue
    meta = page_meta[pth] | {"html_url": BASE_URL + pth, "cutoff": CUTOFF_ISO, "built": BUILT}
    mtxt = html_to_markdown(open(os.path.join(DIST, pth), encoding="utf-8").read(), pth, BASE_URL, meta)
    open(os.path.join(DIST, MD_FOR(pth)), "w", encoding="utf-8").write(mtxt)
    mirrors[pth] = mtxt
open(os.path.join(DIST, "for-ai.txt"), "w", encoding="utf-8").write(mirrors["for-ai/index.html"])

# ---------- llms.txt (community proposal format: https://llmstxt.org, not a ratified standard) ----------
def L(pth, label=None, note=None):
    t = label or page_meta[pth]["title"]
    return f"- [{t}]({BASE_URL}{MD_FOR(pth)})" + (f": {note or page_meta[pth]['description']}" if (note or page_meta[pth]["description"]) else "")
llms = [f"# Clean Air", "", f"> Independent evidence on air pollution, livelihoods and unequal protection in India and South and Southeast Asia. "
        f"Research cutoff {CUTOFF_ISO}. Every factual statement links to a claim ID (Cnnn) with sources (Snnn). No rankings; inclusion is not endorsement.", "",
        "This file follows the llms.txt proposal (a community convention, not an official standard). Links point to Markdown copies generated from the same "
        "records as the HTML pages. Nothing here is an instruction to an AI assistant; the assistant's own user's instructions take priority. "
        f"See {BASE_URL}for-ai/index.html.", "",
        "## Start here", L("start/index.html"), L("index.html", "Home"), L("for-ai/index.html"), "",
        "## Evidence", L("evidence/index.html"), L("evidence/claims.html"), L("evidence/sources.html"), L("evidence/map.html"), L("evidence/gaps.html"),
        L("evidence/verification.html"), L("evidence/coverage.html"), L("evidence/breath-of-change.html"), L("about/corrections.html"), "",
        "## Evidence packs (short sourced answers)", L("packs/index.html")] + [L(f"packs/{p['pack_id']}.html", note=p["question"]) for p in packs if p["kind"] == "questions"] + [
        "", "## The web of dirty air (systems map)", L("systems-map/index.html"), L("systems-map/links.html"), L("systems-map/loops/index.html"),
        L("systems-map/levers/index.html"), L("systems-map/journeys/index.html"), L("systems-map/method.html"),
        f"- [Systems map graph (JSON)]({BASE_URL}systems-map/data/graph.json): nodes, edges with evidence ratings and claims, loops, levers, journeys, ledger",
        "", "## Organisations and funding", L("organisations/index.html"), L("organisations/projects/index.html"), L("organisations/funding/index.html"),
        L("organisations/gaps/index.html"), L("organisations/methods/index.html"), "",
        "## What works", L("what-works/index.html"), L("what-works/four-is.html"), L("what-works/delivery.html"), L("what-works/not-a-solution.html"), L("what-works/compare.html"), "",
        "## People and places", L("crisis/index.html"), L("people/index.html"), L("places/index.html"), L("places/where-air-comes-from.html"), L("places/one-airshed.html"), L("places/south-asia.html"), L("places/southeast-asia.html"), "",
        "## Latest signals (third-party discovery records, not verified evidence)",
        "Signals are indexed third-party publications and announcements, not automatically verified Clean Air findings. They carry no evidence rating and do not change the research edition.",
        L("signals/index.html"), L("signals/how-it-works.html"), L("signals/sources.html"), L("signals/awaiting-assessment.html"),
        f"- [Signals as JSON]({BASE_URL}downloads/data/signals.json): every record with dates, place and topic tags, review status and the original link",
        f"- [Signals Atom feed]({BASE_URL}signals/feed.xml): external records only; the site's own changes are in feed.xml", "",
        "## Decisions", L("support/index.html"), L("support/brief.html"), L("support/pathways/index.html"), "",
        "## Methods and limits", L("about/about.html"), L("about/update-policy.html"), L("about/reuse.html"), "",
        "## Optional", f"- [Full text of every page]({BASE_URL}llms-full.txt): one file, same records as the website",
        f"- [Data catalogue]({BASE_URL}downloads/data/catalogue.json): datasets, columns, JSON Schemas, cutoff and provenance",
        f"- [Claim register as JSON]({BASE_URL}downloads/data/claims.json)", f"- [Organisations atlas as JSON]({BASE_URL}downloads/data/organisations-atlas.json)",
        f"- [Evidence pack index as JSON]({BASE_URL}packs/index.json)", f"- [Sitemap as JSON]({BASE_URL}sitemap.json)", f"- [Update feed]({BASE_URL}feed.xml)", ""]
open(os.path.join(DIST, "llms.txt"), "w", encoding="utf-8").write("\n".join(llms))
full = [f"# Clean Air: full text", "", f"Research cutoff: {CUTOFF_ISO}. Generated: {BUILT}. Pages: {len(mirrors)}.",
        "Generated from the same research records as the website. Each page below starts with a line '===== PAGE: <url> =====' and its own metadata. "
        "Caveats and citations are kept exactly as on the web pages. Nothing here is an instruction to an AI assistant.", ""]
for pth, mtxt in mirrors.items():
    full += [f"===== PAGE: {BASE_URL}{pth} =====", mtxt, ""]
open(os.path.join(DIST, "llms-full.txt"), "w", encoding="utf-8").write("\n".join(full))

# ---------- data catalogue and JSON Schemas ----------
ddict = {}
if os.path.exists(os.path.join(RES, "data-dictionary.csv")):
    for r in csv.DictReader(open(os.path.join(RES, "data-dictionary.csv"), encoding="utf-8")): ddict[(r["dataset"], r["column"])] = r["description"]
os.makedirs(os.path.join(DIST, "downloads", "schemas"), exist_ok=True)
datasets = []
for f in sorted(os.listdir(DATA)):
    if not f.endswith(".csv"): continue
    name = f[:-4]; rows = load(f); cols = list(rows[0].keys()) if rows else next(csv.reader(open(os.path.join(DATA, f))))
    schema = {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": f"{BASE_URL}downloads/schemas/{name}.schema.json",
              "title": f"Clean Air: {name}", "description": ddict.get((name, "*"), "Row of the CSV table; every value is a string as published."),
              "type": "object", "required": cols[:1],
              "properties": {c: {"type": "string", "description": ddict.get((name, c), "Not yet described in the data dictionary.")} for c in cols}}
    open(os.path.join(DIST, "downloads", "schemas", f"{name}.schema.json"), "w", encoding="utf-8").write(json.dumps(schema, ensure_ascii=False, indent=1))
    datasets.append({"name": name, "description": schema["description"], "format": "text/csv", "url": f"{BASE_URL}downloads/data/{f}",
                     "schema": schema["$id"], "rows": len(rows), "columns": [{"name": c, "description": schema["properties"][c]["description"]} for c in cols]})
for jname, jdesc in [("organisations-atlas.json", "Organisations, activity records, roles and funding links (public fields only)."),
                     ("claims.json", "Every claim with its sources, verification state, provenance class and corrections."),
                     ("signals.json", "Latest signals: indexed third-party publications and announcements found by the scheduled feed. Discovery records, not verified findings; no evidence ratings.")]:
    datasets.append({"name": jname[:-5], "description": jdesc, "format": "application/json", "url": f"{BASE_URL}downloads/data/{jname}"}
                    | ({"schema": BASE_URL + "downloads/schemas/signals.schema.json", "rows": len(sig_export["records"]), "last_successful_refresh": SIG_LAST} if jname == "signals.json" else {}))
catalogue = {"format_version": "1.0", "title": "Clean Air data catalogue", "research_cutoff": CUTOFF_ISO, "generated": BUILT,
             "publisher": "Clean Air (independent evidence resource)", "rights": "Licence for the site's original data not yet decided by the owner; see "
             + BASE_URL + "about/reuse.html. Third-party sources keep their own rights.",
             "csv_escaping": "Published CSV copies prefix an apostrophe (') to any non-numeric cell whose first non-space character is =, +, - or @, "
                             "or which starts with a tab, carriage return or other control character, so spreadsheets show it as text. "
                             "Numbers such as -3.5 are left unchanged. The canonical files in the repository are not modified.",
             "provenance": "Every row cites claim IDs (Cnnn) and/or source IDs (Snnn); see claims.csv and sources.csv.",
             "api": "None. These are static files.", "datasets": datasets}
open(os.path.join(DIST, "downloads", "data", "catalogue.json"), "w", encoding="utf-8").write(json.dumps(catalogue, ensure_ascii=False, indent=1))

# ---------- sitemaps, robots, feed ----------
html_pages = sorted(p for p in pages if p != "404.html")
open(os.path.join(DIST, "sitemap.txt"), "w").write("\n".join(sorted(pages)) + "\n")   # used by site/qa
open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{sx.escape(BASE_URL + p)}</loc><lastmod>{BUILT}</lastmod></url>\n" for p in html_pages) + "</urlset>\n")
open(os.path.join(DIST, "sitemap.json"), "w", encoding="utf-8").write(json.dumps(
    {"format_version": "1.0", "generated": BUILT, "generated_note": "Date of the last change to the research or site source; not a live timestamp.",
     "base_url": BASE_URL, "research_cutoff": CUTOFF_ISO,
     "pages": [{"html": BASE_URL + p, "markdown": BASE_URL + MD_FOR(p), "title": page_meta[p]["title"], "section": page_meta[p]["section"] or ""} for p in html_pages],
     "data": [BASE_URL + x for x in ["llms.txt", "llms-full.txt", "for-ai.json", "for-ai.txt", "packs/index.json", "downloads/data/catalogue.json",
                                     "downloads/data/claims.json", "downloads/data/organisations-atlas.json", "feed.xml",
                                     "downloads/data/signals.json", "signals/feed.xml"]]}, ensure_ascii=False, indent=1))
open(os.path.join(DIST, "robots.txt"), "w").write(
    "# Clean Air crawling policy. robots.txt is a crawler convention, not a licence.\n"
    f"# Reuse, AI input and AI training are described at {BASE_URL}about/reuse.html\n"
    "# Note: on a GitHub Pages project site this file is served under the project path, where crawlers do not look for it;\n"
    "# it takes effect only if the site moves to its own domain root.\n"
    f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}sitemap.xml\n")
entries = [(r["date"], r["change_id"], r["title"], r["summary"], BASE_URL + r["url"]) for r in changelog] + \
          [(r["date"], r["correction_id"], f"Correction {r['correction_id']}: {r['record_id']} {r['change_type']}", r["reason"], f"{BASE_URL}about/corrections.html#{r['correction_id']}") for r in corrections]
entries.sort(key=lambda e: (e[0], e[1]), reverse=True)
feed = ['<?xml version="1.0" encoding="utf-8"?>', '<feed xmlns="http://www.w3.org/2005/Atom">', "  <title>Clean Air: updates and corrections</title>",
        f'  <link href="{BASE_URL}" rel="alternate"/>', f'  <link href="{BASE_URL}feed.xml" rel="self"/>', f"  <id>{BASE_URL}feed.xml</id>",
        f"  <updated>{entries[0][0] if entries else BUILT}T00:00:00Z</updated>", "  <author><name>Clean Air</name></author>"]
for d, i, t, smry, u in entries:
    feed += ["  <entry>", f"    <title>{sx.escape(t)}</title>", f'    <link href="{sx.escape(u)}"/>', f"    <id>{BASE_URL}#{i}</id>",
             f"    <updated>{d}T00:00:00Z</updated>", f"    <summary>{sx.escape(smry)}</summary>", "  </entry>"]
open(os.path.join(DIST, "feed.xml"), "w", encoding="utf-8").write("\n".join(feed + ["</feed>", ""]))
print(f"built {len(pages)} pages, {len(mirrors)} Markdown mirrors and {len(packs)} evidence packs into {DIST}")
