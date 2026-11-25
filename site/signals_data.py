# Latest Signals: load the record store, apply reviewed decisions, and index records for contextual lists.
# Executed by site/build.py right after the template globals are set, so every page can show discovery pointers.
# Canonical files: research/signals/signals.json (machine store), review-decisions.csv (human decisions), status.json,
# sources.yml, taxonomy.yml. Signals never carry an evidence rating and never change a claim, rating or funding total.
import datetime as _dt
SIG_DIR = os.path.join(RES, "signals")
_sig_ok = os.path.exists(os.path.join(SIG_DIR, "signals.json"))
SIG_RECORDS = json.load(open(os.path.join(SIG_DIR, "signals.json"), encoding="utf-8"))["records"] if _sig_ok else []
SIG_STATUS = json.load(open(os.path.join(SIG_DIR, "status.json"), encoding="utf-8")) if os.path.exists(os.path.join(SIG_DIR, "status.json")) else {"sources": {}}
SIG_REG = yaml.safe_load(open(os.path.join(SIG_DIR, "sources.yml"), encoding="utf-8")) if os.path.exists(os.path.join(SIG_DIR, "sources.yml")) else {"sources": []}
SIG_TAX = yaml.safe_load(open(os.path.join(SIG_DIR, "taxonomy.yml"), encoding="utf-8")) if os.path.exists(os.path.join(SIG_DIR, "taxonomy.yml")) else {"themes": {}, "countries": {}, "views": {}, "view_of_type": {}}
_dec_path = os.path.join(SIG_DIR, "review-decisions.csv")
SIG_DECISIONS = {r["signal_id"]: r for r in csv.DictReader(open(_dec_path, encoding="utf-8"))} if os.path.exists(_dec_path) else {}
SIG_SRC_BY = {s["id"]: s for s in SIG_REG["sources"]}
SIG_TYPE_LABEL = {"news": "News report", "research": "Research paper", "preprint": "Preprint (not peer reviewed)", "report": "Report or briefing",
                  "policy": "Policy or institutional announcement", "funding": "Funding or partnership announcement", "project": "Project record", "other": "Other"}
SIG_PROV_LABEL = {"official": "Official institutional source", "peer_reviewed_metadata": "Scientific publication (index record)", "preprint": "Preprint",
                  "publisher_report": "The organisation's own publication", "NGO_self_report": "The organisation's own announcement",
                  "company_self_report": "Company's own announcement (company-reported)", "independent_reporting": "News reporting"}
SIG_REVIEW_LABEL = {"discovered_unreviewed": "Source record; not assessed by Clean Air", "metadata_checked": "Details checked against the source; content not assessed",
                    "editorial_reviewed": "Reviewed by Clean Air", "evidence_promoted": "Reviewed by Clean Air and linked to the evidence register",
                    "excluded": "Excluded after review", "withdrawn": "Withdrawn"}
SIG_ORGTYPE_LABEL = {"government": "Government", "ngo": "NGO or community group", "foundation": "Philanthropic foundation", "development_bank": "Development bank",
                     "research": "Research institute or university", "company": "Company or social enterprise", "newsroom": "Publisher or newsroom", "multilateral": "Multilateral body"}
SIG_THEME_LABEL = {k: v["label"] for k, v in SIG_TAX["themes"].items()}
SIG_COUNTRY_LABEL = {k: v["label"] for k, v in SIG_TAX["countries"].items()}
SIG_VIEW_LABEL = SIG_TAX.get("views", {})
_MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
_MONTH = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def sig_date(s, prec="day"):
    if not s: return "Date unknown"
    y, m, d = int(s[:4]), int(s[5:7]), int(s[8:10])
    return {"day": f"{d} {_MON[m-1]} {y}", "month": f"{_MONTH[m-1]} {y}", "year": str(y)}.get(prec, "Date unknown")


