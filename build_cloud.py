"""Builds the cloud-login test version of the app.

Takes index.html (made by build.py), adds the login screen and Firebase cloud
sync from cloud/cloud_ui.html, and writes cloud-test/index.html.

    python build.py         # first, if template.html or data.json changed
    python build_cloud.py
"""
import json, os

src = open('index.html', encoding='utf-8').read()
cfg = json.dumps(json.load(open('cloud/firebase-config.json', encoding='utf-8')))
ui = open('cloud/cloud_ui.html', encoding='utf-8').read().replace('__FIREBASE_CONFIG__', cfg)

def sub(a, b):
    global src
    assert src.count(a) == 1, 'pattern not found once: ' + a[:60]
    src = src.replace(a, b)

nl = '\r\n' if '\r\n' in src else '\n'
# The cloud module opens the julat sheet after sign-in, so the app must not open it on its own.
sub(nl.join(["  if(!getName() || !rangeSaved){", "    setTimeout(openNameModal, 400);", "  } else {", "    setTimeout(showThemeTip, 600);", "  }"]),
    nl.join(["  if(getName() && rangeSaved){", "    setTimeout(showThemeTip, 600);", "  }"]))
sub('<p>Sila nyatakan nama atau panggilan anda untuk mula menggunakan pembantu hafalan ini dalam lembaran pengajian Falsafah Al-Quran.</p>',
    '<p>Pilih julat falsafah yang anda kaji. Nama panggilan di bawah dipaparkan pada skrin utama.</p>')
# index.html is a page fragment; give it a doctype so it renders in standards mode.
# Phones a little smaller (10%); laptops at full size.
SITE = 'https://falsafah200.vercel.app'
head = nl.join([
    '<link rel="manifest" href="manifest.webmanifest">',
    '<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">',
    '<link rel="icon" type="image/png" href="icons/favicon-32.png">',
    '<meta name="mobile-web-app-capable" content="yes">',
    '<meta name="apple-mobile-web-app-capable" content="yes">',
    '<meta name="apple-mobile-web-app-title" content="Falsafah 200">',
    '<meta name="apple-mobile-web-app-status-bar-style" content="default">',
    # link preview card (WhatsApp, Telegram, Facebook, X); WhatsApp needs absolute URLs
    '<meta property="og:type" content="website">',
    '<meta property="og:site_name" content="Al-Fathun Nawa">',
    '<meta property="og:title" content="الفتح النوى · Falsafah 200">',
    '<meta property="og:description" content="Kaji dan hafaz 200 Falsafah Al-Quran dari Al-Fathun Nawa Jilid 7, dengan ayat asal, ulang kaji, kuiz dan kemajuan.">',
    '<meta property="og:url" content="' + SITE + '/">',
    '<meta property="og:image" content="' + SITE + '/icons/og-image.jpg?v=1">',
    '<meta property="og:image:secure_url" content="' + SITE + '/icons/og-image.jpg?v=1">',
    '<meta property="og:image:type" content="image/jpeg">',
    '<meta property="og:image:width" content="1200">',
    '<meta property="og:image:height" content="630">',
    '<meta property="og:image:alt" content="Logo AFN, Falsafah 200">',
    '<meta name="twitter:card" content="summary_large_image">',
    # progress handed over from the old link (landing page): merged into this device before the app starts,
    # then into the student's account when they log in or register
    '<script>' + open('cloud/import.js', encoding='utf-8').read() + '</script>',
    # Android's install prompt can fire early; keep it for the "Pasang sekarang" button
    '<script>window.addEventListener("beforeinstallprompt",function(e){e.preventDefault();window.__bip=e;document.dispatchEvent(new Event("fn-bip"));});'
    'if("serviceWorker" in navigator){window.addEventListener("load",function(){navigator.serviceWorker.register("sw.js").catch(function(){});});}</script>',
])
src = ('<!doctype html>' + nl + '<meta charset="utf-8">' + nl + head + nl
       + '<style>@media (max-width:600px){ html{ zoom:.9; } }</style>' + nl + src + nl + ui + nl)

os.makedirs('cloud-test', exist_ok=True)
open('cloud-test/index.html', 'w', encoding='utf-8', newline='').write(src)
# home-screen app files
import shutil
shutil.copytree('cloud/icons', 'cloud-test/icons', dirs_exist_ok=True)
for f in ('manifest.webmanifest', 'sw.js'):
    shutil.copy('cloud/' + f, 'cloud-test/' + f)
print('cloud-test/index.html', len(src))
