"""Editorial voice check for Clean Air's generated, reader-facing copy.

Run:  python3 tools/check_voice.py [dist_dir]            (default site/dist)
      python3 tools/check_voice.py --self-test            (proves the rules fire on bad fixtures)

What it reads: the <main> text of every generated HTML page, every generated Markdown mirror, and the
string values of public JSON files that are shown to readers (for-ai.json, packs). It skips text that is
not the site's own voice: <cite> (source titles), <blockquote>/<q> (quotations), <code>/<pre>,
anything inside [data-voice="verbatim"], URLs, and claim/source IDs.

Rules (docs/editorial-voice.md explains each, with before/after examples):
  em-dash       no em dash (U+2014) in site-authored prose
  prescriptive  no "should"/"must" in the site's own voice (report legal duties as "the rule requires")
  ranking       no league-table language about places, people, organisations or technologies
  blame         no accusatory labels in the editorial voice ("failed", "misleading", "bad actor" ...)
  hype          no promotional superlatives ("game-changing", "groundbreaking", "holistic" ...)
  unlabelled-rating  every evidence badge carries its text label, never colour alone
  abbreviation  (warning) PM2.5, AQI and similar are expanded or glossary-linked on first use

Exceptions live in tools/voice-exceptions.csv: one row per narrowly scoped exception
(page glob, rule, exact phrase that must appear in the flagged sentence, reason). An exception that
no longer matches anything is itself reported, so stale exceptions do not accumulate.
Exit code 1 if any error remains.
"""
import csv, fnmatch, glob, json, os, re, sys
from bs4 import BeautifulSoup, Comment

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EXC_FILE = os.path.join(HERE, "voice-exceptions.csv")

RULES = [
    ("em-dash", re.compile("—"), "error"),
    ("prescriptive", re.compile(r"\b(should|must)(n't)?\b", re.I), "error"),
    ("ranking", re.compile(r"\b(league tables?|top[- ](?:\d+|ten|five|three)\b|(?:the )?(?:best|worst|leading)\s+(?:ngos?|organisations?|cities|city|countries|country|companies|company|funders?|technolog(?:y|ies)|governments?|states?|performers?)|ranked (?:first|last|best|worst)|ranking of)", re.I), "error"),
    ("blame", re.compile(r"\b(failed|failure to act|misleading|non-compliant|bad actors?|culprits?|shameful|scandalous|villains?)\b", re.I), "error"),
    ("hype", re.compile(r"\b(game[- ]chang\w*|groundbreaking|ground-breaking|holistic|revolutionary|cutting[- ]edge|world[- ]class|unprecedented|transformative|silver bullet)\b", re.I), "error"),
]
ABBR = {"PM2.5": "fine particles", "PM10": "particles", "AQI": "air quality index", "NCAP": "National Clean Air Programme",
        "CPCB": "Central Pollution Control Board", "CSR": "corporate social responsibility"}
SKIP_TAGS = ["script", "style", "code", "pre", "cite", "blockquote", "q", "svg", "noscript", "template"]
EV_CLASSES = {"strong", "moderate", "limited", "none", "negative"}


def load_exceptions(path=EXC_FILE):
    if not os.path.exists(path): return []
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    for r in rows: r["_used"] = 0
    return rows


def excepted(exc, rel, rule, sentence):
    for e in exc:
        if e["rule"] == rule and fnmatch.fnmatch(rel, e["page"]) and e["phrase"] in sentence:
            e["_used"] += 1; return True
    return False


def sentences_of(text):
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\u201c[^\u201d]*\u201d", " ", text)   # text inside curly quotes is quoted, not the site's voice
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]


def html_text_blocks(markup):
    """Yield (approx_line, text) for reader-facing text in <main> (or whole doc if no main)."""
    soup = BeautifulSoup(markup, "html.parser")
    root = soup.find("main") or soup
    for c in root.find_all(string=lambda t: isinstance(t, Comment)): c.extract()
    for t in root.find_all(SKIP_TAGS): t.decompose()
    for t in root.select('[data-voice="verbatim"]'): t.decompose()
    blocks = []
    for el in root.find_all(["p", "li", "td", "th", "h1", "h2", "h3", "h4", "dd", "dt", "caption", "summary", "figcaption", "label", "button", "option", "span", "a"]):
        if el.find_parent(["p", "li", "td", "th", "h1", "h2", "h3", "h4", "dd", "dt", "caption", "summary", "figcaption", "label", "button"]) and el.name in ("span", "a"):
            continue
        if el.name in ("li", "td", "dd") and el.find(["p", "li", "ul", "ol", "table"]):
            continue  # its children are scanned on their own
        txt = el.get_text(" ", strip=True)
        if txt: blocks.append((getattr(el, "sourceline", 0) or 0, txt))
    # attributes that are read aloud or shown as tooltips
    for el in root.find_all(attrs={"title": True}):
        blocks.append((getattr(el, "sourceline", 0) or 0, el["title"]))
    for el in root.find_all(attrs={"aria-label": True}):
        blocks.append((getattr(el, "sourceline", 0) or 0, el["aria-label"]))
    return soup, root, blocks


