package main

// MoAI sentinels. Two isolated gates, no shared state with the compiler:
//   ingest: a payload enters; resource forks are stripped, minor corruption is repaired,
//           anything unsafe is denied and left behind. Extraction continues past every finding.
//   gate:   a build leaves; every object is re-hashed from disk and checked against policy.

import (
	"archive/zip"
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"net/url"
	"os"
	"path"
	"path/filepath"
	"regexp"
	"sort"
	"strings"
)

type finding struct {
	Action string `json:"action"` // strip | repair | warn | deny
	File   string `json:"file"`
	Detail string `json:"detail"`
}

var allowExt = map[string]bool{
	".html": true, ".htm": true, ".css": true, ".js": true, ".svg": true, ".json": true, ".txt": true, ".md": true,
	".woff2": true, ".woff": true, ".ttf": true, ".otf": true, ".png": true, ".jpg": true, ".jpeg": true, ".webp": true,
}

func fontMagic(name string, b []byte) error {
	if len(b) < 4 {
		return fmt.Errorf("%s: %d bytes is not a font", name, len(b))
	}
	want := map[string][]string{".woff2": {"wOF2"}, ".woff": {"wOFF"}, ".ttf": {"\x00\x01\x00\x00", "true"}, ".otf": {"OTTO"}}[strings.ToLower(path.Ext(name))]
	for _, w := range want {
		if string(b[:4]) == w {
			return nil
		}
	}
	return fmt.Errorf("%s: magic %q does not match its extension", name, b[:4])
}

var (
	linkTag   = regexp.MustCompile(`(?is)<link\b[^>]*>`)
	scriptSrc = regexp.MustCompile(`(?is)<script\b[^>]*\bsrc\s*=\s*["']?((?:https?:)?//[^"'\s>]+)[^>]*>\s*</script>`)
	mediaSrc  = regexp.MustCompile(`(?is)<(?:img|iframe|source|audio|video|embed|track)\b[^>]*\bsrc\s*=\s*["']?((?:https?:)?//[^"'\s>]+)`)
	attrHref  = regexp.MustCompile(`(?is)\bhref\s*=\s*["']?([^"'\s>]+)`)
	attrRel   = regexp.MustCompile(`(?is)\brel\s*=\s*["']?([^"'>]+)`)
	cssURL    = regexp.MustCompile(`(?is)(?:url\(\s*["']?|@import\s+["'])((?:https?:)?//[^"')\s]+)`)
	cssImport = regexp.MustCompile(`(?im)^\s*@import\s+[^;]*(?:https?:)?//[^;]*;\s*$`)
	white     = regexp.MustCompile(`(?i)#fff(?:fff)?\b|\bwhite\b`)
	loadRel   = regexp.MustCompile(`(?i)\b(stylesheet|preload|modulepreload|prefetch|preconnect|dns-prefetch|icon)\b`)
)

func external(u string) bool {
	return strings.HasPrefix(u, "//") || strings.HasPrefix(u, "http://") || strings.HasPrefix(u, "https://")
}

func originOf(u string) string {
	if strings.HasPrefix(u, "//") {
		u = "https:" + u
	}
	p, err := url.Parse(u)
	if err != nil || p.Host == "" {
		return u
	}
	return p.Scheme + "://" + p.Host
}

// externalOrigins lists every third-party origin the document would load from.
func externalOrigins(doc string) []string {
	set := map[string]bool{}
	for _, l := range linkTag.FindAllString(doc, -1) {
		r, h := attrRel.FindStringSubmatch(l), attrHref.FindStringSubmatch(l)
		if r != nil && h != nil && loadRel.MatchString(r[1]) && external(h[1]) {
			set[originOf(h[1])] = true
		}
	}
	for _, re := range []*regexp.Regexp{scriptSrc, mediaSrc, cssURL} {
		for _, mm := range re.FindAllStringSubmatch(doc, -1) {
			set[originOf(mm[1])] = true
		}
	}
	out := make([]string, 0, len(set))
	for o := range set {
		out = append(out, o)
	}
	sort.Strings(out)
	return out
}

// braces counts { and } outside comments and strings.
func braces(s string) (open, close int) {
	s = comments.ReplaceAllString(s, "")
	var q byte
	for i := 0; i < len(s); i++ {
		c := s[i]
		switch {
		case q != 0:
			if c == '\\' {
				i++
			} else if c == q {
				q = 0
			}
		case c == '"' || c == '\'':
			q = c
		case c == '{':
			open++
		case c == '}':
			close++
		}
	}
	return
}

