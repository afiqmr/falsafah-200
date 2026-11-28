"""Writes the `arabic` field of data.json and data_en.json from the KFGQPC Hafs text.

Jilid 7 prints every ayat in the KFGQPC Uthmanic Script HAFS font with the King Fahd Complex
(Madinah Mushaf) text, so the app uses the same text (kfgqpc/hafs_v18.json) and the same font
(kfgqpc/hafs.18.woff2). Each `arabic` value is the words the book quotes, with the ayat number
after every ayat the quote finishes (the font draws it as the round marker).

QUOTES lists the falsafah where the book quotes only part of the ayat range, as
[first word, end word) over all the words of the range (0-based, end not included).
Checked against the book (PDF page = printed page + 69).

Class-extended falsafah (the class notes extend them to cover more meaning) keep the longer
ayat, in the same KFGQPC text: 31 (book quotes only "inna Allaha baalighu amrih" of 65:3, class
the whole ayat), 46 (book 53:39-40, class 39-41), 53 (book 74:1-4, class 1-7), 117 (book 24:37,
class 37 plus hafalan tambahan 38), 168 (book 3:103 up to "ikhwaanan", class the whole ayat) and
174 (book 66:6 up to "naaran", class the whole ayat). Do not add them to QUOTES or RANGES.

    python build_arabic.py     # then python build.py and python build_cloud.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
KF = json.loads((ROOT / 'kfgqpc' / 'hafs_v18.json').read_text(encoding='utf-8'))

QUOTES = {
    9: (17, 26), 10: (17, 26), 11: (17, 26), 12: (24, 33), 13: (11, 17), 28: (8, 15),
    38: (27, 32), 39: (8, 14), 42: (0, 12), 55: (0, 5), 60: (0, 10),
    62: (37, 46), 72: (6, 25), 78: (11, 21), 81: (21, 30), 94: (0, 10), 164: (0, 5),
    166: (39, 50),
}
RANGES = {}   # e.g. {46: '39-40'} would cut a class-extended falsafah back to the book's ayat


def ayah_range(r):
    a, _, b = str(r).partition('-')
    return int(a), int(b or a)


def ayah_words(s, a):
    text = KF['%d:%d' % (s, a)]
    body, num = re.match(r'^(.*?)\xa0([٠-٩]+)$', text).groups()
    return body.split(' '), num


def quote(e):
    a1, a2 = ayah_range(e['ayahRange'])
    ayat = [ayah_words(e['surahNumber'], a) for a in range(a1, a2 + 1)]
    total = sum(len(w) for w, _ in ayat)
    start, end = QUOTES.get(e['id'], (0, total))
    assert 0 <= start < end <= total, (e['id'], start, end, total)
    parts, k = [], 0
    for words, num in ayat:
        for i, w in enumerate(words):
            if start <= k < end:
                parts.append(w + ('\xa0' + num if i == len(words) - 1 else ''))
            k += 1
    return ' '.join(parts)


for name, indent in (('data.json', 2), ('data_en.json', 1)):
    path = ROOT / name
    data = json.loads(path.read_text(encoding='utf-8'))
    for e in data:
        if e['id'] in RANGES:
            old = e['ayahRange']
            e['ayahRange'] = RANGES[e['id']]
            e['surahDisplay'] = re.sub(r'(Ayat )%s$' % re.escape(old), r'\g<1>' + RANGES[e['id']], e['surahDisplay'])
            assert e['surahDisplay'].endswith(RANGES[e['id']]), e['surahDisplay']
        e['arabic'] = quote(e)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=indent), encoding='utf-8')
    print('%s: %d entries, %d partial quotes, %d range fixes' % (name, len(data), len(QUOTES), len(RANGES)))
