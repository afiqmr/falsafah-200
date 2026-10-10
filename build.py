"""Build index.html from template.html + data.json + notes.json.

Usage:  python build.py   (run build_notes.py first if the exam-note documents changed)
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent

template = (ROOT / 'template.html').read_text(encoding='utf-8')
data = json.loads((ROOT / 'data.json').read_text(encoding='utf-8'))
notes = json.loads((ROOT / 'notes.json').read_text(encoding='utf-8'))


def inline(obj):
    # Escape "</script" so the inlined JSON cannot close its <script> tag early.
    return json.dumps(obj, ensure_ascii=False).replace('</script', '<\\/script')


for placeholder in ('__DATA_JSON__', '__NOTES_JSON__'):
    assert template.count(placeholder) == 1, 'template.html must contain exactly one %s placeholder' % placeholder
html = template.replace('__DATA_JSON__', inline(data)).replace('__NOTES_JSON__', inline(notes))
(ROOT / 'index.html').write_text(html, encoding='utf-8')
print('Built index.html with %d falsafah entries and %d note topics.' % (len(data), len(notes['topics'])))