func ingest(args []string) {
	if len(args) != 2 {
		usage()
	}
	zpath, dst := args[0], args[1]
	if ents, err := os.ReadDir(dst); err == nil && len(ents) > 0 {
		fatal("ingest: %s is not empty", dst)
	}
	zr, err := zip.OpenReader(zpath)
	must(err)
	defer zr.Close()

	const fileCap, totalCap = 16 << 20, 64 << 20
	var total int64
	var fs []finding
	note := func(a, f, d string, x ...any) { fs = append(fs, finding{a, f, fmt.Sprintf(d, x...)}) }
	kept := 0
	for _, f := range zr.File {
		name := f.Name
		base := path.Base(name)
		switch {
		case strings.HasPrefix(name, "__MACOSX/") || strings.HasPrefix(base, "._") || base == ".DS_Store" || base == "Thumbs.db":
			if !f.FileInfo().IsDir() {
				note("strip", name, "operating-system metadata, %d bytes", f.UncompressedSize64)
			}
			continue
		case f.FileInfo().IsDir():
			continue
		case f.Mode()&os.ModeSymlink != 0:
			note("deny", name, "symbolic link")
			continue
		}
		clean := path.Clean(strings.ReplaceAll(name, "\\", "/"))
		if path.IsAbs(clean) || clean == ".." || strings.HasPrefix(clean, "../") {
			note("deny", name, "path escapes the extraction root")
			continue
		}
		ext := strings.ToLower(path.Ext(clean))
		if !allowExt[ext] {
			note("deny", name, "file type %q is not on the allowlist", ext)
			continue
		}
		if f.UncompressedSize64 > fileCap || (f.CompressedSize64 > 0 && f.UncompressedSize64/f.CompressedSize64 > 200) {
			note("deny", name, "size %d (compressed %d) exceeds the cap", f.UncompressedSize64, f.CompressedSize64)
			continue
		}
		rc, err := f.Open()
		must(err)
		b, err := io.ReadAll(io.LimitReader(rc, fileCap+1))
		rc.Close()
		if err != nil {
			note("repair", name, "read error %v; kept %d readable bytes", err, len(b))
		}
		if total += int64(len(b)); total > totalCap {
			note("deny", name, "payload exceeds %d bytes", totalCap)
			break
		}
		switch ext {
		case ".woff2", ".woff", ".ttf", ".otf":
			if err := fontMagic(clean, b); err != nil {
				note("deny", name, "%v", err)
				continue
			}
		case ".css":
			b = repairCSS(name, b, note)
			b = stripCSS(name, b, note)
		case ".html", ".htm":
			b = stripHTML(name, b, note)
		}
		if ext == ".css" || ext == ".html" || ext == ".htm" {
			if k := len(white.FindAll(b, -1)); k > 0 {
				note("warn", name, "%d white value(s); house ground is #000000", k)
			}
		}
		write(filepath.Join(dst, filepath.FromSlash(clean)), b)
		kept++
	}
	report := map[string]any{"payload": filepath.Base(zpath), "kept": kept, "findings": fs}
	write(strings.TrimRight(dst, "/")+".sentinel.json", append(jsonOut(report, true), '\n'))
	deny := 0
	for _, f := range fs {
		fmt.Printf("%-6s %s: %s\n", f.Action, f.File, f.Detail)
		if f.Action == "deny" {
			deny++
		}
	}
	fmt.Printf("ingest: %d kept, %d findings, %d denied\n", kept, len(fs), deny)
	if deny > 0 {
		os.Exit(2)
	}
}

func repairCSS(name string, b []byte, note func(a, f, d string, x ...any)) []byte {
	open, close := braces(string(b))
	if open == close {
		return b
	}
	if close > open {
		note("warn", name, "%d stray closing brace(s)", close-open)
		return b
	}
	s := strings.TrimRight(string(b), " \t\r\n")
	last := s[len(s)-1:]
	tail := ""
	if last != ";" && last != "{" && last != "}" {
		tail = ";"
	}
	note("repair", name, "truncated after %q: closed %d open rule(s)", s[max(0, len(s)-24):], open-close)
	return []byte(s + tail + strings.Repeat("\n}", open-close) + "\n")
}

func stripCSS(name string, b []byte, note func(a, f, d string, x ...any)) []byte {
	return cssImport.ReplaceAllFunc(b, func(m []byte) []byte {
		note("strip", name, "external @import %s", strings.TrimSpace(string(m)))
		return nil
	})
}

func stripHTML(name string, b []byte, note func(a, f, d string, x ...any)) []byte {
	b = linkTag.ReplaceAllFunc(b, func(l []byte) []byte {
		r, h := attrRel.FindSubmatch(l), attrHref.FindSubmatch(l)
		if r != nil && h != nil && loadRel.Match(r[1]) && external(string(h[1])) {
			note("strip", name, "external %s from %s", string(r[1]), originOf(string(h[1])))
			return nil
		}
		return l
	})
	b = scriptSrc.ReplaceAllFunc(b, func(s []byte) []byte {
		note("strip", name, "external script %s", originOf(string(scriptSrc.FindSubmatch(s)[1])))
		return nil
	})
	return regexp.MustCompile(`(?m)^[ \t]+\r?\n`).ReplaceAll(b, nil)
}

