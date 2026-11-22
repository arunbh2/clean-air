# Clean Air: how to choose a skill

This repo holds the Clean Air work. Most requests here are for writing, decks, documents, analysis or
visuals, not code. Many skills overlap, so use this file to choose one. If two skills could fit,
the rules below decide.

## Rules that decide between skills

1. **Think first, then produce.** For a proposal, deck or funder task, load the skill that decides
   *what to say* before the skill that makes the file.
2. **Practical Action branding beats generic.** If the output carries Practical Action's name, or
   goes to a funder, partner or PA audience, use the `-2026` PA skill. Use the generic
   `document-skills:*` / `anthropic-skills:*` file skills only for unbranded, internal or
   working files. Never mix palettes.
3. **Use the newest PA skill.** Prefer `pa-presentation-2026`, `pa-docx-2026` and
   `pa-rfp-response-2026` over the old versions without the suffix. Use an old version only
   if asked by name.
4. **A named file type means that file.** If the user asks for ".docx", ".pptx", ".xlsx" or
   ".pdf", produce that file. If they ask for "a document", "a page" or "a deck" with no file
   type, first check whether a claude.ai artifact or doc would serve them better.
5. **Write in Arunabha's voice only when it's theirs.** Apply `voice-dna` to LinkedIn posts,
   donor stories, essays, op-eds and anything else published under Arunabha's name. Don't apply
   it to internal analysis unless asked.

## Which skill for which job

### Funding and proposals
| Situation | Skill |
|---|---|
| A funder or RFP is named and the next step is unclear, or the task covers several stages | `donor-os` (it routes the rest) |
| Background on a funder, warming them up, keeping in touch, or a debrief after a decision | `funder-relations` |
| Deciding whether to bid, the win theme, how the argument is built, a red-team review | `proposal-craft` |
| Matching the language to a funder type, drafting sections in their terms | `donor-dialect` |
| Writing the actual RFP, concept note or EOI response as a .docx | `pa-rfp-response-2026` |
| A capacity statement, briefing, donor report or other long PA document | `pa-docx-2026` |

### Decks
| Situation | Skill |
|---|---|
| Story, audience, slide titles, cutting or fixing a deck (always first) | `deck-craft` |
| Choosing a chart, table or diagram for each claim | `exhibit-craft` |
| Producing a Practical Action deck | `pa-presentation-2026` |
| Rehearsing delivery, speaker notes, preparing for questions | `deck-delivery` |
| An end-to-end deck run that covers several of the above | `deck-os` |
| A deck someone asked for in BCG or PwC style | `bcg-presentation` / `pwc-presentation` |
| Unbranded slides, or reading or editing an existing .pptx | `document-skills:pptx` |

### Thinking and diagnosis
| Situation | Skill |
|---|---|
| A deep systems diagnosis of a development problem (air pollution as a valuation failure, missing voices, programme design) | `vr4pp` |
| Mapping how a system shifts, its leverage points and transitions | `system-shift` |
| A real decision with trade-offs that needs pressure-testing | `llm-council` (several perspectives) or `decision-making` |
| Arguing against the strongest version of an opposing case | `thinking-steel-manning` |
| Choosing a mental model, or finding where effort could have outsized effect | `mental-models`, `find-leverage` |
| Research across many sources | `deep-research` |

### Files and data (generic, from the pinned Anthropic plugins)
| Situation | Skill |
|---|---|
| Spreadsheets, CSV cleanup, models | `document-skills:xlsx` |
| Reading, merging, filling or OCR-ing PDFs, or creating a PDF | `document-skills:pdf` |
| An unbranded Word file, tracked changes, editing someone else's .docx | `document-skills:docx` |
| Any chart, graph or dashboard | `dataviz` (read it before writing chart code) |

### Visual and design work
| Situation | Skill |
|---|---|
| A poster or static visual piece (.png/.pdf) | `example-skills:canvas-design` |
| Generative or data-driven art | `example-skills:algorithmic-art` |
| A web page, artifact or interface | `artifact-design`, then `frontend-design` |
| Critique of a design | `design-council` (philosophy) or `design-skills:design-critique` (heuristics) |
| Accessibility check | `design-skills:accessibility-audit` |
| Applying a ready-made theme to an artifact | `example-skills:theme-factory` |

### Writing and communications
| Situation | Skill |
|---|---|
| Internal updates, status reports, newsletters | `example-skills:internal-comms` |
| Co-writing a long document in stages | `example-skills:doc-coauthoring` |
| Interface copy, error messages, button labels | `design-skills:ux-writing` |

### Claude itself
| Situation | Skill |
|---|---|
| Building anything on the Claude API or SDK, or a model or pricing question | `claude-api:claude-api` |
| The user is learning how to use a Claude feature | `academy-guide:academy-guide` |
| After a substantive answer the user will act on (once per conversation) | `discernment-nudge:discernment-nudge` |
| Building a new skill or improving an existing one | `example-skills:skill-creator` |

## Environment notes

- The setup script on the **Clean Air** cloud environment installs the five Anthropic plugins
  (`document-skills`, `example-skills`, `claude-api`, `academy-guide`, `discernment-nudge`) from
  `anthropics/skills`, pinned to commit `e4bb5d960d87126ff3b3a8af1a104b7db67560ba`. They come
  from a local copy at `/opt/anthropic-skills-pinned`, under the marketplace name `skills-pinned`.
- Don't upgrade those plugins or run `claude plugin marketplace update` during a session unless
  asked. Upgrading is a deliberate change to the `SHA=` line in the setup script.
- If one of those skills is missing from a session, check `claude plugin list` and tell the user.
  Don't silently fall back to a different skill.
