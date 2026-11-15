# FAQ and Terms delivery

The static build now serves `/faq` and replaces the existing `/terms` page. Both reuse the existing header, primary navigation, footer, fonts, typography tokens, layout rails and rule primitives. No framework, backend or tracking service was added.

## Universe API and Moai

The document publisher resolves to the studio Organization; `about` also references the canonical Universe API framework. FAQ questions and Terms sections have stable identifiers. FAQPage contains all fourteen Question/Answer pairs; Terms contains nine linkable WebPageElement sections. Their canonical JSON documents, HTML, sitemap and agent index are synchronized.

The source is `tools/engagement-pages/content.json`, transcribed verbatim from the supplied brief. `tools/build_engagement_pages.py` deterministically produces both HTML documents and their schemas using the site's existing shared shell. `--check` rejects drift. The new brief explicitly requires its legal/governance copy verbatim, including its em dashes; the punctuation exception is limited to these two pages, which are checked against the approved source. Existing punctuation rules continue elsewhere.

Before deployment, `tools/check_engagement_pages.py` verifies copy/schema parity, all answer control relationships, unique IDs, section anchors, legacy Terms aliases, local runtime origins and the small accordion script. `engagement_pages.rego` checks the extracted manifest and rejects malformed counts, remote origins, duplicate IDs and an oversized runtime. Five rejection fixtures test the actual OPA policy. Existing global OPA rule-class and clients identity gates remain active.

## Behavior and navigation

FAQ buttons support native Enter/Space activation, aria-expanded and aria-controls. Without JavaScript all answers remain visible. Terms is fully expanded and includes an anchored section index. Print styles use black text on white, hide navigation and retain readable content. A browser-generated PDF was checked during validation.

FAQ is placed immediately before Begin in the primary navigation, including its mobile rendering. FAQ and Terms are also in the footer Practice column. Existing Terms links remain valid; legacy `#sovereign-ip` and `#engagement` anchors are retained. The new Terms links to FAQ and contact; FAQ links to Terms and contact.

The homepage body, including its monolith, and the Method, Protocols and Offerings main content were compared against the previous commit and remain unchanged. Only the requested shared navigation/footer links and crawler metadata change outside the two documents.

## Validation

- Static HTML/asset, metadata, schema, deterministic-build, dependency and link checks pass.
- All 84 page/viewport navigation and typography checks pass at 320, 390, 768 and 1440px.
- All fourteen FAQ controls pass keyboard expand/collapse and exact-answer tests at those widths.
- Terms anchors, print layout and PDF output pass; FAQ remains readable without JavaScript.
- OPA accepts the valid page manifest and rejects five invalid fixtures.

Run:

    python3 tools/build_engagement_pages.py --check
    OPA_BIN=/path/to/opa python3 tools/check_engagement_pages.py
    node tools/test_engagement_pages.cjs
    node tools/test_navigation.cjs
    OPA_BIN=/path/to/opa bash tools/deploy.sh all

## Files created or changed

- `docs/faq-terms.md`
- `engagement_pages.rego`
- `site/about-founder/index.html`
- `site/app/index.html`
- `site/assets/engagement-documents.css`
- `site/assets/faq.js`
- `site/clients/index.html`
- `site/contact/index.html`
- `site/development-protocols/index.html`
- `site/faq/index.html`
- `site/index.html`
- `site/llms.txt`
- `site/magazine/index.html`
- `site/magazine/the-infrastructure-has-an-inner-life/es/index.html`
- `site/magazine/the-infrastructure-has-an-inner-life/index.html`
- `site/manifesto/index.html`
- `site/method/index.html`
- `site/mirror/index.html`
- `site/numerology/index.html`
- `site/practice/index.html`
- `site/pricing/index.html`
- `site/privacy/index.html`
- `site/responsibility/index.html`
- `site/schema/faq.json`
- `site/schema/index.html`
- `site/schema/terms.json`
- `site/schema/website.json`
- `site/sitemap.xml`
- `site/terms/index.html`
- `site/tools/index.html`
- `tools/build_engagement_pages.py`
- `tools/check_copy_sync.py`
- `tools/check_engagement_pages.py`
- `tools/check_metadata.py`
- `tools/check_navigation.py`
- `tools/check_typography.py`
- `tools/deploy.sh`
- `tools/engagement-pages/content.json`
- `tools/navigation.json`
- `tools/sync_navigation.py`
- `tools/test_engagement_pages.cjs`
- `tools/test_navigation.cjs`
