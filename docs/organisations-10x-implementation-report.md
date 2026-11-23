# Organisations 10×: implementation report

Edition: research cutoff **22 November 2026** (unchanged). Pages read 22–23 November 2026.
Branch: `claude/focused-rubin-m4wcmo`. Brief: `docs/organisations-10x-brief.md`. Audit: `docs/organisations-10x-audit.md`.

## 1. What changed and why

**Architecture.** The site is still a static Python generator that renders every page from `/research`. Nothing was hand-written in HTML, and no backend, API or runtime dependency was added. `organisations.csv` remains the single organisation register. Its 16 original columns and 21 original rows are kept verbatim, and 26 columns are appended. Projects that are not financing records live in a new `projects.csv`, so the Funding Atlas's `programmes.csv` (P01–P20) is never duplicated. Many-to-many roles and funding flows are separate tables. All new facts are new claims (C154–C222) and new sources (S111–S180), registered with the existing helper.

| File | Change |
|---|---|
| `research/analysis/add_org_atlas.py` | New. Reproducible registration of every source, claim, organisation, project, role, flow and candidate in this edition |
| `research/data/organisations.csv` | 21 → 95 rows; 26 columns appended (slug, category, countries, plain summary, system roles, business role, independent test, conflict note, last checked, record origin and others) |
| `research/data/projects.csv` | New. J001–J028 activity records, separating activities, outputs, measured outcomes and evaluation |
| `research/data/organisation-project-roles.csv` | New. 106 links, each with an exact role and a source |
| `research/data/funding-flows.csv` | New. 41 funder → recipient → project links |
| `research/data/org-candidates.csv` | New. 24 leads reviewed but not published, with the reason, plus coverage gaps |
| `research/data/programmes.csv` | P16 upgraded from a search snippet to the GEF project record (amount US$3,788,990 approved; co-financing kept separate) |
| `research/data/glossary.csv` | Five terms added: emissions, grant, loan, CSR, independent evaluation |
| `research/data/sources.csv`, `claims.csv` | Appended only |
| `research/site-content/org-atlas.md`, `org-methods.md`, `org-gaps.md`, `org-stories/*.md` (11) | New copy, every factual sentence cited |
| `research/analysis/validate.py` | New atlas gates (see section 7) |
| `site/build.py` | Atlas loaders and page generation; JSON export; glossary word-boundary bug fixed |
| `site/templates/` | `orgs.html` rewritten; new `org_profile`, `org_project`, `org_projects`, `org_story`, `org_places`, `org_gaps`, `org_compare`; `funding.html` gains "Follow the money" |
| `site/static/js/site.js`, `css/site.css` | Explorer (search, eight filters, three presets, show-more, live count, clear all); atlas styles; WCAG 2.2 target sizes |
| `site/qa/qa.js` | Atlas checks added; axe now also runs WCAG 2.2 AA rules |
| `CLAUDE.md` | Brief precedence row added |

**Routes.** All earlier URLs still work, including `organisations/index.html#cpcb` and the other first-edition anchors. The original table is kept, collapsed, on the hub, and opens automatically when an anchor targets it.

| New route | Content |
|---|---|
| `organisations/index.html` (rebuilt) | "Who is working for cleaner air?": data strip, three presets, explorer, system view, measurement-to-action, local voices, independent testing, public responsibility, stories, first-edition table |
| `organisations/o/<slug>.html` (95) | Profiles in the brief's ten-section order |
| `organisations/projects/` and `j001`–`j028.html` | Project register (J and P records) and activity pages |
| `organisations/stories/<id>.html` (11) | Ecosystem stories |
| `organisations/places/`, `gaps/`, `methods/`, `compare.html` | Country entry points, who is missing plus candidate log, methods, compare up to three |
| `downloads/data/organisations-atlas.json` | Public export with attribution note |

Pages: 140 → 279.

## 2. Counts

**Organisations.** There were 21 before, all in India. 98 leads were reviewed in total, of which 74 were published and 24 logged as excluded, grouped or a coverage gap. The directory now holds 95 published organisations.

| Category | All 95 | New 74 |
|---|---|---|
| Research and data organisations | 27 | 21 |
| NGOs | 23 | 20 |
| Companies, social enterprises, industry associations | 13 | 13 |
| Public bodies | 12 | 4 |
| Funders | 6 | 5 |
| Community, worker and parents' groups | 6 | 4 |
| Networks and coalitions | 4 | 4 |
| Multilateral and UN bodies | 4 | 3 |

Countries where organisations are documented working: India 45, Indonesia 12, Philippines 12, Bangladesh 9, Pakistan 9, Nepal 8, Thailand 5, Viet Nam 5, Malaysia 3, Bhutan 2, Sri Lanka 2, Maldives 1, Singapore 1. An organisation can count in several countries.

**Projects and money.**
- 28 new activity records, plus the 20 existing funding records: 48 in all.
- 106 organisation–project roles.
- 41 funding flows. 2 carry amounts: Coefficient Giving's US$1.5 million gift to the EPIC Air Quality Fund, and the GEF's US$3.79 million grant to UNIDO. The other 39 say "Amount not publicly disclosed".
- Flows by funder: Clean Air Fund 21, EPIC Air Quality Fund 13, USAID 2, Coefficient Giving 1, Shakti Foundation 1, DBS Foundation 1, GEF 1, Purpose 1.

