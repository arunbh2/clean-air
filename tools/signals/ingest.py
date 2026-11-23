"""Latest Signals ingestion: fetch -> parse -> normalise -> classify -> deduplicate -> merge -> report.

Run:  python3 tools/signals/ingest.py                 (live: every enabled source in research/signals/sources.yml)
      python3 tools/signals/ingest.py --only europepmc,who-news
      python3 tools/signals/ingest.py --dry-run         (fetch and report; write nothing)
Writes (all under research/signals/): signals.json (record store), status.json (last successful refresh, per source),
run-report.json (this run), runs.csv (one row per run), review-queue.csv (generated list of unreviewed records),
http-cache.json (ETag / Last-Modified). Existing records are never deleted when a source fails or drops an item.
Exit 1 only for schema or integrity violations (malformed output); a failing source is isolated and reported.
"""
import argparse
import csv
import datetime as dt
import json
import os
import sys
import urllib.parse

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from common import (FetchError, UTC, canonical_url, clean_text, date_from_url, http_get, iso, norm_doi, norm_title,  # noqa: E402
                    parse_date, signal_id, title_similarity, to_dt)
from classify import Rules  # noqa: E402
from parse import PARSERS  # noqa: E402
import validate  # noqa: E402

FIELDS_ORDER = ["signal_id", "source_registry_id", "also_listed_by", "canonical_url", "previous_urls", "doi_or_persistent_id", "title_original",
                "language", "publisher", "journal", "publication_type_in_source", "source_type", "provenance_kind", "is_preprint", "published_at",
                "published_date_precision", "date_basis", "date_flag", "source_updated_at", "indexed_at", "discovered_at", "last_checked_at",
                "countries", "country_basis", "cross_border_region", "ambiguous_places", "subjects", "organisation_ids", "related_intervention_ids",
                "related_claim_ids", "funding_record_id", "review_status", "correction_status", "corrects_doi", "external_rights",
                "related_signal_ids", "inclusion_reason", "content_flags", "feed_run_id"]


def load_registry(res):
    return yaml.safe_load(open(os.path.join(res, "signals", "sources.yml"), encoding="utf-8"))


def request_url(src, defaults, since, now, env):
    """Build the exact request URL for a source. Secrets come from the environment only and never reach output files."""
    e = src["endpoint"]
    if src["access"] == "api_europepmc":
        q = f'{src["query"]} AND FIRST_PDATE:[{since:%Y-%m-%d} TO {now:%Y-%m-%d}]'
        return e + "?" + urllib.parse.urlencode({"query": q, "format": "json", "resultType": "core", "pageSize": src.get("page_size", 100), "sort": "FIRST_PDATE_D desc"})
    if src["access"] == "api_crossref":
        return e + "?" + urllib.parse.urlencode({"query.bibliographic": src["query"], "filter": f"from-pub-date:{since:%Y-%m-%d},until-pub-date:{now:%Y-%m-%d},type:journal-article,type:posted-content",
                                                 "rows": src.get("rows", 100), "sort": "published", "order": "desc"})
    if src["access"] == "api_openalex":
        p = {"search": src["query"], "filter": f"from_publication_date:{since:%Y-%m-%d}", "per-page": 100, "sort": "publication_date:desc"}
        if src.get("secret") and env.get(src["secret"]): p["api_key"] = env[src["secret"]]
        return e + "?" + urllib.parse.urlencode(p)
    return e


def redact(url):
    p = urllib.parse.urlsplit(url)
    q = [(k, "REDACTED" if k.lower() in ("api_key", "key", "token", "mailto") else v) for k, v in urllib.parse.parse_qsl(p.query)]
    return urllib.parse.urlunsplit(p._replace(query=urllib.parse.urlencode(q)))


def live_fetcher(reg, cache):
    allow = {urllib.parse.urlsplit(s["endpoint"]).hostname for s in reg["sources"] if s.get("enabled")}
    d = reg["defaults"]
    def fetch(src, url):
        return http_get(url, allow_hosts=allow, user_agent=reg["user_agent"], timeout=d["timeout_seconds"], max_bytes=d["max_bytes"],
                        retries=d["retries"], cache=cache)
    return fetch


