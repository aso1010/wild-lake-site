#!/usr/bin/env python3
"""Keep crawler-visible page metadata aligned with the studio's publishing pattern."""
from pathlib import Path
from html.parser import HTMLParser
import json, struct
root=Path(__file__).resolve().parents[1]/'site'
home_search_title='Wild Lake Studio | Sovereign A&R & Artist Development'
home_social_title='Wild Lake Studio | Talent Architecture and Artist Development'
home_description='Wild Lake Studio is an independent talent architecture and artist development studio for creators across music, art, writing and film.'
image='https://wildlakestudio.com/assets/social/wild-lake-water-preview.png'
class Head(HTMLParser):
    def __init__(self):super().__init__();self.meta={};self.title='';self.in_title=False;self.canonical=''
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='title':self.in_title=True
        if tag=='meta':self.meta.setdefault(a.get('property',a.get('name','')),[]).append(a.get('content',''))
        if tag=='link' and a.get('rel')=='canonical':self.canonical=a.get('href','')
    def handle_endtag(self,tag):
        if tag=='title':self.in_title=False
    def handle_data(self,text):
        if self.in_title:self.title+=text
errors=[];count=0
for p in root.rglob('*.html'):
    h=Head();h.feed(p.read_text());count+=1
    def require(key,value):
        if h.meta.get(key)!=[value]:errors.append(f'{p.relative_to(root)}: {key} differs or is duplicated')
    if p==root/'index.html':
        if h.title!=home_search_title:errors.append('Homepage title differs')
        require('description',home_description)
    elif not h.title.endswith(' | Wild Lake Studio'):errors.append(f'{p.relative_to(root)}: title pattern differs')
    description=h.meta.get('description',[''])[0]
    if not description:errors.append(f'{p.relative_to(root)}: description missing')
    social_title=home_social_title if p==root/'index.html' else h.title
    for key,value in {'title':h.title,'og:title':social_title,'twitter:title':social_title,'og:description':description,'twitter:description':description,'og:site_name':'Wild-Lake','og:type':'website','twitter:card':'summary','og:image':image,'og:image:secure_url':image,'twitter:image':image,'og:image:type':'image/png','og:image:width':'1200','og:image:height':'630','og:url':'https://wildlakestudio.com' if p==root/'index.html' else h.canonical}.items():require(key,value)
    for key in ['og:image:alt','twitter:image:alt']:
        if len(h.meta.get(key,[]))!=1 or not h.meta[key][0]:errors.append(f'{p.relative_to(root)}: image alt missing or duplicated')
preview=root/'assets/social/wild-lake-water-preview.png'
if struct.unpack('>II',preview.read_bytes()[16:24])!=(1200,630):errors.append('Preview is not 1200 × 630')
org=json.loads((root/'schema/organization.json').read_text())
for key,value in {'@type':'Organization','name':'Wild Lake Studio','alternateName':'Wild-Lake','url':'https://wildlakestudio.com','email':'info@wildlakestudio.com','description':'Independent studio for creators across music, art, writing and film. Talent architecture and artist development.','areaServed':['New York','Tampa','Santiago','Worldwide']}.items():
    if org.get(key)!=value:errors.append(f'Organization {key} differs')
if org.get('founder',{}).get('name')!='Argelys Samuel Oriach':errors.append('Founder name differs')
if 'https://www.instagram.com/wildlake.studio' not in org.get('sameAs',[]):errors.append('Instagram identity differs')
if errors:raise SystemExit('\n'.join(errors))
print(f'Validated titles, descriptions, social tags and water preview across {count} pages, plus organization identity.')
