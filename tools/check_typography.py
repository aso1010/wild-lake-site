#!/usr/bin/env python3
"""Verify the canonical type source, document outline, and token-only declarations."""
from pathlib import Path
from html.parser import HTMLParser
import re,json
root=Path(__file__).resolve().parents[1]/'site'
canonical='/assets/css/fibonacci.css'
errors=[]
class Audit(HTMLParser):
 def __init__(self):super().__init__();self.headings=[];self.styles=[];self.block=None;self.copy=[];self.in_footer=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='footer':self.in_footer=True
  if tag in ('script','style','pre'):self.block=tag
  if re.fullmatch(r'h[1-6]',tag):self.headings.append((int(tag[1]),a.get('class','').split(),self.in_footer))
  if tag=='link' and a.get('rel')=='stylesheet':self.styles.append(a.get('href'))
 def handle_endtag(self,tag):
  if tag==self.block:self.block=None
  if tag=='footer':self.in_footer=False
 def handle_data(self,text):
  if not self.block:self.copy.append(text)
for path in root.rglob('*.html'):
 text=path.read_text()
 if path==root/'field/index.html':
  # Explicit instrument requirement: preserve embedded variable fonts, dynamic typography, and -- resting datum.
  if '—' in text:errors.append('field/index.html: em dash')
  continue # tools/check_field.py validates its separate, supplied type system.
 a=Audit();a.feed(text);name=str(path.relative_to(root))
 if sum(n==1 for n,_,_ in a.headings)!=1:errors.append(f'{name}: expected exactly one H1')
 previous=0
 for n,classes,in_footer in a.headings:
  if n>previous+1:errors.append(f'{name}: skipped H{previous} to H{n}')
  role='type-label' if in_footer and n==2 else 'type-display' if path==root/'index.html' and n==1 else f'type-h{n}'
  if role not in classes:errors.append(f'{name}: missing {role}')
  previous=n
 expected='/assets/clients-monolith.css' if name=='clients/index.html' else canonical
 if path!=root/'index.html' and (not a.styles or a.styles[-1]!=expected or a.styles.count(expected)!=1):errors.append(f'{name}: canonical type sheet or compiled bundle must load once, last')
 if (('—' in text and name not in ['faq/index.html','terms/index.html']) or '--' in ''.join(a.copy)):errors.append(f'{name}: banned punctuation in copy')
 for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text,re.S):
  if '—' in json.dumps(json.loads(block),ensure_ascii=False) and name not in ['faq/index.html','terms/index.html']:errors.append(f'{name}: em dash in JSON-LD')
 styles=re.findall(r'<style[^>]*>(.*?)</style>',text,re.S)
 for style in styles:
  for prop,value in re.findall(r'(?<![-\w])(font-size|line-height|letter-spacing)\s*:\s*([^;{}]+)',style):
   if not re.match(r'(?:var\(|inherit|initial|unset|normal|revert)',value.strip()):errors.append(f'{name}: literal inline {prop}')
for path in root.rglob('*.css'):
 text=path.read_text()
 if '—' in text:errors.append(f'{path.name}: em dash')
 for comment in re.findall(r'/\*.*?\*/',text,re.S):
  if '--' in comment:errors.append(f'{path.name}: double hyphen in comment')
 for prop,value in re.findall(r'(?<![-\w])(font-size|line-height|letter-spacing)\s*:\s*([^;{}]+)',text):
  if not re.match(r'(?:var\(|inherit|initial|unset|normal|revert)',value.strip()):errors.append(f'{path.name}: literal {prop}')
 if path not in [root/'assets/css/fibonacci.css',root/'assets/clients-monolith.css'] and re.search(r'--(?:text-(?:caption|xs|sm|base|md|lg|xl|2xl|3xl)|leading-[\w-]+|tracking-[\w-]+|font-(?:sans|mono)|body-size|lead-size)\s*:',text):errors.append(f'{path.name}: competing type token definition')
css=(root/'assets/css/fibonacci.css').read_text()
for token in ['caption','xs','sm','base','md','lg','xl','2xl','3xl']:
 if len(re.findall(r'--text-'+token+r'\s*:',css))!=1:errors.append(f'Duplicated or absent {token} scale')
if errors:raise SystemExit('\n'.join(errors))
print('Validated one canonical typography source, token-only declarations, heading ladders, and copy punctuation across all HTML pages.')