def make_record(item, src, cls, now_iso, run_id):
    url = canonical_url(item.get("url"))
    doi = item.get("doi")
    pid = doi or item.get("pid")
    pub, prec = parse_date(item.get("published"))
    basis = "source" if pub else "none"
    if not pub:
        pub, prec = date_from_url(url)
        basis = "article address" if pub else "none"
    upd, _ = parse_date(item.get("updated"))
    idx, _ = parse_date(item.get("indexed"))
    corr = item.get("correction") or {}
    rec = {"signal_id": signal_id(f"doi:{doi}" if doi else (pid or url)), "source_registry_id": src["id"], "also_listed_by": [],
           "canonical_url": url, "previous_urls": [], "doi_or_persistent_id": pid, "title_original": clean_text(item.get("title"), 400),
           "language": src.get("language", "en"), "publisher": clean_text(item.get("publisher") if item.get("publisher") and src["access"].startswith("api_") else src["publisher"], 200), "journal": clean_text(item.get("journal"), 300) or None,
           "publication_type_in_source": clean_text(item.get("publication_type"), 200) or None, "source_type": cls["source_type"],
           "provenance_kind": cls["provenance_kind"], "is_preprint": bool(item.get("is_preprint")), "published_at": pub,
           "published_date_precision": prec, "date_basis": basis, "date_flag": "", "source_updated_at": upd if upd and upd != pub else None,
           "indexed_at": idx, "discovered_at": now_iso, "last_checked_at": now_iso, "countries": cls["countries"],
           "country_basis": cls["country_basis"], "cross_border_region": cls["cross_border_region"], "ambiguous_places": cls["ambiguous_places"],
           "subjects": cls["subjects"], "organisation_ids": cls["organisation_ids"], "related_intervention_ids": cls["related_intervention_ids"],
           "related_claim_ids": [], "funding_record_id": None, "review_status": "discovered_unreviewed",
           "correction_status": {"retracted": "retracted", "corrected": "corrected", "updates another record": "updates another record"}.get(corr.get("status"), ""),
           "corrects_doi": corr.get("of"), "external_rights": "metadata_only", "related_signal_ids": [], "inclusion_reason": cls["_reason"],
           "content_flags": cls["content_flags"], "feed_run_id": run_id, "_versions": item.get("version_dois", [])}
    return rec


def date_flag(pub, now):
    d = to_dt(pub)
    if not d: return ""
    if d > now + dt.timedelta(hours=36): return "future-dated"
    if d > now: return "ahead of retrieval"
    return ""


def link(a, b, rel):
    if not any(x["signal_id"] == b["signal_id"] for x in a["related_signal_ids"]): a["related_signal_ids"].append({"signal_id": b["signal_id"], "relation": rel})
    if not any(x["signal_id"] == a["signal_id"] for x in b["related_signal_ids"]): b["related_signal_ids"].append({"signal_id": a["signal_id"], "relation": rel})


