# Homepage structure and hierarchy

The refactor applies the repository's Universe API framework identity (`site/schema/universe-api.json`) and Moai sentinel rules (`rules_lint.rego` and the existing deploy gates). No standalone Moai SKILL.md was available. The Mirror compiler targets its own application and is not used to overwrite the homepage.

The content now has one native main landmark, a consistent outer rail, a single section spacing rhythm, three service columns, two client readings, and three independent resources. Ownership terms and the invitation share one closing section. Native section navigation follows the same six-section DOM order. Text has been separated into headings and descriptions without adding claims or services.

All layout changes are confined to the homepage content stylesheet. Existing typography variables and semantic roles remain canonical. Divider rules stay explicitly typed. The monolith, location caption, original inline styles, motion runtime, navigation and footer remain outside the scope of the refactor.

The visible section order drives WebPageElement data in website.json, embedded JSON-LD, schema previews and llms.txt. The existing organization and Universe API references remain intact. No runtime dependency, tracking script, backend or framework was introduced.

Verification: original monolith and ground geometry plus motion toggles at 390, 1440 and 2048px; resource and service grids, closing block, keyboard focus, overflow and divider alignment at 320, 390, 987, 1440 and 2048px; normal publishing gates including Moai's typed-rule OPA sentinel. Desktop and mobile resource/closing screenshots were inspected. The closing layout explicitly clears the old invitation margin and padding that produced the excessive gap.
