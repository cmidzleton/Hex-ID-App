# Builds the hostable home-screen app from colour-scanner.html into site/
import pathlib
from PIL import Image, ImageDraw
# ---- Change the app's name here, then run: python3 src/build.py ----
APP_NAME = 'ColorID'
here=pathlib.Path(__file__).parent; out=here.parent
page=(here/'app.html').read_text()
def brand(n): return n[:-2]+'<em>ID</em>' if n.endswith('ID') else n
page=page.replace('<title>ColorID</title>','<title>__APP__</title>').replace('<h1>Color<em>ID</em></h1>','<h1>'+brand(APP_NAME)+'</h1>')
head='''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="__APP__">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="theme-color" content="#1f6f5c">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}</style>
</head><body>
'''
(out/'index.html').write_text((head+page+'\n</body></html>\n').replace('__APP__',APP_NAME))
(out/'manifest.webmanifest').write_text('''{
  "name": "__APP__",
  "short_name": "__APP__",
  "description": "Point your camera at a colour and read its HEX, RGB, HSL and CMYK codes.",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "background_color": "#eef0ee",
  "theme_color": "#1f6f5c",
  "icons": [
    {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
    {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
  ]
}
'''.replace('__APP__',APP_NAME))
(out/'sw.js').write_text('''// Offline cache: app shell cache-first, fonts cached as they load.
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
''')
def icon(n):
    s=n*4; im=Image.new('RGB',(s,s),(31,111,92)); d=ImageDraw.Draw(im)
    r=int(s*.27); c=s//2; w=max(4,s//28)
    d.ellipse([c-r,c-r,c+r,c+r],fill=(238,240,238))
    g=int(s*.08)
    for a,b in [((c,c-r-g*2),(c,c-g)),((c,c+g),(c,c+r+g*2)),((c-r-g*2,c),(c-g,c)),((c+g,c),(c+r+g*2,c))]:
        d.line([a,b],fill=(21,26,23),width=w)
    d.rectangle([c-g//2,c-g//2,c+g//2,c+g//2],outline=(21,26,23),width=w)
    im.resize((n,n),Image.LANCZOS).save(out/f'icon-{n}.png')
for n in (180,192,512): icon(n)
print('built',APP_NAME)
