//This is the service worker with the Advanced caching

const CACHE = "pwabuilder-adv-cache";
const precacheFiles = [
  /* Add an array of files to precache for your app */
  "https://sayakb.com/site.webmanifest",
  "https://sayakb.com/main.min.1643e5368278aad51dc36916f6fb8d7d959a771436f20f9ca9f8d100cddecbbc.css",
  "https://sayakb.com/bundle.min.cf7871ed49474a80ed457154d24e61f7881adbe0f9384951a74ac46b688a39a4dbfa68bc6d37baeb058186de354ead3487d4ee7f083ea4cba860c48600b694f3.js",
  "https://sayakb.com/fonts/Inter-UI-Bold.woff2",
  "https://sayakb.com/fonts/Inter-UI-Regular.woff2",
  "https://sayakb.com/images/i512.png",
  "https://sayakb.com/images/i192.png",
  "https://sayakb.com/images/i144.png",
  "https://sayakb.com/images/i096.png",
  "https://sayakb.com/images/i072.png",
  "https://sayakb.com/images/i048.png",
  "https://fonts.gstatic.com/s/worksans/v4/QGYsz_wNahGAdqQ43Rh_fKDp.woff2",
  "https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/fonts/fontawesome-webfont.woff2?v=4.4.0",
  "https://fonts.gstatic.com/s/worksans/v4/QGYpz_wNahGAdqQ43Rh3o4T8mNhN.woff2",
  "https://connect.facebook.net/en_US/sdk.js?hash=5b4562eb9a0cd9a25c859e736199890d&ua=modern_es6",
  "https://sd.toneden.io/production/lasso.js"
];

// TODO: replace the following with the correct offline fallback page i.e.: const offlineFallbackPage = "offline.html";
const offlineFallbackPage = "index.html";

const networkFirstPaths = [
  /* Add an array of regex of paths that should go network first */
  // Example: /\/api\/.*/
  "/\/index.html/",
  "/\/404.html/",
  "/\/about\/.*/",
  "/\/music\/.*/",
  "/\/posts\/.*/"
];

const avoidCachingPaths = [
  /* Add an array of regex of paths that shouldn't be cached */
  // Example: /\/api\/.*/
];

function pathComparer(requestUrl, pathRegEx) {
  return requestUrl.match(new RegExp(pathRegEx));
}

function comparePaths(requestUrl, pathsArray) {
  if (requestUrl) {
    for (let index = 0; index < pathsArray.length; index++) {
      const pathRegEx = pathsArray[index];
      if (pathComparer(requestUrl, pathRegEx)) {
        return true;
      }
    }
  }

  return false;
}

self.addEventListener("install", function (event) {
  console.log("[PWA Builder] Install Event processing");

  console.log("[PWA Builder] Skip waiting on install");
  self.skipWaiting();

  event.waitUntil(
    caches.open(CACHE).then(function (cache) {
      console.log("[PWA Builder] Caching pages during install");

      return cache.addAll(precacheFiles).then(function () {
        if (offlineFallbackPage === "ToDo-replace-this-name.html") {
          return cache.add(new Response("TODO: Update the value of the offlineFallbackPage constant in the serviceworker."));
        }

        return cache.add(offlineFallbackPage);
      });
    })
  );
});

// Allow sw to control of current page
self.addEventListener("activate", function (event) {
  console.log("[PWA Builder] Claiming clients for current page");
  event.waitUntil(self.clients.claim());
});

// If any fetch fails, it will look for the request in the cache and serve it from there first
self.addEventListener("fetch", function (event) {
  if (event.request.method !== "GET") return;

  if (comparePaths(event.request.url, networkFirstPaths)) {
    networkFirstFetch(event);
  } else {
    cacheFirstFetch(event);
  }
});

function cacheFirstFetch(event) {
  event.respondWith(
    fromCache(event.request).then(
      function (response) {
        // The response was found in the cache so we responde with it and update the entry

        // This is where we call the server to get the newest version of the
        // file to use the next time we show view
        event.waitUntil(
          fetch(event.request).then(function (response) {
            return updateCache(event.request, response);
          })
        );

        return response;
      },
      function () {
        // The response was not found in the cache so we look for it on the server
        return fetch(event.request)
          .then(function (response) {
            // If request was success, add or update it in the cache
            event.waitUntil(updateCache(event.request, response.clone()));

            return response;
          })
          .catch(function (error) {
            // The following validates that the request was for a navigation to a new document
            if (event.request.destination !== "document" || event.request.mode !== "navigate") {
              return;
            }

            console.log("[PWA Builder] Network request failed and no cache." + error);
            // Use the precached offline page as fallback
            return caches.open(CACHE).then(function (cache) {
              cache.match(offlineFallbackPage);
            });
          });
      }
    )
  );
}

function networkFirstFetch(event) {
  event.respondWith(
    fetch(event.request)
      .then(function (response) {
        // If request was success, add or update it in the cache
        event.waitUntil(updateCache(event.request, response.clone()));
        return response;
      })
      .catch(function (error) {
        console.log("[PWA Builder] Network request Failed. Serving content from cache: " + error);
        return fromCache(event.request);
      })
  );
}

function fromCache(request) {
  // Check to see if you have it in the cache
  // Return response
  // If not in the cache, then return error page
  return caches.open(CACHE).then(function (cache) {
    return cache.match(request).then(function (matching) {
      if (!matching || matching.status === 404) {
        return Promise.reject("no-match");
      }

      return matching;
    });
  });
}

function updateCache(request, response) {
  if (!comparePaths(request.url, avoidCachingPaths)) {
    return caches.open(CACHE).then(function (cache) {
      return cache.put(request, response);
    });
  }

  return Promise.resolve();
}
