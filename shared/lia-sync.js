/* LiaSync – student sign-in with an access code, and progress saved to Supabase.
 *
 * Every lesson page loads this file (after its folder's lia-config.js) in <head>.
 *  - The student types the code their teacher gave them once per folder (area).
 *    The same code then works on every page of that folder.
 *  - Whatever the page keeps in localStorage (answers, scores, names, drafts…) is
 *    mirrored to the database a moment after every change, and restored from the
 *    database the next time the student signs in – on this or any other device.
 *  - Works offline too: changes are kept on the device and uploaded when the
 *    connection returns.
 *  - If lia-config.js still has the placeholder URL/key, nothing changes: the page
 *    works exactly as before (progress stays in this browser only).
 */
(function () {
  'use strict';
  var CFG = window.LIA_CONFIG || {};
  var LIVE = !!(CFG.url && CFG.anonKey && !/YOUR_SUPABASE/.test(CFG.url + CFG.anonKey));
  /* ---------- light / dark toggle (every page that supports it, same stored choice) ---------- */
  (function theme() {
    var root = document.documentElement, mq = window.matchMedia ? matchMedia('(prefers-color-scheme: dark)') : null;
    try { var t = localStorage.getItem('lia-theme'); if (t === 'light' || t === 'dark') root.setAttribute('data-theme', t); } catch (e) {}
    function eff() { return root.getAttribute('data-theme') || ((mq && mq.matches) ? 'dark' : 'light'); }
    function sync() { var e = eff(); [].forEach.call(document.querySelectorAll('[data-theme-set]'), function (b) { b.setAttribute('aria-pressed', String(b.dataset.themeSet === e)); }); }
    function build() {
      var css = ''; [].forEach.call(document.styleSheets, function (ss) { try { [].forEach.call(ss.cssRules, function (r) { css += r.cssText.slice(0, 120); }); } catch (e) {} });
      var supports = /data-theme/.test(css);
      var own = document.querySelector('[data-theme-set],#themeBtn,#theme,.themeBtn,#themeToggle,button[aria-label*="heme"]');
      if (!supports || own) { sync(); return; }
      var st = document.createElement('style');
      st.textContent = '.lia-theme{position:absolute;top:10px;right:max(12px,calc((100vw - 1020px)/2 + 12px));display:inline-flex;border:1px solid rgba(128,128,128,.5);border-radius:99px;overflow:hidden;background:rgba(255,255,255,.14);z-index:50;font-family:inherit}' +
        '.lia-theme button{appearance:none;border:0;background:none;color:inherit;font:600 .78rem/1 inherit;font-family:inherit;letter-spacing:.06em;text-transform:uppercase;padding:6px 11px;cursor:pointer;display:inline-flex;gap:5px;align-items:center}' +
        '.lia-theme button[aria-pressed="true"]{background:#f3f0e9;color:#1b2f4b}@media print{.lia-theme{display:none}}';
      document.head.appendChild(st);
      var host = document.querySelector('header') || document.body;
      if (getComputedStyle(host).position === 'static') host.style.position = 'relative';
      var box = document.createElement('div'); box.className = 'lia-theme'; box.setAttribute('role', 'group'); box.setAttribute('aria-label', 'Color theme');
      box.innerHTML = '<button type="button" data-theme-set="light" aria-pressed="false">☀ Light</button><button type="button" data-theme-set="dark" aria-pressed="false">☾ Dark</button>';
      host.appendChild(box);
      [].forEach.call(box.querySelectorAll('button'), function (b) { b.addEventListener('click', function () { root.setAttribute('data-theme', b.dataset.themeSet); try { localStorage.setItem('lia-theme', b.dataset.themeSet); } catch (e) {} sync(); }); });
      sync();
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build); else build();
  })();

  if (!LIVE) { window.LiaSync = { live: false, name: function () { return ''; }, report: function () {} }; return; }
  document.documentElement.classList.add('lia-live');

  var AREA = CFG.area || 'default';
  var PAGE = (document.querySelector('meta[name="lia-page"]') || {}).content ||
    (location.pathname.split('/').pop() || 'index').replace(/\.html?$/i, '').replace(/[^a-z0-9-]/gi, '-').toLowerCase() || 'index';
  var K_ACCESS = 'lia-access:' + AREA, HUB = !!document.querySelector('meta[name="lia-hub"]'), K_CODE = 'lia-code:' + AREA, K_NAME = 'lia-name:' + AREA, K_MIRROR = 'lia-mirror:' + AREA + ':' + PAGE, K_RELOAD = 'lia-reloaded:' + AREA + ':' + PAGE;
  var BASE = String(CFG.url).replace(/\/+$/, '') + '/rest/v1/rpc/';

  var _get = Storage.prototype.getItem, _set = Storage.prototype.setItem, _rem = Storage.prototype.removeItem;
  function lsGet(k) { try { return _get.call(localStorage, k); } catch (e) { return null; } }
  function lsSet(k, v) { try { _set.call(localStorage, k, v); } catch (e) {} }
  function lsDel(k) { try { _rem.call(localStorage, k); } catch (e) {} }

  var code = lsGet(K_CODE) || '';
  var student = { name: lsGet(K_NAME) || '' };
  var access = null, blocked = false;      // access: which lessons this student's grade + class may open
  try { access = JSON.parse(lsGet(K_ACCESS) || 'null'); } catch (e) { access = null; }
  var mirror = null;            // { owner, state:{key:string}, dirty }
  var applying = false, reloading = false, inflight = false, timer = null, retry = null;
  var sum = { solved: 0, total: 0, score: 0, max: 0 }, reported = false;
  var statusEl = null;

  try { mirror = JSON.parse(lsGet(K_MIRROR) || 'null'); } catch (e) { mirror = null; }
  function saveMirror() { if (mirror) lsSet(K_MIRROR, JSON.stringify(mirror)); }

  /* ---------- keeping the page's own localStorage in step ---------- */
  function trackable(k) { return k && !/^lia-(code|name|mirror|reloaded|theme|admin-session|access)/.test(String(k)); }   // the module's own keys and the theme are not student work
  function applyState(state, previous) {      // write a saved state into localStorage (silently)
    applying = true;
    try {
      var k;
      if (previous) for (k in previous) if (!(k in state)) { lsDel(k); try { sessionStorage.removeItem(k); } catch (e) {} }
      for (k in state) lsSet(k, state[k]);
    } finally { applying = false; }
  }
  function wipeKeys(state) {                  // remove a (previous) student's data from this device
    applying = true;
    try {
      for (var k in (state || {})) { lsDel(k); try { sessionStorage.removeItem(k); } catch (e) {} }
      try { if (window.name && window.name.length > 20) window.name = ''; } catch (e) {}
    } finally { applying = false; }
  }
  function sameState(a, b) {
    var ka = Object.keys(a || {}).sort(), kb = Object.keys(b || {}).sort();
    if (ka.length !== kb.length) return false;
    for (var i = 0; i < ka.length; i++) if (ka[i] !== kb[i] || a[ka[i]] !== b[kb[i]]) return false;
    return true;
  }

  Storage.prototype.setItem = function (k, v) {
    _set.apply(this, arguments);
    try { if (this === localStorage && !applying && !reloading && !blocked && code && mirror && trackable(k)) onWrite(String(k), String(v)); } catch (e) {}
  };
  Storage.prototype.removeItem = function (k) {
    _rem.apply(this, arguments);
    try { if (this === localStorage && !applying && !reloading && !blocked && code && mirror && trackable(k)) onWrite(String(k), null); } catch (e) {}
  };
  function onWrite(k, v) {
    if (v === null) delete mirror.state[k]; else mirror.state[k] = v;
    mirror.dirty = true; saveMirror(); setStatus('Saving…', 'busy'); schedule();
  }

  /* ---------- boot (runs before the page's own scripts) ---------- */
  if (code) {
    if (mirror && mirror.owner !== code) { wipeKeys(mirror.state); mirror = null; lsDel(K_MIRROR); }
    if (!mirror) mirror = { owner: code, state: {}, dirty: false };
    applyState(mirror.state);                 // the page now starts with this student's saved work
  } else {
    if (mirror) { wipeKeys(mirror.state); mirror = null; lsDel(K_MIRROR); }
    document.documentElement.classList.add('lia-locked');
  }

  /* ---------- network ---------- */
  function headers() { var h = { 'Content-Type': 'application/json', apikey: CFG.anonKey }; if (/^eyJ/.test(CFG.anonKey)) h.Authorization = 'Bearer ' + CFG.anonKey; return h; }
  function rpc(fn, args, keep) {
    var ctl = window.AbortController ? new AbortController() : null, to = setTimeout(function () { if (ctl) ctl.abort(); }, 15000);
    return fetch(BASE + fn, { method: 'POST', headers: headers(), body: JSON.stringify(args), keepalive: !!keep, signal: ctl ? ctl.signal : undefined })
      .then(function (r) { clearTimeout(to); if (!r.ok) throw new Error('http ' + r.status); return r.json(); }, function (e) { clearTimeout(to); throw e; });
  }

  /* ---------- saving ---------- */
  function examplesDone() {
    var n = 0; Object.keys(mirror.state).forEach(function (k) { try { var o = JSON.parse(mirror.state[k]); if (o && typeof o === 'object') Object.keys(o).forEach(function (x) { if (x.indexOf('ex_') === 0) n++; }); } catch (e) {} }); return n;
  }
  function push(keep) {
    if (blocked || !code || !mirror || !mirror.dirty) return Promise.resolve();
    if (inflight && !keep) return Promise.resolve();
    inflight = true; setStatus('Saving…', 'busy');
    var snap = JSON.stringify(mirror.state);
    var args = { p_area: AREA, p_code: code, p_page: PAGE, p_state: mirror.state, p_solved: sum.solved, p_total: sum.total, p_examples: examplesDone(), p_score: reported ? sum.score : sum.solved, p_max_score: reported ? sum.max : sum.total };
    return rpc('lia_save_progress', args, keep)
      .catch(function (e) {   // database not yet updated with the score columns (schema.sql not re-run): save without them
        if (!/http 404/.test(String(e && e.message))) throw e;
        delete args.p_score; delete args.p_max_score; return rpc('lia_save_progress', args, keep);
      })
      .then(function (r) {
        inflight = false;
        if (r && r.ok) { if (JSON.stringify(mirror.state) === snap) { mirror.dirty = false; saveMirror(); setStatus('Saved ✓'); } else schedule(); }
        else if (r && r.error === 'invalid_code') { setStatus('Code no longer valid', 'off'); }
        else { setStatus('Could not save – retrying', 'off'); armRetry(); }
      }, function () { inflight = false; setStatus('Offline – will save when connected', 'off'); armRetry(); });
  }
  function schedule() { clearTimeout(timer); timer = setTimeout(function () { push(false); }, 700); }
  function armRetry() { if (retry) return; retry = setInterval(function () { if (!mirror || !mirror.dirty) { clearInterval(retry); retry = null; return; } push(false); }, 15000); }
  window.addEventListener('online', function () { push(false); });
  document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'hidden') { clearTimeout(timer); push(true); } });
  window.addEventListener('pagehide', function () { clearTimeout(timer); push(true); });

  /* ---------- on-screen bits ---------- */
  function css() {
    var st = document.createElement('style');
    st.textContent =
      '.lia-locked body>*:not(#liaGate){visibility:hidden!important}' +
      '#liaGate{position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;padding:20px;background:var(--bg,#f3f0e9);font-family:inherit}' +
      '#liaGate .lia-card{width:100%;max-width:420px;background:var(--surface,var(--card,#fff));color:var(--ink,#1e2937);border:1px solid var(--line,#ddd);border-radius:14px;padding:28px 26px;box-shadow:0 10px 40px rgba(0,0,0,.18)}' +
      '#liaGate .lia-brand{font-size:.78rem;text-transform:uppercase;letter-spacing:.14em;color:var(--warm,var(--primary,#b4763a));font-weight:700}' +
      '#liaGate h2{margin:.3em 0 .4em;font-size:1.6rem;color:var(--ink,#1e2937)}' +
      '#liaGate p{margin:0 0 1em;color:var(--muted,#5a6575)}' +
      '#liaGate label{display:block;font-weight:600;margin-bottom:6px}' +
      '#liaGate input{width:100%;font:inherit;font-size:1.3rem;letter-spacing:.2em;text-transform:uppercase;text-align:center;padding:12px;border:2px solid var(--line,#ddd);border-radius:10px;background:var(--surface,var(--card,#fff));color:var(--ink,#1e2937)}' +
      '#liaGate input:focus{outline:3px solid rgba(43,122,118,.4);border-color:var(--accent,var(--primary,#2b7a76))}' +
      '#liaGate .lia-btn{width:100%;margin-top:14px;font:inherit;font-weight:700;font-size:1.05rem;padding:12px;border-radius:10px;border:0;cursor:pointer;background:var(--primary,#1f3a5f);color:var(--primary-ink,#fff)}' +
      '#liaGate .lia-btn[disabled]{opacity:.6;cursor:wait}' +
      '#liaGate .lia-err{min-height:1.4em;margin-top:10px;color:var(--bad,#a94a3f);font-weight:600}' +
      '#liaGate .lia-small{margin:10px 0 0;font-size:.85rem}' +
      '#liaUser{position:fixed;right:12px;bottom:12px;z-index:9998;display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center;max-width:calc(100vw - 24px);padding:6px 12px;border-radius:99px;font:600 .82rem/1.3 inherit;font-family:inherit;background:var(--surface,var(--card,#fff));color:var(--ink,#1e2937);border:1px solid var(--line,#ddd);box-shadow:0 4px 16px rgba(0,0,0,.18)}' +
      '#liaUser .lia-save{padding:1px 9px;border-radius:99px;background:var(--good-soft,#e1f1e8);color:var(--good,#2c7a57)}' +
      '#liaUser .lia-save.busy{background:var(--blue-soft,#e6edf5);color:var(--primary,#1f3a5f)}' +
      '#liaUser .lia-save.off{background:var(--warm-soft,#f6ebdb);color:var(--warm,#b4763a)}' +
      '#liaUser a.lia-menu{color:var(--primary,#1f3a5f);text-decoration:none;font-size:.8rem;border:1px solid var(--line,#ccc);border-radius:8px;padding:2px 9px}' +
      '.lia-live [data-lia-reset]{display:none!important}' +
      '#liaUser button{font:inherit;font-size:.8rem;background:none;border:1px solid var(--line,#ccc);color:var(--primary,#1f3a5f);border-radius:8px;padding:2px 9px;cursor:pointer}' +
      '@media print{#liaUser{display:none}}';
    document.head.appendChild(st);
  }
  function chip() {
    var el = document.getElementById('liaUser');
    if (!el) {
      el = document.createElement('div'); el.id = 'liaUser';
      el.innerHTML = '<span>👤 <span class="lia-name"></span></span><span class="lia-save" role="status" aria-live="polite">Saved ✓</span><a class="lia-menu" href="index.html">☰ Menu</a><button type="button">Sign out</button>';
      el.querySelector('button').addEventListener('click', signOut);
      document.body.appendChild(el);
    }
    el.querySelector('.lia-name').textContent = student.name || '';
    statusEl = el.querySelector('.lia-save');
    if (mirror && mirror.dirty) setStatus('Saving…', 'busy');
  }
  function setStatus(t, cls) { if (statusEl) { statusEl.textContent = t; statusEl.className = 'lia-save' + (cls ? ' ' + cls : ''); } }

  function gate(msg) {
    var g = document.getElementById('liaGate'); if (g) g.remove();
    document.documentElement.classList.add('lia-locked');
    g = document.createElement('div'); g.id = 'liaGate';
    var area = (CFG.areaName || '').replace(/[<>&]/g, '');
    g.innerHTML = '<form class="lia-card" novalidate><div class="lia-brand">Lincoln International Academy' + (area ? ' · ' + area : '') + '</div><h2>Student sign-in</h2>' +
      '<p>Type the access code your teacher gave you. Your progress is saved to your account, so you can continue on any device.</p>' +
      '<label for="liaCode">Access code</label><input id="liaCode" autocomplete="off" autocapitalize="characters" spellcheck="false" maxlength="24" placeholder="XXXX-XXXX">' +
      '<button class="lia-btn" type="submit">Sign in</button><div class="lia-err" role="alert"></div><p class="lia-small">No code yet? Ask your teacher.</p></form>';
    document.body.appendChild(g);
    var f = g.querySelector('form'), i = g.querySelector('input'), e = g.querySelector('.lia-err'), b = g.querySelector('button');
    if (msg) e.textContent = msg; setTimeout(function () { i.focus(); }, 50);
    return new Promise(function (res) {
      f.addEventListener('submit', function (ev) {
        ev.preventDefault(); var c = i.value.replace(/[^A-Za-z0-9]/g, '').toUpperCase();
        if (c.length < 4) { e.textContent = 'Please type your full code.'; return; }
        b.disabled = true; e.textContent = '';
        rpc('lia_login', { p_area: AREA, p_code: c }).then(function (r) {
          if (r && r.ok) res({ code: c, info: r });
          else { b.disabled = false; e.textContent = r && r.error === 'too_many' ? 'Too many attempts. Please wait a few minutes and try again.' : 'That code was not recognised. Check it and try again.'; i.select(); }
        }, function () { b.disabled = false; e.textContent = 'Cannot reach the server. Check your internet connection and try again.'; });
      });
    });
  }

  /* ---------- who may open what (set by the teacher: Assign lessons) ---------- */
  function slug(f) { return String(f || '').split('?')[0].split('#')[0].split('/').pop().replace(/\.html?$/i, '').replace(/[^a-z0-9-]/gi, '-').toLowerCase() || 'index'; }
  function canOpen(k) { return !access || !access.restricted || access.restricted.indexOf(k) < 0 || (access.allowed || []).indexOf(k) >= 0; }
  function setAccess(a) { access = a && a.restricted ? a : null; if (access) lsSet(K_ACCESS, JSON.stringify(access)); else lsDel(K_ACCESS); }
  function showBlock() {
    blocked = true; clearTimeout(timer);
    var g = document.getElementById('liaGate'); if (g) g.remove();
    document.documentElement.classList.add('lia-locked');
    g = document.createElement('div'); g.id = 'liaGate';
    var who = [student.grade && ('Grade ' + student.grade), student.cls].filter(Boolean).join(' · ');
    g.innerHTML = '<div class="lia-card"><div class="lia-brand">Lincoln International Academy</div><h2>Not available for your class</h2>' +
      '<p>This lesson has not been assigned to ' + (who ? 'your class (' + who.replace(/[<>&]/g, '') + ')' : 'your class') + '. Go back to the menu to see your lessons.</p>' +
      '<a class="lia-btn" style="display:block;text-align:center;text-decoration:none" href="index.html">☰ My lessons</a></div>';
    document.body.appendChild(g);
  }
  function hubFilter() {      // on a folder menu: show only the lessons this student may open
    if (!HUB) return;
    var n = 0;
    [].forEach.call(document.querySelectorAll('a.card[href]'), function (a) {
      var ok = canOpen(slug(a.getAttribute('href'))); a.style.display = ok ? '' : 'none'; if (ok) n++;
    });
    var m = document.getElementById('liaNone');
    if (!n) { if (!m) { m = document.createElement('p'); m.id = 'liaNone'; m.textContent = 'No lessons have been assigned to your class yet.'; var gr = document.querySelector('.grid'); (gr ? gr.parentNode : document.body).appendChild(m); } }
    else if (m) m.remove();
  }
  function enforce() { if (!HUB && !canOpen(PAGE)) { showBlock(); return true; } hubFilter(); return false; }

  function signOut() {
    if (!confirm('Sign out? Your progress is already saved to your account.')) return;
    clearTimeout(timer);
    var finish = function () { reloading = true; wipeKeys(mirror && mirror.state); lsDel(K_MIRROR); lsDel(K_CODE); lsDel(K_NAME); lsDel(K_ACCESS); try { sessionStorage.removeItem(K_RELOAD); } catch (e) {} location.reload(); };
    push(true).then(finish, finish);
    setTimeout(finish, 2500);
  }

  /* ---------- sign-in flow (after the page has been parsed) ---------- */
  function afterLogin(got, firstTime) {
    code = got.code; student = { name: got.info.name || student.name, grade: got.info.grade || '', cls: got.info.class_name || '' }; lsSet(K_CODE, code); if (student.name) lsSet(K_NAME, student.name);
    setAccess(got.info.access); if (enforce()) { chip(); return new Promise(function () {}); }
    return rpc('lia_get_progress', { p_area: AREA, p_code: code, p_page: PAGE }).then(function (r) {
      var remote = {};
      if (r && r.ok && r.state && typeof r.state === 'object') Object.keys(r.state).forEach(function (k) { remote[k] = String(r.state[k]); });
      if (firstTime) {
        wipeKeys(mirror && mirror.state);
        mirror = { owner: code, state: remote, dirty: false }; saveMirror(); applyState(remote);
        reloading = true; location.reload();   // reload so the page starts with the restored work
        return new Promise(function () {});
      }
      if (!mirror) mirror = { owner: code, state: {}, dirty: false };
      if (mirror.dirty) {                        // unsaved work on this device wins; add anything only the server had
        Object.keys(remote).forEach(function (k) { if (!(k in mirror.state)) mirror.state[k] = remote[k]; });
        saveMirror(); push(false);
      } else if (!sameState(remote, mirror.state)) {   // progress made on another device
        var prev = mirror.state; mirror.state = remote; saveMirror(); applyState(remote, prev);
        var done = false; try { done = sessionStorage.getItem(K_RELOAD) === '1'; } catch (e) {}
        if (!done) { try { sessionStorage.setItem(K_RELOAD, '1'); } catch (e) {} reloading = true; location.reload(); return new Promise(function () {}); }
      } else { try { sessionStorage.removeItem(K_RELOAD); } catch (e) {} }
    }, function () { setStatus('Offline – showing saved progress', 'off'); armRetry(); });
  }
  function start() {
    css();
    if (!code) {
      gate('').then(function (got) { return afterLogin(got, true); });
      return;
    }
    document.documentElement.classList.remove('lia-locked');
    chip();
    enforce();                  // uses the last known access list while offline
    rpc('lia_login', { p_area: AREA, p_code: code }).then(function (r) {
      if (r && r.ok) { student.name = r.name || student.name; student.grade = r.grade || ''; student.cls = r.class_name || ''; if (student.name) lsSet(K_NAME, student.name); chip(); return afterLogin({ code: code, info: r }, false).then(watchProgress); }
      // code no longer valid (or too many attempts): start over
      reloading = true; wipeKeys(mirror && mirror.state); lsDel(K_MIRROR); lsDel(K_CODE); lsDel(K_NAME); lsDel(K_ACCESS); access = null; mirror = null; code = ''; reloading = false;
      var el = document.getElementById('liaUser'); if (el) el.remove();
      return gate(r && r.error === 'too_many' ? 'Too many attempts. Please wait a few minutes.' : 'Please sign in again.').then(function (got) { return afterLogin(got, true); });
    }, function () { setStatus('Offline – showing saved progress', 'off'); if (mirror && mirror.dirty) armRetry(); watchProgress(); });
  }
  /* pages that show "N of M … solved" in #overallText let the teacher see completion at a glance */
  function watchProgress() {
    var el = document.getElementById('overallText'); if (!el) return;
    var read = function () { if (reported) return; var m = /(\d+)\s+of\s+(\d+)/.exec(el.textContent || ''); if (m) { sum.solved = +m[1]; sum.total = +m[2]; } };
    read(); if (window.MutationObserver) new MutationObserver(read).observe(el, { childList: true, characterData: true, subtree: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();

  /* name(): the signed-in student's registered name – pages use it instead of asking for a name again */
  /* report({solved,total,score,max}, {keepBest}) – pages call this so the teacher dashboard can show progress and scores.
     keepBest: for pages that restart on every visit – the best result is kept (and saved) instead of the latest. */
  function report(o, opts) {
    try {
      var r = { solved: +o.solved || 0, total: +o.total || 0, score: +o.score || 0, max: +o.max || 0 };
      if (opts && opts.keepBest && mirror) {
        var best = null; try { best = JSON.parse(mirror.state._lia_best || 'null'); } catch (e) {}
        if (best && (best.solved > r.solved || (best.solved === r.solved && best.score >= r.score))) r = best;
        else { try { localStorage.setItem('_lia_best', JSON.stringify(r)); } catch (e) {} }
      }
      var changed = r.solved !== sum.solved || r.total !== sum.total || r.score !== sum.score || r.max !== sum.max || !reported;
      sum = r; reported = true;
      if (changed && code && mirror) { mirror.dirty = true; saveMirror(); schedule(); }
    } catch (e) {}
  }
  window.LiaSync = { live: true, area: AREA, page: PAGE, signOut: signOut, report: report, name: function () { return code ? (student.name || '') : ''; } };
})();
