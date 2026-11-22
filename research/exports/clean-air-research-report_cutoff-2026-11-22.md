# How this study was done

**Research cutoff: 22 November 2026.** Evidence published after this date is out of scope. The 2026–27 winter season was under way at the cutoff, so current-season figures are partial. Seasonal and long-term figures use the most recent complete periods available in each source.

## The question

The study asks where a foundation could reduce the pollution people breathe, protect the livelihoods that depend on that air, and leave behind a service or institution that keeps working after a grant ends. It is organised around five decisions:

- **A.** Which communities and exposure settings merit priority?
- **B.** Which pathways create the greatest avoidable health and livelihood burdens?
- **C.** Which interventions are effective, usable and feasible for the institutions that would run them?
- **D.** What should be funded now, tested first or investigated further?
- **E.** What should not be funded on current evidence?

No technology or programme was assumed in advance. The study separates four kinds of response throughout: reducing emissions, reducing exposure while emissions persist, reducing health consequences, and protecting income and care during illness or restrictions.

## Sources and how they were read

This is desk research. No people or organisations were contacted. Sources were found by web search and, for primary literature, through the Europe PMC database. Each source is recorded in `data/sources.csv` with its URL, publication date, the date it was accessed, its type, and how much of it was actually read:

| Access status | Meaning | Effect on ratings |
|---|---|---|
| `full-text-read` | The document, or the relevant section, was read | Can support any rating |
| `abstract-only` | Only the abstract was available | Findings used as stated; methods not checked |
| `search-snippet-only` | Only a search summary was seen | Claims marked provisional; cannot support a Strong rating |
| `unreachable` | The site could not be reached from the research environment | Claims marked provisional |

Some official sites could not be reached from the research environment. They include `cpcb.nic.in` (TLS failure), several Lancet pages and CEEW's PDF library (blocked), and parts of the Health Ministry's NCDC site (missing files). Where an official document was unavailable, a copy hosted elsewhere was used and recorded as such, or the gap was logged.

Every factual statement in this report carries a claim ID in square brackets, such as [C016]. Each claim ID resolves in `data/claims.csv` to one or more sources, a location in the source, the geography and period it covers, and whether it was read in full or is provisional. A validation script (`analysis/validate.py`) checks that every reference resolves.

## How evidence is rated

Ratings use four labels only: **Strong**, **Moderate**, **Limited/mixed** and **No adequate evidence found**. Every rating comes with a written reason. The study rates two things separately:

1. Confidence that a problem or causal relationship exists.
2. Confidence that an intervention improves outcomes.

Four situations are kept apart:

- absence of evidence;
- evidence of no effect;
- evidence of harm;
- evidence of benefit under conditions that may not transfer.

An intervention is not called ineffective because it has not been studied locally. An unmonitored place is not treated as a low-exposure place.

Funding options are classed:

- **A**: ready to support;
- **B**: promising but needs adaptation and implementation learning;
- **C**: needs proof of concept or stronger causal evidence;
- **D**: not recommended on present evidence.

## Units and measures

The Indian Air Quality Index (AQI), pollutant concentrations, exposure duration and personal exposure are different quantities and are not used interchangeably:

- **Concentrations** are in µg/m³ with their averaging period stated.
- **Emission inventories** (what is emitted), **ambient source apportionment** (what is measured at a monitor), **personal exposure** (what a person breathes), **health burden** and **economic burden** are reported separately.
- **Source shares** from one place or season are never applied to another.

## Limitations

- Earnings evidence for informal workers is thin. The study records gaps instead of filling them with national aggregates.
- Several important documents were read only as abstracts or summaries. Examples are the full Delhi schools trial paper (not yet published at the cutoff) and the HAPIN trial papers.
- Hindi and other local-language sources were searched only lightly. This is a known gap.
- Organisational reporting is used for what organisations say they do. It is not used to establish outcomes.
- Phase 2 of this work will re-fetch every cited URL and flag anything unreachable or unsupported.

## Quality check

Before release, the report was checked against the brief's ten-point checklist:

1. Delhi is a detailed case, not a proxy for all India.
2. Health, productivity, earnings and household welfare are kept distinct.
3. Causal claims match their evidence.
4. Losses caused by policy restrictions are separated from losses caused by illness.
5. Monitoring gaps are not read as safety.
6. Infrastructure options name an operator and recurring finance.
7. Equity is judged by access and outcomes.
8. Existing organisations and obligations are recognised.
9. Recommendations trace back to findings.
10. The report states what not to fund.

The record of that check is in `11-synthesis.md`.

# What people breathe, and what the numbers hide

## Standards and guidelines are not the same thing

India's legal limit for fine particles (PM2.5) is 40 µg/m³ as an annual mean and 60 µg/m³ over 24 hours [C001]. Compliance rules allow the 24-hour limit to be exceeded on 2% of days, as long as it is not breached on two consecutive monitoring days [C002]. The World Health Organization's 2021 guideline is 5 µg/m³ annually and 15 µg/m³ over 24 hours. It also sets stepped interim targets for countries far above the guideline [C003].

India's annual standard is eight times the WHO guideline. It is looser than even WHO's first interim target of 35 µg/m³ [C004]. "Meeting the national standard" and "safe air" are therefore different claims. Evidence from Indian cities shows daily deaths rising with PM2.5 even on days below the national 24-hour limit [C053].

## The AQI is a communication tool, not an exposure measure

India's AQI turns readings for eight pollutants into one number from 0 to 500, in six bands from Good to Severe [C006]. Each pollutant is converted to a sub-index using a rolling 24-hour average (8 hours for carbon monoxide and ozone), and the highest sub-index is reported [C007].

Three design choices limit what the AQI can tell anyone about exposure:

- **The cap.** The index stops at 500. CPCB argues that values above it stay "Severe" and that extending the scale would not change the health advice. The same cap means the index cannot distinguish a bad day from a catastrophic one [C010].
- **The data exclusion.** In November 2026, CPCB acknowledged that hourly particulate readings above 999 µg/m³ are excluded from AQI calculation. The 2015 validation method assumed instruments calibrated to 0–1,000 µg/m³. During extreme episodes those hours appear as gaps and drop out of the 24-hour average [C008]. Reports at the time said 45 of Delhi's 59 stations had missing hourly readings for at least one pollutant. Ministry sources described an internal review with no external expert group yet formed [C009].
- **Averaging.** A 24-hour average describes a place over a day, not a person over a shift.

Taken together, the published AQI can under-describe the very peaks that matter most to people working outside.

## Most of India is not measured

As of March 2026, the national network had 1,646 manual and real-time stations in 603 cities [C011]. Coverage is very uneven:

- An analysis of official data to 2025 found about 40% of districts with no government-operated station, about half of continuous stations delivering stable data, and station numbers only moderately correlated with pollution levels [C033].
- CSE's 2026 State of India's Environment report is reported to estimate that only about 15% of Indians live within 10 km of a continuous monitor [C034]. This figure is provisional pending a reading of the original report.
- In Bihar, the lead investigator of a rural sensor network estimates roughly one regulatory monitor for every 3.5–4 million people [C060]. That network found rural air breaching the national standard on nearly 90% of days [C058].

**An unmonitored district is not a low-exposure district** [C035]. Funding decisions that follow the monitors will follow the metros.

## Overall levels and trends

Satellite-derived estimates put India's population-weighted annual PM2.5 at 41 µg/m³ in 2023. On that estimate everyone lives above the WHO guideline, and 46% live above the national standard [C021]. A different model covering 2009–2019 puts 81.9% above the national standard. Different years, models and spatial methods produce different headline shares, and the two figures are not a trend [C022].

Government reports that 108 of 130 cities in the National Clean Air Programme (NCAP) had lower annual PM10 in FY2025–26 than in 2017–18 [C013]. An independent satellite estimate finds PM2.5 in districts with these cities 10.5% lower in 2023 than in 2017 [C024]. The programme's targets are framed on PM10, the coarser fraction. The fine particles most linked to health are not its target metric [C013].

## Sources: inventories, apportionment and the danger of one number

Three kinds of "source share" are often confused:

- **Emission inventories** estimate what is released.
- **Ambient source apportionment** estimates what is measured at a monitor.
- **Episode modelling** estimates contributions over a few days.

Each answers a different question.

For Delhi, transport's share of the PM2.5 emission inventory has been put at 20%, 39% and 41% by three studies between 2015 and 2018 [C028]. Receptor modelling at Delhi and NCR sites (2016–17) found dust dominant in summer (31–34% of PM2.5) but around 15% in winter. In winter, biomass burning (22%) and secondary particles formed from gases (26%) rose [C025]. Average winter PM2.5 at those sites was 168 µg/m³ [C026]. An earlier IIT Kanpur study found secondary particles the most important single winter component [C027]. Model-based analysis of a ten-day November window found local sources at about 35% of Delhi's PM2.5 in 2025, with vehicles about half of that local share [C029].

None of these numbers is "the" source share of Delhi, and none applies to Patna, Mumbai or rural Bihar. Patna's winter PM2.5 has a large household-fuel component [C061]. Mumbai's has a large marine and secondary component [C065]. Mumbai's study also shows that inventories systematically miss informal sources: receptor modelling attributed 12–20% of particulate matter to industry, while the inventory-based model gave under 1%, because small informal furnaces were not in the inventory [C066]. Plans built only on inventories can miss what workers in informal units breathe.

Across NCAP cities, government attributes 40–50% of PM10 to construction and road dust [C014]. That is a PM10 finding. It should not be read as a statement about the fine particles that drive most health burden.

## Personal exposure: why a fixed monitor understates the street

What a person breathes depends on where they spend their hours:

- In about 180 hours of measurements inside Delhi auto-rickshaws, PM2.5 averaged 190 µg/m³, 1.5 times the simultaneous ambient level. Black carbon was 3.6 times ambient and ultrafine particle counts 8.4 times [C031]. On-road emissions accounted for 30% of in-vehicle PM2.5 but 68% of black carbon and 86% of ultrafine particles [C032].
- Delivery riders measured in Ghaziabad breathed 180 µg/m³ PM2.5 while riding, with benzene above the national standard [C099].

For people who work in traffic, central monitors understate exposure, and they understate it most for the combustion particles that may be most harmful [C052].

## Household and ambient air overlap

Household air pollution from cooking with solid fuels is both an indoor exposure and a source of outdoor pollution. In Patna, the residential sector was modelled at 28% of winter PM2.5 [C061]. In rural Bihar, household biomass is identified as a primary driver [C059].

LPG connections expanded rapidly after 2016, but use has lagged. In 2021–22, 9.6% of beneficiaries took no refill and 56.5% four or fewer, against about seven needed for exclusive use [C036]. Cost, access and women's limited control over household decisions all play a part [C037].

Household, ambient and occupational exposure can be measured in the same person's day. Burden estimates computed separately for each cannot simply be added together.

# Health effects, from established to emerging

Evidence strength differs sharply across outcomes. This section separates what is established from what is suggestive, and Indian evidence from global evidence.

## Established: mortality and cardiorespiratory disease

**Global evidence.** WHO estimates ambient air pollution caused 4.2 million premature deaths in 2019, 89% of them in low- and middle-income countries. Most were from heart disease and stroke [C005].

**Indian modelled burden.** The Global Burden of Disease 2019 analysis for Indian states attributes 1.67 million deaths in 2019 to air pollution, 17.8% of all deaths: 0.98 million to ambient particles and 0.61 million to household air pollution [C016]. Between 1990 and 2019, the death rate attributed to household air pollution fell 64% while that attributed to ambient particles more than doubled [C017].

These are **modelled attributable estimates**. Each depends on an assumed exposure–response curve and a counterfactual level of "clean" air.

**Indian causal evidence.** Two recent studies use Indian deaths directly:

- A ten-city time-series study (2008–2019) found each 10 µg/m³ rise in two-day PM2.5 associated with 1.4% higher daily mortality. Associations persisted below the national 24-hour limit [C053].
- A difference-in-differences analysis of district death registrations (2009–2019) found 8.6% higher annual mortality per 10 µg/m³. It argues that exposure–response functions drawn from low-pollution countries may misstate Indian risk [C019].

The choice of counterfactual changes the answer more than fourfold. The same study attributes 3.8 million deaths over the decade to PM2.5 above the Indian standard, and 16.6 million to PM2.5 above the WHO guideline [C020].

Life-expectancy estimates follow the same logic. Meeting the WHO guideline is modelled to add 3.5 years nationally, 5 years in the Northern Plains and 8.2 years in Delhi [C023]. These are statements about a modelled permanent reduction. They do not forecast any individual's lifespan.

**Judgement: Strong** that PM2.5 raises mortality in India. The magnitude remains uncertain, and the number reported depends on the counterfactual chosen.

## Moderate: pregnancy and birth outcomes

Indian evidence consistently associates maternal PM2.5 exposure with adverse birth outcomes:

- A Tamil Nadu cohort of 1,285 pregnant women measured household PM2.5 directly in each trimester. Each 10 µg/m³ increase was associated with 4 g lower birthweight and slightly higher odds of low birthweight [C049].
- National survey analyses (NFHS-5, 2019–21) linked to satellite exposure report higher low-birthweight and preterm-birth prevalence with rising exposure. Risk was steeper above about 40 µg/m³ and greater in northern districts [C050].
- A second analysis of 208,181 children found 52% higher odds of preterm birth at the highest versus lowest exposure, with a much smaller difference for low birthweight [C051].

Effect sizes vary across studies using the same survey. These designs cannot rule out confounding by poverty, nutrition and household fuel. They also do not identify which weeks of pregnancy matter most.

The one large randomised trial that changed household exposure during pregnancy (HAPIN, with a site in Tamil Nadu) cut personal PM2.5 by about two-thirds but found no significant effect on birthweight [C096]. One reading is that exposure remained well above guideline levels even after the switch [C097]. The trial does not show that pollution is harmless to pregnancy. It shows that partial reduction of one source, in high-ambient settings, may not be enough to move birthweight.

