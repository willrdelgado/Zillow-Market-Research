import json, os

with open('/sessions/kind-beautiful-rubin/master_data.json') as f:
    data = json.load(f)
data_json = json.dumps(data, separators=(',',':'))

html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ZHVI Real Estate Intelligence</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
:root{
  --bg:#08111f;--surf:#0f1e35;--surf2:#162848;--surf3:#1c3255;
  --bdr:rgba(255,255,255,.07);--bdr2:rgba(255,255,255,.12);
  --tx:#dde6f0;--txm:#7a90a8;--txd:#4a607a;
  --ac:#5b8ff9;--ac2:#7c6cf5;--acg:linear-gradient(135deg,#5b8ff9,#7c6cf5);
  --hot:#ef4444;--hotb:rgba(239,68,68,.13);--hotbd:rgba(239,68,68,.32);
  --warm:#f97316;--warmb:rgba(249,115,22,.13);--warmbd:rgba(249,115,22,.32);
  --slow:#eab308;--slowb:rgba(234,179,8,.13);--slowbd:rgba(234,179,8,.32);
  --cool:#3b82f6;--coolb:rgba(59,130,246,.13);--coolbd:rgba(59,130,246,.32);
  --cold:#06b6d4;--coldb:rgba(6,182,212,.13);--coldbd:rgba(6,182,212,.32);
  --pos:#34d399;--neg:#f87171;
  --nav-w:240px;--nav-collapsed:60px;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,"Inter","Segoe UI",sans-serif;background:var(--bg);color:var(--tx);min-height:100vh;font-size:13px;overflow:hidden}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--surf3);border-radius:3px}

/* ── APP SHELL ── */
.app{display:flex;height:100vh;overflow:hidden}

/* ── LEFT NAV ── */
.nav{width:var(--nav-w);min-width:var(--nav-w);background:var(--surf);border-right:1px solid var(--bdr);display:flex;flex-direction:column;transition:width .25s ease,min-width .25s ease;overflow:hidden;z-index:50}
.nav.collapsed{width:var(--nav-collapsed);min-width:var(--nav-collapsed)}
.nav-header{padding:16px 16px 12px;display:flex;align-items:center;gap:10px;border-bottom:1px solid var(--bdr);flex-shrink:0}
.nav-logo{width:32px;height:32px;background:var(--acg);border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0;box-shadow:0 0 14px rgba(91,143,249,.35)}
.nav-brand{white-space:nowrap;overflow:hidden}
.nav-brand h2{font-size:13px;font-weight:700;letter-spacing:-.3px}
.nav-brand p{font-size:10px;color:var(--txm);margin-top:1px}
.nav-toggle{margin-left:auto;background:none;border:none;color:var(--txm);cursor:pointer;padding:4px;border-radius:6px;transition:all .2s;font-size:14px;flex-shrink:0}
.nav-toggle:hover{background:var(--surf2);color:var(--tx)}
.nav-scroll{flex:1;overflow-y:auto;overflow-x:hidden;padding:10px 8px}
.nav-section-label{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:1.2px;color:var(--txd);padding:12px 8px 5px;white-space:nowrap;overflow:hidden}
.nav-item{display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:9px;cursor:pointer;transition:all .18s;margin-bottom:2px;white-space:nowrap;border:1px solid transparent;position:relative}
.nav-item:hover{background:var(--surf2)}
.nav-item.active{background:rgba(91,143,249,.15);border-color:rgba(91,143,249,.25)}
.nav-item.active .nav-icon,.nav-item.active .nav-label{color:var(--ac)}
.nav-icon{font-size:16px;flex-shrink:0;width:20px;text-align:center}
.nav-label{font-size:12px;font-weight:500;color:var(--txm);overflow:hidden;transition:opacity .2s}
.nav.collapsed .nav-label,.nav.collapsed .nav-section-label,.nav.collapsed .nav-brand{opacity:0;width:0;pointer-events:none}
.nav-item.zip-active{background:rgba(52,211,153,.1);border-color:rgba(52,211,153,.25)}
.nav-item.zip-active .nav-icon,.nav-item.zip-active .nav-label{color:var(--pos)}
.nav-divider{height:1px;background:var(--bdr);margin:8px 0}

/* ── MAIN CONTENT ── */
.main{flex:1;display:flex;flex-direction:column;overflow:hidden;min-width:0}

/* ── TOPBAR ── */
.topbar{background:var(--surf);border-bottom:1px solid var(--bdr);padding:12px 20px;display:flex;align-items:center;gap:12px;flex-shrink:0}
.topbar h1{font-size:15px;font-weight:700;letter-spacing:-.4px}
.topbar p{font-size:11px;color:var(--txm)}
.topbar-right{margin-left:auto;display:flex;align-items:center;gap:8px}
.pill{background:var(--surf2);border:1px solid var(--bdr);border-radius:7px;padding:4px 10px;font-size:11px;color:var(--txm)}
.pill span{color:var(--tx);font-weight:600}

