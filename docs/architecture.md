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
