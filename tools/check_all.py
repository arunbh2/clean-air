"""Clean Air: the single validation command.

Run:  python3 tools/check_all.py            (registers, build, every content/design/agent check, every self-test)
      python3 tools/check_all.py --browser  (also the Playwright + axe browser suite in site/qa/qa.js)

CI runs this before any deployment (.github/workflows/pages.yml). A checker that does nothing cannot pass:
each guard also runs a --self-test against a deliberately bad fixture and must FAIL on it.
Writes a summary to site/qa/report/check-all.md.
"""
import os, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
T = lambda *a: [PY, os.path.join(ROOT, *a)]
STEPS = [
    ("Research registers and governance gates", T("research", "analysis", "validate.py")),
    ("Build site from /research", T("site", "build.py")),
    ("Rating change propagates to the page", T("site", "qa", "rating_change_test.py")),
    ("Editorial voice on generated copy", T("tools", "check_voice.py")),
    ("Voice checker fails on bad fixture", T("tools", "check_voice.py") + ["--self-test"]),
    ("Design guardrails (stripes, cards, type, colours, contrast, budget)", T("tools", "check_design.py")),
    ("Design checkers fail on bad fixtures", T("tools", "check_design.py") + ["--self-test"]),
    ("Internal links, anchors, URL shape, first answers", T("tools", "check_links.py")),
    ("Link checker fails on bad fixture", T("tools", "check_links.py") + ["--self-test"]),
    ("Agent files: mirrors, llms.txt, corpus, packs, sync, CSV", T("tools", "check_agent_files.py")),
    ("Agent-file checker fails on damaged build", T("tools", "check_agent_files.py") + ["--self-test"]),
    ("Worked questions identical across HTML, Markdown, JSON", T("tools", "test_formats.py")),
    ("Format comparison fails on tampered JSON", T("tools", "test_formats.py") + ["--self-test"]),
    ("CSV formula-injection guard (malicious fixture)", T("tools", "test_csv_safety.py")),
    ("Canonical edit and withdrawal propagate everywhere", T("tools", "test_propagation.py")),
]
if "--browser" in sys.argv:
    STEPS.append(("Browser suite: axe WCAG 2.2 AA, reflow, zoom, keyboard, print, journeys", ["node", os.path.join(ROOT, "site", "qa", "qa.js")]))


def main():
    rows, failed = [], 0
    for name, cmd in STEPS:
        t0 = time.time()
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        ok = r.returncode == 0
        last = (r.stdout.strip().splitlines() or [""])[-1][:140]
        rows.append((name, ok, round(time.time() - t0, 1), last))
        print(f"{'PASS' if ok else 'FAIL'}  {name}  ({rows[-1][2]}s)  {last}", flush=True)
        if not ok:
            failed += 1
            print(r.stdout[-3000:]); print(r.stderr[-2000:])
            if name.startswith("Build"): break
    os.makedirs(os.path.join(ROOT, "site", "qa", "report"), exist_ok=True)
    with open(os.path.join(ROOT, "site", "qa", "report", "check-all.md"), "w") as f:
        f.write("# check_all summary\n\n| Check | Result | Seconds | Last line |\n|---|---|---|---|\n")
        for n, ok, s, l in rows: f.write(f"| {n} | {'pass' if ok else '**FAIL**'} | {s} | {l.replace('|', '/')} |\n")
    print(f"\n{len(rows) - failed} of {len(rows)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
