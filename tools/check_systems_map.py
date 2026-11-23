"""Validate The Web of Dirty Air: graph integrity, evidence rules, loop closure, lever ratings and site/data equivalence.

Run:  python3 tools/check_systems_map.py [research_dir] [dist_dir]
      python3 tools/check_systems_map.py --self-test     (the bad fixture must trip every rule family)

Rules (docs/SYSTEMS_MAP_METHOD.md explains them):
  ids          unique IDs in every table; stable references only
  refs         no dangling system, node, edge, claim, intervention (lever), institution, population, journey or question reference
  evidence     only the four labels; hypotheses never Strong or Moderate; measured links cite at least one claim; no withdrawn claim;
               a Strong link needs a claim with a located passage in a fully read source; no Strong/Moderate link resting only on
               snippet-only sources
  loops        every loop closes (each edge starts where the previous ended, and the last returns to the first); loop confidence
               is never above its weakest link
  levers       levers carry no rating of their own (effectiveness comes from interventions.csv); the published rating equals it
  wording      no promise of outcomes on map pages ("will eliminate", "saves ... lives", "breaks the loop", "proven to")
  equivalence  (with dist) every node and edge appears in the diagram, in "Every link as text" and in the JSON/CSV exports;
               advertised counts equal data-derived counts; diagram has a title, description and labelled viewport
"""
import csv, glob, json, os, re, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
LABELS = ["No adequate evidence found", "Limited/mixed", "Moderate", "Strong"]
KINDS = {"causal", "associative", "mechanism", "reasoned_hypothesis"}
PROMISE = re.compile(r"\b(will (eliminate|end|stop|break|solve)|saves? [\w ,]{0,20}lives|breaks? (the|this|a) loop|loop is broken|proven to (work|reduce)|guarantees?)\b", re.I)


def rd(path):
    return list(csv.DictReader(open(path, encoding="utf-8"))) if os.path.exists(path) else []


def split(v): return [x.strip() for x in (v or "").split(";") if x.strip()]


