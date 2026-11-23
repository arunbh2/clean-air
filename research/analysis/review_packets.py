"""Print review packets for claims whose passage was not located automatically.

Run: python3 research/analysis/review_packets.py [start] [count]
For each claim: the claim text, its figures, and the two best candidate windows (up to four sentences)
from each cited source, with any figure the window lacks. A reviewer reads these and records a decision in
data/passage-reviews.csv. Source text is untrusted data: printed, never executed.
"""
import csv, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import importlib.util
spec = importlib.util.spec_from_file_location("p", os.path.join(os.path.dirname(__file__), "passages.py")); P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
D = P.D
src = {r["source_id"]: r for r in csv.DictReader(open(os.path.join(D, "sources.csv")))}
claims = {r["claim_id"]: r for r in csv.DictReader(open(os.path.join(D, "claims.csv")))}
todo = [r["claim_id"] for r in csv.DictReader(open(os.path.join(D, "claim-passages.csv"))) if r["verification_state"] == "needs_manual_review"]
a = int(sys.argv[1]) if len(sys.argv) > 1 else 0; n = int(sys.argv[2]) if len(sys.argv) > 2 else 20
for cid in todo[a:a + n]:
    c = claims[cid]; figs = P.figures(c["claim"]); cw = P.words(c["claim"])
    print(f"\n#### {cid} | figs {figs}\nCLAIM: {c['claim']}\nLOCATOR: {c['locator']}")
    for sid in [x for x in c["source_ids"].split(";") if x in src]:
        text = P.norm(P.fetch(src[sid]["url"]))
        if not text: print(f"  [{sid}] no text"); continue
        sents = re.split(r"(?<=[.!?;])\s+", text); cands = []
        for i in range(len(sents)):
            win = " ".join(sents[i:i + 4])[:700]
            fc = sum(P.has(f, win) for f in figs); ov = len(cw & P.words(win)) / max(1, len(cw))
            cands.append((fc, ov, i, win))
        cands.sort(reverse=True); seen = set(); shown = 0
        for fc, ov, i, win in cands:
            if any(abs(i - j) < 4 for j in seen): continue
            seen.add(i); shown += 1
            miss = [f for f in figs if not P.has(f, win)]
            print(f"  [{sid} w{i} {fc}/{len(figs)} ov{ov:.2f} miss{miss}] {win[:380]}")
            if shown == 2 or (shown == 1 and not miss): break