def sig_stamp(s):
    if not s: return "never"
    return f"{sig_date(s)}, {s[11:16]} UTC"


_KIND = {"server_error": "server unavailable", "rate_limited": "rate limited", "timeout": "timed out", "network": "network error", "blocked": "address not allowed",
         "http_error": "refused", "too_large": "response too large", "redirect": "redirected elsewhere", "malformed response": "response could not be read as a feed"}


def sig_result(t):
    """Plain wording for a source's last result (no blame words): read, unchanged, not read and why."""
    if not t: return "Not yet checked"
    if t == "ok": return "Read successfully"
    if t.startswith("unchanged"): return "Read; no change since the previous check"
    if t.startswith("skipped"): return "Not read: access key not configured"
    m = re.match(r"failed: ([a-z_ ]+?):\s*(.*)", t)
    if m:
        code = re.search(r"HTTP (\d{3})", m.group(2))
        return f"Could not be read ({_KIND.get(m.group(1), m.group(1).replace('_', ' '))}{', HTTP ' + code.group(1) if code else ''})"
    return "Could not be read"


def _apply(r):
    r = dict(r); d = SIG_DECISIONS.get(r["signal_id"], {})
    r["review_status"] = d.get("review_status") or r["review_status"]
    reviewed = r["review_status"] in ("editorial_reviewed", "evidence_promoted")
    r["why_it_may_matter"] = d.get("why_it_may_matter", "") if reviewed else ""
    r["note_source_refs"] = d.get("note_source_refs", "") if reviewed else ""
    r["note_claims"] = ";".join(x for x in r["note_source_refs"].split(";") if re.fullmatch(r"C\d{3}", x))   # "source" = the record itself
    r["featured"] = reviewed and d.get("featured") == "yes"
    r["study"] = {k: d.get("study_" + k, "") for k in ("question", "design", "outcomes", "limits")} if reviewed and d.get("study_question") else None
    r["funding_review"] = {k: d.get(k, "") for k in ("funding_stage", "announced_amount", "currency", "recipient", "instrument")} if d.get("funding_stage") else None
    r["related_claim_ids"] = [c for c in (d.get("related_claim_ids") or "").split(";") if c] if r["review_status"] == "evidence_promoted" else []
    if d.get("related_intervention_ids") and r["review_status"] != "discovered_unreviewed":
        r["related_intervention_ids"] = [x for x in d["related_intervention_ids"].split(";") if x]
    r["reviewed_on"] = d.get("reviewed_on", "")
    r["_view"] = SIG_TAX["view_of_type"].get(r["source_type"], "news")
    src = SIG_SRC_BY.get(r["source_registry_id"], {})
    r["_org_type"] = src.get("org_type", "")
    r["_timeline"] = bool(r["published_at"]) and r.get("date_flag") != "future-dated"
    r["_date"] = sig_date(r["published_at"], r["published_date_precision"])
    r["_month"] = (r["published_at"] or "")[:7]
    r["_page"] = f"signals/archive/{r['_month']}.html" if r["_timeline"] else "signals/recently-indexed.html"
    r["_search"] = " ".join([r["title_original"], r["publisher"], r.get("journal") or "", " ".join(SIG_COUNTRY_LABEL.get(c, c) for c in r["countries"]),
                             " ".join(SIG_THEME_LABEL.get(t, t) for t in r["subjects"])]).lower()
    return r


