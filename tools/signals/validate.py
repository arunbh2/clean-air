"""Validate the Latest Signals store, registry and review decisions.

Run:  python3 tools/signals/validate.py [research_dir]
Checks: JSON Schema (research/signals/schema.json), unique IDs and DOIs, HTTPS links, related IDs exist, no evidence-strength
label anywhere in the store, registry fields and tested endpoints, and the review-decision rules that keep discovery apart from
evidence (an editorial note needs a review status and source references; promotion needs an existing claim whose sources
include this record; funding amounts need a stated stage and a checked date and never feed verified totals).
"""
import csv
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
EVIDENCE_LABELS = re.compile(r"\b(Strong|Moderate|Limited/mixed|No adequate evidence found)\b")
REVIEW_STATES = ["discovered_unreviewed", "metadata_checked", "editorial_reviewed", "evidence_promoted", "excluded", "withdrawn"]
FUNDING_STAGES = ["requested", "announced", "pledged", "approved", "contracted", "disbursed", "evaluated"]
DECISION_COLS = ["signal_id", "review_status", "reviewed_on", "reviewer", "checked_fields", "why_it_may_matter", "note_source_refs",
                 "related_claim_ids", "related_intervention_ids", "featured", "study_question", "study_design", "study_outcomes", "study_limits",
                 "funding_stage", "announced_amount", "currency", "recipient", "instrument", "reason"]


def _schema_errors(doc, schema):
    try:
        import jsonschema
    except ImportError:
        return ["jsonschema is not installed (pip install -r site/requirements.txt)"]
    v = jsonschema.Draft202012Validator(schema)
    return [f"schema: {'/'.join(map(str, e.absolute_path))}: {e.message[:160]}" for e in sorted(v.iter_errors(doc), key=lambda e: list(e.absolute_path))]


def validate_store(doc, res):
    errs = _schema_errors(doc, json.load(open(os.path.join(res, "signals", "schema.json"), encoding="utf-8")))
    recs = doc.get("records", [])
    ids = [r.get("signal_id") for r in recs]
    if len(ids) != len(set(ids)): errs.append("integrity: duplicate signal_id")
    dois = [r["doi_or_persistent_id"] for r in recs if (r.get("doi_or_persistent_id") or "").startswith("10.")]
    if len(dois) != len(set(dois)): errs.append("integrity: the same DOI appears in two records")
    known = set(ids)
    for r in recs:
        for x in r.get("related_signal_ids", []):
            if x["signal_id"] not in known: errs.append(f"integrity: {r['signal_id']} links to unknown {x['signal_id']}")
        if EVIDENCE_LABELS.search(json.dumps({k: v for k, v in r.items() if k not in ("title_original", "journal", "inclusion_reason")})):
            errs.append(f"evidence: {r['signal_id']} carries an evidence-strength label; signals are never rated")
        if r.get("related_claim_ids"): errs.append(f"evidence: {r['signal_id']} has claim links in the machine store; claim links come only from reviewed decisions")
    return errs


def validate_registry(res):
    errs = []
    reg = yaml.safe_load(open(os.path.join(res, "signals", "sources.yml"), encoding="utf-8"))
    seen = set()
    for s in reg["sources"]:
        if s["id"] in seen: errs.append(f"registry: duplicate id {s['id']}")
        seen.add(s["id"])
        if not str(s.get("endpoint", "")).startswith("https://"): errs.append(f"registry: {s['id']} endpoint is not HTTPS")
        if not s.get("test") or not s["test"].get("date"): errs.append(f"registry: {s['id']} has no recorded connector test")
        if s.get("enabled"):
            for k in ("publisher", "org_type", "provenance_kind", "default_type", "access", "rights", "requires", "licence_notes"):
                if k not in s: errs.append(f"registry: enabled source {s['id']} lacks {k}")
            if s.get("test", {}).get("status") != 200: errs.append(f"registry: {s['id']} is enabled but its last test was not HTTP 200")
            if s.get("rights") != "metadata_only": errs.append(f"registry: {s['id']} rights must be metadata_only")
    return errs


