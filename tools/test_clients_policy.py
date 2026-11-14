#!/usr/bin/env python3
"""Run healthy and adversarial policy inputs against the real OPA evaluator."""
from pathlib import Path
import json,subprocess,copy,sys
from check_clients import manifest
repo=Path(__file__).resolve().parents[1];opa=sys.argv[1] if len(sys.argv)>1 else 'opa';healthy=manifest()
def allowed(data):
 result=subprocess.run([opa,'eval','--format=json','--stdin-input','--data',str(repo/'policy.rego'),'data.wildlake.clients.allow'],input=json.dumps(data),text=True,capture_output=True,check=True)
 return json.loads(result.stdout)['result'][0]['expressions'][0]['value']
assert allowed(healthy)
mutations=[lambda d:d['article_ids'].pop(),lambda d:d['article_ids'].__setitem__(1,d['article_ids'][0]),lambda d:d['persons'].pop(),lambda d:d['item_ids'].append(d['item_ids'][0]),lambda d:d['script_origins'].append('https://third-party.invalid/beacon.js'),lambda d:d.update(inline_script_bytes=2048),lambda d:d['persons'][0].pop('image'),lambda d:d['persons'][0].update(sameAs=[]),lambda d:d.update(stylesheet_urls=['/assets/site.css','/assets/roster.css']),lambda d:d['organization']['founder'].update({'@id':'https://wrong.invalid/#person'})]
for mutate in mutations:
 data=copy.deepcopy(healthy);mutate(data);assert not allowed(data)
print('OPA policy passed healthy input and rejected ten adversarial identity/runtime fixtures.')
