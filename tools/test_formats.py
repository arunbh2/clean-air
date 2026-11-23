"""Human and agent answers must match: compare the three worked questions across formats.

Run: python3 tools/test_formats.py [dist]

For each worked question (packs/questions/*), the HTML page, its Markdown mirror and its JSON must carry the
same claim IDs, claim texts, verification labels, amounts, funding stages, caveats and cutoff, and those values
must equal the canonical exports (downloads/data/claims.json, organisations-atlas.json) and the funding-record
page a human would reach. Any drift fails the test.
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from check_voice import RULES
RANKING = dict((r[0], r[1]) for r in RULES)["ranking"]
DEMOS = ["delhi-informal-workers", "bangladesh-funding", "low-cost-sensors"]


INLINE = r"</?(a|span|strong|em|b|i|abbr|cite|code|del)\b[^>]*>"
def norm(t):
    t = re.sub(INLINE, "", t)                              # inline markup never adds a word break
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)        # Markdown links -> their text
    t = t.replace("\\", "").replace("**", "")
    t = re.sub(r"(?<!\w)[*_]([^*_]+)[*_](?!\w)", r"\1", t)  # Markdown emphasis
    t = re.sub(r"\s+", " ", t)
    return re.sub(r"\s+([.,;:)])", r"\1", t)


def run(dist):
    errs, rows = [], []
    claims = {c["claim_id"]: c for c in json.load(open(os.path.join(dist, "downloads/data/claims.json")))["claims"]}
    atlas = json.load(open(os.path.join(dist, "downloads/data/organisations-atlas.json")))
    flows = {f["flow_id"]: f for f in atlas["funding_flows"]}
    for d in DEMOS:
        base = os.path.join(dist, "packs", "questions", d)
        j = json.load(open(base + ".json", encoding="utf-8"))
        h_raw = open(base + ".html", encoding="utf-8").read(); h = norm(h_raw.split("<main", 1)[1])
        m_raw = open(base + ".md", encoding="utf-8").read(); m = norm(m_raw)
        ids_j = [c["claim_id"] for c in j["known"]]
        ids_h = set(re.findall(r"claims\.html#(C\d{3})", h_raw.split("<main", 1)[1]))
        ids_m = set(re.findall(r"claims\.html#(C\d{3})", m_raw))
        if set(ids_j) - ids_h: errs.append(f"{d}: JSON claims missing from HTML {sorted(set(ids_j) - ids_h)}")
        if set(ids_j) - ids_m: errs.append(f"{d}: JSON claims missing from Markdown {sorted(set(ids_j) - ids_m)}")
        for c in j["known"]:
            canon = claims[c["claim_id"]]
            if c["text"] != canon["text"]: errs.append(f"{d}: {c['claim_id']} text differs from claims.json")
            if c["verification_state"] != canon["verification_state"]: errs.append(f"{d}: {c['claim_id']} state differs from claims.json")
            for label, txt in (("HTML", h), ("Markdown", m)):
                if norm(c["text"])[:120] not in txt: errs.append(f"{d}: {c['claim_id']} text not found in {label}")
                if c["verification_label"] not in txt: errs.append(f"{d}: {c['claim_id']} verification label not in {label}")
        for k in ("audience_note",):
            if j[k] and (norm(j[k]) not in h or norm(j[k]) not in m): errs.append(f"{d}: {k} differs between formats")
        first = norm(j["short_answer"]).split(". ")[0]
        if first not in h or first not in m: errs.append(f"{d}: short answer opening differs between formats")
        for p in j["funding_records"]:
            for label, txt in (("HTML", h), ("Markdown", m)):
                for v in (p["amount_text"], p["stage_in_source"], p["funding_stage"]):
                    if norm(v) not in txt: errs.append(f"{d}: funding record {p['record_id']} value '{v}' missing from {label}")
            page = norm(open(os.path.join(dist, "organisations", "funding", p["record_id"].lower() + ".html"), encoding="utf-8").read())
            if norm(p["amount_text"]) not in page: errs.append(f"{d}: {p['record_id']} amount differs from its funding page")
        for f in j["funding_links"]:
            canon = flows[f["flow_id"]]
            if (f["amount"] or "") != (canon["amount"] or ""): errs.append(f"{d}: {f['flow_id']} amount differs from organisations-atlas.json")
            if f["stage_in_source"] != canon["commitment_or_disbursement"]: errs.append(f"{d}: {f['flow_id']} stage differs from atlas export")
            for label, txt in (("HTML", h), ("Markdown", m)):
                if norm(f["amount_text"]) not in txt: errs.append(f"{d}: {f['flow_id']} amount text missing from {label}")
        for label, txt in (("HTML", h), ("Markdown", m)):
            if "22 November 2026" not in txt and "2026-11-22" not in txt: errs.append(f"{d}: cutoff missing from {label}")
            hit = RANKING.search(txt)
            if hit: errs.append(f"{d}: ranking language in {label}: '{hit.group(0)}'")
        if j["research_cutoff"] != "2026-11-22": errs.append(f"{d}: JSON cutoff wrong")
        rows.append((d, len(ids_j), len(j["funding_records"]) + len(j["funding_links"]), len(j["source_ids"])))
    return errs, rows


def self_test(dist):
    """Tamper with one value in a copy of the build; the comparison must notice."""
    import shutil, tempfile
    tmp = tempfile.mkdtemp(prefix="ca-fmt-"); bad = os.path.join(tmp, "dist")
    shutil.copytree(dist, bad, ignore=shutil.ignore_patterns("*.pdf"))
    p = os.path.join(bad, "packs", "questions", "bangladesh-funding.json"); j = json.load(open(p))
    j["funding_records"][0]["amount_text"] = "USD 29.00 million (approved project financing)"   # an agent-only drift
    j["known"][0]["text"] = j["known"][0]["text"].replace("290", "209")
    json.dump(j, open(p, "w"))
    errs, _ = run(bad); shutil.rmtree(tmp)
    print(f"format self-test: tampered JSON -> {len(errs)} errors")
    return 0 if len(errs) >= 2 else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv: sys.exit(self_test(os.path.join(ROOT, "site", "dist")))
    dist = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "site", "dist")
    errs, rows = run(dist)
    for d, nc, nf, ns in rows: print(f"  {d}: {nc} claims, {nf} funding items, {ns} sources identical across HTML, Markdown and JSON" if not errs else f"  {d}")
    for e in errs: print("ERROR", e)
    print(f"format comparison: {len(errs)} errors across {len(rows)} worked questions")
    sys.exit(1 if errs else 0)
