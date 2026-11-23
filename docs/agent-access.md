# Agent access

How AI assistants (and people who prefer plain text or data) reach exactly the same content as the web pages. Everything is a static file on GitHub Pages under `https://arunbh2.github.io/clean-air/`. There is **no** API, search endpoint, authentication, content negotiation, custom header or server-side processing, and no file claims otherwise (`tools/check_agent_files.py` scans for over-claims).

## Files

| File | What it is | Generated from |
|---|---|---|
| `llms.txt` | Short Markdown index following the llms.txt **proposal** (a community convention, not a ratified standard). Links to the Markdown copy of each key page; optional resources last. | page metadata |
| `<page>.md` (314 files) | Markdown mirror of every HTML page except 404. Each starts with front matter (title, canonical HTML URL, cutoff, build date) and ends with the cutoff, endorsement and advice caveats. | the rendered `<main>` of the same page (`site/mdmirror.py`), so wording, caveats, citations and tables cannot drift |
| `llms-full.txt` | Every mirror in one file, with `===== PAGE: <url> =====` boundaries, cutoff and build date. 1.96 MB, budget 3 MB; not truncated. | the mirrors |
| `for-ai/index.html`, `for-ai.json`, `for-ai.txt` | When an assistant can point someone to Clean Air, scope, citation pattern, evidence labels, verification states, blind spots, update mechanics, not-medical/not-investment boundaries, and a prominent statement that the assistant's own user's instructions take priority. Visible to humans too. | `research/site-content/for-ai.md` |
| `packs/` (33 packs) | Short sourced answers: 3 worked questions, 9 countries, 15 affected communities, 5 intervention classes, 1 funding view. Each in HTML, Markdown and JSON with: short answer, what is known (claim, sources, verification state, provenance), uncertainties, responses with both ratings, organisations, funding records and links with stage, next questions, source IDs. | CSVs and `research/site-content/questions/*.md` |
| `downloads/data/claims.json` | Every claim with sources, verification state, provenance class, supporting excerpt, corrections. | `claims.csv`, `claim-passages.csv`, `corrections.csv` |
| `downloads/data/organisations-atlas.json` | Organisations (public fields), activity records, roles, funding links. | atlas CSVs |
| `downloads/data/*.csv` | Every research table, formula-escaped (see `catalogue.json` → `csv_escaping`). | `research/data/*.csv` (canonical files untouched) |
| `downloads/data/catalogue.json`, `downloads/schemas/*.schema.json` | Data catalogue (version, cutoff, build date, rights status, provenance, escaping) and a JSON Schema per dataset. This replaces an `openapi.json`, which would wrongly suggest an API. | CSV headers + `research/data-dictionary.csv` |
| `sitemap.xml`, `sitemap.json`, `sitemap.txt` | HTML pages; HTML + Markdown + data URLs with format version and an honest build date. | page list |
| `feed.xml` | Atom feed of genuine dated changes (editions and corrections only). | `changelog.csv`, `corrections.csv` |
| `robots.txt` | Allows all crawlers, points to the sitemap and the reuse page, and says it is not a licence. | fixed |
| `about/reuse.html` | Separate statements for search indexing, AI input, AI training and reuse; third-party rights preserved; undecided rights stated as undecided. | `pages/reuse.md` |

Every HTML page declares `<link rel="canonical">`, `<link rel="alternate" type="text/markdown">` to its mirror, `<link rel="describedby">` to `llms.txt` and the Atom feed, and shows a visible "Markdown version of this page" footer link.

## Base path

The base URL lives in `site/site.json` (override with `CLEAN_AIR_BASE_URL`). Canonical links, mirrors, `llms.txt`, sitemaps, packs and the feed all use it, and `check_agent_files.py` requires every listed URL to sit under it and map to a built file. Moving to a custom domain is a one-line change.

**Known limitation:** crawlers look for `robots.txt` and `llms.txt` only at a domain root. On a GitHub Pages project site they are served under `/clean-air/`, so they are informative rather than authoritative until the site has its own domain (owner decision 4).

## The three worked questions

| Question | Web | Markdown | JSON |
|---|---|---|---|
| Which organisations are working on air pollution and informal workers in Delhi? | `packs/questions/delhi-informal-workers.html` | `.md` | `.json` |
| Who funds clean-air projects in Bangladesh? | `packs/questions/bangladesh-funding.html` | `.md` | `.json` |
| Do low-cost air sensors reduce exposure? | `packs/questions/low-cost-sensors.html` | `.md` | `.json` |

`tools/test_formats.py` compares claim IDs, claim text, verification labels, amounts, funding stages, caveats and cutoff across the three formats and against `claims.json`, `organisations-atlas.json` and the funding-record pages a human would reach. Answers draw values such as the Bangladesh amount and the sensor rating from tokens (`{{amount:P01}}`, `{{int_rating:low-cost-sensors-action}}`) filled from the canonical CSV at build time, so a change in the record changes every answer.
