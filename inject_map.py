with open('/sessions/kind-beautiful-rubin/mnt/outputs/zhvi_dashboard.html') as f:
    html = f.read()

# ── 1. LEAFLET CDN ────────────────────────────────────────────────────────────
leaflet_cdn = """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
"""
html = html.replace('</head>', leaflet_cdn + '</head>', 1)

# ── 2. MAP CSS ────────────────────────────────────────────────────────────────
map_css = """
/* ── MAP VIEW ── */
.map-section{display:flex;height:100%;overflow:hidden}
.map-sidebar{width:270px;min-width:270px;background:var(--surf);border-right:1px solid var(--bdr);display:flex;flex-direction:column;overflow:hidden}
.map-sb-hdr{padding:12px 14px;border-bottom:1px solid var(--bdr);display:flex;align-items:center;gap:8px;flex-shrink:0}
.map-sb-hdr h3{font-size:12px;font-weight:700;flex:1}
.map-pin-count{font-size:10px;font-weight:700;background:rgba(91,143,249,.15);color:var(--ac);border:1px solid rgba(91,143,249,.3);border-radius:20px;padding:2px 8px}
.map-clear-btn{background:none;border:1px solid var(--bdr);border-radius:6px;padding:3px 8px;color:var(--txm);font-size:10px;cursor:pointer;transition:all .18s;display:none}
.map-clear-btn:hover{border-color:var(--neg);color:var(--neg)}

/* ZIP search in map sidebar */
.map-zip-search{padding:10px 14px;border-bottom:1px solid var(--bdr);flex-shrink:0}
.map-zip-input{width:100%;background:var(--surf2);border:1px solid var(--bdr);border-radius:8px;padding:7px 10px;color:var(--tx);font-size:12px;outline:none;transition:border-color .2s}
.map-zip-input:focus{border-color:var(--ac)}
.map-zip-hint{font-size:10px;color:var(--txd);margin-top:4px}

.map-pin-scroll{flex:1;overflow-y:auto;padding:10px 10px 6px}
.map-pin-scroll::-webkit-scrollbar{width:4px}
.map-pin-scroll::-webkit-scrollbar-thumb{background:var(--surf3);border-radius:2px}
.map-empty-pins{font-size:12px;color:var(--txd);padding:20px 4px;text-align:center;line-height:1.6}
.map-pin-card{background:var(--surf2);border:1px solid var(--bdr);border-radius:10px;padding:11px 12px;margin-bottom:8px;transition:border-color .18s}
.map-pin-card:hover{border-color:var(--bdr2)}
.map-pin-hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:3px}
.map-pin-loc{font-size:11px;color:var(--txm);margin-bottom:4px}
.map-pin-val{font-size:14px;font-weight:700;margin-bottom:1px}
.map-pin-yoy{font-size:11px;margin-bottom:5px}
.map-pin-actions{display:flex;gap:5px;margin-top:7px}
.map-pin-btn{flex:1;background:var(--surf3);border:1px solid var(--bdr);border-radius:6px;padding:4px 6px;color:var(--txm);font-size:10px;font-weight:600;cursor:pointer;transition:all .18s;text-align:center}
.map-pin-btn:hover{border-color:var(--ac);color:var(--ac)}
.map-pin-rm{flex:0;background:none;border:1px solid var(--bdr);border-radius:6px;padding:4px 7px;color:var(--txm);font-size:10px;cursor:pointer;transition:all .18s}
.map-pin-rm:hover{border-color:var(--neg);color:var(--neg)}

.map-dist-panel{background:var(--surf2);border-top:1px solid var(--bdr);padding:10px 14px;flex-shrink:0;max-height:160px;overflow-y:auto}
.map-dist-panel::-webkit-scrollbar{width:3px}
.map-dist-title{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:var(--txd);margin-bottom:8px}
.map-dist-row{display:flex;justify-content:space-between;align-items:center;padding:4px 0;border-bottom:1px solid var(--bdr);font-size:11px}
.map-dist-row:last-child{border-bottom:none}
.map-dist-zips{color:var(--txm);font-family:monospace;font-size:10px}
.map-dist-val{font-weight:700;color:var(--ac)}

#leaflet-map{flex:1;background:#0d1a2d}
.leaflet-popup-content-wrapper{background:#162848!important;border:1px solid rgba(255,255,255,.12)!important;border-radius:10px!important;box-shadow:0 8px 24px rgba(0,0,0,.5)!important}
.leaflet-popup-content{color:#dde6f0!important;margin:10px 12px!important}
.leaflet-popup-tip{background:#162848!important}
.leaflet-popup-close-button{color:#7a90a8!important;font-size:16px!important;top:6px!important;right:8px!important}
.leaflet-control-attribution{background:rgba(10,14,26,.85)!important;color:#4a607a!important;font-size:9px!important}
.leaflet-control-zoom a{background:#0f1e35!important;color:#7a90a8!important;border-color:rgba(255,255,255,.1)!important}
.leaflet-control-zoom a:hover{background:#162848!important;color:#dde6f0!important}

/* Row pin button */
.row-pin{background:none;border:none;cursor:pointer;font-size:12px;opacity:0;padding:0 3px;transition:opacity .18s;vertical-align:middle;border-radius:4px}
tbody tr:hover .row-pin{opacity:.7}
.row-pin:hover{opacity:1!important}

/* Pin button in profile */
.pp-pin-btn{background:rgba(91,143,249,.12);border:1px solid rgba(91,143,249,.25);border-radius:8px;padding:5px 12px;color:var(--ac);font-size:11px;font-weight:700;cursor:pointer;transition:all .2s;margin-left:8px}
.pp-pin-btn:hover{background:rgba(91,143,249,.22)}
.pp-pin-btn.pinned{background:rgba(52,211,153,.12);border-color:rgba(52,211,153,.3);color:var(--pos)}
"""
html = html.replace('</style>', map_css + '</style>', 1)

