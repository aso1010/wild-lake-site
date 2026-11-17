#!/usr/bin/env python3
"""Guard the explicitly requested static homepage architecture."""
from pathlib import Path
from html.parser import HTMLParser
import re,json
root=Path(__file__).resolve().parents[1]/'site';text=(root/'index.html').read_text()
class Landing(HTMLParser):
 def __init__(self):super().__init__();self.tags=[];self.comments=[];self.ids=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs);self.tags.append((t,a))
  if 'id' in a:self.ids.append(a['id'])
  assert not any(k.startswith('on') for k in a),'Inline runtime handler'
 def handle_comment(self,c):self.comments.append(c)
p=Landing();p.feed(text);assert len(p.ids)==len(set(p.ids)),'Duplicate IDs'
assert [a['id'] for t,a in p.tags if t=='section']==['overview','work','ledger','proof','begin']
assert sum(t=='h1' for t,_ in p.tags)==1
assert sum(t=='style' for t,_ in p.tags)==1
assert not any(t=='link' and a.get('rel')=='stylesheet' for t,a in p.tags)
assert all(a.get('type')=='application/ld+json' and not a.get('src') for t,a in p.tags if t=='script')
assert not any(t in ['iframe','dialog'] for t,_ in p.tags)
assert '—' not in text
for marker in ['[FORM ENDPOINT]','[PROOF]','[LEDGER FIGURES]']:assert any(marker in c for c in p.comments),marker
inputs=[a for t,a in p.tags if t in ['input','textarea']];assert [a['name'] for a in inputs]==['name','practice','condition','email']
labels={a['for'] for t,a in p.tags if t=='label'};assert all(a['id'] in labels for a in inputs)
form=next(a for t,a in p.tags if t=='form');assert form['action']=='mailto:info@wildlakestudio.com' and form['enctype']=='text/plain'
css=re.search(r'<style>(.*?)</style>',text,re.S)[1]
assert 'max-width:987px' in css
assert 'grid-template-columns:minmax(0,5fr) minmax(0,8fr)' in css
assert 'font-family:Archivo' in css and "font-family:'JetBrains Mono'" in css
assert 'https://' not in css and '@import' not in css
for alias,source in [('li','linkedin'),('ig','instagram'),('fb','facebook')]:assert '/'+alias+' /?utm_source='+source+'&utm_medium=social 302' in (root/'_redirects').read_text()
graph=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',text,re.S)[1])
assert [n['@type'] for n in graph['@graph']]==['Organization','WebPage']
page=graph['@graph'][1];assert page==json.loads((root/'schema/website.json').read_text())['hasPart'][0]
assert page['headline']=='Point zero for starmaking.'
print('Validated static landing order, inline CSS, native mailto intake, owner markers, source aliases and schema parity.')
