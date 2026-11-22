# Phase 2: source verification

Verification run: 22 November 2026 · Research cutoff: 22 November 2026

## What was done

1. **Every source was re-fetched.** `analysis/verify.py` requested each URL in `data/sources.csv`. Where a publisher blocked automated access (PubMed, some journal pages), the script retrieved the abstract from Europe PMC. Results are in `data/source-checks.csv`: HTTP status, final URL, characters of text retrieved and how each source was checked.
2. **Every claim's figures were checked.** For each claim in `data/claims.csv`, the script extracted every figure of two or more digits, excluding years, and searched for it in the re-fetched text of that claim's sources. Results are in `data/verification.csv`.
3. **Every flag was reviewed by hand.** This covered every claim where figures were missing, the source was unreachable, the claim was derived, or the claim had no figures to match. Qualitative claims were checked by keyword overlap with their sources and then read. Manual verdicts, actions and notes are recorded per claim.

## Results

| | Count |
|---|---|
| Sources re-fetched | 68 |
| Sources reachable | 67 |
| Sources unreachable | 1 (S028, CPCB children's lung-function study: `cpcb.nic.in` TLS failure) |
| Claims checked | 110 |
| Claims supported after review | 109 |
| Claims unverified (source unreachable, kept provisional) | 1 (C056) |
| Claims provisional for other reasons | 1 (C034: CSE report known only through press coverage) |

## Corrections made

| Claim | Problem found | Action |
|---|---|---|
| C100 | Phase 1 wording (gig workers lose incentives and face penalties for logging off) was **not supported** by the cited source | Rewritten from a Deccan Herald report (21 Dec 2025) of the gig workers' association's demands and a parliamentary committee's recommendations. Report text in sections 03 and 04 and the community matrix corrected |
| C087 | The 2017 start date for health surveillance came only from search snippets | Rewritten from the Health Ministry advisory letter of 18 Nov 2024, now readable. Date removed. Sections 02 and 07 corrected |
| C108 | Coverage figures were rounded, and a waste-picker figure had no retrievable source | Exact figures (85,819 profiled; 76,736 PPE kits) used. Waste-picker figure dropped |
| C079 | The 2021 "80% reduction" claim had no source attached | Sourced to Deccan Herald, 1 Oct 2021 |
| C003 | WHO's Q&A page, as fetched, did not include the interim-target table | AirClim's reproduction of the WHO table added as a second source |
| C049 | Confidence interval rounded | Corrected to 1.08–6.76 g, matching the abstract |
| C103, C109 | Effective date of the labour codes rested on secondary sources | Confirmed by PIB release (four codes effective 21 Nov 2025) |

## Upgrades

Five claims marked provisional in Phase 1 rested on sources that were readable in Phase 2. After reading, they were confirmed and upgraded:

- C057: conference-abstract status of the Odisha IQ result confirmed;
- C064: abstract confirms black carbon above 200 µg/m³ near the plants;
- C087: rewritten from the advisory letter;
- C098: the UW page states shelter evidence is inconclusive;
- C108: rewritten from the Organiser report.

## Limits of this verification

- **Figures, not meaning.** Finding a figure in a source shows the number is there. It does not prove the claim reads it correctly. Every numeric claim was written while reading the source in Phase 1. Phase 2 confirms the figures and that the sources are still online.
- **Abstract-only sources** (several health studies and the HAPIN trial) were checked against their abstracts. Their methods were not re-examined.
- **Qualitative claims** were checked by keyword overlap and a read of the claim wording against the source. That is a weaker test than figure matching.
- **Pages change.** News sites and official portals can change or move. Each check records the date it was made.

## Re-running

```bash
python3 research/analysis/verify.py
```

The script keeps the manual verdict, action and note columns from earlier runs. New or changed claims need a fresh manual review.

## Expansion verification (regional edition, same cutoff)

Run on 22 November 2026 after the regional expansion added `S069`–`S110` and `C111`–`C153`.

| | Count |
|---|---|
| Sources re-fetched (all) | 110 |
| Sources reachable | 107 |
| Unreachable | S028 (cpcb.nic.in), S082 (CCAC Cambodia page, 403), S110 (ACM DOI, no abstract) |
| Claims reviewed (all) | 153 |
| Supported after review | 149 |
| Unverified, kept provisional | 4: C056, C135 (Cambodia project), C138 (Philippines e-mobility), C153 (CHI paper) |

**Method notes for the expansion.**

- **AQLI pages (C111–C118).** These pages are rendered by JavaScript, so the plain fetch returned an empty page. Figures were confirmed in text captured with a headless browser on the same day.
- **Numbers written in words.** Two abstracts write their sample sizes in words, which the figure check cannot match. Those were confirmed by reading the abstracts.
- **Correction.** C152 was corrected from 59% to 58.7%, the figure stated in the abstract.
- **Funding records** (`programmes.csv`) cite the same sources as their claims. Amounts appear only where a primary record states them. The validator rejects an amount that rests on a search snippet.
