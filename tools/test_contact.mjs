import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';
const source=await readFile(new URL('../site/assets/contact.js',import.meta.url),'utf8');
function draft(values){let handler,prevented=false;const status={textContent:''};const window={location:{href:''}};
 const document={getElementById:id=>id==='intake-form'?{addEventListener:(name,callback)=>{assert.equal(name,'submit');handler=callback;}}:status};
 class FormData {constructor(form){assert.equal(form,values);}get(key){return values[key];}}
 vm.runInNewContext(source,{document,window,FormData,encodeURIComponent});handler({preventDefault(){prevented=true;},currentTarget:values});assert(prevented);return {url:window.location.href,status:status.textContent};}
const values={message:'A film & a performance?\nCafé #2',work:'https://example.com/work?artist=a&project=b',name:'A & B'};
const result=draft(values);const url=new URL(result.url);assert.equal(url.protocol,'mailto:');assert.equal(url.pathname,'info@wildlakestudio.com');assert.equal(url.searchParams.get('subject'),'Wild-Lake — Let’s begin');const body=url.searchParams.get('body');for(const [key,value]of Object.entries(values))assert(body.includes(value),key);assert(result.status.includes('Review and send'));assert(!draft({email:'not-requested@example.com'}).url.includes('not-requested'));assert.equal(draft({}).url,'mailto:info@wildlakestudio.com');assert(!draft({message:'Only my message'}).url.includes('undefined'));console.log('Contact email drafts preserve all optional fields, special characters, the fixed recipient, and the empty-form path.');
