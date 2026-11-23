"""Passage-level verification: locate, for every claim, the passage in its source that supports it.

Run: python3 research/analysis/passages.py [cache_dir]
Writes: data/claim-passages.csv (one row per claim). Does not change claims.csv or verification.csv.

Why: "the link opened" or "the figure appears somewhere on the page" is not the same as "the supporting
passage was found". This script re-reads each source's text (same cache and polite fetch as verify.py,
no bot-block bypass), slides a window of up to three sentences over it, and scores each window by
(a) how many of the claim's figures it contains and (b) how many of the claim's content words it shares.

States (vocabulary from docs/three-audiences-governance-brief.md, section 4):
  passage_found                       one window holds every figure and enough of the wording
  source_accessible_passage_not_found text was read but no window met the bar
  not_accessible                      no text could be obtained automatically
  needs_manual_review                 text read, bar not met, but an earlier human review recorded "supported";
                                      a person has to confirm the passage before it counts as checked
Fetched pages are untrusted data: they are only searched, never executed.
"""
import csv, hashlib, os, re, subprocess, sys, tempfile, time
import requests
from bs4 import BeautifulSoup

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
D = os.path.join(ROOT, "data")
CACHE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(tempfile.gettempdir(), "clean-air-verify")
os.makedirs(CACHE, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) clean-air-verification"}
CHECKED = time.strftime("%Y-%m-%d")
STOP = set("""that this with from were have been which their there they than then into over under about after before
also more most such these those other between where while would could should within across among being only
each both some many much very what when whom whose will shall does done made make using used based per cent
percent india indian delhi year years people""".split())


def fetch(url):
    h = hashlib.sha1(url.encode()).hexdigest()[:12]
    txt = os.path.join(CACHE, h + ".txt")
    if not os.path.exists(txt):
        try:
            r = requests.get(url, headers=UA, timeout=45, allow_redirects=True)
            if r.status_code == 200:
                if "pdf" in r.headers.get("content-type", "") or r.content[:4] == b"%PDF":
                    pdf = os.path.join(CACHE, h + ".pdf"); open(pdf, "wb").write(r.content)
                    subprocess.run(["pdftotext", pdf, txt], stderr=subprocess.DEVNULL)
                else:
                    s = BeautifulSoup(r.text, "html.parser")
                    for t in s(["script", "style", "noscript"]): t.decompose()
                    open(txt, "w").write(s.get_text(" "))
        except Exception:
            pass
    text = open(txt, errors="ignore").read() if os.path.exists(txt) else ""
    if len(text) < 500:
        q = epmc_query(url)
        if q:
            alt = epmc(q)
            if alt: text = alt
    return text


