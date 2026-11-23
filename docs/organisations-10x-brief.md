# CLAUDE CODE MASTER PROMPT
## Clean Air — Transform the Organisations page into an evidence-led Asia Clean Air Ecosystem Atlas

**Target live page:** https://arunbh2.github.io/clean-air/organisations/index.html  
**Repository:** https://github.com/arunbh2/clean-air  
**Scope:** Primarily the Organisations page, its supporting data model, project/funding connections, and necessary linked sub-pages. Preserve the other Clean Air pages and their existing architecture.  
**Evidence cutoff:** 22 November 2026, as defined in the repository's `CLAUDE.md`. Do not advance the cutoff silently.  
**Execution mode:** Research, implement, validate, and document; do not stop at a plan.

---

## 0. Read this mandate before coding

You are an interdisciplinary team operating inside Claude Code: (1) air-quality researcher, (2) South and Southeast Asia civil-society ecosystem researcher, (3) philanthropic grants and development finance analyst, (4) private-sector/technology diligence analyst, (5) investigative data editor and evidence auditor, (6) information architect and plain-language editor, (7) front-end developer with strong accessibility expertise, and (8) quality-assurance tester.

The site is for anyone interested in who is acting on air pollution: a parent, schoolteacher, student, construction worker, street vendor, community organiser, local official, researcher, journalist, business leader or philanthropist. A sophisticated funder must be able to examine the data and sources, but the outward-facing writing must not read like a grant prospectus or fundraising site.

**Core proposition:** `Who is working for cleaner air, where, how, with whose money, for whom, and with what evidence of change?`

**Tenfold expansion is about intelligence and utility, not a tenfold increase in text.** A long directory of logos or names is not acceptable. The new page must expose verified organisations AND their actual projects, interventions, geographic footprint, communities served, partners, funders, outcomes, limitations and evidence gaps. It must make clear where private enterprises are providing solutions, where they are subject to compliance obligations, and where commercial claims remain untested.

The starting page currently presents 21 named organisation rows, chiefly Indian government agencies, researchers, funders and several NGOs. It already has valuable columns for verified activity, demonstrated outcomes, gaps and sources. Preserve those standards, expand their coverage and make the presentation far easier to explore.

**Non-negotiable:** Read `CLAUDE.md`, `docs/site-brief.md`, `docs/research-brief.md`, `docs/design-brief.md` and inspect the actual repository, data files, generation scripts, templates, navigation and deployment workflow before modifying anything. These are binding. `CLAUDE.md` defines evidence labelling, date cutoff, independent Clean Air brand, source traceability and generated pages. Do not use Practical Action branding or copy proprietary Economist assets. Preserve `/clean-air/` GitHub Pages base paths and working existing links.

---

## 1. First: audit the present page and data, then write a gap diagnosis

Inspect `organisations/index.html`, its site generator, the existing `organisations.csv` wherever it is stored, the source register, claim IDs and links to the evidence/what-works/places sections. Do not assume the directory data location: find it. Inspect mobile and desktop screenshots.

Create `docs/organisations-10x-audit.md` with:

1. All existing records, their IDs, source quality, source freshness, and what can be reused.
2. Existing organisation types and geographic coverage. Count by category and country.
3. Current page shortcomings: discoverability, filtering, geographic expansion, project detail, funder relationships, private sector, community organisation representation, verified outcomes, accessibility and readability.
4. A short diagnosis of **whose action is over-represented** (e.g., regulators/research) and **whose action is less visible** (e.g., workers, neighbourhood groups, delivery NGOs, school/community health organisations, local enterprises, infrastructure operators).
5. How to extend the site's current CSV/Markdown-to-HTML pipeline without creating a competing source of truth.
6. Which claims can be preserved exactly, which require updating and which need a verification warning.
7. Proposed information architecture and phased research plan, then PROCEED with implementation without asking for a separate approval.

Do not destroy existing content, claim IDs, or source identifiers. Migrate with backward-compatible mapping where needed. Existing URLs and links must continue to work.

---

## 2. Editorial ambition: explain the ecosystem as a system, not a phonebook

Design around six lay-reader questions:

1. **Who is doing something?** Local groups, NGOs, worker collectives, researchers, regulators, funders, businesses and others.
2. **What are they actually doing?** Installing and maintaining equipment; changing a policy; measuring pollution; organising workers; protecting children; financing a project; changing fuel or technology.
3. **Where, and for whom?** Country, city, airshed, workplace, neighbourhood and the people affected.
4. **Who pays, builds, operates and maintains it?** A grant, a loan, public budget, private investment or user payments; one-off capital vs continuing service costs.
5. **What changed?** Separate activity, output, independently measured environmental/health/livelihood outcome and longer-term impact. Do not confuse them.
6. **What remains unknown?** Unmeasured effectiveness, unclear cost, no local partners, unverified self-report, no evaluation or no long-term funding.