**Judgement: Moderate** that the association exists in India. **Limited/mixed** that any single exposure-reduction measure improves birth outcomes.

## Moderate: children's respiratory health, anaemia and growth

- A national analysis found each 10 µg/m³ of PM2.5 associated with 10% higher anaemia, 11% higher acute respiratory infection and 5% higher low-birthweight prevalence among children. Nitrate, elemental carbon and ammonium were more strongly associated than total mass [C052]. This suggests PM2.5 mass may understate harm from combustion particles.
- In six Patiala villages (3,644 participants), lung function fell during crop-burning periods. FEV1 dropped 16% among boys and 26% among girls aged 10–18 [C068].
- A 2012 CPCB-commissioned study reported lung-function deficits in 43.5% of Delhi schoolchildren against 25.7% in a comparison group. The source could not be retrieved, so this remains provisional [C056].

**Judgement: Moderate**. The associations are consistent but observational, and acute lung-function drops are better documented than long-term lung development.

## Emerging: neurodevelopment and cognition

The most-cited Indian result (an IQ gap between high- and low-pollution sites in Odisha) is a conference abstract without established peer review [C057]. The Delhi schools trial found a marginal improvement in working memory from an education campaign. This tells us about the intervention, not about pollution's effect on cognition [C074].

**Judgement: Limited/mixed** in India. Effect sizes should not be cited.

## Occupational and population-specific evidence

Outdoor informal workers in Delhi show high rates of abnormal lung function in a study with an office-worker control group. Rates were 86% among sanitation workers and guards, 75% among waste pickers and 45% among controls [C082]. Women in every group had lower lung function than men [C084]. The design is cross-sectional, and the groups differ in more than exposure. It is still the strongest Delhi evidence linking informal outdoor work to respiratory impairment.

## What population studies cannot say

None of these studies establishes that a particular person's illness was caused by air pollution. Exposure is usually estimated from satellites or fixed monitors, which may misclassify people who work outdoors. Smoking, household fuel, heat, nutrition and poverty can confound associations. Health outcomes such as lung development, birth outcomes and chronic disease need years of follow-up. Exposure reductions measured over one winter can be used as intermediate outcomes, but they do not by themselves establish a health benefit.

## Health system response

The Health Ministry's National Programme on Climate Change and Human Health reportedly began air-pollution-linked respiratory surveillance in Delhi hospitals in 2017, and has asked states to expand sentinel networks. Its advisory names outdoor workers, pregnant women, children, older adults and people with heart or lung disease as more vulnerable [C087]. These documents were seen only as search summaries. How far the surveillance reaches, and whether it changes clinical practice during episodes, was not established.

# How pollution reaches income, work and household security

National cost estimates are large, but they describe output lost to the economy, not money lost by a household. Air pollution was estimated to cost India US$36.8 billion in 2019 through lost output from premature death and illness, 1.36% of GDP [C018]. As a share of state GDP, the losses were highest in Uttar Pradesh, Bihar, Rajasthan, Madhya Pradesh and Chhattisgarh [C018].

These figures say nothing about a street vendor's takings or a construction worker's debts. This section separates the five pathways through which pollution and its control affect household finances. Every number is listed with its population, place, period, method and limits in `data/economic-estimates.csv`.

## A. Exposure and illness

Pollution can reduce earnings when illness forces people to miss work or work less, adds treatment and travel costs, takes caregivers' time, or interrupts a small business.

**What is measured.** In a Bengaluru garment factory, hourly output fell as fine-particle pollution rose. The effect was larger for complex tasks and older workers, and attentive managers reduced it by reassigning tasks [C045]. This is a measured productivity effect in formal employment. It is not a wage effect, and it does not transfer to self-employed vendors.

**What is self-reported.** In a September 2025 survey of 582 Delhi households, spending rose during pollution months, dominated by medical costs. Coughing, breathing difficulty and eye irritation were the most reported symptoms [C047]. The magnitude appears only in figures.

**What is missing.** No study measuring informal workers' earnings across clean and polluted days, or borrowing after pollution-related illness, was found. Many informal workers keep working while ill because staying home means no income [C086]. Losses may therefore show up as worse health more than as lost days.

## B. Avoidance

Avoiding exposure costs money and time: shorter hours, relocation, protective equipment, filtration, transport changes. The Delhi survey found nine in ten affluent households had air conditioners and that air purifiers are mostly owned by the rich. Fewer than one in ten low-income households had air conditioning [C046]. A large majority in every class reported not wearing masks during severe pollution [C048].

For most low-income workers, the main "avoidance" option is unavailable. They cannot stop working, and private protection is unaffordable.

## C. Pollution-control measures

This is the best-documented pathway, and it is caused by policy, not by illness.

Under Delhi-NCR's Graded Response Action Plan (GRAP), construction is restricted as the AQI rises and fully banned at Stage 4 [C038]. Physical schooling stops for younger children at Stages 3 and 4 [C054]. The Supreme Court ordered in 2021 that affected construction workers be paid from labour-cess welfare funds. It later directed that compensation follow every GRAP closure without a fresh order, and declined to let non-polluting trades continue during the strictest stages [C038][C039].

Delhi announced ₹8,000 per registered worker after the November 2024 closure, and ₹10,000 after 16 days of Stage 3 in December 2025 [C040]. Payment depends on registration with the Delhi Building and Other Construction Workers Welfare Board, and that is where most workers fall out:

- In December 2024, the board's dashboard was cited as showing 1.38 million workers ever registered but only 89,518 active members. 1.29 million memberships had lapsed [C041].
- At four central-Delhi sites surveyed for a court affidavit, 5 of 75 workers were registered, and none had been paid [C042].
- In November 2026, the board said about one lakh workers had been paid. Its website listed about 2.15 lakh registered, and a union told the Supreme Court that about 1,700 workers were still awaiting payment [C043].

These figures come from different dates and definitions and do not reconcile. The pattern is consistent, though: **compensation reaches registered workers, and registration is where migrants and casual workers are lost** [C044]. Nationally, 44% of the construction-welfare cess collected up to November 2022 (₹38,209 crore of ₹87,478 crore) was unspent [C101]. Worker federations blame weak enrolment by welfare boards [C102].

No compensation mechanism covers street vendors, delivery riders, waste pickers or small enterprises whose earnings fall during restrictions. Gig workers describe lost incentives and penalties for logging off [C100]. A social security fund for platform workers came into force under the Code on Social Security in November 2025, but its benefits were still being designed at the cutoff [C103].

## D. Longer-term household consequences

Debt, depleted savings, asset sales, interrupted education and reduced investment in health are plausible consequences of pathways A and C. **No adequate evidence was found** that measures them for air pollution in India. Workers report returning to their villages with their children when construction stops [C043]. School closures of up to 15 days shift learning online, where access is unequal [C054][C055]. Neither has been followed through to household outcomes.

## E. Who gains and who pays in transition

Cleaner production can move costs onto those least able to bear them:

- Converting a brick kiln to zigzag technology costs the owner about ₹40 lakh, reportedly repaid in one to two years through fuel savings [C069]. Workers are paid by piece as family units, often bonded by advances [C071]. How conversion affects their pay and debt is unmeasured.
- Crop-residue machinery subsidies reach farm owners [C093]. The costs to smallholders and labourers are unmeasured.
- Construction bans protect residents' air while workers lose wages [C040].

## Keeping the pathways apart

Earnings lost during a smog episode are not all caused by breathing smog. A construction worker idled by a GRAP ban loses income through pathway C, whatever their health. A vendor who sells less may be losing customers who stay home, not losing capacity. Adding illness costs, restriction losses and national output estimates together would double-count. The evidence base supports a narrower but firmer conclusion. **The best-documented and most avoidable livelihood loss is the one created by pollution control without effective income protection.**

# Communities of fate

"Communities of fate" is used here as a lens, not an epidemiological category. It describes people connected through the air they share, where they work and live, and the services and institutions they depend on. A city's air is shared, but exposure to it, protection from it and recovery from its effects are not. The full group-by-group matrix is in `data/community-impacts.csv`.

## Seven inequalities

| Dimension | What the evidence shows |
|---|---|
| **Exposure** | Roadside and in-traffic work multiplies exposure. Auto-rickshaw passengers breathe 1.5 times ambient PM2.5 and 3.6 times ambient black carbon [C031]. Riders measured at 180 µg/m³ PM2.5 while working [C099]. Workplace exposure rises as class falls [C048]. |
| **Biological susceptibility** | Children, pregnant women, older adults and people with heart or lung disease are named as higher-risk [C087]. Girls aged 10–18 showed the largest lung-function drop during crop burning [C068]. |
| **Ability to avoid exposure** | Private protection is concentrated among the affluent [C046]. Work-from-home advisories do not reach daily-wage workers [C086]. |
| **Access to healthcare** | Low insurance coverage among sanitation workers. Medical costs dominate pollution-month spending for Delhi households [C047]. |
| **Ability to absorb losses** | Construction compensation depends on registration that most migrants lack [C044]. |
| **Voice** | 94% of women construction workers surveyed avoid raising air pollution for fear of losing their job [C089]. |
| **Access to protection and compensation** | Only workers registered with a welfare board are compensated during restrictions. Vendors, riders and waste pickers have no equivalent [C044][C100]. |

## Groups, and how their work is organised

Work relationships determine who has a duty to protect a worker:

- **Wage workers** (sanitation workers, guards, construction labour) have employers or contractors with legal duties, even where these go unenforced.
- **Piece-rate workers** (kiln families, home-based workers, platform riders) are paid per unit, so lost hours are lost income with no buffer.
- **Self-employed workers** (vendors, waste pickers) have no employer to hold responsible.
- **Unpaid family workers** (often women and children at kilns) appear in no payroll [C071].

**Sanitation workers and waste pickers** have the strongest documented respiratory impairment. In a Delhi study with an office-worker control group, abnormal lung function was found in 86% of sanitation workers and 75% of waste pickers, against 45% of controls, with severe impairment in 27% and 17% [C082]. Over 60% of sanitation workers and half of waste pickers did not know about protective equipment. Nearly half of waste pickers burned wood or coal for warmth, and over 30% burned waste [C083].

**Construction workers**, many of them migrants, face site dust and then lose wages when GRAP halts work. Registration determines whether they are compensated [C041][C044]. Women construction workers report feeling unwell on high-pollution days and fear speaking up [C089].

**Drivers, delivery riders and guards** work in the most polluted microenvironments. Combustion particles, which fixed monitors understate, make up most of their extra exposure [C032]. Platform workers lose incentives if they log off [C100].

**Kiln workers** are seasonal migrant families, disproportionately from Scheduled Castes (47% of kiln migrants, against 18.8% of all migrant workers) and Scheduled Tribes (16% against 7.7%) [C072]. One survey found 96% had taken advances, wages withheld for whole seasons, and children working long hours [C071].

**Residents of informal settlements and resettlement colonies** combine outdoor exposure, household fuel and waste burning with little ability to filter or cool their homes [C046]. Tenancy limits what they can change.

**People experiencing homelessness** are exposed day and night. Delhi's winter shelter capacity rises to about 11,000 places in 2026–27. The reported plan lists bedding, water and power but no air filtration, and the shelters close in March [C092].

**Pregnant women and children** carry the most consequential long-term risks [C050][C052]. They depend on schools, health services and adults for protection.

**Home-based workers, people with disabilities and older people** appear in advisories but in almost no Indian research reviewed here. That absence is itself a finding.

## Gender, caste, migration and tenure

The evidence supports four specific observations:

- **Gender.** Women in every occupational group studied had lower lung function than men [C084]. Women's limited control over household decisions constrains consistent clean-fuel use [C037]. Women kiln workers are often unpaid because wages go to the male head of the family [C071].
- **Caste.** Kiln labour, one of the most exposed and least protected forms of work, draws disproportionately on Scheduled Caste and Scheduled Tribe migrants [C072].
- **Migration.** Registration systems tied to paperwork and continuous residence exclude seasonal and recently arrived workers from compensation [C041][C042].
- **Tenure.** Tenants and shelter residents cannot install or maintain protective measures in housing they do not control [C092].

The evidence does not support claims about caste or disability effects on health outcomes from pollution in these settings. Those would require data not found.

## Strength, not only vulnerability

Communities are not only recipients of protection:

- Women trained as AQI ambassadors in Delhi's resettlement colonies became peer trainers and engaged local officials [C088].
- Construction unions have used the courts to establish compensation as a standing obligation [C039].
- Waste-picker organisations produced the occupational evidence used here [C082].

Programmes that treat these groups as sources of knowledge and accountability, not only as beneficiaries, build on capacity that already exists.

# Places: Delhi and five contrasting settings

Six settings were chosen after an initial scan. They were chosen for contrast, not to represent the country. Each is a different kind of unit: a city inside a regional airshed, a state's rural blocks, an industrial cluster, a coastal metro, an agricultural region and a dispersed production sector. Findings, source shares and institutional arrangements from one setting are not applied to another. Each setting's profile and evidence are summarised in `data/settings.csv`.

The brief listed seven selection categories. "A smaller city with limited monitoring" is covered by the rural and small-town Bihar setting, which showed the starkest monitoring gap in the scan. No separate small city with enough evidence was found to stand alone.

## Delhi/NCR: the anchor case

**Why chosen.** Delhi has the deepest evidence base. It is the only setting with a statutory regional commission, an emergency plan that stops work, and court-ordered compensation for the workers it idles.

**Pollution profile.** Winter PM2.5 at sampling sites averaged 168 µg/m³ [C026]. Dust dominates in summer, and secondary particles and biomass burning in winter [C025]. Local sources were about 35% of PM2.5 in the November 2025 episode window [C029]. The AQI cap and data exclusion hide the worst hours [C008][C010].

**Communities.** Construction workers, sanitation workers, waste pickers, vendors, riders, homeless people and residents of resettlement colonies.

**What Delhi shows.** Emergency control has livelihood consequences that are separate from illness [C038][C040]. The protection designed for those consequences reaches registered workers far more often than migrant workers [C041][C044]. Delhi also shows a recurring pattern of visible measures, such as smog towers and anti-smog guns, deployed before evaluation [C077][C080]. Delhi had used only 17% of its NCAP funds by December 2025 [C030].

