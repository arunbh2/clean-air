# CLEAN AIR — 10× EXPANSION OF THE EXISTING LIVE WEBSITE

**This brief is tailored to the current live website, not a hypothetical new project.**

**Prepared:** 22 November 2026  
**Working title:** Clean Air  
**Editorial proposition:** Shared air. Unequal protection.  
**Priority geography:** India, anchored in Delhi/NCR; comparative South Asia and Southeast Asia.  
**Existing website:** https://arunbh2.github.io/clean-air/index.html  
**Public GitHub repository:** https://github.com/arunbh2/clean-air  
**Platform type:** Existing, independent, evidence-led public-interest website. Extend it in place; do not rebuild it from scratch. Do not brand it as Practical Action, Common Shade, BeatTheHeat, or Critical Minerals; do not copy their content or identity without an explicit reason and attribution.

---

## 0. YOUR MANDATE — READ THIS FIRST

You are Claude Code acting as a coordinated team comprising: (1) an investigative environmental-health researcher, (2) a South and Southeast Asia air-quality policy analyst, (3) a philanthropic grantmaking strategist, (4) a systems architect, (5) an experienced public-science editor, (6) an accessible product designer, and (7) a careful full-stack/static-site engineer.

Your assignment is to **research, restructure, expand, implement, test and document** an existing or in-progress site called **Clean Air**. Make it **an order of magnitude more useful** through depth of evidence, geographic breadth, ability to compare interventions and funding, and reader comprehension — **not** through ten times as many paragraphs or navigation items.

The website must serve both:

- **A lay reader** — a street vendor, parent, older person, teacher, undergraduate, journalist or concerned resident who wants answers in plain language and may know little about AQI, PM2.5 or epidemiology.
- **A serious decision-maker** — a senior foundation board member, grantmaker, government official, programme designer or donor adviser who needs cited evidence, feasible interventions, examples of past funding, implementation constraints, unanswered research questions, and realistic routes to scale.

Every major topic must therefore have **three progressive layers**: **"The simple answer" (30–90 seconds)**, **"What this means here" (2–4 minutes)**, and **"Explore the evidence, methods and funding decisions"**. Layer 2 must never obstruct Layer 1.

**Do not stop at a strategy document or mock-up.** Inspect the actual repository, conduct credible research using the tools available, create the structured evidence library, implement the highest-value pages and interactions, run tests, and report what is completed versus still pending. If external research access is unavailable, say so explicitly, preserve clearly labeled research queues, and never invent facts, grant awards or sources. Prioritize correctness over reaching numerical targets.

### Non-negotiable rules

1. **AUDIT FIRST, PRESERVE THE LIVE PRODUCT.** This site is publicly deployed and has substantive content. Read `CLAUDE.md`, `docs/site-brief.md`, `docs/research-brief.md`, and `docs/design-brief.md` before editing. Inspect actual source folders, data files, build commands, routes, design tokens, GitHub Pages workflow, existing claim IDs and generated output. Do not overwrite working modules, discard prior evidence, or renumber source/claim IDs. Produce `docs/CURRENT_STATE_AUDIT.md` before substantive restructuring.
2. **SOURCES, NOT FABRICATION.** Every factual assertion, number, study, project, grant, funder relationship and impact claim must be traceable to a usable source URL, document date and access date. Never invent funding amounts, claimed outcomes, citations, award recipients or dates.
3. **EVIDENCE IS NOT THE SAME AS CERTAINTY.** Explicitly distinguish robust causal evidence, credible associations, modeled estimates, observational studies, preliminary pilots, anecdotal accounts and unknowns. Do not imply a causal relationship from a correlation or make up quantified income losses.
4. **REDUCE JARGON.** Write at approximately an accessible 13–15-year-old reading level in the main reader journey; explain technical terms inline and offer optional deeper treatment. No condescending simplification.
5. **INDEPENDENT PUBLIC-INTEREST VOICE.** No disguised fundraising pitch, premature ranking of organisations, lobbying disguised as neutral analysis, advertorials or unsupported solution claims. Disclose methodology, selection criteria and conflicts of interest.
6. **DESIGN FOR PHONE USERS.** Fast, responsive, low-bandwidth, keyboard accessible; no motion-heavy, map-heavy or API-dependent homepage.
7. **NO COPYCAT DESIGN.** Use the provided Economist-inspired editorial principles (restraint, deliberate typography, clear hierarchy and wayfinding, restrained red accent) to make an original Clean Air identity. Do not copy logos, proprietary fonts, distinctive layouts or protected assets. Use properly licensed font alternatives.
8. **NO CLAIM THAT EVERY ACTION IS EQUAL.** Distinguish pollution-source reduction from exposure protection; explain when the latter is a necessary interim response but not a substitute for the former.
9. **DATES MATTER.** Research as of 22 November 2026; show source publication dates, dataset observation years, programme decision dates and freshness/last-reviewed dates distinctly. Never present a 2019 estimate as a 2026 measurement.
10. **DON'T PAD A DATABASE.** Coverage targets below are ambitions, not an excuse to generate fictitious, repetitive or weak entries. A smaller verified database beats a large speculative one.

---

## 0A. VERIFIED BASELINE — THE EXISTING WEBSITE YOU MUST BUILD ON

This is a verified *public-facing* audit as of 22 November 2026, not a full source-code audit. Confirm the repository's actual implementation yourself.

**Live pages inspected:**

- Home: `https://arunbh2.github.io/clean-air/index.html` — headline **Shared air. Unequal protection.**, the 2026-11-22 evidence cutoff, plain introduction, six prominently linked community starting points, and routes into the research.
- The crisis: `/crisis/index.html` — Indian AQI and WHO guidance, monitoring gaps, PM2.5, source apportionment, personal exposure, health evidence and caveats.
- People and livelihoods: `/people/index.html` — **15 population groups**, including street vendors, waste pickers, sanitation workers, construction labourers, drivers, kiln workers, home-based workers, farmers, informal-settlement residents, homeless people, migrants, older people, pregnant women, children and people with disabilities/chronic illness (audit actual number and classification; treat this list as descriptive and verify in repo).
- Places: `/places/index.html` — **Delhi/NCR plus five contrasting Indian settings**: Bihar/Patna and rural Bihar, Singrauli, Mumbai, the Punjab/Haryana residue belt, and brick-kiln clusters. These six settings are fundamentally different types of place; do not flatten them into a city ranking.
- What works: `/what-works/index.html` — an intervention library that already separates **Fund now / Test first / Not recommended**, rates problem evidence separately from intervention evidence, and explicitly critiques smog towers and generic spraying.
- Organisations: `/organisations/index.html` — a carefully sourced directory covering regulators, public programmes, development banks, funders, researchers and community implementers, with explicit gaps and caveats.
- Evidence: `/evidence/index.html` — claim register, source register, evidence map, economic estimates, pathways, verification record and gaps. Claims are traceable to stable IDs and source statuses.
- Support options: `/support/index.html` — **four existing portfolio options**, notably income continuity for workers affected by restrictions, occupational protection, children's schools/early years, and an explicitly deprioritised production/rural-energy learning agenda.

**The current site already does several difficult things well:** it separates daily pollution and long-term exposure; does not treat AQI as inhaled dose; distinguishes public-policy losses from illness losses; avoids using India's estimates as if they were street-vendor earnings; separates documented effects from causal hypotheses; and documents a source access log. **Preserve all of these.**

**Repo-level instructions are binding unless explicitly updated by the project owner:**

