# Latest Signals pages, feeds and exports. Executed by site/build.py after build_map.py and before build_agent.py,
# so the Markdown mirrors, llms files and sitemaps include these pages. Records come from site/signals_data.py.
# Outputs: /signals/ (index, monthly archive, recently indexed, awaiting assessment, what is missing, sources, how it works),
# /signals/feed.xml and /signals/feeds/<view>.xml (Atom, external records only), downloads/data/signals.json|csv,
# downloads/schemas/signals.schema.json, downloads/data/signals-sources.yml|signals-taxonomy.yml.
import xml.sax.saxutils as _sx
sig_c = home_c + [("Latest signals", "signals/index.html")]
INDEX_LIMIT = SIG_PAGE_SIZE
_months = OrderedDict()
for r in SIG_TIMELINE: _months.setdefault(r["_month"], []).append(r)
month_rows = [(m, sig_date(m + "-01", "month"), len(v)) for m, v in _months.items()]
_notes = []
_ndir = os.path.join(SIG_DIR, "notes")
for fn in sorted(os.listdir(_ndir), reverse=True) if os.path.isdir(_ndir) else []:
    if fn.endswith(".md"):
        nfm, nbody = front(os.path.join(_ndir, fn))
        if nfm.get("status") == "reviewed": _notes.append({"title": nfm["title"], "reviewed": nfm["reviewed"], "html": md(nbody, "../", 1)})
_lead = [r for r in SIG_TIMELINE][:5]
_n_more = max(0, len(SIG_TIMELINE) - INDEX_LIMIT)
render("signals/index.html", "signals.html", "Latest signals",
       "New research, reports, policy and practical work on cleaner air in Asia. Updated on a schedule. Each record links to its original source.",
       "signals", home_c, kind="index", deck="A list of new research, reports, policy and practical work on cleaner air in South and Southeast Asia, found by a scheduled feed. Each record links to its source, and none has been assessed by Clean Air unless it says so.", featured=SIG_FEATURED, lead=_lead, notes=_notes[:1],
       items=SIG_TIMELINE[:INDEX_LIMIT], filters=True, list_heading="All records, newest first",
       more_note=(f"Showing the newest {INDEX_LIMIT}; older records are in the monthly archive" if _n_more else ""), months=month_rows)
def _apath(m, k): return f"signals/archive/{m}.html" if k == 0 else f"signals/archive/{m}-p{k + 1}.html"
for m, rows in _months.items():
    label = sig_date(m + "-01", "month")
    parts = [rows[i:i + SIG_PAGE_SIZE] for i in range(0, len(rows), SIG_PAGE_SIZE)]
    for k, chunk in enumerate(parts):
        part = f", part {k + 1} of {len(parts)}" if len(parts) > 1 else ""
        render(_apath(m, k), "signals.html", f"Signals published in {label}{part}", f"Records published in {label}{part}, newest first. Source records, not reviewed evidence.",
               "signals", sig_c, kind="archive", deck=f"Records with a publication date in {label}{part}.", items=chunk, filters=True,
               list_heading=f"{label}, newest first{part}", months=month_rows,
               more_note=(f"{len(rows)} records this month, split into {len(parts)} parts" if len(parts) > 1 else ""),
               pager=[(f"Part {j + 1}", _apath(m, j), j == k) for j in range(len(parts))] if len(parts) > 1 else [])
_indexed = sorted([r for r in SIG_PUBLIC if r["_timeline"]], key=lambda r: (r["discovered_at"], r["signal_id"]), reverse=True)[:SIG_PAGE_SIZE]
render("signals/recently-indexed.html", "signals.html", "Recently indexed", "Records in the order this feed found them, including older papers newly added to an index, undated records and date anomalies.",
       "signals", sig_c, kind="indexed", deck="Ordered by when this feed first saw each record, not by publication date. An older paper can appear here because an index added it recently.",
       items=_indexed, filters=False, list_heading=f"The {SIG_PAGE_SIZE} newest discoveries",
       extra=[("Date unknown", [r for r in SIG_PUBLIC if not r["published_at"]]),
              ("Date anomalies (source date in the future)", [r for r in SIG_PUBLIC if r.get("date_flag") == "future-dated"])])
