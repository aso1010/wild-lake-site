# Native site motion

The current motion system is local CSS and browser JavaScript. No transition
package, framework, CDN, build step, skill file or recipe archive is required to
render the site. The earlier recipe-based treatment was replaced by this native
implementation; historical attribution remains in Git history.

- CSS transitions provide link, navigation, button and portrait feedback.
- A native dialog provides the image viewer. A short opacity/transform transition
  replaces the former 3D tilt. Escape, focus return and direct image links remain.
- IntersectionObserver and Web Animations provide one-time 8px section entrances.
- CSS View Transitions enhance same-origin navigation where supported.
- Reduced-motion preferences disable optional effects, including during playback.
- Archivo and JetBrains Mono font binaries are hosted alongside the site.

No third-party embeds or analytics scripts are shipped. External links remain
ordinary anchors and load their destination only when followed.
Cloudflare serves the static files. Wrangler is a deployment tool, not a browser
runtime or build dependency. The Mirror and Tarot app already ship self-contained
HTML, local fonts and native browser code; their isolated CSPs remain unchanged.

`python3 tools/check_dependencies.py` rejects remote scripts, styles, font loads,
preconnects, CSS imports and initial iframe embeds. Deployment runs this check
alongside `tools/validate.py`. Browser tests additionally exercise interactions
with external requests blocked.

## Quiet Creek water

The magazine monolith uses the shared, locally hosted Paper Shaders Water GLSL. Its SVG outlines are rasterized into a transparent letter texture rather than using a remote photograph. Settings: gray back color, white highlights, highlights/layering/edges/caustic zero, waves 0.5, size 0.5, scale 0.4, contain fit, speed 0.25. Transparent texture padding prevents the ripples from clipping letter edges.

Water starts moving by default. A transparent button covers the monolith: clicking, Enter or Space freezes the rendered water at its current time; a second activation resumes it. There is no separate visible pause control or persistent border. Reduced-motion preferences and unavailable WebGL retain the static SVG. Offscreen or hidden pages stop the render loop. The homepage renderer is unchanged.

`node tools/test_quiet_creek_water.cjs` checks the actual uniforms, transparent corner pixels, frozen draw count, resume behavior, keyboard access, stable layout and reduced-motion fallback at mobile and desktop widths.
