#!/usr/bin/env python3
"""Enforce self-hosted executable assets, styles and fonts using only the stdlib.
"""
from html.parser import HTMLParser
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1] / 'site'
errors = []
class Assets(HTMLParser):
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        url = ''
        if tag in ('script', 'iframe'): url = a.get('src', '')
        if tag == 'link' and set(a.get('rel', '').split()) & {'stylesheet', 'preload', 'modulepreload', 'preconnect', 'dns-prefetch'}:
            url = a.get('href', '')
        if re.match(r'(?:https?:)?//', url): errors.append(f'{self.path}: remote runtime resource {url}')
for p in root.rglob('*.html'):
    parser = Assets(); parser.path = p.relative_to(root); parser.feed(p.read_text())
for p in root.rglob('*.css'):
    css = p.read_text()
    if re.search(r'@import\b', css): errors.append(f'{p.relative_to(root)}: CSS import')
    if re.search(r'url\(\s*[\"\']?(?:https?:)?//', css): errors.append(f'{p.relative_to(root)}: remote CSS resource')
if errors: raise SystemExit('\n'.join(errors))
print('Validated self-hosted runtime assets, styles and fonts; no remote initial embeds.')