render("signals/awaiting-assessment.html", "signals.html", "New sources awaiting assessment",
       "Research papers, preprints and reports found by the feed that no Clean Air reviewer has assessed. Candidates for the evidence register, not part of it.",
       "signals", sig_c, kind="awaiting", deck="Discovery only. A paper listed here has not been read by Clean Air, is not a claim, and does not change any evidence rating. "
       "The route from here to the evidence register is set out in how this feed works.", items=SIG_AWAITING[:SIG_PAGE_SIZE], filters=True, list_heading="Newest first",
       more_note=(f"Showing the newest {SIG_PAGE_SIZE} of {len(SIG_AWAITING)}; older ones are in the monthly archive" if len(SIG_AWAITING) > SIG_PAGE_SIZE else ""))
_mfm, _mbody = site_md("signals-missing.md")
_theme_n = Counter(t for r in SIG_PUBLIC for t in r["subjects"])
_gap_rows = "\n".join(f"| {SIG_THEME_LABEL[k]} | {_theme_n.get(k, 0)} |" for k in ["livelihoods-workers", "justice", "children-schools", "waste", "cross-border-smoke", "indoor-protection", "clean-cooking", "kilns-industry"])
render("signals/missing.html", "simple.html", _mfm["title"], _mfm["summary"], "signals", sig_c,
       body_html=md(_mbody + "\n\n| Topic | Records currently held |\n|---|---|\n" + _gap_rows + "\n\nCounts change with every refresh and describe feed coverage only.", "../", 0))
_hfm, _hbody = site_md("signals-method.md")
render("signals/how-it-works.html", "simple.html", _hfm["title"], _hfm["summary"], "signals", sig_c, body_html=md(_hbody, "../", 0))
_bfm, _bbody = site_md("signals-blind.md")
_held = Counter(r["source_registry_id"] for r in SIG_PUBLIC)
for r in SIG_PUBLIC:
    for s_ in r.get("also_listed_by") or []: _held[s_] += 1
_enabled = [s for s in SIG_REG["sources"] if s.get("enabled")]
_cov = []
for c, lab in sorted(SIG_COUNTRY_LABEL.items(), key=lambda x: x[1]):
    direct = ", ".join(s["name"] for s in _enabled if c in (s.get("covers") or []))
    _cov.append((c, lab, sum(1 for r in SIG_PUBLIC if c in r["countries"]), direct))
_cov.append(("regional", "Regional or cross-border", sum(1 for r in SIG_PUBLIC if r["cross_border_region"]), ""))
render("signals/sources.html", "signals_sources.html", "Sources and coverage", "Which feeds and indexes are read, when each was last checked, what was tested and not enabled, and where coverage is thin.",
       "signals", sig_c, enabled=_enabled, disabled=[s for s in SIG_REG["sources"] if not s.get("enabled")], SIG_STATUS=SIG_STATUS, held=_held,
       coverage=_cov, blind=md(_bbody, "../", 0),
       access_label={"rss": "RSS feed", "atom": "Atom feed", "api_europepmc": "Europe PMC API", "api_crossref": "Crossref API", "api_openalex": "OpenAlex API", "manual": "Manual"})

# ---------- exports (one canonical store -> JSON, CSV, Atom) ----------
PUB_FIELDS = ["signal_id", "title_original", "publisher", "journal", "canonical_url", "doi_or_persistent_id", "source_type", "provenance_kind", "is_preprint",
              "published_at", "published_date_precision", "date_basis", "date_flag", "source_updated_at", "indexed_at", "discovered_at", "last_checked_at",
              "countries", "cross_border_region", "subjects", "organisation_ids", "related_intervention_ids", "related_signal_ids", "review_status",
              "correction_status", "external_rights", "source_registry_id", "also_listed_by", "language", "why_it_may_matter", "related_claim_ids"]
def _pub(r):
    d = {k: r.get(k) for k in PUB_FIELDS}
    d["review_label"] = SIG_REVIEW_LABEL[r["review_status"]]
    d["page_url"] = f"{BASE_URL}{r['_page']}#{r['signal_id']}"
    return d
