# Clean Air

Clean Air is a standalone evidence website and research dossier about air pollution, livelihoods
and unequal protection in India, with Delhi/NCR as the anchor case.
Descriptor: *Air pollution, livelihoods and unequal protection.* Tagline: *Shared air. Unequal protection.*

## The briefs (read before substantive work)

| Brief | Governs | Wins on conflict over |
|---|---|---|
| `docs/site-brief.md` | What the site contains, its navigation, user journey and build rules | research brief |
| `docs/research-brief.md` | Evidence, method, required outputs and the quality check | — |
| `docs/design-brief.md` | How the site looks: colour, type, logo, layout, visual checks | — (visual polish must never distort the evidence) |
| `docs/clean-air-10x-expansion-brief.md` | The current mandate: regional expansion, layered reading, funding atlas, decision pathways | the site brief on scope and structure; never over the evidence standards, cutoff, claim/source IDs or design tokens above |
| `docs/organisations-10x-brief.md` | The Organisations section: ecosystem atlas, organisation–project–funder links, private-sector diligence | the site brief on the Organisations section only; never over the evidence standards, cutoff, IDs or design tokens above |
| `docs/three-audiences-governance-brief.md` | Cross-cutting quality layer: editorial voice, design guardrails, passage-level verification, corrections sync, agent-readable exports (llms.txt, Markdown mirrors, packs) | adds requirements across all sections; never over the evidence standards, cutoff, IDs, verdicts or design tokens above (conflicts are documented, not silently resolved) |
| `docs/systems-map-master-brief.md` | The Web of Dirty Air: the interactive systems map (`/systems-map/`), its graph data, loops, levers and journeys | the site brief on the systems map only; never over the evidence standards, cutoff, IDs, verdicts, design tokens or three-audience governance above |
| `docs/breath-of-change-integration-brief.md` | Integrating the World Bank's *A Breath of Change* (2025) across the site: sources explainer, 4Is, what works by job, funding lens, systems map, regional collaboration | the site brief on these integrations only; never over the evidence standards, cutoff, IDs, verdicts, design tokens, three-audience governance or systems-map rules above. The PDF lives in `sources/private/` (git-ignored, copyright World Bank) |
| `docs/live-signals-master-brief.md` | Latest Signals (`/signals/`): a scheduled, curated discovery feed of external news, research, reports, policy and funding, with its own source registry, schema, review queue and Atom/JSON outputs | the site brief on the signals section only; never over the evidence standards, cutoff, IDs, verdicts, design tokens or three-audience governance above. Signals are discovery records, not evidence: they never change the research cutoff, claims, ratings or funding totals without a documented review |

The website **is** in scope. The site brief overrides the research brief's line about not building one.
The expansion brief (owner instruction, 22 November 2026) is the updated mandate. It extends the site in place: keep existing
URLs, claim IDs (`Cnnn`), source IDs (`Snnn`), verdicts and the four India portfolio options as a dated baseline.
New records append (`C111+`, `S069+`). Audit: `docs/CURRENT_STATE_AUDIT.md`.
Reference logos: `docs/assets/wordmark.png` and `docs/assets/airflow-icon.png`. They are references
for the redrawn assets, not final files.

## Rules that apply everywhere

### 1. Research cutoff date: 22 November 2026
- Evidence is searched up to and including **22 November 2026**. Anything published later is out of scope
  unless the cutoff is formally moved here.
- Show the cutoff on the site, in every report and brief, and include it in output filenames
  (e.g. `clean-air-decision-brief_cutoff-2026-11-22.pdf`).
- Keep current conditions, seasonal episodes and long-term exposure separate. Use comparable time periods
  and flag incomplete data.

### 2. Never invent
Do not invent any of the following:
- current programmes
- quantitative impacts
- community quotations
- costs
- partnerships
- funding relationships
- claims of programme success

Also: no invented returns or cost-effectiveness ratios. Costs are either sourced ranges or explicitly
labelled planning assumptions, with capital, operating and evaluation costs kept separate.
If evidence is inaccessible or contradictory, record that. If browsing is unavailable, mark the work incomplete.
Every factual claim on the site must trace to a source-register entry with a URL and date.

### 3. Evidence categories
Use only these four labels, and explain each judgement in words (no unexplained scores):

**Strong** | **Moderate** | **Limited/mixed** | **No adequate evidence found**

- Rate two things separately: (A) confidence the problem or causal relationship exists, and
  (B) confidence the intervention improves outcomes.
- Keep four cases apart: absence of evidence; evidence of no effect; evidence of harm; evidence of benefit
  under conditions that may not transfer locally.
- Being unstudied locally does not make an intervention ineffective. Being unmonitored does not make
  a settlement low-exposure.
- One established link does not make a whole causal pathway "proven".
- Classify funding options as **A** ready to support, **B** promising but needs adaptation, **C** needs proof of
  concept or stronger causal evidence, **D** not recommended on present evidence.

