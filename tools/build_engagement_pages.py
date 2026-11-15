#!/usr/bin/env python3
"""Deterministic FAQ/Terms renderer using the site's existing shared shell."""
from pathlib import Path
import json,re,html,sys
from sync_navigation import render
repo=Path(__file__).resolve().parents[1];root=repo/'site';content=json.loads((repo/'tools/engagement-pages/content.json').read_text());e=html.escape
source=(root/'practice/index.html').read_text()
header=re.search(r'<header class="site-topbar">.*?</header>',source,re.S)[0]
footer=re.search(r'<footer class="studio-footer".*?</footer>',source,re.S)[0]
head=source[:source.index('</head>')]
head=re.sub(r'<script type="application/ld\+json">.*?</script>','',head,flags=re.S)
# Keep shared metadata, favicon and asset patterns; page data replaces their values.
head=head.replace('<link rel="stylesheet" href="/assets/site.css"/>','<link rel="stylesheet" href="/assets/site.css"/>\n<link rel="stylesheet" href="/assets/manifesto.css"/>')
head=head.replace('<link rel="stylesheet" href="/assets/css/fibonacci.css"/>','<link rel="stylesheet" href="/assets/engagement-documents.css"/>\n<link rel="stylesheet" href="/assets/css/fibonacci.css"/>')
def paras(lines):
 return ''.join('<p class="type-body">'+e(text).replace('Terms of Practice','<a href="/terms">Terms of Practice</a>')+'</p>' for text in lines)
def schema_base(name,data):
 url='https://wildlakestudio.com/'+name
 return {'@context':'https://schema.org','@type':'FAQPage' if name=='faq' else 'WebPage','@id':url+'#webpage','url':url,'name':data['headline'],'description':data['description'],'inLanguage':'en-US','isPartOf':{'@id':'https://wildlakestudio.com/#website'},'publisher':{'@id':'https://wildlakestudio.com/#organization'},'about':[{'@id':'https://wildlakestudio.com/#organization'},{'@id':'https://argelysoriach.com/universe-api/#framework'}],'breadcrumb':{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':'https://wildlakestudio.com/'},{'@type':'ListItem','position':2,'name':'FAQ' if name=='faq' else 'Terms of Practice','item':url}]}}
outputs={}
for name,data in content.items():
 url='https://wildlakestudio.com/'+name;path=root/name/'index.html';h=head
 h=re.sub(r'<title>.*?</title>','<title>'+e(data['title'])+'</title>',h)
 h=re.sub(r'(<link rel="canonical" href=")[^"]+',lambda m:m[1]+url,h)
 for key,value in {'description':data['description'],'title':data['title'],'og:title':data['title'],'twitter:title':data['title'],'og:description':data['description'],'twitter:description':data['description'],'og:url':url}.items():
  h=re.sub(r'(<meta (?:name|property)="'+re.escape(key)+r'" content=")[^"]*',lambda m:m[1]+e(value,quote=True),h)
 schema=schema_base(name,data)
 main='<main class="manifesto-main engagement-document document-'+name+'" id="main"><article><header class="document-heading"><p class="eyebrow type-eyebrow">NEW YORK / TAMPA / SANTIAGO / WORLDWIDE</p><h1 class="type-h1">'+e(data['headline'])+'</h1><p class="type-body">'+e(data['subhead'])+'</p></header>'
 if name=='faq':
  schema['mainEntity']=[];number=0
  for section in data['sections']:
   main+='<section class="document-section" id="'+section['id']+'" aria-labelledby="'+section['id']+'-heading"><h2 class="type-h2" id="'+section['id']+'-heading">'+e(section['heading'])+'</h2>'
   for question in section['questions']:
    number+=1;id='question-'+str(number);answer='answer-'+str(number)
    main+='<section class="faq-item"><h3 class="type-h3"><button type="button" class="faq-toggle" id="'+id+'" data-faq-toggle aria-expanded="true" aria-controls="'+answer+'"><span>'+e(question['question'])+'</span><span aria-hidden="true">+</span></button></h3><div class="faq-answer" id="'+answer+'" role="region" aria-labelledby="'+id+'">'+paras(question['paragraphs'])+'</div></section>'
    schema['mainEntity'].append({'@type':'Question','@id':url+'#'+id,'name':question['question'],'acceptedAnswer':{'@type':'Answer','text':'\n'.join(question['paragraphs'])}})
   main+='</section>'
  main+='<section class="document-section document-cta" id="begin"><h2 class="type-h2">Tell us about the artist or practice.</h2><a class="studio-action" href="/contact/">Begin <span aria-hidden="true">→</span></a><p class="type-body"><a href="/terms">Read the full Terms of Practice <span aria-hidden="true">→</span></a></p></section>'
 else:
  main+=paras([data['preamble']]);schema['hasPart']=[]
  main+='<nav class="document-outline type-body" aria-label="Terms sections">'+''.join('<a href="#'+s['id']+'">'+s['number']+' '+e(s['heading'])+'</a>' for s in data['sections'])+'</nav>'
  aliases={'ownership':['sovereign-ip'],'scope-fees':['engagement','environment'],'conflicts':['jurisdiction']}
  for section in data['sections']:
   id=section['id'];title=section['number']+' — '+section['heading']
   main+='<section class="document-section" id="'+id+'" aria-labelledby="'+id+'-heading">'+''.join('<span id="'+a+'"></span>' for a in aliases.get(id,[]))+'<h2 class="type-h2" id="'+id+'-heading">'+e(title)+'</h2>'+paras(section['paragraphs'])+'</section>'
   schema['hasPart'].append({'@type':'WebPageElement','@id':url+'#'+id,'name':title,'text':'\n'.join(section['paragraphs'])})
  main+='<section class="document-section document-cta" id="begin"><h2 class="type-h2">Questions?</h2><p class="type-body"><a href="/faq">Read the FAQ <span aria-hidden="true">→</span></a></p><a class="studio-action" href="/contact/">Begin an engagement <span aria-hidden="true">→</span></a></section>'
 main+='</article></main>'
 h+='\n<script type="application/ld+json">\n'+json.dumps(schema,ensure_ascii=True,indent=2)+'\n</script>\n</head>'
 page=h+'\n<body class="home contact-page reading-layout">'+header+render(path)+main+'<div class="base"><hr class="rule rule-datum"/>'+footer+'</div><script src="/assets/header-globe.js" defer></script>'+('<script src="/assets/faq.js" defer></script>' if name=='faq' else '')+'</body></html>\n'
 outputs[path]=page;outputs[root/'schema'/f'{name}.json']=json.dumps(schema,ensure_ascii=True,indent=2)+'\n'
for path,text in outputs.items():
 if '--check' in sys.argv:
  if not path.exists() or path.read_text()!=text:raise SystemExit('Stale generated page/schema: '+str(path.relative_to(root)))
 else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
print('Validated FAQ/Terms deterministic output.' if '--check' in sys.argv else 'Built FAQ and Terms from approved verbatim copy and shared shell.')
