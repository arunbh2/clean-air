# Clean Air site

A static site generated entirely from `/research` (279 pages: the 22 November 2026 regional edition plus the organisations atlas). The templates hold layout and interface labels. Every finding, rating, figure and piece of copy comes from the research files:

- `research/report/*.md`: report sections; each site section renders the report sections listed for it.
- `research/data/*.csv`: settings, communities, interventions, organisations, portfolios, evidence map, gaps, pathways, economic estimates, claims and sources.
- `research/site-content/home.md` and `sections.json`: homepage copy (with claim citations), plus section labels and introductions.
- `research/decision-brief.md` and `research/VERIFICATION.md`.

Change a rating in `research/data/interventions.csv`, rebuild, and every page that shows it changes.

## Build and preview

```bash
pip install -r site/requirements.txt
```

```bash
python3 site/build.py
```

```bash
npx http-server site/dist -p 8080
```

Output goes to `site/dist/`, which is not committed. The pages use relative links, so they also work opened directly from disk.

## Structure

| Path | Built from |
|---|---|
| `index.html` | `site-content/home.md`, priority groups in `community-impacts.csv` |
| `crisis/` | report sections 01–02 |
| `people/` and `people/<group>.html` | report 03, 04, 06; `community-impacts.csv` |
| `places/` and `places/<setting>.html` | report 05; `settings.csv` |
| `what-works/` and `what-works/<intervention>.html` | report 08; `interventions.csv`; `evidence-map.csv` |
| `organisations/` | report 07; `organisations.csv` |
| `evidence/` | report 00, 10; claims, sources, evidence map, gaps, pathways, economic estimates, verification |
| `support/` | report 09, 11; `portfolios.csv`; decision brief; downloads |
| `start/`, `crisis/glossary.html` | `site-content/start.md`; `glossary.csv` |
| `places/<country>.html`, `south-asia`, `southeast-asia`, `compare` | `countries.csv` |
| `organisations/funding/`, `organisations/funders/` | `programmes.csv`, `funders.csv`, `funding-flows.csv` |
| `organisations/index.html`, `o/<slug>.html`, `projects/`, `places/`, `gaps/`, `methods/`, `compare.html`, `stories/` | `organisations.csv`, `projects.csv`, `organisation-project-roles.csv`, `funding-flows.csv`, `org-candidates.csv`, `site-content/org-*.md`, `site-content/org-stories/` |
| `downloads/data/organisations-atlas.json` | Public export of the atlas tables |
| `what-works/compare.html`, `not-a-solution.html` | `interventions.csv` |
| `support/pathways/`, journeys | `decision-pathways.csv`; `site-content/stories/` |
| `evidence/coverage.html` | computed from all registers at build time |
| `about/` | `site-content/pages/` |

## Design

The design follows `docs/design-brief.md`:

- tokens in `static/css/site.css`;
- Georgia and system sans-serif only, with no web fonts loaded;
- logos generated from one master geometry by `src/logo/build_logos.py`;
- AQI categories shown as text only, so no unverified colour scale is implied;
- no green used for ratings.

## Deployment readiness

- Static files only, with no server code, no analytics and no cookies.
- No domain is assumed. Any static host can serve `site/dist/` after `python3 site/build.py`.
- The research cutoff (22 November 2026) appears in the header, footer, homepage and downloads.
- GitHub Pages: `.github/workflows/pages.yml` builds on every pull request and deploys on every push to `main`. In repository Settings → Pages, the source must be "GitHub Actions".
- Before deploying, run the Phase 4 QA checks in `site/qa/`.
