# Organisations 10× audit and gap diagnosis

Research cutoff: **22 November 2026** (unchanged) · Audited: `main` at the merge of PR #2 · Brief: `docs/organisations-10x-brief.md`

## 1. Existing records

The page `/organisations/index.html` is rendered by `site/build.py` → `section_page("organisations", "orgs.html")`
from `research/data/organisations.csv` (21 rows, 16 columns) plus report section 07. Two further registers feed
the Funding Atlas: `programmes.csv` (P01–P20) and `funders.csv` (21 rows, 6 of them "research queue").

| org_id | Type (current `sector`) | Sources (pub. date, type) | Reuse |
|---|---|---|---|
| cpcb | National regulator | S004 (2026-09), S005 (2026-11, news), S032 (2024-09) | Keep exactly |
| caqm | Statutory regional commission | S004, S035 (2025-12, news) | Keep |
| dpcc | State regulator | S041 (2023-09), S042 (2023-11), S010 (2016) | Keep; S010 is old but describes a still-cited study |
| bspcb | State regulator | S030 (2026-07), S031 (2021), S037 (2024-12) | Keep |
| delhi-bocw-board | Statutory welfare board | S016 (2026-11), S017 (2024-12), S019 (2025-12) — all news | Keep; flag "media reporting" |
| dusib | City agency | S052 (2026-11, news) | Keep |
| ncdc-npcchh | Health programme | S048 (2024-11, official letter) | Keep |
| moefcc-ncap | National programme | S004, S008, S011, S053 | Keep |
| world-bank | Multilateral lender | S051 (2025-12), S053 | Keep; link to funder profile |
| clean-air-fund | Philanthropic intermediary | S049, S050, S045, S054 | Keep; link to funder profile |
| mht | NGO | S049 (2024, funder account) | Keep; deepen |
| chintan | NGO | S045 (2023-06, community research) | Keep; deepen |
| hcwh | NGO network | S050 (2023, funder account) | Keep |
| cse | Research/advocacy NGO | S011, S014 | Keep |
| ceew | Think tank | S027, S043 | Keep |
| teri | Research institute | S009, S031, S036, S053 | Keep |
| iit-kanpur | Academic | S010, S030 | Keep |
| igc-kv-trial | Research team | S040 (2026-04) | Keep |
| anti-slavery | International NGO | S038 (c.2017) | Keep; label historical |
| wri-india | Research/implementation NGO | S037 (2024-12) | Keep |
| construction-unions | Worker organisations (grouped) | S016, S018 (news) | Keep as a grouped record; do not split into named unions without sources |

All 21 rows rest on full-text-read sources. Every row is India-only. No row has a profile page, a slug, a website,
a plain-language summary, a last-checked date or a link to the programmes in the Funding Atlas.

## 2. Types and geography (baseline)

| Category | Count | | Country | Count |
|---|---|---|---|---|
| Public bodies and programmes | 8 | | India | 21 |
| Research and think tanks | 6 | | All other countries | 0 |
| NGOs (incl. international) | 4 | | | |
| Funders and lenders | 2 | | | |
| Worker organisations | 1 (grouped) | | | |
| Private companies / social enterprises | 0 | | | |

The Funding Atlas already names regional implementers (Vital Strategies, GAIA, WALHI, IRRI, Clean Air Asia, NTU,
Chiang Mai University, Help Delhi Breathe) inside programme text, but none has an organisation record.

## 3. Shortcomings of the current page

- **Discoverability.** One 6-column table, ~11,500 px tall at 390 px width. A single "function" filter, no search.
- **Geography.** India only, although the Places and Funding sections now cover nine countries.
- **Project detail.** Activities are prose in a cell; no project records, dates or roles.
- **Funder relationships.** Funding lives in a separate atlas; no organisation → project → funder link.
- **Private sector.** Absent. No distinction between solution providers, operators and regulated emitters.
- **Community organisations.** One grouped union record and two NGOs; no waste-picker, vendor, women's or parents' groups as records.
- **Outcomes.** One "demonstrated outcomes" cell mixes activities, outputs and outcomes.
- **Accessibility/readability.** Table passes axe, but a lay reader meets "monitoring; enforcement; research" with no plain explanation; no per-organisation page to link to or cite.