# ── 3. MAP NAV ITEM ───────────────────────────────────────────────────────────
# Add "🗺 Map View" nav item between NATIONAL section and nav-divider before nav-profile
old_nav = '<div class="nav-divider"></div>\n    <div class="nav-item" id="nav-profile"'
new_nav = '''<div class="nav-item" id="nav-map" onclick="setSection(\'map\')"><span class="nav-icon">🗺</span><span class="nav-label">Map View</span></div>
    <div class="nav-divider"></div>
    <div class="nav-item" id="nav-profile"'''
html = html.replace(old_nav, new_nav, 1)

# ── 4. MAP SECTION VIEW HTML ──────────────────────────────────────────────────
map_section_html = """
    <!-- MAP VIEW -->
    <div class="section-view" id="sv-map">
      <div class="map-section">
        <div class="map-sidebar">
          <div class="map-sb-hdr">
            <h3>📍 Pinned Locations</h3>
            <span class="map-pin-count" id="map-pin-count">0 pins</span>
            <button class="map-clear-btn" id="map-clear-btn" onclick="clearAllPins()">Clear All</button>
          </div>
          <div class="map-zip-search">
            <input class="map-zip-input" id="map-zip-input" type="text" placeholder="Enter ZIP code to pin…" onkeydown="if(event.key==='Enter')mapSearchPin()">
            <div class="map-zip-hint">Press Enter or click a ZIP row to add a pin</div>
          </div>
          <div class="map-pin-scroll" id="map-pin-list">
            <div class="map-empty-pins">Select ZIP codes from any table or type a ZIP above to drop pins on the map.</div>
          </div>
          <div class="map-dist-panel" id="map-dist-panel" style="display:none"></div>
        </div>
        <div id="leaflet-map"></div>
      </div>
    </div>
"""
html = html.replace('<!-- NATIONAL ZORF -->', map_section_html + '\n    <!-- NATIONAL ZORF -->', 1)

# ── 5. ADD PIN BUTTON TO ZIP PROFILE HEADER ───────────────────────────────────
old_badge = 'id="pp-badge-row" style="margin-bottom:14px"></div>'
new_badge = 'id="pp-badge-row" style="margin-bottom:14px;display:flex;align-items:center;gap:8px"><button class="pp-pin-btn" id="pp-pin-btn" onclick="toggleProfilePin()">📍 Pin on Map</button></div>'
html = html.replace(old_badge, new_badge, 1)

