/* One quiet greeting per section. No hidden content, scroll interception, or layout changes. */
(function () {
  var reduced = matchMedia('(prefers-reduced-motion: reduce)');
  var sections = document.querySelectorAll('.home .pillars,.home .who,.home .pitch,.home .contact');
  if (!('IntersectionObserver' in window)) return;
  var timers = new WeakMap();
  function greet(section) {
    if (reduced.matches || document.hidden || timers.has(section)) return;
    section.classList.remove('seam-awake');
    requestAnimationFrame(function () {
      if (reduced.matches) return;
      section.classList.add('seam-awake');
      timers.set(section, setTimeout(function () { section.classList.remove('seam-awake'); timers.delete(section); }, 1700));
    });
  }
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) { greet(entry.target); observer.unobserve(entry.target); }
    });
  }, {threshold: .15});
  sections.forEach(function (section) {
    observer.observe(section);
    section.addEventListener('pointerdown', function () { greet(section); }, {passive:true});
  });
  reduced.addEventListener('change', function () {
    if (!reduced.matches) return;
    sections.forEach(function (section) { clearTimeout(timers.get(section)); timers.delete(section); section.classList.remove('seam-awake'); });
  });
})();