**Independent evaluations.** 2 project records involve independent testing. CSTEP's Indi-SET evaluation of 48 devices from six manufacturers is read and reported. Airparif's microsensor challenges are known from a grant listing only; their results were not read. No project in the directory has an independent evaluation of air-quality, health or income outcomes.

**Below the brief's targets.** The brief aimed for 100–140 profiles, about 40 deep profiles, 100+ programme records, 25–40 community and NGO groups and 20–30 private actors. This edition publishes:
- 95 profiles;
- 48 project and funding records;
- 29 NGO and community records;
- 13 private-sector records.

Fewer were published because each one needed a primary source we could read, and several key sites block automated access. Nothing was added to reach a number.

## 3. How to trace a chain (examples)

1. **Funder → project → actor → place → outputs → gaps.**
   - [Coefficient Giving](../site/dist/organisations/o/coefficient-giving.html) → US$1.5 million → EPIC Air Quality Fund (FL001, C154).
   - → grant → Clean Up Nepal and Green Decision Labs (FL002, FL003).
   - → J001, 40 school sensors in Kathmandu (C185, organisation-reported outputs).
   - → "Measured outcomes: Measurement only".
   - → uncertainty: who maintains the sensors after the grant.
2. **Company versus foundation.** Nafas Indonesia (company, C204) and Nafas Foundation (non-profit initiative of the company, C205) have separate profiles that cross-reference each other. DBS Foundation's grant (FL017, C155) went to the company. The pneumonia white paper (J017, C207) is labelled as an association, not peer reviewed.
3. **Workers in Delhi.**
   - Clean Air Fund (FL015) → Mahila Housing Trust and Help Delhi Breathe (J013, C195, C156) → women AQI ambassadors in unrecognised settlements.
   - The public duty holder for compensation is the Delhi BOCW Welfare Board (P18, C040, C043).
   - Outcome: no adequate evidence found.
4. **Public finance.** GEF (FL020, C217) → UNIDO (implementer) and DTI (executing agency) → consortium (C218, press) → J023. Air quality is recorded as a co-benefit, not the objective.

## 4. Sources: completeness and staleness

- 70 new sources. All were read in full on 23 November 2026, and none was published after the cutoff.
- By type: organisational reports 53, journalism 11, evaluations 2, and one each of official dataset, official document, programme description and reference.
- Funder-reported is the commonest class among new organisations (29 of 74). Funders' own records establish that a grant was made, not results.
- By publication year: 2026 31, 2025 10, 2024 5, 2023 5, earlier 9, undated 10. Undated pages are marked "n.d." and dated by access.
- Historical labels: USAID-funded Viet Nam work (support after 2025 not established); ICCT, ICLEI, Pravah, Sesame and Swaniti grants (2021–2022 grant periods); the Nepal kiln manual (2015).
- **Blocked, not bypassed:**
  - Clean Air Asia site (403);
  - CCAC partner pages (403);
  - GreenHub (TLS failure);
  - HACCAP launch page (403);
  - UNDP Viet Nam (403).

  An attempt to fetch blocked pages with a browser user agent was refused by the session's safety controls and not repeated.
- Source and claim verification re-run: see section 7.

## 5. Unverified candidates and exclusions

The full list of 24 is in `research/data/org-candidates.csv` and on the "Who is missing?" page. The main ones:

- **Viet Nam:** GreenHub, Viet Nam Green Generation Network and GreenID.
- **Bangladesh:** BAPA.
- **Thailand:** EARTH and Greenpeace Thailand.
- **India:** Lung Care Foundation, named construction unions, waste-picker groups beyond Chintan, and A-PAG.
- **Philippines:** HACCAP.
- **Indi-SET's funders:** seen only in a snippet.
- **Coverage gaps:** Lao PDR, Myanmar, Timor-Leste, Singapore, Cambodia beyond P13, and community groups in Pakistan outside Lahore.

Bicara Udara is not described as a mothers' group because its pages do not say so.

## 6. Editorial maintenance protocol

1. **Add an organisation.**
   - Find a dated public source for a specific activity.
   - Register the source and a claim with `reg.S()` and `reg.C()`.
   - Append a row to `organisations.csv`. Use a new lowercase slug, one category, countries from `countries.csv`, a 20–30 word summary in plain verbs, and `source_class`.
   - Run `validate.py`, then the build.
2. **Add an activity.** Add a `Jnnn` row to `projects.csv`, keeping activities, outputs, outcomes and evaluation in their own columns. Add a role row for every organisation involved, then a flow row if money is documented.
3. **Correct a relationship.** Edit the role or flow row. Never delete a claim; add a correcting claim and note the change in the source's notes. Record the correction in `docs/RESEARCH_LOG.md`.
4. **Mark a programme ended.** Set `status` and `end_date` in `projects.csv`, and set `record_status` to "historical" on the organisation if nothing else is current. The validator rejects "operating" with a past end date.
5. **Verify a company claim.** Keep the company's own figure labelled "company-reported". Add an independent test only if one has been read, as a source of type `evaluation`, and name it in `independent_test`. The validator rejects promotional words in company records and an "independent" label without a named test.

## 7. Validation, tests and deployment

Results are in section 8, filled in after the final runs.