def validate_reviews(res, store_ids):
    errs = []
    p = os.path.join(res, "signals", "review-decisions.csv")
    if not os.path.exists(p): return ["reviews: research/signals/review-decisions.csv is missing"]
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    with open(p, encoding="utf-8") as f: header = next(csv.reader(f))
    if header != DECISION_COLS: errs.append(f"reviews: header must be {','.join(DECISION_COLS)}")
    cpath = os.path.join(res, "data", "claims.csv")
    claims = {c["claim_id"]: c for c in csv.DictReader(open(cpath, encoding="utf-8"))} if os.path.exists(cpath) else {}
    spath = os.path.join(res, "data", "sources.csv")
    srcs = {s["source_id"]: s for s in csv.DictReader(open(spath, encoding="utf-8"))} if os.path.exists(spath) else {}
    store = {}
    sp = os.path.join(res, "signals", "signals.json")
    if os.path.exists(sp): store = {r["signal_id"]: r for r in json.load(open(sp, encoding="utf-8"))["records"]}
    for i, r in enumerate(rows, 2):
        sid, st = r["signal_id"], r["review_status"]
        if sid not in store_ids: errs.append(f"reviews:{i} {sid} is not in the signal store")
        if st not in REVIEW_STATES[1:]: errs.append(f"reviews:{i} unknown review_status '{st}'")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["reviewed_on"] or ""): errs.append(f"reviews:{i} reviewed_on must be YYYY-MM-DD")
        if not r["reviewer"].strip(): errs.append(f"reviews:{i} reviewer role is required")
        if (r["why_it_may_matter"] or r["study_question"] or r["featured"] == "yes") and st not in ("editorial_reviewed", "evidence_promoted"):
            errs.append(f"reviews:{i} an editorial note, study summary or featured flag needs editorial_reviewed or evidence_promoted")
        if r["why_it_may_matter"] and not r["note_source_refs"].strip(): errs.append(f"reviews:{i} an editorial note needs note_source_refs")
        if r["study_question"] and not all(r[k].strip() for k in ("study_design", "study_outcomes", "study_limits")):
            errs.append(f"reviews:{i} a study summary needs design, outcomes and limits read from the source")
        if r["related_claim_ids"] and st != "evidence_promoted": errs.append(f"reviews:{i} claim links need evidence_promoted")
        if st == "evidence_promoted":
            cl = [c for c in r["related_claim_ids"].split(";") if c]
            if not cl: errs.append(f"reviews:{i} evidence_promoted needs related_claim_ids")
            rec = store.get(sid, {})
            for c in cl:
                if c not in claims: errs.append(f"reviews:{i} claim {c} does not exist; only the research edition creates claims"); continue
                urls = {srcs[s]["url"].rstrip("/") for s in claims[c]["source_ids"].split(";") if s in srcs}
                doi = rec.get("doi_or_persistent_id") or ""
                if rec.get("canonical_url", "").rstrip("/") not in urls and not any(doi and doi in u.lower() for u in urls):
                    errs.append(f"reviews:{i} claim {c} does not cite this record's source; promotion needs a canonical claim-source link")
        if r["announced_amount"]:
            if r["funding_stage"] not in FUNDING_STAGES: errs.append(f"reviews:{i} an amount needs a funding_stage from {FUNDING_STAGES}")
            if not r["currency"] or "amount" not in r["checked_fields"]: errs.append(f"reviews:{i} an amount needs a currency and 'amount' in checked_fields")
        if r["funding_stage"] and r["funding_stage"] not in FUNDING_STAGES: errs.append(f"reviews:{i} unknown funding_stage")
    return errs


def main():
    res = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else os.path.join(ROOT, "research")
    doc = json.load(open(os.path.join(res, "signals", "signals.json"), encoding="utf-8"))
    errs = validate_store(doc, res) + validate_registry(res) + validate_reviews(res, {r["signal_id"] for r in doc["records"]})
    for e in errs: print("ERROR", e)
    print(f"signals: {len(doc['records'])} records, {len(errs)} errors")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
