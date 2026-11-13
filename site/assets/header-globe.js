/* A local, silent globe loop; the still remains for reduced motion or blocked playback. */
(function () {
  const video = document.querySelector('.header-globe video');
  if (!video) return;
  const host = video.parentElement;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  video.muted = true;
  video.addEventListener('playing', () => host.classList.add('is-playing'));
  video.addEventListener('error', () => host.classList.remove('is-playing'));
  function update() {
    if (reduced.matches || document.hidden) {
      video.pause();
      if (reduced.matches) host.classList.remove('is-playing');
      return;
    }
    if (!video.getAttribute('src')) video.src = video.dataset.globeSrc;
    video.play().catch(() => host.classList.remove('is-playing'));
  }
  reduced.addEventListener('change', update);
  document.addEventListener('visibilitychange', update);
  update();
})();