def md_text_blocks(text):
    out, in_code = [], False
    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith("```"): in_code = not in_code; continue
        if in_code or line.startswith(">") or line.startswith("<!--"): continue
        line = re.sub(r"`[^`]*`", " ", line)
        line = re.sub(r"(?<![\\\w])_[^_]+_(?!\w)", " ", line)    # _Source title_ = <cite> in mirrors
        line = re.sub(r"\]\([^)]*\)", "]", line)                 # drop link targets
        line = re.sub(r"<cite>.*?</cite>", " ", line)
        if line.startswith("---") or re.match(r"^\w[\w_-]*: ", line) and i < 15: continue  # front matter
        out.append((i, line))
    return out


def json_text_blocks(obj, path="$"):
    skip_keys = {"url", "source_url", "title", "id", "href", "markdown", "html", "supporting_excerpt", "old_text", "locator"}
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in skip_keys: continue
            yield from json_text_blocks(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj): yield from json_text_blocks(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        yield (path, obj)


def scan_blocks(rel, blocks, exc, findings):
    for line, txt in blocks:
        for s in sentences_of(txt):
            for rule, rx, level in RULES:
                m = rx.search(s)
                if m and not excepted(exc, rel, rule, s):
                    findings.append((level, rel, line, rule, m.group(0), s[:160]))


def check_badges(rel, root, findings):
    for b in root.select(".badge"):
        cls = set(b.get("class", [])) & EV_CLASSES
        if cls and not b.get_text(strip=True):
            findings.append(("error", rel, getattr(b, "sourceline", 0), "unlabelled-rating", ",".join(cls), "evidence badge without a text label"))


def check_abbr(rel, root, findings):
    text = root.get_text(" ", strip=True)
    for ab, expansion in ABBR.items():
        i = text.find(ab)
        if i < 0: continue
        window = text[max(0, i - 120): i + 160].lower()
        linked = any(a.get_text(strip=True).startswith(ab) for a in root.select("a.term, abbr"))
        if not linked and expansion.lower() not in window:
            findings.append(("warning", rel, 0, "abbreviation", ab, f"first use of {ab} is not expanded nearby or glossary-linked"))


def scan_dist(dist, exc):
    findings = []
    for path in sorted(glob.glob(os.path.join(dist, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(path, dist)
        soup, root, blocks = html_text_blocks(open(path, encoding="utf-8").read())
        scan_blocks(rel, blocks, exc, findings); check_badges(rel, root, findings); check_abbr(rel, root, findings)
    for path in sorted(glob.glob(os.path.join(dist, "**", "*.md"), recursive=True)) + \
            [p for p in [os.path.join(dist, "llms.txt"), os.path.join(dist, "for-ai.txt")] if os.path.exists(p)]:
        rel = os.path.relpath(path, dist)
        if rel.startswith("downloads/") and not rel.startswith("downloads/packs"): continue  # report exports are dated snapshots
        scan_blocks(rel, md_text_blocks(open(path, encoding="utf-8").read()), exc, findings)
    for path in [os.path.join(dist, "for-ai.json")] + sorted(glob.glob(os.path.join(dist, "packs", "**", "*.json"), recursive=True)):
        if not os.path.exists(path): continue
        rel = os.path.relpath(path, dist)
        scan_blocks(rel, list(json_text_blocks(json.load(open(path, encoding="utf-8")))), exc, findings)
    return findings


def report(findings, exc, label):
    errs = [f for f in findings if f[0] == "error"]
    warns = [f for f in findings if f[0] == "warning"]
    for lvl, rel, line, rule, hit, ctx in errs[:400]:
        print(f"ERROR {rel}:{line} [{rule}] '{hit}' :: {ctx}")
    stale = [e for e in exc if e["_used"] == 0]
    for e in stale:
        print(f"ERROR tools/voice-exceptions.csv: stale exception ({e['rule']}, {e['page']}, '{e['phrase']}') matches nothing")
    by = {}
    for w in warns: by.setdefault(w[3], []).append(w)
    for rule, ws in by.items():
        print(f"warning [{rule}] {len(ws)} pages, e.g. {ws[0][1]}: {ws[0][5]}")
    print(f"{label}: {len(errs)} errors, {len(warns)} warnings, {len(stale)} stale exceptions, "
          f"{sum(1 for e in exc if e['_used'])} exceptions used")
    return 1 if errs or stale else 0


def self_test():
    """Bad fixture must produce every error rule; good fixture must produce none."""
    fx = os.path.join(HERE, "fixtures", "voice")
    bad = scan_dist(os.path.join(fx, "bad"), [])
    rules_hit = {f[3] for f in bad if f[0] == "error"}
    need = {"em-dash", "prescriptive", "ranking", "blame", "hype", "unlabelled-rating"}
    good = [f for f in scan_dist(os.path.join(fx, "good"), []) if f[0] == "error"]
    ok = need <= rules_hit and not good
    print(f"voice self-test: bad fixture fired {sorted(rules_hit)}; good fixture errors: {len(good)}")
    for g in good: print("  unexpected:", g)
    if not need <= rules_hit: print("  missing rules:", sorted(need - rules_hit))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv: sys.exit(self_test())
    dist = next((a for a in sys.argv[1:] if not a.startswith("-")), os.path.join(ROOT, "site", "dist"))
    exc = load_exceptions()
    sys.exit(report(scan_dist(dist, exc), exc, "voice"))