**What cannot be generalised.** Delhi's source shares, its institutional density, its court oversight and its media attention are not typical. GRAP and its compensation duties apply only in NCR.

## Bihar: Patna and rural blocks

**Why chosen.** Bihar has persistent regional exposure, the weakest monitoring of the settings scanned, and heavy reliance on household biomass. It is also a major origin state for migrant construction and kiln workers.

**Pollution profile.** A low-cost sensor network across all 38 districts recorded breaches of the national standard on nearly 90% of days. Winter PM2.5 in the north-west was around 210 µg/m³ [C058]. The state board disputes the sensors' accuracy, and the investigators cite co-location trials. In Patna, households were modelled at 28% of winter PM2.5, and industry and kilns at about 10% [C061][C105].

**What it shows beyond Delhi.** Pollution is a rural, regional problem that official networks barely see. There is roughly one regulatory monitor per 3.5–4 million people [C060]. Household fuel matters as both exposure and source [C059].

**Limits.** Sensor readings are not regulatory-grade, and Patna's shares do not transfer to rural blocks. No Bihar-specific livelihood evidence was found.

## Singrauli: coal and power belt

**Why chosen.** It concentrates large formal polluters, coal mines and thermal power plants, across two states.

**Pollution profile.** Annual PM10 of 160–167 µg/m³ at two official stations in 2023–24, against a 60 µg/m³ standard. PM2.5 was not reported at those stations [C062]. Black carbon above 200 µg/m³ was measured near plants in a short 2013 campaign [C064].

**What it shows beyond Delhi.** Where polluters are identifiable and formal, accountability can run through regulation and litigation. Residents' allegations of respiratory harm and heavy-metal contamination are before the National Green Tribunal. Official district health data recorded few lung-disease cases at local centres, which points to weak surveillance rather than absence of harm [C063].

**Limits.** No independent community health study was found.

## Mumbai: a coastal metro

**Why chosen.** Mumbai is a western metro with a construction boom, informal industry and a different airshed.

**Pollution profile.** Road dust, linked to Metro and real-estate construction, dominates PM10. Secondary aerosols (22%) and marine sources (26%) make up nearly half of PM2.5 [C065].

**What it shows beyond Delhi.** Emission inventories miss informal sources. Receptor modelling found 12–20% of particulate matter from industry while the inventory found under 1%, because small furnaces were not counted [C066].

**Limits.** No Mumbai-specific worker exposure or earnings evidence was found.

## Rural Punjab and Haryana: the paddy residue belt

**Why chosen.** It is the origin of the most politically visible seasonal source, and it tests who pays for agricultural transition.

**Pollution profile.** Satellite-counted farm fires in Punjab fell to 5,114 in 2025, down 93% from 2021 [C067]. In six Patiala villages, PM2.5 rose by an average of 167 µg/m³ during burning periods, and lung function fell most among adolescents [C068].

**What it shows beyond Delhi.** Burning harms the farming communities themselves, not only downwind cities. Public machinery subsidies of about ₹3,623 crore went mainly to farm owners [C093]. The fall in fires coincided with machinery, enforcement and new uses for straw, and these effects have not been separated [C067].

**Limits.** The evidence is season- and crop-specific, and costs to smallholders and labourers are unmeasured.

## Brick-kiln clusters (Bihar and Punjab examples)

**Why chosen.** Kilns are a labour-intensive, coal-fired production sector with migrant family labour. They are the clearest case of cleaner production meeting precarious work.

**Profile.** India has over one lakh kilns producing about 250 billion bricks a year [C073]. Zigzag conversion reportedly cuts particulate and black carbon emissions by about 75% [C069]. Each Bihar kiln employs 120–150 workers who live on site in temporary housing [C070]. They are disproportionately SC and ST migrants [C072] and often bonded by advances [C071].

**What it shows beyond Delhi.** Cleaner technology can cut emissions while leaving bondage and on-site exposure untouched. No study of workers' outcomes after conversion was found.

**Limits.** Labour evidence comes partly from older advocacy surveys, and regimes vary by state.

## Reading across settings

| Setting | Main exposure route | Best-evidenced harm | Weakest link |
|---|---|---|---|
| Delhi/NCR | Urban plus regional ambient; in-traffic work | Restriction income loss; occupational lung impairment | Earnings for non-construction workers |
| Bihar | Regional ambient plus household fuel | High exposure (sensor) | Credible monitoring; any livelihood data |
| Singrauli | Industrial point sources | Exceedances at official stations | Community health evidence |
| Mumbai | Dust, secondary, marine | Source structure | Worker exposure |
| Punjab/Haryana | Seasonal burning | Acute lung-function falls | Distribution of transition costs |
| Kiln clusters | On-site coal and dust | Labour exploitation | Health and post-conversion outcomes |

# Tracing the consequences, link by link

A pathway is only as well evidenced as its weakest link. This section rates each link separately. The full table, with geography, timescale and alternative explanations for each link, is `data/pathways.csv`. Consequences are classed by what drives them:

- **health-mediated**: illness;
- **behaviour-mediated**: what people do to avoid exposure;
- **market-mediated**: prices, demand and earnings;
- **policy-mediated**: rules and their enforcement.

## P1. Exposure → illness → missed work → lost earnings → borrowing

| Link | Mediation | Confidence | Why |
|---|---|---|---|
| Exposure → illness | health | **Strong** | Mortality and lung-function evidence from Indian data [C053][C082][C068] |
| Illness → missed work or reduced capacity | health/behaviour | **Limited/mixed** | Measured in a formal factory [C045]. Informal workers often keep working while ill [C086] |
| Missed work → lost earnings | market | **No adequate evidence found** | No informal-earnings study located |
| Lost earnings plus medical costs → borrowing | market | **No adequate evidence found** | Medical spending rises in pollution months (self-reported) [C047]. No debt study |

**Alternative explanations.** Heat, festivals, seasonal demand and other shocks coincide with pollution seasons. **Intervention points.** Exposure reduction at work; paid sick leave or health-cost protection. Neither can be sized without measuring links 3 and 4.

## P2. Child illness → extra care → caregiver work interruption → household pressure

| Link | Mediation | Confidence | Why |
|---|---|---|---|
| Child exposure → respiratory infection, anaemia | health | **Moderate** | National survey associations [C052] |
| Child illness → caregiver (mostly women) loses work time | behaviour | **No adequate evidence found** | Not studied in reviewed sources |

**Intervention points.** School and home exposure reduction; childcare continuity. This chain is plausible and important for women's earnings, but it is unmeasured.

## P3. Pollution-control restrictions → work stoppage → income loss → less ability to afford protection

| Link | Mediation | Confidence | Why |
|---|---|---|---|
| Severe AQI → GRAP construction ban | policy | **Strong** | Codified in GRAP; court orders [C038][C039] |
| Ban → wage loss | policy/market | **Strong** | Court-ordered compensation exists because the loss is recognised; workers report returning to villages [C040][C043] |
| Wage loss → unpaid because unregistered | policy | **Moderate** | Dashboard and site-survey evidence [C041][C042][C044] |
| Income loss → less ability to afford protection | market | **Limited/mixed** | Protection devices are concentrated among the affluent [C046] |

This is the best-evidenced chain, and it has the clearest intervention points. **Close the registration gap** so statutory payment reaches those idled. **Design income continuity** for workers outside the construction scheme.

## P4. School closure → unequal alternatives → disrupted learning and care

| Link | Mediation | Confidence | Why |
|---|---|---|---|
| GRAP Stage III/IV → primary classes closed | policy | **Strong** | Directorate circulars; closures up to 15 days [C054] |
| Closure → learning loss larger for children without devices; caregiver time lost | behaviour/market | **Limited/mixed** | Digital gaps plausible; no learning measurement found [C055] |

**Intervention point.** Keeping schools open with in-school protection and behavioural education. The schools trial suggests education is effective, and purifiers need redesign [C074][C075].

## P5. Cleaner-production mandate → transition costs → workers' pay and debt

| Link | Mediation | Confidence | Why |
|---|---|---|---|
| Kiln mandate → owner capital outlay | policy/market | **Moderate** | About ₹40 lakh per kiln, 1–2 year payback [C069] |
| Conversion → changes in workers' pay, debt, exposure | market | **No adequate evidence found** | Not measured [C070][C071] |

**Intervention point.** Attaching labour standards and worker support to conversion, and measuring the result.

## Avoiding double counting

Illness-driven losses (P1), restriction-driven losses (P3) and lost output in national estimates [C018] overlap in time but are different quantities. A worker idled by a ban is not also losing productivity at work that day. A national output loss already includes the earnings of those who die or fall ill. This study therefore does not add them together. It also does not express household losses as shares of GDP.

## What the pathways reveal

Most chains from air to hardship pass through at least one unmeasured link, usually the step from health to money. The exception is the restriction pathway. It is created by policy, recognised in law, and observable in administrative records. That makes it both the most avoidable burden and the most tractable to act on.

# Who already acts, and where the gaps lie

Only activities that could be verified from public documents are recorded. The map in `data/organisations.csv` separates six functions: advocacy, research, monitoring, delivery, financing and enforcement. Claimed outcomes reported by organisations are labelled as self-reports.

## Public institutions

- **Central Pollution Control Board (CPCB).** Runs the national AQI and the monitoring network (1,646 stations) [C011]. It reported to the Green Tribunal on Singrauli [C062], and acknowledged the AQI data exclusion and an internal methodology review in November 2026 [C008].
- **Commission for Air Quality Management (CAQM).** The statutory regional body for NCR and adjoining states. It operates GRAP [C038], directs transport and industrial fuels [C015], and tracks farm fires [C067].
- **National Clean Air Programme (MoEFCC).** Released ₹16,423.55 crore to 130 cities between FY2019 and FY2026, and cities report using 70.5% [C012]. Its targets are framed on PM10 [C013]. Use of funds is uneven: Delhi had used 17% by December 2025 [C030].
- **State boards.** Bihar's board mandated kiln conversion and disputes the accuracy of rural sensor data [C059][C058]. Delhi's committee commissioned the smog-tower evaluation and acted on it [C077].
- **Delhi BOCW Welfare Board.** The payer of GRAP compensation. Its reach is limited by registration [C041][C043].
- **Delhi Urban Shelter Improvement Board.** Runs about 197 night shelters, expanded with winter tents [C092].
- **Health Ministry (NPCCHH).** Respiratory sentinel surveillance and advisories; documents seen only as summaries [C087].
- **Supreme Court.** Not an organisation to fund, but the main source of enforceable worker protection in this field [C039].

## Multilateral and bilateral finance

The World Bank approved about $300 million each for airshed-based programmes in Uttar Pradesh and Haryana in December 2025. The Uttar Pradesh programme includes clean cooking for 3.9 million households [C091]. UNDP, UNEP and Swiss development cooperation have funded monitoring, technical assistance and transboundary work worth tens of crores each [C094]. Large public and multilateral money is going into emission reduction and monitoring. Very little of it is aimed at protecting the livelihoods of people affected by pollution control.

## Research and analysis

TERI, IIT Kanpur, CSIR-NEERI, IIT Bombay and others produced the source apportionment and evaluation studies relied on here [C025][C027][C065][C077]. CSE and CEEW provide policy analysis on Delhi sources, school closures and anti-smog guns [C029][C054][C080]. A research team funded by the International Growth Centre ran the Delhi schools trial [C074]. IIT Kanpur's AMRIT network extended monitoring to rural Bihar [C058]. Research capacity is substantial. Independent evaluation of government measures before they scale is rare. The smog-tower study is the exception that proves its value.

## Civil society and worker organisations

- **Mahila Housing Trust and Help Delhi Breathe**, funded by Clean Air Fund, trained over 75 women construction workers as AQI users and peer trainers, and helped workers register with the welfare board [C088].
- **Chintan** produced the occupational spirometry study of sanitation workers, waste pickers and guards [C082].
- **Health Care Without Harm** is building a network of health workers and about 100 hospitals as clean-air advocates [C090].
- **Construction workers' unions** litigated to make compensation a standing duty [C039] and continue to report unpaid workers [C043].
- **Anti-Slavery International** and others document kiln labour conditions [C071]. **WRI India** supports kiln transition training in Bihar [C069].

## Philanthropic funders

Clean Air Fund is the most visible dedicated funder in the reviewed material. Its India grants span health voice, informal settlements and construction workers [C088][C090]. Bloomberg Philanthropies supported the Patna source-apportionment study [C061]. Globally, funding for ground-level ozone was 0.4% of tracked air-quality funding in 2024 [C095]. Grant sizes for individual Indian programmes were not available in the reviewed sources.

## Gaps across the field

1. **Delivery to affected workers is thin.** Most activity is regulation, research, monitoring and advocacy. Few organisations deliver protection or income support to the most exposed workers, and their outcomes are not independently evaluated [C088].
2. **Statutory money sits unused.** 44% of construction-welfare cess was unspent nationally to 2022 [C101]. Compensation in Delhi reaches a fraction of workers because of registration [C044].
3. **Research does not reliably become implementation.** Evaluations exist for a few measures (towers, school purifiers). Visible but unproven measures keep expanding [C081].
4. **Places without delivery capacity.** Rural Bihar and industrial belts have monitoring disputes and litigation, but few service providers.
5. **Workers rarely take part in decisions.** The government's NCAP summary reviewed here reports on emissions, monitoring and funds but not on livelihoods or affected workers [C012]. Women workers fear raising pollution at work [C089].
6. **Recurring services have identifiable owners.** Welfare boards (compensation), education departments (schools), municipal employers (sanitation workers), DUSIB (shelters) and state health departments all have legal or administrative responsibility. A grant that strengthens their delivery can outlast itself. A grant that replaces them cannot.

No organisation was contacted for this study. Activities are as publicly reported at the cutoff.

# What works, what might, and what does not

Each candidate was assessed against the same questions:

