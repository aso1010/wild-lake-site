#!/usr/bin/env python3
"""Generate the shared primary navigation from one reviewed route manifest."""
from pathlib import Path
import re,json,html
repo=Path(__file__).resolve().parents[1];root=repo/'site';routes=json.loads((repo/'tools/navigation.json').read_text())
arrow='<svg class="link-arrow" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="square" stroke-linejoin="miter" aria-hidden="true" focusable="false"><path d="M5 19 19 5M5 5h14v14"/></svg>'
def route(path):
 name=path.relative_to(root).as_posix();return '/' if name=='index.html' else '/'+name.removesuffix('index.html')
def render(path):
 current=route(path);out=[]
 for item in routes:
  href=item['href'];extra=' aria-current="page"' if href==current else ''
  if href=='/tools/' and current in ['/mirror/','/app/','/numerology/']:extra=' aria-current="location"'
  if href=='/magazine/' and current.startswith('/magazine/') and current!='/magazine/':extra=' aria-current="location"'
  if href=='/method/' and current=='/development-protocols/':extra=' aria-current="location"'
  if item['label']=='Begin':out.append('<a href="'+href+'" class="begin-link">Begin '+arrow+'</a>')
  else:out.append('<a href="'+href+'"'+extra+'>'+html.escape(item['label'])+'</a>')
 return '<nav aria-label="Primary" class="site-nav">'+''.join(out)+'</nav>'
if __name__=='__main__':
 for path in root.rglob('*.html'):
  s=path.read_text();nav=render(path)
  if re.search(r'<nav\b[^>]*class="site-nav"',s):s=re.sub(r'<nav\b[^>]*class="site-nav".*?</nav>',lambda m:nav,s,count=1,flags=re.S)
  else:s=re.sub(r'(<body\b[^>]*>)',lambda m:m[1]+'\n'+nav,s,count=1)
  if '/assets/navigation.css' not in s:s=s.replace('<link rel="stylesheet" href="/assets/css/fibonacci.css"/>','<link rel="stylesheet" href="/assets/navigation.css"/>\n<link rel="stylesheet" href="/assets/css/fibonacci.css"/>')
  path.write_text(s)
 print('Synchronized primary navigation across 20 HTML pages.')