class Store:
    def __init__(self, records):
        self.by_id = {r["signal_id"]: r for r in records}
        self.by_doi = {r["doi_or_persistent_id"]: r for r in records if r.get("doi_or_persistent_id", "") and r["doi_or_persistent_id"].startswith("10.")}
        self.by_url = {}
        for r in records:
            for u in [r["canonical_url"]] + r.get("previous_urls", []): self.by_url[u] = r

    def add(self, r):
        self.by_id[r["signal_id"]] = r
        if r.get("doi_or_persistent_id", "") and str(r["doi_or_persistent_id"]).startswith("10."): self.by_doi[r["doi_or_persistent_id"]] = r
        self.by_url[r["canonical_url"]] = r

    def merge(self, new, now_iso, counts, log):
        """Deduplicate: exact DOI, then canonical URL, then a conservative title/publisher/date cluster."""
        doi = new["doi_or_persistent_id"] if (new["doi_or_persistent_id"] or "").startswith("10.") else None
        old = self.by_id.get(new["signal_id"]) or (self.by_doi.get(doi) if doi else None) or self.by_url.get(new["canonical_url"])
        how = "same signal ID" if new["signal_id"] in self.by_id else ("same DOI" if doi and doi in self.by_doi else "same URL")
        if not old:
            nt, nd = norm_title(new["title_original"]), to_dt(new["published_at"])
            for r in self.by_id.values():
                if (r["source_registry_id"] == new["source_registry_id"] and norm_title(r["title_original"]) == nt and len(nt) > 20
                        and not doi and not (r.get("doi_or_persistent_id") or "").startswith("10.") and r["source_type"] not in ("research", "preprint")):
                    old, how = r, "same title from the same source at a new address"
                    if r["last_checked_at"] == now_iso:     # listed twice in this run: keep the first address
                        if new["canonical_url"] != r["canonical_url"]: r["previous_urls"] = sorted(set(r["previous_urls"] + [new["canonical_url"]]))
                        self.by_url[new["canonical_url"]] = r; how = "listed twice in one feed"
                    elif new["canonical_url"] != r["canonical_url"]:
                        r["previous_urls"] = sorted(set(r["previous_urls"] + [r["canonical_url"]])); r["canonical_url"] = new["canonical_url"]
                        self.by_url[new["canonical_url"]] = r; counts["url_changed"] += 1
                    break
        if old:
            changed = False
            if new["source_registry_id"] != old["source_registry_id"] and new["source_registry_id"] not in old["also_listed_by"]:
                old["also_listed_by"] = sorted(old["also_listed_by"] + [new["source_registry_id"]]); changed = True
            if new["source_updated_at"] and new["source_updated_at"] != old.get("source_updated_at"):
                old["source_updated_at"] = new["source_updated_at"]; changed = True
            if new["correction_status"] and new["correction_status"] != old.get("correction_status"):
                old["correction_status"] = new["correction_status"]; changed = True
            old["last_checked_at"] = now_iso
            counts["updated" if changed else "duplicates"] += 1
            log.append({"title": new["title_original"][:120], "decision": "merged", "reason": how})
            return old
        # new record: link related versions and coverage without merging them
        nt, nd = new["title_original"], to_dt(new["published_at"])
        for r in list(self.by_id.values()):
            if new["_versions"] and r.get("doi_or_persistent_id") in new["_versions"]:
                link(new, r, "version"); continue
            sim = title_similarity(nt, r["title_original"])
            if sim < 0.85: continue
            rd = to_dt(r["published_at"])
            close = nd and rd and abs((nd - rd).days) <= 3
            research = {new["source_type"], r["source_type"]} <= {"research", "preprint"}
            if research and new["is_preprint"] != r.get("is_preprint", False): link(new, r, "version")
            elif close and not research and r["publisher"] != new["publisher"]: link(new, r, "same story, other publisher")
        if new.get("corrects_doi") and new["corrects_doi"] in self.by_doi:
            tgt = self.by_doi[new["corrects_doi"]]; link(new, tgt, "correction")
            tgt["correction_status"] = "retracted" if "retract" in (new["title_original"] + " " + (new["publication_type_in_source"] or "")).lower() else "corrected"
        self.add(new); counts["new"] += 1
        return new


