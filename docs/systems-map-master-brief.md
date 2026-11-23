# CLAUDE CODE MASTER BRIEF
## THE WEB OF DIRTY AIR: Evidence-led, interactive systems map for Clean Air

**Owner mandate: 23 November 2026.**  
**Existing site:** https://arunbh2.github.io/clean-air/index.html  
**Repository:** https://github.com/arunbh2/clean-air  
**Interaction reference (not a style or code template):** https://beattheheat.asia/#explore  
**Proposed canonical page:** `/clean-air/systems-map/` on GitHub Pages, hence `https://arunbh2.github.io/clean-air/systems-map/`. Confirm pathing in the actual build.  
**Working editorial title:** **The Web of Dirty Air**  
**Lede:** *One source can trigger many consequences. Those consequences can reinforce one another, and no single institution holds every solution.*  
**Permanent Clean Air identity:** *Shared air. Unequal protection.*

## 0. YOUR TASK: RESEARCH, MODEL, BUILD AND VERIFY

You are acting as an interdisciplinary team: air-pollution epidemiologist, atmospheric scientist, systems mapper, social-protection researcher, urban-governance specialist, philanthropic investment architect, investigative evidence editor, accessible data-visualisation engineer and software maintainer.

Create a genuinely useful, evidence-linked interactive **systems map** inside the existing Clean Air website. Do not simply copy a visual graph, paste the Common Shade structure, or draw a decorative web. The product is a research-based **causal and institutional exploration tool** that makes the wicked problem of air pollution understandable to a layperson and operationally useful to a funder, civil-society organisation, policymaker, researcher or AI agent.

Go beyond strategy and mocks: inspect the actual repository; conduct and document primary-source research; create the graph dataset and editorial interpretation; implement the live interactive page, textual alternative, downloads and quality checks; run tests; report verified completion. Never claim a test passed unless it ran.

**Important:** The Heat/Commons Shade map is a reference for **reader interactions**, not a source to copy its proprietary code, illustrations, fonts, site structure, brand or factual conclusions. Develop an original Clean Air map using its own existing design system.

## 1. READ FIRST AND PRESERVE EXISTING RULES

Read the entire current repository and, in particular:

- `CLAUDE.md`
- `docs/site-brief.md`
- `docs/research-brief.md`
- `docs/design-brief.md`
- `docs/clean-air-10x-expansion-brief.md`, if present
- `docs/organisations-10x-brief.md`, if present
- `docs/three-audiences-governance-brief.md`, if present
- `docs/CURRENT_STATE_AUDIT.md`, if present
- all relevant `/research` datasets, analysis/build scripts, existing pages under `/site`, existing tests and CI.

Do not assume every named file exists. If a file is absent, record that fact and proceed using the actual repository as the source of truth. Build within the current static GitHub Pages architecture. Preserve existing routes, source IDs (`Snnn`), claim IDs (`Cnnn`), evidence judgments, date-labelled portfolio options, and research-to-site generation workflow. Append records using the current ID allocator/conventions rather than overwriting old IDs. Do not silently update the existing 22 November 2026 research cutoff. This map uses evidence published by that date unless the owner explicitly revises the cutoff. Show the date visibly and in exports.

Follow Clean Air's own tokens: ink `#1A1A1A`, navy `#141F52`, accent `#E3120B`, links `#2E45B8`, paper `#F5F4EF`, white `#FFFFFF`, muted `#595959`, rule `#D9D9D9`, tint `#EBEDFA`. Its editorial serif and system sans-serif remain authoritative. No Common Shade fonts, styles, banners, graphics, menus, animations or analytics. No Practical Action brand. Use only independently developed original code and legally usable assets.

The site voice is calm, readable and non-accusatory. On public pages avoid prescriptive *should/must*, blame language, rankings, em dashes, decorative AI-style gradients/glows, dramatic unsupported certainty and technology hype. Instructions within this brief can be imperative; published website copy must conform to the site's editorial checks. Do not name identifiable people in illustrative narratives; use clearly marked composites. No invented quotations.

## 2. WHAT THE MAP SHOULD ENABLE

A first-time reader can answer **five questions in under three minutes**:

