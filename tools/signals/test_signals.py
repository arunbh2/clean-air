"""Fixture tests for the Latest Signals pipeline (docs/live-signals-master-brief.md, section 10, points 1-9 and 13).

Run:  python3 tools/signals/test_signals.py
Deterministic: captured fixtures in tools/fixtures/signals/ and a fake fetcher; no live provider is contacted.
"""
import copy
import csv
import datetime as dt
import json
import os
import shutil
import sys
import tempfile
import urllib.error

import yaml

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import common  # noqa: E402
import ingest  # noqa: E402
import validate  # noqa: E402
from common import FetchError  # noqa: E402

FX = os.path.join(ROOT, "tools", "fixtures", "signals")
NOW = dt.datetime(2026, 11, 23, 12, 0, 0, tzinfo=dt.timezone.utc)
failures, passed = [], 0


def check(name, cond, detail=""):
    global passed
    if cond: passed += 1
    else: failures.append(f"{name} {detail}")


def fx(name): return open(os.path.join(FX, name), "rb").read()


def src(id_, access, endpoint, **kw):
    s = {"id": id_, "name": id_, "publisher": kw.pop("publisher", id_.title() + " Publisher"), "org_type": "newsroom", "provenance_kind": "independent_reporting",
         "default_type": "news", "access": access, "endpoint": endpoint, "rights": "metadata_only", "scope": "regional", "requires": ["pollution"],
         "language": "en", "licence_notes": "fixture", "test": {"date": "2026-11-23", "status": 200, "result": "fixture"}, "enabled": True}
    s.update(kw); return s


def make_res(sources):
    tmp = tempfile.mkdtemp(prefix="ca-signals-")
    res = os.path.join(tmp, "research"); os.makedirs(os.path.join(res, "signals")); os.makedirs(os.path.join(res, "data"))
    for f in ("taxonomy.yml", "schema.json"): shutil.copy(os.path.join(ROOT, "research", "signals", f), os.path.join(res, "signals", f))
    for f in ("organisations.csv", "claims.csv", "sources.csv"): shutil.copy(os.path.join(ROOT, "research", "data", f), os.path.join(res, "data", f))
    reg = {"user_agent": "test", "defaults": {"timeout_seconds": 5, "max_bytes": 100000, "retries": 0, "window_days": 365, "archive_days": 400}, "sources": sources}
    yaml.safe_dump(reg, open(os.path.join(res, "signals", "sources.yml"), "w"))
    open(os.path.join(res, "signals", "review-decisions.csv"), "w").write(",".join(validate.DECISION_COLS) + "\n")
    return tmp, res


def fetcher_from(mapping):
    def f(s, url):
        v = mapping[s["id"]]
        if isinstance(v, Exception): raise v
        return v
    return f


def by_title(doc, frag):
    return [r for r in doc["records"] if frag.lower() in r["title_original"].lower()]


# ---------- 1, 3, 4, 5, 7: RSS / Atom, duplicates, dates, geography, safety ----------
srcs = [src("fx-news", "rss", "https://news.example.org/feed"), src("fx-wire", "rss", "https://wire.example.com/rss", publisher="Wire Service"),
        src("fx-inst", "atom", "https://institute.example.org/atom", default_type="report", org_type="research", provenance_kind="publisher_report",
            requires=["pollution", "place"], scope="global")]
tmp, res = make_res(srcs)
rep, doc, status = ingest.run(res, fetcher=fetcher_from({"fx-news": (200, fx("rss_mixed.xml"), {}), "fx-wire": (200, fx("rss_other.xml"), {}),
                                                          "fx-inst": (200, fx("atom.xml"), {})}), now=NOW, env={})
