#!/bin/bash
# Starts (or reuses) a throw-away local Postgres 16 on port 54329 in $LIA_PGDIR (default /tmp/lia-pg) and loads supabase/schema.sql.
# Needs the postgresql-16 package. Then:  node tools/test/mock.js &   and   node tools/test/e2e_access.js
D=${LIA_PGDIR:-/tmp/lia-pg}; PGBIN=/usr/lib/postgresql/16/bin
mkdir -p "$D" && chmod 777 "$D"
if [ ! -d "$D/data" ]; then su postgres -c "$PGBIN/initdb -D $D/data -U postgres -A trust" >/dev/null; fi
if ! pg_isready -h "$D" -p 54329 >/dev/null 2>&1; then su postgres -c "$PGBIN/pg_ctl -D $D/data -o '-p 54329 -k $D' -l $D/log -w start" >/dev/null; fi
psql -h "$D" -p 54329 -U postgres -q -c "do \$\$ begin create role anon nologin; exception when duplicate_object then null; end \$\$; do \$\$ begin create role authenticated nologin; exception when duplicate_object then null; end \$\$; create schema if not exists auth; create table if not exists auth.users(id uuid primary key default gen_random_uuid(), email text); create or replace function auth.uid() returns uuid language sql as 'select null::uuid';" 
psql -h "$D" -p 54329 -U postgres -q -v ON_ERROR_STOP=1 -f "$(dirname "$0")/../../supabase/schema.sql" 2>&1 | grep -v NOTICE
pg_isready -h "$D" -p 54329
