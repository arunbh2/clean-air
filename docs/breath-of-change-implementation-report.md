# A Breath of Change: implementation record

**Brief:** `docs/breath-of-change-integration-brief.md` · **Date:** 23 November 2026 · **Cutoff:** 22 November 2026 (unchanged)
**Branch:** `claude/focused-rubin-m4wcmo` · **Deployment:** not deployed. The live site changes when this branch is merged into `main` and CI passes.

## 1. What was read

The overview and executive summary (pp. xv-li, including every chapter summary and every 4Is section), Chapters 1 and 2 and the conclusion were read in full, with Figures 3 and 4 inspected as page images. In Chapters 3-12, the boxes, tables and sections used on the site were read (Table 3.2, Box 3.1, section 3.8, Tables 4.2 and 4.5, Box 4.4, Box 5.1, Table 8.1, Boxes 8.2 and 8.3, Table 8.4, pp. 195-198, Box 11.2, pp. 248-249). The rest of those chapters was searched in the extracted text, not read word for word. Nothing was inaccessible. The bars in Figures 3 and 4 carry no printed values, so those values were not estimated.

## 2. Most important new insights for Clean Air

1. **Air travels, by model estimate:** about half (52%) of PM2.5 in IGP-HF jurisdictions originates outside local boundaries; in Nepal's Terai 68% comes from other countries (C231).
2. **Household cooking is the one universal source:** the only top-four source in every modelled jurisdiction, 33% on average (C233). It is regional, not a Delhi figure.
3. **Technology has not been enough:** cleaner stoves, retrofits, fuels and vehicles have not yet translated into significantly cleaner air (C230); the constraint is fragmented institutions more than missing policy (C261).
4. **The 4Is:** information, incentives, institutions and infrastructure as prerequisites for any measure (C239), now on every intervention.
5. **Three jobs:** abatement, protection and enablers (C240), now labelling every intervention.
6. **Scale of child exposure:** about 81% of public-school students breathe air above 35 µg/m³; no country measures classroom air systematically (C257, C258).
7. **Emissions trading works for large monitored plants:** the Surat RCT found 20-30% lower emissions at about 11% lower cost (C249), but trading does not fit small enterprises, farms or households (C250).
8. **Regional cooperation is mostly proposed:** five functions are set out, but existing arrangements are voluntary and unfunded (C262).

## 3. Change log (local paths; live under `https://arunbh2.github.io/clean-air/` once merged)

| Page or file | Change |
|---|---|
| `index.html` (`home.html`, `home-modules.md`) | "Why cleaning the air is hard, and possible": three statements, three paths, source credit |
| `places/where-air-comes-from.html` (new) | Five steps from source to person; two separate tables (origin, sector) with page, period, method and status; what this does not tell us |
| `places/one-airshed.html` (new) | Local and regional action, 35 by 35 read carefully, five cooperation functions, existing versus proposed |
| `what-works/four-is.html` (new) | The 4Is with blockers, who holds each, interventions depending on each; worked examples: stove to cooking (six steps), small kiln, crop residue |
| `what-works/delivery.html` (new) | Four kinds of money; who pays for what and when for seven pathways, with what we know, what is proposed, what needs proof |
| `what-works/index.html` | Three jobs: every intervention grouped as abatement, protection or enabler |
| 25 intervention pages | Job label, 4Is prerequisites, "What the World Bank's 2025 book says" with claim citations; ratings unchanged |
| `organisations/funding/index.html` | "What will it take to deliver this?" lens; recommendations are not funding records |
| Organisation profiles (TERI, EPIC-India, ICIMOD) | "Named in the World Bank's 2025 book" with page and a no-partnership caveat |
| `people/index.html` | A regional cost is not one worker's lost earnings; link to the protection journey |
| `places/index.html`, `evidence/index.html` | Contextual links |
| `evidence/breath-of-change.html` (new) | Reading guide: five insights, three jobs, qualifications, chapter map, relation to earlier evidence, report-named organisations, citation |
| Systems map | New node (fertiliser and manure ammonia); new links E54-E57 (industry, ammonia, traffic to particles formed in the air; those particles across the airshed); report claims on E01, E03, E04, E05, E10, E44, E45; "Why implementation succeeds or fails" 4Is toggle; journey 6 "Protecting people while the air is cleaned" |
| Glossary | 11 terms: fuel stacking, abatement, protection, 4Is, results-based finance, emissions trading, MRV, cost-effectiveness, interim target, ammonia precursor, source attribution |
| Data | `research/breath-of-change/` (extraction register, origins, 4Is, delivery pathways, report-named organisations, chapter map); interventions gain `response_job`, `four_is`, `boc_note`; downloads `breath-of-change-*.csv` |
| Checks | `tools/check_boc.py` with injected-fault self-test; `passages.py` reads owner-supplied local text and no longer downgrades on a transient fetch failure; `rating_change_test.py` now closes its file before building (latent bug) |
| Agent files | `llms.txt` lists the new pages; Markdown mirrors, `llms-full.txt`, sitemaps and graph JSON regenerate from the same records |

