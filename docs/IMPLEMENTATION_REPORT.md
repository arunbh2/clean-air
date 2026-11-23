# Implementation report: Clean Air 10× expansion

Edition: 22 November 2026 (cutoff unchanged) · Branch: `claude/focused-rubin-m4wcmo` · Baseline: `main` at `d877167`

## A. What I found

- **Stack and pipeline.** A static Python generator (`site/build.py`, Jinja2, Python-Markdown) renders every page from `/research` Markdown and CSV. GitHub Pages deploys on every push to `main`, and pull requests build only. There is no client framework and about 1 KB of JavaScript.
- **Baseline.** 61 pages; 110 claims and 68 sources (109 verified); 6 Indian settings; 15 communities; 18 interventions; 21 organisations; 4 dated portfolio options; 12 evidence gaps. No automated (axe) AA violations.
- **Strengths kept.**
  - AQI is kept apart from exposure and dose.
  - Income lost to policy restrictions is kept apart from income lost to illness.
  - Problem and response are rated separately.
  - Every fact is traceable to a claim, and CSV ratings drive the pages.
- **Gaps.**
  - India only.
  - No programme-level funding data.
  - Dense first layer, with acronyms unexplained at first use.
  - No glossary, comparison tool, regional pathways, governance documents or coverage dashboard.
- **Design.** No inconsistencies beyond those fixed in Phase 4. The full audit is in `docs/CURRENT_STATE_AUDIT.md`.

## B. The 10× changes, as reader value

1. **A first layer anyone can read.** Every section now opens with a 40–90 word simple answer, one example and one honest limit. Start here and a 22-term glossary link automatically from first use on each page.
2. **From India to the shared airshed.** There are now 8 new country dossiers: Bangladesh, Nepal, Pakistan, Indonesia, Thailand, Viet Nam, the Philippines and Cambodia. They are built on the same structure and compared with one consistent 2023 estimate. Regional hubs and a fair-comparison page refuse mismatched rankings.
3. **Who funded what.**
   - 20 programme records across philanthropic grants and development or public finance.
   - Approval, operation and evidence are recorded as three separate stages.
   - Amounts appear only where a primary record states them.
   - Each record says how the relationship was verified.
   - 21 funder profiles, including 6 named funders listed as unverified so the gap is visible.
4. **Decisions, not just descriptions.**
   - Six decision pathways, each with a "what would change my mind" test and a printable board briefing.
   - A comparison of up to three interventions with no single score.
   - A "What not to mistake for a solution" page.
   - The four India options are preserved unchanged as the dated baseline.
5. **Cause and effect you can check.** Two guided journeys (street vendor; foundation trustee) use labelled arrows (*well established* … *not yet established in this setting*), so no chain looks proven end to end.

## C. What I implemented

### Data in `/research/data`

- **New files:**
  - `countries.csv`: 9 dossiers plus 6 queued;
  - `programmes.csv`: 20 records;
  - `funders.csv`: 21;
  - `glossary.csv`: 22;
  - `decision-pathways.csv`: 6.
- **Extended files:**
  - `interventions.csv`: now 25, with 7 new regional rows and new class, infrastructure type, status, funder fit and regional cases fields. All 18 existing verdicts are unchanged.
  - `evidence-gaps.csv`: G13–G20 added.
  - `claims.csv`: C111–C153 added.
  - `sources.csv`: S069–S110 added.
  - `verification.csv` and `source-checks.csv`: all rows re-run.

### Site content in `/research/site-content`

- Simple answers in `sections.json`.
- Homepage modules in `home-modules.md`.
- `start.md`.
- Two journeys in `stories/`.
- Five footer pages in `pages/`.

### Templates in `/site/templates`

- **13 new:** glossary, story, country, region, compare_places, funding, programme, funder, compare, not_solution, pathways_index, pathway, coverage.
- **Updated:** the home page and the seven section templates (layered reading and hub links), plus base (footer).

### Build

- `site/build.py`: new collections, the glossary linker ("explain that"), and generation of all new pages.
- `site/requirements.txt`: adds beautifulsoup4.

### New routes (79 new pages; all 61 earlier URLs unchanged)

| Area | Routes |
|---|---|
| Start and glossary | `start/`, `crisis/glossary.html` |
| Places | `places/{bangladesh,nepal,pakistan,indonesia,thailand,vietnam,philippines,cambodia}.html`, `places/south-asia.html`, `places/southeast-asia.html`, `places/compare.html` |
| Funding | `organisations/funding/` and `p01`–`p20.html`; `organisations/funders/*.html` (21) |
| What works | `what-works/compare.html`, `what-works/not-a-solution.html`, 7 new intervention pages |
| Decisions | `support/pathways/` and `dp1`–`dp6.html`, `support/journey-funder.html` |
| People | `people/journey-street-vendor.html` |
| Evidence | `evidence/coverage.html` (`gaps.html` retitled "Where the evidence is thin") |
| Footer | `about/{about,corrections,update-policy,privacy,accessibility}.html` |