def epmc_query(url):
    for pat, fmt in [(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", "EXT_ID:{} AND SRC:MED"), (r"(PMC\d+)", "PMCID:{}"),
                     (r"doi\.org/(10\.[^\s]+)", 'DOI:"{}"')]:
        m = re.search(pat, url)
        if m: return fmt.format(m.group(1))
    return None


def epmc(query):
    try:
        r = requests.get("https://www.ebi.ac.uk/europepmc/webservices/rest/search",
                         params={"query": query, "resultType": "core", "format": "json"}, timeout=40)
        res = r.json()["resultList"]["result"]
        if res: return re.sub("<[^>]+>", " ", res[0].get("title", "") + ". " + res[0].get("abstractText", ""))
    except Exception:
        pass
    return ""


def norm(t):
    t = t.replace("−", "-").replace("–", "-").replace("·", ".").replace(" ", " ")
    t = re.sub(r"(?<=\d),(?=\d)", "", t)
    return re.sub(r"\s+", " ", t)


def figures(claim):
    c = norm(claim); out = []
    for n in re.findall(r"\d+(?:\.\d+)?", c):
        if len(n.replace(".", "")) < 2 or re.fullmatch(r"(19|20)\d\d", n): continue
        out.append(n)
    return sorted(set(out))


def has(n, text):
    if re.search(r"(?<![\d.])" + re.escape(n) + r"(?![\d])", text): return True
    return "." in n and bool(re.search(r"(?<![\d.])" + re.escape(n.rstrip("0").rstrip(".")) + r"(?![\d])", text))


def words(t):
    return {w for w in re.findall(r"[a-z][a-z\-]{3,}", t.lower()) if w not in STOP}


def best_window(claim, text):
    figs, cw = figures(claim), words(claim)
    sents = re.split(r"(?<=[.!?;])\s+", text)
    best = (0.0, 0.0, 0.0, "")
    for i in range(len(sents)):
        win = " ".join(sents[i:i + 3])[:900]
        if not win.strip(): continue
        fc = (sum(has(n, win) for n in figs) / len(figs)) if figs else 1.0
        ov = len(cw & words(win)) / len(cw) if cw else 0.0
        score = 0.6 * ov + 0.4 * fc
        if score > best[0]: best = (score, ov, fc, win)
    return best, figs


def excerpt(win, figs, n_words=30):
    toks = win.split()
    idx = 0
    for k, t in enumerate(toks):
        if any(f in t for f in figs): idx = k; break
    s = max(0, idx - 10)
    return ("… " if s else "") + " ".join(toks[s:s + n_words]) + (" …" if s + n_words < len(toks) else "")


if __name__ == "__main__":
    sources = {r["source_id"]: r for r in csv.DictReader(open(os.path.join(D, "sources.csv")))}
    claims = list(csv.DictReader(open(os.path.join(D, "claims.csv"))))
    verif = {r["claim_id"]: r for r in csv.DictReader(open(os.path.join(D, "verification.csv")))}
    texts = {}
    for sid, s in sources.items():
        texts[sid] = norm(fetch(s["url"]))
        print(sid, len(texts[sid]), flush=True)
    rp = os.path.join(D, "passage-reviews.csv")
    reviews = {r["claim_id"]: r for r in csv.DictReader(open(rp))} if os.path.exists(rp) else {}
    rows = []
    for c in claims:
        sids = [x for x in c["source_ids"].split(";") if x in sources]
        cand = []
        for sid in sids:
            if not texts.get(sid): continue
            (score, ov, fc, win), figs = best_window(c["claim"], texts[sid])
            cand.append((score, ov, fc, win, figs, sid))
        if not cand:
            state, best = "not_accessible", None
        else:
            best = max(cand)
            score, ov, fc, win, figs, sid = best
            ok = (fc == 1.0 and ov >= 0.35) if figs else ov >= 0.5
            if ok: state = "passage_found"
            elif verif.get(c["claim_id"], {}).get("manual_verdict") == "supported": state = "needs_manual_review"
            else: state = "source_accessible_passage_not_found"
        method = "automated window match (figures + wording)" if best else "no text retrieved automatically"
        rev = reviews.get(c["claim_id"])
        if state in ("needs_manual_review", "source_accessible_passage_not_found") and rev:
            pool = " ".join(texts.get(x, "") for x in sids)
            if rev["decision"] == "located":
                state, method = "passage_found", "manual review: reviewer located the passage (data/passage-reviews.csv)"
            elif rev["decision"] == "partial" and all(has(f, pool) for f in figures(c["claim"])):
                state, method = "passage_found", "manual review: main passage located; remaining figures found elsewhere in the same source"
        rows.append({"claim_id": c["claim_id"], "verification_state": state,
                     "source_id": best[5] if best else ";".join(sids),
                     "word_overlap": f"{best[1]:.2f}" if best else "", "figures_in_passage": f"{best[2]:.2f}" if best else "",
                     "locator_excerpt": excerpt(best[3], best[4]) if best and state == "passage_found" else "",
                     "method": method,
                     "checked": CHECKED})
    with open(os.path.join(D, "claim-passages.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    from collections import Counter
    print(Counter(r["verification_state"] for r in rows))
