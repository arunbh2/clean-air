# CLAUDE CODE MASTER PROMPT
## Clean Air: one source of truth for the human reader, the maintainer, and the AI agent

**Site:** https://arunbh2.github.io/clean-air/index.html  
**Repository:** https://github.com/arunbh2/clean-air  
**Scope:** Entire Clean Air website, including the expanded Organisations and Funding Atlas pages. This is a governance, content-system, design-quality, accessibility and agent-accessibility upgrade. It is **not** a rebrand or a replacement of the existing research.

---

You are the lead editor, evidence engineer, design-system architect, accessibility engineer and static-site maintainer for Clean Air. Work in the actual repository, inspect before changing anything, implement the changes and run the tests. Do not deliver only recommendations, mock-ups or a plan.

## 0. The invariant

Every substantive decision must serve **three audiences simultaneously**:

1. **The human reader**, including a street vendor, district health officer, union organiser, parent, local journalist, researcher or foundation trustee, who wants an understandable, balanced, useful and evidence-backed answer.
2. **The maintainer**, who needs predictable source files, stable IDs, reusable components, deterministic builds, documented exceptions, change tracking and failing tests for preventable regressions.
3. **The AI agent**, which needs a truthful, convenient, source-linked machine-readable representation of exactly the same content, without scraping, fabricated APIs or instructions to override a user's goals.

**One factual record, multiple truthful presentations.** A change in a claim, grant, organisational activity, verdict or source should propagate automatically to web pages, Markdown mirrors, feeds, downloads and agent evidence packs. No parallel manually copied facts that can drift.

The site's identity remains **Clean Air: Shared air. Unequal protection.** Do not import Common Shade's branding, typography, illustrations, colours, menu system or deployment. Copy its *operating discipline*, not its appearance. Do not import Practical Action branding or a proprietary Economist font, asset, masthead or illustration.

## 1. Read and audit before editing

Read, in full, the repository's current `CLAUDE.md`, `docs/site-brief.md`, `docs/research-brief.md`, `docs/design-brief.md`, `docs/clean-air-10x-expansion-brief.md` (if present), relevant subsequent approved expansion briefs, and the research and site build scripts. Inspect representative current pages: homepage, people/livelihoods, interventions, organisations, funding, evidence, methodology, corrections, downloads and about. Determine the actual folder, generator, scripts, hosting base path, workflows, licenses and asset pipeline instead of assuming they exist.

Produce `docs/THREE_AUDIENCES_AUDIT.md` documenting:
- What already works, especially the existing claim/source IDs, evidence-strength categories, verification practices, `research/` to generated `site/` pipeline, `/corrections/` and `/update-policy/` if already present.
- Current site voice violations, with exact file references and reader-facing replacement proposals.
- Existing design tokens, component families, accessibility/performance baselines and design inconsistencies.
- Existing AI/readability/export files and which are absent.
- Each proposed new file, its canonical source, generator, tests and GitHub Pages URL.
- Decisions that require owner approval because they change rights, scope or established evidence standards.

Preserve existing URLs, source IDs (`Snnn`), claim IDs (`Cnnn`), evidence verdicts, historical funding snapshots and contextual caveats. Never renumber records just to fit a new schema.

**Authority and conflicts:** keep the existing `CLAUDE.md` precedence rules. The research cutoff remains **22 November 2026** unless the owner explicitly changes it in `CLAUDE.md`; do not silently add later-published research as though it belonged in that evidence snapshot. Apply the requirements below as a new *cross-cutting quality layer*. If they conflict with the current research standard or Clean Air visual identity, preserve the existing standard, document the conflict and propose the least-disruptive equivalent. Update `CLAUDE.md` to encode the new governance without deleting prior instructions.

## 2. A humane, non-accusatory public voice

The site speaks to people with different responsibilities and views without talking down to them or assigning guilt. Its audience may disagree about regulation, employment, industry, spending or personal protection. The site gives them common facts, viable options and an honest account of uncertainty.