# ── 6. ADD PIN BUTTON TO TABLE ROWS (ZHVI, ZORI, ZHVF) ──────────────────────
# ZHVI: add 📍 button to zip cell
html = html.replace(
    "<td><span class=\"zipcode\">${r.zip}</span></td>\n        <td><span class=\"city\">${r.city||'—'}</span></td>\n        <td><span class=\"st-tag\">${r.state}</span></td>\n        <td style=\"color:var(--txm);font-size:11px\">${r.county}</td>\n        <td><span class=\"badge ${tc.cls}\">",
    "<td><span class=\"zipcode\">${r.zip}</span><button class=\"row-pin\" onclick=\"event.stopPropagation();addPinToMap('${r.zip}')\" title=\"Pin on map\">📍</button></td>\n        <td><span class=\"city\">${r.city||'—'}</span></td>\n        <td><span class=\"st-tag\">${r.state}</span></td>\n        <td style=\"color:var(--txm);font-size:11px\">${r.county}</td>\n        <td><span class=\"badge ${tc.cls}\">",
    1
)
# ZORI: find the zori row template
html = html.replace(
    '`<tr onclick="openZipProfile(\'${r.zip}\')">\n      <td><span class="zipcode">${r.zip}</span></td>\n      <td><span class="city">${r.city||\'—\'}</span></td>\n      <td><span class="st-tag">${r.state}</span></td>\n      <td style="color:var(--txm);font-size:11px">${r.county}</td>\n      <td class="val-bold">${f$(r.rent)}</td>',
    '`<tr onclick="openZipProfile(\'${r.zip}\')">\n      <td><span class="zipcode">${r.zip}</span><button class="row-pin" onclick="event.stopPropagation();addPinToMap(\'${r.zip}\')" title="Pin on map">📍</button></td>\n      <td><span class="city">${r.city||\'—\'}</span></td>\n      <td><span class="st-tag">${r.state}</span></td>\n      <td style="color:var(--txm);font-size:11px">${r.county}</td>\n      <td class="val-bold">${f$(r.rent)}</td>',
    1
)

