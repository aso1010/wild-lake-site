#!/usr/bin/env python3
"""Verify approved copy, FAQ/schema parity, anchors and zero-dependency delivery."""
from pathlib import Path
from html.parser import HTMLParser
import json,re,subprocess,sys,os
repo=Path(__file__).resolve().parents[1];root=repo/'site';data=json.loads((repo/'tools/engagement-pages/content.json').read_text())
subprocess.run([sys.executable,str(repo/'tools/build_engagement_pages.py'),'--check'],check=True)
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.toggles=[];self.remote=[];self.links=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if 'data-faq-toggle' in a:self.toggles.append(a)
  if t=='a':self.links.append(a.get('href',''))
  if t in ['script','iframe'] and re.match(r'^(https?:)?//',a.get('src','')):self.remote.append(a['src'])
manifest={'pages':[]}
for name in ['faq','terms']:
 text=(root/name/'index.html').read_text();p=Page();p.feed(text);schema=json.loads((root/f'schema/{name}.json').read_text())
 assert len(p.ids)==len(set(p.ids)),name+' duplicate IDs'
 assert not p.remote,name+' remote executable origin'
 assert 'https://argelysoriach.com/universe-api/#framework' in json.dumps(schema)
 assert schema['publisher']['@id']=='https://wildlakestudio.com/#organization'
 assert '/faq' in p.links and '/terms' in p.links
 if name=='faq':
  questions=[q for s in data[name]['sections'] for q in s['questions']]
  assert len(p.toggles)==len(questions)==14
  for q,node,button in zip(questions,schema['mainEntity'],p.toggles):
   assert node['name']==q['question'] and node['acceptedAnswer']['text']=='\n'.join(q['paragraphs'])
   assert button.get('type')=='button' and button['aria-controls'] in p.ids and button['aria-expanded']=='true'
 else:
  assert len(schema['hasPart'])==9
  for section,node in zip(data[name]['sections'],schema['hasPart']):
   assert section['id'] in p.ids
   assert node['text']=='\n'.join(section['paragraphs'])
  for legacy in ['sovereign-ip','engagement','confidentiality','environment','jurisdiction']:assert legacy in p.ids
 manifest['pages'].append({'route':'/'+name,'question_count':len(p.toggles),'section_count':len(schema.get('hasPart',[])),'remote_origins':p.remote,'unique_ids':len(p.ids)==len(set(p.ids)),'canonical':schema['url']})
script=(root/'assets/faq.js').read_text();assert len(script.encode())<1024
assert not re.search(r'localStorage|sessionStorage|document\.cookie|fetch\(',script)
manifest['faq_script_bytes']=len(script.encode())
out=repo/'build/engagement-pages-input.json';out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(manifest,indent=2)+'\n')
opa=os.environ.get('OPA_BIN','opa')
def allowed(value):
 result=subprocess.run([opa,'eval','--format=json','--data',str(repo/'engagement_pages.rego'),'--stdin-input','data.moai.engagements.allow'],input=json.dumps(value),text=True,capture_output=True,check=True)
 return json.loads(result.stdout)['result'][0]['expressions'][0]['value']
assert allowed(manifest)
for mutate in [lambda m:m['pages'][0].update(question_count=13),lambda m:m['pages'][1].update(section_count=8),lambda m:m['pages'][0]['remote_origins'].append('https://tracker.invalid'),lambda m:m.update(faq_script_bytes=1024),lambda m:m['pages'][0].update(unique_ids=False)]:
 fixture=json.loads(json.dumps(manifest));mutate(fixture);assert not allowed(fixture)
print('Validated 14 FAQ/schema pairs, nine Terms sections, accessible controls, local runtime and five OPA rejection fixtures.')
