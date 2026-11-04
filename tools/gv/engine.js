(function(){
"use strict";
const G = window.GV;
const $ = (s, r=document) => r.querySelector(s);
const $$ = (s, r=document) => Array.from(r.querySelectorAll(s));
function h(tag, attrs, ...kids){
  const el = document.createElement(tag);
  for(const k in (attrs||{})){
    if(k==='class') el.className = attrs[k];
    else if(k==='html') el.innerHTML = attrs[k];
    else if(k.startsWith('on')) el.addEventListener(k.slice(2), attrs[k]);
    else el.setAttribute(k, attrs[k]);
  }
  kids.flat(Infinity).forEach(c => { if(c!=null) el.append(c.nodeType ? c : document.createTextNode(c)); });
  return el;
}
const SLUG = G.slug;
const store = {
  get(k,d){ try{ const v=localStorage.getItem(k); return v==null?d:JSON.parse(v); }catch(e){ return d; } },
  set(k,v){ try{ localStorage.setItem(k, JSON.stringify(v)); }catch(e){} }
};
const plain = s => String(s).replace(/<[^>]*>/g,'').replace(/&nbsp;/g,' ').replace(/\s+/g,' ').trim();
const studentName = () => (window.LiaSync && LiaSync.name && LiaSync.name()) || '';

/* ---------- saved answers + stable (seeded) answer order ----------
   Every tap/choice is recorded and replayed on the next visit (localStorage, mirrored to the database by LiaSync).
   Shuffles are seeded, so the order is the same on every visit; the correct option is spread over all positions.
   "Try again" starts a new round (new order, that activity's saved answers cleared). */
const AKEY = 'gv-ans-' + SLUG;
let AD = store.get(AKEY, {}) || {};
const asave = () => store.set(AKEY, AD);
let curAct = null, shufN = 0, CNT = {}, replaying = false; const STARTED = {};
function rng(seed){ let a = seed>>>0; return () => { a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a>>>15), 1 | a); t = (t + Math.imul(t ^ (t>>>7), 61 | t)) ^ t; return ((t ^ (t>>>14))>>>0) / 4294967296; }; }
function strSeed(s){ let x = 2166136261; for(let i=0;i<s.length;i++){ x ^= s.charCodeAt(i); x = Math.imul(x, 16777619); } return x>>>0; }
function actRnd(){ shufN++; return rng(strSeed(curAct + '|' + ((AD[curAct] && AD[curAct].round) || 0) + '|' + shufN)); }
function beginAct(id){ if(STARTED[id]){ AD[id] = {round: ((AD[id] && AD[id].round) || 0) + 1, a: []}; asave(); } STARTED[id] = 1; curAct = id; shufN = 0; CNT = {}; }
function armAct(id, mount){
  curAct = null;
  const d = AD[id] = AD[id] || {round: 0, a: []};
  const cs = $$('button.opt, button.btn:not(.ghost), select, input[type=checkbox]', mount);
  cs.forEach((c, i) => c.addEventListener(c.tagName === 'SELECT' ? 'change' : 'click', () => {
    if(replaying) return;
    if(d.a.length < 600){ d.a.push(c.tagName === 'SELECT' ? {i, v: c.value} : {i}); asave(); }
  }));
  if(d.a.length){
    replaying = true;
    d.a.forEach(x => { const c = cs[x.i]; if(!c) return; if(c.tagName === 'SELECT'){ c.value = x.v; c.dispatchEvent(new Event('change')); } else c.click(); });
    replaying = false;
  }
}
function placeOk(arr){
  const ok = arr.find(x => x.ok); if(!ok) return shuffle(arr);
  const n = arr.length, wr = shuffle(arr.filter(x => x !== ok)), k = (CNT[n] = (CNT[n] || 0) + 1) - 1, target = ((k % n) * (n === 4 ? 3 : 2) + Math.floor(k / n)) % n;
  wr.splice(target, 0, ok); return wr;
}
function shuffle(a){ a=a.slice(); const rnd=curAct?actRnd():Math.random; for(let i=a.length-1;i>0;i--){const j=Math.floor(rnd()*(i+1));[a[i],a[j]]=[a[j],a[i]];} return a; }
function feedback(el, kind, text){ el.className = 'fb show ' + kind; el.textContent = text; }