Apply these editorial rules to **site-authored, reader-facing copy**: headings, ledes, articles, cards, tables, charts, labels, tooltips, buttons, empty states, alerts and generated Markdown mirrors. Do not incorrectly rewrite external source titles, citations, legal text or attributed quotations.

1. **No prescriptive “should” or “must” in the site's own voice.** Report requirements as facts and describe options. Example: “Eligible applicants are based in…” rather than “Applicants must be based in…”. For public safety, distinguish actual statutory obligations from the website's editorial preferences; do not erase a legal duty. Those may be accurately reported as “The regulation requires…”.
2. **No insinuation of wrongdoing or blame.** Prefer “data not located”, “outcome not independently assessed”, “the source does not establish”, “coverage remains incomplete”, “possible mismatch” over “failed”, “misleading”, “non-compliant” or “bad actor”. This applies to the editorial voice, not accurate descriptions of legal findings, harms, pollution or court orders. Never soften a documented serious harm to the point of inaccuracy.
3. **No em dashes** in public-authored prose. Use shorter sentences, commas, colons, parentheses or plain hyphens.
4. **No league tables or scores for countries, cities, governments, NGOs, funders, technologies or companies.** Directory completeness is a property of the research record, not the merit of an actor. No “best NGO”, “worst city” or “top ten air-cleaning companies”. Existing evidence-strength labels are **not** a ranking of places or people.
5. **No named individuals or journalists in new editorial prose, profile illustrations or illustrative quotes.** Named organisations, public institutions, programmes and source titles are fine. Keep bibliographic credits intact when legally or academically necessary in source metadata, without turning people into protagonists. Community examples are anonymised and illustrative unless documented and consented.
6. **Short, precise, concrete and calm.** One main point per paragraph. Expand “PM2.5”, “airshed”, “source apportionment”, “ambient” and similar terms on first encounter. Define why numbers matter, the measurement period and the unit. Avoid “game-changing”, “groundbreaking”, “holistic” and unsupported superlatives.
7. **Visible reader next steps.** A page about construction workers should link to the corresponding exposure evidence, relevant interventions, active organisations, funding record and what remains unknown; it should not end with a dead end or a general call to action.
8. **Do not confuse advocacy with a proven outcome.** “The organisation trained 75 people, according to the funder” is different from “the training reduced exposure”. “Approved finance” is not “disbursed finance” or “health impact”. “A programme exists” is not “the programme works”.

Add `docs/editorial-voice.md` with real Clean Air before/after examples, approved recurring phrases, evidence caveat patterns, terms to explain, and voice exceptions.

Implement `tools/check-voice.js` (or integrate equivalent existing build tooling). It inspects **all generated reader-facing HTML and Markdown**, including JSON strings rendered to the public, using extraction that avoids source code, citations, URLs, proper titles and quoted external text. Flag `should`, `must`, em dashes, unsupported rankings, judgement-laden descriptions, unnamed evidence ratings, accusatory framing, and unexplained abbreviations where practical. Because context matters, generate actionable file/line/report errors and support narrowly scoped, documented exceptions. Do not implement a simplistic regex that damages historically accurate text. Add positive and intentionally failing test fixtures proving the checker works.

## 3. Preserve Clean Air's design; enforce craft

Read `docs/design-brief.md` as the visual authority. Preserve Clean Air's existing tokens, including its paper/white/ink/navy, restrained red accent, link colours and editorial serif + system sans approach. Do **not** replace these with Common Shade's Anton, Hanken, Newsreader or orange/ember/green colour scheme.

Strengthen the existing design system by explicitly codifying the following:

