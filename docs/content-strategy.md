# Wild-Lake content and navigation strategy

## Core consideration journey

Home -> Offerings -> Method -> Pricing -> Contact, with Terms of practice available throughout.

| Page | Reader's question | Content responsibility | Primary next step |
| --- | --- | --- | --- |
| Home | Is this studio relevant to my work? | Studio position, audiences, areas of focus, ownership commitment | Explore offerings |
| Offerings /practice/ | What does the studio construct? | Scope across Sovereign A&R and Talent architecture | Next: read the method |
| Method /method/ | How does the practice operate? | Diagnosis, terminology, mechanics, execution, institutional alignment, consent, governance | Next: engagements & pricing |
| Pricing /pricing/ | How is an engagement structured? | Commercial rhythms, cross-subsidy, access boundaries, ownership, intake sequence | Next: begin an engagement |
| Contact /contact/ | What information should I send? | Optional diagnostic prompts and unmediated email draft | Open email draft |
| Terms /terms/ | What governs the agreement? | Ownership, licensing, capacity, payment, agreement boundaries | Contact the studio |

Clients provides evidence of practice. Founder establishes authorship and responsibility. Development protocols explains optional practices and is reached contextually from Method, Offerings, and Pricing. Tools and Magazine serve exploration without replacing the consideration journey.

## Navigation source

The ten-item primary navigation is defined in tools/navigation.json and rendered into all published HTML pages by tools/sync_navigation.py. Order: Home, Clients, Founder, Offerings, Method, Pricing, Tools, Magazine, Contact, Begin.

Use aria-current="page" only when a primary link matches the exact current route. Pages absent from the primary bar do not falsely mark a different route as the current page. Tools, Magazine, and Method can use aria-current="location" to orient readers within the associated branch.

Shared navigation geometry lives in site/assets/navigation.css, loaded before the final typography sheet. Mobile uses three columns with 44px minimum link heights. Desktop wraps without clipping and stays within the shared content rail.

## Maintenance rules

- Keep service scope canonical on Offerings, operating mechanics on Method, and commercial formats on Pricing. Link to the owning page when context is needed elsewhere.
- Place a forward link at the end of each core page and orientation links for readers arriving directly from search.
- Preserve optional outreach. Reviewing other pages establishes context, not a form submission prerequisite.
- Preserve the homepage monolith and first viewport. Changes there require an explicit proposal and user approval.
- Keep visible copy, canonical page schema, embedded JSON-LD, schema previews, and llms.txt synchronized.
- Run tools/check_navigation.py to verify navigation parity, active states, local paths, and anchors. Run tools/check_typography.py and tools/test_typography.cjs for type and responsive integrity.

## Editorial case

Use sentence case for headings, navigation labels, captions, role titles, form labels, and calls to action. Preserve the spelling and capitalization of proper names, acronyms, and published artwork or publication titles. Do not force editorial labels into uppercase with CSS. The protected homepage monolith and its existing first-viewport location line remain unchanged unless the user reviews and approves a proposal.