1. Where does polluted air come from?
2. Why does pollution affect people differently?
3. How can one harm trigger another, and where do the feedback loops arise?
4. Which interventions could interrupt a specific pathway, and what evidence exists that they work?
5. Who can act, who could pay, and what is still unknown?

Three user modes share the SAME graph data:

- **Understand**: plain-language guided journeys and readable explanations.
- **Explore**: interactive systems, consequences, paths, loops, sources and filters.
- **Act and fund**: edge-specific interventions, responsible institutions, delivery partners, funding routes, trade-offs and evidence gaps.

Do not make 'Act and fund' a deterministic intervention simulator. This is an **illustrative, evidence-annotated systems map**, not a quantitative impact model.

## 3. FIRST-PRINCIPLES MODEL: DO NOT CONFLATE SIX DIFFERENT THINGS

Build clear conceptual layers, with visual and data-model distinctions:

**Layer A: Activity and emissions.** Transport, diesel, industrial combustion and processes, brick kilns, coal power, construction dust, household solid fuels, waste burning, crop residue, shipping, wildfire and other context-specific sources. Distinguish primary particulate emissions from precursor gases and other pollutants. Do not assume all sources matter equally everywhere.

**Layer B: Atmospheric processes and ambient concentration.** Secondary PM2.5 formation, weather, inversions, seasonal conditions, geographic transport and shared airsheds. Weather can alter concentrations without changing emitted mass. A city reading is not personal exposure.

**Layer C: Exposure.** Where and for how long people breathe pollution: roadside work, schools, homes, industrial settings, transit and open-air markets; indoor infiltration versus indoor emission sources; personal exposure versus area monitors. Treat short-term and long-term exposure separately.

**Layer D: Outcomes.** Population-specific health effects, symptoms and disease burden. Identify associations, causal evidence and uncertainty correctly. Avoid implying a study on one occupation directly measures another.

**Layer E: Social and economic consequences.** Treatment costs, missed paid days, unpaid care, disrupted schooling, productivity, household vulnerability and effects of pollution-control restrictions. Label every inferred, unmeasured livelihood link as a hypothesis, not a measured impact.

**Layer F: Decisions, institutions and resources.** Legislation, monitoring, enforcement, procurement, infrastructure, public-health services, finance, labour protection, community agency, private-sector provision and cross-boundary coordination. These are **actors and levers**, not automatically evidence of causality.

Crucial distinctions:
- Emissions != ambient concentrations != personal exposure != health outcomes.
- Correlation != causation.
- A source contributing to ambient PM2.5 does not prove it is the primary source at each hotspot.
- A source-apportionment estimate has a place, time, pollutant, method and uncertainty.
- A completed loan or grant is not proof of successful implementation or health impact.
- Evidence for each arrow is not evidence that an entire feedback cycle has been tested.
- An action can potentially influence a relationship without guaranteeing the cycle is broken.

## 4. SYSTEM DOMAINS: RESEARCH THESE TEN, ADJUST IF EVIDENCE DEMANDS

Create a coherent model of approximately ten top-level domains, not ten arbitrary equal buckets:

1. **Emissions and the polluting economy**: transport, kilns, industry, fossil energy, household fuel, waste and agricultural burning.
2. **Atmosphere and shared airsheds**: secondary pollutants, winds, inversions, seasonal transport, cross-border pollution.
3. **Cities and infrastructure**: land use, mobility, streets, construction, waste systems, urban form and public services.
4. **Homes, schools and workplaces**: indoor and outdoor microenvironments, occupational exposure, infiltration and limited options for avoiding pollution.
5. **Health and health services**: exposure-linked illness, vulnerable life stages, clinical capacity and prevention.
6. **Work and livelihoods**: outdoor workers, informal enterprises, industrial workers, earnings, productivity and continuity during restrictions.
7. **Household finances, care and education**: expenses, unpaid care, learning interruption, debt, energy affordability and social protection.
8. **Agriculture, land and ecosystems**: residue management, wildfire smoke, land practices, black carbon where grounded, ecosystem consequences.
9. **Governance, accountability and public information**: standards, monitoring networks, source attribution, enforcement, civic participation, coordination.
10. **Finance, markets and distribution of costs**: public budgets, lending, philanthropy, transition finance, technology markets, distributional equity and investment barriers.