1. The repository's `CLAUDE.md` is a substantive rulebook, not decorative context. It establishes the research cutoff, Claim IDs, evidence labels, independence and content-generation rules.
2. `docs/site-brief.md` governs site content, routes and build. `docs/research-brief.md` governs evidence; `docs/design-brief.md` governs visual design. Respect existing precedence.
3. **Site pages are generated from `/research` Markdown and CSV.** Do not create an isolated new dataset or manually hardcode a competing second evidence base. Extend the existing source/claim/evidence files, add migration-safe fields, regenerate the website and update validation scripts.
4. Preserve stable citations such as `C016`, source references such as `S049`, existing slugs, and downloadable research artifacts. Update cross references instead of breaking them.
5. The current required evidence labels are **Strong / Moderate / Limited/mixed / No adequate evidence found**. Do not introduce an incompatible A–D rating of scientific evidence. The repo uses **A/B/C/D only for funding-option readiness**, with A ready to support, B needs adaptation, C needs proof, D not recommended.
6. Maintain the existing editorial brand and the design tokens already specified in `docs/design-brief.md`: `--ca-ink: #1A1A1A`, `--ca-navy: #141F52`, `--ca-accent: #E3120B`, `--ca-link: #2E45B8`, `--ca-paper: #F5F4EF`, `--ca-surface: #FFFFFF`, `--ca-muted: #595959`, `--ca-rule: #D9D9D9`, `--ca-tint: #EBEDFA`. Use Georgia or another properly licensed editorial serif and system sans. Preserve accessibility restrictions on red and AQI colors. Never adopt Practical Action or Common Shade branding.
7. **Research cutoff stays 22 November 2026 for this expansion.** Any later regular updates require an explicitly documented change to cutoff policy, dated releases and preservation of the previous snapshot. Never silently mix later material into a 22-Nov-2026 evidence edition.

**Specific 10× improvements missing or insufficiently developed in the public site (verify against the repo before claiming absence):**

| Dimension | Current public baseline | Required next step |
| --- | --- | --- |
| Geography | India-focused: Delhi + five contrasting settings | Add a rigorous South Asia shared-airshed layer and deep country/city cases for Bangladesh, Nepal, Pakistan; add selective Southeast Asia cases for Indonesia, Thailand, Vietnam, Philippines, Cambodia, then secondary comparisons |
| Funding | Organisational directory and public financing mentions | Build a linked **Who funded what?** atlas with exact award, instrument, time, stage, recipient, operational status, results and accessible primary documents |
| Intervention library | Critical and well-curated but India-centric | Expand with country-specific evaluated implementation cases, the economics of scale, institutional ownership and conditions for transfer |
| Decision support | Four India-centered portfolio options | Retain those four as the India 2026 baseline; add distinct regional funding pathways rather than quietly changing or reversing their judgments |
| Lay accessibility | Serious evidence with dense technical passages, acronyms and long tables | Add a simple first layer, short question-led explainers, glossary tooltips, accessible maps, progressive disclosure and portable summaries without losing documentation |
| Cause/effect | Strong textual pathway accounting | Add carefully labelled, clickable `exposure → health → time/income/care → household security` story paths; mark unsupported arrows |
| Infrastructure | Operator, O&M and costs assessed | Add capital/operational/enforcement/market infrastructure classification and comparative funding/ownership requirements |
| Updates | Cutoff, claim register and verification log | Add a transparent coverage log, country-specific last-reviewed date, dated releases and stale-reference checks |

**Very important:** This is an expansion and editorial layering programme, not a rebranding exercise or a reason to discard the existing evidence dossier.

---

## 0B. THE CENTRAL DESIGN TEST

An intelligent 16-year-old should be able to answer within 90 seconds: *What is air pollution, why is this person exposed, what does it change in their life, and what could realistically improve it?* A foundation trustee should then be able to drill down and ask: *Which intervention has evidence, who has funded a similar approach, who operates it, what does it cost over time, and which failure mode would invalidate it?*

Every research-heavy page must use a **three-depth editorial pattern**:

- **Simple answer:** 40–90 clear words, a real-world example and one honest limitation, with no unexplained acronym.
- **Where the evidence points:** 2–4 minute overview explaining magnitude, location, relevant communities, plausible causal links and contested claims.
- **Deep evidence:** existing claim IDs, original sources, access status, methods, alternative interpretations, verified funding records, costs, risks and data downloads.

Do not replace prose with charts or dazzling interaction. Visuals should reduce thinking work, not merely decorate the page.

---

## 1. THE CORE STORY AND THE QUESTIONS PEOPLE NEED ANSWERED

The opening proposition:

> **Shared air. Unequal protection.**
>
> Air pollution reaches across cities, homes and borders. But the people who spend the longest hours breathing it often have the fewest choices about where to work, how to travel, or how to protect their families.

Use this framing to answer six simple questions on the home page:

1. **What am I breathing?** PM2.5, PM10, nitrogen dioxide, ozone, indoor smoke, black carbon; AQI versus actual exposure; why a city average does not describe everyone.
2. **Why does it matter?** Health, pregnancy, childhood, schooling, mental well-being, labour productivity, medical bills, income stability, household spending and long-term economic opportunity.
3. **Who bears more of the burden?** People with higher exposure, fewer protections, worse baseline health and limited ability to avoid work or relocate.
4. **Where does pollution come from?** Transport, industrial combustion, power, brick kilns, diesel generators, waste burning, cooking, agriculture, construction/road dust, landscape and peat fires, shipping where relevant; distinguish primary emissions and secondary PM formation.
5. **What actually works?** Source controls and systems reform first, complemented by tested exposure-reduction approaches for vulnerable groups.
6. **Who is already paying, who is doing the work, and what is missing?** Grantmakers, development banks, public budgets, implementers, researchers, private sector; distinguish completed, committed, proposed and exploratory programmes.

The site's recurring intellectual question should be: **"Who is exposed, who has a choice, who can act, and who pays?"**

A vivid example of the storytelling logic: a Delhi street vendor might lose income when shutting their stall to avoid the worst pollution, but might also lose income through sickness, customer footfall and household care burdens. These are **pathways to investigate**, not automatic, quantified effects. Show how each pathway would be tested and what studies already support it.

---

## 2. RESEARCH PROGRAMME — GEOGRAPHIC COVERAGE

Build a regional knowledge system with **Delhi/NCR as the narrative anchor, India as the initial main coverage, and South/Southeast Asia as comparative learning regions**. Avoid presenting all countries as if evidence is equally rich.

### Tier 1: Full, evidence-rich country and city dossiers

**India:** Delhi/NCR plus Kanpur/Lucknow/Varanasi, Kolkata, Mumbai, Chennai, Bengaluru, Punjab-Haryana agricultural/airshed linkages, and brick-kiln clusters. Explain the NCAP, state pollution boards, municipal responsibilities, judicial directions where relevant, sources, sectors, vulnerable groups, measured trends and implementation gaps. Avoid claiming interventions explain a trend without source-apportionment or evaluation evidence.

**Bangladesh:** Dhaka, Gazipur/Narayanganj industrial belt, brick-kiln belts and regional transboundary airshed; review Bangladesh Clean Air Project, public transport, continuous emissions monitoring, industrial enforcement, clean bricks and household exposure.

**Nepal:** Kathmandu Valley, Terai border pollution and mountain/Himalayan black carbon; consider brick kilns, household energy, transport, open burning and transport of particulate pollution from the Indo-Gangetic Plain.

**Pakistan:** Lahore/Punjab and Karachi; provincial clean-air policy, winter episodes, source emissions, agriculture, transport, household and worker exposure.

**Indonesia:** Jakarta and Greater Jakarta, industrial/transport exposure, waste burning; Sumatra/Kalimantan peat and forest fires; cross-border haze and community monitoring.

**Thailand:** Bangkok transport/industry and Chiang Mai/Northern Thailand seasonal biomass burning; cross-border Mekong basin effects and livelihood trade-offs.

**Vietnam:** Hanoi and Ho Chi Minh City; transport, construction and industrial emissions, cleaner public transport and household exposure.

**Philippines:** Metro Manila transport and waste burning; public-health and community-led monitoring, coastal/urban differences where supported.

### Tier 2: Concise comparison dossiers, then deepen based on evidence

**Sri Lanka, Bhutan, Cambodia, Lao PDR, Myanmar, Malaysia, Singapore**. Include country-specific sources, institutions and cross-border issues; do not force an India-centric theory of pollution onto each. For Cambodia investigate rice-straw management and black carbon; for Malaysia/Singapore investigate transboundary haze systems, regulation and upstream prevention; for other countries identify major urban or biomass sources only when supported.

