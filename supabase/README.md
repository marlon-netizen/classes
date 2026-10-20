# Student codes & saved progress (Supabase)

The site has three folders ("areas"). Each folder has its **own list of students and codes**.
A student types their code **once per folder**; the same code then works on **every page** of that folder.
Everything the student does on a page (answers, scores, names, drafts) is **saved to the database a moment
after each change** and **restored automatically the next time they sign in – on any device**.

```
index.html                     front page for students → choose a subject
faith-formation/               Faith Formation + Growing in Values   (lia-config.js, index.html, lessons…)
ciencias-sociales/             Ciencias Sociales
math-physics/                  all Math & Physics classes
teacher/                       ALL teacher tools – not linked from any student page
  index.html                     teacher home (one button per subject)
  scores.html                    scores & progress dashboard
  access.html                    assign lessons to each grade + class
  admin.html                     students & access codes
shared/lia-sync.js             sign-in + saving module loaded by every lesson page
shared/*.template.html         sources of the two teacher pages
supabase/schema.sql            the database (run once per Supabase project)
tools/build_site.py            connects pages, rebuilds menus and admin pages
```

## One-time setup (about 10 minutes)

### 1. Create the database
1. Go to <https://supabase.com> → **New project**. (One project can serve all three folders – the `area` column keeps them
   apart. If you prefer a separate database per folder, create one project per folder and use steps 2–4 for each.)
2. **SQL Editor → New query**, paste the whole of `supabase/schema.sql`, press **Run**.
3. **Authentication → Users → Add user**: your e-mail + a password, tick *Auto confirm*. This is the teacher account.
4. In the SQL Editor run (with your e-mail) so that account becomes an administrator:
   ```sql
   insert into public.admins (user_id) select id from auth.users where email = 'YOUR-EMAIL@school.org' on conflict do nothing;
   ```

### 2. Connect the site to it
In Supabase: **Project Settings → API** → copy the **Project URL** and the **anon / publishable key** (it is meant to be public;
the database only lets students reach their own saved work through their code).

Either edit the three files `faith-formation/lia-config.js`, `ciencias-sociales/lia-config.js`, `math-physics/lia-config.js`
(`url:` and `anonKey:`), or run once:
```bash
python3 tools/build_site.py --url https://YOURPROJECT.supabase.co --key YOUR_ANON_KEY
# separate project for one folder:
python3 tools/build_site.py --area math-physics --url https://OTHER.supabase.co --key OTHER_KEY
```
Commit and publish the site as usual. Until a folder's `lia-config.js` is filled in, its pages simply keep working
without sign-in (progress stays in the student's browser).

### 3. Add your students
Open `<your site>/teacher/` (the teacher home – bookmark it; students never see a link to it), choose a subject and **Students & codes**, and sign in with the teacher account. One login works for every teacher page; the subject switcher in the page header changes between Faith Formation, Ciencias Sociales and Math & Physics.
* **+ Add student** – name, grade, class, e-mail, notes and a code (use *Generate*, or type your own: 4+ letters/numbers).
* **Bulk add** – paste one student per line: `Name, Grade, Class, E-mail, Notes, Code` (only the name is required; empty code = generated).
* **Print code slips** – one cut-out slip per active student, ready to hand out.
* **Export CSV** – names, codes and progress per page.
* **Details** – see each student's saved progress per page and reset it; **Edit** – change a code, deactivate or delete a student.

Codes are not case-sensitive and ignore dashes/spaces (`k7m2-qx9p` = `K7M2QX9P`). The same code may exist in two
different folders – they are different students. A deactivated student can no longer sign in.

## Seeing scores and progress (teacher dashboard)
Open `<your site>/teacher/` → **Scores & progress** for a subject (same teacher account).
* A grid of **students × lesson pages** with colour-coded **score %** or **progress %** (switch with Score / Progress / Both).
* **Class average** under every page title; **Overall score / progress** per student; last activity.
* **Needs attention** flags: no activity for 7+ days, never started, or score under 60 %.
* Sort by any column, filter by class, search, click a student for per-page details, **Export CSV**, **Print**.
* Pages that don't score (e.g. reading-only slides) show "saved"; pages that restart each visit (the three algebra/language
  practice pages and Rules on Wheels) show the student's **best** result.

**Updating an existing database:** when a new version of `supabase/schema.sql` is published, paste and run it again – it is safe to re-run and keeps all data.

## Showing each class only its lessons (Assign lessons)
Open `<your site>/teacher/` → **Assign lessons** for a subject. Rows are every **grade + class** found in your student list (exactly as typed in
*Students & codes*); columns are the lessons. A lesson is shown to **everyone** until you un-tick a box; after that only the ticked rows see it
(**show to everyone** undoes it; **all / none** fill a row). Students see only their lessons in the folder menu, and a lesson that isn't theirs
shows "Not available for your class" even from a direct link – the database refuses to save or load it as well.
Re-run `supabase/schema.sql` once to enable this. Each folder also has its own look (colours and font); only the database and sign-in code are shared.

## How the student experience works
1. Opening any lesson page shows a **Student sign-in** box (once per folder, per device).
2. After signing in, the page restores the student's saved work from the database.
3. Every answer is saved automatically (the small badge at the bottom-right shows **Saving… / Saved ✓**). Offline? Work is kept
   on the device and uploaded as soon as the connection returns.
4. **Sign out** (same badge) removes the student's data from that computer – so the next student on a shared computer starts clean.
5. The name on scores and results comes from the sign-in – students are never asked to type it again – and students cannot reset
   their own scores (the teacher can, from the admin page). Every page has the same ☰ Menu link and a light/dark switch.

## Adding new pages
Drop the `.html` file in the right folder and run `python3 tools/build_site.py`. It adds the sign-in/saving scripts to the page,
updates that folder's menu and the teacher pages' labels. Any page that keeps its state in `localStorage` is saved automatically.
Pages that show `N of M … solved` in an element with `id="overallText"` also show completion in the admin table.

## Security notes
* Students can only call three database functions (`lia_login`, `lia_get_progress`, `lia_save_progress`); each needs the area and a valid, active code.
  Tables are closed to the public key (Row Level Security). Only administrator accounts can read or edit students.
* Wrong codes are throttled (40 per 10 minutes per network address). Generated codes have 8 random characters; use long codes if you choose your own.
* Codes are stored in readable form so you can print them again; keep the admin account password private.