/* ---------- theme (own toggle: wired here) ---------- */
(function(){
  const root = document.documentElement;
  try{ const t = localStorage.getItem('lia-theme'); if(t==='light'||t==='dark') root.dataset.theme = t; }catch(e){}
  $('#themeBtn').addEventListener('click', () => {
    const dark = root.dataset.theme==='dark' || (!root.dataset.theme && matchMedia('(prefers-color-scheme: dark)').matches);
    root.dataset.theme = dark ? 'light' : 'dark';
    try{ localStorage.setItem('lia-theme', root.dataset.theme); }catch(e){}
  });
})();

/* ---------- progress & scores ---------- */
const ACTS = G.acts.map(a => [a.id, a.title]);
const TOTAL = ACTS.length;
const SKEY = 'gv-scores-' + SLUG;
const scores = store.get(SKEY, {}) || {};
function reportProgress(){   // tells the teacher dashboard how far this student is
  try{ let c=0,t=0,n=0; ACTS.forEach(a=>{ const s=scores[a[0]]; if(s){ n++; c+=s[0]; t+=s[1]; } });
    if(window.LiaSync && LiaSync.report) LiaSync.report({solved:n,total:TOTAL,score:c,max:t}); }catch(e){}
}
function paintProgress(){
  reportProgress();
  const n = ACTS.filter(a => scores[a[0]]).length;
  $('#progText').textContent = n + ' of ' + TOTAL + ' activities';
  $('#progBar').style.width = (n/TOTAL*100) + '%';
  $$('.act').forEach(a => a.classList.toggle('done', !!scores[a.id]));
  $('#summaryCta').style.display = n===TOTAL ? '' : 'none';
}
function record(id, correct, total){
  const was = ACTS.filter(a => scores[a[0]]).length;
  scores[id] = [correct, total];
  store.set(SKEY, scores);
  paintProgress();
  if(was===TOTAL-1 && ACTS.every(a => scores[a[0]])) setTimeout(openSummary, 900);
}
function unrecord(id){ if(scores[id]){ delete scores[id]; store.set(SKEY, scores); paintProgress(); } }
function openSummary(){
  let c=0,t=0;
  const rows = ACTS.map(([id,name]) => { const [a,b]=scores[id]||[0,0]; c+=a; t+=b;
    return h('tr',{}, h('td',{},name), h('td',{}, b ? a+' / '+b : (scores[id] ? 'Completed ✓' : '—')), h('td',{}, h('div',{class:'meter'}, h('i',{style:'width:'+(b?a/b*100:(scores[id]?100:0))+'%'})))); });
  const pct = t ? Math.round(c/t*100) : 0;
  $('#sumBig').innerHTML = pct + '% <small>(' + c + ' of ' + t + ' points on the scored activities)</small>';
  $('#sumMsg').textContent = pct>=90 ? 'Outstanding! You can explain this week\'s topic and put it into practice.'
    : pct>=80 ? 'Secure! You have a solid understanding. Review the activities with lower scores to make it even stronger.'
    : pct>=60 ? 'Good progress. Go back to the Worked Examples, then retry the activities with lower scores.'
    : 'Keep going! Re-read the key ideas and the Worked Examples, then try the activities again.';
  const tbl = $('#sumTable'); tbl.innerHTML='';
  tbl.append(h('tr',{},h('th',{},'Activity'),h('th',{},'Result'),h('th',{},'')), ...rows);
  $('#overlay').hidden = false; $('#closeSummary').focus();
}
function closeSummary(){ $('#overlay').hidden = true; }
$('#openSummary').addEventListener('click', openSummary);
$('#closeSummary').addEventListener('click', closeSummary);
$('#reviewBtn').addEventListener('click', () => { closeSummary(); $('#practice').scrollIntoView(); });
document.addEventListener('keydown', e => { if(e.key==='Escape') closeSummary(); });

