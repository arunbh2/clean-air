# The Web of Dirty Air: the systems map. Executed by site/build.py in its namespace, after the main pages and before
# build_agent.py (so every map page gets a Markdown mirror and enters llms-full.txt and the sitemaps).
# Canonical data: research/systems-map/*.csv and journeys/*.md. Evidence comes only from research/data/claims.csv
# (claim IDs) and the existing interventions, organisations and funding records. Nothing here writes facts of its own.
import math

SM = os.path.join(RES, "systems-map")
def sm_load(name): return list(csv.DictReader(open(os.path.join(SM, name), encoding="utf-8")))
SM_SYS = sm_load("systems.csv"); SM_NODES = sm_load("nodes.csv"); SM_EDGES = sm_load("edges.csv"); SM_CYC = sm_load("cycles.csv")
SM_LEV = sm_load("levers.csv"); SM_INST = sm_load("institutions.csv"); SM_ROLES = sm_load("lever-roles.csv"); SM_LEDGER = sm_load("ledger.csv")
SM_Q = sm_load("questions.csv")
SM_J = []
for fn in sorted(os.listdir(os.path.join(SM, "journeys"))):
    fm_, _ = front(os.path.join(SM, "journeys", fn)); SM_J.append(fm_)
SYS_BY = {s["system_id"]: s for s in SM_SYS}; NODE_BY = {n["node_id"]: n for n in SM_NODES}; EDGE_BY = {e["edge_id"]: e for e in SM_EDGES}
INST_BY = {i["institution_id"]: i for i in SM_INST}; LEV_BY = {l["lever_id"]: l for l in SM_LEV}
STRENGTH_ORDER = ["No adequate evidence found", "Limited/mixed", "Moderate", "Strong"]
KIND_LABEL = {"causal": "Causal evidence", "associative": "Association (not proof of cause)", "mechanism": "Physical or institutional mechanism",
              "reasoned_hypothesis": "Reasoned hypothesis (not measured)"}
LAYER_LABEL = {"A": "Sources of pollution", "B": "What happens in the air", "C": "Where people breathe it", "D": "Health",
               "E": "Livelihoods and homes", "F": "Institutions, rules and money"}
DIR_LABEL = {"increase": "increases", "decrease": "reduces", "conditional": "changes, depending on conditions"}

edge_loops = {}
for c in SM_CYC:
    c["_edges"] = split(c["edge_ids"])
    for e in c["_edges"]: edge_loops.setdefault(e, []).append(c["cycle_id"])
lev_targets = {}
for l in SM_LEV:
    l["_targets"] = split(l["target_edges"])
    for e in l["_targets"]: lev_targets.setdefault(e, []).append(l["lever_id"])


def sm_claim(cid):
    c = claims[cid]
    return {"claim_id": cid, "text": c["claim"], "place": c["geography"], "period": c["period"], "verification_state": c["_state"],
            "verification_label": c["_state_label"], "provenance": c["_provenance"], "source_ids": split(c["source_ids"])}


for e in SM_EDGES:
    f, t = NODE_BY[e["from"]], NODE_BY[e["to"]]
    e["_hyp"] = e["relation_kind"] == "reasoned_hypothesis"
    e["_order"] = "hypothesis" if e["_hyp"] else ("direct" if f["layer"] in "AB" else "knock-on")
    e["_loops"] = edge_loops.get(e["edge_id"], [])
    e["_levers"] = lev_targets.get(e["edge_id"], [])
    e["_claims"] = [sm_claim(c) for c in split(e["claim_ids"]) if c in claims]
    e["_sentence"] = f"{f['label']} {DIR_LABEL[e['direction']]} {t['label'].lower()}"
for n in SM_NODES:
    n["_out"] = [e for e in SM_EDGES if e["from"] == n["node_id"]]; n["_in"] = [e for e in SM_EDGES if e["to"] == n["node_id"]]
    n["_claims"] = [sm_claim(c) for c in split(n["claim_ids"]) if c in claims]
    n["_pops"] = [p for p in split(n["populations"]) if p in G_BY]
for c in SM_CYC:
    ws = [EDGE_BY[x]["strength"] for x in c["_edges"]]
    c["_weakest"] = min(ws, key=STRENGTH_ORDER.index)
    c["_nodes"] = [EDGE_BY[x]["from"] for x in c["_edges"]]
    c["_measured"] = sum(1 for x in c["_edges"] if not EDGE_BY[x]["_hyp"])

