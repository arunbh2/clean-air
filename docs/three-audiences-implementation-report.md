# Three-audience implementation report

**Brief:** `docs/three-audiences-governance-brief.md` · **Date:** 23 November 2026 · **Research cutoff:** 22 November 2026 (unchanged)
**Branch:** `claude/focused-rubin-m4wcmo` · **Deployment:** not deployed. The live site changes only when this branch is merged into `main`, after CI passes.

## 1. What changed, in one paragraph

The site now has one factual record and four ways of reading it: the web page, a Markdown copy of every page, JSON and CSV data, and short evidence packs. One command (`python3 tools/check_all.py`) builds all of them and checks voice, design, links, agent files, cross-format consistency, CSV safety and propagation. Each guard also has to fail on a deliberately bad test file. CI runs the same command, with the browser suite, before any deployment. Clean Air's branding, URLs, claim and source IDs, evidence labels and cutoff are unchanged.

## 2. Files changed

97 files relative to the pre-work commit `910adc1` (53 added, 44 modified), plus screenshots.

| Area | Files |
|---|---|
| Governance documents | `docs/THREE_AUDIENCES_AUDIT.md`, `editorial-voice.md`, `design-guardrails.md`, `agent-access.md`, `data-model.md`, `three-audiences-maintenance.md`, this report; `CLAUDE.md` rule 7 |
| Checks (all in `tools/`) | `check_all.py`, `check_voice.py` + `voice-exceptions.csv`, `check_design.py` + `design-tokens.json`, `check_links.py`, `check_agent_files.py`, `test_formats.py`, `test_csv_safety.py`, `test_propagation.py`, `fixtures/` (voice, design, CSV) |
| Generator | `site/build.py` (config, claim enrichment, safe CSV, hooks), `site/build_agent.py` (packs, for-ai, corrections, mirrors, llms, sitemaps, feed, catalogue), `site/mdmirror.py`, `site/csvsafe.py`, `site/site.json` |
| Templates and CSS | new `pack.html`, `packs_index.html`, `corrections.html`; first-answer layers in `group.html`, `intervention.html`, `programme.html`, `setting.html`; `claims.html`, `base.html`, `org_profile.html`, `orgs.html`, `compare.html`, `pathway.html`, `sources.html`, `country.html`; `site.css` |
| Research data | new `claim-passages.csv`, `corrections.csv`, `changelog.csv`, `data-dictionary.csv`, `analysis/passages.py`; copy fixes in 8 CSVs and 14 Markdown files; `validate.py` gates |
| Content | new `site-content/for-ai.md`, `pages/reuse.md`, `questions/q1 to q3`; `pages/corrections.md` |
| CI and QA | `.github/workflows/pages.yml` runs `check_all.py --browser`; `site/qa/qa.js` gains 6 checks and screenshots |

## 3. Public features added (live once merged; paths under `https://arunbh2.github.io/clean-air/`)

| Feature | Path |
|---|---|
| Evidence packs: 33 packs (3 worked questions, 9 countries, 15 communities, 5 intervention classes, 1 funding view), each in HTML, Markdown and JSON | `packs/index.html`, `packs/index.json` |
| Page for AI assistants and their users | `for-ai/index.html`, `for-ai.json`, `for-ai.txt` |
| `llms.txt` index and `llms-full.txt` corpus (1.96 MB, every page) | `llms.txt`, `llms-full.txt` |
| Markdown copy of every page (314), linked from each page | `<page>.md` |
| Corrections register: 11 real entries with earlier wording, reason and the pages that cite each record | `about/corrections.html` |
| Passage-level verification state, provenance class and supporting excerpt on every claim | `evidence/claims.html`, `downloads/data/claims.json` |
| Plain-language first answer on 66 more record pages (communities, interventions, funding records, places) | e.g. `people/construction-workers.html` |
| Data catalogue, 25 JSON Schemas, formula-safe CSV downloads | `downloads/data/catalogue.json`, `downloads/schemas/` |
| Sitemaps (XML and JSON), Atom feed of editions and corrections, `robots.txt` | `sitemap.xml`, `sitemap.json`, `feed.xml`, `robots.txt` |
| Reuse, crawling and AI page (indexing, AI input, AI training and reuse stated separately) | `about/reuse.html` |

Counts: **315 HTML pages** (was 279), **314 Markdown mirrors**, **33 packs**.

## 4. Checks run and results

`python3 tools/check_all.py --browser`: **16 of 16 passed**.

