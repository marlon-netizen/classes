/* Growing in Values weekly pages: solves every activity with a bot, checks the saved state in the database, restores it in a second browser context,
   checks the spread of correct answer positions, dark mode, page errors and that written answers reach "Student responses" (resp- keys).
   Usage:  bash tools/test/pg.sh; node tools/test/mock.js &  node tools/test/e2e_gv.js [page.html …]   (default: every page of growing-in-values/) */
const { chromium } = require('playwright');
const { execSync } = require('child_process');
const fs = require('fs');
const P = process.env.LIA_PGDIR || '/tmp/lia-pg';
const sql = q => execSync(`psql -h ${P} -p 54329 -U postgres -At -c "${q.replace(/"/g, '\\"')}"`, { encoding: 'utf8' }).trim();
let fails = 0; const ok = (c, m) => { if (!c) fails++; console.log((c ? 'PASS' : 'FAIL') + ' ' + m); };
const R = process.env.LIA_SITE || 'file:///home/user/classes/';
async function fetchMock(r, u) { const q = r.request(); const res = await fetch('http://localhost:54400' + u.pathname + u.search, { method: q.method(), headers: q.headers(), body: ['GET', 'HEAD', 'OPTIONS'].includes(q.method()) ? undefined : q.postData() }); const hd = {}; res.headers.forEach((v, k) => hd[k] = v); r.fulfill({ status: res.status, headers: hd, body: Buffer.from(await res.arrayBuffer()) }); }
async function newCtx(b, extra) { const c = await b.newContext(Object.assign({ viewport: { width: 1200, height: 900 } }, extra || {})); await c.route('https://plctzbzncedwhmwumaaf.supabase.co/**', r => fetchMock(r, new URL(r.request().url()))); await c.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort()); return c; }
async function signIn(p, url, code) { await p.goto(url); await p.waitForSelector('#liaGate'); await p.fill('#liaCode', code); await p.click('#liaGate .lia-btn'); await p.waitForSelector('#liaUser .lia-name'); await p.waitForTimeout(1200); }

async function solve(p, a) {
  const root = '#' + a.id;
  if (a.type === 'quiz') {
    for (let i = 0; i < a.qs.length; i++) {
      const q = a.qs[i]; const blk = p.locator(root + ' .qblock').nth(i);
      await blk.locator('button.opt', { hasText: new RegExp('^' + q.o[q.a].replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '$') }).first().click();
    }
  } else if (a.type === 'multi') {
    for (let i = 0; i < a.qs.length; i++) {
      const q = a.qs[i]; const blk = p.locator(root + ' .qblock').nth(i);
      for (const k of q.a) await blk.locator('label.opt', { hasText: new RegExp('^' + q.o[k].replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '$') }).first().locator('input').check();
      await blk.locator('button.btn').click();
    }
  } else if (a.type === 'scenario') {
    for (let i = 0; i < a.steps.length; i++) {
      const best = a.steps[i].o.find(o => o.p === 2); const blk = p.locator(root + ' .qblock').nth(i);
      await blk.locator('button.opt', { hasText: new RegExp('^' + best.t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '$') }).first().click();
    }
  } else if (a.type === 'seq') {
    for (const it of a.items) await p.locator(root + ' .pool button.opt', { hasText: new RegExp('^' + it.t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '$') }).first().click();
  } else if (a.type === 'match') {
    for (const [l, r] of a.pairs) {
      await p.locator(root + ' .match > div:nth-child(1) button.opt', { hasText: new RegExp('^' + l.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '$') }).first().click();
      await p.locator(root + ' .match > div:nth-child(2) button.opt', { hasText: new RegExp('^' + r.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '$') }).first().click();
    }
  } else if (a.type === 'sort') {
    for (let i = 0; i < a.cards.length; i++) {
      const txt = (await p.locator(root + ' .sortcard span').innerText()).trim(); const c = a.cards.find(x => x[0] === txt);
      const lab = a.choices.find(x => x.k === c[1]).label; await p.locator(root + ' .row button.btn', { hasText: lab }).first().click();
    }
  } else if (a.type === 'cloze') {
    const sels = p.locator(root + ' select'); for (let i = 0; i < a.items.length; i++) await sels.nth(i).selectOption({ index: a.items[i][2] + 1 });
  } else if (a.type === 'open') {
    for (let i = 0; i < a.prompts.length; i++) await p.fill('#' + a.id + '-q' + i, 'This is my written answer number ' + (i + 1) + ' for ' + a.id + ' with enough words.');
  } else if (a.type === 'alloc') {
    const n = a.items.length, each = Math.floor((a.total || 100) / n), rest = (a.total || 100) - each * n;
    for (let i = 0; i < n; i++) await p.fill('#' + a.id + '-i' + i, String(each + (i === 0 ? rest : 0)));
    await p.fill('#' + a.id + '-why', 'I chose this split because every service helps the community.');
  } else if (a.type === 'calc') {
    const n = a.n || 5;
    for (let k = 0; k < n; k++) { const blk = p.locator(root + ' .qblock').nth(k); for (let t = 0; t < 3; t++) { await blk.locator('input.num').fill('0.123' + t); await blk.locator('button.btn').click(); } }
  } else throw new Error('unknown type ' + a.type);
}
async function snapshot(p) {   // everything the student sees that depends on saved state
  return p.evaluate(() => ({
    prog: document.getElementById('progText').textContent,
    good: Array.from(document.querySelectorAll('.opt.good,label.opt.good,select.good,input.num.good')).length,
    done: Array.from(document.querySelectorAll('.act.done')).map(x => x.id).join(','),
    areas: Array.from(document.querySelectorAll('textarea,input.amt')).map(x => x.value).join('|'),
    fb: Array.from(document.querySelectorAll('.fb.show')).map(x => x.textContent.slice(0, 40)).join('|'),
    ex: Array.from(document.querySelectorAll('.step.show')).length
  }));
}

