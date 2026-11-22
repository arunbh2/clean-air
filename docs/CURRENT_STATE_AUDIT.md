# Clean Air: current-state audit before the 10× expansion

Audit date: 22 November 2026 · Research cutoff: 22 November 2026 · Audited commit: `d877167` (main, live at https://arunbh2.github.io/clean-air/)

This audit was made from the repository source, the generated output and the live deployment. It is not a usability study with real readers.

## 1. Pipeline (how the site is made)

```
research/report/*.md      ─┐
research/data/*.csv       ─┤  site/build.py (Python, Jinja2, Python-Markdown)
research/site-content/*   ─┼──────────────────────────────────────────────▶ site/dist/  ──▶ GitHub Pages
research/decision-brief.md ┤  templates: site/templates/*.html                         (.github/workflows/pages.yml)
research/VERIFICATION.md  ─┘  static:    site/static/{css,js,logo}
```

**Commands**

| Command | What it does |
|---|---|
| `python3 research/analysis/validate.py` | Checks referential integrity |
| `python3 research/analysis/verify.py` | Re-fetches sources and checks claim figures |
| `python3 research/analysis/export.py` | Builds the PDF and Markdown exports |
| `python3 site/build.py` | Builds the site |
| `node site/qa/qa.js` | Runs axe, link, functional, reflow, print and weight checks |
| `python3 site/qa/rating_change_test.py` | Proves that changing a CSV rating changes the site |

**Deployment.** The workflow builds the site on every pull request and deploys it on every push to `main`.

**Stack.** A static generator with no client framework. The only JavaScript is about 1 KB of progressive enhancement (filters and a print button).

## 2. Inventory at audit

| Item | Count | Notes |
|---|---|---|
| Generated pages | 61 | home, 7 sections, 15 people, 6 places, 18 interventions, 4 portfolios, 7 evidence, brief, downloads, 404 |
| Claims (`C001`–`C110`) | 110 | 109 verified in Phase 2; C056 unverifiable (cpcb.nic.in down); C034 provisional |
| Sources (`S001`–`S068`) | 68 | 67 reachable at re-check |
| Settings | 6 | all in India |
| Communities | 15 | priorities: 5 outdoor-worker groups (P1) and children (P2) |
| Interventions | 18 | 4 fund now, 9 test first, 5 not recommended; classes A–D |
| Organisations | 21 | function-based, verified activity only |
| Portfolios | 4 | PF1–PF4, dated 22 November 2026 |
| Evidence gaps | 12 | G1–G12 |
| Downloads | 2 PDFs, 2 Markdown, 13 CSVs | |

## 3. Strengths to preserve

- **Measurement concepts kept apart.** Daily, seasonal and long-term exposure are separated, and AQI is never treated as dose.
- **Two separate ratings.** Confidence that a problem exists and confidence that a response works are rated separately, with written reasons, using the four labels.
- **Policy losses separate from illness losses.** Income lost to restrictions is separated from income lost to illness, and GDP-scale estimates are never used for households.
- **Traceable claims.** Every factual sentence carries a claim ID, every claim has a source, and every source has access and re-check status.
- **Data-driven pages.** CSV ratings drive the pages, and this is tested.
- **Accessibility and weight.** No automated axe AA violations, no external requests, and a 26 KB homepage.

## 4. Gap matrix

| Area | Status at audit | Issue | Priority | Effort |
|---|---|---|---|---|
| Geography | existing: India only (6 settings) | South Asia airshed and South-East Asia missing | high | high |
| Funding | existing: organisation map mentions finance | no programme-level atlas with instrument, stage and amount type | high | high |
| Lay first layer | **needs simplification** | sections open with dense report prose; acronyms (GRAP, NCAP, BOCW, CAQM, PM2.5) often unexplained at first use; long tables | high | medium |
| Start here and glossary | missing | no glossary, no inline definitions | high | low |
| Homepage | existing: works | lacks beginner questions, story choices, regional lens, funding signal, gap cards | high | medium |
| What works | existing: 18 entries, verdicts | no intervention class (emissions / exposure / governance …), no regional cases, no comparison tool | high | medium |
| People journeys | existing: 15 groups | no guided story path with labelled arrows | medium | medium |
| Decision support | existing: 4 India options | no regional pathways, no board briefing view | medium | medium |
| Evidence | existing: registers, map, gaps | no coverage dashboard, no region filter, no stale-review checks | medium | low |
| Governance docs | missing | no evidence policy, content governance, research log, corrections route | medium | low |
| Footer | partial | no About, Methodology, Corrections, Update policy, Privacy or Accessibility pages | medium | low |
| Accuracy | none found uncited | Phase 2 fixed C100; C034 and C056 remain provisional | low | — |
| Design consistency | minor | metadata sizes were mixed before Phase 4 fixes; badges fixed for print | low | — |

## 5. Decisions taken from this audit

1. **Keep the stack.** It is fast, tested and GitHub Pages-compatible, and there is no maintenance case for a framework rewrite.
2. **Keep all existing URLs, slugs, claim IDs, source IDs and verdicts.** New records append from `C111` and `S069` upwards.
3. **Extend the existing evidence base with migration-safe new files**: `countries.csv`, `programmes.csv`, `funders.csv`, `glossary.csv`, `research/site-content/stories/`. Nothing is duplicated.
4. **Add second-level hubs** under the seven existing routes. Do not add new top-level navigation.
5. **Keep the four India portfolio options as the dated baseline.** Regional pathways are added alongside them.