### Governance documents

- `docs/CURRENT_STATE_AUDIT.md`, `EVIDENCE_POLICY.md`, `CONTENT_GOVERNANCE.md`, `RESEARCH_LOG.md`, `OPEN_QUESTIONS.md`, `HANDOVER.md`.
- `docs/SOURCE_REGISTER.md`, generated by `research/analysis/source_register.py`.
- `.github/ISSUE_TEMPLATE/` (correction; new source).
- `CLAUDE.md` precedence updated.

### Validation

`validate.py` now also checks:

- programme, funder, country, pathway and intervention references;
- duplicate IDs;
- ISO review dates;
- that every amount has an amount type, a currency and a source;
- that no amount rests on a search snippet;
- orphan claims.

### Tests (all run, all pass)

**`node site/qa/qa.js`** (20 checks on 140 pages):

- axe WCAG 2.1 A and AA: 0 violations;
- 1,047 citations, all resolving to a claim;
- 0 broken internal links or anchors;
- one h1 per page, and the research cutoff on every page;
- logo accessible name, and logos are vector-only with transparent backgrounds;
- no external requests;
- filters work;
- skip link and focus outline;
- no horizontal scroll at 320 px, and none at 200% text size;
- print output;
- homepage at 49 KB;
- both reader journeys, driven by keyboard on a 390 px screen;
- the comparison caps at three interventions;
- every image has alt text.

**`python3 site/qa/rating_change_test.py`**: pass.

**`python3 research/analysis/validate.py`**: no errors.

## D. What is verified and what is unknown

- **Claims.** 153 in total; 149 supported after a re-fetch and manual review. 4 are unverified (C056, C135, C138, C153) and stay labelled provisional. Including C034, there are 5 provisional claims in all.
- **Sources.** 110 in total; 107 reachable at the last check.
- **Funding records** (20):
  - 11 verified from the funder's or lender's own record, or from official or court reporting;
  - 6 from the funder's own account;
  - 1 from a government account;
  - 2 resting on search snippets (Cambodia P13, Philippines P16), both without amounts.
  - Amounts are published for 10 records.
  - None of the records has measured results yet.
- **Not checked.**
  - World Bank and ADB results frameworks and disbursements.
  - The grant databases of six named foundations.
  - Full reports from ADB (March 2026), the World Bank "A Breath of Change" report, and the Clean Air Fund and IGES Southeast Asia platform report. Only their landing pages and summaries were read.
- **Needs a human check.**
  - The figures in P18, which rest on news reports of board statements.
  - The AQLI page figures, which came from a browser render.
  - The Lahore inventory, read second-hand because the original PDF was blocked.
  - The ambiguous Clean Air Fund philanthropic total.

## E. What a foundation could now learn: three illustrative pathways

These are not recommendations.

1. **Protect now (DP1).**
   - **The opportunity:** idled Delhi construction workers are legally owed compensation, and public money exists to pay it. Strong evidence on the problem.
   - **Risk:** board data access.
   - **Evidence quality:** registration support itself is unevaluated.
   - **Gap:** G2.
2. **Measure the invisible (DP2).**
   - **The opportunity:** rural Bihar sensors and community wearables in the Philippines and Indonesia reveal exposure that official networks miss.
   - **Risk:** the data may be dismissed.
   - **Evidence quality:** no documented action triggered yet.
   - **Gaps:** G7, G16.
3. **Build the public systems (DP4).**
   - **The opportunity:** about US$1.2 billion in World Bank airshed programmes has been approved across Bangladesh, Pakistan, Uttar Pradesh, Haryana and Nepal (P01, P02, P04–P06).
   - **Risk:** large commitments without public results.
   - **Evidence quality:** approved targets only.
   - **Gap:** G13. Independent tracking of plan delivery is the low-cost complement.

## F. Next phase, in priority order

1. Open the World Bank and ADB project documents for P01–P07 and record results frameworks and disbursement.
2. Check the grant databases of the six queued foundations, plus Bloomberg Philanthropies and C40 records for Breathe Cities.
3. Gather source studies for Bangkok, Hanoi and Metro Manila, and deepen city profiles: Lahore, Karachi, Kathmandu, Dhaka, Jakarta, Chiang Mai.
4. Write the Tier-2 dossiers: Sri Lanka, Malaysia/Singapore (haze), Lao PDR, Myanmar, Bhutan.
5. Add an earnings-measurement design for vendors (G1), and test the journeys with real lay readers and a trustee.
6. Run a manual screen-reader test, and add Hindi summaries of the simple layer.
