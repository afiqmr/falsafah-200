"""Demo only: writes cloud-test/bacaan-test.html, which runs the recitation model on Quran.com
recordings (full, first half, wrong ayat) and shows the scores, so the model can be checked
without a microphone. Reuses the app's own worker and matcher code from template.html."""
import json, re
t = open('template.html', encoding='utf-8').read()
def grab(start, end):
    a = t.index(start); b = t.index(end, a) + len(end); return t[a:b]
code = '\n'.join([
    "var EN = false; function T(m, e){ return m; }",
    grab("  var BC_MODEL =", "\n"), grab("  var BC_LIB =", "\n"),
    grab("  var BC_WORKER_SRC = [", "].join('\\n');"),
    grab("  function arSkeleton(s){", "\n  }"),
    grab("  function vNorm(w){", "\n  }"), grab("  function vEdit(a, b){", "\n  }"),
    grab("  function voiceMatch(arabic, transcript){", "\n  }"),
    grab("  function bcTo16k(ab){", "\n  }"), grab("  function bcDecode(blob){", "\n  }"),
])
data = json.load(open('data.json', encoding='utf-8'))
pick = [1, 19, 77, 101, 150, 200]
cases = [{'no': e['noStart'], 'key': '%d:%s' % (e['surahNumber'], e['ayahRange']), 'arabic': e['arabic']} for e in data if e['noStart'] in pick and '-' not in e['ayahRange']]
page = """<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Ujian model bacaan</title>
<style>body{font:14px system-ui;margin:16px}td,th{border:1px solid #ccc;padding:4px 6px;font-size:13px}table{border-collapse:collapse}.ar{font-size:15px;direction:rtl}</style>
<h3>Ujian model bacaan (demo)</h3><p id="st">Menunggu…</p><button id="go">Mula ujian</button>
<table id="tb"><tr><th>Falsafah</th><th>Kes</th><th>Saat audio</th><th>Masa semak (ms)</th><th>Skor</th><th>Didengar</th></tr></table>
<script>
""" + code + """
var CASES = """ + json.dumps(cases, ensure_ascii=False) + """;
var w = new Worker(URL.createObjectURL(new Blob([BC_WORKER_SRC], {type:'text/javascript'})), {type:'module'});
var seq = 0, wait = {};
w.onmessage = function(e){ var m = e.data; if(m.type === 'progress'){ if(m.p && m.p.file && m.p.total) st('Muat turun ' + m.p.file + ' ' + Math.round((m.p.loaded||0)/1e6) + '/' + Math.round(m.p.total/1e6) + ' MB'); return; }
  var x = wait[m.id]; if(!x) return; delete wait[m.id]; m.type === 'error' ? x.rej(new Error(m.error)) : x.res(m); };
w.onerror = function(e){ st('WORKER ERROR ' + (e.message || '')); };
function call(msg, tr){ return new Promise(function(res, rej){ var id = ++seq; wait[id] = {res:res, rej:rej}; msg.id = id; w.postMessage(msg, tr || []); }); }
function st(s){ document.getElementById('st').textContent = s; }
function row(c, kase, secs, ms, r, text){ var tr = document.createElement('tr'); tr.innerHTML = '<td>' + c.no + ' (' + c.key + ')</td><td>' + kase + '</td><td>' + secs.toFixed(1) + '</td><td>' + ms + '</td><td>' + r.pct + '% (' + r.ok + '/' + r.total + ')</td><td class="ar">' + text + '</td>'; document.getElementById('tb').appendChild(tr); }
function audioFor(key){ return fetch('https://api.quran.com/api/v4/verses/by_key/' + key + '?audio=5').then(function(r){ return r.json(); }).then(function(j){ var u = j.verse.audio.url; return fetch(/^https?:/.test(u) ? u : (/^\\/\\//.test(u) ? 'https:' + u : 'https://verses.quran.com/' + u)); }).then(function(r){ return r.blob(); }).then(bcDecode); }
async function run(pcm, c, kase){ var t0 = Date.now(); var m = await call({type:'run', audio: pcm}, [pcm.buffer]); var r = voiceMatch(c.arabic, m.text); row(c, kase, pcm.length/16000, Date.now() - t0, r, m.text); return r; }
document.getElementById('go').onclick = async function(){
  try{
    st('Memuatkan model…'); var t0 = Date.now(); await call({type:'load'}); st('Model sedia dalam ' + (Date.now()-t0) + ' ms. Menguji…');
    var pcms = [];
    for(var i = 0; i < CASES.length; i++){ pcms.push(await audioFor(CASES[i].key)); }
    for(i = 0; i < CASES.length; i++){
      var c = CASES[i], p = pcms[i];
      await run(p.slice(), c, 'penuh');
      await run(p.slice(0, Math.floor(p.length/2)), c, 'separuh pertama');
      await run(p.slice(0, Math.floor(p.length/4)), c, 'suku pertama');
      await run(pcms[(i+1) % pcms.length].slice(), c, 'ayat lain');
    }
    st('Selesai.');
  }catch(e){ st('RALAT: ' + (e && e.message || e)); }
};
</script>"""
open('cloud-test/bacaan-test.html', 'w', encoding='utf-8').write(page)
print('cloud-test/bacaan-test.html', len(page))
