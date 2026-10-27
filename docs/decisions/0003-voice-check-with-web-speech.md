# ADR 0003: Voice check with the browser's speech recogniser

- Status: Withdrawn on 2026-10-27
- Date: 2026-10-18

> Removed from the app. In real use a fluent, correct reading by an experienced reader scored only
> 60 to 65%, even after the letter-swap and idgham fixes, so the score could not be trusted. The
> code remains in Git history (commit `be4bc37`). A future attempt should use a Quran-trained
> speech model rather than the phone's general recogniser.

## Context

Students wanted the app to hear them recite an ayat from memory and tell them whether they got it
right. A dedicated Quran recitation model would need a server and paid hosting.

## Decision

Use the Web Speech API (`ar-SA`) that phones already provide. Compare the transcript with the
ayat letter by letter after removing diacritics and alif, allowing joined, split and slightly
misheard words, in order. Show the result as a percentage of kalimah heard.

Before Dedah, 80% or more marks the card Ingat after 3 seconds, with Batal to undo. Below that the
student retries (2 tries) or grades by hand. Voice never marks Belum ingat. After Dedah, "Cuba
baca" is practice only.

## Consequences

- No server or cost. Works in Chrome on Android and Safari on iPhone; other browsers get a
  message.
- It checks words, not tajwid. The recogniser is trained on everyday speech, so slow murattal and
  long ayat can lose words; the 80% bar and "never auto-fail" absorb this.
- The student's voice goes to Google or Apple while listening. Students are told it is a word
  check, and it only runs when they press the button.
- Every step has a watchdog so a silent recogniser can never freeze the page.
