#!/usr/bin/env python3
"""Validate the supplied instrument's independent typography and deterministic graph."""
from pathlib import Path
from html.parser import HTMLParser
import re,json,hashlib,base64
root=Path(__file__).resolve().parents[1]/'site';text=(root/'field/index.html').read_text()
assert '—' not in text,'Em dashes are prohibited throughout the instrument'
class Structure(HTMLParser):
 def __init__(self):super().__init__();self.head=False;self.body=False;self.heads=0;self.bodies=0;self.h1=0;self.styles=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='head':self.head=True;self.heads+=1
  if tag=='body':self.body=True;self.bodies+=1
  if tag in ['title','meta','link','style'] or tag=='script' and a.get('type')=='application/ld+json':assert self.head and not self.body,(tag,'must be in head')
  if tag=='style':self.styles+=1
  if tag=='h1':self.h1+=1
  if tag=='script':assert not a.get('src'),'Instrument must be self-contained'
 def handle_endtag(self,tag):
  if tag=='head':self.head=False
  if tag=='body':self.body=False
p=Structure();p.feed(text);assert (p.heads,p.bodies,p.h1,p.styles)==(1,1,1,1)
assert 'color-scheme:light' not in text and 'background:#fff' not in text
assert 'grid-template-columns:1fr 1fr 2fr 3fr 5fr 8fr' in text
for constant in ['const HAND_W = 1.1;','const P_CLENCHED = 4.0;','const P_RESONANT = 6.25;','const RELEASE = 9;','prefers-reduced-motion: reduce',"put(out.breath, '--')",'id="o-breath">--</span>','class="lung"','href="https://wildlakestudio.com/">Wild-Lake</a>']:assert constant in text,constant
fonts=[hashlib.sha256(base64.b64decode(x.split(',',1)[1])).hexdigest() for x in re.findall(r'url\((data:[^)]+)\)',text)]
assert fonts==['3795b924bdce25b5ec5b2f10b21aeebd14b3f35dcbadf24baf4ca51c4ddcb887','f16937c9fe20752fff8dd5409dbaf50530dec5e35fedfd3f88c8765602f78fdb'],'Supplied embedded font payloads changed'
graph=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',text,re.S)[1]);assert graph==json.loads((root/'schema/field.json').read_text())
nodes={n['@id']:n for n in graph['@graph']};app=nodes['https://wildlakestudio.com/field/#app'];page=nodes['https://wildlakestudio.com/field/#webpage']
assert app['applicationCategory']=='Somatic Instrument'
assert app['name']=='Come Home to Your Body'
assert page['mainEntity']['@id']==app['@id']
assert app['publisher']==app['creator']=={'@id':'https://wildlakestudio.com/#organization'}
assert app['author']=={'@id':'https://argelysoriach.com/#person'}
assert 'https://wildlakestudio.com/field/' in (root/'sitemap.xml').read_text()
assert 'https://wildlakestudio.com/field/#app' in (root/'llms.txt').read_text()
assert 'href="/field/"' in (root/'tools/index.html').read_text()
assert '/somatic/ /field/ 301' in (root/'_redirects').read_text()
print('Validated field document structure, exact embedded fonts, breath constants, punctuation and canonical graph.')
