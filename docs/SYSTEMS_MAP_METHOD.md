# Systems map method (maintainer edition)

The public method is `research/site-content/systems-map-method.md`, rendered at `/systems-map/method.html`. This file adds the schema and maintenance steps.

## Model

Six layers kept apart: sources (A), atmosphere (B), exposure (C), health (D), livelihoods and households (E), institutions, rules and money (F). Ten systems group the nodes thematically (`systems.csv`). Emissions, concentrations, exposure and outcomes are different nodes; an area reading is never treated as personal exposure.

## Schema (`research/systems-map/`)

| File | Key | Fields |
|---|---|---|
| `systems.csv` | `system_id` | title, plain description, order |
| `nodes.csv` | `node_id` | system, layer (A to F), short label, explanation (two sentences), type, population tags (community-impacts IDs), geography, timescale, claim IDs, key (shown in the simple view) |
| `edges.csv` | `edge_id` (Ennn, never renumbered; E37 retired) | from, to, mechanism, direction (increase, decrease, conditional), relation kind (causal, associative, mechanism, reasoned_hypothesis), evidence strength (four labels), reason in words, claim IDs, geography, uncertainty, key |
| `cycles.csv` | `cycle_id` (Ln) | title, ordered edge IDs, why feedback occurs, loop confidence (whole loop), contexts, caveats |
| `levers.csv` | `lever_id` = intervention `int_id` | mode, target edges, what could change, risks, what to measure, what is unproven. **No rating column**: effectiveness comes from `interventions.csv`. |
| `institutions.csv`, `lever-roles.csv` | institution, (lever, role, institution) | generic institutional functions per lever (sets standard, pays, delivers, operates, evaluates, represents) |
| `journeys/*.md` | `id` | composite label, population, ordered steps (edge ID, what happens, who bears it) |
| `questions.csv` | `question_id` | the brief's reader questions with answer and links (edge, loop, lever, journey) |
| `ledger.csv` | `candidate_id` | accepted, contested, rejected and queued candidate loops and edges, with reasons |

Derived at build: edge order (direct, knock-on, hypothesis), loop membership, targeting levers, weakest link and measured links per loop, lever organisations (verified roles on activity records listing the intervention), lever funding (programmes and flows listing it).

## Rules enforced by `tools/check_systems_map.py`

Unique IDs; no dangling references (systems, nodes, edges, claims, interventions, institutions, populations, journeys, questions); only the four labels; hypotheses never Strong or Moderate; measured edges cite claims; no withdrawn claims; Strong edges need a passage-checked claim from a fully read source; no Strong or Moderate edge on snippet-only sources; every loop closes; loop confidence never above its weakest link; levers carry no rating and the published rating equals the intervention assessment; no outcome promises on map pages; every node and edge present in the diagram, the text view, the CSV and the JSON; advertised counts equal the data. `--self-test` appends the bad rows in `tools/fixtures/systems-map/` to a copy of the data and requires every rule family to fail.

## Adding things

- **An edge:** add claims first (and run `research/analysis/passages.py`; new claims need a located passage), then a row in `edges.csv` with a reason for the rating. A link with no claim is a `reasoned_hypothesis` rated "No adequate evidence found" or "Limited/mixed".
- **A loop:** list existing edge IDs in order so that each starts where the last ended and the last returns to the first. Rate the loop as a whole "No adequate evidence found" unless a study tested the cycle end to end. Record rejected candidates in `ledger.csv`.
- **A lever:** use an existing intervention ID (assess it in `interventions.csv` first), list target edges, risks, measures and what is unproven, and add roles in `lever-roles.csv`. Organisations and funding appear automatically from the atlas when an activity record lists the intervention.
- Run `python3 tools/check_all.py`.

## Limits

Mostly India, anchored on Delhi-NCR; livelihood and household links are the least measured; loops are interpretations; no quantitative propagation of effects; geography filters for non-Indian settings are not offered because few edges carry non-Indian evidence (edges show their place in text instead).
