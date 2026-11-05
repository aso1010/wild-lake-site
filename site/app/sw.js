// Quiet Creek Tarot service worker. The engine writes VERSION (a hash of every object below)
// and FILES at compile. Everything is precached on install and served from cache, so the app
// opens with no network at all. A new build installs beside the old one and waits until the
// reader taps Update; a reading in progress is never reloaded out from under them.
const VERSION = 'e15689916d1c';
const PREFIX = 'quiet-creek-tarot-';
const CACHE = PREFIX + VERSION;
const FILES = ["./","assets/fonts/Archivo-Variable.c2193589.woff2","assets/fonts/JetBrainsMono-Variable.98f8fe00.woff2","assets/icons/icon-180.8f990ede.png","assets/icons/icon-192.9a065b14.png","assets/icons/icon-512.3295d325.png","manifest.webmanifest"];
const SHELL = new URL('./', self.location).href;

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(FILES.map((f) => new Request(f, { cache: 'reload' })))));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k.startsWith(PREFIX) && k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('message', (e) => {
  if (e.data === 'skip') self.skipWaiting();
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== self.location.origin) return;
  if (req.mode === 'navigate') {
    e.respondWith(caches.open(CACHE).then((c) => c.match(SHELL)).then((hit) => hit || fetch(req)));
    return;
  }
  e.respondWith(caches.open(CACHE).then((c) => c.match(req)).then((hit) => hit || fetch(req)));
});