- Which pollutant or pathway does it address?
- Does it reduce emissions, exposure, consequences or income loss?
- Who uses it, and for how many hours?
- What measured performance supports it?
- Who owns, runs and pays for it after a grant?
- Who might it exclude?

The full matrix is `data/interventions.csv`, and the two-dimension ratings are in `data/evidence-map.csv`. Each intervention page follows the same order: what it does, who benefits, evidence, operating requirements, costs and uncertainties.

## Four approaches that cannot substitute for one another

1. **Reducing emissions** is the only lasting solution. It is mostly a public and regulatory task, backed by large public and multilateral budgets [C091][C093].
2. **Reducing exposure while emissions persist** protects specific people in specific places and hours. It never reaches everyone, and it can have side-effects [C075].
3. **Reducing health consequences** depends on health services being ready during episodes [C087].
4. **Protecting income and care** addresses losses that the other three cannot. That includes the losses caused by pollution control itself [C044].

A classroom purifier does nothing for a child's parent who loses a week's wages to a construction ban. Compensation does nothing for that parent's lungs. These approaches complement one another, and none replaces another.

## Not recommended on present evidence

**Outdoor smog towers.** IIT Bombay's independent evaluation of Delhi's Connaught Place tower found particle reductions of about half within 20 m, falling to 12–13% at 109–199 m [C077]. The regulator told the Green Tribunal the towers were ineffective, at about ₹25 crore each to build and ₹15 lakh a month to run [C078]. Early government claims of an 80% reduction did not survive measurement [C079]. *Evidence: Strong that the effect is very limited.*

**Anti-smog guns and water sprinklers for ambient air.** There is no robust evaluation. At Delhi's planned scale they would cover under 0.5% of the city and need 25–90 lakh litres of water a day [C080]. Delhi's 2026 plan nonetheless expands them [C081]. *Evidence: Limited/mixed.*

**Mass distribution of masks.** Fitted respirators reduce exposure, but Delhi's past mass distribution met low use and social norms against wearing them [C085]. Untargeted handouts without fit or replacement offer false reassurance.

**Purpose-built clean-air shelters.** International evidence on shelter use and health benefit is inconclusive [C098]. The people most exposed are working outdoors and cannot leave work to sit in a shelter without losing income [C086]. *Evidence: No adequate evidence found.* Any exposure reduction indoors is better placed inside services people already use (see below).

**Crop-residue machinery as a philanthropic purchase.** Public subsidy is already large (₹3,623 crore) [C093]. Fire counts fell, but the roles of machinery, enforcement and straw markets have not been separated [C067]. There is no capital gap for philanthropy to fill. There is an evaluation gap on who bears the costs.

## Ready to support

**Making statutory compensation reach the workers it is meant for.** The duty to compensate construction workers idled by GRAP exists by Supreme Court order, and the money exists in welfare cess funds [C039][C101]. What fails is registration and renewal. Only 89,518 of 1.38 million workers ever registered in Delhi were active members in December 2024 [C041], and a site survey found 5 of 75 workers registered and none paid [C042]. Philanthropy can fund:

- registration and renewal drives;
- tracking of payment after each closure;
- legal support;
- independent reporting on who is missed.

It should not fund the transfers themselves. *Problem evidence: Strong. Intervention evidence: Limited*, but the mechanism is short and its outcome (payment received) is directly observable in board records. **Operator:** worker organisations and NGOs, with the welfare board as payer. **Recurring cost:** seasonal case workers, to be absorbed by the board over time.

**Enrolling waste pickers and sanitation workers in existing entitlements.** Since 2024–25, waste pickers can receive occupational ID cards, PPE kits and PM-JAY health insurance through the NAMASTE scheme [C106]. The 2016 waste rules already required municipalities to issue ID cards, but most did not [C107]. The OSH Code now gives employees a free annual health check-up [C109]. Self-employed waste pickers have no employer to whom that duty attaches, so their route runs through schemes [C110]. Philanthropy can fund enrolment support and tracking of benefits received, and press for municipal compliance. It should not pay premiums or buy kits. *Problem evidence: Strong. Intervention evidence: Limited*, but enrolment is directly observable. **Operator:** waste-picker and sanitation worker organisations, with municipalities and the scheme as providers.

**Air-pollution education in school curricula.** A two-year cluster-randomised trial in 180 Delhi classes raised awareness and protective behaviour, reduced self-reported breathing difficulty, and spread through peer networks. Effects weakened in the second year [C074][C076]. It is low-cost and runs through an existing school system. *Evidence: Moderate.* The full paper was not yet available at the cutoff, and a second setting is needed to test transfer.

**Independent evaluation and spending accountability.** Visible measures have repeatedly scaled before evaluation [C079][C080]. Where evaluations were done, they changed decisions: Delhi's regulator acted on the tower study [C077]. Funds are under-used in places, for example Delhi's 17% use of NCAP funds [C030]. A standing, independent evaluation facility, with agreed government data access and use, is low-cost. It improves every other public investment in the field.

## Test first

**Classroom HEPA purifiers.** In the same Delhi trial, purifiers significantly reduced classroom PM2.5. Yet children in purifier classrooms did worse than those receiving education alone on working memory in year one and spirometry in year two. They also reduced protective behaviour outside school [C075]. Benefit depends on:

- room sealing, clean-air delivery rate and occupancy;
- hours of use and maintenance;
- the behaviour of the children using the room.

Purifiers filter particles, not gases. **Test only** as redesigned pilots that pair filtration with behavioural messaging, with the education department committing to running costs (filters, electricity, servicing).

**Occupational protection for sanitation workers, waste pickers, guards and riders.** The problem evidence is strong [C082][C099]. Fitted respirators work in principle, but adherence in heat and in informal work is unproven in India [C085]. Pilot fit-tested respirator programmes with employer or municipal co-payment, shift timing away from early-morning inversions, and periodic lung-function checks through public schemes. Measure personal exposure and adherence.

**Filtration inside existing night shelters, childcare centres and clinics.** These buildings already have operators, staff and occupants present for many hours. DUSIB alone runs about 197 shelters [C092]. There is no Indian evaluation. Porta-cabins and tents may leak too much for filtration to matter, and fire and ventilation trade-offs need design. Pilot in permanent buildings, with the operator committing to running costs.

**Low-cost sensor networks tied to action.** Monitoring is not exposure reduction. Rural Bihar's network made exposure visible where regulators had almost none [C058][C060], but its credibility is disputed and no triggered action is documented. Fund only with three things in place: calibration against reference monitors, a named decision-maker, and a written response protocol with a budget.

**Sustained clean cooking.** LPG cuts household exposure sharply, and household fuel is a major ambient source in Bihar [C061]. But the HAPIN trial found no birthweight or stunting benefit from the switch alone [C096][C097], and refill use remains low [C036]. Support research on women's access and on supply within government programmes, including the World Bank-financed Uttar Pradesh programme [C091]. Do not fund fuel.

**Kiln conversion with labour standards.** Emissions fall substantially with zigzag conversion [C069]. Workers' pay, debt and exposure after conversion are unmeasured, and bondage is documented [C071]. Owners finance conversion. Philanthropy can fund the worker-side components and independent measurement.

**Income continuity beyond construction.** Vendors, riders and small-enterprise workers lose earnings during restrictions with no scheme [C100]. The new platform social security fund [C103] could carry a pollution-day benefit. Design and pilot only with a public or platform payer committed.

**Health-system readiness.** Mortality rises on high-pollution days [C053], and national surveillance exists on paper [C087]. A district demonstration of episode protocols in primary care, owned by the state health department, would test feasibility.

## The infrastructure judgement

Infrastructure helps when four conditions hold:

- it addresses a specific pollutant and pathway;
- the intended users are actually present for many hours;
- an existing institution owns and pays for its operation;
- its performance is measured.

It fails when it is visible but placed where few people spend time (towers). It fails when it asks the most exposed people to give up earnings to use it (shelters). It fails when it changes behaviour in ways that offset its benefit (classroom purifiers without messaging). And it fails when it is left without a running budget.

On current evidence, the strongest infrastructure case in this field is not a new asset. It is filtration and monitoring added to services that already exist and already have operators, tested before scale.

# Four portfolio options

These are alternatives to compare, not a recommendation of one flagship. Each draws on the findings above. Structured fields are in `data/portfolios.csv`.

## Focus of this dossier

After the first round of findings, the dossier sets two priorities:

1. **Outdoor informal workers in Delhi-NCR.** This covers PF1 (income) and PF3 (occupational protection).
2. **Children in high-pollution cities.** This covers PF2.

Both groups combine strong evidence of harm, identifiable institutions that can carry the work, and outcomes that can be observed within a season or a school year [C082][C044][C074]. PF4 is not prioritised. Its questions stay in the learning agenda. That choice reflects where evidence and operators are strongest today, not a judgement that kiln workers or rural households matter less.

**Costs are not estimated here.** The study found few sourced cost figures beyond those cited:

- purifiers about ₹40,000 per unit;
- smog towers ₹25 crore to build and ₹15 lakh a month to run;
- kiln conversion about ₹40 lakh per kiln.

No cost-effectiveness ratio is offered. Any budgeting should separate capital, operating and evaluation costs, and label planning assumptions as such.

## PF1. When the air stops work: income protection for restriction-affected workers (Priority 1)

**Problem and population.** Construction workers first, then vendors, platform riders and small-enterprise workers who lose earnings when GRAP stops work. Migrants and women are most often excluded [C044][C089].

**Evidence for action.** The restriction pathway is the best-evidenced livelihood harm [C038][C040]. The compensation duty is established by court order [C039], but registration gaps keep most workers out [C041][C042]. Statutory cess funds go largely unspent [C101].

**Combination.**

- registration and renewal drives;
- payment tracking after every closure;
- legal support;
- organising and voice for affected workers;
- design and time-bound piloting of income continuity for non-construction workers, with a public or platform payer.

**Why philanthropy.** Government pays the transfers, but nobody is paid to close the registration gap or count who is missed. **Additionality.** Works through existing boards and court orders, not parallel schemes. **Partners.** Construction unions, MHT, Help Delhi Breathe, the Delhi welfare board and labour department, and the new platform social security board [C103].

**Geography.** Delhi-NCR, the only place with GRAP compensation, then the other NCR states bound by the same order. **Approach.** Population-based. **Infrastructure.** None.

**Recurring services.** Seasonal case workers and board data systems, to be absorbed by the board.

**Outcomes and measurement.**

- share of affected workers paid within 30 days;
- time to payment;
- inclusion of migrants and women;
- measured earnings loss compared with compensation.

**Failure modes.** The board refuses data access, payments are delayed, or no payer emerges for non-construction workers.

**Expand, redesign or exit.**

- Expand if the share paid rises measurably over two seasons.
- Redesign if board data are unavailable.
- Exit when the board runs outreach itself.

**Class: A** for registration and monitoring; **B** for income-continuity design.

## PF2. Children's air: schools and early years (Priority 2)

**Problem and population.** Children in high-exposure cities, especially in government schools and in households without private protection. Pregnant women are a linked group [C050][C052].

**Evidence for action.** A school education trial improved behaviour and some health outcomes [C074]. Purifiers cleaned air but outcomes lagged [C075]. School closures disrupt learning unevenly [C054][C055].

**Combination.**

- curriculum-embedded air-pollution education;
- redesigned classroom filtration pilots with behavioural messaging and education-department running budgets;
- school continuity planning to reduce closures;
- a review of whether antenatal services advise women on exposure.

**Why philanthropy.** Education systems adopt proven, low-cost content but rarely test hardware rigorously before buying it. **Additionality.** Extends a tested Delhi design to a second setting and prevents procurement racing ahead of evidence. **Partners.** KV Sangathan, state education departments, the trial's research team, CEEW.

**Geography.** Delhi plus one Indo-Gangetic city with weaker capacity, such as Patna, to test transfer. **Approach.** Place-based, through schools. **Infrastructure.** Classroom HEPA units, only as measured pilots.

**Recurring services.** Teacher time; filters and electricity, paid by the education department.

**Outcomes.** Behaviour and awareness; symptoms; spirometry; classroom PM2.5; in-person school days retained.

**Failure modes.** Effects fade; purifier offsets persist; mass procurement before evidence.

**Expand, redesign or exit.**

- Expand education if the second-site effect holds.
- Stop purifier pilots if outcomes still lag education alone.

**Class: A** for education; **B** for purifiers and continuity planning.

## PF3. Essential work in toxic air: occupational protection (Priority 1)

**Problem and population.** Sanitation workers, waste pickers, security guards and delivery riders, with documented high exposure and lung impairment [C082][C099].

**Evidence for action.** Strong on the problem; limited on interventions [C085]. Entitlements now exist but reach is uneven:

- From 2024–25, waste pickers can receive ID cards, PPE kits and health insurance under the NAMASTE scheme [C106]. Municipal ID-card issuance has lagged [C107], and coverage figures are inconsistent [C108].
- The OSH Code, in force since November 2025, gives employees a free annual health check-up [C109]. Self-employed waste pickers have no employer to whom that duty attaches [C110].

**Combination.**

- enrolment support so workers actually receive NAMASTE profiling, municipal ID cards, insurance and statutory health check-ups;
- fit-tested respirator programmes with employer or municipal co-payment;
- shift timing away from early-morning inversions;
- periodic lung-function checks through public schemes;
- organising to press employer and platform duties.

**Why philanthropy.** Employers and platforms have obligations but no tested model for outdoor informal work exists in India. **Additionality.** No public programme covers these workers' exposure. **Partners.** Municipal corporations and contractors, Chintan, waste-picker collectives, platform worker unions, state health departments.

**Geography.** Delhi, where the evidence exists, then a second city. **Approach.** Population-based. **Infrastructure.** None beyond equipment.

**Recurring services.** Respirator replacement and screening, paid by employers or public health.

**Outcomes.** Personal exposure; adherence; lung-function trend; costs borne by workers.

**Failure modes.** Low adherence in heat; employers refuse to co-pay; screening without access to treatment.

