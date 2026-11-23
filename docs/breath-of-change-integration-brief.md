# CLAUDE CODE MASTER BRIEF
## Integrate *A Breath of Change* into the existing Clean Air website

**Project:** Clean Air — *Shared air. Unequal protection.*  
**Live site:** https://arunbh2.github.io/clean-air/index.html  
**Repository:** https://github.com/arunbh2/clean-air  
**Primary new source supplied by the owner:** `A Breath of Change.pdf` — *A Breath of Change: Solutions for Cleaner Air in the Indo-Gangetic Plains and Himalayan Foothills*, World Bank Group, 2025, edited by Martin Philipp Heger, Marion Cros and Ashley Pople. **Read the actual attached PDF in full.** The PDF has approximately 320 physical pages, with Roman-numbered overview pages and Arabic-numbered chapters.  
**Project evidence cutoff:** 22 November 2026, unless the repository owner has formally changed that date in `CLAUDE.md`.

---

## 0. Your assignment: implement a research-to-website upgrade, not a report summary

Act as a multidisciplinary team: senior South Asian air-quality researcher, systems thinker, environmental economist, community-health practitioner, philanthropic investment strategist, investigative editor, accessible-information designer and maintainable static-site engineer.

**The outcome is a materially more useful Clean Air website**, incorporating the report's evidence, sectoral solutions, implementation barriers, finance and governance insights and implications for vulnerable people. This is not an invitation to write an academic review page and stop. The insights must appear in the appropriate existing pages, associated datasets, interactive systems map, organisation and funding records, evidence registers, decision journeys and machine-readable copies. Add a concise source-specific reading guide if useful, but avoid a standalone report silo.

The upgrade must answer, for an ordinary person and a foundation trustee alike:

1. Where does the pollution I breathe actually come from, locally and regionally?
2. Why are its health, learning and livelihood effects unequal?
3. Which specific interventions reduce emissions, which protect people, and which merely enable action?
4. What prevents a technically sound solution from being adopted and maintained?
5. Who can do what — governments, community groups, NGOs, businesses, researchers and financial institutions?
6. What financing, infrastructure and cross-border cooperation are needed?
7. What is known, modelled, proposed, demonstrated or still unproven?
8. Which parts are suited to philanthropy, public finance, commercial capital or a deliberately blended approach?

**Do the work.** Inspect, extract, compare, verify, edit and test. Do not respond with a plan, a list of suggested pages or a report summary as your only deliverable. Do not fabricate research, results, permissions or implementation success.

---

## 1. Read and honour the existing site's rules before editing

Read these repository files if present, in this order:

- `CLAUDE.md`;
- `docs/site-brief.md`, `docs/research-brief.md`, `docs/design-brief.md`;
- `docs/clean-air-10x-expansion-brief.md` and any later owner-approved brief;
- `docs/three-audiences-governance-brief.md`, `docs/organisations-10x-brief.md`, `docs/systems-map-master-brief.md` if present;
- `docs/CURRENT_STATE_AUDIT.md` if present;
- all source registries, claim registries, intervention data, organisation data, funding records, site generators, map data, test scripts and CI workflows.

If a named brief does not exist, record that fact and proceed with the source of authority that exists; do not invent its contents. Inspect the actual build system before choosing implementation technologies.

### Non-negotiable preservation rules

- Extend the existing Clean Air website **in place**. Do not replatform or redesign its identity.
- Preserve working URLs, stable `Cnnn` claim IDs, `Snnn` source IDs, existing verdicts, existing dated India portfolio options and published historical records. Append or amend transparently with an audit trail. A new report may alter the synthesis **only through a documented evidence review**, not automatic replacement.
- Preserve the existing four evidence labels: `Strong`, `Moderate`, `Limited/mixed`, `No adequate evidence found`. Always explain the label in language, separately for (a) evidence that a problem or causal relationship exists and (b) evidence that an intervention changes outcomes.
- Preserve the distinction among emissions, ambient concentration, source apportionment, personal exposure, health outcomes, learning outcomes, household income and macroeconomic welfare/output costs. No silent conversions.
- Keep the Clean Air visual language: restrained editorial typography, paper-and-white surfaces, existing navy/ink/link tokens, sparse red accent, purpose-led visuals. Do not copy World Bank, Common Shade, Practical Action or Economist visual identities or proprietary artwork.
- Follow the repository's live editorial/agent-accessibility/CI rules. In public-facing copy, favour calm, non-accusatory description over prescriptive orders; avoid em dashes and decorative AI-generated design patterns. The public interface should be understandable on a low-end phone.
- Maintain the existing research cutoff. The World Bank book is from 2025, so it is eligible as of 22 November 2026. Use the report's *data reference years*, which may be earlier than 2025, rather than treating publication year as observation year.
- Do not imply that the World Bank, any report contributor, Practical Action, Tata Trusts, or any named organisation endorses Clean Air.

