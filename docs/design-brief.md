# Clean Air: visual identity and design direction

This brief governs how the site looks. `docs/site-brief.md` governs what it contains. `docs/research-brief.md` governs the evidence. Visual polish must support accurate interpretation of the research.

Reference assets: the Clean Air wordmark and airflow icon images go in `docs/assets/` (wordmark.png, airflow-icon.png). Treat them as references and starting points, not final files.

Adopt these editorial principles: restrained colour, deliberate typography, clear wayfinding, generous whitespace and consistent layouts.

Create an independent Clean Air identity. Do not reproduce The Economist's masthead, branded illustrations or proprietary assets.

## Colour tokens

```css
--ca-ink: #1A1A1A;
--ca-navy: #141F52;
--ca-accent: #E3120B;
--ca-link: #2E45B8;
--ca-paper: #F5F4EF;
--ca-surface: #FFFFFF;
--ca-muted: #595959;
--ca-rule: #D9D9D9;
--ca-tint: #EBEDFA;
```

- Use warm paper and white for most surfaces.
- Use ink for text, navy for navigation, and red sparingly for emphasis.
- Do not turn entire pages into red warning panels.
- Keep AQI colours separate from brand colours. Where AQI is displayed, use the verified Indian (CPCB) classification with explicit text labels.
- Do not use green to imply that an intervention is proven or risk-free.
- Contrast note: `--ca-accent` on `--ca-paper` measures about 4.4:1, below the 4.5:1 AA threshold for small text. Use red on paper for large text, rules and icons only. Use it for small text on white (about 4.8:1) or darken it.

## Typography

- Use a readable editorial serif for headlines and long-form narrative. Pair it with a clear sans-serif for navigation, filters and tables.
- Use fonts available under suitable licences. Do not assume Milo or Econ Sans are available for reuse.
- Begin with Georgia and system sans-serif fallbacks. If you introduce other fonts, verify their licences and minimise loading overhead.
- Narrative text: about 18–20px, comfortable line spacing, reading width of about 65 characters.
- Use tabular numerals for numerical comparisons.

## Logo assets

- Create one consistent SVG airflow symbol using simple paths and flat fills. Do not embed a raster image inside an SVG and call it vector.
- Derive every version from one master geometry.
- Use licensed typography or accessible live text for the wordmark. Do not claim an exact match to the generated lettering if it differs.
- Keep the tagline separate: "Shared air. Unequal protection."

Produce:

1. Horizontal logo for light backgrounds.
2. Reversed logo for dark backgrounds.
3. Navy monochrome version.
4. White monochrome version.
5. Standalone symbol.
6. Simplified favicon suitable for 16px and 32px.

Test legibility at actual header and favicon sizes. Give the homepage logo link the accessible name "Clean Air — home". Hide purely decorative duplicates from assistive technology.

## Layout and components

- Use typography, whitespace and horizontal rules to establish hierarchy.
- Reserve bordered cards for genuinely distinct interactive objects.
- Keep corners subtle. Avoid decorative gradients and heavy shadows.
- Use 12px grid gaps on small screens and 16px on larger screens, with wider spacing between major sections.
- Make evidence details expandable without hiding the main finding.
- Intervention pages follow this order: what it does → who benefits → evidence → operating requirements → costs and uncertainties.

## Verification

Check colour contrast, keyboard focus, mobile layouts, text zoom, print output, logo transparency and loading performance.

Inspect the actual rendered result (screenshots at mobile and desktop widths) before declaring completion.
