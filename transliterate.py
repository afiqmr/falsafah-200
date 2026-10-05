import json, re, sys, unicodedata

# Malay-friendly consonant spelling; the in-app search normalises spelling variants anyway.
CONS = {
    'ب': 'b', 'ت': 't', 'ث': 'ts', 'ج': 'j', 'ح': 'h', 'خ': 'kh', 'د': 'd', 'ذ': 'dz',
    'ر': 'r', 'ز': 'z', 'س': 's', 'ش': 'sy', 'ص': 's', 'ض': 'dh', 'ط': 't', 'ظ': 'z',
    'ع': "'", 'غ': 'gh', 'ف': 'f', 'ق': 'q', 'ك': 'k', 'ل': 'l', 'م': 'm', 'ن': 'n',
    'ه': 'h', 'ء': "'", 'أ': "'", 'إ': "'", 'ؤ': "'", 'ئ': "'",
}
VOWELS = {'َ': 'a', 'ِ': 'i', 'ُ': 'u',
          'ً': 'an', 'ٍ': 'in', 'ٌ': 'un',
          'ࣰ': 'an', 'ࣱ': 'un', 'ࣲ': 'in'}
SHADDA = 'ّ'
SUKUN = {'ْ', 'ۡ'}
SILENT = {'۟', '۠'}
HAMZA_MARKS = {'ٔ', 'ٕ'}
DAGGER = 'ٰ'
YA = {'ي', 'ی'}
WAW = 'و'
MARK_CHARS = set(VOWELS) | {SHADDA, DAGGER, 'ۥ', 'ۦ', 'ۧ'} | SUKUN | SILENT | HAMZA_MARKS


def is_mark(ch):
    return unicodedata.category(ch) == 'Mn' or ch in ('ۥ', 'ۦ')


def clusters(text):
    text = text.replace(' ', '')
    # a space directly before a combining mark is a rendering split inside one word
    text = re.sub(r'[  ]+(?=[ٰۥۦ])', '', text)
    text = text.replace(' ', ' ')
    out = []
    i = 0
    while i < len(text):
        base = text[i]
        j = i + 1
        while j < len(text) and is_mark(text[j]):
            j += 1
        out.append((base, text[i + 1:j]))
        i = j
    return out


def transliterate(text):
    cl = clusters(text)
    out = []
    seen_letter = False

    def last():
        s = ''.join(out).rstrip(' ')
        return s[-1] if s else ''

    for k, (base, marks) in enumerate(cl):
        if base.isspace():
            if out and out[-1] != ' ':
                out.append(' ')
            continue
        if any(m in SILENT for m in marks):
            continue
        hamza = any(m in HAMZA_MARKS for m in marks)
        vowel = ''.join(VOWELS[m] for m in marks if m in VOWELS)
        has_shadda = SHADDA in marks
        has_sukun = any(m in SUKUN for m in marks)

        cons = None
        if hamza:
            cons = "'"
        elif base == 'ٱ':  # alif wasla: voiced only at the very start
            if not seen_letter:
                out.append('a')
            seen_letter = True
            continue
        elif base == 'آ':
            out.append("'aa")
            seen_letter = True
            continue
        elif base == 'ا':
            if vowel:
                cons = "'"
            else:
                if last() == 'a':
                    out.append('a')
                seen_letter = True
                continue
        elif base == 'ى':
            if DAGGER in marks:
                out.append('a' if last() == 'a' else 'aa')
            elif vowel or has_shadda:
                cons = 'y'
            elif last() in ('a', 'i'):
                out.append(last())
            seen_letter = True
            continue
        elif base in YA or base == WAW:
            c = 'y' if base in YA else 'w'
            long_v = 'i' if base in YA else 'u'
            if vowel or has_shadda or has_sukun:
                cons = c
            elif last() == long_v:
                out.append(long_v)
                seen_letter = True
                continue
            else:
                cons = c
        elif base == 'ة':
            cons = 't' if vowel else 'h'
        elif base == 'ل' and not vowel and not has_sukun and not has_shadda:
            # lam of the article assimilated into a following shadda letter (ar-rahman, an-nas)
            nxt = next(((b, m) for b, m in cl[k + 1:] if not b.isspace()), None)
            if nxt and SHADDA in nxt[1]:
                seen_letter = True
                continue
            cons = 'l'
        elif base in CONS:
            cons = CONS[base]
        elif base == 'ـ':  # tatweel carries marks only
            cons = ''
        else:
            continue  # waqf signs, rub el hizb, etc.

        seen_letter = True
        out.append(cons)
        if has_shadda and cons:
            out.append(cons)
        out.append(vowel)
        if DAGGER in marks:
            out.append('a' if last() == 'a' else 'aa')
        if 'ۥ' in marks:
            out.append('u')
        if 'ۦ' in marks or 'ۧ' in marks:
            out.append('i')

    return re.sub(r' +', ' ', ''.join(out)).strip()


if __name__ == '__main__':
    data = json.load(open('data.json', encoding='utf-8'))
    for e in data:
        e['translit'] = transliterate(e['arabic'])
    json.dump(data, open('data.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    ids = [int(x) for x in sys.argv[1:]] or [e['id'] for e in data[:8]]
    byid = {e['id']: e for e in data}
    with open('translit_check.txt', 'w', encoding='utf-8') as f:
        for i in ids:
            f.write('%s | %s\n%s\n\n' % (byid[i]['rangeLabel'], byid[i]['surahDisplay'], byid[i]['translit']))