---

## 2. Read the entire 320-page PDF systematically, not just its executive summary

Before coding, make a structured **report evidence extraction workbook** in a repository-native, diffable format (CSV, JSON or Markdown; not an undocumented notebook). Use the PDF itself as the source of truth. Distinguish **physical PDF page number** from **printed book page number** and cite the latter in public reading notes, with a PDF page locator for maintainers.

For each substantial finding, intervention, number, institutional recommendation or example, capture:

- Report title, publisher, publication year; chapter/section; printed page(s) and PDF page(s); table/figure/box ID if applicable.
- Exact passage or adequately precise passage locator used to support the claim. Internal extraction may retain brief quotations for validation; published content paraphrases rather than copying large passages.
- Claim wording and kind: observation / attribution model / projection / economic estimate / case study / proposed measure / implementation hypothesis / evaluated outcome / legal or policy description.
- Geography and jurisdiction, population or sector, reference years and season, pollutant, units, averaging interval and denominators.
- Study method and original upstream reference where possible, plus assumptions and uncertainty.
- Evidence strength for the specific claim and whether the report is synthesising another study rather than providing primary evaluation.
- Existing Clean Air claim/source IDs that overlap; whether the report reinforces, narrows, contests or adds to them.
- Where in the site the insight should appear, the exact reader question it answers, and the right short layperson explanation.
- Whether further verification of an upstream study, government page, lender database or technical standard is needed.

Review the **complete chapters** below. The book's chapter numbering, not arbitrary web-search fragments, governs coverage:

| Report section | Research to extract | Website use |
|---|---|---|
| Executive summary and overview | 13-jurisdiction IGP-HF airshed, transboundary estimates, regional sectors, `35 by 35`, 4Is, intervention logic | Homepage, Places, regional explainer, systems map, decision pathways |
| Ch. 1 — Why air quality matters | Health, mortality, cognition, learning, economic impacts, inequalities and denominators | People, children, livelihoods, evidence and economic-estimate notes |
| Ch. 2 — Sources | Local vs neighbouring-jurisdiction vs cross-border shares; sector-specific source composition; secondary PM2.5; seasonal conditions | Source-attribution explorer, place profiles, map |
| Ch. 3 — Residential cooking | Fuel stacking, affordability, behaviour, women and girls, reliable supply, clean-fuel access, pay-as-you-go, results-based finance, delivery networks | What Works, rural households, NGOs, enterprise/finance pathways |
| Ch. 4 — Industry | Brick kiln technology, boilers, furnaces, power plants, performance monitoring, small-firm financing and trade-offs | Industrial-cluster profiles, interventions, private sector, systems map |
| Ch. 5 — Transport | Vehicle standards, fuels, inspection, scrappage, public transport, nonmotorised mobility, data | Urban interventions and equity conditions |
| Ch. 6 — Agriculture | Crop residue, nitrogen/fertilizer/ammonia, manure, machinery, farm economics and service models | Rural geographies, farmer livelihoods, secondary particles |
| Ch. 7 — Waste | Open burning, segregation/collection, construction-and-demolition waste, road dust, operating capacity | What Works, urban services, municipal infrastructure |
| Ch. 8 — Health | Primary/secondary prevention, health systems, public warnings, exposure reduction, frontline skills; Thailand examples | Health protection, community profiles, decision pathways |
| Ch. 9 — Education | Classroom air, filtration and ventilation, education, school policies, teacher training and clean-air skills | School and child protection; evidence comparison |
| Ch. 10 — Governance | Institutional mandates, nested planning, regulatory authority, vertical/horizontal coordination, implementation | Organisational responsibilities; 4Is and systems map |
| Ch. 11 — Market-based instruments | Price incentives, fiscal reform, emissions trading, Surat/Gujarat case, transferability and market limits | Funding atlas, funder pathways, industrial solutions |
| Ch. 12 — Regional collaboration | Regional airshed governance, shared measurement, five cooperation functions, practical cooperation and financing | Regional systems map, policy pathways and collaborations |
| Conclusion | Sequencing, cost-effectiveness, readiness, implementation, protection and 4Is | Funder decision synthesis and next-step logic |

Also examine the **report's actual data tables and diagrams**, not just extracted text, especially overview Figures 3 and 4, tables comparing clean-cooking conditions and kiln technologies, governance tables, the Gujarat ETS case study and the regional collaboration framework. If a figure is raster-only or text extraction is garbled, inspect the page image. Where values cannot be read confidently or are not in a machine-readable source, mark them unavailable rather than estimating bar heights by eye.