**Expand, redesign or exit.**

- Expand if exposure falls and adherence holds.
- Redesign around shift timing if respirators fail.

**Class: A** for entitlement enrolment; **B** for respirator programmes and shift redesign.

## PF4. Fair transition in production and rural energy (not prioritised)

**Problem and population.** Kiln workers, often SC and ST migrant families in debt bondage [C071][C072], and biomass-cooking households in rural Bihar and the Indo-Gangetic Plain [C058][C059].

**Evidence for action.**

- Kiln emission savings are reported [C069].
- Labour abuse is documented [C071].
- LPG cuts exposure, but its health effect alone is limited [C096].
- Rural exposure is high but poorly monitored [C060].

**Combination.**

- kiln conversion paired with labour standards and worker support;
- calibrated rural monitoring with response protocols;
- research on sustained clean cooking within government programmes.

**Why philanthropy.** Owners and governments fund capital; nobody funds the worker side or the measurement. **Additionality.** Attaches labour and equity conditions to transitions already mandated. **Partners.** Bihar's pollution board, WRI India, anti-slavery organisations, IIT Kanpur, the World Bank's Uttar Pradesh programme.

**Geography.** Bihar: a major kiln hub and migrant origin, with the weakest monitoring. **Approach.** Place-based. **Infrastructure.** Sensors with response protocols.

**Recurring services.** Calibration; labour inspection; worker support.

**Outcomes.** Kiln emissions; pay records, debt and child presence; actions triggered by monitoring.

**Failure modes.** Owners resist labour conditions; regulators reject sensor data; health outcomes take years.

**Expand, redesign or exit.** Proceed beyond measurement only after a one-season comparison of converted and unconverted kilns. Exit if regulators do not adopt the protocols.

**Class: C.**

## Comparing the options

| | PF1 Income | PF2 Children | PF3 Occupational | PF4 Transition |
|---|---|---|---|---|
| Strongest evidence | Restriction losses; registration gap | School education RCT | Exposure and lung impairment | Kiln emissions; labour abuse |
| Main approach | Protect income | Reduce exposure (behaviour first) | Reduce exposure and consequences | Reduce emissions fairly |
| Place- or population-based | Population | Place (schools) | Population | Place |
| Who keeps it running | Welfare boards; platform fund | Education departments | Employers; health departments | Pollution and labour boards |
| Time to observable result | One season | One school year | One winter | One season (labour); years (health) |
| Main risk | Data access | Behavioural offsets | Adherence | Owner resistance |
| Class | A/B | A/B | A/B | C |
| Priority | 1 | 2 | 1 | Learning only |

A **vendor- and market-focused portfolio** was considered as an alternative. It would reach a large, mostly self-employed, often female workforce. But the evidence on vendors' exposure and earnings is thinnest of all the groups, and vendors have no employer or welfare board to carry recurring costs. On current evidence, vendors are better served inside PF1 (income-continuity design) and PF3 (occupational protection) than as a standalone portfolio. The first step for them is the measurement study in the learning agenda (G1).

The **prioritised portfolio** combines PF1 and the enrolment component of PF3 for outdoor workers with the education component of PF2 for children. Together these rest on the strongest evidence and the clearest operators. Respirator programmes (PF3) and redesigned purifiers (PF2) run alongside as measured pilots. PF4 waits on the learning agenda.

# A proportionate learning agenda

Not every uncertainty needs a randomised trial. Established protective measures should not be delayed to create one. The register in `data/evidence-gaps.csv` matches each question to the lightest method that could answer it:

- better use of existing data;
- exposure or service assessments;
- qualitative research;
- feasibility studies;
- pilots;
- quasi-experimental or randomised evaluation where ethical and appropriate.

## Questions that would change a decision soonest

| # | Question | Lightest credible method | Why it matters |
|---|---|---|---|
| G1 | How much do informal workers lose in earnings during episodes, and through which pathway? | Earnings diary or app panel of 300–500 workers over one winter, linked to local PM and GRAP days | Sizes the case for income protection versus health services |
| G2 | Does registration support raise receipt of compensation among migrants? | Staggered rollout across sites, with board payment records as the outcome | Tests the cheapest lever |
| G3 | What do classroom purifiers achieve once behavioural offsets are addressed? | Additional trial arm or quasi-experiment in state schools, with cost tracking | Avoids funding hardware that leaves children no better off |
| G4 | Do respirator programmes reduce outdoor workers' exposure in practice? | Pilot with personal monitors on a sample of workers | Decides whether PPE merits employer and grant money |
| G7 | How high is exposure in unmonitored districts, and who acts on it? | Co-location calibration plus a response protocol in two districts | Turns visibility into action |

## Questions for later or in parallel

- **G5.** Do pregnancy and newborn services reach women exposed at work and home?
- **G6.** What happens to kiln workers when kilns convert?
- **G8.** Do school closures widen learning gaps?
- **G9.** Does filtration in shelters or childcare reduce indoor exposure enough to matter?
- **G10.** What happens to debt and schooling after pollution-related illness?
- **G11.** Who bears the costs of crop-residue rules?
- **G12.** How do health services respond during episodes?

## Outcomes to measure

Studies in this field should measure across eight domains:

- exposure;
- health;
- earnings;
- out-of-pocket costs;
- care burden;
- uptake;
- access;
- institutional performance.

Exposure reductions are valid intermediate outcomes. They do not by themselves establish a health benefit, as the HAPIN and Delhi schools trials both show [C096][C075]. Lung development, birth outcomes and chronic disease need follow-up over years, not a winter.

## Distributional analysis

Every evaluation should report who benefited, who did not, and whether any group bore new costs. Examples:

- workers paying for respirators;
- children in purifier classrooms changing behaviour;
- kiln workers absorbing conversion costs.

## Ethics

Any future research with people requires informed consent, privacy protection and ethics review. This study was desk research only.

# Synthesis: what to fund, what to test, what to avoid

## The answer to the central question

*Where can a foundation help reduce the pollution people face, protect the livelihoods they depend on, and leave behind a service or institution that continues to work after the grant ends?*

**Three places stand out.**

1. **Where pollution control takes away people's income.** Emergency restrictions in Delhi-NCR stop work, and the law already says idled construction workers must be paid from funds that exist [C039][C101]. Most are not paid, because they are not registered [C041][C044]. Closing that gap protects livelihoods directly. It also strengthens a statutory welfare board, and the board can carry the work after the grant. Extending the same logic to vendors and platform workers needs design and a public payer [C103].
2. **Where children learn.** A low-cost education programme improved protective behaviour and some health outcomes in a rigorous Delhi trial [C074]. It runs through school systems that will continue it. Classroom filtration needs redesign before scale [C075].
3. **Where public money is spent on clean air without anyone checking that it works.** Independent evaluation has already stopped one costly mistake [C077]. Repeated investment in unproven measures continues [C081]. An evaluation facility leaves behind better decisions, not an asset.

## Priorities set for this dossier

Two groups are prioritised:

1. **Outdoor informal workers in Delhi-NCR**: construction workers, sanitation workers, waste pickers, guards and riders.
2. **Children in high-pollution cities.**

For the first group, the work is to make existing protections reach them. That means GRAP compensation [C044], NAMASTE and municipal ID cards [C106][C107], and statutory health check-ups [C109], alongside measured pilots of occupational protection. For children, it is curriculum education first, with redesigned classroom filtration tested before it scales [C074][C075].

## Answers to the five decisions

**A. Which communities and settings merit priority?** These groups combine high exposure, weak protection and little capacity to absorb losses:

- outdoor informal workers in Delhi-NCR (construction workers, sanitation workers, waste pickers, riders) [C082][C099][C044];
- children in high-exposure cities [C052][C054];
- kiln families and biomass-cooking households in under-monitored Bihar [C071][C058].

Delhi-NCR is the place to start because the institutions and legal duties exist there. Bihar is where exposure is least visible.

**B. Which pathways create the greatest avoidable burdens?**

- The restriction pathway is the best evidenced and the most avoidable, because it is created by policy [C038][C040].
- The illness pathway is large in mortality terms [C016][C053], but its route to household finances is unmeasured [C047].
- Occupational exposure is high and documented [C082].

**C. Which interventions are effective, usable and feasible?**

- Effective and feasible: school education [C074]; registration support for statutory compensation, where the mechanism is observable but unevaluated [C042].
- Effective on exposure but not yet on health: classroom purifiers [C075]; LPG [C096].
- Unproven: occupational PPE programmes, sensor-to-action systems, shelter filtration.

**D. Fund now, test first, investigate further.**

| Fund now (A) | Test first (B/C) | Investigate further |
|---|---|---|
| Registration, payment tracking and legal support for GRAP compensation | Income continuity beyond construction (B) | Informal earnings losses (G1) |
| Enrolment of waste pickers and sanitation workers in NAMASTE, ID cards, insurance and health check-ups | | |
| Curriculum air-pollution education | Redesigned classroom purifiers (B) | Debt after illness (G10) |
| Independent evaluation and spending accountability | Occupational protection (B) | Pregnancy service reach (G5) |
| | Sensors with response protocols (B) | School-closure learning loss (G8) |
| | Sustained clean cooking research (B) | Costs of residue rules (G11) |
| | Worker and community organising (B) | |
| | Shelter and childcare filtration (C) | |
| | Kiln conversion with labour standards (C) | |
| | Health-system episode readiness (C) | |

**E. What should not be funded on current evidence?**

- outdoor smog towers [C077][C078];
- anti-smog guns and sprinklers as air-quality investments [C080];
- untargeted mask distribution [C085];
- purpose-built clean-air shelters for outdoor workers [C098][C086];
- crop-residue machinery as a philanthropic purchase [C093];
- direct payment of statutory transfers, or of fuel subsidies, in place of public duty-bearers [C101][C036].

## Second-order effects to watch

- **Behavioural offsets.** Protection in one place can reduce caution elsewhere [C075].
- **Displacement of cost.** Cleaner production can push costs onto workers [C069][C071]. Restrictions protect air while removing wages [C040].
- **Visibility bias.** Measures that can be seen and photographed attract money. Measures that work quietly through registration offices and curricula do not [C079].
- **Monitoring bias.** Money follows monitors to metros [C033][C035].

## Quality check against the brief

| Check | Result |
|---|---|
| Delhi detailed without becoming a proxy | Delhi is the anchor; five settings with stated limits; no source shares transferred |
| Health, productivity, earnings and household welfare distinguished | Separate pathways A–E; factory output not equated with wages; GDP not used for households |
| Causal claims match evidence | Two-dimension ratings with written reasons; association and causation labelled |
| Policy losses separated from illness | Pathway C kept separate from A throughout |
| Monitoring gaps not read as safety | Stated as a rule and applied to Bihar and districts |
| Infrastructure has operator and recurring finance | Each infrastructure option names both, or is not recommended |
| Equity assessed through access and outcomes | Registration, tenure, caste and gender examined for who actually receives protection |
| Existing organisations and obligations recognised | Organisation map; statutory duty-bearers named for each recurring service |
| Recommendations trace to findings | Every recommendation cites claim IDs |
| What not to fund, and why | Decision E list above |

## What remains uncertain

The weakest parts of this study are its evidence on informal earnings and debt, its reliance on summaries for several official health documents, and the unpublished full results of the Delhi schools trial. Phase 2 will re-check every source. The conclusions most sensitive to new evidence are the purifier judgement and the scale of earnings losses outside construction.

# Appendix A. Claim register (cited claims)

