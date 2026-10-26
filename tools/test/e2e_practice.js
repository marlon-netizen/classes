const { chromium } = require('playwright');
const {execSync}=require('child_process');
const P=(process.env.LIA_PGDIR||'/tmp/lia-pg');
const sql=q=>execSync(`psql -h ${P} -p 54329 -U postgres -At -c "${q.replace(/"/g,'\\"')}"`,{encoding:'utf8'}).trim();
const ok=(c,m)=>console.log((c?'PASS':'FAIL')+' '+m);
async function fetchMock(r,u){ const q=r.request(); const res=await fetch('http://localhost:54400'+u.pathname+u.search,{method:q.method(),headers:q.headers(),body:['GET','HEAD','OPTIONS'].includes(q.method())?undefined:q.postData()}); const hd={}; res.headers.forEach((v,k)=>hd[k]=v); r.fulfill({status:res.status,headers:hd,body:Buffer.from(await res.arrayBuffer())}); }
async function newCtx(b,w=1100){ const c=await b.newContext({viewport:{width:w,height:900}}); await c.route('https://plctzbzncedwhmwumaaf.supabase.co/**',r=>fetchMock(r,new URL(r.request().url()))); await c.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort()); return c; }
const PAGE=''+(process.env.LIA_SITE||'file:///home/user/classes/')+'physics/physics1-lesson-2-3-practice.html';
async function login(b,code,w){ const c=await newCtx(b,w), p=await c.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message)); await p.goto(PAGE); await p.waitForSelector('#liaGate'); await p.fill('#liaCode',code); await p.click('#liaGate .lia-btn'); await p.waitForSelector('#liaUser .lia-name'); await p.waitForSelector('#problemList .prob',{timeout:8000}); await p.waitForTimeout(500); return {c,p,errs}; }
(async()=>{
  sql("delete from public.progress; delete from public.lesson_access; delete from public.students");
  sql("insert into public.students(area,code,full_name,grade,class_name) values ('physics','AAAA1111','Ana Pérez','10','Physics I'),('physics','BBBB2222','Ben Ruiz','10','Physics I')");
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const A=await login(b,'AAAA1111'), B=await login(b,'BBBB2222');
  const qa=await A.p.$$eval('.prob p',e=>e.map(x=>x.textContent)), qb=await B.p.$$eval('.prob p',e=>e.map(x=>x.textContent));
  ok(qa.length===25,'25 exercises'); ok((await A.p.$$('#problemList .acts .btn')).length===50&&!(await A.p.$$eval('#problemList .btn',e=>e.some(x=>/hint/i.test(x.textContent)))),'no Hint button (only Check and Solution)'); const diff=qa.filter((t,i)=>t!==qb[i]).length; ok(diff>=23,'two students: '+diff+' of 25 exercises have different numbers');
  // one wrong try then correct for exercise 1, everything else right
  const sols=await A.p.evaluate(()=>window.LIAPRACTICE.P.map(p=>p.parts.map(x=>String(+x.ans.toPrecision(4)))));
  await A.p.fill('#in_1_0','12'); await A.p.click('#ex1 .acts .btn'); await A.p.waitForTimeout(200);
  ok(await A.p.$eval('#ex1 .partrow .fb',e=>/Not quite|Right size|Close|Off/.test(e.textContent)||e.className.includes('no')),'wrong answer gets feedback');
  for(let i=0;i<25;i++){ for(let j=0;j<sols[i].length;j++) await A.p.fill(`#in_${i+1}_${j}`,sols[i][j]); await A.p.click(`#ex${i+1} .acts .btn`); }
  ok(await A.p.$$eval('.prob.done',e=>e.length)===25,'all 25 solved with the model answers');
  ok(await A.p.$eval('#overallText',e=>e.textContent)==='25 of 25 practice problems solved','overall text');
  await A.p.waitForTimeout(1800);
  console.log('DB:',sql("select page_key,solved,total,score,max_score from public.progress"));
  const st=JSON.parse(sql("select p.state::text from public.progress p join public.students s on s.id=p.student_id where s.code='AAAA1111' and p.page_key='physics1-lesson-2-3-practice'"));
  const resp=JSON.parse(st['resp-physics1-practice-2-3']);
  ok(resp.q.length===25&&resp.a.length===25&&/Try 1: 12/.test(resp.a[0])&&/Try 2/.test(resp.a[0]),'teacher "responses" entry saved with all tries: '+resp.a[0].slice(0,120));
  ok(typeof st['lia-physics1-practice-2-3']==='string'&&JSON.parse(st['lia-physics1-practice-2-3']).seed>0,'seed saved with the work');
  // second device, same student
  const A2=await login(b,'AAAA1111'); const qa2=await A2.p.$$eval('.prob p',e=>e.map(x=>x.textContent));
  ok(JSON.stringify(qa2)===JSON.stringify(qa),'same exercises on another device'); ok(await A2.p.$$eval('.prob.done',e=>e.length)===25,'solved state restored on another device');
  // generator sanity over many seeds
  const res=await A.p.evaluate(()=>{ const out={bad:[],n:0}; const stats={}; for(let s=1;s<=600;s++){ const set=window.LIAPRACTICE.makeSet(s*2654435761>>>0); set.forEach(p=>{ p.parts.forEach(x=>{ out.n++; if(!isFinite(x.ans)||Math.abs(x.ans)>1e5||Math.abs(x.ans)<1e-3) out.bad.push([p.n,x.ans]); const j=window.LIAPRACTICE.judge(x.ans,x); if(j.state!=='ok') out.bad.push([p.n,'judge',x.ans]); (stats[p.n]=stats[p.n]||[]).push(Math.abs(x.ans)); }); if(p.n===16&&!(p.parts[0].ans<0)) out.bad.push([16,'sign']); if(p.n===12&&!(p.parts[0].ans>0)) out.bad.push([12,'sign']); if(p.n===22&&p.parts[0].ans<30) out.bad.push([22,'net too low',p.parts[0].ans]); if([2,3,6,7,8,13,14,17,18,21,23,25].includes(p.n)&&p.parts[0].ans<=0) out.bad.push([p.n,'should be positive']); }); } out.range=Object.fromEntries(Object.entries(stats).map(([k,v])=>[k,[+Math.min(...v).toPrecision(3),+Math.max(...v).toPrecision(3)]])); return out; });
  ok(res.bad.length===0,'600 seeds × 25 exercises: all answers finite, sensible and accepted by the checker '+JSON.stringify(res.bad.slice(0,5)));
  console.log('answer ranges (min,max):',JSON.stringify(res.range));
  await A.p.screenshot({path:'pr_page.png'});
  const M=await login(b,'AAAA1111',390); ok(await M.p.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+2),'no horizontal scroll on phone');
  console.log('errors',A.errs,B.errs,A2.errs); await b.close();
})();
