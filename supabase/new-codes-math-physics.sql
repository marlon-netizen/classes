-- New random codes for every student in the Math and Physics folders. Saved progress, names, classes and assignments are kept.
-- A student who is in both folders gets the SAME new code in both. The teacher master code is not changed.
do $$
declare
  r     record;
  c     text;
  alpha constant text := 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';   -- no 0/O/1/I/L to avoid mix-ups
  i     int;
begin
  for r in select distinct code as old_code from public.students where area in ('math', 'physics') and not is_preview loop
    loop
      c := '';
      for i in 1..8 loop
        c := c || substr(alpha, 1 + (('x' || substr(replace(gen_random_uuid()::text, '-', ''), 1, 2))::bit(8)::int % length(alpha)), 1);
      end loop;
      continue when exists (select 1 from public.students where area in ('math', 'physics') and code = c);   -- already used: try again
      update public.students set code = c where area in ('math', 'physics') and code = r.old_code and not is_preview;
      exit;
    end loop;
  end loop;
end $$;

-- The codes, grouped by folder and class (export this result as CSV, or use Print code slips on the teacher pages)
select area as folder, class_name, grade, full_name, code, notes
from public.students
where area in ('math', 'physics') and not is_preview
order by area, class_name, grade, full_name;
