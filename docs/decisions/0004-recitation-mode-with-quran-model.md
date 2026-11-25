# ADR 0004: Recitation mode with a Quran-trained model on the phone (demo)

- Status: Demo, on branch `bacaan-demo` and its own link, not the live app
- Date: 2026-11-25

## Context

ADR 0003 was withdrawn because the phone's everyday speech recogniser scored fluent, correct
readings at 60 to 65%. Its note said a future attempt should use a Quran-trained model.

## Decision

- Use `tarteel-ai/whisper-base-ar-quran` (Whisper base fine-tuned on EveryAyah), in the ONNX int8
  export `iqbalaesthetic/Basira` (encoder 23 MB, decoder 79 MB), run by transformers.js 4.3.2 on
  WASM inside a Web Worker. The library comes from jsDelivr and the model from Hugging Face; both
  are cached by the browser (`transformers-cache`).
- Opt-in per device (`falsafah200_bacaan_v1`, not synced). Off by default. The model is downloaded
  only when the student turns the mode on, and deleted when they turn it off (with a confirm).
- In Kaji with the mode on: recite first (up to 60 s). The model loads while the student recites.
  The transcript is matched with the letter-level matcher from ADR 0003. 70% or more: Ingat. Below
  70%: one more try without seeing the ayat; a second fail: Belum ingat. Nothing heard does not
  count as a try. "Tak boleh baca sekarang" shows Dedah and the usual buttons for that card only.
- Demo counts per device (`falsafah200_bacaan_log_v1`) show in the Mod bacaan sheet.

## Consequences

- No server or cost. The voice stays on the phone.
- About 103 MB of storage and a one-off download. The first check of a session waits while the
  model loads; slow phones may take several seconds per check.
- The model knows the Quran, so it may complete an ayat the student only half recited. The demo
  must test deliberately wrong and partial readings before the pass mark is trusted.
- It checks words, not tajwid. It was trained on professional reciters, so ordinary students may
  score lower.
- iPhone may clear the model when storage runs low; the card then offers to download it again.
