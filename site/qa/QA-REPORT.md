# QA report

Pages checked: 140

| Check | Result | Detail |
|---|---|---|
| every page shows the research cutoff | pass |  |
| every page has exactly one h1 | pass |  |
| home logo link named "Clean Air — home" | pass |  |
| no broken internal links or anchors | pass | 0 problems |
| no external scripts, styles or images | pass |  |
| intervention filter shows only "Fund now" items | pass | 4 shown vs 4 in CSV |
| organisation filter narrows the table | pass | 4 rows |
| every citation resolves to a claim | pass | 1047 citations, 0 unresolved |
| first Tab focuses the skip link | pass | skip|Skip to content |
| focused element shows an outline | pass | solid |
| street-vendor journey: home → story → response (2 clicks) → funding → gap | pass |  |
| funder journey: atlas → Bangladesh record → pathway with falsification test | pass |  |
| comparison shows at most three interventions | pass | 3 shown |
| every image has an alt attribute | pass | 0 without alt |
| no horizontal page scroll at 320 px | pass |  |
| home page has no horizontal scroll with text at 200% | pass | 0px |
| print hides navigation and produces a PDF | pass |  |
| logos are pure vector with transparent backgrounds | pass |  |
| home page under 150 KB including CSS, JS and logos | pass | 49 KB |
| no axe WCAG 2.1 A/AA violations | pass | 0 violation types across 0 pages |

External links (source URLs, verified in Phase 2): 110

## axe violations

None.

## Additional checks

- Rating change test: pass
- Run on 22 November 2026 against site/dist (140 pages), regional edition.

## Limits

- axe is automated and catches only part of WCAG; no manual screen-reader pass yet.
- Test browser lacked Georgia; screenshots show a fallback serif.
- External links were checked by research/analysis/verify.py (107 of 110 reachable), not by this run.