| Check | Result |
|---|---|
| Research registers and new governance gates | pass (3 existing warnings: two claims provisional, one wording flag on J020) |
| Build | pass: 315 pages, 314 mirrors, 33 packs |
| Rating change propagates (existing test) | pass |
| Editorial voice | 0 errors (baseline 166 in the site's own copy); 38 warnings about first-use abbreviations; 6 scoped exceptions, 0 stale |
| Voice checker fails on bad fixture | pass: all 6 error rules fire; good fixture clean |
| Design (stripes, cards, type, colours, contrast, budget) | 0 errors (baseline 35); 18 contrast pairs all at or above their minimum |
| Design checkers fail on bad fixtures | pass: each of the 6 checks fails |
| Links, anchors, URL shape, first answers | 0 errors across 315 pages |
| Link checker fails on bad fixture | pass |
| Agent files (mirrors, llms, corpus, packs, capabilities, corrections sync, CSV, XML, schemas) | 0 errors |
| Agent-file checker fails on damaged build | pass: missing mirror, dead link, over-claim and injection all caught |
| Worked questions identical across HTML, Markdown and JSON | 0 errors (this test caught and led to a fix of a real mirror spacing bug) |
| Format comparison fails on tampered JSON | pass (6 errors raised) |
| CSV injection guard | 13 fixture cells correct; 0 real cells needed escaping |
| Edit and withdrawal propagate to every output in one build | pass |
| Browser suite (Playwright, axe) | **31 of 31**: 0 axe WCAG 2.1/2.2 A/AA violations on 315 pages; no sideways scroll at 320 px (all pages) and at 320, 375, 768 and 1280 px with text at 200% (10 pages); 30 keyboard stops with visible focus; no animations under reduced motion; no rendered text under 12 px; print; journeys; every page declares its Markdown mirror |

Screenshots (desktop and mobile): `docs/screenshots/three-audiences/` (packs, corrections, for-ai, claim register).

## 5. The three worked questions

**1. Which organisations are working on air pollution and informal workers in Delhi?** The records name Chintan (lung-function study of waste pickers, sanitation workers and guards [C082]), Mahila Housing Trust and Help Delhi Breathe (women trained as air quality ambassadors [C195]), construction workers' unions (court action on compensation; the Supreme Court directed that affected workers are to be compensated [C039]), the Delhi construction workers' welfare board and Clean Air Fund. None has an independent evaluation showing reduced exposure. Web: `packs/questions/delhi-informal-workers.html` · agent: `.md`, `.json` · 6 claims, 5 funding items, 17 sources.

**2. Who funds clean-air projects in Bangladesh?** The World Bank approved the Bangladesh Clean Air Project on 18 June 2025, USD 290.00 million of approved financing [C120]. The release does not say whether it is a credit or a grant; the operational stage is not established, and no source reports spending. The EPIC Air Quality Fund awarded grants to Smart Air Bangladesh [C179] and OBHIZATRIK Foundation [C180], amounts not published. The University of Dhaka is named in a Clean Air Fund research grant made with Stockholm University [C170]. Web: `packs/questions/bangladesh-funding.html` · 4 claims, 4 funding items, 11 sources.

**3. Do low-cost air sensors reduce exposure?** Not on present evidence. The records separate measurement [C058][C197], independent testing (none of six manufacturers met NO₂ and ozone precision targets in a Bengaluru co-location study [C202]), public communication [C185][C180] and aims at a policy decision [C184], with no recorded decision yet. The intervention is rated **Limited** for improving outcomes, a value read from `interventions.csv` at build time. Companies appear only as test subjects or operators, unranked. Web: `packs/questions/low-cost-sensors.html` · 9 claims, 7 funding items, 21 sources.

## 6. Unresolved issues (stated plainly)

- **85 claims are `needs_manual_review`.** An earlier human review said they were supported, but the new passage check did not re-locate the passage. They are labelled as such everywhere. Three claims are `not_accessible`. Automated matches on tables can read as a jumble (for example C001's excerpt), so a match is strong evidence of support, not proof of correct reading.
- **Data dictionary:** every dataset has a description, but 291 of 363 columns still read "Not yet described".
- **38 abbreviation warnings** (for example AQI on pages where the glossary link is not on first use). Warnings, not failures.
- **`robots.txt` and `llms.txt` are informative only** while the site lives under a project path (crawlers read them at a domain root).
- **Not created on purpose:** `openapi.json` (no API), `agents.txt`, `auth.md`, `security.txt`, `terms-of-use.md` (owner input needed).
- **No user testing yet** with the readers the brief names. The checks are automated.
- **Inaccessible sources** are unchanged from the atlas edition: Clean Air Asia, CCAC, HACCAP and UNDP pages refused automated access, and GreenHub's site could not be reached (TLS error). They were not bypassed.

## 7. Decisions that need the owner

1. **Licence** for Clean Air's original writing, data and graphics (stated as undecided on `about/reuse.html` and in the catalogue).
2. **AI training permission** for the site's writing (stated as not granted until decided).
3. **Security contact** and expiry before any `security.txt`.
4. **Custom domain**, which would make `robots.txt` and `llms.txt` authoritative.
5. **Terms of use**, if wanted.
6. **Accessible name "Clean Air — home"**: `CLAUDE.md` mandates this text, which contains an em dash. It is kept until you decide.
7. **Merge and deploy** this branch (not done).
