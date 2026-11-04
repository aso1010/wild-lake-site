# Site motion

The portrait viewer's transform, tilt keyframes, separate scale transition, and configurable timing are adapted from the user-supplied transitions.dev Pro `image-open-tilt/css.md` recipe in `transitions-pro-skill.zip`. The optional software bend is disabled; pitch and travel are reduced for Wild-Lake. Native `<dialog>` supplies modal behavior, focus containment, Escape dismissal, and focus return. Image links work directly without JavaScript.

Section entrances use native Web Animations and IntersectionObserver. They run once, move at most 13px, and never hide content in the base stylesheet. Reduced motion suppresses entrances and image flights. Interaction feedback is 150ms; entrances/opening are 360ms; closing is 240ms. No motion is attached to the homepage monolith, top-level page scroll, or browser history.

The review pass leaves initially visible sections untouched and skips entrances for focused groups. Live reduced-motion changes cancel active entrances, settle an opening viewer, and finish a closing viewer immediately. Viewer labels, image dimensions, and captions follow the selected portrait.

The remaining Pro recipes were inspected but not used: the site has no matching delete, drag/drop, confetti, loading, or card-stack workflows. The supplied premium library and skill archives are not included in the public website.

The responsive delight pass adapts organic-shimmer's travelling light into a single monochrome sweep along section rules, without its turbulence filters or continuous loading animation. The card-stack-hover spring timing drives small navigation underlines, arrow travel, and service title movement. Rules greet once on entry and can greet again on touch; no interaction blocks navigation or selects text. Live reduced motion cancels the sweeps. Recipe archives remain outside the public directory.

The contact action uses the supplied get-pro-button CSS recipe with a lower rim strength, slower clocks, existing button geometry, and animation paused until hover/focus. Its label and mailto semantics stay intact. Spinner-to-check was reviewed and omitted because draft preparation is synchronous and cannot confirm email delivery.

Blog: the supplied Transitions Pro card-stack-hover spring timing is reused for a small directional arrow on the studio return link; hover and reduced-motion guards preserved. No placeholder posts are published.