def run(res, fetcher=None, now=None, only=None, dry_run=False, env=None, write=True):
    env = os.environ if env is None else env
    now = now or dt.datetime.now(UTC).replace(microsecond=0)
    now_iso, run_id = iso(now), "run-" + now.strftime("%Y%m%dT%H%M%SZ")
    sig = os.path.join(res, "signals")
    reg = load_registry(res)
    rules = Rules(res)
    store_path = os.path.join(sig, "signals.json")
    records = json.load(open(store_path, encoding="utf-8"))["records"] if os.path.exists(store_path) else []
    status_path = os.path.join(sig, "status.json")
    status = json.load(open(status_path, encoding="utf-8")) if os.path.exists(status_path) else {"last_successful_refresh": None, "sources": {}}
    cache_path = os.path.join(sig, "http-cache.json")
    cache = json.load(open(cache_path, encoding="utf-8")) if os.path.exists(cache_path) else {}
    fetcher = fetcher or live_fetcher(reg, cache)
    store = Store(records)
    d = reg["defaults"]
    report = {"run_id": run_id, "started_at": now_iso, "sources": [], "excluded_sample": [], "merge_log": []}
    totals = {k: 0 for k in ("fetched", "included", "excluded", "new", "updated", "duplicates", "url_changed", "skipped_old", "held_for_review")}
    ok_sources = 0
    for src in reg["sources"]:
        if not src.get("enabled") or (only and src["id"] not in only): continue
        st = status["sources"].setdefault(src["id"], {})
        row = {"source": src["id"], "endpoint": src["endpoint"], "result": "", "http_status": None, "items": 0, "included": 0, "excluded": 0}
        st["last_attempt_at"] = now_iso
        if src.get("secret") and not env.get(src["secret"]):
            row["result"] = f"skipped: secret {src['secret']} not set"; st["last_result"] = row["result"]; report["sources"].append(row); continue
        last_ok = to_dt(st.get("last_success_at")) if st.get("last_success_at") else None
        since = max(now - dt.timedelta(days=d["window_days"]), (last_ok - dt.timedelta(days=7)) if last_ok else now - dt.timedelta(days=d["window_days"]))
        if not last_ok and src["access"].startswith("api_"): since = now - dt.timedelta(days=45)   # first run: recent research only, history fills forward
        url = request_url(src, d, since, now, env)
        row["request"] = redact(url)
        try:
            code, body, _hdr = fetcher(src, url)
            row["http_status"] = code
            if code == 304:
                row["result"] = "unchanged (HTTP 304)"; ok_sources += 1; st["last_success_at"] = now_iso; st["last_result"] = row["result"]
                report["sources"].append(row); continue
            items = PARSERS[src["access"]](body)
            pages = 1
            while src["access"] == "api_europepmc" and pages < src.get("max_pages", 1):   # cursor paging, bounded
                nxt = json.loads(body).get("nextCursorMark")
                if not nxt or len(items) < src.get("page_size", 100) * pages: break
                code, body, _hdr = fetcher(src, url + "&" + urllib.parse.urlencode({"cursorMark": nxt}))
                items += PARSERS[src["access"]](body); pages += 1
        except FetchError as e:
            row["result"] = f"failed: {e.kind}: {e}"; row["http_status"] = e.status
            st["last_result"] = row["result"]; st["last_error_at"] = now_iso; report["sources"].append(row); continue
        except ValueError as e:
            row["result"] = f"failed: malformed response: {e}"; st["last_result"] = row["result"]; st["last_error_at"] = now_iso
            report["sources"].append(row); continue
        row["items"] = len(items); totals["fetched"] += len(items)
        for it in items:
            ok, reason, cls = rules.classify(it, src)
            if ok and not canonical_url(it.get("url")): ok, reason = False, "excluded: link is not a valid HTTPS address"
            if ok and len(clean_text(it.get("title"))) < 3: ok, reason = False, "excluded: no usable title"
            if ok and cls["content_flags"]: ok, reason = False, "held for review: " + ", ".join(cls["content_flags"]); totals["held_for_review"] += 1
            if not ok:
                row["excluded"] += 1; totals["excluded"] += 1
                if len(report["excluded_sample"]) < 300:
                    report["excluded_sample"].append({"source": src["id"], "title": clean_text(it.get("title"), 160), "reason": reason})
                continue
            cls["_reason"] = reason
            rec = make_record(it, src, cls, now_iso, run_id)
            rec["date_flag"] = date_flag(rec["published_at"], now)
            pd = to_dt(rec["published_at"])
            idx = to_dt(rec["indexed_at"])
            recently_indexed = idx and idx >= now - dt.timedelta(days=60)
            if pd and pd < now - dt.timedelta(days=d["archive_days"]) and rec["signal_id"] not in store.by_id and not recently_indexed:
                totals["skipped_old"] += 1; continue
            row["included"] += 1; totals["included"] += 1
            store.merge(rec, now_iso, totals, report["merge_log"])
        row["result"] = "ok"; ok_sources += 1
        st["last_success_at"] = now_iso; st["last_result"] = "ok"; st["last_items"] = row["items"]; st["last_included"] = row["included"]
        report["sources"].append(row)
    out = sorted(store.by_id.values(), key=lambda r: r["signal_id"])
    for r in out:
        r.pop("_versions", None)
        r["related_signal_ids"].sort(key=lambda x: x["signal_id"])
    out = [{k: r.get(k) for k in FIELDS_ORDER if k in r or k in ("journal",)} for r in out]
    doc = {"schema_version": "1.0", "records": out}
    errors = validate.validate_store(doc, res)
    attempted = [r for r in report["sources"] if not r["result"].startswith("skipped")]
    report.update({"finished_at": iso(dt.datetime.now(UTC).replace(microsecond=0)) if not env.get("SIGNALS_FIXED_CLOCK") else now_iso,
                   "totals": totals, "records_in_store": len(out), "sources_ok": ok_sources, "sources_attempted": len(attempted),
                   "schema_errors": errors[:50], "outcome": "schema violation" if errors else ("all sources failed" if attempted and ok_sources == 0 else ("partial" if ok_sources < len(attempted) else "ok")),
                   "review_queue": sum(1 for r in out if r["review_status"] == "discovered_unreviewed")})
    report["merge_log"] = report["merge_log"][:200]
    if not errors and ok_sources > 0:
        status["last_successful_refresh"] = now_iso; status["last_run_id"] = run_id
    status["last_run_at"] = now_iso; status["last_run_outcome"] = report["outcome"]
    if write and not dry_run and not errors:
        json.dump(doc, open(store_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        json.dump(status, open(status_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
        json.dump(cache, open(cache_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
        write_queue(sig, out)
    if write and not dry_run:
        json.dump(report, open(os.path.join(sig, "run-report.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        new_file = not os.path.exists(os.path.join(sig, "runs.csv"))
        with open(os.path.join(sig, "runs.csv"), "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if new_file: w.writerow(["run_id", "outcome", "sources_ok", "sources_attempted", "fetched", "included", "excluded", "new", "updated", "duplicates", "records_in_store"])
            w.writerow([run_id, report["outcome"], ok_sources, len(attempted), totals["fetched"], totals["included"], totals["excluded"], totals["new"], totals["updated"], totals["duplicates"], len(out)])
    return report, doc, status


def write_queue(sig, records):
    dec_path = os.path.join(sig, "review-decisions.csv")
    decided = {r["signal_id"] for r in csv.DictReader(open(dec_path, encoding="utf-8"))} if os.path.exists(dec_path) else set()
    pend = sorted((r for r in records if r["signal_id"] not in decided), key=lambda r: (r["published_at"] or "0000"), reverse=True)
    with open(os.path.join(sig, "review-queue.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["signal_id", "published_at", "source_type", "publisher", "title_original", "countries", "subjects", "suggested_interventions", "canonical_url"])
        for r in pend:
            w.writerow([r["signal_id"], (r["published_at"] or "")[:10], r["source_type"], r["publisher"], r["title_original"], ";".join(r["countries"]),
                        ";".join(r["subjects"]), ";".join(r["related_intervention_ids"]), r["canonical_url"]])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only"); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--research", default=os.path.join(ROOT, "research"))
    a = ap.parse_args()
    rep, doc, status = run(a.research, only=set(a.only.split(",")) if a.only else None, dry_run=a.dry_run)
    for s in rep["sources"]: print(f"{s['source']:24} {s['result'][:70]:70} items={s['items']} included={s['included']}")
    print(f"outcome={rep['outcome']} totals={rep['totals']} store={rep['records_in_store']} last_successful_refresh={status.get('last_successful_refresh')}")
    return 1 if rep["schema_errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