### 4. Clean Air is an independent brand. Don't use Practical Action styling.
- No Practical Action palette, fonts, logos, lock-ups or document templates. Do not load the `pa-*`
  skills (including the `-2026` versions) for anything in this repo.
- Do not imply endorsement by Practical Action, any foundation, or any organisation named in the research.
- Do not inherit Common Shade or beattheheat.asia branding, menus, analytics or deployment.
- Do not reproduce The Economist's masthead, illustrations or proprietary assets. Borrow its editorial
  principles only.
- Do not assume a domain has been bought or chosen.

### 5. Design brief (summary; `docs/design-brief.md` is authoritative)
- **Principles:** restrained colour, deliberate typography, clear wayfinding, generous whitespace, consistent layouts.
- **Tokens:**
  ```css
  --ca-ink: #1A1A1A;   --ca-navy: #141F52;  --ca-accent: #E3120B;
  --ca-link: #2E45B8;  --ca-paper: #F5F4EF; --ca-surface: #FFFFFF;
  --ca-muted: #595959; --ca-rule: #D9D9D9;  --ca-tint: #EBEDFA;
  ```
  Paper and white for surfaces, ink for text, navy for navigation, red sparingly.
  No full-page red warning panels.
- **Contrast:** red on paper is about 4.4:1. Use it only for large text, rules and icons. Small red text
  goes on white (about 4.8:1) or uses a darker red.
- **AQI colours** stay separate from brand colours. Use the verified CPCB classification, always with text labels.
  **Never use green** to imply an intervention is proven or risk-free.
- **Type:** an editorial serif (start with Georgia) for headlines and narrative, system sans-serif for navigation,
  filters and tables. Narrative text 18–20px with a measure of about 65 characters, and tabular numerals
  for comparisons. Check the licence of any added font.
- **Logo:** one master SVG airflow geometry with flat fills and no embedded rasters. The wordmark is live or
  licensed text, so never claim an exact match to the reference lettering. Produce six versions: horizontal,
  reversed, navy mono, white mono, symbol, and a 16/32px favicon. The home link's accessible name is
  "Clean Air — home", and decorative duplicates are hidden from assistive technology.
- **Layout:** structure comes from rules and whitespace. Use cards only for distinct interactive objects.
  Corners are subtle, with no decorative gradients or heavy shadows. Grid gaps are 12px on small screens and
  16px on larger ones. Evidence details expand without hiding the main finding.
- **Intervention pages, in this order:** what it does → who benefits → evidence → operating requirements → costs and uncertainties.
- **Verify before calling it done:** contrast, keyboard focus, mobile, text zoom, print, logo transparency and
  load performance, plus screenshots at mobile and desktop widths.

### 6. Build rule
Site pages are generated from `/research` (Markdown and CSV), not hand-written copy. Changing a rating in the
evidence map must change the site.

### 7. Three-audience governance (`docs/three-audiences-governance-brief.md`)
Every change serves the human reader, the maintainer and the AI agent from **one canonical record** in `research/`.
- **Voice** (`docs/editorial-voice.md`): no "should"/"must" in the site's own voice, no blame wording, no em dashes in
  site-authored prose, no rankings, no hype; legal duties reported as "the rule requires". Enforced by `tools/check_voice.py`.
- **Design** (`docs/design-guardrails.md`, `tools/design-tokens.json`): tokens only, four container families, no left
  stripes, shadows or gradients, minimum 12px text, zoom-safe at 320px with 200% text. Enforced by `tools/check_design.py` and `site/qa/qa.js`.
- **Evidence** (`docs/data-model.md`): every claim has a passage-level state in `research/data/claim-passages.csv`
  (`research/analysis/passages.py`). New claims after C222 marked `read` need `passage_found`. Corrections and withdrawals go in
  `research/data/corrections.csv`; claims are never deleted (status `withdrawn`). Approved, committed, disbursed and evaluated stay separate.
- **Agent access** (`docs/agent-access.md`): Markdown mirror of every page, `llms.txt`, `llms-full.txt`, `for-ai`, packs, catalogue,
  feed: all generated, never hand-written. Base URL only in `site/site.json`. Describe only real static-site capabilities.
- **One command:** `python3 tools/check_all.py` (`--browser` for the Playwright/axe suite). CI runs it before deploying. Never weaken
  a check to pass; add a narrow, documented exception instead. Maintenance steps: `docs/three-audiences-maintenance.md`.
- Owner decisions still open (licence, AI training, security contact, custom domain): `docs/THREE_AUDIENCES_AUDIT.md` section 6.

### 8. The web of dirty air (`docs/systems-map-master-brief.md`)
- Canonical graph in `research/systems-map/` (systems, nodes, edges, cycles, levers, institutions, lever-roles, journeys, questions, ledger).
  Generated by `site/build_map.py` into `/systems-map/` (SVG map, text alternative, loops, levers, journeys, method, data exports).
- Every measured edge cites claim IDs; hypotheses are labelled, dotted and never rated Strong or Moderate. Loops must close and are
  interpretations unless studied end to end. Levers reuse intervention IDs and take their effectiveness rating only from `interventions.csv`.
