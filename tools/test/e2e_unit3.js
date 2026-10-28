const { chromium } = require('playwright');
const {execSync}=require('child_process');
const P=(process.env.LIA_PGDIR||'/tmp/lia-pg');
const sql=q=>execSync(`psql -h ${P} -p 54329 -U postgres -At -c "${q.replace(/"/g,'\\"')}"`,{encoding:'utf8'}).trim();
const ok=(c,m)=>console.log((c?'PASS':'FAIL')+' '+m);
async function fetchMock(r,u){ const q=r.request(); const res=await fetch('http://localhost:54400'+u.pathname+u.search,{method:q.method(),headers:q.headers(),body:['GET','HEAD','OPTIONS'].includes(q.method())?undefined:q.postData()}); const hd={}; res.headers.forEach((v,k)=>hd[k]=v); r.fulfill({status:res.status,headers:hd,body:Buffer.from(await res.arrayBuffer())}); }
async function ctx(b){ const c=await b.newContext({viewport:{width:1200,height:900}}); await c.route('https://plctzbzncedwhmwumaaf.supabase.co/**',r=>fetchMock(r,new URL(r.request().url()))); await c.route(/fonts|cdnjs/,r=>r.abort()); return c; }
(async()=>{ const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}); const c=await ctx(b); const p=await c.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 await p.goto(''+(process.env.LIA_SITE||'file:///home/user/classes/')+'ciencias-sociales/social-science-11-unit-3.html#l1'); await p.waitForSelector('#liaGate'); await p.fill('#liaCode','SOCIAL11'); await p.click('#liaGate .lia-btn'); await p.waitForSelector('#liaUser .lia-name'); await p.waitForTimeout(800);
 await p.evaluate(()=>{ location.hash='#l1'; }); await p.click('#mainNav button[data-t=l1]'); await p.click('#p-l1 .subnav button[data-s=practice]').catch(()=>{});
 await p.waitForSelector('#p-l1 .practiceRoot .quiz .q',{state:'visible',timeout:5000});
 ok((await p.$$('.submitBtn')).length===0&&!(await p.$('#scoreModal')),'no Submit button, no score pop-up');
 // answer all questions of the first 3 activity types (mcq, tf, cloze)
 for(const mode of ['mcq','tf','cloze','voc','src']){
   await p.click(`#p-l1 .practiceRoot .ptab[data-p=${mode}]`); await p.waitForTimeout(150);
   const n=await p.$$eval('#p-l1 .practiceRoot .quiz .q',e=>e.length);
   for(let i=0;i<n;i++){ const opts=await p.$$('#p-l1 .practiceRoot .quiz .q:nth-child('+(i+1)+') .opt'); if(opts.length){ await opts[0].click(); } }
 }
 // match
 await p.click('#p-l1 .practiceRoot .ptab[data-p=match]'); await p.waitForTimeout(150);
 const sels=await p.$$('#p-l1 .practiceRoot .quiz .q:nth-child(1) select'); for(const s of sels){ await s.selectOption({index:1}); } await p.click('#p-l1 .practiceRoot .quiz .q:nth-child(1) .btn');
 // written
 await p.click('#p-l1 .practiceRoot .ptab[data-p=wr]'); await p.waitForTimeout(150);
 await p.fill('#p-l1 .practiceRoot .quiz .q:nth-child(1) textarea','Both movements defended liberty and popular sovereignty, and criollos in America fought Spanish rule; Bolivar wanted unity and freedom for the whole region.'); await p.waitForTimeout(900);
 const mid=await p.evaluate(()=>{ const o=JSON.parse(localStorage.getItem('resp-u3-l1-10-wr')); return o; }); ok(mid&&mid.a[0]&&/not checked yet/.test(mid.a[0]),'written text saved while typing: '+(mid&&mid.a[0].slice(0,70)));
 await p.click('#p-l1 .practiceRoot .quiz .q:nth-child(1) .btn'); await p.waitForTimeout(300);
 const keys=await p.evaluate(()=>Object.keys(localStorage).filter(k=>k.startsWith('resp-u3')).sort()); console.log('resp keys:',keys.join(', '));
 ok(keys.length>=7,'responses saved for each activity');
 const mc=await p.evaluate(()=>JSON.parse(localStorage.getItem('resp-u3-l1-01-mcq'))); ok(mc.q.length>=1&&/✔|✘/.test(mc.a[0]),'MCQ answer text: '+mc.a[0]);
 await p.waitForTimeout(1800);
 const st=JSON.parse(sql("select p.state::text from public.progress p join public.students s on s.id=p.student_id where s.code='SOCIAL11'")); ok(Object.keys(st).filter(k=>k.startsWith('resp-u3')).length>=7,'responses mirrored to the database');
 // reload keeps the written text
 await p.reload(); await p.waitForSelector('#liaUser .lia-name'); await p.click('#mainNav button[data-t=l1]'); await p.click('#p-l1 .subnav button[data-s=practice]'); await p.click('#p-l1 .practiceRoot .ptab[data-p=wr]').catch(()=>{}); await p.waitForTimeout(300);
 const txts=await p.$$eval('#p-l1 .practiceRoot .quiz textarea',e=>e.map(x=>x.value)); ok(txts.some(x=>/liberty/.test(x)),'written text restored after reload ('+txts.map(x=>x.length).join(',')+' chars)');
 // teacher page
 const tc=await ctx(b), t=await tc.newPage(); await t.goto(''+(process.env.LIA_SITE||'file:///home/user/classes/')+'teacher/responses.html?area=ciencias-sociales'); await t.fill('#lEmail','t@x.org'); await t.fill('#lPass','secret'); await t.click('#lBtn'); await t.waitForSelector('#list .sc',{timeout:8000});
 const body=await t.$eval('#list',e=>e.textContent); ok(/Carlos Mora/.test(body)&&/Unit III/.test(body),'teacher "Student responses" shows the student and Unit III sets'); ok(/liberty and popular sovereignty/.test(body),'the written answer is visible to the teacher');
 await t.screenshot({path:'/tmp/u3_resp.png'});
 console.log('errors',errs); await b.close(); })();
