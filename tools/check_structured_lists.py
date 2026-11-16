#!/usr/bin/env python3
"""Reject missing or empty structured list elements before publishing."""
from pathlib import Path
from html.parser import HTMLParser
import json
root=Path(__file__).resolve().parents[1]/'site'
class Scripts(HTMLParser):
 def __init__(self):super().__init__();self.active=False;self.parts=[];self.blocks=[]
 def handle_starttag(self,tag,attrs):
  if tag=='script' and dict(attrs).get('type')=='application/ld+json':self.active=True;self.parts=[]
 def handle_data(self,text):
  if self.active:self.parts.append(text)
 def handle_endtag(self,tag):
  if tag=='script' and self.active:self.blocks.append(json.loads(''.join(self.parts)));self.active=False

def inspect(node,location,errors):
 count=0
 if isinstance(node,dict):
  types=node.get('@type',[]);types=types if isinstance(types,list) else [types]
  types={t.rstrip('/').split('/')[-1].split(':')[-1] for t in types if isinstance(t,str)}
  if types & {'ItemList','BreadcrumbList','OfferCatalog'}:
   count+=1;elements=node.get('itemListElement')
   if not isinstance(elements,(list,dict,str)) or not elements:errors.append(location+': missing or empty itemListElement')
   elif isinstance(elements,list) and any(e is None or e=={} or e=='' for e in elements):errors.append(location+': empty itemListElement member')
  for key,value in node.items():count+=inspect(value,location+'/'+key,errors)
 elif isinstance(node,list):
  for i,value in enumerate(node):count+=inspect(value,location+'/'+str(i),errors)
 return count

def main():
 errors=[];count=0
 for path in root.rglob('*'):
  if path.suffix=='.html':
   parser=Scripts();parser.feed(path.read_text());blocks=parser.blocks
  elif path.suffix in ['.json','.jsonld']:blocks=[json.loads(path.read_text())]
  else:continue
  for block in blocks:count+=inspect(block,str(path.relative_to(root)),errors)
 if errors:raise SystemExit('\n'.join(errors))
 # Regression fixtures model GSC's exact critical error, including nested lists.
 for invalid in [{'@type':'BreadcrumbList'},{'@type':'ItemList','itemListElement':[]},{'hasOfferCatalog':{'@type':'OfferCatalog','itemListElement':None}}]:
  rejected=[];inspect(invalid,'fixture',rejected);assert rejected
 accepted=[];inspect({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':'https://wildlakestudio.com/'}]},'fixture',accepted);assert not accepted
 print(f'Validated {count} structured lists across HTML, JSON and JSON-LD; no missing itemListElement fields. Regression fixtures passed.')
if __name__=='__main__':main()
