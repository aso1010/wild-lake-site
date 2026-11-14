#!/usr/bin/env python3
"""Extract rule ASTs for fail-closed OPA validation before deployment."""
from html.parser import HTMLParser
from pathlib import Path
import json,subprocess,os
root=Path(__file__).resolve().parents[1]
class AST(HTMLParser):
 def __init__(self):super().__init__();self.nodes=[]
 def handle_starttag(self,tag,attrs):
  if tag=='hr':self.nodes.append({'tag':tag,'attributes':dict(attrs),'line':self.getpos()[0]})
opa=os.environ.get('OPA_BIN','opa')
for path in (root/'site').rglob('*.html'):
 parser=AST();parser.feed(path.read_text());data={'html':{'nodes':parser.nodes}}
 result=subprocess.run([opa,'eval','--fail','--format=raw','--data',str(root/'rules_lint.rego'),'--stdin-input','count(data.moai.sentinel.layout.deny) = 0'],input=json.dumps(data),text=True,capture_output=True)
 if result.returncode:raise SystemExit(str(path)+'\n'+result.stdout+result.stderr)
# Regression fixtures: missing class must deny, each typed rule must pass.
for attrs,expected in [({},False),({'class':'other'},False)]+[({'class':'rule '+n},True) for n in ['rule-datum','rule-measure','rule-inline']]:
 data={'html':{'nodes':[{'tag':'hr','attributes':attrs,'line':1}]}}
 result=subprocess.run([opa,'eval','--fail','--data',str(root/'rules_lint.rego'),'--stdin-input','count(data.moai.sentinel.layout.deny) = 0'],input=json.dumps(data),text=True,capture_output=True)
 assert (result.returncode==0)==expected
print('Validated typed rule ASTs across all HTML builds and five OPA regression fixtures.')
