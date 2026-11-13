import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
const source = await readFile(new URL('../site/assets/numerology-core.js', import.meta.url), 'utf8');
const { reduceNumber, normalizeName, nameNumbers, dateNumbers, maturityNumber } = await import('data:text/javascript;base64,'+Buffer.from(source).toString('base64'));
assert.deepEqual(reduceNumber(86), {number:5,steps:[86,14,5],root:5});
assert.deepEqual(reduceNumber(38), {number:11,steps:[38,11],root:2});
for (const master of [11,22,33]) assert.equal(reduceNumber(master).number,master);
assert.equal(reduceNumber(44).number,8);
assert.throws(()=>reduceNumber(0));assert.throws(()=>reduceNumber(NaN));
const birthName='Argelys Samuel Oriach';
const withY=nameNumbers(birthName,true), withoutY=nameNumbers(birthName,false);
assert.deepEqual([withY.expression.total,withY.expression.number,withY.soul.total,withY.soul.number,withY.personality.total,withY.personality.number],[86,5,38,11,48,3]);
assert.deepEqual([withoutY.expression.number,withoutY.soul.number,withoutY.personality.number],[5,4,1]);
assert.equal(withY.soul.total+withY.personality.total,withY.expression.total);
for (const input of ['Zoë García','Anne-Marie O’Neill','Björk','Łukasz','Ægir','Straße']) {
 const n=nameNumbers(input);assert.equal(n.soul.total+n.personality.total,n.expression.total);
}
assert.equal(normalizeName('Zoë García'),'ZOEGARCIA');
assert.equal(normalizeName('Æ Œ ß Ø Ł Þ'),'AEOESSOLTH');
assert.equal(nameNumbers('BC').soul.number,null);
assert.equal(nameNumbers('AE').personality.number,null);
assert.throws(()=>nameNumbers('---'));assert.throws(()=>nameNumbers('张伟'));assert.throws(()=>nameNumbers('<script>'));
// Verify every alphabet mapping, including the shorter final row.
const letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ';
for(let i=0;i<letters.length;i++)assert.equal(nameNumbers(letters[i]).expression.total,i%9+1);
const date=dateNumbers('1990-01-01');assert.equal(date.life.number,3);assert.equal(date.birthday.number,1);
assert.equal(dateNumbers('2000-02-29').life.number,6);
assert.equal(dateNumbers('2000-02-29').birthday.number,11);
assert.equal(dateNumbers('2009-11-11').life.number,33);
assert.equal(dateNumbers('2000-01-22').birthday.number,22);
for(const invalid of ['1900-02-29','2024-02-30','2020-13-01','2020-00-01','2020-01-00','0000-01-01','2020-1-1','not-a-date'])assert.throws(()=>dateNumbers(invalid));
assert.equal(maturityNumber(5,3).number,8);assert.deepEqual(maturityNumber(5,3).operands,[5,3]);assert.equal(maturityNumber(11,11).number,22);
console.log('Numerology arithmetic passed: reference totals, Y partition, full alphabet, Unicode normalization, missing letter groups, master numbers, leap years, invalid input, and Maturity.');