var keyShape = regexp.MustCompile(`^[A-Za-z0-9][A-Za-z0-9._/-]*$`)

func gate(args []string) {
	fs := flag.NewFlagSet("gate", flag.ExitOnError)
	dist := fs.String("dist", "dist", "upload root to re-hash")
	must(fs.Parse(args))
	if fs.NArg() != 1 {
		usage()
	}
	var m manifest
	must(json.Unmarshal(read(fs.Arg(0)), &m))
	var deny []string
	no := func(f string, a ...any) { deny = append(deny, fmt.Sprintf(f, a...)) }
	if len(m.Objects) == 0 {
		no("manifest holds no objects")
	}
	keys := map[string]bool{}
	for _, o := range m.Objects {
		k := o.Key
		keys[k] = true
		if !keyShape.MatchString(k) || strings.Contains(k, "..") || strings.Contains(k, "//") {
			no("%s: key shape", k)
		}
		if strings.Contains(k, "__MACOSX") || strings.Contains("/"+k, "/._") || strings.HasSuffix(k, ".DS_Store") {
			no("%s: operating-system metadata", k)
		}
		if want, ok := contentTypes[path.Ext(k)]; !ok || o.ContentType != want {
			no("%s: content type %q", k, o.ContentType)
		}
		if len(o.SHA256) != 64 {
			no("%s: sha256 missing", k)
		}
		font := strings.HasPrefix(k, "assets/fonts/")
		switch {
		case font && (o.Class != "immutable" || o.CacheControl != cacheImmutable):
			no("%s: font objects must be class immutable with %q", k, cacheImmutable)
		case font:
			p := strings.Split(path.Base(k), ".")
			if len(p) < 3 || len(o.SHA256) < 8 || p[len(p)-2] != o.SHA256[:8] {
				no("%s: immutable object without its content hash in the name", k)
			}
		case o.Class != "document" || o.CacheControl != cacheDocument:
			no("%s: documents must be class document with %q", k, cacheDocument)
		}
		if o.Bytes > 1<<20 {
			no("%s: %d bytes exceeds 1 MiB", k, o.Bytes)
		}
		if o.ContentType == contentTypes[".html"] {
			if !strings.Contains(o.CSP, "default-src 'none'") || strings.Contains(o.CSP, "unsafe-") {
				no("%s: CSP must start from default-src 'none' with no unsafe- sources", k)
			}
			for _, x := range o.ExternalOrigins {
				no("%s: loads from third-party origin %s", k, x)
			}
		}
		// zero trust: the manifest's word is not enough; re-hash what will be uploaded
		b, err := os.ReadFile(filepath.Join(*dist, filepath.FromSlash(k)))
		switch {
		case err != nil:
			no("%s: %v", k, err)
		case sum(b) != o.SHA256 || len(b) != o.Bytes:
			no("%s: bytes on disk do not match the manifest", k)
		case font:
			if err := fontMagic(k, b); err != nil {
				no("%v", err)
			}
		case o.ContentType == contentTypes[".html"]:
			doc := string(b)
			if len(externalOrigins(doc)) > 0 || !strings.Contains(doc, o.CSP) {
				no("%s: document differs from its recorded CSP or loads third-party origins", k)
			}
			if bytes.Contains(b, []byte("{{")) {
				no("%s: unfilled template slot", k)
			}
		}
	}
	for _, p := range m.Invalidate {
		if !strings.HasPrefix(p, "/") || strings.ContainsAny(p, "*?") {
			no("invalidate %q: exact paths only", p)
		}
		if strings.HasPrefix(p, "/assets/fonts/") {
			no("invalidate %q: immutable objects are never invalidated", p)
		}
	}
	filepath.WalkDir(*dist, func(p string, d os.DirEntry, err error) error {
		if err == nil && !d.IsDir() {
			rel, _ := filepath.Rel(*dist, p)
			if !keys[filepath.ToSlash(rel)] {
				no("%s: on disk but not in the manifest", filepath.ToSlash(rel))
			}
		}
		return nil
	})
	for _, d := range deny {
		fmt.Println("deny  " + d)
	}
	if len(deny) > 0 {
		fmt.Printf("gate: %d denial(s); nothing ships\n", len(deny))
		os.Exit(1)
	}
	fmt.Printf("[ Moai Rendering Engine // Sentinel gates passed at compile ] %d objects\n", len(m.Objects))
}