### Important reading cautions

1. The report's **“35 by 35”** is an aspirational regional/interim objective of annual average PM2.5 *below 35 µg/m³ by 2035*, not a guarantee, not a binding commitment by every jurisdiction, and not the WHO annual guideline of *5 µg/m³*. Explain this precisely, with reference to the Kathmandu Roadmap and Thimphu Outcome as described in the report.
2. The overview's **52% local contribution** is an *IGP-HF aggregate model-based estimate* in the report. It is not a universal 52% for Delhi, Bangladesh, Nepal or any particular season. The geographic-origins figure uses 2020–24 modelled averages; record per-jurisdiction source and timeframe.
3. The **sector shares** and **geographical-origin shares** answer different questions. Never collapse them into a single chart or add them together. Figure 4 shows the leading contributors to *population-weighted exposure* for specified jurisdictions; it is not automatically a complete 100% national emissions inventory.
4. The report's roughly **33% average household-cooking contribution** applies to the analysed region/model and is not a Delhi-specific figure. Do not replace Delhi's existing source-apportionment data with it.
5. The report's estimates of mortality, life-expectancy loss and economic damage are geographically and methodologically specific. Label them as *estimates*, name the year, method and denominator. Do not confuse annual welfare costs, GDP loss and direct income losses of individual street vendors.
6. A proposed or internationally successful intervention may have **no demonstrated local impact**, especially for school filtration, masks, worker protection and livelihoods. The site's existing evidence judgement remains until reviewed with the actual studies.
7. The book studies the Indo-Gangetic Plains and Himalayan Foothills. **Do not generalise its numerical findings to Southeast Asia.** An externally verified comparator can be mentioned with a separate citation and explicit transferability discussion.
8. Avoid stale present-tense claims. The report was published in 2025; any “currently”, “now”, “in progress” or “adopted” statement about programmes or policy must be anchored to its date and ideally verified to the project's cutoff.
9. The PDF is copyrighted by the World Bank. Cite and paraphrase. Do not upload the entire copyrighted book to the public website, reproduce its maps/illustrations/screenshots wholesale or relicense its images or third-party data under Clean Air's open licence. If republishing a figure requires rights not obtained, construct an original, clearly attributed graphic from permitted and verified data, or provide a link and description instead.

---

## 3. Create a gap-and-integration audit BEFORE altering content

Map the World Bank report against what Clean Air already publishes. Inspect at least:

- `https://arunbh2.github.io/clean-air/index.html`
- `/people/index.html`
- `/places/index.html` and the existing Delhi, Bihar, Mumbai, Singrauli, Punjab/Haryana, kiln-cluster profiles
- `/what-works/index.html` and individual intervention pages
- `/organisations/index.html` and its NGO/company/research/agency profiles
- `/organisations/funding/index.html`
- `/support/pathways/index.html` and dated decision options
- `/evidence/index.html`, `/evidence/` registers, consequence pathways, source register and the glossary
- the existing systems map, if implemented, rather than creating a competing map.

Make `docs/research/world-bank-breath-of-change-integration-audit.md` with a matrix:

`Finding | Report printed page | Existing claim/page | Agreement or tension | New source needed? | Content action | Data change | Interface change | Priority | Verification status`

Use four change classifications: **reinforce**, **refine**, **add**, **flag contradiction**. Explicitly identify what the report does *not* establish. Rank proposed website changes by user benefit and evidentiary readiness, **not** by organisations' or countries' supposed merits. Do not turn a thin source into a “missing programme” claim.

Examples of tensions requiring adjudication:

- The current website distinguishes evidence of pollution impacts from evidence that classroom air filters improve children's health. World Bank recommendations to improve classroom air do not automatically convert *limited/mixed health-outcome evidence* into `Strong`.
- The current website is cautious about one-off masks, anti-smog technologies and public clean-air shelters. Report proposals for protective equipment/clean-air centres may apply to different contexts, designs and outcome metrics. Keep both perspectives, explain when each might apply and identify whether actual exposure reductions were evaluated.
- The existing India funding options are date-stamped. Add the World Bank-derived system-enabler analysis alongside them; do not silently rewrite their original conclusion or imply that a proposed financing mechanism is an announced grant.

---

## 4. Make the following specific improvements to the website

### A. Homepage: a new, simple “Why cleaning the air is hard — and possible” explanation

Preserve the current lead **“Shared air. Unequal protection.”** Keep the homepage uncluttered. Add a short entry-point module with three plain statements, three links and one meaningful visual:

