#!/usr/bin/env python3
"""Require one generated site menu covering every static page and valid local outlines."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json,re
repo=Path(__file__).resolve().parents[1];root=repo/'site';groups=json.loads((repo/'tools/site-menu.json').read_text())
expected={p.resolve() for p in root.rglob('*.html')};found=[]
for group in groups:
 for _,href in group['pages']:
  path=root/urlsplit(href).path.lstrip('/')
  if path.is_dir():path=path/'index.html'
  found.append(path.resolve())
assert len(found)==len(set(found)) and set(found)==expected,'Site menu must cover every static page exactly once'
for path in expected:
 text=path.read_text();assert text.count('class="site-menu"')==1,path
 assert text.count('class="site-nav-primary"')==1,path
 assert text.count('class="site-menu-panel"')==1,path
 assert 'sovereign A&amp;R practice.<br' not in text,path
 if path.parent.name in ['app','mirror']:
  assert '/assets/navigation.js' not in text,'Native tool menus must not require CSP changes'
  assert "script-src 'self'" not in text,'Keep the existing tool CSP unchanged'
 if 'class="page-outline"' in text:
  assert ('/assets/page-outline.js' in text or path.parent.name=='clients'),path
  for id in re.findall(r'<option value="([^"]+)"',re.search(r'<nav class="page-outline".*?</nav>',text,re.S)[0]):assert f'id="{id}"' in text,(path,id)
print(f'Validated one complete menu for {len(expected)} pages, local section navigation and the unbroken footer paragraph.')
