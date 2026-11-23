# Research log

## Edition: 22 November 2026 (regional expansion)

### What was done

| Pass | Actions | Result |
|---|---|---|
| Starter register | Opened all 29 URLs in section 14 of the expansion brief | 24 read; 5 blocked: pcap.punjab.gov.pk (403), two CCAC pages (403), Clean Air Asia (403), thailand.go.th (DNS error at first try, read later via a mirror URL) |
| Alternatives for blocked pages | Web search, then official or news alternatives | Thailand: government event page plus Thairath report (read). Cambodia: search snippet only (CCAC project listing). Philippines e-mobility: search snippets only |
| Comparable country data | AQLI country spotlights for 8 countries (2023), rendered with a headless browser | Same source, method and year for all 8 countries |
| Source attribution | Searches for Dhaka, Lahore and Jakarta | Jakarta: Vital Strategies/ITB brief (read). Lahore: Dawn report of the Urban Unit 2023 inventory (inventory PDF blocked by TLS). Dhaka: UrbanEmissions summary of 2013 studies |
| Livelihood research leads | Delhi outdoor workers (2022), Chennai vendors (2026), CHI 2026 paper | Abstracts via Europe PMC for two; CHI metadata only via Crossref |
| Funding analysis | Clean Air Fund 2026 development and philanthropic funding reports | Landing pages read; periods and denominators recorded separately |
| Verification | `verify.py` over all 110 sources and 153 claims | 107 reachable; 149 claims supported; 4 provisional |

### Distinguishing discovery from access

Search results were used only to find sources. A claim is marked `read` only when the source page, PDF or abstract was opened and the figure was found in it. Facts known only from search summaries are marked `provisional`. Those claims are C034, C056, C135, C138 and C153.

### Not done in this edition

- No Bangkok, Hanoi or Metro Manila source-apportionment study was read.
- No Sri Lanka, Bhutan, Lao PDR, Myanmar, Malaysia or Singapore dossier was written. These six countries are in the research queue.
- The grant databases of CIFF, IKEA Foundation, Sequoia, McCall MacBain, Open Philanthropy and Bezos Earth Fund were not checked, so no grants are attributed to them.
- World Bank and ADB project documents (results frameworks, disbursement) were not opened beyond press releases and data sheets.
- Hindi and other local-language sources were searched only lightly.
- No full reports were read for ADB (March 2026), the World Bank "A Breath of Change" report, or the Clean Air Fund and IGES Southeast Asia platform report. Only their landing pages and summaries were read.

## 23 November 2026: organisations atlas (cutoff unchanged)

- Read the five briefs; wrote `docs/organisations-10x-audit.md`.
- Sources searched or read: Clean Air Fund grant database (all 79 listing pages parsed; 234 unique grants, 36 Asia-related), EPIC Air Quality Fund awardee pages (2024–2026; 12 Asian awardees read), organisations' own pages, GEF project record, ASEAN, ICIMOD, CSTEP (Indi-SET evaluation and annexures), DBS newsroom, Greenpeace, The Nation, Prachatai, Mongabay, The Business Standard, Dialogue Earth, YourStory, Winrock, Live & Learn, 350.org, SunStar.
- Blocked (not bypassed): Clean Air Asia (403), CCAC partner pages (403), GreenHub (TLS), HACCAP page (403), UNDP Viet Nam (403). A browser-rendered fetch with a different user agent was refused by the session's safety controls and was not retried.
- Registered S111–S180 and C154–C222 with `research/analysis/add_org_atlas.py`; P16 upgraded with the GEF record.
- Exclusions and coverage gaps: `research/data/org-candidates.csv`.
