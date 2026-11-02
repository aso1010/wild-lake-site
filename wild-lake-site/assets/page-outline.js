(function () {
  var outline = document.querySelector('.page-outline');
  if (!outline) return;
  var links = Array.prototype.slice.call(outline.querySelectorAll('ol a'));
  var select = outline.querySelector('select');
  var targets = links.map(function (link) { return document.getElementById(link.hash.slice(1)); });
  if (targets.some(function (target) { return !target; })) return;
  outline.classList.add('is-enhanced');
  var wide = window.matchMedia('(min-width: 1440px)');
  var pending = false;
  function update() {
    pending = false;
    var marker = wide.matches ? 144 : outline.getBoundingClientRect().height + 34;
    var active = 0;
    targets.forEach(function (target, index) {
      var margin = parseFloat(getComputedStyle(target).scrollMarginTop) || 0;
      if (target.getBoundingClientRect().top <= marker + margin) active = index;
    });
    // Short final sections still register when the reader reaches the page bottom.
    if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 4) active = targets.length - 1;
    links.forEach(function (link, index) {
      if (index === active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    select.value = targets[active].id;
    var footer = document.querySelector('.base');
    outline.classList.toggle('is-in-reading-area', targets[0].getBoundingClientRect().top <= 180 && (!footer || footer.getBoundingClientRect().top > 180));
    document.documentElement.style.setProperty('--outline-offset', wide.matches ? '34px' : Math.ceil(outline.getBoundingClientRect().height + 21) + 'px');
  }
  function schedule() {
    if (!pending) { pending = true; requestAnimationFrame(update); }
  }
  select.addEventListener('change', function () {
    var target = document.getElementById(select.value);
    window.location.hash = target.id;
    target.setAttribute('tabindex', '-1');
    target.focus({ preventScroll: true });
    schedule();
  });
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule);
  window.addEventListener('hashchange', schedule);
  window.addEventListener('load', schedule);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(schedule);
  update();
})();
