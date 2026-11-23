"""Spreadsheet formula-injection guard for published CSV downloads.

A cell that a spreadsheet would treat as a formula is prefixed with an apostrophe (') so it is shown as
text. Triggers: a first non-whitespace character of =, +, -, @, or a leading tab / carriage return /
other control character (OWASP CSV injection guidance). Plain numbers such as -3.5 or +12 stay numbers,
because escaping them would change the data. The canonical research CSVs are never modified: only the
copies in downloads/data/ are escaped, and the escaping is documented in the data catalogue.
"""
import csv, io, re

NUMERIC = re.compile(r"^[+-]?(\d+([.,]\d+)*|\d*\.\d+)(e[+-]?\d+)?%?$", re.I)
TRIGGER = re.compile(r"^[\s\x00-\x1f]*[=+\-@]|^[\t\r\x00-\x1f]")


def safe_cell(v):
    if v is None or v == "": return v
    s = str(v)
    if NUMERIC.match(s.strip()): return s
    if TRIGGER.match(s): return "'" + s
    return s


def safe_csv_text(text):
    rows = list(csv.reader(io.StringIO(text)))
    out = io.StringIO()
    w = csv.writer(out, lineterminator="\n")
    for i, r in enumerate(rows):
        w.writerow(r if i == 0 else [safe_cell(c) for c in r])
    return out.getvalue()


def is_safe(text):
    rows = list(csv.reader(io.StringIO(text)))
    return [(i, j, c) for i, r in enumerate(rows[1:], 1) for j, c in enumerate(r)
            if c and not NUMERIC.match(c.strip()) and TRIGGER.match(c)]
