# Phase 1 plan: research

Research cutoff: **22 November 2026**. This is desk research only: no contact with people or organisations, no fieldwork.
Briefs: `docs/research-brief.md` (method), `docs/site-brief.md` (wins on conflict), `docs/design-brief.md`.

## 1. Output layout (built so Phase 3 can generate the site from it)

```
research/
  README.md                         manifest, cutoff, method, file guide
  report/                           full report as section files with YAML front matter
    00-method.md                    scope, cutoff, sources, rating rules, limitations
    01-pollution-and-exposure.md    AQI vs concentration vs exposure; standards; monitoring gaps; source apportionment
    02-health.md                    established vs emerging; pregnancy & childhood
    03-livelihoods.md               the five economic pathways (A–E)
    04-communities-of-fate.md       group-by-group, with protective constraints
    05-places.md                    Delhi/NCR in depth + 4–6 contrasting settings
    06-consequence-pathways.md      link-level secondary/tertiary chains
    07-organisations.md             who does what, verified
    08-interventions-and-infrastructure.md
    09-portfolio-options.md         3–4 concepts, A–D classes, failure conditions
    10-learning-agenda.md
    11-synthesis.md                 answer to the brief's closing question; what not to fund
  decision-brief.md                 3–4 pages
  data/
    sources.csv                     source register (every source; URL, pub date, access date, access status)
    claims.csv                      claim-level evidence register: claim → source(s), page/section, evidence type
    settings.csv                    (C) geographic comparison
    community-impacts.csv           (D) community impact matrix
    organisations.csv               (E) organisation & programme map
    interventions.csv               (F) intervention & infrastructure matrix
    evidence-map.csv                two-dimension ratings with written rationale
    evidence-gaps.csv               (G) evidence-gap register
    economic-estimates.csv          every number: population|place|period|exposure|outcome|method|estimate|uncertainty|limitations
    pathways.csv                    each causal link: evidence, geography, timescale, alternatives, confidence, intervention point
    portfolios.csv                  (H) structured fields behind the portfolio pages
  analysis/                         scripts + notes for any calculation (I); reproducible, with inputs cited
  exports/                          assembled report .md and PDFs, filenames carry cutoff-2026-11-22
```

Conventions: sources are `S###` and claims are `C###`. Prose cites claim IDs inline (`[C042]`), and each claim
resolves to sources. Ratings use only Strong / Moderate / Limited/mixed / No adequate evidence found, each with
a written reason. The CSVs are the single source of truth: prose links to the tables and never restates a
rating that differs from them.

## 2. Sequence

