# Clients refactor

The clients page loads one generated stylesheet and a 1,222-byte vanilla runtime. Its native portrait dialog reads the clicked portrait source, alternative text and caption. The outline uses IntersectionObserver; without JavaScript, ordinary anchor navigation and portrait links remain available.

Edit `tools/clients/layout.css` for local layout and run `python3 tools/build_clients_css.py`. Shared fonts, typography utilities, navigation and footer are compiled from their canonical sources. No homepage presentation styles were changed.

The twelve roster articles, Person identities and ItemList references are validated as a bijection. The Organization identifies Lab 783 as its parent and the roster Argelys identity as its founder. Artistic direction uses Schema.org Person.jobTitle, worksFor and Organization.member, rather than a nonstandard artisticDirector property. The canonical personal identity and roster identity cross-reference each other.

Identity source additions: Aissa's existing Writers Colony profile; Kyle's LinkedIn profile at linkedin.com/in/kylemroach; Patrick's portfolio at cargocollective.com/patrickschlotterback, linked from his Popps Packing residency biography; Timo's Instagram at instagram.com/timosassen, linked by PAPER's profile. Artwork URLs are not treated as Person sameAs identities.

Before deployment, the build checks bundle freshness and extracts a trusted HTML/schema manifest into ignored `build/clients-policy-input.json`. `policy.rego` validates the manifest with OPA. Set OPA_BIN to the OPA executable if it is not on PATH:

    OPA_BIN=/path/to/opa bash tools/deploy.sh all

Checks:

    python3 tools/build_clients_css.py --check
    python3 tools/check_clients.py
    python3 tools/test_clients_policy.py /path/to/opa
    node tools/test_clients.cjs
    node tools/test_typography.cjs

The browser suite verifies overflow, the 377:610 grid breakpoint, all portrait dialogs and outline state at five widths. The actual OPA suite accepts the valid roster and rejects ten malformed identity/runtime fixtures.
