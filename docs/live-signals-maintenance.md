# Latest Signals: maintenance

## Commands

```
python3 tools/signals/ingest.py                    # live refresh of every enabled source
python3 tools/signals/ingest.py --only who-news    # one source
python3 tools/signals/ingest.py --dry-run          # fetch and report; write nothing
python3 tools/signals/validate.py                  # store, registry, review decisions
python3 tools/signals/test_signals.py              # fixture tests (no network)
python3 tools/check_signals.py                     # built pages, feeds, parity, refresh honesty (after site/build.py)
python3 tools/check_all.py                         # everything, as CI runs it
```

## Scheduled refresh

`.github/workflows/signals.yml` runs at 02:17 and 14:17 UTC and on demand (Actions tab, "Refresh signals", Run workflow; optional comma-separated source IDs). It runs the fixture tests, collects, validates, writes a summary table to the run page, and commits `research/signals/` to `main` if anything changed. `.github/workflows/pages.yml` listens for the refresh to complete and rebuilds and deploys the site through the full `check_all.py --browser` gate. A failed refresh leaves the published site as it was.

GitHub may delay scheduled runs and disables schedules after 60 days without repository activity; re-enable from the Actions tab. If `main` is protected against pushes from the workflow token, the commit step fails visibly; switch to opening a pull request or allow the bot to push (owner decision 1 in `docs/LIVE_SIGNALS_AUDIT.md`).

## Adding a source

1. Find the publisher's documented feed or API. Never guess a `/feed/` address.
2. Test it by hand: HTTP status, content type, a parseable response, item dates, and the publisher's terms. Do not bypass bot checks or paywalls.
3. Add an entry to `research/signals/sources.yml` with `test: {date, status, result}`, `rights: metadata_only`, `scope`, `requires`, `covers` for regional sources and `atlas_org_id` only for an exact match in `organisations.csv`.
4. Run `python3 tools/signals/ingest.py --only <id> --dry-run`, read `run-report.json` (included and excluded titles with reasons), adjust `taxonomy.yml` if needed, then run for real.
5. Run `python3 tools/check_all.py` and commit.

A source that stops working is isolated: its earlier records stay, its row on `/signals/sources.html` shows the last successful check and why the latest one did not succeed. Disable it (`enabled: false` with a `status_note`) if it keeps failing.

## Secrets

Only `OPENALEX_API_KEY` (optional, repository secret). It is read from the environment, sent only to the OpenAlex host, and redacted from the run report. No key is ever committed or shipped to the browser.

## Reviewing records

The generated queue is `research/signals/review-queue.csv` (unreviewed records, newest first). Add one row per decision to `research/signals/review-decisions.csv` (the header lists the columns). Rules enforced at build: a note needs `editorial_reviewed` and `note_source_refs`; a study summary needs design, outcomes and limits; a claim link needs `evidence_promoted` and an existing claim that cites the record's source; an amount needs a funding stage, a currency and `amount` in `checked_fields`, and never enters a funding total. A weekly note goes in `research/signals/notes/YYYY-MM-DD.md` with front matter `title`, `reviewed`, `status: reviewed`; without one the block is omitted.

## Takedowns and corrections

For a rights or privacy request, add a decision row with `review_status: withdrawn` and the reason, rebuild, and log the change in `research/data/corrections.csv` if it affected published text. For a wrong tag, fix the rule in `taxonomy.yml` (preferred) or exclude the record with a reason.

## Debugging a run

`research/signals/run-report.json`: per-source result, HTTP status, request (keys redacted), items, included and excluded counts, up to 300 excluded titles with reasons, the merge log, totals and the outcome. `research/signals/runs.csv` keeps one row per run. `research/signals/http-cache.json` holds ETag and Last-Modified values for conditional requests.

## Page size as the feed grows

List pages show at most `SIG_PAGE_SIZE` records (40, set in `site/signals_data.py`) so each stays inside the HTML byte budget in
`tools/design-tokens.json`. The index, recently indexed and awaiting-assessment pages show the newest 40. Monthly archives split into
parts (`archive/YYYY-MM.html`, then `archive/YYYY-MM-p2.html` and so on), and each record's anchor and `page_url` export follow its part.
If a budget failure names a signals page, lower `SIG_PAGE_SIZE` rather than raising the budget.

The refresh-honesty check in `tools/check_signals.py` ignores attribute text such as claim tooltips, which quote the register
(claim C011 mentions "real-time" stations), and reads only the page copy.
