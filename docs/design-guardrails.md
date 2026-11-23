# Design guardrails

`docs/design-brief.md` remains the visual authority. This file turns its principles into testable limits so that the Clean Air look (paper, white, ink, navy, a restrained red, Georgia plus system sans) cannot drift. Machine-readable values: `tools/design-tokens.json`. Checks: `tools/check_design.py` (static CSS) and `site/qa/qa.js` (rendered pages). Nothing here imports another site's identity.

## Command mapping

| Brief's suggested check | Command | What fails it |
|---|---|---|
| `check-stripes.js` | `python3 tools/check_design.py stripes` | a left border or inset left shadow on anything other than `.finding` and `details.evidence`; gradients; glows; blur; grain |
| `check-cards.js` | `python3 tools/check_design.py cards` | a bordered surface not registered in the four container families; any `box-shadow`; a radius outside the tokens |
| `check-type.js` | `python3 tools/check_design.py type` + qa.js | a font family other than `var(--serif)`/`var(--sans)`; any public text under 12 px (static estimate and rendered measurement) |
| `check-colours.js` | `python3 tools/check_design.py colours` | a colour literal outside `:root` tokens (print CSS excepted); a CSS token that differs from `design-tokens.json`; an undocumented token; green; AQI colours outside an AQI legend |
| `check-contrast.js` | `python3 tools/check_design.py contrast` + axe in qa.js | any documented foreground/background pair below its WCAG ratio |
| size budget | `python3 tools/check_design.py budget` | CSS, JS, page, Markdown or `llms-full.txt` over budget |
| self-test | `python3 tools/check_design.py --self-test` | each check must fail on `tools/fixtures/design/bad.css` or the oversized fixture |

## Rules

**No template decoration.** No gradients, glows, grain, decorative noise, heavy shadows, left accent stripes on cards, arbitrary icon sets or gratuitous motion. Structure comes from rules and whitespace. Notes now carry a 3 px navy *top* rule (the same device as section rules) instead of a left stripe.

**Four container families** (existing classes registered, not renamed):

| Family | Classes | Use |
|---|---|---|
| card | `.card`, `.org-card`, `.preset`, `.entry` | distinct interactive objects |
| note | `.notice`, `.layer.simple`, `.trust` | short answer, caveat, notice |
| row | `.flow`, `.chain-step` | one step or link in a sequence |
| panel | `.explorer`, `.toc`, `.compare-pick`, `details.q` | controls and navigation blocks |

Chips (`.badge`, `.fcat`, `.tag`), controls and tables are registered separately as inline components.

**Radii:** `--radius` 3 px (containers, controls), `--radius-chip` 2 px (chips), or 0. **Padding steps:** `--pad-1`, `--pad-2`, `--pad-3`. **Shadows:** none; reserved for genuinely floating surfaces (there are none today).

**Seven type roles** from two families: page title (h1 serif), section heading (h2 serif), subheading (h3 serif), narrative/lede (`.deck`, `.simple-answer`, `.finding`, serif 1.2 rem), body (serif 18 px, 19 px from 720 px), caption/metadata (sans 0.75 to 0.9 rem), numeric/table (sans 0.88 rem). Measure about 65 characters. Minimum 12 px everywhere, including citation superscripts (`max(12px, .72em)`).

**Colour roles** (each token has one job; see `colour_roles` in the JSON):

| Role | Tokens |
|---|---|
| brand accent: rules, large text, active-nav marker; never small text on paper (4.38:1) | `--ca-accent`, `--ca-accent-dark` (6.93:1 on white, for small red text) |
| navigation and headings | `--ca-navy`, `--ca-on-navy` |
| links and focus | `--ca-link`; white focus ring on navy (15.6:1) |
| text | `--ca-ink`, `--ca-muted`, `--ca-muted-strong` |
| surfaces | `--ca-paper`, `--ca-surface`, `--ca-rule`, `--ca-tint`, `--ca-highlight` |
| evidence strength | navy fill (Strong), navy outline (Moderate), grey outline (Limited/mixed), dashed grey (No adequate evidence), always with the text label; never green |
| measured AQI categories | reserved prefix `--aqi-*`. No AQI legend is drawn in this edition, so no AQI colours are defined; if one is added it uses the verified CPCB classification with text labels, separate from brand colours. |

**Phone first.** Zero sideways page scroll at 320, 375, 768 and 1280 px with text at 200% (10 representative pages), and at 320 px for all 315 pages. Grids use `minmax(min(Xrem,100%),1fr)`; long words wrap (`overflow-wrap:anywhere`, tables excepted, which scroll inside `.table-wrap`). Keyboard focus visible on every stop. Targets meet WCAG 2.2 (24 × 24 px; source and citation links use `.src-link` / `a.cite`). Print hides navigation. `prefers-reduced-motion` disables any animation or smooth scroll; the site has no animation.

**Budgets.** See `budgets_bytes` in the JSON and section 4 of `docs/THREE_AUDIENCES_AUDIT.md`. Current: CSS 19.5 kB, JS 6.3 kB, largest page 170 kB (organisations hub, budget 250 kB).

## Changes made to meet these rules (appearance otherwise unchanged)

Left stripes on `.notice`, `.layer.simple`, `.trust`, `.flow`, `.preset.on`, `.fcat.philanthropic` replaced by top rules, outlines or weight. Active navigation underline moved from `box-shadow` to a border. 16 colour literals tokenised (`--ca-on-navy`, `--ca-muted-strong`, `--ca-highlight` added). 4 px radii unified to the 3 px token. Grids and selects made zoom-safe. Citation size floor of 12 px.
