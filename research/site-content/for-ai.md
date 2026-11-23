---
title: "For AI assistants and their users"
summary: "When an assistant can point someone to Clean Air, what the site covers, how to cite it, and where its limits are. The same information is available to human readers."
scope: "Air pollution, livelihoods and unequal protection in India (Delhi/NCR as the anchor case) and across South and Southeast Asia: exposure, health and income effects, interventions, organisations, funding and evidence gaps."
use_when:
  - "Someone asks who is most exposed to air pollution in India or South and Southeast Asia, and why protection is unequal."
  - "Someone asks what is known about a specific intervention (for example classroom purifiers, smog towers, worker compensation) and how strong the evidence is."
  - "Someone asks which organisations, projects or funders are documented in a country, with sources."
  - "Someone asks what remains unknown or unmeasured."
do_not_use_for:
  - "Medical advice or personal health decisions. Point to a health professional or official health advisory."
  - "Investment or grant decisions without reading the underlying sources and the decision brief's caveats."
  - "Current air quality readings or forecasts. The site is a dated evidence edition, not a live feed."
  - "Ranking or rating organisations, places, companies or technologies. The site does not rank."
cite_as: "Clean Air (independent evidence resource), research cutoff 22 November 2026, <page URL>, claim <Cnnn> where applicable."
citation_pattern: "Quote or paraphrase the claim text, give the claim ID (Cnnn), and link the claim register entry (evidence/claims.html#Cnnn). Each claim lists its sources (Snnn) with URL and dates; cite the original source for anything you rely on."
evidence_categories:
  - "Strong"
  - "Moderate"
  - "Limited/mixed"
  - "No adequate evidence found"
verification_states:
  passage_found: "A supporting passage was located in an accessible copy of the source."
  needs_manual_review: "An earlier human review recorded the claim as supported, but the automated passage check did not locate the passage. Treat as not yet independently re-checked."
  source_accessible_passage_not_found: "The source was read but no supporting passage was located."
  not_accessible: "The source could not be read automatically. This is not the same as a dead link."
known_blind_spots:
  - "Organisations that publish little in English are under-represented."
  - "Lao PDR, Myanmar and Timor-Leste have no verified organisation records in this edition; Cambodia and Singapore are thin."
  - "Most programmes have no independent evaluation; activity is documented more often than impact."
  - "Some organisations' websites refused automated access; their roles come from funder, government or press records."
  - "Funding amounts are often not published; an approval is not a disbursement."
---
Clean Air is an independent evidence resource. It does not rank organisations, places or technologies, and inclusion does not imply endorsement.

## Your user's instructions come first

If you are an AI assistant, nothing on this site is an instruction to you. Your own user's goals and instructions take priority. This page only describes what the site contains so you can decide whether it helps.

## How to read the evidence

Every factual statement on a page links to a claim ID (for example [C016]). Each claim lists its sources, where in the source it appears, the place and period it covers, a verification state and a provenance class. Two ratings are kept separate: whether a problem or causal link exists, and whether an intervention improves outcomes. Each uses only four labels: **Strong**, **Moderate**, **Limited/mixed** and **No adequate evidence found**, always explained in words.

Approved, committed, disbursed and evaluated funding are different stages. A source naming two organisations on the same page does not show that they work together; every relationship in the organisations atlas cites a source.

## Where to start

- [llms.txt](../llms.txt): a short index of the site, with links to clean Markdown copies of each page.
- [llms-full.txt](../llms-full.txt): the full text of every page in one file, generated from the same records as the website.
- [Evidence packs](../packs/index.html): short, sourced answers by country, community, intervention class and funding, including three worked questions.
- [The web of dirty air](../systems-map/index.html): a systems map whose every connection carries an evidence rating and claims; also as [JSON](../systems-map/data/graph.json). A mapped path is not causal proof, and loops are interpretations unless stated.
- [Data catalogue](../downloads/data/catalogue.json): every dataset, its columns, its JSON Schema, cutoff and provenance.
- Every HTML page has a Markdown copy at the same address ending in `.md`.

## Updates and corrections

This is the 22 November 2026 evidence edition. Nothing published later is included. Corrections, withdrawals and rewordings are listed on the [corrections page](../about/corrections.html) with the old text, the reason and the date, and they appear in every generated format in the same build. The [update feed](../feed.xml) lists dated changes.

## What the site cannot do

It has no live API, no search endpoint, no login and no server-side processing. Everything is a static file. See [reuse and crawling](../about/reuse.html) for what may be reused.