check("store validates", not rep["schema_errors"], rep["schema_errors"][:3])
delhi = by_title(doc, "Delhi air quality turns severe")
check("tracker-only duplicate merged into one record per publisher", len([r for r in delhi if r["source_registry_id"] == "fx-news"]) == 1)
check("tracking parameters removed, meaningful ones kept", any(r["canonical_url"] == "https://news.example.org/2026/11/20/delhi-aqi?id=7" for r in delhi), [r["canonical_url"] for r in delhi])
check("syndicated coverage kept separate and linked", len(delhi) == 2 and all(any(x["relation"] == "same story, other publisher" for x in r["related_signal_ids"]) for r in delhi))
dk = by_title(doc, "brick kilns")
check("double-escaped HTML decoded", dk and dk[0]["title_original"] == "Dhaka’s brick kilns: a winter of haze & coughs", dk and dk[0]["title_original"])
check("two-digit RSS year read as 2026", dk and dk[0]["published_at"].startswith("2026-11-16"), dk and dk[0]["published_at"])
check("Bangladesh tagged from a city in the title", dk and dk[0]["countries"] == ["bangladesh"])
ktm = by_title(doc, "Kathmandu air pollution")
check("non-ASCII title preserved", ktm and "काठमाडौँ" in ktm[0]["title_original"])
check("missing date stays unknown, never invented", ktm and ktm[0]["published_at"] is None and ktm[0]["published_date_precision"] == "unknown")
lh = by_title(doc, "closes schools")
check("script markup removed from title", lh and "<" not in lh[0]["title_original"] and "script" not in lh[0]["title_original"].lower(), lh and lh[0]["title_original"])
excl = {x["title"]: x["reason"] for x in rep["excluded_sample"]}
check("javascript: link rejected", any("Bangkok" in t and "HTTPS" in r for t, r in excl.items()), excl)
check("http: link rejected", any("officials respond" in t and "HTTPS" in r for t, r in excl.items()))
check("instruction-like title held for review, not published", any("Ignore previous" in t and r.startswith("held for review") for t, r in excl.items()) and not by_title(doc, "Ignore previous"))
check("water pollution excluded", any("Ganga" in t for t in excl))
check("title naming a place outside scope excluded even if the summary names India", any("Ghana" in t and "outside" in r for t, r in excl.items()))
check("the word 'us' is not read as the United States", bool(by_title(doc, "affects us all")))
check("airline false positive excluded", any("Air India" in t for t in excl))
pj = by_title(doc, "Punjab")
check("ambiguous place name gives no country tag", pj and pj[0]["countries"] == [] and pj[0]["ambiguous_places"] == ["punjab"])
oc = by_title(doc, "Indian Ocean")
check("'Indian Ocean' is not India", (not oc) or "india" not in oc[0]["countries"])
fut = by_title(doc, "Jakarta")
check("future-dated item flagged as an anomaly", fut and fut[0]["date_flag"] == "future-dated", fut and fut[0]["date_flag"])
check("regional cross-border record keeps both countries", fut and fut[0]["countries"] == ["indonesia", "singapore"])
vn = by_title(doc, "Vietnam updated")
check("update date kept apart from original publication date", vn and vn[0]["published_at"].startswith("2025-12-02") and vn[0]["source_updated_at"] == "2026-11-10T00:00:00Z", vn and (vn[0]["published_at"], vn[0]["source_updated_at"]))
bh = by_title(doc, "Bihar")
check("Atom entry parsed with published date", bh and bh[0]["published_at"].startswith("2026-11-12") and bh[0]["source_type"] == "report")
gr = by_title(doc, "Grant programme")
check("institutional grant announcement typed as funding", gr and gr[0]["source_type"] == "funding", gr and gr[0]["source_type"])
check("no stored article text: records hold no summary field", all("summary" not in r and "description" not in r for r in doc["records"]))
check("every record starts unreviewed", all(r["review_status"] == "discovered_unreviewed" for r in doc["records"]))
first_ids = {r["signal_id"] for r in doc["records"]}

# unchanged feed (304), source URL change, partial failure, stale data kept
later = NOW + dt.timedelta(hours=12)
moved = fx("rss_other.xml").replace(b"https://wire.example.com/delhi-air-severe", b"https://wire.example.com/2026/11/20/delhi-air-severe-update")
rep2, doc2, status2 = ingest.run(res, fetcher=fetcher_from({"fx-news": (304, None, {}), "fx-wire": (200, moved, {}),
                                                            "fx-inst": FetchError("rate_limited", "HTTP 429", 429)}), now=later, env={})