- **No AI-template decoration:** no gradients, glows, grain, decorative noise, multicolour hero flourishes, left accent stripes on cards, heavy drop shadows, arbitrary icon sets, tiny labels or gratuitous motion.
- **Small, reusable component vocabulary:** define four base containers suited to Clean Air, such as `.ca-card`, `.ca-note`, `.ca-row` and `.ca-panel`, only if those do not already exist. Use three corner-radius sizes and three spacing/padding steps, or document the smallest compatible set already in the codebase. Shadows are for truly floating surfaces only, such as open menus.
- **Seven named type roles, not seven unrelated fonts:** page title, section heading, subheading, narrative/lede, body, caption/metadata, and numeric/table data. Use Clean Air's existing serif and system sans families, with deliberate scale and limited line-height tokens. No public text below 12px; body copy remains comfortably legible, ideally 18-20px for narrative passages. Maintain a readable line length.
- **Colour carries stable meaning:** brand accent, navigation, link, caution, evidence strength and measured AQI categories must have distinct, documented roles. Critically, keep existing CPCB AQI category colours separate from the site brand. Do not use green to imply a technology or intervention is proven, harmless or recommended. Evidence strength always has a text label, not colour alone.
- **Use lines, whitespace and typography for editorial hierarchy.** The homepage's initial screen should make the subject, who is affected and the first reading path instantly understandable without a decorative hero.
- **Motion earns its place.** Do not add animations merely to appear modern. Respect `prefers-reduced-motion`; any interactive chart or map provides a nonanimated, text-first equivalent. If an illustration is helpful, use purposeful, accessible, genuinely original simple diagrams; clearly label illustrative human scenes. Never use imaginary documentary photos or invented quotes.
- **Phone-first usability:** zero sideways overflow at 320px viewport with text enlarged to 200%; keyboard navigation and visible focus; coherent reading order; useful print styles; minimum WCAG 2.2 AA target-size treatment (24×24px or applicable exception) and roughly 44×44px mobile touch targets where practical. Test at 320, 375, 768 and desktop widths, including 200% zoom. Do not let invisible expanded targets overlap.
- **Budget the weight:** measure baseline bytes for each major page, image transfer, initial JS and CSS. Propose realistic budgets based on those measurements, then enforce them without breaking data-rich evidence pages. Avoid large client bundles; use progressive enhancement and static-first search/filter where possible.

Create or refine `docs/design-guardrails.md`. Implement focused checks `tools/check-stripes.js`, `tools/check-cards.js`, `tools/check-type.js`, `tools/check-colours.js`, `tools/check-contrast.js` (or equivalent with explicit command mapping). These are testable boundaries, not a demand to mimic the other website's aesthetics. Detect computed CSS and representative rendered DOM where static source scanning is insufficient. Include tests that make each checker fail on a deliberately bad fixture. Contrast tests cover normal and large text, links, focus, evidence chips and AQI legends.

## 4. Make evidence verifiable in more than a superficial sense

Preserve the existing four evidence categories exactly:
**Strong / Moderate / Limited-mixed / No adequate evidence found.**
Maintain separate assessments for **(A) whether a problem or causal relationship exists** and **(B) whether an intervention improves outcomes**. A grade must always come with a plain-English explanation, never a numerical popularity score or pseudo-precision.

Expand the research metadata **without invalidating older IDs**. Where applicable, each public factual claim has:
- Stable claim ID; exact text or minimally edited proposition; country/place/period/units; status (established, reported, inferred, disputed, withdrawn as appropriate).
- Stable source ID; publisher; publication date; access/check date; original URL; relevant section/page/table; brief supporting passage or exact locator; source type.
- **Passage-level verification state:** `passage_found`, `source_accessible_passage_not_found`, `not_accessible`, or `needs_manual_review`. Merely opening a page is never labelled “verified”. Do not publish a new factual claim as checked until the supporting passage has been located in an accessible source.
- Provenance classification: primary data / peer-reviewed study / independently evaluated study / regulator or official programme / funder report / implementing organisation self-report / media account / site inference.
- Outcome category: activity, output, observed change, independently attributed outcome, or long-term population effect. Keep correlation and causation separate.
- Where funding is involved: announced, approved, committed, contracted, disbursed, expended and independently evaluated are different states. Preserve source-defined meanings and do not infer missing stages.
- If a source cannot be checked automatically, say “could not be checked automatically”; a link that opens is “opened”, not “verified”, and a failed automated request is not automatically a “dead link”.

