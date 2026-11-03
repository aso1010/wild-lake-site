# Site motion

The portrait viewer's transform, tilt keyframes, separate scale transition, and configurable timing are adapted from the user-supplied transitions.dev Pro `image-open-tilt/css.md` recipe in `transitions-pro-skill.zip`. The optional software bend is disabled; pitch and travel are reduced for Wild-Lake. Native `<dialog>` supplies modal behavior, focus containment, Escape dismissal, and focus return. Image links work directly without JavaScript.

Section entrances use native Web Animations and IntersectionObserver. They run once, move at most 13px, and never hide content in the base stylesheet. Reduced motion suppresses entrances and image flights. Interaction feedback is 150ms; entrances/opening are 360ms; closing is 240ms. No motion is attached to the homepage monolith, top-level page scroll, or browser history.

The review pass leaves initially visible sections untouched and skips entrances for focused groups. Live reduced-motion changes cancel active entrances, settle an opening viewer, and finish a closing viewer immediately. Viewer labels, image dimensions, and captions follow the selected portrait.

The remaining Pro recipes were inspected but not used: the site has no matching delete, drag/drop, confetti, loading, or card-stack workflows. The supplied premium library and skill archives are not included in the public website.
