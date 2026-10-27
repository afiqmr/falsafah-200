"""Build index.html (BM) and index_en.html (English) from template.html and the JSON content.

BM:      data.json,    notes.json,    quiz.json
English: data_en.json, notes_en.json (falls back to notes.json if missing), quiz.json with the
         question text from i18n/quiz_en.json
         plus the static text in i18n/en_static.json

Usage:  python build.py   (run build_notes.py first if the exam-note documents changed)
"""
import base64
import json
from pathlib import Path

ROOT = Path(__file__).parent

template = (ROOT / 'template.html').read_text(encoding='utf-8')
logo = 'data:image/png;base64,' + base64.b64encode((ROOT / 'logo-afiq.png').read_bytes()).decode('ascii')


def load(name, fallback=None):
    p = ROOT / name
    if not p.exists() and fallback:
        print('  %s not found, using %s' % (name, fallback))
        p = ROOT / fallback
    return json.loads(p.read_text(encoding='utf-8'))


def inline(obj):
    # Escape "</script" so the inlined JSON cannot close its <script> tag early.
    return json.dumps(obj, ensure_ascii=False).replace('</script', '<\\/script')


def build(lang, out):
    en = lang == 'en'
    data = load('data_en.json' if en else 'data.json')
    notes = load('notes_en.json', 'notes.json') if en else load('notes.json')
    quiz = load('quiz.json')  # from quiz_bank.py
    if en:
        # same answers and distractors; only the question text is English (i18n/quiz_en.json, keyed by falsafah id)
        q_en = load('i18n/quiz_en.json')
        assert len(q_en) == len(quiz) and all(str(q['id']) in q_en for q in quiz), 'i18n/quiz_en.json must have every Kuiz id'
        quiz = [dict(q, q=q_en[str(q['id'])]) for q in quiz]
    html = template
    for placeholder in ('__DATA_JSON__', '__NOTES_JSON__', '__QUIZ_JSON__', '__LOGO_URI__', '__LANG__'):
        assert html.count(placeholder) == 1, 'template.html must contain exactly one %s placeholder' % placeholder
    if en:
        for old, new in json.loads((ROOT / 'i18n' / 'en_static.json').read_text(encoding='utf-8'))['pairs']:
            assert html.count(old) == 1, 'en_static.json: pattern not found once: ' + old[:60]
            html = html.replace(old, new)
        html = html.replace('<title>', '<html lang="en">\n<title>', 1)
    html = (html.replace('__DATA_JSON__', inline(data))
                .replace('__NOTES_JSON__', inline(notes))
                .replace('__QUIZ_JSON__', inline(quiz))
                .replace('__LOGO_URI__', logo)
                .replace('__LANG__', lang))
    (ROOT / out).write_text(html, encoding='utf-8')
    print('Built %s (%s) with %d falsafah entries and %d note topics.' % (out, lang, len(data), len(notes['topics'])))


build('ms', 'index.html')
build('en', 'index_en.html')
