import json, re

with open('data.json', encoding='utf-8') as f:
    data = json.load(f)
byid = {e['id']: e for e in data}

# Re-derived on the new Tanzil-derived text. Note: this source splits a few
# words across two whitespace-delimited tokens around the dagger-alif
# (e.g. "وَأَمۡوَ" + "ٰلَهُم"), per its documented rendering convention - the
# ranges below were picked to never cut through the middle of such a pair.
TRIMS = [
    (39, 0, 5),
    (24, 28, 33),
    (77, 1, 12),
    (46, 38, 48),
    (147, 40, 51),
    (61, 11, 21),
    (3, 17, 26),
    (145, 0, 5),
    (64, 21, 30),
    (4, 25, 34),
    (5, 11, 18),
    (25, 8, 14),
    (27, 0, 12),
]

for eid, start, end in TRIMS:
    e = byid[eid]
    # Split into alternating word/separator tokens so the EXACT original
    # inter-word whitespace is preserved (this source uses a special narrow
    # no-break space around the dagger-alif split; a naive ' '.join would
    # silently replace it with a plain space and could subtly break that
    # rendering convention).
    tokens = re.split(r'(\s+)', e['arabic'])
    words_only = tokens[0::2]
    assert len(words_only) == len(e['arabic'].split())
    # tokens layout: word0 sep0 word1 sep1 ... wordN (no trailing sep)
    kept = tokens[2 * start: 2 * end - 1]
    e['arabic'] = ''.join(kept)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Applied {len(TRIMS)} trims.")
for eid, _, _ in TRIMS:
    e = byid[eid]
    print(f"id={eid} {e['rangeLabel']}: {e['arabic']}")

print("\n=== sanity: full-range entries (should be untouched) ===")
for cid in [18, 167]:
    e = byid[cid]
    print(f"id={cid} {e['rangeLabel']} | {e['surahDisplay']}")
    print(f"  TEXT: {e['text']}")
    print(f"  AR:   {e['arabic']}")