- **Air travels:** A city breathes pollution from local sources and wider regions.
- **People differ:** Exposure, health risk and ability to protect income are unequal.
- **Solutions need systems:** Cleaner technology helps only when finance, institutions, incentives and services make it usable over time.

Offer paths: `Follow the air`, `Explore what works`, `See what it takes to implement`. Include a short source-credit and prominent link to the report note; do not make the homepage a dashboard of numbers.

### B. Places: add an “Where our air comes from” explainer, with careful geographic attribution

Create an accessible page or section titled **“Where does the pollution in our air come from?”** explaining, in the following order:

1. A source emits a pollutant.
2. Pollution travels or forms secondarily in the atmosphere.
3. Wind, topography, temperature and season affect concentration.
4. People breathe different amounts at home, school, in transit and at work.
5. Governments control different parts of the airshed; no city's boundary contains the full problem.

Add two separate optional explorers based on the report:

**Explorer 1: “Where did this pollution originate?”** Local jurisdiction / other states or provinces / outside the country / natural or other (matching definitions in report overview Figure 3). Use the report's jurisdiction-specific modelled averages and years only after values are accurately extracted. Never imply a daily or live air-quality feed.

**Explorer 2: “Which activities contribute most here?”** Cooking, industry/power, transport, agriculture, waste, forest fires and other model categories as appropriate (report Figure 4 and Chapter 2). Label any chart of top four contributors as *selected leading sectors*; show missing/unassigned share honestly.

Connect these to existing India place profiles and a clearly dated regional IGP-HF introduction. Add Bangladesh, Nepal, Bhutan and Pakistan context only as far as the report supports. Keep Southeast Asian place data separate from the book's regional model.

Use tooltips that explain `air shed`, `PM2.5`, `emissions`, `secondary particles`, `source apportionment`, `modelled estimate`, `annual average`, and `personal exposure` in one sentence each. Every chart requires an accessible table, uncertainty notes, report page and data-method description.

### C. What Works: restructure understanding around THREE different intervention jobs

Retain the current intervention listings and evidence grades, but visibly categorise each intervention by its actual *job*:

**1. Reduce emissions at the source (abatement)**
- Clean cooking: transition from polluting fuels; fuel stacking; demand, affordability, reliable supply, appliance servicing and gendered time costs.
- Industry: brick-kiln upgrades, cleaner boilers/furnaces, effective industrial emissions controls, continuous emissions monitoring and suitable enterprise finance.
- Transport: cleaner fuels/standards, vehicle inspection and retirement, buses, walking, cycling and charging infrastructure.
- Agriculture: crop-residue services, appropriate machinery, fertilizer/ammonia management, manure practices and viable farm economics.
- Waste: reliable collection, prevention of open burning, separation, recycling, construction waste, road-dust management and operation/maintenance.

**2. Reduce exposure and harm while pollution persists (protection)**
- Schools and childcare: ventilation, filtration, fit-for-purpose monitoring, behaviour and school protocols, with separate labels for measured indoor concentrations, health, attendance and learning outcomes.
- Health systems: advisories, primary-care preparedness, frontline-worker training, surveillance and services for high-exposure groups.
- Outdoor and informal workers: practical exposure reduction, workplace protections, financial continuity during restrictions and accessible health care — identifying where these needs are from the *website's own research*, not claimed as a report-proven intervention.

**3. Help solutions spread and survive (enablers)**
- Better monitoring, accessible data and independent evaluation.
- Public procurement and regulatory capacity.
- Financing and incentives for households, farmers, MSMEs and municipalities.
- Coordinated airshed governance and public accountability.

Each intervention page should state, in a consistent compact format:

`What problem is this tackling?` → `How does it work?` → `What does the report say?` → `What has actually been measured?` → `Who benefits / who bears costs?` → `What makes it stick?` → `4Is prerequisites` → `Who can deliver/fund it?` → `What remains uncertain?` → `Sources`.

Attach report chapters, technologies and exact pages, but do not assign ratings based on authority alone. Display measurable end points separately: appliance sales, sustained usage, emission reductions, outdoor concentrations, indoor concentrations, personal exposure, health outcomes and livelihoods.

### D. Launch a coherent “The 4Is: Why good solutions do not automatically scale” guide

This is the report's most transferable insight. Add a public-facing **4Is implementation explainer** accessible from What Works, Funding, Organisations and the systems map:

| Prerequisite | Layperson question | Examples to investigate |
|---|---|---|
| **Information** | Do people and institutions know what is happening, and what works? | Reliable source measurement, emissions inventories, awareness, data sharing, evaluation |
| **Incentives** | Can people and businesses afford or justify changing? | Grants, taxes, credit, rebates, performance payments, transition support |
| **Institutions** | Who has the authority, staff, trust and duty to make it happen? | Local agencies, enforceable standards, worker groups, producer associations, coordinating bodies |
| **Infrastructure** | Does the equipment or service needed for change actually exist? | Power supply, charging, clean-fuel distribution, common boilers, collection systems, monitoring services |

