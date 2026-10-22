-- Split the old "math-physics" area into two areas: "math" and "physics".
-- Run it ONCE in the Supabase SQL Editor (it is safe to repeat). Existing codes keep working: a student keeps the SAME code
-- in each new folder they belong to. Nothing is deleted - the old "math-physics" rows stay until you run the optional clean-up at the end.
--   physics = any class whose name starts with "Physics" (Physics I, Physics II); progress on pages physics1-* / physics2-*
--   math    = every other class (Advanced Algebra, AP Statistics, Pre-Calculus ...) and everything else
-- A student listed in both (e.g. "Physics II / Pre-Calculus") gets one row in each new area, with only that area's subjects.

-- 1) students
insert into public.students (area, code, full_name, grade, class_name, email, notes, active, is_preview, created_at, last_login)
select 'physics', o.code, o.full_name, o.grade,
       coalesce((select string_agg(btrim(t), ' / ') from unnest(string_to_array(coalesce(o.class_name, ''), '/')) t where lower(btrim(t)) like 'physics%'), ''),
       o.email, o.notes, o.active, o.is_preview, o.created_at, o.last_login
from public.students o
where o.area = 'math-physics'
  and (o.is_preview or exists (select 1 from unnest(string_to_array(coalesce(o.class_name, ''), '/')) t where lower(btrim(t)) like 'physics%'))
on conflict (area, code) do nothing;

insert into public.students (area, code, full_name, grade, class_name, email, notes, active, is_preview, created_at, last_login)
select 'math', o.code, o.full_name, o.grade,
       coalesce((select string_agg(btrim(t), ' / ') from unnest(string_to_array(coalesce(o.class_name, ''), '/')) t where lower(btrim(t)) not like 'physics%' and btrim(t) <> ''), ''),
       o.email, o.notes, o.active, o.is_preview, o.created_at, o.last_login
from public.students o
where o.area = 'math-physics'
  and (o.is_preview
       or btrim(coalesce(o.class_name, '')) = ''
       or exists (select 1 from unnest(string_to_array(coalesce(o.class_name, ''), '/')) t where lower(btrim(t)) not like 'physics%' and btrim(t) <> ''))
on conflict (area, code) do nothing;

-- 2) saved progress (physics pages go to "physics", the rest to "math")
insert into public.progress (student_id, area, page_key, state, solved, total, examples, score, max_score, updated_at)
select n.id, n.area, p.page_key, p.state, p.solved, p.total, p.examples, p.score, p.max_score, p.updated_at
from public.progress p
join public.students o on o.id = p.student_id and o.area = 'math-physics'
join public.students n on n.code = o.code and n.area = case when p.page_key like 'physics%' then 'physics' else 'math' end
on conflict (student_id, page_key) do nothing;

-- 3) lesson assignments (Assign lessons)
insert into public.lesson_access (area, page_key, grade, class_name)
select case when page_key like 'physics%' then 'physics' else 'math' end, page_key, grade, class_name
from public.lesson_access
where area = 'math-physics'
on conflict do nothing;

-- check: students per area and codes shared with the old area
select area, count(*) as students, count(*) filter (where is_preview) as preview_codes from public.students group by area order by area;

-- 4) OPTIONAL clean-up, only after the new site is live and you have checked the numbers above:
-- delete from public.progress      where area = 'math-physics';
-- delete from public.lesson_access where area = 'math-physics';
-- delete from public.students      where area = 'math-physics';