### For EVERY country page, build the same understandable but honest structure

- One-sentence takeaway, followed by 3 things a resident should know.
- The main pollutants; long-term trends and data limitations.
- Who is most exposed, and why (not just who is medically susceptible).
- 4–6 key emission sources, supported by source-apportionment evidence if available; state when source estimates disagree.
- Health and income/livelihood pathways, separated by evidence strength.
- Who regulates, monitors, funds, delivers and can hold others accountable.
- 3–5 evidenced interventions or current experiments.
- Specific, verified funding examples with funder, implementer, instrument, amount only if verified, status, dates and sources.
- What is transferable from other countries, and what may not transfer.
- Gaps, unanswered questions and links to original research.
- `last reviewed`, `data year`, citation provenance and any important method notes.

Do not make flags, pictures, pollution rankings or a dramatic red map the principal content. Comprehension first.

---

## 3. FOLLOW PEOPLE, NOT JUST POLLUTANTS

Create a deeply researched section titled **"People & livelihoods"**, with at least these profiles when evidence supports them:

1. Street vendors and informal market traders.
2. Construction workers, road workers and street sweepers.
3. Auto-rickshaw/taxi/bus drivers, couriers and delivery riders.
4. Brick-kiln and industrial workers.
5. Waste pickers, sanitation workers and waste-burning-adjacent residents.
6. Farmers and seasonal agricultural workers.
7. Domestic workers and low-income commuters.
8. Pregnant people and newborns.
9. Infants and children, including asthma, respiratory infection, school attendance and developmental concerns.
10. Older adults and people with pre-existing respiratory/cardiovascular disease.
11. Residents of informal settlements and overcrowded rental housing.
12. Teachers, children and staff in poorly ventilated schools.
13. Migrants and people with disabilities whose capacity to alter exposure may be limited.
14. Women and unpaid caregivers experiencing the indirect consequences of illness, school closures and care needs.

Each profile should answer: **Where does exposure happen? What do we know about the health pathway? What can happen to earnings, learning, household spending and opportunity? What can the person realistically control? What requires employers/municipalities/governments to act? What interventions have actually been evaluated?**

Show first-, second- and third-order impacts visually:

`Pollution/emissions → exposure → physiological harm / service disruption → sick days, care work, productivity, attendance → lower earnings or extra cost → debt, reduced school investment, reduced resilience.`

Label every arrow as `well established`, `supported but context dependent`, `plausible / needs testing` or `not yet established in this setting` based on the evidence. Never make the flow look like a proven chain end to end if it is not.

### Distinguish these analytical concepts

- Hazard versus measured ambient concentration versus personal exposure versus inhaled dose.
- A high-risk person's *susceptibility* versus the level of exposure they receive.
- A population association versus a causal estimate.
- Measured earnings impact versus estimates derived from health outcomes.
- Short-term pollution episodes versus year-round cumulative exposure.
- AQI versus annual PM2.5; country indices can differ, and comparisons require comparable underlying concentrations and methods.
- Outdoor, indoor, household-fuel, occupational and transboundary exposures: overlapping, not interchangeable categories.
- Air pollution alone versus compounding heat, poverty, housing precarity and poor access to care.

For sensitive outcomes (pregnancy, childhood neurodevelopment, dementia, mental health), match the wording to consensus evidence and qualify emerging findings.

---

## 4. WHAT WORKS: CREATE A SERIOUS INTERVENTION LIBRARY

Build a filterable library of 40–60 **distinct interventions or programmes** only if well supported; target the most important 20 fully developed entries first. Each intervention card must have:

- A literal one-sentence explainer understandable to a non-expert.
- `Problem addressed`, `source/emission pathway`, `people affected`, `geography and operating context`.
- `Intervention class`: emissions prevention/abatement; exposure protection; evidence/monitoring; governance/enforcement; finance/market change; enabling infrastructure; workforce/transition.
- `What changes in the real world?`, not just a generic promise to "raise awareness".
- `Expected outcomes`: which are measured, which are modeled and which are hypotheses.
- `Strength of evidence`, `generalizability`, `time to impact`, `indicative cost band` if grounded, `operating and maintenance cost`, `who pays`, `who maintains`, `who benefits`, `who could lose`, and `prerequisites`.
- `Failure modes`, `equity safeguards`, `what monitoring would prove success`, linked case studies and cited studies.
- `Funder fit`: philanthropy/grant, public finance, concessional finance, commercial finance, regulation, household spending or blended mechanism.
- `Status`: concept, pilot, operating, evaluated, scaled, discontinued.

Research at least these families:

**A. Emissions and economic infrastructure:** cleaner brick production and kiln transition (including black carbon), industrial boilers and heat, continuous emissions monitoring, transport fleets/buses/last-mile electrification, inspection and maintenance, fuel quality, non-motorised transport, road/construction dust management, reliable electricity to displace diesel generators, cleaner cooking, solid-waste collection and segregation to replace open burning, controlled composting/material recovery, crop-residue collection and viable markets, agricultural machinery/services and avoided burning, peatland and landscape fire prevention.

**B. Public systems:** airshed-wide action plans; credible monitoring networks, source-apportionment studies, emission inventories, enforcement capacity, municipal procurement, cleaner school/building standards, occupational protection requirements, cross-ministry finance, interjurisdictional agreements, and community participation.

**C. Interim exposure protection:** clean-air rooms in schools or community centres, well-sized and correctly maintained HEPA filtration, ventilation and building-envelope measures tailored to pollutant/context, occupational policies, masks/respirators with proper fit and limitations, clear alerts with accessible options, protection for people who cannot stop earning, workplace changes and outreach through primary health systems.

**D. Behaviour and communication:** communicating risks, community monitoring that changes decisions, school information, citizen litigation/complaint systems where relevant, and campaigns. Separate measured policy/behaviour changes from media reach and impressions.

**E. Systems with co-benefits and trade-offs:** black-carbon reduction; waste-picker formal inclusion; locally appropriate clean cooking; lower-carbon transport; rural livelihood alternatives to burning. Test transition burdens, adoption incentives, payment mechanisms and maintenance.

### A crucial editorial feature: "What not to mistake for a solution"

Provide fair, researched explanations of why giant outdoor smog towers, tree planting as a stand-alone citywide PM2.5 cure, generic indoor plants, AQI dashboards without action, unsupported air-purifier coverage claims and symbolic one-day bans can be insufficient or weakly evidenced. Do **not** dismiss legitimate local benefits where demonstrated. Make clear that personal protective measures may reduce exposure but cannot by themselves solve emissions.

### Compare interventions intelligently

Let users compare **up to three** interventions on `what it changes`, `beneficiaries`, `evidence`, `implementation dependencies`, `cost/finance type`, `maintenance`, `fairness`, and `measurement`. Do not produce a single pseudo-precise "best intervention" score. If data is absent, render `Not established` rather than zero.

---

## 5. CREATE A RESEARCHED "WHO FUNDED WHAT?" FUNDING ATLAS

This is a differentiator. A senior foundation board member should be able to see **verified grants, technical assistance, public investments, development-bank projects, co-financing and catalytic philanthropy**, rather than a generic list of philanthropic logos.

Build linked records for:

**Funder → instrument → initiative/project → implementing organisation → country/city → intervention → intended beneficiaries → amount/currency/year (only if verified) → documented outcome → evaluation quality → original source.**

Make **four funding categories visually distinct**:

1. **Philanthropic grants** (awarded and attributable).
2. **Development/public finance** (loan/grant/guarantee/budget allocation, with board approval and disbursement status distinguished).
3. **Private or blended investment** (identify commercial and catalytic portions where verified).
4. **Prospective or thematic funder relevance** (NOT a grant award; clearly label as a potential alignment hypothesis).

