# A Breath of Change: integration audit

**Source:** World Bank (2025), *A Breath of Change: Solutions for Cleaner Air in the Indo-Gangetic Plains and Himalayan Foothills*, eds. Heger, Cros and Pople (S182). **Read:** 23 November 2026. **Cutoff:** 22 November 2026 (the book is eligible; data years are earlier and are named on each claim).
**Rights:** copyright World Bank. The PDF and its extracted text live only in `sources/private/` (git-ignored). Clean Air paraphrases, cites printed pages and reproduces no figures. The book's own rights statement allows non-commercial reproduction with attribution, but the brief's stricter rule (no wholesale reproduction) is followed.

## 1. What was read

| Part | Pages | Depth |
|---|---|---|
| Executive summary and overview (all 12 chapter summaries, all 4Is sections) | xv-li | read in full |
| Ch. 1 Why air quality matters; Ch. 2 Sources | 1-24 | read in full, figures inspected as images |
| Ch. 3-12 | 25-262 | targeted reading of the boxes, tables and sections used (listed in `research/breath-of-change/chapter-map.csv`); the remaining text was searched, not read word for word |
| Conclusion | 263-268 | read in full |

Every published claim was checked against the page text (`research/data/claim-passages.csv`, `passage-reviews.csv`).

## 2. Matrix

Classification: **reinforce**, **refine**, **add**, **flag contradiction**. Pages are printed pages; PDF page = printed + 52 in chapters.

