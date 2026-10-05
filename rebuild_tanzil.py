import json, re, glob, os

# Load every surah file into {surah_number: [ayah_text, ...]} (1-indexed list,
# so ayah N is at index N-1). Each line ends with a non-breaking space + the
# U+06DD end-of-ayah marker + Arabic-Indic ayah number, which we strip.
surahs = {}
for path in glob.glob('tanzil_quran/*.txt'):
    name = os.path.basename(path)
    if not re.match(r'^\d{3}\.txt$', name):
        continue
    num = int(name[:3])
    with open(path, encoding='utf-8') as f:
        raw_lines = f.read().split('\n')
    ayahs = []
    for line in raw_lines:
        line = line.strip()
        if not line:
            continue
        line = re.sub(r'\xa0۝[٠-٩١-٩]+$', '', line).strip()
        ayahs.append(line)
    surahs[num] = ayahs

print(f'Loaded {len(surahs)} surahs.')
print('Surah 1 ayah count:', len(surahs[1]), '(expect 7)')
print('Surah 2 ayah count:', len(surahs[2]), '(expect 286)')
print('Surah 114 ayah count:', len(surahs[114]), '(expect 6)')

with open('data.json', encoding='utf-8') as f:
    data = json.load(f)
byid = {e['id']: e for e in data}


def parse_ayah_range(s):
    s = s.strip()
    m = re.match(r'^(\d+)\s*-\s*(\d+)$', s)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.match(r'^(\d+)$', s)
    if m:
        return int(m.group(1)), int(m.group(1))
    return None, None


issues = []
for e in data:
    num = e['surahNumber']
    a, b = parse_ayah_range(e['ayahRange'])
    if a is None or num not in surahs:
        issues.append((e['id'], 'unparsed/missing surah', e['ayahRange'], num))
        continue
    ayahs = surahs[num]
    if b > len(ayahs):
        issues.append((e['id'], 'ayah out of range', f'{a}-{b}', 'max', len(ayahs)))
        b = len(ayahs)
    e['arabic'] = ' '.join(ayahs[a - 1:b])

print(f'\nRegenerated {len(data)} entries. Issues: {len(issues)}')
for i in issues:
    print(i)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