These domains are a starting taxonomy, not a claim that every location exhibits every relationship. Keep cross-cutting pollutant, geography, season, population and timescale tags.

## 5. RESEARCH APPROACH: START WITH EXISTING EVIDENCE, THEN EXTEND

Map the current Clean Air evidence inventory before searching externally: community profiles, consequence-pathway register, interventions, organisations, grants and decision pathways. Do not duplicate existing claims. Then conduct a source-led regional scan.

Suggested starting references to inspect **at the actual relevant passage**, not as automatic proof of any edge:

- WHO Global Air Quality Guidelines (2021): https://www.who.int/publications/i/item/9789240034228/
- World Bank, *Striving for Clean Air: Air Pollution and Public Health in South Asia*: https://www.worldbank.org/en/region/sar/publication/striving-for-clean-air
- World Bank, *A Breath of Change: Solutions for Cleaner Air in the Indo-Gangetic Plains and Himalayan Foothills*: https://www.worldbank.org/en/region/sar/publication/a-breath-of-change-solutions-for-cleaner-air-in-the-indo-gangetic-plains-and-himalayan-foothills
- Health Effects Institute / State of Global Air: https://www.stateofglobalair.org/resources/report/state-global-air-report-2025
- Health Effects Institute, Database of South Asia - Air Pollution and Health (DoSAAH): https://www.stateofglobalair.org/news-events/database-south-asia-air-pollution-and-health-dosaah
- UNEP, Actions on Air Quality in Asia and the Pacific: https://wedocs.unep.org/items/80e17444-c4d4-4703-84e5-57ff96f109e2
- Relevant peer-reviewed source-apportionment, exposure, health, economics, occupational and impact-evaluation studies for each setting.

Prioritise India with Delhi/NCR as the anchor, then investigate evidence-transfer limits and differences in Bangladesh, Nepal, Pakistan, Indonesia, Thailand, Vietnam and the Philippines. Use specific settings where justified: Indo-Gangetic Plain, Dhaka, Kathmandu Valley, Lahore/Punjab, Jakarta, Chiang Mai/northern Thailand and Southeast Asian urban/agrarian airsheds. Do not imply comparable exposure, source mixtures or policies merely because two places are in Asia.

For each candidate edge: locate the passage or table that supports it; record source ID, claim ID, quote or tight passage pointer, geography, dates, population, pollutant, study design, limitations and precise claim wording. Store original quoted spans internally for auditing, but respect copyright in public displays. Classify evidence using the existing Clean Air categories: **Strong**, **Moderate**, **Limited/mixed**, **No adequate evidence found**, and independently rate (a) the pathway and (b) the effect of each intervention. Do not represent abstracts or search snippets as full-text verification. A source page merely loading is not a passage check.

Prepare a research ledger with accepted, contested and rejected edges. Record which tentative loops were **not** accepted and why. Keep a research queue of unanswered questions.

## 6. THE GRAPH: CONSEQUENTIAL LINKS, NOT DECORATIVE CONNECTIONS

Create a canonical machine-readable directed, typed graph. Study the actual repo's data format and choose a simple, maintainable representation (JSON/CSV/Markdown in `/research`, with derived output files). Proposed record families:

- `systems`: stable ID, title, short plain-language description, optional geography.
- `nodes`: stable ID, system, label (short), explanation (two sentences max), type [source, concentration, exposure, outcome, social effect, institutional condition], pollutant/population/geography/timescale tags, evidence IDs, status.
- `edges`: stable ID, from, to, mechanism, direction [increase/decrease/conditional], relation_kind [causal, associative, mechanism, reasoned_hypothesis], **strength-of-evidence category**, source/claim IDs, passage locators, geographic/temporal relevance, uncertainty, public wording, reviewer status.
- `cycles`: stable ID, title, **ordered closed path** referencing existing edges, why feedback occurs, cycle-level confidence (separate from its component edge strengths), contexts where it operates, caveats, linked levers.
- `levers`: stable ID, action, targeted edges, mode [source reduction, exposure protection, healthcare, livelihood support, governance/financing], implementer requirements, local relevance, cost category when sourced, timescale, possible adverse trade-offs, outcomes to measure, separate intervention-effectiveness rating, mapped organisations.
- `actors`: IDs linking existing organisations, government functions, communities, firms, health providers and funders; do not invent relationships.
- `funding`: link to existing verified projects/finance records, with committed/disbursed/implemented/results status retained.
- `journeys`: curated ordered, sourced sequences for a lay reader.

