"""Builds the live app with accounts and sync, in two languages.

Takes index.html and index_en.html (made by build.py), adds the login screen and Firebase cloud
sync from cloud/cloud_ui.html, and writes:
    cloud-test/index.html      BM (main)
    cloud-test/en/index.html   English, same site, same accounts and progress

    python build.py         # first, if template.html or the content changed
    python build_cloud.py
"""
import json, os, shutil

cfg = json.dumps(json.load(open('cloud/firebase-config.json', encoding='utf-8')))
ui = open('cloud/cloud_ui.html', encoding='utf-8').read().replace('__FIREBASE_CONFIG__', cfg)
SITE = 'https://falsafah200.vercel.app'


def build(lang, src_file, out_file):
    en = lang == 'en'
    up = '../' if en else ''     # the English page sits one folder down and shares the icons, manifest and SW
    src = open(src_file, encoding='utf-8').read()

    def sub(a, b):
        nonlocal src
        assert src.count(a) == 1, 'pattern not found once: ' + a[:60]
        src = src.replace(a, b)

    nl = '\r\n' if '\r\n' in src else '\n'
    # The cloud module opens the julat sheet after sign-in, so the app must not open it on its own.
    sub(nl.join(["  if(!getName() || !rangeSaved){", "    setTimeout(openNameModal, 400);", "  } else {", "    setTimeout(showThemeTip, 600);", "  }"]),
        nl.join(["  if(getName() && rangeSaved){", "    setTimeout(showThemeTip, 600);", "  }"]))
    if en:
        sub('<p>Tell us your name or what you like to be called to start using this memory helper for your Al-Quran Philosophy studies.</p>',
            '<p>Choose the falsafah range you are studying. The name below shows on the main screen.</p>')
        # the share card draws the logo from the shared icons folder
        sub("loadImg('icons/logo-240.png')", "loadImg('../icons/logo-240.png')")
    else:
        sub('<p>Sila nyatakan nama atau panggilan anda untuk mula menggunakan pembantu hafalan ini dalam lembaran pengajian Falsafah Al-Quran.</p>',
            '<p>Pilih julat falsafah yang anda kaji. Nama panggilan di bawah dipaparkan pada skrin utama.</p>')
    # index.html is a page fragment; give it a doctype so it renders in standards mode.
    # Phones a little smaller (10%); laptops at full size. Text boxes get 17.8px (x 90% = 16px) so iPhone does not zoom into them.
    head = nl.join([
        # backup for vercel.json: the old test address always shows the moved notice
        '<script>if(location.hostname==="falsafah200-test.vercel.app")location.replace("/moved.html");</script>',
        # the BM page opens the English one for students who chose English (the installed app starts at /)
        '' if en else '<script>try{if(localStorage.getItem("falsafah200_lang_v1")==="en")location.replace("/en/"+location.search+location.hash);}catch(e){}</script>',
        '<link rel="manifest" href="' + up + 'manifest.webmanifest">',
        '<link rel="apple-touch-icon" href="' + up + 'icons/apple-touch-icon.png">',
        '<link rel="icon" type="image/png" href="' + up + 'icons/favicon-32.png">',
        '<meta name="mobile-web-app-capable" content="yes">',
        '<meta name="apple-mobile-web-app-capable" content="yes">',
        '<meta name="apple-mobile-web-app-title" content="Falsafah 200">',
        '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">',
        # link preview card (WhatsApp, Telegram, Facebook, X); WhatsApp needs absolute URLs
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="Al-Fathun Nawa">',
        '<meta property="og:title" content="الفتح النوى · Falsafah 200">',
        '<meta property="og:description" content="' + ('Review the 200 falsafah of Al-Fathun Nawa Volume 7. Listen to the ayat, test your memory, see your progress.' if en else
                                                       'Ulang kaji 200 falsafah Al-Fathun Nawa Jilid 7. Dengar ayat, uji ingatan, lihat kemajuan anda.') + '">',
        '<meta property="og:url" content="' + SITE + ('/en/' if en else '/') + '">',
        '<meta property="og:image" content="' + SITE + '/icons/og-square.jpg?v=2">',
        '<meta property="og:image:secure_url" content="' + SITE + '/icons/og-square.jpg?v=2">',
        '<meta property="og:image:type" content="image/jpeg">',
        '<meta property="og:image:width" content="800">',
        '<meta property="og:image:height" content="800">',
        '<meta property="og:image:alt" content="Logo AFN, Falsafah 200">',
        '<meta name="twitter:card" content="summary">',
        # progress handed over from the old link (landing page): merged into this device before the app starts,
        # then into the student's account when they log in or register
        '<script>' + open('cloud/import.js', encoding='utf-8').read() + '</script>',
        # Android's install prompt can fire early; keep it for the "Pasang sekarang" button
        '<script>window.addEventListener("beforeinstallprompt",function(e){e.preventDefault();window.__bip=e;document.dispatchEvent(new Event("fn-bip"));});'
        'if("serviceWorker" in navigator){window.addEventListener("load",function(){navigator.serviceWorker.register("' + up + 'sw.js").catch(function(){});});}</script>',
    ])
    src = ('<!doctype html>' + nl + '<meta charset="utf-8">' + nl + head + nl
           + '<style>@media (max-width:600px){ html{ zoom:.9; } input:not(.pin), select, textarea{ font-size:17.8px !important; } }</style>' + nl + src + nl + ui + nl)
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    open(out_file, 'w', encoding='utf-8', newline='').write(src)
    print(out_file, len(src))


build('ms', 'index.html', 'cloud-test/index.html')
build('en', 'index_en.html', 'cloud-test/en/index.html')
# home-screen app files
shutil.copytree('cloud/icons', 'cloud-test/icons', dirs_exist_ok=True)
# moved.html: the notice shown on the old test address (vercel.json routes that host to it)
for f in ('manifest.webmanifest', 'sw.js', 'moved.html'):
    shutil.copy('cloud/' + f, 'cloud-test/' + f)
