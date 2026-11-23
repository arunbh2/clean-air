---
title: How the latest signals feed works
summary: What the feed collects, how records are chosen, what the dates mean, and how a record can move from discovery towards the evidence register.
---

## What this feed is

Latest signals is a discovery layer. Twice a day a scheduled job reads a short list of tested feeds and public research indexes, keeps the records that are about air pollution in India, South Asia or Southeast Asia, removes duplicates and publishes them here with a link to the original source.

A signal is an indexed third-party publication or announcement. It is not a verified Clean Air finding. A news report, a press release, a new paper or a funding announcement in this feed has not been assessed by Clean Air, carries no evidence rating, and does not change the research edition, the claim register, any evidence rating or any funding total. The research edition stays dated 22 November 2026; this feed has its own, later dates.

## How records are chosen

Inclusion follows written rules (published in the [source registry](sources.html) and the [classification rules](../downloads/data/signals-taxonomy.yml)), not a score:

- **An air-pollution term.** For research indexes the term has to be in the title; for news and institutional feeds it can be in the title, or appear at least twice in the publisher's own summary.
- **A place in scope.** A country, city or state from the list, or a named region such as South Asia, the Indo-Gangetic Plain or ASEAN. Feeds that only cover the region are exempt from this test.
- **Exclusions.** Water, plastic, noise and soil pollution without an air term; tobacco; airlines and air forces; stock-market items. Titles that read like instructions to an automated system are held back for a person to look at.
- **A safe link.** Only HTTPS links are kept. Tracking parameters are removed.

Country tags need the country, a city or a state in the title or the publisher's summary. A record that names more than four countries is tagged as regional rather than country by country. An ambiguous name such as Punjab gives no country tag on its own. Topic tags come from words in the same text and say what the record mentions, not what it shows.

The run report for each refresh lists every exclusion with its reason, so the rules can be checked and corrected.

## Duplicates, versions and coverage

Records are matched first by DOI, then by cleaned address, then by an identical title from the same publisher. A preprint and its journal article stay as two records linked as versions. The same story from two publishers stays as two records linked as coverage. A correction or retraction notice is linked to the paper it concerns, and the paper is marked.

## What the dates mean

- **Published:** the date the publisher gives. Records are ordered by it. Day, month or year precision is shown as given.
- **Updated:** a later date the publisher gives for a change. It never replaces the publication date.
- **Discovered:** when this feed first saw the record.
- **Last checked:** when the record was last seen in a source.
- **Last successful refresh:** the end of the most recent run in which at least one source was read and the output passed validation. If a run fails, this time stays as it was, and after 36 hours the page says the refresh is delayed.

A record without a date is shown as "Date unknown" outside the timeline. A date read from an article's address is labelled as such. A date in the future is flagged and kept out of the timeline.

## From discovery to evidence

Every record starts as **source record, not assessed**. A curator can move it forward in `research/signals/review-decisions.csv`, and each step is checked when the site is built:

1. **Details checked:** title, date and publisher confirmed against the source.
2. **Reviewed by Clean Air:** a reviewer has read the source. Only now can a "Why it may matter" note appear, labelled as Clean Air's interpretation and linked to the material it rests on, or a summary of what a study actually tested.
3. **Proposed for the evidence register:** a new claim or an amendment is drafted through the normal research process, with a located passage.
4. **Linked to the evidence register:** allowed only when a claim in a dated research edition cites this source. The feed cannot create a claim or change a rating.

**Who reviews.** Reviews are carried out by the editor, or by an AI reviewer working on the editor's behalf. Both follow the same rules: the source is read before any note is written, each note records what it rests on, and no review can create a claim or change a rating.

Funding announcements stay apart from verified funding records. An amount appears only after its stage (requested, announced, pledged, approved, contracted, disbursed or evaluated), currency and source have been checked, and it is never added to a funding total on this site.

## Rights and privacy

Only titles, dates, publishers, links and tags are stored. No article text, abstract, image or PDF is copied, and paywalled text is never fetched. Each record belongs to its publisher, and following a link takes you to the publisher's site. Visiting these pages loads nothing from third parties: the feed is built in advance and served as static files.

## Corrections and reports

To report a wrong date, a broken or misfiled record, a missed exclusion or a takedown request, use the route on the [corrections page](../about/corrections.html). A record removed for rights or privacy reasons is withdrawn from the feed; other records stay as a historical index even if the publisher's feed drops them, and their correction or retraction status is shown when the publisher marks it.
