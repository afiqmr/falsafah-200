# Architecture

Falsafah 200 is a single HTML page. Two small Python scripts assemble it from a template and
JSON content, and a second step adds accounts and sync. There is no framework, bundler or
server code.

## Build pipeline

```text
data.json ─┐
notes.json ├─ build.py ──► index.html ── build_cloud.py ──► cloud-test/index.html  (live)
quiz.json ─┤   (inlines JSON           (adds cloud/cloud_ui.html,       + icons, manifest,
logo-afiq ─┘    and the logo)           head tags, import.js, SW)          sw.js, moved.html
```

- `build.py` replaces the `__DATA_JSON__`, `__NOTES_JSON__`, `__QUIZ_JSON__` and `__LOGO_URI__`
  placeholders in `template.html`. JSON is inlined in `<script type="application/json">` tags, with
  `</script` escaped.
- `build_cloud.py` makes a few exact string substitutions in `index.html`. Each one asserts that
  its pattern occurs exactly once, so a template change that breaks a substitution fails the build
  instead of shipping silently. It then appends `cloud/cloud_ui.html` with the Firebase config.
- `index.html` on its own is a complete offline app without accounts.

## Inside the page

All app code is one IIFE at the end of `template.html`. Main areas, in file order:

| Area                 | What it does                                                              |
| -------------------- | ------------------------------------------------------------------------- |
| Daily state          | Today's Kaji ids, Kuiz count, results, cheer flags; rolls over at midnight |
| Streak               | Days with both targets met; the 🔥 tile in the mission bar                 |
| Markah and gred      | Last 10 answers per falsafah (Kaji ±1, Kuiz ±½) mapped to A+ … G           |
| History              | Per-day Ingat / Belum ingat / missed-once lists, kept 120 days            |
| Kaji                 | Card queue over the julat, Dedah, grading, day summary, focus sessions    |
| Voice check          | "Baca dari ingatan" and "Cuba baca" using the Web Speech API              |
| Progres              | Gred tiles, Perlu fokus, markah list, chart, history, weekly popups       |
| Senarai              | Search, opening-word groups, detail sheet, share card                     |
| Kuiz                 | Question bank, Arabic-only options, reveal with Jilid 7 explanation       |
| Nota                 | Topic switch by subject year and the note cards                           |
| Dengar               | Audio player, word by word, Media Session controls, silent "bed" track   |
| Word by word         | Quran.com words aligned to the quoted part of each ayat, cached on device |
| Tour and init        | First-time walkthrough, theme, initial render                             |

The cloud layer talks to the app through `window.FN_APP` (tour, weekly check, refresh) and
provides `window.FN_HALON` (Dr. HALO-N recordings) and `window.FN_SONGKET_BAND` (share card
motif).

## Cloud layer (`cloud/cloud_ui.html`)

- **Accounts**: Firebase Auth with email and password. Students type a username and a 6-digit
  PIN; the username is looked up in `usernames/{name}` to find the sign-in email.
- **Sync**: the synced localStorage keys are read into one snapshot, merged with the copy in
  `users/{uid}`, written back to both, and the page reloads once if local data changed. Merging is
  per item, never last-write-wins for the whole record:
  - cards keep the one with more Kaji answers, then the latest answer;
  - today's Kaji ids, history lists and streak days are unions;
  - Kuiz count takes the higher value.
- **Admin**: one verified email sees every student's progress, publishes the weekly class list to
  `stats/weekly`, and uploads Dr. HALO-N recordings to `stats/halon-*`.
- **Pandangan**: students write an opinion on one or more falsafah from the menu or the Senarai
  detail sheet (`window.FN_PANDANGAN.open(id)`). The admin publishes it from the admin panel; only
  published ones appear to other students.
- **Install and offline**: `manifest.webmanifest` and `sw.js` make it installable. The service
  worker is network-first, so students always get the newest build and the cached copy is used
  only offline.
- **Moving address**: the old `falsafah200-test.vercel.app` serves `moved.html` (by `vercel.json`
  and a head script). Its button carries the student's progress in the URL hash (`#bawa=`), and
  `import.js` merges it into the new address before the app starts.

## External services

| Service          | Used for                                   | Without internet                     |
| ---------------- | ------------------------------------------ | ------------------------------------ |
| Firebase         | Sign-in, sync, class stats, recordings     | App works; syncs on next sign-in     |
| Quran.com API    | Word by word, murattal audio and timings   | Word by word works for cached ayat   |
| Google Fonts     | Noto Sans and Scheherazade New             | Falls back to system fonts           |
| Speech services  | Voice check (inside the browser)           | Voice check shows a message          |
