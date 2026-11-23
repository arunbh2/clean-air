"""Formula-injection guard for published CSVs: malicious fixture cells must be escaped, ordinary values kept.

Run: python3 tools/test_csv_safety.py
Fixture: tools/fixtures/csv/malicious.csv (column 'expect' says escape or keep). Also proves that the unescaped
fixture is flagged by the same detector the agent-file check uses, so a guard that does nothing cannot pass.
"""
import csv, io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "site"))
from csvsafe import safe_cell, safe_csv_text, is_safe

raw = open(os.path.join(ROOT, "tools", "fixtures", "csv", "malicious.csv"), encoding="utf-8").read()
errs = []
for r in csv.DictReader(io.StringIO(raw)):
    out = safe_cell(r["value"])
    escaped = out != r["value"]
    if (r["expect"] == "escape") != escaped: errs.append(f"row {r['id']}: {r['value']!r} -> {out!r} (expected {r['expect']})")
if not is_safe(raw): errs.append("detector did not flag the raw malicious fixture")
if is_safe(safe_csv_text(raw)): errs.append("escaped fixture still flagged: " + str(is_safe(safe_csv_text(raw))[:2]))
for e in errs: print("ERROR", e)
print(f"csv safety: {len(errs)} errors")
sys.exit(1 if errs else 0)