Use **clean cooking** as a primary guided example: buying or subsidising a stove does not establish continued exclusive use if fuel refills, reliability, cultural preferences or service networks are barriers. Present these as report-described adoption barriers; confirm any programme-specific outcome before asserting it.

A second example should show a **small brick kiln or industrial boiler**: technical conversion requires upfront capital, technical services, monitoring, permits, viable operating economics and worker protections. Use the report's brick-kiln and boiler chapter/tables; do not infer kilns have achieved worker health improvements absent direct measurement.

Optional third example: **crop residue**. A no-burning rule does not by itself supply farmers with collection services, equipment, market demand, usable incentives and time to change harvest practices.

The 4Is are **implementation prerequisites, not a score or causal proof**. Avoid a simplistic radar chart or automatic “ready to invest” label. A reader can click each I to see the relevant blockers, actors, funding instruments and evidence.

### E. People and livelihoods: strengthen the protection story without losing the equity focus

Cross-reference the book's chapters on health, education, clean cooking and economic impacts with existing community profiles. Explain:

- Why a regional health/economic burden estimate cannot establish a specific street vendor's lost daily earnings.
- How exposure differs across locations and occupations and why unequal ability to avoid exposure compounds consequences.
- How school air quality may affect attention, attendance and longer-run opportunity, while separating association from causal evidence and distinguishing learner outcomes from merely lower measured indoor PM2.5.
- Why cleaner cooking involves women's time, affordability and household decision-making in addition to appliances and fuels.
- How poor households and MSMEs can face transition costs, and how implementation design can prevent costs simply shifting to them.

Add a short “Protecting people while we clean the air” journey from school to household to outdoor work to health clinic. The report offers policy options, but the website should keep each outcome's evidence strength visible.

### F. Organisations: move from names to sector roles, implementation capacity and delivery relationships

The existing directory already has NGOs, community groups, researchers, public bodies, companies and funders. Extend its metadata where verified:

- `sector_role`: source reduction / public health / education / financing / monitoring / research / technology supply / installation / maintenance / enforcement / convening / community organising.
- `implementation_4is`: which of Information / Incentives / Institutions / Infrastructure the organisation demonstrably contributes to.
- `project_or_programme`, operating location, time period, local partner, public mandate, actual activity, technology or service, and publicly disclosed result.
- `report_named?`: clearly distinguish names documented in the World Bank report from organisations identified by the website's independent research. A mention in the report does not establish an ongoing collaboration, funding link or endorsement.
- Evidence status: self-described activity / public record / independently evaluated outcome.

Use the report's concrete examples as **leads for verified records**: clean-cooking delivery models, technology suppliers, kiln/boiler upgrades, continuous emissions monitoring, school/health-system examples, public regulators and regional coordination institutions. Investigate any current claim separately, particularly company/project status.

Show the role of **private companies and social enterprises** honestly: equipment seller, financier, service provider, buyer/offtaker, employer, or independently assessed solution. Never confuse commercial presence with air-quality benefits.

### G. Funding and philanthropy: create an “What will it take to deliver this?” lens

Strengthen `/organisations/funding/` and `/support/pathways/` with a decision framework that separates:

1. **Public obligation and public finance:** regulation, enforcement, public-health systems, essential services and the regional coordination mandate.
2. **Philanthropic catalytic support:** pilots where learning is genuinely needed, independent measurement, rights/equity protection, local participation, convening, organisational capacity and evidence commons.
3. **Commercial capital:** productive equipment, creditworthy services, infrastructure where operating revenue exists, and scale finance under realistic risk conditions.
4. **Blended/concessional instruments:** guarantees, subsidised credit, results-based finance and technical assistance where documented market failures and additionality justify them.

For each intervention or pathway, create a **who pays for what and when** matrix:

`problem → actor who controls it → investable asset/service → 4Is prerequisites → capital type → who pays upfront → who covers ongoing costs → who benefits → implementation risk → evidence needed → credible scale pathway`.

Investigate the report's discussion of credit lines, taxes, incentives, results-based finance, private distributors, industrial conversion, emissions trading and regional cooperation financing. Record them as **proposed instruments or existing case studies** accurately. **Do not create funding entries for an idea that the World Bank recommends.** Add a funding record only for a named, dated, sourced approval/commitment/project, using the site's existing stages (announced, approved, disbursed, operating, evaluated, etc.).