/* ---------- key ideas (tabs) ---------- */
(function(){
  const tabs = $('#stageTabs'), panel = $('#stagePanel'); if(!tabs) return;
  function show(i){
    $$('.tab', tabs).forEach((b,j) => b.setAttribute('aria-selected', j===i));
    const s = G.ideas[i];
    panel.innerHTML = '';
    panel.append(h('h3', {}, s.title), s.ref ? h('p', {class:'ref'}, s.ref) : null, h('ul', {}, s.pts.map(p => h('li', {html:p}))), h('div', {class:'callout'}, h('strong', {}, 'Key idea: '), s.key));
  }
  G.ideas.forEach((s,i) => tabs.append(h('button', {class:'tab', role:'tab', type:'button', 'aria-selected':'false', onclick:()=>show(i)}, s.tab)));
  show(0);
})();

/* ---------- vocabulary cards ---------- */
G.vocab.forEach(([t,d]) => {
  const b = h('button', {class:'flip', type:'button', 'aria-pressed':'false'}, h('div', {class:'front'}, t), h('div', {class:'hint'}, 'Tap to see the meaning'), h('div', {class:'back'}, d));
  b.addEventListener('click', () => { const on = b.classList.toggle('on'); b.setAttribute('aria-pressed', on); });
  $('#flips').append(b);
});

/* ---------- worked examples (steps shown are saved) ---------- */
const EKEY = 'gv-ex-' + SLUG, EX = store.get(EKEY, {}) || {};
G.examples.forEach((ex, ei) => {
  const list = h('ol', {class:'steps'});
  const items = ex.steps.map(([t,b,fin]) => { const li = h('li', {class:'step' + (fin?' final':'')}, h('b',{class:'t'}, t), h('span',{html:b})); list.append(li); return li; });
  let n = Math.min(+EX[ei]||0, items.length);
  const next = h('button', {class:'btn', type:'button'}, 'Show next step');
  const all = h('button', {class:'btn ghost', type:'button'}, 'Show all');
  const reset = h('button', {class:'btn ghost', type:'button'}, 'Hide steps');
  const status = h('span', {class:'ref', 'aria-live':'polite'}, '');
  function paint(){ items.forEach((li,i) => li.classList.toggle('show', i<n)); next.disabled = n>=items.length; status.textContent = n + ' of ' + items.length + ' steps shown'; EX[ei] = n; store.set(EKEY, EX); }
  next.addEventListener('click', () => { if(n<items.length) n++; paint(); items[n-1].scrollIntoView({block:'nearest', behavior:'smooth'}); });
  all.addEventListener('click', () => { n=items.length; paint(); });
  reset.addEventListener('click', () => { n=0; paint(); });
  paint();
  $('#exampleList').append(h('div', {class:'card'}, h('h3', {}, ex.title), h('div', {class:'problem', html:'<b>Situation:</b> ' + ex.problem}), h('div', {class:'row', style:'margin-top:12px'}, next, all, reset, status), list));
});

/* ---------- activity engines ---------- */
const mountOf = id => $('#'+id+' .mount');
function withRound(id, render0){ const mount = mountOf(id); function render(){ beginAct(id); render0(mount, render); armAct(id, mount); } render(); }
function againBtn(render){ const b = h('button',{class:'btn ghost',type:'button',style:'display:none'},'Try again'); b.addEventListener('click', render); return b; }

/* 1. multiple choice (optional picture per question) */
function mountQuiz(a){
  withRound(a.id, (mount, render) => {
    mount.innerHTML = '';
    let answered = 0, correct = 0;
    const summary = h('p', {class:'score', 'aria-live':'polite'});
    const again = againBtn(render);
    function paintSummary(){
      if(answered<a.qs.length){ summary.textContent = 'Answered ' + answered + ' of ' + a.qs.length; return; }
      summary.textContent = 'Score: ' + correct + ' / ' + a.qs.length + (correct===a.qs.length ? ' – perfect!' : correct/a.qs.length>=.8 ? ' – secure (80% or higher).' : ' – review the explanations and try again.');
      again.style.display = ''; record(a.id, correct, a.qs.length);
    }
    if(a.intro) mount.append(h('p', {html:a.intro}));
    a.qs.forEach((q,qi) => {
      const order = placeOk(q.o.map((t,i) => ({t, ok:i===q.a})));
      const fb = h('div', {class:'fb', 'aria-live':'polite'});
      const btns = order.map(o => {
        const b = h('button', {class:'opt', type:'button'}, o.t);
        b.addEventListener('click', () => {
          if(b.disabled) return;
          answered++; btns.forEach(x => x.disabled = true);
          if(o.ok){ correct++; b.classList.add('good'); feedback(fb,'good','✓ Correct. ' + q.e); }
          else { b.classList.add('bad','shake'); btns[order.findIndex(x=>x.ok)].classList.add('good'); feedback(fb,'bad','✗ Not quite. ' + q.e); }
          paintSummary();
        });
        return b;
      });
      mount.append(h('div', {class:'qblock'}, h('div', {class:'qhead'}, (qi+1) + '. ' + q.q), q.svg ? h('div',{class:'fig',html:q.svg}) : null, btns, fb));
    });
    mount.append(h('div', {class:'row', style:'margin-top:16px'}, summary, again));
    paintSummary();
  });
}

