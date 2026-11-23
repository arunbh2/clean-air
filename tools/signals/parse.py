"""Parsers: RSS 2.0 / Atom, Europe PMC, Crossref and OpenAlex responses -> raw items.

A raw item is a dict: title, url, doi, published (raw string), updated (raw), summary (used for classification only,
never stored), publication_type, journal, is_preprint, indexed (raw), correction (dict) and pid.
Malformed input raises ValueError; entity declarations (XML bombs, external entities) are refused before parsing.
"""
import json
import re
import xml.etree.ElementTree as ET

from common import clean_text, norm_doi


def _strip_ns(tag): return tag.rsplit("}", 1)[-1].lower() if isinstance(tag, str) else ""


def _child(el, *names):
    for c in el:
        if _strip_ns(c.tag) in names: return c
    return None


def _alltext(el):
    """Text of an element and its children, skipping script/style children (their tails are kept)."""
    out = [el.text or ""]
    for ch in el:
        if _strip_ns(ch.tag) not in ("script", "style"): out.append(_alltext(ch))
        out.append(ch.tail or "")
    return "".join(out)


def _text(el, *names):
    c = _child(el, *names)
    return _alltext(c).strip() if c is not None else ""


def parse_feed(body):
    if body is None: return []
    raw = body.decode("utf-8", "replace") if isinstance(body, bytes) else body
    raw = raw.lstrip("﻿ \r\n\t")
    if re.search(r"<!ENTITY|<!DOCTYPE[^>]*\[", raw[:5000], re.I): raise ValueError("feed declares entities; refused")
    if not raw.startswith("<"): raise ValueError("not an XML feed (got HTML or text)")
    try: root = ET.fromstring(raw.encode("utf-8"))
    except ET.ParseError:
        fixed = re.sub(r"&(?!#\d+;|#x[0-9a-fA-F]+;|[A-Za-z][A-Za-z0-9]{1,31};)", "&amp;", raw)   # common publisher fault: bare ampersands
        try: root = ET.fromstring(fixed.encode("utf-8"))
        except ET.ParseError as e: raise ValueError(f"malformed XML: {e}")
    tag = _strip_ns(root.tag)
    if tag == "html": raise ValueError("an HTML page was returned instead of a feed")
    items = []
    if tag == "rss" or tag == "rdf":
        chan = _child(root, "channel")
        entries = [e for e in (chan if chan is not None else []) if _strip_ns(e.tag) == "item"] + [e for e in root if _strip_ns(e.tag) == "item"]
        for e in entries:
            items.append({"title": _text(e, "title"), "url": _text(e, "link") or (_text(e, "guid") if _text(e, "guid").startswith("http") else ""),
                          "published": _text(e, "pubdate") or _text(e, "date"), "updated": _text(e, "updated", "modified"),
                          "summary": _text(e, "description")})
    elif tag == "feed":
        for e in root:
            if _strip_ns(e.tag) != "entry": continue
            link = ""
            for l in e:
                if _strip_ns(l.tag) == "link" and l.get("rel", "alternate") == "alternate": link = l.get("href", ""); break
            items.append({"title": _text(e, "title"), "url": link, "published": _text(e, "published", "issued") or _text(e, "updated"),
                          "updated": _text(e, "updated"), "summary": _text(e, "summary", "content")})
    else:
        raise ValueError(f"unknown feed root <{tag}>")
    return items


def _load_json(body):
    try: return json.loads(body.decode("utf-8", "replace") if isinstance(body, bytes) else body)
    except (ValueError, AttributeError) as e: raise ValueError(f"malformed JSON: {e}")