For every named entity, check against its own grant database, annual report, official project portal or funding announcement. A foundation that funds a regranting intermediary does not automatically fund every downstream project directly. Never confuse fundraising received, funding committed, project cost and disbursed funding. Distinguish air-quality-primary from air-quality-co-benefit finance.

### Priority entities to research and verify

**Philanthropy and intermediaries:** Clean Air Fund and its grantee listings; Bloomberg Philanthropies / Breathe Cities; Children's Investment Fund Foundation (CIFF); IKEA Foundation; Sequoia Climate Foundation; McCall MacBain Foundation; Open Philanthropy; Bezos Earth Fund; relevant local and regional foundations. Do not say each has funded South Asian or Southeast Asian clean-air projects until a specific grant is confirmed.

**Development and international institutions:** World Bank / IDA / IBRD / MIGA; Asian Development Bank and Asia Clean Blue Skies; Japan International Cooperation Agency; UK FCDO; Swiss Development Cooperation; Climate and Clean Air Coalition; UNEP; relevant UN, bilateral and regional technical assistance. The WHO, Health Effects Institute and universities may be research authorities rather than funders in a given project. Classify their actual roles correctly.

**Implementers and knowledge institutions:** Clean Air Asia; OpenAQ; Vital Strategies; ICIMOD; CEEW; TERI; Centre for Science and Environment; EPIC/Air Quality Life Index; local community-led organisations, public health coalitions, worker organisations, city and national regulators. Include only where a demonstrated air-quality role exists.

### Verified example leads to investigate deeply (not unquestioningly repeat)

- **Bangladesh Clean Air Project:** World Bank announced a **US$290m** project on 18 June 2025, including vehicle-emissions control and replacement of aging diesel buses with 400 zero-emission buses. Confirm loan/grant composition, project status, results framework and responsible entities directly from World Bank project records: https://www.worldbank.org/en/news/press-release/2025/06/18/world-bank-helps-bangladesh-improve-energy-security-air-quality
- **India, Agra/Gorakhpur:** Clean Air Fund grants describe city-level multisectoral action support; verify specific recipients, periods and outputs from https://www.cleanairfund.org/what-we-do/our-grants/ . Do not infer citywide pollution reductions from an activity grant.
- **India, Uttar Pradesh/Haryana:** Clean Air Fund reports its support contributed to unlocking World Bank clean-air finance; distinguish the role of advocacy/enabling funds from the full value of development-bank financing: https://www.cleanairfund.org/what-we-do/our-impact/
- **Indonesia / Jakarta:** Clean Air Fund's country programme and work with Vital Strategies/Jakarta government; distinguish data use, health/economic analysis, governance outcomes and measured pollution changes: https://www.cleanairfund.org/geography/indonesia/
- **Indonesia / Philippines:** Community-led air-quality monitoring through GAIA, including wearable-monitor approaches and questions of whose exposures are invisible: https://www.cleanairfund.org/news-item/lessons-community-led-air-monitoring/
- **Indonesia:** community research around waste burning and the role of WALHI; verify local context, grant relationships and outcomes: https://www.cleanairfund.org/news-item/communities-waste-burning/
- **Pakistan/Punjab, Nepal, Bangladesh and Indian states:** World Bank IGP-HF programme overview and precise project statuses: https://www.worldbank.org/en/brief/2025/12/09/air-quality-management-in-the-indo-gangetic-plains-and-himalayan-foothills
- **Cambodia:** Climate and Clean Air Coalition-supported integrated rice-straw management for black-carbon reduction; verify approved activity, implementer, finance and evaluation: https://www.ccacoalition.org/projects/cambodia-scaling-integrated-rice-straw-management-reducing-black-carbon-emissions
- **Southeast Asia eight-city assessment:** ADB's March 2026 regional analysis; extract city-specific priority actions and financing needs from the official publication: https://www.adb.org/publications/air-quality-southeast-asia
- **Global funding patterns:** Clean Air Fund / Climate Policy Initiative 2026 development-finance analysis and 2026 philanthropic analysis; distinguish their different denominators, geography and time windows: https://www.cleanairfund.org/resource/air-quality-funding-2026/ and https://www.cleanairfund.org/resource/philanthropic-foundation-funding-2026/

### Questions to answer across funding cases

- Which funding created a **public good** (data, standards, institutions, regulatory capacity) versus directly paid for implementation?
- Which early grant catalysed a large public investment, with evidence of attribution and no double-counting?
- Which interventions have scaled beyond pilots, and who is paying operating costs?
- What is funded for transport versus waste, industry, agriculture, health, worker protection and schools?
- Is clean air financed explicitly, or claimed as an incidental climate/urban co-benefit?
- Where is local civil society able to access resources, and what stops it?
- Where are large project commitments but no public evidence yet of results?
- What do funders *not* fund and why — weak data, policy constraints, adoption risk, O&M, market economics or lack of investible vehicles?

Create a **Funding Atlas** with filters (`country`, `city`, `funder`, `recipient`, `instrument`, `sector`, `beneficiary`, `stage`, `year`, `evidence level`) and a **Funder profile** page with a source-verified chronology. Do not invent contact names, active application windows or open calls.

---

## 6. A FOUNDATION BOARD MEMBER'S "INVESTMENT PATHWAYS" ROOM

Create a public, clearly marked **"For funders & decision-makers"** route. It must remain legible to a motivated lay reader and should not read like a consultancy sales deck.

Present six decision pathways:

1. **Protect now:** defensible measures for children, workers and people with constrained choices while systemic changes take effect.
2. **Measure the invisible:** credible neighbourhood and occupational exposure monitoring, open data, source apportionment and linking data to decisions.
3. **Make the polluting economy cleaner:** kilns, SME industry, waste handling, agricultural burning alternatives and public transport, with technology and transition economics.
4. **Build the public systems:** implementation capacity, procurement, standards, budget alignment, airshed coordination and enforcement.
5. **Fund locally led action:** community groups, labour organisations, health professionals, independent monitoring and accountable participation, with safeguards against tokenism.
6. **Create investable pathways:** philanthropic proof-of-concept → technical assistance → public procurement or regulation → concessional/commercial finance where appropriate → stable O&M.

For each pathway provide:

- A one-paragraph theory of change.
- A compact schematic of **who needs to change what**.
- 2–4 country-relevant examples linked to verified programme records.
- Suitable capital form and approximate order of magnitude only if grounded in actual project costs; otherwise label `costing required`.
- Policy and infrastructure prerequisites; implementation/maintenance owner.
- Evidence already available, evidence thin and decisive unanswered questions.
- A practical 12–24-month learning agenda with intermediate indicators and evaluation design.
- Risks, distributional effects, local partner roles and exit/sustainability options.
- "What would change my mind?" — a transparent falsification and due-diligence checklist.

**Create a robust distinction between:**

- *Prevention/abatement infrastructure*: actual emission-source reductions.
- *Protective/health infrastructure*: cleaner spaces, occupational protections, health-system response.
- *Information/governance infrastructure*: monitoring, transparent data, regulation, procurement and accountability.
- *Market/transition infrastructure*: financing access, equipment/service models, training and viable replacement livelihoods.

Treat catalytic philanthropy as funding conditions for scaled action, not necessarily funding the final infrastructure asset itself. Explain who pays for what, when, and why.

---

## 7. EVIDENCE LIBRARY, RESEARCH GAPS AND OPEN QUESTIONS

Create a structured **Evidence Explorer** — not a page of PDFs. Users must be able to browse by population, geography, source, outcome, method, date, intervention and quality.

### Sources to prioritize

**Authoritative global/regional:** WHO 2021 Air Quality Guidelines and subsequent 2026 health briefs; Health Effects Institute / State of Global Air 2025 and regional reports; World Bank airshed management and country-specific environmental-health reports; Asian Development Bank Southeast Asia assessments and projects; Clean Air Fund funding/grant repositories; Climate Policy Initiative; UNEP and Climate and Clean Air Coalition; peer-reviewed literature; official national monitoring and health statistics; OpenAQ provenance-checked observational data.