| Claim | Statement | Sources | Status |
|---|---|---|---|
| C001 | India's national ambient standard for PM2.5 is 40 µg/m³ as an annual mean and 60 µg/m³ as a 24-hour value; for PM10 it is 60 and 100 µg/m³. | S001 | read |
| C002 | The Indian annual standard is an arithmetic mean of at least 104 measurements a year at a site; 24-hour values must be met 98% of the time and may not be exceeded on two consecutive monitoring days. | S001 | read |
| C003 | WHO's 2021 guideline levels for PM2.5 are 5 µg/m³ annual mean and 15 µg/m³ 24-hour (99th percentile), with interim targets of 35/25/15/10 (annual) and 75/50/37.5/25 (24-hour); the guidelines are not legally binding. | S002 | read |
| C004 | India's annual PM2.5 standard (40 µg/m³) is eight times the WHO 2021 guideline level (5 µg/m³); at 40 µg/m³ it is less stringent than even WHO interim target 1 (35 µg/m³). | S001, S002 | read |
| C005 | WHO estimates ambient air pollution caused 4.2 million premature deaths worldwide in 2019, 89% of them in low- and middle-income countries; 68% were from ischaemic heart disease and stroke. | S003 | read |
| C006 | India's AQI has six categories: Good 0-50, Satisfactory 51-100, Moderate 101-200, Poor 201-300, Very Poor 301-400, Severe 401-500. | S004 | read |
| C007 | The AQI is generated hourly from sub-indices for eight pollutants (PM2.5, PM10, CO, NO2, SO2, NH3, O3, lead); the highest sub-index is reported as the AQI, using a running average of the preceding 24 hours (8 hours for CO and ozone) with at least 16 hours of data required. | S005 | read |
| C008 | CPCB acknowledged in November 2026 that hourly particulate readings above 999 µg/m³ are excluded from AQI calculation because the 2015 validation method assumed analysers calibrated to 0-1,000 µg/m³; such hours appear as data gaps and do not count toward the 24-hour average. | S005 | read |
| C009 | Reports at the time said 45 of Delhi's 59 monitoring stations had missing hourly readings for at least one pollutant during the episode; ministry sources said the methodology was under internal review with no external expert group constituted. | S005 | read |
| C010 | The AQI is capped at 500; CPCB states values above this remain 'Severe' and extrapolation would not change the health category. A capped index therefore cannot distinguish 500 from much higher concentrations. | S005 | read |
| C011 | As of March 2026 India's ambient monitoring network had 1,646 stations (manual and real-time) across 603 cities in 28 states and 7 union territories; SAMEER shows near real-time AQI for more than 292 cities. | S004 | read |
| C012 | NCAP, launched in 2019, covers 130 cities; ₹16,423.55 crore in performance-linked grants was released FY2019-20 to FY2025-26 and cities report using ₹11,575.54 crore (70.5%). | S004 | read |
| C013 | Government reports that in FY2025-26, 108 of 130 NCAP cities had lower annual PM10 than in 2017-18; 72 by more than 20%, 26 by more than 40%, and 14 met the national standard. NCAP targets are framed on PM10, not PM2.5. | S004 | read |
| C014 | NCAP source-apportionment studies attribute about 40-50% of PM10 in most cities to construction and road dust, according to government. | S004 | read |
| C015 | CAQM directed that only BS-VI, CNG or electric buses may enter Delhi from 1 November 2026, and set a revised industrial PM emission norm of 50 mg/Nm³ for polluting and large industries from 1 October 2026. | S004 | read |
| C016 | GBD 2019 attributes 1.67 million deaths in India in 2019 (95% UI 1.42-1.92) to air pollution, 17.8% of all deaths: 0.98 million to ambient particulate matter and 0.61 million to household air pollution. | S006 | read |
| C017 | Between 1990 and 2019 the death rate attributed to household air pollution fell 64.2% while that attributed to ambient particulate matter rose 115.3% (UI 28.3-344.4). | S006 | read |
| C018 | GBD 2019 values lost output from air-pollution deaths and illness at US$36.8 billion (UI 27.4-47.7) in 2019, 1.36% of GDP; as a share of state GDP the loss was highest in low-income states (Uttar Pradesh, Bihar, Rajasthan, Madhya Pradesh, Chhattisgarh), while Delhi had the highest per-capita loss. | S006 | read |
| C019 | A 2024 difference-in-differences study using district civil-registration deaths 2009-2019 found each 10 µg/m³ increase in annual PM2.5 associated with 8.6% (95% CI 6.4-10.8) higher annual mortality; it argues GBD exposure-response functions drawn from low-pollution countries may be inappropriate for India. | S007 | read |
| C020 | The same study estimates 3.8 million deaths (2.9-4.9) over 2009-2019 attributable to PM2.5 above the Indian standard, and 16.6 million (13.0-21.8) above the WHO guideline; the counterfactual chosen changes the estimate more than fourfold. | S007 | read |
| C021 | Population-weighted annual PM2.5 in India was 41 µg/m³ in 2023 on AQLI's satellite-derived data, up from 2022; all 1.4 billion people live above the WHO guideline and 46% above the national annual standard. | S008 | read |
| C022 | Estimates of the share of Indians living above the national standard differ by source and period: 46% (AQLI, 2023 satellite data) versus 81.9% (de Bont et al., 2009-2019 modelled data). | S008, S007 | read |
| C023 | AQLI estimates that meeting the WHO guideline would add 3.5 years to average Indian life expectancy, 5 years for 544.4 million Northern Plains residents, and 8.2 years for Delhi residents. | S008 | read |
| C024 | AQLI reports that pollution in districts with NCAP non-attainment cities was 10.5% lower in 2023 than 2017; the revised NCAP target is a 40% reduction by 2026 for 131 cities. | S008 | read |
| C025 | In TERI-ARAI receptor modelling for Delhi and NCR towns, dust contributed 31-34% of PM2.5 in summer but about 15% in winter; biomass burning 22% in winter vs 15% in summer; secondary ions 26% in winter vs 17-18% in summer; vehicles 20-23% in winter vs 18-20% in summer; industry 10-13% in both. | S009 | read |
| C026 | TERI-ARAI measured average winter PM2.5 of 168 ± 45 µg/m³ across its Delhi-NCR sampling sites (range 92-254). | S009 | read |
| C027 | IIT Kanpur's 2016 study for DPCC found secondary particles (nitrate, sulphate, ammonium) to be the most important single component of winter PM2.5 at its Delhi sites, with average winter PM2.5 of about 375 µg/m³ at sampling sites. | S010 | read |
| C028 | Transport's share of Delhi's PM2.5 emission inventory is put at 20% (IIT Kanpur 2015), 39% (TERI-ARAI 2018) and 41% (SAFAR-IITM 2018): emission inventories and ambient apportionment measure different things and are not interchangeable. | S011 | read |
| C029 | CSE's analysis of Decision Support System outputs for 10-20 November found Delhi's local sources contributed about 35% of PM2.5 in 2025 (27.3% in 2024) and surrounding NCR districts about 25.8% (36% in 2023); vehicles were 51-53% of the local share across 2023-25. | S011 | read |
| C030 | CSE reports Delhi had received ₹81.36 crore under NCAP by December 2025 but utilised only ₹14.1 crore (17%). | S011 | read |
| C031 | Real-time measurements inside Delhi auto-rickshaws (about 180 hours) found trip-averaged PM2.5 geometric mean of 190 µg/m³, 1.5 times simultaneous ambient levels; black carbon was 3.6 times and ultrafine particle number 8.4 times ambient. | S012 | read |
| C032 | On-road and near-road emissions accounted for 30% of in-vehicle PM2.5 but 68% of black carbon and 86% of ultrafine particles in auto-rickshaws: fixed ambient monitors understate exposure of people who work in traffic, especially for combustion particles. | S012 | read |
| C033 | An Airvoice analysis of official datasets up to 2025 found about 40% of India's districts have no government-operated monitoring station, about half of continuous stations deliver stable data, and station numbers correlate only moderately with PM2.5 levels. | S013 | read |
| C034 | CSE's 2026 State of India's Environment report estimates only about 15% of India's population (about 200 million) lives within 10 km of a continuous monitor. | S014 | provisional |
| C035 | An unmonitored district is not a low-exposure district: monitoring is concentrated in large metros, and several highly populated districts in Uttar Pradesh, Bihar, West Bengal and Andhra Pradesh are poorly monitored or outside the real-time network. | S013 | read |
| C036 | PMUY connections rose sharply after 2016, but in 2021-22 9.6% of beneficiaries took no refill, 11.3% one refill and 56.5% four or fewer, against about seven refills a year needed for exclusive cooking use. | S015 | read |
| C037 | Research in Delhi and Jharkhand reported by Mongabay found refill cost, access, misconceptions and women's limited decision-making autonomy constrain consistent LPG use among PMUY households. | S015 | read |
| C038 | Under GRAP, construction is restricted as AQI rises and fully banned at Stage 4 (AQI above 450); the Supreme Court's 24 November 2021 order required financial assistance to workers affected by construction bans, paid from labour-cess (BOCW welfare) funds. | S018, S016 | read |
| C039 | The Supreme Court later directed that whenever GRAP closes construction, affected workers must be compensated even without a specific court order; it declined a plea to let non-polluting construction trades continue during Stages 3 and 4. | S018 | read |
| C040 | Delhi announced ₹8,000 for registered construction workers after the November 2024 GRAP-4 closure and ₹10,000 after 16 days of GRAP-III in December 2025; eligibility was limited to workers registered and verified with the Delhi BOCW Welfare Board. | S017, S019 | read |
| C041 | Welfare Board dashboard figures cited in December 2024 showed 1,378,199 workers ever registered but only 89,518 active members; 1,288,681 memberships had expired and 507,863 of 716,174 renewal applications had been approved. | S017 | read |
| C042 | In a rapid survey of 75 workers at four central-Delhi sites (filed in a December 2024 affidavit), only five were registered with the Welfare Board and none had received the ₹8,000 payment. | S017 | read |
| C043 | In November 2026 the Welfare Board said about one lakh workers had been paid (nearly ₹100 crore) while its website listed about 2.15 lakh registered workers; a union affidavit says about 1,700 workers still await payment. | S016 | read |
| C044 | Compensation is tied to registration, so the registration gap determines who is protected: unregistered and migrant workers whose registrations have lapsed lose wages during restrictions without receiving relief. | S017, S016 | read |
| C045 | In a Bengaluru garment factory, hourly output fell with fine particulate pollution; effects were heterogeneous across workers and tasks, and attentive managers mitigated losses by reassigning workers. | S020 | read |
| C046 | In a September 2025 survey of 582 Delhi households, 9 in 10 affluent households had air conditioners versus fewer than 1 in 10 low-income households; the authors report air purifiers are mostly owned by the rich. | S021 | read |
| C047 | The same survey found household spending rose during pollution months, dominated by medical expenses; coughing, breathing difficulty and eye irritation were the most reported symptoms. | S021 | read |
| C048 | Workplace exposure to outdoor air was higher the lower a respondent's class, and a large majority across all classes reported not using masks during severe pollution. | S021 | read |
| C049 | In a Tamil Nadu rural-urban cohort of 1,285 pregnant women with directly measured household PM2.5 in each trimester, a 10 µg/m³ increase was associated with 4 g lower birthweight (95% CI 1.1-6.8) and 2% higher odds of low birthweight. | S022 | read |
| C050 | Analyses of NFHS-5 (2019-21) linked to satellite PM2.5 associate higher in-utero exposure with low birthweight and preterm birth: one reports a 5% higher LBW prevalence and 12% higher preterm prevalence per 10 µg/m³, with steeper risk above about 40 µg/m³ and greater susceptibility in northern districts. | S023 | read |
| C051 | A second NFHS-5 analysis of 208,181 children (mean in-utero PM2.5 56 µg/m³) found 52% higher odds of preterm birth in the highest versus lowest exposure octile (AOR 1.52, 1.43-1.61) but only a small LBW difference (AOR 1.06). | S024 | read |
| C052 | Using national survey data, each 10 µg/m³ increase in PM2.5 was associated with 10% higher anaemia, 11% higher acute respiratory infection and 5% higher low-birthweight prevalence among Indian children; nitrate, elemental carbon and ammonium were more strongly associated than total mass. | S025 | read |
| C053 | A ten-city time-series study (2008-2019) found a 10 µg/m³ rise in 2-day average PM2.5 associated with 1.4% higher daily mortality (0.7-2.2); associations persisted below the Indian 24-hour standard of 60 µg/m³. | S026 | read |
| C054 | Under GRAP Stages III-IV, physical classes are discontinued for children up to Class V and higher classes move to hybrid mode; CEEW's review of Directorate of Education circulars found closures in some years lasted up to 15 days, often announced with less than a day's notice. | S027 | read |
| C055 | CEEW argues online classes give limited continuity because of digital access gaps and reduced peer interaction; students it interviewed (about 30, Classes V and X, one school) all preferred attending school. | S027 | read |
| C056 | A 2012 CPCB-commissioned study reported lung-function deficits in 43.5% of Delhi schoolchildren versus 25.7% in a control group. | S028 | provisional |
| C057 | Indian evidence linking air pollution to children's cognition is preliminary: the most-cited result (Odisha, IQ 80 vs 98 between high- and low-pollution sites) is a conference abstract without established peer review. | S029 | provisional |
| C058 | An IIT Kanpur network of 538 low-cost sensor nodes across every block of Bihar's 38 districts found rural air violated national standards on nearly 90% of days, with winter PM2.5 in northwest Bihar routinely around 210 µg/m³. | S030 | read |
| C059 | The AMRIT study attributes rural Bihar's pollution mainly to household solid biomass, seasonal stubble burning, dust and brick kilns; Bihar's kiln owners' association says most kilns have converted to zigzag technology under a March 2022 BSPCB notification. | S030 | read |
| C060 | The IIT Kanpur lead investigator estimates Bihar has roughly one regulatory monitor per 3.5-4 million people, concentrated in urban centres. | S030 | read |
| C061 | In Patna, receptor modelling found dust the largest PM10 source in winter (30%) and summer (57%); secondary inorganic particles 24% (winter) vs 9% (summer); dispersion modelling put the residential sector at 28% of PM2.5 in winter and 6% in summer, transport 21-23%, and sources outside the city 46% in summer and 16% in winter. | S031 | read |
| C062 | Annual PM10 averages of 166.75 and 159.67 µg/m³ were recorded at NAMP stations at Anpara and Renusagar (Sonbhadra, Singrauli region) for April 2023 to May 2024, against a 60 µg/m³ standard; PM2.5 was not reported at these stations. | S032 | read |
| C063 | Applicants before the NGT (OA 240/2024) allege 359 industries including thermal power plants and coal mines, health harm and heavy-metal contamination; official health data supplied by the district CMO recorded few lung-disease patients at local health centres, illustrating weak health surveillance rather than absence of harm. | S032 | read |
| C064 | Black carbon concentrations above 200 µg/m³ were measured close to Singrauli's coal-fired power plants in a 2013 campaign; satellite NO2 shows a persistent hotspot over its seven plants. | S033 | provisional |
| C065 | Mumbai's 2023 NEERI study found resuspended road dust (linked to Metro and real-estate construction) the main PM10 source; for PM2.5, secondary aerosols (22%) and marine sources (26%) made up 48%. | S034 | read |
| C066 | Mumbai's receptor modelling attributed 12-20% of PM to industry while the inventory-based dispersion model gave under 1%, because small informal units such as 'bhatties' were missing from the inventory: inventories systematically miss informal sources. | S034 | read |
| C067 | CAQM reported 5,114 farm fires in Punjab and 662 in Haryana between 15 September and 30 November 2025, down 53% on 2024 and 93% (Punjab) on 2021; it credits machinery, enforcement, ex-situ straw use and district plans. | S035 | read |
| C068 | In six Patiala villages (3,644 participants, 2018-19), lung function fell during crop-residue burning periods (mean PM2.5 increase 167 µg/m³): FEV1 declined 16% in boys and 26% in girls aged 10-18, with smaller declines in adults. | S036 | read |
| C069 | Zigzag kilns cut coal use about 20% and black carbon and PM about 75% compared with fixed-chimney kilns, produce about 8 bricks per kg of coal versus 5, and cost about ₹40 lakh to retrofit with a reported one- to two-year payback. | S037 | read |
| C070 | Each Bihar kiln employs 120-150 workers, mostly trained on the job; owners report converted kilns cannot reach full efficiency without trained workers, and workers live for months in temporary housing exposed to coal dust and heat. | S037 | read |
| C071 | Anti-Slavery International's Punjab kiln survey found 96% of moulders had taken advances, wages were withheld for whole 8-10-month seasons, families were paid as units through the male head, and 65-80% of children under 14 worked in summer months. | S038 | read |
| C072 | NSS-based analysis finds 47% of migrants working in brick kilns are Scheduled Castes and about 16% Scheduled Tribes, against 18.8% and 7.7% of the all-sector migrant workforce. | S039 | read |
| C073 | There are over one lakh brick kilns in India producing about 250 billion bricks a year. | S039 | read |
| C074 | A two-year cluster-randomised trial in 180 classes (about 9,000 students) in Delhi's Kendriya Vidyalaya schools, winters 2024-25 and 2025-26, found an air-pollution education campaign raised awareness and protective behaviour, reduced self-reported breathing difficulty and marginally improved working memory, mainly in year one. | S040 | read |
| C075 | In the same trial HEPA purifiers significantly reduced classroom PM2.5, but the purifier-plus-education arm underperformed education alone on working memory (year one) and spirometry (year two); students in purifier classrooms reduced protective behaviour outside school, consistent with a moral-hazard offset. | S040 | read |
| C076 | Education effects spread to untreated classrooms through peer networks; behavioural effects attenuated in year two as controls caught up. | S040 | read |
| C077 | IIT Bombay's evaluation of the Connaught Place smog tower found PM reductions of 48-56% within 20 m, 30-34% at 21-99 m and 12-13% at 109-199 m; DPCC told the NGT in November 2023 that the towers were ineffective and not justified. | S042, S041 | read |
| C078 | DPCC's affidavit put tower capital cost at about ₹25 crore each and operation at about ₹15 lakh per month, and stated the Anand Vihar tower was non-operational with no measurable effect at a monitor 30 m away. | S042 | read |
| C079 | Government stated in 2021 that early smog-tower results showed an 80% reduction; later independent evaluation found effects confined to a few hundred metres, illustrating the gap between launch claims and measured performance. | S042 | read |
| C080 | CEEW finds limited evidence on anti-smog gun effectiveness; deploying 250-600 guns on large Delhi buildings would cost about ₹5-12 crore plus electricity and need 25-90 lakh litres of water a day, while covering under 0.5% of Delhi's area. | S043, S044 | read |
| C081 | Delhi's 2026 action plan expands anti-smog guns and water sprinklers at large scale while experts question enforcement capacity and the evidence for these measures. | S044 | read |
| C082 | In Chintan's 2023 Delhi study, abnormal lung function was found in 86% of sanitation workers (safai karamcharis) and security guards and 75% of waste pickers, versus 45% of an indoor office-worker control group; 27% of sanitation workers, 17% of waste pickers and 10% of guards had severe impairment, none in controls. | S045 | read |
| C083 | Over 60% of sanitation workers, 50% of waste pickers and 30% of security guards did not know about protective equipment; nearly half of waste pickers burned wood or coal to keep warm in winter and over 30% burned waste. | S045 | read |
| C084 | Women in all three occupational groups had lower lung function than men in Chintan's study. | S045 | read |
| C085 | Properly fitted masks reduce exposure, but mask use in Delhi has been low; researchers attribute this to low awareness and social norms, and questioned what a mass distribution of 5 million masks would achieve. | S046 | read |
| C086 | Work-from-home advisories issued during severe pollution do not reach daily-wage workers, vendors, construction labourers and delivery staff, for whom staying home means losing income. | S047, S021 | read |
| C087 | The NPCCHH (Ministry of Health) began acute respiratory illness sentinel surveillance linked to air pollution in selected Delhi hospitals in 2017 and has asked states to expand sentinel hospital networks; its health advisory names outdoor workers, pregnant women, children, older adults and people with heart or lung disease as more vulnerable. | S048 | provisional |
| C088 | Clean Air Fund grants supported Mahila Housing Trust and Help Delhi Breathe to train more than 75 women construction workers in three Delhi resettlement colonies (Bakkarwala, Gokulpuri, Sawda Ghevra) to use AQI devices and engage local authorities; five became peer trainers. | S049 | read |
| C089 | Clean Air Fund reports that 94% of women construction workers it surveyed avoid talking about air pollution for fear of losing their jobs, and that construction bans in peak months stopped women from earning. | S049 | read |
| C090 | Clean Air Fund funds Health Care Without Harm to build a network of health workers as clean-air advocates, including work with about 100 hospitals in polluted regions to monitor air quality and communicate risks to patients. | S050 | read |
| C091 | The World Bank approved about $299.66 million for Uttar Pradesh and $300 million for Haryana clean-air programmes in December 2025, described as the first airshed-based multi-sector state programmes; UP's includes clean cooking for 3.9 million households and 15,000 electric three-wheelers. | S051 | read |
| C092 | Delhi's homeless-shelter board (DUSIB) runs about 197 shelters with capacity for 7,092 people, expanding to over 11,000 with 400 winter tents from 15 November 2026 to 15 March 2027; the plan lists bedding, water, toilets and power but no air filtration. | S052 | read |
| C093 | NCAP allocated ₹3,072 crore FY2019-20 to FY2025-26 and a further ₹16,539 crore went to 48 million-plus cities through the 15th Finance Commission challenge fund; ₹3,623 crore was released for crop-residue management in Punjab, Haryana, UP and Delhi FY2018-19 to FY2024-25. | S053 | read |
| C094 | External finance includes World Bank loans for UP (about ₹2,741 crore) and Haryana (about ₹2,498 crore), UNDP projects (about ₹90 crore, 2023-25), UNEP (about ₹53 crore) and Swiss SDC (about ₹72 crore, 2019-23, plus about ₹90 crore for IGP transboundary work). | S053 | read |
| C095 | International funding for ground-level ozone was about $111 million in 2024, 0.4% of total air quality funding tracked. | S054 | read |
| C096 | In the HAPIN randomised trial (3,200 pregnant women; sites included Tamil Nadu), free LPG stoves and fuel achieved near-complete uptake and cut median personal PM2.5 from 70.7 to 23.9 µg/m³, yet birth weight did not differ significantly (adjusted difference 19.6 g, 95% CI -10.1 to 49.2). | S055 | read |
| C097 | HAPIN follow-up analyses report no reduction in infant stunting and no clear effect on childhood lung function outcomes; even with LPG, personal exposure remained well above the WHO guideline, so partial exposure reduction may be insufficient for some outcomes. | S055, S056 | read |
| C098 | Direct evidence that community clean-air shelters reduce health harm is limited and inconclusive; most evidence concerns indoor filtration performance rather than use or outcomes, and no studies of uptake by those most at risk were found. | S057 | provisional |
| C099 | Thirty food-delivery riders measured in Ghaziabad in December 2020 had breathing-zone exposures of 516 µg/m³ PM10 and 180 µg/m³ PM2.5 while riding, with benzene of 19 µg/m³ against a 5 µg/m³ national standard; 67% were unaware of health risks, and traffic junctions drove modelled risk. | S058 | read |
| C100 | Platform workers report that logging off during smog means lost income, lost incentives and sometimes penalties; worker groups have sought a 'pollution surcharge' and a parliamentary panel recommended free N95 masks and health monitoring. | S059 | provisional |
| C101 | Of ₹87,478 crore collected nationally as construction workers' welfare cess up to November 2022, ₹49,269 crore (56%) had been spent and ₹38,209 crore (44%) remained unutilised, according to a reply in Parliament. | S060 | read |
| C102 | Worker federations attribute low disbursement partly to welfare boards' weak enrolment and registration of workers. | S060 | read |
| C103 | The Code on Social Security came into force on 21 November 2025, defining gig and platform workers and requiring aggregators to contribute 1-2% of annual turnover (capped at 5% of payments to workers) to a social security fund whose benefit framework was still being finalised. | S061 | read |
| C105 | Dispersion modelling for Patna attributed about 11% of winter PM10 and 10% of winter PM2.5 to industry and brick kilns within and outside the city. | S031 | read |
| C106 | From 2024-25 waste pickers were added to the NAMASTE scheme (Ministry of Social Justice), which offers enumeration, occupational safety training, PPE kits, occupation-based ID cards and Ayushman Bharat PM-JAY health insurance. | S062 | read |
| C107 | The 2016 Solid Waste Management Rules required municipalities to recognise and issue ID cards to waste pickers, but most urban local bodies failed to issue cards because of budget constraints or reluctance, according to the waste pickers' federation. | S062 | read |
| C108 | Reported NAMASTE coverage figures vary by date and definition: about 85,800 sewer and septic workers profiled and 76,700 given PPE kits by August 2025, and about 2.8 lakh waste pickers validated by mid-2026. | S064 | provisional |
| C109 | The OSH Code came into force on 21 November 2025; government states every employee is eligible for a free annual health check-up and that the Code applies with a uniform threshold of 10 employees, or to any establishment with even one employee in hazardous work. | S063 | read |
| C110 | The OSH Code creates duties for employers of wage workers (including contract and migrant workers) but self-employed waste pickers and vendors have no employer to whom these duties attach; their protection runs through schemes such as NAMASTE instead. | S063, S062 | read |