## 4. Counts (from the data)

- **Sources:** 2 new (S182 the book; S183 the Surat RCT paper).
- **Claims:** 41 new (C227-C267), all with page locators and a located passage (24 automated, 17 reviewer-located). No existing claim changed meaning; no existing rating changed.
- **Interventions:** 25 updated with job, 4Is and a report note; 0 new interventions.
- **Organisation relationships:** 0 new partnerships or roles. 3 existing profiles marked as named in the book; 4 report-named organisations logged as leads only.
- **Funding records:** 0 new. The book's instruments are shown as proposals in the delivery lens.
- **Systems map:** 41 nodes (+1), 56 links (+4), 6 journeys (+1), 78 claims linked (+9).

## 5. Evidence conflicts and decisions

- Kiln emission cuts and paybacks differ between C069 and the book's table (C244): both kept with sources.
- The book gives two results for the Surat market (C248); the primary RCT (C249) is cited for outcomes.
- Chapter 2 jurisdiction origin shares differ from the overview and figure (C232): both shown, each with its page.
- Purifiers, masks and clean-air centres are recommended in the book without regional outcome evidence: Clean Air's ratings are unchanged and each page says so.
- "35 by 35" is presented only as an aspirational interim target, never as the WHO guideline (enforced).

## 6. Tests run

`python3 tools/check_all.py`: **19 of 19 passed**, including the new report checks and their negative test. The self-test injected a wrong WHO target, a bogus funding record citing the book, an orphaned claim ID and a percentage given in µg/m³, and all four were caught (plus a proposal worded as a finding). The real-data run also caught three genuine issues, which were fixed: C264 worded as a finding, C262 mentioning 35 by 35 unqualified, and quoted passages being misread. `node site/qa/qa.js` (Playwright + axe, 363 pages): **every check passed**, including cutoff on every page, one h1, 0 broken links or anchors, 2,417 citations all resolving to claims, keyboard focus, no horizontal scroll at 320 px and at 320-1280 px with 200% text on representative pages (now including the four new pages).

## 7. Published, internal and needing permission

- **Published (once merged):** the pages and data above.
- **Internal only:** the PDF and its extracted text (`sources/private/`, git-ignored); the extraction register is public but contains no copied passages beyond short locators.
- **Needs another source or permission:** exact Figure 3 and 4 values (would need the World Bank's underlying data); national 35 µg/m³ standards (C229) against each government's notification; current status of the regional platform beyond the book's 2025 description; the four lead organisations before any atlas record; reproduction of any figure (not attempted).

## 8. For funders: what changed in our understanding?

The World Bank's book does not change what Clean Air rates as working. It changes how a funder can see why things that work on paper do not reach people.

**First, the air is regional.** On the book's model estimates, about half the fine particles in the Indo-Gangetic plain's jurisdictions come from outside local boundaries, and in places such as Nepal's Terai most does ([where our air comes from](../places/where-air-comes-from.html)). City programmes still matter, but a grant that measures success only by one city's average may be judging the wrong thing. Regional coordination exists mostly as dialogue; the book's proposed secretariat and financing window do not yet exist ([one airshed](../places/one-airshed.html)).

**Second, household cooking is the one source everywhere.** It is the only top-four source in every modelled jurisdiction. India's experience shows the gap between a connection and clean cooking: refills, supply and habits decide whether the old stove goes out ([the 4Is](../what-works/four-is.html)).

**Third, the bottleneck is delivery.** The book's 4Is (information, incentives, institutions and infrastructure) explain why sound technologies stall. Clean Air now shows, for every intervention, which of the four it depends on, and for seven pathways who pays upfront, who pays to keep it running, and what still needs proof ([who pays](../what-works/delivery.html)). The pattern is consistent: public budgets carry enforcement, health services and waste collection; commercial capital fits equipment with revenue, such as shared boilers; philanthropy fits where learning, measurement or a fair transition is missing.

**Fourth, one market-based tool has randomised evidence.** Surat's particulate emissions market cut emissions by 20-30% at lower cost in a randomised evaluation. It needs continuous monitoring and large plants, so it does not solve kilns, farms or households.

**What has not changed:** classroom purifiers, masks and clean-air centres remain unproven for health or learning in the region, whatever their appeal. Worker outcomes after kiln conversion and the earnings informal workers lose to pollution are still unmeasured. Those are the questions a foundation can fund without taking over a public duty.
