# Somatic field

The supplied Come Home to Your Body instrument lives at `/field/`. `/field`, `/somatic`, and `/somatic/` redirect to the canonical route. The studio menu, Tools page, sitemap, website graph, and llms.txt all index that route. The complete application graph is published at `/schema/field.json` and embedded in the instrument head.

The page remains one independent HTML document. Its supplied Archivo WL and JetBrains Mono WL base64 font payloads, six-track Fibonacci grid, lung datum, breath curve, and critically damped hand physics are preserved. The conflicting light style was removed. Metadata, schema, and the single stylesheet reside in the head. The studio wordmark links home. Touch capture and release prevent a stuck hand load.

There are no external dependencies, network endpoints, storage, analytics, or data submission. Universe API indexing is represented by the deterministic canonical entity graph, not a new transmission service.

The field intentionally retains its supplied dynamic typography rather than loading the studio type sheet or full navigation rail. Shared audits explicitly recognize that standalone instrument; tools/check_field.py separately enforces the original font hashes, constants, document hierarchy, punctuation, and schema. The two resting breath placeholders use `--` as requested. No em dashes appear anywhere in the document.

Validation: `python3 tools/check_field.py` and `node tools/test_field.cjs`. Browser checks cover mobile, desktop, wide desktop, landscape, deterministic frequency and damping, keyboard focus and hold/release, touch, reduced motion, JavaScript-disabled first paint, no horizontal overflow, no external requests, and no storage.