# Appendix B. Source register

| Source | Title | Author / organisation | Published | Access | URL |
|---|---|---|---|---|---|
| S001 | National Ambient Air Quality Standards (Notification B-29016/20/90/PCI-L) | Central Pollution Control Board | 2009-11-18 | full-text-read | <https://leap.unep.org/en/akn/in/act/2009/b-29016-20-90-pci-l/eng%402009-11-18> |
| S002 | WHO global air quality guidelines: questions and answers | World Health Organization | 2021-09-22 | full-text-read | <https://www.who.int/news-room/questions-and-answers/item/who-global-air-quality-guidelines> |
| S003 | Ambient (outdoor) air pollution fact sheet | World Health Organization | 2024-10-24 | full-text-read | <https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health> |
| S004 | India's Path to Blue Skies: From Awareness to Action for Cleaner Air (backgrounder) | Press Information Bureau, Government of India | 2026-09-07 | full-text-read | <https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/sep/doc_9816_20260907_20291701.pdf> |
| S005 | CPCB Admits PM Readings Above 999 µg/m³ Excluded From AQI Calculation; Reviews 2015 Methodology | ANI (agency feed) | 2026-11-11 | full-text-read | <https://www.freepressjournal.in/india/cpcb-admits-pm-readings-above-999-gm-excluded-from-aqi-calculation-reviews-2015-methodology> |
| S006 | Health and economic impact of air pollution in the states of India: the Global Burden of Disease Study 2019 | India State-Level Disease Burden Initiative Air Pollution Collaborators (ICMR, PHFI, IHME et al.) | 2020-12-22 | full-text-read | <https://www.econ.umd.edu/sites/www.econ.umd.edu/files/pubs/GBD%20India%202019.pdf> |
| S007 | Estimating the effect of annual PM2.5 exposure on mortality in India: a difference-in-differences approach | de Bont J. et al. | 2024-12-01 | abstract-only | <https://pubmed.ncbi.nlm.nih.gov/39674205/> |
| S008 | AQLI India Fact Sheet 2025 (2023 PM2.5 data) | Energy Policy Institute at the University of Chicago (EPIC) | 2025-08 | full-text-read | <https://aqli.epic.uchicago.edu/files/India%20FactSheet_2025_IndiaWV.pdf> |
| S009 | Source Apportionment of PM2.5 & PM10 of Delhi NCR for Identification of Major Sources (executive summary) | TERI and ARAI | 2018-08 | full-text-read | <https://www.teriin.org/sites/default/files/2018-08/AQM-SA_0.pdf> |
| S010 | Comprehensive Study on Air Pollution and Green House Gases (GHGs) in Delhi | IIT Kanpur (for Delhi Pollution Control Committee) | 2016-01 | full-text-read | <https://home.iitk.ac.in/~mukesh/Publications/DPCC_2016_SA%20study%20IIT%20Kanpur%20report_Comprehensive%20Study%20on%20Air%20Pollution%20and%20Green%20House%20Gases%20(GHGs)%20in%20Delhi.pdf> |
| S011 | From episodic smog to structural pollution: why vehicles remain Delhi's biggest challenge | Centre for Science and Environment (analysis) / Down To Earth | 2025-12-22 | full-text-read | <https://www.downtoearth.org.in/air/from-episodic-smog-to-structural-pollution-why-vehicles-remain-delhis-biggest-challenge> |
| S012 | Concentrations of fine, ultrafine, and black carbon particles in auto-rickshaws in New Delhi, India | Apte J.S., Kirchstetter T.W., Reich A.H., Deshpande S.J., Kaushik G., Chel A., Marshall J.D., Nazaroff W.W. | 2011 | full-text-read | <https://ce.berkeley.edu/sites/default/files/assets/users/kirchstetter/Apte%20et%20al%2C%20Particles%20in%20Auto-Rickshaw%20Exhaust%2C%20Atm%20Env%202011.pdf> |
| S013 | No govt-operated air quality monitoring station in about 40 pc of India's districts: Study (reporting Airvoice analysis) | PTI | 2026-03-31 | full-text-read | <https://theprint.in/india/no-govt-operated-air-quality-monitoring-station-in-about-40-pc-of-indias-districts-study/2893115/> |
| S014 | India's Air Quality Monitoring Covers Just 15% of India's Population, Says Report (reporting CSE State of India's Environment 2026) | Outlook Business | 2026 | full-text-read | <https://www.outlookbusiness.com/news/india-air-quality-monitoring-coverage-gap-15-percent-report-2026> |
| S015 | LPG subsidy can increase uptake, but interventions needed to counter myths and improve access | Mongabay India | 2023-09 | full-text-read | <https://india.mongabay.com/2023/09/lpg-subsidy-can-increase-uptake-but-interventions-needed-to-counter-myths-and-improve-access/> |
| S016 | No work, little compensation: Delhi's construction workers pay the price for its toxic air | Newslaundry | 2026-11-11 | full-text-read | <https://www.newslaundry.com/2026/11/11/no-work-little-compensation-delhis-construction-workers-pay-the-price-for-its-toxic-air> |
| S017 | With GRAP-4 enforcing construction ban, is government compensating daily wage labourers? | Down To Earth | 2024-12 | full-text-read | <https://www.downtoearth.org.in/governance/with-grap-4-enforcing-construction-ban-is-government-compensating-daily-wage-labourers> |
| S018 | Supreme Court directs NCR states to compensate construction workers for GRAP-related shutdowns | Scroll staff | 2025 | full-text-read | <https://scroll.in/latest/1079780/supreme-court-directs-ncr-states-to-compensate-construction-workers-for-grap-related-shutdowns> |
| S019 | Delhi govt to pay Rs 10,000 to workers hit by anti-pollution restrictions | PTI | 2025-12-17 | full-text-read | <https://theprint.in/india/delhi-govt-to-pay-rs-10000-to-workers-hit-by-anti-pollution-restrictions/2807368/> |
| S020 | Management and Shocks to Worker Productivity (NBER Working Paper 25865) | Adhvaryu A., Kala N., Nyshadham A. | 2019 (rev.) | full-text-read | <https://www.nber.org/papers/w25865.pdf> |
| S021 | The Price of the Air We Breathe, The Heat We Endure (Delhi household and workplace survey) | Azad R., Chakraborty S. | 2026-04 (posted; survey Sept 2025) | full-text-read | <https://peri.umass.edu/wp-content/uploads/2026/04/Kyoto_Final_Report_Delhi_March032026.pdf> |
| S022 | Exposures to fine particulate matter (PM2.5) and birthweight in a rural-urban, mother-child cohort in Tamil Nadu, India | Balakrishnan K. et al. | 2018-02-01 | abstract-only | <https://pubmed.ncbi.nlm.nih.gov/29227900/> |
| S023 | In-utero exposure to PM2.5 and adverse birth outcomes in India: geostatistical modelling using remote sensing and DHS data 2019-21 | Jana A., Pramanik M., Maiti A., Chattopadhyay A., Abed Al Ahad M. | 2025-07-02 | abstract-only | <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12220995/> |
| S024 | Beyond household and individual factors: examining the association between ambient air pollution and birth outcomes in India | Bera T., Rout N.R., Pradhan J. | 2025-06-13 | abstract-only | <https://www.cambridge.org/core/journals/journal-of-biosocial-science/article/beyond-household-and-individual-factors-examining-the-association-between-ambient-air-pollution-and-birth-outcomes-in-india/8D2CBFFDD49A08280E2E9E6D075412CF> |
| S025 | Cumulative effect of PM2.5 components is larger than the effect of PM2.5 mass on child health in India | Chaudhary E., George F., Saji A., Dey S. et al. | 2023 | full-text-read | <https://www.nature.com/articles/s41467-023-42709-1.pdf> |
| S026 | Ambient air pollution and daily mortality in ten cities of India: a causal modelling study | de Bont J., Krishna B., Stafoggia M. et al. | 2024-07-01 | abstract-only | <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11774940/> |
| S027 | How can we ensure schools are not disrupted by air pollution? | CEEW | 2025-12-19 | full-text-read | <https://www.ceew.in/blogs/how-can-we-ensure-schools-are-not-disrupted-air-pollution> |
| S028 | Study on Ambient Air Quality, Respiratory Symptoms and Lung Function of Children in Delhi | Central Pollution Control Board (with Chittaranjan National Cancer Institute) | 2012 | unreachable | <https://www.cpcb.nic.in/uploads/healthreports/Study-Air-Quality-health-effects_Children-2012.pdf> |
| S029 | Children's IQ plummets by almost 20 points in Indian state with high air pollution (reporting KIIT conference abstract) | Health Policy Watch | 2025 | search-snippet-only | <https://healthpolicy-watch.news/childrens-iq-plummets-by-almost-20-points-in-indian-state-with-high-air-pollution/> |
| S030 | The hidden burden of rural air pollution (reporting IIT Kanpur AMRIT sensor network in Bihar) | Mongabay India | 2026-07 | full-text-read | <https://india.mongabay.com/2026/07/the-hidden-burden-of-rural-air-pollution/> |
| S031 | Receptor Modelling Based Source Apportionment Study of Ambient Particulate Matter in Patna City, Bihar | TERI (supported by Bloomberg Philanthropies; with BSPCB) | 2021-09 | full-text-read | <https://www.teriin.org/sites/default/files/2021-09/Source_Apportionment_Study_of_%20Ambient_Particulate_Matter_in_Patna.pdf> |
| S032 | Report of CPCB in OA No. 240 of 2024 (Singrauli Pradooshan Mukti Vahini & Ors. vs Union of India & Ors.) | Central Pollution Control Board | 2024-09-10 | full-text-read | <https://www.greentribunal.gov.in/sites/default/files/news_updates/Report%20of%20CPCB%20in%20OA%20NO%20240%20of%202024%20(Singrauli%20Pradooshan%20Mukti%20Vs.%20UOI%20&%20Ors.).pdf> |
| S033 | Black carbon emissions from coal-fired thermal power plants in Singrauli (IJERPH 15(11):2472) | IJERPH authors (2018) | 2018 | abstract-only | <https://ideas.repec.org/a/gam/jijerp/v15y2018i11p2472-d180733.html> |
| S034 | Air Quality Assessment, Emission Inventory & Source Apportionment Study for Mumbai (Final Report) | CSIR-NEERI for Maharashtra Pollution Control Board | 2023-12 | full-text-read | <https://www.mpcb.gov.in/sites/default/files/inline-files/Final_SA%20%26%20EI%20Report_Mumbai.pdf> |
| S035 | Farm fires in Punjab, Haryana lowest in 5 years: CAQM | PTI | 2025-12-01 | full-text-read | <https://theprint.in/india/farm-fires-in-punjab-haryana-lowest-in-5-years-caqm/2796043/> |
| S036 | Effect of crop residue burning on respiratory health of an agricultural community in Patiala, India (conference abstract) | Uttreja M., Lal K., Sehgal M., Ghosh S.K. et al. | 2022-10-31 | full-text-read | <https://www.teriin.org/sites/default/files/2023-09/1694685266Uttreja%20et%20al.%20%282022%29-The%20Lancet%20Planetary%20Health.pdf> |
| S037 | Breaking the mold: transforming Bihar's brick kilns | WRI India | 2024-12-23 | full-text-read | <https://wri-india.org/perspectives/breaking-mold-transforming-bihars-brick-kilns> |
| S038 | New report reveals 'appalling' levels of slavery in India's brick kiln industry | Anti-Slavery International | 2017 | full-text-read | <https://www.antislavery.org/latest/report-slavery-india-brick-kilns/> |
| S039 | Migration to Brick Kilns in India: An Appraisal (policy brief) | Roy S.N., Kunduri E. | 2018-07 | full-text-read | <https://cprindia.org/wp-content/uploads/2021/12/Migration-to-Brick-Kilns-in-India.pdf> |
| S040 | Protecting schoolchildren from air pollution in Delhi: evidence from a two-year randomised controlled trial in KV schools (Policy Brief IND-24351) | Ruiz-Tagle J.C., Salazar Espinoza C.A., Kacker K., Sangwan N., Jaime M. | 2026-04 | full-text-read | <https://www.theigc.org/sites/default/files/2026-06/Ruiz-Tagle-Espinoza-Kacker-Sangwan-Jaime-Policy-Brief-April-2026.pdf> |
| S041 | Performance evaluation of smog tower at Connaught Place, New Delhi (final report) | IIT Bombay for DPCC | 2023-09-30 | full-text-read | <https://dpcc.delhi.gov.in/sites/default/files/DPCC/important-news/final_report_dated_30-09-2023_of_iit_bombay.pdf> |
| S042 | Smog towers ineffective, at least 40,000 needed in Delhi to combat toxic air: DPCC tells NGT | Down To Earth | 2023-11 | full-text-read | <https://www.downtoearth.org.in/pollution/smog-towers-ineffective-at-least-40-000-needed-in-delhi-to-combat-toxic-air-dpcc-tells-ngt-92841> |
| S043 | Are anti-smog guns the solution to Delhi's air pollution problem? | CEEW | 2025 | full-text-read | <https://www.ceew.in/blogs/are-anti-smog-guns-the-solution-to-delhi%E2%80%99s-air-pollution-problem> |
| S044 | Delhi has a new plan to fight its toxic air, but will it deliver? | Health Policy Watch | 2026-11-19 | full-text-read | <https://healthpolicy-watch.news/delhi-has-a-new-plan-to-fight-its-toxic-air-but-will-it-deliver/> |
| S045 | Unfair Quality: The impact of air pollution on three occupations (safai karamcharis, waste pickers, security guards) in Delhi | Chintan Environmental Research and Action Group (supported by Clean Air Fund) | 2023-06 | full-text-read | <https://www.chintan-india.org/wp-content/uploads/2023/08/Chintan_Unfair_Mail.pdf> |
| S046 | Delhi's air pollution is a public health emergency, so why aren't more people wearing masks? | EPIC (University of Chicago) researchers | 2019-11 | full-text-read | <https://epic.uchicago.edu/insights/delhis-air-pollution-is-a-public-health-emergency-so-why-arent-more-people-wearing-masks> |
| S047 | 'We are breathing smog to survive': Delhi's dirty air is killing the city's invisible workforce | RT (republished by IOL) | 2026-01-20 | full-text-read | <https://iol.co.za/news/world/2026-01-20-we-are-breathing-smog-to-survive-delhis-dirty-air-is-killing-the-citys-invisible-workforce/> |
| S048 | Health advisory and preparedness letters on air pollution (NPCCHH) | National Centre for Disease Control, MoHFW | 2024-2025 | search-snippet-only | <https://ncdc.mohfw.gov.in/uploads/pdf/Air%20Pollution%20advisory%20and%20letter%20by%20Sec%20Health-2024.pdf> |
| S049 | Supporting women construction workers to access protective measures for mitigating impacts of air pollution (case study) | Clean Air Fund | 2024 | full-text-read | <https://www.cleanairfund.org/case-study/supporting-women-in-construction-to-campaign-for-clean-air/> |
| S050 | Helping India's health workers become clean air champions (case study) | Clean Air Fund | 2023 | full-text-read | <https://www.cleanairfund.org/case-study/helping-indias-health-workers-become-clean-air-champions/> |
| S051 | India: World Bank approves financing for programs to promote clean air in Haryana and Uttar Pradesh states | World Bank | 2025-12-10 | full-text-read | <https://www.worldbank.org/en/news/press-release/2025/12/10/india-world-bank-approves-financing-for-programs-to-promote-clean-air-in-haryana-and-uttar-pradesh-states> |
| S052 | Delhi govt to install 400 additional tents to shelter more of the capital's homeless during winter | PTI | 2026-11-16 | full-text-read | <https://theprint.in/india/delhi-govt-to-install-400-additional-tents-to-shelter-more-of-the-capitals-homeless-during-winter/3100333/> |
| S053 | Clean air, choked finance: why India's war on air pollution is running out of cash | TERI | 2025 | full-text-read | <https://teriin.org/article/clean-air-choked-finance-why-indias-war-air-pollution-running-out-cash> |
| S054 | Global clean air funding: short-term win, long-term risk | Down To Earth (CSE) | 2026-11 | full-text-read | <https://www.downtoearth.org.in/air/global-clean-air-funding-short-term-win-long-term-risk> |
| S055 | Liquefied petroleum gas or biomass for cooking and effects on birth weight (HAPIN trial) | Clasen T.F., Chang H.H., Thompson L.M., Kirby M.A., Balakrishnan K. et al. | 2022-10-10 | abstract-only | <https://pmc.ncbi.nlm.nih.gov/articles/PMC9710426> |
| S056 | Provision of an LPG cookstove and fuel during pregnancy and infancy and linear growth trajectories (HAPIN) | HAPIN investigators | 2025-12-31 | abstract-only | <https://doi.org/10.1371/journal.pgph.0004831> |
| S057 | Making breathing room: research on clean air shelters | University of Washington DEOHS | 2024 | search-snippet-only | <https://deohs.washington.edu/hsm-blog/making-breathing-room> |
| S058 | Gig workers in India are exposed to highly polluted air and carcinogens, finds preliminary study (reporting Sekar et al., Atmospheric Pollution Research) | Mongabay India | 2023-08 | full-text-read | <https://india.mongabay.com/2023/08/gig-workers-in-india-are-exposed-to-highly-polluted-air-and-carcinogens-finds-preliminary-study/> |
| S059 | Riders in the smog: gig workers and pollution | Rest of World | 2024 | search-snippet-only | <https://restofworld.org/2024/riders-in-the-smog-gig-workers-pollution/> |
| S060 | Construction workers: Rs 38,000 crore cess funds for welfare unused | Business Standard | 2023-04-03 | full-text-read | <https://www.business-standard.com/india-news/welfare-boards-coffers-remain-full-construction-workers-woes-continues-123040301104_1.html> |
| S061 | India's gig workers win legal status, but access to social security remains elusive | TechCrunch | 2025-11-24 | full-text-read | <https://techcrunch.com/2025/11/24/indias-gig-workers-win-legal-status-but-access-to-social-security-remains-elusive/> |
| S062 | India launches NAMASTE scheme to recognize and support waste pickers | International Alliance of Waste Pickers | 2025-04-02 | full-text-read | <https://wastepickersinternational.org/2025/04/02/india-launches-namaste-scheme-to-recognize-and-support-waste-pickers/> |
| S063 | Occupational Safety, Health and Working Conditions Code, 2020: backgrounder | Press Information Bureau | 2025-11-22 | full-text-read | <https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251122702801.pdf> |
| S064 | NAMASTE scheme coverage figures (news and government summaries) | Various | 2025-2026 | search-snippet-only | <https://organiser.org/2025/08/24/310713/bharat/namaste-scheme-brings-safety-dignity-85000-sanitation-workers-covered-76000-get-safety-kits-ayushman-cards/> |