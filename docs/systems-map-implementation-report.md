# The web of dirty air: completion report

**Brief:** `docs/systems-map-master-brief.md` · **Date:** 23 November 2026 · **Research cutoff:** 22 November 2026 (unchanged)
**Branch:** `claude/focused-rubin-m4wcmo` · **Deployment:** not deployed; the live site changes when this branch is merged into `main` and CI passes.

## 1. Routes and files

**New public routes** (under `https://arunbh2.github.io/clean-air/`): `systems-map/` (interactive map), `systems-map/links.html` (every link as text), `systems-map/loops/` and 6 loop pages, `systems-map/levers/` and 25 lever pages, `systems-map/journeys/` and 5 journeys, `systems-map/method.html`, `systems-map/data/graph.json`, `nodes.csv`, `edges.csv`, `loops.json`, `levers.json`. Each page also has its Markdown mirror. No existing URL changed.

**New files:** `research/systems-map/` (systems, nodes, edges, cycles, levers, institutions, lever-roles, questions, ledger, 5 journeys), `research/site-content/systems-map.md`, `systems-map-method.md`, `site/build_map.py`, `site/static/js/systems-map.js`, 9 templates (`systems_*.html`, `_sm_edge.html`), `tools/check_systems_map.py` with `tools/fixtures/systems-map/`, `docs/SYSTEMS_MAP_AUDIT.md`, `docs/SYSTEMS_MAP_METHOD.md`, screenshots in `docs/screenshots/systems-map/`.
**Changed:** `site/build.py` (one hook), `base.html` (scripts block, footer link), `home.html` (gateway section), `people.html`, `works.html`, `evidence.html`, `orgs.html` (links), `site.css`, `build_agent.py` (`llms.txt`, `for-ai.json`), `for-ai.md`, `qa.js` (map tests; query-string links), `check_links.py` (query strings), `check_design.py` and `design-tokens.json` (map components; per-file JS budgets), `check_all.py`, `CLAUDE.md` (rule 8), `changelog.csv`.

## 2. What the map contains (computed from the data)

| Item | Count |
|---|---|
| Systems | 10 |
| Parts (nodes) | 40 |
| Connections (edges) | 52: 40 measured, 12 reasoned hypotheses |
| By evidence | Strong 10 · Moderate 20 · Limited/mixed 13 · No adequate evidence found 9 |
| Feedback loops | 6, each closed over existing edges; all rated "No adequate evidence found" as a whole (none studied end to end) |
| Levers | 25 (reusing the intervention assessments) across source reduction, exposure protection, healthcare, livelihood support, governance and financing |
| Institution categories | 15, with 90 role assignments (sets standard, pays, delivers, operates, evaluates, represents) |
| Guided journeys | 5 (street vendor, child at school, family cooking, kiln worker, city official), all labelled composites |
| Claims linked | 69 distinct claims |
| Research ledger | 17 candidates: 12 loops investigated (6 accepted as interpretive loops, 6 rejected or partly rejected) and 5 contested or queued edges |

## 3. Research added

- **New source:** S181 (Chowdhury et al. 2019, PNAS; abstract read via Europe PMC).
- **New claims:** C223 (weather traps pollution, S009), C224 (stoves create outdoor pollution, S074), C225 (airsheds cross boundaries, S075), C226 (household emissions and the national standard, S181). All four have a located supporting passage; C224 and C226 were reviewer-located and recorded in `passage-reviews.csv`.
- **Excluded for weak evidence:** transport-and-urban-form loop, waste-services loop, construction-compliance loop, black-carbon and climate loop, and protective-technology inequality as a loop (kept as a pathway); secondary particles by sector; cross-border transport as Delhi's dominant source (contradicted by C029). Earnings lost to illness, pollution-related debt, medical bills crowding out fuel, and compliance with emergency rules remain on the map as dotted hypotheses.

## 4. Navigation, accessibility and agent outputs

- Gateway section on the home page ("Explore the connections", "Start with one person's day"); links from People, What works, Organisations and Evidence; footer link on every page.
- Map features: simple view of key connections and "Show the whole web"; highlight a system or an affected group; select any box or arrow for its evidence; path finder (measured links only unless hypotheses are included; "No checked pathway found yet" when none); loop explorer; lever switch with the eight-part panel (problem link, action, who could act, documented organisations, funders, what to measure, what could go wrong, what is unproven); zoom buttons and a scrollable labelled viewport; Escape closes details; journeys one step at a time with Previous, Next and Show all.
- Line patterns, not colour, distinguish direct effects (thick), knock-on effects (thin), hypotheses (dotted) and the selected loop or path (dashed); evidence strength is always written in words.
- Without JavaScript the diagram shows the whole web and every box and arrow links to its text entry.
- Machine-readable: `graph.json` (schema version, dataset version, cutoff, rights status, counts, nodes, edges with claims and verification states, loops, levers with roles, organisations and funding, journeys, ledger), formula-safe CSVs, Markdown mirrors, a new section in `llms.txt`, and a pointer in `for-ai.json`.

## 5. Checks run

`python3 tools/check_all.py` (17 of 17 passed) and the browser suite `site/qa/qa.js` (35 of 35 passed):

| Check | Result |
|---|---|
| Systems-map validator (IDs, references, evidence rules, loop closure, lever ratings, wording, diagram/text/CSV/JSON equivalence, advertised counts, accessible names) | 0 errors |
| Validator self-test (bad edge, hypothesis rated Strong, unclosed loop, unknown lever, duplicate ID) | all 5 rule families fail as required |
| Voice, design, links, agent files, formats, CSV safety, propagation (existing) | all pass with the map included |
| Browser: node, loop, lever and path interactions with no script errors; keyboard opens a box; no outcome language in lever panels; whole web visible without JavaScript | pass |
| Browser: no sideways page scroll at 320 px on all 357 pages, and at 320, 375, 768 and 1280 px with text at 200% on 14 pages including the map, text view, a journey and a lever | pass |
| axe WCAG 2.1 and 2.2 A/AA on all 357 pages | 0 violations |
| Reduced motion, rendered text 12 px or larger, print, Markdown alternates | pass |

Page weight: the map page is 237 kB (budget 300 kB) because the graph data is embedded so it works offline and on slow connections; `systems-map.js` is 16 kB (budget 25 kB) and loads only on map pages. The home page is unchanged in weight apart from one short section (35 kB HTML).

**Not tested:** real low-end Android hardware and real screen readers (automated keyboard and axe checks only); a throttled-network timing test; pinch zoom on a physical touch screen (native scrolling and zoom buttons are used instead).

## 6. Named actors and funders

- **Verified:** 63 organisations appear on 11 levers, only through verified roles on activity records that list the lever's intervention. 15 levers show funding records or funding links from the atlas, with the stage in the source's own words.
- **Generic only:** institutional roles on every lever are functions by type (for example "Labour departments and welfare boards: pays"), not named endorsements.
- **Absent:** 14 levers have no verified activity record yet, and 10 have no funding record; their pages say so.

## 7. Unresolved

- Livelihood and household links are the weakest part of the map; 12 of 52 connections are unmeasured hypotheses.
- No loop has been tested end to end anywhere in the region.
- Geography filters for non-Indian settings are not offered, because few edges carry non-Indian evidence; each edge states its place instead.
- Suggested sources not yet added: HEI's DoSAAH database and UNEP's Asia-Pacific actions report.
- Licence for the graph data remains an owner decision (stated in `graph.json`).
- 18 claims in the wider register still await passage review; one of them (C037) supports edge E35, which is labelled accordingly.
