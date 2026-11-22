# QA report

Pages checked: 61

| Check | Result | Detail |
|---|---|---|
| every page shows the research cutoff | pass |  |
| every page has exactly one h1 | pass |  |
| home logo link named "Clean Air — home" | pass |  |
| no broken internal links or anchors | pass | 0 problems |
| no external scripts, styles or images | pass |  |
| intervention filter shows only "Fund now" items | pass | 4 shown vs 4 in CSV |
| organisation filter narrows the table | pass | 4 rows |
| every citation resolves to a claim | pass | 707 citations, 0 unresolved |
| first Tab focuses the skip link | pass | skip|Skip to content |
| focused element shows an outline | pass | solid |
| no horizontal page scroll at 320 px | pass |  |
| home page has no horizontal scroll with text at 200% | pass | 0px |
| print hides navigation and produces a PDF | pass |  |
| logos are pure vector with transparent backgrounds | pass |  |
| home page under 150 KB including CSS, JS and logos | pass | 26 KB |
| no axe WCAG 2.1 A/AA violations | pass | 0 violation types across 0 pages |

External links (source URLs, verified in Phase 2): 68

## axe violations

None.

## Additional checks

- Rating change test (`rating_change_test.py`): pass
- Screenshot review at 1280 px and 390 px: home, crisis, people, a community page, places, what works, two intervention pages, support, brief, claims. Issues found and fixed: header gutter, mobile card overflow, overuse of red rules, misleading badge for 'evidence of very limited effect', badges unreadable in print, oversized metadata text.
- Run on 22 November 2026 against site/dist built from commit HEAD.

## Limits of this QA

- **axe is automated.** It finds roughly a third to a half of WCAG issues. No manual screen-reader pass (NVDA, VoiceOver) was done.
- **Fonts in the test environment.** The test browser had no Georgia installed, so screenshots show a fallback serif. On most visitor devices Georgia is present.
- **Favicon size not proven.** The favicon is a simplified three-bar mark designed for 16 and 32 px, but it was not rendered and inspected at 16 px.
- **External links.** These were checked in Phase 2 (`research/VERIFICATION.md`), not in this run.

## Deployment readiness

The site is ready for any static host:

1. Run `python3 site/build.py`.
2. Upload `site/dist/`.

There is no server code, no analytics, no cookies and no external requests. No domain has been chosen. Before going live, re-run `node site/qa/qa.js` and `python3 site/qa/rating_change_test.py`.
