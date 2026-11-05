// moai: the Fibonacci Engine compiler for Wild-Lake routes. Go standard library only.
//
//	moai ingest <payload.zip> <new-dir>   zero-trust extraction: strip, repair, deny
//	moai build  [flags]                   compile src/ + the 783 typographic core into dist/
//	moai gate   [-dist dist] build/manifest.json
//	                                      deploy sentinel; same rules as sentinel/deploy.rego,
//	                                      plus a re-hash of every object on disk
package main

import (
	"crypto/sha256"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"path"
	"path/filepath"
	"regexp"
	"sort"
	"strings"
)

const (
	cacheImmutable = "public, max-age=31536000, immutable"
	cacheDocument  = "public, max-age=300, s-maxage=31536000, stale-while-revalidate=86400"
	coreID         = "https://seveneightythree.com/assets/#typography"
	coreBase       = "https://seveneightythree.com/assets/"
	description    = "A tarot web app for artists and creators. It shows the cards and no meanings: the querent reads the images and writes their own interpretation in the log."
)

var contentTypes = map[string]string{
	".html":   "text/html; charset=utf-8",
	".jsonld": "application/ld+json; charset=utf-8",
	".woff2":  "font/woff2",
	".ttf":    "font/ttf",
}

type object struct {
	Key             string   `json:"key"`
	Bytes           int      `json:"bytes"`
	SHA256          string   `json:"sha256"`
	ContentType     string   `json:"content_type"`
	CacheControl    string   `json:"cache_control"`
	Class           string   `json:"class"`
	CSP             string   `json:"csp,omitempty"`
	ExternalOrigins []string `json:"external_origins,omitempty"`
}

type manifest struct {
	Engine     string   `json:"engine"`
	Origin     string   `json:"origin"`
	Route      string   `json:"route"`
	Built      string   `json:"built"`
	Objects    []object `json:"objects"`
	Invalidate []string `json:"invalidate"`
}

func main() {
	if len(os.Args) < 2 {
		usage()
	}
	switch os.Args[1] {
	case "ingest":
		ingest(os.Args[2:])
	case "build":
		build(os.Args[2:])
	case "gate":
		gate(os.Args[2:])
	default:
		usage()
	}
}

func usage() {
	fmt.Fprintln(os.Stderr, "usage: moai ingest <payload.zip> <new-dir> | moai build [flags] | moai gate [-dist dist] <manifest.json>")
	os.Exit(64)
}

func fatal(f string, a ...any) {
	fmt.Fprintf(os.Stderr, "moai: "+f+"\n", a...)
	os.Exit(1)
}

func must(err error) {
	if err != nil {
		fatal("%v", err)
	}
}

func read(p string) []byte {
	b, err := os.ReadFile(p)
	must(err)
	return b
}

func write(p string, b []byte) {
	must(os.MkdirAll(filepath.Dir(p), 0o755))
	must(os.WriteFile(p, b, 0o644))
}

func sum(b []byte) string { h := sha256.Sum256(b); return hex.EncodeToString(h[:]) }

func cspHash(s string) string {
	h := sha256.Sum256([]byte(s))
	return "'sha256-" + base64.StdEncoding.EncodeToString(h[:]) + "'"
}

var comments = regexp.MustCompile(`(?s)/\*.*?\*/`)

func tidyCSS(s string) string {
	s = comments.ReplaceAllString(s, "")
	var out []string
	for _, l := range strings.Split(s, "\n") {
		if l = strings.TrimRight(l, " \t\r"); strings.TrimSpace(l) != "" {
			out = append(out, l)
		}
	}
	return "\n" + strings.Join(out, "\n") + "\n"
}

func jsonOut(v any, indent bool) []byte {
	var b []byte
	var err error
	if indent {
		b, err = json.MarshalIndent(v, "", "  ")
	} else {
		b, err = json.Marshal(v)
	}
	must(err)
	return b
}

type node = map[string]any

func ref(id string) node { return node{"@id": id} }

