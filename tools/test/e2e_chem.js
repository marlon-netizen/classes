// Chemistry Chapter 3 practice page: per-student tables, every row solvable, answers saved/restored, MC spread, phone width.
// Run:  bash tools/test/pg.sh; node tools/test/mock.js &  node tools/test/e2e_chem.js
const { chromium } = require('playwright');
const {execSync}=require('child_process');
const P=process.env.LIA_PGDIR||'/tmp/lia-pg';
const sql=q=>execSync(`psql -h ${P} -p 54329 -U postgres -At -c "${q.replace(/"/g,'\\"')}"`,{encoding:'utf8'}).trim();
let bad=0; const ok=(c,m)=>{ if(!c) bad++; console.log((c?'PASS':'FAIL')+' '+m); };
async function fetchMock(r,u){ const q=r.request(); const res=await fetch('http://localhost:54400'+u.pathname+u.search,{method:q.method(),headers:q.headers(),body:['GET','HEAD','OPTIONS'].includes(q.method())?undefined:q.postData()}); const hd={}; res.headers.forEach((v,k)=>hd[k]=v); r.fulfill({status:res.status,headers:hd,body:Buffer.from(await res.arrayBuffer())}); }
async function newCtx(b,w=1200){ const c=await b.newContext({viewport:{width:w,height:900}}); await c.route('https://plctzbzncedwhmwumaaf.supabase.co/**',r=>fetchMock(r,new URL(r.request().url()))); await c.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort()); return c; }
const PAGE=(process.env.LIA_SITE||'file:///home/user/classes/')+'physics/chemistry-chapter-3-atoms-practice.html';
async function login(pg,code){ await pg.goto(PAGE); await pg.waitForSelector('#liaGate'); await pg.fill('#liaCode',code); await pg.click('#liaGate .lia-btn'); await pg.waitForSelector('#liaUser .lia-name'); await pg.waitForTimeout(2300); }
(async()=>{
  sql("delete from public.lesson_access; delete from public.progress; delete from public.students");
  sql("insert into public.students(area,code,full_name,grade,class_name) values ('physics','AAAA1111','Ana Pérez','10','Chemistry'),('physics','BBBB2222','Luis Mora','10','Chemistry')");
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}); const errs=[];
  try{
  // ---------- 1. offline preview: sufficiency of every generated row over many seeds
  { const c=await b.newContext(); const pg=await c.newPage(); pg.on('pageerror',e=>errs.push('pre:'+e.message)); await pg.route(/fonts\./,r=>r.abort()); await pg.route(/lia-config|lia-sync/,r=>r.abort());
    let badRows=0, n=0, dup=0;
    for(let i=0;i<120;i++){
      await pg.goto(PAGE); 
      const r=await pg.evaluate(()=>{ const L=window.LIACHEM; let bad=[],rows=0,dup=0; L.TABLES.forEach(t=>{ const seen=new Set(); t.rows.forEach(r=>{ rows++; if(t.id!=='w'&&seen.has(r.sym)) dup++; seen.add(r.sym);
          const G=r.given, Z=L.BYSYM[r.sym].Z; let A=null,q=t.ion?null:0;
          if(G.includes('hyphen')||G.includes('sym')||G.includes('A')) A=r.A; if(G.includes('n')) A=Z+(r.A-Z);
          if(G.includes('q')) q=r.q; if(G.includes('e')) q=Z-(Z-r.q); if(G.includes('sym')) q=r.q;
          if(G.includes('p')&&G.length===1) {}
          if(A!==r.A||q!==r.q||(G.includes('sym')&&!t.ion&&r.q!==0)) bad.push(t.id+':'+r.sym+':'+G.join('+')); }); }); return {bad,rows,dup}; });
      badRows+=r.bad.length; n+=r.rows; dup+=r.dup; if(r.bad.length&&badRows<5) console.log(' bad',r.bad);
    }
    ok(badRows===0,`${n} generated rows over 120 seeds: all solvable from their clues`); ok(dup===0,'no repeated element inside a table');
    // generated problems finite and solvable with their own answers
    const pr=await pg.evaluate(()=>{ const L=window.LIACHEM; let bad=0; L.P.forEach(p=>{ if(p.parts) p.parts.forEach(x=>{ if(!x.txt){ if(!isFinite(x.ans)) bad++; const s=Math.abs(x.ans)>=1e5||Math.abs(x.ans)<1e-3?x.ans.toExponential(6):String(x.ans); const j=L.judge(s,x); if(j.state!=='ok') bad++; } else if(!x.ok(x.show)) bad++; }); }); return {bad,n:L.P.length}; });
    ok(pr.bad===0,`${pr.n} problems: every model answer accepted by its own checker`);
    await c.close(); }
  // ---------- 2. signed in: two students, different tables
  const ctxA=await newCtx(b), pg=await ctxA.newPage(); pg.on('pageerror',e=>errs.push(e.message));
  await login(pg,'AAAA1111');
  const sigA=await pg.evaluate(()=>window.LIACHEM.TABLES.map(t=>t.rows.map(r=>r.sym+r.A+r.q+r.given.join('')).join(',')).join('|'));
  const ctxB=await newCtx(b), pb=await ctxB.newPage(); pb.on('pageerror',e=>errs.push(e.message)); await login(pb,'BBBB2222');
  const sigB=await pb.evaluate(()=>window.LIACHEM.TABLES.map(t=>t.rows.map(r=>r.sym+r.A+r.q+r.given.join('')).join(',')).join('|'));
  ok(sigA!==sigB,'two students get different tables'); await ctxB.close();
  // ---------- 3. UI: tables
  const nRows=await pg.evaluate(()=>window.LIACHEM.TABLES.reduce((n,t)=>n+t.rows.length,0)); console.log('table rows',nRows);
  await pg.screenshot({path:'/tmp/chem_a.png'});
  // answer first table row wrong, then correctly; second table row partially; leave a typed-but-unchecked cell
  const tdefs=await pg.evaluate(()=>window.LIACHEM.TABLES.map(t=>({id:t.id,ion:t.ion,rows:t.rows.map(r=>({given:r.given,t:r.t,sym:r.sym,A:r.A,Z:r.Z,q:r.q}))})));
  async function fillRow(page,ti,ri,mode){
    const row=page.locator('.tblcard').nth(ti).locator('tr.crow').nth(ri); const d=tdefs[ti].rows[ri], keys=['hyphen','sym','Z','A','p','n','e'].concat(tdefs[ti].ion?['q']:[]);
    for(const k of keys){ if(d.given.includes(k)) continue;
      if(k==='sym'){ const ins=row.locator('td[data-k=sym] input'); await ins.nth(0).fill(String(mode==='bad'?d.A+1:d.A)); await ins.nth(1).fill(String(d.Z)); await ins.nth(2).fill(d.sym); }
      else { const inp=row.locator(`td[data-k=${k}] input`); let v; if(k==='hyphen') v=BYS(d)+'-'+d.A; else if(k==='q') v=d.q===0?'0':(d.q>0?'+'+d.q:'-'+Math.abs(d.q)); else v=String(d.t[k]); if(mode==='bad'&&k==='n') v=String(d.t.n+3); await inp.fill(v); } }
  }
  const NAMES=await pg.evaluate(()=>Object.fromEntries(Object.entries(window.LIACHEM.BYSYM).map(([k,v])=>[k,v.name]))); const BYS=d=>NAMES[d.sym];
  // stay on tables set (default)
  await pg.click('#setPicker button[data-set=tb]');
  await fillRow(pg,1,0,'bad'); await pg.locator('.tblcard').nth(1).locator('tr.crow').nth(0).locator('button.btn').first().click();
  ok(await pg.locator('.tblcard').nth(1).locator('tr.crow').nth(0).locator('td.no').count()>=1,'wrong cell is marked');
  await fillRow(pg,1,0,'good'); await pg.locator('.tblcard').nth(1).locator('tr.crow').nth(0).locator('button.btn').first().click();
  ok(await pg.locator('.tblcard').nth(1).locator('tr.crow.done').count()===1,'row solved after correcting');
  // a typed (unchecked) row in table 2 to test restore
  await fillRow(pg,2,0,'good'); // typed, not checked
  await pg.waitForTimeout(2600);
  const p2=await (await newCtx(b)).newPage(); p2.on('pageerror',e=>errs.push(e.message)); await login(p2,'AAAA1111');
  ok(await p2.locator('.tblcard').nth(1).locator('tr.crow.done').count()===1,'solved row restored on a second device');
  const firstBlank=tdefs[2].rows[0].given.includes('Z')?'A':'Z'; 
  ok((await p2.locator('.tblcard').nth(2).locator('tr.crow').nth(0).locator('input').first().inputValue()).length>0,'typed (unchecked) answers restored');
  // ---------- 4. solve everything
  for(let ti=0;ti<tdefs.length;ti++) for(let ri=0;ri<tdefs[ti].rows.length;ri++){
    const row=pg.locator('.tblcard').nth(ti).locator('tr.crow').nth(ri);
    if(await row.evaluate(e=>e.classList.contains('done'))) continue;
    await fillRow(pg,ti,ri,'good'); await row.locator('button.btn').first().click(); }
  const doneRows=await pg.locator('tr.crow.done').count(); ok(doneRows===nRows,`all ${nRows} table rows solved (${doneRows})`);
  // show-answer unlock after two wrong tries (use a fresh row after reset of state? use table w row 0 shown test)
  // problems
  const sets=await pg.evaluate(()=>window.LIACHEM.SETS.map(s=>s.id).filter(x=>x!=='tb'));
  let tot=0, solved=0;
  for(const sid of sets){
    await pg.click(`#setPicker button[data-set="${sid}"]`); const n=await pg.locator('.prob').count();
    for(let i=0;i<n;i++){
      const pr=pg.locator('.prob').nth(i);
      const info=await pg.evaluate(([sid,i])=>{ const p=window.LIACHEM.P.filter(p=>p.set===sid)[i]; return {parts:p.parts?p.parts.map(x=>x.txt?x.show:(Math.abs(x.ans)>=1e5||(Math.abs(x.ans)<1e-3&&x.ans!==0)?x.ans.toExponential(6):String(x.ans))):null,correct:p.correct||null}; },[sid,i]);
      if(info.parts){ const ins=pr.locator('input[type=text]'); for(let j=0;j<info.parts.length;j++) await ins.nth(j).fill(info.parts[j]); }
      else { for(const c of info.correct) await pr.locator('input').nth(c).check({force:true}); }
      await pr.locator('.acts .btn').first().click();
    }
    const d=await pg.locator('.prob.done').count(); tot+=n; solved+=d; if(d!==n) console.log(' set',sid,d,'/',n);
  }
  ok(solved===tot,`practice ${solved}/${tot} solved with model answers`);
  await pg.waitForTimeout(500); console.log(await pg.$eval('#overallText',e=>e.textContent));
  // MC spread
  const dist=await pg.evaluate(()=>{ const d={}; window.LIACHEM.P.forEach(p=>{ if(p.opts&&p.correct.length===1) d[p.correct[0]]=(d[p.correct[0]]||0)+1; }); return d; }); console.log('correct positions',JSON.stringify(dist)); ok(Object.keys(dist).length>=3&&Math.max(...Object.values(dist))<=Object.values(dist).reduce((a,x)=>a+x,0)*0.4,'MC correct answers spread');
  await pg.waitForTimeout(2500);
  console.log('DB:',sql("select page_key,solved,total,score,max_score from public.progress"));
  const resp=sql("select count(*) from public.progress p, jsonb_object_keys(p.state) k where k like 'resp-chemistry%'"); ok(resp==='1','responses saved under resp-');
  // dark mode + phone
  await pg.click('#setPicker button[data-set=tb]'); await pg.click('.theme [data-theme-set=dark]'); await pg.waitForTimeout(300); await pg.screenshot({path:'/tmp/chem_dark.png'});
  const mc=await newCtx(b,390); const mp=await mc.newPage(); await login(mp,'AAAA1111'); ok(await mp.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+2),'no horizontal page scroll on phone width');
  console.log('errors',errs.filter(e=>!/ERR_FAILED/.test(e)));
  }catch(e){ console.log('CRASH',e.message.split('\n').slice(0,4).join(' | ')); bad++; }
  console.log(bad?'FAILURES: '+bad:'ALL OK'); await b.close();
})();
