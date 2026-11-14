import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';
const source=await readFile(new URL('../site/assets/contact.js',import.meta.url),'utf8');
function draft(values){let handler,prevented=false;const status={textContent:''};const window={location:{href:''}};
 const document={getElementById:id=>id==='intake-form'?{addEventListener:(name,callback)=>{assert.equal(name,'submit');handler=callback;}}:status};
 class FormData {constructor(form){assert.equal(form,values);}get(key){return values[key];}}
 vm.runInNewContext(source,{document,window,FormData,encodeURIComponent});handler({preventDefault(){prevented=true;},currentTarget:values});assert(prevented);return {url:window.location.href,status:status.textContent};}
const values={message:'A film & a performance?\nCafé #2',work:'https://example.com/work?artist=a&project=b',name:'A & B'};
const result=draft(values);const url=new URL(result.url);assert.equal(url.protocol,'mailto:');assert.equal(url.pathname,'info@wildlakestudio.com');assert.equal(url.searchParams.get('subject'),'Wild-Lake: Let’s begin');const body=url.searchParams.get('body');for(const [key,value]of Object.entries(values))assert(body.includes(value),key);assert(result.status.includes('Review and send'));assert(!draft({email:'not-requested@example.com'}).url.includes('not-requested'));assert.equal(draft({}).url,'mailto:info@wildlakestudio.com');assert(!draft({message:'Only my message'}).url.includes('undefined'));console.log('Contact email drafts preserve all optional fields, special characters, the fixed recipient, and the empty-form path.');

for (const format of ['Retainer and intensive', 'Subsidized Stewardship subscription', 'Fixed project commission', 'Institutional advisory']) {
 const selected = new URL(draft({...values,format}).url);
 assert.equal(selected.searchParams.get('subject'), 'Wild-Lake inquiry: ' + format);
 assert(selected.searchParams.get('body').startsWith('Engagement format: ' + format));
 for (const value of Object.values(values)) assert(selected.searchParams.get('body').includes(value));
}
assert.equal(draft({format:''}).url, 'mailto:info@wildlakestudio.com');
assert.equal(draft({format:'unexpected\r\nBcc:someone@example.com'}).url, 'mailto:info@wildlakestudio.com');
assert(!/[—]|--/.test(source));
assert(!/fetch\(|XMLHttpRequest|localStorage|sessionStorage|sendBeacon/.test(source));
console.log('All four optional tracks are encoded into subject and body; blank or invalid tracks preserve direct outreach. No storage or network transport added.');