Exact field names can adapt to the repository's conventions. **Do not create a competing evidence store or alter the semantics of existing C/S records.** Relationships should resolve to current entities by stable identifiers, with forward compatibility for future regional records.

Validation is mandatory:

- No dangling node, edge, claim, source, institution, intervention or project references.
- Directed cycles must actually close. A chain of harms is not a vicious cycle without a supported feedback path.
- No duplicate IDs; no silent overrides of existing sources or claims.
- No edge marked strong from a snippet-only source, and no intervention rated by the strength of the problem evidence.
- No advertised count differs from the data-derived count.
- No actor, funder or private-sector company appears as a confirmed project partner without evidence.
- Graph and text alternative use the same canonical data, generated at build time.

Produce `docs/SYSTEMS_MAP_METHOD.md` covering model assumptions, connection types, selection/rejection rules, why loops are interpreted rather than proven by default, and limitations.

## 7. CANDIDATE CHAINS AND FEEDBACK LOOPS: INVESTIGATE, DO NOT AUTO-PUBLISH

Start research with the following hypotheses. **They are NOT preverified facts, and several may prove to be chains rather than genuine loops.** Keep unsupported elements as clearly tagged hypotheses or exclude them from the public main graph.

**A. Occupational exposure and income insecurity:** roadside/industrial exposure -> possible illness -> missed work or treatment cost -> reduced ability to avoid hazardous work -> continued exposure. Investigate occupation-specific evidence for each link, especially the final return arrow.

**B. Household energy affordability:** limited access to affordable cleaner fuels -> use of higher-emitting household fuels -> indoor exposure -> illness/expenditure -> constrained energy choices. Distinguish household exposure from ambient emissions and check whether the feedback cycle is empirically supported in context.

**C. Informal waste and open burning:** weak collection and alternatives -> open burning -> local exposure -> harms and local costs -> constraints on waste service investment or compliance. Do not assert the last return link without governance or financing evidence.

**D. Kiln and small-industry transition:** finance/technology constraints -> high-emitting operations -> exposure/emissions -> pressure for restrictions -> business and worker adjustment costs -> further finance constraints. Segment kilns by technology, place, scale and regulatory regime.

**E. Reactive policy and uneven protection:** severe episodes -> emergency restrictions -> differential livelihood effects -> weakened compliance/trust or hardship -> challenges for future protective measures. Treat institutional feedback as context-specific, not universal.

**F. Transport and urban form:** long travel distances / weak mass transit -> high vehicle activity -> concentrations and exposures -> health/economic impacts. A true feedback loop requires a verified return mechanism, such as institutional or travel choices, not simply a long causal chain.

**G. Crop-residue practices and transition cost:** narrow harvest windows, machinery, residue markets and incentives -> burning -> episodic regional pollution -> restrictions/costs -> limited viable alternatives. Verify local practice and do not blame farmers.

**H. Monitoring and invisibility:** sparse monitoring -> uncertain exposure identification -> poor prioritisation of action -> continued exposure. This is plausibly reinforcing institutionally, but mark it an interpretation unless studied end-to-end.

**I. Dust and construction economy:** earthworks/road dust -> local concentration and worker exposure -> health/livelihood impacts; investigate whether construction compliance capacity or operating costs form a feedback loop.

**J. Cross-border airshed coordination:** upwind and downwind emissions -> transported concentrations -> local policy limits -> fragmented action -> continuing pollution. Do not imply that cross-border transport is the sole or dominant source in a particular city without source-apportionment evidence.

**K. Black carbon and climate:** locally relevant combustion -> black carbon emissions -> health-related particulate exposure and climate effects; examine any climate/fire feedback separately and do not present it as a proven local loop without regionally supported evidence.

**L. Protective technology inequality:** wealthier households can afford cleaner indoor air, poorer households have fewer options. This is an unequal exposure/protection pathway, **not automatically a reinforcing feedback loop**.

