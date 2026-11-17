#!/usr/bin/env python3
"""Check shared primary navigation, exact active routes, and all local link targets."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin,urlsplit,unquote
import re,json
from sync_navigation import render,route
root=Path(__file__).resolve().parents[1]/'site';errors=[];pages={}
class Links(HTMLParser):
 def __init__(self):super().__init__();self.ids=set();self.hrefs=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  if t=='a' and 'href' in a:self.hrefs.append(a['href'])
for p in root.rglob('*.html'):
 s=p.read_text();parser=Links();parser.feed(s);pages[p.resolve()]=parser
 nav=re.findall(r'<nav\b[^>]*class="site-nav".*?</nav>',s,re.S)
 if p==root/'index.html':
  if nav or '/assets/navigation.js' in s:errors.append('Landing page must retain its native anchor navigation')
  continue
 if p==root/'field/index.html':
  if nav or 'href="https://wildlakestudio.com/"' not in s:errors.append('Field must retain its native studio return link')
  continue
 if nav!=[render(p)]:errors.append(f'{p.relative_to(root)}: navigation differs from canonical manifest')
 if p==root/'clients/index.html':
  if s.count('/assets/clients-monolith.css')!=1:errors.append('clients/index.html: compiled navigation bundle missing')
 elif s.count('/assets/navigation.css')!=1:errors.append(f'{p.relative_to(root)}: shared navigation CSS missing or duplicated')
 if '—' in s and p.relative_to(root).as_posix() not in ['faq/index.html','terms/index.html']:errors.append(f'{p.relative_to(root)}: em dash')
count=0
for p,parsed in pages.items():
 base='https://wildlakestudio.com'+route(p)
 for href in parsed.hrefs:
  url=urlsplit(urljoin(base,href))
  if url.scheme not in ['http','https'] or url.hostname not in ['wildlakestudio.com','mirror.wildlakestudio.com']:continue
  target=root/unquote(url.path).lstrip('/')
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'{p.relative_to(root)}: broken path {href}');continue
  if url.fragment and target.suffix=='.html' and unquote(url.fragment) not in pages[target.resolve()].ids:errors.append(f'{p.relative_to(root)}: missing anchor {href}')
  count+=1

journey = {
 'practice/index.html': ('/method/', 'Next: read the method'),
 'method/index.html': ('/pricing/', 'Next: engagements &amp; pricing'),
 'pricing/index.html': ('/contact/#contact-intake', 'Next: begin an engagement'),
}
for filename,(href,label) in journey.items():
 text=(root/filename).read_text()
 if not re.search(r'<a\b[^>]*href="'+re.escape(href)+r'"[^>]*>'+re.escape(label),text):errors.append(f'{filename}: missing forward progression link')
site=json.loads((root/'schema/website.json').read_text())
expected=['https://wildlakestudio.com/#home']+['https://wildlakestudio.com/'+name+'/#webpage' for name in ['practice','method','pricing','contact']]
if [node['@id'] for node in site['hasPart'][:5]]!=expected:errors.append('WebSite consideration journey order differs')

if errors:raise SystemExit('\n'.join(sorted(set(errors))))
print(f'Validated canonical primary navigation and {count} internal links/anchors across {len(pages)} pages.')
