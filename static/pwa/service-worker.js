//service-worker.js
//tid_corporate_project(2024)
//gen3
//created T.Saito

const CACHE_NAME = 'shirayama-cache';
const urlsToCache = ["/", "/static/css/style.css", "/static/svgs/add.svg", "/static/svgs/call.svg", 
"/static/svgs/delete.svg", "/static/svgs/folder.svg", "/static/svgs/home.svg", "/static/svgs/info.svg", 
"/static/svgs/question.svg", "/static/svgs/user.svg", "/static/ico/shirayama_app_mm.png","/static/ico/shirayama_app_bm.png"
];

self.addEventListener('install', function (e) {
    e.waitUntil(
        caches.open('CACHE_NAME').then(function (cache) {
            return cache.addAll(urlsToCache);
        })
    );
});

self.addEventListener('fetch', function (ev) {
    if(ev.request.url.includes('/')){
        ev.respondWith(fetch(ev.request));
    }else{
        ev.respondWith(
            caches.match(ev.request).then(function (response) {
                return response || fetch(ev.request);
            })
        );
    }
});

self.addEventListener('activate', evnt => {
    const cacheWhitelist = [CACHE_NAME];
    evnt.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (!cacheWhitelist.includes(cacheName)) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});