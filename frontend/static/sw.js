self.addEventListener('install', function(e) {
  self.skipWaiting();
});

self.addEventListener('fetch', function(e) {
  e.respondWith(fetch(e.request).catch(function() {
    return new Response('离线中，请检查网络连接', {
      headers: {'Content-Type': 'text/plain'}
    });
  }));
});