# ── 7. INJECT MAP JS ──────────────────────────────────────────────────────────
map_js = r"""
// ── MAP SYSTEM (Leaflet + OpenStreetMap) ──────────────────────────────────────
let leafMap = null, mapPins = {}, mapLines = [], geoCache = {};

function initMapView() {
  if (leafMap) { setTimeout(() => leafMap.invalidateSize(), 80); return; }
  const el = document.getElementById('leaflet-map');
  if (!el || typeof L === 'undefined') return;
  leafMap = L.map(el, { center: [39.5, -98.35], zoom: 4, zoomControl: true });
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '© <a href="https://www.openstreetmap.org/copyright" style="color:#4a607a">OpenStreetMap</a> contributors © <a href="https://carto.com/" style="color:#4a607a">CARTO</a>',
    subdomains: 'abcd', maxZoom: 19
  }).addTo(leafMap);
  setTimeout(() => leafMap.invalidateSize(), 150);
}

async function geocodeZip(zip) {
  if (geoCache[zip]) return geoCache[zip];
  try {
    const r = await fetch(
      `https://nominatim.openstreetmap.org/search?postalcode=${encodeURIComponent(zip)}&countrycodes=us&format=json&limit=1`,
      { headers: { 'User-Agent': 'ZHVI-Dashboard/1.0', 'Accept-Language': 'en-US' } }
    );
    const d = await r.json();
    if (d && d[0]) {
      const c = { lat: parseFloat(d[0].lat), lng: parseFloat(d[0].lon) };
      geoCache[zip] = c; return c;
    }
  } catch(e) { console.warn('Geocode failed', zip); }
  return null;
}

async function addPinToMap(zip) {
  // Switch to map view
  setSection('map');
  // Already pinned → just fly to it
  if (mapPins[zip]) {
    const p = mapPins[zip];
    leafMap.setView([p.lat, p.lng], Math.max(leafMap.getZoom(), 10));
    p.marker.openPopup();
    updatePPPinBtn();
    return;
  }
  showToast('🔍 Locating ' + zip + '…');
  const coords = await geocodeZip(zip);
  if (!coords) { showToast('⚠️ Could not locate ZIP ' + zip); return; }

  const zi = D.zhvi.index[zip], zr = zi != null ? D.zhvi.records[zi] : null;
  const fi = D.zhvf.index[zip], fr = fi != null ? D.zhvf.records[fi] : null;
  const oi = D.zori.index[zip], or_ = oi != null ? D.zori.records[oi] : null;
  const city = zr?.city || fr?.city || or_?.city || '';
  const state = zr?.state || fr?.state || or_?.state || '';
  const value = zr?.value;
  const yoy = zr?.yoy;
  const rent = or_?.rent;
  const f12 = fr?.f12;
  const temp = zr?.temp || 'unknown';
  const tc = TC[temp] || TC.unknown;
  const color = tc.color;

  const icon = L.divIcon({
    className: '',
    html: `<div style="position:relative">
      <div style="width:16px;height:16px;border-radius:50%;background:${color};border:2.5px solid #fff;box-shadow:0 0 10px ${color}90,0 2px 6px rgba(0,0,0,.5);"></div>
      <div style="position:absolute;top:-20px;left:50%;transform:translateX(-50%);background:rgba(15,30,53,.9);color:#dde6f0;font-size:9px;font-weight:700;font-family:monospace;padding:1px 4px;border-radius:4px;white-space:nowrap;border:1px solid rgba(255,255,255,.15)">${zip}</div>
    </div>`,
    iconSize: [16, 16], iconAnchor: [8, 8],
  });

  const marker = L.marker([coords.lat, coords.lng], { icon }).addTo(leafMap);
  const popup = `<div style="font-family:-apple-system,sans-serif;min-width:170px;padding:2px">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
      <span style="font-size:18px;font-weight:800;color:#5b8ff9;font-family:monospace">${zip}</span>
      <span style="background:${color}22;color:${color};border:1px solid ${color}50;border-radius:12px;padding:2px 7px;font-size:9px;font-weight:700">${tc.lbl}</span>
    </div>
    <div style="font-size:12px;color:#8892a4;margin-bottom:8px">${[city,state].filter(Boolean).join(', ')||'—'}</div>
    ${value?`<div style="font-size:14px;font-weight:700;margin-bottom:2px">$${Math.round(value).toLocaleString()}</div>`:''}
    ${yoy!=null?`<div style="font-size:11px;color:${yoy>=0?'#34d399':'#f87171'};margin-bottom:2px">${yoy>=0?'+':''}${yoy.toFixed(2)}% YoY (home value)</div>`:''}
    ${rent?`<div style="font-size:11px;color:#7a90a8">Rent: $${Math.round(rent).toLocaleString()}/mo</div>`:''}
    ${f12!=null?`<div style="font-size:11px;color:${f12>=0?'#34d399':'#f87171'}">12-mo forecast: ${f12>=0?'+':''}${f12.toFixed(1)}%</div>`:''}
    <div style="display:flex;gap:5px;margin-top:10px">
      <button onclick="openZipProfile('${zip}');closeMapPopup()" style="flex:1;background:#162848;border:1px solid rgba(91,143,249,.3);border-radius:6px;padding:5px 8px;color:#5b8ff9;font-size:10px;font-weight:600;cursor:pointer">📋 Profile</button>
      <button onclick="removePin('${zip}')" style="background:#162848;border:1px solid rgba(255,255,255,.1);border-radius:6px;padding:5px 8px;color:#7a90a8;font-size:10px;cursor:pointer">✕ Remove</button>
    </div>
  </div>`;
  marker.bindPopup(popup, { maxWidth: 250, className: '' });

  mapPins[zip] = { lat: coords.lat, lng: coords.lng, marker, city, state, value, yoy, rent, temp };
  updateMapLines();
  renderPinList();
  leafMap.setView([coords.lat, coords.lng], Math.max(leafMap.getZoom(), 9));
  marker.openPopup();
  updatePPPinBtn();
  showToast('📍 ' + zip + (city ? ' · ' + city : '') + ' pinned');
}

function closeMapPopup() { if(leafMap) leafMap.closePopup(); }

function removePin(zip) {
  if (!mapPins[zip]) return;
  leafMap.removeLayer(mapPins[zip].marker);
  delete mapPins[zip];
  updateMapLines();
  renderPinList();
  leafMap.closePopup();
  updatePPPinBtn();
}

function clearAllPins() {
  Object.values(mapPins).forEach(p => { try{leafMap.removeLayer(p.marker);}catch(e){} });
  mapPins = {};
  mapLines.forEach(l => { try{leafMap.removeLayer(l);}catch(e){} });
  mapLines = [];
  renderPinList();
  updatePPPinBtn();
}

function updateMapLines() {
  mapLines.forEach(l => { try{leafMap.removeLayer(l);}catch(e){} });
  mapLines = [];
  const pins = Object.values(mapPins);
  if (pins.length < 2) return;
  for (let i = 0; i < pins.length; i++) {
    for (let j = i + 1; j < pins.length; j++) {
      const ln = L.polyline([[pins[i].lat,pins[i].lng],[pins[j].lat,pins[j].lng]],
        { color:'#5b8ff9', weight:1.5, opacity:.35, dashArray:'6,9' }).addTo(leafMap);
      mapLines.push(ln);
    }
  }
  if (pins.length >= 2) {
    const bounds = L.latLngBounds(pins.map(p => [p.lat, p.lng]));
    leafMap.fitBounds(bounds, { padding: [50, 50] });
  }
}

function haversine(lat1, lng1, lat2, lng2) {
  const R = 3958.8, r = Math.PI/180;
  const dLat = (lat2-lat1)*r, dLng = (lng2-lng1)*r;
  const a = Math.sin(dLat/2)**2 + Math.cos(lat1*r)*Math.cos(lat2*r)*Math.sin(dLng/2)**2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}

function renderPinList() {
  const el = document.getElementById('map-pin-list');
  const de = document.getElementById('map-dist-panel');
  const pins = Object.entries(mapPins);
  const cnt = document.getElementById('map-pin-count');
  const clrBtn = document.getElementById('map-clear-btn');

  cnt.textContent = pins.length + ' pin' + (pins.length !== 1 ? 's' : '');
  clrBtn.style.display = pins.length ? '' : 'none';

  if (!pins.length) {
    el.innerHTML = '<div class="map-empty-pins">Select ZIP codes from any table or type a ZIP above to drop pins on the map.</div>';
    de.style.display = 'none'; return;
  }

  el.innerHTML = pins.map(([zip, p]) => {
    const tc = TC[p.temp] || TC.unknown;
    return `<div class="map-pin-card">
      <div class="map-pin-hdr">
        <span class="zipcode" style="font-size:13px">${zip}</span>
        <button class="map-pin-rm" onclick="removePin('${zip}')" title="Remove pin">✕</button>
      </div>
      <div class="map-pin-loc">${[p.city,p.state].filter(Boolean).join(', ')||'—'}</div>
      ${p.value?`<div class="map-pin-val">$${Math.round(p.value).toLocaleString()}</div>`:''}
      ${p.yoy!=null?`<div class="map-pin-yoy ${p.yoy>=0?'pos':'neg'}">${p.yoy>=0?'+':''}${p.yoy.toFixed(2)}% YoY</div>`:''}
      <div style="margin:4px 0"><span class="badge ${tc.cls}" style="font-size:9px">${tc.lbl}</span></div>
      <div class="map-pin-actions">
        <button class="map-pin-btn" onclick="gotoPin('${zip}')">🎯 Center</button>
        <button class="map-pin-btn" onclick="openZipProfile('${zip}')">📋 Profile</button>
      </div>
    </div>`;
  }).join('');

  // Distances panel
  if (pins.length >= 2) {
    de.style.display = 'block';
    const pairs = [];
    for (let i = 0; i < pins.length; i++)
      for (let j = i+1; j < pins.length; j++) {
        const [z1,p1] = pins[i], [z2,p2] = pins[j];
        pairs.push({ z1, z2, mi: haversine(p1.lat,p1.lng,p2.lat,p2.lng) });
      }
    pairs.sort((a,b) => a.mi - b.mi);
    de.innerHTML = '<div class="map-dist-title">📐 Distances</div>' +
      pairs.map(({z1,z2,mi}) =>
        `<div class="map-dist-row">
          <span class="map-dist-zips">${z1} ↔ ${z2}</span>
          <span class="map-dist-val">${mi < 1 ? Math.round(mi*5280)+' ft' : mi.toFixed(1)+' mi'}</span>
        </div>`).join('');
  } else { de.style.display = 'none'; }
}

function gotoPin(zip) {
  const p = mapPins[zip];
  if (!p) return;
  leafMap.setView([p.lat, p.lng], Math.max(leafMap.getZoom(), 11));
  p.marker.openPopup();
}

async function mapSearchPin() {
  const inp = document.getElementById('map-zip-input');
  const zip = inp.value.trim().replace(/\D/g,'').padStart(5,'0').slice(-5);
  if (zip.length !== 5) { showToast('⚠️ Enter a 5-digit ZIP code'); return; }
  inp.value = '';
  await addPinToMap(zip);
}

// Update pin button in profile panel
function updatePPPinBtn() {
  const btn = document.getElementById('pp-pin-btn');
  if (!btn || !selectedZip) return;
  const isPinned = !!mapPins[selectedZip];
  btn.textContent = isPinned ? '✅ Pinned on Map' : '📍 Pin on Map';
  btn.className = 'pp-pin-btn' + (isPinned ? ' pinned' : '');
}

async function toggleProfilePin() {
  if (!selectedZip) return;
  if (mapPins[selectedZip]) { removePin(selectedZip); updatePPPinBtn(); }
  else { await addPinToMap(selectedZip); updatePPPinBtn(); }
}

"""
html = html.replace('// ── FILE UPLOAD SYSTEM', map_js + '\n// ── FILE UPLOAD SYSTEM', 1)