func build(args []string) {
	fs := flag.NewFlagSet("build", flag.ExitOnError)
	src := fs.String("src", "src", "route source: index.html, app.css, app.js")
	core := fs.String("core", "../archivo-typography-substrate", "783 typographic core (its assets/ folder is read)")
	out := fs.String("out", "dist", "upload root: mirrors the bucket key space")
	bld := fs.String("build", "build", "manifest and invalidation list (never uploaded)")
	origin := fs.String("origin", "https://wild-lake.org", "public origin")
	route := fs.String("route", "/quiet-creek/tarot/", "route path")
	date := fs.String("date", "2026-11-05", "datePublished")
	must(fs.Parse(args))

	must(os.RemoveAll(*out))
	must(os.RemoveAll(*bld))
	routeKey := strings.Trim(*route, "/") + "/"
	url := *origin + *route
	m := manifest{Engine: "moai/1", Origin: *origin, Route: *route, Built: *date}
	add := func(key, class string, b []byte) *object {
		write(filepath.Join(*out, key), b)
		cc := cacheDocument
		if class == "immutable" {
			cc = cacheImmutable
		}
		m.Objects = append(m.Objects, object{Key: key, Bytes: len(b), SHA256: sum(b), ContentType: contentTypes[path.Ext(key)], CacheControl: cc, Class: class})
		return &m.Objects[len(m.Objects)-1]
	}

	// 1. typography: the 783 core, font URLs pointed at this origin's /assets/fonts/
	coreCSS := tidyCSS(strings.ReplaceAll(string(read(filepath.Join(*core, "assets/typography.css"))), "url('fonts/", "url('/assets/fonts/"))
	fontURL := regexp.MustCompile(`url\('/assets/fonts/([^']+)'\)`)
	type font struct {
		name, sha string
		bytes     int
	}
	var fonts []font
	seen := map[string]bool{}
	for _, mm := range fontURL.FindAllStringSubmatch(coreCSS, -1) {
		name := mm[1]
		if seen[name] {
			continue
		}
		seen[name] = true
		b := read(filepath.Join(*core, "assets/fonts", name))
		h := sum(b)
		parts := strings.Split(name, ".")
		if len(parts) < 3 || parts[len(parts)-2] != h[:8] {
			fatal("sentinel: %s hashes to %s, which its filename does not carry", name, h[:8])
		}
		if err := fontMagic(name, b); err != nil {
			fatal("sentinel: %v", err)
		}
		add("assets/fonts/"+name, "immutable", b)
		fonts = append(fonts, font{name, h, len(b)})
	}
	if len(fonts) == 0 {
		fatal("no font objects found in the core typography.css")
	}

	// 2. deck
	cards := deck()
	index := map[string]card{}
	pairs := make([][2]string, len(cards))
	for i, c := range cards {
		index[c.ID] = c
		pairs[i] = [2]string{c.ID, strings.ToUpper(c.Name)}
	}

	// 3. page
	css := coreCSS + tidyCSS(string(read(filepath.Join(*src, "app.css"))))
	js := string(read(filepath.Join(*src, "app.js")))
	if !strings.Contains(js, "/*DECK*/[]") {
		fatal("app.js has no /*DECK*/[] slot")
	}
	js = strings.Replace(js, "/*DECK*/[]", string(jsonOut(pairs, false)), 1)
	page := string(read(filepath.Join(*src, "index.html")))
	for _, mm := range regexp.MustCompile(`<use href="#([a-z0-9]+)"/>`).FindAllStringSubmatch(page, -1) {
		if _, ok := index[mm[1]]; !ok && mm[1] != "back" {
			fatal("index.html draws #%s, which is not in the deck", mm[1])
		}
	}
	csp := strings.Join([]string{"default-src 'none'", "style-src " + cspHash(css), "script-src " + cspHash(js), "font-src 'self'", "img-src 'self'", "base-uri 'none'", "form-action 'none'"}, "; ")
	var preload []string
	for _, f := range fonts {
		if strings.HasSuffix(f.name, ".woff2") && !strings.Contains(f.name, "Italic") {
			preload = append(preload, fmt.Sprintf(`  <link rel="preload" href="/assets/fonts/%s" as="font" type="font/woff2" crossorigin>`, f.name))
		}
	}

	wl, site, person := *origin+"/#organization", *origin+"/#website", "https://argelysoriach.com/#person"
	blog := *origin + "/quiet-creek/#blog"
	app, deckID := url+"#app", url+"#deck"
	pageNodes := []node{
		{"@type": "WebPage", "@id": url + "#page", "url": url, "name": "Tarot Framework // 783", "inLanguage": "en-US",
			"isPartOf": ref(site), "mainEntity": ref(app), "datePublished": *date},
		{"@type": "WebApplication", "@id": app, "name": "Quiet Creek Tarot", "url": url, "description": description,
			"applicationCategory": "LifestyleApplication", "operatingSystem": "Any", "isAccessibleForFree": true,
			"browserRequirements": "Drawing and the log need JavaScript; the opening spread renders without it.",
			"audience":            node{"@type": "Audience", "audienceType": "Artists and creators"},
			"isPartOf":            ref(blog), "publisher": ref(wl), "creator": ref(person), "hasPart": ref(deckID), "isBasedOn": ref(coreID), "datePublished": *date},
		{"@type": "CreativeWork", "@id": deckID, "name": "Quiet Creek Tarot deck",
			"description": "78 original cards, 22 major arcana and four suits of 14 (wands, cups, swords, pentacles), drawn as solid geometry in #FFFFFF on #000000. Card names only; no meanings.",
			"creator":     ref(person), "isPartOf": ref(app)},
		{"@type": "Blog", "@id": blog, "name": "Quiet Creek", "alternateName": "Quiet Creek by Wild-Lake", "url": *origin + "/quiet-creek/",
			"description": "On artists, creative work, and the structures that support an independent practice.", "publisher": ref(wl), "isPartOf": ref(site)},
	}
	pageLD := jsonOut(node{"@context": "https://schema.org", "@graph": pageNodes}, false)

	html := page
	for k, v := range map[string]string{
		"{{CSP}}": csp, "{{DESCRIPTION}}": description, "{{URL}}": url, "{{PRELOAD}}": strings.Join(preload, "\n"),
		"{{STYLE}}": css, "{{JSONLD}}": string(pageLD), "{{SPRITE}}": sprite(cards), "{{SCRIPT}}": js,
	} {
		html = strings.Replace(html, k, v, 1)
	}
	if strings.Contains(html, "{{") {
		fatal("unfilled slot in index.html")
	}
	o := add(routeKey+"index.html", "document", []byte(html))
	o.CSP = csp
	o.ExternalOrigins = externalOrigins(html)

	// 4. routing schema: every route and object this build puts on the edge
	graph := []node{
		{"@type": "Organization", "@id": wl, "name": "Wild-Lake", "url": *origin + "/"},
		{"@type": "WebSite", "@id": site, "url": *origin + "/", "name": "Wild-Lake", "publisher": ref(wl), "hasPart": []node{ref(blog)}},
		{"@type": "Person", "@id": person, "name": "Argelys Samuel Oriach", "url": "https://argelysoriach.com/"},
		{"@type": "CreativeWork", "@id": coreID, "name": "783 Monolithic Typographic Core", "url": coreBase},
	}
	pageNodes[3]["hasPart"] = []node{ref(app)}
	graph = append(graph, pageNodes...)
	parts := make([]node, len(cards))
	for i, c := range cards {
		parts[i] = node{"@type": "VisualArtwork", "@id": url + "#" + c.ID, "name": c.Name, "position": i + 1,
			"artform": "Tarot card", "artMedium": "SVG", "isPartOf": ref(deckID)}
	}
	pageNodes[2]["hasPart"] = parts
	for _, f := range fonts {
		u := *origin + "/assets/fonts/" + f.name
		graph = append(graph, node{"@type": "MediaObject", "@id": u, "contentUrl": u, "encodingFormat": contentTypes[path.Ext(f.name)],
			"contentSize": fmt.Sprintf("%d bytes", f.bytes), "sha256": f.sha, "sameAs": coreBase + "fonts/" + f.name, "isPartOf": ref(coreID)})
	}
	add(routeKey+"schema.jsonld", "document", append(jsonOut(node{"@context": "https://schema.org", "@graph": graph}, true), '\n'))

	// 5. manifest
	sort.Slice(m.Objects, func(i, j int) bool { return m.Objects[i].Key < m.Objects[j].Key })
	m.Invalidate = []string{*route}
	for _, o := range m.Objects {
		if o.Class == "document" {
			m.Invalidate = append(m.Invalidate, "/"+o.Key)
		}
	}
	write(filepath.Join(*bld, "manifest.json"), append(jsonOut(m, true), '\n'))
	write(filepath.Join(*bld, "invalidate.txt"), []byte(strings.Join(m.Invalidate, "\n")+"\n"))
	for _, o := range m.Objects {
		fmt.Printf("%-58s %9d  %s\n", o.Key, o.Bytes, o.SHA256[:12])
	}
	fmt.Printf("Structural integrity holds: %d objects, %d cards, route %s\n", len(m.Objects), len(cards), url)
}
