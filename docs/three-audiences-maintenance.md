# Maintaining Clean Air for three audiences

Edit one canonical record. Run one command. Everything else follows.

```bash
python3 tools/check_all.py
```

Add `--browser` to include the Playwright and axe suite (needs `site/qa` dependencies; CI always runs it). CI (`.github/workflows/pages.yml`) runs `check_all.py --browser` on every pull request and push. Nothing deploys unless every check passes.

## Add one claim

1. Append a row to `research/data/sources.csv` (next Snnn) if the source is new. Its publication date has to be on or before 22 November 2026.
2. Append a row to `research/data/claims.csv` (next Cnnn) with the locator, place and period. Write the claim in the site's voice (`docs/editorial-voice.md`).
3. Run `python3 research/analysis/passages.py`. If the state is not `passage_found`, mark the claim `provisional` or fix the claim or source. The validator refuses a new `read` claim without a located passage.
4. Cite it as `[Cnnn]` in any Markdown or CSV text.
5. `python3 tools/check_all.py`.

What changes automatically: the claim register (HTML, Markdown), every page that cites it, `claims.json`, `claims.csv` download, `llms-full.txt`, every pack that includes it, and the coverage dashboard.

## Add one organisation

1. Append a row to `research/data/organisations.csv` with `claim_ids` and/or `source_ids`, `category`, `countries_active`, `summary` and `date_last_checked`. Companies need `independent_test` filled in, or "No independent test found".
2. `python3 tools/check_all.py`.

What changes: a profile page and its mirror, the explorer, places, compare, country packs, `organisations-atlas.json`, the catalogue's row count, `llms-full.txt` and the sitemaps.

## Add one project and funding relationship

1. Append the activity to `projects.csv` (next Jnnn) with outputs, measured outcomes and evaluation in separate fields.
2. Append one row per organisation to `organisation-project-roles.csv`, each with its own source. Two names on the same page do not make a partnership.
3. Append the money to `funding-flows.csv` (next FLnnn). Record the stage in the source's own words (`commitment_or_disbursement`); leave `amount` blank unless a primary public record states it.
4. `python3 tools/check_all.py`.

What changes: the project page, both profiles' "Funding and partners", Follow the money, country and funding packs (including the Bangladesh worked question if relevant), JSON exports and the feed (corrections only).

## Correct or withdraw a claim

1. Edit the claim text in `claims.csv`, or set its status to `withdrawn` (never delete the row).
2. Append a row to `corrections.csv` with the earlier wording, change type, reason and date.
3. `python3 tools/check_all.py`. `tools/test_propagation.py` shows how one edit and one withdrawal reach HTML, Markdown, `llms-full.txt`, JSON, CSV, packs, the corrections page, `for-ai.json` and the feed in a single build.

## When a check fails

| Failure | Where to look |
|---|---|
| `voice` | file and line in the built page. Find the sentence in `research/` and reword it. A genuine exception goes in `tools/voice-exceptions.csv` with a reason. |
| `design` | the CSS selector. Use a token, a registered container family, or a top rule instead of a left stripe. |
| `links` / `reader` | the page and href. A record page needs a plain first answer and onward links. |
| `agent files` | a missing mirror, a dead URL in `llms.txt`, an over-claim, or a formula-trigger cell. |
| `formats` | an HTML, Markdown or JSON value that differs for a worked question. |
| validator | the CSV row named. |

Do not delete or weaken a check to make the pipeline pass. A checker that fires on a legitimate case gets a narrow, documented exception.
