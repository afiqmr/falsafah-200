"""Build index.html from template.html + data.json.

Usage:  python build.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent

template = (ROOT / 'template.html').read_text(encoding='utf-8')
data = json.loads((ROOT / 'data.json').read_text(encoding='utf-8'))

# Escape "</script" so the inlined JSON cannot close its <script> tag early.
data_json = json.dumps(data, ensure_ascii=False).replace('</script', '<\\/script')

assert template.count('__DATA_JSON__') == 1, 'template.html must contain exactly one __DATA_JSON__ placeholder'
(ROOT / 'index.html').write_text(template.replace('__DATA_JSON__', data_json), encoding='utf-8')
print('Built index.html with %d falsafah entries.' % len(data))
