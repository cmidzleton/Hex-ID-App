// Offline cache: app shell cache-first, fonts cached as they load.
const V='colorid-v2',SHELL=['./','index.html','manifest.webmanifest','icon-192.png','icon-512.png','icon-180.png'];
self.addEventListener('install',e=>e.waitUntil(caches.open(V).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  e.respondWith(caches.match(e.request).then(hit=>hit||fetch(e.request).then(res=>{
    const u=new URL(e.request.url);
    if(res.ok&&(u.origin===location.origin||u.host.endsWith('fonts.googleapis.com')||u.host.endsWith('fonts.gstatic.com'))){const copy=res.clone();caches.open(V).then(c=>c.put(e.request,copy))}
    return res;
  }).catch(()=>caches.match('index.html'))));
});
