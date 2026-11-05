#!/usr/bin/env python3
"""Validate published JSON, local asset references, XML and inline CSP hashes."""
from pathlib import Path
from html.parser import HTMLParser
import base64, hashlib, json, re, xml.etree.ElementTree as ET
root = Path(__file__).resolve().parents[1] / 'site'
errors = []
class Page(HTMLParser):
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ('src', 'href'):
            url = a.get(key, '').split('?', 1)[0].split('#', 1)[0]
            if not url.startswith('/') or url.startswith('//'): continue
            target = root / url.lstrip('/')
            if target.is_file() or (target / 'index.html').is_file(): continue
            errors.append(f'{self.path}: missing {url}')
for p in root.rglob('*'):
    if p.suffix in ('.json', '.jsonld', '.webmanifest'):
        try: json.loads(p.read_text())
        except Exception as e: errors.append(f'{p}: {e}')
    if p.suffix == '.xml':
        try: ET.parse(p)
        except Exception as e: errors.append(f'{p}: {e}')
    if p.suffix != '.html': continue
    text = p.read_text()
    page = Page(); page.path = p.relative_to(root); page.feed(text)
    for data in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
        try: json.loads(data)
        except Exception as e: errors.append(f'{p}: {e}')
    if 'Content-Security-Policy' in text:
        for tag, attrs, block in re.findall(r'<(script|style)([^>]*)>(.*?)</(?:script|style)>', text, re.S):
            if tag == 'script' and re.search(r'type=[\"\']application/ld\+json[\"\']', attrs):
                continue  # Structured data is parsed separately; it is not executable JavaScript.
            digest = base64.b64encode(hashlib.sha256(block.encode()).digest()).decode()
            if 'sha256-' + digest not in text: errors.append(f'{p}: stale CSP hash')
if errors: raise SystemExit('\n'.join(errors))
print('Validated published JSON, XML, local assets and inline CSP hashes.')
