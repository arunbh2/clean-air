# Latest Signals: method

The public explanation is generated from `research/site-content/signals-method.md` (`/signals/how-it-works.html`). This file is the maintainer's version, with the rules as code.

## Discovery is not verification

| Stage | Who | Where recorded | What it allows on the site |
|---|---|---|---|
| `discovered_unreviewed` | the scheduled job | `research/signals/signals.json` (the schema allows only this state there) | title, publisher, dates, tags, link, "Source record; not assessed by Clean Air" |
| `metadata_checked` | a curator | `research/signals/review-decisions.csv` | the same, labelled "details checked against the source" |
| `editorial_reviewed` | an editor who has read the source | decisions file, with `note_source_refs` | a "Why it may matter" note labelled as Clean Air's interpretation; a "What the study actually tested" block (question, design, outcomes, limits); the featured flag |
| proposed claim | the research process | `research/data/claims.csv` with passage verification, in a dated edition | nothing on the signal itself |
| `evidence_promoted` | after the claim exists | decisions file, `related_claim_ids` | a link from the signal to the claim; allowed only if the claim's sources include this record's URL or DOI (`tools/signals/validate.py`) |
| `excluded` / `withdrawn` | a curator | decisions file, with `reason` | removed from public lists; withdrawn records stay in the store |

Ingestion never writes a review state, claim link, editorial note, funding amount or evidence label. `validate.py` and the JSON Schema enforce this, and `tools/signals/test_signals.py` proves it with failing fixtures.

## Classification rules (`research/signals/taxonomy.yml`)

Inclusion needs an air-pollution term (in the title for research indexes; in the title or twice in the publisher's summary otherwise), a place in scope (unless the source covers only the region), no exclusion, and an HTTPS link. Text is unescaped, stripped of markup and normalised (NFKC, so PM₂.₅ reads as PM2.5) before matching. Titles naming a place outside the region with no place in scope are excluded. Instruction-like titles are held back. Country tags need a country, city or state in the title or summary; more than four countries from the summary become a regional tag; ambiguous names (Punjab, Hyderabad, Borneo, Kashmir) give no tag. Every decision is written to the run report with its reason.

Item types: research indexes give `research` or `preprint`; newsroom feeds give `news`; institutional and NGO feeds start from the registry's default and are refined by title words to `funding`, `policy` or `report`. Provenance comes from the registry; preprints are labelled as such. No public score or ranking exists.

## Deduplication

DOI first (normalised from any DOI URL form), then the cleaned canonical URL (tracking parameters removed), then the same title from the same non-research source (a URL change: the old URL moves to `previous_urls`). Records are linked, not merged, when they are a preprint and its journal version (`version`), the same story from another publisher within three days (`same story, other publisher`), or a correction or retraction notice (`correction`; the original is marked).

## Dates

`published_at` (the source's date, with `day`/`month`/`year`/`unknown` precision; `date_basis` says when it came from the article address), `source_updated_at`, `indexed_at` (index date for research), `discovered_at`, `last_checked_at`. Timeline order uses the publication date. More than 36 hours ahead of retrieval is `future-dated` and kept out of the timeline; less is labelled as a likely time-zone label. Undated records sit outside the timeline. A record older than 400 days is not added unless an index added it in the last 60 days.

## Refresh honesty

`status.json` holds `last_successful_refresh`, updated only when at least one source was read and the output validated. Per-source times and results are kept. The page shows the time in UTC; it says "Feed refresh delayed" if the build is more than 36 hours after the last success, and a small script shows the same message in the browser when the stamp is older than 36 hours at viewing time.

## Rights

`metadata_only` for every source: title, dates, publisher, link, tags. No description, abstract, image, author list or full text is stored. HTML is escaped by the templates; links are validated (HTTPS only).

## Coverage limits

See `/signals/sources.html` (generated) and `docs/LIVE_SIGNALS_AUDIT.md`. A thin feed reflects source coverage, not an absence of research or action.