Target a sufficiently rich research set, perhaps 8-12 well-documented guided chains, 5-10 defensible loops, 20-35 relevant action levers and 8-12 institution categories for a first release. These are planning ranges, never quotas. Publish fewer if evidentiary quality requires it. Never invent numbers to fill a network.

## 8. USER EXPERIENCE: ORIGINAL, CLEAR, DEEP ON DEMAND

**A. Main introduction:** A clear section on the homepage pointing to a dedicated `/systems-map/` page; do not replace the existing site. Opening title: **The web of dirty air**. A two-sentence explanation and one obvious action: **Explore the connections**. Secondary path: **Start with one person's day**. Introductory graphic communicates a few relationships, not the whole network.

**B. Guided journeys (3-5 to start):** Build story-based paths anchored to published evidence and clearly labelled illustrative composites. Suggested prompts:
- 'A street vendor beside a busy road'
- 'A child in a school near traffic or burning'
- 'A family cooking with polluting fuels'
- 'A brick-kiln worker and the cost of changing technology'
- 'A city official trying to act on a regional airshed'

Each journey reveals one relationship at a time: **What happens? -> Why? -> What is known? -> Who bears it? -> Where can it be interrupted? -> Who can act/pay?** Include contextual caveats, not unsupported individual anecdotes. A reader can exit the journey at any time.

**C. Whole systems view:** Initially show 8-10 systems and a selected set of relationships. Add 'Show the whole web' for experienced users. Direct impact vs knock-on effect vs hypothesised relationship vs feedback loop need distinct **labels and line patterns**, not colour alone. Optional overlay for **cross-system links**. Nodes explain themselves when selected; clicking a relationship reveals its evidence.

**D. Explore paths:** Allow a user to choose 'How does [X] connect to [Y]?' and find a path using only published eligible edges. Clearly label it **a possible mapped pathway, not a causal proof or prediction**. If several routes exist, show alternatives and edge uncertainties. If no valid path is known, say 'No checked pathway found yet' rather than making one up.

**E. Explore feedback loops:** Curated loops list with short name, 4-8 step narrative, context, evidence for whole loop, links to edge evidence, breakpoints and limitations. Differentiate verified parts from interpretive return arrows. Show a loop in the graph and in a simple numbered text sequence.

**F. Switch on interventions:** A controlled comparison tool, not an impact prediction. Activating a lever highlights the exact edges it **could** influence, institutions and delivery dependencies, trade-offs, what to monitor, and separate evidence of effectiveness. Wording: 'could weaken this connection' or 'addresses this mechanism', never automatically 'will eliminate X', 'saves Y lives', 'breaks 12 loops' or invented percentage improvements. Offer source-control, exposure-protection, health and livelihood intervention packages; do not equate personal protective measures with reducing emissions at source.

**G. 'Who can act?' mode:** Select a lever and show roles: sets standard, pays, procures, delivers, operates, monitors, evaluates, represents workers/communities. Pull only verified named actors from existing Organisations/Funding Atlas records and separately show generic institutional functions. A named NGO's presence is not evidence of partnership. Integrate private companies and social enterprises only after independent scrutiny of their products, deployment and outcomes.

**H. 'Who pays for what?' mode:** Link relevant verified funding records to actions/implementation responsibilities. Separate grants, public budget, concessional finance, commercial capital, procurement and household payments. Record capital versus operating and monitoring expenses when sourced. No promise of investability, no automatic grant fit, no implied endorsement.

**I. Geography and populations:** Filters for India/Delhi-NCR baseline and, only when researched, other settings. Show 'evidence from [location], local transfer uncertain' when transferring evidence. Filters for street vendors, waste workers, children, pregnant women, older people, industrial workers and households, linked to the actual profile data. Allow pollutant and exposure-setting filters where backed by metadata.

**J. 'Every link as text':** A complete, keyboard-navigable, indexed HTML alternative and downloadable printable text/CSV/JSON. Same order, caveats and citations as the graph. Basic content remains usable with JavaScript disabled.

## 9. DELIBERATE DESIGN AND MOTION

The reference map demonstrates the value of guided paths, layered detail, loops, intervention toggles, institutional overlays and accessible text. Translate those **interaction concepts** into Clean Air's independent editorial language.

