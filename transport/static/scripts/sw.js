// Service worker para instalar la PWA, y que hace funcionar la caché en la misma
self.addEventListener("install", event => {
    console.log("Service worker installed");
});
self.addEventListener("activate", event => {
    console.log("Service worker activated");    
})

caches.open("pwa-assets")
.then(cache => {
    cache.addAll(["/inicio?lang=gal", "/static/scripts/buscar.js", "/static/scripts/buses.js", "/static/scripts/linea.js", "/static/scripts/mapa.js", "/static/scripts/parada.js", "/static/css/main.css", "/static/css/map.css", "/static/css/other.css"]);
    //cache.addAll(["/static/css/main.css", "/static/css/map.css", "/static/css/other.css"]);
})

/* self.addEventListener("fetch", event => {
    event.respondWith(
      caches.match(event.request)
      .then(cachedResponse => {
        // It can update the cache to serve updated content on the next request
          return cachedResponse || fetch(event.request);
      }
    )
   )
 }); */

 self.addEventListener("fetch", event => {
    event.respondWith(
      fetch(event.request)
      .catch(error => {
        return caches.match(event.request) ;
      })
    );
 });
