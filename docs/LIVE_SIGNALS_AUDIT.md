# Latest Signals: audit and decisions

**Brief:** `docs/live-signals-master-brief.md` · **Audited:** 23 November 2026 · **Research edition:** 22 November 2026 (unchanged)

## 1. What existed before

| Item | State found | Decision |
|---|---|---|
| `feed.xml` | Atom feed of site editions and corrections (`changelog.csv`, `corrections.csv`) | Kept with the same meaning and title. Signals get their own feed at `signals/feed.xml`; `tools/check_signals.py` fails if a signal entry reaches `feed.xml`. |
| Build | Static Jinja2 generator (`site/build.py` and its `exec`'d parts), GitHub Pages deploy in `.github/workflows/pages.yml`, gated by `tools/check_all.py --browser` | Reused. Signals add `site/signals_data.py` (records and indexes) and `site/build_signals.py` (pages, feeds, exports). No server, no CMS. |
| Agent layer | Markdown mirror of every page, `llms.txt`, `llms-full.txt`, catalogue, sitemaps | Signals pages are mirrored automatically; `llms.txt`, the catalogue and `sitemap.json` list the signals JSON and feed with the statement that signals are not verified findings. |
| Routes | No `/signals/` path | `/signals/` created; no collision. |
| Dependencies | jinja2, markdown, PyYAML, beautifulsoup4 | Added `jsonschema` (schema validation). Fetching uses the Python standard library only. |
| Governance | Evidence labels, passage verification, corrections, voice and design checks | All apply. Signal pages pass the voice, design, link and agent-file checks unchanged; source titles sit in `<cite>`, which the voice check treats as the publisher's words. |

## 2. Connector tests (23 November 2026, from the build environment)

Enabled after a successful test (HTTP 200 and a parseable response): Europe PMC REST search, Crossref works API, WHO news RSS, Health Effects Institute RSS, State of Global Air RSS, ADB RSS, ICIMOD RSS, Clean Air Fund RSS (valid, empty on the test date), UrbanEmissions RSS, Mongabay India, Mongabay (global), Dialogue Earth, Eco-Business, The Hindu energy and environment, The Daily Star environment, The Kathmandu Post (malformed XML with bare ampersands, repaired before parsing; no item dates, so dates are read from article addresses and labelled), Dawn, The Straits Times Asia, VnExpress International, Bangkok Post. Europe PMC returned HTTP 503 for about 20 minutes during testing, which exercised the outage path, then recovered.

Tested and not enabled: OpenAlex (works without a key but returns metered-credit headers; owner decision), World Bank Documents and Projects APIs (respond, but return no records after March 2025 and October 2024), ReliefWeb (needs an approved appname), GDELT (rate limited; an aggregator), PIB (Access Denied), CPCB (no response, no feed), CCAC and The Third Pole legacy domain (bot checks), CREA (intermittent JavaScript bot check), CEEW (403), UNEP and Clean Air Asia (no feed at tested addresses), Down To Earth (no feed), arXiv (rate limited). Details and exact endpoints: `research/signals/sources.yml`.

## 3. Conflicts with existing rules, and how each is handled

| Existing rule | Tension | Resolution |
|---|---|---|
| Research cutoff 22 November 2026 (`CLAUDE.md` rule 1) | Signals have later dates | Narrow exception added to `CLAUDE.md` (rule 10): the rolling discovery feed may hold later records, which do not change the cutoff, claims, ratings, verdicts, funder assessments or site assertions. A dated review is the only route into the evidence edition. |
| "Every factual claim traces to a source-register entry" | A signal is a third-party record, not a Clean Air claim | Signal pages state what a source published (title, date, publisher, link). They make no factual claim of their own. A "Why it may matter" note needs an editorial review and source references. |
| "No named individuals in new editorial prose" | Bibliographic metadata usually lists authors | Authors are not stored. |
| Evidence labels everywhere carry text | Signals have no evidence rating | The schema and checks forbid evidence-strength labels and badges on signals. |
| Build date from the last commit to `research/` or `site/` | Each refresh commits to `research/signals/` | The site's build date moves with each refresh. The evidence edition date is separate and unchanged. |
| `docs/agent-access.md`: "There is no API" | A JSON export is published | Described as a static file regenerated on each refresh, never as a query service. |

## 4. Owner decisions needed

1. **Automatic commits to `main`.** The refresh workflow commits `research/signals/` to `main` with the built-in token (`contents: write`). If `main` gets branch protection that blocks this, the push fails and the run report says so; the alternatives are a pull request per refresh or a bot account allowed to push.
2. **OpenAlex.** Enable only with an API key stored as the `OPENALEX_API_KEY` repository secret and a budget decision.
3. **ReliefWeb appname**, and **permission or manual records** for CREA, CEEW, CPCB, CAQM and PIB.
4. **Curators.** Decided 23 November 2026: the owner and Claude both review signals. At the owner's request, records carry no per-record reviewer attribution ("Reviewed by Clean Air"); the reviewer is kept in `review-decisions.csv`, and the how-it-works page states that reviews are by the editor or by an AI reviewer acting for the editor. The brief's "human-reviewed" wording for editorial notes is therefore met only in part; this departure is documented here.
5. **Local-language sources** and any **paid news API**.
6. **A new dated evidence edition** if reviewed signals are to become claims.
