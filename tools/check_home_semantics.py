#!/usr/bin/env python3
"""Verify homepage section text, entity links, and commercial list references."""
from pathlib import Path
from html.parser import HTMLParser
import json,re
root=Path(__file__).resolve().parents[1]/'site'
s=(root/'index.html').read_text()
class Copy(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,t):self.parts.append(t)
def copy(markup):
 p=Copy();p.feed(markup);return ' '.join(' '.join(p.parts).split())
blocks=re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S)
assert len(blocks)==1,'Homepage must have one unified graph'
graph=json.loads(blocks[0]);nodes={n['@id']:n for n in graph['@graph']}
base='https://wildlakestudio.com/'
page=nodes[base+'#home']
main=re.search(r'<main\b.*?</main>',s,re.S)[0]
sections=re.findall(r'<section id="([^"]+)"[^>]*>(.*?)</section>',main,re.S)
assert [n['@id'] for n in page['hasPart']]==[base+'#'+id for id,_ in sections]
for node,(_,markup) in zip(page['hasPart'],sections):assert node['text']==copy(markup),'Visible/schema text differs'
assert {'thesis','practice','publications','inquiries'}.issubset({id for id,_ in sections})
assert nodes[base+'#organization']['founder']['@id']=='https://argelysoriach.com/#person'
assert nodes[base+'#organization']['parentOrganization']['@id']=='https://seveneightythree.com/#organization'
items=nodes[base+'#practice-areas']['itemListElement'];assert len(items)==3
for i,item in enumerate(items,1):
 assert item['position']==i
 service=nodes[item['item']['@id']];assert service['@type']=='Service'
 assert service['name']==item['name']
 assert service['provider']['@id']==base+'#organization'
assert '[https://' not in blocks[0],'Markdown URL used in JSON-LD'
print('Validated homepage section/schema parity, three practice Services, list references and principal identities.')
