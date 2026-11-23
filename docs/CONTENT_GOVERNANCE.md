# Content governance

## Where content lives

| Content | File | Generated page |
|---|---|---|
| Report sections | `research/report/*.md` | section pages ("Explore the evidence") |
| Simple answers and section intros | `research/site-content/sections.json` | top of each section |
| Homepage copy and modules | `research/site-content/home.md`, `home-modules.md` | `index.html` |
| Start here, journeys, footer pages | `research/site-content/start.md`, `stories/`, `pages/` | `start/`, journeys, `about/` |
| Facts | `research/data/claims.csv` and `sources.csv` | citations everywhere |
| Structured records | `research/data/*.csv` | places, people, interventions, funding, pathways, evidence |

Templates in `site/templates/` hold layout and interface labels only. They must not hold findings. Templates may cite claims (for example on the region pages), and those citations are checked by the validator.

## Making a change

1. Edit the research file, citing claim IDs. If you add a fact, add a claim and a source first, using `research/analysis/reg.py`.
2. Run `python3 research/analysis/validate.py`. It must report no errors.
3. Run `python3 research/analysis/verify.py` for new sources, and fill in the manual verdict columns in `verification.csv`.
4. Run `python3 site/build.py`, then `node site/qa/qa.js` and `python3 site/qa/rating_change_test.py`.
5. Open a pull request. The workflow builds the site, and merging to `main` deploys it.

## Writing standards

- **Plain language.** Aim for a 13–15-year-old reading level in the simple layer. Explain acronyms at first use, or let the glossary link do it.
- **Simple answers.** 40–90 words, with one example and one honest limit.
- **Independence.** No fundraising tone, no ranking of organisations, no endorsement.
- **People.** Vignettes are labelled illustrative, built from study findings, and never presented as real individuals.

## Corrections

Corrections come in through the "Correction" issue template. The fix goes into the claim register with a note, and the verification record lists significant corrections.

## Review dates

Each country dossier has a `last_reviewed` date. The coverage dashboard lists dossiers by review date, along with provisional claims and unreachable sources.
