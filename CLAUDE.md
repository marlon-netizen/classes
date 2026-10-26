# Lincoln International Academy – class website (read this before adding or changing anything)

Static HTML site (GitHub Pages) for teacher Eduardo Vásquez and colleagues, with a Supabase backend for **student access codes,
saved progress, scores and teacher tools**. Every new page or feature must follow the rules below so all pages behave the same.
Setup/usage for humans: `supabase/README.md`. This file is the engineering contract.

## 1. Layout (and what is generated – never hand-edit generated files)
```
index.html                 GENERATED – teacher home (sign-in gate, links to share, master preview code). There is NO public student index.
faith-formation/  ciencias-sociales/  math/  physics/
    <lesson>.html          one self-contained page each (YOU write these)
    lia-config.js          GENERATED per folder: Supabase url + anon key, area, areaName, pages{slug: label}
teacher/                   GENERATED from shared/*.template.html: admin.html (students & codes), scores.html, access.html (assign lessons), responses.html (students' saved text answers); index.html only redirects to /
shared/lia-sync.js         the ONE module every lesson page loads (sign-in, saving, restore, access control, theme toggle)
shared/*.template.html     sources of the teacher pages – edit these, then run the build
supabase/schema.sql        the whole database; idempotent (safe to re-run); keep it that way
tools/make_icons.js        renders favicon.png fallbacks from each favicon.svg (after changing icons)
tools/build_site.py        run after adding/moving/renaming a page or editing a template/theme: python3 tools/build_site.py
tools/test/                local test harness (Postgres + Supabase mock + Playwright) – see §8
```
Students receive **direct links only** (`<base>/<folder>/<lesson>.html`). Never add a student menu/index, a link to teacher pages, or
links between lessons that a student might not be assigned.

## 2. Adding a new lesson page (checklist)
1. One self-contained `.html` file (inline CSS/JS, no build step) in the correct folder. File name = page key (`physics1-lesson-2-4.html` → `physics1-lesson-2-4`;
   lower-case letters, digits, hyphens). To override, set `<meta name="lia-page" content="slug">`.
   **Name by class, then lesson:** Physics I pages are `physics1-lesson-<chapter>-<section>-<topic>.html` (Chapters 1–2 belong to Physics I) and Physics II pages are
   `physics2-lesson-<chapter>-<section>.html` (Chapters 9, 10 and 11 belong to Physics II). The class named in the `<title>`, the header "Class" box and the footer must match the file name prefix.
   Renaming a page changes its key: also migrate `progress.page_key` and `lesson_access.page_key` in the database (see `supabase/README.md`).
2. `<title>` = `Short lesson name | Lincoln International Academy` (the part before ` | ` becomes the label in every teacher table).
3. Header (every page): school name **Lincoln International Academy**, class, teacher name, lesson title. Sober palette; **each folder has its own look**
   (colours/font – see `THEMES` in `tools/build_site.py`); pages inside a folder may vary but must not borrow another folder's look.
4. Content pattern: review → step-by-step worked examples → practice with immediate feedback. Responsive; print-friendly; accessible (labels, focus, contrast).
5. **Dark mode:** colours as CSS variables on `:root`, dark variant in `@media (prefers-color-scheme: dark)` **and** `:root[data-theme="dark"]` (use
   `:root:not([data-theme="light"])` inside the media query). If the CSS mentions `data-theme`, `lia-sync.js` injects the Light/Dark toggle automatically;
   if the page has its own toggle (`#themeBtn`, `[data-theme-set]`, …) it is left alone. Theme choice key: `localStorage['lia-theme']`.
