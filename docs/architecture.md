# Architecture

The public root is `site/`. No root-level repository files, deployment configuration,
Go source, or policy source are served by the Workers.

`deploy/site.wrangler.json` deploys the existing `dark-queen-31fb` static Worker.
Its existing custom-domain bindings remain managed in Cloudflare.

`deploy/mirror.wrangler.json` deploys `wild-lake-mirror` and its custom domain,
`mirror.wildlakestudio.com`. The Worker maps root requests to `/mirror/` in the
same static asset tree. Both deployments must run after shared public files change.

Canonical URLs, browser routes, font URLs and public schemas are independent of
the checkout directory name. Legacy `/blog/` routes remain in `site/_redirects`.

`build/`, `dist/`, caches and tool binaries are generated artifacts and ignored.
The tracked Mirror HTML is the current deployed artifact; its inline CSP hashes
must match its scripts and styles. `tools/validate.py` checks that contract.

## Fluid Fibonacci system

`site/assets/fibonacci.css` is loaded after page styles. Shared spacing uses 8, 13,
21, 34, 55, 89 and 144px anchors in rem units, with fluid interpolation. Desktop
introductory columns use 0.618:1 proportions; small screens stack. Typography
remains stable while reading; motion honors reduced-motion preferences. The
homepage retains the studio descriptor; interior introductions omit it. Mirror
keeps its isolated inline layout and CSP, with its own Fibonacci spacing.

## Installed tarot app

`site/app/` is the supplied dist-app artifact, served directly at
`https://mirror.wildlakestudio.com/app/`. The Mirror Worker passes `/app/`
requests through without its legacy `/mirror/` rewrite. The app service worker
is scoped to `/app/`; it does not control the existing Mirror root.
The supplied UI copy reference is preserved in `docs/mirror-app-copy.md`.

## Structured copy

`site/schema/` holds the canonical organization, founder, website, client roster,
Method, Development Protocols, and engagement descriptions. Full entity definitions
embedded in page JSON-LD must match those documents; identity-only references may
remain compact. The client-page founder identity stays distinct so its role list
can focus on the artistic practice. `site/llms.txt` summarizes the current public
copy and links to each document. The schema page previews the canonical files.

`tools/check_copy_sync.py` checks repeated entity definitions and previews before
deployment. Copy changes affecting these descriptions require their canonical
JSON and llms.txt counterparts to be updated in the same change. The check uses
only the Python standard library and adds no browser dependency.

## Water monolith preview

`/?water=1` enables Paper Shaders Water (0.0.82, Apache-2.0) through a local native WebGL2 renderer. The GLSL and license are vendored in `site/assets/`; no React or package runtime is required. Water settings follow the supplied example, using a transparent SVG wordmark as its image texture. The background is transparent and the shader output is alpha-masked to the distorted glyphs, keeping the surrounding site pure black. The animation clock runs at 1/8 speed (8 is a Fibonacci number), independently of its smooth render cadence. The effect pauses outside the viewport or hidden tabs, provides a pause control, and falls back to the SVG for reduced motion or unavailable WebGL. The normal homepage remains the default presentation.