SIG_ALL = [_apply(r) for r in SIG_RECORDS]
SIG_PUBLIC = [r for r in SIG_ALL if r["review_status"] not in ("excluded", "withdrawn")]
SIG_WITHDRAWN = [r for r in SIG_ALL if r["review_status"] == "withdrawn"]
SIG_TIMELINE = sorted([r for r in SIG_PUBLIC if r["_timeline"]], key=lambda r: (min(r["published_at"], r["discovered_at"]) if len(r["published_at"]) > 10 else r["published_at"], r["signal_id"]), reverse=True)
SIG_PAGE_SIZE = 40   # records per list page, so pages stay inside the HTML byte budget as the feed grows
_mseen = {}
for _r in SIG_TIMELINE:   # monthly archives split into parts of SIG_PAGE_SIZE; each record's anchor page follows its part
    _k = _mseen.get(_r["_month"], 0); _mseen[_r["_month"]] = _k + 1
    _r["_page"] = f"signals/archive/{_r['_month']}.html" if _k < SIG_PAGE_SIZE else f"signals/archive/{_r['_month']}-p{_k // SIG_PAGE_SIZE + 1}.html"
SIG_BY_ID = {r["signal_id"]: r for r in SIG_ALL}
SIG_LAST = SIG_STATUS.get("last_successful_refresh")
SIG_STALE_HOURS = 36
try:
    _built_dt = _dt.datetime.fromisoformat(BUILT + "T23:59:59+00:00")
    SIG_DELAYED = (not SIG_LAST) or (_built_dt - _dt.datetime.fromisoformat(SIG_LAST.replace("Z", "+00:00"))).total_seconds() > SIG_STALE_HOURS * 3600 + 86400
except ValueError:
    SIG_DELAYED = True


def _idx(keyfn):
    out = {}
    for r in SIG_TIMELINE:
        for k in keyfn(r): out.setdefault(k, []).append(r)
    return out


SIG_BY_INT = _idx(lambda r: r["related_intervention_ids"])
SIG_BY_GROUP = _idx(lambda r: sorted({g for t in r["subjects"] for g in SIG_TAX["themes"].get(t, {}).get("related_groups", [])}))
SIG_BY_NODE = _idx(lambda r: sorted({n for t in r["subjects"] for n in SIG_TAX["themes"].get(t, {}).get("related_nodes", [])}))
SIG_BY_ORG_PUB = _idx(lambda r: [o["org_id"] for o in r["organisation_ids"] if o["link_type"] == "publisher"])
SIG_BY_ORG_NAMED = _idx(lambda r: [o["org_id"] for o in r["organisation_ids"] if o["link_type"] == "named in title"])
SIG_FUNDING = [r for r in SIG_TIMELINE if r["_view"] == "funding"]
SIG_AWAITING = [r for r in SIG_TIMELINE if r["source_type"] in ("research", "preprint", "report") and r["review_status"] in ("discovered_unreviewed", "metadata_checked")]
SIG_FEATURED = [r for r in SIG_TIMELINE if r["featured"]][:5]
env.globals.update(SIG_BY_INT=SIG_BY_INT, SIG_BY_GROUP=SIG_BY_GROUP, SIG_BY_NODE=SIG_BY_NODE, SIG_BY_ORG_PUB=SIG_BY_ORG_PUB, SIG_BY_ORG_NAMED=SIG_BY_ORG_NAMED,
                   SIG_FUNDING=SIG_FUNDING, SIG_AWAITING=SIG_AWAITING, SIG_TIMELINE=SIG_TIMELINE, SIG_LAST=SIG_LAST, SIG_DELAYED=SIG_DELAYED,
                   SIG_TYPE_LABEL=SIG_TYPE_LABEL, SIG_PROV_LABEL=SIG_PROV_LABEL, SIG_REVIEW_LABEL=SIG_REVIEW_LABEL, SIG_THEME_LABEL=SIG_THEME_LABEL,
                   SIG_COUNTRY_LABEL=SIG_COUNTRY_LABEL, SIG_ORGTYPE_LABEL=SIG_ORGTYPE_LABEL, SIG_VIEW_LABEL=SIG_VIEW_LABEL, sig_stamp=sig_stamp,
                   SIG_STALE_HOURS=SIG_STALE_HOURS, SIG_PAGE_SIZE=SIG_PAGE_SIZE, SIG_BY_ID=SIG_BY_ID, sig_result=sig_result)
