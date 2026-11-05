# Mirror development source

`engine/`, `src/` and `sentinel/` preserve the source supplied in quiet-creek-tarot.zip.
They are outside the public asset root. The Go engine uses the standard library.

The supplied generator targets the original `/quiet-creek/tarot/` application and
requires an external typography substrate. It does not reproduce the current site's
routing, metadata or narrower layout without adapting its source inputs.
Do not overwrite `site/mirror/` directly with its output.

Compile for inspection:

    cd tools/mirror/engine
    go build -o /tmp/wild-lake-mirror-engine .

Use a scratch output directory when running the generator. Review generated output,
apply the current `/mirror/` URLs and layout, regenerate CSP hashes, and validate
before promoting changes to `site/mirror/`. The shipped Terraform was not adopted:
this application remains hosted on the existing Cloudflare architecture.
