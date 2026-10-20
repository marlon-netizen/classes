-- =====================================================================
--  Lincoln International Academy – student codes & progress (Supabase)
--  Run this whole file once in:  Supabase Dashboard → SQL Editor → New query
--  It is safe to run again (it uses "if not exists" / "or replace").
--
--  How it works
--  * The site has three areas (folders): faith-formation, ciencias-sociales,
--    math-physics. Every student row belongs to one "area"; a student's code
--    works on every page of that area and is unique inside the area.
--    Use ONE Supabase project for all areas, or one project per area – this
--    same script works for both (run it once in each project you use).
--  * Students never touch the tables directly. The public ("anon") key can
--    only call three functions: lia_login, lia_get_progress, lia_save_progress.
--    Each one needs the area and a valid, active student code.
--  * The teacher signs in to admin.html with a normal Supabase Auth account
--    that is listed in the "admins" table. Admins can read/write everything.
-- =====================================================================

-- ---------- tables ---------------------------------------------------
create table if not exists public.students (
  id          uuid primary key default gen_random_uuid(),
  area        text not null default 'default',   -- 'faith-formation' | 'ciencias-sociales' | 'math-physics'
  code        text not null,                 -- stored upper-case, letters+digits only
  full_name   text not null,
  grade       text,
  class_name  text,
  email       text,
  notes       text,
  active      boolean not null default true,
  created_at  timestamptz not null default now(),
  last_login  timestamptz
);
-- upgrading an older copy of this script: add the column, then swap the unique index
alter table public.students add column if not exists area text not null default 'default';
drop index if exists public.students_code_key;
create unique index if not exists students_area_code_key on public.students (area, code);

create table if not exists public.progress (
  student_id  uuid not null references public.students(id) on delete cascade,
  area        text not null default 'default',
  page_key    text not null,                 -- the page's file name, e.g. 'physics-lesson-2-3'
  state       jsonb not null default '{}'::jsonb,
  solved      integer not null default 0,    -- practice problems solved
  total       integer not null default 0,    -- practice problems in the page
  examples    integer not null default 0,    -- worked examples completed
  updated_at  timestamptz not null default now(),
  primary key (student_id, page_key)
);

alter table public.progress add column if not exists area text not null default 'default';
create index if not exists progress_area on public.progress (area);

create table if not exists public.admins (
  user_id     uuid primary key references auth.users(id) on delete cascade
);

create table if not exists public.login_attempts (
  id          bigserial primary key,
  ip          text,
  ok          boolean not null default false,
  at          timestamptz not null default now()
);
create index if not exists login_attempts_ip_at on public.login_attempts (ip, at);

-- ---------- code normalisation ("ab12-cd34" and "AB12CD34" are the same) ----
create or replace function public.lia_norm(t text) returns text
language sql immutable as $$
  select upper(regexp_replace(coalesce(t, ''), '[^A-Za-z0-9]', '', 'g'))
$$;

create or replace function public.students_norm_code() returns trigger
language plpgsql as $$
begin
  new.code := public.lia_norm(new.code);
  if length(new.code) < 4 then
    raise exception 'The access code needs at least 4 letters or numbers';
  end if;
  return new;
end $$;

drop trigger if exists students_norm on public.students;
create trigger students_norm
  before insert or update of code on public.students
  for each row execute function public.students_norm_code();

-- ---------- row level security --------------------------------------
alter table public.students       enable row level security;
alter table public.progress       enable row level security;
alter table public.admins         enable row level security;
alter table public.login_attempts enable row level security;   -- no policies = nobody but the functions below

create or replace function public.lia_is_admin() returns boolean
language sql security definer stable set search_path = public as $$
  select exists (select 1 from public.admins where user_id = auth.uid())
$$;

drop policy if exists "admins manage students" on public.students;
create policy "admins manage students" on public.students
  for all to authenticated
  using (public.lia_is_admin()) with check (public.lia_is_admin());

drop policy if exists "admins manage progress" on public.progress;
create policy "admins manage progress" on public.progress
  for all to authenticated
  using (public.lia_is_admin()) with check (public.lia_is_admin());

drop policy if exists "admins see themselves" on public.admins;
create policy "admins see themselves" on public.admins
  for select to authenticated using (user_id = auth.uid());

-- the public key gets no direct table access at all
revoke all on public.students, public.progress, public.admins, public.login_attempts from anon;
revoke all on public.admins, public.login_attempts from authenticated;
grant select, insert, update, delete on public.students, public.progress to authenticated;
grant select on public.admins to authenticated;

