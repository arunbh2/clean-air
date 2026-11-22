"""Assemble the report and decision brief into single Markdown files and PDFs.

Run: python3 research/analysis/export.py
Requires pandoc and Node with the pre-installed Playwright (html2pdf.js).
Outputs go to research/exports/ with the research cutoff in each filename.
"""
import csv, glob, os, re, subprocess, html

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "exports")
CUTOFF = "2026-11-22"
os.makedirs(OUT, exist_ok=True)

def body(path):
    t = open(path).read()
    return re.sub(r"\A---\n.*?\n---\n", "", t, flags=re.S).strip()

claims = list(csv.DictReader(open(os.path.join(ROOT, "data", "claims.csv"))))
sources = list(csv.DictReader(open(os.path.join(ROOT, "data", "sources.csv"))))

def esc(s):  # Markdown table cell
    return s.replace("|", "\\|").replace("\n", " ")

def appendix(cited):
    lines = ["# Appendix A. Claim register (cited claims)", "",
             "| Claim | Statement | Sources | Status |", "|---|---|---|---|"]
    for c in claims:
        if c["claim_id"] in cited:
            lines.append(f"| {c['claim_id']} | {esc(c['claim'])} | {c['source_ids'].replace(';', ', ')} | {c['status']} |")
    used = {s for c in claims if c["claim_id"] in cited for s in c["source_ids"].split(";")}
    lines += ["", "# Appendix B. Source register", "",
              "| Source | Title | Author / organisation | Published | Access | URL |", "|---|---|---|---|---|---|"]
    for s in sources:
        if s["source_id"] in used:
            lines.append(f"| {s['source_id']} | {esc(s['title'])} | {esc(s['author_org'])} | {s['pub_date']} | {s['access_status']} | <{s['url']}> |")
    return "\n".join(lines)

CSS = """
:root{--ca-ink:#1A1A1A;--ca-navy:#141F52;--ca-accent:#E3120B;--ca-link:#2E45B8;--ca-paper:#F5F4EF;--ca-muted:#595959;--ca-rule:#D9D9D9;--ca-tint:#EBEDFA}
@page{size:A4;margin:18mm 16mm 18mm 16mm}
body{font-family:Georgia,'Times New Roman',serif;color:var(--ca-ink);font-size:10.5pt;line-height:1.5;max-width:none}
h1,h2,h3{font-family:Georgia,serif;color:var(--ca-navy);line-height:1.2}
h1{font-size:20pt;border-top:3px solid var(--ca-accent);padding-top:8px;margin-top:28px;page-break-before:always}
h1:first-of-type{page-break-before:avoid}
h2{font-size:13.5pt;margin-top:20px}
h3{font-size:11.5pt}
a{color:var(--ca-link);word-break:break-all}
table{border-collapse:collapse;width:100%;font-family:system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;font-size:8pt;font-variant-numeric:tabular-nums;margin:10px 0}
th{background:var(--ca-tint);color:var(--ca-navy);text-align:left}
th,td{border-bottom:1px solid var(--ca-rule);padding:4px 5px;vertical-align:top}
tr{page-break-inside:avoid}
code{font-size:9pt}
.cover{page-break-after:always;padding-top:60mm}
.cover .mark{display:flex;align-items:center;gap:14px}
.cover h1{border:none;page-break-before:avoid;font-size:30pt;margin:0}
.cover .tag{font-size:13pt;color:var(--ca-muted);margin-top:6px}
.cover .meta{margin-top:40mm;font-family:system-ui,Arial,sans-serif;font-size:10pt;color:var(--ca-muted);border-top:1px solid var(--ca-rule);padding-top:8px}
"""

SYMBOL = """<svg width="56" height="40" viewBox="0 0 112 80" aria-hidden="true"><path d="M4 30 C24 6 52 12 70 18 C86 23 98 20 108 4 C100 26 80 34 62 30 C44 26 22 20 4 30 Z" fill="#141F52"/><path d="M8 52 C26 32 50 38 66 42 C80 46 92 44 102 32 C94 50 76 56 60 52 C44 48 24 44 8 52 Z" fill="#E3120B"/><path d="M4 76 C22 56 48 62 64 66 C80 70 92 68 102 56 C94 74 76 80 58 76 C42 72 22 68 4 76 Z" fill="#141F52"/></svg>"""

def cover(title, subtitle, kind):
    return (f"<div class='cover'><div class='mark'>{SYMBOL}<h1>Clean Air</h1></div>"
            f"<p class='tag'>Shared air. Unequal protection.</p>"
            f"<h2 style='margin-top:30mm;font-size:18pt'>{html.escape(title)}</h2><p>{html.escape(subtitle)}</p>"
            f"<p class='meta'>{kind} · Research cutoff {CUTOFF} · Independent evidence resource. "
            f"No endorsement by any organisation named in the research is implied.</p></div>")

def render(md_text, cover_html, md_out, pdf_out, title):
    open(md_out, "w").write(md_text)
    html_body = subprocess.run(["pandoc", "-f", "gfm", "-t", "html5"], input=md_text, capture_output=True, text=True, check=True).stdout
    doc = f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{html.escape(title)}</title><style>{CSS}</style></head><body>{cover_html}{html_body}</body></html>"
    tmp = pdf_out.replace(".pdf", ".html")
    open(tmp, "w").write(doc)
    subprocess.run(["node", os.path.join(os.path.dirname(__file__), "html2pdf.js"), tmp, pdf_out, f"Clean Air · cutoff {CUTOFF}"], check=True)
    os.remove(tmp)

sections = sorted(glob.glob(os.path.join(ROOT, "report", "*.md")))
report_md = "\n\n".join(body(s) for s in sections)
cited = set(re.findall(r"\[(C\d{3})\]", report_md))
report_md += "\n\n" + appendix(cited)
render(report_md,
       cover("Shared air, unequal costs", "Where philanthropy can improve health and livelihood security in India. Full research report.", "Research report"),
       os.path.join(OUT, f"clean-air-research-report_cutoff-{CUTOFF}.md"),
       os.path.join(OUT, f"clean-air-research-report_cutoff-{CUTOFF}.pdf"), "Clean Air research report")

brief_md = body(os.path.join(ROOT, "decision-brief.md"))
bcited = set(re.findall(r"\[(C\d{3})\]", brief_md))
brief_full = brief_md + "\n\n" + appendix(bcited)
render(brief_full,
       cover("Shared air, unequal costs", "Decision brief.", "Decision brief"),
       os.path.join(OUT, f"clean-air-decision-brief_cutoff-{CUTOFF}.md"),
       os.path.join(OUT, f"clean-air-decision-brief_cutoff-{CUTOFF}.pdf"), "Clean Air decision brief")
print("cited in report:", len(cited), "| cited in brief:", len(bcited))
for f in sorted(os.listdir(OUT)): print(f, os.path.getsize(os.path.join(OUT, f)))