| Finding | Pages | Existing claim or page | Relation | Content action | Data change | Interface change | Priority | Verification |
|---|---|---|---|---|---|---|---|---|
| 13-jurisdiction airshed, ~1 billion people | xvii | C123, C124 | reinforce | one-airshed page | C227 | places hub link | high | passage located |
| "35 by 35" aspirational interim target; WHO IT-1; Kathmandu Roadmap, Thimphu Outcome | xviii, 249, 264 | C003, C004 | add | home, one-airshed, guide | C228, C229 | target-wording check | high | passage located; national standards to re-check (C229) |
| Technology gains have not translated into cleaner air | xviii | C021, C111 | add | home module, 4Is guide | C230 | home | high | passage located |
| 52% local (model average); Terai 68% from other countries | xx-xxi | C029, C125 | add | where air comes from | C231, origins.csv | origins table; systems map E10 | high | passage located; bar values not printed |
| Chapter 2 jurisdiction figures differ from overview and chart | 22 | none | flag contradiction | origins page discloses both | C232 | status column | high | reviewer-located |
| Sector ranking; cooking 33% average and top four everywhere | xxi | C226, C025 | add (regional), not a Delhi replacement | origins page; E05 | C233 | sector table | high | reviewer-located |
| Industry 21%, MSMEs dominate, ground-level cluster exposure | xxix | C066, C105 | refine | kilns, boilers; E04 | C234 | | medium | passage located |
| Transport 10-40% (17%); largest in Delhi and Kathmandu | xxxii | C028, C029 | refine | E01 | C235 | | medium | passage located |
| Agriculture 12%; ammonia forms secondary PM | xxi, xxxv, 19 | C027 | add | new map node and links E55 | C236, C237 | systems map | high | located |
| 4Is framework | xxiii | none | add | 4Is guide; 4Is on every intervention; map toggle | C239, four-is.csv | new page, map control | high | reviewer-located |
| Abatement / protection / enablers | xxiii-xxiv | none | add | what works by job | C240, interventions.response_job | works index, intervention pages | high | located |
| 124 m households lack clean cooking; refill costs limit Ujjwala | xxvi-xxvii | C036, C037 | reinforce | stove-to-cooking sequence | C241 | 4Is example | high | reviewer-located |
| Clean cooking proposals; Bihar women entrepreneur model | xxvii, 38 | none | add | delivery pathway | C242, C243 | | medium | reviewer-located; model reports no measured exposure |
| Kiln technology table: zigzag 40-70% lower PM2.5, 1.5-4 yr payback | 59 | C069 (75%, 1-2 yr) | refine | kiln page, E44 | C244 | | high | reviewer-located; upstream sources named |
| Kiln adoption barriers despite payback | 59 | C070, C059 | refine | E45 reason | C245 | | high | located |
| Industrial finance proposals (guarantees 20%, subsidies 25-50%) | xxxi | none | add (proposal) | delivery lens | C246 | | medium | located |
| Surat shared boiler (company figures) | 65 | none | add | boilers, delivery | C247 | | low | reviewer-located; not independent |
| Surat emissions market: two different results in the book | xlvii, 240 | none | flag contradiction | guide; CEMS lever | C248 | | high | reviewer-located |
| Primary RCT: 20-30% lower emissions, ~11% lower cost | S183 abstract | none | add | delivery, CEMS | C249 (new source S183) | | high | reviewer-located in paper text |
| ETS unsuited to MSMEs, farms, households, crop burning | 240 | none | add | delivery | C250 | | medium | located |
| Fossil subsidies 1.2% GDP (9.8% implicit); MBI revenue 1.3% by 2030 | xxxii, xlvii | none | add | delivery | C251 | | medium | reviewer-located |
| Health coverage 55; 17% catastrophic spending; NHM <1% | xli-xlii | C087 | add | health readiness | C252 | | medium | located |
| Dhaka purifier ownership <1% | xli | C046 | add | protection | C253 | | low | located |
| Thailand clinics and clean-air centres (no outcomes) | 174 | C098 | refine | shelters lever | C254 | | medium | reviewer-located |
| Mask RCT is COVID-19, not air pollution | 174 | C085 | refine | masks lever, rating unchanged | C255 | | medium | located |
| Delhi graded health response plan | 171 | C087 | reinforce | health readiness | C256 | | low | located |
| 255 m students, 81% above 35 µg/m³ | 6-7 | none | add | home, schools | C257 | | high | reviewer-located |
| No classroom monitoring; Punjab indoor lower than outdoor at monsoon end | 197 | C075 | refine | schools pathway | C258 | | high | located |
| Closures: learning loss, unclear exposure benefit | 196 | C054, C055 | reinforce | schools | C259 | | medium | located |
| Teachers 90% willing to pay for purifiers | 198 | none | add | schools pathway | C260 | | low | located |
| Clean-air curricula absent; proposals | xliv-xlv | C074 | add | school education | C267 | | medium | reviewer-located |
| Fragmentation, not absence of policy | xlvi | C030 | add | 4Is guide | C261 | | high | located |
| Five regional cooperation functions; no regional financing | xlviii-l, 248-249 | C125, C220 | add | one-airshed page | C262 | | high | located |
| Smallholders 540 m; residue machinery unaffordable | xxxv-xxxvi | C067, C136 | refine | crop residue | C263 | | medium | located |
| Formalise informal waste sector (proposal) | xxxix | C106, C107 | add | waste pickers | C264 | | medium | located |
| Welfare cost 10.3% of GDP (PPP), 2019 | 10 | C018, C124 | refine (measure named) | people note | C265 | | medium | located |
| Peshawar scrappage with compensation | 102 | none | add | transport equity | C266 | | low | reviewer-located |

**What the book does not establish:** health or learning gains from classroom purifiers in the region; air-pollution benefits of mass masks or clean-air centres; worker outcomes after kiln conversion; livelihood losses of individual informal workers; any finding for Southeast Asia; that recommended finance instruments are funded.

## 3. Decisions on tensions

