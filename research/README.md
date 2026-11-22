# Clean Air research dossier

**Shared air, unequal costs: where philanthropy can improve health and livelihood security in India**

Research cutoff: **22 November 2026** · Phase 1 (research) and Phase 2 (source verification) complete

These files are the single source of truth for the Clean Air site. Pages are generated from them. If you change a rating here, the site changes with it.

## Contents

| Path | What it is |
|---|---|
| `decision-brief.md` | Decision brief, about 3–4 pages |
| `report/00-method.md` … `report/11-synthesis.md` | Full report as 12 section files (about 10,000 words of prose). YAML front matter gives `id`, `title`, `nav` (site section), `order` and `summary` |
| `data/sources.csv` | Source register: every source with URL, publication date, access date, type and access status |
| `data/claims.csv` | Claim-level evidence register. Each `Cnnn` links to one or more sources, with location, geography, period and read status |
| `data/settings.csv` | (C) Geographic comparison of six settings |
| `data/community-impacts.csv` | (D) Community impact matrix, 15 groups |
| `data/organisations.csv` | (E) Organisation and programme map, verified activities only |
| `data/interventions.csv` | (F) Intervention and infrastructure matrix with fund now / test first / not recommended |
| `data/evidence-map.csv` | Two-dimension evidence ratings with written judgements |
| `data/evidence-gaps.csv` | (G) Evidence-gap register with proportionate next studies |
| `data/portfolios.csv` | (H) Four portfolio concepts, structured fields |
| `data/economic-estimates.csv` | Every economic number, with population, place, period, exposure, outcome, method, estimate, uncertainty, limitations and type |
| `data/pathways.csv` | Consequence pathways rated link by link |
| `analysis/reg.py` | Helper used to append sources and claims during research |
| `analysis/validate.py` | Integrity check: every reference resolves and ratings use permitted labels |
| `exports/` | Assembled report and PDFs, with the cutoff date in each filename |
| `PHASE1-PLAN.md` | The plan this phase followed |

## Conventions

- **Citations.** `[C042]` in prose resolves to `data/claims.csv`, which resolves to `data/sources.csv`.
- **Ratings.** Only four labels are used: Strong · Moderate · Limited/mixed · No adequate evidence found. Each rating has a written reason. Problem confidence and intervention confidence are rated separately.
- **Funding classes.**
  - A: ready to support
  - B: promising, needs adaptation
  - C: needs proof of concept
  - D: not recommended on present evidence
- **Access status.** `full-text-read`, `abstract-only`, `search-snippet-only` or `unreachable`. Claims resting only on snippets or unreachable sources are marked `provisional` and cannot carry a Strong rating.
- **Separation rules.**
  - Emission inventories, ambient apportionment, personal exposure, health burden and economic burden are kept apart.
  - Losses caused by pollution-control policy are kept apart from losses caused by illness.
  - No source share or finding is transferred between places.

## Checking integrity

```bash
python3 research/analysis/validate.py
```

The script exits non-zero if any claim, source or intervention reference fails to resolve. Warnings list where provisional claims are cited.

## Status at the end of Phase 1

- 110 claims from 68 sources; 109 verified in Phase 2 (see `VERIFICATION.md`).
- 2 claims remain provisional (C034, C056).
- Several official sites could not be reached from the research environment: `cpcb.nic.in` (TLS), CEEW PDFs and Lancet pages (blocked), and some NCDC files (missing).
- Hindi-language sources were searched only lightly.