/* 2. select ALL that apply */
function mountMulti(a){
  withRound(a.id, (mount, render) => {
    mount.innerHTML = '';
    let answered = 0, correct = 0;
    const summary = h('p', {class:'score', 'aria-live':'polite'});
    const again = againBtn(render);
    function paintSummary(){
      if(answered<a.qs.length){ summary.textContent = 'Answered ' + answered + ' of ' + a.qs.length; return; }
      summary.textContent = 'Score: ' + correct + ' / ' + a.qs.length + ' (a question counts only when you pick every right choice and no wrong one).';
      again.style.display = ''; record(a.id, correct, a.qs.length);
    }
    if(a.intro) mount.append(h('p', {html:a.intro}));
    a.qs.forEach((q,qi) => {
      const order = shuffle(q.o.map((t,i) => ({t, ok:q.a.includes(i)})));
      const fb = h('div', {class:'fb', 'aria-live':'polite'});
      const boxes = order.map(o => { const cb = h('input', {type:'checkbox'}); return {cb, o, l:h('label', {class:'opt'}, cb, h('span', {}, o.t))}; });
      const check = h('button', {class:'btn', type:'button'}, 'Check my answer');
      check.addEventListener('click', () => {
        if(check.disabled) return;
        check.disabled = true; answered++;
        const ok = boxes.every(b => b.cb.checked === b.o.ok);
        boxes.forEach(b => { b.cb.disabled = true; if(b.o.ok) b.l.classList.add('good'); else if(b.cb.checked) b.l.classList.add('bad'); });
        if(ok){ correct++; feedback(fb,'good','✓ Yes, that is every right choice. ' + q.e); } else feedback(fb,'bad','✗ Not quite. The right choices are highlighted. ' + q.e);
        paintSummary();
      });
      mount.append(h('div', {class:'qblock'}, h('div', {class:'qhead'}, (qi+1) + '. ' + q.q + '  (select all that apply)'), boxes.map(b => b.l), h('div',{class:'row'}, check), fb));
    });
    mount.append(h('div', {class:'row', style:'margin-top:16px'}, summary, again));
    paintSummary();
  });
}

/* 3. scenarios: choose the best response (2 = best, 1 = partly, 0 = not helpful) */
function mountScenario(a){
  withRound(a.id, (mount, render) => {
    mount.innerHTML = '';
    let answered = 0, pts = 0;
    const summary = h('p', {class:'score', 'aria-live':'polite'});
    const again = againBtn(render);
    function paintSummary(){
      if(answered<a.steps.length){ summary.textContent = 'Answered ' + answered + ' of ' + a.steps.length; return; }
      summary.textContent = 'Points: ' + pts + ' / ' + (2*a.steps.length) + ' (best response = 2, partly helpful = 1, not helpful = 0).';
      again.style.display = ''; record(a.id, pts, 2*a.steps.length);
    }
    if(a.intro) mount.append(h('p', {html:a.intro}));
    a.steps.forEach((st,si) => {
      const order = placeOk(st.o.map(o => ({...o, ok:o.p===2})));
      const fb = h('div', {class:'fb', 'aria-live':'polite'});
      const btns = order.map(o => {
        const b = h('button', {class:'opt', type:'button'}, o.t);
        b.addEventListener('click', () => {
          if(b.disabled) return;
          answered++; pts += o.p; btns.forEach(x => x.disabled = true);
          b.classList.add(o.p===2 ? 'good' : o.p===1 ? 'sel' : 'bad');
          if(o.p<2) btns[order.findIndex(x=>x.ok)].classList.add('good');
          feedback(fb, o.p===2?'good':o.p===1?'info':'bad', (o.p===2?'✓ Best response. ':o.p===1?'◑ Partly helpful. ':'✗ Not helpful. ') + o.f + (o.p<2 ? ' Better: ' + order.find(x=>x.ok).t : ''));
          paintSummary();
        });
        return b;
      });
      mount.append(h('div', {class:'qblock'}, h('div', {class:'qhead'}, 'Situation ' + (si+1)), h('p',{html:st.s}), btns, fb));
    });
    mount.append(h('div', {class:'row', style:'margin-top:16px'}, summary, again));
    paintSummary();
  });
}

