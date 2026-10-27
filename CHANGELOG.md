# Changelog

Notable changes to Falsafah 200, newest first. The live app is updated on every push to `main`.

## 2026-10-27

### Added

- Pandangan: students write an opinion on a falsafah (title, 1 to 5 linked falsafah, opinion),
  from the account menu or "Kongsi pandangan" in Senarai. They see their own and the published
  ones. The admin reads all of them first and chooses Terbit or Simpan in the admin panel.

### Changed

- Voice check is more forgiving of the phone's mishearing: letters it often swaps (ص/س, ط/ت,
  ض/د, ذ/ظ/ز, ق/ك, ح/ه) count as the same, merged idgham words count, and on Android the best of
  several guesses is used. A wrong ayat still scores low.

## 2026-10-25

### Fixed

- Dengar keeps playing ulangan and the next falsafah with the screen locked or another app in
  front (such as Google Maps). A silent track now fills every pause and load, so the phone never
  stops the page, and a pause caused by another app is resumed by itself.

## 2026-10-22

### Changed

- Nota is ordered Ta'wiilul Ma'ani, Syariat Khafiah, Khitab Hilaalul Washil, Al Ashlih Asbaabun
  Nuzul, under Subjek Tahun 1 and Subjek Tahun 2.
- Word by word is fetched before Dedah (this card and the next) and kept on the device, so it
  shows at once and works offline after the first time.
- The daily boxes show the real count past the target (for example 14/10, 5/3).

### Added

- Project documentation: README, PRODUCT, DESIGN, CHANGELOG, CLAUDE.md and `docs/`.

## 2026-10-18

### Added

- Kuiz Jilid 7: 200 critical-thinking questions written from the Jilid 7 notes, 2 or 3
  similar-theme ayat as answers, shown in Arabic only. The answer reveals the ayat, maksud,
  Jilid 7 explanation and page reference.
- Streak 🔥 in the mission bar when both daily targets are met.
- "Baca dari ingatan" before Dedah: the phone listens, scores the kalimah heard as a percentage,
  marks Ingat at 80% or more (with 3 s to cancel), and offers one retry below that.
- "Cuba baca" after Dedah as practice.

### Changed

- Daily targets: Kaji 10, Kuiz 3.
- Tabs: Kaji, Kuiz, Progres, Senarai, Nota.
- The past exam countdown box is replaced by the streak.

### Fixed

- The voice check can no longer freeze the page: watchdogs, a forced stop, one reading at a time
  on iPhone, and other audio paused first.

## 2026-10-14 to 2026-10-16

### Added

- Book page reference (Al-Fathun Nawa Jilid 7, ms.) for all 200 falsafah.
- Share for every falsafah: a light image card with songket bands, or text with the app link.
- Saturday popup with last week's Belum ingat and Ingat lists.

### Changed

- Kaji covers the whole julat every day, with plain Ingat and Belum ingat buttons.
- Word by word: the second line is labelled BM, in blue-grey.
- Falsafah 167 title: Bila susah, tunduk; bila senang, lupa.

## 2026-10-13

### Added

- Gred hafalan A+ to G from the last 10 answers, Perlu fokus (C, D, G), a markah list and gred
  badges.
- Day summary after every Kaji round, with Ulang belum ingat and a ribbon at the daily target.
- Range progress on the Kaji card.
- New address falsafah200.vercel.app; the old link shows a moved notice and carries progress over.
- Songket motif on wide screens and in the account menu; Kongsi Falsafah 200 in the menu.

### Changed

- Senarai opens faster on phones.
- iPhone: status bar follows the theme, and tapping search no longer zooms the page.

## 2026-10-11 to 2026-10-12

### Added

- Accounts with username and PIN, Firebase sync across devices, and an admin panel.
- Word by word for all 200 falsafah.
- Progres tab, focus sessions and daily history.
- Dengar: ayat player with murattal, word by word, chosen pause and lock-screen controls.
- Dr. HALO-N's recordings for signed-in students, uploaded by the admin.
- Install to the home screen, first-time tour, link preview image.

### Changed

- Dark theme: warm greys and one softer gold.

## 2026-09

- First version: Kaji, Senarai, Kuiz and Nota in one HTML file, progress in the browser.
