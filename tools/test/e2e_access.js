const { chromium } = require('playwright');
const {execSync}=require('child_process');
const P=(process.env.LIA_PGDIR||'/tmp/lia-pg');
const sql=q=>execSync(`psql -h ${P} -p 54329 -U postgres -At -c "${q.replace(/"/g,'\\"')}"`,{encoding:'utf8'}).trim();
const ok=(c,m)=>console.log((c?'PASS':'FAIL')+' '+m);
const R=''+(process.env.LIA_SITE||'file:///home/user/classes/')+'';
async function fetchMock(r,u){ const q=r.request(); const h=q.headers(); const res=await fetch('http://localhost:54400'+u.pathname+u.search,{method:q.method(),headers:h,body:['GET','HEAD','OPTIONS'].includes(q.method())?undefined:q.postData()}); const hd={}; res.headers.forEach((v,k)=>hd[k]=v); r.fulfill({status:res.status,headers:hd,body:Buffer.from(await res.arrayBuffer())}); }
async function newCtx(b){ const c=await b.newContext({viewport:{width:1300,height:900}}); await c.route('https://plctzbzncedwhmwumaaf.supabase.co/**',r=>{ const u=new URL(r.request().url()); fetchMock(r,u); }); await c.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort()); return c; }
(async()=>{
  sql("delete from public.lesson_access; delete from public.progress; delete from public.students");
  sql("insert into public.students(area,code,full_name,grade,class_name) values ('math-physics','AAAA1111','Ana','11','Physics I'),('math-physics','BBBB2222','Ben','12','Physics II'),('math-physics','CCCC3333','Cy','12','Physics II / Pre-Calculus')");
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}); const errs=[];
  // ---- teacher assigns
  let ctx=await newCtx(b); let pg=await ctx.newPage(); pg.on('pageerror',e=>errs.push('t:'+e.message));
  await pg.goto(R+'teacher/access.html?area=math-physics'); await pg.fill('#lEmail','t@x.org'); await pg.fill('#lPass','secret'); await pg.click('#lBtn'); await pg.waitForSelector('#mx tbody tr');
  ok((await pg.$$('#mx tbody tr')).length===3,'matrix: 3 grade/class rows (Cy listed in both)');
  ok((await pg.$$('#mx tbody input:checked')).length===27,'everything shown to everyone at first');
  const colIdx=async key=>pg.evaluate(k=>[...document.querySelectorAll('#mx tbody tr:nth-child(1) input')].findIndex(i=>i.dataset.p===k),key);
  const set=async(row,key,on)=>{ const sel=`#mx tbody tr:nth-child(${row}) input[data-p="${key}"]`; await pg.locator(sel).setChecked(on); await pg.waitForTimeout(700); };
  // order of rows: by class: Physics I, Physics II, Pre-Calculus
  const labels=await pg.$$eval('#mx tbody tr td:first-child b',e=>e.map(x=>x.textContent)); console.log(labels);
  await set(1,'physics-lesson-2-3',false);   // untick Physics I (row 1)
  console.log(sql("select page_key||'|'||grade||'|'||class_name from public.lesson_access order by 1"));
  ok(await pg.$eval('#mx tbody tr:nth-child(1) input[data-p="physics-lesson-2-3"]',i=>!i.checked)&&await pg.$eval('#mx tbody tr:nth-child(2) input[data-p="physics-lesson-2-3"]',i=>i.checked),'unticking one class keeps the others');
  // restrict a second page to Physics II only
  await set(1,'physics-lesson-10-3',false); await set(3,'physics-lesson-10-3',false);
  ok(+sql("select count(*) from public.lesson_access where page_key='physics-lesson-10-3' and grade<>'~'")===1,'10-3 now only for Physics II');
  // re-show to everyone
  await pg.click('[data-all="physics-lesson-10-3"]'); await pg.waitForTimeout(700);
  ok(+sql("select count(*) from public.lesson_access where page_key='physics-lesson-10-3'")===0,'"show to everyone" removes restriction');
  // none then all on a row
  await pg.click('#mx tbody tr:nth-child(3) [data-row="0"]'); await pg.waitForTimeout(3000);
  ok(await pg.$$eval('#mx tbody tr:nth-child(3) input:checked',e=>e.length)===0,'row "none" clears the row');
  await pg.click('#mx tbody tr:nth-child(3) [data-row="1"]'); await pg.waitForTimeout(3000);
  ok(await pg.$$eval('#mx tbody tr:nth-child(3) input:checked',e=>e.length)===9,'row "all" restores the row');
  // final state for students: 2-3 only Physics II + Pre-Calculus, not Physics I
  console.log(sql("select page_key,grade,class_name from public.lesson_access order by 1,2,3").split('\n').length,'rows');
  await ctx.close();
  // ---- students
  async function student(code){ const c=await newCtx(b); const p=await c.newPage(); p.on('pageerror',e=>errs.push('s:'+e.message)); await p.goto(R+'math-physics/index.html'); await p.waitForSelector('#liaGate'); await p.fill('#liaCode',code); await p.click('#liaGate .lia-btn'); await p.waitForSelector('#liaUser .lia-name'); await p.waitForTimeout(800); return {c,p}; }
  let s=await student('AAAA1111'); 
  const vis=await s.p.$$eval('a.card',a=>a.filter(x=>x.style.display!=='none').map(x=>x.getAttribute('href')));
  ok(vis.length===8&&!vis.includes('physics-lesson-2-3.html'),'Physics I student: menu hides 2.3 (shows '+vis.length+')');
  await s.p.goto(R+'math-physics/physics-lesson-2-3.html'); await s.p.waitForTimeout(1500);
  ok(await s.p.evaluate(()=>/Not available/.test(document.getElementById('liaGate')?.textContent||'')),'Physics I student: 2.3 page blocked');
  await s.p.screenshot({path:'blocked.png'});
  ok(sql("select count(*) from public.progress")==='0','blocked page saved nothing');
  await s.p.goto(R+'math-physics/complex-numbers.html'); await s.p.waitForSelector('#liaUser .lia-name'); ok(!(await s.p.$('#liaGate')),'allowed page opens');
  await s.c.close();
  s=await student('BBBB2222');
  const v2=await s.p.$$eval('a.card',a=>a.filter(x=>x.style.display!=='none').length); ok(v2===9,'Physics II student: sees all 9');
  await s.p.goto(R+'math-physics/physics-lesson-2-3.html'); await s.p.waitForSelector('#liaUser .lia-name'); ok(!(await s.p.$('#liaGate')),'Physics II student: 2.3 opens');
  await s.c.close();
  console.log('server guard:', sql("select public.lia_get_progress('math-physics','AAAA1111','physics-lesson-2-3')"));
  console.log('errors',errs);
  await b.close();
})();