/* 4. put the steps in order */
function mountSeq(a){
  withRound(a.id, (mount, render) => {
    mount.innerHTML = '';
    const items = a.items; let next = 0, mistakes = 0;
    const slots = items.map((_,i) => h('div', {class:'slot' + (i===0?' next':'')}, h('small', {}, 'Step ' + (i+1)), h('span', {}, '?')));
    const fb = h('div', {class:'fb', 'aria-live':'polite'});
    let pool = shuffle(items.map((it,i) => ({...it, i})));
    while(items.length>1 && pool.every((p,k) => p.i===k)) pool = shuffle(pool);
    const poolEl = h('div', {class:'pool'});
    const again = againBtn(render);
    pool.forEach(p => {
      const b = h('button', {class:'opt', type:'button'}, p.t);
      b.addEventListener('click', () => {
        if(b.disabled) return;
        if(p.i===next){
          b.disabled = true; b.style.display='none';
          slots[next].classList.remove('next'); slots[next].classList.add('filled'); slots[next].lastChild.textContent = p.t;
          feedback(fb,'good','✓ Yes! ' + p.why); next++;
          if(next<items.length) slots[next].classList.add('next');
          else { feedback(fb,'good','🎉 Complete! ' + (mistakes===0 ? 'No mistakes.' : mistakes + ' mistake' + (mistakes>1?'s':'') + ' along the way.') + ' ' + p.why); again.style.display=''; record(a.id, Math.max(0, items.length-mistakes), items.length); }
        } else { mistakes++; b.classList.add('bad','shake'); setTimeout(()=>b.classList.remove('bad','shake'), 600); feedback(fb,'bad','Not yet. Hint for step ' + (next+1) + ': ' + items[next].hint); }
      });
      poolEl.append(b);
    });
    mount.append(h('p', {html:a.intro}), h('div', {class:'slots'}, slots), h('p', {class:'ref'}, 'Tap the step that belongs in the next empty box.'), poolEl, fb, h('div', {class:'row', style:'margin-top:10px'}, again));
  });
}

/* 5. match pairs */
function mountMatch(a){
  withRound(a.id, (mount, render) => {
    mount.innerHTML = '';
    const pairs = a.pairs; let sel=null, matched=0, mistakes=0;
    const fb = h('div',{class:'fb','aria-live':'polite'}); const again = againBtn(render);
    const L = pairs.map((p,i) => h('button',{class:'opt',type:'button','data-i':i},p[0]));
    const R = shuffle(pairs.map((p,i) => ({i,t:p[1]}))).map(p => h('button',{class:'opt',type:'button','data-i':p.i},p.t));
    L.forEach(b => b.addEventListener('click',()=>{ if(b.classList.contains('done')) return; L.forEach(x=>x.classList.remove('sel')); b.classList.add('sel'); sel=b; feedback(fb,'info','Now choose the matching item on the right.'); }));
    R.forEach(b => b.addEventListener('click',()=>{
      if(b.classList.contains('done')) return;
      if(!sel){ feedback(fb,'info','First tap an item on the left.'); return; }
      if(sel.dataset.i===b.dataset.i){
        sel.classList.remove('sel'); sel.classList.add('done'); b.classList.add('done'); sel=null; matched++; feedback(fb,'good','✓ Match!');
        if(matched===pairs.length){ feedback(fb,'good','🎉 All matched' + (mistakes? ' with ' + mistakes + ' miss' + (mistakes>1?'es':'') : ' with no misses') + '.'); again.style.display=''; record(a.id, Math.max(0, pairs.length-mistakes), pairs.length); }
      } else { mistakes++; b.classList.add('bad','shake'); setTimeout(()=>b.classList.remove('bad','shake'),600); feedback(fb,'bad','Not that one. Re-read and try another.'); }
    }));
    mount.append(h('p',{html:a.intro}),h('div',{class:'match'},h('div',{},L),h('div',{},R)),fb,h('div',{class:'row',style:'margin-top:10px'},again));
  });
}

