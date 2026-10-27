# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this is

Falsafah 200 is a study app for the 200 falsafah of _Al-Fathun Nawa Jilid 7_. It is one HTML page
built from `template.html` and JSON content, with an account and sync layer added at build time.
The live app is https://falsafah200.vercel.app (BM) and https://falsafah200.vercel.app/en/ (English).
Both come from the same template: `window.FN_LANG` is `ms` or `en`, and interface text is written as
`T('BM text', 'English text')`.

## Commands

```bash
python quiz_bank.py      # validate the Kuiz bank and write quiz.json (must print "ok 200")
python build.py          # -> index.html (BM) and index_en.html (English), standalone, no accounts
python build_cloud.py    # -> cloud-test/ and cloud-test/en/ (the live app: accounts, sync, install)
python build_notes.py    # only after changing notes_source/*.docx or the summaries in the script
```

Always run `build.py` then `build_cloud.py` after any change to `template.html`, `data.json`,
`quiz.json` or `cloud/`. Never edit `index.html` or `cloud-test/index.html` by hand.

Deploy: commit to `main`, push, then deploy the `cloud-test` folder to the Vercel project
`falsafah200-test` (framework none, empty build and install commands, output `cloud-test`) and
wait for READY.

## Rules

- **Content**: titles, maksud, Kata Kunci, Catitan and page numbers come from Jilid 7. Do not
  reword them unless asked. `bookPages` are printed page numbers (PDF page minus 69).
- **Kuiz**: edit questions in `quiz_bank.py`, never `quiz.json`. Distractors must not share an
  ayat with the answer.
- **Recordings**: Dr. HALO-N's recordings are for signed-in students only. Never add audio files
  to the repository.
- **Share**: the share card and share text never include the Catitan.
- **Screenshots and videos** use demo accounts and demo progress, never real students.
- **Sync**: a new progress key must be added to `KEYS` in `cloud/cloud_ui.html` with a merge rule
  in `merge()`, or it will stay on one device.
- **Admin**: the admin email in `ADMIN_EMAILS` must match the Firestore rules in
  `docs/security.md`.
- **`build_cloud.py` substitutions** assert that each pattern occurs once. If you change those
  lines in `template.html`, update the script.
- **Interface text** is short, plain BM, with English beside it in `T(ms, en)`. Static markup in
  English goes in `i18n/en_static.json` (each pattern must occur once). Keep both themes and phone
  width (390 px) working in both languages.
- **English content**: `data_en.json` (from Al-Fathun Nawa Volume 7, English edition; BM ayat ranges
  are the main reference), `notes_en.json` and `i18n/quiz_en.json` (question text only, keyed by id).
  App-written English never uses "verse"; use "Ayat". Text quoted from the English book keeps its
  own wording. English terms: Sadaqah, Rasul / Rasulullah, Solat.
- **Pandangan**: the author name always comes from the account profile. Only admin-published
  opinions reach other students, and a student's delete only hides it (`deleted: true`).

## Where things are

- App code: `template.html`, one IIFE, areas in the order listed in `docs/architecture.md`.
- Account layer: `cloud/cloud_ui.html` (login, sync and merge, admin, recordings, install).
- Content formats and storage keys: `docs/data-formats.md`.
- Firestore rules and privacy: `docs/security.md`.
- How to check a change: `docs/testing.md`.
- Decisions: `docs/decisions/`.

Update `CHANGELOG.md` and the relevant doc when a change affects what students see, a data
format, or the rules.