/* ── FILTER BAR ── */
.filter-bar{background:var(--surf);border-bottom:1px solid var(--bdr);padding:10px 20px;display:flex;align-items:center;gap:8px;flex-wrap:wrap;flex-shrink:0}
.filter-bar input,.filter-bar select{background:var(--surf2);border:1px solid var(--bdr);border-radius:8px;padding:6px 10px;color:var(--tx);font-size:12px;outline:none;transition:border-color .2s,box-shadow .2s}
.filter-bar input:focus,.filter-bar select:focus{border-color:var(--ac);box-shadow:0 0 0 2px rgba(91,143,249,.15)}
.filter-bar select{appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'%3E%3Cpath fill='%237a90a8' d='M5 7L1 3h8z'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 8px center;padding-right:24px}
.filter-bar select option{background:#162848}
.search-wrap{position:relative}
.search-wrap input{padding-left:28px;min-width:180px}
.search-wrap .si{position:absolute;left:8px;top:50%;transform:translateY(-50%);color:var(--txm);font-size:13px;pointer-events:none}
.reset-btn{background:var(--surf2);border:1px solid var(--bdr);border-radius:8px;padding:6px 12px;color:var(--txm);font-size:11px;cursor:pointer;transition:all .2s;white-space:nowrap}
.reset-btn:hover{border-color:var(--ac);color:var(--ac)}
.filter-bar .spacer{flex:1}

/* TEMP FILTER chips */
.temp-chips{display:flex;gap:4px}
.chip{display:inline-flex;align-items:center;gap:4px;padding:4px 9px;border-radius:20px;font-size:10px;font-weight:700;cursor:pointer;border:1px solid transparent;transition:all .18s;opacity:.45;text-transform:uppercase;letter-spacing:.5px}
.chip.on{opacity:1}
.chip-hot{background:var(--hotb);color:var(--hot);border-color:var(--hotbd)}
.chip-warm{background:var(--warmb);color:var(--warm);border-color:var(--warmbd)}
.chip-slow{background:var(--slowb);color:var(--slow);border-color:var(--slowbd)}
.chip-cool{background:var(--coolb);color:var(--cool);border-color:var(--coolbd)}
.chip-cold{background:var(--coldb);color:var(--cold);border-color:var(--coldbd)}

/* ── CONTENT AREA ── */
.content-area{flex:1;display:flex;flex-direction:column;overflow:hidden}
.section-view{display:none;flex:1;flex-direction:column;overflow:hidden}
.section-view.active{display:flex}

/* ── TABLE ── */
.table-toolbar{padding:9px 20px;display:flex;align-items:center;gap:10px;border-bottom:1px solid var(--bdr);background:var(--surf);flex-wrap:wrap;flex-shrink:0}
.rc{font-size:11px;color:var(--txm)}.rc span{color:var(--tx);font-weight:600}
.sort-group{display:flex;gap:4px;margin-left:auto;align-items:center}
.sort-lbl{font-size:10px;color:var(--txd)}
.sbtn{background:var(--surf2);border:1px solid var(--bdr);border-radius:6px;padding:4px 9px;color:var(--txm);font-size:10px;font-weight:600;cursor:pointer;transition:all .18s}
.sbtn:hover{border-color:var(--ac);color:var(--tx)}
.sbtn.on{background:rgba(91,143,249,.15);border-color:var(--ac);color:var(--ac)}
.spark-group{display:flex;gap:3px;align-items:center}
.spark-lbl{font-size:10px;color:var(--txd)}
.spr-btn{background:var(--surf2);border:1px solid var(--bdr);border-radius:5px;padding:3px 7px;color:var(--txm);font-size:10px;font-weight:600;cursor:pointer;transition:all .18s}
.spr-btn:hover{color:var(--tx);border-color:var(--ac)}
.spr-btn.on{background:rgba(91,143,249,.15);border-color:var(--ac);color:var(--ac)}

.table-wrap{flex:1;overflow-y:auto;overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:12px}
thead{background:var(--surf2);position:sticky;top:0;z-index:10}
th{padding:9px 13px;text-align:left;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.8px;color:var(--txm);border-bottom:1px solid var(--bdr);white-space:nowrap;cursor:pointer;user-select:none;transition:color .18s}
th:hover{color:var(--tx)}
th.sorted{color:var(--ac)}
.sa{opacity:.4;margin-left:2px}
th.sorted .sa{opacity:1}
tbody tr{border-bottom:1px solid var(--bdr);transition:background .12s;cursor:pointer}
tbody tr:hover{background:var(--surf2)}
td{padding:9px 13px;vertical-align:middle;white-space:nowrap}

.zipcode{font-family:"SF Mono","Fira Code",monospace;font-weight:700;color:var(--ac);font-size:12px}
.city{font-weight:500}
.st-tag{background:var(--surf3);padding:1px 5px;border-radius:4px;font-size:10px;color:var(--txm);margin-left:3px}
.val-bold{font-weight:700;font-size:13px}
.pos{color:var(--pos)}.neg{color:var(--neg)}.neu{color:var(--txm)}
canvas.spark{display:block}

/* ── TEMP BADGE ── */
.badge{display:inline-flex;align-items:center;gap:3px;padding:3px 8px;border-radius:20px;font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.5px}
.bdot{width:5px;height:5px;border-radius:50%}
.b-hot{background:var(--hotb);color:var(--hot);border:1px solid var(--hotbd)}
.b-hot .bdot{background:var(--hot)}
.b-warm{background:var(--warmb);color:var(--warm);border:1px solid var(--warmbd)}
.b-warm .bdot{background:var(--warm)}
.b-slow{background:var(--slowb);color:var(--slow);border:1px solid var(--slowbd)}
.b-slow .bdot{background:var(--slow)}
.b-cool{background:var(--coolb);color:var(--cool);border:1px solid var(--coolbd)}
.b-cool .bdot{background:var(--cool)}
.b-cold{background:var(--coldb);color:var(--cold);border:1px solid var(--coldbd)}
.b-cold .bdot{background:var(--cold)}

/* ── PAGINATION ── */
.pager{padding:8px 20px;display:flex;align-items:center;justify-content:center;gap:4px;border-top:1px solid var(--bdr);background:var(--surf);flex-shrink:0}
.pgb{background:var(--surf2);border:1px solid var(--bdr);border-radius:6px;padding:4px 9px;color:var(--txm);font-size:11px;cursor:pointer;transition:all .18s;min-width:30px;text-align:center}
.pgb:hover:not(:disabled){border-color:var(--ac);color:var(--tx)}
.pgb.on{background:var(--ac);border-color:var(--ac);color:#fff;font-weight:700}
.pgb:disabled{opacity:.3;cursor:default}
.pgi{font-size:10px;color:var(--txm);padding:0 5px}

/* ── NATIONAL VIEW ── */
.national-view{flex:1;display:flex;align-items:center;justify-content:center;padding:40px}
.nat-card{background:var(--surf2);border:1px solid var(--bdr);border-radius:16px;padding:32px;max-width:600px;width:100%}
.nat-header{text-align:center;margin-bottom:28px}
.nat-header h2{font-size:22px;font-weight:800}
.nat-header p{color:var(--txm);margin-top:6px;font-size:13px}
.nat-metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:24px}
.nat-metric{background:var(--surf3);border:1px solid var(--bdr);border-radius:11px;padding:16px;text-align:center}
.nat-ml{font-size:10px;color:var(--txm);text-transform:uppercase;letter-spacing:.8px;margin-bottom:8px}
.nat-mv{font-size:26px;font-weight:800;color:var(--pos)}
.nat-ms{font-size:11px;color:var(--txm);margin-top:3px}
.nat-note{text-align:center;font-size:11px;color:var(--txd);background:var(--surf);border:1px solid var(--bdr);border-radius:8px;padding:12px;margin-top:8px}

/* ── ZIP PROFILE PANEL ── */
.profile-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.7);backdrop-filter:blur(12px);z-index:300;align-items:flex-start;justify-content:flex-end}
.profile-overlay.open{display:flex}
.profile-panel{width:680px;max-width:97vw;height:100vh;background:var(--surf);border-left:1px solid var(--bdr);overflow-y:auto;display:flex;flex-direction:column;box-shadow:-20px 0 50px rgba(0,0,0,.4)}
.profile-panel::-webkit-scrollbar{width:4px}
.pp-header{padding:20px 24px 16px;background:linear-gradient(135deg,#0f172a,#1e1b4b);border-bottom:1px solid var(--bdr);flex-shrink:0;position:sticky;top:0;z-index:10}
.pp-close{position:absolute;top:16px;right:16px;background:var(--surf2);border:1px solid var(--bdr);border-radius:8px;width:28px;height:28px;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:14px;color:var(--txm);transition:all .2s}
.pp-close:hover{color:var(--tx);border-color:var(--bdr2)}
.pp-zip{font-size:32px;font-weight:900;color:var(--ac);font-family:"SF Mono","Fira Code",monospace;letter-spacing:-1px}
.pp-loc{font-size:13px;color:var(--txm);margin-top:3px}
.pp-metro{font-size:11px;color:var(--txd);margin-top:2px}
.pp-body{padding:20px 24px;flex:1}
.pp-tabs{display:flex;gap:2px;margin-bottom:18px;background:var(--surf2);border:1px solid var(--bdr);border-radius:10px;padding:3px}
.pp-tab{flex:1;padding:7px 4px;text-align:center;font-size:11px;font-weight:600;color:var(--txm);cursor:pointer;border-radius:8px;transition:all .18s;white-space:nowrap}
.pp-tab:hover{color:var(--tx)}
.pp-tab.active{background:var(--surf3);color:var(--ac);box-shadow:0 1px 4px rgba(0,0,0,.3)}
.pp-pane{display:none}.pp-pane.active{display:block}

/* PP metrics grid */
.pp-metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:18px}
.ppm{background:var(--surf2);border:1px solid var(--bdr);border-radius:10px;padding:12px 14px}
.ppm-l{font-size:10px;color:var(--txm);text-transform:uppercase;letter-spacing:.7px;margin-bottom:4px}
.ppm-v{font-size:18px;font-weight:700}
.ppm-s{font-size:10px;color:var(--txd);margin-top:2px}

/* PP chart */
.pp-chart-box{background:var(--surf2);border:1px solid var(--bdr);border-radius:11px;padding:14px;margin-bottom:14px}
.pp-chart-hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
.pp-chart-title{font-size:10px;color:var(--txm);text-transform:uppercase;letter-spacing:.8px;font-weight:600}
.tr-btns{display:flex;gap:3px}
.trb{background:var(--surf3);border:1px solid var(--bdr);border-radius:5px;padding:3px 8px;color:var(--txm);font-size:10px;font-weight:600;cursor:pointer;transition:all .18s}
.trb:hover{border-color:var(--ac);color:var(--tx)}
.trb.on{background:rgba(91,143,249,.2);border-color:var(--ac);color:var(--ac)}

/* PP forecast badges */
.fcst-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.fcst-card{background:var(--surf2);border:1px solid var(--bdr);border-radius:10px;padding:14px;text-align:center}
.fcst-period{font-size:9px;color:var(--txm);text-transform:uppercase;letter-spacing:.8px;margin-bottom:6px}
.fcst-val{font-size:22px;font-weight:800}
.fcst-lbl{font-size:10px;color:var(--txd);margin-top:3px}

/* PP metro charts grid */
.metro-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.metro-mini{background:var(--surf2);border:1px solid var(--bdr);border-radius:10px;padding:12px}
.metro-mini-title{font-size:10px;color:var(--txm);text-transform:uppercase;letter-spacing:.7px;margin-bottom:4px;font-weight:600}
.metro-mini-val{font-size:16px;font-weight:700;margin-bottom:6px}
.metro-mini-sub{font-size:10px;color:var(--txd)}
.no-data{color:var(--txd);font-size:12px;font-style:italic;text-align:center;padding:20px}

/* ZHVF table forecast cols */
.fcol-pos{color:var(--pos);font-weight:600}
.fcol-neg{color:var(--neg);font-weight:600}
.fcol-neu{color:var(--txm)}

/* Empty state */
.empty{padding:50px;text-align:center;color:var(--txm)}
.empty h3{font-size:16px;margin-bottom:6px;color:var(--tx)}
</style>
</head>
<body>
<div class="app">

<!-- ── LEFT NAV ── -->
<nav class="nav" id="nav">
  <div class="nav-header">
    <div class="nav-logo">🏠</div>
    <div class="nav-brand">
      <h2>ZHVI Intelligence</h2>
      <p>Real Estate Analytics</p>
    </div>
    <button class="nav-toggle" onclick="toggleNav()" title="Collapse">☰</button>
  </div>
  <div class="nav-scroll">
    <div class="nav-section-label">ZIP-LEVEL DATA</div>
    <div class="nav-item active" id="nav-zhvi" onclick="setSection('zhvi')"><span class="nav-icon">🏠</span><span class="nav-label">Home Values</span></div>
    <div class="nav-item" id="nav-zhvf" onclick="setSection('zhvf')"><span class="nav-icon">📈</span><span class="nav-label">Value Forecast</span></div>
    <div class="nav-item" id="nav-zori" onclick="setSection('zori')"><span class="nav-icon">🏘</span><span class="nav-label">Rentals (ZORI)</span></div>
    <div class="nav-divider"></div>
    <div class="nav-section-label">METRO-LEVEL DATA</div>
    <div class="nav-item" id="nav-mkt" onclick="setSection('mkt')"><span class="nav-icon">🌡</span><span class="nav-label">Market Temp Index</span></div>
    <div class="nav-item" id="nav-invt" onclick="setSection('invt')"><span class="nav-icon">🏗</span><span class="nav-label">For Sale Inventory</span></div>
    <div class="nav-item" id="nav-sales" onclick="setSection('sales')"><span class="nav-icon">📊</span><span class="nav-label">Sales Activity</span></div>
    <div class="nav-item" id="nav-newcon" onclick="setSection('newcon')"><span class="nav-icon">🔨</span><span class="nav-label">New Construction</span></div>
    <div class="nav-item" id="nav-doz" onclick="setSection('doz')"><span class="nav-icon">⏱</span><span class="nav-label">Days on Market</span></div>
    <div class="nav-item" id="nav-income" onclick="setSection('income')"><span class="nav-icon">💵</span><span class="nav-label">Income Needed</span></div>
    <div class="nav-divider"></div>
    <div class="nav-section-label">NATIONAL</div>
    <div class="nav-item" id="nav-zorf" onclick="setSection('zorf')"><span class="nav-icon">📉</span><span class="nav-label">Rental Forecast</span></div>
    <div class="nav-divider"></div>
    <div class="nav-item" id="nav-profile" onclick="openProfileFromNav()" style="display:none">
      <span class="nav-icon">📍</span><span class="nav-label" id="nav-profile-label">ZIP Profile</span>
    </div>
  </div>
</nav>

<!-- ── MAIN ── -->
<div class="main">

  <!-- TOPBAR -->
  <div class="topbar">
    <div>
      <h1 id="section-title">Home Values (ZHVI)</h1>
      <p id="section-desc">Zillow Home Value Index · Single Family + Condo · Middle Tier · 2000–Feb 2026</p>
    </div>
    <div class="topbar-right">
      <div class="pill">Latest: <span>Feb 2026</span></div>
      <div class="pill">Showing <span id="count-pill">—</span></div>
    </div>
  </div>

  <!-- FILTER BAR -->
  <div class="filter-bar" id="filter-bar">
    <div class="search-wrap">
      <span class="si">🔍</span>
      <input type="text" id="fi-search" placeholder="Search zip, city, metro…" oninput="onSearch()">
    </div>
    <select id="fi-state" onchange="onStateChange()"><option value="">All States</option></select>
    <select id="fi-city" disabled onchange="applyFilters()"><option value="">All Cities</option></select>
    <select id="fi-value" onchange="applyFilters()" style="display:none"><option value="">Any Price</option><option value="0-200000">Under $200K</option><option value="200000-400000">$200K–$400K</option><option value="400000-600000">$400K–$600K</option><option value="600000-1000000">$600K–$1M</option><option value="1000000-9999999">$1M+</option></select>
    <div class="temp-chips" id="temp-chips" style="display:none">
      <div class="chip chip-hot on" data-t="hot" onclick="toggleChip('hot')">🔥 Hot</div>
      <div class="chip chip-warm on" data-t="warm" onclick="toggleChip('warm')">☀️ Warm</div>
      <div class="chip chip-slow on" data-t="slow" onclick="toggleChip('slow')">🌤 Slow</div>
      <div class="chip chip-cool on" data-t="cooling" onclick="toggleChip('cooling')">🌧 Cool</div>
      <div class="chip chip-cold on" data-t="cold" onclick="toggleChip('cold')">❄️ Cold</div>
    </div>
    <div class="spacer"></div>
    <button class="reset-btn" onclick="resetFilters()">↺ Reset</button>
  </div>

  <!-- CONTENT AREA -->
  <div class="content-area">

    <!-- ZHVI -->
    <div class="section-view active" id="sv-zhvi">
      <div class="table-toolbar">
        <div class="rc">Showing <span id="rc-zhvi">0</span> zip codes</div>
        <div class="spark-group">
          <span class="spark-lbl">TREND:</span>
          <button class="spr-btn on" id="zhvi-spr-1y" onclick="setZhviSpark('1y')">1Y</button>
          <button class="spr-btn" id="zhvi-spr-3y" onclick="setZhviSpark('3y')">3Y</button>
          <button class="spr-btn" id="zhvi-spr-all" onclick="setZhviSpark('all')">2000→</button>
        </div>
        <div class="sort-group">
          <span class="sort-lbl">SORT:</span>
          <button class="sbtn on" id="zhvi-sort-yoy" onclick="zhviSort('yoy')">YoY%</button>
          <button class="sbtn" id="zhvi-sort-value" onclick="zhviSort('value')">Value</button>
          <button class="sbtn" id="zhvi-sort-zip" onclick="zhviSort('zip')">Zip</button>
        </div>
      </div>
      <div class="table-wrap">
        <table><thead><tr>
          <th onclick="zhviSort('zip')">ZIP<span class="sa">↕</span></th>
          <th onclick="zhviSort('city')">City<span class="sa">↕</span></th>
          <th>ST</th><th>County</th>
          <th onclick="zhviSort('temp')">Market<span class="sa">↕</span></th>
          <th onclick="zhviSort('value')">Median Value<span class="sa">↕</span></th>
          <th onclick="zhviSort('yoy')">YoY %<span class="sa">↕</span></th>
          <th onclick="zhviSort('mo6')">6-Mo %<span class="sa">↕</span></th>
          <th onclick="zhviSort('yr3')">3-Yr %<span class="sa">↕</span></th>
          <th id="zhvi-spark-hdr">Trend (1Y)</th>
        </tr></thead>
        <tbody id="tb-zhvi"></tbody></table>
        <div id="es-zhvi" class="empty" style="display:none"><h3>No results</h3><p>Adjust your filters</p></div>
      </div>
      <div class="pager" id="pg-zhvi"></div>
    </div>

    <!-- ZHVF -->
    <div class="section-view" id="sv-zhvf">
      <div class="table-toolbar">
        <div class="rc">Showing <span id="rc-zhvf">0</span> zip codes</div>
        <div class="sort-group"><span class="sort-lbl">SORT:</span>
          <button class="sbtn on" id="zhvf-sort-f12" onclick="zhvfSort('f12')">12-Mo Fcst</button>
          <button class="sbtn" id="zhvf-sort-f3" onclick="zhvfSort('f3')">3-Mo Fcst</button>
          <button class="sbtn" id="zhvf-sort-f1" onclick="zhvfSort('f1')">1-Mo Fcst</button>
          <button class="sbtn" id="zhvf-sort-zip" onclick="zhvfSort('zip')">Zip</button>
        </div>
      </div>
      <div class="table-wrap">
        <table><thead><tr>
          <th onclick="zhvfSort('zip')">ZIP<span class="sa">↕</span></th>
          <th onclick="zhvfSort('city')">City<span class="sa">↕</span></th>
          <th>ST</th><th>County</th><th>Metro</th>
          <th onclick="zhvfSort('f1')">+1 Mo<span class="sa">↕</span></th>
          <th onclick="zhvfSort('f3')">+3 Mo<span class="sa">↕</span></th>
          <th onclick="zhvfSort('f12')">+12 Mo<span class="sa">↕</span></th>
        </tr></thead>
        <tbody id="tb-zhvf"></tbody></table>
        <div id="es-zhvf" class="empty" style="display:none"><h3>No results</h3></div>
      </div>
      <div class="pager" id="pg-zhvf"></div>
    </div>

    <!-- ZORI -->
    <div class="section-view" id="sv-zori">
      <div class="table-toolbar">
        <div class="rc">Showing <span id="rc-zori">0</span> zip codes</div>
        <div class="spark-group">
          <span class="spark-lbl">TREND:</span>
          <button class="spr-btn on" id="zori-spr-1y" onclick="setZoriSpark('1y')">1Y</button>
          <button class="spr-btn" id="zori-spr-3y" onclick="setZoriSpark('3y')">3Y</button>
          <button class="spr-btn" id="zori-spr-all" onclick="setZoriSpark('all')">2015→</button>
        </div>
        <div class="sort-group"><span class="sort-lbl">SORT:</span>
          <button class="sbtn on" id="zori-sort-yoy" onclick="zoriSort('yoy')">YoY%</button>
          <button class="sbtn" id="zori-sort-rent" onclick="zoriSort('rent')">Rent</button>
          <button class="sbtn" id="zori-sort-zip" onclick="zoriSort('zip')">Zip</button>
        </div>
      </div>
      <div class="table-wrap">
        <table><thead><tr>
          <th onclick="zoriSort('zip')">ZIP<span class="sa">↕</span></th>
          <th onclick="zoriSort('city')">City<span class="sa">↕</span></th>
          <th>ST</th><th>County</th>
          <th onclick="zoriSort('rent')">Monthly Rent<span class="sa">↕</span></th>
          <th onclick="zoriSort('yoy')">YoY %<span class="sa">↕</span></th>
          <th onclick="zoriSort('mo6')">6-Mo %<span class="sa">↕</span></th>
          <th id="zori-spark-hdr">Trend (1Y)</th>
        </tr></thead>
        <tbody id="tb-zori"></tbody></table>
        <div id="es-zori" class="empty" style="display:none"><h3>No results</h3></div>
      </div>
      <div class="pager" id="pg-zori"></div>
    </div>

    <!-- METRO: MKT TEMP -->
    <div class="section-view" id="sv-mkt">
      <div class="table-toolbar">
        <div class="rc">Showing <span id="rc-mkt">0</span> metros</div>
        <div class="sort-group"><span class="sort-lbl">SORT:</span>
          <button class="sbtn on" id="mkt-sort-val" onclick="metroSort('mkt','temp_idx')">Index</button>
          <button class="sbtn" id="mkt-sort-yoy" onclick="metroSort('mkt','yoy')">YoY%</button>
          <button class="sbtn" id="mkt-sort-name" onclick="metroSort('mkt','name')">Name</button>
        </div>
      </div>
      <div class="table-wrap">
        <table><thead><tr>
          <th onclick="metroSort('mkt','name')">Metro Area<span class="sa">↕</span></th>
          <th>State</th>
          <th onclick="metroSort('mkt','temp_idx')">Temp Index<span class="sa">↕</span></th>
          <th onclick="metroSort('mkt','yoy')">YoY %<span class="sa">↕</span></th>
          <th onclick="metroSort('mkt','mo6')">6-Mo %<span class="sa">↕</span></th>
          <th>12-Mo Trend</th>
        </tr></thead>
        <tbody id="tb-mkt"></tbody></table>
        <div id="es-mkt" class="empty" style="display:none"><h3>No results</h3></div>
      </div>
      <div class="pager" id="pg-mkt"></div>
    </div>

    <!-- METRO: INVENTORY -->
    <div class="section-view" id="sv-invt">
      <div class="table-toolbar">
        <div class="rc">Showing <span id="rc-invt">0</span> metros</div>
        <div class="sort-group"><span class="sort-lbl">SORT:</span>
          <button class="sbtn on" id="invt-sort-val" onclick="metroSort('invt','invt')">Inventory</button>
          <button class="sbtn" id="invt-sort-yoy" onclick="metroSort('invt','yoy')">YoY%</button>
          <button class="sbtn" id="invt-sort-name" onclick="metroSort('invt','name')">Name</button>
        </div>
      </div>
      <div class="table-wrap">
        <table><thead><tr>
          <th onclick="metroSort('invt','name')">Metro Area<span class="sa">↕</span></th><th>State</th>
          <th onclick="metroSort('invt','invt')">Listings<span class="sa">↕</span></th>
          <th onclick="metroSort('invt','yoy')">YoY %<span class="sa">↕</span></th>
          <th onclick="metroSort('invt','mo6')">6-Mo %<span class="sa">↕</span></th><th>12-Mo Trend</th>
        </tr></thead><tbody id="tb-invt"></tbody></table>
        <div id="es-invt" class="empty" style="display:none"><h3>No results</h3></div>
      </div>
      <div class="pager" id="pg-invt"></div>
    </div>

    <!-- METRO: SALES -->
    <div class="section-view" id="sv-sales">
      <div class="table-toolbar">
        <div class="rc">Showing <span id="rc-sales">0</span> metros</div>
        <div class="sort-group"><span class="sort-lbl">SORT:</span>
          <button class="sbtn on" id="sales-sort-val" onclick="metroSort('sales','sales')">Sales Count</button>
          <button class="sbtn" id="sales-sort-yoy" onclick="metroSort('sales','yoy')">YoY%</button>
          <button class="sbtn" id="sales-sort-name" onclick="metroSort('sales','name')">Name</button>
        </div>
      </div>
      <div class="table-wrap">
        <table><thead><tr>
          <th onclick="metroSort('sales','name')">Metro Area<span class="sa">↕</span></th><th>State</th>
          <th onclick="metroSort('sales','sales')">Sales Count<span class="sa">↕</span></th>
          <th onclick="metroSort('sales','yoy')">YoY %<span class="sa">↕</span></th>
          <th onclick="metroSort('sales','mo6')">6-Mo %<span class="sa">↕</span></th><th>12-Mo Trend</th>
        </tr></thead><tbody id="tb-sales"></tbody></table>
        <div id="es-sales" class="empty" style="display:none"><h3>No results</h3></div>
      </div>
      <div class="pager" id="pg-sales"></div>
    </div>

    <!-- METRO: NEW CON -->
    <div class="section-view" id="sv-newcon">
      <div class="table-toolbar">
        <div class="rc">Showing <span id="rc-newcon">0</span> metros</div>
        <div class="sort-group"><span class="sort-lbl">SORT:</span>
          <button class="sbtn on" id="newcon-sort-val" onclick="metroSort('newcon','new_con')">New Con Sales</button>
          <button class="sbtn" id="newcon-sort-yoy" onclick="metroSort('newcon','yoy')">YoY%</button>
          <button class="sbtn" id="newcon-sort-name" onclick="metroSort('newcon','name')">Name</button>
        </div>
      </div>
      <div class="table-wrap">
        <table><thead><tr>
          <th onclick="metroSort('newcon','name')">Metro Area<span class="sa">↕</span></th><th>State</th>
          <th onclick="metroSort('newcon','new_con')">New Con Sales<span class="sa">↕</span></th>
          <th onclick="metroSort('newcon','yoy')">YoY %<span class="sa">↕</span></th>
          <th onclick="metroSort('newcon','mo6')">6-Mo %<span class="sa">↕</span></th><th>12-Mo Trend</th>
        </tr></thead><tbody id="tb-newcon"></tbody></table>
        <div id="es-newcon" class="empty" style="display:none"><h3>No results</h3></div>
      </div>
      <div class="pager" id="pg-newcon"></div>
    </div>

    <!-- METRO: DOZ -->
    <div class="section-view" id="sv-doz">
      <div class="table-toolbar">
        <div class="rc">Showing <span id="rc-doz">0</span> metros</div>
        <div class="sort-group"><span class="sort-lbl">SORT:</span>
          <button class="sbtn on" id="doz-sort-val" onclick="metroSort('doz','doz')">Days</button>
          <button class="sbtn" id="doz-sort-yoy" onclick="metroSort('doz','yoy')">YoY%</button>
          <button class="sbtn" id="doz-sort-name" onclick="metroSort('doz','name')">Name</button>
        </div>
      </div>
      <div class="table-wrap">
        <table><thead><tr>
          <th onclick="metroSort('doz','name')">Metro Area<span class="sa">↕</span></th><th>State</th>
          <th onclick="metroSort('doz','doz')">Avg Days Pending<span class="sa">↕</span></th>
          <th onclick="metroSort('doz','yoy')">YoY %<span class="sa">↕</span></th>
          <th onclick="metroSort('doz','mo6')">6-Mo %<span class="sa">↕</span></th><th>12-Mo Trend</th>
        </tr></thead><tbody id="tb-doz"></tbody></table>
        <div id="es-doz" class="empty" style="display:none"><h3>No results</h3></div>
      </div>
      <div class="pager" id="pg-doz"></div>
    </div>

    <!-- METRO: INCOME -->
    <div class="section-view" id="sv-income">
      <div class="table-toolbar">
        <div class="rc">Showing <span id="rc-income">0</span> metros</div>
        <div class="sort-group"><span class="sort-lbl">SORT:</span>
          <button class="sbtn on" id="income-sort-val" onclick="metroSort('income','income')">Income Needed</button>
          <button class="sbtn" id="income-sort-yoy" onclick="metroSort('income','yoy')">YoY%</button>
          <button class="sbtn" id="income-sort-name" onclick="metroSort('income','name')">Name</button>
        </div>
      </div>
      <div class="table-wrap">
        <table><thead><tr>
          <th onclick="metroSort('income','name')">Metro Area<span class="sa">↕</span></th><th>State</th>
          <th onclick="metroSort('income','income')">Income Needed (20% Down)<span class="sa">↕</span></th>
          <th onclick="metroSort('income','yoy')">YoY %<span class="sa">↕</span></th>
          <th onclick="metroSort('income','mo6')">6-Mo %<span class="sa">↕</span></th><th>12-Mo Trend</th>
        </tr></thead><tbody id="tb-income"></tbody></table>
        <div id="es-income" class="empty" style="display:none"><h3>No results</h3></div>
      </div>
      <div class="pager" id="pg-income"></div>
    </div>

    <!-- NATIONAL ZORF -->
    <div class="section-view" id="sv-zorf">
      <div class="national-view">
        <div class="nat-card">
          <div class="nat-header">
            <h2>📉 National Rental Forecast</h2>
            <p>Zillow Observed Rent Forecast (ZORF) · Single Family · Smoothed · Base: Feb 2026</p>
          </div>
          <div class="nat-metrics">
            <div class="nat-metric"><div class="nat-ml">+1 Month (Mar 2026)</div><div class="nat-mv">+0.5%</div><div class="nat-ms">Projected growth</div></div>
            <div class="nat-metric"><div class="nat-ml">+3 Months (May 2026)</div><div class="nat-mv">+1.2%</div><div class="nat-ms">Projected growth</div></div>
            <div class="nat-metric"><div class="nat-ml">+12 Months (Feb 2027)</div><div class="nat-mv">+1.7%</div><div class="nat-ms">Projected growth</div></div>
          </div>
          <div class="pp-chart-box"><div class="pp-chart-hdr"><div class="pp-chart-title">Cumulative Rental Growth Forecast</div></div><canvas id="zorf-chart" height="120"></canvas></div>
          <div class="nat-note">This is a national-level aggregate forecast for single-family rentals. Individual metro and zip-level rental trends may vary significantly.</div>
        </div>
      </div>
    </div>

  </div><!-- /content-area -->
</div><!-- /main -->
</div><!-- /app -->

<!-- ── ZIP PROFILE PANEL ── -->
<div class="profile-overlay" id="profile-overlay" onclick="closeProfile(event)">
  <div class="profile-panel" onclick="event.stopPropagation()">
    <div class="pp-header">
      <button class="pp-close" onclick="closeProfile()">✕</button>
      <div class="pp-zip" id="pp-zip">—</div>
      <div class="pp-loc" id="pp-loc">—</div>
      <div class="pp-metro" id="pp-metro">—</div>
    </div>
    <div class="pp-body">
      <div id="pp-badge-row" style="margin-bottom:14px"></div>
      <div class="pp-tabs">
        <div class="pp-tab active" onclick="ppTab('home')">🏠 Home Values</div>
        <div class="pp-tab" onclick="ppTab('forecast')">📈 Forecast</div>
        <div class="pp-tab" onclick="ppTab('rentals')">🏘 Rentals</div>
        <div class="pp-tab" onclick="ppTab('metro')">🌆 Metro Data</div>
      </div>
      <!-- HOME VALUES PANE -->
      <div class="pp-pane active" id="pane-home">
        <div class="pp-metrics" id="pp-zhvi-metrics"></div>
        <div class="pp-chart-box">
          <div class="pp-chart-hdr">
            <div class="pp-chart-title">Home Value History</div>
            <div class="tr-btns">
              <button class="trb on" id="ppzhvi-1y" onclick="ppZhviRange('1y')">1Y</button>
              <button class="trb" id="ppzhvi-3y" onclick="ppZhviRange('3y')">3Y</button>
              <button class="trb" id="ppzhvi-all" onclick="ppZhviRange('all')">2000→</button>
            </div>
          </div>
          <canvas id="pp-zhvi-chart" height="130"></canvas>
        </div>
      </div>
      <!-- FORECAST PANE -->
      <div class="pp-pane" id="pane-forecast">
        <div id="pp-zhvf-content"></div>
      </div>
      <!-- RENTALS PANE -->
      <div class="pp-pane" id="pane-rentals">
        <div id="pp-zori-metrics" class="pp-metrics"></div>
        <div class="pp-chart-box">
          <div class="pp-chart-hdr">
            <div class="pp-chart-title">Monthly Rental Trend</div>
            <div class="tr-btns">
              <button class="trb on" id="ppzori-1y" onclick="ppZoriRange('1y')">1Y</button>
              <button class="trb" id="ppzori-3y" onclick="ppZoriRange('3y')">3Y</button>
              <button class="trb" id="ppzori-all" onclick="ppZoriRange('all')">2015→</button>
            </div>
          </div>
          <canvas id="pp-zori-chart" height="130"></canvas>
        </div>
      </div>
      <!-- METRO PANE -->
      <div class="pp-pane" id="pane-metro">
        <div class="metro-grid" id="pp-metro-grid"></div>
        <div style="margin-top:14px">
          <div class="pp-chart-box">
            <div class="pp-chart-hdr"><div class="pp-chart-title" id="pp-metro-chart-title">Metro Chart</div>
              <select id="pp-metro-select" onchange="drawMetroChart()" style="background:var(--surf3);border:1px solid var(--bdr);border-radius:6px;padding:3px 8px;color:var(--tx);font-size:11px;outline:none">
                <option value="temp_idx">Market Temp Index</option>
                <option value="invt">For Sale Inventory</option>
                <option value="sales">Sales Count</option>
                <option value="new_con">New Construction</option>
                <option value="doz">Days on Market</option>
                <option value="income">Income Needed</option>
              </select>
            </div>
            <canvas id="pp-metro-chart" height="130"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
const D = """ + data_json + """;

// ── GLOBALS ──────────────────────────────────────────────────────────────────
const PG = 50;
let currentSection = 'zhvi';
let sparkCharts = {};
let ppZhviChart=null, ppZoriChart=null, ppMetroChart=null, zorfChart=null;
let selectedZip = null;
let selectedMetro = null;

// Per-section state
const SEC = {
  zhvi:   { data:[], filtered:[], sort:{k:'yoy',d:-1}, page:1, spark:'1y', temps:new Set(['hot','warm','slow','cooling','cold']) },
  zhvf:   { data:[], filtered:[], sort:{k:'f12',d:-1}, page:1 },
  zori:   { data:[], filtered:[], sort:{k:'yoy',d:-1}, page:1, spark:'1y' },
  mkt:    { data:[], filtered:[], sort:{k:'temp_idx',d:-1}, page:1 },
  invt:   { data:[], filtered:[], sort:{k:'invt',d:-1}, page:1 },
  sales:  { data:[], filtered:[], sort:{k:'sales',d:-1}, page:1 },
  newcon: { data:[], filtered:[], sort:{k:'new_con',d:-1}, page:1 },
  doz:    { data:[], filtered:[], sort:{k:'doz',d:1}, page:1 },
  income: { data:[], filtered:[], sort:{k:'income',d:-1}, page:1 },
};

// Section config
const SCFG = {
  zhvi:   { title:'Home Values (ZHVI)', desc:'Zillow Home Value Index · Single Family + Condo · Middle Tier · 2000–Feb 2026', showState:true, showCity:true, showValue:true, showTemp:true },
  zhvf:   { title:'Home Value Forecast (ZHVF)', desc:'Projected % growth from base Feb 2026 · Zip-level · 1-month, 3-month, 12-month horizons', showState:true, showCity:true },
  zori:   { title:'Rentals — ZORI', desc:'Zillow Observed Rent Index · All homes + MFR · Smoothed · 2015–Feb 2026', showState:true, showCity:true },
  mkt:    { title:'Market Temperature Index', desc:'Metro-level market heat index (0–100) · Higher = more competitive · 2018–Feb 2026', showState:true },
  invt:   { title:'For Sale Inventory', desc:'Active for-sale listings count · Metro-level · Smoothed · 2018–Feb 2026', showState:true },
  sales:  { title:'Sales Activity', desc:'Closed home sales count · Metro-level · 2008–Feb 2026', showState:true },
  newcon: { title:'New Construction Sales', desc:'New construction home sales · Metro-level · 2018–Jan 2026', showState:true },
  doz:    { title:'Days on Market (Pending)', desc:'Average days homes spent pending on Zillow · Metro-level · 2018–Feb 2026', showState:true },
  income: { title:'Income Needed (20% Down)', desc:'Annual income required to purchase a home with 20% down payment · Metro-level · 2012–Feb 2026', showState:true },
  zorf:   { title:'Rental Forecast — ZORF (National)', desc:'Zillow Observed Rent Forecast · National aggregate · Projected from Feb 2026' },
};

// Formatters
const f$ = v => v==null?'—':'$'+Math.round(v).toLocaleString();
const fP = v => v==null?'—':(v>0?'+':'')+v.toFixed(2)+'%';
const fN = v => v==null?'—':Math.round(v).toLocaleString();
const pc = v => v==null?'neu':v>0?'pos':'neg';
const fD = v => v==null?'—':v.toFixed(1)+' days';

const TC = {
  hot:     {lbl:'🔥 Hot',    cls:'b-hot',  color:'#ef4444'},
  warm:    {lbl:'☀️ Warm',   cls:'b-warm', color:'#f97316'},
  slow:    {lbl:'🌤 Slow',   cls:'b-slow', color:'#eab308'},
  cooling: {lbl:'🌧 Cool',   cls:'b-cool', color:'#3b82f6'},
  cold:    {lbl:'❄️ Cold',   cls:'b-cold', color:'#06b6d4'},
  unknown: {lbl:'—',         cls:'b-slow', color:'#7a90a8'},
};

const METRO_KEYS = {
  temp_idx:{key:'temp_idx',vkey:'temp_idx',fmt:fN,lbl:'Market Temp Index',unit:'/ 100',color:'#7c6cf5'},
  invt:    {key:'invt',    vkey:'invt',    fmt:fN,lbl:'For Sale Listings', unit:'listings',color:'#f97316'},
  sales:   {key:'sales',   vkey:'sales',   fmt:fN,lbl:'Sales Count',       unit:'homes',  color:'#34d399'},
  new_con: {key:'new_con', vkey:'new_con', fmt:fN,lbl:'New Con Sales',     unit:'homes',  color:'#5b8ff9'},
  doz:     {key:'doz',     vkey:'doz',     fmt:v=>v==null?'—':v+' days',   lbl:'Days Pending', unit:'days',color:'#eab308'},
  income:  {key:'income',  vkey:'income',  fmt:f$,lbl:'Income Needed',     unit:'/ year', color:'#ef4444'},
};

// ── INIT ─────────────────────────────────────────────────────────────────────
function init() {
  // Load data into sections
  SEC.zhvi.data = D.zhvi.records;
  SEC.zhvf.data = D.zhvf.records;
  SEC.zori.data = D.zori.records;
  SEC.mkt.data    = D.metro.temp_idx.records;
  SEC.invt.data   = D.metro.invt.records;
  SEC.sales.data  = D.metro.sales.records;
  SEC.newcon.data = D.metro.new_con.records;
  SEC.doz.data    = D.metro.doz.records;
  SEC.income.data = D.metro.income.records;

  // Populate state filter
  const se = document.getElementById('fi-state');
  D.zhvi.states.forEach(s => { const o=document.createElement('option'); o.value=s; o.textContent=s; se.appendChild(o); });

  // Event listeners
  document.getElementById('fi-search').addEventListener('input', debounce(applyFilters, 180));
  document.addEventListener('keydown', e => { if(e.key==='Escape') closeProfile(); });

  // Draw ZORF chart
  setTimeout(drawZorfChart, 100);

  setSection('zhvi');
}

// ── NAV ──────────────────────────────────────────────────────────────────────
let navCollapsed = false;
function toggleNav() {
  navCollapsed = !navCollapsed;
  document.getElementById('nav').classList.toggle('collapsed', navCollapsed);
}

function setSection(sec) {
  currentSection = sec;
  // update nav
  document.querySelectorAll('.nav-item').forEach(el => {
    const id = el.id.replace('nav-','');
    const map = {mkt:'mkt',invt:'invt',sales:'sales',newcon:'newcon',doz:'doz',income:'income'};
    const sid = map[id]||id;
    el.classList.toggle('active', sid===sec);
  });
  // update views
  document.querySelectorAll('.section-view').forEach(el => el.classList.remove('active'));
  const sv = document.getElementById('sv-'+sec);
  if(sv) sv.classList.add('active');
  // update topbar
  const cfg = SCFG[sec]||{};
  document.getElementById('section-title').textContent = cfg.title||sec;
  document.getElementById('section-desc').textContent = cfg.desc||'';
  // update filters
  const fb = document.getElementById('filter-bar');
  fb.style.display = sec==='zorf' ? 'none' : 'flex';
  document.getElementById('fi-city').style.display = cfg.showCity?'':'none';
  document.getElementById('fi-value').style.display = cfg.showValue?'':'none';
  document.getElementById('temp-chips').style.display = cfg.showTemp?'':'none';
  // reset search/state for metro sections (state filter repurposed)
  if(!cfg.showState) {
    document.getElementById('fi-state').style.display='none';
  } else {
    document.getElementById('fi-state').style.display='';
  }
  applyFilters();
}

// ── FILTERS ──────────────────────────────────────────────────────────────────
function onStateChange() {
  const s = document.getElementById('fi-state').value;
  const ce = document.getElementById('fi-city');
  ce.innerHTML = '<option value="">All Cities</option>';
  if(s && ['zhvi','zhvf','zori'].includes(currentSection)) {
    const cities = D.zhvi.cities_by_state[s]||[];
    cities.forEach(c => { const o=document.createElement('option'); o.value=c; o.textContent=c; ce.appendChild(o); });
    ce.disabled=false;
  } else { ce.disabled=true; }
  applyFilters();
}
function onSearch() { applyFilters(); }

function toggleChip(t) {
  const s = SEC.zhvi.temps;
  s.has(t)?s.delete(t):s.add(t);
  document.querySelector(`.chip[data-t="${t}"]`).classList.toggle('on', s.has(t));
  SEC.zhvi.page=1; applyFilters();
}

function applyFilters() {
  const q = document.getElementById('fi-search').value.toLowerCase().trim();
  const st = document.getElementById('fi-state').value;
  const ct = document.getElementById('fi-city').value;
  const vr = document.getElementById('fi-value').value;
  let [mn,mx] = [0,Infinity];
  if(vr){const p=vr.split('-'); mn=+p[0]; mx=+p[1];}

  if(['zhvi','zhvf','zori'].includes(currentSection)) {
    const s = SEC[currentSection];
    s.filtered = s.data.filter(r => {
      if(st && r.state!==st) return false;
      if(ct && r.city!==ct) return false;
      if(currentSection==='zhvi'){
        if(!s.temps.has(r.temp)) return false;
        if(r.value!=null&&(r.value<mn||r.value>mx)) return false;
      }
      if(q){const h=(r.zip+' '+r.city+' '+r.county+' '+r.state+' '+r.metro).toLowerCase(); if(!h.includes(q)) return false;}
      return true;
    });
    sortSection(currentSection);
  } else if(['mkt','invt','sales','newcon','doz','income'].includes(currentSection)) {
    const s = SEC[currentSection];
    s.filtered = s.data.filter(r => {
      if(st && !r.state.includes(st)) return false;
      if(q && !r.name.toLowerCase().includes(q)) return false;
      return true;
    });
    sortSection(currentSection);
  }
  renderSection(currentSection);
}

function resetFilters() {
  document.getElementById('fi-search').value='';
  document.getElementById('fi-state').value='';
  const ce=document.getElementById('fi-city');
  ce.innerHTML='<option value="">All Cities</option>'; ce.disabled=true;
  document.getElementById('fi-value').value='';
  SEC.zhvi.temps=new Set(['hot','warm','slow','cooling','cold']);
  document.querySelectorAll('.chip').forEach(c=>c.classList.add('on'));
  applyFilters();
}

// ── SORT & RENDER ─────────────────────────────────────────────────────────────
function sortSection(sec) {
  const s=SEC[sec];
  s.filtered.sort((a,b)=>{
    let av=a[s.sort.k], bv=b[s.sort.k];
    if(av==null) av=s.sort.d>0?Infinity:-Infinity;
    if(bv==null) bv=s.sort.d>0?Infinity:-Infinity;
    if(typeof av==='string') return s.sort.d*av.localeCompare(bv);
    return s.sort.d*(bv-av);
  });
}

function zhviSort(k) { const s=SEC.zhvi; s.sort.k===k?s.sort.d*=-1:(s.sort={k,d:-1}); s.page=1; document.querySelectorAll('[id^="zhvi-sort"]').forEach(b=>b.classList.remove('on')); const b=document.getElementById('zhvi-sort-'+k); if(b)b.classList.add('on'); sortSection('zhvi'); renderSection('zhvi'); }
function zhvfSort(k) { const s=SEC.zhvf; s.sort.k===k?s.sort.d*=-1:(s.sort={k,d:-1}); s.page=1; document.querySelectorAll('[id^="zhvf-sort"]').forEach(b=>b.classList.remove('on')); const b=document.getElementById('zhvf-sort-'+k); if(b)b.classList.add('on'); sortSection('zhvf'); renderSection('zhvf'); }
function zoriSort(k) { const s=SEC.zori; s.sort.k===k?s.sort.d*=-1:(s.sort={k,d:-1}); s.page=1; document.querySelectorAll('[id^="zori-sort"]').forEach(b=>b.classList.remove('on')); const b=document.getElementById('zori-sort-'+k); if(b)b.classList.add('on'); sortSection('zori'); renderSection('zori'); }
function metroSort(sec,k) { const s=SEC[sec]; s.sort.k===k?s.sort.d*=-1:(s.sort={k,d:-1}); s.page=1; document.querySelectorAll(`[id^="${sec}-sort"]`).forEach(b=>b.classList.remove('on')); const b=document.getElementById(`${sec}-sort-${k==='yoy'?'yoy':k==='name'?'name':'val'}`); if(b)b.classList.add('on'); sortSection(sec); renderSection(sec); }

function setZhviSpark(r) { SEC.zhvi.spark=r; ['1y','3y','all'].forEach(k=>document.getElementById('zhvi-spr-'+k).classList.toggle('on',k===r)); const lbl={'1y':'1Y','3y':'3Y','all':'2000→'}; document.getElementById('zhvi-spark-hdr').textContent='Trend ('+lbl[r]+')'; renderSection('zhvi'); }
function setZoriSpark(r) { SEC.zori.spark=r; ['1y','3y','all'].forEach(k=>document.getElementById('zori-spr-'+k).classList.toggle('on',k===r)); const lbl={'1y':'1Y','3y':'3Y','all':'2015→'}; document.getElementById('zori-spark-hdr').textContent='Trend ('+lbl[r]+')'; renderSection('zori'); }

function renderSection(sec) {
  destroySparklines();
  const s = SEC[sec];
  const start=(s.page-1)*PG, rows=s.filtered.slice(start,start+PG);
  const pill = document.getElementById('count-pill');

  if(['zhvi','zhvf','zori'].includes(sec)) {
    const rc=document.getElementById('rc-'+sec);
    if(rc) rc.textContent=s.filtered.length.toLocaleString();
    if(pill) pill.textContent=s.filtered.length.toLocaleString()+' zips';
    renderZipTable(sec, rows, start);
    renderPager(sec);
  } else if(['mkt','invt','sales','newcon','doz','income'].includes(sec)) {
    const smap={mkt:'mkt',invt:'invt',sales:'sales',newcon:'newcon',doz:'doz',income:'income'};
    const rc=document.getElementById('rc-'+sec);
    if(rc) rc.textContent=s.filtered.length.toLocaleString();
    if(pill) pill.textContent=s.filtered.length.toLocaleString()+' metros';
    renderMetroTable(sec, rows, start);
    renderPager(sec);
  }
}

// ── ZIP TABLE RENDER ──────────────────────────────────────────────────────────
function renderZipTable(sec, rows, start) {
  const tb = document.getElementById('tb-'+sec);
  const es = document.getElementById('es-'+sec);
  es.style.display = rows.length?'none':'block';
  if(!rows.length){tb.innerHTML='';return;}

  if(sec==='zhvi') {
    const spark = SEC.zhvi.spark;
    tb.innerHTML = rows.map((r,i) => {
      const tc=TC[r.temp]||TC.unknown;
      return `<tr onclick="openZipProfile('${r.zip}')">
        <td><span class="zipcode">${r.zip}</span></td>
        <td><span class="city">${r.city||'—'}</span></td>
        <td><span class="st-tag">${r.state}</span></td>
        <td style="color:var(--txm);font-size:11px">${r.county}</td>
        <td><span class="badge ${tc.cls}"><span class="bdot"></span>${tc.lbl}</span></td>
        <td class="val-bold">${f$(r.value)}</td>
        <td class="${pc(r.yoy)}" style="font-weight:600">${fP(r.yoy)}</td>
        <td class="${pc(r.mo6)}">${fP(r.mo6)}</td>
        <td class="${pc(r.yr3)}">${fP(r.yr3)}</td>
        <td><canvas id="sp-${start+i}" width="110" height="30" class="spark"></canvas></td>
      </tr>`;
    }).join('');
    requestAnimationFrame(()=>{
      rows.forEach((r,i)=>{
        const c=document.getElementById('sp-'+(start+i));
        if(!c) return;
        const td=r['t'+spark]==='t'+spark?r['t1y']:r['t'+spark]||(spark==='1y'?r.t1y:spark==='3y'?r.t3y:r.tall);
        const tdata = spark==='1y'?r.t1y:spark==='3y'?r.t3y:r.tall;
        const labs = spark==='1y'?D.zhvi.labels_1y:spark==='3y'?D.zhvi.labels_3y:D.zhvi.labels_tall;
        drawSparkline(c,'sp-'+(start+i),tdata,labs,TC[r.temp]?.color||'#7a90a8');
      });
    });
  } else if(sec==='zhvf') {
    const fcls = v => v==null?'fcol-neu':v>0?'fcol-pos':'fcol-neg';
    const fp = v => v==null?'—':(v>0?'+':'')+v.toFixed(1)+'%';
    tb.innerHTML = rows.map(r=>`<tr onclick="openZipProfile('${r.zip}')">
      <td><span class="zipcode">${r.zip}</span></td>
      <td><span class="city">${r.city||'—'}</span></td>
      <td><span class="st-tag">${r.state}</span></td>
      <td style="color:var(--txm);font-size:11px">${r.county}</td>
      <td style="color:var(--txm);font-size:11px;max-width:200px;overflow:hidden;text-overflow:ellipsis">${r.metro}</td>
      <td class="${fcls(r.f1)}" style="font-size:13px">${fp(r.f1)}</td>
      <td class="${fcls(r.f3)}" style="font-size:13px">${fp(r.f3)}</td>
      <td class="${fcls(r.f12)}" style="font-size:14px;font-weight:700">${fp(r.f12)}</td>
    </tr>`).join('');
  } else if(sec==='zori') {
    const spark = SEC.zori.spark;
    tb.innerHTML = rows.map((r,i)=>`<tr onclick="openZipProfile('${r.zip}')">
      <td><span class="zipcode">${r.zip}</span></td>
      <td><span class="city">${r.city||'—'}</span></td>
      <td><span class="st-tag">${r.state}</span></td>
      <td style="color:var(--txm);font-size:11px">${r.county}</td>
      <td class="val-bold">${f$(r.rent)}</td>
      <td class="${pc(r.yoy)}" style="font-weight:600">${fP(r.yoy)}</td>
      <td class="${pc(r.mo6)}">${fP(r.mo6)}</td>
      <td><canvas id="sp-${start+i}" width="110" height="30" class="spark"></canvas></td>
    </tr>`).join('');
    requestAnimationFrame(()=>{
      rows.forEach((r,i)=>{
        const c=document.getElementById('sp-'+(start+i));
        if(!c) return;
        const tdata=spark==='1y'?r.t1y:spark==='3y'?r.t3y:r.tall;
        const labs=spark==='1y'?D.zori.labels_1y:spark==='3y'?D.zori.labels_3y:D.zori.labels_tall;
        const color=r.yoy>=0?'#34d399':'#f87171';
        drawSparkline(c,'sp-'+(start+i),tdata,labs,color);
      });
    });
  }
}

// ── METRO TABLE RENDER ───────────────────────────────────────────────────────
const METRO_VAL_KEY = {mkt:'temp_idx',invt:'invt',sales:'sales',newcon:'new_con',doz:'doz',income:'income'};
const METRO_FMT = {mkt:fN,invt:fN,sales:fN,newcon:fN,doz:v=>v==null?'—':v+' days',income:f$};
const METRO_COLOR = {mkt:'#7c6cf5',invt:'#f97316',sales:'#34d399',newcon:'#5b8ff9',doz:'#eab308',income:'#ef4444'};

function renderMetroTable(sec, rows, start) {
  const tb=document.getElementById('tb-'+sec);
  const es=document.getElementById('es-'+sec);
  es.style.display=rows.length?'none':'block';
  if(!rows.length){tb.innerHTML='';return;}
  const vk=METRO_VAL_KEY[sec], fmt=METRO_FMT[sec], color=METRO_COLOR[sec];
  tb.innerHTML=rows.map((r,i)=>`<tr onclick="openMetroProfile('${r.name.replace(/'/g,"\\'")}','${sec}')">
    <td style="font-weight:600;max-width:280px;overflow:hidden;text-overflow:ellipsis">${r.name}</td>
    <td><span class="st-tag">${r.state||'—'}</span></td>
    <td class="val-bold">${fmt(r[vk])}</td>
    <td class="${pc(r.yoy)}" style="font-weight:600">${fP(r.yoy)}</td>
    <td class="${pc(r.mo6)}">${fP(r.mo6)}</td>
    <td><canvas id="sp-${start+i}" width="110" height="30" class="spark"></canvas></td>
  </tr>`).join('');
  requestAnimationFrame(()=>{
    rows.forEach((r,i)=>{
      const c=document.getElementById('sp-'+(start+i));
      if(!c) return;
      const src=sec==='mkt'?D.metro.temp_idx:sec==='invt'?D.metro.invt:sec==='sales'?D.metro.sales:sec==='newcon'?D.metro.new_con:sec==='doz'?D.metro.doz:D.metro.income;
      drawSparkline(c,'sp-'+(start+i),r.t1y,src.labels_1y,color);
    });
  });
}

// ── SPARKLINES ───────────────────────────────────────────────────────────────
function drawSparkline(canvas, id, data, labels, color) {
  if(!canvas||!data) return;
  try {
    sparkCharts[id] = new Chart(canvas,{type:'line',data:{labels,datasets:[{data,borderColor:color,borderWidth:1.5,pointRadius:0,tension:.4,fill:true,backgroundColor:color+'18'}]},options:{responsive:false,animation:false,plugins:{legend:{display:false},tooltip:{enabled:false}},scales:{x:{display:false},y:{display:false}}}});
  } catch(e){}
}
function destroySparklines() { Object.values(sparkCharts).forEach(c=>{try{c.destroy();}catch(e){}}); sparkCharts={}; }

// ── PAGINATION ───────────────────────────────────────────────────────────────
function renderPager(sec) {
  const s=SEC[sec], tot=s.filtered.length, tp=Math.ceil(tot/PG);
  const el=document.getElementById('pg-'+sec);
  if(!el||tp<=1){if(el)el.innerHTML='';return;}
  const p=s.page;
  let h=[];
  h.push(`<button class="pgb" onclick="goPage('${sec}',${p-1})" ${p===1?'disabled':''}>←</button>`);
  const range=[];
  for(let i=1;i<=tp;i++){
    if(i===1||i===tp||(i>=p-2&&i<=p+2)) range.push(i);
    else if(range[range.length-1]!=='…') range.push('…');
  }
  range.forEach(i=>{
    if(i==='…') h.push(`<span class="pgi">…</span>`);
    else h.push(`<button class="pgb ${i===p?'on':''}" onclick="goPage('${sec}',${i})">${i}</button>`);
  });
  h.push(`<button class="pgb" onclick="goPage('${sec}',${p+1})" ${p===tp?'disabled':''}>→</button>`);
  h.push(`<span class="pgi">Page ${p} of ${tp}</span>`);
  el.innerHTML=h.join('');
}
function goPage(sec,p) {
  const s=SEC[sec], tp=Math.ceil(s.filtered.length/PG);
  if(p<1||p>tp) return;
  s.page=p; destroySparklines(); renderSection(sec);
  document.querySelector('.table-wrap')?.scrollTo(0,0);
}

// ── ZIP PROFILE ──────────────────────────────────────────────────────────────
let ppZhviRange_='1y', ppZoriRange_='1y', ppActiveTab='home';

function openZipProfile(zip) {
  selectedZip=zip;
  const zi=D.zhvi.index[zip], zr=zi!=null?D.zhvi.records[zi]:null;
  const ori=D.zori.index[zip], or_=ori!=null?D.zori.records[ori]:null;
  const fi=D.zhvf.index[zip], fr=fi!=null?D.zhvf.records[fi]:null;
  const metro=zr?.metro||fr?.metro||or_?.metro||'';
  selectedMetro=metro;

  document.getElementById('pp-zip').textContent=zip;
  document.getElementById('pp-loc').textContent=[zr?.city||fr?.city||'', zr?.state||fr?.state||''].filter(Boolean).join(', ')||'—';
  document.getElementById('pp-metro').textContent=metro||'—';

  // Badge
  let badgeHtml='';
  if(zr){const tc=TC[zr.temp]||TC.unknown;badgeHtml=`<span class="badge ${tc.cls}" style="font-size:11px;padding:4px 10px"><span class="bdot"></span>${tc.lbl}</span> &nbsp; <span style="font-size:11px;color:var(--txm)">Market Temperature</span>`;}
  document.getElementById('pp-badge-row').innerHTML=badgeHtml;

  // ZHVI metrics
  if(zr){
    document.getElementById('pp-zhvi-metrics').innerHTML=`
      <div class="ppm"><div class="ppm-l">Median Value</div><div class="ppm-v">${f$(zr.value)}</div></div>
      <div class="ppm"><div class="ppm-l">YoY Change</div><div class="ppm-v ${pc(zr.yoy)}">${fP(zr.yoy)}</div></div>
      <div class="ppm"><div class="ppm-l">6-Month</div><div class="ppm-v ${pc(zr.mo6)}">${fP(zr.mo6)}</div></div>
      <div class="ppm"><div class="ppm-l">3-Year</div><div class="ppm-v ${pc(zr.yr3)}">${fP(zr.yr3)}</div></div>
      <div class="ppm"><div class="ppm-l">County</div><div class="ppm-v" style="font-size:12px">${zr.county||'—'}</div></div>
      <div class="ppm"><div class="ppm-l">Metro</div><div class="ppm-v" style="font-size:10px;line-height:1.4">${zr.metro||'—'}</div></div>`;
  } else {
    document.getElementById('pp-zhvi-metrics').innerHTML='<div class="no-data">No ZHVI data for this zip code</div>';
  }

  // ZHVF forecast
  if(fr){
    const fc=v=>v==null?'—':(v>0?'+':'')+v.toFixed(1)+'%';
    const fcls=v=>v==null?'':(v>0?'pos':'neg');
    document.getElementById('pp-zhvf-content').innerHTML=`
      <div class="fcst-grid">
        <div class="fcst-card"><div class="fcst-period">1 Month (Mar 2026)</div><div class="fcst-val ${fcls(fr.f1)}">${fc(fr.f1)}</div><div class="fcst-lbl">Projected change</div></div>
        <div class="fcst-card"><div class="fcst-period">3 Months (May 2026)</div><div class="fcst-val ${fcls(fr.f3)}">${fc(fr.f3)}</div><div class="fcst-lbl">Projected change</div></div>
        <div class="fcst-card"><div class="fcst-period">12 Months (Feb 2027)</div><div class="fcst-val ${fcls(fr.f12)}">${fc(fr.f12)}</div><div class="fcst-lbl">Projected change</div></div>
      </div>
      <div style="margin-top:14px;padding:12px;background:var(--surf2);border:1px solid var(--bdr);border-radius:8px;font-size:11px;color:var(--txm)">
        Base date: ${fr.base} · Source: Zillow Home Value Forecast (ZHVF) · Middle Tier SFR+Condo
      </div>`;
  } else {
    document.getElementById('pp-zhvf-content').innerHTML='<div class="no-data">No forecast data for this zip code</div>';
  }

  // ZORI metrics
  if(or_){
    document.getElementById('pp-zori-metrics').innerHTML=`
      <div class="ppm"><div class="ppm-l">Monthly Rent</div><div class="ppm-v">${f$(or_.rent)}</div></div>
      <div class="ppm"><div class="ppm-l">YoY Change</div><div class="ppm-v ${pc(or_.yoy)}">${fP(or_.yoy)}</div></div>
      <div class="ppm"><div class="ppm-l">6-Month</div><div class="ppm-v ${pc(or_.mo6)}">${fP(or_.mo6)}</div></div>`;
  } else {
    document.getElementById('pp-zori-metrics').innerHTML='<div class="no-data" style="grid-column:span 3">No rental data for this zip code</div>';
  }

  // Metro grid
  const metroGrid=document.getElementById('pp-metro-grid');
  const mKeys=['temp_idx','invt','sales','new_con','doz','income'];
  const mSrcs={temp_idx:D.metro.temp_idx,invt:D.metro.invt,sales:D.metro.sales,new_con:D.metro.new_con,doz:D.metro.doz,income:D.metro.income};
  const mFmts={temp_idx:v=>v==null?'—':v+' / 100',invt:fN,sales:fN,new_con:fN,doz:v=>v==null?'—':v+' days',income:f$};
  const mLbls={temp_idx:'Market Temp Index',invt:'For Sale Inventory',sales:'Sales Count',new_con:'New Construction',doz:'Avg Days Pending',income:'Income Needed'};
  let gridHtml='';
  mKeys.forEach(k=>{
    const src=mSrcs[k]; const mi=src.index[metro]; const mr=mi!=null?src.records[mi]:null;
    const val=mr?mr[k]:null;
    gridHtml+=`<div class="metro-mini">
      <div class="metro-mini-title">${mLbls[k]}</div>
      <div class="metro-mini-val">${mr?mFmts[k](val):'<span style="color:var(--txd);font-size:12px">No data</span>'}</div>
      <div class="metro-mini-sub">${mr?'YoY: '+fP(mr.yoy):'Metro not found'}</div>
    </div>`;
  });
  metroGrid.innerHTML=gridHtml;

  // Show panel + active tab
  document.getElementById('profile-overlay').classList.add('open');
  ppActiveTab='home'; ppTab('home');

  // Draw charts after open
  ppZhviRange_='1y'; ppZoriRange_='1y';
  ['ppzhvi-1y','ppzhvi-3y','ppzhvi-all'].forEach(id=>{const el=document.getElementById(id);if(el)el.classList.toggle('on',id==='ppzhvi-1y');});
  ['ppzori-1y','ppzori-3y','ppzori-all'].forEach(id=>{const el=document.getElementById(id);if(el)el.classList.toggle('on',id==='ppzori-1y');});

  setTimeout(()=>{
    drawPpZhviChart(zr);
    drawPpZoriChart(or_);
    drawMetroChart();
  },50);

  // Show ZIP profile nav item
  const navPP=document.getElementById('nav-profile');
  const navLbl=document.getElementById('nav-profile-label');
  navPP.style.display='flex'; navPP.classList.add('zip-active');
  navLbl.textContent='ZIP '+zip;
}

function openMetroProfile(metro,sec) {
  // just filter the metro section for now
}

function openProfileFromNav() {
  if(selectedZip) document.getElementById('profile-overlay').classList.add('open');
}

function closeProfile(e) {
  if(!e||e.target===document.getElementById('profile-overlay'))
    document.getElementById('profile-overlay').classList.remove('open');
}

function ppTab(tab) {
  ppActiveTab=tab;
  document.querySelectorAll('.pp-tab').forEach((el,i)=>{
    const tabs=['home','forecast','rentals','metro'];
    el.classList.toggle('active',tabs[i]===tab);
  });
  document.querySelectorAll('.pp-pane').forEach(el=>el.classList.remove('active'));
  document.getElementById('pane-'+tab).classList.add('active');
}

function ppZhviRange(r) {
  ppZhviRange_=r;
  ['1y','3y','all'].forEach(k=>{const el=document.getElementById('ppzhvi-'+k);if(el)el.classList.toggle('on',k===r);});
  const zi=D.zhvi.index[selectedZip];
  drawPpZhviChart(zi!=null?D.zhvi.records[zi]:null);
}
function ppZoriRange(r) {
  ppZoriRange_=r;
  ['1y','3y','all'].forEach(k=>{const el=document.getElementById('ppzori-'+k);if(el)el.classList.toggle('on',k===r);});
  const oi=D.zori.index[selectedZip];
  drawPpZoriChart(oi!=null?D.zori.records[oi]:null);
}

function drawPpZhviChart(zr) {
  if(ppZhviChart){try{ppZhviChart.destroy();}catch(e){}} ppZhviChart=null;
  if(!zr) return;
  const k=ppZhviRange_; const color=(TC[zr.temp]||TC.unknown).color;
  const data=k==='1y'?zr.t1y:k==='3y'?zr.t3y:zr.tall;
  const labs=k==='1y'?D.zhvi.labels_1y:k==='3y'?D.zhvi.labels_3y:D.zhvi.labels_tall;
  ppZhviChart=makeDetailChart('pp-zhvi-chart',data,labs,color,'$');
}
function drawPpZoriChart(or_) {
  if(ppZoriChart){try{ppZoriChart.destroy();}catch(e){}} ppZoriChart=null;
  if(!or_) return;
  const k=ppZoriRange_; const color=or_.yoy>=0?'#34d399':'#f87171';
  const data=k==='1y'?or_.t1y:k==='3y'?or_.t3y:or_.tall;
  const labs=k==='1y'?D.zori.labels_1y:k==='3y'?D.zori.labels_3y:D.zori.labels_tall;
  ppZoriChart=makeDetailChart('pp-zori-chart',data,labs,color,'$');
}
function drawMetroChart() {
  if(ppMetroChart){try{ppMetroChart.destroy();}catch(e){}} ppMetroChart=null;
  const sel=document.getElementById('pp-metro-select').value;
  const mc=METRO_KEYS[sel];
  if(!mc||!selectedMetro) return;
  const srcMap={temp_idx:D.metro.temp_idx,invt:D.metro.invt,sales:D.metro.sales,new_con:D.metro.new_con,doz:D.metro.doz,income:D.metro.income};
  const src=srcMap[sel]; const mi=src?.index[selectedMetro]; const mr=mi!=null?src.records[mi]:null;
  document.getElementById('pp-metro-chart-title').textContent=mc.lbl+' — '+selectedMetro;
  if(!mr) return;
  const labs=src.labels_1y;
  ppMetroChart=makeDetailChart('pp-metro-chart',mr.t1y,labs,mc.color,sel==='income'?'$':'');
}

function makeDetailChart(id,data,labs,color,prefix) {
  const ctx=document.getElementById(id); if(!ctx) return null;
  try {
    return new Chart(ctx,{type:'line',data:{labels:labs,datasets:[{label:'',data,borderColor:color,borderWidth:2.5,pointRadius:3,pointBackgroundColor:color,pointBorderColor:'var(--surf2)',pointBorderWidth:2,tension:.4,fill:true,backgroundColor:color+'20'}]},options:{responsive:true,plugins:{legend:{display:false},tooltip:{callbacks:{label:ctx=>prefix+''+Math.round(ctx.parsed.y).toLocaleString()+(prefix===''?' days':'')},backgroundColor:'#162848',borderColor:color,borderWidth:1,titleColor:'#dde6f0',bodyColor:color,padding:8}},scales:{x:{grid:{color:'rgba(255,255,255,.04)'},ticks:{color:'#7a90a8',font:{size:9},maxRotation:45,maxTicksLimit:13}},y:{grid:{color:'rgba(255,255,255,.04)'},ticks:{color:'#7a90a8',font:{size:9},callback:v=>prefix+=(prefix==='$'?(v>=1e6?(v/1e6).toFixed(1)+'M':(v/1000).toFixed(0)+'K'):Math.round(v).toLocaleString())?prefix+((v>=1e6?(v/1e6).toFixed(1)+'M':(v/1000).toFixed(0)+'K')):v}}}}}); 
  } catch(e){return null;}
}

function drawZorfChart() {
  const ctx=document.getElementById('zorf-chart'); if(!ctx) return;
  const color='#34d399';
  try {
    zorfChart=new Chart(ctx,{type:'bar',data:{labels:['Mar 2026 (+1mo)','May 2026 (+3mo)','Feb 2027 (+12mo)'],datasets:[{label:'Projected Growth %',data:[0.5,1.2,1.7],backgroundColor:[color+'60',color+'80',color+'a0'],borderColor:color,borderWidth:2,borderRadius:8}]},options:{responsive:true,plugins:{legend:{display:false},tooltip:{callbacks:{label:ctx=>'+'+ctx.parsed.y+'% projected growth'},backgroundColor:'#162848',borderColor:color,borderWidth:1,titleColor:'#dde6f0',bodyColor:color}},scales:{x:{grid:{display:false},ticks:{color:'#7a90a8',font:{size:11}}},y:{grid:{color:'rgba(255,255,255,.05)'},ticks:{color:'#7a90a8',font:{size:10},callback:v=>'+'+v+'%'},min:0,max:2.5}}}});
  } catch(e){}
}

function debounce(fn,d){let t;return(...a)=>{clearTimeout(t);t=setTimeout(()=>fn(...a),d);}}

init();
</script>
</body>
</html>"""

out = '/sessions/kind-beautiful-rubin/mnt/outputs/zhvi_dashboard.html'
with open(out, 'w') as f:
    f.write(html)

sz = os.path.getsize(out)
print(f"Written: {sz/1024/1024:.1f} MB")
