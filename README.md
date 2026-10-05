# Al-Fathun Nawa: Falsafah 1-200

A study app for students of the Advanced Diploma in Al-Quranic Philosophy (Institut Falsafah Al-Quran) to understand and memorise the 200 falsafah of *Al-Fathun Nawa Jilid 7* by Philosopher D'Outreach Professor Dr. HALO-N.

Created by Afiq Rashdi, September 2026.

## Features

- **Kaji**: spaced-repetition flashcards in random order, covering every falsafah in the chosen range. Each card reveals the ayat, the Malay meaning, the surah reference, Kata Kunci Falsafah and Catitan Kaedah Pembuka Mulut.
- **Senarai**: all falsafah, searchable by number, title, meaning, surah, Kata Kunci or a romanised pronunciation of the ayat (e.g. `wahuwa ma'akum`). It also has a "Kumpulan permulaan ayat" view that groups Falsafah 101-200 by shared opening words.
- **Kuiz**: match ayat to title and title to ayat.
- **Progres**: mastery breakdown for the chosen range.
- **Study range**: Tahun 1 (1-100), Tahun 2 (101-200), Semua (1-200) or a custom range. It applies to Kaji, Kuiz and Progres.
- Daily goals, a countdown to the exam date, and light and dark themes.

Progress is stored in the browser (`localStorage`), so it stays on each device. There is no server or account.

## Using it

`index.html` is the whole app in one file. Open it in a browser, or host it anywhere that serves static files (e.g. GitHub Pages, Netlify). It needs an internet connection only to load Google Fonts.

## Editing

| File | What it is |
|------|------------|
| `template.html` | All HTML, CSS and JavaScript, with a `__DATA_JSON__` placeholder |
| `data.json` | The 181 falsafah entries (numbers, title, Malay meaning, surah reference, Arabic, Kata Kunci, Catitan, transliteration) |
| `build.py` | Combines the two into `index.html` |

After changing `template.html` or `data.json`, rebuild:

```
python build.py
```

Never edit `index.html` directly, because the next build overwrites it.

Settings you are likely to change are near the top of the script in `template.html`:
- `DEADLINE`: the exam date used for the countdown (and the "13 Okt" label in `renderMissionBar`).
- `DAILY_KAJI_GOAL` and `DAILY_KUIZ_GOAL`: the daily targets.
- `AYAT_GROUPS`: the opening-word groups shown in Senarai.

### Arabic text and transliteration

The Arabic in `data.json` comes from the Tanzil-derived text in `tanzil_quran/` (one file per surah, one ayah per line).

- `rebuild_tanzil.py` regenerates every entry's Arabic from each entry's `surahNumber` and `ayahRange`.
- `trim_tanzil.py` then cuts entries where the book quotes only part of an ayat, using word ranges.
- `transliterate.py` generates the romanised `translit` field used by the pronunciation search.

Run all three in that order after a full Arabic rebuild, then run `build.py`. For a one-off fix, edit the entry in `data.json` directly and rebuild.

## Sources and credits

- Falsafah titles, meanings, Kata Kunci and Catitan come from *Al-Fathun Nawa Jilid 7* by Prof. Dr. HALO-N.
- The Quran text is from [khaledhosny/quran-data](https://github.com/khaledhosny/quran-data), which is based on the [Tanzil](https://tanzil.net) Uthmani text. That project notes the text has not been formally reviewed. Please report any errors you find.
- The Arabic font is [Scheherazade New](https://software.sil.org/scheherazade/) by SIL, and the interface font is Noto Sans. Both load from Google Fonts.

Made for students of the Advanced Diploma in Al-Quranic Philosophy, Institut Falsafah Al-Quran, in collaboration with Yayasan Gual Periok and World Philosophical Forum (WPF) Malaysia.
