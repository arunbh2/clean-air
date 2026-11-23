# Handover guide

**What this is.** Clean Air is a static evidence site generated from `/research`. To change anything a reader sees, edit `/research` and rebuild. Never edit `site/dist/`.

## Daily commands

Install the build dependencies once:

```bash
pip install -r site/requirements.txt
```

Check that every reference resolves (this must report no errors):

```bash
python3 research/analysis/validate.py
```

Build the site into `site/dist/`:

```bash
python3 site/build.py
```

Run the browser QA (needs Node and the pre-installed Playwright):

```bash
cd site/qa && npm install && node qa.js
```

Confirm that CSV ratings still drive the pages:

```bash
python3 site/qa/rating_change_test.py
```

## Adding a fact

1. Register the source and the claim with `research/analysis/reg.py`. See the examples in the file's docstring.
2. Cite the new claim ID in Markdown or CSV as `[Cnnn]`, or in a `claim_ids` column.
3. Run `python3 research/analysis/verify.py` and fill in `manual_verdict`, `action` and `note` in `verification.csv`.
4. Regenerate the source register:

```bash
python3 research/analysis/source_register.py
```

## Adding a funding record

Add a row to `research/data/programmes.csv` with every stage field. Leave `amount` empty unless a primary record states it, and set `amount_type` to say what the figure is. Add the funder to `funders.csv` if new. The validator enforces these rules.

## Adding a country

Add a row to `countries.csv`. Use the same comparable PM2.5 source as the other countries, or flag clearly that it differs. Give it at least one claim and a `last_reviewed` date. Change `coverage_status` from `research queue` once the dossier has sources.

## Deploying

Open a pull request. The workflow builds the site. Merging to `main` deploys it to https://arunbh2.github.io/clean-air/.

## Starting a new edition

Change the cutoff in `CLAUDE.md`, the build constants (`CUTOFF` and `CUTOFF_ISO` in `site/build.py`) and the update-policy page. Tag the previous edition in git. Do not mix later material into the current edition.

## Where to read more

- Rules: `CLAUDE.md`, `docs/EVIDENCE_POLICY.md`, `docs/CONTENT_GOVERNANCE.md`
- State: `docs/CURRENT_STATE_AUDIT.md`, `docs/IMPLEMENTATION_REPORT.md`, `docs/RESEARCH_LOG.md`, `docs/OPEN_QUESTIONS.md`
