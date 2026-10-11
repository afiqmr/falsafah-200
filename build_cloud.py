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
sub('<title>الفتح النوى - Falsafah 200</title>', '<title>الفتح النوى - Falsafah 200 (Test)</title>')
# index.html is a page fragment; give it a doctype so it renders in standards mode.
# Phones a little smaller (10%); laptops at full size.
src = ('<!doctype html>' + nl + '<meta charset="utf-8">' + nl
       + '<style>@media (max-width:600px){ html{ zoom:.9; } }</style>' + nl + src + nl + ui + nl)

os.makedirs('cloud-test', exist_ok=True)
open('cloud-test/index.html', 'w', encoding='utf-8', newline='').write(src)
print('cloud-test/index.html', len(src))