check("304 counted as a successful unchanged check", any(s["source"] == "fx-news" and s["result"].startswith("unchanged") for s in rep2["sources"]))
check("429 isolated to one source", rep2["outcome"] == "partial" and any(s["source"] == "fx-inst" and "rate_limited" in s["result"] for s in rep2["sources"]))
check("records kept when a source fails or is unchanged", first_ids <= {r["signal_id"] for r in doc2["records"]})
wire = [r for r in doc2["records"] if r["source_registry_id"] == "fx-wire"]
check("same story at a new address updates the record, keeps the old address", len(wire) == 1 and wire[0]["previous_urls"] == ["https://wire.example.com/delhi-air-severe"], wire and wire[0].get("previous_urls"))
check("last successful refresh moves forward on partial success", status2["last_successful_refresh"] == common.iso(later))
rep3, doc3, status3 = ingest.run(res, fetcher=fetcher_from({"fx-news": FetchError("timeout", "timed out"), "fx-wire": (200, fx("malformed.xml"), {}),
                                                            "fx-inst": (200, fx("html_page.xml"), {})}), now=later + dt.timedelta(hours=12), env={})
check("all sources failing is reported honestly", rep3["outcome"] == "all sources failed")
check("last successful refresh stays historical when ingestion fails", status3["last_successful_refresh"] == common.iso(later), status3["last_successful_refresh"])
check("malformed feed reported", any("malformed" in s["result"] for s in rep3["sources"]))
check("bot-check HTML page reported, not parsed", any(s["source"] == "fx-inst" and "HTML" in s["result"] for s in rep3["sources"]))
check("stale valid data recovered on the next run", len(json.load(open(os.path.join(res, "signals", "signals.json")))["records"]) == len(doc2["records"]))
try:
    from parse import parse_feed
    parse_feed(fx("bomb.xml")); check("entity declarations refused", False)
except ValueError:
    check("entity declarations refused", True)
q = list(csv.DictReader(open(os.path.join(res, "signals", "review-queue.csv"), encoding="utf-8")))
check("review queue lists every unreviewed record", len(q) == len(doc2["records"]))
shutil.rmtree(tmp)

# ---------- 2, 9: research metadata, versions, corrections, DOI forms ----------
rs = [src("fx-epmc", "api_europepmc", "https://epmc.example.org/search", default_type="research", provenance_kind="peer_reviewed_metadata", scope="global",
          requires=["pollution", "place"], pollution_in_title=True, query="q"),
      src("fx-cr", "api_crossref", "https://cr.example.org/works", default_type="research", provenance_kind="peer_reviewed_metadata", scope="global",
          requires=["pollution", "place"], pollution_in_title=True, query="q"),
      src("fx-oa", "api_openalex", "https://oa.example.org/works", default_type="research", provenance_kind="peer_reviewed_metadata", scope="global",
          requires=["pollution", "place"], pollution_in_title=True, query="q", secret="OPENALEX_API_KEY")]
tmp, res = make_res(rs)
fm = fetcher_from({"fx-epmc": (200, fx("europepmc.json"), {}), "fx-cr": (200, fx("crossref.json"), {}), "fx-oa": (200, fx("openalex.json"), {})})
rep, doc, _ = ingest.run(res, fetcher=fm, now=NOW, env={})
check("research store validates", not rep["schema_errors"], rep["schema_errors"][:3])
check("missing secret skips the source gracefully", any(s["source"] == "fx-oa" and s["result"].startswith("skipped: secret") for s in rep["sources"]))
j = [r for r in doc["records"] if r["doi_or_persistent_id"] == "10.1000/abc.2026.1"]
check("same DOI from two indexes is one record", len(j) == 1 and j[0]["also_listed_by"] == ["fx-cr"], [(r["signal_id"], r["also_listed_by"]) for r in j])
check("entity-encoded markup in a title becomes plain text", j and j[0]["title_original"].startswith("Fine particulate (PM2.5)"), j and j[0]["title_original"])
pre = [r for r in doc["records"] if r["is_preprint"]]
check("preprint labelled and linked to the journal version", pre and pre[0]["source_type"] == "preprint" and pre[0]["provenance_kind"] == "preprint"
      and any(x["relation"] == "version" and x["signal_id"] == j[0]["signal_id"] for x in pre[0]["related_signal_ids"]))
