// Minimal service worker: cache the app shell + tradebook CSVs for offline use.
// Lets the PWA install prompt appear and gives offline access to the last-loaded view.
const CACHE = "rimali-pf-v1";
const SHELL = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icon.svg",
  "./tradebooks/tradebook-JWT515-EQ.csv",
  "./tradebooks/tradebook-JWT515-EQ-1.csv",
  "./tradebooks/tradebook-JWT515-EQ-2.csv",
  "./tradebooks/tradebook-JWT515-EQ-3.csv",
  "./tradebooks/tradebook-JWT515-EQ-4.csv"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) =>
      Promise.all(SHELL.map((u) => cache.add(u).catch(() => null)))
    )
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  // Always go to network for the price feed (Google Sheets CSV).
  if (url.hostname === "docs.google.com") return;
  // App shell + CSVs: cache first, fall back to network.
  if (event.request.method === "GET" && url.origin === self.location.origin) {
    event.respondWith(
      caches.match(event.request).then((cached) =>
        cached ||
        fetch(event.request)
          .then((res) => {
            const copy = res.clone();
            caches.open(CACHE).then((c) => c.put(event.request, copy));
            return res;
          })
          .catch(() => cached)
      )
    );
  }
});