## 4. Whose action is over-represented, and whose is less visible

Regulators, national programmes and research institutes make up 14 of 21 records. Their work is the best
documented because they publish. The work of delivery NGOs, worker collectives, waste-picker groups, parents'
networks, school and health actors, local enterprises and city operators is less visible — partly because they
publish less in English and partly because funders' own pages describe it second-hand. The atlas should correct
for visibility where sources allow, and say so where they do not. Absence from the directory is not evidence of
absence of action.

## 5. Extending the pipeline without a competing source of truth

- `organisations.csv` stays the one organisation register. Existing 16 columns are kept verbatim; new columns are
  appended (slug, category, countries, plain summary, website, system roles, business role, last checked, etc.).
  Existing `org_id`s are permanent; new ones follow the same lowercase-slug convention.
- `programmes.csv` (P01–P20) stays the register of financed programmes. A new `projects.csv` holds activities that
  are not financing records (J001+). Both are "projects" to the reader; neither duplicates the other.
- New `organisation-project-roles.csv` links organisations to `Pnn` or `Jnnn` with an exact role.
- New `funding-flows.csv` records funder → recipient → project links. Amounts for P01–P20 stay in `programmes.csv`
  only (the flow row points to it), so no amount is stored twice.
- `funders.csv` keeps its IDs; each funder gets a matching organisation record via a `funder_id` column, so
  `/organisations/funders/*.html` keep working.
- New `org-candidates.csv` logs every lead reviewed, including exclusions and reasons.
- All new facts become claims `C154+` and sources `S111+` through `research/analysis/reg.py`.

## 6. Claims: preserve, update, warn

- **Preserve exactly:** all 153 claims and 110 sources; all 21 organisation rows' existing cells.
- **Update (append, never overwrite):** new claims for the same organisations (e.g. MHT, Chintan, CSE) where newer primary pages exist.
- **Verification warning shown on profiles:** records resting on news reporting (delhi-bocw-board, dusib,
  construction-unions), on a funder's account (mht, hcwh), historical (anti-slavery), and the provisional claims
  C034, C056, C135, C138, C153.

## 7. Information architecture and plan

Chosen structure (fits the generator, adds no top-level nav item):

| URL | Purpose |
|---|---|
| `organisations/index.html` (kept) | "Who is working for cleaner air?" — data strip, three presets, searchable explorer, system view, stories, the original 21-row table preserved below as the dated baseline (anchors `#cpcb` etc. keep working) |
| `organisations/o/<slug>.html` | One generated profile per organisation, ten sections in the brief's order |
| `organisations/projects/` | Project register (P + J), filterable; each J project has its own page |
| `organisations/funding/` (kept) | Gains a "Follow the money" flow table from `funding-flows.csv` |
| `organisations/places/` | Country entry points with counts and an honest under-representation note |
| `organisations/gaps/` | Who is missing — coverage gaps from the candidate log, not from inference |
| `organisations/methods/` | Inclusion rules, source hierarchy, company diligence, corrections |
| `organisations/stories/<id>.html` | Ecosystem stories, generated from Markdown in `research/site-content/org-stories/` |
| `downloads/data/organisations-atlas.json` | Public export (no internal notes, no personal data) |

Research plan: Tier 1 countries first (India deepening, then Bangladesh, Nepal, Pakistan, Indonesia, Thailand,
Viet Nam, Philippines), then funders and private firms, then Tier 2/3. Each lead is fetched from its own site or a
primary record; anything not confirmed is logged in `org-candidates.csv` with the reason. Then model → write →
build → verify, as the brief's steps A–G. Proceeding without a separate approval, as the brief instructs.
