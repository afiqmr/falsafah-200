(function(){
  var h = location.hash, m = /^#bawa=([A-Za-z0-9_-]+)$/.exec(h);
  if(!m) return;
  try{ history.replaceState(null, '', location.pathname + location.search); }catch(e){}
  try{
    var b = m[1].replace(/-/g, '+').replace(/_/g, '/'); while(b.length % 4) b += '=';
    var bin = atob(b), bytes = new Uint8Array(bin.length);
    for(var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    var d = JSON.parse(new TextDecoder().decode(bytes));
    if(!d || d.v !== 1) return;
    var get = function(k){ try{ return JSON.parse(localStorage.getItem(k) || 'null'); }catch(e){ return null; } };
    var put = function(k, v){ localStorage.setItem(k, typeof v === 'string' ? v : JSON.stringify(v)); };
    var better = function(a, b){ if(!a) return b; if(!b) return a;
      if((a.seen||0) !== (b.seen||0)) return (a.seen||0) > (b.seen||0) ? a : b;
      if((a.box||0) !== (b.box||0)) return (a.box||0) > (b.box||0) ? a : b;
      return (a.due||'') >= (b.due||'') ? a : b; };
    var n = 0;
    if(d.srs){
      var loc = get('falsafah200_srs_v1') || {}, out = {};
      Object.keys(loc).concat(Object.keys(d.srs)).forEach(function(id){ out[id] = better(loc[id], d.srs[id]); });
      n = Object.keys(d.srs).length;
      // the old link already moved its progress to the 200 falsafah numbers
      if(!localStorage.getItem('falsafah200_ids_v2')) put('falsafah200_ids_v2', '1');
      put('falsafah200_srs_v1', out);
    }
    if(d.daily){
      var ld = get('falsafah200_daily_v1');
      if(!ld || (d.daily.date || '') > (ld.date || '')) put('falsafah200_daily_v1', d.daily);
    }
    if(d.range && !localStorage.getItem('falsafah200_range_v1')) put('falsafah200_range_v1', d.range);
    if(d.username && !localStorage.getItem('falsafah200_username_v1')) put('falsafah200_username_v1', d.username);
    if(d.theme && !localStorage.getItem('falsafah200_theme_v1')) put('falsafah200_theme_v1', d.theme);
    if(n) sessionStorage.setItem('fn_imported', String(n));
  }catch(e){}
})();
