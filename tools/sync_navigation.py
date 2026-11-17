#!/usr/bin/env python3
"""Generate the shared primary navigation from one reviewed route manifest."""
from pathlib import Path
import re,json,html
from urllib.parse import urlsplit
repo=Path(__file__).resolve().parents[1];root=repo/'site';routes=json.loads((repo/'tools/navigation.json').read_text())
arrow='<svg class="link-arrow" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="square" stroke-linejoin="miter" aria-hidden="true" focusable="false"><path d="M5 19 19 5M5 5h14v14"/></svg>'
def route(path):
 name=path.relative_to(root).as_posix();return '/' if name=='index.html' else '/'+name.removesuffix('index.html')
groups=json.loads((repo/'tools/site-menu.json').read_text())
def render(path):
 current=route(path);out=[]
 for item in routes:
  href=item['href'];extra=' aria-current="page"' if href.rstrip('/')==current.rstrip('/') else ''
  if href=='/tools/' and current in ['/mirror/','/app/','/numerology/']:extra=' aria-current="location"'
  if href=='/magazine/' and current.startswith('/magazine/') and current!='/magazine/':extra=' aria-current="location"'
  if href=='/method/' and current=='/development-protocols/':extra=' aria-current="location"'
  if item['label']=='Begin':out.append('<a href="'+href+'" class="begin-link">Begin '+arrow+'</a>')
  else:out.append('<a href="'+href+'"'+extra+'>'+html.escape(item['label'])+'</a>')
 panel=[]
 for i,group in enumerate(groups):
  links=[]
  for label,href in group['pages']:
   active=' aria-current="page"' if href.rstrip('/')==current.rstrip('/') else ''
   links.append('<li><a href="'+href+'"'+active+'>'+html.escape(label)+'</a></li>')
  panel.append('<div class="site-menu-group" role="group" aria-labelledby="site-menu-group-'+str(i)+'"><p class="type-label" id="site-menu-group-'+str(i)+'">'+html.escape(group['label'])+'</p><ul>'+''.join(links)+'</ul></div>')
 menu='<details class="site-menu"><summary aria-controls="site-menu-panel" aria-label="Site menu"><svg class="site-menu-icon" width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg><span class="site-menu-open-label">Menu</span><span class="site-menu-close-label">Close</span></summary><div class="site-menu-panel" id="site-menu-panel">'+''.join(panel)+'<a class="site-menu-begin" href="mailto:info@wildlakestudio.com">Begin '+arrow+'</a></div></details>'
 nav='<nav aria-label="Primary" class="site-nav">'+menu+'<div class="site-nav-primary">'+''.join(out)+'</div></nav>'
 if current in ['/app/','/mirror/']:nav=re.sub(r'href="(/[^"]*)"',lambda m:'href="https://wildlakestudio.com'+m[1]+'"',nav)
 return nav
def add_outline(path,text):
 # Read class tokens, not an exact class attribute: authored outlines may carry runtime classes.
 def outline_nav(match):
  attrs=re.match(r'<nav\b([^>]*)>',match[0])[1]
  classes=re.search(r"\bclass=([\"'])(.*?)\1",attrs)
  return bool(classes and 'page-outline' in classes[2].split())
 navs=list(re.finditer(r'<nav\b[^>]*>.*?</nav>',text,re.S))
 for match in reversed(navs):
  if outline_nav(match) and re.search(r'data-page-outline=[\"\']generated[\"\']',match[0]):
   text=text[:match.start()]+text[match.end():]
 if any(outline_nav(m) for m in re.finditer(r'<nav\b[^>]*>.*?</nav>',text,re.S)):return text
 if route(path) in ['/app/','/mirror/']:return text
 main=re.search(r'<main\b[^>]*>.*?</main>',text,re.S)
 if not main:return text
 sections=[]
 def heading(m):
  attrs,title=m[1],m[2];label=html.unescape(re.sub('<[^>]+>','',title)).strip();match=re.search(r'\bid="([^\"]+)"',attrs)
  id=match[1] if match else 'section-'+re.sub(r'[^a-z0-9]+','-',label.lower()).strip('-')
  sections.append((id,label))
  return m[0] if match else '<h2'+attrs+' id="'+id+'">'+title+'</h2>'
 updated=''.join(part if part.startswith('<footer') else re.sub(r'<h2([^>]*)>(.*?)</h2>',heading,part,flags=re.S) for part in re.split(r'(<footer\b.*?</footer>)',main[0],flags=re.S))
 if len(sections)<2:return text
 nav='<nav class="page-outline" data-page-outline="generated" aria-label="On this page"><p class="page-outline-title type-eyebrow">On this page</p><label class="page-outline-mobile type-label" for="page-outline-select">On this page</label><select class="page-outline-mobile" id="page-outline-select" aria-label="Current section and jump to section">'+''.join('<option value="'+id+'">'+html.escape(label)+'</option>' for id,label in sections)+'</select><ol>'+''.join('<li><a href="#'+id+'">'+html.escape(label)+'</a></li>' for id,label in sections)+'</ol></nav>'
 return text[:main.start()]+nav+updated+text[main.end():]

if __name__=='__main__':
 for path in root.rglob('*.html'):
  if route(path)=='/field/':continue # Self-contained instrument retains its frame and return link.
  s=path.read_text();nav=render(path)
  if re.search(r'<nav\b[^>]*class="site-nav"',s):s=re.sub(r'<nav\b[^>]*class="site-nav".*?</nav>',lambda m:nav,s,count=1,flags=re.S)
  else:s=re.sub(r'(<body\b[^>]*>)',lambda m:m[1]+'\n'+nav,s,count=1)
  if path != root/'clients/index.html' and '/assets/navigation.css' not in s:s=s.replace('<link rel="stylesheet" href="/assets/css/fibonacci.css"/>','<link rel="stylesheet" href="/assets/navigation.css"/>\n<link rel="stylesheet" href="/assets/css/fibonacci.css"/>')
  s=add_outline(path,s)
  if path==root/'clients/index.html':
   if 'data-site-menu-runtime' not in s:s=s.replace('</body>','<script data-site-menu-runtime>'+ (root/'assets/navigation.js').read_text().strip()+'</script></body>')
  else:
   if route(path) not in ['/app/','/mirror/'] and '/assets/navigation.js' not in s:s=s.replace('</body>','<script src="/assets/navigation.js" defer></script></body>')
   if 'class="page-outline"' in s and '/assets/page-outline.js' not in s:s=s.replace('</body>','<script src="/assets/page-outline.js" defer></script></body>')
  path.write_text(s)
 print('Synchronized primary navigation across all HTML builds.')