/* 6. sort cards into categories (optional picture per card) */
function mountSort(a){
  withRound(a.id, (mount, render) => {
    mount.innerHTML = '';
    const deck = shuffle(a.cards); let i=0, right=0;
    const fb = h('div',{class:'fb','aria-live':'polite'}); const card = h('div',{class:'sortcard'});
    const btns = a.choices.map(c => h('button',{class:'btn',type:'button'},c.label));
    const count = h('p',{class:'ref'}); const again = againBtn(render);
    function paint(){
      if(i>=deck.length){ card.textContent='Finished!'; btns.forEach(b=>b.disabled=true); count.textContent=''; return; }
      card.innerHTML=''; if(deck[i][3]) card.append(h('div',{class:'fig',html:deck[i][3]})); card.append(h('span',{},deck[i][0])); count.textContent='Card ' + (i+1) + ' of ' + deck.length;
    }
    function pick(k){
      if(i>=deck.length) return;
      const c=deck[i], ok=c[1]===k; if(ok) right++;
      const msg=(ok?'✓ Correct. ':'✗ Not quite. ') + c[2]; i++;
      if(i>=deck.length){ paint(); feedback(fb, right===deck.length?'good':'info', msg + ' — Score: ' + right + ' / ' + deck.length + '.'); again.style.display=''; record(a.id, right, deck.length); }
      else { feedback(fb, ok?'good':'bad', msg); paint(); }
    }
    btns.forEach((b,j) => b.addEventListener('click',()=>pick(a.choices[j].k)));
    mount.append(h('p',{html:a.intro}),count,card,h('div',{class:'row'},btns),fb,h('div',{class:'row',style:'margin-top:10px'},again));
    paint();
  });
}

/* 7. fill in the blanks (drop-down) */
function mountCloze(a){
  withRound(a.id, (mount, render) => {
    mount.innerHTML = '';
    const S = a.items, ok=new Set(); let wrong=0;
    const fb = h('div',{class:'fb','aria-live':'polite'}); const again = againBtn(render); const box = h('div',{class:'cloze'});
    S.forEach((s,k) => {
      const sel = h('select',{'aria-label':'Choose the word for sentence ' + (k+1)}, h('option',{value:''},'— choose —'), s[1].map((o,j)=>h('option',{value:j},o)));
      sel.addEventListener('change',()=>{
        if(sel.value===''){ sel.className=''; return; }
        if(+sel.value===s[2]){ sel.className='good'; sel.disabled=true; ok.add(k); feedback(fb,'good','✓ ' + s[4]);
          if(ok.size===S.length){ feedback(fb,'good','🎉 All sentences complete!'); again.style.display=''; record(a.id, Math.max(0, S.length-wrong), S.length); } }
        else { wrong++; sel.className='bad shake'; setTimeout(()=>sel.classList.remove('shake'),600); feedback(fb,'bad','Not quite – try another word. Think about what you learned this week.'); }
      });
      box.append(h('p',{}, s[0], sel, s[3]));
    });
    mount.append(h('p',{html:a.intro}),box,fb,h('div',{class:'row',style:'margin-top:10px'},again));
  });
}

