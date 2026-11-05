(() => {
  // [id, name] for all 78 cards, filled in by the engine at compile.
  const DECK = /*DECK*/[];
  const KEY = 'quiet-creek-tarot.v1';
  const cards = [...document.querySelectorAll('.card')];
  const log = document.querySelector('.raw-input');
  const draw = document.querySelector('.draw');
  const out = document.querySelector('.export');
  const calm = matchMedia('(prefers-reduced-motion: reduce)');

  const pick = () => {
    const a = DECK.map((_, i) => i);
    const r = crypto.getRandomValues(new Uint32Array(4));
    for (let i = 0; i < 4; i++) {
      const j = i + (r[i] % (a.length - i));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a.slice(0, 4);
  };
  const fresh = () => ({ at: new Date().toISOString(), spread: pick(), turned: [0, 0, 0, 0], text: '' });
  const valid = (s) =>
    s && typeof s.at === 'string' && typeof s.text === 'string' && Array.isArray(s.past) &&
    Array.isArray(s.turned) && s.turned.length === 4 &&
    Array.isArray(s.spread) && s.spread.length === 4 && new Set(s.spread).size === 4 &&
    s.spread.every((i) => Number.isInteger(i) && i >= 0 && i < DECK.length);

  let st = null;
  try { st = JSON.parse(localStorage.getItem(KEY)); } catch (e) { st = null; }
  if (!valid(st)) st = { ...fresh(), past: [] };
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) { /* private window: the reading lives until the tab closes */ } };

  const paint = () => st.spread.forEach((n, i) => {
    const c = cards[i];
    c.querySelector('.face use').setAttribute('href', '#' + DECK[n][0]);
    c.querySelector('.symbol').textContent = DECK[n][1];
    c.querySelector('.turn').checked = !!st.turned[i];
  });
  const names = (r) => r.spread.map((n) => DECK[n][1]).join(' / ');
  const stamp = (iso) => { const d = new Date(iso), p = (v) => String(v).padStart(2, '0'); return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`; };

  paint();
  log.value = st.text;
  save();

  cards.forEach((c, i) => c.querySelector('.turn').addEventListener('change', (e) => { st.turned[i] = e.target.checked ? 1 : 0; save(); }));
  log.addEventListener('input', () => { st.text = log.value; save(); });

  let busy = false;
  draw.addEventListener('click', () => {
    if (busy) return;
    busy = true;
    if (st.text.trim()) st.past.push({ at: st.at, spread: st.spread, text: st.text });
    st.past = st.past.slice(-610);
    cards.forEach((c) => { c.querySelector('.turn').checked = false; });
    setTimeout(() => {
      Object.assign(st, fresh());
      paint();
      log.value = '';
      save();
      busy = false;
    }, calm.matches ? 0 : 610);
  });

  out.addEventListener('click', () => {
    const all = [...st.past, st].filter((r) => r.text.trim());
    const txt = all.map((r) => `${stamp(r.at)}\n${names(r)}\n\n${r.text.trim()}\n`).join('\n---\n\n');
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([txt], { type: 'text/plain;charset=utf-8' }));
    a.download = 'quiet-creek-tarot-log.txt';
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 0);
  });

  draw.hidden = false;
  out.hidden = false;
})();
