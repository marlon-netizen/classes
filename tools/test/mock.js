// Test double for Supabase: translates REST calls into the real SQL in supabase/schema.sql (local Postgres).
const http=require('http'), {spawnSync}=require('child_process'), url=require('url');
const D=(process.env.LIA_PGDIR||'/tmp/lia-pg');
function psql(sql,role){
  const env=Object.assign({},process.env,role?{PGOPTIONS:'-c role='+role}:{});
  const r=spawnSync('psql',['-h',D,'-p','54329','-U','postgres','-At','-q','-v','ON_ERROR_STOP=1'],{input:sql,env,encoding:'utf8'});
  return {out:(r.stdout||'').trim(),err:(r.stderr||'').trim(),code:r.status};
}
const q=s=>'$q$'+s+'$q$';
function send(res,code,body,extra){ res.writeHead(code,Object.assign({'Content-Type':'application/json','Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'apikey,authorization,content-type,prefer','Access-Control-Allow-Methods':'GET,POST,PATCH,DELETE,OPTIONS'},extra||{})); res.end(typeof body==='string'?body:JSON.stringify(body)); }
http.createServer((req,res)=>{
  if(req.method==='OPTIONS') return send(res,204,'');
  let body=''; req.on('data',c=>body+=c); req.on('end',()=>{
    const u=url.parse(req.url,true), p=u.pathname;
    const ip=req.headers['x-test-ip']||'9.9.9.9';
    try{
      if(p.startsWith('/rest/v1/rpc/')){
        const fn=p.split('/').pop(), a=JSON.parse(body||'{}');
        if(!(req.headers.apikey)) return send(res,401,{message:'No API key'});
        let call;
        if(fn==='lia_login') call=`select public.lia_login(${q(a.p_area)},${q(a.p_code)})`;
        else if(fn==='lia_get_progress') call=`select public.lia_get_progress(${q(a.p_area)},${q(a.p_code)},${q(a.p_page)})`;
        else if(fn==='lia_save_progress') call=`select public.lia_save_progress(${q(a.p_area)},${q(a.p_code)},${q(a.p_page)},${q(JSON.stringify(a.p_state))}::jsonb,${+a.p_solved||0},${+a.p_total||0},${+a.p_examples||0},${+a.p_score||0},${+a.p_max_score||0})`;
        else return send(res,404,{message:'no function'});
        const r=psql(`\\o /dev/null\nselect set_config('request.headers',${q(JSON.stringify({'x-forwarded-for':ip}))},false);\n\\o\n${call};`,'anon');
        if(r.code) return send(res,400,{message:r.err});
        return send(res,200,r.out);
      }
      if(p==='/auth/v1/token'){ const a=JSON.parse(body||'{}'); if(u.query.grant_type==='password'&&(a.email!=='t@x.org'||a.password!=='secret')) return send(res,400,{error_description:'Invalid login credentials'}); return send(res,200,{access_token:'tok-'+Date.now(),refresh_token:'ref',expires_in:3600,user:{email:'t@x.org'}}); }
      if(!/^Bearer tok-/.test(req.headers.authorization||'')) return send(res,401,{message:'JWT required'});
      const m=p.match(/^\/rest\/v1\/(\w+)$/); if(!m) return send(res,404,{});
      const t=m[1], f=Object.entries(u.query).filter(([k,v])=>/^eq\./.test(v)).map(([k,v])=>`${k}='${v.slice(3).replace(/'/g,"''")}'`).join(' and ');
      let sql;
      if(t==='admins') return send(res,200,[{user_id:'1'}]);
      if(req.method==='GET') sql=`select coalesce(json_agg(x ${t==='students'?'order by x.full_name':''}),'[]') from public.${t} x ${f?'where '+f:''}`;
      else if(req.method==='POST'&&t==='students'){ let b=JSON.parse(body); if(!Array.isArray(b)) b=[b]; sql=`with i as (insert into public.students(id,area,code,full_name,grade,class_name,email,notes,active) select id,area,code,full_name,grade,class_name,email,notes,coalesce(active,true) from json_populate_recordset(null::public.students,${q(JSON.stringify(b.map(r=>Object.assign({id:require('crypto').randomUUID()},r))))}) returning *) select json_agg(i) from i`; }
      else if(req.method==='PATCH'&&t==='students'){ sql=`with r as (select * from json_populate_record(null::public.students,${q(body)})) update public.students s set full_name=r.full_name,grade=r.grade,class_name=r.class_name,email=r.email,notes=r.notes,code=r.code,active=r.active from r where s.${f}`; }
      else if(req.method==='POST'&&t==='lesson_access'){ let b=JSON.parse(body); if(!Array.isArray(b)) b=[b]; sql=b.map(r=>`insert into public.lesson_access(area,page_key,grade,class_name) values (${q(r.area)},${q(r.page_key)},${q(r.grade)},${q(r.class_name)}) on conflict do nothing`).join(';\n'); }
      else if(req.method==='DELETE') sql=`delete from public.${t} where ${f}`;
      else return send(res,405,{});
      const r=psql(sql,null);
      if(r.code){ const dup=/duplicate key/.test(r.err); return send(res,dup?409:400,{code:dup?'23505':'x',message:r.err.split('\n')[0]}); }
      return send(res,req.method==='GET'?200:(r.out?201:204),req.method==='GET'||r.out?(r.out||'[]'):'');
    }catch(e){ send(res,500,{message:String(e)}); }
  });
}).listen(54400,()=>console.log('mock up'));
