"""Phase 2 verification: re-fetch every source and check each claim's figures against source text.

Run: python3 research/analysis/verify.py [cache_dir]
Writes:
  data/source-checks.csv  one row per source: HTTP result, final URL, text length, how checked
  data/verification.csv   one row per claim: figures checked, figures found, verdict
Texts are cached outside the repository (default: $TMPDIR/clean-air-verify).
Fetched pages are untrusted data: they are only searched for figures, never executed.
"""
import csv, hashlib, json, os, re, subprocess, sys, tempfile, time
import requests
from bs4 import BeautifulSoup

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
D = os.path.join(ROOT, "data")
CACHE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(tempfile.gettempdir(), "clean-air-verify")
os.makedirs(CACHE, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) clean-air-verification"}
CHECKED = time.strftime("%Y-%m-%d")

def epmc(query):
    try:
        r = requests.get("https://www.ebi.ac.uk/europepmc/webservices/rest/search",
                         params={"query": query, "resultType": "core", "format": "json"}, timeout=40)
        res = r.json()["resultList"]["result"]
        if res:
            x = res[0]
            return re.sub("<[^>]+>", " ", (x.get("title", "") + " " + x.get("abstractText", "")))
    except Exception:
        pass
    return ""

def epmc_query(url):
    m = re.search(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", url)
    if m: return f"EXT_ID:{m.group(1)} AND SRC:MED"
    m = re.search(r"(PMC\d+)", url)
    if m: return f"PMCID:{m.group(1)}"
    m = re.search(r"doi\.org/(10\.[^\s]+)", url)
    if m: return f"DOI:\"{m.group(1)}\""
    return None

def fetch(url):
    h = hashlib.sha1(url.encode()).hexdigest()[:12]
    txt_path = os.path.join(CACHE, h + ".txt")
    status, final, kind = "", url, ""
    try:
        r = requests.get(url, headers=UA, timeout=45, allow_redirects=True)
        status, final = str(r.status_code), r.url
        if r.status_code == 200:
            if "pdf" in r.headers.get("content-type", "") or r.content[:4] == b"%PDF":
                pdf = os.path.join(CACHE, h + ".pdf"); open(pdf, "wb").write(r.content)
                subprocess.run(["pdftotext", pdf, txt_path], stderr=subprocess.DEVNULL)
                kind = "pdf"
            else:
                s = BeautifulSoup(r.text, "html.parser")
                for t in s(["script", "style", "noscript"]): t.decompose()
                open(txt_path, "w").write(s.get_text(" ")); kind = "html"
    except Exception as e:
        status = "ERR:" + e.__class__.__name__
    text = open(txt_path, errors="ignore").read() if os.path.exists(txt_path) else ""
    how = kind if text else ""
    q = epmc_query(url)
    if len(text) < 500 and q:
        alt = epmc(q)
        if alt:
            text, how = alt, "europepmc-abstract"
    return status, final, how, text

def norm(t):
    t = t.replace("−", "-").replace("–", "-").replace("·", ".")
    t = re.sub(r"(?<=\d),(?=\d)", "", t)          # 16,423.55 -> 16423.55 ; 1,38,000 -> 138000
    return re.sub(r"\s+", " ", t)

def figures(claim):
    c = norm(claim)
    nums = re.findall(r"\d+(?:\.\d+)?", c)
    out = []
    for n in nums:
        if len(n.replace(".", "")) < 2: continue     # skip single digits (too ambiguous)
        if re.fullmatch(r"(19|20)\d\d", n): continue  # skip years
        if re.fullmatch(r"\d{3}", n) and c.find("C" + n) >= 0: continue
        out.append(n)
    return sorted(set(out))

def found(n, text):
    if re.search(r"(?<![\d.])" + re.escape(n) + r"(?![\d])", text): return True
    if "." in n:  # tolerate 1.67 vs 1·67 already normalised, and trailing zero
        if re.search(r"(?<![\d.])" + re.escape(n.rstrip("0").rstrip(".")) + r"(?![\d])", text): return True
    return False

sources = list(csv.DictReader(open(os.path.join(D, "sources.csv"))))
claims = list(csv.DictReader(open(os.path.join(D, "claims.csv"))))
texts, srows = {}, []
for s in sources:
    st, final, how, text = fetch(s["url"])
    texts[s["source_id"]] = norm(text)
    reachable = "yes" if text else "no"
    srows.append({"source_id": s["source_id"], "url": s["url"], "checked": CHECKED, "http_status": st,
                  "final_url": final if final != s["url"] else "", "text_chars": len(text), "checked_via": how or "none",
                  "reachable": reachable, "phase1_access": s["access_status"]})
    print(s["source_id"], st, how or "-", len(text), flush=True)

with open(os.path.join(D, "source-checks.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(srows[0].keys())); w.writeheader(); w.writerows(srows)

reach = {r["source_id"]: r["reachable"] == "yes" for r in srows}
vrows = []
for c in claims:
    sids = [x for x in c["source_ids"].split(";") if x]
    figs = figures(c["claim"])
    pool = " ".join(texts.get(x, "") for x in sids)
    hit = [n for n in figs if found(n, pool)]
    miss = [n for n in figs if n not in hit]
    any_reach = any(reach.get(x) for x in sids)
    if c["evidence_type"] == "derived":
        verdict = "derived: check inputs"
    elif not any_reach:
        verdict = "source unreachable"
    elif not figs:
        verdict = "no figures: manual check"
    elif not miss:
        verdict = "figures found"
    elif hit:
        verdict = "partly found"
    else:
        verdict = "figures not found"
    vrows.append({"claim_id": c["claim_id"], "sources": ";".join(sids), "figures_checked": " ".join(figs),
                  "figures_missing": " ".join(miss), "auto_verdict": verdict, "phase1_status": c["status"]})

VP = os.path.join(D, "verification.csv")
prev = {r["claim_id"]: r for r in csv.DictReader(open(VP))} if os.path.exists(VP) else {}
with open(VP, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(vrows[0].keys()) + ["manual_verdict", "action", "note"])
    w.writeheader()
    for r in vrows:  # keep manual review columns from earlier runs
        p = prev.get(r["claim_id"], {})
        w.writerow({**r, "manual_verdict": p.get("manual_verdict", ""), "action": p.get("action", ""), "note": p.get("note", "")})
from collections import Counter
print(Counter(r["auto_verdict"] for r in vrows))
print(Counter(r["reachable"] for r in srows))