6. **Progress** (see §3) – keep all student state in `localStorage`; report completion/score.
7. **Browser-tab icon:** every page gets its folder's icon automatically (`<folder>/favicon.svg` + `favicon.png`, linked from the loader block). Never add your own `<link rel="icon">`. To change an icon edit `ICON_GLYPHS`/`ICON_BG` in `tools/build_site.py`, run the build, then `node tools/make_icons.js` to refresh the PNG fallbacks. A new folder needs an entry in both tables.
8. Run `python3 tools/build_site.py` (adds the loader block to `<head>`, regenerates `lia-config.js` pages map and the root/teacher pages), run the tests, commit.
   The block between `<!--LIA-SYNC-START-->` and `<!--LIA-SYNC-END-->` is owned by the build script – leave it.

## 3. Progress-saving contract (what every page must do)
* **Mirror mode:** `lia-sync.js` wraps `Storage.prototype.setItem/removeItem`; every non-`lia-*` localStorage key the page writes is mirrored to
  `progress.state` (jsonb) shortly after each change and restored on sign-in (page reloads once) – on any device. Offline: kept on the device and retried.
  So a page only has to **persist its state in localStorage** (JSON strings are fine). Do not use cookies, sessionStorage or IndexedDB for student work.
* **Never prompt for a name.** Use `window.LiaSync && LiaSync.name()` (registered name from the sign-in) wherever a name is printed/submitted; show it read-only.
* **No student self-reset.** Do not offer "clear my scores/progress" in a live page. Mark such controls `data-lia-reset` (or id `resetAll`) – they are hidden when
  signed in (`.lia-live [data-lia-reset]{display:none}`). Handlers must stay null-safe. Only the teacher resets (admin page → Details).
* **Report completion + score** so the teacher dashboard works: call
  `LiaSync.report({solved, total, score, max})` whenever the totals change (guard: `window.LiaSync&&LiaSync.report&&…`).
  `solved/total` = activities completed / activities available (progress %); `score/max` = points (score %). Pages that restart on every visit
  (no persisted state) pass `{keepBest:true}` as 2nd argument so the best result is kept. Pages that show `N of M …` in `#overallText` are picked up automatically.
  Reading-only pages may report nothing (they show as "saved").
* Reserved localStorage keys (never written by a page, never saved as student work): `lia-code`, `lia-name`, `lia-mirror`, `lia-reloaded`, `lia-theme`, `lia-admin-session`, `lia-access` (each suffixed with the area/page where relevant).
  Any other key – including page-owned ones such as `lia-physics2-…` – is saved. Don't invent new reserved names without adding them to `trackable()` in `shared/lia-sync.js`.
* **Free-text answers the teacher should be able to read** (exit tickets, reflections): save each set in `localStorage` under a key that starts with `resp-`
  as JSON `{"title":"Week 3: … – Exit ticket","q":["question",…],"a":["answer",…]}` (answers in the same order as the questions). The mirror saves it automatically and
  `teacher/responses.html` lists it per student and lesson (questions included, CSV export). Autosave on `input`/`blur`; restore on load.
* The page must still work if `LiaSync` is absent (no config / offline file preview): everything optional-chained.
* The signed-in badge (`#liaUser`), the sign-in gate (`#liaGate`) and the "not available for your class" card are drawn by the module – don't restyle or duplicate them.

## 4. Sign-in, codes and areas
* Four **areas** = folders: `faith-formation`, `ciencias-sociales`, `math` (Algebra, AP Statistics, Pre-Calculus…) and `physics` (all `physics1-` / `physics2-` pages) (`CFG.area`). One student list + codes per area; **same code works on every page of that folder**,
  different folders = different students. Codes: upper-case letters/digits, ≥4 (shown `XXXX-XXXX`), unique per area, generated 8 chars from an unambiguous alphabet (no 0/O/1/I/L). Never use student IDs as codes.
* Student fields: `grade` = the number only (`10`), `class_name` = the **subject** (`Physics II`). A student in several subjects lists them separated by ` / ` (`Physics II / Pre-Calculus`). Section ("10 A") and school ID go in `notes`.
* The anon/publishable key in `lia-config.js` is public by design; all student access goes through three SECURITY DEFINER functions
  (`lia_login`, `lia_get_progress`, `lia_save_progress`) – tables are closed by RLS; teachers use Supabase Auth + the `admins` table (`lia_is_admin()`). Wrong codes are throttled per IP.