def parse_europepmc(body):
    d = _load_json(body)
    if "resultList" not in d: raise ValueError("Europe PMC response without resultList")
    out = []
    for r in d["resultList"].get("result", []):
        src = r.get("source", ""); types = (r.get("pubTypeList") or {}).get("pubType") or []
        pre = src == "PPR" or any("preprint" in t.lower() for t in types)
        doi = norm_doi(r.get("doi"))
        pid = f"ppr:{r['id']}" if src == "PPR" and str(r.get("id", "")).startswith("PPR") else (f"pmid:{r['pmid']}" if r.get("pmid") else None)
        url = f"https://doi.org/{doi}" if doi else (f"https://europepmc.org/article/{src}/{r.get('id')}" if src and r.get("id") else "")
        jt = ((r.get("journalInfo") or {}).get("journal") or {}).get("title") or r.get("bookOrReportDetails", {}).get("publisher", "")
        corr = {}
        cc = " ".join(c.get("type", "") for c in ((r.get("commentCorrectionList") or {}).get("commentCorrection") or []))
        if "Retraction in" in cc or "retracted publication" in " ".join(types).lower(): corr = {"status": "retracted"}
        elif "Erratum in" in cc or "Correction in" in cc: corr = {"status": "corrected"}
        out.append({"title": r.get("title", ""), "url": url, "doi": doi, "pid": pid, "published": r.get("firstPublicationDate") or r.get("pubYear"),
                    "indexed": r.get("firstIndexDate"), "summary": r.get("abstractText", ""), "publication_type": "; ".join(types)[:200],
                    "journal": jt, "is_preprint": pre, "correction": corr, "publisher": (jt or None)})
    return out


def _cr_date(it):
    for k in ("published-online", "published-print", "published", "issued", "created"):
        dp = ((it.get(k) or {}).get("date-parts") or [[None]])[0]
        if dp and dp[0]:
            return "-".join(f"{int(x):02d}" if i else str(int(x)) for i, x in enumerate(dp[:3]))
    return None


def parse_crossref(body):
    d = _load_json(body)
    if d.get("status") != "ok" or "message" not in d: raise ValueError("Crossref response not ok")
    out = []
    for it in d["message"].get("items", []):
        doi = norm_doi(it.get("DOI"))
        if not doi: continue
        rel = it.get("relation") or {}
        corr = {}
        for u in it.get("update-to") or []:   # this record is a correction or retraction notice of another DOI
            corr = {"status": "updates another record", "of": norm_doi(u.get("DOI")), "kind": u.get("type", "")}
        pre = it.get("type") == "posted-content" or it.get("subtype") == "preprint"
        versions = [norm_doi(x.get("id")) for k in ("is-preprint-of", "has-preprint") for x in rel.get(k, []) if x.get("id-type") == "doi"]
        out.append({"title": (it.get("title") or [""])[0], "url": f"https://doi.org/{doi}", "doi": doi, "pid": None, "published": _cr_date(it),
                    "indexed": ((it.get("indexed") or {}).get("date-time") or "")[:19] + "Z" if (it.get("indexed") or {}).get("date-time") else None,
                    "summary": it.get("abstract", ""), "publication_type": it.get("type", ""), "journal": (it.get("container-title") or [""])[0],
                    "is_preprint": pre, "correction": corr, "version_dois": [v for v in versions if v], "publisher": it.get("publisher")})
    return out


def parse_openalex(body):
    d = _load_json(body)
    if "results" not in d: raise ValueError("OpenAlex response without results")
    out = []
    for w in d["results"]:
        doi = norm_doi(w.get("doi"))
        loc = (w.get("primary_location") or {}).get("source") or {}
        pre = w.get("type") == "preprint"
        out.append({"title": w.get("title") or w.get("display_name") or "", "url": f"https://doi.org/{doi}" if doi else (w.get("id") or "").replace("http://", "https://"),
                    "doi": doi, "pid": None, "published": w.get("publication_date"), "indexed": w.get("created_date"), "summary": "",
                    "publication_type": w.get("type", ""), "journal": loc.get("display_name", ""), "is_preprint": pre,
                    "correction": {"status": "retracted"} if w.get("is_retracted") else {}, "publisher": loc.get("host_organization_name")})
    return out


PARSERS = {"rss": parse_feed, "atom": parse_feed, "api_europepmc": parse_europepmc, "api_crossref": parse_crossref, "api_openalex": parse_openalex}