- Editorial typography, white/paper background, ink/navy text, restrained red accents, fine rules, generous whitespace.
- No gradient-hero, glowing spheres, uncontrolled particle simulations, decorative spaghetti graphs, over-animated dots, endless auto-looping animations, coloured stripe cards, or heavy shadows.
- Use whitespace, node grouping, simple geometry and quiet motion to support comprehension. Each domain has a readable text label; no dependence on hue alone.
- Diagram and controls must work at 320px width and 200% zoom, with no horizontal scrolling of the *page*. The diagram itself may pan/zoom inside an explicitly labelled bounded viewport with a fully equivalent accessible text/list view.
- Keyboard-accessible nodes/edges, visible focus, Escape closes detail, predictable reading order, correct button semantics, ARIA labels, no hover-only revelations.
- Touch controls approximately 44px, pinch/pan where supported, explicit zoom/reset controls; avoid scroll hijacking. Respect `prefers-reduced-motion`.
- Lazy-load graph code and large datasets; do not make the normal homepage dependent on the heavy map bundle. Keep a fallback for weaker devices.
- Provide responsive SVG/Canvas only after evaluating accessibility/performance and the repo's existing stack; avoid an unnecessary framework migration. If Canvas is used, ship the complete HTML text alternative and keyboard-operable controls.
- Make print legible: a concise systems summary plus loop catalogue and sources rather than a microscopic full-network image.
- Every interaction has a job: reveal a path, isolate a loop, expose an uncertainty, locate an intervention or identify an accountable role.

## 10. FUNDERS, NGOS, PRIVATE SECTOR AND PARTNERSHIP INTELLIGENCE

The map must be structurally connected to the expansion of `/organisations/`, `/organisations/funding/`, `/what-works/`, `/people/` and the evidence library.

When a reader activates a lever, display:

1. **Problem edge:** precisely which emissions/exposure/social/institutional relationship it targets.
2. **Possible action:** what changes in practice; whether it tackles the source or protects people while sources persist.
3. **Who could act:** functions by type, not just named institutions.
4. **Who's documented doing related work:** verified NGOs, community groups, government bodies, researchers, firms and social enterprises, linked to real existing organisation profiles.
5. **Who has funded related work:** verified grants/loans/procurement links, with dates and financial status where known.
6. **What has been measured:** emissions, ambient concentrations, exposure, health, income, service delivery; distinguish output from outcome.
7. **What could go wrong:** displacement of pollution, social costs, lost work, maintenance, low compliance, technology failure, inequitable access.
8. **What remains unproven:** specific research or pilot measurement that would change a decision.

Each actor or funder appears only with verified role and clear scope. No ranking, no invented partnership, no assumption a funded initiative succeeded. Design for the future when the Organisations Atlas contains many more actors; do not hard-code its current size.

## 11. MACHINES AND MAINTAINERS GET THE SAME TRUTH

Generate public machine-readable exports from the canonical graph, e.g. `/systems-map/data/graph.json`, `/systems-map/data/nodes.csv`, `/systems-map/data/edges.csv`, `/systems-map/data/loops.json`, `/systems-map/data/levers.json`, plus `/systems-map/index.md` and `/systems-map/method/`. Choose actual output paths compatible with the site's build.

Any existing `/llms.txt`, `/llms-full.txt`, `/for-ai/`, `/sitemap.json` or similar feature should be updated **only through its canonical generation workflow**. If absent, do not invent a redundant competing system; follow the existing governance brief or document the smallest reliable extension. Ensure downloads guard against spreadsheet formula injection. Include dataset version, evidence cutoff, schema version, licence/reuse limits, attribution and date of generation. Do not apply a broad CC BY licence to third-party material without rights.

The JSON should enable another researcher or AI to answer, with the same caveats as the page: 'Which relationships connect brick kilns to worker health?'; 'Which levers target waste burning in Delhi?'; 'Which reported programme targets this edge in Dhaka?'; 'Which loops have only emerging evidence?'.

Build validators for schema, IDs, graph integrity, source/claim existence, cycle closure, evidentiary statements, intervention effects, broken links, missing outputs, and equivalence between rendered site and generated text/data. Add checks to the existing build/CI, retaining previous tests. Include a small test fixture with an intentionally bad link/ID/edge to demonstrate that each validator actually fails when required.