Any new NGOs, private firms, research groups, funders or project profiles added to the Organisations Atlas must meet the same standard. Commercial product claims are not independent outcome evidence. A source naming two organisations on the same page does not prove collaboration. All relationships in the funder–implementer–project graph need explicit source support.

Store a single canonical data model in `research/` (adapt CSV/Markdown/JSON structure already present), and generate public profiles, at-a-glance tables, evidence pages, Markdown alternatives, JSON/CSV downloads and agent packs from it. Do not maintain a human-only and agent-only version of the answer.

## 5. Corrections, withdrawals and visible uncertainty

Audit existing `/corrections/`, verification record and update policy before creating anything new. Preserve them and make them easier to maintain. A correction entry should identify: stable record/claim, what changed, old text/figure where appropriate, corrected statement, date, reason, source, affected pages and whether charts/downloads/packs were regenerated.

Support corrections for retracted studies, revised monitoring methods, adjusted sample sizes, wrong conversions, changed source URLs and interrupted project status. Removed or superseded claims remain traceable as withdrawn rather than disappearing from history. Do not fabricate a correction example. If no real Clean Air correction exists, use a clearly fake fixture **only in tests**, not on the public site.

Create a test that proves editing a canonical claim (or withdrawing it) updates the HTML, Markdown copy, full corpus, relevant JSON/CSV and affected evidence packs in one build. The correction page and data provenance remain visible to humans and agents.

## 6. Make the site agent-readable without scraping

Implement machine-readable access *only through capabilities a static GitHub Pages project can actually serve*. Do not claim a server, live API, HTTP content negotiation, dynamic requests, custom headers or authentication where none exists.

**GitHub Pages base-path discipline is essential:** the current project is published under `https://arunbh2.github.io/clean-air/`, **not** the web-domain root. Generate canonical absolute URLs or configurable base-aware links for every resource. Test all listed paths against the real deployed project prefix. If the project later uses a custom domain, the config should update the URLs deterministically.

Produce or improve these generated resources where appropriate:

A. `llms.txt`: concise Markdown index written for agents and humans. Follow the applicable community convention but describe any unratified proposal as a proposal, never an official standard. Link to the clean Markdown copy of each key section. Put optional secondary resources last. Prioritise evidence, organisations, interventions, funding, country guides, methodology, corrections and limitations.

B. `llms-full.txt`: complete canonical plain-text/Markdown corpus, generated from the **same** article/source records as the website. Include source and cutoff metadata, section boundaries, update/build date, and a deliberate size budget. If too large, document split files with a useful top-level index; do not silently truncate or omit caveats.

C. `for-ai/index.html`, `for-ai.json`, `for-ai.txt`: plain explanation of when an assistant may direct someone to Clean Air; scope (air pollution, livelihoods and unequal protection), evidence cutoff, attribution patterns, known blind spots, citation recommendations, update mechanics, not-medical-advice/not-investment-advice boundaries, and prominent statement that the agent's own user instructions take priority. Everything visible to agents is also available to human readers.

D. A Markdown mirror of **every substantive public page**, e.g. an `index.md` adjacent to its `index.html` if the build supports that convention. Each HTML page links to its Markdown mirror via `rel="alternate"` and, where useful, to the site-specific `llms.txt` via `rel="describedby"`. Use valid type attributes and working, base-aware URLs. Preserve heading order, data units, caveats, citations, tables and contextual links. Do not give a Markdown mirror inaccurate or more confident wording than the HTML.

