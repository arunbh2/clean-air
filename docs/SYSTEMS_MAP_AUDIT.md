# Systems map audit and architecture

**Brief:** `docs/systems-map-master-brief.md` · **Date:** 23 November 2026 · **Research cutoff (unchanged):** 22 November 2026

## 1. What the repository already had (reused, not duplicated)

| Asset | Where | How the map uses it |
|---|---|---|
| Claim register (C001 to C222) with passage-level verification | `research/data/claims.csv`, `claim-passages.csv` | Every measured connection cites claims; the verification label travels with each claim into the map panel, text view and JSON. |
| Consequence pathways P1 to P5 | `research/data/pathways.csv` | Seeded the livelihood links (illness to debt, restrictions to unpaid wages, school closures, kiln transition). Their "no evidence found" steps became the map's reasoned hypotheses. |
| Community profiles (15 groups) | `community-impacts.csv` | Node population tags; "Highlight who is affected" filter; journey links to people pages. |
| Intervention assessments (25) | `interventions.csv` | Levers reuse intervention IDs; the effectiveness rating, reason, recommendation and costs come from here and nowhere else. |
| Organisations atlas, activity records, roles, funding links, funding records | `organisations.csv`, `projects.csv`, `organisation-project-roles.csv`, `funding-flows.csv`, `programmes.csv` | "Who is documented doing related work" and "who has funded related work" on each lever, through verified roles only. |
| Evidence gaps (G1 to G20) | `evidence-gaps.csv` | The "unproven" text on levers points to the matching gap. |
| Static generator, Jinja templates, design tokens, three-audience checks | `site/`, `tools/` | The map is generated at build time like every other page; mirrors, `llms.txt`, sitemaps and voice/design/link checks cover it automatically. |

Absent before this work: any graph data, loop records, lever-to-edge mapping, institution functions, journeys, or graph validator.

## 2. Evidence gaps found during the audit

| Gap | Action |
|---|---|
| No claim on weather trapping pollution | New claim C223 from an existing source (TERI-ARAI, S009), passage located. |
| No claim on household stoves feeding outdoor air | New source S181 (Chowdhury et al. 2019, PNAS) and claim C226; plus C224 from an existing World Bank source. Both passage-checked. |
| No claim defining an airshed | New claim C225 from an existing World Bank source (S075). |
| Earnings lost to illness, pollution-related debt, medical bills competing with fuel, compliance with emergency rules | No source found. Published as reasoned hypotheses rated "No adequate evidence found", with dotted lines. |
| Secondary particles by sector, health-service demand during episodes, learning loss from closures, caregiver income | Kept off the map or in the research queue (ledger X1 to X4). |

Sources the brief suggested (WHO guidelines, World Bank *Striving for Clean Air* and *A Breath of Change*, State of Global Air) were already in the source register; their relevant passages are cited through existing claims (C003, C125, C124, C145, C146). DoSAAH and the UNEP Asia-Pacific report were not added in this run.

## 3. Architecture decisions

| Decision | Choice | Why |
|---|---|---|
| Canonical store | CSV and Markdown in `research/systems-map/` | Same conventions as the rest of `research/`; no competing evidence store: edges cite claim IDs and never restate facts without a claim. |
| Rendering | SVG generated at build time by `site/build_map.py`, laid out in six layer columns | Works without JavaScript, prints a summary, needs no library or framework, accessible names on every box and arrow, small. Canvas was rejected (no native accessibility). |
| Interaction | `site/static/js/systems-map.js` (16 kB, no dependencies), loaded only on map pages | Homepage and other pages unaffected. Data embedded as JSON in the page (works from `file://` and on slow connections; no extra request). |
| Zoom and pan | Diagram keeps a readable minimum width inside a labelled, scrollable viewport; zoom buttons change its width | Native scrolling works on low-end phones and with keyboards; no scroll hijacking; page itself never scrolls sideways. |
| Text alternative | "Every link as text" page generated from the same records, plus Markdown mirror and JSON/CSV | Equivalence checked by `tools/check_systems_map.py`. |
| Path finding | Breadth-first search over published edges in the browser, up to three routes, measured links only unless the reader includes hypotheses | Labelled "a possible mapped pathway, not a causal proof or prediction"; "No checked pathway found yet" when none. |

## 4. Routes

`/systems-map/` (map), `/systems-map/links.html`, `/systems-map/loops/` (+6), `/systems-map/levers/` (+25), `/systems-map/journeys/` (+5), `/systems-map/method.html`, `/systems-map/data/{graph.json,nodes.csv,edges.csv,loops.json,levers.json}`. No existing URL changed.