# levers: effectiveness comes ONLY from interventions.csv (never from the strength of the problem edge)
for l in SM_LEV:
    i = I_BY[l["lever_id"]]
    l["_name"] = i["intervention"]; l["_rating"] = i["evidence_intervention"]; l["_reason"] = i["evidence_reason"]; l["_rec"] = i["recommendation"]
    l["_capital"] = i["capital_needs"]; l["_recurring"] = i["recurring_needs"]; l["_operator"] = i["operator"]
    l["_roles"] = [(r["role"], INST_BY[r["institution_id"]]) for r in SM_ROLES if r["lever_id"] == l["lever_id"]]
    # documented organisations: only verified roles on activity records that list this intervention
    docs = []
    for j in atlas_projects:
        if l["lever_id"] in split(j["intervention_ids"]):
            for r in R_BY_PROJ.get(j["project_id"], []):
                if r["organisation_id"] in O_BY: docs.append((O_BY[r["organisation_id"]], r["role"], j))
    l["_orgs"] = docs
    l["_progs"] = [p for p in programmes if l["lever_id"] in split(p["intervention_ids"])]
    l["_flows"] = [f_ for f_ in atlas_flows if f_["project_id"] in J_BY and l["lever_id"] in split(J_BY[f_["project_id"]]["intervention_ids"])]

# ---------- layout: five columns (layers A to E) above a band for institutions (layer F) ----------
COL_X = {"A": 20, "B": 262, "C": 504, "D": 746, "E": 988}
NW, NH, VGAP = 200, 46, 66
pos = {}
for lay in "ABCDE":
    col = [n for n in SM_NODES if n["layer"] == lay]
    for k, n in enumerate(col): pos[n["node_id"]] = (COL_X[lay], 70 + k * VGAP)
top_h = 70 + max(len([n for n in SM_NODES if n["layer"] == l]) for l in "ABCDE") * VGAP
band = [n for n in SM_NODES if n["layer"] == "F"]
per_row = 6
for k, n in enumerate(band):
    r, cpos = divmod(k, per_row)
    pos[n["node_id"]] = (20 + cpos * 202, top_h + 70 + r * VGAP)
MAP_W = 1240; MAP_H = top_h + 70 + (math.ceil(len(band) / per_row)) * VGAP + 10


def wrap(label, n=24):
    words, lines, cur = label.split(), [], ""
    for w_ in words:
        if len(cur) + len(w_) + 1 > n and cur: lines.append(cur); cur = w_
        else: cur = (cur + " " + w_).strip()
    lines.append(cur); return lines[:2]


def edge_path(e):
    (x1, y1), (x2, y2) = pos[e["from"]], pos[e["to"]]
    a = (x1 + NW, y1 + NH / 2); b = (x2, y2 + NH / 2)
    if x2 <= x1:  # backwards or same column: leave from the top/bottom and curve
        a = (x1 + NW / 2, y1 + (NH if y2 > y1 else 0)); b = (x2 + NW / 2, y2 + (0 if y2 > y1 else NH))
        dy = (b[1] - a[1]) / 2 or 40
        return f"M{a[0]:.0f},{a[1]:.0f} C{a[0] + 60:.0f},{a[1] + dy:.0f} {b[0] + 60:.0f},{b[1] - dy:.0f} {b[0]:.0f},{b[1]:.0f}"
    dx = max(40, (b[0] - a[0]) / 2)
    return f"M{a[0]:.0f},{a[1]:.0f} C{a[0] + dx:.0f},{a[1]:.0f} {b[0] - dx:.0f},{b[1]:.0f} {b[0]:.0f},{b[1]:.0f}"


key_nodes = {x for e in SM_EDGES if e["key"] == "1" for x in (e["from"], e["to"])}
svg = [f'<svg class="map-svg" viewBox="0 0 {MAP_W} {MAP_H}" role="group" aria-labelledby="map-title map-desc" data-w="{MAP_W}" data-h="{MAP_H}">',
       '<title id="map-title">The web of dirty air: systems map</title>',
       f'<desc id="map-desc">{len(SM_NODES)} parts of the system and {len(SM_EDGES)} documented or hypothesised connections. Every connection is also listed as text on the page "Every link as text".</desc>',
       '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="arrow"/></marker></defs>']
