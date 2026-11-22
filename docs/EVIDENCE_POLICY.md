# Evidence policy

This policy applies to everything in `/research` and everything generated from it. `CLAUDE.md` holds the binding summary.

## Cutoff

This is the **22 November 2026 evidence edition**. Nothing published later is included. A new edition needs a new cutoff recorded in `CLAUDE.md`, and the previous snapshot is preserved.

## Every fact has a trail

1. Each factual statement carries a claim ID (`Cnnn`).
2. Each claim lists its sources (`Snnn`), where in the source the fact appears, the place and period it covers, and its status (`read` or `provisional`).
3. Each source records its URL, publication date, access date, type and how much of it was read: `full-text-read`, `abstract-only`, `search-snippet-only` or `unreachable`.
4. Claim and source IDs are permanent. New records append, and old IDs are never renumbered or reused.

## Ratings

**Evidence labels.** Only four labels are used: **Strong**, **Moderate**, **Limited/mixed** and **No adequate evidence found**. Each comes with a written reason.

**Two separate ratings.** We rate (a) confidence that a problem exists and (b) confidence that a response works, separately.

**Four situations kept apart:**

- absence of evidence;
- evidence of no effect;
- evidence of harm;
- benefit only under specific conditions.

**Cause-and-effect arrows.** Arrows in story paths are labelled *well established*, *supported but context dependent*, *plausible / needs testing* or *not yet established in this setting*. These map to the four evidence labels.

**Funding readiness (A–D)** is a separate scale:

- A: ready to support;
- B: promising, needs adaptation;
- C: needs proof of concept;
- D: not recommended on present evidence.

It never rates scientific quality.

## Measurement concepts kept apart

- **What is measured:**
  - AQI and concentration;
  - ambient concentration, personal exposure and dose;
  - emission inventories, ambient source apportionment and episode modelling.
- **What a result shows:**
  - association and causal estimates;
  - measured, self-reported, modelled and administrative figures.
- **Time and money:**
  - short episodes and long-term exposure;
  - losses from illness and losses from pollution-control rules.

## Funding records

**Required fields.** Every record in `programmes.csv` carries:

- funding category;
- instrument;
- amount type (approved, disbursed, project total, listed sources, or not public);
- currency;
- nominal year;
- three separate stages (approval, operation, evidence);
- air-quality intent (primary or co-benefit);
- how the relationship was verified.

**Amounts.** An amount appears only when a primary record states it. The validator rejects amounts that rest on search snippets.

**Totals.** Totals from different reports are never combined, because they use different periods and bases.

**Intermediaries.** A funder of a regranting intermediary is not recorded as funding downstream projects.

## Source quality and directness

Source type (government, peer-reviewed, multilateral, funder record, implementer account, news) is recorded separately from how certain a fact is. Organisational reports are used for what organisations say they did. They are not used for outcomes, unless an independent evaluation exists.

## Never invent

The following are never invented:

- programmes and funding relationships;
- amounts and costs;
- outcomes and success claims;
- quotations, community voices and contact details;
- open calls.

Gaps are shown as gaps.