1. **Kiln figures (C069 vs C244).** The book's table gives lower emission cuts for natural-draught zigzag (40-60%) than C069's 75% and longer paybacks. Both are kept with sources; C069 is not changed. The kiln page shows both.
2. **Purifiers, masks, clean-air centres.** The book recommends them; it does not show regional outcome evidence. Clean Air's effectiveness ratings are unchanged and each page says why.
3. **Surat market results.** The book's two versions conflict; the primary RCT (S183) is cited for outcomes.
4. **Jurisdiction origin shares.** Overview, Chapter 2 text and Figure 3 differ for some places; only text-stated values are published, each with its page, and unprinted bar values are marked as not printed.
5. **Dated India portfolio options.** Unchanged. The delivery lens sits alongside them; no proposal became a funding record (enforced by `tools/check_boc.py`).

## 4. Answers to the brief's ten analytical questions

1. **Why technology has not cleaned the air.** The book says cleaner cooking, retrofits, fuels and vehicles have not translated into significant improvements and that growth will push emissions up (p. xviii, C230). Missing conditions: refill affordability and supply for cooking (C241), finance and enforcement for kilns (C245), fragmented institutions (C261). No study quantifying these gaps is cited.
2. **Sector priorities by place.** All model-derived (GAINS, 2020-24): cooking in Bihar, Uttar Pradesh and Terai; large industry in Greater Dhaka and Jharkhand; small industry in Nepal and Uttar Pradesh; transport in Delhi, Haryana, Kathmandu; agriculture in Uttar Pradesh, Bihar, Punjab; waste in Delhi; forest fires in Kathmandu (p. xxi, C238). None are observed measurements; Delhi's receptor studies (C025, C029) remain the measured local evidence.
3. **Abatement versus protection.** Abatement: the five sectors (Chs. 3-7). Protection: health and education (Chs. 8-9). Time-horizon conflict: protection is needed for a decade or more because reaching 35 µg/m³ may take that long (p. xxiv, C240); school closures protect briefly but cost learning (C259).
4. **Private sector.** The book describes clean-cooking enterprises as MSMEs needing results-based and concessional finance (p. xxvii), a role matrix for enterprises and financiers (Table 3.2, p. 41), a company-run steam utility (p. 65) and PPPs in waste and charging. It establishes roles and case descriptions, not independently measured results, except the Surat market (S183).
5. **Known institutions versus new ones.** Deliverable with existing institutions: inspection, fuel standards, health advisories, school protocols, municipal collection. Needing new infrastructure, authority or markets: shared boilers, charging, clean-fuel supply in rural areas, residue markets, a regional secretariat and financing window (pp. xxx-l).
6. **Where city-only action underperforms.** Where most pollution originates outside the city, such as Nepal's Terai (68% from other countries) and, on Chapter 2 text, Jharkhand and Bangladesh (C231, C232).
7. **Equity risks.** Report-derived: scrappage compensation and alternative work for operators (Peshawar, C266); informal waste workers' formalisation (C264); smallholders unable to afford machinery (C263). Clean Air's synthesis: kiln conversion may change workers' pay and debt (gap G6); restrictions cost daily earners wages (C040, C086).
8. **Plausible instruments without causal evidence.** Pay-as-you-go cooking finance, results-based finance for cookstoves, partial guarantees for kilns, school purifiers, clean-air centres, mask distribution for pollution, regional financing window. The Surat market is the exception with RCT evidence.
9. **Five fundable learning questions** (none substitutes for public duties): (a) Does results-based finance raise *sustained* clean-cooking use and lower personal exposure? (b) What happens to kiln workers' pay, debt and exposure after conversion? (c) Do classroom purifiers improve health or learning once behavioural offsets are addressed? (d) Can a particulate market or disclosure approach work for clusters of small plants? (e) Does a regional data platform change any jurisdiction's measures or concentrations?
10. **New versus already represented.** New: regional origin and sector picture, the 4Is, the three-job framing, delivery and capital-type lens, regional cooperation functions, emissions trading evidence, school exposure scale. Already represented: GRAP health advisories, Ujjwala refill limits, kiln technology, school closures, regional transboundary framing (C125).