The page must show air pollution as a system of **emissions → exposure → health and livelihood consequences → policy and service responses → funding and accountability**. Organisations play different roles in different parts of the system. Not all actions clean the air directly, and not all clean-air projects protect those with greatest exposure.

Use the strapline `Shared air. Unequal protection.` and preserve Clean Air's independent, measured editorial voice.

---

## 3. Research scope: India anchor, South Asia, Southeast Asia

The organisations page is allowed to be more regionally expansive than the currently India-anchored analytical pages. Explain the geographic expansion accurately without silently rewriting claims in the rest of the site.

**Tier 1 — deep research:** India, Bangladesh, Nepal, Pakistan, Indonesia, Thailand, Vietnam and the Philippines. Seek substantial NGO, government, science, philanthropic and private-sector coverage in each, while allowing genuine unevenness when evidence is thin.

**Tier 2 — targeted research:** Sri Lanka, Bhutan, Cambodia, Malaysia, Singapore and Laos.

**Tier 3 — carefully selected cross-border and emergent cases:** Myanmar, Timor-Leste and Maldives, plus regional airshed and haze initiatives where credible public documentation exists. Do not force entries where public verification is impossible.

Look at rural and peri-urban settings, not only Delhi/Dhaka/Kathmandu/Lahore/Jakarta/Bangkok/Hanoi/Manila. Include the Indo-Gangetic Plain and Himalayan Foothills airshed, forest/peat haze crossing Southeast Asian borders, brick kiln clusters, transport corridors, agricultural burning landscapes, industrial centres and neglected smaller towns.

**Research targets (quality-gated, not artificial quotas):** Build a research candidate register of ~160–250 organisations; publish a first genuinely verified set aiming for at least 100–140 non-duplicated profiles (including retained records), with about 40 thoroughly researched deep profiles, 100+ verified programme/activity records and substantial NGO and private-sector presence. If verification cannot support these numbers, publish fewer and state the gap. Never invent to hit a numerical target. For depth, aim for roughly 25–40 grassroots/NGO/worker/community organisations, 20–30 private-sector or social-enterprise actors, 15–25 research or network actors, and an appropriate number of verified funders and public institutions; multi-role classification is allowed. Prioritise diverse local actors over a directory dominated by international institutions.

**Organisational types (multiple roles permitted, one clear primary type):**
- Community-based organisations; residents' and parents' associations; informal-worker and trade unions; women's groups; youth/citizen-science networks.
- National/local NGOs, international NGOs, health and environmental justice networks.
- Academic, scientific, independent policy institutes and media/data initiatives.
- Municipal/local governments; environmental regulators; public health; school/transport/waste authorities; national policy bodies.
- Philanthropic foundations, regranters, pooled funds and grantmaking intermediaries.
- Multilateral/bilateral lenders and development agencies; UN/ASEAN/regional institutions.
- For-profit companies: monitoring and data, industrial/brick kiln pollution control, cleaner transport, alternative fuels/cooking, waste-management systems, building ventilation/filtration, environmental services, and relevant infrastructure operators.
- Social enterprises and hybrid NGO/business initiatives, with legal structures clearly distinguished.
- Business coalitions and industry associations, with careful attention to claimed commitments versus delivered change.

**Functions (multi-select):** evidence and monitoring; research and evaluation; health protection; community mobilisation; worker protection; advocacy and litigation; policy-making; enforcement; technical assistance; financing and grantmaking; manufacturing; technology supply; installation; operations and maintenance; service delivery; skills; procurement; infrastructure development; air pollution source reduction; exposure reduction; public communication; independent accountability.

**Intervention domains:** ambient monitoring, personal/occupational exposure monitoring, source apportionment, clean cooking/household fuels, clean heating, transport/freight/e-mobility, industrial emissions, brick kilns, crop residue and agriculture, waste/open burning, forest/peat haze, construction dust, outdoor workers, schools and childcare, health facilities, respiratory care, community shelters/clean-air rooms, data systems, rights and legal enforcement, welfare/compensation and income protection.

For mixed climate/air projects, record **air quality as primary objective, explicit co-benefit or unverified possible co-benefit**. Do not automatically count renewable energy, EVs, recycling or general climate work as proven clean-air interventions.

---

## 4. Named research leads, NOT pre-approved directory entries

Use the following as candidate starting points. Before publishing, verify each entity's current status, relevant programme, date, geography, legal type and specific role using source material. An organisation being on this list means *research it*, not *publish a claim about it*.

### India — preserve and deepen current entries

Mahila Housing Trust; Help Delhi Breathe; Chintan Environmental Research and Action Group; Centre for Science and Environment; Council on Energy, Environment and Water; TERI; WRI India; CSTEP and its Indi-SET sensor evaluation facility; IIT Kanpur and other institutes with relevant projects; Health Care Without Harm and hospital networks; Clean Air Fund India grants; local construction-worker unions; waste-picker groups and informal-worker networks; local and state pollution-control bodies; municipal and school-sector agencies; programme delivery NGOs involved in the National Clean Air Programme. Explore A-PAG, Respirer Living Sciences and other leads **only after verifying** their specific activities.

