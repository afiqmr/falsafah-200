# ADR 0001: One HTML file built from a template and JSON

- Status: Accepted
- Date: 2026-09

## Context

The app is maintained by one person and used by students on phones of every age, often on
mobile data. It must open fast, work offline once loaded, and be easy to host anywhere.

## Decision

Keep all HTML, CSS and JavaScript in `template.html` with no framework or bundler. Keep the
content in JSON (`data.json`, `quiz.json`, `notes.json`) and inline it with a short Python script
(`build.py`). The output is one self-contained `index.html`.

## Consequences

- Any static host can serve it, and the service worker can cache it as a single file.
- Content editors change JSON or the quiz bank, not code.
- `template.html` is large. Areas are kept in a fixed order with clear section comments (see
  `docs/architecture.md`), and functions are plain and named.
- There is no type checker. Changes are checked by building and walking the screens
  (`docs/testing.md`).
