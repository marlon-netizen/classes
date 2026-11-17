// 10th-grade Social Science, Unit III page: sign-in gate, all 4 lessons render, every activity type answers + saves + restores on a second device,
// correct-answer positions are spread, dark mode, phone width, teacher "Student responses" lists the sets, no page errors.
// Run:  bash tools/test/pg.sh; node tools/test/mock.js &  node tools/test/e2e_ss10.js
const { chromium } = require('playwright');
const {execSync}=require('child_process');
const P=process.env.LIA_PGDIR||'/tmp/lia-pg';
const sql=q=>execSync(`psql -h ${P} -p 54329 -U postgres -At -c "${q.replace(/"/g,'\\"')}"`,{encoding:'utf8'}).trim();
let bad=0; const ok=(c,m)=>{ if(!c) bad++; console.log((c?'PASS':'FAIL')+' '+m); };
async function fetchMock(r,u){ const q=r.request(); const res=await fetch('http://localhost:54400'+u.pathname+u.search,{method:q.method(),headers:q.headers(),body:['GET','HEAD','OPTIONS'].includes(q.method())?undefined:q.postData()}); const hd={}; res.headers.forEach((v,k)=>hd[k]=v); r.fulfill({status:res.status,headers:hd,body:Buffer.from(await res.arrayBuffer())}); }
async function newCtx(b,w=1200){ const c=await b.newContext({viewport:{width:w,height:900}}); await c.route('https://plctzbzncedwhmwumaaf.supabase.co/**',r=>fetchMock(r,new URL(r.request().url()))); await c.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort()); return c; }
const SITE=process.env.LIA_SITE||'file:///home/user/classes/';
const PAGE=SITE+'ciencias-sociales/social-science-10-unit-3.html';
async function login(pg,code){ await pg.goto(PAGE); await pg.waitForSelector('#liaGate'); await pg.fill('#liaCode',code); await pg.click('#liaGate .lia-btn'); await pg.waitForSelector('#liaUser .lia-name'); await pg.waitForTimeout(1500); }
const MODES=['mcq','tf','cloze','voc','match','sort','order','map','src','wr'];
(async()=>{
  sql("delete from public.lesson_access; delete from public.progress; delete from public.students");
  sql("insert into public.students(area,code,full_name,grade,class_name) values ('ciencias-sociales','SSTEN100','Carlos Mora','10','Social Science'),('ciencias-sociales','SSTEN200','Eva Ruiz','10','Social Science')");
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}); const errs=[];
  try{
  // ---------- 1. offline preview (no LiaSync): everything renders and works without it
  { const c=await b.newContext(); const pg=await c.newPage(); pg.on('pageerror',e=>errs.push('pre:'+e.message)); await pg.route(/fonts\./,r=>r.abort()); await pg.route(/lia-config|lia-sync/,r=>r.abort());
    await pg.goto(PAGE); await pg.waitForTimeout(500);
    ok((await pg.$$('.tabpanel')).length===5,'5 panels (home + 4 lessons)');
    for(let l=1;l<=4;l++){
      await pg.click(`#mainNav button[data-t=l${l}]`);
      const voc=await pg.$$eval(`#p-l${l} .vcard`,e=>e.length); ok(voc>=8,`lesson ${l}: ${voc} vocabulary cards`);
      const tbl=await pg.$$eval(`#p-l${l} #t${l} .mini, #p-l${l} #t${l} .chain`,e=>e.length); ok(tbl>=3,`lesson ${l}: study card has content blocks (${tbl})`);
      await pg.click(`#p-l${l} .subnav button[data-s=practice]`);
      const tabs=await pg.$$eval(`#p-l${l} .ptab`,e=>e.map(x=>x.dataset.p)); ok(tabs.join()===MODES.join(),`lesson ${l}: 10 activity types (${tabs.length})`);
      for(const m of MODES){
        await pg.click(`#p-l${l} .ptab[data-p=${m}]`); const n=await pg.$$eval(`#p-l${l} .quiz .q`,e=>e.length); if(!n) ok(false,`lesson ${l} ${m}: no cards`);
        // no duplicate options inside one card, and 2-6 options
        const dupes=await pg.$$eval(`#p-l${l} .quiz .q`,cs=>cs.filter(c=>{const t=[...c.querySelectorAll('.opt')].map(x=>x.textContent);return t.length&&new Set(t).size!==t.length;}).length);
        if(dupes) ok(false,`lesson ${l} ${m}: duplicate options`);
      }
    }
    // pins on the map are dimmed per lesson
    await pg.click('#mainNav button[data-t=l4]'); const dim=await pg.$$eval('.pin',p=>p.filter(x=>x.classList.contains('dim')).length); ok(dim===4,`map: lesson 4 shows 3 pins, ${dim} dimmed`);
    // dark mode toggle
    const bg1=await pg.evaluate(()=>getComputedStyle(document.body).backgroundColor); await pg.click('#themeBtn'); const bg2=await pg.evaluate(()=>getComputedStyle(document.body).backgroundColor);
    ok(bg1!==bg2,'theme toggle changes colours ('+bg1+' → '+bg2+')'); await c.close(); }
  // ---------- 2. signed-in student: gate, answer everything, reporting
  const c1=await newCtx(b); const p=await c1.newPage(); p.on('pageerror',e=>errs.push('p:'+e.message));
  await p.goto(PAGE); await p.waitForSelector('#liaGate'); ok(true,'sign-in gate shows on the new page');
  await login(p,'SSTEN100');
  const hist={}; let total=0;
  const answerAll=async(page,l)=>{
    await page.click(`#mainNav button[data-t=l${l}]`); await page.click(`#p-l${l} .subnav button[data-s=practice]`);
    for(const m of ['mcq','tf','cloze','voc','src']){
      await page.click(`#p-l${l} .ptab[data-p=${m}]`); await page.waitForTimeout(80);
      const n=await page.$$eval(`#p-l${l} .quiz .q`,e=>e.length);
      for(let i=0;i<n;i++){ const sel=`#p-l${l} .quiz .q:nth-child(${i+1}) .opt`; const opts=await page.$$(sel); if(!opts.length) continue; await opts[0].click();
        if(opts.length===4){ const idx=await page.$$eval(sel,o=>o.findIndex(x=>x.classList.contains('right'))); hist[idx]=(hist[idx]||0)+1; total++; } }
    }
    await page.click(`#p-l${l} .ptab[data-p=match]`); for(const q of await page.$$(`#p-l${l} .quiz .q`)){ for(const s of await q.$$('select')) await s.selectOption({index:1}); await (await q.$('.btn')).click(); }
    await page.click(`#p-l${l} .ptab[data-p=sort]`); for(const q of await page.$$(`#p-l${l} .quiz .q`)){ for(const r of await q.$$('.srow')) await (await r.$('.cat')).click(); }
    await page.click(`#p-l${l} .ptab[data-p=order]`); for(const q of await page.$$(`#p-l${l} .quiz .q`)) await (await q.$('.btn')).click();
    await page.click(`#p-l${l} .ptab[data-p=map]`); for(const q of await page.$$(`#p-l${l} .quiz .q`)) await (await q.$('path.d')).click();
    await page.click(`#p-l${l} .ptab[data-p=wr]`); const w=await page.$$(`#p-l${l} .quiz .q`);
    await (await w[0].$('textarea')).fill('Independence ended the Spanish monopoly and opened trade, but civil war, debt and unstable production hurt the economy, and the criollo elite who owned land benefited most from the new State and its sovereignty.');
    await page.waitForTimeout(700); await (await w[0].$('.btn')).click();
  };
  for(let l=1;l<=4;l++) await answerAll(p,l);
  ok(total>=60,`answered ${total} four-option cards`); console.log('correct-position histogram (slot:count)',JSON.stringify(hist));
  const mx=Math.max(...Object.values(hist)); ok(Object.keys(hist).length===4&&mx/total<=0.4,'correct option spread over all 4 slots (max share '+Math.round(mx/total*100)+'%)');
  const keys=await p.evaluate(()=>Object.keys(localStorage).filter(k=>k.startsWith('resp-ss10u3')).sort()); ok(keys.length===40,'40 response sets saved (4 lessons × 10 activities): '+keys.length);
  ok(!(await p.evaluate(()=>Object.keys(localStorage).some(k=>/^resp-u3-/.test(k)))),'no key collision with the 11th-grade page');
  await p.waitForTimeout(2500);
  const row=sql("select p.page_key||'|'||p.solved||'|'||p.total||'|'||p.score||'|'||p.max_score from public.progress p join public.students s on s.id=p.student_id where s.code='SSTEN100'");
  console.log('progress row:',row); const [pk,sv,tt,sc,mxs]=row.split('|'); ok(pk==='social-science-10-unit-3'&&+tt===40&&+sv>=30&&+mxs>0&&+sc>0,'teacher dashboard row: page key, solved/total, score/max');
  // ---------- 3. second device restores everything
  const c2=await newCtx(b); const q=await c2.newPage(); q.on('pageerror',e=>errs.push('q:'+e.message)); await login(q,'SSTEN100');
  await q.click('#mainNav button[data-t=l2]'); await q.click('#p-l2 .subnav button[data-s=practice]');
  const st=await q.$$eval('#p-l2 .quiz .q .opt:disabled',e=>e.length); ok(st>=4,'second device: MCQ answers restored with feedback ('+st+' disabled options)');
  const fb=await q.$$eval('#p-l2 .quiz .q .fb.show',e=>e.length); ok(fb>=1,'second device: feedback shown again');
  await q.click('#p-l1 .ptab[data-p=wr]').catch(()=>{}); await q.click('#mainNav button[data-t=l1]'); await q.click('#p-l1 .subnav button[data-s=practice]'); await q.click('#p-l1 .ptab[data-p=wr]');
  const tx=await q.$$eval('#p-l1 .quiz textarea',e=>e.map(x=>x.value)); ok(tx.some(x=>/Spanish monopoly/.test(x)),'second device: written answer restored');
  // other student on same code area sees nothing of Carlos
  const c3=await newCtx(b); const r=await c3.newPage(); await login(r,'SSTEN200'); await r.click('#mainNav button[data-t=l1]'); await r.click('#p-l1 .subnav button[data-s=practice]'); ok((await r.$$('#p-l1 .quiz .opt:disabled')).length===0,'another student starts empty');
  // ---------- 4. phone width: no horizontal scroll
  const cm=await newCtx(b,375); const m=await cm.newPage(); await login(m,'SSTEN200');
  for(const t of ['home','l1','l2','l3','l4']){ await m.click(`#mainNav button[data-t=${t}]`); const w=await m.evaluate(()=>[document.documentElement.scrollWidth,innerWidth]); ok(w[0]<=w[1]+1,`phone: ${t} fits (${w[0]}/${w[1]})`); }
  await m.screenshot({path:process.env.SHOT||'/tmp/ss10_phone.png'});
  // ---------- 5. teacher page lists the sets
  const tc=await newCtx(b), t=await tc.newPage(); await t.goto(SITE+'teacher/responses.html?area=ciencias-sociales'); await t.fill('#lEmail','t@x.org'); await t.fill('#lPass','secret'); await t.click('#lBtn'); await t.waitForSelector('#list .sc',{timeout:8000});
  const body=await t.$eval('#list',e=>e.textContent); ok(/Carlos Mora/.test(body)&&/10th Unit III/.test(body),'teacher "Student responses" shows Carlos and 10th Unit III sets'); ok(/Spanish monopoly/.test(body),'written answer visible to the teacher');
  }catch(e){ ok(false,'exception: '+e.message); }
  console.log('page errors:',errs); ok(errs.length===0,'no page errors'); await b.close(); console.log(bad?('FAILED: '+bad):'ALL PASSED'); process.exit(bad?1:0);
})();