A useful worked case is the **Gujarat/Surat particulate matter emissions trading system** (Chapter 11, Box 11.2). Explain what was tested, which industrial participants and public bodies were involved, why continuous monitoring mattered, what outcomes the evaluation measured, and what limits transfer to small informal enterprises or other sectors. Check primary evaluation before stating quantitative impacts or costs.

Do not treat every technology as philanthropic. Ask which institutional condition a grant can unlock, and which costs need a durable public or commercial payer.

### H. Systems map: convert the report into evidence-backed causal and implementation layers

If the Clean Air systems map exists, enhance it; if not, follow the approved `docs/systems-map-master-brief.md` when available. Do not build a disconnected report-specific visual.

Add or enrich nodes and links for:

- Five source systems: domestic solid fuels; industry/power/kilns; transport; agriculture and ammonia; open burning/municipal waste/dust.
- Atmospheric movement/secondary formation, seasons, topography and cross-border exchange.
- Exposure at schools, workplaces, homes and during journeys.
- Health, learning and work/income pathways, including uncertainty flags.
- The four 4Is enablers, plus capital and authority relationships.
- Governance across municipal, state/provincial, national and regional levels.

Make available four ways to explore:

**Follow the air:** from source → transport/formation → exposure → human consequence.  
**Find a break point:** select an intervention → highlight the specific edge it could change and what evidence supports it.  
**Why implementation fails or succeeds:** toggle Information, Incentives, Institutions or Infrastructure and inspect prerequisites as scenario *illustrations*, not numerical predictions.  
**Who can act / who pays:** overlay the organisations and capital instruments with verified roles and relationships.

**Do not invent feedback loops.** A directional causal chain is not a reinforcing loop unless the return path is explicit and evidenced or clearly labelled as a hypothesis. Where an edge is inferred rather than observed, display that distinction. Every edge must link to a claim and its source location.

### I. Regional collaboration: explain how neighbours can act on one shared airshed

Add an accessible “One airshed, many governments” explainer using Chapter 12. Capture the report's five cooperation functions in clear language, and show how they relate to local action: shared measurement, public/technical dialogue, cross-jurisdiction institutional coordination, aligning actual interventions and reliable financing. Confirm exact function labels from the chapter before publication.

Use country/jurisdiction boundaries respectfully. Do not suggest that one state alone is responsible for another's exposure or assign blame based on a model. Show both local responsibility and legitimate cross-boundary coordination. Separate the report's proposed future governance architecture from institutions already operating.

### J. Evidence, glossary and AI-accessible outputs

Register the report as a properly licensed **source**, not an automatically validated source for every cited upstream result. Add a clear “Read this report through Clean Air” page with:

- Five key insights in plain language.
- One graphic showing the distinction among abatement / protection / enablers.
- Report scope and limitations.
- A chapter-by-chapter reading map to relevant Clean Air pages.
- A list of findings that substantially strengthen existing evidence, and any that warrant review or conflict with earlier interpretations.
- An official bibliographic citation and publisher link where available.

Update the glossary for `airshed`, `source attribution`, `secondary PM2.5`, `ammonia precursor`, `fuel stacking`, `abatement`, `protection`, `4Is`, `results-based finance`, `emissions trading`, `MRV`, `cost-effectiveness` and `interim target`. Explain each in no more than two simple sentences before offering technical detail.

Update all relevant `.md` copies, `llms.txt`, data exports, search indexes, sitemap, accessible text alternatives and site feeds **from the same canonical data** as the HTML, following existing architecture and rights controls. Do not generate a contradictory second narrative solely for AI agents.

---

## 5. Exact content requirements for five flagship explanatory features

Build these only in ways supported by the source and existing framework; if a chart's input data cannot be extracted reliably, publish its text alternative first and mark the chart deferred.

### Feature 1 — “Where does the air come from?”

A short introduction, two distinct chart tabs (geographic origin versus emitting sector), jurisdiction selector where data exist, period/source line, actual percentages from verified tables, no guessed bars, accessible table, and an “What this does NOT tell us” note. If only modelled source data exist, label **Modelled, not measured personal exposure**.

### Feature 2 — “A cleaner stove is not the same as cleaner cooking”

A six-step sequence: purchase → fuel availability → affordability/refills → use alongside old fuels → sustained use → measured household exposure/health. Mark each step as a condition, measured outcome or research question. Include women's groups, entrepreneurs, service businesses, public subsidy and finance roles where supported. Cross-link to Ch. 3 and report figures/tables.

### Feature 3 — “Can schools protect children while the region cleans its air?”

Compare four separate questions: Is the building's indoor PM2.5 lower? Does personal exposure fall? Do health outcomes change? Do attendance/learning outcomes improve? Treat those as different end points. Connect evidence to school operators, education departments, health departments, filter maintenance, electricity, cost and evaluation design. Do not imply health gains merely from lower classroom particle concentration.

