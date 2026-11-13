/* Pythagorean arithmetic only. No storage, network calls, or interpretation claims. */
const masters = new Set([11, 22, 33]);
export function reduceNumber(total) {
  if (!Number.isSafeInteger(total) || total < 1) throw new Error('Use a positive whole number.');
  const steps = [total];
  while (total > 9 && !masters.has(total)) {
    total = String(total).split('').reduce((sum, digit) => sum + Number(digit), 0);
    steps.push(total);
  }
  return { number: total, steps, root: total > 9 ? String(total).split('').reduce((a, b) => a + Number(b), 0) : total };
}
export function normalizeName(input) {
  const expanded = input.replace(/æ/gi, 'AE').replace(/œ/gi, 'OE').replace(/ß/g, 'SS').replace(/[øØ]/g, 'O').replace(/[łŁ]/g, 'L').replace(/[ðÐ]/g, 'D').replace(/[þÞ]/g, 'TH').replace(/[ıİ]/g, 'I');
  const normalized = expanded.normalize('NFD').replace(/\p{M}/gu, '').toUpperCase();
  if (/[^A-Z\s.'’‘ʼ\-‐‑–—]/u.test(normalized)) throw new Error('This tool uses the Latin A–Z alphabet. Enter a Latin transliteration for other scripts; spaces, apostrophes, periods, and hyphens are ignored.');
  const letters = normalized.replace(/[^A-Z]/g, '');
  if (!letters.length) throw new Error('Enter a name containing letters.');
  return letters;
}
function summarize(letters) {
  const values = letters.split('').map(letter => (letter.charCodeAt(0) - 65) % 9 + 1);
  const total = values.reduce((a, b) => a + b, 0);
  return { letters, values, total, ...(total ? reduceNumber(total) : { number: null, steps: [], root: null }) };
}
export function nameNumbers(input, yIsVowel = false) {
  const letters = normalizeName(input);
  const vowels = yIsVowel ? 'AEIOUY' : 'AEIOU';
  return {
    normalized: letters,
    expression: summarize(letters),
    soul: summarize([...letters].filter(l => vowels.includes(l)).join('')),
    personality: summarize([...letters].filter(l => !vowels.includes(l)).join(''))
  };
}
export function dateNumbers(value) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) throw new Error('Enter a complete birth date.');
  const [year, month, day] = value.split('-').map(Number);
  const leap = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
  const days = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  if (year < 1 || month < 1 || month > 12 || day < 1 || day > days[month - 1]) throw new Error('Enter a valid calendar date.');
  const parts = [reduceNumber(month), reduceNumber(day), reduceNumber(year)];
  const total = parts.reduce((sum, part) => sum + part.number, 0);
  return { life: { ...reduceNumber(total), total, parts }, birthday: { ...reduceNumber(day), total: day } };
}
export function maturityNumber(expression, life) { return { ...reduceNumber(expression + life), total: expression + life, operands: [expression, life] }; }
