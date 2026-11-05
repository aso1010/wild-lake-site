/* A settled masthead with a shallow, slow water ripple. */
(function () {
  const svg = document.querySelector('.quiet-creek-monolith svg');
  if (!svg || !window.requestAnimationFrame) return;
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const letters = Array.from(svg.querySelectorAll('use')).map((node, i) => ({
    node, x: Number(node.dataset.x), y: Number(node.dataset.y),
    scale: Number(node.dataset.s), phase: i * 0.53
  }));
  let frameId = null;
  let origin = null;
  function rest() {
    letters.forEach(l => l.node.setAttribute('transform',
      `translate(${l.x} ${l.y}) scale(${l.scale})`));
  }
  function frame(now) {
    if (origin === null) origin = now;
    const t = (now - origin) / 1000;
    const fade = Math.min(t / 4, 1);
    letters.forEach(l => {
      const wave = t * Math.PI * 2 / 14 + l.phase;
      const x = Math.sin(wave * 0.7) * 0.45 * fade;
      const y = Math.sin(wave) * 1.15 * fade;
      const angle = Math.sin(wave * 0.8) * 0.18 * fade;
      l.node.setAttribute('transform',
        `translate(${(l.x + x).toFixed(3)} ${(l.y + y).toFixed(3)}) rotate(${angle.toFixed(3)}) scale(${l.scale})`);
    });
    frameId = requestAnimationFrame(frame);
  }
  function sync() {
    if (frameId !== null) cancelAnimationFrame(frameId);
    frameId = null;
    origin = null;
    rest();
    if (!motion.matches && !document.hidden) frameId = requestAnimationFrame(frame);
  }
  motion.addEventListener('change', sync);
  document.addEventListener('visibilitychange', sync);
  sync();
})();