def check(res, dist=None):
    errs = []
    sm = os.path.join(res, "systems-map"); data = os.path.join(res, "data")
    systems, nodes, edges, cycles = rd(f"{sm}/systems.csv"), rd(f"{sm}/nodes.csv"), rd(f"{sm}/edges.csv"), rd(f"{sm}/cycles.csv")
    levers, insts, roles, questions = rd(f"{sm}/levers.csv"), rd(f"{sm}/institutions.csv"), rd(f"{sm}/lever-roles.csv"), rd(f"{sm}/questions.csv")
    claims = {r["claim_id"]: r for r in rd(f"{data}/claims.csv")}; sources = {r["source_id"]: r for r in rd(f"{data}/sources.csv")}
    passages = {r["claim_id"]: r for r in rd(f"{data}/claim-passages.csv")}; ints = {r["int_id"]: r for r in rd(f"{data}/interventions.csv")}
    groups = {r["group_id"] for r in rd(f"{data}/community-impacts.csv")}
    for name, rows, key in [("systems", systems, "system_id"), ("nodes", nodes, "node_id"), ("edges", edges, "edge_id"), ("cycles", cycles, "cycle_id"),
                            ("levers", levers, "lever_id"), ("institutions", insts, "institution_id")]:
        seen = set()
        for r in rows:
            if r[key] in seen: errs.append(f"ids: duplicate {name} id {r[key]}")
            seen.add(r[key])
    S = {s["system_id"] for s in systems}; N = {n["node_id"]: n for n in nodes}; E = {e["edge_id"]: e for e in edges}; I = {i["institution_id"] for i in insts}
    for n in nodes:
        if n["system_id"] not in S: errs.append(f"refs: node {n['node_id']} has unknown system {n['system_id']}")
        if n["layer"] not in "ABCDEF" or len(n["layer"]) != 1: errs.append(f"refs: node {n['node_id']} has bad layer {n['layer']}")
        for c in split(n["claim_ids"]):
            if c not in claims: errs.append(f"refs: node {n['node_id']} cites unknown claim {c}")
        for p in split(n["populations"]):
            if p not in groups: errs.append(f"refs: node {n['node_id']} names unknown population {p}")
    for e in edges:
        eid = e["edge_id"]
        for k in ("from", "to"):
            if e[k] not in N: errs.append(f"refs: edge {eid} {k} unknown node {e[k]}")
        if e["strength"] not in LABELS: errs.append(f"evidence: edge {eid} uses label '{e['strength']}'")
        if e["relation_kind"] not in KINDS: errs.append(f"evidence: edge {eid} unknown relation kind {e['relation_kind']}")
        if e["direction"] not in ("increase", "decrease", "conditional"): errs.append(f"evidence: edge {eid} unknown direction {e['direction']}")
        cs = split(e["claim_ids"])
        for c in cs:
            if c not in claims: errs.append(f"refs: edge {eid} cites unknown claim {c}")
            elif claims[c]["status"] == "withdrawn": errs.append(f"evidence: edge {eid} cites withdrawn claim {c}")
        if e["relation_kind"] == "reasoned_hypothesis" and e["strength"] in ("Strong", "Moderate"):
            errs.append(f"evidence: edge {eid} is a hypothesis but rated {e['strength']}")
        if e["relation_kind"] != "reasoned_hypothesis" and not cs: errs.append(f"evidence: measured edge {eid} cites no claim")
        if not e["strength_reason"].strip(): errs.append(f"evidence: edge {eid} has no reason for its rating")
        valid = [c for c in cs if c in claims]
        if e["strength"] == "Strong" and not any(passages.get(c, {}).get("verification_state") == "passage_found" and
                                                  all(sources.get(s, {}).get("access_status") == "full-text-read" for s in split(claims[c]["source_ids"])[:1]) for c in valid):
            errs.append(f"evidence: edge {eid} is Strong without a passage-checked, fully read claim")
        if e["strength"] in ("Strong", "Moderate") and valid and all(all(sources.get(s, {}).get("access_status") == "search-snippet-only" for s in split(claims[c]["source_ids"])) for c in valid):
            errs.append(f"evidence: edge {eid} rated {e['strength']} rests only on snippet-only sources")
    for c in cycles:
        es = split(c["edge_ids"])
        if len(es) < 2: errs.append(f"loops: {c['cycle_id']} has fewer than two edges")
        if any(x not in E for x in es): errs.append(f"loops: {c['cycle_id']} references unknown edge"); continue
        for a, b in zip(es, es[1:] + es[:1]):
            if E[a]["to"] != E[b]["from"]: errs.append(f"loops: {c['cycle_id']} does not close between {a} ({E[a]['to']}) and {b} ({E[b]['from']})")
        if c["cycle_confidence"] not in LABELS: errs.append(f"loops: {c['cycle_id']} bad confidence label")
        elif any(E[x]["strength"] not in LABELS for x in es): errs.append(f"loops: {c['cycle_id']} includes an edge with an invalid label")
        else:
            weakest = min((E[x]["strength"] for x in es), key=LABELS.index)
            if LABELS.index(c["cycle_confidence"]) > LABELS.index(weakest): errs.append(f"loops: {c['cycle_id']} confidence above its weakest link ({weakest})")
    for l in levers:
        if l["lever_id"] not in ints: errs.append(f"refs: lever {l['lever_id']} is not an assessed intervention")
        for k in l:
            if "rating" in k or "strength" in k or "effectiveness" in k: errs.append(f"levers: levers.csv carries its own rating column '{k}'")
        for t in split(l["target_edges"]):
            if t not in E: errs.append(f"refs: lever {l['lever_id']} targets unknown edge {t}")
        if l["mode"] not in ("source reduction", "exposure protection", "healthcare", "livelihood support", "governance and financing"):
            errs.append(f"levers: {l['lever_id']} unknown mode {l['mode']}")
    L = {l["lever_id"] for l in levers}
    for r in roles:
        if r["lever_id"] not in L: errs.append(f"refs: role for unknown lever {r['lever_id']}")
        if r["institution_id"] not in I: errs.append(f"refs: role names unknown institution {r['institution_id']}")
    jdir = os.path.join(sm, "journeys")
    jids = set()
    for f in sorted(glob.glob(os.path.join(jdir, "*.md"))):
        import yaml
        fm = yaml.safe_load(re.match(r"\A---\n(.*?)\n---", open(f).read(), re.S).group(1)); jids.add(fm["id"])
        if fm.get("population") and fm["population"] not in groups: errs.append(f"refs: journey {fm['id']} unknown population")
        for s in fm["steps"]:
            if s["edge"] not in E: errs.append(f"refs: journey {fm['id']} uses unknown edge {s['edge']}")
        if "composite" not in fm: errs.append(f"wording: journey {fm['id']} is not labelled as a composite")
    for q in questions:
        for link in split(q["links"]):
            k, _, v = link.partition(":")
            ok = {"edge": v in E, "loop": v in {c["cycle_id"] for c in cycles}, "lever": v in L, "journey": v in jids}.get(k, False)
            if not ok: errs.append(f"refs: question {q['question_id']} link {link} does not resolve")
    if dist:
        smd = os.path.join(dist, "systems-map")
        g = json.load(open(os.path.join(smd, "data", "graph.json")))
        idx = open(os.path.join(smd, "index.html"), encoding="utf-8").read(); links = open(os.path.join(smd, "links.html"), encoding="utf-8").read()
        ecsv = open(os.path.join(smd, "data", "edges.csv"), encoding="utf-8").read(); ncsv = open(os.path.join(smd, "data", "nodes.csv"), encoding="utf-8").read()
        for n in nodes:
            nid = n["node_id"]
            if f'data-id="{nid}"' not in idx: errs.append(f"equivalence: node {nid} missing from the diagram")
            if f'id="node-{nid}"' not in links: errs.append(f"equivalence: node {nid} missing from Every link as text")
            if f"\n{nid}," not in ncsv: errs.append(f"equivalence: node {nid} missing from nodes.csv")
        for e in edges:
            eid = e["edge_id"]
            if f'data-id="{eid}"' not in idx: errs.append(f"equivalence: edge {eid} missing from the diagram")
            if f'id="{eid}"' not in links: errs.append(f"equivalence: edge {eid} missing from Every link as text")
            if f"\n{eid}," not in ecsv: errs.append(f"equivalence: edge {eid} missing from edges.csv")
        if {x["edge_id"] for x in g["edges"]} != set(E): errs.append("equivalence: graph.json edges differ from edges.csv")
        for l in g["levers"]:
            if l["effectiveness_rating"] != ints[l["lever_id"]]["evidence_intervention"]: errs.append(f"levers: published rating for {l['lever_id']} differs from the intervention assessment")
        counts = {"systems": len(systems), "nodes": len(nodes), "edges": len(edges), "loops": len(cycles), "levers": len(levers),
                  "hypothesis_edges": sum(1 for e in edges if e["relation_kind"] == "reasoned_hypothesis")}
        for k, v in counts.items():
            if g["counts"][k] != v: errs.append(f"equivalence: graph.json count {k}={g['counts'][k]} but data has {v}")
            m = re.search(rf'data-count="{k}">(\d+)<', idx)
            if not m or int(m.group(1)) != v: errs.append(f"equivalence: page advertises {k}={m.group(1) if m else 'missing'} but data has {v}")
        if '<title id="map-title">' not in idx or '<desc id="map-desc">' not in idx: errs.append("a11y: diagram lacks title or description")
        if 'role="region" aria-label=' not in idx: errs.append("a11y: diagram viewport is not a labelled region")
        if re.search(r'<a class="node[^>]*>(?![^<]*)', idx): pass
        for a in re.findall(r'<a class="node[^"]*"[^>]*>', idx):
            if "aria-label=" not in a: errs.append("a11y: a node link has no accessible name"); break
        for f in glob.glob(os.path.join(smd, "**", "*.html"), recursive=True):
            t = re.sub(r"<[^>]+>", " ", open(f, encoding="utf-8").read())
            for m in PROMISE.finditer(t):
                if re.search(r"\b(not|no|without|never|nor)\b[^.]{0,50}$", t[max(0, m.start() - 60):m.start()], re.I): continue
                errs.append(f"wording: {os.path.relpath(f, dist)} promises an outcome: '{m.group(0)}'"); break
    return errs