(async () => {
  const pages = process.argv.slice(2).length ? process.argv.slice(2) : fs.readdirSync('/home/user/classes/growing-in-values').filter(f => f.endsWith('.html'));
  sql("delete from public.progress where area='growing-in-values'; delete from public.students where area='growing-in-values'");
  sql("insert into public.students(area,code,full_name,grade,class_name) values ('growing-in-values','GVTEST11','Gina Test','8','Growing in Values')");
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  for (const f of pages) {
    const url = R + 'growing-in-values/' + f, key = f.replace(/\.html$/, ''); console.log('\n== ' + f);
    const errs = [];
    const c1 = await newCtx(b), p = await c1.newPage(); p.on('pageerror', e => { errs.push(e.message); console.log('PAGEERR', e.message); }); p.on('console', m => { if (m.type() === 'error' && !/Failed to load resource|net::ERR/.test(m.text())) errs.push(m.text()); });
    await p.goto(url); await p.waitForSelector('#liaGate'); ok(true, 'sign-in gate shown on a new page');
    await signIn(p, url, 'GVTEST11');
    const GV = await p.evaluate(() => window.GV);
    ok(GV.acts.length >= 10, GV.acts.length + ' activities (' + [...new Set(GV.acts.map(a => a.type))].join(', ') + ')');
    ok(await p.$('#liaGate') === null || !(await p.isVisible('#liaGate')), 'signed in, gate hidden');
    ok(await p.evaluate(() => !!document.querySelector('#themeBtn')) && !(await p.$('.lia-theme')), 'one theme toggle only (own button)');
    // correct-answer positions over every quiz question
    const pos = {};
    for (const a of GV.acts.filter(x => x.type === 'quiz')) {
      const n = await p.locator('#' + a.id + ' .qblock').count();
      for (let i = 0; i < n; i++) { const q = a.qs[i]; const texts = await p.locator('#' + a.id + ' .qblock').nth(i).locator('button.opt').allInnerTexts(); const k = texts.map(t => t.trim()).indexOf(q.o[q.a]); const key2 = texts.length + ':' + k; pos[key2] = (pos[key2] || 0) + 1; }
    }
    const four = Object.keys(pos).filter(k => k.startsWith('4:')).length;
    ok(four >= 4, 'correct options spread over all 4 slots: ' + JSON.stringify(pos));
    for (const a of GV.acts) { await p.locator('#' + a.id).scrollIntoViewIfNeeded(); await solve(p, a); }
    await p.waitForTimeout(1300);
    ok(await p.isVisible('#overlay'), 'score summary opens when all activities are done');
    await p.click('#closeSummary');
    const s1 = await snapshot(p); ok(s1.prog === GV.acts.length + ' of ' + GV.acts.length + ' activities', 'progress ' + s1.prog);
    await p.waitForTimeout(2500);
    const row = sql("select solved||'/'||total||' '||score||'/'||max_score from public.progress where area='growing-in-values' and page_key='" + key + "'");
    ok(new RegExp('^' + GV.acts.length + '/' + GV.acts.length + ' ').test(row), 'database progress: ' + row);
    const resp = sql("select count(*) from public.progress p, jsonb_object_keys(p.state) k where p.area='growing-in-values' and p.page_key='" + key + "' and k like 'resp-%'");
    ok(+resp >= 2, resp + ' written-answer sets (resp-…) saved for the Student responses page');
    ok(errs.length === 0, 'no page errors' + (errs.length ? ': ' + errs.join(' / ') : ''));
    // restore on a second device
    const c2 = await newCtx(b), p2 = await c2.newPage(); p2.on('pageerror', e => errs.push(e.message));
    await signIn(p2, url, 'GVTEST11'); await p2.waitForTimeout(800);
    const s2 = await snapshot(p2);
    ok(JSON.stringify(s1) === JSON.stringify(s2), 'second browser shows the same answers, feedback and progress' + (JSON.stringify(s1) === JSON.stringify(s2) ? '' : '\n   A: ' + JSON.stringify(s1) + '\n   B: ' + JSON.stringify(s2)));
    ok(errs.length === 0, 'still no page errors after restore');
    // dark mode + screenshots
    await p2.evaluate(() => { document.documentElement.dataset.theme = 'dark'; });
    ok(await p2.evaluate(() => getComputedStyle(document.body).backgroundColor) !== 'rgb(238, 245, 244)', 'dark mode changes the background');
    if (process.env.SHOTS) { await p2.screenshot({ path: process.env.SHOTS + '/' + key + '-dark.png', fullPage: false }); await p2.evaluate(() => { document.documentElement.dataset.theme = 'light'; }); await p2.screenshot({ path: process.env.SHOTS + '/' + key + '-top.png' }); }
    await c1.close(); await c2.close();
  }
  // teacher side: the "Growing in Values" column on the home page, Student responses and Scores for this area
  const tc = await newCtx(b), t = await tc.newPage(); const terrs = []; t.on('pageerror', e => terrs.push(e.message));
  await t.goto(R + 'index.html'); await t.fill('#lEmail', 't@x.org'); await t.fill('#lPass', 'secret'); await t.click('#lBtn'); await t.waitForSelector('#home:not([hidden])');
  ok(await t.$('section[data-area="growing-in-values"]') !== null, 'teacher home has a separate Growing in Values column');
  const nl = await t.$$eval('section[data-area="growing-in-values"] a.lk', a => a.length); ok(nl === fs.readdirSync('/home/user/classes/growing-in-values').filter(f => f.endsWith('.html')).length, 'home lists ' + nl + ' lesson links to share');
  ok(await t.$$eval('section[data-area="growing-in-values"] a.btn', a => a.map(x => x.getAttribute('href')).join(' ')).then(h => /responses\.html\?area=growing-in-values/.test(h) && /scores\.html\?area=growing-in-values/.test(h) && /access\.html\?area=growing-in-values/.test(h) && /admin\.html\?area=growing-in-values/.test(h)), 'column has Scores, Students & codes, Assign lessons and Student responses buttons');
  await t.goto(R + 'teacher/responses.html?area=growing-in-values'); await t.waitForTimeout(800); if (await t.isVisible('#lEmail')) { await t.fill('#lEmail', 't@x.org'); await t.fill('#lPass', 'secret'); await t.click('#lBtn'); } await t.waitForSelector('#list .sc', { timeout: 8000 });
  const body = await t.$eval('#list', e => e.textContent); ok(/Gina Test/.test(body) && /Exit ticket/.test(body) && /Q02 Week/.test(body), 'Student responses lists the student, the Q02 week and the exit ticket');
  ok(/for act-exit with enough words/.test(body), 'the written answer text is visible to the teacher');
  await t.goto(R + 'teacher/scores.html?area=growing-in-values'); await t.waitForSelector('#grid tbody tr', { timeout: 8000 });
  ok(/Gina Test/.test(await t.$eval('#grid', e => e.textContent)), 'Scores & progress lists the student for this area');
  ok(terrs.length === 0, 'no page errors on teacher pages' + (terrs.length ? ': ' + terrs.join(' / ') : ''));
  await b.close();
  console.log(fails ? '\n' + fails + ' FAILED' : '\nALL PASSED'); process.exit(fails ? 1 : 0);
})();
