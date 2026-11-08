/* Progressive motion enhancements. Content is visible before and without JS. */
(function () {
  var preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  var running = new Set();
  var selector = '.home .statement-block, .home .vectors-grid .vector-node, .home .who, .home .pitch, .home .contact, .founder-layout, .founder-main > section, .roster-entry, .roster .profile-grid, .roster-closing, .contact-main .intake, .files .file';
  if ('IntersectionObserver' in window && Element.prototype.animate) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        observer.unobserve(entry.target);
        if (preference.matches || entry.target.contains(document.activeElement)) return;
        var animation = entry.target.animate([
          { opacity: 0, transform: 'translateY(8px)' },
          { opacity: 1, transform: 'translateY(0)' }
        ], { duration: 377, easing: 'cubic-bezier(.22,1,.36,1)' });
        running.add(animation);
        animation.finished.then(function () { running.delete(animation); }, function () { running.delete(animation); });
      });
    }, { threshold: 0.08 });
    document.querySelectorAll(selector).forEach(function (element) {
      var bounds = element.getBoundingClientRect();
      // Leave content already in view untouched, including restored scroll positions.
      if (bounds.top < window.innerHeight && bounds.bottom > 0) return;
      observer.observe(element);
    });
  }
  function motionChanged() {
    if (!preference.matches) return;
    running.forEach(function (animation) { animation.cancel(); });
    if (dialog && dialog.open) {
      if (closing) finishClose();
      else card.classList.add('is-open');
    }
  }
  if (preference.addEventListener) preference.addEventListener('change', motionChanged);
  else preference.addListener(motionChanged);

  var previews = document.querySelectorAll('.portrait-preview');
  if (!previews.length || !window.HTMLDialogElement || !HTMLDialogElement.prototype.showModal) return;
  var dialog = document.createElement('dialog');
  dialog.className = 'roster-image-dialog';
  dialog.setAttribute('aria-label', 'Portrait of Argelys Samuel Oriach');
  dialog.innerHTML = '<button type="button" class="roster-image-dialog-close" autofocus>Close portrait</button><div class="portrait-stage"><div class="portrait-frame"><img alt="Portrait of Argelys Samuel Oriach" width="1117" height="1107"/></div></div><p class="roster-image-dialog-caption">Argelys Samuel Oriach · Wild-Lake</p>';
  document.body.appendChild(dialog);
  var card = dialog.querySelector('.portrait-frame');
  var image = dialog.querySelector('img');
  var trigger = null, closeTimer = 0, closing = false;
  function finishClose() {
    clearTimeout(closeTimer);
    card.classList.remove('is-closing');
    if (dialog.open) dialog.close();
    closing = false;
  }
  function close() {
    if (!dialog.open || closing) return;
    closing = true;
    card.classList.remove('is-open');
    if (preference.matches) { finishClose(); return; }
    card.classList.add('is-closing');
    closeTimer = setTimeout(finishClose, 280);
  }
  card.addEventListener('transitionend', function (event) {
    if (event.target === card && event.propertyName === 'opacity' && closing) finishClose();
  });
  previews.forEach(function (preview) {
    preview.setAttribute('aria-haspopup', 'dialog');
    preview.setAttribute('aria-expanded', 'false');
    preview.addEventListener('click', function (event) {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      trigger = preview;
      var thumbnail = preview.querySelector('img');
      var figure = preview.closest('figure');
      var caption = figure && figure.querySelector('figcaption');
      var description = thumbnail ? thumbnail.alt : 'Full-size image';
      dialog.setAttribute('aria-label', description);
      image.alt = description;
      if (thumbnail) {
        image.width = thumbnail.naturalWidth || thumbnail.width;
        image.height = thumbnail.naturalHeight || thumbnail.height;
      }
      dialog.querySelector('.roster-image-dialog-caption').textContent = caption ? caption.textContent : description;
      image.src = preview.href;
      clearTimeout(closeTimer);
      closing = false;
      card.classList.remove('is-open', 'is-closing');
      dialog.showModal();
      trigger.setAttribute('aria-expanded', 'true');
      if (preference.matches) card.classList.add('is-open');
      else requestAnimationFrame(function () { if (dialog.open && !closing) card.classList.add('is-open'); });
    });
  });
  dialog.querySelector('button').addEventListener('click', close);
  dialog.addEventListener('cancel', function (event) { event.preventDefault(); close(); });
  dialog.addEventListener('click', function (event) {
    if (event.target !== dialog) return;
    var bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) close();
  });
  dialog.addEventListener('keydown', function (event) {
    if (event.key !== 'Tab') return;
    var focusable = Array.prototype.slice.call(dialog.querySelectorAll('button, a[href], input, select, textarea, [tabindex="0"]'));
    var first = focusable[0], last = focusable[focusable.length - 1];
    if ((event.shiftKey && document.activeElement === first) || (!event.shiftKey && document.activeElement === last)) {
      event.preventDefault();
      (event.shiftKey ? last : first).focus();
    }
  });
  dialog.addEventListener('close', function () {
    clearTimeout(closeTimer);
    card.classList.remove('is-open', 'is-closing');
    closing = false;
    if (trigger) { trigger.setAttribute('aria-expanded', 'false'); trigger.focus({ preventScroll: true }); }
  });
})();
