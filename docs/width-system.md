# Width and rule system

The outer layout rail is 85rem, bounded by the viewport and the shared responsive gutter. Navigation, section boundaries and footer use that rail. The protected homepage first viewport retains its existing gutter and presentation.

Body paragraphs use the shared 64ch reading measure; lead paragraphs use 55ch. Measures are maximums, so copy in narrower cards and grid columns stays within its track. Paragraph width does not determine the length of a section divider.

`assets/primitives.css` defines three explicit rule tiers:

- `rule-datum`: section or page boundary, full parent container width.
- `rule-measure`: an editorial break within prose, at most 64ch.
- `rule-inline`: a break within a card or grid track, full track width.

Existing standalone section rules are semantic hr elements with rule-datum. Container borders such as navigation, cards and data rows remain attached to their owning containers. Unclassed hr elements have zero footprint and are rejected by the deployment gate. The dark theme overrides the primitive's default black stroke with the existing structural rule color.

`rules_lint.rego` uses Rego v1 syntax. `tools/check_rules.py` extracts each HTML document's rule AST, preserves source line numbers, runs OPA, and checks five valid/invalid regression fixtures. Missing class attributes fail closed. The deploy script runs this gate before uploading assets.

Clients includes the primitives in its compiled stylesheet, preserving its single-CSS-request architecture. Other static pages load primitives before the canonical typography layer.

## Opening viewport correspondence

The homepage monolith and location caption share `.monolith-fold`. Its geometry follows the uploaded Argelys Samuel Oriach page: desktop gutters clamp from 13px through 2vw to 55px; vertical mark padding clamps from 13px through 2svh to 34px; the caption uses a 1.5 line height and 21px bottom inset. On screens up to 600px the mark and caption form a centered group with 5px side insets and a 13px caption gap. The two Wild-Lake rows occupy the same overall frame as the personal site's three name rows.

`node tools/test_hero.cjs` checks the frame and caption coordinates at 390, 1440 and 2048px and verifies that toggling between double sine and water motion leaves the frame unchanged. Direct browser comparison against the uploaded reference confirmed matching desktop boxes and mobile boxes within 0.04px.

## Caption hierarchy

`--text-caption` is the single 9 to 11px responsive caption scale. The homepage locations line aliases that token; `.type-caption` applies it to the globe tagline, magazine/essay deck and Instagram link. Captions use the shared 1.5 line height, while the tagline retains its existing italic font style. This separates those supporting elements from body copy and navigation without changing headline or monolith sizing.
