const CACHE_NAME = "mustgo-receipts-v1.1.0";

const ASSETS_TO_CACHE = [
  "./",
  "./index.html",
  "./manifest.json",
  "./assets/styles.css",
  "./assets/app.js",
  "./assets/favicon.svg",
  "./data/claims.js",
  "./data/claims.json",
  "./data/mps.js",
  "./data/mps.json",
  "./data/impunity.js",
  "./data/impunity.json",
  "./data/memorial.js",
  "./data/memorial.json",
  "./data/i18n.js"
];

// Install: Cache core application shell and data
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    }).then(() => self.skipWaiting())
  );
});

// Activate: Cleanup outdated cache versions
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch: Stale-while-revalidate for local assets, cache-first for fonts
self.addEventListener("fetch", (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // Skip non-GET requests or browser extension protocols
  if (req.method !== "GET" || !url.protocol.startsWith("http")) {
    return;
  }

  // Google Fonts caching
  if (url.origin === "https://fonts.googleapis.com" || url.origin === "https://fonts.gstatic.com") {
    event.respondWith(
      caches.open(CACHE_NAME).then((cache) => {
        return cache.match(req).then((cached) => {
          const fetched = fetch(req).then((resp) => {
            if (resp.status === 200) cache.put(req, resp.clone());
            return resp;
          }).catch(() => cached);
          return cached || fetched;
        });
      })
    );
    return;
  }

  // Local static files: Stale-while-revalidate with cache fallback
  event.respondWith(
    caches.match(req).then((cached) => {
      const fetchPromise = fetch(req).then((networkResp) => {
        if (networkResp && networkResp.status === 200 && networkResp.type === "basic") {
          const respClone = networkResp.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(req, respClone);
          });
        }
        return networkResp;
      }).catch((err) => {
        // Network failed; return cached if available
        if (cached) return cached;
        // If navigating to an HTML page while offline, return cached index.html
        if (req.mode === "navigate") {
          return caches.match("./index.html");
        }
        throw err;
      });

      return cached || fetchPromise;
    })
  );
});