### Feature 4 — “Why one city cannot clean the entire airshed”

Explain the difference between local controls and regional coordination, with the report's labelled 2020–24 origin-of-pollution estimates. Show an implementation diagram: city action + state policy + national standards + regional evidence/cooperation. Do not overstate treaty status or legal commitments.

### Feature 5 — “Who pays to make clean air last?”

An interactive/text-first 4Is × intervention matrix showing who holds authority, which organisations do delivery work, what can be commercially financed, what philanthropy might unlock, and what ongoing public budget or customer payment is needed. Add a “What we know / What is proposed / What would need proof” sentence for each pathway.

---

## 6. Data architecture, verification and software standards

Respect the current repository's canonical research files. Prefer extending them to creating parallel databases. If the schema genuinely needs a new dataset, document the relationship and foreign keys. Proposed fields (map to existing equivalents rather than copying blindly):

```text
report_id | edition_year | chapter | section | printed_page | pdf_page
figure_or_table | original_reference | claim_id | source_id
geography | jurisdiction | period | season | population | pollutant
metric | unit | denominator | value | estimate_or_observation | method
claim_kind | evidence_problem | evidence_intervention | limitation
intervention_id | organisation_id | funding_id | systems_node_id
four_i_prerequisite | upstream_source_check | rights_status
published_copy_locations | review_status
```

For an intervention added from the report, require a structured card:

```text
id, name, sector, response_job, problem_claim_ids,
mechanism, target_communities, outcome_measured,
report_chapter_pages, primary_source_ids,
effect_on_emissions, effect_on_exposure, effect_on_health,
effect_on_learning, effect_on_income,
evidence_rating_problem, evidence_rating_effectiveness,
four_is, delivery_actors, cost_type, funding_type,
operational_requirements, limitations, transferability,
last_checked, update_reason
```

Never fill absent evidence with a zero. Use null plus a plain-language explanation. Keep modelled percentages, grant/loan approvals, disbursements, actual implementation and evaluated results in separate fields. Preserve stable original IDs; append new records according to the repository's ID policy. Validate citations, country names, periods and units, referential integrity, and no broken URLs.

### Required programmatic checks

Enhance the existing test pipeline with the smallest suitable set of checks:

1. Every newly published factual claim has a source and a precise report-page or external-passage locator.
2. Every report-derived figure includes geography, period, unit and method; no mixing of geographic-origin shares with emitting-sector shares.
3. `35 by 35` is always described as **aspirational/interim**, never equivalent to the WHO 5 µg/m³ annual guideline.
4. Approved loan/grant ≠ disbursed financing ≠ independently evaluated result.
5. “Proposed,” “projected,” “observed,” “measured,” and “reported by implementer” cannot silently turn into each other.
6. Every map edge has a valid claim ID, relation type and evidence descriptor.
7. Country totals do not silently mix incompatible years, denominators, periods, model versions or administrative areas.
8. HTML, Markdown copies, structured data exports and AI files use consistent factual records, caveats and corrections.
9. Rebuilt pages preserve stable deep links, accessible navigation, keyboard/touch input and complete no-JavaScript alternatives.
10. The build fails on orphaned records, broken internal navigation, out-of-range data, unresolved required fields and wrong content licensing.

Use real **negative tests**: deliberately inject an incorrect WHO target, a bogus funding outcome, an orphaned claim ID and a mismatched unit into test fixtures and demonstrate that appropriate checks fail. Then restore a clean build.

### User experience and performance

- Lead every new page with a short, concrete answer and a named evidence limit.
- Make technical detail progressively available rather than crowding the first screen.
- Do not add generic dashboards, scored country rankings, decorative gradients/glows, bloated chart libraries or auto-playing animations.
- Make charts and interactive elements usable on narrow phones, at 200% text zoom and without horizontal scrolling.
- Provide the same reasoning in HTML text/table form if interactive JavaScript fails.
- Reuse existing design components and design tokens; check contrast and avoid colour-only evidence indicators.
- Keep the generated site compatible with GitHub Pages and the existing deployment/CI workflow. Do not claim headers, API capabilities or server-side behaviour it cannot serve.
- Improve discoverability through contextual links, not duplicative top-level navigation. Add a top-level item only if the information architecture genuinely needs it.

---

## 7. Research quality: answer these specific analytical questions

As part of the internal `docs/research/...` analysis, do not only list solutions. Write short, sourced answers to:

