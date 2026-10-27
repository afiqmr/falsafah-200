# Testing

There is no automated test suite in the repository yet. Changes are checked by building, running
the page in a browser, and, for bigger changes, Playwright scripts against `cloud-test/index.html`
with Firebase replaced by local mocks.

## Before every deploy

1. `python quiz_bank.py` if the Kuiz bank changed. It must print `ok 200`.
2. `python build.py` and `python build_cloud.py`. Both must finish without an assertion.
3. Open `cloud-test/index.html` and check the browser console is free of errors.
4. Walk the area you changed in **both themes** and at **phone width (390 px)** and desktop width.

## What to check by area

| Area     | Check                                                                                  |
| -------- | -------------------------------------------------------------------------------------- |
| Kaji     | Dedah, Ingat, Belum ingat; day summary; Ulang belum ingat; target ribbon; streak        |
| Voice    | Baca dari ingatan: Selesai, 80% auto Ingat and Batal, Hampir, Cuba lagi, no mic        |
| Kuiz     | 2 or 3 Arabic options; right and wrong answers; reveal; count in the mission bar      |
| Progres  | Gred tiles open their lists; Perlu fokus; markah list; chart; history                  |
| Senarai  | Search by number, title and pronunciation; detail sheet; word by word; share          |
| Nota     | Subject-year groups; each topic opens; last topic remembered                           |
| Dengar   | Play, skip, pause length, lock-screen controls, word by word while playing            |
| Accounts | Register, log in, Lupa PIN, two devices merging, log out clears the device             |
| Pandangan| Write from menu and Senarai; required fields; 5 falsafah cap; delete; admin Terbit     |

## Playwright approach

- Route `**/firebasejs/**` to local mock modules and abort other `https://` requests, so tests
  never touch the real project.
- Seed localStorage in an init script (range, theme, progress) to reach a state quickly.
- Replace `window.webkitSpeechRecognition` with a mock that returns a chosen transcript, to test
  the voice check without a microphone.
- Route `fonts.googleapis.com` to local Fontsource files so Arabic renders as students see it.
- `window.FN_APP.voiceMatch(arabic, transcript)` exposes the word matcher for direct checks.

## Known gaps

- The real speech recognisers on iPhone and Android can only be checked on the devices.
- Installing to the home screen, the iPhone status bar and lock-screen audio need a real phone.
