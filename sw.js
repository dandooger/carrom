// Offline cache for the Carrom app. The page itself comes fresh from the internet when
// possible (so updates arrive right away) and from the cache when offline.
const CACHE = "carrom-1794172759061";
const SHELL = ["./", "index.html", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png", "icons/logo.webp", "icons/logo-mark.webp", "boards/classic.webp", "boards/pro.webp", "boards/champion.webp"];
self.addEventListener("install", (e) => { e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;
  const url = new URL(e.request.url);
  if (url.protocol !== "https:" && url.protocol !== "http:") return;
  const page = url.origin === location.origin && (url.pathname.endsWith("/") || url.pathname.endsWith(".html") || url.pathname.endsWith(".webmanifest"));
  if (page) {
    e.respondWith(fetch(e.request, { cache: "no-store" })
      .then((r) => { const cp = r.clone(); caches.open(CACHE).then((c) => c.put(e.request, cp)); return r; })
      .catch(() => caches.match(e.request)));
    return;
  }
  // fonts, icons and the message-server library: cache first
  e.respondWith(caches.match(e.request).then((hit) => hit || fetch(e.request).then((r) => {
    if (r.ok || r.type === "opaque") { const cp = r.clone(); caches.open(CACHE).then((c) => c.put(e.request, cp)); }
    return r;
  })));
});