### Bangladesh

Bangladesh Environmental Lawyers Association (BELA), Bangladesh Poribesh Andolon (BAPA), locally rooted civil-society and worker/health groups with identifiable air pollution activities; the Department of Environment; local air quality/brick kiln/transport research groups; Bangladesh Clean Air Project implementing agencies; universities, hospitals and independent researchers. A broad environmental remit does not automatically qualify as a clean-air programme. Verify brick kiln work, legal actions, monitoring, worker exposure and community delivery individually.

### Nepal

Clean Energy Nepal and its Swachh Hawa Pariyojana; Clean Up Nepal; Green Decision Labs and Research; the EPIC Air Quality Fund-supported school monitoring initiative; relevant school and children's health groups; local authorities and monitoring networks; ICIMOD where specific air quality or black-carbon work is verified. Explicitly distinguish measurement in schools from demonstrated reductions in children's exposure or illness.

### Pakistan

Pakistan Air Quality Initiative (PAQI), relevant air-quality research programmes, local health and environmental justice NGOs, city/air-shed institutions and verified Punjab Clean Air Program implementation partners. Look for worker/community groups outside Lahore. Do not assume a public data provider is a grantmaking NGO or intervention implementer.

### Indonesia

Bicara Udara (Yayasan Udara Anak Bangsa); Nafas Indonesia (commercial technology company); Nafas Foundation (separate nonprofit initiative); relevant Greenpeace Indonesia campaigns; haze/peatland and environmental justice groups; air quality researchers; Jakarta city authorities; companies changing operational emissions. Verify each brand's legal relationship, funding and monitoring reach; do not merge Nafas Foundation with the commercial company. Include independent evaluation where available.

### Thailand

Thailand Clean Air Network; relevant Chiang Mai/Northern Thailand haze civil-society groups; Greenpeace Thailand; Ecological Alert and Recovery – Thailand (EARTH) where programme-specific evidence exists; air quality/health research centres; verified citizen-led policy initiatives, local government measures and private mitigation firms. Separate advocacy for a clean-air law from evidence that enforcement or emissions reductions have occurred.

### Vietnam

Live & Learn (Center for Living and Learning for Environment and Community); GreenHub; Viet Nam Green Generation Network; GreenID (verify current clean air activities); local governments and health/research institutions; Clean Air–Green City programme participants; relevant cleaner-production or clean transport service providers. Distinguish project dates and donor history from current funding.

### Philippines

Clean Air Asia (regional NGO headquartered in Manila); relevant clean transport and air quality initiatives; De La Salle University; Electric Vehicle Association of the Philippines; Urban Electric Mobility Initiative; GEF/UNEP/UNIDO and government execution roles in the e-mobility ASAP programme; Health Care Without Harm Southeast Asia where verified; local community groups; anti-open-burning/coal pollution groups. List each actor's precise role, not simply all as project ‘implementers’.

### Other countries and regional ecosystem

Sri Lanka, Bhutan, Cambodia, Malaysia, Singapore, Laos, Myanmar, Timor-Leste and Maldives: identify verified local NGOs, researchers, policy bodies, public and private operators, especially those tackling household air, transport, pollution monitoring, industrial emissions and transboundary haze. Check Clean Air Asia country networks, ASEAN haze mechanisms, WHO and UNEP country work, CCAC member/project registries and funded research. Where the evidence is weak, produce a transparent coverage-gap record rather than a made-up organisation profile.

### Philanthropy, development finance and intermediation

Clean Air Fund (use its public **grant database**); EPIC Air Quality Fund; Bloomberg Philanthropies and relevant clean-air programme platforms; Climate and Clean Air Coalition (CCAC); World Bank; Asian Development Bank; GEF; UNEP; UNIDO; UNDP; relevant bilateral development partners; DBS Foundation (verify its named Indonesian sensor partnership); and relevant local philanthropic foundations or pooled funds. Carefully distinguish a philanthropic funder, lender, intermediary, implementing organisation, technology supplier and grant recipient. Explore relevant grants to NGOs and research teams, not just funding announcements by large institutions.

### Private sector — deliberate diligence, not a vendor showcase