## 12. PHASED EXECUTION WITH NON-NEGOTIABLE OUTPUTS

### Phase 1: Audit and architecture
Inventory current data, repository routes, available design patterns, build scripts, tests, and any existing paths/graph elements. Write `docs/SYSTEMS_MAP_AUDIT.md` identifying reuse opportunities and evidence gaps. Only then choose graph library/render strategy and canonical schema.

### Phase 2: Rigorous systems research
Research at passage level, derive domains, nodes, edges, candidate feedback cycles, interventions and actors. Add accepted records to `/research` in current conventions, preserving all existing IDs. Build a rejected/uncertain edge ledger. Create public methodology and caveat statements.

### Phase 3: Content and information design
Write the introductory experience, node/edge summaries, 3-5 guided journeys and plain-language loop catalogue. Each statement links back to its source or is clearly labelled as interpretation. Make the default view simple enough for a teenager to understand without having to know 'PM2.5', 'airshed' or 'causal loop' beforehand.

### Phase 4: Website implementation
Build the interactive map under `/systems-map/`, add a strong homepage gateway and links from People, What Works, Organisations and Evidence. Maintain working legacy pages. Add all specified exploration features that the sourced dataset can support. If a feature cannot honestly be offered, include a transparent limitations note rather than fake functionality.

### Phase 5: Verification
Run repository build/tests, graph validators, checks for source IDs and public claim wording, browser-level functionality, keyboard navigation, 320px mobile view, 200% text zoom, touch interactions, print styling, no-JS fallback, reduced motion and slow connection/load size. Capture actual screenshots if browser tools exist. Log tests that could not run.

### Phase 6: Completion report
Provide a concise but exact report covering:
- Routes and files created/changed.
- Number of evidence-backed domains, nodes, edges, cycles, levers and actors (computed from data, never invented).
- Research sources added, source/claim IDs linked, pathways excluded for weak evidence.
- Navigation, accessibility, download and agent outputs implemented.
- Automated checks and browser tests actually executed, and whether they passed.
- Unresolved uncertainties, licensing issues, broken external links, and improvements not yet done.
- Which named actor/funder connections are verified and which remain generic or absent.

## 13. DEFINITION OF DONE: TEST THE READER'S ACTUAL QUESTIONS

All of the following need to work from the same factual data and caveats:

1. **A vendor:** 'Why might a day of traffic pollution affect my health and earnings, and where is that effect still unmeasured?'
2. **A parent:** 'What is different between reducing pollution around a school and using an air cleaner inside a classroom?'
3. **A city official:** 'Which interventions can this city control, and which need coordination across the airshed?'
4. **An NGO:** 'Which harms and causal mechanisms are relevant to waste pickers or informal workers, and where is a local evidence gap?'
5. **A foundation:** 'If I support better monitoring, what changes only if institutions actually use the information? What further funding/authority is required?'
6. **A private firm:** 'What independently supported evidence, operating costs and implementation conditions are needed to assess this technology?'
7. **An AI agent:** 'Give the exact documented chain from an exposure source to an outcome, with claims, sources, evidence strength, contextual limits and interventions.'

**Acceptance requirement:** selecting a lever NEVER fabricates an outcome or recolours a feedback loop as definitively 'broken'. Uncertain arrows are visibly uncertain. The evidence details contain actual passage-checked source references. Every visual graph relationship has an equivalent accessible text record. The site remains useful without JavaScript. The new map does not make the homepage slower for readers who never open it.

## 14. THE HIGHER-ORDER DESIGN CHALLENGE

A good map is not measured by how many coloured nodes it contains. It is measured by how many useful questions it lets a person ask and answer without overstating what science knows.

The intellectual test is whether a grantmaker can move from:

**'We want to improve air quality'**

to:

**'Here is the specific emissions-to-exposure-to-harm pathway; here is the intervention edge; here are the relevant actors; here is what each must fund or operate; and here is the evidence we still need before claiming an outcome.'**

That is the purpose of The Web of Dirty Air: make a wicked problem legible while retaining its complexity, uncertainty and shared responsibility.

**Begin with the repository audit, then conduct research and implement. Do not stop at an outline or ask me to choose colours, libraries or a layout unless a genuine blocking dependency arises. Make defensible defaults, document them, and complete the work possible in this run.**