* **Teacher preview/master code:** a `students` row with `is_preview=true` (one per area, same code). It opens every lesson regardless of assignment and is excluded from
  dashboards, assignment matrix and code slips (`is_preview=eq.false` in the templates). Any new teacher report must also exclude `is_preview`.

## 5. Who sees which lesson (assignment)
* Table `lesson_access(area, page_key, grade, class_name)`; **no rows for a lesson = everyone in the folder sees it**; once any row exists only matching grade + class (case/space-insensitive,
  any one of the student's ` / ` subjects) may open it. Sentinel row `grade='~', class_name='~'` marks "restricted to nobody yet" – never show it in UI.
* Enforced three ways: `lia_login` returns `access:{restricted,allowed}` (cached in `lia-access:<area>` for offline), the module blocks the page, and `lia_get_progress` / `lia_save_progress`
  refuse (`not_allowed`). A new page therefore needs nothing extra; the teacher assigns it in `teacher/access.html`.

## 6. Teacher side
* Everything teacher-facing is behind Supabase Auth: the root home, `admin`, `scores`, `access`. They share one session (`localStorage['lia-admin-session:<url>']`) and one subject
  switcher (`?area=`). Never expose student data or codes without that session. Keep them `noindex`.
* Edit `shared/*.template.html` / `teacher_home()` in `build_site.py`, then rebuild. All teacher pages: same header (`.who` nav + ☀/☾ toggle), same palette variables, dark mode via `data-theme`.
* Scores dashboard uses `progress.solved/total/score/max_score/updated_at` per student × page; attention flags = 7+ days idle, never started, score < 60 %.
* The **Student responses** page (`shared/responses.template.html`) reads `progress.state` keys starting with `resp-`; it excludes `is_preview` students like every report.
* New teacher feature → add it to all of: teacher home buttons (in `build_site.py`), the header nav in the three templates, and `supabase/README.md`.

## 7. Database changes
* Edit `supabase/schema.sql` only in an idempotent way (`create … if not exists`, `add column if not exists`, `create or replace`, `drop policy if exists`). Re-running must never delete data.
* Anything new that a student page needs goes through a SECURITY DEFINER function with `search_path = public`, revoked from `public`, granted to `anon, authenticated`.
  Tables stay closed to `anon`; admin tables get an `lia_is_admin()` RLS policy.
* The teacher must re-run the schema in the Supabase SQL Editor after changes – say so in your final message. Provide one-paste SQL when asked (setup + reset script pattern: structure first, then data).
* **Personal data never goes in the repo** (rosters, codes, master code, SQL with names). The repo/site is public. Keep such files outside it and hand them to the user as files.

## 8. Testing (do this before pushing – there is no CI)
`tools/test/`: `pg.sh` (local Postgres 16 with `schema.sql`), `mock.js` (Supabase stand-in on :54400 that runs the REAL SQL), Playwright e2e (`e2e_access.js`, `e2e_final.js`).
Playwright redirects the Supabase host to the mock (`context.route`), Chromium is at `/opt/pw-browsers/chromium`. Pattern: `bash tools/test/pg.sh; node tools/test/mock.js & node tools/test/e2e_final.js`.
Check at least: sign-in gate on a new page, restore from the DB on a second browser context, wrong/blocked lessons, no page errors, dark mode, `node --check` on inline scripts. The sandbox cannot reach the real Supabase – say that
you could not verify against production.

## 9. Git / delivery
Develop on the branch the session names; commit with clear messages; push; do not open a PR unless asked. `main` is what GitHub Pages serves, so new work is only live after the branch is merged.
Run `python3 tools/build_site.py` before committing (generated files must be in sync). Give the user the **full direct link** for any new lesson
(`https://marlon-netizen.github.io/classes/<folder>/<file>.html`; folder = `math`, `physics`, `ciencias-sociales` or `faith-formation`) and tell them what to run in Supabase, if anything.
