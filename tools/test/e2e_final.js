const { chromium } = require('playwright');
const {execSync}=require('child_process');
const P=(process.env.LIA_PGDIR||'/tmp/lia-pg');
const sql=q=>execSync(`psql -h ${P} -p 54329 -U postgres -At -c "${q.replace(/"/g,'\\"')}"`,{encoding:'utf8'}).trim();
const ok=(c,m)=>console.log((c?'PASS':'FAIL')+' '+m);
const R=''+(process.env.LIA_SITE||'file:///home/user/classes/')+'';
async function fetchMock(r,u){ const q=r.request(); const res=await fetch('http://localhost:54400'+u.pathname+u.search,{method:q.method(),headers:q.headers(),body:['GET','HEAD','OPTIONS'].includes(q.method())?undefined:q.postData()}); const hd={}; res.headers.forEach((v,k)=>hd[k]=v); r.fulfill({status:res.status,headers:hd,body:Buffer.from(await res.arrayBuffer())}); }
async function newCtx(b){ const c=await b.newContext({viewport:{width:1300,height:900}}); await c.route('https://plctzbzncedwhmwumaaf.supabase.co/**',r=>fetchMock(r,new URL(r.request().url()))); await c.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort()); return c; }
(async()=>{
  sql("delete from public.lesson_access; delete from public.progress; delete from public.students");
  sql("insert into public.students(area,code,full_name,grade,class_name) values ('physics','AAAA1111','Ana','11','Physics I')");
  sql("insert into public.students(area,code,full_name,grade,class_name,is_preview) values ('physics','PREVIEW99','Teacher preview','','',true),('faith-formation','PREVIEW99','Teacher preview','','',true)");
  sql("insert into public.lesson_access values ('physics','physics2-lesson-11-2','12','Physics II')");
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}); const errs=[];
  let ctx=await newCtx(b), pg=await ctx.newPage(); pg.on('pageerror',e=>errs.push(e.message));
  await pg.goto(R+'index.html'); await pg.waitForTimeout(500);
  ok(await pg.$eval('#home',e=>e.hidden)&&!await pg.$eval('#gate',e=>e.hidden),'root: only the sign-in is visible');
  await pg.fill('#lEmail','t@x.org'); await pg.fill('#lPass','bad'); await pg.click('#lBtn'); await pg.waitForTimeout(800);
  ok(await pg.$eval('#home',e=>e.hidden),'wrong password stays gated');
  await pg.fill('#lPass','secret'); await pg.click('#lBtn'); await pg.waitForSelector('#home:not([hidden])');
  const links=await pg.$$eval('a.lk',a=>a.map(x=>x.textContent)); ok(links.length===18&&links.every(l=>/^file:\/\/\/home\/user\/classes\/(math|physics|ciencias-sociales|faith-formation)\//.test(l)),'home: 18 full links built from the site address');
  await pg.reload(); await pg.waitForSelector('#home:not([hidden])'); ok(true,'session remembered on reload');
  await pg.screenshot({path:'home_light.png'});
  await pg.emulateMedia({colorScheme:'dark'}); await pg.screenshot({path:'home_dark.png'});
  await pg.goto(R+'teacher/index.html'); await pg.waitForTimeout(500); ok(/index\.html$/.test(pg.url())&&!/teacher/.test(pg.url()),'teacher/index.html redirects to the root');
  ok(!require('fs').existsSync('/home/user/classes/physics/index.html'),'no student menu pages exist');
  // preview code
  const c2=await newCtx(b), p=await c2.newPage(); p.on('pageerror',e=>errs.push(e.message));
  await p.goto(R+'physics/physics2-lesson-11-2.html'); await p.waitForSelector('#liaGate'); await p.fill('#liaCode','PREVIEW99'); await p.click('#liaGate .lia-btn'); await p.waitForSelector('#liaUser .lia-name'); await p.waitForTimeout(800);
  ok(!(await p.$('#liaGate')),'preview code opens a lesson restricted to Physics II');
  ok(!(await p.$('.lia-menu')),'no Menu link');
  const c3=await newCtx(b), q=await c3.newPage(); await q.goto(R+'physics/physics2-lesson-11-2.html'); await q.waitForSelector('#liaGate'); await q.fill('#liaCode','AAAA1111'); await q.click('#liaGate .lia-btn'); await q.waitForTimeout(1500);
  ok(await q.evaluate(()=>/Not available/.test(document.getElementById('liaGate')?.textContent||'')),'real student still blocked');
  // preview hidden from dashboard
  await p.evaluate(()=>localStorage.setItem('x-test','1')); await p.waitForTimeout(1500);
  const d=await newCtx(b), t=await d.newPage(); await t.goto(R+'teacher/scores.html?area=physics'); await t.fill('#lEmail','t@x.org'); await t.fill('#lPass','secret'); await t.click('#lBtn'); await t.waitForSelector('#grid tbody tr');
  const names=await t.$$eval('#grid tbody td.name b',e=>e.map(x=>x.textContent)); ok(names.length===1&&names[0]==='Ana','dashboard excludes the preview account: '+names);
  console.log('errors',errs); await b.close();
})();
