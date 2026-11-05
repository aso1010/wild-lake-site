/* Load Spotify only after the visitor opens the listening room. */
(function () {
  var player = document.querySelector('.lake-listener');
  if (!player) return;
  var summary = player.querySelector('summary');
  var slot = player.querySelector('.listen-embed');
  player.addEventListener('toggle', function () {
    if (!player.open || slot.querySelector('iframe')) return;
    var frame = document.createElement('iframe');
    frame.title = 'Listen to the lake — Spotify playlist curated by Argelys Samuel Oriach';
    frame.src = 'https://open.spotify.com/embed/playlist/0JnQHXOviA4z31q0G6bh7x?utm_source=generator&theme=0';
    frame.allow = 'autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture';
    frame.allowFullscreen = true;
    slot.appendChild(frame);
  });
  player.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && player.open) {
      player.open = false;
      summary.focus({preventScroll:true});
    }
  });
})();