sig_export = {"title": "Clean Air: latest signals", "format_version": "1.0", "schema": BASE_URL + "downloads/schemas/signals.schema.json",
              "statement": "Signals are indexed third-party publications and announcements, not automatically verified Clean Air findings. They carry no evidence rating and do not change the research edition dated " + CUTOFF + ".",
              "research_cutoff": CUTOFF_ISO, "last_successful_refresh": SIG_LAST, "build_date": BUILT,
              "rights": "Titles, dates, publishers and links only. Each record belongs to its publisher; Clean Air's terms do not apply to third-party material.",
              "records": [_pub(r) for r in SIG_TIMELINE + [r for r in SIG_PUBLIC if not r["_timeline"]]]}
open(os.path.join(DIST, "downloads", "data", "signals.json"), "w", encoding="utf-8").write(json.dumps(sig_export, ensure_ascii=False, indent=1))
os.makedirs(os.path.join(DIST, "downloads", "schemas"), exist_ok=True)
shutil.copy(os.path.join(SIG_DIR, "schema.json"), os.path.join(DIST, "downloads", "schemas", "signals.schema.json"))
for _f, _o in (("sources.yml", "signals-sources.yml"), ("taxonomy.yml", "signals-taxonomy.yml")):
    shutil.copy(os.path.join(SIG_DIR, _f), os.path.join(DIST, "downloads", "data", _o))
import io as _io
_buf = _io.StringIO(); _w = csv.writer(_buf)
_cols = ["signal_id", "published_at", "published_date_precision", "source_type", "publisher", "title_original", "canonical_url", "doi_or_persistent_id", "countries", "subjects", "review_status", "correction_status", "discovered_at"]
_w.writerow(_cols)
for r in sig_export["records"]: _w.writerow([";".join(r[c]) if isinstance(r[c], list) else ("" if r[c] is None else r[c]) for c in _cols])
open(os.path.join(DIST, "downloads", "data", "signals.csv"), "w", encoding="utf-8").write(safe_csv_text(_buf.getvalue()))   # formula-injection guard
def _atom(path, title, rows):
    upd = (SIG_LAST or BUILT + "T00:00:00Z")
    out = ['<?xml version="1.0" encoding="utf-8"?>', '<feed xmlns="http://www.w3.org/2005/Atom">', f"  <title>{_sx.escape(title)}</title>",
           f"  <subtitle>Third-party records found by Clean Air's scheduled feed. Source records, not reviewed evidence. The research edition is dated {CUTOFF}.</subtitle>",
           f'  <link href="{BASE_URL}signals/index.html" rel="alternate"/>', f'  <link href="{BASE_URL}{path}" rel="self"/>', f"  <id>{BASE_URL}{path}</id>",
           f"  <updated>{upd}</updated>", "  <author><name>Clean Air (independent evidence site)</name></author>"]
    for r in rows[:100]:
        d = r["published_at"] if len(r["published_at"]) > 10 else r["published_at"] + "T00:00:00Z"
        cats = "".join(f'<category term="{_sx.escape(t)}" label="{_sx.escape(SIG_THEME_LABEL[t])}"/>' for t in r["subjects"])
        out += ["  <entry>", f"    <title>{_sx.escape(r['title_original'])}</title>", f'    <link href="{_sx.escape(r["canonical_url"])}" rel="alternate"/>',
                f'    <link href="{BASE_URL}{r["_page"]}#{r["signal_id"]}" rel="related"/>', f"    <id>{BASE_URL}signals/{r['signal_id']}</id>",
                f"    <published>{d}</published>", f"    <updated>{d}</updated>", f"    <source><title>{_sx.escape(r['publisher'])}</title></source>",
                f"    <summary>{_sx.escape(SIG_TYPE_LABEL[r['source_type']] + ' from ' + r['publisher'] + '. ' + SIG_REVIEW_LABEL[r['review_status']] + '.')}</summary>",
                f"    {cats}" if cats else "", "  </entry>"]
    out += ["</feed>", ""]
    full = os.path.join(DIST, path); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write("\n".join(x for x in out if x))
_atom("signals/feed.xml", "Clean Air: latest signals", SIG_TIMELINE)
for _k, _v in SIG_VIEW_LABEL.items():
    _atom(f"signals/feeds/{_k}.xml", f"Clean Air: latest signals, {_v.lower()}", [r for r in SIG_TIMELINE if r["_view"] == _k])