Research Airveda, Aurassure, Oizom, Respirer Living Sciences, Nafas Indonesia, Airly and other firms only where current clean-air-related products/projects and operating geography can be verified. Include meaningful clean transport, kiln/industrial retrofit, cleaner production, school/clinic building, waste services and fuel-switch enterprises wherever supported. Seek independent assessments (e.g., CSTEP's Indi-SET sensor testing) and procurement/contract/implementation evidence. **Do not equate being shortlisted for procurement, selling sensors, raising venture capital, obtaining certification, or making a marketing claim with verified pollution reduction or improved health.**

Consider **three different business roles:** (A) provider of a solution, (B) infrastructure owner/operator or employer implementing cleaner practices, (C) regulated emitter/supply-chain actor facing accountability. A firm can play more than one role, but mark possible conflicts of interest.

---

## 5. Source discovery and evidence hierarchy

Search English and local-language materials where practical (Hindi, Bangla, Nepali, Urdu, Bahasa Indonesia, Thai, Vietnamese, Filipino and relevant others), retaining original titles and accessible English explanations. Use official organisational sites for identity and project claims; seek independent evidence for evaluation and outcome claims. Cross-check dates and distinguish an expired project page from a continuing programme.

**Priority source classes:**
1. Government budget/implementation/monitoring records and environmental regulator publications.
2. Official funder grant records, agreements, evaluation reports, procurement awards, donor databases and project documents.
3. Peer-reviewed studies, accredited sensor tests, independent evaluations and reputable research institutes.
4. Primary NGO annual reports/project documents, publicly disclosed programme data and activity reports.
5. Company disclosures and certified testing documentation, clearly labelled company-reported when not independently checked.
6. Credible investigative journalism for leads, scrutiny and disputes; triangulate major claims.
7. Network and conference lists for discovering candidates ONLY, not sufficient proof of specific ongoing projects.

Essential research starting URLs (links are discovery sources; verify all facts and dates against them):
- https://www.cleanairfund.org/what-we-do/our-grants/
- https://www.cleanairfund.org/resource/air-quality-funding-2026/
- https://www.cleanairfund.org/resource/philanthropic-foundation-funding-2026/
- https://www.cleanairfund.org/resource/clean-air-platform-southeast-asia/
- https://www.cleanairasia.org/projects
- https://www.cleanairasia.org/what-we-do
- https://www.cleanairasia.org/who-we-are/country-networks
- https://www.worldbank.org/en/brief/2025/12/09/air-quality-management-in-the-indo-gangetic-plains-and-himalayan-foothills
- https://www.ccacoalition.org/
- https://aqfund.epic.uchicago.edu/
- https://cen.org.np/clean-air-and-urban-mobility/swachh-hawa-pariyojana.html
- https://www.cleanupnepal.org.np/epic
- https://pakairquality.com/
- https://bicaraudara.id/
- https://nafas.co.id/about
- https://nafas.foundation/
- https://thailandcan.net/en/about-us
- https://www.greenhub.org.vn/cagc-en
- https://www.cleanairasia.org/projects/e-mobility-asap
- https://indiset.cstep.in/
- https://cstep.in/publication/performance-evaluation-of-multi-pollutant-air-quality-sensors-at-indi-set-bengaluru-india/

**Evidence cutoff discipline:** The repository cutoff is 22 November 2026. If a source was published after that date, exclude its claims until a separately authorised cutoff update. Archive source publication/access dates. Do not claim that information is current after the cutoff; distinguish 'current at cutoff', 'historical', 'announced/approved', 'ended', 'unknown'.

Maintain a **source verification log** for every lead reviewed, including excluded candidates and why they were excluded. No unverifiable exact fund totals, numbers served, partnerships, certifications, programme success, commercial performance or dates. No inferred relationships from name proximity or co-attendance at an event.

---

## 6. Data architecture: turn names into a verifiable ecosystem map

Keep existing records and stable IDs. Extend the current source-of-truth files under `/research`, following the repository's actual conventions. Use CSV/Markdown or JSON **only where consistent with the existing generator**. A candidate structure (adapt naming to existing files):

**A. `organisations.csv`: one organisation per row**

`organisation_id`, `canonical_name`, `short_name`, `name_in_local_language`, `organisation_type`, `legal_form`, `profit_status`, `headquarters_country`, `countries_active`, `regions_cities_airsheds`, `functions`, `themes`, `communities`, `plain_english_summary`, `why_it_matters`, `public_website`, `public_contact_url`, `verified_status`, `activity_period`, `last_public_activity_date`, `date_last_checked`, `evidence_category`, `verification_notes`, `source_ids`, `profile_slug`.

**B. `projects.csv`: one programme/initiative per row**

`project_id`, `title`, `short_plain_language_description`, `intervention_id`, `problem_or_pollutant`, `country`, `specific_location`, `airshed`, `start_date`, `end_date`, `status`, `target_groups`, `intended_change`, `activities`, `outputs_reported`, `outcomes_measured`, `outcome_measure`, `baseline`, `counterfactual_or_comparator`, `evaluation_type`, `unintended_effects`, `cost_amount`, `cost_currency`, `cost_type`, `continuing_cost_owner`, `funding_visibility`, `limitations`, `source_ids`.

**C. `organisation_project_roles.csv`: many-to-many relationship**

`organisation_id`, `project_id`, `role` (grantmaker / co-funder / borrower / implementer / delivery partner / technical partner / supplier / evaluator / regulator / public duty holder / operator / network member), `role_description`, `source_ids`, `verification_status`.

**D. `funding_flows.csv`: evidence-based project-level capital**

`flow_id`, `funder_organisation_id`, `recipient_organisation_id` (if verified), `project_id`, `funding_instrument` (grant/loan/equity/guarantee/public-budget/CSR/in-kind/unknown), `amount`, `original_currency`, `commitment_or_disbursement`, `approval_year`, `financing_dates`, `conditions_or_restrictions`, `public_source_ids`, `confidence_note`.

**E. `claims` and `sources`**

Extend the existing source register and claim ID structure; preserve existing IDs. Each displayed number, date, partnership, result, grant or technological-performance claim must link to its source, with publication date, last checked date, page or section, document type and accessibility notes. Keep an `excluded_or_unverified_candidates.csv` and a `research_log.md` to prevent invented completeness.

**Mandatory distinction:** An *organisation* is not a *project*. A *funder* is not necessarily an *implementer*. A *technology's tested measurement accuracy* is not evidence of *reduced emissions*. A *policy enacted* is not proof of *policy enforced*. A *programme announced* is not a *programme delivered*; a *trained participant* is not an *avoided illness*.

No identifying personal contact information beyond public organisational contact pages. Do not scrape and publish individual emails/phone numbers. No outreach, requests for quotes or implied endorsement.

---

## 7. Build an outstanding reader experience, not a giant table

Keep the page location `/organisations/index.html` and its place in main navigation. Reuse the site's existing global typography, tokens, logo, header/footer and source conventions.

### Above the fold

**H1:** `Who is working for cleaner air?`

**Deck:** `Explore the people and organisations measuring pollution, protecting communities, changing how cities and industries operate, and funding cleaner air across Asia.`

**Trust note:** `Only publicly documented activities are shown. Inclusion does not imply endorsement. Projects and results are labelled according to the evidence available. Research cutoff: 22 November 2026.`

A modest dynamic data strip (calculate only from verified records): `Organisations documented · Countries covered · Programmes traced · Funding links verified`. Do not use vanity counters or claim completeness.

**Three prominent visitor paths** (one-click functional presets, not separate fake search buttons):
- `See groups working with communities`
- `Explore solutions and businesses`
- `Follow funding to projects`

### Main section: Searchable ecosystem explorer

Implement a fast, accessible, responsive search and filters for country, city/airshed, organisation type, sector/intervention, function, target community, funding status, project status and evidence category. Add clear-all; show active filters, result counts and meaningful no-results states. Search aliases and local names; indexing must be based on source-of-truth data, not manual HTML.

Use an appropriate data-driven interface: concise entry cards or a clean compact list with short descriptions on mobile; optional accessible table on desktop. Do not render 100+ full-width dense tables or giant walls of cards. Provide lazy/chunked rendering or pagination for performance. Avoid drop-downs that are complex on phones.

Each organisation result includes:
- Name, verified category and countries/places.
- **What they actually do:** one concrete 20–30 word plain-language explanation grounded in a named programme.
- Role tags: e.g., `Community organising`, `Air monitoring`, `Transport transition`, `Funding`, `Health`, `Policy`.
- Communities or settings served where established.
- `View verified work` leading to its profile; source links on detailed views.
- A small, unambiguous evidence/status note, not a visual “trust score”.

### The organisation profile template

Use descriptive URL slugs; do not hand-code independent layouts. Proposed sections in this order:

1. **In one sentence:** what this organisation contributes to the clean-air field.
2. **At a glance:** type; home base; actual work geography; public website; active/historical status; evidence cutoff; language (optional).
3. **What it does in practice:** named, dated, sourced activities with a one-sentence explanation of who is involved.
4. **Who is meant to benefit:** communities, workers, students, neighbourhoods or institutions, with inclusion/access caveats.
5. **Projects in context:** project cards with role and dates; link to full verified project dossier.
6. **Funding and partners:** observed donor → recipient → programme connections with exact role labels, grant/loan/CSR/own budget distinctions and 'amount not publicly disclosed' where appropriate.
7. **What changed, and how do we know?** four distinct rows: activities, outputs, measured outcomes, independent evaluations. Show ‘No adequate evidence found’ when warranted.
8. **What remains uncertain:** scale, cost, local delivery, uptake, safety, operational financing, independent evaluation, or anything missing.
9. **Where they fit in the system:** reduce emissions / reduce exposure / protect health / protect income / improve accountability; identify which it actually does, avoiding speculative tags.
10. **Sources and record history:** numbered source citations, publication/access dates, last reviewed, corrections route via public repo issues, disclaimer.

Example style (illustrative only, not publishable without source verification):
> `Clean Energy Nepal works with local partners on air monitoring and clean-air policy. One documented programme supports lower-cost PM2.5 measurement across Nepalese cities. Measurement helps decision-makers see the problem; evidence that this particular programme reduced pollution must be assessed separately.`

### Additional page views under `/organisations/` (do not overcrowd global top navigation)

1. **`/organisations/projects/`** — `What are organisations doing?` Filterable, linked project/activity register. Where local action is visible, people should be able to find it without knowing the organisation's name.
2. **`/organisations/funding/`** — `Who funds what?` Plain-language capital-flow explorer; distinguish philanthropic grants, state budgets, development loans, CSR and commercial investment. Never aggregate incomparable amounts without clear currency/year/method.
3. **`/organisations/places/`** — country and airshed entry points with verified organisation/project counts and a thoughtful narrative on under-represented actors; link to existing `Places` pages where the content exists. An interactive map is optional and must not be the only way to access data.
4. **`/organisations/gaps/`** — `Who is missing?` An evidence-grounded explanation of where monitoring exists but action does not, where mandates are unfunded, where local delivery partners are scarce, where community participation is absent, and which questions require research. No unsubstantiated conclusions from absence in the directory.
5. **`/organisations/methods/`** — eligibility, inclusion criteria, source hierarchy, cutoffs, company due diligence, editorial independence, corrections and uncertainty.

If the existing generator has a better established structure, adapt. These pages may be implemented as clearly delineated sections/tabs within the Organisations hub if that reduces unnecessary navigation; choose a coherent, maintainable solution and explain it in the audit.

### Editorial features worth building

- `Follow the money`: a sourced, clickable chain linking a named foundation/agency → grant or financing → intermediary/implementer → project → location → target group → measured outputs/outcomes. Show missing links, never fill them by inference.
- `From measurement to action`: a short visual explainer asking whether monitored data prompted a concrete decision (school action, transport policy, industry compliance, public-warning process), without falsely asserting impact.
- `Local voices and power`: surface verifiable worker unions, women's collectives and community groups; a large research institute should not crowd them out. Never fabricate individual voices or testimonials.
- `Public responsibility`: show which public entity must approve/operate/pay for recurrent services even when a donor or NGO catalysed a pilot.
- `Is it independently tested?`: a cross-cutting view particularly important for commercial sensor, filtration and mitigation claims.
- `Compare 2–3 organisations/projects`: if feasible, compare **what they do**, funding model, target group, outputs, independent outcome evidence, maintenance responsibility and location; do not rank organisations or award an invented impact score.

---

## 8. Private-sector treatment: responsible business intelligence, not advertising

Private-sector participation should substantially expand, but never become a commercial marketplace or product advert. Research with the same skepticism used for NGO self-reports and government claims.

For every commercial entity, where relevant capture:
- Exact service/product, pollutant targeted, physical mechanism and limits.
- Commercial arrangement: procurement, sales, subscription, installation, service, ownership model or public-private partnership.
- Customer and deployment claims, source and date; independently verified deployments vs marketing claims.
- Public technical performance validation, sensor calibration and quality-control requirements, or independent product efficacy study; disclose evidence not found.
- Actual air-quality benefit, if separately measured, and whether this is emissions reduction, exposure reduction, improved data or unverified possible co-benefit.
- Capital expense, running costs, filter replacements, repairs, power needs, staff training and what happens after funding ends, only when sourced.
- Possible harm: cost/exclusion, burden shifted to workers or small firms, rebound effects, unequal access, electronic waste, water/energy use, displaced emissions, data privacy and conflicts of interest.
- Business model and beneficiary affordability; philanthropy's potential role in independent evaluations, equity safeguards, shared infrastructure or early-stage derisking, **not indiscriminate subsidy of a commercial product**.

For monitoring firms, draw on CSTEP/Indi-SET testing as a candidate independent evidence source. For Indonesia, keep Nafas company and Nafas Foundation separate. For e-mobility programmes, distinguish clean-energy outputs from measured reduction in exposure to traffic-related air pollution. For brick kilns, quantify claims about fuel, PM and black carbon only if an evaluation reports them and state whether workers benefit or bear upgrade costs.

Do **not** describe a company as `verified`, `effective`, `proven`, `best` or `impactful` solely because a product or project page exists. Instead use explicit phrasing such as `Activity documented; outcome not independently evaluated`.

---

## 9. Case studies and explainers for lay readers

Write 8–12 concise, source-rich ecosystem stories (roughly 250–500 words each) showcasing different mechanisms, geographies and limitations. Start with the following **research candidates**, substituting only when verification cannot support a credible case:

1. **Delhi, India — women construction workers:** Mahila Housing Trust and Help Delhi Breathe: air quality awareness, worker registration and public-service links; distinguish training and advocacy from demonstrated exposure reduction.
2. **Nepal — schools and air monitoring:** Clean Up Nepal/Green Decision Labs and Clean Energy Nepal projects: who gets information, whether it connects to action, and evidence limitations.
3. **Pakistan — open data:** PAQI and the institutional use of measurement and analysis; measurement alone is not a policy outcome.
4. **Indonesia — mothers organising:** Bicara Udara's advocacy and education; distinguish civic mobilisation from policy implementation and pollution impacts.
5. **Indonesia — a commercial air-quality network:** Nafas and Nafas Foundation; commercial vs nonprofit roles, sponsor relationship where verifiable, monitoring vs exposure reduction.
6. **Thailand — citizen-led policy:** Thailand Clean Air Network and clean-air legislation; distinguish legislative process from enacted law and enforcement.
7. **Vietnam — a multi-actor project:** USAID-funded Clean Air–Green City project involving Live & Learn and GreenHub; identify precise roles, dates, project outputs and whether the funding remains active.
8. **Philippines — transport transition:** e-mobility ASAP: GEF funding, UNEP/UNIDO and national government roles, Clean Air Asia and consortium roles, job/skills/equity implications; no assumed measured health benefit.
9. **Bangladesh — public finance:** Bangladesh Clean Air Project and the different implementation roles of public agencies; approved credit and intended outputs vs results achieved.
10. **India — sensors under scrutiny:** CSTEP's Indi-SET independent testing as an example of why not all readings and claims can be treated alike.
11. **Regional — transboundary haze:** NGOs, civil society coalitions, scientific institutions and ASEAN coordination; explain who can act on pollution that crosses borders.
12. **Underrepresented local delivery:** a documented rural/industrial-worker or small-city case where community groups carry practical actions but have limited resources; do not invent an example to fill the slot.

For each story include: `The problem in everyday language`; `The actors and their different roles`; `What they did`; `Who paid`; `What evidence of change exists`; `What remains uncertain`; `What another place could learn, without assuming transferability`.

Avoid lengthy jargon. Each story must link back to underlying organisation and project records and sources.

---

## 10. Make the funding map decision-useful, without calling it a funding recommendation

The funding view must let readers answer:
- Which grantmakers and agencies actually financed named clean-air projects in each geography?
- Which NGOs and local organisations received money, rather than just which large intermediaries announced commitments?
- How much is disclosed? In which currency, year and funding instrument? Was it **approved, committed, disbursed or spent**?
- Is the intervention a pollution source solution, an exposure/health protection measure or a community/worker livelihoods measure?
- Are there repeated grants to the same organisations while other geographies and groups are invisible?
- Which initiatives are still relying on time-limited grants for services that need ongoing public financing?
- Where does public infrastructure spending coexist with thin community delivery?

Explicitly separate **known funding gaps** from **research visibility gaps**. `We could not find a public grant record` is not `No one funds this`. For each financial relationship show the provenance and date. Highlight sector investment patterns without confusing funding volume with effectiveness or equity. Large multilateral loans cannot be silently compared with philanthropic grants as if they were the same resource.

Do not put `Donate now`, `Fund this` or fabricated contact details in the page. Use contextual `Why this matters` notes. The page is independent evidence, not an investment broker.

---

## 11. Write at two depths: simple on the surface, rigorous underneath

Reading experience should follow **three progressive layers**:

- **Layer 1 — A person new to air pollution:** 20–30 word summary, unambiguous category and place, one concrete activity. Explain `PM2.5`, `source apportionment`, `airshed`, `emissions`, `exposure`, `grants`, `loans`, `CSR` and `independent evaluation` using optional inline explanations on first use. Avoid acronyms in headings.
- **Layer 2 — Interested reader:** named programmes, partnerships, examples, geography, who benefits, sources and limitations.
- **Layer 3 — Researcher/funder:** methodology, source register, linked grants, dates, independent assessments, evidence classes, exportable data and corrections history.

Each card should pass the test: `Could a 15-year-old understand what this organisation does and why it matters?` Each detailed profile should pass the test: `Could a careful funder understand what is documented, what is not, and who is accountable?`

Use matter-of-fact verbs; e.g. `measures`, `helped register`, `funded`, `advocated`, `installed`, `tested` rather than `transformed`, `revolutionised`, `empowered` absent precise substantiation. Distinguish `organisations are active in a place` from `their activities reach vulnerable communities in that place`.

---

## 12. Design and engineering constraints

Use the existing Clean Air design tokens from `docs/design-brief.md`:

```css
--ca-ink: #1A1A1A;
--ca-navy: #141F52;
--ca-accent: #E3120B;
--ca-link: #2E45B8;
--ca-paper: #F5F4EF;
--ca-surface: #FFFFFF;
--ca-muted: #595959;
--ca-rule: #D9D9D9;
--ca-tint: #EBEDFA;
```

Maintain serif editorial headlines, system sans for interfaces, restrained red emphasis, generous whitespace, subtle rules, strong focus outlines and readable type. Never reproduce The Economist's proprietary fonts, logos or layouts. No heavy dashboards, animated globes, random map pins or icon clutter. Minimise code and dependencies. Fast loading on modest mobile data connections is essential.

Works on GitHub Pages static hosting under `/clean-air/`; do not add a backend, paid API, private token or runtime scraping dependency. Generate data and HTML during build. A client-side filter/search implementation is fine if small and accessible. Choose a static-friendly map only if actual coordinates are sourced, properly licensed and accessible via a non-map list. Do not approximate project locations with arbitrary coordinates and present them as verified. Make all external links secure and labelled.

Add SEO metadata (accurate titles/descriptions, internal links, canonical URLs if appropriate), sensible schema.org structured data where accurate, descriptive page titles, skip links, keyboard functionality, semantic form controls, ARIA announcements for filter results, obvious source affordances, print styles and mobile performance. Target WCAG 2.2 AA where feasible. Test at ~360px mobile and desktop widths, 200% text scaling, and with keyboard-only navigation. Never hide core evidence behind a hover.

Provide export of the public organisation/project data (`CSV` or `JSON`), including `last verified`, source identifiers and a short reuse/attribution note. Do not expose internal-only research notes or any personal contact data. Avoid unlicensed logos; show text names rather than copying organisational logos by default.

---

## 13. Research and content QA: enforce gates automatically where possible

Create validation scripts appropriate to the repo that fail for:
- Duplicate organisation IDs, malformed URLs or missing slugs.
- Programme references to nonexistent organisations.
- Funding relationships with unknown source IDs or missing source references.
- Numeric outcomes/financial figures without cited sources and date.
- Missing `role` in the organisation–project links.
- Status/date inconsistencies, source published after 22 Nov 2026, or expired dates labelled 'active' without current support.
- Broken internal links, route collisions, source anchors, missing country/type labels.
- Unknown or non-authorised evidence labels; preserve EXACT repository categories: `Strong`, `Moderate`, `Limited/mixed`, `No adequate evidence found`.
- Company self-reports rendered as independent findings.

Run build, unit/data validation, smoke tests for search and all filters, responsive screenshots and link checks. Check accessible no-result state and no-JavaScript graceful fallback where practical. Verify the number of published records and precise inclusions manually using a sample of at least 20 records across regions and organisational types. Test no empty profile pages are emitted.

For every new claim, maintain `source ID → source URL & date → claim or record ID → rendered page`. Existing claim IDs must keep resolving. Document unresolved sources, rejected candidates and why. Where a source is an organisation's own account, mark it `organisation-reported` and do not call a numerical result independently verified.

---

## 14. Execution sequence and required final output

**Step A — Inspect.** Read repo rules; audit directory, data, generator and links. Write `docs/organisations-10x-audit.md`.

**Step B — Research.** Build candidate log; verify locally relevant civil society, NGOs, worker collectives, business actors, funders and programmes; gather independent assessments; preserve all provenance.

**Step C — Model.** Extend `/research` data schema and existing source/claim registers; migrate current records; create robust many-to-many links; establish quality and freshness gates.

**Step D — Write.** Produce plain-language summaries, verified organisation dossiers, programme summaries, funding explanations and 8–12 sourced ecosystem stories (as far as verification permits).

**Step E — Build.** Redesign only the Organisations experience and needed subordinate pages within Clean Air's existing visual system and GitHub Pages architecture. Link to existing People, Places, What Works and Evidence material where there is a documented connection.

**Step F — Verify.** Run data/source validation, build, performance, accessibility and usability tests. Inspect screenshots. Fix broken links and cutoffs. Keep current site deployable.

**Step G — Report.** Create `docs/organisations-10x-implementation-report.md` with:
- Files changed and architectural rationale.
- Organisation counts **before / candidates identified / verified published**, by country and role, and NGO/private/funder breakdown.
- Project, donor-recipient and independent-evaluation counts.
- Detailed examples of how to trace any organisation to projects, funds, communities, outcomes and sources.
- Source completeness and staleness audit, with dates.
- Unverified candidates and why excluded.
- Validation results, screenshots, GitHub Pages build/deploy status and any remaining work.
- A small editorial maintenance protocol: adding a new org, adding an activity, correcting a relationship, marking a programme ended, verifying a company claim.

**Keep going until there is a functioning page, source-backed records, working filters and traceable programme/funding relationships. Do not deliver only strategy prose, placeholders, arbitrary example data or a redesigned shell. If access to research sources is constrained, do not pretend otherwise. Build the verified subset and report exactly what is missing.**

---

## 15. Final acceptance test: five people, five questions

A parent in Kathmandu can locate people working on school air, understand what is actually being measured or changed, and see where evidence ends.

A construction worker in Delhi can identify the NGOs, unions and public bodies involved in information, welfare and protection, without confusing those roles.

A reporter in Jakarta can distinguish a commercial data company from its nonprofit foundation and inspect sources rather than repeating marketing numbers.

A city official in Hanoi or Manila can find a comparable programme and understand who financed, delivered and operated it, and which lessons are and are not transferable.

A foundation board member can trace a verified funder → named project → responsible actor → location and community → outputs, outcomes and research gaps, without mistaking financial commitments or promotional success stories for independent impact.

If those five experiences work, the site has genuinely become ten times more useful. If it merely contains hundreds of names and prettier cards, it has failed.