# ── 8. UPDATE setSection to handle 'map' ──────────────────────────────────────
# Find the setSection function and add map handling
old_setsec = """  // update views
  document.querySelectorAll('.section-view').forEach(el => el.classList.remove('active'));
  const sv = document.getElementById('sv-'+sec);
  if(sv) sv.classList.add('active');"""

new_setsec = """  // update views
  document.querySelectorAll('.section-view').forEach(el => el.classList.remove('active'));
  const sv = document.getElementById('sv-'+sec);
  if(sv) sv.classList.add('active');
  if(sec === 'map') { setTimeout(initMapView, 80); }"""

html = html.replace(old_setsec, new_setsec, 1)

# Add 'map' to SCFG
old_scfg_end = "  zorf:   { title:'Rental Forecast — ZORF (National)'"
new_scfg_end = "  map:    { title:'Map View', desc:'Visualize and compare ZIP code locations. Drop pins, measure distances.' },\n  zorf:   { title:'Rental Forecast — ZORF (National)'"
html = html.replace(old_scfg_end, new_scfg_end, 1)

# Fix setSection to not call applyFilters for map/zorf
old_apply = "  // update filters\n  const fb = document.getElementById('filter-bar');\n  fb.style.display = sec==='zorf' ? 'none' : 'flex';"
new_apply = "  // update filters\n  const fb = document.getElementById('filter-bar');\n  fb.style.display = (sec==='zorf'||sec==='map') ? 'none' : 'flex';"
html = html.replace(old_apply, new_apply, 1)

# Add 'map' to applyFilters guard (skip applyFilters for map)
old_apply2 = "  if(['zhvi','zhvf','zori'].includes(currentSection)) {"
new_apply2 = "  if(currentSection==='map'||currentSection==='zorf') return;\n  if(['zhvi','zhvf','zori'].includes(currentSection)) {"
html = html.replace(old_apply2, new_apply2, 1)

# Also update openZipProfile to refresh the pin button
old_open_profile_end = "  document.getElementById('profile-overlay').classList.add('open');"
new_open_profile_end = "  document.getElementById('profile-overlay').classList.add('open');\n  updatePPPinBtn();"
html = html.replace(old_open_profile_end, new_open_profile_end, 1)

# Write output
with open('/sessions/kind-beautiful-rubin/mnt/outputs/zhvi_dashboard.html', 'w') as f:
    f.write(html)

import os
sz = os.path.getsize('/sessions/kind-beautiful-rubin/mnt/outputs/zhvi_dashboard.html')
print(f"Written: {sz/1024/1024:.1f} MB")
