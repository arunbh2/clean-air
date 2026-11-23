# Data model

One canonical record in `research/`. Everything public is generated from it by `site/build.py` (pages) and `site/build_agent.py` (packs, mirrors, agent files, catalogue, feed). Nothing public is hand-copied.

## Canonical files

| File | Key | Holds |
|---|---|---|
| `data/claims.csv` | `claim_id` (Cnnn, append-only) | claim text, sources, locator, evidence type, place, period, status (`read`, `provisional`, `withdrawn`) |
| `data/sources.csv` | `source_id` (Snnn, append-only) | title, publisher, dates, URL, type, access status |
| `data/claim-passages.csv` | `claim_id` | passage-level verification state, excerpt, scores, date |
| `data/passage-reviews.csv` | `claim_id` | reviewer decisions (located, partial, not_located) for claims the automated check missed, with notes |
| `data/verification.csv`, `data/source-checks.csv` | claim / source | earlier figure-level verification and reachability (kept) |
| `data/corrections.csv` | `correction_id` (CRnnn) | what changed, earlier wording, reason, date |
| `data/changelog.csv` | `change_id` | dated public changes (feed) |
| `data/organisations.csv`, `projects.csv`, `organisation-project-roles.csv`, `funding-flows.csv`, `programmes.csv`, `funders.csv` | org / J / role / FL / P / funder | the organisations and funding atlas |
| `data/interventions.csv`, `evidence-map.csv`, `evidence-gaps.csv`, `community-impacts.csv`, `countries.csv`, ... | various | evidence, communities, places |
| `site-content/*.md`, `site-content/questions/*.md`, `report/*.md` | file | narrative copy, worked questions, report |
| `data-dictionary.csv` | dataset, column | descriptions used in the catalogue and JSON Schemas |

## Derived fields (computed at build, never stored twice)

| Field | Rule |
|---|---|
| Verification state | from `claim-passages.csv`; `withdrawn` if the claim's status is withdrawn |
| Provenance class | `evidence_type` mapped to: primary data or research study · evaluation study · regulator or official programme · organisation or funder report (self-reported) · media account · modelled estimate · community research · testimony or court record · site inference |
| Funding stage | source wording mapped without inference: announced · approved · committed (awarded) · disbursed · legal obligation · stage not specified in source. "Expended" and "independently evaluated" are never inferred; results stay in their own field. |
| Evidence basis of an organisation | `source_class` mapped to independent test · official record · funder's record · organisation's own account · company's own account · news reporting |

## Verification states

| State | Meaning | Counts in this build |
|---|---|---|
| `passage_found` | either an automated window of up to three sentences in an accessible copy holds every figure in the claim and at least 35% of its content words (50% when the claim has no figures), or a reviewer located the passage (recorded in `data/passage-reviews.csv`) | 201 (142 automated, 40 reviewer-located, 19 main passage located with remaining figures found elsewhere in the same source) |
| `needs_manual_review` | the passage check did not confirm it, but an earlier human review recorded "supported"; a person has to locate the passage | 18 (each with a reviewer note saying what is missing) |
| `source_accessible_passage_not_found` | text read, no supporting passage, no earlier human support | 0 |
| `not_accessible` | no text could be obtained automatically (not the same as a dead link) | 3 |

Gate: any claim after C222 that is marked `read` must be `passage_found`, or the validator fails. Claims C001 to C222 are reported as they stand, so the 18 awaiting review are visible on the claim register, in packs and in `claims.json`. **Limitation:** the matcher works on extracted text; passages from tables can read as a jumble (for example C001), and a match on figures plus wording is strong evidence of support, not proof of correct interpretation.

## Integrity rules (`research/analysis/validate.py`)

Unknown IDs, bad ratings, unsourced roles or flows, amounts resting on snippets, sources after the cutoff (existing). Added: every claim has a passage check with a known state; a `passage_found` row has an excerpt; new claims need a located passage; statuses limited to read / provisional / withdrawn; every correction has a known type, date, record and reason; a withdrawal in `corrections.csv` matches the claim's status, and every withdrawn claim has a correction; worked questions reference only existing records and tokens.