old = [r for r in doc["records"] if r["doi_or_persistent_id"] == "10.1000/old.2024.9"]
check("2024 paper indexed in 2026 kept with its real date", old and old[0]["published_at"] == "2024-03-01" and old[0]["indexed_at"] == "2026-11-20")
check("retraction notice marks the original as retracted", old and old[0]["correction_status"] == "retracted"
      and any(x["relation"] == "correction" for x in old[0]["related_signal_ids"]), old and old[0]["correction_status"])
fu = [r for r in doc["records"] if r["doi_or_persistent_id"] == "10.1000/future.1"]
check("issue date in 2027 flagged as future-dated", fu and fu[0]["date_flag"] == "future-dated" and fu[0]["published_date_precision"] == "month")
gl = [r for r in doc["records"] if r["doi_or_persistent_id"] == "10.1000/global.1"]
check("multi-country abstract not tagged country by country", gl and gl[0]["countries"] == [] and gl[0]["cross_border_region"])
check("DOI URL forms normalise to one identifier", common.norm_doi("https://doi.org/10.1000/ABC.2026.1") == common.norm_doi("doi:10.1000/abc.2026.1") ==
      common.norm_doi("http://dx.doi.org/10.1000/abc.2026.1") == "10.1000/abc.2026.1")
rep_k, doc_k, _ = ingest.run(res, fetcher=fm, now=NOW + dt.timedelta(hours=1), env={"OPENALEX_API_KEY": "secret-value-123"}, write=False)
oa = [s for s in rep_k["sources"] if s["source"] == "fx-oa"][0]
check("API key used but redacted from the run report", oa["result"] == "ok" and "secret-value-123" not in json.dumps(rep_k) and "REDACTED" in oa["request"])
check("unreviewed research never carries claim IDs", all(not r["related_claim_ids"] for r in doc["records"]))

# ---------- 6, 7: HTTP client: retries, 429, blocked hosts and schemes ----------
calls, waits = [], []
class FakeResp:
    status = 200; headers = {}
    def __init__(self, b): self.b = b
    def read(self, n): return self.b
    def __enter__(self): return self
    def __exit__(self, *a): return False
class FakeOpener:
    def open(self, req, timeout):
        calls.append(req.full_url)
        if len(calls) <= 2: raise urllib.error.HTTPError(req.full_url, 429, "Too Many", {"Retry-After": "3"}, None)
        return FakeResp(b"<rss/>")
orig = common.urllib.request.build_opener
common.urllib.request.build_opener = lambda *a: FakeOpener()
try:
    st, body, _ = common.http_get("https://ok.example.org/feed", allow_hosts={"ok.example.org"}, user_agent="t", retries=2, sleep=waits.append)
    check("429 retried with Retry-After backoff, then succeeds", st == 200 and waits == [3, 3] and len(calls) == 3, (waits, calls))
    calls.clear()
    try: common.http_get("https://ok.example.org/feed", allow_hosts={"ok.example.org"}, user_agent="t", retries=1, sleep=waits.append); check("persistent 429 raises", False)
    except FetchError as e: check("persistent 429 raises rate_limited", e.kind == "rate_limited")
finally:
    common.urllib.request.build_opener = orig
for bad in ("http://ok.example.org/feed", "https://evil.example.net/feed", "file:///etc/passwd"):
    try: common.http_get(bad, allow_hosts={"ok.example.org"}, user_agent="t"); check(f"blocked {bad}", False)
    except FetchError as e: check(f"blocked {bad}", e.kind == "blocked")
