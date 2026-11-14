#!/usr/bin/env python3
"""Extract trusted HTML/schema evidence and enforce the clients deployment gate."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import argparse,json,re,hashlib
repo=Path(__file__).resolve().parents[1];root=repo/'site';path=root/'clients/index.html'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.styles=[];self.scripts=[];self.inline=[];self.mode=None;self.bits=[];self.overrides=0;self.saved=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='article' and 'roster-person' in a.get('class','').split():self.ids.append(a.get('id',''))
  if t=='link' and a.get('rel')=='stylesheet':self.styles.append(a.get('href',''))
  if t=='script':
   if a.get('src'):self.scripts.append(a['src'])
   elif a.get('type')!='application/ld+json':self.mode='script';self.bits=[]
  if 'style' in a:self.overrides+=1
  if any('Clients _ Wild Lake Studio_files' in v for _,v in attrs if v):self.saved.append(t)
 def handle_data(self,t):
  if self.mode:self.bits.append(t)
 def handle_endtag(self,t):
  if t==self.mode:self.inline.append(''.join(self.bits));self.mode=None

def manifest():
 text=path.read_text();page=Page();page.feed(text)
 data=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',text,re.S)[1]);graph=data['@graph'];people=[n for n in graph if n.get('@type')=='Person'];collection=next(n for n in graph if n.get('@type')=='CollectionPage');org=next(n for n in graph if n.get('@id')=='https://wildlakestudio.com/#organization')
 result={'document_sha256':hashlib.sha256(text.encode()).hexdigest(),'css_sha256':hashlib.sha256((root/'assets/clients-monolith.css').read_bytes()).hexdigest(),'article_ids':page.ids,'persons':people,'item_ids':[n['item']['@id'] for n in collection['mainEntity']['itemListElement']],'script_origins':[s for s in page.scripts if urlsplit(s).netloc and urlsplit(s).hostname not in ['wildlakestudio.com','mirror.wildlakestudio.com']],'inline_script_bytes':sum(len(s.encode()) for s in page.inline),'stylesheet_urls':page.styles,'organization':org}
 errors=[];expected={'https://wildlakestudio.com/clients/#'+id for id in page.ids};person_ids=[n['@id'] for n in people]
 if len(page.ids)!=12 or len(set(page.ids))!=12:errors.append('Expected twelve unique roster articles')
 if len(people)!=12 or len(set(person_ids))!=12 or set(person_ids)!=expected:errors.append('Roster/Person identity bijection failed')
 if len(result['item_ids'])!=12 or set(result['item_ids'])!=expected:errors.append('Roster/ItemList identity bijection failed')
 if result['script_origins'] or page.scripts:errors.append('Clients runtime must be inline and first-party')
 if result['inline_script_bytes']>=2048:errors.append('Clients runtime exceeds two KiB')
 if page.styles!=['/assets/clients-monolith.css']:errors.append('Expected one stylesheet')
 if page.overrides or page.saved:errors.append('Inline styles or saved-browser paths remain')
 for n in people:
  if not n.get('image') or not n.get('sameAs'):errors.append('Missing image/sameAs: '+n['name'])
  image=root/urlsplit(n.get('image','')).path.lstrip('/')
  if not image.is_file():errors.append('Missing image file: '+n['name'])
 if org['parentOrganization']['@id']!='https://seveneightythree.com/#organization':errors.append('Parent relationship differs')
 if org['founder']['@id']!='https://wildlakestudio.com/clients/#argelys-oriach':errors.append('Founder does not resolve to roster node')
 if errors:raise SystemExit('\n'.join(errors))
 return result
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--manifest',default='build/clients-policy-input.json');args=parser.parse_args();data=manifest();out=repo/args.manifest;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');print(f'Validated twelve roster/Person/ItemList identities and first-party runtime; wrote {out.relative_to(repo)}.')