for lay in "ABCDE":
    svg.append(f'<text class="layer-head" x="{COL_X[lay]}" y="40">{LAYER_LABEL[lay]}</text>')
svg.append(f'<text class="layer-head" x="20" y="{top_h + 40}">{LAYER_LABEL["F"]}</text>')
svg.append(f'<line class="band-rule" x1="20" x2="{MAP_W - 20}" y1="{top_h + 14}" y2="{top_h + 14}"/>')
for e in SM_EDGES:
    cls = f'edge {e["_order"]}' + ("" if e["key"] == "1" else " minor")
    svg.append(f'<a class="{cls}" href="links.html#{e["edge_id"]}" data-id="{e["edge_id"]}" tabindex="-1" aria-label="{html.escape(e["_sentence"])}. Evidence: {e["strength"]}">'
               f'<path class="hit" d="{edge_path(e)}"/><path class="line" d="{edge_path(e)}" marker-end="url(#arr)"/></a>')
for n in SM_NODES:
    x, y = pos[n["node_id"]]
    cls = f'node t-{n["node_type"].replace(" ", "-")}' + ("" if n["node_id"] in key_nodes else " minor")
    lines = wrap(n["label"])
    ty = y + (NH / 2 + 5 if len(lines) == 1 else NH / 2 - 3)
    tx = "".join(f'<tspan x="{x + 10}" dy="{0 if k == 0 else 16}">{html.escape(t)}</tspan>' for k, t in enumerate(lines))
    svg.append(f'<a class="{cls}" href="links.html#node-{n["node_id"]}" data-id="{n["node_id"]}" data-system="{n["system_id"]}" data-pops="{" ".join(n["_pops"])}" '
               f'aria-label="{html.escape(n["label"])}, {html.escape(SYS_BY[n["system_id"]]["title"])}">'
               f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="3"/><text x="{x + 10}" y="{ty:.0f}">{tx}</text></a>')
svg.append("</svg>")
SVG = "\n".join(svg)

# ---------- canonical graph export (the same object drives the page script, the text views and the downloads) ----------
def edge_pub(e):
    return {"edge_id": e["edge_id"], "from": e["from"], "to": e["to"], "sentence": e["_sentence"], "mechanism": e["mechanism"], "direction": e["direction"],
            "relation_kind": e["relation_kind"], "relation_label": KIND_LABEL[e["relation_kind"]], "evidence_strength": e["strength"],
            "why_this_rating": e["strength_reason"], "order": e["_order"], "geography": e["geography"], "uncertainty": e["uncertainty"],
            "claims": e["_claims"], "loops": e["_loops"], "levers": e["_levers"], "key": e["key"] == "1",
            "url": f"{BASE_URL}systems-map/links.html#{e['edge_id']}"}
GRAPH = {
    "title": "The web of dirty air", "schema_version": "1.0", "dataset_version": BUILT, "research_cutoff": CUTOFF_ISO, "generated": BUILT,
    "about": "An illustrative, evidence-annotated systems map. It is not a quantitative impact model or a prediction. A mapped pathway is not causal proof; "
             "a lever 'could weaken' a connection, it does not guarantee an outcome. Loops are interpretations unless stated; none has been tested end to end.",
    "evidence_categories": STRENGTH_ORDER[::-1], "relation_kinds": KIND_LABEL,
    "rights": "Clean Air's original data: licence not yet decided by the owner (see about/reuse.html). Third-party sources keep their own rights.",
    "systems": [{"system_id": s["system_id"], "title": s["title"], "plain": s["plain"]} for s in SM_SYS],
    "nodes": [{"node_id": n["node_id"], "system_id": n["system_id"], "layer": n["layer"], "label": n["label"], "explanation": n["explanation"],
               "type": n["node_type"], "populations": n["_pops"], "geography": n["geography"], "timescale": n["timescale"],
               "claims": [c["claim_id"] for c in n["_claims"]], "key": n["node_id"] in key_nodes,
               "url": f"{BASE_URL}systems-map/links.html#node-{n['node_id']}"} for n in SM_NODES],
    "edges": [edge_pub(e) for e in SM_EDGES],
    "loops": [{"loop_id": c["cycle_id"], "title": c["title"], "edges": c["_edges"], "nodes": c["_nodes"], "why_feedback": c["why_feedback"],
               "loop_confidence": c["cycle_confidence"], "weakest_link": c["_weakest"], "measured_links": c["_measured"], "links": len(c["_edges"]),
               "contexts": c["contexts"], "caveats": c["caveats"], "url": f"{BASE_URL}systems-map/loops/{c['cycle_id'].lower()}.html"} for c in SM_CYC],
    "levers": [{"lever_id": l["lever_id"], "name": l["_name"], "mode": l["mode"], "targets": l["_targets"], "could_change": l["could_change"],
                "effectiveness_rating": l["_rating"], "effectiveness_reason": l["_reason"], "recommendation": l["_rec"],
                "capital_needs": l["_capital"], "recurring_needs": l["_recurring"], "risks": l["risks"], "measure": l["measure"], "unproven": l["unproven"],
                "roles": [{"role": r, "institution": inst["label"]} for r, inst in l["_roles"]],
                "documented_organisations": [{"org_id": o["org_id"], "name": o["organisation"], "role": role, "record": j["project_id"]} for o, role, j in l["_orgs"]],
                "funding_records": [{"record_id": p["programme_id"], "title": p["title"], "amount": fmt_amount(p), "stage_in_source": p["approval_stage"]} for p in l["_progs"]],
                "funding_links": [{"flow_id": f_["flow_id"], "funder": O_BY[f_["funder_organisation_id"]]["organisation"] if f_["funder_organisation_id"] in O_BY else f_["funder_organisation_id"],
                                   "recipient": O_BY[f_["recipient_organisation_id"]]["organisation"] if f_["recipient_organisation_id"] in O_BY else "", "amount": fmt_flow(f_),
                                   "stage_in_source": f_["commitment_or_disbursement"]} for f_ in l["_flows"]],
                "url": f"{BASE_URL}systems-map/levers/{l['lever_id']}.html"} for l in SM_LEV],
    "institutions": [{"institution_id": i["institution_id"], "label": i["label"], "plain": i["plain"]} for i in SM_INST],
    "journeys": [{"journey_id": j["id"], "title": j["title"], "steps": [s["edge"] for s in j["steps"]], "url": f"{BASE_URL}systems-map/journeys/{j['id']}.html"} for j in SM_J],
    "ledger": SM_LEDGER,
    "counts": {"systems": len(SM_SYS), "nodes": len(SM_NODES), "edges": len(SM_EDGES), "measured_edges": sum(1 for e in SM_EDGES if not e["_hyp"]),
               "hypothesis_edges": sum(1 for e in SM_EDGES if e["_hyp"]), "loops": len(SM_CYC), "levers": len(SM_LEV), "institutions": len(SM_INST),
               "journeys": len(SM_J), "claims_linked": len({c["claim_id"] for e in SM_EDGES for c in e["_claims"]})},
}
GRAPH["counts"]["by_strength"] = {s: sum(1 for e in SM_EDGES if e["strength"] == s) for s in STRENGTH_ORDER[::-1]}
sm_dir = os.path.join(DIST, "systems-map", "data"); os.makedirs(sm_dir, exist_ok=True)
open(os.path.join(sm_dir, "graph.json"), "w", encoding="utf-8").write(json.dumps(GRAPH, ensure_ascii=False, indent=1))
open(os.path.join(sm_dir, "loops.json"), "w", encoding="utf-8").write(json.dumps({"research_cutoff": CUTOFF_ISO, "generated": BUILT, "loops": GRAPH["loops"]}, ensure_ascii=False, indent=1))
open(os.path.join(sm_dir, "levers.json"), "w", encoding="utf-8").write(json.dumps({"research_cutoff": CUTOFF_ISO, "generated": BUILT, "levers": GRAPH["levers"]}, ensure_ascii=False, indent=1))
import io as _io
def _csv(rows, hdr):
    b = _io.StringIO(); w_ = csv.writer(b, lineterminator="\n"); w_.writerow(hdr); w_.writerows(rows); return safe_csv_text(b.getvalue())
open(os.path.join(sm_dir, "nodes.csv"), "w", encoding="utf-8").write(_csv(
    [[n["node_id"], n["system_id"], n["layer"], n["label"], n["explanation"], n["node_type"], ";".join(n["_pops"]), n["geography"], n["timescale"], n["claim_ids"]] for n in SM_NODES],
    ["node_id", "system_id", "layer", "label", "explanation", "type", "populations", "geography", "timescale", "claim_ids"]))
open(os.path.join(sm_dir, "edges.csv"), "w", encoding="utf-8").write(_csv(
    [[e["edge_id"], e["from"], e["to"], e["mechanism"], e["direction"], e["relation_kind"], e["strength"], e["strength_reason"], e["claim_ids"], e["geography"],
      e["uncertainty"], ";".join(e["_loops"]), ";".join(e["_levers"]), CUTOFF_ISO] for e in SM_EDGES],
    ["edge_id", "from", "to", "mechanism", "direction", "relation_kind", "evidence_strength", "why_this_rating", "claim_ids", "geography", "uncertainty",
     "loops", "levers", "research_cutoff"]))

# ---------- pages ----------
sm_c = home_c + [("The web of dirty air", "systems-map/index.html")]
env.globals.update(SM_NODE_BY=NODE_BY, SM_EDGE_BY=EDGE_BY, SM_SYS_BY=SYS_BY, SM_LEV_BY=LEV_BY, SM_KIND=KIND_LABEL, SM_LAYER=LAYER_LABEL)
smfm, smbody = site_md("systems-map.md")
map_data = {"nodes": GRAPH["nodes"], "edges": GRAPH["edges"], "loops": GRAPH["loops"], "systems": GRAPH["systems"],
            "levers": [{k: v for k, v in l.items() if k in ("lever_id", "name", "mode", "targets", "could_change", "effectiveness_rating", "effectiveness_reason",
                                                         "recommendation", "risks", "measure", "unproven", "roles", "documented_organisations", "funding_records", "funding_links", "url")}
                       for l in GRAPH["levers"]], "groups": [{"id": g["group_id"], "label": g["group"]} for g in groups if any(g["group_id"] in n["_pops"] for n in SM_NODES)]}
render("systems-map/index.html", "systems_map.html", smfm["title"], smfm["lede"], None, home_c, smfm=smfm, intro_html=md(smbody, "../", 0), SVG=SVG,
       G=GRAPH, journeys=SM_J, questions=SM_Q, map_json=json.dumps(map_data, ensure_ascii=False).replace("</", "<\\/"), glossify=False)
render("systems-map/links.html", "systems_links.html", "Every link as text", "Every part of the systems map and every connection, with its evidence, in the same order as the map.",
       None, sm_c, nodes=SM_NODES, edges=SM_EDGES, systems=SM_SYS, G=GRAPH)
render("systems-map/loops/index.html", "systems_loops.html", "Feedback loops", "Where harms may reinforce one another, which links are measured, and where the loop could be weakened.",
       None, sm_c, loops=SM_CYC, ledger=[r for r in SM_LEDGER if r["kind"] == "loop"])
for c in SM_CYC:
    render(f"systems-map/loops/{c['cycle_id'].lower()}.html", "systems_loop.html", c["title"], c["why_feedback"], None, sm_c + [("Feedback loops", "systems-map/loops/index.html")], c=c)
render("systems-map/levers/index.html", "systems_levers.html", "Where action could weaken a link", "Levers on the systems map: which connection each could weaken, how strong the evidence is that it works, and who could act.",
       None, sm_c, levers=SM_LEV)
for l in SM_LEV:
    render(f"systems-map/levers/{l['lever_id']}.html", "systems_lever.html", l["_name"], l["could_change"], None, sm_c + [("Levers", "systems-map/levers/index.html")], l=l)
render("systems-map/journeys/index.html", "systems_journeys.html", "Start with one person's day", "Five guided journeys through the map, one relationship at a time.", None, sm_c, journeys=SM_J)
for j in SM_J:
    render(f"systems-map/journeys/{j['id']}.html", "systems_journey.html", j["title"], j["summary"], None, sm_c + [("Journeys", "systems-map/journeys/index.html")], j=j)
mmfm, mmbody = site_md("systems-map-method.md")
render("systems-map/method.html", "systems_method.html", mmfm["title"], mmfm["summary"], None, sm_c, body_html=md(mmbody, "../", 0), ledger=SM_LEDGER, G=GRAPH)