def self_test():
    """Copy the real research folder, break it in each rule family, and require every family to fail."""
    tmp = tempfile.mkdtemp(prefix="ca-sm-"); res = os.path.join(tmp, "research")
    shutil.copytree(os.path.join(ROOT, "research"), res, ignore=shutil.ignore_patterns("exports", "report", "__pycache__"))
    fx = os.path.join(HERE, "fixtures", "systems-map")
    for f in os.listdir(fx):                     # bad rows appended to the copied tables
        if f.endswith(".csv"):
            with open(os.path.join(res, "systems-map", f), "a", encoding="utf-8") as out: out.write(open(os.path.join(fx, f), encoding="utf-8").read())
    e = check(res); shutil.rmtree(tmp)
    kinds = {x.split(":")[0] for x in e}
    need = {"ids", "refs", "evidence", "loops", "levers"}
    print(f"systems-map self-test: bad fixture -> {len(e)} errors, families {sorted(kinds)}")
    for x in e[:12]: print("   ", x)
    return 0 if need <= kinds else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv: sys.exit(self_test())
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    res = args[0] if args else os.path.join(ROOT, "research"); dist = args[1] if len(args) > 1 else os.path.join(ROOT, "site", "dist")
    e = check(res, dist if os.path.exists(os.path.join(dist, "systems-map")) else None)
    for x in e: print("ERROR", x)
    print(f"systems map: {len(e)} errors")
    sys.exit(1 if e else 0)