/* 8. written answers: saved word for word and listed on the teacher's "Student responses" page (resp- key) */
function mountOpen(a){
  const mount = mountOf(a.id), key = 'resp-' + SLUG + '-' + a.id, n = a.prompts.length, min = a.min || 12;
  const qs = a.prompts.map(p => plain(p.q));
  let R = store.get(key, null);
  if(!R || !Array.isArray(R.a)) R = {a:[]};
  R = {title: G.label + ' – ' + (a.rtitle || a.title), q: qs, a: qs.map((_,i) => String(R.a[i] || ''))};
  const status = h('span', {class:'saved'}, '');
  function check(){
    const done = R.a.every(t => t.trim().length >= min);
    status.textContent = done ? '✓ Saved. Your teacher can read your answers.' : 'Saved automatically as you type. Write at least a full sentence for each answer to complete this activity.';
    if(done) record(a.id, 0, 0); else unrecord(a.id);
  }
  if(a.intro) mount.append(h('p', {html:a.intro}));
  if(a.who){ const nm = studentName(); mount.append(h('p', {class:'who'}, 'Name: ', h('b', {}, nm || '(sign in to show your name)'), '  ·  Week: ' + G.label)); }
  a.prompts.forEach((p,i) => {
    const ta = h('textarea', {id:a.id+'-q'+i, rows:p.rows||4, 'aria-label':plain(p.q)});
    ta.value = R.a[i];
    ta.addEventListener('input', () => { R.a[i] = ta.value; store.set(key, R); check(); });
    ta.addEventListener('blur', () => { R.a[i] = ta.value; store.set(key, R); });
    mount.append(h('div', {class:'qa'}, h('label', {for:a.id+'-q'+i, html:p.q}), p.hint ? h('div',{class:'ref',style:'margin:0 0 4px'},p.hint) : null, ta));
  });
  if(a.model) mount.append(h('details', {class:'acc'}, h('summary', {}, 'See a model answer'), h('div', {class:'body', html:a.model})));
  mount.append(status);
  check();
}

/* 9. share a budget (percent) and explain the choice – saved as written answers */
function mountAlloc(a){
  const mount = mountOf(a.id), key = 'resp-' + SLUG + '-' + a.id, names = a.items.map(x => x.n);
  const qs = names.map(n => 'Share of the budget for: ' + n).concat([plain(a.reason)]);
  let R = store.get(key, null); if(!R || !Array.isArray(R.a)) R = {a:[]};
  R = {title: G.label + ' – ' + (a.rtitle || a.title), q: qs, a: qs.map((_,i) => String(R.a[i] == null ? '' : R.a[i]))};
  const total = a.total || 100, tot = h('span', {class:'pct'}), status = h('span', {class:'saved'}, '');
  const inputs = a.items.map((it,i) => { const inp = h('input', {class:'amt', type:'number', min:0, max:total, step:1, id:a.id+'-i'+i, 'aria-label':'Percent for ' + it.n});
    inp.value = R.a[i]; inp.addEventListener('input', () => { R.a[i] = inp.value; store.set(key, R); paint(); }); return inp; });
  const why = h('textarea', {id:a.id+'-why', rows:4, 'aria-label':plain(a.reason)}); why.value = R.a[names.length];
  why.addEventListener('input', () => { R.a[names.length] = why.value; store.set(key, R); paint(); });
  function paint(){
    const s = inputs.reduce((t,i) => t + (+i.value||0), 0);
    tot.textContent = 'Total: ' + s + '% of ' + total + '%'; tot.className = 'pct ' + (s===total ? 'ok' : 'no');
    const done = s===total && why.value.trim().length >= 15;
    status.textContent = done ? '✓ Saved. Your teacher can read your budget and your reasons.' : (s===total ? 'Now explain your biggest choice (at least a full sentence).' : (s>total ? 'You gave away more than ' + total + '%: lower some numbers.' : 'Share all ' + total + '% of the budget: ' + (total-s) + '% still to assign.'));
    if(done) record(a.id, 0, 0); else unrecord(a.id);
  }
  mount.append(h('p', {html:a.intro}), h('div', {class:'alloc'}, a.items.map((it,i) => [h('label', {for:a.id+'-i'+i, html:'<b>' + it.n + '</b><br><span class="ref">' + (it.hint||'') + '</span>'}), inputs[i]])), h('p', {}, tot),
    h('div', {class:'qa'}, h('label', {for:a.id+'-why', html:a.reason}), why), status);
  paint();
}

