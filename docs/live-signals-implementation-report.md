# Latest Signals: implementation report

**Brief:** `docs/live-signals-master-brief.md` · **Date:** 23 November 2026 · **Research edition:** 22 November 2026 (unchanged)
**Branch:** `claude/focused-rubin-m4wcmo`. Live only after merge to `main` and a passing deploy.

## 1. What works now

Paths are under `https://arunbh2.github.io/clean-air/` once deployed.

- `signals/index.html`: the last successful refresh in UTC, plus a "delayed" message that appears both when the site is built and in the browser. The "Recently discovered" lead is labelled as unselected. Search and filters cover view (News, Research, Reports, Policy and practice, Funding and partnerships), place (15 countries plus regional), topic and publisher type. The static list stays readable without JavaScript, and empty states describe coverage limits. The page also links to the monthly archive.
- Other pages:
  - `signals/archive/YYYY-MM.html`
  - `signals/recently-indexed.html`, which includes date-unknown records and date anomalies
  - `signals/awaiting-assessment.html`
  - `signals/missing.html`
  - `signals/sources.html`: the registry, last checks, untested candidates, coverage by place and blind spots
  - `signals/how-it-works.html`: rules, dates, the review pathway, rights, privacy and corrections
- Feeds and exports:
  - `signals/feed.xml` and five per-view Atom feeds
  - `downloads/data/signals.json` with its schema, and `signals.csv`, which is formula-escaped
  - The registry and the classification rules as downloads
  - Markdown mirrors of every signals page; `llms.txt`, the catalogue and `sitemap.json` list them
- Contextual lists. Each is labelled as discovery only and is not shown when empty:
  - Home page: 3 items
  - Intervention pages: related new publications
  - People group pages
  - Organisation profiles: publications by the organisation, and titles that name it
  - Funding page: announcements, not counted in any total. None in the current data.
  - Evidence hub: new sources awaiting assessment
  - Systems-map lever pages: related recent sources, with no new links and no ratings
- `feed.xml` still lists only site updates and corrections.

## 2. Sources

All enabled sources were tested on 23 November 2026, and every one returned HTTP 200 in the seeding run `run-20261123T114338Z`.

| Group | Sources |
|---|---|
| Research | Europe PMC (300 items fetched, 42 included), Crossref (100 fetched, 12 included) |
| Institutions | WHO news, HEI, State of Global Air, ADB, ICIMOD |
| NGOs and research | Clean Air Fund, UrbanEmissions |
| News | Mongabay India, Mongabay, Dialogue Earth, Eco-Business, The Hindu, The Daily Star, The Kathmandu Post, Dawn, The Straits Times, VnExpress, Bangkok Post |

15 sources were tested and not enabled; the reasons are in `docs/LIVE_SIGNALS_AUDIT.md` section 2:
- OpenAlex needs a key and a budget.
- The World Bank Documents and Projects APIs respond but are stale.
- ReliefWeb needs an approved application name.
- GDELT is rate-limited, and it is an aggregator.
- PIB, CPCB, CEEW, CCAC and The Third Pole are blocked or have no feed.
- CREA has a bot check.
- UNEP, Clean Air Asia and Down To Earth have no feed.
- arXiv is rate-limited.

## 3. Refresh mechanics

- **Schedule:** `.github/workflows/signals.yml` runs at cron `17 2,14 * * *` (02:17 and 14:17 UTC), and can also be started by hand.
- **Deploy:** the refresh commits `research/signals/` to `main`. `pages.yml` then rebuilds through `check_all.py --browser` on `workflow_run`.
- **Permissions:** the workflow uses `contents: write` and nothing else. The only optional secret is `OPENALEX_API_KEY`.
- **Where the times shown come from:** the last real successful refresh is the local seeding run, 23 Nov 2026 11:43 UTC. No GitHub-hosted run has happened yet, because the workflow exists only on this branch.
- **Failure handling:**
  - A failing source is isolated, and its records are kept.
  - If every source fails, the last successful refresh time stays as it was.
  - A schema violation stops the run without writing anything.
  - The page says "Feed refresh delayed" after 36 hours without a successful refresh.

## 4. Content quality (seeding run)

| Measure | Count |
|---|---|
| Fetched | 860 |
| Included | 68 |
| Excluded, each with a recorded reason | 792 |
| Records | 67 |
| Duplicates merged | 1 (same DOI from Europe PMC and Crossref) |
| Pending review | 67 |
| Manually reviewed | 0 |
| Promoted to evidence | 0 |

By type: 35 research papers, 18 preprints, 8 news reports, 5 reports and 1 policy item. Topic matching links 46 records to existing interventions as discovery pointers. No funding announcement passed the rules in this run.

## 5. Changes to existing site and data

- **Navigation:** a new "Latest signals" item.
- **Templates:** home, intervention, group, organisation profile, funding, evidence and systems-map lever.
- **Changelog:** E008.
- **Explanatory text:** `for-ai.md` now explains that signals are not evidence. `agent-access.md` and `CLAUDE.md` rule 10 add the narrow cutoff exception.
- **Deliberately not changed:**
  - claims, sources, ratings and verdicts
  - funding records and portfolio options
  - the systems-map graph
  - the meaning of `feed.xml`

## 6. Tests

`python3 tools/check_all.py` passes 24 of 24. The new steps are:

| Step | Result |
|---|---|
| Pipeline fixture tests | 72 passed |
| Store, registry and review validation | Passed |
| `check_signals.py` | Passed |
| Its self-test | All 6 fault families fired: data, feeds, parity, links, evidence, refresh |
| Base-URL relocation build | Passed |

The browser suite (`node site/qa/qa.js`) adds three checks: the list is readable without JavaScript, filters narrow and announce empty results, and the refresh stamp is dated. `python3 tools/check_all.py --browser` passed 25 of 25 across 373 pages, including axe WCAG 2.2 AA. One failure along the way was a short title link under the 24 px touch-target minimum, which was fixed.

**Known risks:**
- The scheduled push may be blocked by branch protection.
- GitHub may delay scheduled runs, or disable them in inactive repositories.
- Newsroom feeds list only their latest items.
- Matching is keyword-based. Precision was checked by reading every included title, but misses and stray topic tags remain.

## 7. Decisions for the owner

These are listed in `docs/LIVE_SIGNALS_AUDIT.md` section 4: automatic commits to `main`, the OpenAlex key and budget, permissions for blocked sources, named curators, local-language and paid sources, and whether reviewed signals feed a new dated evidence edition.