| Step | Work | Main outputs |
|---|---|---|
| 0 | Scaffolding: folder tree, CSV headers, ID rules, `README.md` | empty schemas |
| 1 | **Foundations**: CPCB AQI method (incl. the Nov 2026 disclosure that PM readings >999 µg/m³ are excluded, and the methodology review); NAAQS vs WHO 2021; monitoring network coverage and gaps; Delhi source-apportionment studies compared by season, year and method; national burden estimates (GBD/ICMR, AQLI) with their assumptions; household air pollution | `01-…`, sources, claims |
| 2 | **Initial scan → setting selection.** Score candidates against the brief's seven categories for contrast, evidence availability and livelihood relevance. Likely shortlist to test: an IGP city/district (e.g. Kanpur, Lucknow or Patna), a mining/industrial belt (e.g. Singrauli, Dhanbad or Korba), a western/southern metro (Mumbai, Chennai or Bengaluru), a smaller under-monitored city, a rural household-energy and crop-residue setting, a brick-kiln or small-manufacturing cluster. Choose 5–7, Delhi/NCR included, and record why each was chosen or dropped | `settings.csv`, `05-…` |
| 3 | **Health**, labelled global / Indian / local and association / causal: respiratory, cardiovascular, mortality; pregnancy (exposure windows, birth weight, preterm birth); child lung development; school disruption; neurodevelopment with caution | `02-…`, evidence-map rows |
| 4 | **Livelihoods**, the central workstream: pathways A (illness), B (avoidance), C (control measures: GRAP stoppages, construction bans and worker compensation in practice, school closures), D (debt, savings, education), E (who pays for transition). Wages, piece rates, informal net earnings, unpaid care, small-enterprise margins. Every figure goes in `economic-estimates.csv` with measured / self-reported / modelled / hypothetical labels | `03-…`, `economic-estimates.csv` |
| 5 | **Communities of fate**: the 14 priority groups, plus work relationships (self-employed, wage, piece, unpaid family) and gender, caste, migration, tenure, age and disability where evidence supports them. Community organisation and knowledge, not only vulnerability | `04-…`, `community-impacts.csv` |
| 6 | **Consequence pathways**: link-level chains, sorted into health-, behaviour-, market- and policy-mediated, with double-counting checks | `06-…`, `pathways.csv` |
| 7 | **Organisations**: public bodies (CPCB, SPCBs, CAQM, municipal, health incl. NPCCHH), research (CSE, CEEW, TERI, IITs and others), worker and vendor organisations, community and women's organisations, NGOs, funders. Only activities verified from public documents, with advocacy / research / monitoring / delivery / financing / enforcement kept separate | `07-…`, `organisations.csv` |
| 8 | **Interventions and infrastructure**: four categories (emission-, exposure-, health-service-, information-reducing), each candidate run through the brief's 15 questions. Specific tests: filtration (CADR, occupancy, infiltration, gases), smog towers against independent evaluation, sensors (decision, actor, response budget), clean-air shelters (can users actually attend), mechanisation and kiln conversion (who bears the cost). Compared with non-infrastructure measures | `08-…`, `interventions.csv` |
| 9 | **Evidence map and gap register**: both dimensions, plus relevance, feasibility, equity, cost and maintenance | `evidence-map.csv`, `evidence-gaps.csv` |
| 10 | **Portfolio options**: 3–4 alternatives traced to findings, e.g. informal markets and vendors; schools, childcare and maternal care; industrial and kiln clusters with fair transition; income continuity and entitlement access during restrictions. These are hypotheses to test, not conclusions. A–D classes, place- vs population-based comparison, sourced cost ranges only | `09-…`, `portfolios.csv` |
| 11 | **Write-up**: report 7–10k words with progressive depth, decision brief 3–4 pages, learning agenda, synthesis incl. what not to fund. Run the brief's quality checklist and record the result in `00-method.md`. PDFs if a renderer works here | `decision-brief.md`, `exports/` |
| 12 | **Stop.** Summarise findings for review before Phase 2 | summary in chat |

Checkpoint commits after steps 1, 2, 5, 8 and 11 so work is never lost. The phase-complete commit follows step 11.

## 3. Source discipline

- Order of preference: official datasets and documents → primary studies and systematic reviews → evaluations →
  documented community research → organisational reports (outcome claims flagged) → journalism and testimony (labelled).
- Literature via PubMed / Europe PMC (both reachable), plus publisher pages where open.
- **Access status recorded per source**: `full-text-read`, `abstract-only`, `search-snippet-only`, `unreachable`.
  A claim backed only by a snippet is marked provisional and cannot carry a Strong rating.
- Sites blocked from this container (cpcb.nic.in timed out; thelancet.com and ceew.in return 403): try mirrors of the
  same official document, PMC copies, or the web-fetch route, and record which copy was read.
- Hindi sources where they add something (e.g. Delhi government GRAP and compensation notices, Hindi press on work stoppages).
- Nothing on the never-invent list is written without a source. A gap is recorded as a gap.

## 4. Known limits going in

- The 2026–27 winter season is under way at the cutoff, so "current conditions" will be partial. Seasonal and long-term
  figures will use complete earlier periods.
- Evidence on informal earnings, unpaid care, pregnancy in India, small-enterprise effects and long-term maintenance is
  expected to be thin. The output will show that, not fill it.
- Paywalls will limit some primary studies to abstracts. Those ratings will be capped accordingly.