/* 10. numbers practice: every student gets their own set of numbers (seeded by the sign-in) */
function mountCalc(a){
  const mount = mountOf(a.id), skey = 'gv-calc-' + SLUG + '-' + a.id, rkey = 'resp-' + SLUG + '-' + a.id, gen = (window.GV_GENS||{})[a.gen];
  let S = store.get(skey, null); if(!S || !Array.isArray(S.t)) S = {seed:'', t:[], d:[]};
  const sd = (window.LiaSync && LiaSync.seed && LiaSync.seed()) || ''; if(!S.seed && sd) S.seed = sd;
  const n = a.n || 5, Q = [];
  for(let k=0;k<n;k++){ Q.push(gen(rng(strSeed((S.seed||'demo') + '|' + a.id + '|' + k)), k)); S.t[k] = S.t[k] || []; S.d[k] = S.d[k] || 0; }
  store.set(skey, S);
  function saveResp(){ store.set(rkey, {title: G.label + ' – ' + (a.rtitle||a.title), q: Q.map((q,k) => (k+1) + '. ' + plain(q.q)), a: Q.map((q,k) => S.t[k].length ? 'Tries: ' + S.t[k].join(' → ') + (S.d[k] ? ' (solved)' : '') : '') }); }
  let first = 0;
  const summary = h('p', {class:'score', 'aria-live':'polite'});
  function paint(){
    const solved = S.d.filter(Boolean).length; first = Q.filter((q,k) => S.d[k] && S.t[k].length===1).length;
    summary.textContent = solved < n ? 'Solved ' + solved + ' of ' + n : 'Done! Solved on the first try: ' + first + ' of ' + n + '.';
    if(solved === n) record(a.id, first, n);
  }
  mount.append(h('p', {html:a.intro}), h('p', {class:'ref'}, 'Your numbers are your own: classmates get different ones. Type a number, then press Check. Use a calculator if you like.'));
  Q.forEach((q,k) => {
    const fb = h('div', {class:'fb', 'aria-live':'polite'}), inp = h('input', {class:'num', type:'text', inputmode:'decimal', 'aria-label':'Answer to question ' + (k+1)}), btn = h('button', {class:'btn', type:'button'}, 'Check');
    function lock(good){ inp.disabled = true; btn.disabled = true; inp.classList.add(good ? 'good' : 'bad'); }
    function show(){ if(S.d[k]){ const last = S.t[k][S.t[k].length-1], v = parseFloat(String(last).replace(',', '.')), good = isFinite(v) && Math.abs(v - q.ans) <= (q.tol == null ? 0.01 : q.tol); inp.value = last; lock(good);
      if(good) feedback(fb,'good','✓ ' + q.e + ' Answer: ' + q.ans + (q.unit ? ' ' + q.unit : '') + '.'); else feedback(fb,'bad','The answer is ' + q.ans + (q.unit ? ' ' + q.unit : '') + '. ' + q.e); } }
    btn.addEventListener('click', () => {
      const raw = inp.value.trim(); if(!raw) return;
      const v = parseFloat(raw.replace(',', '.')); S.t[k].push(raw);
      if(isFinite(v) && Math.abs(v - q.ans) <= (q.tol == null ? 0.01 : q.tol)){ S.d[k] = 1; lock(true); feedback(fb,'good','✓ ' + q.e + ' Answer: ' + q.ans + (q.unit ? ' ' + q.unit : '') + '.'); }
      else if(S.t[k].length >= 3){ S.d[k] = 1; lock(false); feedback(fb,'bad','The answer is ' + q.ans + (q.unit ? ' ' + q.unit : '') + '. ' + q.e); }
      else { inp.classList.add('bad','shake'); setTimeout(()=>inp.classList.remove('bad','shake'),600); feedback(fb,'bad','Not yet. Hint: ' + q.hint); }
      store.set(skey, S); saveResp(); paint();
    });
    mount.append(h('div', {class:'qblock'}, h('div', {class:'qhead', html:(k+1) + '. ' + q.q}), h('div', {class:'row'}, inp, q.unit ? h('span',{class:'ref'},q.unit) : null, btn), fb));
    show();
  });
  mount.append(summary); saveResp(); paint();
}

const MOUNT = {quiz:mountQuiz, multi:mountMulti, scenario:mountScenario, seq:mountSeq, match:mountMatch, sort:mountSort, cloze:mountCloze, open:mountOpen, alloc:mountAlloc, calc:mountCalc};
G.acts.forEach(a => MOUNT[a.type](a));
paintProgress();
})();