**Local/primary:** CPCB, state boards, NCAP and national audit/evaluation evidence in India; Bangladesh Department of Environment, public records and World Bank project evaluation; Nepal government and ICIMOD; Pakistan provincial environment departments; Indonesia KLHK and Jakarta data; Thailand PCD; Vietnam government monitoring and peer-reviewed work; Philippines DENR and locally led studies; other country agencies as confirmed.

**Relevant emerging research leads:** occupational exposure among Delhi street vendors, auto drivers and sweepers; 2026 Chennai vendor respiratory-health study; qualitative work on air pollution, daily wage work, market closures and the informational burden on Delhi's marginalised livelihoods. Extract sample design, date, limitations and *which claims the studies actually support*, not just a dramatic quote.

### Evidence strength rubric — maintain compatibility with the live repo

Use exactly the four established evidence labels from `CLAUDE.md`:

- **Strong** — multiple high-quality sources and/or strong causal evidence in a directly relevant context, with written reasoning.
- **Moderate** — credible evidence but meaningful context, methods or transferability limitations.
- **Limited/mixed** — few studies, inconsistent results, proxy outcomes, or weak causal identification.
- **No adequate evidence found** — verified research gap, not proof an intervention is ineffective.

For each relevant subject, separately rate **(a) confidence that a problem or harm exists** and **(b) confidence that a proposed response produces the intended outcome**. Distinguish explicitly `no evidence`, `evidence of no effect`, `evidence of harm`, and `evidence that works only under specific conditions`. Write a reason for every rating; do not merely assign a colour.

The separate A/B/C/D scale, already in use in the repo, governs **readiness for grantmaking**, not quality of scientific evidence: A support-ready; B promising/adaptation; C proof required; D not recommended on present evidence. Reuse, do not redefine.

### Dedicated "Where the evidence is thin" page

Cover and update questions like:

- How much annual income is lost from pollution among Delhi street vendors and informal workers after controlling for weather, seasonality and demand?
- Which worker protections reduce personal exposure without shifting the economic burden onto workers?
- Do clean-air classrooms protect children at meaningful scale, and who pays for filters and electricity?
- How do air-quality interventions affect pregnant people in low-income housing — measured exposure and outcomes versus plausible benefit?
- What is the true net impact and adoption economics of cleaner bricks/alternative kilns in India, Bangladesh and Nepal?
- Which municipal waste-management changes durably eliminate open burning while protecting waste-picker livelihoods?
- Which low-cost monitors and exposure models are reliable for dense informal settlements, roadside kiosks and very polluted conditions?
- How do cross-border controls work when political jurisdictions, funding and airsheds differ?
- What happens after a pilot grant ends — maintenance, public budgets, governance and adoption?
- Do air alerts result in a safer choice for someone who must earn outdoors that day?

For each gap: `why it matters`, `current evidence`, `missing counterfactual/data`, `promising method`, `who can investigate`, `what the finding would change`, `links`.

---

## 8. SYSTEMS EXPLANATIONS: MAKE COMPLEXITY VISIBLE WITHOUT CONFUSION

Develop a simple optional **"How the problem connects"** module using causal loops and an intuitive `Sense → Decide → Act → Sustain` storyline.

Example loops to research and make understandable:

- Dirty air → illness → lost income → reduced ability to purchase protection or access care → increased vulnerability.
- Dirty air → school or outdoor-work closure → income loss and care burden → less economic choice.
- Clean technology adoption → up-front costs and credit constraints → weak uptake → continued pollution, unless finance/service/market models change.
- Low-quality data → weak enforcement → persistent emissions → distrust → limited political accountability.
- Poor waste collection → open burning → exposure → reduced trust and social costs; create credible livelihood roles in collection/recycling as a potential lever.
- Independent monitoring → credible local accountability → cleaner public spending/regulation → measured improvements → public trust and political durability (hypothesis to test, not universally proven).

Users should see a readable explanation before any diagram. Use proper causal-loop notation only in advanced views; define sign and delay. Never imply a model is an empirically proven causal mechanism.

**Cross-sector bridge:** Air pollution + heat stress + weak housing + informal work can create compounding risks. Treat the joint exposure as a research topic, not a replacement for the air-quality focus.

---

## 9. CONTENT INFORMATION ARCHITECTURE — EXTEND THE CURRENT SITE WITHOUT BREAKING IT

**Preserve the existing seven top-level routes and their names first:** The crisis; People and livelihoods; Places; What works; Organisations; Evidence; and the prominent secondary route Where support could make a difference. Keep existing slugs, references and backlinks working. Improve the information architecture through **second-level hubs**, scoped search and cross-linked journeys rather than replacing the entire header with seven new categories.

Suggested nested experiences:

- **The crisis** → `Start here`, `Air pollution explained`, `Pollution sources`, `Why AQI is not your exposure`, `Shared airsheds`, `Health effects`, `Basic glossary`.
- **People and livelihoods** → existing 15 communities, `children and schools`, `women and pregnancy`, `outdoor and informal workers`, `income and care pathways`, `take a guided journey`.
- **Places** → retain six Indian case types; add `South Asian airshed`, South Asian country and city profiles; `Southeast Asian haze/urban air` country and city profiles; carefully sourced comparisons.
- **What works** → retain original intervention IDs and verdicts; add categories `emissions`, `exposure`, `health`, `livelihood and social protection`, `governance`, `finance`, `infrastructure`; add verified country cases and up-to-three comparisons.
- **Organisations** → keep existing function-based directory; add `Who funded what?` Funding Atlas, funder profiles and verified delivery relationships. This is a dataset, **not** a logos page.
- **Evidence** → retain claim register, source register, evidence map, verification record, gaps, economics and consequence pathways; add region-specific filters, explainers and coverage metrics.
- **Where support could make a difference** → keep the four baseline India portfolio options and dated decision brief; add clearly separate regional pathways, public/private/philanthropic financing roles and researchable investment hypotheses.

A short, reader-friendly `Start here` route can be a subroute of the home page. Do not duplicate existing research pages; assemble introductory views from the same underlying validated records. Keep a footer for About, Methodology, Corrections, Data/Downloads, Update policy, Privacy and Accessibility.

### Homepage wireframe, in order

1. Small original CLEAN AIR masthead and compact top nav.
2. Editorial opening: **Shared air. Unequal protection.** with clear subtitle and one strong, sourced insight.
3. Six clickable beginner questions, each answered in two sentences.
4. Three story-led choices: **"I want to understand the problem"**, **"I want to see what works"**, **"I want to know who funds action"**.
5. One person-led vignette (e.g., Delhi street vendor) with labeled evidence and no invented personal biography.
6. Regional lens: India anchor; South Asia and Southeast Asia as expandable comparisons.
7. **Action is possible**: 3 carefully chosen interventions, their actual limitations, and citations.
8. **Following the money**: grounded funding signal with publication period and transparent denominator.
9. **Questions researchers still cannot answer**: 3 gap cards.
10. Latest verified evidence updates, methodology and invitation to report corrections.

**Preserve the current homepage's successful basic story as you add the following modules. Do not replace existing working content with a wholly new homepage layout without a demonstrated usability benefit. Do not default to an alarming AQI ticker or a giant unlabeled pollution heatmap.** Real-time data can be a separate optional module with source/timezone, coverage gaps and health disclaimers; it is not a substitute for historical and structural understanding.

### Story page template

- Question as H1: e.g., "What does bad air cost a street vendor?"
- 40–60 word plain-English answer.
- One human-centered illustration *only if licensed / authentic / clearly illustrative*.
- 3 ways the problem may affect the person; cite each.
- "What studies show" and "What we still don't know" side by side.
- "What can change" across individual, employer, public systems and finance.
- Links to interventions, programme funding, country dossier, original evidence and glossary.
- Short `Key fact / source / period / caveat` summary.

### Comparison page template

- Simple question: "How does Lahore compare with Delhi?" or "What can Jakarta teach Dhaka?"
- Comparable indicators only, using the same year and method when possible.
- Context on geography, meteorology, fuel mix, policy and data coverage.
- 3 genuinely transferable lessons and 3 caveats.
- Never declare city A healthier than city B based on mismatched sensor networks, country AQI formulas or incomplete urban coverage.

