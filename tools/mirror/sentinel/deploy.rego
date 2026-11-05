# MoAI deploy sentinel. Input: build/manifest.json. An empty deny set is the only way through.
#
#   opa eval --fail-defined -d sentinel -i build/manifest.json 'data.moai.sentinel.deny[x]'
#
# Same policy as `moai gate`, which additionally re-hashes every object on disk.
package moai.sentinel

import rego.v1

immutable := "public, max-age=31536000, immutable"

document := "public, max-age=300, s-maxage=31536000, stale-while-revalidate=86400"

types := {
	".html": "text/html; charset=utf-8",
	".jsonld": "application/ld+json; charset=utf-8",
	".woff2": "font/woff2",
	".ttf": "font/ttf",
}

ext(key) := e if {
	parts := split(key, ".")
	count(parts) > 1
	e := concat("", [".", parts[count(parts) - 1]])
}

font(o) if startswith(o.key, "assets/fonts/")

hashed(o) if {
	parts := split(o.key, ".")
	count(parts) >= 3
	parts[count(parts) - 2] == substring(o.sha256, 0, 8)
}

csp_ok(o) if {
	contains(o.csp, "default-src 'none'")
	not contains(o.csp, "unsafe-")
}

deny contains "manifest holds no objects" if count(input.objects) == 0

deny contains msg if {
	some o in input.objects
	not regex.match(`^[A-Za-z0-9][A-Za-z0-9._/-]*$`, o.key)
	msg := sprintf("%s: key shape", [o.key])
}

deny contains msg if {
	some o in input.objects
	contains(o.key, "..")
	msg := sprintf("%s: key shape", [o.key])
}

deny contains msg if {
	some o in input.objects
	regex.match(`(^|/)(__MACOSX|\._|\.DS_Store)`, o.key)
	msg := sprintf("%s: operating-system metadata", [o.key])
}

deny contains msg if {
	some o in input.objects
	not types[ext(o.key)] == o.content_type
	msg := sprintf("%s: content type %s", [o.key, o.content_type])
}

deny contains msg if {
	some o in input.objects
	count(o.sha256) != 64
	msg := sprintf("%s: sha256 missing", [o.key])
}

deny contains msg if {
	some o in input.objects
	font(o)
	not o.cache_control == immutable
	msg := sprintf("%s: font objects must be served %q", [o.key, immutable])
}

deny contains msg if {
	some o in input.objects
	font(o)
	not hashed(o)
	msg := sprintf("%s: immutable object without its content hash in the name", [o.key])
}

deny contains msg if {
	some o in input.objects
	not font(o)
	not o.cache_control == document
	msg := sprintf("%s: documents must be served %q", [o.key, document])
}

deny contains msg if {
	some o in input.objects
	o.bytes > 1048576
	msg := sprintf("%s: %d bytes exceeds 1 MiB", [o.key, o.bytes])
}

deny contains msg if {
	some o in input.objects
	o.content_type == types[".html"]
	not csp_ok(o)
	msg := sprintf("%s: CSP must start from default-src 'none' with no unsafe- sources", [o.key])
}

deny contains msg if {
	some o in input.objects
	some origin in o.external_origins
	msg := sprintf("%s: loads from third-party origin %s", [o.key, origin])
}

deny contains msg if {
	some p in input.invalidate
	startswith(p, "/assets/fonts/")
	msg := sprintf("invalidate %s: immutable objects are never invalidated", [p])
}

deny contains msg if {
	some p in input.invalidate
	not regex.match(`^/[^*?]*$`, p)
	msg := sprintf("invalidate %s: exact paths only", [p])
}
