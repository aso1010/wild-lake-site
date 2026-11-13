#!/usr/bin/env python3
"""Check canonical structured identities and published schema previews agree."""
from pathlib import Path
import html, json, re
root = Path(__file__).resolve().parents[1] / 'site'
canonical = {}
for name in ['organization.json', 'person.json', 'talent-architect.json', 'website.json', 'method.json', 'development-protocols.json', 'practice.json', 'clients.json', 'numerology.json', 'contact.json', 'pricing.json']:
    data = json.loads((root / 'schema' / name).read_text())
    for node in data.get('@graph', [data]):
        if '@id' in node: canonical[node['@id']] = {k:v for k,v in node.items() if k != '@context'}
errors = []
def check(node, path):
    if isinstance(node, dict):
        key = node.get('@id')
        if key in canonical and node.get('@type') and ('description' in node or 'url' in node or 'jobTitle' in node):
            actual = {k:v for k,v in node.items() if k != '@context'}
            if actual != canonical[key]: errors.append(f'{path}: stale entity {key}')
            return
        for value in node.values(): check(value, path)
    elif isinstance(node, list):
        for value in node: check(value, path)
for path in root.rglob('*.html'):
    for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', path.read_text(), re.S):
        check(json.loads(match[1]), path.relative_to(root))
page = root / 'schema' / 'index.html'
for match in re.finditer(r'<pre\b[^>]*data-src="([^"]+)"[^>]*><code>(.*?)</code></pre>', page.read_text(), re.S):
    if html.unescape(match[2]) != (page.parent / match[1]).read_text(): errors.append(f'Stale schema preview: {match[1]}')
if errors: raise SystemExit('\n'.join(errors))
print('Validated canonical structured copy and schema document previews.')