---

## 10. DESIGN SYSTEM, LANGUAGE AND ACCESSIBILITY

Build a distinctive **independent editorial research platform**. The prior direction draws on restrained editorial practices: visual hierarchy, plain wayfinding, clear rules, purposeful contrast and calm visual storytelling.

### Preserve the site's existing design tokens — source of truth is `docs/design-brief.md`

- Ink: `#1A1A1A` — headings and body.
- Navy: `#141F52` — navigation, charts and analytical context.
- Red accent: `#E3120B` — sparingly for critical data/category emphasis only, *not* for every alert or button. Be mindful this red is a familiar Economist brand token; adapt toward a distinguishable Clean Air palette if necessary.
- Warm paper: `#F5F4EF` — editorial surfaces.
- White: `#FFFFFF`; muted slate/grey for nonessential metadata.
- Keep the existing Georgia + system sans-serif starting point. Introduce a different editorial serif or sans only if performance, license and consistency are demonstrably improved. No proprietary font downloads or embedding.
- Preserve the existing **18–20px long-form narrative** recommendation, generous line height, ~65-character reading measure, high contrast and meaningful underlines for links. Navigation/meta may use smaller accessible sizes.
- Use restrained lines/dividers, ample spacing, 8-point spacing logic, consistency across cards and templates.

### Reader interactions

- "Explain that" inline glossary for terms such as `PM2.5`, `AQI`, `airshed`, `black carbon`, `source apportionment`, `DALY`, `confidence interval`, `causal evidence`, `concessional finance`.
- Small, accessible charts with plain language takeaways, source labels and downloadable underlying data; include text alternatives.
- Filter chips for evidence, countries, groups and interventions; usable by keyboard and screen reader.
- Breadcrumbs, good related reading, inline sources and an obvious return route.
- Country/region comparison with explicit comparability flags.
- Plain-text printable brief for each intervention and country dossier.
- Compact one-page "Board briefing" view of a funding pathway.
- Mobile no-data fallback for graphs, maps and external integrations.
- WCAG 2.2 AA as target; test text and controls against relevant contrast criteria, keyboard navigation, focus and reduced-motion preferences.

Use real images only with licenses/permission and captions. No generic stock photography implying a named person is a study subject. Record alt text, attribution and source license. Prefer original vector diagrams and carefully labeled schematic illustrations where imagery does not add evidence.

---

## 11. DATA ARCHITECTURE AND CONTENT GOVERNANCE

Inspect the existing stack and keep it unless there is a concrete maintenance/performance problem. This is suitable for an accessible, statically deployable site (e.g., Astro + TypeScript + content collections, or the existing equivalent). Do not force a rebuild simply because you prefer another framework. Maintain Github Pages compatibility if that is the deployment architecture.

### Suggested structured collections

Use version-controlled YAML/JSON/Markdown/MDX or existing equivalents, with schemas and tests. At minimum:

- `countries` and `cities` — geographic identifiers, context, data coverage, airshed relationships, sources and facts.
- `populations` — vulnerability, exposure contexts, mechanisms, health/livelihood evidence, relevant interventions.
- `pollutants` and `emissionSources` — accessible definitions and quantitative reference values with time basis.
- `interventions` — type, beneficiaries, evidence, outcomes, finance, prerequisites, cases, caveats.
- `programmes` — project title, country, status, funder, recipient, instrument, dates, amount, outcomes, funding documents.
- `funders` and `organisations` — verified roles, identities, geography, actual relationship links, not promotional copy.
- `studies` — title, authors, DOI, date, abstract written afresh, geography, method, sample, findings, limits, evidence grade.
- `claims` — claim ID, display text, source IDs, observation period, method, confidence, last verification.
- `researchGaps` — question, current evidence, why it matters, study design options.
- `stories` — accessible content with links back to the verified records, avoiding duplicated numbers.
- `glossary` — definitions, analogies, cautions and related concepts.

### Minimal mandatory provenance fields

`id`, `title`, `canonicalUrl`, `sourcePublisher`, `publicationDate`, `dateAccessed`, `geography`, `observationPeriod`, `claimType`, `confidence`, `limitations`, `lastReviewed`, `reviewStatus` and `editorialNotes` as applicable. Not every entity needs every field, but factual records must point to sources.

Add source types: `primary government`, `peer-reviewed`, `multilateral original`, `funder grant record`, `implementer account`, `secondary news`, `other`. Show `source quality` and `directness` independently from factual certainty.

Funding records additionally require `fundingStage`, `amountType` (project cost/committed/approved/disbursed/awarded), `currency`, `nominalYear`, `implementer`, `directRecipient`, `airQualityIntent` (primary/co-benefit) and `relationshipVerification`.

### Validation and editorial controls

- Enforce unique IDs and stable slugs, schema validation, valid ISO dates and outbound links.
- Reject funding records with unsupported amounts or ambiguous funder-recipient relationships.
- Prevent an uncited number on a public page unless it is a mathematically derived display backed by cited inputs and method.
- Add scripts to find broken internal links, missing alt text, uncited claims, stale review dates, duplicate entries, orphaned citations and unknown statuses.
- Add `docs/RESEARCH_LOG.md`, `docs/SOURCE_REGISTER.md`, `docs/EVIDENCE_POLICY.md`, `docs/CONTENT_GOVERNANCE.md` and `docs/OPEN_QUESTIONS.md`.
- Create simple contribution/edit templates for future researchers with source and quality fields.
- If an API is used (for real-time air quality), cache appropriately, document API licenses and limits, and show a graceful failure state. Never pass scraped or unreliable data as official personal health guidance.

---

## 12. REAL RESEARCH WORKFLOW — DO NOT GENERATE 150 PAGES FROM MEMORY

Execute the following in sequence:

**Pass 1 — site inventory and gap analysis**
Read all current routes, content, repository notes and user-supplied design references. Produce a matrix with `existing`, `missing`, `inaccurate/uncited`, `needs editorial simplification`, `opportunity`, `priority`, `effort`. Preserve canonical URLs or add redirects; do not silently break search indexing.

**Pass 2 — source gathering**
Collect original sources with coverage of 2024–2026 where available, retaining landmark older work. Save URLs, dates and method notes; use official project/grant documents for finance. Distinguish search discovery from verified access to a primary source. For scientific studies, read abstracts and methods/limitations before writing claims. Do not scrape whole copyrighted books/reports into the repo.

**Pass 3 — evidence extraction**
Create structured notes for every material source: what was measured, where, when, which population, comparison group/counterfactual, effect size if reported, uncertainty, limitations, policy relevance. Track country comparability.

**Pass 4 — editorial shaping**
Write a plain-English short answer first. Add the deeper evidence tier second. Add cross-links only where they help the reader pursue the question. Copyedit for accessibility and disambiguation.

**Pass 5 — implementation**
Implement templates, components, data schemas, indexes, filters, citations and navigation. Populate with verified content and useful cross-links. Build at least one exemplary end-to-end reader journey:

`Delhi resident / street vendor → exposure and income consequences → source-of-pollution explanation → evidence level → viable municipal/occupational intervention → who has funded something similar → what remains to be tested.`

Build a second journey:

`Foundation board member → priority opportunity → verified grant/project comparisons across India/Bangladesh/Indonesia → intervention trade-offs → financing pathway → evaluation/maintenance safeguards → source evidence.`

**Pass 6 — QA and public-interest review**
Test factual traceability, stale data, mobile performance, accessibility, language, links, scientific caveats, SEO, deployment, security/privacy and consistency. Use real navigation and keyboard tests; do not claim tests you have not run.

**Pass 7 — delivery**
Create a concise implementation report listing what changed, actual sources used, public URLs/routes, data counts verified, test status, limitations and next research priorities. Never say "complete" if evidence records are placeholders.

---

## 13. AMBITIOUS BUT HONEST COVERAGE TARGETS