-- ---------- functions the student pages call -------------------------
-- (older versions of these functions had no area argument: drop them first)
drop function if exists public.lia_login(text);
drop function if exists public.lia_get_progress(text, text);
drop function if exists public.lia_save_progress(text, text, jsonb, integer, integer, integer);

-- 1) sign in with a code
create or replace function public.lia_login(p_area text, p_code text) returns json
language plpgsql security definer set search_path = public as $$
declare
  v_code text := public.lia_norm(p_code);
  v_ip   text;
  v_fail integer;
  s      public.students%rowtype;
begin
  v_ip := coalesce(split_part(coalesce(
            nullif(current_setting('request.headers', true), '')::json ->> 'x-forwarded-for', ''), ',', 1), '');
  -- throttle: 40 wrong codes from one address in 10 minutes (a school shares one address)
  select count(*) into v_fail from public.login_attempts
   where ip = v_ip and ok = false and at > now() - interval '10 minutes';
  if v_fail >= 40 then
    return json_build_object('ok', false, 'error', 'too_many');
  end if;

  select * into s from public.students where area = p_area and code = v_code and active;
  if not found then
    insert into public.login_attempts (ip, ok) values (v_ip, false);
    delete from public.login_attempts where at < now() - interval '1 day';
    return json_build_object('ok', false, 'error', 'invalid_code');
  end if;

  update public.students set last_login = now() where id = s.id;
  return json_build_object('ok', true, 'name', s.full_name, 'grade', s.grade, 'class_name', s.class_name);
end $$;

-- 2) read a student's saved progress for one page
create or replace function public.lia_get_progress(p_area text, p_code text, p_page text) returns json
language plpgsql security definer set search_path = public as $$
declare
  s public.students%rowtype;
  r public.progress%rowtype;
begin
  select * into s from public.students where area = p_area and code = public.lia_norm(p_code) and active;
  if not found then
    return json_build_object('ok', false, 'error', 'invalid_code');
  end if;
  select * into r from public.progress where student_id = s.id and page_key = p_page;
  if not found then
    return json_build_object('ok', true, 'state', '{}'::json, 'updated_at', null);
  end if;
  return json_build_object('ok', true, 'state', r.state, 'updated_at', r.updated_at);
end $$;

-- 3) save a student's progress for one page
create or replace function public.lia_save_progress(
  p_area text, p_code text, p_page text, p_state jsonb,
  p_solved integer default 0, p_total integer default 0, p_examples integer default 0
) returns json
language plpgsql security definer set search_path = public as $$
declare
  s public.students%rowtype;
begin
  select * into s from public.students where area = p_area and code = public.lia_norm(p_code) and active;
  if not found then
    return json_build_object('ok', false, 'error', 'invalid_code');
  end if;
  if p_page is null or p_page !~ '^[a-z0-9-]{1,80}$' then
    return json_build_object('ok', false, 'error', 'bad_page');
  end if;
  if p_state is null or jsonb_typeof(p_state) <> 'object' or octet_length(p_state::text) > 400000 then
    return json_build_object('ok', false, 'error', 'bad_state');
  end if;
  insert into public.progress (student_id, area, page_key, state, solved, total, examples, updated_at)
  values (s.id, s.area, p_page, p_state, greatest(coalesce(p_solved, 0), 0), greatest(coalesce(p_total, 0), 0),
          greatest(coalesce(p_examples, 0), 0), now())
  on conflict (student_id, page_key) do update
     set state = excluded.state, solved = excluded.solved, total = excluded.total,
         examples = excluded.examples, updated_at = now();
  return json_build_object('ok', true, 'updated_at', now());
end $$;

revoke all on function public.lia_login(text, text)                                   from public;
revoke all on function public.lia_get_progress(text, text, text)                      from public;
revoke all on function public.lia_save_progress(text, text, text, jsonb, integer, integer, integer) from public;
grant execute on function public.lia_login(text, text)                                   to anon, authenticated;
grant execute on function public.lia_get_progress(text, text, text)                      to anon, authenticated;
grant execute on function public.lia_save_progress(text, text, text, jsonb, integer, integer, integer) to anon, authenticated;

-- ---------- make yourself an admin (edit the e-mail, then run) ----------
-- 1. Dashboard → Authentication → Users → Add user (e-mail + password, tick "Auto confirm")
-- 2. Run this line with that e-mail:
--
--   insert into public.admins (user_id) select id from auth.users where email = 'YOUR-EMAIL@school.org'
--   on conflict do nothing;