E. `sitemap.json` with canonical HTML, Markdown and key structured-data URLs; continue supporting the conventional XML sitemap if present. Include a format version and honest timestamp. No pretend real-time updates.

F. `agents.txt`, `auth.md` ("none required" for public pages), `terms-of-use.md`, and a minimal `.well-known/` directory only to the extent those files have genuine, documented meaning. A `security.txt` must contain real maintainer contact and expiry or be marked pending owner action, not invented. Do not create empty standards-sounding files simply to look agent-ready.

G. `openapi.json` **only if** there is a real, documented static-data retrieval interface whose URLs and response structures the OpenAPI file can truthfully describe. Otherwise document the static files and schemas using a clear data catalogue instead. Do not claim a REST backend. Expose machine-readable JSON Schema for canonical datasets as useful.

H. Atom feed for content updates, and separate topic feeds only if the source includes genuine dated change records. Do not manufacture updates or fake freshness. No calendar unless Clean Air actually has dated public events or deadlines to represent.

I. JSON and CSV downloads for organisations, NGO programmes, private-sector interventions, funding relationships, case studies and evidence/source registers where public data rights and editorial policies allow. Include version, cutoff, updated date, provenance columns and data dictionary. Guard against spreadsheet formula injection (`=`, `+`, `-`, `@` and control/whitespace-prefix edge cases); test malicious fixtures and document the escaping method.

J. Evidence packs at `/packs/` for practical questions: one per country, affected community, intervention class, and an organisation/funder view where warranted. Each pack contains a short answer, what is known, source IDs, uncertainties, intervention evidence and next questions. Generate from canonical sources. Do not produce invented impact estimates or unreviewed funder claims.

K. `robots.txt` and text/data-mining permissions: publish an explicit, human-readable crawling and reuse policy. Do not pretend `robots.txt` legally grants copyright permission or reliably controls AI training. Search indexing, AI input, AI training and reuse need distinct, accurate statements. Make licensing and crawler choices explicit for the owner's original content, honour third-party rights, and do not treat external papers, logos, photos or quotations as CC BY just because the site's own writing is. If existing rights are unclear, record an owner decision rather than silently asserting universal CC BY 4.0.

## 7. Build, CI and maintenance: make the promises executable

Create or enhance a single documented validation command, such as `npm run check:all` if the repository is Node-based, adapting to the actual tech stack. It should run:

- Content compilation and schema validation; no orphan claim/source IDs or broken evidence joins.
- Passage-level source gating for all *new* “checked” claims and clear reports for historical records needing review.
- Voice checks on generated reader-facing copy, with controlled exceptions.
- Design token/card/stripe/type/colour checks and accessible contrast on representative pages.
- `tools/check-agent-files.js`: checks file presence, shape, valid base-aware links, Markdown mirrors, corpus section completeness, source/date coherence, non-empty packs, accurate public capability descriptions, and dataset/correction sync.
- Mobile/responsive, keyboard/focus, text zoom, reduced motion, print and size-budget tests. Add Playwright or equivalent browser tests if available; otherwise implement the best available checks and transparently label what was not visually tested.
- Broken internal-link and malformed external-link checks. For external URLs, distinguish `opened`, `passage matched`, `could not be checked automatically`, and `not found by source` where defensible. Avoid brittle CI that fails solely because a remote website blocks bots.
- HTML, structured JSON, RSS/Atom where used, and CSV/schema checks.
- A test proving changes to the canonical content are reflected everywhere after rebuild.
- Positive and intentionally failing fixtures for each major guard so a checker that does nothing cannot pass.

Wire this into the existing GitHub Actions build rather than inventing a second competing deployment. No deployment until the check command passes. If external network dependencies prevent verification, fail safely for genuinely new unsupported claims and report the blocker instead of silently marking it complete. Do not erase existing checks to make the pipeline green.

