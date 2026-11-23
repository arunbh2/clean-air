# Editorial voice

Clean Air speaks to street vendors, district health officers, union organisers, parents, reporters, researchers and foundation trustees. They disagree about regulation, jobs, industry and spending. The site gives them common facts, real options and an honest account of uncertainty, without telling anyone what to do or who to blame.

These rules apply to **site-authored, reader-facing copy**: headings, ledes, report text, cards, tables, labels, tooltips, empty states, packs and the generated Markdown, JSON and text files. They do **not** apply to external source titles, quotations, legal text or the earlier wording kept in the corrections register.

Enforced by `tools/check_voice.py` (part of `python3 tools/check_all.py`).

## The rules

| # | Rule | Check |
|---|---|---|
| 1 | No "should" or "must" in the site's own voice. Report requirements as facts ("the regulation requires", "the court directed"). Never erase a legal duty. | `prescriptive` |
| 2 | No insinuation of blame. Prefer "had not issued", "data not located", "outcome not independently assessed", "the source does not establish". Accurate descriptions of court findings, harms and pollution stay accurate. | `blame` |
| 3 | No em dashes. Use a full stop, comma, colon or brackets. Empty table cells say what they mean: "Not applicable", "Not recorded", "None recorded". | `em-dash` |
| 4 | No league tables or rankings of countries, cities, governments, organisations, funders, companies or technologies. Evidence labels describe the evidence, not the merit of an actor. | `ranking` |
| 5 | No named individuals or journalists in new editorial prose. Organisations, public bodies, programmes and source titles are fine. | review |
| 6 | Short, precise, calm. One point per paragraph. Expand PM2.5, AQI and similar terms on first use (glossary links do this automatically). No "game-changing", "groundbreaking", "holistic". | `hype`, `abbreviation` (warning) |
| 7 | Visible next steps. Record pages open with a plain first answer and link onward: evidence, responses, organisations, funding, open questions. | `tools/check_links.py` (`reader`) |
| 8 | Advocacy is not an outcome. "Trained 75 people, according to the funder" is not "reduced exposure". "Approved" is not "disbursed", and "a programme exists" is not "the programme works". | packs and profiles keep these as separate fields |
| 9 | Every evidence badge carries its text label, never colour alone. | `unlabelled-rating` |

## Real before and after examples from this site

| Before (baseline) | After | Rule |
|---|---|---|
| "24-hour values must be met 98% of the time" (C002) | "the standard requires 24-hour values to be met 98% of the time" | 1, legal duty kept |
| "affected workers must be compensated" (C039) | "affected workers are to be compensated" | 1 |
| "most urban local bodies failed to issue cards" (C107) | "most urban local bodies had not issued cards, because of budget constraints or reluctance, according to the waste pickers' federation" | 2, attribution kept |
| "so effective management must coordinate across sectors" (C125) | "and concludes that effective management requires coordination across sectors" | 1, conclusion attributed to the source |
| "Effect sizes should not be cited." | "The effect sizes are not reliable enough to cite." | 1 |
| "It should not fund the transfers themselves." | "It does not fund the transfers themselves." | 1 |
| "What should not be funded on current evidence?" | "What does current evidence not support funding?" | 1 |
| "Readers should keep the three roles apart." | "The three roles are distinct, and this page keeps them apart." | 1 |
| "Own site failed TLS" | "Own site could not be reached (TLS error)" | 2 |
| "Limited/mixed — Fitted respirators work in principle" | "Limited/mixed. Fitted respirators work in principle" | 3 |
| Evidence-map cell "—" | "Not applicable" | 3 |
| "Three things a resident should know" | "Three things for residents to know" | 1 |

Each rewording of a claim is logged in the corrections register (CR008 to CR011) with the earlier text.

## Approved recurring phrases

- "No public funding record was found for this organisation. That does not mean it is unfunded."
- "Amount not publicly disclosed."
- "An approval is not a disbursement, and spending is not a result."
- "No independent evaluation was found in the sources read."
- "Being active in a place does not mean reaching the people most exposed there."
- "Inclusion does not imply endorsement; nothing here is a ranking."
- "Source could not be checked automatically" (never "dead link" unless the publisher removed it).
- "Supporting passage located" (never "verified" for a page that merely opened).

## Evidence caveat patterns

- **Absence of evidence:** "No adequate evidence found" means unstudied or inconclusive, not shown to fail.
- **Evidence of no effect:** say what was tested, where, and what was found ("Effects confined to about 200 m").
- **Self-report:** "according to the organisation", "the funder reports".
- **Transfer:** "benefit under conditions that may not transfer locally".

## Terms to explain on first use

PM2.5, PM10, AQI, GRAP, NCAP, CPCB, CSR, airshed, source apportionment, ambient, exposure-response, modelled estimate, grant, loan, independent evaluation. The glossary (`research/data/glossary.csv`) links the first use on each page automatically.

## Documented exceptions

Exceptions live in `tools/voice-exceptions.csv`, each scoped to a page pattern, a rule and an exact phrase, with a reason. A stale exception (one that no longer matches anything) fails the check. Current exceptions: the corrections register and `for-ai.json`, which quote the removed word ("must", "failed to issue") to explain a rewording.

Not checked, by design: `<cite>` (source titles), `<blockquote>` and `<q>`, text in curly quotes, `[data-voice="verbatim"]` (earlier wording, source excerpts), code. The accessible name "Clean Air — home" is fixed by `CLAUDE.md` and sits outside page prose (owner decision 6 in the audit).