1. Why have technology improvements not always resulted in sufficient reductions in ambient pollution, according to the report? What enabling conditions are missing?
2. How do sector priorities differ between Kathmandu, Greater Dhaka, Delhi, the Terai, Punjab and other included jurisdictions? Which differences are model-derived and which are observed?
3. Which policy options reduce emissions and which protect people from residual exposure? What conflicts exist between time horizons?
4. What does the report actually establish about private-sector roles, MSME finance, clean-cooking entrepreneurs and technology supply?
5. Which interventions can be delivered with known operating institutions, and which need new infrastructure, regulatory authority or market formation?
6. Where could city-only interventions underperform because much pollution originates outside city limits?
7. What equity risks arise from vehicle retirement, kiln conversion, crop-burning restrictions or industrial compliance, and what measures might protect affected workers or farmers? Distinguish report-derived statements from Clean Air's own synthesis.
8. Where does the report describe a plausible instrument but lack direct evidence of causal impact, sustainable operation or local transferability?
9. What are five **fundable learning questions** that a foundation could test without substituting grants for the public sector's continuing responsibilities?
10. Which ideas are new relative to the existing Clean Air website, and which are already well represented?

For each answer, cite report pages and any independent supporting source. If no direct evidence exists, say so.

---

## 8. Work order and minimum acceptance criteria

Execute in this order, committing changes in logical batches if the environment permits:

**Phase 1 — Source and audit.** Confirm that the PDF is accessible, inspect all chapters, tables and figures; create the extraction register, source and claim crosswalk, conflict matrix, rights check and current-page audit. Publish no unsupported factual copy.

**Phase 2 — Core explanatory upgrades.** Implement the homepage pathway; the geographic versus sector source explainer; the 4Is and clean-cooking example; and appropriate intervention/people/place cross-links. Ensure at least one complete path from report claim to user-facing record to source.

**Phase 3 — Implementation and finance.** Extend intervention pages, organisations, actor roles, financing pathways and systems-map overlays using verified linkages. Do not add unverified partnerships or programme outcomes.

**Phase 4 — Evidence infrastructure.** Integrate claim IDs, page citations, machine-readable outputs, glossary, corrections compatibility, navigation and structured downloads from canonical records.

**Phase 5 — QA and delivery.** Run the actual site generator, existing quality/voice/accessibility scripts, added integrity tests, local link checks and responsive checks. Confirm deployment readiness, but do not claim deployment if the environment cannot deploy.

### Three acceptance journeys

**A parent or teacher** starts at the homepage and can explain the difference among school filtration, cleaner nearby emissions and community health measures — without encountering technical jargon or confusing reduced indoor concentrations with proven learning gains.

**A street vendor or worker organiser** can follow pollution from a source to exposure and income/health consequences, understand what is known versus uncertain, and find actors responsible for prevention and protection.

**A foundation board member** can select clean cooking, kilns, schools or an airshed intervention, see 4Is prerequisites, responsible institutions, capital type, annual operating obligations, evidence of results and realistic next research questions — without mistaking a World Bank recommendation for a funded project.

**An AI assistant** can retrieve the same facts, caveats and source links from the site's machine-readable outputs and give a substantively consistent answer to any of those three questions.

### Final handover required from Claude Code

Return a concise implementation record containing:

1. What you read: chapter coverage and any unread/inaccessible portions of the PDF.
2. The most important **new** insights relative to the prior website, not just the report's executive summary.
3. A page-by-page **change log** with live/local URLs and files modified.
4. A count of new/updated claims, interventions, organisation relationships, and funding records **based on actual completed changes**, not targets.
5. The top evidence conflicts and decisions made to reconcile or disclose them.
6. Tests actually run, their outputs and any failures or limitations.
7. What is published, what remains an internal evidence candidate, and what needs permission or another source.
8. A short **“For funders: what changed in our understanding?”** synthesis of no more than 600 words, linking to the finished site.

**Completion standard:** The report changes how the reader understands the air-pollution system and how the funder evaluates delivery pathways. It does not merely increase article count. A credible Clean Air page should say: **what happens, why, for whom, what can change it, what makes that change feasible, who acts, who pays, and what remains uncertain.**

---

## 9. Start immediately

1. Locate and read the user-provided `A Breath of Change.pdf` in the Claude Code workspace. If not accessible, stop and say that the essential primary source is missing; do not substitute an internet summary.
2. Read the current `CLAUDE.md` and the available governing briefs.
3. Run a full current-state audit of the repo and build.
4. Extract and crosswalk the complete report.
5. Implement the highest-value, fully sourced upgrades, then the remaining verified upgrades.
6. Test, repair, and provide the concrete handover described above.

Do not request a redesign approval, create invented facts or stop after an outline. Make the work auditable by a human, maintainable by a developer and accurately usable by an AI agent.