Targets for a mature regional edition; phase them instead of filling gaps with imagined data:

- 1 very strong Delhi/NCR flagship guide, plus substantial India state/urban research.
- 8 full priority country dossiers; 7 additional lighter South/Southeast Asian country comparisons.
- 15–20 useful city/airshed profiles, subject to comparable evidence.
- Preserve and enrich the **existing 15 population/livelihood profiles** before adding new categories (avoid duplicating them).
- Preserve the existing India intervention entries, add evaluable regional implementation examples and mature toward 40–60 **distinct verified** intervention entries; do not overwrite the existing Fund now/Test first/Not recommended decisions without new evidence and a recorded reason.
- 25–40 **verified** funded programme examples across philanthropy/public/development finance; expand only if original evidence is available.
- 15–25 verified funder/intermediary profiles, correctly labeled by type and grant relationships.
- 80–120 curated research/source records as an initial evidence backbone, with real citations and deduplication; longer-term ambition beyond 150.
- 15–25 clearly written evidence gaps with concrete learning implications.
- A searchable glossary and a short, coherent introductory journey.

Track completeness counts in a generated, transparent **Coverage & Quality Dashboard**: verified records, countries, sources, datedness, citation coverage, weak evidence flags, open review tasks. No public vanity metrics.

---

## 14. SOURCE STARTER REGISTER — OPEN AND VERIFY THESE BEFORE WRITING

**Global health and methods**

- WHO, *Global Air Quality Guidelines*: https://www.who.int/publications/i/item/9789240034228
- WHO, health effects of air pollution, 2026 technical brief: https://www.who.int/publications/i/item/B09563
- Health Effects Institute / State of Global Air 2025: https://www.stateofglobalair.org/resources/report/state-global-air-report-2025
- State of Global Air regional Asia evidence: https://www.stateofglobalair.org/resources/asia
- State of Global Air interactive data: https://www.stateofglobalair.org/data

**South Asian air sheds and countries**

- World Bank, Nepal Clean Air and Prosperity Project, **$52 million credit plus $5 million RAP grant**, announced 11 March 2026: https://www.worldbank.org/en/news/press-release/2026/03/11/world-bank-supports-nepal-s-clean-air-and-prosperity-project-to-reduce-air-pollution-from-industries-strengthen-air-qual  — verify financing components and progress directly in project records.
- World Bank, Pakistan **Punjab Clean Air Program**, **$300 million** concessional loan, March 2025: https://www.worldbank.org/en/news/press-release/2025/03/27/pakistan-world-bank-supports-punjab-s-smog-mitigation-action-plan-with-300-million-concessional-loan ; official implementation portal https://pcap.punjab.gov.pk/introduction . Do not present approved objectives as achieved results.

- World Bank, *Striving for Clean Air*: https://www.worldbank.org/en/region/sar/publication/striving-for-clean-air
- World Bank, *A Breath of Change* IGP-HF 2025: https://www.worldbank.org/en/news/press-release/2025/12/15/clean-air-solutions-can-improve-lives-of-nearly-one-billion-people-across-south-asia
- World Bank, India clean-air programme 2026: https://www.worldbank.org/en/country/india/publication/catalyzing-clean-air-in-india
- World Bank, Nepal clean-air report: https://www.worldbank.org/en/news/press-release/2025/06/17/air-pollution-is-the-number-one-health-risk-factor-in-nepal
- World Bank, Bangladesh Clean Air Project: https://www.worldbank.org/en/news/press-release/2025/06/18/world-bank-helps-bangladesh-improve-energy-security-air-quality
- World Bank, IGP-HF programmes: https://www.worldbank.org/en/brief/2025/12/09/air-quality-management-in-the-indo-gangetic-plains-and-himalayan-foothills

**Southeast Asia and practical programmes**

- **Start here for the region:** Clean Air Fund + Institute for Global Environmental Strategies, *A Clean Air Platform for Southeast Asia*, **9 November 2026**: https://www.cleanairfund.org/resource/clean-air-platform-southeast-asia/ — maps regional air-quality policy, governance and civil-society gaps; do not misclassify the report itself as an awarded programme.
- Thailand, government-described **Zero Burn to Earn** agricultural-residue initiative, July 2026: https://www.thailand.go.th/useful-information-detail/mhesi-drives-zero-burn-to-earn-model-to-tackle-northern-haze-and-turn-farm-waste-into-income — verify implementation uptake, yields and outcomes rather than assuming impact.
- Viet Nam, WHO/UNDP commentary on action and policy 2026–2030: https://www.who.int/vietnam/news/commentaries/detail/air-pollution-in-viet-nam--turning-policies-into-action — distinguish announced policy commitments from enforcement.
- Philippines, Clean Air Asia **E-Mobility ASAP**, 2023–2027 programme: https://www.cleanairasia.org/projects/e-mobility-asap — inspect project scope, implementing partners, funders and actual progress.

- Asian Development Bank, *Air Quality in Southeast Asia: Status, Trends, and Priority Interventions Across Eight ASEAN Cities* (March 2026): https://www.adb.org/publications/air-quality-southeast-asia
- ADB Asia Clean Blue Skies / regional programme: https://www.adb.org/projects/58076-001/main
- Clean Air Fund Indonesia: https://www.cleanairfund.org/geography/indonesia/
- Clean Air Fund, community-led monitoring: https://www.cleanairfund.org/news-item/lessons-community-led-air-monitoring/
- Clean Air Fund, community waste-burning programmes: https://www.cleanairfund.org/news-item/communities-waste-burning/
- CCAC, Cambodia rice-straw management: https://www.ccacoalition.org/projects/cambodia-scaling-integrated-rice-straw-management-reducing-black-carbon-emissions
- CCAC, Indonesia waste-burning programme: https://www.ccacoalition.org/resources/reducing-open-burning-waste-through-clean-oceans-through-clean-communities-clocc-programme-indonesia

**Funding and grantees**

- Wellcome, **PREDICT-ASIA grant award 2025**, research into pollution and climate-health interactions: https://wellcome.org/research-funding/funding-portfolio/funded-grants/pollution-and-rising-environmental-drivers-illness — research grant, not evidence that the health impacts have already improved.
- Clean Air Fund, India project example, **Mahila Housing Trust + Help Delhi Breathe** working with women construction workers: https://www.cleanairfund.org/case-study/supporting-women-in-construction-to-campaign-for-clean-air/ — identify what was undertaken, self-reported outputs, and what cannot yet be claimed as a causal result.

- Clean Air Fund, grants: https://www.cleanairfund.org/what-we-do/our-grants/
- Clean Air Fund, 2026 philanthropic funding: https://www.cleanairfund.org/resource/philanthropic-foundation-funding-2026/
- Clean Air Fund, 2026 global air-quality funding: https://www.cleanairfund.org/resource/air-quality-funding-2026/
- Clean Air Fund, India portfolio: https://www.cleanairfund.org/geography/india/
- Clean Air Fund, reported impact: https://www.cleanairfund.org/what-we-do/our-impact/
- World Bank, financing/project status portals: https://www.worldbank.org/ and https://financesone.worldbank.org/

**Occupational/livelihood research leads**

- Delhi outdoor workers epidemiology: https://pmc.ncbi.nlm.nih.gov/articles/PMC9200945/
- Occupational respiratory health among Chennai street vendors: https://pubmed.ncbi.nlm.nih.gov/42399879/
- The 2026 CHI work on marginalized livelihoods and pollution-related information/closures: https://doi.org/10.1145/3772318.3791369

**Key caution:** Do not automatically call a report's title or a data portal "the evidence". Read it, verify the specific claim and record the original observation period. Some sources mix modeled burden, monitored concentration and intervention case studies.

---

## 14A. REQUIRED CROSS-REGIONAL CASE STUDIES AND EDITORIAL QUESTIONS

Use the following **research starting points** (not pre-written claims) as initial cross-links between a daily experience, an intervention, an institution and a funding mechanism. Each must become a real, cited case card **only when verified**:

| Case | Reader's practical question | Intervention/funding research | Key caution |
| --- | --- | --- | --- |
| Delhi, India: worker payment during GRAP restrictions | "If work is stopped to reduce pollution, who replaces my wages?" | Worker registration, BOCW entitlements, compensation, municipal/employer duties, India's original PF1 | Avoid treating economic loss from restrictions as the same as pollution-induced illness |
| Dhaka, Bangladesh: diesel buses and industrial smoke | "What would make the air on my commute cleaner?" | World Bank-approved Bangladesh Clean Air Project, buses, inspection centres, monitoring, DoE institutional capacity | Approved project emissions estimates are not measured improvement yet |
| Kathmandu/Terai, Nepal: local and regional sources | "How much pollution arrives from elsewhere, and how can local industry clean up?" | Nepal 2026 Clean Air and Prosperity credit/grant, brick/cement industry, cross-border data and compliance | Separate local controls from external airshed contributions |
| Lahore/Punjab, Pakistan: smog and crop burning | "Why do winter restrictions keep returning?" | 2025 Punjab Clean Air Program, crop-residue alternatives, transport, health/worker outcomes | Published programme target is not a verified realised result |
| Jakarta, Indonesia: urban transport, local exposure and waste burning | "What does a city need beyond more air monitors?" | Clean Air Fund country programme; government policy, Vital Strategies, transport and waste research | Do not imply grant relationships without original programme documents |
| Northern Thailand/Chiang Mai: agricultural livelihoods and haze | "Can farmers earn money without burning fields?" | Government Zero Burn to Earn, residue markets, local farmer incentives, seasonal health consequences | Do not present unverified income gains as measured |
| Hanoi, Vietnam: urban growth and air pollution | "Can cleaner transport and building enforcement change city air?" | WHO/UNDP policy analysis; Hanoi government plans; air-quality monitoring and emissions control | Announced plans, statutory rules and delivered impact are different stages |
| Metro Manila, Philippines: transport systems | "How can cleaner transport reach people who cannot buy a private electric vehicle?" | Clean Air Asia E-Mobility ASAP; delivery, finance, accessibility and workforce transition | Electric mobility climate benefits are not automatically equivalent to measured street-level air quality benefits |
| Cambodia: rice-straw burning | "What makes non-burning residue management economically viable?" | CCAC-funded integrated rice-straw management and black-carbon reduction | Verify whether project is awarded, in delivery, or evaluated |

**Comparative research questions required:**

1. Why do some regions have large clean-air financing commitments but comparatively little community-level implementation evidence?
2. How much pollution is transported across cities/borders, and what action must happen at the *airshed* scale versus the ward/city scale?
3. Which successful interventions depended on enforcement and public budgeting rather than technology procurement alone?
4. What is the evidence that cleaner production changes worker exposure, labour conditions and take-home pay?
5. Which form of capital builds the enabling conditions for others to invest or regulate, and who ultimately covers maintenance?
6. What happens when an intervention protects people indoors but leaves informal outdoor workers and the polluting sources untouched?
7. Does the same intervention transfer across different meteorology, fuel mix, market structure and informal labour conditions?

**Funding-map classification rules:** Create separate fields for `announced`, `board-approved`, `legally committed`, `disbursed`, `operating`, `completed`, `evaluated` and `results measured`. These are not a single linear status field; approval stage, operational stage and evidence stage are three different dimensions. Funding instrument can be grant, credit/loan, guarantee, technical assistance, public budget, prize, equity or unknown. Show whether an amount is project total or donor share. Never claim an open call based on a historical award.

**Actual source context to retain:** Clean Air Fund's *The State of Global Air Quality Funding 2026* describes **international development funding, 2020–2024**; its *Philanthropic Foundation Funding for Clean Air 2026* covers a different philanthropic reporting base and period. Never combine these totals, time windows or denominators. Record source definitions before drawing any chart.

---

## 15. FIRST BUILD SPRINT — IMPLEMENT IN THIS ORDER

1. Audit the **existing live and GitHub Pages site** and report the actual source→CSV/Markdown→generated-page pipeline; read all four controlling briefs, list current exact pages, counts, claims, downloads, deployment commands, issues and gaps. Do not create duplicate datasets.
2. **Preserve** the existing accessible masthead, responsive navigation, typography and Clean Air design tokens; improve only audited faults. Do not initiate a rebrand or framework rewrite.
3. Add a public-facing layered `Start here` and glossary **on top of the existing crisis explanation**; preserve and link to existing detailed definitions of AQI, PM2.5 and exposure rather than recopying them.
4. Enrich the **existing** Delhi/NCR hub and three priority people/livelihood journeys (street vendors, children/schools, and waste or brick-kiln workers), each with linked existing claim IDs, incremental evidence and honest uncertainty.
5. Add regional filtering, verified examples and comparison to the **existing** `What works` library; preserve its individual interventions and judgements, and clearly classify source reduction versus exposure protection.
6. Implement `Funding & action` with at least 8 fully verified case studies representing multiple financial instruments; include Bangladesh and Jakarta and an Indian city example if the original programme documents support them.
7. **Extend the existing** linked claim records, inline footnotes, source and verification registers; validate migration safety and preserve stable IDs.
8. Add Bangladesh, Nepal and Pakistan as the first new shared-airshed dossiers; then Indonesia, Thailand, Vietnam and the Philippines, then Cambodia and secondary comparisons. Attach each to relevant existing population/intervention/funding records.
9. Preserve and date the **four current India portfolio options**, then implement regional decision pathways and a three-intervention comparison with evidence provenance.
10. Add the evidence gaps, community correction workflow, systematic QA and coverage dashboard.

### Acceptance tests / definition of done for the first sprint

- A curious person with no prior air-quality knowledge can understand the issue and navigate to a concrete action within three clicks.
- An external reviewer can find a direct source for every numerical claim and every funded project.
- No page conflates AQI and PM2.5; no site-wide ranking silently compares incompatible sources.
- Each proposed solution shows who must deliver it, what it does and does not do, and how to measure whether it works.
- Funding records distinguish grants, loans, co-benefits, promises and disbursement.
- At least two complete cross-linked reader journeys work on mobile and keyboard.
- First sprint pages contain zero invented funder/project records, lorem ipsum, fake interviews or unlicensed imagery.
- Build, lint, type-check, link checks and accessibility checks run successfully, or failures are reported with reproducible detail.
- The repository contains the audit, evidence policy, coverage dashboard logic, source register and a concise handover guide.

---

## 16. HOW TO COMMUNICATE YOUR WORK BACK TO ME

After inspecting the repository and doing your research, respond in this order. The public site and GitHub repository are known; do not begin by claiming their location is unknown:

**A. What I found:** Actual site routes, existing strengths, critical gaps, stack/deployment, and current design inconsistencies. Be factual about what you could inspect.

**B. The 10x transformation:** Five biggest editorial/product changes, explained as added reader or decision-maker value, not number of features.

**C. What I implemented:** Files and routes changed, source-verified content additions, datasets created, interactions and tests, deploy/build result.

**D. What's verified vs. unknown:** Coverage counts, exact source provenance, gaps and items that still require human source checking.

**E. What a foundation could now learn:** Three illustrative, verified clean-air funding pathways, each with strengths, risks, evidence quality and research gaps — not recommendations based on invented precision.

**F. Next phase:** Highest-leverage remaining countries, funder cases, local partners, data and user-testing improvements in sensible priority order.

**Your test throughout:** Could a parent in Delhi understand this? Could a street vendor recognize the constraints described? Could a foundation trustee use it to ask better grantmaking questions? Could an epidemiologist verify the claims? Could an engineer maintain it six months later?

The output should feel like a carefully reported, understandable public resource — **an atlas of unequal exposure, tested action and the financing needed to improve the air** — not a dense encyclopedia or an unsourced AI-generated dashboard.

**Start now by reading the repository and existing website. Do not ask me to decide the architecture before conducting the audit. Implement and verify as far as tools and evidence allow.**
