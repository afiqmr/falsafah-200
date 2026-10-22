# ADR 0002: Accounts and sync as a layer added at build time

- Status: Accepted
- Date: 2026-10-11

## Context

Students study on more than one device and the lecturer wants to see class progress. The app
already stored everything in localStorage and worked without any account.

## Decision

Keep the app account-free inside. `build_cloud.py` appends `cloud/cloud_ui.html`, which adds a
username + 6-digit PIN login on Firebase Auth, copies a fixed set of localStorage keys to
`users/{uid}`, and merges local and cloud copies item by item. The app and the layer talk only
through `window.FN_APP`, `window.FN_HALON` and the shared localStorage keys.

## Consequences

- The standalone `index.html` still works with no account and no network.
- New progress data must be added to the synced keys and given a merge rule in `merge()`,
  otherwise it stays on one device.
- Merging is per item (more answers win, lists are unions) so two phones used on the same day do
  not overwrite each other.
- The Firebase web config is public; security comes from the Firestore rules.
