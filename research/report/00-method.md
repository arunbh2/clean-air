---
id: method
title: How this study was done
nav: evidence
order: 0
summary: Desk research to a 22 November 2026 cutoff, organised around five funding decisions, with every claim traced to a source and every rating explained.
---

# How this study was done

**Research cutoff: 22 November 2026.** Evidence published after this date is out of scope. The 2026–27 winter season was under way at the cutoff, so current-season figures are partial. Seasonal and long-term figures use the most recent complete periods available in each source.

## The question

The study asks where a foundation could reduce the pollution people breathe, protect the livelihoods that depend on that air, and leave behind a service or institution that keeps working after a grant ends. It is organised around five decisions:

- **A.** Which communities and exposure settings merit priority?
- **B.** Which pathways create the greatest avoidable health and livelihood burdens?
- **C.** Which interventions are effective, usable and feasible for the institutions that would run them?
- **D.** What should be funded now, tested first or investigated further?
- **E.** What should not be funded on current evidence?

No technology or programme was assumed in advance. The study separates four kinds of response throughout: reducing emissions, reducing exposure while emissions persist, reducing health consequences, and protecting income and care during illness or restrictions.

## Sources and how they were read

This is desk research. No people or organisations were contacted. Sources were found by web search and, for primary literature, through the Europe PMC database. Each source is recorded in `data/sources.csv` with its URL, publication date, the date it was accessed, its type, and how much of it was actually read:

| Access status | Meaning | Effect on ratings |
|---|---|---|
| `full-text-read` | The document, or the relevant section, was read | Can support any rating |
| `abstract-only` | Only the abstract was available | Findings used as stated; methods not checked |
| `search-snippet-only` | Only a search summary was seen | Claims marked provisional; cannot support a Strong rating |
| `unreachable` | The site could not be reached from the research environment | Claims marked provisional |

Some official sites could not be reached from the research environment. They include `cpcb.nic.in` (TLS failure), several Lancet pages and CEEW's PDF library (blocked), and parts of the Health Ministry's NCDC site (missing files). Where an official document was unavailable, a copy hosted elsewhere was used and recorded as such, or the gap was logged.

Every factual statement in this report carries a claim ID in square brackets, such as [C016]. Each claim ID resolves in `data/claims.csv` to one or more sources, a location in the source, the geography and period it covers, and whether it was read in full or is provisional. A validation script (`analysis/validate.py`) checks that every reference resolves.

## How evidence is rated

Ratings use four labels only: **Strong**, **Moderate**, **Limited/mixed** and **No adequate evidence found**. Every rating comes with a written reason. The study rates two things separately:

1. Confidence that a problem or causal relationship exists.
2. Confidence that an intervention improves outcomes.

Four situations are kept apart:

- absence of evidence;
- evidence of no effect;
- evidence of harm;
- evidence of benefit under conditions that may not transfer.

An intervention is not called ineffective because it has not been studied locally. An unmonitored place is not treated as a low-exposure place.

Funding options are classed:

- **A**: ready to support;
- **B**: promising but needs adaptation and implementation learning;
- **C**: needs proof of concept or stronger causal evidence;
- **D**: not recommended on present evidence.

## Units and measures

The Indian Air Quality Index (AQI), pollutant concentrations, exposure duration and personal exposure are different quantities and are not used interchangeably:

- **Concentrations** are in µg/m³ with their averaging period stated.
- **Emission inventories** (what is emitted), **ambient source apportionment** (what is measured at a monitor), **personal exposure** (what a person breathes), **health burden** and **economic burden** are reported separately.
- **Source shares** from one place or season are never applied to another.

## Limitations

- Earnings evidence for informal workers is thin. The study records gaps instead of filling them with national aggregates.
- Several important documents were read only as abstracts or summaries. Examples are the full Delhi schools trial paper (not yet published at the cutoff) and the HAPIN trial papers.
- Hindi and other local-language sources were searched only lightly. This is a known gap.
- Organisational reporting is used for what organisations say they do. It is not used to establish outcomes.
- Phase 2 of this work will re-fetch every cited URL and flag anything unreachable or unsupported.

## Quality check

Before release, the report was checked against the brief's ten-point checklist:

1. Delhi is a detailed case, not a proxy for all India.
2. Health, productivity, earnings and household welfare are kept distinct.
3. Causal claims match their evidence.
4. Losses caused by policy restrictions are separated from losses caused by illness.
5. Monitoring gaps are not read as safety.
6. Infrastructure options name an operator and recurring finance.
7. Equity is judged by access and outcomes.
8. Existing organisations and obligations are recognised.
9. Recommendations trace back to findings.
10. The report states what not to fund.

The record of that check is in `11-synthesis.md`.
