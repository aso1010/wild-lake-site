# Static home landing page

The homepage uses the approved seven-block order: header, hero, three services, cross-subsidy ledger, proof, four-field intake, footer. It replaces the former animated homepage under the owner's explicit landing-page brief.

One HTML file contains all CSS and the Organization/WebPage JSON-LD. There is no executable JavaScript, framework, tracker, popup, or email gate. The owner's later visual-identity instruction takes precedence over the initial no-web-fonts restriction: the existing self-hosted Archivo and JetBrains Mono files supply the studio typefaces, with no third-party requests. Black, white, square controls, thin divider rules, a 987px container, Fibonacci spacing, and the 13/21/34/55px type scale preserve studio continuity.

Native navigation links to Work, Ledger, Proof, and Begin. Legacy /#services and /#practice targets remain valid. Service links lead to existing offering anchors. Quiet Creek proof links directly to the essay, and the roster link leads to /clients/.

The four-field form uses the supplied mailto/text/plain fallback. It opens the user's configured email app; it does not submit to a web handler or store information. [FORM ENDPOINT], [PROOF], and [LEDGER FIGURES] remain as owner markers in HTML comments.

/li, /ig, and /fb, with or without trailing slashes, return 302 redirects to the same homepage with the corresponding utm_source and utm_medium=social query. These are URL attribution parameters, with no client-side analytics. All six routes were verified using Cloudflare's local static-assets router.

Validation: HTML markup validation passes. Lighthouse 12.8.2 accessibility 100 on mobile and desktop; browser checks at 390, 987, and 1440px; native keyboard navigation, form validity and mailto action, loaded studio fonts, no horizontal overflow or third-party requests; all repository links and schema checks. Local audit artifacts are build/home-lighthouse-mobile.json and build/home-lighthouse-desktop.json. The original animated-hero test entry now delegates to the static landing test.
