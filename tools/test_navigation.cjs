/* Reuse the page harness while checking the shared navigation at four widths. */
const fs=require('node:fs');
let source=fs.readFileSync(require('node:path').join(__dirname,'test_typography.cjs'),'utf8');
source=source.replace('[390,1440]','[320,390,768,1440]');
source=source.replace('const errors=[];const headings=',"const errors=[];const nav=document.querySelector('.site-nav');const frame=nav.getBoundingClientRect();for(const a of nav.querySelectorAll('a')){const r=a.getBoundingClientRect();if(r.left<frame.left-1||r.right>frame.right+1||r.height<43)errors.push('Navigation clipping or undersized target: '+a.textContent)}if(nav.querySelectorAll('a').length!==10)errors.push('Navigation count');const headings=");
eval(source);