Keep documentation concise: `docs/editorial-voice.md`, `docs/design-guardrails.md`, `docs/agent-access.md`, `docs/data-model.md`, `docs/three-audiences-maintenance.md`, plus the audit. Document how a maintainer adds one claim, one organisation and one project/funding relationship, and which generated outputs change. A new contributor should need to edit one canonical record, not six pages.

## 8. Three end-to-end demonstration questions

Implement and test identical human-facing and agent-facing answers for these examples, using records actually present:

1. **“Which organisations are working on air pollution and informal workers in Delhi?”** The HTML view, organisation data, Markdown and pack should use the same records and caveats; no exaggerated impact or implied endorsement.
2. **“Who funds clean-air projects in Bangladesh?”** Distinguish a loan approval from actual expenditure, grants from lending, and a named implementing partner from an assumed partnership. If the canonical record lacks a funding amount, say so.
3. **“Do low-cost air sensors reduce exposure?”** Distinguish measurement, public communication, policy response and demonstrated exposure/health improvement; distinguish a supplier test from independent field evaluation. Do not rank sensor companies.

For each, provide a readable web journey (plain-language landing answer, relevant links, evidence) and an agent path (index, Markdown, JSON or pack). Write an automated comparison test for key values, source IDs, evidence caveats and dates across formats.

## 9. Work sequence and deliverables

Execute in this order, in the repository:

**Phase 1 – inspect and baseline.** Read all instructions; map the content generator; inventory existing pages and agent files; measure performance; produce `docs/THREE_AUDIENCES_AUDIT.md`.

**Phase 2 – editorial/source governance.** Add the public voice guidance and checks; enrich provenance metadata without losing IDs; implement verification states and corrections synchronization.

**Phase 3 – design-system hardening.** Consolidate existing components/tokens; install guard checks; correct any violations while preserving Clean Air's appearance and the strongest existing editorial patterns.

**Phase 4 – agent access and exports.** Generate Markdown, index files, full corpus, for-ai guide, structured datasets, feeds, packs and accurate permission documents from canonical records. Verify GitHub Pages base paths.

**Phase 5 – test and ship readiness.** Run validation, accessibility and screenshots; compare human and agent answers for the three demonstrations; document fixes and unresolved limitations. Make real code changes, not example-only files.

**Final response in Claude Code:** provide (1) short summary of actual changed files; (2) direct paths to new public pages/exports; (3) number of pages mirrored and packs generated; (4) checks run and pass/fail counts; (5) three demonstrator answers with provenance links; (6) unresolved issues, rights decisions and inaccessible sources; and (7) actual deployment state. Do not claim deployment unless it occurred and the links were checked.

## 10. Non-negotiable acceptance criteria

- Existing Clean Air branding, domain paths, research IDs, evidence categories and 22 November 2026 cutoff are preserved unless expressly authorised.
- No content drift between the published webpage and its generated Markdown, JSON, downloadable CSV or agent pack.
- New claims labelled “checked” have passage-level support. Approved, funded, implemented and evaluated remain separate.
- Every major page has a clear, jargon-light first answer and a deeper evidence layer.
- The Organisations Atlas includes NGOs and private-sector records without implying endorsement, success, partnership or independent validation when those are unproven.
- Voice, design, evidence, responsive/accessibility and agent-interface standards are backed by meaningful tests that fail on deliberately bad fixtures.
- The site is usable at 320px and 200% text zoom, has keyboard operation and reduced-motion support, and respects the measured performance budget.
- All machine-readable resources work under the GitHub Pages `/clean-air/` project prefix and describe only real static-site capabilities.
- No copied proprietary design assets and no automatic relicensing of third-party material.
- The work ends with **implemented, testable code and a candid verification report**, not a future-work plan.

**The editorial north star:** A reader, a maintainer and an AI assistant can all ask “who is doing what about air pollution, what has changed, and how certain is the evidence?” and arrive at the *same sourced, qualified answer* through different interfaces.