for u in ("javascript:alert(1)", "data:text/html,x", "https://x.org/a b", "ftp://x.org/f"): check(f"canonical_url rejects {u}", common.canonical_url(u) is None)
check("date from article address", common.date_from_url("https://kathmandupost.com/national/2026/11/23/story") == ("2026-11-23", "day"))

# ---------- 6, 8, 9: schema guards and review rules ----------
good = copy.deepcopy(doc)
bad = copy.deepcopy(doc); r0 = bad["records"][0]
r0["canonical_url"] = "javascript:alert(1)"; r0["review_status"] = "evidence_promoted"; r0["related_claim_ids"] = ["C001"]
e = validate.validate_store(bad, res)
check("schema rejects a javascript URL", any("canonical_url" in x for x in e))
check("schema rejects ingestion-side promotion", any("review_status" in x for x in e))
check("store rejects claim links outside the review workflow", any("claim links" in x for x in e))
bad2 = copy.deepcopy(doc); bad2["records"][0]["subjects"] = ["health"]; bad2["records"][0]["publication_type_in_source"] = "Strong"
check("store rejects an evidence-strength label", any("evidence-strength" in x for x in validate.validate_store(bad2, res)))
sid = j[0]["signal_id"]
rows = [
    {"signal_id": sid, "review_status": "discovered_unreviewed", "reviewed_on": "2026-11-23", "reviewer": "curator", "why_it_may_matter": "x"},
    {"signal_id": sid, "review_status": "metadata_checked", "reviewed_on": "2026-11-23", "reviewer": "curator", "why_it_may_matter": "An interpretation."},
    {"signal_id": sid, "review_status": "evidence_promoted", "reviewed_on": "2026-11-23", "reviewer": "curator", "related_claim_ids": "C999"},
    {"signal_id": sid, "review_status": "evidence_promoted", "reviewed_on": "2026-11-23", "reviewer": "curator", "related_claim_ids": "C001"},
    {"signal_id": sid, "review_status": "metadata_checked", "reviewed_on": "2026-11-23", "reviewer": "curator", "announced_amount": "5000000", "currency": "USD"},
    {"signal_id": sid, "review_status": "editorial_reviewed", "reviewed_on": "2026-11-23", "reviewer": "curator", "study_question": "Does X?"},
]
with open(os.path.join(res, "signals", "review-decisions.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, validate.DECISION_COLS); w.writeheader(); [w.writerow({k: r.get(k, "") for k in validate.DECISION_COLS}) for r in rows]
e = validate.validate_reviews(res, {r["signal_id"] for r in doc["records"]})
check("unknown review state rejected", any("reviews:2" in x and "unknown review_status" in x for x in e))
check("editorial note without editorial review rejected", any("reviews:3" in x and "editorial_reviewed" in x for x in e))
check("editorial note without source references rejected", any("reviews:3" in x and "note_source_refs" in x for x in e))
check("promotion to a claim that does not exist rejected", any("reviews:4" in x and "does not exist" in x for x in e))
check("promotion to a claim that does not cite the source rejected", any("reviews:5" in x and "does not cite" in x for x in e))
check("amount without a funding stage rejected (announced is not approved is not disbursed)", any("reviews:6" in x and "funding_stage" in x for x in e))
check("study summary without design, outcomes and limits rejected", any("reviews:7" in x and "study summary" in x for x in e))
with open(os.path.join(res, "signals", "review-decisions.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, validate.DECISION_COLS); w.writeheader()
    w.writerow({k: "" for k in validate.DECISION_COLS} | {"signal_id": sid, "review_status": "metadata_checked", "reviewed_on": "2026-11-23", "reviewer": "curator", "checked_fields": "title;date;publisher"})
check("a valid metadata check passes", validate.validate_reviews(res, {r["signal_id"] for r in doc["records"]}) == [])
shutil.rmtree(tmp)

print(f"signals tests: {passed} passed, {len(failures)} failed")
for f in failures: print("FAIL", f)
sys.exit(1 if failures else 0)
