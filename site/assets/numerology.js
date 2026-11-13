import { nameNumbers, dateNumbers, maturityNumber } from './numerology-core.js';
const form = document.querySelector('#number-form');
const nameInput = form.elements.birthName, dateInput = form.elements.birthDate;
const error = document.querySelector('#number-error'), results = document.querySelector('#number-results');
const output = document.querySelector('#number-cards'), status = document.querySelector('#number-status');
const yField = document.querySelector('#y-setting');
const now = new Date();
const today = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
dateInput.max = today;
let report = '';
const patterns = {
  1: ['Initiative', 'The impulse to begin, choose, and make a mark.', 'Independence can become isolation. What can you initiate without carrying everything alone?'],
  2: ['Attunement', 'Sensitivity to relationships, timing, and the space between people.', 'Listening can become self-erasure. Where does cooperation need a boundary?'],
  3: ['Expression', 'The urge to give an inner experience a voice, image, or form.', 'Expression needs a container. What would help an idea become a finished work?'],
  4: ['Structure', 'Attention to foundations, repetition, and the material conditions of making.', 'A structure can also become a cage. Which routine supports you, and which merely persists?'],
  5: ['Movement', 'Curiosity, experimentation, and a willingness to change form.', 'Freedom needs somewhere to land. What can remain steady while the work changes?'],
  6: ['Care', 'Responsibility for people, places, and the conditions that allow work to grow.', 'Care needs limits. What is yours to hold, and what belongs to someone else?'],
  7: ['Inquiry', 'A pull toward close study, solitude, and meaning beneath the surface.', 'Investigation needs contact with life. When is it time to stop studying and test the work?'],
  8: ['Stewardship', 'A concern with resources, agency, and the ability to act at scale.', 'Power needs a purpose. What would enough look like, and who gets to define it?'],
  9: ['Completion', 'Attention to the larger field: endings, contribution, and what the work leaves behind.', 'Contribution does not require depletion. What can you release without abandoning what matters?'],
  11: ['Sensitivity into form', 'An intensified symbolic emphasis on perception, imagination, and translating subtle experience.', 'Attention needs grounding. What helps a strong impression become something usable?'],
  22: ['Vision into structure', 'An intensified symbolic emphasis on bringing a large idea into material form.', 'Scale needs carrying capacity. What is the smallest structure that can hold the vision now?'],
  33: ['Care into practice', 'An intensified symbolic emphasis on teaching, creative service, and shared responsibility.', 'Service needs consent and limits. How can you contribute without becoming indispensable?']
};
const roles = {
  expression: ['Expression / Destiny', 'The material', 'All letters in your birth name. A prompt about the abilities and possibilities you want to develop.'],
  soul: ['Soul Urge', 'The desire', 'Vowels in your birth name. A prompt about what sustains your interest when nobody is watching.'],
  personality: ['Personality', 'The encounter', 'Consonants in your birth name. A prompt about what others may meet first, and what remains beneath that surface.'],
  life: ['Life Path', 'The recurring question', 'Your birth date. A prompt about the themes you return to, rather than a route you must follow.'],
  birthday: ['Birthday', 'The first impulse', 'Your day of birth. A narrower prompt about an instinct or resource you might recognize.'],
  maturity: ['Maturity', 'The integration', 'Expression plus Life Path. A prompt about how possibility and lived experience might come together over time.']
};
function el(tag, text, cls) { const n = document.createElement(tag); if (text !== undefined) n.textContent = text; if (cls) n.className = cls; return n; }
const chain = steps => steps.join(' → ');
function calculation(key, value) {
  if ('letters' in value) {
    if (!value.letters) return key === 'soul' ? 'No vowels under the selected Y rule. No Soul Urge number is assigned.' : 'No consonants under the selected Y rule. No Personality number is assigned.';
    return `Letters: ${value.letters.split('').join(' ')}\nValues: ${value.values.join(' + ')} = ${value.total}\nReduction: ${chain(value.steps)}`;
  }
  if (key === 'life') return `Month: ${chain(value.parts[0].steps)}\nDay: ${chain(value.parts[1].steps)}\nYear: ${chain(value.parts[2].steps)}\nCombine: ${value.parts.map(p=>p.number).join(' + ')} = ${value.total}\nReduction: ${chain(value.steps)}`;
  if (key === 'maturity') return `Combine: ${value.operands.join(' + ')} = ${value.total}\nReduction: ${chain(value.steps)}`;
  return `Reduction: ${chain(value.steps)}`;
}
function renderCard(key, value, index) {
  const [title, label, explanation] = roles[key];
  const card = el('article', undefined, 'number-card');
  card.append(el('p', `${String(index+1).padStart(2,'0')} // ${label}`, 'number-index'));
  const h = el('h3', title); card.append(h);
  const result = value.number === null ? '—' : String(value.number);
  card.append(el('p', result, 'number-value'));
  if (value.number > 9) card.append(el('p', `Master number · underlying ${value.root}`, 'number-root'));
  card.append(el('p', explanation, 'number-explanation'));
  if (value.number !== null) {
    const [theme, reflection, question] = patterns[value.number];
    card.append(el('h4', theme), el('p', reflection), el('p', question, 'number-prompt'));
  }
  const detail = el('details');detail.append(el('summary','Show the calculation'),el('p',calculation(key,value),'number-calculation'));card.append(detail);
  output.append(card);
  return `${title}: ${result}${value.number > 9 ? ' / '+value.root : ''}\n${explanation}\n${value.number !== null ? patterns[value.number].join('\n')+'\n' : ''}${calculation(key,value)}\n`;
}
function updateY() { yField.hidden = !/y/i.test(nameInput.value); }
nameInput.addEventListener('input', updateY);
form.addEventListener('submit', event => {
  event.preventDefault();error.textContent='';status.textContent='';report='';
  nameInput.removeAttribute('aria-invalid');dateInput.removeAttribute('aria-invalid');
  results.hidden=true;output.replaceChildren();
  const name=nameInput.value.trim(), date=dateInput.value;
  if (!name && !date) { error.textContent='Enter a birth name, a birth date, or both.';nameInput.focus();return; }
  let names, dates;
  if (name) { try { names=nameNumbers(name,form.elements.yVowel.checked); } catch(e) { error.textContent=e.message;nameInput.setAttribute('aria-invalid','true');nameInput.focus();return; } }
  if (date) { try { if(date>today)throw new Error('A birth date must be today or earlier.');dates=dateNumbers(date); } catch(e) { error.textContent=e.message;dateInput.setAttribute('aria-invalid','true');dateInput.focus();return; } }
  const readings=[];
  if(names)readings.push(['expression',names.expression],['soul',names.soul],['personality',names.personality]);
  if(dates)readings.push(['life',dates.life],['birthday',dates.birthday]);
  if(names && dates) readings.push(['maturity',maturityNumber(names.expression.number,dates.life.number)]);
  report='WILD-LAKE / NAME & NUMBER\nA symbolic framework for reflection. Numbers are prompts, not verdicts.\n\n';
  if(names)report+=`Birth name: ${name}\nCalculated letters: ${names.normalized}\nY counted as: ${form.elements.yVowel.checked?'vowel':'consonant'}\n`;
  if(dates)report+=`Birth date: ${date}\n`;
  report+='Method: Pythagorean letter values; retain 11, 22, and 33 at each reduction. Life Path reduces month, day, and year separately before combining.\n\n';
  readings.forEach(([key,value],i)=>{report+=renderCard(key,value,i)+'\n';});
  document.querySelector('#number-basis').textContent = names ? `Calculated letters: ${names.normalized}. Y is counted as a ${form.elements.yVowel.checked?'vowel':'consonant'}.` : 'Calculated from your birth date. Add your birth name to explore Expression, Soul Urge, Personality, and Maturity.';
  if(names && !dates)document.querySelector('#number-basis').textContent+=' Add a birth date for Life Path, Birthday, and Maturity.';
  results.hidden=false;status.textContent=`${readings.length} numbers calculated. Your reading is below.`;
  document.querySelector('#reading-heading').focus({preventScroll:true});
  results.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'});
});
form.addEventListener('reset',()=>{results.hidden=true;output.replaceChildren();error.textContent='';status.textContent='';report='';document.querySelector('#reading-notes').value='';nameInput.removeAttribute('aria-invalid');dateInput.removeAttribute('aria-invalid');setTimeout(updateY,0);});
document.querySelector('#download-reading').addEventListener('click',()=>{
  if(!report)return;
  const notes=document.querySelector('#reading-notes').value.trim();
  const url=URL.createObjectURL(new Blob([report+(notes?'\nYOUR NOTES\n'+notes+'\n':'')],{type:'text/plain;charset=utf-8'}));
  const a=el('a');a.href=url;a.download='wild-lake-name-and-number.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
});
updateY();

form.hidden = false;
