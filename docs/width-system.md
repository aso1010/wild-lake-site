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