- Organisations and funders appear on a lever only through verified atlas roles. Never write "will eliminate", "saves lives" or "breaks the loop".
- Enforced by `tools/check_systems_map.py` (in `tools/check_all.py`). Maintenance: `docs/SYSTEMS_MAP_METHOD.md`.

### 9. A Breath of Change (`docs/breath-of-change-integration-brief.md`)
- The World Bank book is source S182 (cited by printed page; PDF page = printed + 52). Findings live in `research/breath-of-change/`
  (extraction register, origins, 4Is, delivery pathways, report-named organisations, chapter map) and claims C227-C267.
- "35 by 35" is always aspirational or interim, never the WHO guideline. Origin shares and sector shares are never combined. Modelled
  shares are not measurements. A World Bank recommendation is never a funding record. Ratings change only through a documented review.
- The PDF and its text stay in `sources/private/` (git-ignored). Enforced by `tools/check_boc.py`. Audit: `docs/research/world-bank-breath-of-change-integration-audit.md`.

### 10. Latest signals (`docs/live-signals-master-brief.md`)
- **Narrow cutoff exception.** `/signals/` is a rolling discovery feed and may hold records published after 22 November 2026. These records do not
  change the research cutoff, the claim register, any evidence rating or verdict, funder assessments or any assertion elsewhere on the site.
  Only a documented review in a new dated research edition can turn a signal into a claim.
- Canonical files in `research/signals/` (sources.yml registry with a recorded test per endpoint, taxonomy.yml rules, schema.json, signals.json store,
  review-decisions.csv, status.json). Ingestion: `tools/signals/` (standard library HTTP, HTTPS allowlist, metadata only, no article text).
  Schedule: `.github/workflows/signals.yml` (02:17 and 14:17 UTC), which triggers the deploy workflow.
- Signals never carry an evidence-strength label. Ingestion only writes `discovered_unreviewed`; editorial notes, claim links and funding amounts come
  only from reviewed rows in `review-decisions.csv`. Unverified amounts never enter funding totals. `feed.xml` stays reserved for site updates and corrections.
- **Reviewer (owner decision, 23 November 2026):** signal review is delegated to Claude. Reviewer value `AI reviewer (Claude), delegated by the editor`;
  the site discloses AI review on every reviewed record. Read the source before any note; never write a claim or change a rating from a signal.
- Enforced by `tools/signals/test_signals.py`, `tools/signals/validate.py`, `tools/check_signals.py` and `tools/signals/test_base_url.py` (all in `tools/check_all.py`).
  Audit and owner decisions: `docs/LIVE_SIGNALS_AUDIT.md`. Method: `docs/live-signals-method.md`. Maintenance: `docs/live-signals-maintenance.md`.

## Which skill for which job

Clean Air's own identity governs every visual output. Generic skills handle file mechanics and must
use the Clean Air tokens, never their default themes.

| Situation | Skill |
|---|---|
| Large evidence scans across many sources | `deep-research` |
| Systems diagnosis, leverage points and second-order pathways | `vr4pp`, `system-shift` |
| Pressure-testing portfolio options or a "what not to fund" call | `llm-council`, `thinking-steel-manning`, `decision-making` |
| Structuring the decision brief and portfolio concepts (the thinking, not the file) | `proposal-craft`, `exhibit-craft` |
| CSV tables, source register, reproducible analysis | `document-skills:xlsx` |
| PDF exports of the report and brief | `document-skills:pdf` |
| Any chart, map or data display | `dataviz` (read it before writing chart code) |
| Site design and components | `frontend-design`, `design-skills:design-systems`, `design-skills:interaction-design` |
| Logo and SVG work | `design-skills:design-systems`, `design-council` for critique |
| Accessibility checks | `design-skills:accessibility-audit` |
| Interface copy, labels, empty and error states | `design-skills:ux-writing` |
| Browser testing and screenshots | `example-skills:webapp-testing` |
| After a substantive answer the user will act on (once per conversation) | `discernment-nudge:discernment-nudge` |
| Claude API questions | `claude-api:claude-api` |

Not for this repo: every `pa-*` skill, `bcg-presentation`, `pwc-presentation`, `example-skills:brand-guidelines`,
`example-skills:theme-factory`. Use `voice-dna` only if the user asks for something under their own byline.

## Environment notes

- The **Clean Air** cloud environment's setup script installs `document-skills`, `example-skills`, `claude-api`,
  `academy-guide` and `discernment-nudge` from `anthropics/skills`, pinned to commit
  `e4bb5d960d87126ff3b3a8af1a104b7db67560ba`. It installs them from a local copy at
  `/opt/anthropic-skills-pinned` under the marketplace name `skills-pinned`.
- Don't upgrade those plugins or run `claude plugin marketplace update` unless asked.
- If an expected skill is missing, check `claude plugin list` and tell the user. Don't silently substitute another.
