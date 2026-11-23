"""Shared helpers for Latest Signals: safe HTTP, text and URL normalisation, dates.

All external content is untrusted data. Nothing here evaluates, executes or forwards feed text; text is unescaped,
stripped of markup and control characters, length-capped and later HTML-escaped by the site templates.
"""
import datetime as dt
import email.utils
import hashlib
import html
import re
import time
import urllib.error
import urllib.parse
import urllib.request

TRACKING = re.compile(r"^(utm_[a-z]+|fbclid|gclid|dclid|mc_cid|mc_eid|cmpid|ito|_ga|igshid|ref|ref_src|rss|from|at_[a-z]+|s_cid|ncid|ocid|spm)$", re.I)
UTC = dt.timezone.utc


# ---------- HTTP ----------
class FetchError(Exception):
    def __init__(self, kind, message, status=None):
        super().__init__(message); self.kind = kind; self.status = status


class _NoRedirectOutsideAllowlist(urllib.request.HTTPRedirectHandler):
    def __init__(self, allow_hosts): self.allow = allow_hosts
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        u = urllib.parse.urlsplit(newurl)
        if u.scheme != "https" or u.hostname not in self.allow:
            raise FetchError("redirect", f"redirect to {u.scheme}://{u.hostname} refused (not HTTPS or not on the allowlist)", code)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def http_get(url, *, allow_hosts, user_agent, timeout=25, max_bytes=3_000_000, retries=2, cache=None, headers=None, sleep=time.sleep):
    """GET over HTTPS with a host allowlist, size cap, bounded retries with backoff, and ETag/Last-Modified caching.
    Returns (status, body_bytes or None for 304, response_headers). Raises FetchError(kind) on failure."""
    u = urllib.parse.urlsplit(url)
    if u.scheme != "https": raise FetchError("blocked", "only HTTPS endpoints are fetched")
    if u.hostname not in allow_hosts: raise FetchError("blocked", f"host {u.hostname} is not on the allowlist")
    h = {"User-Agent": user_agent, "Accept": "application/json, application/rss+xml, application/atom+xml, application/xml;q=0.9, text/xml;q=0.8"}
    h.update(headers or {})
    c = (cache or {}).get(url, {})
    if c.get("etag"): h["If-None-Match"] = c["etag"]
    if c.get("last_modified"): h["If-Modified-Since"] = c["last_modified"]
    opener = urllib.request.build_opener(_NoRedirectOutsideAllowlist(allow_hosts))
    last = None
    for attempt in range(retries + 1):
        try:
            with opener.open(urllib.request.Request(url, headers=h), timeout=timeout) as r:
                body = r.read(max_bytes + 1)
                if len(body) > max_bytes: raise FetchError("too_large", f"response over {max_bytes} bytes")
                if cache is not None:
                    cache[url] = {k: v for k, v in {"etag": r.headers.get("ETag"), "last_modified": r.headers.get("Last-Modified")}.items() if v}
                return r.status, body, dict(r.headers)
        except urllib.error.HTTPError as e:
            if e.code == 304: return 304, None, dict(e.headers)
            if e.code == 429 or e.code >= 500:
                last = FetchError("rate_limited" if e.code == 429 else "server_error", f"HTTP {e.code}", e.code)
                ra = str((e.headers or {}).get("Retry-After") or "")
                wait = min(30, int(ra)) if ra.isdigit() else 2 ** (attempt + 1)
                if attempt < retries: sleep(wait); continue
                raise last
            raise FetchError("http_error", f"HTTP {e.code}", e.code)
        except FetchError:
            raise
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last = FetchError("timeout" if "timed out" in str(e).lower() else "network", str(e)[:200])
            if attempt < retries: sleep(2 ** (attempt + 1)); continue
            raise last
    raise last


# ---------- text ----------
CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f​-‏‪-‮⁦-⁩]")


def clean_text(s, cap=400):
    """Unescape entities (twice, for double-escaped feeds), drop tags and control characters, collapse spaces, cap length."""
    if not s: return ""
    s = html.unescape(html.unescape(str(s)))
    s = re.sub(r"<(script|style)[^>]*>.*?</\1\s*>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]{0,500}>", "", s)
    s = s.replace("<", "‹").replace(">", "›")          # anything left that looks like markup becomes inert
    s = CTRL.sub("", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= cap else s[: cap - 1].rstrip() + "…"


def norm_title(t):
    return " ".join(re.findall(r"[a-z0-9]+", (t or "").lower()))


def title_similarity(a, b):
    ta, tb = set(norm_title(a).split()), set(norm_title(b).split())
    if len(ta) < 5 or len(tb) < 5: return 1.0 if norm_title(a) == norm_title(b) else 0.0
    return len(ta & tb) / len(ta | tb)


# ---------- URLs and identifiers ----------
def canonical_url(u):
    """Return a cleaned HTTPS URL or None. Rejects javascript:, data:, file:, http: and malformed URLs; drops tracking parameters and fragments."""
    if not u: return None
    u = clean_text(u, 1000).strip()
    try: p = urllib.parse.urlsplit(u)
    except ValueError: return None
    if p.scheme.lower() != "https" or not p.hostname or re.search(r"[\s<>\"'`]", u): return None
    q = [(k, v) for k, v in urllib.parse.parse_qsl(p.query, keep_blank_values=True) if not TRACKING.match(k)]
    host = p.hostname.lower() + (f":{p.port}" if p.port and p.port != 443 else "")
    path = p.path or "/"
    return urllib.parse.urlunsplit(("https", host, path, urllib.parse.urlencode(q), ""))


DOI_RE = re.compile(r"(10\.\d{4,9}/[^\s\"<>]+)", re.I)


def norm_doi(d):
    if not d: return None
    m = DOI_RE.search(urllib.parse.unquote(str(d)))
    return m.group(1).rstrip(".,;)").lower() if m else None


def signal_id(identity):
    return "sig-" + hashlib.sha1(identity.encode("utf-8")).hexdigest()[:12]


# ---------- dates ----------
def iso(d):
    return d.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ") if isinstance(d, dt.datetime) else None


def parse_date(s):
    """Parse RSS (RFC 822, incl. two-digit years and 'Z'), ISO 8601, or partial dates. Returns (iso_string_or_None, precision)."""
    if not s: return None, "unknown"
    s = str(s).strip()
    m = re.fullmatch(r"(\d{4})(?:-(\d{1,2})(?:-(\d{1,2}))?)?", s)
    if m:
        y, mo, d = int(m.group(1)), m.group(2), m.group(3)
        if d: return f"{y:04d}-{int(mo):02d}-{int(d):02d}", "day"
        if mo: return f"{y:04d}-{int(mo):02d}-01", "month"
        return f"{y:04d}-01-01", "year"
    try:
        d = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
        return iso(d if d.tzinfo else d.replace(tzinfo=UTC)), "day"
    except ValueError:
        pass
    try:
        d = email.utils.parsedate_to_datetime(re.sub(r"\s+Z$", " +0000", s))
        return iso(d if d.tzinfo else d.replace(tzinfo=UTC)), "day"
    except (TypeError, ValueError, IndexError):
        return None, "unknown"


def date_from_url(u):
    m = re.search(r"/(20\d\d)/(\d{1,2})/(\d{1,2})/", u or "")
    if m and 1 <= int(m.group(2)) <= 12 and 1 <= int(m.group(3)) <= 31:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}", "day"
    return None, "unknown"


def to_dt(s):
    if not s: return None
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")) if "T" in s else dt.datetime.fromisoformat(s + "T00:00:00+00:00")
